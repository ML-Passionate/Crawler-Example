# 004-Crawler Example
Exercicio de crawler para ler livros e gerar box-blot e radar.

Crawler para o site https://books.toscrape.com/

O script:
1. Acessa a página inicial e descobre todas as categorias de livros.
2. Para cada categoria, percorre todas as páginas (paginação) e coleta:
   - nome do livro
   - preço do livro
   - quantidade de estrelas (avaliação)
3. Monta um DataFrame do pandas com todos os dados coletados.
4. Gera um boxplot (seaborn) mostrando a distribuição de preços por categoria.
5. Gera um gráfico de radar mostrando a quantidade de livros por categoria

# Resultado

![BoxPlot](boxplot_precos_por_categoria.png)

![Radar](radar_livros_por_categoria.png)
