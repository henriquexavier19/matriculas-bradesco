import customtkinter as ctk
from consulta_rede import buscar_rede_dados

ctk.set_appearance_mode("light")

COR_BARRA = "#13303F"
COR_HABILITADA_FUNDO = "#E6F4EA"
COR_HABILITADA_TEXTO = "#1E8E3E"
COR_NAO_HABILITADA_FUNDO = "#FCE8E6"
COR_NAO_HABILITADA_TEXTO = "#D93025"

janela = ctk.CTk()
janela.title("Innovex Management")
janela.geometry("750x550")
janela.configure(fg_color="white")

# --- Barra superior escura ---
barra_superior = ctk.CTkFrame(janela, fg_color=COR_BARRA, height=110, corner_radius=0)
barra_superior.pack(fill="x", side="top")
barra_superior.pack_propagate(False)

titulo_app = ctk.CTkLabel(
    barra_superior, text="INNOVEX MANAGEMENT",
    text_color="white", font=("Arial", 20, "bold")
)
titulo_app.pack(side="left", padx=30, pady=30)

# --- Área branca de conteúdo ---
area_conteudo = ctk.CTkFrame(janela, fg_color="white", corner_radius=0)
area_conteudo.pack(fill="both", expand=True, padx=30, pady=20)

titulo_tela = ctk.CTkLabel(
    area_conteudo, text="Consultar rede",
    text_color="black", font=("Arial", 18)
)
titulo_tela.pack(anchor="w", pady=(0, 15))

# --- Linha de busca: campo + botão lado a lado ---
linha_busca = ctk.CTkFrame(area_conteudo, fg_color="transparent")
linha_busca.pack(fill="x")

campo_nome = ctk.CTkEntry(linha_busca, placeholder_text="Digite o nome da rede", width=400, height=38)
campo_nome.pack(side="left", fill="x", expand=True)

# --- Área onde o resultado (cartão + tabela) vai aparecer ---
resultado_frame = ctk.CTkFrame(area_conteudo, fg_color="white", corner_radius=0)
resultado_frame.pack(fill="both", expand=True, pady=(20, 0))


def criar_badge(pai, habilitada: bool):
    if habilitada:
        cor_fundo, cor_texto, texto = COR_HABILITADA_FUNDO, COR_HABILITADA_TEXTO, "✓ Habilitada"
    else:
        cor_fundo, cor_texto, texto = COR_NAO_HABILITADA_FUNDO, COR_NAO_HABILITADA_TEXTO, "✕ Não habilitada"

    badge = ctk.CTkFrame(pai, fg_color=cor_fundo, corner_radius=12)
    ctk.CTkLabel(badge, text=texto, text_color=cor_texto, font=("Arial", 12, "bold")).pack(padx=12, pady=4)
    return badge


def ao_clicar_consultar():
    for widget in resultado_frame.winfo_children():
        widget.destroy()

    nome_rede = campo_nome.get()
    dados = buscar_rede_dados(nome_rede)

    if not dados["encontrada"]:
        ctk.CTkLabel(
            resultado_frame, text=f"Rede '{dados['nome_rede']}': NÃO HABILITADO para atender.",
            text_color="#D93025", font=("Arial", 13)
        ).pack(anchor="w", pady=10)
        return

    cartao_rede = ctk.CTkFrame(resultado_frame, fg_color="#F5F7FA", corner_radius=10)
    cartao_rede.pack(fill="x", pady=(0, 15))
    ctk.CTkLabel(
        cartao_rede, text=f"Rede:\n{dados['nome_rede']}",
        text_color="black", font=("Arial", 16, "bold"), justify="left"
    ).pack(anchor="w", padx=20, pady=15)

    cabecalho = ctk.CTkFrame(resultado_frame, fg_color="transparent")
    cabecalho.pack(fill="x", padx=5)
    ctk.CTkLabel(cabecalho, text="ESPECIALIDADE", text_color="#888888", font=("Arial", 11, "bold")).pack(side="left")
    ctk.CTkLabel(cabecalho, text="STATUS", text_color="#888888", font=("Arial", 11, "bold")).pack(side="right")

    for especialidade in dados["especialidades"]:
        linha = ctk.CTkFrame(resultado_frame, fg_color="#FAFAFA", corner_radius=8)
        linha.pack(fill="x", pady=4, padx=5)

        ctk.CTkLabel(linha, text=especialidade["nome"], text_color="black", font=("Arial", 13)).pack(
            side="left", padx=15, pady=10
        )

        badge = criar_badge(linha, especialidade["habilitada"])
        badge.pack(side="right", padx=15, pady=8)


botao_consultar = ctk.CTkButton(
    linha_busca, text="Consultar", width=120, height=38,
    fg_color=COR_BARRA, command=ao_clicar_consultar
)
botao_consultar.pack(side="left", padx=(10, 0))

janela.mainloop()