# -*- coding: utf-8 -*-
"""aula0_ds_alura.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1LMPxbo_6up9mXuPRPV8AyQ9Am22ReClo

# Importando bibliotecas
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Por padrão, o Colab importa a versão 0.7.1 do Seaborn, sendo necessário solicitar a instalação da versão mais recente para utilizar alguns recursos. 
# Caso seja importado antes de rodar este comando, é necessário resetar o Runtime para apagar a antiga importação e ele instalar a versão mais recente do Seaborn.

!pip install seaborn==0.9.0
import seaborn as sns

print(sns.__version__)

"""# Importando dados"""

notas = pd.read_csv('ratings.csv')

filmes = pd.read_csv('movies.csv')

tmdb = pd.read_csv("tmdb_5000_movies.csv")

"""# Analisando notas no geral"""

notas.head()

notas.shape

notas.columns = ['usuarioId', 'filmeId', 'nota', 'momento']

notas.head()

notas['nota'].unique()

notas['nota'].value_counts()

print("Média", notas['nota'].mean())
print("Mediana", notas['nota'].median())

notas.nota.head()

#forma de ler a coluna sem usar []

notas.nota.plot()

notas.nota.plot(kind='hist')

#o describe() nos trás um calculo das principais medidas dos dados

notas.nota.describe()

sns.boxplot(notas.nota)

filmes.head()

"""# Olhando os Filmes"""

filmes.columns = ['filmeId', 'titulo', 'genero']

"""# Analisando algumas notas especificas por filme"""

notas.query('filmeId==1').nota.mean()

notas.query('filmeId==2').nota.mean()

media_por_filme = notas.groupby('filmeId').mean().nota
media_por_filme.head()

media_por_filme.plot(kind='hist')

#podemos usar pyplot junto de outras bibliotecas para configurar os graficos

import matplotlib.pyplot as plt

plt.figure(figsize=(5,8))
sns.boxplot(y=media_por_filme)

sns.distplot(media_por_filme, bins=10)

#por debaixo dos panos, o seaborn e o pandas usam o plt

import matplotlib.pyplot as plt

plt.hist(media_por_filme)
plt.title("Histograma da média dos filmes")



"""# TMDB 5000 filmes"""

tmdb.head()

tmdb['vote_average'].unique()

#Por padrão, ao tentarmos comparar categorias, a maneira mais comum é descobrir quantas vezes cada uma delas aparece. 
#Normalmente, ao utilizarmos funções no Pandas, ele nos retorna uma série (que aparenta ser colunas mas, na realidade, sempre a primeira será um índice e a segunda uma série). 
#Para transformarmos isso para um dataframe, usaremos a função to_frame. E para resetar o index e torna-lo uma coluna usamos o comando reset_index, que criará um novo (contador) a parte

tmdb.original_language.value_counts().to_frame().reset_index()

contagem_de_lingua = tmdb.original_language.value_counts().to_frame().reset_index()
contagem_de_lingua.columns = ["original_language", "total"] #renomeando as colunas
contagem_de_lingua.head()

sns.barplot(x="original_language", y="total", data = contagem_de_lingua)

#No seaborn existe plotagens de baixo nivel (exemplo anterior, que temos que tratar os dados isoladamente e depois plotar os dados) e as de alto nível, que podemos usar a fonte
#de dados original e configurar para que o Plot exiba da forma que gostaríamos

#No seaborn existem os 'kind', conhecidos como 'tipos', que são as formas de agregar as informações. 

#No exemplo abaixo, usamos um recurso de alto nível do Seaborn, utilizando a base original da informação, usando a variável original_language como nosso eixo x e o y realizando a contagem de 
#aparições direto na função.

#Este tipo de gráfico realiza a ordenação das informações de forma automática, deixando um pouco confuso a visualização

sns.catplot(x="original_language", kind="count", data=tmdb)

#Por mais que não utilizemos tanto o gráfico de pizza (pie chart) por ser de difícil compreensão, caso precisemos utilizar, o Seaborn não possui esse tipo de visualização, mas o Matplotlib
#sim, através da função plt.pie()

plt.pie(contagem_de_lingua["total"], labels = contagem_de_lingua["original_language"])

#Anteriormente percebemos que ambos os nossos gráficos não traziam uma visualização clara da história que gostaríamos de contar. Visto que a lingua inglesa é a de maior volume
#em comparação às outras linguas, podemos isolar estas informações para trazer uma visualização mais limpa. 

#a função loc é o mesmo de "locate", ela permite filtrar uma informação a partir de um parâmetro que passarmos. 

total_por_lingua = tmdb["original_language"].value_counts()
total_por_lingua.loc["en"]

#Como o objetivo aqui é separar o inglês das demais linguas, faremos uma soma do total de todas as linguas e vamos subtrair o valor encontrado apenas para inglês anteriormente

total_por_lingua = tmdb["original_language"].value_counts()
total_geral = total_por_lingua.sum()
total_de_ingles = total_por_lingua.loc["en"]
total_do_resto = total_geral - total_de_ingles
print(total_de_ingles, total_do_resto)

#Agora, criaremos um dataframe a partir dessas informações para conseguirmor plotar em um gráfico. Criaremos a variável dados, que conterá um dicionário do python e representará duas colunas
#sendo: lingua, contendo ingles e outros; e total, contendo a quantidade de filmes em ingles e outros

dados = {
    'lingua' : ['ingles','outros'],
    'total' : [total_de_ingles, total_do_resto]

}

pd.DataFrame(dados)

#Podemos sobreescrever a variável e deixa-la apenas como dataframe 

dados = {
    'lingua' : ['ingles','outros'],
    'total' : [total_de_ingles, total_do_resto]

}

dados = pd.DataFrame(dados)
dados

#Agora podemos plotar as informações a partir do dataframe

sns.barplot(data = dados, x = 'lingua', y = 'total')

#Podemos filtrar nossos dados usando a função query(), que neste novo caso, focaremos apenas nos dados de filmes que não tenham a lingua original em inglês

total_por_lingua_de_outros_filmes = tmdb.query("original_language != 'en'").original_language.value_counts()

filmes_sem_lingua_original_em_ingles = tmdb.query("original_language != 'en'")

sns.catplot(x = "original_language", data = filmes_sem_lingua_original_em_ingles, kind="count")

#O catplot do seaborn é uma função de plotagem de alto nível, ou seja, por conta disso não é possível usar configurações de baixo nível como o figsize utilizado anteriormente em outro exemplo
#(boxplot) para configurar o tamanho da visualização. 
#Para isso, o catplot entrega vários parâmetros e configurações nativas em sua função que podemos consultar na documentação. Com elas é possível trazer uma visualização de dados muito mais 
#conveniente.

sns.catplot(x = "original_language", data = filmes_sem_lingua_original_em_ingles, kind="count", aspect=2) #o parâmetro aspect permitiu que a plotagem mudasse de quadrado para retângulo

#Podemos perceber que no exemplo anterior, a ordenação das informações estão confusas, deixando a visualização longe do ideal. Para corrigirmos isso, usamos a função order() do catplot.

#Aqui temos um truque. Se olharmos para nossa serie anterior que geramos a partir da query dos filmes com lingua original diferente de inglês, percebemos que automaticamente o pandas 
#ordenou esses dados pelas suas grandezas. Sendo assim, é possível utilizar a variável que guardamos essa consulta como parâmetro dentro de order, sem que manualmente precisemos especificar
#a ordem das informações

sns.catplot(x = "original_language", data = filmes_sem_lingua_original_em_ingles, 
            kind="count", 
            aspect=2,
            order = total_por_lingua_de_outros_filmes.index)

#Podemos ajustar a paleta de cores do catplot através da função "palette". Na documentação podemos encontrar inúmeras sugestões e como selecionar a cor correta.

sns.catplot(x = "original_language", data = filmes_sem_lingua_original_em_ingles, 
            kind="count", 
            aspect=2,
            palette="GnBu_d",
            order = total_por_lingua_de_outros_filmes.index)

#Exemplo de outros tipos de gráficos que existem no Seaborn

import seaborn as sns
sns.set(style="ticks")

# Load the example dataset for Anscombe's quartet
df = sns.load_dataset("anscombe")

# Show the results of a linear regression within each dataset
sns.lmplot(x="x", y="y", col="dataset", hue="dataset", data=df,
           col_wrap=2, ci=None, palette="muted", height=4,
           scatter_kws={"s": 50, "alpha": 1})

"""# Analisando movies.csv"""

filmes.head(2)

#Passamos uma query em notas para trazermos as notas do filme com Id 1 (Toy Story) e 2 (Jumanji)

notas_do_toy_story = notas.query("filmeId==1")
notas_do_jumanji = notas.query("filmeId==2")
print(len(notas_do_toy_story), len(notas_do_jumanji))

#Trazer a nota média dos filmes. Lembrando que quando usamos cálculos de média, mediana e moda, estamos resumindo todo nosso dataset em um único
#número central, "jogando fora" características únicas desses dados. Assim poderíamos não saber qual a tendência de um tipo, ou valor de nota, que
#mais prevalece nesse conjunto de dados.

print("Nota média do Toy Story %.2f" % notas_do_toy_story.nota.mean())
print("Nota média do Jumanji %.2f" % notas_do_jumanji.nota.mean())

#Podemos perceber que mesmo com o valor da mediana se alterando bem pouco, não conseguimos ainda entender quantas pessoas amaram ou odiaram o filme.
#Ou seja, não conseguimos entender quantas pessoas realmente deram nota 5 ou quantas deram 0.5. Perdemos muitas informações ao reduzir os valores
#em um "comportamento central".

print("Mediana do Toy Story %.2f" % notas_do_toy_story.nota.median())
print("Mediana do Jumanji %.2f" % notas_do_jumanji.nota.median())

#Utilizaremos uma situação hipotética para ilustrar a situação, em que teremos 10 notas de valor maior e 10 menor. Usaremos o 
#numpy como biblioteca principal pois ele permite trabalhar de forma melhor com os arrays, inclusive realizar cálculos diretos dentro dos valores
#do array


np.array([2.5] * 10) #método array que criar uma lista de valores que especificarmos, o *10 diz que queremos 10 vezes o valor que passarmos
np.array([2.5] * 10).mean() #exemplo calculando a media dos valores contidos no array

#Criamos um novo array com notas maiores e usamos a função append para juntar os dois conjuntos de array em um só pela variável "filme1" e "filme2"

filme1 = np.append(np.array([2.5] * 10), np.array([3.5] * 10))

filme2 = np.append(np.array([5] * 10), np.array([1] * 10))

#Veja que quando imprimos a média de ambos os filmes o resultado é 3! Mas sabemos que em nosso conjunto de dados existe notas 5 e 1, por exemplo,
#fazendo com que o resultado do cálculo não condiza muito com a realidade.

print(filme1.mean(), filme2.mean())

#A mediana para os dois filmes tbm serão iguais

print(np.median(filme1), np.median(filme2))

plt.hist(filme1)
plt.hist(filme2)

#Podemos explorar nossos dados por meio de visões. O histograma anterior pode não ser o melhor, assim como o boxplot abaixo, mas o boxplot pelo menos
#nos entrega uma visão de dispersão dos dados dentro do intervalo de notas;

plt.boxplot([filme1,filme2])

#utilizando a fonte dos filmes toy story e jumanji

plt.boxplot([notas_do_toy_story.nota, notas_do_jumanji.nota])

#Aqui estamos o seaborn para plotar um boxplot e utilizando a fonte de dados primária sem tratamento. Como parametro, filtramos apenas dois ids
#para que o gráfico não fique poluído

sns.boxplot(x = "filmeId", y = "nota", data = notas.query("filmeId in (1,2)"))

sns.boxplot(x = "filmeId", y = "nota", data = notas.query("filmeId in (1,2,3,4,5)"))

#Uma forma de analisarmos, de uma maneira numérica, o quanto nossos dados estão distantes de uma tendência central é por meio do desvio padrão, 
#trazendo um valor que indica o quanto nossos dados estão longe do valor central

print("Desvio padrão do Jumanji %.2f" % notas_do_jumanji.nota.std(), "Desvio padrão do Toy Story %.2f" % notas_do_toy_story.nota.std())

print(np.mean(filme1), np.mean(filme2))
print(np.std(filme1), np.std(filme2))
print(np.median(filme1), np.median(filme2))

#dispersão de dados = É um gráfico que mostra quão dispersa ou condensada uma distribuição está.

plt.boxplot([notas_do_toy_story.nota, notas_do_jumanji.nota])

sns.boxplot(x="filmeId", y="nota", data=notas.query("filmeId in [1,2]"))

