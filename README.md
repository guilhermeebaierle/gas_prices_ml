# 📊 Previsão de Preços de Combustíveis no Brasil

Este projeto utiliza dados históricos de preços de combustíveis para criar um dashboard interativo que permite visualizar tanto o histórico de preços quanto previsões futuras de diferentes tipos de combustíveis no Brasil. O projeto é desenvolvido em Python, utilizando as bibliotecas Pandas e Prophet

# 📌 Descrição do Projeto

Com o aumento das incertezas sobre os preços de combustíveis, este projeto oferece uma ferramenta de análise preditiva para monitorar tendências e realizar previsões dos preços de combustíveis no Brasil, incluindo Etanol, Gasolina, GLP e Diesel. O dataset contém dados desde 2004 até 2021, extraídos da Kaggle.

O dashboard permite alternar entre a visualização do histórico de preços e a previsão de preços futuros, oferecendo uma experiência interativa para análise.

# 🛠 Tecnologias Utilizadas
## 📚 Principais Bibliotecas

- Pandas: Utilizado para carregamento, limpeza, e pré-processamento dos dados.
- Prophet: Biblioteca de modelagem de séries temporais criada pela Meta, usada para realizar previsões de preços com base em padrões sazonais e tendências de longo prazo.

# 📈 Metodologia

- Preparação dos Dados: O dataset é carregado e processado usando o Pandas. As colunas de preços, margens e desvio padrão são convertidas para tipos numéricos, e valores ausentes são tratados.
- Modelagem Preditiva: Para cada tipo de combustível, o modelo Prophet é ajustado com sazonalidade anual e uma curva de crescimento logístico. Este ajuste é essencial para capturar a tendência de longo prazo e sazonais específicas de cada combustível.

# 🔍 Exemplo de Previsão

Com base nos dados históricos, o modelo Prophet projeta preços futuros até julho de 2024. Exemplos de previsões incluem:

- GLP: R$ 106,82 (comparado ao preço atual de R$ 106,50)
- Gasolina Comum: R$ 6,86 (comparado ao preço atual de R$ 6,07)

Essas previsões fornecem insights sobre tendências futuras, mas são influenciadas pela incerteza devido ao horizonte de previsão.

# RESULTADO

![image](https://github.com/user-attachments/assets/2d1034e1-f8ed-41d6-a6e0-2e0865ad6f53)

