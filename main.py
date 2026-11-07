import os
from core.engine import run_agent

def init_environment():
    """Garante que a pasta workspace e os arquivos básicos existam antes de rodar."""
    os.makedirs("workspace", exist_ok=True)
    os.makedirs("assets", exist_ok=True)

if __name__ == "__main__":
    init_environment()
    print("--- Inicializando SDD Harness Modular Engine ---")
    run_agent()
