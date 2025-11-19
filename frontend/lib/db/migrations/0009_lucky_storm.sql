CREATE TABLE IF NOT EXISTS "Event" (
	"id" uuid PRIMARY KEY DEFAULT gen_random_uuid() NOT NULL,
	"type" varchar(50) NOT NULL,
	"rawData" jsonb NOT NULL,
	"analysisResult" jsonb,
	"severity" varchar(20),
	"isThreat" boolean DEFAULT false NOT NULL,
	"confidence" numeric(5, 4),
	"createdAt" timestamp DEFAULT now() NOT NULL,
	"acknowledgedAt" timestamp
);
