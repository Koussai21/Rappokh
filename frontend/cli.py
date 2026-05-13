#!/usr/bin/env python
"""CLI interface for Rappokh Report Generator"""
import click
import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.report_gen.generator import ReportGenerator
from backend.agents.clarification_agent import ClarificationAgent
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

console = Console()

@click.group()
def cli():
    """Rappokh - AI-Powered Report Generator"""
    pass

@cli.command()
@click.option('--notes', prompt='Entrez vos notes de brainstorming', help='Notes initiales du rapport')
def brainstorm(notes):
    """Démarrer une session de brainstorming"""
    console.print("[bold blue]🧠 Démarrage session de brainstorming[/]")

    generator = ReportGenerator()

    try:
        result = generator.start_brainstorming_session(notes)

        console.print(Panel(
            "[bold green]Analyse initiale complétée[/]\n\n" +
            result['initial_analysis'],
            title="Analyse du contenu"
        ))

        if result['needs_more_info']:
            console.print("\n[bold yellow]⚠️ Des clarifications sont nécessaires[/]\n")
            for i, question in enumerate(result['clarification_questions'], 1):
                console.print(f"[cyan]{i}. {question}[/]")
        else:
            console.print("\n[bold green]✓ Informations suffisantes pour générer le rapport[/]")

    except Exception as e:
        console.print(f"[bold red]❌ Erreur: {str(e)}[/]")

@cli.command()
@click.option('--notes', prompt='Entrez vos notes de brainstorming', help='Notes du rapport')
@click.option('--clarify', is_flag=True, help='Poser des questions de clarification')
def generate(notes, clarify):
    """Générer un rapport complet"""
    generator = ReportGenerator()

    answers = {}
    if clarify:
        console.print("[bold blue]📝 Questions de clarification[/]\n")
        questions = generator.clarification_agent.ask_clarification_questions(notes)

        for i, question in enumerate(questions, 1):
            answer = click.prompt(f"\n{i}. {question}")
            answers[f"question_{i}"] = answer

    console.print("\n[bold blue]⏳ Génération du rapport en cours...[/]")

    try:
        report = generator.generate_full_report(notes, answers if answers else None)

        # Save report
        output_file = "rapport_generé.md"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(report)

        console.print(Panel(
            f"[bold green]✓ Rapport généré avec succès![/]\n\n"
            f"Sauvegardé dans: [bold cyan]{output_file}[/]",
            title="Succès"
        ))

        # Display preview
        console.print("\n[bold yellow]Aperçu du rapport:[/]\n")
        console.print(Markdown(report[:1000] + "..."))

    except Exception as e:
        console.print(f"[bold red]❌ Erreur lors de la génération: {str(e)}[/]")

@cli.command()
@click.option('--notes', prompt='Entrez vos notes', help='Notes à évaluer')
def evaluate(notes):
    """Évaluer la complétude des informations"""
    generator = ReportGenerator()

    try:
        evaluation = generator.clarification_agent.evaluate_content_completeness(notes)
        console.print(Panel(
            evaluation['evaluation'],
            title="Évaluation de complétude"
        ))
    except Exception as e:
        console.print(f"[bold red]❌ Erreur: {str(e)}[/]")

@cli.command()
def server():
    """Lancer le serveur API FastAPI"""
    import uvicorn
    from backend.app import app
    from backend.config import settings

    console.print(f"[bold green]🚀 Démarrage du serveur Rappokh[/]")
    console.print(f"URL: http://{settings.host}:{settings.port}")
    console.print(f"Docs: http://{settings.host}:{settings.port}/docs")

    uvicorn.run(
        app,
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )

if __name__ == "__main__":
    cli()
