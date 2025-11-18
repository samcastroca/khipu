import { createOpenRouter } from "@openrouter/ai-sdk-provider";
import {
  customProvider
} from "ai";
import { isTestEnvironment } from "../constants";

const openrouter = createOpenRouter({
  apiKey: process.env.OPENROUTER_API_KEY,
});

export const myProvider = isTestEnvironment
  ? (() => {
      const {
        artifactModel,
        chatModel,
        titleModel,
      } = require("./models.mock");
      return customProvider({
        languageModels: {
          "chat-model": chatModel,
          "title-model": titleModel,
          "artifact-model": artifactModel,
        },
      });
    })()
  : customProvider({
      languageModels: {
        "chat-model": openrouter("google/gemini-2.0-flash-001"),
        "title-model": openrouter("google/gemini-2.0-flash-001"),
        "artifact-model": openrouter("google/gemini-2.0-flash-001"),
      },
    });
