
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


# TESTES BÁSICOS DA API

def test_home():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "AI Quality Lab funcionando!",
        "status": "success"
    }


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy"
    }


def test_rota_inexistente():
    response = client.get("/rota-que-nao-existe")

    assert response.status_code == 404


# TESTES DE AVALIAÇÃO DE RESPOSTA

def test_evaluate_empty_response():
    response = client.post(
        "/evaluate",
        json={"response": "   "}
    )

    assert response.status_code == 200
    assert response.json() == {
        "has_content": False,
        "character_count": 0,
        "meets_minimum_length": False,
        "passed": False
    }


def test_evaluate_short_response():
    response = client.post(
        "/evaluate",
        json={"response": "Oi"}
    )

    assert response.status_code == 200
    assert response.json() == {
        "has_content": True,
        "character_count": 2,
        "meets_minimum_length": False,
        "passed": False
    }


def test_evaluate_valid_response():
    response = client.post(
        "/evaluate",
        json={
            "response": "A inteligência artificial permite que sistemas realizem tarefas que normalmente exigem inteligência humana."
        }
    )

    assert response.status_code == 200
    assert response.json()["has_content"] is True
    assert response.json()["meets_minimum_length"] is True
    assert response.json()["passed"] is True


# TESTES DE RELEVÂNCIA POR PALAVRAS-CHAVE

def test_evaluate_relevance_all_keywords():
    response = client.post(
        "/evaluate-relevance",
        json={
            "response": "A inteligência artificial permite que computadores executem tarefas.",
            "expected_keywords": [
                "inteligência artificial",
                "computadores",
                "tarefas"
            ]
        }
    )

    assert response.status_code == 200
    assert response.json()["matched_count"] == 3
    assert response.json()["relevance_score"] == 1.0
    assert response.json()["relevant"] is True


def test_evaluate_relevance_no_keywords():
    response = client.post(
        "/evaluate-relevance",
        json={
            "response": "Hoje está fazendo um dia muito bonito.",
            "expected_keywords": [
                "inteligência artificial",
                "computadores"
            ]
        }
    )

    assert response.status_code == 200
    assert response.json()["matched_count"] == 0
    assert response.json()["relevance_score"] == 0
    assert response.json()["relevant"] is False


def test_evaluate_relevance_empty_keywords():
    response = client.post(
        "/evaluate-relevance",
        json={
            "response": "A inteligência artificial transforma a tecnologia.",
            "expected_keywords": []
        }
    )

    assert response.status_code == 200
    assert response.json()["matched_count"] == 0
    assert response.json()["total_keywords"] == 0
    assert response.json()["relevance_score"] == 0
    assert response.json()["relevant"] is False


# TESTES DE COMPARAÇÃO COM RESPOSTA DE REFERÊNCIA

def test_evaluate_reference_equal():
    response = client.post(
        "/evaluate-reference",
        json={
            "response": "Brasília é a capital do Brasil.",
            "reference": "Brasília é a capital do Brasil."
        }
    )

    assert response.status_code == 200
    assert response.json()["similarity_score"] == 1.0
    assert response.json()["passed"] is True


def test_evaluate_reference_partial():
    response = client.post(
        "/evaluate-reference",
        json={
            "response": "Brasília é a capital brasileira.",
            "reference": "Brasília é a capital do Brasil."
        }
    )

    assert response.status_code == 200
    assert response.json()["similarity_score"] == 0.67
    assert response.json()["passed"] is True


def test_evaluate_reference_no_match():
    response = client.post(
        "/evaluate-reference",
        json={
            "response": "Hoje está fazendo um dia ensolarado.",
            "reference": "Brasília é a capital do Brasil."
        }
    )

    assert response.status_code == 200
    assert response.json()["similarity_score"] == 0.0
    assert response.json()["passed"] is False


def test_evaluate_reference_empty():
    response = client.post(
        "/evaluate-reference",
        json={
            "response": "Brasília é a capital do Brasil.",
            "reference": "   "
        }
    )

    assert response.status_code == 200
    assert response.json() == {
        "error": "A resposta de referência não pode estar vazia."
    }

# ============================================================
# TESTE 14 - VALIDAÇÃO DE CAMPO OBRIGATÓRIO AUSENTE
# ============================================================

def test_evaluate_reference_missing_field():
    response = client.post(
        "/evaluate-reference",
        json={
            "response": "Brasília é a capital do Brasil."
        }
    )

    # Verifica se a API rejeitou a requisição
    assert response.status_code == 422

    # Verifica se o campo ausente foi identificado
    errors = response.json()["detail"]

    assert any(
        error["loc"] == ["body", "reference"]
        for error in errors
    )
    
# ============================================================
# TESTE 15 - AUSÊNCIA DO CAMPO RESPONSE
# ============================================================

def test_evaluate_reference_missing_response():
    response = client.post(
        "/evaluate-reference",
        json={
            "reference": "Brasília é a capital do Brasil."
        }
    )

    # Valida o código HTTP
    assert response.status_code == 422

    # Valida se o campo ausente foi identificado
    errors = response.json()["detail"]

    assert any(
        error["loc"] == ["body", "response"]
        for error in errors
    )

# ============================================================
# TESTE 16 - RESPOSTA VAZIA NA COMPARAÇÃO DE REFERÊNCIA
# ============================================================

def test_evaluate_reference_empty_response():
    response = client.post(
        "/evaluate-reference",
        json={
            "response": "",
            "reference": "Brasília é a capital do Brasil."
        }
    )

    # Valida o status HTTP
    assert response.status_code == 200

    # Valida a ausência de palavras correspondentes
    assert response.json()["matched_count"] == 0

    # Valida a similaridade
    assert response.json()["similarity_score"] == 0.0

    # A avaliação não deve ser aprovada
    assert response.json()["passed"] is False


# ============================================================
# TESTE 17 - RESPOSTA COM APENAS ESPAÇOS
# ============================================================

def test_evaluate_reference_whitespace_response():
    response = client.post(
        "/evaluate-reference",
        json={
            "response": "   ",
            "reference": "Brasília é a capital do Brasil."
        }
    )

    # Valida o status HTTP
    assert response.status_code == 200

    # Não deve encontrar palavras correspondentes
    assert response.json()["matched_count"] == 0

    # A similaridade deve ser zero
    assert response.json()["similarity_score"] == 0.0

    # A avaliação não deve ser aprovada
    assert response.json()["passed"] is False

# ============================================================
# TESTE 18 - PALAVRAS-CHAVE COM MAIUSCULAS E MINUSCULAS
# ============================================================

def test_evaluate_relevance_case_insensitive():
    response = client.post(
        "/evaluate-relevance",
        json={
            "response": "A inteligência artificial transforma a tecnologia.",
            "expected_keywords": [
                "INTELIGÊNCIA ARTIFICIAL",
                "TECNOLOGIA",
                "TRANSFORMA"
            ]
        }
    )

    # Valida o status HTTP
    assert response.status_code == 200

    # Todas as palavras-chave devem ser encontradas
    assert response.json()["matched_count"] == 3

    # A relevância deve ser 100%
    assert response.json()["relevance_score"] == 1.0

    # A avaliação deve ser aprovada
    assert response.json()["relevant"] is True

# ============================================================
# TESTE 19 - REMOCAO DE PONTUACAO NA AVALIACAO DE RELEVANCIA
# ============================================================

def test_evaluate_relevance_ignores_punctuation():
    response = client.post(
        "/evaluate-relevance",
        json={
            "response": "A inteligência artificial transforma a tecnologia!",
            "expected_keywords": [
                "inteligência artificial",
                "tecnologia"
            ]
        }
    )

    # Valida o status HTTP
    assert response.status_code == 200

    # As duas palavras-chave devem ser encontradas
    assert response.json()["matched_count"] == 2

    # A relevância deve ser 100%
    assert response.json()["relevance_score"] == 1.0

    # A avaliação deve ser aprovada
    assert response.json()["relevant"] is True

# ============================================================
# TESTE 20 - LIMITE MINIMO DE RELEVANCIA (50%)
# ============================================================

def test_evaluate_relevance_exactly_at_threshold():
    response = client.post(
        "/evaluate-relevance",
        json={
            "response": "A inteligência artificial transforma a tecnologia.",
            "expected_keywords": [
                "inteligência artificial",
                "computadores"
            ]
        }
    )

    # Valida o status HTTP
    assert response.status_code == 200

    # Apenas uma das duas palavras-chave foi encontrada
    assert response.json()["matched_count"] == 1

    # A pontuação deve ser exatamente 50%
    assert response.json()["relevance_score"] == 0.5

    # No limite de 50%, a avaliação deve ser aprovada
    assert response.json()["relevant"] is True

# ============================================================
# TESTE 21 - RELEVANCIA ABAIXO DO LIMITE MINIMO
# ============================================================

def test_evaluate_relevance_below_threshold():
    response = client.post(
        "/evaluate-relevance",
        json={
            "response": "A inteligência artificial transforma a tecnologia.",
            "expected_keywords": [
                "inteligência artificial",
                "computadores",
                "aprendizado de máquina"
            ]
        }
    )

    # Valida o status HTTP
    assert response.status_code == 200

    # Apenas uma das três palavras-chave foi encontrada
    assert response.json()["matched_count"] == 1

    # A pontuação deve ser aproximadamente 33%
    assert response.json()["relevance_score"] == 0.33

    # A avaliação deve ser reprovada
    assert response.json()["relevant"] is False

# ============================================================
# TESTE 22 - EVITAR FALSOS POSITIVOS EM PALAVRAS-CHAVE
# ============================================================

def test_evaluate_relevance_does_not_match_partial_word():
    response = client.post(
        "/evaluate-relevance",
        json={
            "response": "A tecnologia está avançando.",
            "expected_keywords": ["IA"]
        }
    )

    # Valida o status HTTP
    assert response.status_code == 200

    # IA não deve ser encontrada dentro de tecnologia
    assert response.json()["matched_count"] == 0

    # A relevância deve ser zero
    assert response.json()["relevance_score"] == 0.0

    # A avaliação não deve ser aprovada
    assert response.json()["relevant"] is False

def test_evaluate_semantic_similar_response(monkeypatch):
    import semantic_evaluator

    monkeypatch.setattr(
        semantic_evaluator,
        "calculate_semantic_similarity",
        lambda response, reference: 0.8445
    )

    response = client.post(
        "/evaluate-semantic",
        json={
            "response": "A IA ajuda máquinas a executar tarefas humanas.",
            "reference": "A inteligência artificial permite que máquinas realizem tarefas humanas."
        }
    )

    assert response.status_code == 200
    assert response.json()["similarity_score"] == 0.8445
    assert response.json()["semantically_similar"] is True


def test_evaluate_semantic_below_threshold(monkeypatch):
    import semantic_evaluator

    monkeypatch.setattr(
        semantic_evaluator,
        "calculate_semantic_similarity",
        lambda response, reference: 0.45
    )

    response = client.post(
        "/evaluate-semantic",
        json={
            "response": "O céu é azul.",
            "reference": "A inteligência artificial aprende com dados."
        }
    )

    assert response.status_code == 200
    assert response.json()["similarity_score"] == 0.45
    assert response.json()["semantically_similar"] is False


def test_evaluate_semantic_exactly_at_threshold(monkeypatch):
    import semantic_evaluator

    monkeypatch.setattr(
        semantic_evaluator,
        "calculate_semantic_similarity",
        lambda response, reference: 0.70
    )

    response = client.post(
        "/evaluate-semantic",
        json={
            "response": "A IA auxilia pessoas.",
            "reference": "A inteligência artificial ajuda pessoas."
        }
    )

    assert response.status_code == 200
    assert response.json()["semantically_similar"] is True


def test_evaluate_semantic_empty_response():
    response = client.post(
        "/evaluate-semantic",
        json={
            "response": "   ",
            "reference": "A inteligência artificial aprende."
        }
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "A resposta não pode estar vazia."


def test_evaluate_semantic_empty_reference():
    response = client.post(
        "/evaluate-semantic",
        json={
            "response": "A inteligência artificial aprende.",
            "reference": "   "
        }
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "A referência não pode estar vazia."
