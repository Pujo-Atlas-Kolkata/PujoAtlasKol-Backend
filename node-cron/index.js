const { Client } = require("pg");
const cron = require("node-cron");
require("dotenv").config({ path: "../.env" });

console.log("code run");

// Schedule cron job to run every 6 hours  ==> 0 */6 * * *
// schedule cron job every 30 mins => */30 * * * *
// schedule a cron at start of every hour => 0 * * * *
cron.schedule("0 * * * *", async () => {
  console.log("This cron job will running every 30 minutes");
  console.log(`started at ${new Date()} - lastscoremodel`);
  // PostgreSQL credentials
  const client = new Client({
    user: process.env.DJANGO_DB_USER,
    host: process.env.DJANGO_DB_HOST,
    database: process.env.DJANGO_DB_NAME,
    password: process.env.DJANGO_DB_PASSWORD,
    port: process.env.DJANGO_DB_PORT,
  });

  try {
    await client.connect(); // Open a new client for transaction

    const minutes = 30; //in minutes
    const currentTime = new Date();
    const timeXMinutesAgo = new Date(
      currentTime.getTime() - minutes * 60 * 1000
    );
    const time2XMinutesAgo = new Date(
      currentTime.getTime() - 2 * minutes * 60 * 1000
    );

    // Start a transaction
    await client.query("BEGIN");

    // Fetch Pujo objects not updated in the last X hours
    const pujoQuery = `
            SELECT * FROM pujo_pujo
            WHERE "updated_at" < $1
        `;
    const pujos = await client.query(pujoQuery, [timeXMinutesAgo]);

    if (pujos.rows.length === 0) {
      console.log("No pujos found for score update - lastscoremodel");
    } else {
      for (const pujo of pujos.rows) {
        // Fetch positive LastScoreModel entries for the last 2X hours for this Pujo
        const lastScoresQuery = `
                    SELECT * FROM pujo_lastscoremodel
                    WHERE pujo_id = $1 AND last_updated_at > $2
                `;
        const lastScores = await client.query(lastScoresQuery, [
          pujo.id,
          time2XMinutesAgo,
        ]);

        // Sum all positive scores
        const scoreSum = lastScores.rows.reduce((sum, score) => {
          return score.value > 0 ? sum + score.value : sum;
        }, 0);

        // Update the pujo's search score ensuring it does not go below zero
        const newSearchScore = Math.max(pujo.search_score - scoreSum, 0);
        const updatePujoQuery = `
        UPDATE pujo_pujo
        SET search_score = $1, updated_at = $2
        WHERE "id" = $3
        `;
        await client.query(updatePujoQuery, [
          newSearchScore,
          currentTime,
          pujo.id,
        ]);

        console.log(
          `Updated pujo: ${pujo.id}, new search_score: ${newSearchScore} - lastscoremodel`
        );

        // Delete all previous last scores for this pujo
        const deleteLastScoresQuery = `
                    DELETE FROM pujo_lastscoremodel
                    WHERE pujo_id::uuid = $1
                `;

        const result = await client.query(deleteLastScoresQuery, [
          pujo.id.trim(),
        ]);

        console.log(
          `Deleted ${result.rowCount} rows from pujo_lastscoremodel for pujo_id ${pujo.id} - lastscoremodel`
        );
      }
    }

    //check if it actually went through
    await client.query("COMMIT");

    console.log(`Finished at ${new Date()} - lastscoremodel`);
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

// Schedule a cron job to run every day at 12:10 AM IST ==> 40 6 * * *
cron.schedule("40 6 * * *", async () => {
  console.log("This cron job will run every day at 12:10 AM");
  console.log(`started at ${new Date()} - normalize score`);
  // PostgreSQL credentials
  const client = new Client({
    user: process.env.DJANGO_DB_USER,
    host: process.env.DJANGO_DB_HOST,
    database: process.env.DJANGO_DB_NAME,
    password: process.env.DJANGO_DB_PASSWORD,
    port: process.env.DJANGO_DB_PORT,
  });

  try {
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
  } catch (e) {
    console.error("Error normalizing scores:", e);
  } finally {
    client.end();
  }
});
