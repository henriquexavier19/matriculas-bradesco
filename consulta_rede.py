import pandas as pd


def consultar_rede(nome_rede: str, caminho_planilha: str = "workbook_v1.xlsx") -> str:
    df = pd.read_excel(caminho_planilha)

    df["Nome da Rede"] = df["Nome da Rede"].astype(str).str.strip().str.upper()
    nome_rede = nome_rede.strip().upper()

    resultado = df[df["Nome da Rede"] == nome_rede]

    if resultado.empty:
        return f"Rede '{nome_rede}' NÃO HABILITADO PARA ATENDER."

    linhas = [f"Rede: {nome_rede}\n"]
    for _, linha in resultado.iterrows():
        especialidade = linha["Especialidade"]
        habilitada = str(linha["Habilitada"]).strip().upper()
        status = "SIM" if habilitada == "SIM" else "NÃO"
        linhas.append(f"Especialidade: {especialidade} | Habilitada: {status}")

    return "\n".join(linhas)

def buscar_rede_dados(nome_rede: str, caminho_planilha: str = "workbook_v1.xlsx") -> dict:
    df = pd.read_excel(caminho_planilha)
    df["Nome da Rede"] = df["Nome da Rede"].astype(str).str.strip().str.upper()
    nome_rede = nome_rede.strip().upper()

    resultado = df[df["Nome da Rede"] == nome_rede]

    if resultado.empty:
        return {"encontrada": False, "nome_rede": nome_rede, "especialidades": []}

    especialidades = []
    for _, linha in resultado.iterrows():
        habilitada = str(linha["Habilitada"]).strip().upper() == "SIM"
        especialidades.append({"nome": linha["Especialidade"], "habilitada": habilitada})

    return {"encontrada": True, "nome_rede": nome_rede, "especialidades": especialidades}
