import { useChat } from "@ai-sdk/react"
import type { Message } from "ai"

/**
 * Custom hook for multimodal chat functionality
 * Extends the base useChat hook with multimodal capabilities
 */
export function useMultimodalChat() {
  // Use the AI SDK's useChat hook with our custom API endpoint
  const chatHook = useChat({
    api: "/api/chat", // Points to our API route handler

    // Optional: Handle errors
    onError: (error) => {
      console.error("Chat error:", error)
    },

    // Optional: Handle when response finishes
    onFinish: (message: Message) => {
      console.log("Response finished:", message)
    },
  })

  // Return all the hook functionality
  // This includes: messages, input, handleInputChange, handleSubmit, isLoading, etc.
  return {
    ...chatHook,
  }
}
