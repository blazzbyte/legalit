import { Loader2, FileText } from "lucide-react";
import { useEffect, useRef } from "react";

import ChatActions from "./chat-actions";
import ChatMessage from "./chat-message";
import { ChatHandler } from "./chat.interface";

export default function ChatMessages(
  props: Pick<ChatHandler, "messages" | "isLoading" | "reload" | "stop"> & {
    files?: UploadedFile[];
  },
) {
  const scrollableChatContainerRef = useRef<HTMLDivElement>(null);
  const messageLength = props.messages.length;
  const lastMessage = props.messages[messageLength - 1];

  const scrollToBottom = () => {
    if (scrollableChatContainerRef.current) {
      scrollableChatContainerRef.current.scrollTop =
        scrollableChatContainerRef.current.scrollHeight;
    }
  };

  const isLastMessageFromAssistant =
    messageLength > 0 && lastMessage?.role !== "user";
  const showReload =
    props.reload && !props.isLoading && isLastMessageFromAssistant;
  const showStop = props.stop && props.isLoading;

  const isPending = props.isLoading && !isLastMessageFromAssistant;

  useEffect(() => {
    scrollToBottom();
  }, [messageLength, lastMessage]);

  return (
    <div className="flex-grow w-full rounded-xl bg-white p-4 shadow-xl pb-0 overflow-y-auto">
      <div
        className="flex flex-col gap-5 divide-y pb-4"
        ref={scrollableChatContainerRef}
      >
        {props.messages.map((m, index) => (
          <div className="flex flex-col flex-wrap" key={m.id}>
            <ChatMessage {...m} />
            {
              props.files && props.files.filter(file => file.index === index).map(file => (
                <div key={file.index} className="w-fit flex items-center ml-12 px-4 py-2 gap-4 bg-gray-200 rounded-lg">
                  <FileText size={20} />
                  <a href={file.file_url} target="_blank" rel="noopener noreferrer" className="font-semibold">{file.file_name}</a>
                </div>
              ))
            }
          </div>
        ))}
        {isPending && (
          <div className="flex justify-center items-center pt-10">
            <Loader2 className="h-4 w-4 animate-spin" />
          </div>
        )}
      </div>
      <div className="flex justify-end py-4">
        <ChatActions
          reload={props.reload}
          stop={props.stop}
          showReload={showReload}
          showStop={showStop}
        />
      </div>
    </div>
  );
}
