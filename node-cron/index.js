const { Client } = require("pg");
const cron = require("node-cron");
require("dotenv").config({ path: "../.env" });

console.log("code run");

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
  console.log(`current score: ${currentScore}`);

  const decayFactor = calculateDecayFactor(venue.updated_at);
  const noveltyBonus = calculateNoveltyBonus(index);

  const newScore = currentScore * decayFactor + noveltyBonus;
  console.log(`new score: ${newScore}`);

  return parseFloat(newScore.toFixed(2));
}

//     {
//   id: '679add7a-fa15-496d-a2b1-b917a432fc3e',
//   name: 'Mohit Moitra Mancha',
//   lat: 22.612299,
//   lon: 88.382918,
//   address: '34/1, 13/1/2, Raja Manindra Rd, Jora Mandir, Gangulipara, Paikpara, Kolkata, West Bengal 700059',
//   city: 'Kolkata',
//   zone: 'CCU-N',
//   search_score: 100,
//   created_at: 2024-10-06T01:12:19.581Z,
//   updated_at: 2024-10-06T01:17:08.031Z,
//   nearest_transport_distance: 0.8027723109124077,
//   transport_id: 'cdd76e65-62a3-4f68-9cca-6278a6eeeafe'
// }
async function update_scores() {
  const client = new Client({
    user: process.env.DJANGO_DB_USER,
    host: process.env.DJANGO_DB_HOST,
    database: process.env.DJANGO_DB_NAME,
    password: process.env.DJANGO_DB_PASSWORD,
    port: process.env.DJANGO_DB_PORT,
  });

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
  let index = 0;
  let updated_pujos = [];
  let same_score_pujos = {};
  if (pujos.rows.length === 0) {
    console.log("No pujos found for score update - lastscoremodel");
  } else {
    for (const pujo of pujos.rows) {
      // console.log(pujo);
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
}

// Schedule cron job to run every 6 hours  ==> 0 */6 * * *
// schedule cron job every 30 mins => */30 * * * *
// schedule a cron at start of every hour => 0 * * * *
cron.schedule("0 * * * *", async () => {
  console.log("This cron job will running every hour");
  console.log(`started at ${new Date()} - lastscoremodel`);
  // PostgreSQL credentials
  try {
    await update_scores();
  } catch (error) {
    console.error("Error running update_pujo_scores:", error);
    //   await client.query("ROLLBACK");
  } finally {
    client.end();
  }
});

function calculateMean(values) {
  console.log("calculating mean");
  const sum = values.reduce((acc, val) => acc + val, 0);
  return sum / values.length;
}

function calculateStandardDeviation(values, mean) {
  console.log("calculating std deviance");
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

  await client.connect(); // Open a new client for transaction
  console.log("connected to database");

  const currentDateTime = new Date();
  //get all pujos
  // Fetch Pujo objects not updated in the last X hours
  const pujoQuery = `
            SELECT * FROM pujo_pujo
        `;
  const pujos = await client.query(pujoQuery);
  console.log(`Fetched ${pujos.rows.length} pujos`);

  if (pujos.rows.length > 0) {
    //zscorenormalization
    const searchScores = pujos.rows.map((row) => row.search_score);
    const mean = calculateMean(searchScores);
    console.log(`mean is ${mean}`);
    const stdDev = calculateStandardDeviation(searchScores, mean);
    console.log(`std dev is ${stdDev}`);

    for (const pujo of pujos.rows) {
      // (score - mean) / stdDev
      console.log(`current score is ${pujo.search_score}`);

      const normalizedScore =
        (pujo.search_score - mean) / (stdDev > 0 ? stdDev : 1);

      console.log(
        `normalized score: ${normalizedScore} for pujo id: ${pujo.id}`
      );
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

      console.log(
        `Updated pujo: ${pujo.id}, new search_score: ${newSearchScore} - normalize score`
      );

      //check if it actually went through
      await client.query("COMMIT");

      console.log(`Finished at ${new Date()} - normalize score`);
    }
  }
}

// Schedule a cron job to run every day at 12:10 AM IST ==> 40 6 * * *
cron.schedule("50 6 * * *", async () => {
  console.log("This cron job will run every day at 12:10 AM");
  console.log(`started at ${new Date()} - normalize score`);
  try {
    await normalize_scores();
  } catch (e) {
    console.error("Error normalizing scores:", e);
  } finally {
    client.end();
  }
});
