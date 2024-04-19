import { Message, CreateMessage, ChatRequestOptions } from "ai";

export interface ChatHandler {
  messages: Message[];
  input: string;
  isLoading: boolean;
  handleSubmit: (
    e: React.FormEvent<HTMLFormElement>,
    ops?: {
      data?: any;
    },
  ) => void;
  handleInputChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  reload?: () => void;
  stop?: () => void;
  onFileUpload?: (file_url: string, file_name: string) => void;
  onRemoveFile?: () => void;
  onFileError?: (errMsg: string) => void;
  append: (message: any, chatRequestOptions?: ChatRequestOptions) => Promise<string | null | undefined>;
}
