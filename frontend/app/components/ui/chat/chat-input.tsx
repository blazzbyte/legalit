import { useState } from "react";
import { Button } from "../button";
import FileUploader from "../file-uploader";
import { Input } from "../input";
import UploadFilePreview from "../upload-file-preview";
import { ChatHandler } from "./chat.interface";
import axios from "axios";
import { useUser } from "@/app/contexts/user-context";

export default function ChatInput(
  props: Pick<
    ChatHandler,
    | "isLoading"
    | "input"
    | "handleSubmit"
    | "handleInputChange"
    | "onFileUpload"
    | "onFileError"
    | "onRemoveFile"
  > & {
    multiModal?: boolean;
  },
) {

  const { uploadedContext } = useUser()

  const [file, setFile] = useState<File | null>(null);
  const [urlFile, setUrlFile] = useState<string | null>(null);

  const onSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    if (file) {
      submitFiles()
      props.handleSubmit(e, {
        data: {
          user_id: "testing",
          use_llama_parse: true,
          use_unstructured: false
        },
      });

    } else {
      props.handleSubmit(e);
    }
  };

  const submitFiles = async () => {
    if (file) {
      const formData = new FormData();
      formData.append('file', file);
      formData.append('user_id', "testing");

      try {
        const response = await axios.post(process.env.NEXT_PUBLIC_API_URL + '/api/upload/document', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        });

        if (response.status !== 200) {
          throw new Error('Failed to upload documents');
        }
        if (props.onFileUpload && urlFile) {
          props.onFileUpload(urlFile, file.name)
        }
        onRemoveFile()
      } catch (error) {
        console.error('Error uploading documents:', (error as Error).message);
      }
    }
  };

  const onRemoveFile = () => {
    setFile(null);
    setUrlFile(null);
  };

  const onRemove = () => {
    if (props.onRemoveFile) {
      props.onRemoveFile()
    }
    onRemoveFile()
  }

  const onUpload = async (file: File) => {
    if (props.multiModal && file.type.startsWith("application/pdf")) {
      setFile(file)
      setUrlFile(URL.createObjectURL(file));
    }
  };

  const onFileError = (errMsg: any) => {
    console.log(errMsg)
  }

  return (
    <form
      onSubmit={onSubmit}
      className="rounded-xl bg-white p-4 shadow-xl space-y-4"
    >
      {file && file.type === "application/pdf" && urlFile && (
        <UploadFilePreview url={urlFile} onRemove={onRemove} />
      )}
      <div className="flex w-full items-start justify-between gap-4 ">
        <Input
          autoFocus
          name="message"
          placeholder="Type a message"
          className="flex-1"
          value={props.input}
          onChange={props.handleInputChange}
          disabled={!uploadedContext}
        />
        <FileUploader
          onFileUpload={onUpload}
          onFileError={onFileError}
          config={{
            allowedExtensions: ["application/pdf"],
            disabled: file !== null || !uploadedContext,
          }}
        />
        <Button type="submit" disabled={props.isLoading || !uploadedContext}>
          Send message
        </Button>
      </div>
    </form>
  );
}
