import os
import re

WORKSPACE_DIR = "workspace"

def read_workspace_file(filename: str) -> str:
    """Lê com segurança um arquivo de dentro do diretório workspace."""
    filepath = os.path.join(WORKSPACE_DIR, filename)
    if not os.path.exists(filepath):
        return f"Error: File '{filename}' does not exist in workspace."
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()

def update_task_markdown(filename: str, completed_task: str) -> str:
    """Encontra a primeira tarefa não concluída no tasks.md e marca como [x]."""
    filepath = os.path.join(WORKSPACE_DIR, filename)
    try:
        if not os.path.exists(filepath):
            return f"Error: '{filename}' not found."
            
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        
        escaped_task = re.escape(completed_task.strip())
        pattern = rf"-\s*\[\s*\]\s*{escaped_task}"
        
        if re.search(pattern, content, re.IGNORECASE):
            updated_content = re.sub(pattern, f"- [x] {completed_task.strip()}", content, count=1, flags=re.IGNORECASE)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(updated_content)
            return f"Success: Marked '{completed_task}' as completed."
        else:
            return f"Notice: Uncompleted task matching '{completed_task}' not found."
    except Exception as e:
        return f"Error updating task file: {str(e)}"
