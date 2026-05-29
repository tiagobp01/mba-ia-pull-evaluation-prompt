# Otimização e Avaliação de Prompts com LangChain e LangSmith

Este repositório contém uma solução para o desafio de otimização de prompts para conversão de relatos de bugs em **User Stories** ágeis estruturadas e prontas para o backlog, utilizando **LangChain** e avaliações automatizadas com **LangSmith**.

---

## 🛠️ Tecnologias Utilizadas

- **Linguagem:** Python 3.11+
- **Orquestração de Prompts:** LangChain
- **Avaliação e Tracing:** LangSmith (API & Prompt Hub)
- **Provedor de LLM:** Google Gemini (`gemini-2.5-flash`)
- **Containerização:** Docker & Docker Compose
- **Testes Unitários:** Pytest

---

## 🧠 Técnicas de Engenharia de Prompt Aplicadas (Fase 2)

Para otimizar o prompt de conversão (`bug_to_user_story_v2`), foram aplicadas quatro técnicas avançadas de Prompt Engineering:

### 1. Role Prompting (Definição de Persona)
* **Como foi aplicada:** O prompt define o modelo como um **Product Manager Sênior e Analista de Sistemas Ágil** com larga experiência em engenharia de software.
* **Justificativa:** Isso instrui o LLM a adotar a linguagem técnica, o tom profissional e a visão estruturada esperados de uma documentação ágil de alta qualidade.

### 2. Chain of Thought (CoT - Raciocínio Passo a Passo)
* **Como foi aplicada:** Instruímos o modelo a analisar quatro aspectos antes de gerar a saída: identificar a persona do usuário, mapear a ação funcional, determinar o valor de negócio e classificar a complexidade (Simples, Média, Complexa).
* **Justificativa:** Essa abordagem garante que o LLM analise criticamente a severidade, impacto e causa raiz do bug antes de propor a solução.

### 3. Few-shot Learning (Aprendizado com Poucos Exemplos)
* **Como foi aplicada:** Incluímos três exemplos reais e completos que cobrem os três níveis de complexidade (Simples, Médio e Complexo), mostrando exatamente a entrada desejada (relato do bug) e a saída esperada (User Story correspondente).
* **Justificativa:** Fornecer exemplos práticos reduz drasticamente alucinações e garante conformidade exata com a formatação e os critérios das User Stories esperadas.

### 4. Skeleton of Thought (Estruturação Dinâmica)
* **Como foi aplicada:** O prompt instrui o modelo a gerar formatos diferentes de acordo com a complexidade identificada:
  * **Simples:** Apenas a User Story principal e critérios básicos de aceitação (Given-When-Then).
  * **Média:** Inclui critérios de aceitação e uma seção de **Contexto Técnico**.
  * **Complexa:** Inclui **User Story Principal**, **Critérios de Aceitação categorizados**, **Critérios Técnicos**, **Contexto do Bug (Severidade/Impacto)** e **Tasks Técnicas Sugeridas**.
* **Justificativa:** Garante que bugs críticos e complexos recebam o detalhamento técnico necessário para os desenvolvedores, mantendo simplicidade para bugs cosméticos.

---

## 📋 Como Executar o Projeto

### Pré-requisitos
* Ter o **Docker** e **Docker Compose** instalados (ou ambiente local com **Python 3.11+**).
* Credenciais de API para o **LangSmith** e o provedor de LLM **Google Gemini**.

### Configuração do Ambiente (.env)
Copie o arquivo `.env.example` para `.env` e preencha suas chaves:
```bash
cp .env.example .env
```
Preencha as seguintes chaves no arquivo `.env`:
* `LANGSMITH_API_KEY`: Sua chave de API do LangSmith.
* `USERNAME_LANGSMITH_HUB`: Seu nome de usuário público do LangSmith Hub.
* `GOOGLE_API_KEY`: Sua chave de API do Google Gemini.

---

### Opção A: Executando via Docker (Recomendado)

Todas as dependências e o ambiente Python já vêm isolados e prontos no Docker.

1. **Construir a imagem do Docker:**
   ```bash
   docker compose build
   ```

2. **Executar os testes de validação do prompt:**
   ```bash
   docker compose run --rm app pytest tests/test_prompts.py -v
   ```

3. **Puxar o prompt v1 do Hub (Pull):**
   ```bash
   docker compose run --rm app python src/pull_prompts.py
   ```

4. **Enviar o prompt otimizado v2 para o Hub (Push):**
   ```bash
   docker compose run --rm app python src/push_prompts.py
   ```

5. **Executar a avaliação automática de métricas:**
   ```bash
   docker compose run --rm app python src/evaluate.py
   ```

---

### Opção B: Executando Localmente (Sem Docker)

1. **Crie e ative seu ambiente virtual Python:**
   ```bash
   python -m venv .venv
   # No Windows:
   .venv\Scripts\activate
   # No Linux/macOS:
   source .venv/bin/activate
   ```

2. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Execute os testes de validação:**
   ```bash
   pytest tests/test_prompts.py -v
   ```

4. **Execute o Pull do prompt v1:**
   ```bash
   python src/pull_prompts.py
   ```

5. **Execute o Push do prompt v2:**
   ```bash
   python src/push_prompts.py
   ```

6. **Execute a avaliação:**
   ```bash
   python src/evaluate.py
   ```

---

## 📊 Resultados Finais

> [!NOTE]
> Esta seção deve ser preenchida após a execução bem-sucedida do script de avaliação (`python src/evaluate.py`), que calculará as notas finais no LangSmith.

* **Link Público das Avaliações no LangSmith:** [Insira aqui o link público do seu dashboard]
* **Print das notas finais:** (Insira screenshots das execuções e do dashboard contendo notas ≥ 0.9)

### Tabela Comparativa de Performance

| Métrica | Prompt Ruim (v1) | Prompt Otimizado (v2) | Status |
| :--- | :---: | :---: | :---: |
| **Helpfulness** | ~0.45 ✗ | **[Score V2]** | [APROVADO / REPROVADO] |
| **Correctness** | ~0.52 ✗ | **[Score V2]** | [APROVADO / REPROVADO] |
| **F1-Score** | ~0.48 ✗ | **[Score V2]** | [APROVADO / REPROVADO] |
| **Clarity** | ~0.50 ✗ | **[Score V2]** | [APROVADO / REPROVADO] |
| **Precision** | ~0.46 ✗ | **[Score V2]** | [APROVADO / REPROVADO] |
| **Média Geral** | **~0.48** | **[Média V2]** | **[STATUS FINAL]** |
