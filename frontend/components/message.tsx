"use client";
import type { Vote } from "@/lib/db/schema";
import type { ChatMessage } from "@/lib/types";
import { cn, sanitizeText } from "@/lib/utils";
import type { UseChatHelpers } from "@ai-sdk/react";
import equal from "fast-deep-equal";
import { motion } from "framer-motion";
import { Bot } from "lucide-react";
import { memo, useState } from "react";
import { useDataStream } from "./data-stream-provider";
import { MessageContent } from "./elements/message";
import { Response } from "./elements/response";
import { MessageActions } from "./message-actions";
import { MessageEditor } from "./message-editor";
import { PhishingResultDisplay } from "./phishing-result-display";
import { SpamResultDisplay } from "./spam-result-display";
import { SuspiciousAccessDisplay } from "./suspicious-access-display";

const PurePreviewMessage = ({
  chatId,
  message,
  vote,
  isLoading,
  setMessages,
  regenerate,
  isReadonly,
  requiresScrollPadding,
}: {
  chatId: string;
  message: ChatMessage;
  vote: Vote | undefined;
  isLoading: boolean;
  setMessages: UseChatHelpers<ChatMessage>["setMessages"];
  regenerate: UseChatHelpers<ChatMessage>["regenerate"];
  isReadonly: boolean;
  requiresScrollPadding: boolean;
}) => {
  const [mode, setMode] = useState<"view" | "edit">("view");

  const attachmentsFromMessage = message.parts.filter(
    (part) => part.type === "file"
  );

  useDataStream();

  return (
    <motion.div
      animate={{ opacity: 1 }}
      className="group/message w-full"
      data-role={message.role}
      data-testid={`message-${message.role}`}
      initial={{ opacity: 0 }}
    >
      <div
        className={cn("flex w-full items-start gap-2 md:gap-3", {
          "justify-end": message.role === "user" && mode !== "edit",
          "justify-start": message.role === "assistant",
        })}
      >
        {message.role === "assistant" && (
          <div className="-mt-1 flex size-8 shrink-0 items-center justify-center rounded-full bg-background ring-1 ring-border">
            <Bot size={14} />
          </div>
        )}

        <div
          className={cn("flex flex-col", {
            "gap-2 md:gap-4": message.parts?.some(
              (p) => p.type === "text" && p.text?.trim()
            ),
            "min-h-96": message.role === "assistant" && requiresScrollPadding,
            "w-full":
              (message.role === "assistant" &&
                message.parts?.some(
                  (p) => p.type === "text" && p.text?.trim()
                )) ||
              mode === "edit",
            "max-w-[calc(100%-2.5rem)] sm:max-w-[min(fit-content,80%)]":
              message.role === "user" && mode !== "edit",
          })}
        >
          {message.parts?.map((part, index) => {
            const { type } = part;
            const key = `message-${message.id}-part-${index}`;

            if (type === "text") {
              if (mode === "view") {
                return (
                  <div key={key}>
                    <MessageContent
                      className={cn({
                        "w-fit rounded-2xl px-3 py-2 text-right text-white":
                          message.role === "user",
                        "bg-transparent px-0 py-0 text-left":
                          message.role === "assistant",
                      })}
                      data-testid="message-content"
                      style={
                        message.role === "user"
                          ? { backgroundColor: "#202020" }
                          : undefined
                      }
                    >
                      <Response>{sanitizeText(part.text)}</Response>
                    </MessageContent>
                  </div>
                );
              }

              if (mode === "edit") {
                return (
                  <div
                    className="flex w-full flex-row items-start gap-3"
                    key={key}
                  >
                    <div className="size-8" />
                    <div className="min-w-0 flex-1">
                      <MessageEditor
                        key={message.id}
                        message={message}
                        regenerate={regenerate}
                        setMessages={setMessages}
                        setMode={setMode}
                      />
                    </div>
                  </div>
                );
              }
            }

            if (type.startsWith("tool-") && type.includes("spamClassifier")) {
              const { toolCallId, state, output } = part as any;

              return (
                <div className="my-4" key={toolCallId}>
                  {state === "partial-call" && (
                    <div className="rounded-lg border border-blue-200 bg-blue-50 p-4 dark:border-blue-900 dark:bg-blue-950/20">
                      <div className="flex items-center gap-2">
                        <div className="size-4 animate-spin rounded-full border-2 border-blue-600 border-t-transparent" />
                        <span className="text-sm font-medium text-blue-900 dark:text-blue-100">
                          Analizando email con modelo ML...
                        </span>
                      </div>
                    </div>
                  )}
                  {state === "output-available" && output && (
                    <SpamResultDisplay
                      success={output.success}
                      prediction={output.prediction}
                      is_spam={output.is_spam}
                      confidence={output.confidence}
                      details={output.details}
                      email_preview={output.email_preview}
                      error={output.error}
                      message={output.message}
                    />
                  )}
                </div>
              );
            }

            if (type.startsWith("tool-") && type.includes("phishingDetector")) {
              const { toolCallId, state, output } = part as any;

              return (
                <div className="my-4" key={toolCallId}>
                  {state === "partial-call" && (
                    <div className="rounded-lg border border-blue-200 bg-blue-50 p-4 dark:border-blue-900 dark:bg-blue-950/20">
                      <div className="flex items-center gap-2">
                        <div className="size-4 animate-spin rounded-full border-2 border-blue-600 border-t-transparent" />
                        <span className="text-sm font-medium text-blue-900 dark:text-blue-100">
                          Analizando URL con modelo ML...
                        </span>
                      </div>
                    </div>
                  )}
                  {state === "output-available" && output && (
                    <PhishingResultDisplay
                      success={output.success}
                      url={output.url}
                      prediction={output.prediction}
                      is_phishing={output.is_phishing}
                      confidence={output.confidence}
                      details={output.details}
                      error={output.error}
                      message={output.message}
                    />
                  )}
                </div>
              );
            }

            if (type.startsWith("tool-") && type.includes("suspiciousAccessDetector")) {
              const { toolCallId, state, output } = part as any;

              return (
                <div className="my-4" key={toolCallId}>
                  {state === "partial-call" && (
                    <div className="rounded-lg border border-blue-200 bg-blue-50 p-4 dark:border-blue-900 dark:bg-blue-950/20">
                      <div className="flex items-center gap-2">
                        <div className="size-4 animate-spin rounded-full border-2 border-blue-600 border-t-transparent" />
                        <span className="text-sm font-medium text-blue-900 dark:text-blue-100">
                          Analizando acceso de red con modelo ML...
                        </span>
                      </div>
                    </div>
                  )}
                  {state === "output-available" && output && (
                    <SuspiciousAccessDisplay
                      success={output.success}
                      prediction={output.prediction}
                      is_suspicious={output.is_suspicious}
                      confidence={output.confidence}
                      details={output.details}
                      analyzed_params={output.analyzed_params}
                      error={output.error}
                      message={output.message}
                    />
                  )}
                </div>
              );
            }

            return null;
          })}

          {!isReadonly && (
            <MessageActions
              chatId={chatId}
              isLoading={isLoading}
              key={`action-${message.id}`}
              message={message}
              setMode={setMode}
              vote={vote}
            />
          )}
        </div>
      </div>
    </motion.div>
  );
};

export const PreviewMessage = memo(
  PurePreviewMessage,
  (prevProps, nextProps) => {
    if (prevProps.isLoading !== nextProps.isLoading) {
      return false;
    }
    if (prevProps.message.id !== nextProps.message.id) {
      return false;
    }
    if (prevProps.requiresScrollPadding !== nextProps.requiresScrollPadding) {
      return false;
    }
    if (!equal(prevProps.message.parts, nextProps.message.parts)) {
      return false;
    }
    if (!equal(prevProps.vote, nextProps.vote)) {
      return false;
    }

    return false;
  }
);

export const ThinkingMessage = () => {
  const role = "assistant";

  return (
    <motion.div
      animate={{ opacity: 1 }}
      className="group/message w-full"
      data-role={role}
      data-testid="message-assistant-loading"
      exit={{ opacity: 0, transition: { duration: 0.5 } }}
      initial={{ opacity: 0 }}
      transition={{ duration: 0.2 }}
    >
      <div className="flex items-start justify-start gap-3">
        <div className="-mt-1 flex size-8 shrink-0 items-center justify-center rounded-full bg-background ring-1 ring-border">
          <Bot/>
        </div>

        <div className="flex w-full flex-col gap-2 md:gap-4">
          <div className="p-0 text-muted-foreground text-sm">
            Pensando...
          </div>
        </div>
      </div>
    </motion.div>
  );
};

