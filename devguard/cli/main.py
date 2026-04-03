import click
import json
import sys
from pathlib import Path
from devguard.core.config import Config
from devguard.core.scanner import Scanner
from devguard.ai.engine import AIEngine

@click.group()
def cli():
    """DevGuard - Local-first security scanner."""
    pass

@cli.command()
@click.argument('path', type=click.Path(exists=True), default=".")
@click.option('--json-output', is_flag=True, help="Output results in JSON")
def scan(path, json_output):
    """Scan a directory for security issues."""
    config = Config()
    scanner = Scanner(path, config)
    
    if not json_output:
        click.secho(f"Scanning {path}...", fg="cyan")
        
    issues = scanner.scan()
    
    if json_output:
        click.echo(json.dumps([i.to_dict() for i in issues], indent=2))
        return

    if not issues:
        click.secho("✅ No issues found!", fg="green")
        return

    for issue in issues:
        click.secho(f"[{issue.severity}] {issue.file_path}:{issue.line_number}", fg="red", bold=True)
        click.secho(f"  Type: {issue.category}")
        click.secho(f"  Desc: {issue.description}")
        click.secho(f"  Code: {issue.snippet.strip()}\n", fg="yellow")

@cli.group()
def ai():
    """Manage AI settings."""
    pass

@ai.command()
def enable():
    config = Config()
    config.ai_enabled = True
    config.save()
    click.secho("AI features enabled. Ensure OLLAMA is set.", fg="green")

@ai.command()
def disable():
    config = Config()
    config.ai_enabled = False
    config.save()
    click.secho("AI features disabled.", fg="yellow")

@cli.command()
def tui():
    """Launch the Textual Terminal UI."""
    from devguard.tui.app import DevGuardTUI
    app = DevGuardTUI()
    app.run()

@cli.command()
def gui():
    """Launch the PySide6 Desktop GUI."""
    from PySide6.QtWidgets import QApplication
    from devguard.gui.app import DevGuardGUI
    
    app = QApplication(sys.argv)
    window = DevGuardGUI()
    window.show()
    sys.exit(app.exec())  # nosec
