from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, DataTable, Markdown
from textual.containers import Horizontal, Vertical
from devguard.core.config import Config
from devguard.core.scanner import Scanner
from devguard.ai.engine import AIEngine
import os

class DevGuardTUI(App):
    CSS = """
    DataTable { height: 100%; border: solid green; }
    Markdown { height: 100%; padding: 1; border: solid cyan; }
    """
    
    BINDINGS = [
        ("q", "quit", "Quit"),
        ("s", "scan", "Scan Current Dir"),
        ("a", "ask_ai", "AI Explain")
    ]

    def __init__(self):
        super().__init__()
        self.config = Config()
        self.issues = []
        self.ai = AIEngine(self.config)

    def compose(self) -> ComposeResult:
        yield Header("DevGuard TUI")
        with Horizontal():
            yield DataTable(id="issue_table")
            yield Markdown("# Select an issue\nPress 's' to scan current directory.", id="details")
        yield Footer()

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_columns("File", "Line", "Severity", "Description")
        table.cursor_type = "row"

    def action_scan(self) -> None:
        scanner = Scanner(os.getcwd(), self.config)
        self.issues = scanner.scan()
        
        table = self.query_one(DataTable)
        table.clear()
        
        for idx, issue in enumerate(self.issues):
            table.add_row(issue.file_path, str(issue.line_number), issue.severity, issue.description, key=str(idx))
            
    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        issue = self.issues[int(event.row_key.value)]
        details = self.query_one(Markdown)
        content = f"### {issue.category}\n**File:** {issue.file_path}:{issue.line_number}\n\n**Description:** {issue.description}\n\n**Code:**\n```python\n{issue.snippet}\n```"
        details.update(content)

    def action_ask_ai(self) -> None:
        table = self.query_one(DataTable)
        try:
            row_key = table.coordinate_to_cell_key(table.cursor_coordinate).row_key
            issue = self.issues[int(row_key.value)]
            details = self.query_one(Markdown)
            
            details.update(f"{details.markdown}\n\n---\n### 🤖 AI Analysis...\nThinking...")
            
            explanation = self.ai.explain_issue(issue)
            fix = self.ai.suggest_fix(issue)
            
            details.update(f"{details.markdown}\n**Explanation:** {explanation}\n\n**Suggested Fix:**\n{fix}")
        except Exception:
            pass # Ignore if no row is selected
