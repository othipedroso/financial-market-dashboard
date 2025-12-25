# 📈 Investidor Pro V2 - Dashboard Financeiro

Uma ferramenta interativa de análise de dados financeiros desenvolvida em Python. Este dashboard permite visualizar cotações de ações, criptomoedas e commodities em tempo real, utilizando gráficos profissionais de mercado (Candlestick).

![Preview do Dashboard](screenshot.png)
*(Se você tiver tirado o print, a imagem aparecerá aqui. Caso contrário, pode remover esta linha)*

## 🚀 Funcionalidades

- **Monitoramento em Tempo Real:** Dados atualizados via API do Yahoo Finance.
- **Gráficos Interativos (Plotly):** Gráficos de velas (Candlestick) com zoom, seleção de período e tooltip.
- **Indicadores Técnicos:** Opção para ativar/desativar Média Móvel de 20 períodos.
- **Dados Fundamentais:** Exibição de variação percentual, setor e máximas/mínimas do período.
- **Exportação de Dados:** Botão para baixar o histórico completo em formato `.csv` (Excel).
- **Performance:** Sistema de cache para carregamento rápido das consultas.

## 🛠️ Tecnologias Utilizadas

- **Python 3.12+**
- **Streamlit:** Framework para criação da interface web.
- **Yfinance:** Coleta de dados financeiros.
- **Plotly:** Biblioteca gráfica para visualizações interativas.
- **Pandas:** Manipulação e tratamento das tabelas de dados.
