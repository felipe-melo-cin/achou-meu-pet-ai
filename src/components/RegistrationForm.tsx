import { useState } from 'react';
import { ImageUpload } from './ImageUpload';
import { petVisionAnalysis, generateEmbedding } from '../services/models';
import { uploadImage, registerPet } from '../services/supabase';
import { Loader2, CheckCircle2, PawPrint } from 'lucide-react';
import { motion } from 'motion/react';
import { cn } from '../lib/utils';

export function RegistrationForm() {
  const [image, setImage] = useState<{ file: File; base64: string } | null>(null);
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState<string>('');
  const [formData, setFormData] = useState({
    name: '',
    species: '',
    breed: '',
    color: '',
    description: '',
    lastLocation: '',
    contactInfo: '',
  });

  const handleImageSelect = async (file: File, base64: string) => {
    setImage({ file, base64 });
    setLoading(true);
    setStatus('Analisando foto com IA...');
    try {
      const base64Data = base64.split(',')[1];
      const analysis = await petVisionAnalysis(base64Data);
      setFormData(prev => ({
        ...prev,
        species: analysis.species || '',
        breed: analysis.breed || '',
        color: analysis.primaryColor || '',
        description: `Pet ${analysis.likelyMood}. Marcas: ${analysis.distinguishingMarks}`,
      }));
      setStatus('IA preencheu o formulário! Verifique os dados.');
    } catch (error) {
      console.error(error);
      setStatus('Erro na análise da IA. Por favor, preencha manualmente.');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!image) return;

    setLoading(true);
    setStatus('Salvando pet no sistema...');
    try {
      // 1. Upload Image to Storage
      const imageUrl = await uploadImage(image.file);
      
      // 2. Generate Embedding
      const base64Data = image.base64.split(',')[1];
      const embedding = await generateEmbedding(base64Data);

      // 3. Register in Database
      await registerPet({
        ...formData,
        imageUrl,
        embedding,
      });

      setStatus('Pet cadastrado com sucesso!');
      // Reset form
      setImage(null);
      setFormData({
        name: '',
        species: '',
        breed: '',
        color: '',
        description: '',
        lastLocation: '',
        contactInfo: '',
      });
    } catch (error: any) {
      console.error(error);
      setStatus(error.message || 'Erro ao salvar pet. Verifique sua conexão.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto p-6 space-y-8">
      <div className="text-center space-y-2">
        <h2 className="text-3xl font-bold text-slate-900">Cadastrar Pet Encontrado</h2>
        <p className="text-slate-500">Ajude um animal a voltar para casa. A IA ajudará a preencher os detalhes.</p>
      </div>

      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-white rounded-2xl shadow-xl shadow-slate-200/50 p-8 border border-slate-100"
      >
        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="space-y-2">
            <label className="text-sm font-semibold text-slate-700">Foto do Pet</label>
            <ImageUpload 
              selectedImage={image?.base64} 
              onImageSelect={handleImageSelect}
              onClear={() => setImage(null)}
            />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-2">
              <label className="text-sm font-semibold text-slate-700">Nome (se souber)</label>
              <input
                type="text"
                placeholder="Ex: Totó"
                value={formData.name}
                onChange={e => setFormData({ ...formData, name: e.target.value })}
                className="w-full px-4 py-2 rounded-lg border border-slate-200 focus:outline-none focus:ring-2 focus:ring-orange-500/20 focus:border-orange-500 transition-all text-slate-900"
              />
            </div>
            <div className="space-y-2">
              <label className="text-sm font-semibold text-slate-700">Espécie</label>
              <input
                type="text"
                required
                placeholder="Cachorro, Gato..."
                value={formData.species}
                onChange={e => setFormData({ ...formData, species: e.target.value })}
                className="w-full px-4 py-2 rounded-lg border border-slate-200 focus:outline-none focus:ring-2 focus:ring-orange-500/20 focus:border-orange-500 transition-all text-slate-900"
              />
            </div>
            <div className="space-y-2">
              <label className="text-sm font-semibold text-slate-700">Raça</label>
              <input
                type="text"
                placeholder="Ex: SRD, Poodle..."
                value={formData.breed}
                onChange={e => setFormData({ ...formData, breed: e.target.value })}
                className="w-full px-4 py-2 rounded-lg border border-slate-200 focus:outline-none focus:ring-2 focus:ring-orange-500/20 focus:border-orange-500 transition-all text-slate-900"
              />
            </div>
            <div className="space-y-2">
              <label className="text-sm font-semibold text-slate-700">Cor</label>
              <input
                type="text"
                placeholder="Ex: Marrom, Preto..."
                value={formData.color}
                onChange={e => setFormData({ ...formData, color: e.target.value })}
                className="w-full px-4 py-2 rounded-lg border border-slate-200 focus:outline-none focus:ring-2 focus:ring-orange-500/20 focus:border-orange-500 transition-all text-slate-900"
              />
            </div>
          </div>

          <div className="space-y-2">
            <label className="text-sm font-semibold text-slate-700">Localização do Encontro</label>
            <input
              type="text"
              required
              placeholder="Rua, Bairro, Cidade..."
              value={formData.lastLocation}
              onChange={e => setFormData({ ...formData, lastLocation: e.target.value })}
              className="w-full px-4 py-2 rounded-lg border border-slate-200 focus:outline-none focus:ring-2 focus:ring-orange-500/20 focus:border-orange-500 transition-all text-slate-900"
            />
          </div>

          <div className="space-y-2">
            <label className="text-sm font-semibold text-slate-700">Sua Informação de Contato</label>
            <input
              type="text"
              required
              placeholder="Telefone ou Instagram"
              value={formData.contactInfo}
              onChange={e => setFormData({ ...formData, contactInfo: e.target.value })}
              className="w-full px-4 py-2 rounded-lg border border-slate-200 focus:outline-none focus:ring-2 focus:ring-orange-500/20 focus:border-orange-500 transition-all text-slate-900"
            />
          </div>

          <div className="space-y-2">
            <label className="text-sm font-semibold text-slate-700">Descrição/Detalhes Adicionais</label>
            <textarea
              rows={3}
              placeholder="Detalhes sobre coleira, comportamento..."
              value={formData.description}
                onChange={e => setFormData({ ...formData, description: e.target.value })}
              className="w-full px-4 py-2 rounded-lg border border-slate-200 focus:outline-none focus:ring-2 focus:ring-orange-500/20 focus:border-orange-500 transition-all text-slate-900 resize-none"
            />
          </div>

          {status && (
            <div className={cn(
              "p-3 rounded-lg flex items-center gap-2 text-sm font-medium",
              status.includes('sucesso') ? "bg-green-50 text-green-700" : "bg-blue-50 text-blue-700"
            )}>
              {status.includes('sucesso') ? <CheckCircle2 size={16} /> : <Loader2 size={16} className="animate-spin" />}
              {status}
            </div>
          )}

          <button
            type="submit"
            disabled={loading || !image}
            className="w-full py-4 bg-orange-500 text-white rounded-xl font-bold text-lg hover:bg-orange-600 active:scale-[0.98] transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2 shadow-lg shadow-orange-500/30"
          >
            {loading ? <Loader2 className="animate-spin" /> : <PawPrint />}
            Registrar Pet
          </button>
        </form>
      </motion.div>
    </div>
  );
}
