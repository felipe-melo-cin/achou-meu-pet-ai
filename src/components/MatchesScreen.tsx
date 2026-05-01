import { useCallback } from 'react';
import { MatchResult } from '../types';
import { motion } from 'motion/react';
import { MessageCircle, MapPin, Tag, ArrowLeft } from 'lucide-react';

interface MatchesScreenProps {
  results: MatchResult[];
  onBack: () => void;
}

export function MatchesScreen({ results, onBack }: MatchesScreenProps) {
  return (
    <div className="max-w-4xl mx-auto p-6 space-y-8">
      <div className="flex items-center justify-between">
        <button 
          onClick={onBack}
          className="flex items-center gap-2 text-slate-600 hover:text-slate-900 transition-colors font-medium"
        >
          <ArrowLeft size={20} /> Voltar para busca
        </button>
        <div className="text-right">
           <h2 className="text-2xl font-bold text-slate-900">Resultados Encontrados</h2>
           <p className="text-slate-500 text-sm">{results.length} possíveis correspondências</p>
        </div>
      </div>

      {results.length === 0 ? (
        <div className="text-center py-20 bg-slate-50 rounded-3xl border-2 border-dashed border-slate-200">
          <div className="mx-auto w-16 h-16 bg-slate-200 rounded-full flex items-center justify-center text-slate-400 mb-4">
            <Search size={32} />
          </div>
          <p className="text-slate-600 font-medium">Nenhum pet similar encontrado no momento.</p>
          <p className="text-slate-400 text-sm">Tente uma foto diferente ou com melhor iluminação.</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {results.map((pet, index) => (
            <motion.div
              key={pet.id || index}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
              className="bg-white rounded-2xl overflow-hidden shadow-md hover:shadow-xl transition-all border border-slate-100 group"
            >
              <div className="relative aspect-video overflow-hidden">
                <img 
                  src={pet.imageUrl} 
                  alt={pet.name || 'Pet'} 
                  className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                />
                <div className="absolute top-3 right-3 bg-orange-500 text-white text-xs font-bold px-2 py-1 rounded-full shadow-lg">
                  {Math.round(pet.similarity * 100)}% Match
                </div>
              </div>
              
              <div className="p-5 space-y-4">
                <div>
                  <h3 className="text-xl font-bold text-slate-900">{pet.name || 'Pet sem nome'}</h3>
                  <div className="flex flex-wrap gap-2 mt-2">
                    <span className="flex items-center gap-1 text-xs bg-slate-100 text-slate-700 px-2 py-1 rounded-md">
                      <Tag size={12} /> {pet.breed}
                    </span>
                    <span className="flex items-center gap-1 text-xs bg-slate-100 text-slate-700 px-2 py-1 rounded-md">
                      <Tag size={12} /> {pet.color}
                    </span>
                  </div>
                </div>

                <div className="space-y-2 text-sm text-slate-600">
                  <p className="flex items-start gap-2">
                    <MapPin size={16} className="text-orange-500 shrink-0 mt-0.5" />
                    <span>{pet.lastLocation}</span>
                  </p>
                  <p className="line-clamp-2 italic italic opacity-80">{pet.description}</p>
                </div>

                <div className="pt-4 border-t border-slate-50">
                  <a 
                    href={`https://wa.me/${pet.contactInfo.replace(/\D/g, '')}`}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="w-full py-3 bg-green-500 text-white rounded-xl font-bold flex items-center justify-center gap-2 hover:bg-green-600 transition-colors"
                  >
                    <MessageCircle size={18} /> Entrar em Contato
                  </a>
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      )}
    </div>
  );
}

// Fixed import
import { Search } from 'lucide-react';
