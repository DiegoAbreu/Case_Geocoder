# Pacotes
import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import geopy.distance

# Título:
st.title('Caso de uso de Geocodificação:')
st.header('Aplicação para encontrar endereços mais próximos')

# Recursos
recursos_df = pd.read_csv('recursos.csv', sep=';', encoding = "ISO-8859-1")
recursos_df['Localidade'] = 'Recursos'
recursos_df['Bolha'] = 0.05

# Mostrar tabela de recursos
#st.write('Esta é nossa lista de pontos de recursos:')
st.text("Um exemplo bastante comum de uso de dados geocodificados é o cálculo de distância \nentre dois ou mais pontos. Diversos sites utilizam esse recurso para permitir que \nos usuários possam pesquisar e encontrar locais próximos.")
st.text("Esta é uma lista de 100 escolas públicas do Rio de Janeiro")


tabela = pd.DataFrame(recursos_df['Ponto'])
tabela


st.text("Um exemplo bastante comum de uso de dados geocodificados é o cálculo de distância \nentre dois ou mais pontos. Diversos sites utilizam esse recurso para permitir que \nos usuários possam pesquisar e encontrar locais próximos.")
st.text("Esta é uma lista de 100 escolas públicas do Rio de Janeiro")

# Plot Recursos
import plotly.express as px
fig = px.scatter_mapbox(recursos_df, lat="Latitude", lon="Longitude", hover_name="Ponto", zoom=10, height=500)
fig.update_layout(mapbox_style="carto-positron")
fig.update_layout(margin={"r":0,"t":25,"l":0,"b":0})
#fig.show()
st.plotly_chart(fig)

st.text("Um exemplo bastante comum de uso de dados geocodificados é o cálculo de distância \nentre dois ou mais pontos. Diversos sites utilizam esse recurso para permitir que \nos usuários possam pesquisar e encontrar locais próximos.")
st.text("Esta é uma lista de 100 escolas públicas do Rio de Janeiro")

# Endereço para geocodificar:
endereco_usuario = st.text_input('Insira Aqui seu endereço','')
# Token:
Token_ = st.sidebar.text_input('Insira o token do Portal de geocodificação','')

def consulta(x):
    if x == '':
        return
    else:
        #Consulta:
        headers = {'accept': '*/*','Authorization': Token_}
        params = (('endereco', x),)
        response = requests.get('https://geosite.oi.net.br/geocodificacao-api/api/v1/geocode/json', headers=headers, params=params)
        # Resultados:
        #resultado = response.json()
        resultado = pd.DataFrame(response.json())
        Loc_usuario = pd.DataFrame()
        Loc_usuario['Ponto'] = resultado['endereco']
        Loc_usuario['Latitude'] = resultado['latitude']
        Loc_usuario['Longitude'] = resultado['longitude']
        Loc_usuario['Bolha'] = 0.3
        Loc_usuario['Localidade'] = "Você"

        # Usuário + Recursos
        usu_recs = pd.concat([Loc_usuario, recursos_df])

        # Concatenação de lat_longs
        ref_usuario = list(zip(Loc_usuario['Latitude'], Loc_usuario['Longitude']))
        lat_long = list(zip(usu_recs['Latitude'], usu_recs['Longitude']))


        # Distancia ref_usu
        list_dist = list(map(lambda x: round(geopy.distance.distance(x, ref_usuario).km,3), lat_long))
        usu_recs["distancia_da_ref(km)"] = list_dist
        usu_recs = usu_recs.reset_index(drop=True)
        usu_recs = usu_recs.sort_values(by=['distancia_da_ref(km)'])
        usu_recs = usu_recs.reset_index(drop=True)


        # Tag top 5
        usu_recs.loc[usu_recs.index <= 5, 'Localidade'] = 'Recursos mais próximos' 
        usu_recs.loc[usu_recs.index == 0, 'Localidade'] = 'Você' 


        # Top 5 mais próximas
        st.write('Esses são os 5 pontos mais próximos:')
        st.text("Um exemplo bastante comum de uso de dados geocodificados é o cálculo de distância \nentre dois ou mais pontos. Diversos sites utilizam esse recurso para permitir que \nos usuários possam pesquisar e encontrar locais próximos.")
        st.text("Esta é uma lista de 100 escolas públicas do Rio de Janeiro")
        # Plot
        import plotly.express as px
        fig = px.scatter_mapbox(usu_recs, lat="Latitude", lon="Longitude", hover_name="Ponto", zoom=10, height=500, color="Localidade", size= 'Bolha')
        fig.update_layout(mapbox_style="carto-positron")
        fig.update_layout(margin={"r":0,"t":25,"l":0,"b":0})
        fig.update_layout({'legend_orientation':'h'})
        #fig.show()
        st.plotly_chart(fig)
        # DataFrame Top5
        top_5 = (usu_recs.loc[1:]).head()
        top_5

        st.text("Um exemplo bastante comum de uso de dados geocodificados é o cálculo de distância \nentre dois ou mais pontos. Diversos sites utilizam esse recurso para permitir que \nos usuários possam pesquisar e encontrar locais próximos.")
        st.text("Esta é uma lista de 100 escolas públicas do Rio de Janeiro")
        usu_recs
        return
consulta(endereco_usuario)

