import React from 'react'
import { Scale } from 'lucide-react'
import ContextUploader from './ui/context-uploader'

const sidebar = () => {
    return (
        <nav className='w-3/12 bg-white rounded-xl flex flex-col p-4 gap-4'>
            <a href='' className='flex gap-4 items-center'>
                <div className='w-10 grid place-items-center aspect-square rounded-xl bg-sky-500 text-white'><Scale /></div>
                <h2 className='text-xl font-semibold tracking-wider'>ASSUDIT</h2>
            </a>
            <div className='flex flex-col gap-2'>
                <h4 className='text-sky-600 font-bold'>Legal Context</h4>
                <p className='text-sm'>Upload relevant legal documents</p>
                <ContextUploader />
            </div>
            <div className='flex flex-col gap-2'>
                <h4 className='text-sky-600 font-bold'>Key Elements (Optional)</h4>
                <p className='text-sm'>Key elements that must be reviewed in the document</p>
            </div>
        </nav>
    )
}

export default sidebar