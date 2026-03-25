from flask import Flask, render_template_string, request
from tools.gerador_sql.actions.materia_prima import gerar_sql_materia_prima

app = Flask(__name__)

# Template HTML minimalista embutido (facilita o PyInstaller depois)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>implantools - Menu</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 40px; background-color: #f4f4f9; color: #333; }
        .container { max-width: 800px; margin: auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }
        h1 { text-align: center; color: #2c3e50; border-bottom: 2px solid #eee; padding-bottom: 10px;}
        .tool-section { margin-top: 30px; }
        .tool-section h2 { color: #34495e; font-size: 1.2em; margin-bottom: 15px; }
        h3 { color: #34495e; font-size: 1.0em; margin-top: 20px; margin-bottom: 10px; }
        button { background-color: #2980b9; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; font-size: 1em; transition: background 0.3s; }
        button:hover { background-color: #1a5276; }
        textarea, input[type="file"] { width: 100%; padding: 8px; margin-bottom: 10px; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box; }
        .code-box { margin-top: 20px; padding: 15px; background: #272822; color: #f8f8f2; border-radius: 5px; font-family: monospace; white-space: pre-wrap; }
    </style>
    <script>
        function copyToClipboard(elementId) {
            const textToCopy = document.getElementById(elementId).innerText;
            navigator.clipboard.writeText(textToCopy).then(() => {
                // Opcional: feedback para o usuário
                alert('Copiado para a área de transferência!');
            }).catch(err => {
                console.error('Erro ao copiar texto: ', err);
                alert('Falha ao copiar.');
            });
        }
    </script>
</head>
<body>
    <div class="container">
        <h1>🛠️ implantools</h1>
        
        <div class="tool-section" style="text-align: center;">
            <h2>Menu de Ferramentas</h2>
            <div style="display: flex; gap: 10px; justify-content: center; margin-bottom: 30px;">
                <form action="/gerador-sql/materia-prima" method="GET">
                    <button type="submit">Gerar SQL - Matéria Prima</button>
                </form>
                <form action="/gerador-sql/ncm" method="GET">
                    <button type="submit">Gerar SQL - Verificar NCMs</button>
                </form>
            </div>
        </div>

        {% if active_tool == 'ncm' %}
        <form action="/gerador-sql/ncm" method="POST" enctype="multipart/form-data" style="margin-top: 20px; padding: 15px; background-color: #ecf0f1; border-radius: 5px;">
            <h3>Pesquisa de NCM</h3>
            <label for="ncm_text">Lista de NCMs (separados por vírgula ou por linha):</label>
            <textarea id="ncm_text" name="ncm_text" rows="4"></textarea>
            
            <label for="ncm_file">Ou carregue um arquivo de texto (.txt, .csv):</label>
            <input type="file" id="ncm_file" name="ncm_file" accept=".txt,.csv">
            
            <button type="submit">Gerar SQL NCM</button>
        </form>
        {% endif %}

        {% if active_tool == 'materia_prima' %}
        <div style="margin-top: 20px; padding: 15px; background-color: #ecf0f1; border-radius: 5px;">
            <h3>Matéria Prima</h3>
            <p>Comando SQL de rotina gerado abaixo:</p>
        </div>
        {% endif %}

        {% if resultado_sql %}
        <div style="text-align: right;">
             <button onclick="copyToClipboard('code-output')" style="margin-top: 20px; margin-bottom: -15px; padding: 5px 10px; font-size: 0.8em;">Copiar</button>
        </div>
        <div id="code-output" class="code-box">{{ resultado_sql }}</div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, active_tool=None)

@app.route('/gerador-sql/materia-prima')
def web_materia_prima():
    # Consome a lógica da pasta tools/
    resultado = gerar_sql_materia_prima()
    return render_template_string(HTML_TEMPLATE, active_tool='materia_prima', resultado_sql=resultado)

@app.route('/gerador-sql/ncm', methods=['GET', 'POST'])
def web_ncm():
    if request.method == 'GET':
        return render_template_string(HTML_TEMPLATE, active_tool='ncm')
        
    from tools.gerador_sql.actions.ncm_query import gerar_sql_ncm
    ncms = []
    
    ncm_text = request.form.get('ncm_text', '')
    if ncm_text:
        ncms.extend(ncm_text.replace(',', '\n').split('\n'))
        
    ncm_file = request.files.get('ncm_file')
    if ncm_file and ncm_file.filename:
        content = ncm_file.read().decode('utf-8', errors='ignore')
        ncms.extend(content.replace(',', '\n').split('\n'))
        
    resultado = gerar_sql_ncm(ncms)
    return render_template_string(HTML_TEMPLATE, active_tool='ncm', resultado_sql=resultado)

def iniciar_servidor_web():
    print("[*] Iniciando interface Web em http://127.0.0.1:5000")
    print("[*] Pressione CTRL+C para encerrar.")
    # Rodando sem debug para ambiente de produção/PyInstaller
    app.run(host='127.0.0.1', port=5000, debug=False)