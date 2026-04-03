from dataclasses import dataclass
from typing import Optional

@dataclass
class Issue:
    file_path: str
    line_number: int
    category: str
    description: str
    snippet: str
    severity: str = "HIGH"

    def to_dict(self) -> dict:
        return {
            "file": self.file_path,
            "line": self.line_number,
            "category": self.category,
            "description": self.description,
            "severity": self.severity
        }
