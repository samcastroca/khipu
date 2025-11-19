import { suspiciousAccessDetector } from "@/lib/ai/tools/suspicious-access-detector";
import { suspiciousLogsDetector } from "@/lib/ai/tools/suspicious-logs-detector";
import { event } from "@/lib/db/schema";
import { drizzle } from "drizzle-orm/postgres-js";
import { NextResponse } from "next/server";
import postgres from "postgres";

const client = postgres(process.env.POSTGRES_URL!);
const db = drizzle(client);

export async function GET() {
  return NextResponse.json({ message: "Event ingestion endpoint is working" });
}

export async function POST(request: Request) {
  try {
    const body = await request.json();
    const { type, data } = body;

    if (!type || !data) {
      return NextResponse.json(
        { error: "Type and data are required" },
        { status: 400 }
      );
    }

    // Validate type - only network_access and suspicious_logs allowed
    if (!["network_access", "suspicious_logs"].includes(type)) {
      return NextResponse.json(
        { error: "Invalid type. Must be: network_access or suspicious_logs" },
        { status: 400 }
      );
    }

    // Analyze event with appropriate ML tool
    let analysisResult: any = null;
    let isThreat = false;
    let severity: "low" | "medium" | "high" | "critical" = "low";
    let confidence = 0;

    try {
      if (type === "network_access") {
        // Use suspicious access detector - call tool directly with defaults
        const params = {
          network_packet_size: data.network_packet_size || 1500,
          protocol_type: data.protocol_type || "HTTP",
          login_attempts: data.login_attempts || 1,
          session_duration: data.session_duration || 30,
          encryption_used: data.encryption_used || "TLS",
          ip_reputation_score: data.ip_reputation_score || 50,
          failed_logins: data.failed_logins || 0,
          browser_type: data.browser_type || "Chrome",
          unusual_time_access: data.unusual_time_access || 0,
        };
        if (suspiciousAccessDetector.execute) {
          analysisResult = await suspiciousAccessDetector.execute(
            params,
            { toolCallId: "event-ingest", messages: [] }
          );
        }
        
        if (analysisResult?.success) {
          isThreat = analysisResult.is_suspicious === true;
          confidence = analysisResult.confidence || 0;
          
          if (confidence >= 0.9) severity = "critical";
          else if (confidence >= 0.7) severity = "high";
          else if (confidence >= 0.5) severity = "medium";
          else severity = "low";
        }
      } else if (type === "suspicious_logs") {
        // Use suspicious logs detector - call tool directly with defaults
        const params = {
          duration: data.duration || "0",
          proto: data.proto || "tcp",
          src_ip_addr: data.src_ip_addr || "0.0.0.0",
          src_pt: data.src_pt || "0",
          dst_ip_addr: data.dst_ip_addr || "0.0.0.0",
          dst_pt: data.dst_pt || "0",
          packets: data.packets || "0",
          bytes_str: data.bytes_str || "0",
          flags: data.flags || "",
        };
        if (suspiciousLogsDetector.execute) {
          analysisResult = await suspiciousLogsDetector.execute(
            params,
            { toolCallId: "event-ingest", messages: [] }
          );
        }
        
        if (analysisResult?.success) {
          isThreat = analysisResult.is_suspicious === true;
          confidence = analysisResult.confidence || 0;
          
          if (confidence >= 0.9) severity = "critical";
          else if (confidence >= 0.7) severity = "high";
          else if (confidence >= 0.5) severity = "medium";
          else severity = "low";
        }
      }
    } catch (analysisError) {
      console.error("Analysis error:", analysisError);
      // Continue with null analysis result
    }

    // Save event to database
    const [savedEvent] = await db
      .insert(event)
      .values({
        type,
        rawData: data,
        analysisResult,
        isThreat,
        severity,
        confidence: confidence.toString(),
      })
      .returning();

    return NextResponse.json({
      success: true,
      event: savedEvent,
      message: "Event ingested and analyzed successfully",
    });
  } catch (error) {
    console.error("Event ingestion error:", error);
    return NextResponse.json(
      { error: "Failed to ingest event" },
      { status: 500 }
    );
  }
}
