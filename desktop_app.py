import customtkinter as ctk
from tkinter import filedialog
from consulta_rede import buscar_rede_dados, listar_redes
from extrator_pdf import extrair_matricula_do_pdf
from consulta_playwright import consultar_matricula_no_portal

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

# --- Botões de navegação (lado direito da barra) ---
menu_navegacao = ctk.CTkFrame(barra_superior, fg_color="transparent")
menu_navegacao.pack(side="right", padx=30, pady=30)

# --- Área branca de conteúdo (aqui a tela troca) ---
area_conteudo = ctk.CTkFrame(janela, fg_color="white", corner_radius=0)
area_conteudo.pack(fill="both", expand=True, padx=30, pady=20)


def limpar_area_conteudo():
    for widget in area_conteudo.winfo_children():
        widget.destroy()


def criar_badge(pai, habilitada: bool):
    if habilitada:
        cor_fundo, cor_texto, texto = COR_HABILITADA_FUNDO, COR_HABILITADA_TEXTO, "✓ Habilitada"
    else:
        cor_fundo, cor_texto, texto = COR_NAO_HABILITADA_FUNDO, COR_NAO_HABILITADA_TEXTO, "✕ Não habilitada"

    badge = ctk.CTkFrame(pai, fg_color=cor_fundo, corner_radius=12)
    ctk.CTkLabel(badge, text=texto, text_color=cor_texto, font=("Arial", 12, "bold")).pack(padx=12, pady=4)
    return badge


# ========================================================
# TELA 1: CONSULTAR REDE
# ========================================================
def mostrar_tela_rede():
    limpar_area_conteudo()

    titulo_tela = ctk.CTkLabel(
        area_conteudo, text="Consultar rede",
        text_color="black", font=("Arial", 18)
    )
    titulo_tela.pack(anchor="w", pady=(0, 15))

    linha_busca = ctk.CTkFrame(area_conteudo, fg_color="transparent")
    linha_busca.pack(fill="x")

    redes_disponiveis = listar_redes()

    campo_nome = ctk.CTkComboBox(
        linha_busca,
        values=redes_disponiveis,
        width=400,
        height=38,
        corner_radius=6,
        fg_color="white",
        text_color="black",
        border_color="#cccccc",
        button_color=COR_BARRA,
        button_hover_color="#032735",
        dropdown_fg_color="white",
        dropdown_text_color="black",
        dropdown_hover_color="#F5F7FA",
    )
    campo_nome.set("")
    campo_nome.pack(side="left", fill="x", expand=True)

    resultado_frame = ctk.CTkFrame(area_conteudo, fg_color="white", corner_radius=0)
    resultado_frame.pack(fill="both", expand=True, pady=(20, 0))

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


# ========================================================
# TELA 2: CONSULTAR MATRÍCULA
# ========================================================
def mostrar_tela_matricula():
    limpar_area_conteudo()

    titulo_tela = ctk.CTkLabel(
        area_conteudo, text="Consultar matrícula",
        text_color="black", font=("Arial", 18)
    )
    titulo_tela.pack(anchor="w", pady=(0, 15))

    resultado_frame = ctk.CTkFrame(area_conteudo, fg_color="white", corner_radius=0)

    def mostrar_resultado(dados):
        for widget in resultado_frame.winfo_children():
            widget.destroy()

        if dados and dados.get("encontrada"):
            linha_resultado = ctk.CTkFrame(resultado_frame, fg_color="transparent")
            linha_resultado.pack(anchor="w", pady=15, fill="x")

            texto_resultado = (
                f"Beneficiário: {dados['nome']}\n"
                f"Matrícula: {dados['numero']}\n"
                f"Situação: {dados['situacao']}"
            )

            ctk.CTkLabel(
                linha_resultado, text=texto_resultado,
                text_color="black", font=("Arial", 16, "bold"), justify="left"
            ).pack(side="left")

            def ao_clicar_copiar():
                janela.clipboard_clear()
                janela.clipboard_append(dados["numero"])

            ctk.CTkButton(
                linha_resultado, text="Copiar número", width=120, height=32,
                fg_color=COR_BARRA, command=ao_clicar_copiar
            ).pack(side="left", padx=(20, 0))
        else:
            ctk.CTkLabel(
                resultado_frame, text="Não foi possível encontrar a matrícula.",
                text_color="#D93025", font=("Arial", 13)
            ).pack(anchor="w", pady=15)

        resultado_frame.pack(fill="both", expand=True, pady=(20, 0))

    def consultar_e_mostrar(numero):
        if not numero:
            mostrar_resultado(None)
            return
        try:
            dados = consultar_matricula_no_portal(numero)
        except Exception as erro:
            print("Erro ao consultar no portal:", erro)
            dados = None
        mostrar_resultado(dados)

    # --- Opção 1: enviar PDF ---
    bloco_pdf = ctk.CTkFrame(area_conteudo, fg_color="#F5F7FA", corner_radius=10)
    bloco_pdf.pack(fill="x", pady=(0, 15))

    ctk.CTkLabel(
        bloco_pdf, text="Opção 1: Enviar PDF",
        text_color="black", font=("Arial", 14, "bold")
    ).pack(anchor="w", padx=20, pady=(15, 5))

    def ao_clicar_selecionar_pdf():
        caminho_arquivo = filedialog.askopenfilename(
            title="Selecione o PDF",
            filetypes=[("Arquivos PDF", "*.pdf")]
        )
        if not caminho_arquivo:
            return
        matricula = extrair_matricula_do_pdf(caminho_arquivo)
        consultar_e_mostrar(matricula)

    botao_pdf = ctk.CTkButton(
        bloco_pdf, text="Selecionar PDF", width=160, height=38,
        fg_color=COR_BARRA, command=ao_clicar_selecionar_pdf
    )
    botao_pdf.pack(anchor="w", padx=20, pady=(0, 15))

    # --- Opção 2: digitar manualmente ---
    bloco_manual = ctk.CTkFrame(area_conteudo, fg_color="#F5F7FA", corner_radius=10)
    bloco_manual.pack(fill="x")

    ctk.CTkLabel(
        bloco_manual, text="Opção 2: Digitar o número",
        text_color="black", font=("Arial", 14, "bold")
    ).pack(anchor="w", padx=20, pady=(15, 5))

    linha_manual = ctk.CTkFrame(bloco_manual, fg_color="transparent")
    linha_manual.pack(fill="x", padx=20, pady=(0, 15))

    campo_matricula = ctk.CTkEntry(
        linha_manual, width=300, height=38,
        placeholder_text="Digite o número da matrícula"
    )
    campo_matricula.pack(side="left", fill="x", expand=True)

    def ao_clicar_consultar_manual():
        consultar_e_mostrar(campo_matricula.get().strip())

    botao_manual = ctk.CTkButton(
        linha_manual, text="Consultar", width=120, height=38,
        fg_color=COR_BARRA, command=ao_clicar_consultar_manual
    )
    botao_manual.pack(side="left", padx=(10, 0))


# --- Botões de navegação (ficam depois das funções acima, porque usam elas no "command") ---
botao_nav_rede = ctk.CTkButton(
    menu_navegacao, text="Rede", width=100, height=32,
    fg_color="transparent", hover_color="#032735",
    command=mostrar_tela_rede
)
botao_nav_rede.pack(side="left", padx=(0, 10))

botao_nav_matricula = ctk.CTkButton(
    menu_navegacao, text="Matrícula", width=100, height=32,
    fg_color="transparent", hover_color="#032735",
    command=mostrar_tela_matricula
)
botao_nav_matricula.pack(side="left")

# --- Tela que abre por padrão ---
mostrar_tela_rede()

janela.mainloop()