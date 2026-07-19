print("SCRIPT DE TESTE INICIADO")

try:
    from consulta_playwright import consultar_matricula_no_portal
    print("IMPORT OK")

    resultado = consultar_matricula_no_portal("954460167282004")
    print("--- RESULTADO ---")
    print(resultado)
except Exception as erro:
    import traceback
    print("ERRO CAPTURADO:")
    traceback.print_exc()

print("SCRIPT DE TESTE FINALIZADO")