"use client";
import { useState } from "react";
import { useChat } from "ai/react";
import { ChatInput, ChatMessages } from "./ui/chat";

export default function ChatSection() {

  const {
    messages,
    input,
    isLoading,
    handleSubmit,
    handleInputChange,
    reload,
    stop
  } = useChat({
    api: process.env.NEXT_PUBLIC_CHAT_API,
    headers: {
      "Content-Type": "application/json",
    },
    sendExtraMessageFields: true,
  });

  const [files, setFiles] = useState<UploadedFile[]>([]);

  const onFileUpload = (file_url: string, file_name: string) => {
    const newFile = {
      index: messages.length,
      file_url: file_url,
      file_name: file_name,
    };
    setFiles([...files, newFile]);
  }

  const onRemoveFile = () => {
    if (files.length === 0) {
      return;
    }
    setFiles(files.slice(0, -1));
  }

  return (
    <div className="max-h-full flex-grow w-full flex flex-col gap-4">
      <ChatMessages
        messages={messages}
        isLoading={isLoading}
        reload={reload}
        stop={stop}
        files={files}
      />
      <ChatInput
        input={input}
        handleSubmit={handleSubmit}
        handleInputChange={handleInputChange}
        isLoading={isLoading}
        multiModal={true}
        onFileUpload={onFileUpload}
        onRemoveFile={onRemoveFile}
      />
    </div>
  );
}
