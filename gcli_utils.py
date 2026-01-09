import os
import re
import yaml
import sys
from pathlib import Path
from typing import Dict, Any
from rich.console import Console


class AppUtils:
    def __init__(self, config: Dict[str, Any]) -> None:
        self.config = config
        # Инициализация консоли — этот атрибут ищет run_chat.py
        self.console = Console()

        ui = config.get("ui", {})
        colors = ui.get("colors", {})

        self.color_bot = colors.get("bot", "green")
        self.color_error = colors.get("error", "red")


    @staticmethod
    def load_yaml_config(file_path: str) -> Dict[str, Any]:
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Config file not found: {file_path}")

        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        pattern = re.compile(r"\$\{(\w+)\}")

        def replace_env_var(match):
            var_name = match.group(1)
            value = os.getenv(var_name)
            if value is None:
                raise EnvironmentError(f"System variable '{var_name}' is not set.")
            return value.strip().strip('"').strip("'")

        processed = pattern.sub(replace_env_var, content)
        config = yaml.safe_load(processed)

        if not config or not config.get("auth", {}).get("api_key"):
            raise KeyError("Config Error: 'auth.api_key' is mandatory.")

        return config


    def collect_project_context(self) -> str:
        proc = self.config.get("processing", {})
        excludes = proc.get("exclude_patterns", [])

        root = Path(".")
        parts = []

        for item in root.rglob("*"):
            if not item.is_file():
                continue

            rel = item.relative_to(root)
            # Фильтруем скрытые папки (начинаются с точки) и паттерны из конфига
            if any(rel.match(p) or any(s.startswith('.') for s in rel.parts) for p in excludes):
                continue

            try:
                content = item.read_text(encoding='utf-8')
                parts.append(f"--- FILE: {rel} ---\n{content}")
            except (UnicodeDecodeError, PermissionError):
                continue

        return "\n\n".join(parts)


    def get_multiline_input(self) -> str:
        self.console.print("\n[bold cyan]User:[/bold cyan] [dim](Ctrl+Z/D to submit, 'exit' to quit)[/dim]")
        lines = sys.stdin.readlines()
        return "".join(lines).strip()
