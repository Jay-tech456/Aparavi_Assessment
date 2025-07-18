"use client"

import type React from "react"

import { useMultimodalChat } from "@/hooks/use-multimodal-chat"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent } from "@/components/ui/card"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Paperclip, Send, FileText, User, Bot } from "lucide-react"
import { useRef, useState } from "react"
import Image from "next/image"

export default function MultimodalChatbot() {
  // Use our custom hook for chat functionality
  const { messages, input, handleInputChange, handleSubmit, isLoading } = useMultimodalChat()

  // State for file handling
  const [files, setFiles] = useState<FileList | undefined>(undefined)
  const fileInputRef = useRef<HTMLInputElement>(null)

  // Handle form submission with file attachments
  const onSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault()

    // Call the hook's submit handler with attachments
    handleSubmit(event, {
      experimental_attachments: files,
    })

    // Reset file state after submission
    setFiles(undefined)
    if (fileInputRef.current) {
      fileInputRef.current.value = ""
    }
  }

  // Handle file selection
  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files) {
      setFiles(event.target.files)
    }
  }

  // Trigger file input click
  const triggerFileUpload = () => {
    fileInputRef.current?.click()
  }

  return (
    <div className="flex flex-col h-screen max-w-4xl mx-auto p-4">
      {/* Header */}
      <div className="mb-4">
        <h1 className="text-2xl font-bold text-center">Multimodal AI Chatbot</h1>
        <p className="text-center text-muted-foreground">Ask questions and upload PDF documents for analysis</p>
      </div>

      {/* Chat Messages Area */}
      <Card className="flex-1 mb-4">
        <CardContent className="p-0">
          <ScrollArea className="h-[calc(100vh-200px)] p-4">
            {messages.length === 0 ? (
              <div className="flex items-center justify-center h-full text-muted-foreground">
                <div className="text-center">
                  <Bot className="mx-auto mb-2 h-8 w-8" />
                  <p>Start a conversation or upload a PDF to begin!</p>
                </div>
              </div>
            ) : (
              <div className="space-y-4">
                {messages.map((message) => (
                  <div key={message.id} className={`flex ${message.role === "user" ? "justify-end" : "justify-start"}`}>
                    <div
                      className={`flex max-w-[80%] ${
                        message.role === "user" ? "flex-row-reverse" : "flex-row"
                      } items-start space-x-2`}
                    >
                      {/* Avatar */}
                      <div
                        className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${
                          message.role === "user"
                            ? "bg-primary text-primary-foreground ml-2"
                            : "bg-secondary text-secondary-foreground mr-2"
                        }`}
                      >
                        {message.role === "user" ? <User className="w-4 h-4" /> : <Bot className="w-4 h-4" />}
                      </div>

                      {/* Message Content */}
                      <div
                        className={`rounded-lg p-3 ${
                          message.role === "user" ? "bg-primary text-primary-foreground" : "bg-secondary"
                        }`}
                      >
                        {/* Text Content */}
                        <div className="whitespace-pre-wrap">{message.content}</div>

                        {/* Attachments Display */}
                        {message.experimental_attachments && message.experimental_attachments.length > 0 && (
                          <div className="mt-2 space-y-2">
                            {message.experimental_attachments
                              .filter(
                                (attachment) =>
                                  attachment?.contentType?.startsWith("image/") ||
                                  attachment?.contentType?.startsWith("application/pdf"),
                              )
                              .map((attachment, index) => (
                                <div key={`${message.id}-${index}`} className="border rounded p-2">
                                  {attachment.contentType?.startsWith("image/") ? (
                                    // Display images
                                    <Image
                                      src={attachment.url || "/placeholder.svg"}
                                      width={300}
                                      height={200}
                                      alt={attachment.name ?? `attachment-${index}`}
                                      className="rounded"
                                    />
                                  ) : attachment.contentType?.startsWith("application/pdf") ? (
                                    // Display PDF info and preview
                                    <div className="space-y-2">
                                      <div className="flex items-center space-x-2">
                                        <FileText className="w-4 h-4" />
                                        <span className="text-sm font-medium">
                                          {attachment.name ?? `PDF Document ${index + 1}`}
                                        </span>
                                      </div>
                                      <iframe
                                        src={attachment.url}
                                        width="100%"
                                        height="400"
                                        title={attachment.name ?? `pdf-${index}`}
                                        className="border rounded"
                                      />
                                    </div>
                                  ) : null}
                                </div>
                              ))}
                          </div>
                        )}
                      </div>
                    </div>
                  </div>
                ))}

                {/* Loading indicator */}
                {isLoading && (
                  <div className="flex justify-start">
                    <div className="flex items-start space-x-2">
                      <div className="flex-shrink-0 w-8 h-8 rounded-full bg-secondary text-secondary-foreground flex items-center justify-center">
                        <Bot className="w-4 h-4" />
                      </div>
                      <div className="bg-secondary rounded-lg p-3">
                        <div className="flex space-x-1">
                          <div className="w-2 h-2 bg-current rounded-full animate-bounce" />
                          <div
                            className="w-2 h-2 bg-current rounded-full animate-bounce"
                            style={{ animationDelay: "0.1s" }}
                          />
                          <div
                            className="w-2 h-2 bg-current rounded-full animate-bounce"
                            style={{ animationDelay: "0.2s" }}
                          />
                        </div>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            )}
          </ScrollArea>
        </CardContent>
      </Card>

      {/* Input Form */}
      <Card>
        <CardContent className="p-4">
          <form onSubmit={onSubmit} className="space-y-3">
            {/* File Preview */}
            {files && files.length > 0 && (
              <div className="flex flex-wrap gap-2">
                {Array.from(files).map((file, index) => (
                  <div key={index} className="flex items-center space-x-2 bg-secondary rounded-lg p-2 text-sm">
                    <FileText className="w-4 h-4" />
                    <span>{file.name}</span>
                    <Button
                      type="button"
                      variant="ghost"
                      size="sm"
                      onClick={() => {
                        const newFiles = Array.from(files).filter((_, i) => i !== index)
                        const dt = new DataTransfer()
                        newFiles.forEach((f) => dt.items.add(f))
                        setFiles(dt.files)
                      }}
                    >
                      ×
                    </Button>
                  </div>
                ))}
              </div>
            )}

            {/* Input Row */}
            <div className="flex space-x-2">
              {/* Hidden file input */}
              <input
                type="file"
                ref={fileInputRef}
                onChange={handleFileChange}
                accept=".pdf,image/*"
                multiple
                className="hidden"
              />

              {/* File upload button */}
              <Button type="button" variant="outline" size="icon" onClick={triggerFileUpload} disabled={isLoading}>
                <Paperclip className="w-4 h-4" />
              </Button>

              {/* Text input */}
              <Input
                value={input}
                onChange={handleInputChange}
                placeholder="Ask a question or upload a PDF..."
                disabled={isLoading}
                className="flex-1"
              />

              {/* Send button */}
              <Button type="submit" disabled={isLoading || (!input.trim() && !files?.length)}>
                <Send className="w-4 h-4" />
              </Button>
            </div>
          </form>
        </CardContent>
      </Card>
    </div>
  )
}
