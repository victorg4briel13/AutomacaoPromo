from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
import os
import textwrap

def carregar_imagem(imagem_origem):
    if imagem_origem.startswith("http://") or imagem_origem.startswith("https://"):
        response = requests.get(imagem_origem)
        imagem = Image.open(BytesIO(response.content))
    else:
        imagem = Image.open(imagem_origem)
    return imagem.convert("RGBA")

def gerar_card(nome, descricao, preco, frete_gratis, temcupom, cupom, imagem_produto_path, imagem_moldura_path, imagem_moldura_frete_path):
    # Tamanho do card 1080x1350 (Instagram retrato)
    largura = 1080
    altura = 1350

    # Criar fundo branco
    card = Image.new("RGBA", (largura, altura), "white")

    # Carregar e redimensionar imagem do produto
    imagem_produto = carregar_imagem(imagem_produto_path).resize((1080, 1080))
    pos_img = ((largura - 1080) // 2, 0)  # centralizada horizontalmente
    card.paste(imagem_produto, pos_img, imagem_produto)
    
    # Carregar moldura
    if frete_gratis:
        moldura = carregar_imagem(imagem_moldura_frete_path).resize((largura, altura))
        card.paste(moldura, (0, 0), moldura)
    else:
        moldura = carregar_imagem(imagem_moldura_path).resize((largura, altura))
        card.paste(moldura, (0, 0), moldura)

    draw = ImageDraw.Draw(card)

    # Fontes e textos
    try:
        fonte_titulo = ImageFont.truetype("Fontes\Montserrat-SemiBoldItalic.otf", 80)
        fonte_texto = ImageFont.truetype("Fontes\Montserrat-Medium.otf", 45)
        fonte_cupom = ImageFont.truetype("Fontes\Montserrat-BoldItalic.otf", 45)
        fonte_cupom2 = ImageFont.truetype("Fontes\Montserrat-Bold.otf", 45)
        fonte_preco = ImageFont.truetype("Fontes\Montserrat-BoldItalic.otf", 110)
        fonte_decimal = ImageFont.truetype("Fontes\Montserrat-BoldItalic.otf", 50)
    except:
        fonte_titulo = fonte_texto = ImageFont.load_default()

    # Título
    def titulo(texto, fonte, cor):
        bbox = draw.textbbox((0, 0), texto, font=fonte)
        largura_texto = bbox[2] - bbox[0]
        x = (largura - largura_texto) // 2
        draw.text((x + 60, 100), texto, font=fonte, fill=cor)

    titulo(nome, fonte_titulo, "white")
    #--------------------------------------

    # Preço
    def designpreco(valor): 
        parte_inteira, parte_decimal = valor.split(',')

        # Calcula largura para centralizar o preço inteiro + decimal
        bbox_inteiro = draw.textbbox((0, 0), parte_inteira, font=fonte_preco)
        bbox_decimal = draw.textbbox((0, 0), f",{parte_decimal}", font=fonte_decimal)
        largura_total = (bbox_inteiro[2] - bbox_inteiro[0]) + (bbox_decimal[2] - bbox_decimal[0])
        x = ((largura - largura_total) // 2) + 355
        y = 1120

        # Desenha parte inteira
        draw.text((x, y), parte_inteira, font=fonte_preco, fill="black")
        # Desenha parte decimal
        x_decimal = x + (bbox_inteiro[2] - bbox_inteiro[0])
        draw.text((x_decimal, y + 15), f",{parte_decimal}", font=fonte_decimal, fill="black")

        #draw.text((760, 1150), f"{valor}", font=fonte_preco, fill="black")

    designpreco(preco)
    #--------------------------------------

    # Descrição
    if temcupom:
        #cupom
        draw.text((25, 1090), f"cupom: ", font=fonte_cupom, fill="white")
        draw.text((210, 1090), f"{cupom}", font=fonte_cupom2, fill="white")

        # Descrição
        linhas = textwrap.wrap(descricao, width=28)  
        y = 1140
        for linha in linhas:
            #bbox = draw.textbbox((0, 0), linha, font=fonte_texto)
            #largura_linha = bbox[2] - bbox[0]
            draw.text((25, y), linha, font=fonte_texto, fill="white")
            y += 45
    else:
        # Descrição
        linhas = textwrap.wrap(descricao, width=28)  
        y = 1100
        for linha in linhas:
            #bbox = draw.textbbox((0, 0), linha, font=fonte_texto)
            #largura_linha = bbox[2] - bbox[0]
            draw.text((25, y), linha, font=fonte_texto, fill="white")
            y += 50


    # Salvar imagem final
    nome_arquivo = f"card_{nome.replace(' ', '_')}.png"
    card.convert("RGB").save("D:\Capitão promo\Automação promo\cards criados\\" + nome_arquivo)
    print(f"Card salvo como: {nome_arquivo}")

# Exemplo de uso:
gerar_card(
    nome="Camisa",
    descricao="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed aliquam nibh varius ",
    preco="165,19",
    frete_gratis=True,
    temcupom=True,
    cupom="CAPITAO10",
    imagem_produto_path="D:\Photoshop\Camiseta hackers 2 costas.png",   # local ou link
    imagem_moldura_path="D:\Capitão promo\Automação promo\Modelos\moldura post instagram capitão promo.png",
    imagem_moldura_frete_path="D:\Capitão promo\Automação promo\Modelos\moldura post instagram capitão promo frete gratis.png" 
)
