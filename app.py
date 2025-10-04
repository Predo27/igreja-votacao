from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)

# --- Usuários cadastrados (usuário -> senha) ---
membros = {
    "artur": "16ar",
    "mateus": "17ma",
    "ana": "senha1",
    "paulo": "4321"
}

# --- Propostas em votação ---
propostas = {
    1: "Passeio para o Museu do Amanhã.",
    2: "Passeio para a Biblioteca Nacional.",
    3: "Passeio para o Bioparque."
}

# --- Registro de votos (memória) ---
votos = {}
resultado_votacao = {pid: 0 for pid in propostas}

# ------------------- FUNÇÃO AUXILIAR -------------------
def mostrar_resultado_terminal():
    total = sum(resultado_votacao.values())
    print("\n=== RESULTADO PARCIAL ===")
    for pid, desc in propostas.items():
        print(f"{desc}: {resultado_votacao[pid]} votos")
    print(f"Total de votos: {total}\n")

# ------------------- ROTAS -------------------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form["usuario"].strip().lower()
        senha = request.form["senha"]
        if usuario in membros and membros[usuario] == senha:
            if usuario in votos:
                return "Você já votou!."
            return redirect(url_for("votar", usuario=usuario))
        return "Usuário ou senha incorretos."
    return render_template_string('''
        <html>
        <head>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                body {
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    background: #f0f2f5;
                    font-family: Arial, sans-serif;
                }
                .container {
                    background: white;
                    padding: 25px;
                    border-radius: 12px;
                    box-shadow: 0 0 15px rgba(0,0,0,0.1);
                    width: 90%;
                    max-width: 400px;
                    text-align: center;
                }
                h2 {
                    margin-bottom: 20px;
                    color: #333;
                }
                input[type=text], input[type=password] {
                    width: 90%;
                    padding: 12px;
                    margin: 10px 0;
                    border: 1px solid #ccc;
                    border-radius: 8px;
                    font-size: 16px;
                }
                input[type=submit] {
                    background-color: #007bff;
                    color: white;
                    border: none;
                    padding: 12px 20px;
                    border-radius: 8px;
                    cursor: pointer;
                    font-size: 16px;
                    width: 100%;
                }
                input[type=submit]:hover {
                    background-color: #0056b3;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h2>Login de Membro</h2>
                <form method="post">
                    <input type="text" name="usuario" placeholder="Usuário"><br>
                    <input type="password" name="senha" placeholder="Senha"><br>
                    <input type="submit" value="Entrar">
                </form>
            </div>
        </body>
        </html>
    ''')

@app.route("/votar/<usuario>", methods=["GET", "POST"])
def votar(usuario):
    if request.method == "POST":
        try:
            escolha = int(request.form["proposta"])
        except (KeyError, ValueError):
            return "Proposta inválida."
        if escolha in propostas:
            votos[usuario] = escolha
            resultado_votacao[escolha] += 1

            print(f"Usuário '{usuario}' votou em: {propostas[escolha]}")
            mostrar_resultado_terminal()

            with open("votos.txt", "a", encoding="utf-8") as f:
                f.write(f"Usuário '{usuario}' votou em: {propostas[escolha]}\n")

            return redirect(url_for("resultado"))
        return "Proposta inválida."

    opcoes = "".join([
        f'<label><input type="radio" name="proposta" value="{pid}"> {desc}</label><br><br>'
        for pid, desc in propostas.items()
    ])

    return render_template_string(f'''
        <html>
        <head>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                body {{
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    background: #f0f2f5;
                    font-family: Arial, sans-serif;
                }}
                .container {{
                    background: white;
                    padding: 25px;
                    border-radius: 12px;
                    box-shadow: 0 0 15px rgba(0,0,0,0.1);
                    width: 90%;
                    max-width: 450px;
                    text-align: left;
                }}
                h2 {{
                    text-align: center;
                    color: #333;
                }}
                label {{
                    font-size: 18px;
                }}
                input[type=submit] {{
                    background-color: #28a745;
                    color: white;
                    border: none;
                    padding: 14px 20px;
                    border-radius: 8px;
                    cursor: pointer;
                    font-size: 18px;
                    width: 100%;
                }}
                input[type=submit]:hover {{
                    background-color: #1e7e34;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h2>Propostas em Votação</h2>
                <form method="post">
                    {opcoes}
                    <br>
                    <input type="submit" value="Votar">
                </form>
            </div>
        </body>
        </html>
    ''')

@app.route("/resultado")
def resultado():
    total = sum(resultado_votacao.values())
    lista = "".join([f"<li>{desc}: {resultado_votacao[pid]} votos</li>"
                     for pid, desc in propostas.items()])
    return render_template_string(f'''
        <html>
        <head>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background: #f9f9f9;
                    text-align: center;
                    padding: 20px;
                }}
                ul {{
                    list-style: none;
                    padding: 0;
                }}
                li {{
                    font-size: 18px;
                    margin: 10px 0;
                }}
                a {{
                    display: inline-block;
                    margin-top: 20px;
                    text-decoration: none;
                    color: white;
                    background: #007bff;
                    padding: 10px 20px;
                    border-radius: 8px;
                }}
                a:hover {{
                    background: #0056b3;
                }}
            </style>
        </head>
        <body>
            <h2>Resultado Parcial</h2>
            <ul>{lista}</ul>
            <p>Total de votos: {total}</p>
            <a href="/">Voltar</a>
        </body>
        </html>
    ''')

# ------------------- MAIN -------------------
if __name__ == "__main__":
    print("Sistema de votação iniciado! Acesse via navegador na mesma rede Wi-Fi.")
    app.run(host="0.0.0.0", port=5000, debug=True)
