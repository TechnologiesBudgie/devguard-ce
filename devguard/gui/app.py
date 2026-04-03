from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                               QPushButton, QFileDialog, QTreeWidget, QTreeWidgetItem, 
                               QTextEdit, QLabel)
from devguard.core.config import Config
from devguard.core.scanner import Scanner
from devguard.ai.engine import AIEngine

class DevGuardGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DevGuard Security Scanner")
        self.resize(1000, 600)
        self.config = Config()
        self.ai = AIEngine(self.config)
        self.issues = []
        self.setup_ui()

    def setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        # Top Bar
        top_bar = QHBoxLayout()
        self.btn_select = QPushButton("Select Folder & Scan")
        self.btn_select.clicked.connect(self.scan_folder)
        
        self.lbl_status = QLabel("Ready")
        
        self.btn_ai = QPushButton("AI Explain (Selected)")
        self.btn_ai.clicked.connect(self.explain_issue)
        if not self.ai.is_ready:
            self.btn_ai.setEnabled(False)
            self.btn_ai.setText("AI Disabled/No Connection")

        top_bar.addWidget(self.btn_select)
        top_bar.addWidget(self.btn_ai)
        top_bar.addWidget(self.lbl_status)
        top_bar.addStretch()
        layout.addLayout(top_bar)

        # Main Split
        main_split = QHBoxLayout()
        
        # Issue Tree
        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(["File", "Line", "Issue"])
        self.tree.itemSelectionChanged.connect(self.on_select)
        main_split.addWidget(self.tree, 1)

        # Details Panel
        self.details = QTextEdit()
        self.details.setReadOnly(True)
        main_split.addWidget(self.details, 1)

        layout.addLayout(main_split)

    def scan_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Directory to Scan")
        if folder:
            self.lbl_status.setText(f"Scanning {folder}...")
            self.tree.clear()
            
            scanner = Scanner(folder, self.config)
            self.issues = scanner.scan()
            
            for idx, issue in enumerate(self.issues):
                item = QTreeWidgetItem([issue.file_path, str(issue.line_number), issue.category])
                item.setData(0, 99, idx) # Store index in user role
                self.tree.addTopLevelItem(item)
                
            self.lbl_status.setText(f"Found {len(self.issues)} issues.")

    def on_select(self):
        selected = self.tree.selectedItems()
        if selected:
            idx = selected[0].data(0, 99)
            issue = self.issues[idx]
            self.details.setText(f"File: {issue.file_path}:{issue.line_number}\nType: {issue.category}\n\nDescription:\n{issue.description}\n\nSnippet:\n{issue.snippet}")

    def explain_issue(self):
        selected = self.tree.selectedItems()
        if selected:
            idx = selected[0].data(0, 99)
            issue = self.issues[idx]
            self.details.append("\n\n--- AI Analysis ---")
            self.details.append("Thinking...")
            
            # Note: In a true prod app, this should run on a QThread to prevent GUI freezing.
            # Kept synchronous here for architectural clarity and brevity.
            explanation = self.ai.explain_issue(issue)
            self.details.append(f"\nExplanation: {explanation}")
            
            fix = self.ai.suggest_fix(issue)
            self.details.append(f"\nSuggested Fix:\n{fix}")
