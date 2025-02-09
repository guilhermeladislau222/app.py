import streamlit as st
import pandas as pd
import plotly.express as px

# Definição completa dos fatores de impacto baseados na tabela fornecida
IMPACT_FACTORS = {
    'eletricidade': {
        'Ecotoxidade de Água Doce': 0.00097,
        'Eutrofização de Água Doce': 0.00000,
        'Aquecimento Global': 0.25056,
        'Uso da Terra': 0.00142,
        'Ecotoxidade Marinha': 0.00144,
        'Eutrofização Marinha': 0.00,
        'Ecotoxidade Terrestre': 0.28,
    },
    'cloreto_ferrico': {
        'Ecotoxidade de Água Doce': 0.06756,
        'Eutrofização de Água Doce': 1.09053,
        'Aquecimento Global': 0.05594,
        'Uso da Terra': 0.09093,
        'Ecotoxidade Marinha': 0.00002,
        'Eutrofização Marinha': 0.00,
        'Ecotoxidade Terrestre': 5.87,
    },
    'sulfato_ferro': {
        'Ecotoxidade de Água Doce': 0.02592,
        'Eutrofização de Água Doce': 0.27481,
        'Aquecimento Global': 0.02132,
        'Uso da Terra': 0.03479,
        'Ecotoxidade Marinha': 0.00001,
        'Eutrofização Marinha': 0.00,
        'Ecotoxidade Terrestre': 0.00,
    },
    'policloreto_aluminio': {
        'Ecotoxidade de Água Doce': 0.11691,
        'Eutrofização de Água Doce': 0.00051,
        'Aquecimento Global': 1.87017,
        'Uso da Terra': -0.04174,
        'Ecotoxidade Marinha': 0.16189,
        'Eutrofização Marinha': 0.00,
        'Ecotoxidade Terrestre': 10.55,
    },
    'sulfato_aluminio': {
        'Ecotoxidade de Água Doce': 0.06946,
        'Eutrofização de Água Doce': 0.00034,
        'Aquecimento Global': 0.35950,
        'Uso da Terra': 0.02799,
        'Ecotoxidade Marinha': 0.09619,
        'Eutrofização Marinha': 0.00,
        'Ecotoxidade Terrestre': 6.44,
    },
    'hipoclorito_sodio': {
        'Ecotoxidade de Água Doce': 0.07766,
        'Eutrofização de Água Doce': 0.00026,
        'Aquecimento Global': 3.00893,
        'Uso da Terra': 0.07189,
        'Ecotoxidade Marinha': 0.10527,
        'Eutrofização Marinha': 0.00,
        'Ecotoxidade Terrestre': 15.28,
    },
    'acido_paracetico': {
        'Ecotoxidade de Água Doce': -0.01571,
        'Eutrofização de Água Doce': 0.00069,
        'Aquecimento Global': 1.15457,
        'Uso da Terra': -0.03251,
        'Ecotoxidade Marinha': -0.01050,
        'Eutrofização Marinha': 0.00,
        'Ecotoxidade Terrestre': 2.73,
    },
    'peroxido_hidrogenio': {
        'Ecotoxidade de Água Doce': 0.06871,
        'Eutrofização de Água Doce': 0.00037,
        'Aquecimento Global': 1.56913,
        'Uso da Terra': 0.03429,
        'Ecotoxidade Marinha': 0.09324,
        'Eutrofização Marinha': 0.00,
        'Ecotoxidade Terrestre': 7.48,
    },
    'cal': {
        'Ecotoxidade de Água Doce': 0.00106,
        'Eutrofização de Água Doce': 0.00001,
        'Aquecimento Global': 0.96049,
        'Uso da Terra': 0.01615,
        'Ecotoxidade Marinha': 0.00250,
        'Eutrofização Marinha': 0.00,
        'Ecotoxidade Terrestre': 1.46,
    },
    'hidroxido_sodio': {
        'Ecotoxidade de Água Doce': 0.11233,
        'Eutrofização de Água Doce': 0.00279,
        'Aquecimento Global': 1.33577,
        'Uso da Terra': 0.52521,
        'Ecotoxidade Marinha': 0.15473,
        'Eutrofização Marinha': 0.00,
        'Ecotoxidade Terrestre': 12.12,
    },
    'nitrato_calcio': {
        'Ecotoxidade de Água Doce': 0.09145,
        'Eutrofização de Água Doce': 0.00039,
        'Aquecimento Global': 2.93506,
        'Uso da Terra': 0.05360,
        'Ecotoxidade Marinha': 0.12332,
        'Eutrofização Marinha': 0.00,
        'Ecotoxidade Terrestre': 18.11,
    },
    'sulfato_sodio': {
        'Ecotoxidade de Água Doce': 0.04309,
        'Eutrofização de Água Doce': 0.00016,
        'Aquecimento Global': 0.71981,
        'Uso da Terra': 0.06517,
        'Ecotoxidade Marinha': 0.05961,
        'Eutrofização Marinha': 0.00,
        'Ecotoxidade Terrestre': 7.72,
    },
    'transportes': {
        'Ecotoxidade de Água Doce': 0.01729,
        'Eutrofização de Água Doce': 0.00008,
        'Aquecimento Global': 0.59323,
        'Uso da Terra': 0.01975,
        'Ecotoxidade Marinha': 0.02558,
        'Eutrofização Marinha': 0.00,
        'Ecotoxidade Terrestre': 6.21,
    },
    'uso_terra': {
        'Uso da Terra': 1.00,
    },
    'fosforo_total': {
        'Eutrofização de Água Doce': 1.0000,
    },
    'nitrogenio_total': {
        'Eutrofização Marinha': 0.297,
    },
    'bario': {
        'Ecotoxidade de Água Doce': 2.7900,
        'Ecotoxidade Marinha': 3.93,
        'Ecotoxidade Terrestre': 1.33e-16,
    },
    'cobre': {
        'Ecotoxidade de Água Doce': 162.0000,
        'Ecotoxidade Marinha': 193.0,
        'Ecotoxidade Terrestre': 1.01e-14,
    },
    'selenio': {
        'Ecotoxidade de Água Doce': 15.3000,
        'Ecotoxidade Marinha': 19.1,
        'Ecotoxidade Terrestre': 8.79e-16,
    },
    'zinco': {
        'Ecotoxidade de Água Doce': 211.0000,
        'Ecotoxidade Marinha': 299.0,
        'Ecotoxidade Terrestre': 1.29e-14,
    },
    'tolueno': {
        'Ecotoxidade de Água Doce': 0.1390,
        'Ecotoxidade Marinha': 0.00276,
        'Ecotoxidade Terrestre': 0.0301,
    },
    'cromo': {
        'Ecotoxidade de Água Doce': 2.3000,
        'Ecotoxidade Marinha': 2.47,
        'Ecotoxidade Terrestre': 1.54e-16,
    },
    'cadmio': {
        'Ecotoxidade de Água Doce': 16.8000,
        'Ecotoxidade Marinha': 19.6,
        'Ecotoxidade Terrestre': 8.73e-16,
    },
    'chumbo': {
        'Ecotoxidade de Água Doce': 0.6060,
        'Ecotoxidade Marinha': 0.593,
        'Ecotoxidade Terrestre': 2.59e-17,
    },
    'niquel': {
        'Ecotoxidade de Água Doce': 46.0000,
        'Ecotoxidade Marinha': 57.1,
        'Ecotoxidade Terrestre': 2.91e-15,
    },
    'fosforo': {
        'Eutrofização de Água Doce': 0.1000,
    },
    'nitrogenio_amoniacal': {
        'Eutrofização de Água Doce': 0.1000,
    },
    'arsenio': {
        'Ecotoxidade de Água Doce': 1.6300,
        'Ecotoxidade Marinha': 1.33,
        'Ecotoxidade Terrestre': 6.42e-17,
    },
    'estanho': {
        'Ecotoxidade de Água Doce': 0.0696,
        'Ecotoxidade Marinha': 0.0444,
    },
    'diclorobenzeno': {
        'Ecotoxidade de Água Doce': 0.0320,
        'Ecotoxidade Marinha': 0.0816,
        'Ecotoxidade Terrestre': 1.00,
    },
    'metano': {
        'Aquecimento Global': 34.0,
    },
    'oxido_nitroso': {
        'Aquecimento Global': 298.0,
    },
    'dioxido_carbono': {
        'Aquecimento Global': 1.00,
    },
    'residuos_trat_preliminar_aterro': {
        'Ecotoxidade de Água Doce': 3.09e-04,
        'Eutrofização de Água Doce': 1.44e-03,
        'Aquecimento Global': 8.71e-02,
        'Uso da Terra': 7.83e-04,
        'Ecotoxidade Marinha': 5.01e-04,
        'Eutrofização Marinha': 4.69e-04,
        'Ecotoxidade Terrestre': 1.08e-01,
    },
    'residuos_trat_preliminar_lixao': {
        'Ecotoxidade de Água Doce': 4.80e-01,
        'Eutrofização de Água Doce': 7.35e-05,
        'Aquecimento Global': 9.84e-01,
        'Uso da Terra': 0.0026,
        'Ecotoxidade Marinha': 6.35e-01,
        'Eutrofização Marinha': 8.96e-04,
        'Ecotoxidade Terrestre': 3.03e-03,
    },
    'lodo_aterro': {
        'Ecotoxidade de Água Doce': 3.09e-04,
        'Eutrofização de Água Doce': 1.44e-03,
        'Aquecimento Global': 8.71e-02,
        'Uso da Terra': 7.83e-04,
        'Ecotoxidade Marinha': 5.01e-04,
        'Eutrofização Marinha': 4.69e-04,
        'Ecotoxidade Terrestre': 1.08e-01,
    },
    'lodo_lixao': {
        'Ecotoxidade de Água Doce': 4.80e-01,
        'Eutrofização de Água Doce': 7.35e-05,
        'Aquecimento Global': 9.84e-01,
        'Uso da Terra': 0.0026,
        'Ecotoxidade Marinha': 6.35e-01,
        'Eutrofização Marinha': 8.96e-04,
        'Ecotoxidade Terrestre': 3.03e-03,
    },
}

IMPACT_NAMES = {
    'Ecotoxidade de Água Doce': "Ecotoxidade de Água Doce (kg 1,4-DCB)",
    'Eutrofização de Água Doce': "Eutrofização de Água Doce (kg P eq)",
    'Aquecimento Global': "Aquecimento Global (kg CO2 eq)",
    'Uso da Terra': "Uso da Terra (m2a crop eq)",
    'Ecotoxidade Marinha': "Ecotoxidade Marinha (kg 1,4-DCB)",
    'Eutrofização Marinha': "Eutrofização Marinha (kg N eq)",
    'Ecotoxidade Terrestre': "Ecotoxidade Terrestre (kg 1,4-DCB)",
}

# [Mantenha a definição de IMPACT_FACTORS e IMPACT_NAMES como está]

def parse_scientific_notation(value):
    try:
        return float(value)
    except ValueError:
        return 0.0

def number_input_scientific(label, value=0.0, step=0.1):
    value_input = st.text_input(label, value=str(value))
    return parse_scientific_notation(value_input)

def calculate_impacts(inputs):
    results = {impact: 0 for impact in IMPACT_NAMES}
    
    # Processando entradas básicas (energia elétrica)
    if 'eletricidade' in inputs:
        for impact, factor in IMPACT_FACTORS['eletricidade'].items():
            results[impact] += inputs['eletricidade'] * factor
    
    # Processando Uso da Terra
    if 'area_utilizada' in inputs:
        results['Uso da Terra'] += inputs['area_utilizada'] * IMPACT_FACTORS['uso_terra']['Uso da Terra']
    
    # Processando Transporte de Resíduos (incluindo preliminar)
    total_transport = 0
    if 'ton_km_factor' in inputs:
        total_transport += inputs['ton_km_factor']
    if 'ton_km_factor_lodo' in inputs:
        total_transport += inputs['ton_km_factor_lodo']
    
    if total_transport > 0:
        for impact, factor in IMPACT_FACTORS['transportes'].items():
            results[impact] += total_transport * factor
    
    # Processando Disposição de Resíduos do Tratamento Preliminar
    if 'quantity' in inputs and 'destination' in inputs:
        impact_key = 'residuos_trat_preliminar_aterro' if inputs['destination'] == 'Aterro Sanitário' else 'residuos_trat_preliminar_lixao'
        for impact, factor in IMPACT_FACTORS[impact_key].items():
            results[impact] += inputs['quantity'] * factor
    
    # Processando Lodo
    if 'disposicao_lodo' in inputs and 'quantidade_lodo' in inputs:
        if inputs['disposicao_lodo'] == 'Disposição em aterro':
            impact_key = 'lodo_aterro'
        elif inputs['disposicao_lodo'] == 'Disposição em lixão':
            impact_key = 'lodo_lixao'
        
        if impact_key:
            for impact, factor in IMPACT_FACTORS[impact_key].items():
                results[impact] += inputs['quantidade_lodo'] * factor
    
    # Processando emissões para água

    for emission, factors in water_emissions.items():
        if emission in inputs and inputs[emission] > 0:
            for impact, factor in factors.items():
                results[impact] += inputs[emission] * factor
    
    # Processando emissões para solo (ferti-irrigação)
        
        for lodo_key, impact_key in soil_emissions.items():
            input_key = f'lodo_{lodo_key}'
            if input_key in inputs and inputs[input_key] > 0:
                for impact, factor in IMPACT_FACTORS[impact_key].items():
                    results[impact] += inputs[input_key] * factor
    
    # Processando emissões atmosféricas do biogás
    gas_emissions = ['metano', 'oxido_nitroso', 'dioxido_carbono']
    for emission in gas_emissions:
        if emission in inputs and inputs[emission] > 0:
            if 'Aquecimento Global' in IMPACT_FACTORS[emission]:
                results['Aquecimento Global'] += inputs[emission] * IMPACT_FACTORS[emission]['Aquecimento Global']
    
    return results


# Atualização da parte de visualização
if st.button('Calcular Impactos'):
    # ... [código anterior de processamento de inputs permanece igual]
    
    results = calculate_impacts(inputs)
    
    
    # Criando o gráfico de barras com Plotly
    fig = px.bar(
        df_results,
        x='Categoria de Impacto',
        y='Valor',
        title='Impactos Ambientais por Categoria',
        labels={'Valor': 'Impacto'},
        template='plotly_white'
    )
    
    # Customização do layout
    fig.update_layout(
        xaxis_title='Categoria de Impacto',
        yaxis_title='Valor do Impacto',
        xaxis={'tickangle': 45},
        showlegend=False,
        height=600
    )
    
    # Exibição dos resultados
    st.plotly_chart(fig)
    st.table(df_results)
