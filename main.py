
import json, random, datetime
import typer
from pathlib import Path
from ia import generate_pdi_plan, faq_cert
from storage import save_session

app = typer.Typer()
QUESTIONS_FILE = Path("questions.json")

@app.command()
def pdi():
    """Entrevista de PDI e geração de plano com Gemini."""
    questions = json.loads(QUESTIONS_FILE.read_text(encoding="utf-8"))
    responses = []
    typer.echo("=== Entrevista de PDI ===")
    for q in questions:
        ans = typer.prompt(q["text"])
        responses.append((q["text"], ans))
    plan = generate_pdi_plan(responses)
    typer.secho("\n--- Plano de Desenvolvimento Individual ---", fg=typer.colors.GREEN)
    typer.echo(plan)
    # salvar
    email = next((a for (q,a) in responses if "e-mail" in q.lower()), "anon@example.com")
    timestamp = datetime.datetime.now().isoformat(timespec='seconds')
    save_session(email, {"timestamp": timestamp, "responses": responses, "plan": plan})
    typer.echo(f"\nSessão salva em pdi_data.json ({timestamp}).")

@app.command()
def faq(cert_name: str):
    """Mostra FAQ e materiais de estudo de uma certificação."""
    typer.echo(faq_cert(cert_name))

@app.command()
def simulado(cert_name: str = "comptia_itf", n: int = 5):
    """Aplica um simulado rápido (N questões)."""
    path = Path("exams") / f"{cert_name}.json"
    if not path.exists():
        typer.echo("Simulado não encontrado.")
        raise typer.Exit()
    exam = json.loads(path.read_text(encoding="utf-8"))
    questions = random.sample(exam["questions"], min(n, len(exam["questions"])))
    correct = 0
    wrong_q = []
    for q in questions:
        typer.echo(f"\n{q['text']}")
        for idx, choice in enumerate(q["choices"]):
            typer.echo(f"{idx}) {choice}")
        answer = typer.prompt("Sua resposta (número)")
        try:
            idx_answer = int(answer)
        except ValueError:
            idx_answer = -1
        if idx_answer == q["answer"]:
            correct += 1
        else:
            wrong_q.append(q)
    score = 100 * correct / len(questions)
    color = typer.colors.GREEN if score >= 70 else typer.colors.RED
    typer.secho(f"\nPontuação: {score:.1f}% ({correct}/{len(questions)})", fg=color)
    if wrong_q:
        typer.echo("\nQuestões para revisar:")
        for q in wrong_q:
            typer.echo(f"- {q['text']} (Correta: {q['choices'][q['answer']]} )")

if __name__ == "__main__":
    app()
