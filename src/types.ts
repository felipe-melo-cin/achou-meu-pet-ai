export interface PetData {
  id?: string;
  name?: string;
  species: string;
  breed: string;
  color: string;
  description: string;
  lastLocation: string;
  contactInfo: string;
  imageUrl: string;
  embedding?: number[];
  createdAt?: string;
}

export interface MatchResult extends PetData {
  similarity: number;
}
