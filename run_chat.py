import sys
import os
from pathlib import Path

# Fix for "uv run gcli" imports in flat layout
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from gcli_utils import AppUtils
from gemini_service import GeminiService

def run_chat() -> None:
    utils = None
    service = None
    
    try:
        # Load config with strict validation
        cfg = AppUtils.load_yaml_config("config.yaml")
        
        utils = AppUtils(cfg)
        service = GeminiService(cfg, utils)
        
        # Initialize session
        gen_cfg = service.build_config()
        chat = service.start_session(gen_cfg)
        
        utils.console.print(f"[bold {utils.color_bot}]GCli Session Active. Use '/scan' for context.[/bold {utils.color_bot}]")

        while True:
            try:
                user_input = utils.get_multiline_input()
                if not user_input or user_input.lower() == 'exit':
                    break

                if user_input.lower() == '/scan':
                    context = utils.collect_project_context()
                    user_input = f"PROJECT CONTEXT:\n{context}\n\nReview this code."
                    utils.console.print("[blue]Context collected and sent.[/blue]")

                service.send_prompt(chat, user_input)

            except KeyboardInterrupt:
                utils.console.print(f"\n[yellow]Interrupted by user.[/yellow]")
                break

    except Exception as e:
        if utils:
            utils.console.print(f"[bold {utils.color_error}]Fatal Error:[/bold {utils.color_error}] {e}")
        else:
            print(f"Initialization Error: {e}")


if __name__ == "__main__":
    run_chat()
