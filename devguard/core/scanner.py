import re
from pathlib import Path
from typing import List
from devguard.core.models import Issue
from devguard.core.config import Config

RULES = {
    "AWS_KEY": (r"AKIA[0-9A-Z]{16}", "Hardcoded AWS Access Key detected."),
    "GENERIC_SECRET": (r"(?i)(password|secret|token|api_key)\s*[:=]\s*['\"][a-zA-Z0-9\-_]{16,}['\"]", "Possible hardcoded secret/token."),
    # Negative lookbehind ensures we don't flag PySide6/Qt 'app.exec()'
    "UNSAFE_EVAL": (r"(?<!app\.)\b(eval|exec)\s*\(", "Unsafe use of eval() or exec()."),
    "UNSAFE_SUBPROCESS": (r"subprocess\.Popen\([^)]*shell=True", "Unsafe subprocess execution with shell=True."),
    "TODO_FIXME": (r"(?i)#\s*(TODO|FIXME)", "Unresolved TODO or FIXME comment.")
}

class Scanner:
    def __init__(self, target_dir: str, config: Config):
        self.target_dir = Path(target_dir)
        self.config = config

    def _is_ignored(self, path: Path) -> bool:
        if path.suffix in self.config.ignore_extensions:
            return True
        for part in path.parts:
            if part in self.config.ignore_dirs:
                return True
        return False

    def scan(self) -> List[Issue]:
        issues = []
        for file_path in self.target_dir.rglob("*"):
            if file_path.is_file() and not self._is_ignored(file_path):
                issues.extend(self._scan_file(file_path))
        return issues

    def _scan_file(self, file_path: Path) -> List[Issue]:
        issues = []
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                for line_num, line in enumerate(f, 1):
                    # Industry standard: allow devs to explicitly ignore a line
                    if "# nosec" in line:
                        continue
                        
                    for rule_id, (pattern, desc) in RULES.items():
                        if re.search(pattern, line):
                            issues.append(Issue(
                                file_path=str(file_path),
                                line_number=line_num,
                                category=rule_id,
                                description=desc,
                                snippet=line.strip()[:100]
                            ))
                            
            if file_path.name == "Dockerfile":
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    if "USER root" in content or "USER" not in content:
                         issues.append(Issue(
                            file_path=str(file_path),
                            line_number=0,
                            category="DOCKER_ROOT",
                            description="Dockerfile runs as root (no USER instruction found).",
                            snippet=""
                        ))
        except (UnicodeDecodeError, PermissionError):
            pass 
        except Exception as e:
            print(f"Error scanning {file_path}: {e}")
            
        return issues
