const { Client } = require("pg");
const cron = require("node-cron");
require("dotenv").config({ path: "../.env" });
// const Minio = require("minio");
// const Papa = require("papaparse");
const express = require("express"); // Import Express
const app = express(); // Create an Express application
const PORT = 4000; // Set the port for the Express server
let cron_logs = [];
console.log("code run");
let job_in_progress = false;

function AddToCronLogs(message) {
  cron_logs.push({
    id: null,
    level: "INFO",
    message,
    module: "CRON JOBS",
    user_id: null,
    created_at: new Date(),
  });
}

/*
updated_at needs to be in this format => 2024-10-06 11:06:44.456247+00
tau is in seconds
significance of tau: tau controls the rate at which the score decays over time
default to 1800 ==> 30 mins / this means that the score will decrease by approx 63% every 30 minutes
Purpose: To reduce the score of a venue over time
Why: To prioritize recent interactions over older ones
How: The score decreases exponentially as time passes
*/
function calculateDecayFactor(updatedTime, tau = 1800) {
  if (updatedTime === null) {
    return 1;
  } else {
    // Ensure updatedTime is in the correct format
    if (typeof updatedTime === "string") {
      updatedTime = updatedTime.replace(" ", "T");
      updatedTime = new Date(updatedTime);
    }

    const now = new Date();
    const t = (now.getTime() - updatedTime.getTime()) / 1000;
    return parseFloat(Math.exp(-t / tau).toFixed(2));
  }
}

/*
Purpose: To Promote less popular venue
Why: To prevent dominant venues from always ranking first
How: Add a bonus to venue with lower ranks
Alpha => higher alpha will strongly promote less popular venues
*/
function calculateNoveltyBonus(index, alpha = 0.5) {
  return parseFloat((alpha * (index - 1)).toFixed(2));
}

//We are using time decay algorithm to reduce venue scores exponentially over time to prioritize recent interactions
function getScore(venue, index) {
  // Decay factor and novelty bonus calculation
  const currentScore = venue.search_score;
  const decayFactor = calculateDecayFactor(venue.updated_at);
  const noveltyBonus = calculateNoveltyBonus(index);
  const newScore = currentScore * decayFactor + noveltyBonus;

  return parseFloat(newScore.toFixed(2));
}

async function update_scores() {
  const client = new Client({
    user: process.env.DJANGO_DB_USER,
    host: process.env.DJANGO_DB_HOST,
    database: process.env.DJANGO_DB_NAME,
    password: process.env.DJANGO_DB_PASSWORD,
    port: process.env.DJANGO_DB_PORT,
  });
  try {
    await client.connect(); // Open a new client for transaction
    // Start a transaction
    await client.query("BEGIN");

    // Fetch Pujo objects not updated in the last X hours
    const pujoQuery = `
            SELECT * FROM pujo_pujo
            ORDER BY "search_score" DESC
            LIMIT 10;
        `;
    const pujos = await client.query(pujoQuery);
    AddToCronLogs(`fetched ${pujos.rows.length} pujos - lastscoremodel`);
    let index = 0;
    let updated_pujos = [];
    let same_score_pujos = {};
    if (pujos.rows.length === 0) {
      AddToCronLogs("No pujos found for score update - lastscoremodel");
    } else {
      for (const pujo of pujos.rows) {
        const newScore = getScore(pujo, index);
        pujo.search_score = Math.max(newScore, 0);
        updated_pujos.push(pujo);

        updated_pujos.forEach((pujo) => {
          const score = pujo.search_score;

          if (!same_score_pujos[score]) {
            same_score_pujos[score] = []; // Initialize the array if it doesn't exist
          }

          same_score_pujos[score].push(pujo); // Add the pujo to the corresponding score array
        });

        for (const [score, pujos] of Object.entries(same_score_pujos)) {
          if (pujos.length > 1) {
            // More than one pujo with the same score
            const mostRecentPujo = pujos.sort((a, b) => {
              const updatedAtA = a.updated_at
                ? new Date(a.updated_at)
                : new Date(0); // Fallback to Jan 1, 1970
              const updatedAtB = b.updated_at
                ? new Date(b.updated_at)
                : new Date(0); // Fallback to Jan 1, 1970
              return updatedAtB - updatedAtA; // Sort in descending order
            })[0]; // Get the most recent pujo

            mostRecentPujo.search_score += 1;

            if (!updated_pujos.includes(mostRecentPujo)) {
              updated_pujos.push(mostRecentPujo);
            }
          }
        }
        index++;
      }

      for (const pujo of updated_pujos) {
        const updateQuery = `
            UPDATE pujo_pujo
            SET search_score = $1
            WHERE id = $2;
        `;
        try {
          await client.query(updateQuery, [pujo.search_score, pujo.id]);
        } catch (error) {
          console.error(`Failed to update pujo with id ${pujo.id}:`, error);
        }
      }
    }

    //check if it actually went through
    await client.query("COMMIT");
  } catch (e) {
    console.error(e);
    await client.query("ROLLBACK");
  } finally {
    client.end();
  }
}

function calculateMean(values) {
  AddToCronLogs("calculating mean");
  const sum = values.reduce((acc, val) => acc + val, 0);
  return sum / values.length;
}

function calculateStandardDeviation(values, mean) {
  AddToCronLogs("calculating std deviance");
  const variance =
    values.reduce((acc, val) => acc + Math.pow(val - mean, 2), 0) /
    values.length;
  return Math.sqrt(variance);
}

async function normalize_scores() {
  const client = new Client({
    user: process.env.DJANGO_DB_USER,
    host: process.env.DJANGO_DB_HOST,
    database: process.env.DJANGO_DB_NAME,
    password: process.env.DJANGO_DB_PASSWORD,
    port: process.env.DJANGO_DB_PORT,
  });

  try {
    await client.connect(); // Open a new client for transaction
    AddToCronLogs("connected to database");

    const currentDateTime = new Date();
    //get all pujos
    // Fetch Pujo objects not updated in the last X hours
    const pujoQuery = `
            SELECT * FROM pujo_pujo
        `;
    const pujos = await client.query(pujoQuery);
    AddToCronLogs(`Fetched ${pujos.rows.length} pujos`);

    if (pujos.rows.length > 0) {
      //zscorenormalization
      const searchScores = pujos.rows.map((row) => row.search_score);
      const mean = calculateMean(searchScores);
      AddToCronLogs(`mean is ${mean}`);
      const stdDev = calculateStandardDeviation(searchScores, mean);
      AddToCronLogs(`std dev is ${stdDev}`);

      for (const pujo of pujos.rows) {
        // (score - mean) / stdDev
        const normalizedScore =
          (pujo.search_score - mean) / (stdDev > 0 ? stdDev : 1);

        const newSearchScore = 100 + normalizedScore;
        //reset scores for all pujos => add normalized + 100
        const updatePujoQuery = `
          UPDATE pujo_pujo
          SET search_score = $1, updated_at = $2
          WHERE "id" = $3
          `;

        await client.query(updatePujoQuery, [
          newSearchScore,
          currentDateTime,
          pujo.id,
        ]);

        //check if it actually went through
        await client.query("COMMIT");
      }
    }
  } catch (e) {
    console.error(e);
    await client.query("ROLLBACK");
  } finally {
    client.end();
  }
}

// async function uploadLogsToMinIO() {
//   // Create a MinIO client
//   const minioClient = new Minio.Client({
//     endPoint: process.env.MINIO_URL,
//     port: 9000, // Default MinIO port
//     useSSL: false, // Set to true if using SSL
//     accessKey: process.env.MINIO_ACCESS_KEY,
//     secretKey: process.env.MINIO_SECRET_KEY,
//   });

//   // Create a MySQL connection (adjust for your database)
//   const client = new Client({
//     user: process.env.DJANGO_DB_USER,
//     host: process.env.DJANGO_DB_HOST,
//     database: process.env.DJANGO_DB_NAME,
//     password: process.env.DJANGO_DB_PASSWORD,
//     port: process.env.DJANGO_DB_PORT,
//   });

//   try {
//     await client.connect();
//     console.log("connected to database");
// const currentDateTime = new Date();
// const twentyMinutesAgo = new Date(
//   currentDateTime.getTime() - 20 * 60 * 1000
// );
// const query = `SELECT * FROM systemLogs_systemlogs WHERE created_at >= $1`;
// const logs = await client.query(query, [twentyMinutesAgo]);
//     console.log(`Fetched ${logs.rows.length} logs`);

//     const csv = Papa.unparse(results);

//     const fileName = `logs/logs_${Date.now()}.csv`;

//     await minioClient
//       .putObject(process.env.MINIO_BUCKET_NAME, fileName, csv)
//       .then(async (res) => {
//         console.log(`Upload success`);
//         try {
//           const query = `DELETE FROM systemLogs_systemlogs WHERE created_at >= $1`;
//           await client.query(query, [twentyMinutesAgo]);
//         } catch (e) {
//           client.query("ROLLBACK");
//         }
//       })
//       .catch((e) => {
//         if (err) {
//           console.error(`Error uploading: ${err}`);
//         }
//       });
//     await client.query("COMMIT");
//   } catch (e) {
//     console.error(`Error: ${e}`);
//     client.query("ROLLBACK");
//   } finally {
//     client.end();
//   }
// }

// Schedule cron job to run every 6 hours  ==> 0 */6 * * *
// schedule cron job every 30 mins => */30 * * * *
// schedule a cron at start of every hour => 0 * * * *
cron.schedule("0 * * * *", async () => {
  job_in_progress = true;
  AddToCronLogs("This cron job will run every hour");
  AddToCronLogs(`started at ${new Date()} - lastscoremodel`);
  // PostgreSQL credentials
  try {
    await update_scores();
  } catch (error) {
    AddToCronLogs(`Error running update_pujo_scores: ${error}`);
    //   await client.query("ROLLBACK");
  }
  job_in_progress = false;
});

// Schedule a cron job to run every day at 12:10 AM IST ==> 40 6 * * *
cron.schedule("0 19 * * * ", async () => {
  job_in_progress = true;
  AddToCronLogs("This cron job will run every day at 12:10 AM");
  AddToCronLogs(`started at ${new Date()} - normalize score`);
  try {
    await normalize_scores();
  } catch (e) {
    console.error("Error normalizing scores:", e);
  }
  job_in_progress = false;
});

// API
const ALLOWED_IP = process.env.ALLOWED_IP_NODE;

const restrictAccess = (req, res, next) => {
  const requestIP = req.ip || req.connection.remoteAddress;
  // Check if the request IP matches the allowed IP
  if (requestIP === ALLOWED_IP) {
    return next(); // Allow access
  } else {
    return res.status(403).json({ message: "Access denied" }); // Deny access
  }
};

// Endpoint to say hello
app.get("/log", restrictAccess, async (req, res) => {
  if (!job_in_progress) {
    const client = new Client({
      user: process.env.DJANGO_DB_USER,
      host: process.env.DJANGO_DB_HOST,
      database: process.env.DJANGO_DB_NAME,
      password: process.env.DJANGO_DB_PASSWORD,
      port: process.env.DJANGO_DB_PORT,
    });
    try {
      await client.connect();
      const currentDateTime = new Date();
      const twentyMinutesAgo = new Date(
        currentDateTime.getTime() - 20 * 60 * 1000
      );
      const query = `SELECT * FROM "systemLogs_systemlogs" WHERE created_at >= $1`;
      const logs = await client.query(query, [twentyMinutesAgo]);
      AddToCronLogs(`fetched ${logs.rows.length} logs`);
      // cron_logs.push(logs.rows);
      logs.rows.forEach((log) => cron_logs.push(log));

      res.json({
        message: "success",
        system_logs: cron_logs,
      });

      const deletequery = `DELETE FROM "systemLogs_systemlogs" WHERE created_at >= $1`;
      await client.query(deletequery, [twentyMinutesAgo]);
      cron_logs = [];
    } catch (e) {
      await client.query("ROLLBACK");
      res.json({
        message: e,
        system_logs: [],
      });
    } finally {
      client.end();
      return;
    }
  } else {
    return res.json({
      message: "job in progress",
      system_logs: [],
    });
  }
});

// Start the Express server
app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
