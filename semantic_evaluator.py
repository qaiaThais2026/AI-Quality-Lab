
from functools import lru_cache

from sentence_transformers import SentenceTransformer, util


# Modelo multilíngue com suporte ao português
MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"


@lru_cache(maxsize=1)
def load_semantic_model():
    """
    Carrega o modelo apenas uma vez.
    Mantém o modelo em memória para reutilização.
    """
    return SentenceTransformer(MODEL_NAME, device="cpu")


def calculate_semantic_similarity(response: str, reference: str) -> float:
    """
    Calcula a similaridade semântica entre uma resposta
    e um texto de referência.

    Retorna um valor de similaridade cosseno.
    """
    if not response.strip():
        raise ValueError("A resposta não pode estar vazia.")

    if not reference.strip():
        raise ValueError("A referência não pode estar vazia.")

    model = load_semantic_model()

    embeddings = model.encode(
        [response, reference],
        convert_to_tensor=True
    )

    similarity = util.cos_sim(
        embeddings[0],
        embeddings[1]
    )

    return round(float(similarity.item()), 4)
