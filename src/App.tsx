import { useState } from 'react';
import { RegistrationForm } from './components/RegistrationForm';
import { SearchScreen } from './components/SearchScreen';
import { MatchesScreen } from './components/MatchesScreen';
import { MatchResult } from './types';
import { PawPrint, Search, Info, HelpCircle } from 'lucide-react';
import { cn } from './lib/utils';
import { motion, AnimatePresence } from 'motion/react';

type Screen = 'registration' | 'search' | 'matches';

export default function App() {
  const [currentScreen, setCurrentScreen] = useState<Screen>('registration');
  const [searchResults, setSearchResults] = useState<MatchResult[]>([]);

  const handleSearchResults = (results: MatchResult[]) => {
    setSearchResults(results);
    setCurrentScreen('matches');
  };

  const [showHelp, setShowHelp] = useState(false);

  return (
    <div className="min-h-screen bg-[#F8FAFC] text-slate-900 font-sans">
      {/* Help Modal */}
      <AnimatePresence>
        {showHelp && (
          <div className="fixed inset-0 z-[100] flex items-center justify-center p-6 sm:p-12">
            <motion.div 
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              onClick={() => setShowHelp(false)}
              className="absolute inset-0 bg-slate-900/60 backdrop-blur-sm"
            />
            <motion.div 
              initial={{ opacity: 0, scale: 0.9, y: 20 }}
              animate={{ opacity: 1, scale: 1, y: 0 }}
              exit={{ opacity: 0, scale: 0.9, y: 20 }}
              className="relative bg-white w-full max-w-2xl max-h-[80vh] rounded-3xl shadow-2xl overflow-y-auto p-8"
            >
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-2xl font-bold flex items-center gap-2">
                  <Info className="text-orange-500" /> Guia de Configuração
                </h2>
                <button 
                  onClick={() => setShowHelp(false)}
                  className="p-2 hover:bg-slate-100 rounded-full transition-colors"
                >
                  <Search className="rotate-45" size={20} />
                </button>
              </div>

              <div className="space-y-6">
                <section className="space-y-3">
                  <h3 className="font-bold text-slate-800 flex items-center gap-2">
                    <div className="w-6 h-6 rounded-full bg-orange-100 text-orange-600 flex items-center justify-center text-xs">1</div>
                    Storage (Imagens)
                  </h3>
                  <p className="text-sm text-slate-600">
                    Crie um bucket <strong>público</strong> no Supabase chamado <code className="bg-slate-100 px-1.5 py-0.5 rounded text-orange-600 font-mono">pet-images</code>.
                  </p>
                </section>

                <section className="space-y-3">
                  <h3 className="font-bold text-slate-800 flex items-center gap-2">
                    <div className="w-6 h-6 rounded-full bg-orange-100 text-orange-600 flex items-center justify-center text-xs">2</div>
                    Database (SQL)
                  </h3>
                  <p className="text-sm text-slate-600">
                    Execute o seguinte SQL no <strong>SQL Editor</strong> do seu projeto Supabase:
                  </p>
                  <pre className="bg-slate-900 text-slate-300 p-4 rounded-xl text-[10px] overflow-x-auto font-mono leading-relaxed">
{`-- Habilitar extensão de vetores
create extension if not exists vector;

-- Tabela de Pets
create table pets (
  id uuid primary key default gen_random_uuid(),
  name text,
  species text not null,
  breed text,
  color text,
  description text,
  lastLocation text,
  contactInfo text,
  imageUrl text,
  embedding vector(768),
  createdAt timestamp with time zone default now()
);

-- Função de Busca Recompensada (Match Vetorial)
create or replace function match_pets (
  query_embedding vector(768),
  match_threshold float,
  match_count int
)
returns table (
  id uuid,
  name text,
  species text,
  breed text,
  color text,
  description text,
  lastLocation text,
  contactInfo text,
  imageUrl text,
  similarity float
)
language plpgsql
as $$
begin
  return query
  select
    pets.id,
    pets.name,
    pets.species,
    pets.breed,
    pets.color,
    pets.description,
    pets.lastLocation,
    pets.contactInfo,
    pets.imageUrl,
    1 - (pets.embedding <=> query_embedding) as similarity
  from pets
  where 1 - (pets.embedding <=> query_embedding) > match_threshold
  order by pets.embedding <=> query_embedding
  limit match_count;
end;
$$;`}
                  </pre>
                </section>
              </div>

              <button 
                onClick={() => setShowHelp(false)}
                className="w-full mt-8 py-3 bg-orange-500 text-white font-bold rounded-xl hover:bg-orange-600 transition-colors"
              >
                Entendi, tudo pronto!
              </button>
            </motion.div>
          </div>
        )}
      </AnimatePresence>

      {/* Header */}
      <header className="sticky top-0 z-50 bg-white/80 backdrop-blur-md border-b border-slate-100">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
             <div className="bg-orange-500 p-2 rounded-xl text-white">
                <PawPrint size={24} />
             </div>
             <h1 className="font-extrabold text-xl tracking-tight hidden sm:block">
                Achou Meu Pet <span className="text-orange-500">AI</span>
             </h1>
          </div>

          <nav className="flex items-center bg-slate-100 p-1 rounded-full border border-slate-200">
            <button
              onClick={() => setCurrentScreen('registration')}
              className={cn(
                "px-6 py-2 rounded-full text-sm font-bold transition-all flex items-center gap-2",
                currentScreen === 'registration' 
                  ? "bg-white text-orange-600 shadow-sm" 
                  : "text-slate-500 hover:text-slate-700"
              )}
            >
              <PawPrint size={16} /> Cadastrar
            </button>
            <button
              onClick={() => setCurrentScreen('search')}
              className={cn(
                "px-6 py-2 rounded-full text-sm font-bold transition-all flex items-center gap-2",
                currentScreen !== 'registration' 
                  ? "bg-white text-orange-600 shadow-sm" 
                  : "text-slate-500 hover:text-slate-700"
              )}
            >
              <Search size={16} /> Procurar
            </button>
          </nav>

          <div className="flex items-center gap-2">
             <button 
               onClick={() => setShowHelp(true)}
               className="p-2 text-slate-400 hover:text-slate-600 transition-colors"
             >
                <HelpCircle size={20} />
             </button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="py-8 px-6">
        <AnimatePresence mode="wait">
          {currentScreen === 'registration' && (
            <motion.div
              key="registration"
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: 20 }}
              transition={{ duration: 0.2 }}
            >
              <RegistrationForm />
            </motion.div>
          )}

          {currentScreen === 'search' && (
            <motion.div
              key="search"
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: 20 }}
              transition={{ duration: 0.2 }}
            >
              <SearchScreen onResults={handleSearchResults} />
            </motion.div>
          )}

          {currentScreen === 'matches' && (
            <motion.div
              key="matches"
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: 20 }}
              transition={{ duration: 0.2 }}
            >
              <MatchesScreen 
                results={searchResults} 
                onBack={() => setCurrentScreen('search')} 
              />
            </motion.div>
          )}
        </AnimatePresence>
      </main>

      {/* Footer info */}
      <footer className="max-w-7xl mx-auto px-6 py-12 border-t border-slate-100 mt-20">
         <div className="grid grid-cols-1 md:grid-cols-3 gap-12">
            <div className="space-y-4">
               <div className="flex items-center gap-2 text-orange-600">
                  <PawPrint size={20} />
                  <span className="font-bold">Achou Meu Pet AI</span>
               </div>
               <p className="text-slate-500 text-sm leading-relaxed">
                  Utilizamos o Vision AI e Embeddings para conectar animais perdidos aos seus donos através de reconhecimento visual avançado.
               </p>
            </div>
          
            <div className="space-y-4 text-right">
               <p className="text-slate-400 text-xs">
                  © 2026 Achou Meu Pet AI.
               </p>
            </div>
         </div>
      </footer>
    </div>
  );
}
