import { useState } from 'react';;
import { ImageUpload } from './ImageUpload';
import { generateEmbedding } from '../services/models';
import { searchSimilarPets } from '../services/supabase';
import { Loader2, Search, Zap } from 'lucide-react';
import { motion } from 'motion/react';
import { MatchResult } from '../types';

interface SearchScreenProps {
  onResults: (results: MatchResult[]) => void;
}

export function SearchScreen({ onResults }: SearchScreenProps) {
  const [image, setImage] = useState<{ file: File; base64: string } | null>(null);
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState<string>('');

  const handleSearch = async () => {
    if (!image) return;

    setLoading(true);
    setStatus('Gerando assinatura visual do seu pet...');
    try {
      const base64Data = image.base64.split(',')[1];
      
      // 1. Generate Embedding
      const embedding = await generateEmbedding(base64Data);

      setStatus('Procurando no banco de dados (AI Match)...');
      
      // 2. Vector Search (> 70%)
      const matches = await searchSimilarPets(embedding || [], 0.7);
      
      onResults(matches);
    } catch (error: any) {
      console.error(error);
      setStatus(error.message || 'Erro na busca. Verifique se o banco de dados está configurado.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto p-6 space-y-8">
      <div className="text-center space-y-2">
        <h2 className="text-3xl font-bold text-slate-900">Procurar meu Pet</h2>
        <p className="text-slate-500">Envie uma foto do seu animal perdido para encontrarmos correspondências.</p>
      </div>

      <motion.div 
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        className="bg-white rounded-2xl shadow-xl shadow-slate-200/50 p-8 border border-slate-100 flex flex-col items-center gap-6"
      >
        <div className="w-full space-y-2 text-center">
            <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-orange-100 text-orange-700 text-xs font-bold uppercase tracking-wider">
                <Zap size={12} fill="currentColor" /> Busca Impulsionada por IA
            </span>
        </div>

        <ImageUpload 
          selectedImage={image?.base64} 
          onImageSelect={(file, base64) => setImage({ file, base64 })}
          onClear={() => setImage(null)}
          className="max-w-md"
        />

        {status && (
          <div className="flex items-center gap-2 text-sm text-slate-600 font-medium">
            <Loader2 size={16} className="animate-spin text-orange-500" />
            {status}
          </div>
        )}

        <button
          onClick={handleSearch}
          disabled={loading || !image}
          className="w-full max-w-md py-4 bg-slate-900 text-white rounded-xl font-bold text-lg hover:bg-slate-800 active:scale-[0.98] transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2 shadow-lg shadow-slate-900/20"
        >
          {loading ? <Loader2 className="animate-spin" /> : <Search />}
          Iniciar Busca Inteligente
        </button>
      </motion.div>

      <div className="bg-orange-50 border border-orange-100 p-4 rounded-xl">
        <p className="text-xs text-orange-800 leading-relaxed">
            <strong>Como funciona:</strong> Nossa rede neural cria uma "digital" única para a foto enviada e a compara com centenas de pets cadastrados, retornando aqueles com pelo menos 70% de similaridade visual.
        </p>
      </div>
    </div>
  );
}
