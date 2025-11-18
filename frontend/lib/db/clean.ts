import { config } from "dotenv";
import { drizzle } from "drizzle-orm/postgres-js";
import { resolve } from "path";
import postgres from "postgres";
import { chat, document, message, stream, suggestion, user, vote } from "./schema";

// Load environment variables
config({ path: resolve(process.cwd(), ".env.local") });

// biome-ignore lint: Forbidden non-null assertion.
const client = postgres(process.env.POSTGRES_URL!);
const db = drizzle(client);

async function cleanDatabase() {
  console.log("🧹 Starting database cleanup...");

  try {
    // Delete in order to respect foreign key constraints
    console.log("Deleting votes...");
    await db.delete(vote);

    console.log("Deleting suggestions...");
    await db.delete(suggestion);

    console.log("Deleting documents...");
    await db.delete(document);

    console.log("Deleting messages...");
    await db.delete(message);

    console.log("Deleting streams...");
    await db.delete(stream);

    console.log("Deleting chats...");
    await db.delete(chat);

    console.log("Deleting users...");
    await db.delete(user);

    console.log("✅ Database cleaned successfully!");
  } catch (error) {
    console.error("❌ Error cleaning database:", error);
    throw error;
  } finally {
    await client.end();
  }
}

cleanDatabase();
