import { useState } from 'react'
import { Check, Copy } from "lucide-react";

import { Message } from "ai";
import { Button } from "../button";
import ChatAvatar from "./chat-avatar";
import Markdown from "./markdown";
import { useCopyToClipboard } from "./use-copy-to-clipboard";

interface Metadata {
  [key: string]: any;
}


export default function ChatMessage(chatMessage: Message) {
  const { isCopied, copyToClipboard } = useCopyToClipboard({ timeout: 2000 });

  let displayContent = chatMessage.content;
  let metadataInfo = null;

  console.log(displayContent)

  const metadataRegex = /\[.*?\]$/;
  const metadataMatch = displayContent.match(metadataRegex);

  if (metadataMatch) {
    const metadataString = metadataMatch[0];
    const metadata = JSON.parse(metadataString);

    metadataInfo = metadata.map(({ name, offset }: Metadata) => ({ name, offset }));

    displayContent = displayContent.replace(metadataRegex, '');
  }

  return (
    <div className="flex flex-col gap-2">
      <div className="flex items-start gap-4 pr-5 pt-5">
        <ChatAvatar role={chatMessage.role} />
        <div className="group flex flex-1 justify-between gap-2">
          <div className="flex-1 space-y-4">
            <Markdown content={displayContent} />
          </div>
          <Button
            onClick={() => copyToClipboard(displayContent)}
            size="icon"
            variant="ghost"
            className="h-8 w-8 opacity-0 group-hover:opacity-100"
          >
            {isCopied ? (
              <Check className="h-4 w-4" />
            ) : (
              <Copy className="h-4 w-4" />
            )}
          </Button>
        </div>
      </div>
      {metadataInfo && (
        <div className="flex flex-col gap-1 items-start pl-10">
          {metadataInfo.map((info: Metadata, index: number) => (
            <div key={index}>
              <span className="font-semibold">Name:</span> {info.filename}
              <br />
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
