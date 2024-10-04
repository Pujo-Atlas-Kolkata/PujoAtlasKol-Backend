const { Client } = require("pg");
const cron = require("node-cron");
require("dotenv").config({ path: "./.env" });

// Schedule cron job to run every day at 5 AM
cron.schedule("0 */6 * * *", async () => {
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
    console.log("Running update_pujo_scores cron job");

    const X = 3;
    const currentTime = new Date();
    const timeXHoursAgo = new Date(currentTime.getTime() - X * 60 * 60 * 1000);
    const time2XHoursAgo = new Date(
      currentTime.getTime() - 2 * X * 60 * 60 * 1000
    );

    // Start a transaction
    await client.query("BEGIN");

    // Fetch Pujo objects not updated in the last X hours
    const pujoQuery = `
            SELECT * FROM "pujo_pujo"
            WHERE "updated_at" < $1
        `;
    const pujos = await client.query(pujoQuery, [timeXHoursAgo]);

    if (pujos.rows.length === 0) {
      console.log("No pujos found for score update.");
    } else {
      for (const pujo of pujos.rows) {
        // Fetch positive LastScoreModel entries for the last 2X hours for this Pujo
        const lastScoresQuery = `
                    SELECT * FROM "pujo_lastscoremodel"
                    WHERE "pujo_id" = $1 AND "last_updated_at" > $2
                `;
        const lastScores = await client.query(lastScoresQuery, [
          pujo.id,
          time2XHoursAgo,
        ]);

        // Sum all positive scores
        const scoreSum = lastScores.rows.reduce((sum, score) => {
          return score.value > 0 ? sum + score.value : sum;
        }, 0);

        // Update the pujo's search score ensuring it does not go below zero
        const newSearchScore = Math.max(pujo.search_score - scoreSum, 0);
        const updatePujoQuery = `
                    UPDATE "pujo_pujo"
                    SET "search_score" = $1, "updated_at" = $2
                    WHERE "id" = $3
                `;
        await client.query(updatePujoQuery, [
          newSearchScore,
          currentTime,
          pujo.id,
        ]);

        // Delete all previous last scores for this pujo
        const deleteLastScoresQuery = `
                    DELETE FROM "pujo_lastscoremodel"
                    WHERE "pujo_id" = $1 AND "last_updated_at" > $2
                `;
        await client.query(deleteLastScoresQuery, [pujo.id, time2XHoursAgo]);

        // Log the score summation - create a new negative score entry
        const insertNewScoreQuery = `
                    INSERT INTO "pujo_lastscoremodel" ("pujo_id", "value", "last_updated_at")
                    VALUES ($1, $2, $3)
                `;
        await client.query(insertNewScoreQuery, [
          pujo.id,
          -scoreSum,
          currentTime,
        ]);

        console.log(
          `Updated pujo: ${pujo.id}, new search_score: ${newSearchScore}`
        );
      }
    }

    //check if it actually went through
    await client.query("COMMIT");
  } catch (error) {
    console.error("Error running update_pujo_scores:", error);
    //   await client.query("ROLLBACK");
  } finally {
    client.end();
  }
});
