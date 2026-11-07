import json
import ollama
from core.tools import read_workspace_file, update_task_markdown, create_code_file

TOOLS_SCHEMA = [
    {
        'type': 'function',
        'function': {
            'name': 'update_task_markdown',
            'description': 'Updates tasks.md by changing a specific task from [ ] to [x].',
            'parameters': {
                'type': 'object',
                'properties': {
                    'filename': { 'type': 'string', 'description': 'Always tasks.md' },
                    'completed_task': { 'type': 'string', 'description': 'The exact task text string.' }
                },
                'required': ['filename', 'completed_task'],
            },
        },
    },
    {
        'type': 'function',
        'function': {
            'name': 'create_code_file',
            'description': 'Creates a brand new source file inside the workspace containing specific code.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'filename': { 'type': 'string', 'description': 'The file target name (e.g. logger.py)' },
                    'source_code': { 'type': 'string', 'description': 'The complete code text to write.' }
                },
                'required': ['filename', 'source_code'],
            },
        },
    }
]

def run_agent():
    specs = read_workspace_file("specs.md")
    tasks = read_workspace_file("tasks.md")

    if "Error" in specs or "Error" in tasks:
        print("❌ Erro: Arquivos specs.md e tasks.md necessitam existir dentro de /workspace.")
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
2. If the task requires writing or modifying code, call the 'create_code_file' tool.
3. Immediately after completing the task, call the 'update_task_markdown' tool to mark that task string as completed [x].
"""

    messages = [
        {'role': 'system', 'content': SYSTEM_PROMPT},
        {'role': 'user', 'content': "Execute the next uncompleted task in the checklist."}
    ]

    print("\n[Turn 1] Enviando contexto modular para o modelo local...")
    # Using a developer-centric coding model like qwen2.5-coder or llama3.1 is recommended here
    response = ollama.chat(model='llama3.2:3b', messages=messages, tools=TOOLS_SCHEMA)
    
    if response['message'].get('tool_calls'):
        # Track if the agent calls multiple tools in parallel
        for tool_call in response['message']['tool_calls']:
            func_name = tool_call['function']['name']
            args = tool_call['function']['arguments']
            
            print(f"\n👉 Agente chamou a ferramenta: {func_name}")
            
            if func_name == "create_code_file":
                print(f"   Criando arquivo: '{args.get('filename')}'")
                result = create_code_file(args.get('filename'), args.get('source_code'))
                print(f"✅ {result}")
                
            elif func_name == "update_task_markdown":
                print(f"   Tarefa Alvo: '{args.get('completed_task')}'")
                result = update_task_markdown(args.get('filename', 'tasks.md'), args.get('completed_task'))
                print(f"✅ {result}")
    else:
        print("\n--- Resposta do Modelo ---")
        print(response['message']['content'])
