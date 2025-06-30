
import os
import json
import pathlib
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()  # carrega variáveis do .env

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise RuntimeError("Variável GEMINI_API_KEY não encontrada. Crie um arquivo .env com GEMINI_API_KEY=...")

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

def generate_pdi_plan(responses):
    """Gera um PDI usando Gemini 1.5 Flash. 'responses' é lista (pergunta, resposta)."""
    user_part = "\n".join([f"Pergunta: {q}\nResposta: {a}" for q, a in responses])

    prompt = (
        "Você é um consultor de carreira. "
        "Com base nas respostas abaixo, gere um Plano de Desenvolvimento Individual contendo:\n"
        "- 3 a 5 metas SMART\n"
        "- Competências a desenvolver\n"
        "- Ações recomendadas (cursos, práticas, leituras)\n"
        "- Prazo sugerido para cada ação\n"
        "- Indicadores de sucesso\n\n"
        + user_part
    )

    response = model.generate_content(prompt, generation_config={ "temperature": 0.4 })
    return response.text.strip()

def faq_cert(cert_name):
    """Retorna informações de certificação a partir de certs.json"""
    data = json.loads(pathlib.Path("certs.json").read_text(encoding="utf-8"))
    info = data.get(cert_name)
    if not info:
        return f"Desculpe, não encontrei informações sobre {cert_name}."
    links = "\n".join(info["study_links"])
    return (
        f"**{cert_name} ({info['exam_code']})**\n{info['description']}\n"
        f"Recursos de estudo:\n{links}"
    )
