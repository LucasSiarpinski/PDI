
# PDI Assistant (CLI)

Assistente em linha de comando que:
* Coleta respostas para montar um PDI.
* Usa GPT‑4o para gerar o plano personalizado.
* Traz FAQ de certificações e aplica simulados com correção.

## Comandos principais
```bash
# entrevista PDI
python main.py pdi

# FAQ de certificação
python main.py faq "AWS Certified Cloud Practitioner"

# Simulado rápido (5 questões aleatórias)
python main.py simulado comptia_itf 5
```

## Instalação
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export OPENAI_API_KEY="sua-chave-aqui"
```


## Usando o Gemini 1.5 Flash

1. Crie um arquivo `.env` na raiz:

```
GEMINI_API_KEY=sua_chave_gemini_aqui
```

2. Instale dependências:

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

3. Execute normalmente:

```bash
python main.py pdi
```

Gemini 1.5 Flash é gratuito dentro dos limites mensais da Google AI (confira no console).
