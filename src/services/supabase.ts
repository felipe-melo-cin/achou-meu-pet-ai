import { createClient } from '@supabase/supabase-js';
import type { PetData } from '../types';

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL;
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY;

if (!supabaseUrl || !supabaseAnonKey) {
  throw new Error('Supabase configuration missing. Please provide VITE_SUPABASE_URL and VITE_SUPABASE_ANON_KEY.');
}

// Inicializa de forma síncrona uma única vez
export const supabase = createClient(supabaseUrl, supabaseAnonKey);

// Agora suas funções não precisam mais de getSupabase()!
export async function uploadImage(file: File) {
  const fileExt = file.name.split('.').pop();
  const fileName = `${Math.random()}.${fileExt}`;
  const filePath = `pets/${fileName}`;

  const { error } = await supabase.storage
    .from('pet_images')
    .upload(filePath, file);

  if (error) {
    if (error.message.includes('Bucket not found')) {
      throw new Error('Bucket "pet-images" não encontrado. Por favor, crie um bucket PÚBLICO chamado "pet-images" no seu console do Supabase (Storage).');
    }
    throw error;
  }
  
  const { data: { publicUrl } } = supabase.storage
    .from('pet_images')
    .getPublicUrl(filePath);

  return publicUrl;
}

export async function registerPet(pet: PetData) {
  const { data, error } = await supabase
    .from('pets')
    .insert([pet])
    .select();

  if (error) throw error;
  return data ? data[0] : null;
}

export async function searchSimilarPets(vector: number[], threshold = 0.7) {
  const { data, error } = await supabase.rpc('match_pets', {
    query_embedding: vector,
    match_threshold: threshold,
    match_count: 10,
  });

  if (error) throw error;
  return data;
}