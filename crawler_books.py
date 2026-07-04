"""
Crawler para o site https://books.toscrape.com/

O script:
1. Acessa a página inicial e descobre todas as categorias de livros.
2. Para cada categoria, percorre todas as páginas (paginação) e coleta:
   - nome do livro
   - preço do livro
   - quantidade de estrelas (avaliação)
3. Monta um DataFrame do pandas com todos os dados coletados.
4. Gera um boxplot (seaborn) mostrando a distribuição de preços por categoria.
5. Gera um gráfico de radar mostrando a quantidade de livros por categoria.
"""

import time
import re

import numpy as np
import requests
from bs4 import BeautifulSoup
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

#%%

# URL base do site
URL_BASE = "https://books.toscrape.com/"

# Mapeamento das palavras usadas nas classes CSS para números de estrelas
MAPA_ESTRELAS = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5,
}


def obter_soup(url):
    """Faz a requisição HTTP para a URL informada e retorna um objeto BeautifulSoup."""
    resposta = requests.get(url, timeout=10)
    resposta.raise_for_status()
    return BeautifulSoup(resposta.text, "html.parser")


def obter_categorias():
    """
    Acessa a página inicial do site e retorna uma lista de dicionários
    contendo o nome da categoria e a URL completa dela.
    """
    soup = obter_soup(URL_BASE)

    # As categorias ficam dentro do menu lateral (div.side_categories)
    lista_links = soup.select("div.side_categories ul li ul li a")

    categorias = []
    for link in lista_links:
        nome_categoria = link.get_text(strip=True)
        url_categoria = URL_BASE + link["href"]
        categorias.append({"nome": nome_categoria, "url": url_categoria})

    return categorias


def extrair_estrelas(tag_livro):
    """Extrai a quantidade de estrelas (1 a 5) a partir da classe CSS do elemento p.star-rating."""
    tag_estrela = tag_livro.find("p", class_="star-rating")
    if tag_estrela is None:
        return None

    # A classe vem no formato "star-rating Three", por exemplo
    classes = tag_estrela.get("class", [])
    for classe in classes:
        if classe in MAPA_ESTRELAS:
            return MAPA_ESTRELAS[classe]
    return None


def extrair_preco(tag_livro):
    """Extrai o preço do livro e converte para float (removendo símbolo de moeda)."""
    texto_preco = tag_livro.find("p", class_="price_color").get_text(strip=True)
    # Remove qualquer caractere que não seja dígito ou ponto decimal
    valor_numerico = re.sub(r"[^\d.]", "", texto_preco)
    return float(valor_numerico)


def extrair_nome(tag_livro):
    """Extrai o nome (título) do livro."""
    tag_titulo = tag_livro.find("h3").find("a")
    # O atributo 'title' contém o nome completo do livro (sem truncamento)
    return tag_titulo["title"]


def coletar_livros_categoria(url_categoria):
    """
    Percorre todas as páginas de uma categoria (seguindo a paginação) e
    retorna uma lista de dicionários com nome, preço e estrelas de cada livro.
    """
    livros = []
    url_pagina = url_categoria

    while True:
        soup = obter_soup(url_pagina)

        artigos = soup.select("article.product_pod")
        for artigo in artigos:
            livros.append({
                "nome": extrair_nome(artigo),
                "preco": extrair_preco(artigo),
                "estrelas": extrair_estrelas(artigo),
            })

        # Verifica se existe um link para a próxima página
        tag_proxima = soup.select_one("li.next a")
        if tag_proxima is None:
            break

        # Monta a URL da próxima página com base na URL atual da categoria
        url_pagina = url_pagina.rsplit("/", 1)[0] + "/" + tag_proxima["href"]

        # Pequena pausa entre requisições para não sobrecarregar o servidor
        time.sleep(0.2)

    return livros


def montar_dataframe():
    """Percorre todas as categorias e monta o DataFrame final com todos os livros."""
    categorias = obter_categorias()
    print(f"Foram encontradas {len(categorias)} categorias.")

    todos_os_livros = []

    for categoria in categorias:
        print(f"Coletando livros da categoria: {categoria['nome']}...")
        livros_da_categoria = coletar_livros_categoria(categoria["url"])

        for livro in livros_da_categoria:
            livro["categoria"] = categoria["nome"]
            todos_os_livros.append(livro)

    df = pd.DataFrame(todos_os_livros)
    return df


def gerar_boxplot(df):
    """Gera um boxplot único mostrando a distribuição de preços por categoria."""
    plt.figure(figsize=(16, 8))

    # Ordena as categorias pela mediana de preço, apenas para melhor visualização
    ordem_categorias = (
        df.groupby("categoria")["preco"].median().sort_values().index
    )

    sns.boxplot(data=df, x="categoria", y="preco", order=ordem_categorias)

    plt.xticks(rotation=90)
    plt.xlabel("Categoria")
    plt.ylabel("Preço (£)")
    plt.title("Distribuição de preços dos livros por categoria")
    plt.tight_layout()

    caminho_saida = "boxplot_precos_por_categoria.png"
    plt.savefig(caminho_saida, dpi=150)
    print(f"Boxplot salvo em: {caminho_saida}")
    plt.show()


def gerar_radar(df, top_n=10):
    """Gera um gráfico de radar com a quantidade de livros das top_n categorias com mais livros."""

    # Conta quantos livros existem em cada categoria e mantém apenas as top_n maiores
    contagem_por_categoria = df["categoria"].value_counts().head(top_n)

    # Ordena por nome da categoria apenas para deixar o gráfico mais organizado visualmente
    contagem_por_categoria = contagem_por_categoria.sort_index()

    categorias = contagem_por_categoria.index.tolist()
    valores = contagem_por_categoria.values.tolist()

    numero_eixos = len(categorias)

    # Calcula o ângulo de cada eixo do radar (distribuídos igualmente em um círculo)
    angulos = np.linspace(0, 2 * np.pi, numero_eixos, endpoint=False).tolist()

    # Fecha o polígono repetindo o primeiro valor/ângulo no final
    valores += valores[:1]
    angulos += angulos[:1]

    fig, eixo = plt.subplots(figsize=(9, 9), subplot_kw={"projection": "polar"})

    # Desenha a linha e preenche a área do radar
    eixo.plot(angulos, valores, linewidth=2, linestyle="solid")
    eixo.fill(angulos, valores, alpha=0.25)

    # Define um rótulo para cada eixo (uma categoria por eixo)
    eixo.set_xticks(angulos[:-1])
    eixo.set_xticklabels(categorias, fontsize=10)

    # Coloca o primeiro eixo no topo do gráfico e segue no sentido horário
    eixo.set_theta_offset(np.pi / 2)
    eixo.set_theta_direction(-1)

    eixo.set_title(f"Top {top_n} categorias com mais livros", fontsize=14, pad=30)

    plt.tight_layout()

    caminho_saida = "radar_livros_por_categoria.png"
    plt.savefig(caminho_saida, dpi=150)
    print(f"Radar salvo em: {caminho_saida}")
    plt.show()


if __name__ == "__main__":
    # Monta o DataFrame com todos os livros de todas as categorias
    dataframe_livros = montar_dataframe()

    # Salva os dados coletados em um arquivo CSV para consulta posterior
    dataframe_livros.to_csv("livros_coletados.csv", index=False, encoding="utf-8-sig")
    print("Dados salvos em: livros_coletados.csv")

    # Exibe um resumo rápido dos dados coletados
    print(dataframe_livros.head())
    print(f"\nTotal de livros coletados: {len(dataframe_livros)}")

    # Gera o gráfico boxplot com a distribuição de preços por categoria
    gerar_boxplot(dataframe_livros)

    # Gera o gráfico de radar com a quantidade de livros por categoria
    gerar_radar(dataframe_livros)
