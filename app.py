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

def main():
    st.title('Avaliação do Ciclo de Vida para ETE')

    st.header('Passo 1: Processo de Tratamento')

    # Tratamento UASB (obrigatório)
    st.subheader('Tratamento UASB')
    st.write('O tratamento UASB é obrigatório.')

    # Processos adicionais (opcionais)
    st.subheader('Processos Adicionais')
    additional_processes = {
        'wetland': st.checkbox('Wetland de Fluxo Vertical'),
        'filtro': st.checkbox('Filtro Biológico Percolador +Decantador Secundário'),
        'lagoa': st.checkbox('Lagoa de Polimento')
    }

    st.header('Passo 2: Inventário do ciclo de vida')
    inputs = {}

    # Consumo de Energia
    st.subheader('Consumo de Energia')
    inputs['eletricidade'] = st.number_input('Eletricidade (kWh/m³)', value=0.0, step=0.1)
    st.info('Se selecionou reaproveitamento de gás, somar a energia gasta do sistema de reaproveitamento.')

    # Uso da Terra
    st.subheader('Uso da Terra')
    inputs['area_utilizada'] = st.number_input('Área utilizada (m²)', value=0.0, step=1.0)

    # Emissões para a Água
    st.subheader('Emissões para a Água')
    inputs['fosforo_total'] = st.number_input('Fósforo Total (kg/m³)', value=0.0, step=0.001)
    inputs['nitrogenio_total'] = st.number_input('Nitrogênio Total (kg/m³)', value=0.0, step=0.001)

    # Parâmetros opcionais
    show_optional = st.checkbox('Mostrar parâmetros opcionais')
    if show_optional:
        optional_params = ['Bário', 'Cobre', 'Selenio', 'Zinco', 'Tolueno', 'Cromo', 'Cádmio', 'Chumbo', 'Níquel']
        for param in optional_params:
            inputs[param.lower()] = st.number_input(f'{param} (kg/m³)', value=0.0, step=0.0001)

    st.info('Fósforo e nitrogênio é obrigatório informar. Os outros parâmetros são opcionais.')

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

if __name__ == "__main__":
    main()
