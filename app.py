import streamlit as st
import pandas as pd
import plotly.express as px

# Definição dos fatores de impacto (simplificados para este exemplo)
IMPACT_FACTORS = {
    'eletricidade': {
        'aquecimento_global': 0.25056,
        'ecotoxidade_agua': 0.00097,
        'eutrofizacao_agua': 0.00000,
    },
    'cloreto_ferrico': {
        'aquecimento_global': 0.05594,
        'ecotoxidade_agua': 0.06756,
        'eutrofizacao_agua': 1.09053,
    },
    'sulfato_aluminio': {
        'aquecimento_global': 0.35950,
        'ecotoxidade_agua': 0.06946,
        'eutrofizacao_agua': 0.00034,
    },
}

IMPACT_NAMES = {
    'aquecimento_global': "Aquecimento Global (kg CO2 eq)",
    'ecotoxidade_agua': "Ecotoxidade de Água Doce (kg 1,4-DCB)",
    'eutrofizacao_agua': "Eutrofização de Água Doce (kg P eq)",
}

def calculate_impacts(inputs):
    results = {impact: 0 for impact in IMPACT_NAMES}
    for input_name, value in inputs.items():
        if input_name in IMPACT_FACTORS:
            for impact, factor in IMPACT_FACTORS[input_name].items():
                results[impact] += value * factor
    return results

st.title('Avaliação do Ciclo de Vida para ETE')

# Passo 1: Processo de Tratamento
st.header('Passo 1: Processo de Tratamento')

# Tratamento Preliminar (obrigatório)
st.subheader('Tratamento Preliminar')
st.write('O tratamento preliminar é obrigatório.')

col1, col2 = st.columns(2)
with col1:
    distance = st.number_input('Distância para o transporte de resíduos (Ida e Volta) (km)', min_value=0.0, step=0.1)
    quantity = st.number_input('Quantidade de resíduos (ton/m³)', min_value=0.0, step=0.001)
with col2:
    destination = st.selectbox('Destino dos resíduos', ['Lixão', 'Aterro Sanitário'])

st.info('A quantidade é multiplicada pelo km, isso dá o fator em ton.km')
st.info('Os impactos em cada categoria são diferentes de acordo com a destinação.')

ton_km_factor = distance * quantity
st.write(f'Fator ton.km: {ton_km_factor:.2f}')

# UASB (pré-selecionado)
st.subheader('Tratamento UASB')
st.write('O tratamento UASB está pré-selecionado.')

# Processos adicionais
st.subheader('Processos Adicionais')
additional_processes = st.multiselect(
    'Selecione o(s) Processo(s) Adicional(is)',
    ['Wetland de Fluxo Vertical', 'Filtro Biológico percolador + Decantador Segundario', 'Lagoa de Polimento']
)

# Passo 2: Inventário do ciclo de vida
st.header('Passo 2: Inventário do ciclo de vida')

inputs = {}

st.subheader('Consumo de Energia')
inputs['eletricidade'] = st.number_input('Eletricidade (kWh/m³)', value=0.0, step=0.1)

st.subheader('Uso da Terra')
inputs['area_utilizada'] = st.number_input('Área utilizada (m²)', value=0.0, step=0.1)

st.subheader('Emissões para a Água')
inputs['fosforo_total'] = st.number_input('Fósforo Total (kg/m³)', value=0.0, step=0.001)
inputs['nitrogenio_total'] = st.number_input('Nitrogênio Total (kg/m³)', value=0.0, step=0.001)

st.write("Os outros parâmetros são opcionais. Clique em 'Mostrar mais' para exibi-los.")
if st.checkbox('Mostrar mais'):
    optional_params = ['Bário', 'Cobre', 'Selênio', 'Zinco', 'Tolueno', 'Cromo', 'Cádmio', 'Chumbo', 'Níquel']
    for param in optional_params:
        inputs[param.lower()] = st.number_input(f'{param} (kg/m³)', value=0.0, step=0.0001)

# Passo 3: Disposição do Lodo
st.header('Passo 3: Disposição do Lodo')

disposicao_lodo = st.selectbox(
    'Escolha o método de disposição do lodo',
    ['Disposição em aterro', 'Disposição em lixão', 'Ferti-irrigação ou agricultura']
)

if disposicao_lodo in ['Disposição em aterro', 'Disposição em lixão']:
    st.subheader('Tratamento do Lodo')
    
    col1, col2 = st.columns(2)
    with col1:
        distancia_lodo = st.number_input('Distância para o transporte do lodo (Ida e Volta) (km)', min_value=0.0, step=0.1)
    with col2:
        quantidade_lodo = st.number_input('Quantidade de lodo (ton/m³)', min_value=0.0, step=0.001)
    
    ton_km_factor_lodo = distancia_lodo * quantidade_lodo
    st.write(f'Fator ton.km para o lodo: {ton_km_factor_lodo:.2f}')

elif disposicao_lodo == 'Ferti-irrigação ou agricultura':
    st.subheader('Composição do Lodo')
    
    col1, col2 = st.columns(2)
    with col1:
        lodo_fosforo = st.number_input('Fósforo (kg/m³)', min_value=0.0, step=0.001)
    with col2:
        lodo_nitrogenio = st.number_input('Nitrogênio Amoniacal (kg/m³)', min_value=0.0, step=0.001)
    
    st.write("Elementos adicionais (opcionais)")
    if st.checkbox('Mostrar mais elementos'):
        elementos_adicionais = [
            'Arsênio', 'Bário', 'Cádmio', 'Chumbo', 'Cobre', 'Cromo',
            'Molibdênio', 'Níquel', 'Estanho', 'Zinco', '1,4-Diclorobenzeno'
        ]
        for elemento in elementos_adicionais:
            inputs[f'lodo_{elemento.lower()}'] = st.number_input(f'{elemento} (kg/m³)', value=0.0, step=0.0001)

# Passo 4: Queima de Biogás
st.header('Passo 4: Queima de Biogás')

tipo_queimador = st.selectbox(
    'Escolha o tipo de queimador',
    ['Queimador aberto', 'Queimador fechado com reaproveitamento energético']
)

if tipo_queimador == 'Queimador fechado com reaproveitamento energético':
    st.subheader('Emissões do Queimador Fechado')
    inputs['dioxido_carbono_fechado'] = st.number_input('Dióxido de Carbono (kg/m³)', min_value=0.0, step=0.001)

elif tipo_queimador == 'Queimador aberto':
    st.subheader('Emissões do Queimador Aberto')
    
    col1, col2 = st.columns(2)
    with col1:
        inputs['metano_aberto'] = st.number_input('Metano (kg/m³)', min_value=0.0, step=0.001)
        inputs['dioxido_carbono_aberto'] = st.number_input('Dióxido de Carbono (kg/m³)', min_value=0.0, step=0.001)
    with col2:
        inputs['nitrogenio_amoniacal_aberto'] = st.number_input('Nitrogênio Amoniacal (kg/m³)', min_value=0.0, step=0.001)

if st.button('Calcular Impactos'):
    # Adicione as informações do lodo aos inputs
    if disposicao_lodo in ['Disposição em aterro', 'Disposição em lixão']:
        inputs['ton_km_factor_lodo'] = ton_km_factor_lodo
        inputs['disposicao_lodo'] = disposicao_lodo
    elif disposicao_lodo == 'Ferti-irrigação ou agricultura':
        inputs['lodo_fosforo'] = lodo_fosforo
        inputs['lodo_nitrogenio'] = lodo_nitrogenio
        inputs['disposicao_lodo'] = disposicao_lodo
    
    # Adicione as informações do queimador aos inputs
    inputs['tipo_queimador'] = tipo_queimador
    
    results = calculate_impacts(inputs)
    
    st.header('Resultados')
    
    # Criar um DataFrame para os resultados
    df_results = pd.DataFrame(list(results.items()), columns=['Impacto', 'Valor'])
    df_results['Impacto'] = df_results['Impacto'].map(IMPACT_NAMES)
    
    # Criar gráfico de barras com Plotly
    fig = px.bar(df_results, x='Impacto', y='Valor', title='Impactos Ambientais')
    st.plotly_chart(fig)
    
    # Mostrar resultados em formato de tabela
    st.table(df_results)
