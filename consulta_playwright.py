from playwright.sync_api import sync_playwright
import os
import config

print("MODULO consulta_playwright.py CARREGADO")


def _esperar_texto(pagina, seletor, tentativas=10, espera_ms=500):
    texto = ""
    for _ in range(tentativas):
        texto = pagina.locator(seletor).first.inner_text().strip()
        if texto:
            return texto
        pagina.wait_for_timeout(espera_ms)
    return texto


def consultar_matricula_no_portal(numero_matricula: str) -> dict:
    print("Iniciando o navegador...")
    with sync_playwright() as p:
        rodando_no_render = os.getenv("RENDER") is not None
        if rodando_no_render:
            navegador = p.chromium.launch(headless=True)
        else:
            navegador = p.chromium.launch(channel="chrome", headless=False)
        pagina = navegador.new_page(viewport={"width": 1366, "height": 768})

        print("Abrindo o site...")
        pagina.goto("https://wwws.bradescosaude.com.br/PCBS-GerenciadorPortal/td/loginReferenciado.do")

        print("Aguardando carregamento completo...")
        pagina.wait_for_load_state("networkidle")

        print("Preenchendo CPF, CNPJ e senha...")
        pagina.fill("#cpfRefPJ", config.BRADESCO_CPF)
        pagina.fill("#cnpjRef", config.BRADESCO_CNPJ)
        pagina.fill("#senhaRef", config.BRADESCO_SENHA)

        print("Enviando login...")
        pagina.click("#btLoginReferenciado")

        print("Aguardando login processar...")
        pagina.wait_for_timeout(3000)
        pagina.wait_for_load_state("networkidle")

        print("Abrindo o campo de busca de matrícula...")
        print("Preenchendo o número da matrícula na busca...")
        for _ in range(10):
            pagina.evaluate("var el = document.getElementById('sitBenefArea'); if (el) { el.style.display = 'block'; }")
            try:
                pagina.fill("#numCartao", numero_matricula, timeout=2000)
                break
            except Exception:
                pagina.wait_for_timeout(1000)
        else:
            raise Exception("Não foi possível abrir o campo de busca de matrícula.")

        pagina.click("#search_input")

        print("Aguardando resultado da busca...")
        pagina.wait_for_load_state("networkidle")

        print("Extraindo dados do beneficiário...")
        nome = _esperar_texto(pagina, "#nome-beneficiario")
        numero = _esperar_texto(pagina, "#numero")
        situacao = _esperar_texto(pagina, "#situacao ~ p")

        navegador.close()

        return {
            "encontrada": True,
            "nome": nome,
            "numero": numero,
            "situacao": situacao,
        }