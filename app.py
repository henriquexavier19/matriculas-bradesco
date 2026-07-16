from flask import Flask, render_template, request
from consulta_rede import buscar_rede_dados

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/rede-credenciada-bradesco-TC", methods=["GET", "POST"])
def rede():
    dados = None
    if request.method == "POST":
        nome_rede = request.form.get("nome_rede", "")
        dados = buscar_rede_dados(nome_rede)
    return render_template("rede.html", dados=dados)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)
