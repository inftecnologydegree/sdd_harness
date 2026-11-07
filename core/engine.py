import ollama
from core.tools import read_workspace_file, update_task_markdown

TOOLS_SCHEMA = [
    {
        'type': 'function',
        'function': {
            'name': 'update_task_markdown',
            'description': 'Updates tasks.md by changing a specific task from [ ] to [x].',
            'parameters': {
                'type': 'object',
                'properties': {
                    'filename': {
                        'type': 'string',
                        'description': 'The name of the file (always tasks.md).',
                    },
                    'completed_task': {
                        'type': 'string',
                        'description': 'The exact text string of the task that was just completed.',
                    }
                },
                'required': ['filename', 'completed_task'],
            },
        },
    }
]

def run_agent():
    specs = read_workspace_file("specs.md")
    tasks = read_workspace_file("tasks.md")

    if "Error" in specs or "Error" in tasks:
        print("❌ Erro: Certifique-se de que os arquivos specs.md e tasks.md existem na pasta /workspace.")
        return

    SYSTEM_PROMPT = f"""
You are an advanced SDD Autonomous Engineering Agent. 
Your behavior is strictly dictated by the product rules defined in the <SPECIFICATIONS> block.
Your progress is tracked strictly by the <TASKS_CHECKLIST> block.

<SPECIFICATIONS>
{specs}
</SPECIFICATIONS>

<TASKS_CHECKLIST>
{tasks}
</TASKS_CHECKLIST>

INSTRUCTIONS:
1. Identify the FIRST uncompleted task containing '- [ ]' in the checklist.
2. Formulate your engineering analysis or answer for that specific task.
3. Immediately call the 'update_task_markdown' tool to mark that exact task string as completed [x].
"""

    messages = [
        {'role': 'system', 'content': SYSTEM_PROMPT},
        {'role': 'user', 'content': "Execute the next uncompleted task in the checklist."}
    ]

    print("\n[Turn 1] Enviando contexto modular para o modelo local...")
    response = ollama.chat(model='llama3.2:3b', messages=messages, tools=TOOLS_SCHEMA)
    
    if response['message'].get('tool_calls'):
        for tool_call in response['message']['tool_calls']:
            func_name = tool_call['function']['name']
            args = tool_call['function']['arguments']
            
            if func_name == "update_task_markdown":
                print(f"\n👉 Agente chamou a ferramenta: {func_name}")
                print(f"   Tarefa Alvo: '{args.get('completed_task')}'")
                
                result = update_task_markdown(args.get('filename', 'tasks.md'), args.get('completed_task'))
                print(f"✅ {result}")
    else:
        print("\n--- Resposta do Modelo (Nenhuma ferramenta chamada) ---")
        print(response['message']['content'])
