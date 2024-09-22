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
processes = st.multiselect(
    'Selecione o(s) Processo(s)',
    ['UASB', 'Wetland de Fluxo Vertical', 'Filtro Biológico Percolador', 'Lagoa de Polimento']
)

chemicals = st.multiselect(
    'Selecione os Produto(s) Químico(s) utilizados',
    list(IMPACT_FACTORS.keys())
)

st.header('Passo 2: Inventário do ciclo de vida')
inputs = {}

st.subheader('Consumo de Energia')
inputs['eletricidade'] = st.number_input('Eletricidade (kWh/m³)', value=0.0, step=0.1)

st.subheader('Consumo de Produtos Químicos')
for chemical in chemicals:
    inputs[chemical] = st.number_input(f'{chemical.replace("_", " ").title()} (kg/m³)', value=0.0, step=0.1)

st.subheader('Emissões para a Água')
inputs['fosforo_total'] = st.number_input('Fósforo Total (kg/m³)', value=0.0, step=0.001)
inputs['nitrogenio_total'] = st.number_input('Nitrogênio Total (kg/m³)', value=0.0, step=0.001)

if st.button('Calcular Impactos'):
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
