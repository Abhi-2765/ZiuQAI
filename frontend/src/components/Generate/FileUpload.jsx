import { useRef, useState } from "react";
import { UploadCloud, File, X, Check } from "lucide-react";

export default function FileUpload() {
    const [files, setFiles] = useState([]);
    const [dragActive, setDragActive] = useState(false);
    const [uploading, setUploading] = useState(false);
    const inputRef = useRef(null);

    const handleDrag = (e) => {
        e.preventDefault();
        e.stopPropagation();
        if (e.type === "dragenter" || e.type === "dragover") {
            setDragActive(true);
        } else if (e.type === "dragleave") {
            setDragActive(false);
        }
    };

    const handleDrop = (e) => {
        e.preventDefault();
        e.stopPropagation();
        setDragActive(false);
        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            handleFiles(e.dataTransfer.files);
        }
    };

    const handleChange = (e) => {
        e.preventDefault();
        if (e.target.files && e.target.files[0]) {
            handleFiles(e.target.files);
        }
    };

    const handleFiles = (selectedFiles) => {
        const newFiles = Array.from(selectedFiles).map((file) => ({
            id: crypto.randomUUID(),
            file,
            name: file.name,
            size: (file.size / 1024 / 1024).toFixed(2) + " MB",
            progress: 0,
            uploaded: false
        }));
        setFiles((prev) => [...prev, ...newFiles]);
    };

    const handleRemove = (id) => {
        setFiles((prev) => prev.filter((f) => f.id !== id));
    };

    const handleUpload = () => {
        if (files.length === 0 || uploading) return;
        setUploading(true);

        const uploadFile = (fileId) =>
            new Promise((resolve) => {
                let progress = 0;
                const interval = setInterval(() => {
                    progress += Math.random() * 30;
                    if (progress >= 100) progress = 100;

                    setFiles((prev) =>
                        prev.map((f) =>
                            f.id === fileId ? { ...f, progress } : f
                        )
                    );

                    if (progress === 100) {
                        clearInterval(interval);
                        setFiles((prev) =>
                            prev.map((f) =>
                                f.id === fileId ? { ...f, uploaded: true } : f
                            )
                        );
                        resolve();
                    }
                }, 400);
            });

        Promise.all(files.filter(f => !f.uploaded).map(f => uploadFile(f.id)))
            .then(() => setUploading(false));
    };

    return (
        <div className="h-full flex flex-col">
            {/* Drop Zone */}
            <div
                className={`
                    flex-1 flex flex-col items-center justify-center
                    border-2 border-dashed rounded-xl transition-all duration-200 mt-2
                    ${dragActive
                        ? "border-indigo-500 bg-indigo-50 dark:bg-indigo-900/10"
                        : "border-slate-300 dark:border-slate-700 bg-slate-50 dark:bg-slate-900/50"}
                `}
                onDragEnter={handleDrag}
                onDragLeave={handleDrag}
                onDragOver={handleDrag}
                onDrop={handleDrop}
            >
                <input
                    ref={inputRef}
                    type="file"
                    multiple
                    className="hidden"
                    onChange={handleChange}
                    accept=".pdf,.doc,.docx,.txt,.png,.jpg,.jpeg"
                />

                <div className="text-center p-8">
                    <div className="w-16 h-16 bg-indigo-100 dark:bg-indigo-900/30 text-indigo-600 dark:text-indigo-400 rounded-full flex items-center justify-center mx-auto mb-4">
                        <UploadCloud size={32} />
                    </div>
                    <p className="text-lg font-semibold text-slate-700 dark:text-slate-200">
                        Select a file or drag and drop here
                    </p>
                    <p className="text-sm text-slate-500 dark:text-slate-400 mt-2 mb-6">
                        JPG, PNG or PDF file size no more than 10MB
                    </p>
                    <button
                        onClick={() => inputRef.current?.click()}
                        className="px-6 py-2.5 rounded-xl bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-slate-700 dark:text-slate-300 font-semibold shadow-sm hover:bg-slate-50 dark:hover:bg-slate-700 transition"
                    >
                        Select Files
                    </button>
                </div>
            </div>

            {/* File List */}
            {files.length > 0 && (
                <div className="mt-6 space-y-3">
                    <div className="flex items-center justify-between mb-2">
                        <p className="text-sm font-semibold text-slate-500 uppercase tracking-wider">
                            Attached Files
                        </p>
                        <button
                            onClick={handleUpload}
                            disabled={uploading || files.every(f => f.uploaded)}
                            className="text-sm font-bold text-indigo-600 hover:text-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed"
                        >
                            {uploading ? "Uploading..." : "Upload All"}
                        </button>
                    </div>

                    {files.map((file) => (
                        <FileCard
                            key={file.id}
                            file={file}
                            onRemove={handleRemove}
                            uploading={uploading}
                        />
                    ))}
                </div>
            )}
        </div>
    );
}

function FileCard({ file, onRemove, uploading }) {
    return (
        <div className="bg-white dark:bg-slate-800 p-4 rounded-xl border border-slate-200 dark:border-slate-700 shadow-sm flex items-center gap-4">
            <div className="w-10 h-10 rounded-lg bg-indigo-50 dark:bg-indigo-900/20 flex items-center justify-center text-indigo-600 dark:text-indigo-400">
                <File size={20} />
            </div>

            <div className="flex-1 min-w-0">
                <div className="flex justify-between mb-1">
                    <p className="text-sm font-medium text-slate-700 dark:text-slate-200 truncate">
                        {file.name}
                    </p>
                    <p className="text-xs text-slate-500">{file.size}</p>
                </div>

                <div className="h-1.5 w-full bg-slate-100 dark:bg-slate-700 rounded-full overflow-hidden">
                    <div
                        className={`h-full transition-all duration-300 ${file.uploaded ? "bg-green-500" : "bg-indigo-600"
                            }`}
                        style={{ width: `${file.uploaded ? 100 : file.progress}%` }}
                    />
                </div>
            </div>

            <button
                onClick={() => onRemove(file.id)}
                disabled={uploading}
                className="text-slate-400 hover:text-red-500 transition p-1"
            >
                {file.uploaded
                    ? <Check size={20} className="text-green-500" />
                    : <X size={20} />}
            </button>
        </div>
    );
}
