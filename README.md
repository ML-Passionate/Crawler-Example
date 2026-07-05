# 004-Crawler Example
Exercicio de crawler para ler livros e gerar box-blot e radar.

Crawler para o site https://books.toscrape.com/

![Books](Books.png)

O script:
1. Acessa a página inicial e descobre todas as categorias de livros.
2. Para cada categoria, percorre todas as páginas (paginação) e coleta:
   - nome do livro
   - preço do livro
   - quantidade de estrelas (avaliação)
3. Monta um DataFrame do pandas com todos os dados coletados e grava um csv (por segurança)
4. Gera um boxplot (seaborn) mostrando a distribuição de preços por categoria, em ordem crescente de preço médio
5. Gera um gráfico de radar mostrando a quantidade de livros por categoria, para as 10 categorias mais importantes
6. Gera um gráfico da distribuição de preços por estrelas
7. Faz a correlação de pearson entra preço e estrelas e gera um heatmap

![BeautifulSoup](https://img.shields.io/badge/BeautifulSoup-green?style=for-the-badge&logo=python&logoColor=white)
![Requests](https://img.shields.io/badge/Requests-0052CC?style=for-the-badge&logo=git&logoColor=white)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-%23ffffff.svg?style=for-the-badge&logo=Matplotlib&logoColor=black)
![Seaborn](https://img.shields.io/badge/Seaborn-4C72B0?style=for-the-badge&logo=python&logoColor=white)

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Status](https://img.shields.io/badge/status-finalizado-brightgreen?style=for-the-badge)
![Release](https://img.shields.io/badge/release-v2.0-blue?style=for-the-badge)

# Resultado - gráficos

![BoxPlot](boxplot_precos_por_categoria.png)

![Radar](radar_livros_por_categoria.png)

![Radar](scatter_preco_estrelas.png)

![Radar](heatmap_correlacao_preco_estrelas.png)
