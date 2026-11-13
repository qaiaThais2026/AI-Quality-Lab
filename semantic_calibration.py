
from semantic_evaluator import calculate_semantic_similarity


examples = [
    {
        "category": "PARAFRASE",
        "reference": "A inteligencia artificial ajuda medicos a analisar exames.",
        "response": "Sistemas de IA podem apoiar profissionais de saude na interpretacao de exames."
    },
    {
        "category": "ASSUNTO DIFERENTE",
        "reference": "A inteligencia artificial ajuda medicos a analisar exames.",
        "response": "Uma receita de bolo leva farinha, ovos e acucar."
    },
    {
        "category": "CONTRADICAO",
        "reference": "As vacinas reduzem o risco de doencas graves.",
        "response": "As vacinas aumentam o risco de doencas graves."
    }
]


print("\n===== AI QUALITY LAB - CALIBRACAO SEMANTICA =====\n")

for example in examples:
    score = calculate_semantic_similarity(
        example["response"],
        example["reference"]
    )

    print(f"Cenario: {example['category']}")
    print(f"Referencia: {example['reference']}")
    print(f"Resposta: {example['response']}")
    print(f"Similaridade: {score:.4f}")
    print("-" * 60)
