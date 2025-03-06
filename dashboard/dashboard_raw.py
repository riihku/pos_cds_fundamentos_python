import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt


# Configurações Gerais
sns.set_theme()
plt.rcParams['figure.figsize'] = (6, 3) # tamanho da figura
plt.rcParams['axes.titlesize'] = 10     # tamanho do título
plt.rcParams['axes.labelsize'] = 8      # tamanho dos rótulos dos eixos
plt.rcParams['xtick.labelsize'] = 7     # tamanhos dos ticks eixo x
plt.rcParams['ytick.labelsize'] = 7     # tamanhos dos ticks eixo y
plt.rcParams['legend.fontsize'] = 8     # tamanho da fonte das legendas
plt.rcParams['lines.markersize'] = 4    # tamanho dos marcadores nas linhas

order_items_df = pd.read_csv('../datasets/order_items_cleaned.csv')

st.set_page_config(page_title='Análise de Vendas por Estado', layout='wide')
st.markdown(
    """
    <style>
    .stApp {
        background-color: #000000;
        color: #C84C09;
    }
    .stButton>button {
        background-color: #FF4B4B;
        color: black;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# Título
st.title('Dashboard de Análise de Vendas por Estado')

# Side Bar
st.sidebar.header('Filtros')
lista_estados = list(order_items_df['seller_state'].unique())
estados_selecionados = st.sidebar.multiselect('Selecione um Estado', options=lista_estados,
                                                                   default=lista_estados)

customers_df_filtered = order_items_df[order_items_df['customer_state'].isin(estados_selecionados)]
sellers_df_filtered = order_items_df[order_items_df['seller_state'].isin(estados_selecionados)]

# Big Numbers
st.subheader('Indicadores Gerais')

total_vendas = customers_df_filtered['total_price'].sum()
total_customers = customers_df_filtered['customer_unique_id'].nunique()
total_sellers = sellers_df_filtered['seller_id'].nunique()

# Criar 3 colunas
col1, col2, col3 = st.columns(3) # posso botar uma lista [] com as proporções : [1, 2, 1]

col1.metric('Vendas Totais', f"R${total_vendas:,.2f}")
col2.metric('Clientes Únicos', f"{total_customers:,.0f}")
col3.metric('Vendedores Únicos', f"{total_sellers:,.0f}")

# Visões Gerais
st.subheader('Visao Geral das Vendas por Estado')

col1, col2, col3 = st.columns(3)

# Grafico 1
vendas_estados = customers_df_filtered[['customer_state', 'total_price']].groupby('customer_state').sum().reset_index()

fig1, ax1 = plt.subplots()
sns.barplot(data=vendas_estados, x= 'customer_state', y= 'total_price', ax=ax1)
ax1.set_title('Vendas Totais por Estado')
plt.xlabel('Estado')
plt.ylabel('Vendas (R$)')
col1.pyplot(fig1)

# Grafico 2
clientes_estado = customers_df_filtered[['customer_state', 'customer_unique_id']].groupby('customer_state').nunique().reset_index()

fig2, ax2 = plt.subplots()
sns.barplot( data=clientes_estado, x='customer_state', y='customer_unique_id', ax=ax2)
ax2.set_title('Clientes Únicos por Estado')
plt.xlabel('Estado')
plt.ylabel('Vendas (R$)')
col2.pyplot(fig2)

# Grafico 3
vendedores_estado = sellers_df_filtered[['seller_state', 'seller_id']].groupby('seller_state').nunique().reset_index()
fig3, ax3 = plt.subplots()
sns.barplot( data=vendedores_estado, x='seller_state', y='seller_id', ax=ax3)
ax3.set_title('Vendedores Únicos por Estado')
plt.xlabel('Estado')
plt.ylabel('Vendas (R$)')
col3.pyplot(fig3)

# Visoes Temporais (mês) para o Estado Selecionado
st.subheader('Visão Temporal por Estado')

col1, col2, col3 = st.columns(3)

vendas_temporal = customers_df_filtered[['order_purchase_year_month', 'total_price']].groupby('order_purchase_year_month').sum().reset_index()

fig1, ax1 = plt.subplots()
sns.lineplot(data=vendas_temporal, x='order_purchase_year_month', y='total_price', ax=ax1)
ax1.set_title(f'Vendas (R$) por mês')
plt.xlabel('Ano-mês')
plt.ylabel('Vendas (R$)')
plt.xticks(rotation=60)
col1.pyplot(fig1)

clientes_temporal = customers_df_filtered[['order_purchase_year_month', 'customer_unique_id']].groupby('order_purchase_year_month').nunique().reset_index()
fig2, ax2 = plt.subplots()
sns.lineplot(data=clientes_temporal, x='order_purchase_year_month', y='customer_unique_id', ax=ax2)
ax2.set_title(f'Clientes Únicos por mês')
plt.xlabel('Ano-mês')
plt.ylabel('Clientes Únicos')
plt.xticks(rotation=60)
col2.pyplot(fig2)

vendedores_temporal = sellers_df_filtered[['order_purchase_year_month', 'seller_id']].groupby('order_purchase_year_month').nunique().reset_index()
fig3, ax3 = plt.subplots()
sns.lineplot(data=vendedores_temporal, x='order_purchase_year_month', y='seller_id', ax=ax3)
ax3.set_title(f'Vendedores Únicos por mês')
plt.xlabel('Ano-mês')
plt.ylabel('Vendedores Únicos')
plt.xticks(rotation=60)
col3.pyplot(fig3)




