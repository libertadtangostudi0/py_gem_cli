from pathlib import Path
from typing import Dict, Any, Optional
from google import genai
from google.genai import types
from rich.markdown import Markdown


class GeminiService:
    def __init__(self, config: Dict[str, Any], utils: Any) -> None:
        self.config = config
        self.utils = utils
        
        # Taking API key directly from config as it was already validated
        api_key = self.config["auth"]["api_key"]
        self.client = genai.Client(api_key=api_key)


    def build_config(self) -> types.GenerateContentConfig:
        m_set = self.config["model_settings"]
        p_set = self.config["processing"]
        
        sys_instr = None
        s_path = Path(p_set.get("system_instruction_path", ""))
        if s_path.exists():
            sys_instr = s_path.read_text(encoding="utf-8")

        return types.GenerateContentConfig(
            temperature=m_set.get("temperature"),
            top_p=m_set.get("top_p"),
            max_output_tokens=m_set.get("max_tokens"),
            system_instruction=sys_instr
        )


    def start_session(self, gen_config: types.GenerateContentConfig) -> Any:
        model_name = self.config["model_settings"]["name"]
        return self.client.chats.create(model=model_name, config=gen_config)


    def send_prompt(self, session: Any, text: str) -> None:
        try:
            show_spin = self.config.get("ui", {}).get("show_spinner", True)
            
            if show_spin:
                with self.utils.console.status("[bold yellow]Thinking...", spinner="dots"):
                    resp = session.send_message(text)
            else:
                resp = session.send_message(text)
                
            self._display(resp.text)
        except Exception as e:
            self.utils.console.print(f"[bold {self.utils.color_error}]API Error:[/bold {self.utils.color_error}] {e}")


    def _display(self, text: Optional[str]) -> None:
        if not text: return
        c = self.utils.color_bot
        self.utils.console.print(f"\n[bold {c}]— GEMINI —[/bold {c}]")
        self.utils.console.print(Markdown(text))
        self.utils.console.print(f"[bold {c}]" + "—" * 50 + f"[/bold {c}]\n")
