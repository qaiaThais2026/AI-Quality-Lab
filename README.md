 AI Quality Lab

AI Quality Engineering | API Testing | LLM Testing | Semantic Evaluation

Projeto prático de Engenharia de Qualidade de Software com foco em testes automatizados de APIs e avaliação da qualidade de respostas produzidas por sistemas de Inteligência Artificial.

O laboratório combina práticas tradicionais de QA com técnicas de avaliação semântica, utilizando Python, FastAPI, Pytest e Sentence Transformers.

 1. Objetivo do projeto

Desenvolver uma estrutura de testes capaz de avaliar diferentes aspectos da qualidade de respostas de sistemas de Inteligência Artificial.

O projeto explora:

Validação de APIs e respostas HTTP.

Identificação de respostas vazias ou insuficientes.

Avaliação de relevância por palavras-chave.

Comparação de respostas com textos de referência.

Avaliação de similaridade semântica.

Testes positivos, negativos e de exceção.

Identificação de limitações de métodos de avaliação de IA.

O objetivo é evoluir o laboratório para uma estrutura de AI Quality Engineering aplicável a sistemas baseados em LLMs.

 2. Tecnologias e ferramentas

Tecnologia

Aplicação

Python 3.12

Linguagem principal

FastAPI

Desenvolvimento da API

Pytest

Testes automatizados

HTTPX

Cliente HTTP para testes

Pydantic

Validação de dados

Sentence Transformers

Avaliação semântica

PyTorch

Execução do modelo de IA

REST API

Comunicação entre sistemas

JSON

Estruturação de requisições e respostas

Modelo de avaliação semântica

Modelo: sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2

Modelo multilíngue utilizado para gerar embeddings de frases e calcular similaridade semântica por similaridade de cosseno.

 3. Estrutura do projeto

AI-Quality-Lab/
│
├── tests/
│   └── test_api.py
│
├── main.py
├── semantic_evaluator.py
├── semantic_calibration.py
├── README.md
├── .gitignore
└── requirements.txt (se criado)

Responsabilidade dos arquivos

Arquivo

Responsabilidade

main.py

Implementação dos endpoints da API

semantic_evaluator.py

Carregamento do modelo e cálculo de similaridade

semantic_calibration.py

Execução de experimentos de calibração semântica

tests/test_api.py

Testes automatizados da API

README.md

Documentação do projeto

.gitignore

Exclusão de arquivos locais e temporários do controle de versão

 4. Endpoints e funcionalidades

Endpoint

Método

Funcionalidade

/

GET

Verificação da rota inicial

/health

GET

Verificação de saúde da API

/evaluate

POST

Avaliação básica de respostas

/evaluate-relevance

POST

Avaliação por palavras-chave

/evaluate-reference

POST

Comparação com texto de referência

/evaluate-semantic

POST

Avaliação de similaridade semântica

4.1 Response Evaluation

Endpoint: POST /evaluate

Avalia se uma resposta possui conteúdo suficiente conforme o tamanho mínimo configurado.

Critérios:

Verificação de conteúdo.

Contagem de caracteres.

Validação do tamanho mínimo.

Resultado de aprovação ou reprovação.

4.2 Relevance Evaluation

Endpoint: POST /evaluate-relevance

Avalia a presença de palavras-chave esperadas na resposta.

Cenários contemplados:

Palavras-chave encontradas.

Palavras-chave não encontradas.

Lista de palavras-chave vazia.

Diferenças entre maiúsculas e minúsculas.

Pontuação.

Correspondências parciais indevidas.

Avaliação no limite configurado.

Avaliação abaixo do limite.

4.3 Reference-based Evaluation

Endpoint: POST /evaluate-reference

Compara uma resposta com um texto de referência utilizando a interseção entre conjuntos de palavras.

Cenários contemplados:

Correspondência integral.

Correspondência parcial.

Ausência de correspondência.

Referência vazia.

Campos obrigatórios ausentes.

Resposta vazia ou contendo somente espaços.

Limitação: a abordagem lexical não compreende equivalência semântica, contexto ou contradições.

4.4 Semantic Evaluation

Endpoint: POST /evaluate-semantic

Utiliza Sentence Transformers para gerar embeddings e calcular a similaridade semântica entre uma resposta e uma referência.

O resultado é comparado com o limite configurado de 0.70.

Cenários contemplados:

Respostas semanticamente semelhantes.

Similaridade abaixo do limite.

Similaridade exatamente no limite.

Resposta vazia.

Referência vazia.

 5. Estratégia de testes automatizados

A suíte possui 27 testes automatizados distribuídos em cinco categorias funcionais.

5.1 Resumo da cobertura

Categoria

Quantidade

API Testing

3

Response Evaluation

3

Relevance Evaluation

8

Reference-based Evaluation

8

Semantic Evaluation

5

Total

27

5.2 API Testing

ID

Teste

Objetivo

QA-001

test_home

Validar endpoint inicial

QA-002

test_health

Validar estado de saúde da API

QA-003

test_rota_inexistente

Validar tratamento de rota inexistente (404)

5.3 Response Evaluation

ID

Teste

Objetivo

QA-004

test_evaluate_empty_response

Identificar resposta vazia

QA-005

test_evaluate_short_response

Identificar resposta abaixo do tamanho mínimo

QA-006

test_evaluate_valid_response

Validar resposta com conteúdo suficiente

5.4 Relevance Evaluation

ID

Teste

Objetivo

QA-007

test_evaluate_relevance_all_keywords

Validar correspondência de todas as palavras-chave

QA-008

test_evaluate_relevance_no_keywords

Validar ausência de correspondências

QA-009

test_evaluate_relevance_empty_keywords

Tratar lista de palavras-chave vazia

QA-018

test_evaluate_relevance_case_insensitive

Validar normalização de maiúsculas e minúsculas

QA-019

test_evaluate_relevance_ignores_punctuation

Validar remoção de pontuação

QA-020

test_evaluate_relevance_exactly_at_threshold

Validar aprovação no limite de 50%

QA-021

test_evaluate_relevance_below_threshold

Validar reprovação abaixo do limite

QA-022

test_evaluate_relevance_does_not_match_partial_word

Evitar correspondências parciais indevidas

5.5 Reference-based Evaluation

ID

Teste

Objetivo

QA-010

test_evaluate_reference_equal

Validar correspondência integral com a referência

QA-011

test_evaluate_reference_partial

Validar correspondência parcial

QA-012

test_evaluate_reference_no_match

Validar ausência de correspondência

QA-013

test_evaluate_reference_empty

Validar referência vazia

QA-014

test_evaluate_reference_missing_field

Validar ausência do campo reference

QA-015

test_evaluate_reference_missing_response

Validar ausência do campo response

QA-016

test_evaluate_reference_empty_response

Validar resposta vazia

QA-017

test_evaluate_reference_whitespace_response

Validar resposta contendo somente espaços

5.6 Semantic Evaluation

ID

Teste

Objetivo

QA-023

test_evaluate_semantic_similar_response

Validar resposta semanticamente semelhante

QA-024

test_evaluate_semantic_below_threshold

Validar similaridade abaixo do limite

QA-025

test_evaluate_semantic_exactly_at_threshold

Validar similaridade exatamente em 0.70

QA-026

test_evaluate_semantic_empty_response

Validar resposta vazia com HTTP 400

QA-027

test_evaluate_semantic_empty_reference

Validar referência vazia com HTTP 400

Estratégia de validação

Os testes verificam:

Status HTTP e estrutura das respostas JSON.

Regras de negócio e critérios de aprovação.

Entradas válidas e inválidas.

Limites mínimos de avaliação.

Tratamento de campos obrigatórios.

Normalização de texto.

Comportamento da avaliação semântica.

Os testes do endpoint de avaliação semântica utilizam monkeypatch para simular resultados da função de similaridade, isolando a validação do endpoint da execução real do modelo.

 6. Resultados da suíte de testes

Última execução registrada após a limpeza dos testes:

============================= test session starts =============================
collected 27 items

27 passed in 17.03s

Indicador

Resultado

Testes coletados

27

Testes aprovados

27

Testes reprovados

0

Tempo de execução

17,03 segundos

Comando utilizado:

python -m pytest -v

 7. Experimentos de calibração semântica

O arquivo semantic_calibration.py contém experimentos para observar o comportamento do modelo em diferentes cenários.

Cenário

Similaridade observada

Paráfrase

0.7521

Assunto diferente

0.0725

Contradição

0.8536

Principal descoberta

O modelo identificou uma similaridade maior entre frases com significados próximos e uma similaridade baixa entre assuntos diferentes.

Entretanto, o cenário de contradição apresentou similaridade elevada.

Isso demonstra uma limitação importante: similaridade semântica não é equivalente à verificação de verdade ou consistência factual.

Uma resposta pode ser semanticamente semelhante à referência e, ainda assim, contradizê-la.

 8. Limitações conhecidas

O projeto está em desenvolvimento e apresenta as seguintes limitações:

A avaliação por palavras-chave não compreende o significado completo da resposta.

A comparação lexical não identifica paráfrases de forma confiável.

A similaridade semântica não comprova precisão factual.

O cálculo de similaridade não identifica contradições de maneira confiável.

O limite de similaridade precisa ser calibrado conforme o contexto e os cenários de uso.

Essas limitações orientam as próximas etapas de evolução do laboratório.

 9. Próximas evoluções

O roadmap técnico prevê:

Natural Language Inference (NLI): classificação de relações entre referência e resposta em entailment, contradiction e neutral.

RAG Evaluation: avaliação de recuperação de documentos e qualidade das respostas baseadas em contexto.

Hallucination Testing: investigação de afirmações sem suporte nas fontes.

Prompt Injection Testing: testes de segurança e resistência a instruções maliciosas.

LLM Evaluation Metrics: incorporação de métricas de relevância, fidelidade e consistência.

Test Automation: expansão da cobertura e organização dos cenários automatizados.

Observability: monitoramento de resultados e indicadores de qualidade.

 10. Como executar o projeto

Pré-requisitos

Python 3.12.

Ambiente virtual Python.

Dependências instaladas.

Ativar o ambiente virtual no Windows PowerShell

.\.venv-semantic\Scripts\Activate.ps1

Executar os testes automatizados

python -m pytest -v

Executar a API localmente

uvicorn main:app --reload

A documentação interativa da API estará disponível em:

http://127.0.0.1:8000/docs

👩‍💻 Sobre o projeto

O AI Quality Lab é um projeto prático de desenvolvimento de competências em Quality Engineering, automação de testes e avaliação de sistemas de Inteligência Artificial.


Status: Em desenvolvimento contínuo.
