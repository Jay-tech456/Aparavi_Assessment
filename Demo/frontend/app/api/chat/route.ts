import { anthropic } from "@ai-sdk/anthropic"
import { openai } from "@ai-sdk/openai"
import { streamText, convertToModelMessages, type UIMessage } from "ai"

// Allow streaming responses up to 30 seconds
export const maxDuration = 30

/**
 * POST handler for chat API endpoint
 * Handles both text and multimodal (PDF/image) conversations
 */
export async function POST(req: Request) {
  try {
    // Extract messages from the request body
    const { messages }: { messages: UIMessage[] } = await req.json()

    // Check if any message contains PDF attachments
    // PDFs require special handling with Claude model
    const messagesHavePDF = messages.some((message) =>
      message.experimental_attachments?.some((attachment) => attachment.contentType === "application/pdf"),
    )

    // Check if any message contains image attachments
    const messagesHaveImages = messages.some((message) =>
      message.experimental_attachments?.some((attachment) => attachment.contentType?.startsWith("image/")),
    )

    // Select the appropriate model based on attachment types
    let selectedModel

    if (messagesHavePDF) {
      // Use Claude for PDF processing (supports both images and PDFs)
      selectedModel = anthropic("claude-3-5-sonnet-latest")
      console.log("Using Claude model for PDF processing")
    } else if (messagesHaveImages) {
      // Use GPT-4o for image processing (good image understanding)
      selectedModel = openai("gpt-4o")
      console.log("Using GPT-4o model for image processing")
    } else {
      // Use GPT-4o for text-only conversations (fast and capable)
      selectedModel = openai("gpt-4o")
      console.log("Using GPT-4o model for text conversation")
    }

    // Stream the response using the selected model
    const result = streamText({
      model: selectedModel,
      messages: convertToModelMessages(messages),

      // Optional: Add system message for better responses
      system: `You are a helpful AI assistant that can analyze text, images, and PDF documents. 
               When analyzing PDFs, provide detailed insights about the content, structure, and key information.
               When analyzing images, describe what you see and answer any questions about the visual content.
               Always be thorough and helpful in your responses.`,
    })

    // Return the streaming response
    return result.toDataStreamResponse()
  } catch (error) {
    console.error("API Error:", error)

    // Return error response
    return new Response(
      JSON.stringify({
        error: "Failed to process request",
        details: error instanceof Error ? error.message : "Unknown error",
      }),
      {
        status: 500,
        headers: { "Content-Type": "application/json" },
      },
    )
  }
}
