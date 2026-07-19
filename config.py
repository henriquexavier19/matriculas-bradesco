import os
from dotenv import load_dotenv

load_dotenv()

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
BRADESCO_CPF = os.getenv("BRADESCO_CPF")
BRADESCO_CNPJ = os.getenv("BRADESCO_CNPJ")
BRADESCO_SENHA = os.getenv("BRADESCO_SENHA")