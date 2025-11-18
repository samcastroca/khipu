import type { InferUITool, UIMessage } from "ai";
import { z } from "zod";
import type { phishingDetector } from "./ai/tools/phishing-detector";
import type { spamClassifier } from "./ai/tools/spam-classifier";
import type { suspiciousAccessDetector } from "./ai/tools/suspicious-access-detector";
import type { AppUsage } from "./usage";

export type DataPart = { type: "append-message"; message: string };

export const messageMetadataSchema = z.object({
  createdAt: z.string(),
});

export type MessageMetadata = z.infer<typeof messageMetadataSchema>;

type spamClassifierTool = InferUITool<typeof spamClassifier>;
type phishingDetectorTool = InferUITool<typeof phishingDetector>;
type suspiciousAccessDetectorTool = InferUITool<typeof suspiciousAccessDetector>;

export type ChatTools = {
  spamClassifier: spamClassifierTool;
  phishingDetector: phishingDetectorTool;
  suspiciousAccessDetector: suspiciousAccessDetectorTool;
};

export type CustomUIDataTypes = {
  textDelta: string;
  sheetDelta: string;
  codeDelta: string;
  imageDelta: string;
  appendMessage: string;
  id: string;
  title: string;
  clear: null;
  finish: null;
  usage: AppUsage;
};

export type ChatMessage = UIMessage<
  MessageMetadata,
  CustomUIDataTypes,
  ChatTools
>;

export type Attachment = {
  name: string;
  url: string;
  contentType: string;
};

