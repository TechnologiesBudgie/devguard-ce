# DevGuard Community Edition
### Open Source Code Analysis and Security Auditing
  
---
*This software comes with ABSOLUTELY NO WARRANTY, to the extent permitted by applicable law.*
---
  
## 1. Overview
DevGuard Community Edition is a high-performance, offline-first security engine designed to identify hardcoded secrets, unsafe code patterns, and infrastructure misconfigurations. By prioritizing local execution, DevGuard ensures that sensitive code fragments never leave your local environment.

The tool is built with a strictly decoupled architecture, separating core scanning logic from its three primary interfaces: Command Line Interface (CLI), Terminal User Interface (TUI), and Graphical User Interface (GUI).

## 2. Core Features
* **Recursive Secret Detection:** Identifies AWS Access Keys, generic API tokens, and potential password leaks within configuration files and environment templates.
* **Static Pattern Analysis:** Detects high-risk code execution patterns such as `eval()`, `exec()`, and insecure `subprocess` calls across multiple languages (Python, JavaScript, Go).
* **Infrastructure Auditing:** Scans Dockerfiles for security anti-patterns, specifically identifying containers configured to run with elevated root privileges.
* **Multi-Interface Deployment:**
    * **CLI:** Optimized for integration into automated workflows.
    * **TUI:** Provides a keyboard-driven interactive dashboard for manual issue triage.
    * **GUI:** A desktop application built on the PySide6 (Qt) framework for high-level oversight.
* **Local AI Integration:** Supports Ollama for context-aware vulnerability explanation and remediation suggestions without sending code to the cloud.

## 3. Installation and Setup

### Prerequisites
* Python 3.11 or higher
* (Optional) Ollama for localized AI analysis

### Environment Configuration
1. Clone the repository:
   ```bash
   git clone https://github.com/devguard-community/devguard.git
   cd devguard
   ```
2. Initialize and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## 4. Operational Instructions

### Standard Directory Scan (CLI)
```bash
python run.py scan /path/to/target/directory
```

### Interactive Dashboard (TUI)
```bash
python run.py tui
```

### Desktop Application (GUI)
```bash
python run.py gui
```

### AI Module Configuration (Local Only)
To utilize the automated remediation features using local LLMs via Ollama:
```bash
export DEVGUARD_AI_PROVIDER="ollama"
export OLLAMA_MODEL="llama3"
python run.py ai enable
```

## 5. Configuration and Overrides
The scanner's behavior is managed via `.devguard.yml`. To ignore specific false positives within the source code, append the `# nosec` comment to the end of the relevant line.

---
**Released under the MIT and Apache 2.0 License.**
**Provided AS-IS and without ANY guarantee.**
