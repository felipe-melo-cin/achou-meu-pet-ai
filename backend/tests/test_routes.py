import pytest
import json
from unittest.mock import patch
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


# ─── Health check ────────────────────────────────────────────────

def test_health_endpoint(client):
    """GET /api/health deve retornar status ok."""
    resp = client.get("/api/health")
    assert resp.status_code == 200
    assert resp.get_json() == {"status": "ok"}


# ─── /api/pets/search ────────────────────────────────────────────

class TestSearchRoute:

    def test_retorna_400_sem_imagem(self, client):
        """POST /api/pets/search sem campo 'image' deve retornar 400."""
        resp = client.post("/api/pets/search",
                           data=json.dumps({}),
                           content_type="application/json")
        assert resp.status_code == 400
        assert "error" in resp.get_json()

    @patch("routes.pets.generate_embedding", return_value=[0.1] * 1536)
    @patch("routes.pets.search_similar_pets", return_value=[{"id": "1", "species": "Gato"}])
    def test_retorna_matches_quando_imagem_enviada(self, mock_search, mock_embed, client):
        """POST /api/pets/search com imagem válida deve retornar lista de matches."""
        resp = client.post("/api/pets/search",
                           data=json.dumps({"image": "base64_fake"}),
                           content_type="application/json")
        assert resp.status_code == 200
        body = resp.get_json()
        assert "matches" in body
        assert len(body["matches"]) == 1


# ─── /api/pets/analyze ───────────────────────────────────────────

class TestAnalyzeRoute:

    def test_retorna_400_sem_imagem(self, client):
        """POST /api/pets/analyze sem 'image' deve retornar 400."""
        resp = client.post("/api/pets/analyze",
                           data=json.dumps({}),
                           content_type="application/json")
        assert resp.status_code == 400

    @patch("routes.pets.pet_vision_analysis", return_value={
        "species": "Cachorro", "breed": "Poodle",
        "primaryColor": "Branco", "distinguishingMarks": ""
    })
    def test_retorna_analise_quando_imagem_valida(self, mock_vision, client):
        """POST /api/pets/analyze com imagem válida deve retornar análise."""
        resp = client.post("/api/pets/analyze",
                           data=json.dumps({"image": "base64_fake"}),
                           content_type="application/json")
        assert resp.status_code == 200
        body = resp.get_json()
        assert body["species"] == "Cachorro"


# ─── /api/auth/register ──────────────────────────────────────────

class TestAuthRegisterRoute:

    def test_retorna_400_sem_email(self, client):
        """POST /api/auth/register sem email deve retornar 400."""
        resp = client.post("/api/auth/register",
                           data=json.dumps({"senha": "123456"}),
                           content_type="application/json")
        assert resp.status_code == 400

    def test_retorna_400_senha_curta(self, client):
        """POST /api/auth/register com senha < 6 chars deve retornar 400."""
        resp = client.post("/api/auth/register",
                           data=json.dumps({"email": "a@b.com", "senha": "123"}),
                           content_type="application/json")
        assert resp.status_code == 400
        assert "6 caracteres" in resp.get_json()["error"]

    @patch("routes.auth.register_user", return_value={"user_id": "uuid-999"})
    def test_registro_bem_sucedido(self, mock_register, client):
        """POST /api/auth/register com dados válidos deve retornar success: true."""
        resp = client.post("/api/auth/register",
                           data=json.dumps({
                               "email": "novo@email.com",
                               "senha": "senha_valida",
                               "nome": "Lucas",
                           }),
                           content_type="application/json")
        assert resp.status_code == 200
        assert resp.get_json()["success"] is True
