const { Client } = require('pg');
const cron = require('node-cron');
require('dotenv').config();

// PostgreSQL credentials
const pgClient = new Client({
    user: process.env.DJANGO_DB_USER,
    host: process.env.DJANGO_DB_HOST,
    database: process.env.DJANGO_DB_NAME,
    password: process.env.DJANGO_DB_PASSWORD,
    port: process.env.DJANGO_DB_PORT,
});

// Connect to PostgreSQL
pgClient.connect()
    .then(() => console.log("Connected to PostgreSQL"))
    .catch(err => console.error("Connection error", err.stack));

// Schedule cron job to run every day at 5 AM
cron.schedule('0 5 * * *', async () => {
    try {
        console.log("Running update_pujo_scores cron job");

        const X = 3;
        const currentTime = new Date();
        const timeXHoursAgo = new Date(currentTime.getTime() - X * 60 * 60 * 1000);
        const time2XHoursAgo = new Date(currentTime.getTime() - 2 * X * 60 * 60 * 1000);

        // Fetch Pujo objects not updated in the last X hours
        const pujoQuery = `
      SELECT * FROM "pujo_pujo"
      WHERE "updated_at" < $1
    `;
        const pujos = await pgClient.query(pujoQuery, [timeXHoursAgo]);

        if (pujos.rows.length === 0) {
            console.log("No pujos found for score update.");
        } else {
            for (const pujo of pujos.rows) {
                // Fetch positive LastScoreModel entries for the last 2X hours for this Pujo
                const lastScoresQuery = `
          SELECT * FROM "LastScoreModel"
          WHERE "pujo_id" = $1 AND "last_updated_at" > $2
        `;
                const lastScores = await pgClient.query(lastScoresQuery, [pujo.id, time2XHoursAgo]);

                // Sum all positive scores
                const scoreSum = lastScores.rows.reduce((sum, score) => {
                    return score.value > 0 ? sum + score.value : sum;
                }, 0);

                // Update the pujo's search score ensuring it does not go below zero
                const newSearchScore = Math.max(pujo.search_score - scoreSum, 0);
                const updatePujoQuery = `
          UPDATE "Pujo"
          SET "search_score" = $1, "updated_at" = $2
          WHERE "id" = $3
        `;
                await pgClient.query(updatePujoQuery, [newSearchScore, currentTime, pujo.id]);

                // Delete all previous last scores for this pujo
                const deleteLastScoresQuery = `
          DELETE FROM "LastScoreModel"
          WHERE "pujo_id" = $1 AND "last_updated_at" > $2
        `;
                await pgClient.query(deleteLastScoresQuery, [pujo.id, time2XHoursAgo]);

                // Log the score summation - create a new negative score entry
                const insertNewScoreQuery = `
          INSERT INTO "LastScoreModel" ("pujo_id", "value", "last_updated_at")
          VALUES ($1, $2, $3)
        `;
                await pgClient.query(insertNewScoreQuery, [pujo.id, -scoreSum, currentTime]);

                console.log(`Updated pujo: ${pujo.id}, new search_score: ${newSearchScore}`);
            }
        }
    } catch (error) {
        console.error("Error running update_pujo_scores:", error);
    }
});

