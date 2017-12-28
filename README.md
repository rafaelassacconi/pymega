# PyMega

Análise de resultados anteriores da Mega-Sena e gerador de números.

---

## Dicas para aumentar as chances de ganhar

1. Os números com final 9 ou 0 saem pouco, evite escolher números com essa sequencia.
2. As dezenas 01, 02, 03, 11, 22, 44, 55, 48 e 57 saem pouco.
3. Não jogue números seguidos.
4. Não jogue em números que estejam na mesma linha vertical.
5. Divida a cartela em quatro quadrantes e distribua seu jogo entre eles.
6. Jogue a mesma quantidade de números pares e ímpares. Na Mega-Sena, 81% dos sorteios têm o seguinte esquema: 3 números pares e 3 ímpares ou 4 pares e 2 ímpares, ou vice-versa.
7. Prefira apenas um cartão com mais de seis dezenas do que vários de seis dezenas. Quanto mais números você apostar em um mesmo jogo, maiores são as chances ganhar.
8. Um jogo em que se preenche 12 dezenas utilizando essas regras teria mais chances de êxito. Logo, o bolão é a melhor chance que se tem de ganhar.

Fonte: [8 dicas para ganhar na loteria](http://www.infomoney.com.br/minhas-financas/planeje-suas-financas/noticia/3796300/dicas-para-ganhar-loteria-sem-precisar-sorte)

---

## Como usar o script

1. Crie um virtualenv e instale as dependências **pip install -r requirements.txt**.
2. Para visualizar as estatísticas execute **python estatisticas.py**
3. Para gerar um número excute **python gerar_numero.py 10** passando a quantidade de números

Os dados da pasta **data** com histório de números sorteados anteriormente foram baixados do [site oficial da Mega-Sena](http://loterias.caixa.gov.br/wps/portal/loterias/landing/megasena/).