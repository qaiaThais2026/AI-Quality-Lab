
# ============================================================
# AI QUALITY LAB
# API para avaliação da qualidade de respostas de IA
# ============================================================


# 1. IMPORTS

import re

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


# 2. CONFIGURAÇÕES DA API

app = FastAPI(
    title="AI Quality Lab",
    description="API para testes de qualidade de inteligência artificial",
    version="1.0.0"
)

MIN_RESPONSE_LENGTH = 20
REFERENCE_SIMILARITY_THRESHOLD = 0.5
RELEVANCE_THRESHOLD = 0.5
SEMANTIC_SIMILARITY_THRESHOLD = 0.70

# 3. FUNÇÕES AUXILIARES

def normalize_text(text: str) -> str:
    """
    Padroniza o texto antes da avaliação:
    - Converte para letras minúsculas
    - Remove pontuação
    - Remove espaços extras
    """

    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)
    text = re.sub(r"\s+", " ", text)

    return text.strip()


# 4. MODELOS DE DADOS

class EvaluationRequest(BaseModel):
    response: str


class RelevanceEvaluationRequest(BaseModel):
    response: str
    expected_keywords: list[str]


class ReferenceEvaluationRequest(BaseModel):
    response: str
    reference: str


# 5. ROTAS BÁSICAS DA API

@app.get("/")
def home():
    return {
        "message": "AI Quality Lab funcionando!",
        "status": "success"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


# 6. AVALIAÇÃO BÁSICA DE RESPOSTAS

@app.post("/evaluate")
def evaluate_response(request: EvaluationRequest):

    response_text = request.response.strip()
    character_count = len(response_text)

    has_content = character_count > 0
    meets_minimum_length = character_count >= MIN_RESPONSE_LENGTH

    passed = has_content and meets_minimum_length

    return {
        "has_content": has_content,
        "character_count": character_count,
        "meets_minimum_length": meets_minimum_length,
        "passed": passed
    }


# 7. AVALIAÇÃO DE RELEVÂNCIA POR PALAVRAS-CHAVE


@app.post("/evaluate-relevance")
def evaluate_relevance(request: RelevanceEvaluationRequest):
    response_text = normalize_text(request.response)

    matched_keywords = [
        keyword
        for keyword in request.expected_keywords
        if normalize_text(keyword)
        and re.search(
            rf"(?<!\w){re.escape(normalize_text(keyword))}(?!\w)",
            response_text
        )
    ]

    total_keywords = len(request.expected_keywords)
    matched_count = len(matched_keywords)

    relevance_score = (
        matched_count / total_keywords
        if total_keywords > 0
        else 0
    )

    return {
        "matched_keywords": matched_keywords,
        "matched_count": matched_count,
        "total_keywords": total_keywords,
        "relevance_score": round(relevance_score, 2),
        "relevant": relevance_score >= RELEVANCE_THRESHOLD
    }

# 8. COMPARAÇÃO COM RESPOSTA DE REFERÊNCIA

@app.post("/evaluate-reference")
def evaluate_reference(request: ReferenceEvaluationRequest):

    normalized_response = normalize_text(request.response)
    normalized_reference = normalize_text(request.reference)

    response_words = set(normalized_response.split())
    reference_words = set(normalized_reference.split())

    if len(reference_words) == 0:
        return {
            "error": "A resposta de referência não pode estar vazia."
        }

    matched_words = response_words.intersection(reference_words)

    similarity_score = len(matched_words) / len(reference_words)

    return {
        "matched_words": sorted(matched_words),
        "matched_count": len(matched_words),
        "reference_word_count": len(reference_words),
        "similarity_score": round(similarity_score, 2),
        "passed": similarity_score >= REFERENCE_SIMILARITY_THRESHOLD
    }

@app.post("/evaluate-semantic")
def evaluate_semantic(request: ReferenceEvaluationRequest):
    """
    Avalia a similaridade semântica entre uma resposta
    e um texto de referência.
    """

    if not request.response.strip():
        raise HTTPException(
            status_code=400,
            detail="A resposta não pode estar vazia."
        )

    if not request.reference.strip():
        raise HTTPException(
            status_code=400,
            detail="A referência não pode estar vazia."
        )

    # Importação sob demanda: não exige Sentence Transformers
    # para iniciar a API ou executar os testes antigos.
    from semantic_evaluator import calculate_semantic_similarity

    similarity_score = calculate_semantic_similarity(
        request.response,
        request.reference
    )

    return {
        "similarity_score": similarity_score,
        "threshold": SEMANTIC_SIMILARITY_THRESHOLD,
        "semantically_similar": (
            similarity_score >= SEMANTIC_SIMILARITY_THRESHOLD
        )
    }
