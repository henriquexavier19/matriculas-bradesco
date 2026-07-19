import re
from mistralai.client import Mistral
import config


def extrair_matricula_do_pdf(caminho_pdf: str) -> str | None:
    client = Mistral(api_key=config.MISTRAL_API_KEY)

    with open(caminho_pdf, "rb") as arquivo:
        arquivo_enviado = client.files.upload(
            file={"file_name": "documento.pdf", "content": arquivo},
            purpose="ocr"
        )

    url_assinada = client.files.get_signed_url(file_id=arquivo_enviado.id)

    resposta_ocr = client.ocr.process(
        model="mistral-ocr-latest",
        document={"type": "document_url", "document_url": url_assinada.url}
    )

    texto_completo = "\n".join(pagina.markdown for pagina in resposta_ocr.pages)

    padrao_matricula = re.compile(r"matr[ií]cula\s*n?[ºo°:]*\s*([\d.\-/]+)", re.IGNORECASE)
    padrao_carteira = re.compile(r"n[uú]mero da carteira\s*n?[ºo°:]*\s*([\d.\-/]+)", re.IGNORECASE)

    resultado = padrao_matricula.search(texto_completo) or padrao_carteira.search(texto_completo)

    if resultado:
        return resultado.group(1).strip()
    return None