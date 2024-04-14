'use client'
import React, { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { XCircle } from 'lucide-react';

const ContextUploader = () => {
    const [files, setFiles] = useState<File[]>([]);
    const [names, setNames] = useState<string[]>([]);
    const [isSubmitted, setIsSubmitted] = useState<boolean>(false);

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

    const submitFiles = () => {
        const fileNames = files.map(file => file.name);
        setNames(fileNames);
        console.log("Submitting files:", files);
        clearFiles();
        setIsSubmitted(true);
    };

    return (
        <div className="p-4 flex flex-col gap-4 border-2 border-dashed border-gray-400 rounded-lg">
            <div {...getRootProps()} className={`text-center ${isDragActive ? 'bg-gray-200' : ''}`}>
                <input {...getInputProps()} />
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
        </div>
    );
};

export default ContextUploader;
