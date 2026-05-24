import pytest
from unittest.mock import MagicMock, patch


# ─── Testes de register_pet ──────────────────────────────────────

class TestRegisterPet:

    @patch("services.supabase_service.supabase")
    def test_insere_somente_colunas_permitidas(self, mock_sb):
        """Deve filtrar campos inválidos antes de inserir no banco."""
        mock_execute = MagicMock()
        mock_execute.data = [{"id": "abc", "species": "Cachorro"}]
        mock_sb.table.return_value.insert.return_value.execute.return_value = mock_execute

        from services.supabase_service import register_pet
        pet_data = {
            "species": "Cachorro",
            "breed": "Labrador",
            "campoInvalido": "não deveria ir",
        }
        result = register_pet(pet_data)

        inserted = mock_sb.table.return_value.insert.call_args[0][0]
        assert "campoInvalido" not in inserted
        assert inserted["species"] == "Cachorro"

    @patch("services.supabase_service.supabase")
    def test_retorna_dict_vazio_quando_data_vazio(self, mock_sb):
        """Deve retornar {} se o Supabase não devolver nenhum registro."""
        mock_execute = MagicMock()
        mock_execute.data = []
        mock_sb.table.return_value.insert.return_value.execute.return_value = mock_execute

        from services.supabase_service import register_pet
        result = register_pet({"species": "Gato"})

        assert result == {}


# ─── Testes de list_pets ─────────────────────────────────────────

class TestListPets:

    @patch("services.supabase_service.supabase")
    def test_normaliza_created_at_para_createdAt(self, mock_sb):
        """Deve renomear created_at → createdAt para compatibilidade com o frontend."""
        mock_execute = MagicMock()
        mock_execute.data = [{"id": "1", "species": "Cachorro", "color": "Preto", "created_at": "2024-01-01"}]
        (mock_sb.table.return_value
            .select.return_value
            .order.return_value
            .limit.return_value
            .execute.return_value) = mock_execute

        from services.supabase_service import list_pets
        result = list_pets()

        assert "createdAt" in result[0]
        assert "created_at" not in result[0]

    @patch("services.supabase_service.supabase")
    def test_mapeia_color_para_primaryColor(self, mock_sb):
        """Deve adicionar primaryColor como alias de color."""
        mock_execute = MagicMock()
        mock_execute.data = [{"id": "1", "color": "Dourado", "created_at": "2024-01-01"}]
        (mock_sb.table.return_value
            .select.return_value
            .order.return_value
            .limit.return_value
            .execute.return_value) = mock_execute

        from services.supabase_service import list_pets
        result = list_pets()

        assert result[0]["primaryColor"] == "Dourado"

    @patch("services.supabase_service.supabase")
    def test_retorna_lista_vazia_quando_nao_ha_pets(self, mock_sb):
        """Deve retornar lista vazia sem erros quando não há registros."""
        mock_execute = MagicMock()
        mock_execute.data = None
        (mock_sb.table.return_value
            .select.return_value
            .order.return_value
            .limit.return_value
            .execute.return_value) = mock_execute

        from services.supabase_service import list_pets
        result = list_pets()

        assert result == []


# ─── Testes de search_similar_pets ───────────────────────────────

class TestSearchSimilarPets:

    @patch("services.supabase_service.supabase")
    def test_chama_rpc_com_parametros_corretos(self, mock_sb):
        """Deve chamar match_pets com query_embedding, match_threshold e match_count."""
        mock_execute = MagicMock()
        mock_execute.data = []
        mock_sb.rpc.return_value.execute.return_value = mock_execute

        from services.supabase_service import search_similar_pets
        embedding = [0.1] * 1536
        search_similar_pets(embedding, threshold=0.7, limit=5)

        mock_sb.rpc.assert_called_once_with("match_pets", {
            "query_embedding": embedding,
            "match_threshold": 0.7,
            "match_count": 5,
        })


# ─── Testes de login_user ────────────────────────────────────────

class TestLoginUser:

    @patch("services.supabase_service.supabase")
    def test_retorna_access_token_e_user_id(self, mock_sb):
        """Deve retornar access_token, user_id e nome do usuário."""
        mock_user = MagicMock()
        mock_user.id = "uuid-123"
        mock_user.user_metadata = {"nome": "Ana"}
        mock_session = MagicMock()
        mock_session.access_token = "token_abc"
        mock_response = MagicMock()
        mock_response.session = mock_session
        mock_response.user = mock_user
        mock_sb.auth.sign_in_with_password.return_value = mock_response

        from services.supabase_service import login_user
        result = login_user("ana@email.com", "senha123")

        assert result["access_token"] == "token_abc"
        assert result["user_id"] == "uuid-123"
        assert result["nome"] == "Ana"

    @patch("services.supabase_service.supabase")
    def test_levanta_erro_quando_sessao_invalida(self, mock_sb):
        """Deve lançar ValueError quando credenciais são inválidas."""
        mock_response = MagicMock()
        mock_response.session = None
        mock_sb.auth.sign_in_with_password.return_value = mock_response

        from services.supabase_service import login_user
        with pytest.raises(ValueError, match="Email ou senha incorretos"):
            login_user("errado@email.com", "senhaerrada")

# Adicione suporte para testar as funções em falta:
class TestMissingSupabaseServices:
    @patch("services.supabase_service.supabase")
    def test_upload_image_sucesso(self, mock_sb):
        from services.supabase_service import upload_image
        mock_sb.storage.from_().get_public_url.return_value = "https://fake-url.com/img.jpg"
        url = upload_image(b"fakebytes", "jpg")
        assert url == "https://fake-url.com/img.jpg"

    @patch("services.supabase_service.supabase")
    def test_register_user_sucesso(self, mock_sb):
        from services.supabase_service import register_user
        mock_user = MagicMock()
        mock_user.id = "user-uuid-999"
        mock_sb.auth.sign_up.return_value.user = mock_user
        
        res = register_user("test@email.com", "senha123", {"nome": "Teste"})
        assert res["user_id"] == "user-uuid-999"
