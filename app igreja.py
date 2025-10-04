from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)

# --- Usuários cadastrados (usuário -> senha) ---
membros = {
    "joao": "1234",
    "maria": "abcd",
    "ana": "senha1",
    "paulo": "4321"
}

# --- Propostas em votação ---
propostas = {
    1: "Aprovar a reforma do telhado da igreja",
    2: "Compra de novo equipamento de som",
    3: "Organização de novo grupo de jovens"
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
                return "Você já votou nesta assembleia."
            return redirect(url_for("votar", usuario=usuario))
        return "Usuário ou senha incorretos."
    return render_template_string('''
        <h2>Login de Membro</h2>
        <form method="post">
            Usuário: <input type="text" name="usuario"><br>
            Senha: <input type="password" name="senha"><br>
            <input type="submit" value="Entrar">
        </form>
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

            # 🔹 Mostrar no terminal
            print(f"Usuário '{usuario}' votou em: {propostas[escolha]}")
            mostrar_resultado_terminal()

            # 🔹 Salvar em arquivo votos.txt
            with open("votos.txt", "a", encoding="utf-8") as f:
                f.write(f"Usuário '{usuario}' votou em: {propostas[escolha]}\n")

            return redirect(url_for("resultado"))
        return "Proposta inválida."
    opcoes = "".join([f'<input type="radio" name="proposta" value="{pid}"> {desc}<br>'
                      for pid, desc in propostas.items()])
    return render_template_string(f'''
        <h2>Propostas em Votação</h2>
        <form method="post">
            {opcoes}
            <input type="submit" value="Votar">
        </form>
    ''')

@app.route("/resultado")
def resultado():
    total = sum(resultado_votacao.values())
    lista = "".join([f"<li>{desc}: {resultado_votacao[pid]} votos</li>"
                     for pid, desc in propostas.items()])
    return render_template_string(f'''
        <h2>Resultado Parcial</h2>
        <ul>{lista}</ul>
        <p>Total de votos: {total}</p>
        <a href="/">Voltar</a>
    ''')

# ------------------- MAIN -------------------
if __name__ == "__main__":
    print("Sistema de votação iniciado! Acesse via navegador na mesma rede Wi-Fi.")
    app.run(host="0.0.0.0", port=5000, debug=True)