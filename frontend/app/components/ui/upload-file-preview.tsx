import { XCircleIcon } from "lucide-react";
import { cn } from "./lib/utils";

const uploadFilePreview = ({
    url,
    onRemove,
}: {
    url: string;
    onRemove: () => void;
}) => {
    return (
        <div className="mb-2 select-none relative group">
            <embed type="application/pdf" src={url} width="500" height="150" className="w-full" />
            <div
                className={cn(
                    "absolute top-2 right-8 w-6 h-6 z-10 bg-red-500 text-white rounded-full hidden group-hover:block",
                )}
            >
                <XCircleIcon
                    className="w-8 h-8 bg-red-500 text-white rounded-full"
                    onClick={onRemove}
                />
            </div>
        </div>
    )
}

export default uploadFilePreview