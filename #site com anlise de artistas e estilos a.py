#site com anlise de artistas e estilos ao longo do tempo
#streamlit run "/home/samha-aim/Documentos/Meus codigod/#site com anlise de artistas e estilos a.py"

import streamlit as st
import pandas as pd
import plotly.express as px

url='https://raw.githubusercontent.com/Samha-aim/Meus-codigod/refs/heads/master/artist.csv'

st.write(
    """
<center>

# Grandes artistas
### Nacionalidade e estilo ao longo do tempo

</center>
""",
    unsafe_allow_html=True,
)

tabela =pd.read_csv(url)
tabela=tabela.drop(columns="artist_id")
# 1. Garante que tudo seja tratado como texto e substitui valores vazios por ""
middle = tabela["middle_names"].fillna("").astype(str)
last = tabela["last_name"].fillna("").astype(str)

# 2. Junta as duas colunas com um espaço entre elas
nova_coluna = middle + " " + last

# 3. Insere exatamente na posição 3 (lembrando que a contagem começa em 0)
tabela.insert(3, "surname", nova_coluna)

# 4. Deleta as colunas de origem (se quiser deletar direto no DataFrame)
tabela = tabela.drop(columns=["middle_names", "last_name"])
st.subheader("Lista de Artistas")
tabela1 = st.dataframe(tabela)

col1, col2 = st.columns(2)
col3 = st.columns(1)
grafico3 = px.histogram(tabela, x="style", color="nationality", title="Distribuição de artistas por estilo e nacionalidade", barmode="group")
st.plotly_chart(grafico3)
# exibição dos graficos
grafico2 = px.pie(tabela, names="nationality", title="Distribuição de artistas por pais", hole=0.3)
col2.plotly_chart(grafico2)

grafico1 = px.pie(tabela, names="style", title="Distribuição de artistas por estilo", hole=0.3)

col1.plotly_chart(grafico1)





#barra lateral
with st.sidebar:
    st.write("filtros de busca")

    busca = st.text_input("Digite o nome do artista que deseja buscar")

    nacionalidade= st.selectbox("Selecione a nacionalidade do artista", options=("todas",) + tuple(tabela["nationality"].unique()))

    estilos = st.multiselect("Selecione o estilo do artista", options=tabela["style"].unique())

    botao_aplicar = st.button("Aplicar Filtros")

sidebar = st.sidebar   

#logica da side bar
tabela_filtrada = tabela.copy()
if busca:
    tabela_filtrada= tabela_filtrada[tabela_filtrada["full_name"].str.contains(busca, case=False)]

if nacionalidade:
    tabela= tabela_filtrada[tabela_filtrada["nationality"] == nacionalidade]

if estilos:
    tabela= tabela_filtrada[tabela_filtrada["style"].isin(estilos)]

if botao_aplicar:
    st.toast("SEUS RESULTADOS ESTÃO AO FIM DA PAGINA!", icon="✅")
    st.subheader(f"📋 Tabela de Artistas ({len(tabela_filtrada)} encontrados)")
    tabela1=st.dataframe(tabela, use_container_width=True)

    col4, col5 = st.columns(2)
    # exibição dos graficos
    grafico2 = px.pie(tabela, names="nationality", title="Distribuição de artistas por pais", hole=0.3)
    col4.plotly_chart(grafico2)

    grafico1 = px.pie(tabela, names="style", title="Distribuição de artistas por estilo", hole=0.3)

    col5.plotly_chart(grafico1)

    grafico3 = px.histogram(tabela, x="style", color="nationality", title="Distribuição de artistas por estilo e nacionalidade", barmode="group")
    plotly_chart = st.plotly_chart(grafico3)

