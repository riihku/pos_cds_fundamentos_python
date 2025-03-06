import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

from PIL import Image

def definicao_parametros_graficos():
        
    # Configurações Gerais
    sns.set_theme()
    plt.rcParams['figure.figsize'] = (4, 2) # tamanho da figura
    plt.rcParams['axes.titlesize'] = 8     # tamanho do título
    plt.rcParams['axes.labelsize'] = 6      # tamanho dos rótulos dos eixos
    plt.rcParams['xtick.labelsize'] = 6     # tamanhos dos ticks eixo x
    plt.rcParams['ytick.labelsize'] = 6     # tamanhos dos ticks eixo y
    plt.rcParams['legend.fontsize'] = 6     # tamanho da fonte das legendas
    plt.rcParams['lines.markersize'] = 4    # tamanho dos marcadores nas linhas

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

    return None

def aplicar_filtros(df):
    # Side Bar
    img = Image.open('../images/comunidade_ds.jpg')
    st.sidebar.image(img, use_container_width=True)
    st.sidebar.header('Filtros')
    st.sidebar.write("")

    # Converte a coluna 'order_purchase_timestamp' para datetime
    if not pd.api.types.is_datetime64_any_dtype(df['order_purchase_timestamp']):
        df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])

    # Filtro de data com slider de range
    st.sidebar.write("Selecione o intervalo de datas:")
    data_min = df['order_purchase_timestamp'].min().date()  # Data mínima do DataFrame
    data_max = df['order_purchase_timestamp'].max().date()  # Data máxima do DataFrame

    # Slider de range para seleção de datas
    if 'data_range' not in st.session_state:
        st.session_state['data_range'] = (data_min, data_max)

    data_range = st.sidebar.slider(
        "Período",
        min_value=data_min,
        max_value=data_max,
        value=st.session_state['data_range'],
        key="slider_data_range"  # Chave única para o slider
    )
    st.session_state['data_range'] = data_range
    data_inicio, data_fim = data_range  # Extrai as datas de início e fim
    
    st.sidebar.write("")

    # Filtro de estados
    lista_estados = list(df['seller_state'].unique())
    lista_estados.insert(0, "Todos os estados")  # Adiciona a opção "Todos os estados"

    if 'estados_selecionados' not in st.session_state:
        st.session_state['estados_selecionados'] = ["Todos os estados"]

    estados_selecionados = st.sidebar.multiselect(
        'Selecione um Estado',
        options=lista_estados,
        default=st.session_state['estados_selecionados'],
        key="multiselect_estados"  # Chave única para o multiselect
    )

    selecionar_todos_estados = st.sidebar.checkbox(
        "Selecionar todos os estados",
        value=("Todos os estados" in estados_selecionados),
        key="checkbox_estados"  # Chave única para o checkbox
    )


    if selecionar_todos_estados:
        if estados_selecionados != ["Todos os estados"]:
            estados_selecionados = ["Todos os estados"]
            st.session_state['estados_selecionados'] = estados_selecionados
            st.rerun()
    else:
        if "Todos os estados" in estados_selecionados and len(estados_selecionados) > 1:
            estados_selecionados.remove("Todos os estados")
            st.session_state['estados_selecionados'] = estados_selecionados
            st.rerun()

    if "Todos os estados" in estados_selecionados:
        estados_para_filtro = lista_estados[1:]
    else:
        estados_para_filtro = estados_selecionados

    st.sidebar.write("")

    # Filtro de categorias
    lista_categorias = list(df['product_category_name'].unique())
    lista_categorias.insert(0, "Todas as categorias")  # Adiciona a opção "Todas as categorias"

    if 'categorias_selecionadas' not in st.session_state:
        st.session_state['categorias_selecionadas'] = ["Todas as categorias"]

    categorias_selecionadas = st.sidebar.multiselect(
        'Selecione uma categoria de produto',
        options=lista_categorias,
        default=st.session_state['categorias_selecionadas'],
        key="multiselect_categorias"  # Chave única para o multiselect
    )

    selecionar_todas_categorias = st.sidebar.checkbox(
        "Selecionar todas as categorias",
        value=("Todas as categorias" in categorias_selecionadas),
        key="checkbox_categorias"  # Chave única para o checkbox
    )

    st.write("")

    # Filtro de status (Entregue/Cancelado)
    st.sidebar.write("Filtrar por status do pedido:")
    status_entregue = st.sidebar.checkbox("Entregue", value=True, key="checkbox_entregue")
    status_cancelado = st.sidebar.checkbox("Cancelado", value=True, key="checkbox_cancelado")
    # Filtro de status
    status_filtro = []
    if status_entregue:
        status_filtro.append("delivered")
    if status_cancelado:
        status_filtro.append("canceled")

    if status_filtro:  # Se pelo menos um status estiver selecionado
        df = df[df['order_status'].isin(status_filtro)]
    else:
        st.sidebar.warning("Selecione pelo menos um status para filtrar.")


    if selecionar_todas_categorias:
        if categorias_selecionadas != ["Todas as categorias"]:
            categorias_selecionadas = ["Todas as categorias"]
            st.session_state['categorias_selecionadas'] = categorias_selecionadas
            st.rerun()
    else:
        if "Todas as categorias" in categorias_selecionadas and len(categorias_selecionadas) > 1:
            categorias_selecionadas.remove("Todas as categorias")
            st.session_state['categorias_selecionadas'] = categorias_selecionadas
            st.rerun()

    if "Todas as categorias" in categorias_selecionadas:
        categorias_para_filtro = lista_categorias[1:]
    else:
        categorias_para_filtro = categorias_selecionadas

    
    # Aplicando os filtros
    df_filtrado = df[
        (df['order_purchase_timestamp'].dt.date >= data_inicio) & 
        (df['order_purchase_timestamp'].dt.date <= data_fim)
    ]
    customers_df_filtered = df_filtrado[
        (df_filtrado['customer_state'].isin(estados_para_filtro)) & 
        (df_filtrado['product_category_name'].isin(categorias_para_filtro))
    ]
    sellers_df_filtered = df_filtrado[
        (df_filtrado['seller_state'].isin(estados_para_filtro)) & 
        (df_filtrado['product_category_name'].isin(categorias_para_filtro))
    ]

    return customers_df_filtered, sellers_df_filtered

def big_numbers(c_df, s_df):
    st.subheader('Indicadores Gerais')

    total_vendas = c_df['total_price'].sum()
    total_customers = c_df['customer_unique_id'].nunique()
    total_sellers = s_df['seller_id'].nunique()

    # Criar 3 colunas
    col1, col2, col3 = st.columns(3) # posso botar uma lista [] com as proporções : [1, 2, 1]

    col1.metric('Vendas Totais', f"R${total_vendas:,.2f}")
    col2.metric('Clientes Únicos', f"{total_customers:,.0f}")
    col3.metric('Vendedores Únicos', f"{total_sellers:,.0f}")

    return None

def visoes_gerais(c_df, s_df):
    st.subheader('Visao Geral das Vendas por Estado')

    col1, col2, col3 = st.columns(3)

    # Grafico 1
    vendas_estados = c_df[['customer_state', 'total_price']].groupby('customer_state').sum().reset_index()

    fig1, ax1 = plt.subplots()
    sns.barplot(data=vendas_estados, x= 'customer_state', y= 'total_price', ax=ax1)
    ax1.set_title('Vendas Totais por Estado')
    plt.xlabel('Estado')
    plt.ylabel('Vendas (R$)')
    col1.pyplot(fig1)

    # Grafico 2
    clientes_estado = c_df[['customer_state', 'customer_unique_id']].groupby('customer_state').nunique().reset_index()

    fig2, ax2 = plt.subplots()
    sns.barplot( data=clientes_estado, x='customer_state', y='customer_unique_id', ax=ax2)
    ax2.set_title('Clientes Únicos por Estado')
    plt.xlabel('Estado')
    plt.ylabel('Vendas (R$)')
    col2.pyplot(fig2)

    # Grafico 3
    vendedores_estado = s_df[['seller_state', 'seller_id']].groupby('seller_state').nunique().reset_index()
    fig3, ax3 = plt.subplots()
    sns.barplot( data=vendedores_estado, x='seller_state', y='seller_id', ax=ax3)
    ax3.set_title('Vendedores Únicos por Estado')
    plt.xlabel('Estado')
    plt.ylabel('Vendas (R$)')
    col3.pyplot(fig3)
    
    return None

def visoes_temporais(c_df, s_df):
    st.subheader('Visão Temporal por Estado')

    col1, col2, col3 = st.columns(3)

    vendas_temporal = c_df[['order_purchase_year_month', 'total_price']].groupby('order_purchase_year_month').sum().reset_index()

    fig1, ax1 = plt.subplots()
    sns.lineplot(data=vendas_temporal, x='order_purchase_year_month', y='total_price', ax=ax1)
    ax1.set_title(f'Vendas (R$) por mês')
    plt.xlabel('Ano-mês')
    plt.ylabel('Vendas (R$)')
    plt.xticks(rotation=60)
    col1.pyplot(fig1)

    clientes_temporal = c_df[['order_purchase_year_month', 'customer_unique_id']].groupby('order_purchase_year_month').nunique().reset_index()
    fig2, ax2 = plt.subplots()
    sns.lineplot(data=clientes_temporal, x='order_purchase_year_month', y='customer_unique_id', ax=ax2)
    ax2.set_title(f'Clientes Únicos por mês')
    plt.xlabel('Ano-mês')
    plt.ylabel('Clientes Únicos')
    plt.xticks(rotation=60)
    col2.pyplot(fig2)

    vendedores_temporal = s_df[['order_purchase_year_month', 'seller_id']].groupby('order_purchase_year_month').nunique().reset_index()
    fig3, ax3 = plt.subplots()
    sns.lineplot(data=vendedores_temporal, x='order_purchase_year_month', y='seller_id', ax=ax3)
    ax3.set_title(f'Vendedores Únicos por mês')
    plt.xlabel('Ano-mês')
    plt.ylabel('Vendedores Únicos')
    plt.xticks(rotation=60)
    col3.pyplot(fig3)

    return None
    
def visoes_categoria(c_df, s_df):
    
    st.write("### Análise de Categorias")

    # Primeira Parte: Exibir a fatia dos dados considerada
    st.write("#### Fatia dos Dados Considerada")
    st.dataframe(c_df.reset_index(drop=True))  # Exibe o DataFrame filtrado sem o índice

    # Segunda Parte: Gráfico de barras com as categorias selecionadas e total_price
    st.write("#### Gráfico de Vendas por Categoria (Filtre para uma melhor visualização)")

    # Calcular o total_price por categoria
    df_categorias = c_df.groupby('product_category_name')['total_price'].sum().reset_index()
    df_categorias = df_categorias.sort_values(by='total_price', ascending=False)

    # Calcular a média de todas as categorias (considerando todo o DataFrame)
    total_vendas_todas_categorias = c_df['total_price'].sum()  # Soma total das vendas de todas as categorias
    num_categorias = c_df['product_category_name'].nunique()  # Número de categorias únicas
    media_todas_categorias = total_vendas_todas_categorias / num_categorias  # Média de todas as categorias

    # Criar o gráfico de barras
    fig, ax = plt.subplots(figsize=(6, 3))  # Reduzindo o tamanho do gráfico
    sns.barplot(data=df_categorias, x='product_category_name', y='total_price', ax=ax, palette='viridis')
    ax.axhline(media_todas_categorias, color='red', linestyle='--', label=f'Média de Vendas das categorias: {media_todas_categorias:,.2f}')  # Linha da média
    ax.set_xlabel('Categoria', fontsize=6)
    ax.set_ylabel('Total de Vendas (R$)', fontsize=8)
    ax.set_title('Vendas por Categoria', fontsize=8)
    ax.tick_params(axis='x', rotation=80)  # Rotacionar os rótulos do eixo X para melhor visualização
    ax.legend()
    plt.tight_layout()

    # Exibir o gráfico no Streamlit
    st.pyplot(fig)

def insights(c_df, s_df):

    # Gráfico 1: Comportamento das Top 10 Categorias no 1º Semestre de 2017 e 2018
    st.write("#### Comportamento das Top 10 Categorias (1º Semestre 2017 vs 1º Semestre 2018)")
    st.write("##### Crescimento de vendas das principais categorias quando comparado os períodos.")

    # Filtrar os dados para o primeiro semestre de 2017 e 2018
    df_2017 = c_df[(c_df['order_purchase_year'] == 2017) & (c_df['order_purchase_month'] <= 6)]
    df_2018 = c_df[(c_df['order_purchase_year'] == 2018) & (c_df['order_purchase_month'] <= 6)]

    # Agrupar as vendas por categoria e período
    top_categorias_2017 = df_2017.groupby('product_category_name')['total_price'].sum().nlargest(10).reset_index()
    top_categorias_2018 = df_2018.groupby('product_category_name')['total_price'].sum().nlargest(10).reset_index()

    # Juntar as categorias únicas de ambos os anos
    categorias_unicas = set(top_categorias_2017['product_category_name']).union(set(top_categorias_2018['product_category_name']))

    # Criar um DataFrame com todas as categorias únicas e seus valores em 2017 e 2018
    dados_comparacao = []
    for categoria in categorias_unicas:
        vendas_2017 = df_2017[df_2017['product_category_name'] == categoria]['total_price'].sum()
        vendas_2018 = df_2018[df_2018['product_category_name'] == categoria]['total_price'].sum()
        dados_comparacao.append({'product_category_name': categoria, '2017': vendas_2017, '2018': vendas_2018})

    df_comparacao = pd.DataFrame(dados_comparacao).fillna(0)  # Preencher com 0 se não houver vendas em um dos anos

    # Ordenar as categorias pelo desempenho de 2018 (decrescente)
    df_comparacao = df_comparacao.sort_values(by='2018', ascending=False)

    # Criar o gráfico de barras lado a lado
    fig1, ax1 = plt.subplots()
    df_comparacao.set_index('product_category_name').plot(kind='bar', ax=ax1, color=['skyblue', 'orange'])
    ax1.set_xlabel('Categoria')
    ax1.set_ylabel('Total de Vendas (R$)')
    ax1.set_title('Top 10 Categorias: 1º Semestre 2017 vs 1º Semestre 2018')
    ax1.tick_params(axis='x', rotation=80)
    ax1.tick_params(axis='y')
    ax1.legend(title='Ano')
    st.pyplot(fig1)

    # Gráfico 2: Relação entre product_photos_qty e quantidade de pedidos únicos
    st.write("#### Relação entre Quantidade de Fotos e Pedidos Únicos")
    st.write("##### Não há uma relação clara entre a quantidade de fotos do produto com o número de pedidos, indicando que não é um fator determinante. Nota-se também que grande parte dos produtos possuem poucas fotos.")
    # Agrupar por product_photos_qty e contar a quantidade de pedidos únicos (order_id)
    df_photos = c_df.groupby('product_photos_qty')['order_id'].nunique().reset_index()
    df_photos.rename(columns={'order_id': 'quantidade_pedidos'}, inplace=True)

    # Gráfico barras + kde (qtd de fotos e vendas)
    fig2, ax2 = plt.subplots()
    
    # Histograma com KDE
    sns.histplot(
        data=df_photos, 
        x='product_photos_qty', 
        weights='quantidade_pedidos',  # Peso para refletir a quantidade de pedidos
        binwidth=1,
        kde=True,  # Adiciona a linha KDE
        ax=ax2, 
        color='blue', 
        alpha=0.6, 
        line_kws={'color': 'red', 'linewidth': 1}  # Configurações da linha KDE
    )
    
    ax2.set_xlabel('Quantidade de Fotos')
    # Definir os ticks do eixo X como números inteiros
    ax2.set_xticks(range(int(df_photos['product_photos_qty'].min()), int(df_photos['product_photos_qty'].max()) + 1))
    ax2.set_xticklabels([str(int(x)) for x in ax2.get_xticks()])  # Garantir que os rótulos sejam inteiros

    ax2.set_ylabel('Quantidade de Pedidos Únicos')
    ax2.set_title('Relação entre Quantidade de Fotos e Pedidos Únicos')
    ax2.tick_params(axis='x')
    ax2.tick_params(axis='y')
    
    st.pyplot(fig2)

if __name__ == '__main__':

    definicao_parametros_graficos()

    order_items_df = pd.read_csv('../datasets/order_items_cleaned.csv')
    
    # Side Bar (Filtros)
    customers_df_filtered, sellers_df_filtered = aplicar_filtros(order_items_df)
    
    # Criando abas
    tab1, tab2, tab3 = st.tabs(["Análise Geral", "Análise Categorias", "Insights"])

    # Conteúdo da Aba 1
    with tab1:
        # Título
        st.title('Dashboard de Análise de Vendas por Estado')

        # Big Numbers
        big_numbers(customers_df_filtered, sellers_df_filtered)

        # Visões Gerais
        visoes_gerais(customers_df_filtered, sellers_df_filtered)

        # Visoes Temporais (mês) para o Estado Selecionado
        visoes_temporais(customers_df_filtered, sellers_df_filtered)


    # Conteúdo da Aba 2
    with tab2:
        # Título
        st.title('Dashboard de Análise por Categorias')

        # # Big Numbers
        big_numbers(customers_df_filtered, sellers_df_filtered)

        # # Visões Gerais
        visoes_categoria(customers_df_filtered, sellers_df_filtered)


    # Conteúdo da Aba 3
    with tab3:
        st.header("Insights")

        insights(customers_df_filtered, sellers_df_filtered)


