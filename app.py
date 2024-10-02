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

st.header('Passo 1: Processo de Tratamento')

# Tratamento Preliminar (obrigatório)
st.subheader('Tratamento Preliminar')
st.write('O tratamento preliminar é obrigatório.')

# Campos para o tratamento preliminar
col1, col2 = st.columns(2)
with col1:
    distance = st.number_input('Distância para o transporte de resíduos (Ida e Volta) (km)', min_value=0.0, step=0.1)
    quantity = st.number_input('Quantidade de resíduos (ton/m³)', min_value=0.0, step=0.001)
with col2:
    destination = st.selectbox('Destino dos resíduos', ['Lixão', 'Aterro Sanitário'])

st.info('A quantidade é multiplicada pelo km, isso dá o fator em ton.km')
st.info('Os impactos em cada categoria são diferentes de acordo com a destinação.')

# Cálculo do fator ton.km
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

if st.button('Calcular Impactos'):
    # Adicione o fator ton.km e o destino dos resíduos aos inputs
    inputs['ton_km_factor'] = ton_km_factor
    inputs['destino_residuos'] = destination
    
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
