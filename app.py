from flask import Flask, render_template, request
from consulta_rede import buscar_rede_dados, listar_redes
from extrator_pdf import extrair_matricula_do_pdf
from consulta_playwright import consultar_matricula_no_portal
import os
import tempfile

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/rede", methods=["GET", "POST"])
def rede():
    dados = None
    if request.method == "POST":
        nome_rede = request.form.get("nome_rede", "")
        dados = buscar_rede_dados(nome_rede)
    redes_disponiveis = listar_redes()
    return render_template("rede.html", dados=dados, redes=redes_disponiveis)

@app.route("/matricula", methods=["GET", "POST"])
def matricula():
    dados = None
    if request.method == "POST":
        numero = request.form.get("numero_matricula", "").strip()

        arquivo_pdf = request.files.get("arquivo_pdf")
        if arquivo_pdf and arquivo_pdf.filename:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp:
                arquivo_pdf.save(temp.name)
                caminho_temp = temp.name
            numero = extrair_matricula_do_pdf(caminho_temp)
            os.remove(caminho_temp)

        if numero:
            try:
                dados = consultar_matricula_no_portal(numero)
            except Exception as erro:
                print("Erro ao consultar no portal:", erro)
                dados = None
        else:
            dados = None

    return render_template("matricula.html", dados=dados)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)