import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import date, timedelta

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Investidor Pro V2", layout="wide")

# --- BARRA LATERAL (CONTROLES) ---
st.sidebar.header("🔧 Configurações")

# Lista expandida com Commodities e Indices
opcoes = ["PETR4.SA", "VALE3.SA", "ITUB4.SA", "BBAS3.SA", "WEGE3.SA", 
          "BTC-USD", "ETH-USD", "USDBRL=X", "EURBRL=X", "GC=F"] # GC=F é Ouro

ticker = st.sidebar.selectbox("Selecione o Ativo:", opcoes, index=0)

# Seleção de Datas Personalizada
data_inicio = st.sidebar.date_input("Data de Início", date.today() - timedelta(days=365))
data_fim = st.sidebar.date_input("Data Final", date.today())

# Opções de Análise Técnica
st.sidebar.subheader("Análise Técnica")
mostrar_media = st.sidebar.checkbox("Média Móvel (20 dias)", value=True)

# --- CARREGAMENTO DE DADOS ---
@st.cache_data # Isso faz o site ficar rápido (salva o cache)
def carregar_dados(simbolo, inicio, fim):
    dados = yf.Ticker(simbolo)
    historico = dados.history(start=inicio, end=fim)
    return dados.info, historico

with st.spinner('Baixando dados do mercado...'):
    info, df = carregar_dados(ticker, data_inicio, data_fim)

# --- DASHBOARD PRINCIPAL ---
st.title(f"📈 Análise: {ticker}")

# Se não tiver dados, para por aqui
if df.empty:
    st.error("Não há dados para o período selecionado.")
    st.stop()

# 1. LINHA DE DESTAQUES (Cards)
try:
    preco_atual = df['Close'].iloc[-1]
    variacao = df['Close'].iloc[-1] - df['Close'].iloc[-2]
    var_pct = (variacao / df['Close'].iloc[-2]) * 100
    
    # Tenta pegar dados extras (pode falhar em moedas, por isso o try)
    setor = info.get('sector', 'N/A')
    mercado = info.get('marketCap', 0) / 1e9 # Bilhões
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Preço Atual", f"R$ {preco_atual:.2f}", f"{var_pct:.2f}%")
    col2.metric("Alta (Período)", f"R$ {df['High'].max():.2f}")
    col3.metric("Baixa (Período)", f"R$ {df['Low'].min():.2f}")
    col4.metric("Setor", setor)
except:
    st.warning("Alguns dados fundamentais não estão disponíveis para este ativo.")

# 2. GRÁFICO INTERATIVO (CANDLESTICK)
st.subheader("Gráfico de Preços")

fig = go.Figure()

# Adiciona as velas (Candles)
fig.add_trace(go.Candlestick(
    x=df.index,
    open=df['Open'], high=df['High'],
    low=df['Low'], close=df['Close'],
    name="Preço"
))

# Adiciona Média Móvel se o usuário pediu
if mostrar_media:
    df['SMA20'] = df['Close'].rolling(window=20).mean()
    fig.add_trace(go.Scatter(
        x=df.index, y=df['SMA20'], 
        mode='lines', name='Média 20 dias',
        line=dict(color='orange', width=2)
    ))

# Layout do gráfico
fig.update_layout(
    xaxis_rangeslider_visible=False,
    template="plotly_dark", # Fica com visual 'dark mode' profissional
    height=500
)

st.plotly_chart(fig, use_container_width=True)

# 3. DADOS BRUTOS (Expander)
with st.expander("📥 Ver Tabela de Dados (Clique para abrir)"):
    st.dataframe(df.sort_index(ascending=False))
    
    # Botão de download
    csv = df.to_csv().encode('utf-8')
    st.download_button(
        label="Baixar dados em CSV",
        data=csv,
        file_name=f'{ticker}_dados.csv',
        mime='text/csv',
    )