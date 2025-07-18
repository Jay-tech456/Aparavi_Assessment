import { type Message } from "ai"

export const maxDuration = 30

export async function POST(req: Request) {
  try {
    const { messages }: { messages: Message[] } = await req.json()

    const lastMessage = messages[messages.length - 1]?.content
    const sessionId = "1234" // In production, generate this per user/session

    if (!lastMessage) {
      return new Response(
        JSON.stringify({ error: "No message content found" }),
        { status: 400, headers: { "Content-Type": "application/json" } }
      )
    }

    const flaskPayload = {
      session_id: sessionId,
      message: lastMessage,
    }

    const flaskResponse = await fetch("http://127.0.0.1:5000/ask", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(flaskPayload),
    })

    if (!flaskResponse.ok) {
      const errorText = await flaskResponse.text()
      throw new Error(`Flask API error: ${flaskResponse.status} - ${errorText}`)
    }

    const data = await flaskResponse.json()

    // Respond with plain text so your frontend chat can render it
    return new Response(data.response, {
      headers: {
        "Content-Type": "text/plain",
      },
    })
  } catch (error) {
    console.error("Chat error:", error)

    return new Response(
      JSON.stringify({
        error: "Failed to process request",
        details: error instanceof Error ? error.message : "Unknown error",
      }),
      {
        status: 500,
        headers: { "Content-Type": "application/json" },
      }
    )
  }
}
