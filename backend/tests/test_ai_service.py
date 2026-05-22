import pytest
import json
from unittest.mock import MagicMock, patch


# ─── Testes de pet_vision_analysis ───────────────────────────────

class TestPetVisionAnalysis:

    def _make_mock_client(self, content: str):
        """Monta um cliente OpenAI mockado que retorna 'content' como resposta."""
        mock_message = MagicMock()
        mock_message.content = content
        mock_choice = MagicMock()
        mock_choice.message = mock_message
        mock_response = MagicMock()
        mock_response.choices = [mock_choice]
        return mock_response

    @patch("services.ai_service.client")
    def test_retorna_dict_com_campos_esperados(self, mock_client):
        """Deve retornar dict com species, breed, primaryColor e distinguishingMarks."""
        payload = {
            "species": "Cachorro",
            "breed": "Golden Retriever",
            "primaryColor": "Dourado",
            "distinguishingMarks": "Mancha branca no peito",
        }
        mock_client.chat.completions.create.return_value = self._make_mock_client(
            json.dumps(payload)
        )

        from services.ai_service import pet_vision_analysis
        result = pet_vision_analysis("base64_fake")

        assert result["species"] == "Cachorro"
        assert result["breed"] == "Golden Retriever"
        assert result["primaryColor"] == "Dourado"

    @patch("services.ai_service.client")
    def test_limpa_markdown_do_json(self, mock_client):
        """Deve remover blocos ```json``` que o modelo às vezes inclui."""
        payload = {"species": "Gato", "breed": "Persa", "primaryColor": "Branco", "distinguishingMarks": ""}
        raw = f"```json\n{json.dumps(payload)}\n```"
        mock_client.chat.completions.create.return_value = self._make_mock_client(raw)

        from services.ai_service import pet_vision_analysis
        result = pet_vision_analysis("base64_fake")

        assert result["species"] == "Gato"

    @patch("services.ai_service.client")
    def test_levanta_erro_quando_conteudo_vazio(self, mock_client):
        """Deve lançar ValueError se a IA retornar conteúdo vazio."""
        mock_client.chat.completions.create.return_value = self._make_mock_client(None)

        from services.ai_service import pet_vision_analysis
        with pytest.raises(ValueError, match="IA não retornou conteúdo"):
            pet_vision_analysis("base64_fake")

    @patch("services.ai_service.client")
    def test_levanta_erro_para_json_invalido(self, mock_client):
        """Deve lançar json.JSONDecodeError se a resposta não for JSON válido."""
        mock_client.chat.completions.create.return_value = self._make_mock_client(
            "Isso não é JSON"
        )

        from services.ai_service import pet_vision_analysis
        with pytest.raises(json.JSONDecodeError):
            pet_vision_analysis("base64_fake")


# ─── Testes de generate_embedding ────────────────────────────────

class TestGenerateEmbedding:

    @patch("services.ai_service.client")
    def test_retorna_lista_de_floats(self, mock_client):
        """Deve retornar uma lista de floats (o vetor de embedding)."""
        vision_payload = {
            "species": "Cachorro", "breed": "Vira-lata",
            "primaryColor": "Preto", "distinguishingMarks": "",
        }
        mock_vision_resp = MagicMock()
        mock_vision_resp.choices = [MagicMock()]
        mock_vision_resp.choices[0].message.content = json.dumps(vision_payload)

        mock_embedding_obj = MagicMock()
        mock_embedding_obj.embedding = [0.1, 0.2, 0.3]
        mock_embed_resp = MagicMock()
        mock_embed_resp.data = [mock_embedding_obj]

        mock_client.chat.completions.create.return_value = mock_vision_resp
        mock_client.embeddings.create.return_value = mock_embed_resp

        from services.ai_service import generate_embedding
        result = generate_embedding("base64_fake")

        assert isinstance(result, list)
        assert result == [0.1, 0.2, 0.3]

    @patch("services.ai_service.client")
    def test_texto_concatenado_correto(self, mock_client):
        """O texto enviado ao modelo de embedding deve combinar todos os campos do pet."""
        vision_payload = {
            "species": "Gato", "breed": "Siamês",
            "primaryColor": "Creme", "distinguishingMarks": "Olhos azuis",
        }
        mock_vision_resp = MagicMock()
        mock_vision_resp.choices = [MagicMock()]
        mock_vision_resp.choices[0].message.content = json.dumps(vision_payload)

        mock_embedding_obj = MagicMock()
        mock_embedding_obj.embedding = [0.5] * 1536
        mock_embed_resp = MagicMock()
        mock_embed_resp.data = [mock_embedding_obj]

        mock_client.chat.completions.create.return_value = mock_vision_resp
        mock_client.embeddings.create.return_value = mock_embed_resp

        from services.ai_service import generate_embedding
        generate_embedding("base64_fake")

        call_args = mock_client.embeddings.create.call_args
        input_text = call_args.kwargs.get("input") or call_args.args[0]
        assert "Gato" in input_text
        assert "Siamês" in input_text
        assert "Olhos azuis" in input_text
