from PIL import Image, ImageDraw, ImageFont

tamanho = 256
img = Image.new("RGBA", (tamanho, tamanho), (0,0,0,0))
draw = ImageDraw.Draw(img)

cor_fundo = (19, 48, 63, 255) # mes azul  escuro da barra do app (#13303F)
draw.rounded_rectangle([(0, 0), (tamanho, tamanho)], radius=50, fill=cor_fundo)

texto = "IM"
try:
    fonte = ImageFont.truetype("arialbd.ttf", 120)
except:
    fonte = ImageFont.load_default()

caixa_texto = draw.textbbox((0, 0), texto, font=fonte)
largura_texto = caixa_texto[2] - caixa_texto[0]
altura_texto = caixa_texto[3] - caixa_texto[1]
posicao = ((tamanho - largura_texto) / 2 - caixa_texto[0], (tamanho - altura_texto) / 2 - caixa_texto[1])

draw.text(posicao, texto, font=fonte, fill="white")

img.save("icone.ico", format="ICO", sizes=[(16, 16), (32, 32), (48, 48), (128, 128), (256, 256)])
print("Ícone criado: icone.ico")