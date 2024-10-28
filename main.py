from prophet import Prophet
import pandas as pd
import os

file_path = 'C:\\Users\\scoou\\OneDrive\\Área de Trabalho\\gas-prices.tsv'
dados = pd.read_csv(file_path, sep='\t')

dados['MARGEM MEDIA REVENDA'] = pd.to_numeric(dados['MARGEM MÉDIA REVENDA'], errors='coerce')
dados['PRECO MEDIO DISTRIBUICAO'] = pd.to_numeric(dados['PREÇO MÉDIO DISTRIBUIÇÃO'], errors='coerce')
dados['DESVIO PADRAO DISTRIBUICAO'] = pd.to_numeric(dados['DESVIO PADRÃO DISTRIBUIÇÃO'], errors='coerce')
dados['PRECO MINIMO DISTRIBUICAO'] = pd.to_numeric(dados['PREÇO MÍNIMO DISTRIBUIÇÃO'], errors='coerce')
dados['PRECO MAXIMO DISTRIBUICAO'] = pd.to_numeric(dados['PREÇO MÁXIMO DISTRIBUIÇÃO'], errors='coerce')
dados['COEF VARIACAO DISTRIBUICAO'] = pd.to_numeric(dados['COEF DE VARIAÇÃO DISTRIBUIÇÃO'], errors='coerce')

dados_limpos = dados.dropna(subset=['MARGEM MEDIA REVENDA', 'PRECO MEDIO DISTRIBUICAO', 
                                    'DESVIO PADRAO DISTRIBUICAO', 'PRECO MINIMO DISTRIBUICAO', 
                                    'PRECO MAXIMO DISTRIBUICAO', 'COEF VARIACAO DISTRIBUICAO']).copy()

dados_limpos['PRODUTO'] = dados_limpos['PRODUTO'].str.upper().replace({
    'OLEO DIESEL': 'ÓLEO DIESEL',
    'OLEO DIESEL S10': 'ÓLEO DIESEL S10',
    'GLP': 'GÁS DE COZINHA (GLP)'
})
dados_limpos['DATA INICIAL'] = pd.to_datetime(dados_limpos['DATA INICIAL'], errors='coerce')
dados_limpos = dados_limpos[dados_limpos['DATA INICIAL'] >= '2019-01-01']

dados_agregados = dados_limpos.groupby(['DATA INICIAL', 'PRODUTO'])['PREÇO MÉDIO REVENDA'].mean().reset_index()

df_resultado = pd.DataFrame(columns=['DATA', 'COMBUSTIVEL', 'TIPO', 'PRECO_MEDIO_REVENDA'])

def gerar_previsoes_para_todos_combustiveis():
    combustiveis = dados_agregados['PRODUTO'].unique()
    
    for combustivel in combustiveis:
        dados_historicos = dados_agregados[dados_agregados['PRODUTO'] == combustivel]
        dados_historicos = dados_historicos.rename(columns={'DATA INICIAL': 'DATA', 'PREÇO MÉDIO REVENDA': 'PRECO_MEDIO_REVENDA'})
        dados_historicos['COMBUSTIVEL'] = combustivel
        dados_historicos['TIPO'] = 'Histórico'
        
        dados_historicos['PRECO_MEDIO_REVENDA'] = dados_historicos['PRECO_MEDIO_REVENDA'].round(2)

        global df_resultado
        df_resultado = pd.concat([df_resultado, dados_historicos[['DATA', 'COMBUSTIVEL', 'TIPO', 'PRECO_MEDIO_REVENDA']]])

        df_prophet = dados_historicos[['DATA', 'PRECO_MEDIO_REVENDA']].rename(columns={'DATA': 'ds', 'PRECO_MEDIO_REVENDA': 'y'})
        df_prophet['cap'] = df_prophet['y'].max() * 1.2
        
        modelo_prophet = Prophet(yearly_seasonality=True, weekly_seasonality=False, daily_seasonality=False, 
                                 changepoint_prior_scale=0.8, growth='logistic')
        modelo_prophet.fit(df_prophet)
        
        future_dates = modelo_prophet.make_future_dataframe(periods=40, freq='ME')
        future_dates['cap'] = df_prophet['cap'].iloc[0]
        
        forecast = modelo_prophet.predict(future_dates)
        
        previsao = forecast[['ds', 'yhat']].rename(columns={'ds': 'DATA', 'yhat': 'PRECO_MEDIO_REVENDA'})
        previsao['COMBUSTIVEL'] = combustivel
        previsao['TIPO'] = 'Previsão'
        
        previsao['PRECO_MEDIO_REVENDA'] = previsao['PRECO_MEDIO_REVENDA'].round(2)

        df_resultado = pd.concat([df_resultado, previsao[['DATA', 'COMBUSTIVEL', 'TIPO', 'PRECO_MEDIO_REVENDA']]])

gerar_previsoes_para_todos_combustiveis()

df_resultado['PRECO_MEDIO_REVENDA'] = df_resultado['PRECO_MEDIO_REVENDA'].apply(lambda x: f'{x:,.2f}'.replace(',', '.'))
df_resultado.to_csv('previsoes_combustiveis_completas.csv', index=False, sep=';')
print("Arquivo 'previsoes_combustiveis_completas.csv' gerado com sucesso!")