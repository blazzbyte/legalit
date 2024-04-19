'use client'
import React, { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { Loader2, XCircle } from 'lucide-react';
import axios from 'axios';
import { useUser } from '@/app/contexts/user-context';

const ContextUploader = () => {
    const [files, setFiles] = useState<File[]>([]);
    const [names, setNames] = useState<string[]>([]);
    const [isSubmitted, setIsSubmitted] = useState<boolean>(false);

    const [uploading, setUploading] = useState<boolean>(false);

    const { userId, setUserByDefault, setUploadedContext } = useUser()

    console.log(userId)

    const onDrop = useCallback((acceptedFiles: File[]) => {
        setFiles(prevFiles => [...prevFiles, ...acceptedFiles]);
    }, []);

    const { getRootProps, getInputProps, isDragActive } = useDropzone({
        onDrop,
        disabled: isSubmitted,
    });

    const removeFile = (index: number) => {
        setFiles(prevFiles => prevFiles.filter((_, i) => i !== index));
    };

    const clearFiles = () => {
        setFiles([]);
    };

    const submitFiles = async () => {
        setUploading(true);

        const formData = new FormData();

        files.forEach((file, index) => {
            formData.append(`file-${index + 1}`, file);
        });

        formData.append('use_llama_parse', String(false));
        formData.append('use_unstructured', String(true));
        formData.append('user_id', "testing");

        try {
            const response = await axios.post(process.env.NEXT_PUBLIC_API_URL + '/api/upload', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            });

            if (response.status !== 200) {
                throw new Error('Failed to upload documents');
            }

            setNames(files.map(file => file.name));
            clearFiles();
            setIsSubmitted(true);
            setUploadedContext();
        } catch (error) {
            console.error('Error uploading documents:', (error as Error).message);
        } finally {
            setUploading(false);
        }
    };

    const setDefault = () => {
        setUserByDefault()
        setNames(["Document 1", "Document 2", "Document 3"])
        setIsSubmitted(true)
    }

    return (
        <div className='flex flex-col gap-4'>
            {uploading && <div className="p-4 flex flex-col items-center border-2 border-dashed border-gray-400 rounded-lg">
                <Loader2 className="h-4 w-4 animate-spin" />
            </div>}
            {!uploading &&
                <div className="p-4 flex flex-col gap-4 border-2 border-dashed border-gray-400 rounded-lg cursor-pointer">
                    <div {...getRootProps()} className={`text-center ${isDragActive ? 'bg-gray-200' : ''}`}>
                        <input {...getInputProps()} accept='application/pdf' />
                        {isSubmitted ? (
                            <p>Files submitted successfully: <span className='font-semibold'>{names.join(", ")}</span></p>
                        ) : (
                            <p className='text-sm outline-none select-none '>Drag and drop some PDF files here, or click to select files</p>
                        )}
                    </div>
                    {files.length > 0 && (
                        <div className='space-y-2'>
                            {files.map((file, index) => (
                                <div key={index} className="flex items-center justify-between rounded-md bg-gray-100 p-2">
                                    <span>{file.name}</span>
                                    <button
                                        onClick={() => removeFile(index)}
                                        className="text-red-500 hover:text-red-700"
                                    >
                                        <XCircle />
                                    </button>
                                </div>
                            ))}
                        </div>
                    )}
                    {files.length > 0 && !isSubmitted && (
                        <div className="flex justify-center gap-4">
                            <button
                                onClick={submitFiles}
                                disabled={files.length === 0 || isSubmitted}
                                className='bg-sky-500 hover:bg-sky-600 font-bold py-2 px-4 rounded'
                            >
                                Submit
                            </button>
                            <button
                                onClick={clearFiles}
                                disabled={files.length === 0 || isSubmitted}
                                className='bg-gray-500 hover:bg-gray-700 font-bold py-2 px-4 rounded'
                            >
                                Clear
                            </button>
                        </div>
                    )}
                </div>}
            {!uploading && !isSubmitted && (<div className='flex flex-col space-y-3'>
                <button onClick={setDefault} className='self-center px-4 py-2 bg-cyan-600 text-white font-medium rounded-md text-center'>
                    SET DOCUMENTS BY DEFAULT
                </button>
                <p className='text-sm'>If you don&apos;t want to upload your own documents, try the demo, which contains the following documents by default:</p>
                <ul className='text-sm'>
                    <li> - Document 1</li>
                    <li> - Document 2</li>
                    <li> - Document 3</li>
                </ul>
            </div>)
            }
        </div>
    );
};

export default ContextUploader;
