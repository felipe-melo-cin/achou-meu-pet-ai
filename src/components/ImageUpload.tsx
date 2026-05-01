import { useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { Upload, X, MousePointer2 } from 'lucide-react';
import { cn } from '../lib/utils';

interface ImageUploadProps {
  onImageSelect: (file: File, base64: string) => void;
  selectedImage?: string;
  onClear: () => void;
  className?: string;
}

export function ImageUpload({ onImageSelect, selectedImage, onClear, className }: ImageUploadProps) {
  const onDrop = useCallback((acceptedFiles: File[]) => {
    const file = acceptedFiles[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        onImageSelect(file, reader.result as string);
      };
      reader.readAsDataURL(file);
    }
  }, [onImageSelect]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { 'image/*': [] },
    multiple: false,
  } as any);

  return (
    <div className={cn("w-full", className)}>
      {!selectedImage ? (
        <div
          {...getRootProps()}
          className={cn(
            "border-2 border-dashed rounded-xl p-8 transition-all cursor-pointer flex flex-col items-center justify-center gap-3",
            isDragActive ? "border-orange-500 bg-orange-50" : "border-slate-300 hover:border-orange-400 hover:bg-slate-50"
          )}
        >
          <input {...getInputProps()} />
          <div className="p-3 rounded-full bg-orange-100 text-orange-600">
            <Upload size={24} />
          </div>
          <div className="text-center">
            <p className="font-medium text-slate-900">Clique ou arraste uma foto</p>
            <p className="text-sm text-slate-500">PNG, JPG ou JPEG (máx. 5MB)</p>
          </div>
        </div>
      ) : (
        <div className="relative rounded-xl overflow-hidden group">
          <img
            src={selectedImage}
            alt="Pet preview"
            className="w-full aspect-video object-cover"
          />
          <button
            onClick={(e) => {
              e.stopPropagation();
              onClear();
            }}
            className="absolute top-2 right-2 p-1.5 bg-black/50 text-white rounded-full hover:bg-black/70 transition-colors"
          >
            <X size={18} />
          </button>
        </div>
      )}
    </div>
  );
}
