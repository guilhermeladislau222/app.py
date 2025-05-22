import streamlit as st
import pandas as pd
import plotly.express as px

# Valores de referência da tabela para cada cenário
SCENARIO_VALUES = {
    'Somente UASB': {
        'eletricidade': 3.58e-03,
        'fosforo_total': 5.82e-03,
        'nitrogenio_total': 6.72e-02,
        'cobre': 2.14e-05,
        'selenio': 8.00e-06,
        'zinco': 1.32e-04,
        'tolueno': 8.51e-03,
        'cromo': 1.38e-05,
        'lodo_fosforo': 3.83e-04,
        'lodo_arsenio': 1.58e-07,
        'lodo_bario': 7.01e-06,
        'lodo_cadmio': 6.70e-08,
        'lodo_chumbo': 1.55e-06,
        'lodo_cobre': 1.39e-05,
        'lodo_cromo': 5.09e-06,
        'lodo_molibdenio': 1.76e-06,
        'lodo_niquel': 1.52e-06,
        'lodo_zinco': 6.47e-05,
        'metano': 3.11e-02,
        'dioxido_carbono': 1.68e-02,
        'quantity': 2.55e-02,
        'ton_km_factor': 2.38e-02
    },
    'UASB+FBP': {
        'eletricidade': 9.60e-01,
        'fosforo_total': 4.07e-03,
        'nitrogenio_total': 4.70e-02,
        'cobre': 1.06e-05,
        'selenio': 8.00e-06,
        'zinco': 4.85e-05,
        'tolueno': 8.51e-03,
        'cromo': 0.00e+00,
        'lodo_fosforo': 6.15e-04,
        'lodo_arsenio': 1.58e-07,
        'lodo_bario': 7.01e-06,
        'lodo_cadmio': 6.70e-08,
        'lodo_chumbo': 1.55e-06,
        'lodo_cobre': 1.39e-05,
        'lodo_cromo': 3.00e+00,
        'lodo_molibdenio': 1.76e-06,
        'lodo_niquel': 1.52e-06,
        'lodo_zinco': 6.47e-05,
        'metano': 3.31e-02,
        'oxido_nitroso': 1.00e-03,
        'dioxido_carbono': 1.09e-01,
        'quantity': 2.55e-02,
        'ton_km_factor': 2.38e-02,
        'quantidade_lodo': 1.71e-01,
        'ton_km_factor_lodo': 3.95e+02
    },
    'UASB+Wetland': {
        'eletricidade': 2.46e-01,
        'fosforo_total': 2.57e-03,
        'nitrogenio_total': 3.51e-02,
        'cobre': 7.00e-05,
        'selenio': 8.00e-06,
        'zinco': 5.00e-04,
        'tolueno': 8.51e-03,
        'cromo': 0.00e+00,
        'cadmio': 5.00e-05,
        'chumbo': 1.57e-03,
        'niquel': 1.80e-04,
        'lodo_fosforo': 3.83e-04,
        'lodo_arsenio': 1.58e-07,
        'lodo_bario': 7.01e-06,
        'lodo_cadmio': 6.70e-08,
        'lodo_chumbo': 1.55e-06,
        'lodo_cobre': 1.39e-05,
        'lodo_cromo': 3.00e+00,
        'lodo_molibdenio': 1.76e-06,
        'lodo_niquel': 1.52e-06,
        'lodo_zinco': 6.47e-05,
        'metano': 3.64e-04,
        'oxido_nitroso': 1.70e-05,
        'dioxido_carbono': 2.24e-02,
        'quantity': 2.55e-02,
        'ton_km_factor': 2.38e-02,
        'quantidade_lodo': 5.87e-02,
        'ton_km_factor_lodo': 3.16e+01
    },
    'UASB+LP': {
        'eletricidade': 2.46e-01,
        'fosforo_total': 3.29e-03,
        'nitrogenio_total': 3.18e-02,
        'lodo_fosforo': 3.83e-04,
        'lodo_arsenio': 1.58e-07,
        'lodo_bario': 7.01e-06,
        'lodo_cadmio': 6.70e-08,
        'lodo_chumbo': 1.55e-06,
        'lodo_cobre': 1.39e-05,
        'lodo_cromo': 3.00e+00,
        'lodo_molibdenio': 1.76e-06,
        'lodo_niquel': 1.52e-06,
        'lodo_zinco': 6.47e-05,
        'metano': 3.11e-02,
        'nitrogenio_amoniacal': 5.80e-04,
        'quantity': 2.55e-02,
        'ton_km_factor': 2.38e-02,
        'quantidade_lodo': 5.87e-02,
        'ton_km_factor_lodo': 3.16e+01
    },
    'Reaproveitamento Biogás': {
        'eletricidade': 1.92e-02,
        'dioxido_carbono': 4.08e-02,
        'quantidade_biogas': 4.17e-01
    }
}

# Fatores para impactos
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
        'Ecotoxidade de Água Doce': 1.5100,
        'Ecotoxidade Marinha': 3.47,
        'Ecotoxidade Terrestre': 6.42e-17,
    },
    'cobre': {
        'Ecotoxidade de Água Doce': 6.17,
        'Ecotoxidade Marinha': 4.19,
        'Ecotoxidade Terrestre': 2.24e-16,
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
        'Ecotoxidade de Água Doce': 0.8530,
        'Ecotoxidade Marinha': 0.543,
        'Ecotoxidade Terrestre': 3.94e-17,
    },
    'cadmio': {
        'Ecotoxidade de Água Doce': 2.0400,
        'Ecotoxidade Marinha': 1.36,
        'Ecotoxidade Terrestre': 7.04e-17,
    },
    'chumbo': {
        'Ecotoxidade de Água Doce': 0.0074,
        'Ecotoxidade Marinha': 0.0039,
        'Ecotoxidade Terrestre': 2.03e-17,
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

# Adicione as novas funções aqui
def calculate_impacts_by_category(inputs, impact_type):
    category_impacts = {
        'Consumo de Energia': 0,
        'Produtos Químicos': 0,
        'Transportes': 0,
        'Emissões para a Água': 0,
        'Emissões Atmosféricas': 0,
        'Disposição de Lodo': 0,
        'Disposição de Resíduos': 0
    }
    
    # Produtos Químicos
    chemical_products = ['cloreto_ferrico', 'sulfato_ferro', 'policloreto_aluminio', 
                        'sulfato_aluminio', 'hipoclorito_sodio', 'acido_paracetico',
                        'peroxido_hidrogenio', 'cal', 'hidroxido_sodio', 'nitrato_calcio',
                        'sulfato_sodio']
    for product in chemical_products:
        if product in inputs:
            category_impacts['Produtos Químicos'] += inputs[product] * IMPACT_FACTORS.get(product, {}).get(impact_type, 0)

    # Emissões para a Água
    water_emissions = ['fosforo_total', 'nitrogenio_total', 'bario', 'cobre', 'selenio', 
                      'zinco', 'tolueno', 'cromo', 'cadmio', 'chumbo', 'niquel']
    for emission in water_emissions:
        if emission in inputs:
            category_impacts['Emissões para a Água'] += inputs[emission] * IMPACT_FACTORS.get(emission, {}).get(impact_type, 0)

    # Emissões Atmosféricas
    if 'metano' in inputs:
        category_impacts['Emissões Atmosféricas'] += inputs['metano'] * IMPACT_FACTORS.get('metano', {}).get(impact_type, 0)
    if 'dioxido_carbono' in inputs:
        category_impacts['Emissões Atmosféricas'] += inputs['dioxido_carbono'] * IMPACT_FACTORS.get('dioxido_carbono', {}).get(impact_type, 0)
    if 'oxido_nitroso' in inputs:
        category_impacts['Emissões Atmosféricas'] += inputs['oxido_nitroso'] * IMPACT_FACTORS.get('oxido_nitroso', {}).get(impact_type, 0)

    # Consumo de Energia
    if 'eletricidade' in inputs:
        category_impacts['Consumo de Energia'] = inputs['eletricidade'] * IMPACT_FACTORS.get('eletricidade', {}).get(impact_type, 0)

    # Transportes
    if 'ton_km_factor' in inputs:
        category_impacts['Transportes'] += inputs['ton_km_factor'] * IMPACT_FACTORS.get('transportes', {}).get(impact_type, 0)
    if 'ton_km_factor_lodo' in inputs:
        category_impacts['Transportes'] += inputs['ton_km_factor_lodo'] * IMPACT_FACTORS.get('transportes', {}).get(impact_type, 0)
    if 'transportes_quimicos' in inputs:
        category_impacts['Transportes'] += inputs['transportes_quimicos'] * IMPACT_FACTORS.get('transportes', {}).get(impact_type, 0)

    # Disposição de Lodo
    if 'quantidade_lodo' in inputs and 'disposicao_lodo' in inputs:
        if inputs['disposicao_lodo'] == 'Disposição em aterro':
            category_impacts['Disposição de Lodo'] = inputs['quantidade_lodo'] * IMPACT_FACTORS.get('lodo_aterro', {}).get(impact_type, 0)
        elif inputs['disposicao_lodo'] == 'Disposição em lixão':
            category_impacts['Disposição de Lodo'] = inputs['quantidade_lodo'] * IMPACT_FACTORS.get('lodo_lixao', {}).get(impact_type, 0)

    # Disposição de Resíduos
    if 'quantity' in inputs and 'destination' in inputs:
        if inputs['destination'] == 'Aterro Sanitário':
            category_impacts['Disposição de Resíduos'] = inputs['quantity'] * IMPACT_FACTORS.get('residuos_trat_preliminar_aterro', {}).get(impact_type, 0)
        else:
            category_impacts['Disposição de Resíduos'] = inputs['quantity'] * IMPACT_FACTORS.get('residuos_trat_preliminar_lixao', {}).get(impact_type, 0)

    # Remove categorias com valor zero
    return {k: v for k, v in category_impacts.items() if abs(v) > 1e-10}

def group_parameters_by_category(inputs):
    # Define as categorias e seus respectivos parâmetros
    categories = {
        # Emissões para água inclui todos os parâmetros de qualidade da água
        'Emissões para a água': [
            'fosforo_total', 'nitrogenio_total', 'bario', 'cobre', 'selenio',
            'zinco', 'tolueno', 'cromo', 'cadmio', 'chumbo', 'niquel'
        ],
        
        # Emissões para o solo inclui todos os parâmetros relacionados ao lodo
        'Emissões para o solo (Lodo)': [
            'lodo_fosforo', 'lodo_nitrogenio', 'lodo_arsenio', 'lodo_bario',
            'lodo_cadmio', 'lodo_chumbo', 'lodo_cobre', 'lodo_cromo',
            'lodo_molibdenio', 'lodo_niquel', 'lodo_estanho', 'lodo_zinco',
            'lodo_diclorobenzeno'
        ],
        
        # Emissões para o ar inclui gases e compostos voláteis
        'Emissões para o ar': [
            'metano', 'oxido_nitroso', 'nitrogenio_amoniacal', 'dioxido_carbono'
        ],
        
        # Resíduos inclui todos os tipos de disposição, incluindo ferti-irrigação
        'Resíduos': [
            'residuos_trat_preliminar_aterro', 'residuos_trat_preliminar_lixao',
            'lodo_aterro', 'lodo_lixao'
        ] + [f'ferti_irrigacao_{impact}' for impact in IMPACT_NAMES],  
        
        # Transportes inclui todos os impactos relacionados ao transporte
        'Transportes': [
            'transportes', 'transportes_quimicos'
        ],
        
        # Emissões evitadas inclui fatores que reduzem impactos
        'Emissões evitadas': [
            'eletricidade'
        ]
    }
    
    grouped_data = {}
    for category, params in categories.items():
        category_data = {param: inputs.get(param, 0) for param in params if inputs.get(param, 0) != 0}
        if category_data:
            grouped_data[category] = category_data
            
    return grouped_data

def create_category_graphs(grouped_data):
    graphs = []
    for category, data in grouped_data.items():
        if data:
            df = pd.DataFrame(list(data.items()), columns=['Parâmetro', 'Valor'])
            
            fig = px.bar(
                df,
                x='Parâmetro',
                y='Valor',
                title=f'{category}',
                labels={'Valor': 'Impacto'},
                color='Parâmetro'
            )
            
            fig.update_layout(
                xaxis_title="Parâmetro",
                yaxis_title="Valor",
                xaxis={'categoryorder':'total descending'},
                showlegend=False
            )
            
            graphs.append(fig)
    
    return graphs

def parse_scientific_notation(value):
    try:
        return float(value)
    except ValueError:
        return 0.0

def number_input_with_suggestion(label, value=0.0, step=0.1, key=None, selected_scenario='Somente UASB'):
    """
    Cria um campo de entrada com um botão de sugestão ao lado que atualiza o valor quando clicado
    """
    # Inicializa o estado da sessão para este campo específico, se ainda não existir
    if f"state_{key}" not in st.session_state:
        st.session_state[f"state_{key}"] = str(value)
    
    # Função para atualizar o valor quando o botão de sugestão for clicado
    def update_value():
        if key in SCENARIO_VALUES[selected_scenario]:
            st.session_state[f"state_{key}"] = str(SCENARIO_VALUES[selected_scenario][key])
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        value_input = st.text_input(
            label, 
            value=st.session_state[f"state_{key}"],
            key=f"input_{key}"
        )
        # Atualiza o estado da sessão quando o usuário digitar um novo valor
        st.session_state[f"state_{key}"] = value_input
        parsed_value = parse_scientific_notation(value_input)
    
    with col2:
        # Verifica se há um valor sugerido para este campo no cenário selecionado
        if key in SCENARIO_VALUES[selected_scenario]:
            suggested_value = SCENARIO_VALUES[selected_scenario][key]
            if st.button(f"Sugerir: {suggested_value:.2e}", key=f"btn_{key}", on_click=update_value):
                pass  # A ação é executada pelo on_click
    
    return parsed_value

def calculate_impacts(inputs):
    # Inicializa o dicionário de resultados com zero para cada categoria de impacto
    results = {impact: 0 for impact in IMPACT_NAMES}
    
    # Processamento geral para todos os inputs que têm fatores diretos
    for input_name, value in inputs.items():
        if input_name in IMPACT_FACTORS:
            for impact, factor in IMPACT_FACTORS[input_name].items():
                results[impact] += value * factor
    
    # Processamento específico para resíduos do tratamento preliminar
    if 'quantity' in inputs and 'destination' in inputs:
        # Seleciona os fatores corretos baseado no destino (aterro ou lixão)
        impact_key = 'residuos_trat_preliminar_aterro' if inputs['destination'] == 'Aterro Sanitário' else 'residuos_trat_preliminar_lixao'
        
        # Aplica os fatores de impacto dos resíduos
        for impact, factor in IMPACT_FACTORS[impact_key].items():
            results[impact] += inputs['quantity'] * factor
            
        # Adiciona impacto do transporte dos resíduos
        if 'ton_km_factor' in inputs and inputs['ton_km_factor'] > 0:
            for impact, factor in IMPACT_FACTORS['transportes'].items():
                results[impact] += inputs['ton_km_factor'] * factor
    
    # Processamento específico para disposição do lodo
    if 'disposicao_lodo' in inputs:
        # Caso 1: Disposição em Aterro
        if inputs['disposicao_lodo'] == 'Disposição em aterro':
            if 'quantidade_lodo' in inputs:
                # Aplica os fatores de impacto do lodo em aterro
                for impact, factor in IMPACT_FACTORS['lodo_aterro'].items():
                    results[impact] += inputs['quantidade_lodo'] * factor
                
                # Adiciona impacto do transporte do lodo
                if 'ton_km_factor_lodo' in inputs and inputs['ton_km_factor_lodo'] > 0:
                    for impact, factor in IMPACT_FACTORS['transportes'].items():
                        results[impact] += inputs['ton_km_factor_lodo'] * factor
        
        # Caso 2: Disposição em Lixão
        elif inputs['disposicao_lodo'] == 'Disposição em lixão':
            if 'quantidade_lodo' in inputs:
                # Aplica os fatores de impacto do lodo em lixão
                for impact, factor in IMPACT_FACTORS['lodo_lixao'].items():
                    results[impact] += inputs['quantidade_lodo'] * factor
                
                # Adiciona impacto do transporte do lodo
                if 'ton_km_factor_lodo' in inputs and inputs['ton_km_factor_lodo'] > 0:
                    for impact, factor in IMPACT_FACTORS['transportes'].items():
                        results[impact] += inputs['ton_km_factor_lodo'] * factor
        
        # Caso 3: Ferti-irrigação
        elif inputs['disposicao_lodo'] == 'Ferti-irrigação ou agricultura':
            # Lista de elementos que podem estar presentes no lodo
            elementos_lodo = [
                'arsenio', 'bario', 'cadmio', 'chumbo', 'cobre', 'cromo',
                'molibdenio', 'niquel', 'estanho', 'zinco', 'diclorobenzeno'
            ]
            
            # Processa cada elemento do lodo de ferti-irrigação
            for elemento in elementos_lodo:
                input_key = f'lodo_{elemento}'
                if input_key in inputs and inputs[input_key] > 0:
                    if elemento in IMPACT_FACTORS:
                        # Para cada elemento, aplica seus fatores de impacto
                        for impact, factor in IMPACT_FACTORS[elemento].items():
                            impact_value = inputs[input_key] * factor
                            results[impact] += impact_value
            
            # Processa fósforo e nitrogênio se presentes
            if 'lodo_fosforo' in inputs and inputs['lodo_fosforo'] > 0:
                if 'fosforo' in IMPACT_FACTORS:
                    for impact, factor in IMPACT_FACTORS['fosforo'].items():
                        results[impact] += inputs['lodo_fosforo'] * factor
            
            if 'lodo_nitrogenio' in inputs and inputs['lodo_nitrogenio'] > 0:
                if 'nitrogenio_amoniacal' in IMPACT_FACTORS:
                    for impact, factor in IMPACT_FACTORS['nitrogenio_amoniacal'].items():
                        results[impact] += inputs['lodo_nitrogenio'] * factor

    # Processamento do transporte de produtos químicos
    if 'transportes_quimicos' in inputs and inputs['transportes_quimicos'] > 0:
        for impact, factor in IMPACT_FACTORS['transportes'].items():
            results[impact] += inputs['transportes_quimicos'] * factor

    # Nova seção: Processamento do reaproveitamento de biogás
    if ('quantidade_biogas' in inputs and inputs['quantidade_biogas'] > 0):
        # Como a eficiência está fixa em 100%, a energia gerada é igual à quantidade de biogás
        energia_gerada = inputs['quantidade_biogas']
        # Aplica fatores negativos para emissões evitadas
        for impact, factor in IMPACT_FACTORS['eletricidade'].items():
            results[impact] += -1 * energia_gerada * factor
    
    return results
    
st.title('Avaliação do Ciclo de Vida para ETE')

# Permitir ao usuário selecionar um cenário de valores de referência
selected_scenario = st.sidebar.selectbox(
    "Selecione um cenário para valores de referência",
    ["Somente UASB", "UASB+FBP", "UASB+Wetland", "UASB+LP", "Reaproveitamento Biogás"]
)

# Passo 1: Processo de Tratamento
st.header('Passo 1: Processo de Tratamento')

# Tratamento Preliminar (deve ser obrigatório)
st.subheader('Tratamento Preliminar')
st.write('O tratamento preliminar é obrigatório.')

col1, col2 = st.columns(2)
with col1:
    distance = number_input_with_suggestion('Distância para o transporte de resíduos (Ida e Volta) (km)', value=0.0, step=0.1, key="distance", selected_scenario=selected_scenario)
    quantity = number_input_with_suggestion('Quantidade de resíduos (ton/m³)', value=0.0, step=0.001, key="quantity", selected_scenario=selected_scenario)
with col2:
    destination = st.selectbox('Destino dos resíduos', ['Lixão', 'Aterro Sanitário'])

st.info('A quantidade é multiplicada pelo km, isso dá o fator em ton.km')
st.info('Os impactos em cada categoria são diferentes de acordo com a destinação.')

ton_km_factor = distance * quantity
st.write(f'Fator ton.km: {ton_km_factor:.2e}')

# UASB (deve ser pré-selecionado segundo o fernando)
st.subheader('Tratamento UASB')
st.write('O tratamento UASB está pré-selecionado.')

# Processos adicionais 
st.subheader('Processos Adicionais')
additional_processes = st.multiselect(
    'Selecione o(s) Processo(s) Adicional(is)',
    ['Somente UASB',
     'Wetland de Fluxo Vertical', 
     'Filtro Biológico percolador + Decantador Segundario', 
     'Lagoa de Polimento']
)

# Nova seção para produtos químicos
st.header('Produtos Químicos')
st.write('Selecione os produtos químicos utilizados no tratamento:')

# Expandir/colapsar seção de produtos químicos
show_chemicals = st.checkbox('Mostrar produtos químicos', value=True)

inputs = {}  # Inicializa o dicionário de inputs aqui

if show_chemicals:
    col1, col2, col3 = st.columns(3)
    
    with col1:
        inputs['cloreto_ferrico'] = number_input_with_suggestion('Cloreto Férrico (kg/m³)', value=0.0, step=0.001, key="cloreto_ferrico", selected_scenario=selected_scenario)
        inputs['policloreto_aluminio'] = number_input_with_suggestion('Policloreto de Alumínio (kg/m³)', value=0.0, step=0.001, key="policloreto_aluminio", selected_scenario=selected_scenario)
        inputs['sulfato_aluminio'] = number_input_with_suggestion('Sulfato de Alumínio (kg/m³)', value=0.0, step=0.001, key="sulfato_aluminio", selected_scenario=selected_scenario)
        inputs['acido_paracetico'] = number_input_with_suggestion('Ácido Paracético (kg/m³)', value=0.0, step=0.001, key="acido_paracetico", selected_scenario=selected_scenario)
    
    with col2:
        inputs['hipoclorito_sodio'] = number_input_with_suggestion('Hipoclorito de Sódio (kg/m³)', value=0.0, step=0.001, key="hipoclorito_sodio", selected_scenario=selected_scenario)
        inputs['peroxido_hidrogenio'] = number_input_with_suggestion('Peróxido de Hidrogênio (kg/m³)', value=0.0, step=0.001, key="peroxido_hidrogenio", selected_scenario=selected_scenario)
        inputs['cal'] = number_input_with_suggestion('Cal (kg/m³)', value=0.0, step=0.001, key="cal", selected_scenario=selected_scenario)
        inputs['hidroxido_sodio'] = number_input_with_suggestion('Hidróxido de Sódio (kg/m³)', value=0.0, step=0.001, key="hidroxido_sodio", selected_scenario=selected_scenario)
    
    with col3:
        inputs['nitrato_calcio'] = number_input_with_suggestion('Nitrato de Cálcio (kg/m³)', value=0.0, step=0.001, key="nitrato_calcio", selected_scenario=selected_scenario)
        inputs['sulfato_sodio'] = number_input_with_suggestion('Sulfato de Sódio (kg/m³)', value=0.0, step=0.001, key="sulfato_sodio", selected_scenario=selected_scenario)
        inputs['sulfato_ferro'] = number_input_with_suggestion('Sulfato de Ferro (kg/m³)', value=0.0, step=0.001, key="sulfato_ferro", selected_scenario=selected_scenario)
        inputs['transportes_quimicos'] = number_input_with_suggestion('Transporte de Químicos (kg.km)', value=0.0, step=0.1, key="transportes_quimicos", selected_scenario=selected_scenario)
    
    st.write('Uso da Terra')
    inputs['uso_terra'] = number_input_with_suggestion('Área utilizada (m²)', value=0.0, step=0.1, key="uso_terra", selected_scenario=selected_scenario)

# Passo 2: Inventário do ciclo de vida
st.header('Passo 2: Inventário do ciclo de vida')

st.subheader('Consumo de Energia')
inputs['eletricidade'] = number_input_with_suggestion('Eletricidade (kWh/m³)', value=0.0, step=0.1, key="eletricidade", selected_scenario=selected_scenario)

st.subheader('Emissões para a Água')
inputs['fosforo_total'] = number_input_with_suggestion('Fósforo Total (kg/m³)', value=0.0, step=0.001, key="fosforo_total", selected_scenario=selected_scenario)
inputs['nitrogenio_total'] = number_input_with_suggestion('Nitrogênio Total (kg/m³)', value=0.0, step=0.001, key="nitrogenio_total", selected_scenario=selected_scenario)

st.write("Os outros parâmetros são opcionais. Clique em 'Mostrar mais' para exibi-los.")
if st.checkbox('Mostrar mais'):
    optional_params = [
        ('bario', 'Bário'),
        ('cobre', 'Cobre'),
        ('selenio', 'Selênio'),
        ('zinco', 'Zinco'),
        ('tolueno', 'Tolueno'),
        ('cromo', 'Cromo'),
        ('cadmio', 'Cádmio'),
        ('chumbo', 'Chumbo'),
        ('niquel', 'Níquel')
    ]
    
    for param_key, param_display in optional_params:
        inputs[param_key] = number_input_with_suggestion(
            f'{param_display} (kg/m³)', 
            value=0.0, 
            step=0.0001, 
            key=param_key,
            selected_scenario=selected_scenario
        )

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
        distancia_lodo = number_input_with_suggestion('Distância para o transporte do lodo (Ida e Volta) (km)', value=0.0, step=0.1, key="distancia_lodo", selected_scenario=selected_scenario)
    with col2:
        quantidade_lodo = number_input_with_suggestion('Quantidade de lodo (ton/m³)', value=0.0, step=0.001, key="quantidade_lodo", selected_scenario=selected_scenario)
    
    ton_km_factor_lodo = distancia_lodo * quantidade_lodo
    st.write(f'Fator ton.km para o lodo: {ton_km_factor_lodo:.2e}')

elif disposicao_lodo == 'Ferti-irrigação ou agricultura':
    st.subheader('Composição do Lodo')
    
    col1, col2 = st.columns(2)
    with col1:
        inputs['lodo_fosforo'] = number_input_with_suggestion('Fósforo (kg/m³)', value=0.0, step=0.001, key="lodo_fosforo", selected_scenario=selected_scenario)
    with col2:
        inputs['lodo_nitrogenio'] = number_input_with_suggestion('Nitrogênio Amoniacal (kg/m³)', value=0.0, step=0.001, key="lodo_nitrogenio", selected_scenario=selected_scenario)
    
    st.write("Elementos adicionais (opcionais)")
    if st.checkbox('Mostrar elementos do lodo'):
        # Lista de elementos usando nomes padronizados (sem acentos, minúsculos) e seus nomes de exibição
        elementos_adicionais = [
            ('arsenio', 'Arsênio'),
            ('bario', 'Bário'),
            ('cadmio', 'Cádmio'),
            ('chumbo', 'Chumbo'),
            ('cobre', 'Cobre'),
            ('cromo', 'Cromo'),
            ('molibdenio', 'Molibdênio'),
            ('niquel', 'Níquel'),
            ('estanho', 'Estanho'),
            ('zinco', 'Zinco'),
            ('diclorobenzeno', 'Diclorobenzeno')
        ]
        
        # Para cada elemento, criamos um campo de entrada
        for elemento_key, elemento_display in elementos_adicionais:
            # Criamos a chave do input com prefixo 'lodo_'
            input_key = f'lodo_{elemento_key}'
            # Criamos o campo de entrada com o botão de sugestão
            inputs[input_key] = number_input_with_suggestion(
                f'Lodo - {elemento_display} (kg/m³)', 
                value=0.0, 
                step=0.0001,
                key=input_key,
                selected_scenario=selected_scenario
            )
    
# Passo 4: Queima de Biogás
st.header('Passo 4: Queima de Biogás')

tipo_queimador = st.selectbox(
    'Escolha o tipo de queimador',
    ['Queimador aberto', 'Queimador fechado com reaproveitamento energético']
)

if tipo_queimador == 'Queimador fechado com reaproveitamento energético':
    st.subheader('Emissões do Queimador Fechado')
    inputs['dioxido_carbono'] = number_input_with_suggestion('Dióxido de Carbono (kg/m³)', value=0.0, step=0.001, key="dioxido_carbono", selected_scenario=selected_scenario)
    
    # Passo 5 aparece automaticamente quando o queimador fechado é selecionado
    st.header('Passo 5: Reaproveitamento Biogás')
    st.write('Como você selecionou o queimador fechado com reaproveitamento energético, preencha os dados do reaproveitamento de biogás para calcular as emissões evitadas.')
    st.info('A eficiência de conversão energética está definida em 100%.')
    
    # Agora apenas um input para a quantidade de biogás
    inputs['quantidade_biogas'] = number_input_with_suggestion(
        'Eletricidade (kWh.m−3)', 
        value=0.0, 
        step=0.1,
        key="quantidade_biogas",
        selected_scenario="Reaproveitamento Biogás"  # Usando um cenário específico para este campo
    )
    
    # Definimos a eficiência como 100% automaticamente
    inputs['eficiencia_conversao'] = 100.0

elif tipo_queimador == 'Queimador aberto':
    st.subheader('Emissões do Queimador Aberto')
    
    col1, col2 = st.columns(2)
    with col1:
        inputs['metano'] = number_input_with_suggestion('Metano (kg/m³)', value=0.0, step=0.001, key="metano", selected_scenario=selected_scenario)
        inputs['dioxido_carbono'] = number_input_with_suggestion('Dióxido de Carbono (kg/m³)', value=0.0, step=0.001, key="dioxido_carbono", selected_scenario=selected_scenario)
    with col2:
        inputs['oxido_nitroso'] = number_input_with_suggestion('Óxido Nitroso (kg/m³)', value=0.0, step=0.001, key="oxido_nitroso", selected_scenario=selected_scenario)

# Coloque isso antes do botão 'Calcular Impactos'
# Adicione esta seção antes do botão 'Calcular Impactos'
st.markdown("---")
st.subheader("Opções de Visualização")

# Criamos duas colunas para organizar os controles
viz_col1, viz_col2 = st.columns(2)

with viz_col1:
    st.write("Selecione as categorias de impacto para visualizar:")
    # Criamos checkboxes para todas as categorias de impacto
    impact_options = {}
    for impact in IMPACT_NAMES.keys():
        # Por padrão, 'Uso da Terra' vem desmarcado, os outros vêm marcados
        default_value = impact != 'Uso da Terra'
        impact_options[impact] = st.checkbox(IMPACT_NAMES[impact], value=default_value, key=f"check_{impact}")

with viz_col2:
    st.subheader("Análise Detalhada")
    # Seletor de impacto para a visualização detalhada
    impact_selected = st.selectbox(
        'Selecione o tipo de impacto para visualizar detalhes:',
        ['Ecotoxidade de Água Doce', 'Eutrofização de Água Doce', 'Aquecimento Global', 
         'Uso da Terra', 'Ecotoxidade Marinha', 'Eutrofização Marinha', 'Ecotoxidade Terrestre']
    )

# Botão para calcular os impactos
if st.button('Calcular Impactos'):
    # Primeiro, adicionamos todas as informações do tratamento preliminar ao dicionário inputs
    inputs['quantity'] = quantity
    inputs['destination'] = destination
    inputs['ton_km_factor'] = ton_km_factor
    
    # Adicionamos as informações do lodo dependendo do tipo de disposição
    if disposicao_lodo in ['Disposição em aterro', 'Disposição em lixão']:
        # Para aterro e lixão, precisamos da disposição, quantidade e transporte
        inputs['disposicao_lodo'] = disposicao_lodo
        inputs['quantidade_lodo'] = quantidade_lodo
        inputs['ton_km_factor_lodo'] = ton_km_factor_lodo
    
    elif disposicao_lodo == 'Ferti-irrigação ou agricultura':
        # Para ferti-irrigação, só precisamos registrar o tipo de disposição
        # Os elementos já foram adicionados ao inputs quando foram preenchidos
        inputs['disposicao_lodo'] = disposicao_lodo
    
    # Adicionamos as informações do queimador
    inputs['tipo_queimador'] = tipo_queimador
    
    # Calculamos os impactos usando nossa função modificada
    results = calculate_impacts(inputs)
    
    # Filtramos os resultados com base nas categorias selecionadas
    selected_impacts = [impact for impact, selected in impact_options.items() if selected]
    filtered_results = {k: v for k, v in results.items() if k in selected_impacts}
    
    # Criamos DataFrame com apenas as categorias selecionadas
    df_results = pd.DataFrame(
        list(filtered_results.items()), 
        columns=['Categoria de Impacto', 'Valor']
    )
    
    # Mapeamos os nomes das categorias para seus nomes completos com unidades
    df_results['Categoria de Impacto'] = df_results['Categoria de Impacto'].map(IMPACT_NAMES)
    
    # Garantimos que todos os valores são numéricos
    df_results['Valor'] = pd.to_numeric(df_results['Valor'], errors='coerce')
    
    # Verificamos se temos dados para mostrar
    if len(df_results) > 0:
        # Mostramos o cabeçalho dos resultados
        st.header('Resultados')
        
        # Criamos o gráfico principal com um estilo visual melhorado
        fig = px.bar(
            df_results, 
            x='Categoria de Impacto', 
            y='Valor',
            title='Impactos Ambientais por Categoria',
            labels={'Valor': 'Valor do Impacto'},
            color='Categoria de Impacto',
            color_discrete_sequence=px.colors.qualitative.Bold,  # Cores mais vibrantes
            template="plotly_white"  # Fundo branco com linhas de grade suaves
        )
        
        # Personalizamos o layout do gráfico principal
        fig.update_layout(
            xaxis_title="Categoria de Impacto",
            yaxis_title="Valor do Impacto",
            xaxis={'categoryorder':'total descending'},
            showlegend=False,
            height=500,
            margin=dict(t=50, b=100, l=100, r=30),
            title_font=dict(size=20, family="Arial", color="#333333"),
            font=dict(family="Arial", size=14),
            xaxis_tickangle=-45,  # Ângulo dos rótulos do eixo x para melhor legibilidade
            plot_bgcolor='white',  # Fundo branco
            bargap=0.3  # Espaçamento entre barras
        )
        
        # Adiciona linhas de grade horizontais suaves para facilitar a leitura dos valores
        fig.update_yaxes(
            showgrid=True,
            gridcolor='lightgray',
            gridwidth=0.5
        )
        
        # Remove linhas de grade verticais para um visual mais limpo
        fig.update_xaxes(
            showgrid=False
        )
        
        # Mostramos o gráfico principal
        st.plotly_chart(fig, use_container_width=True)  # Utiliza a largura total do container
        
        # Análise Detalhada por Categoria
        category_impacts = calculate_impacts_by_category(inputs, impact_selected)
        
        if category_impacts:
            # Criamos tabela de contribuições por categoria (apenas uma vez)
            st.subheader("Tabela de Contribuições por Categoria")
            df_categories_all = pd.DataFrame({
                'Categoria': ['Consumo de Energia', 'Produtos Químicos', 'Transportes', 
                             'Emissões para a Água', 'Emissões Atmosféricas', 
                             'Disposição de Lodo', 'Disposição de Resíduos'],
                'Impacto': [category_impacts.get('Consumo de Energia', 0),
                           category_impacts.get('Produtos Químicos', 0),
                           category_impacts.get('Transportes', 0),
                           category_impacts.get('Emissões para a Água', 0),
                           category_impacts.get('Emissões Atmosféricas', 0),
                           category_impacts.get('Disposição de Lodo', 0),
                           category_impacts.get('Disposição de Resíduos', 0)]
            })
            st.table(df_categories_all)
    
            # Força exibição de todas as categorias no gráfico
            df_categories = pd.DataFrame(
                [{'Categoria': cat, 'Impacto': category_impacts.get(cat, 0)} 
                 for cat in ['Consumo de Energia', 'Produtos Químicos', 'Transportes', 
                            'Emissões para a Água', 'Emissões Atmosféricas', 
                            'Disposição de Lodo', 'Disposição de Resíduos']]
            )
            
            # Cria o gráfico de categorias com estilo melhorado
            fig_categories = px.bar(
                df_categories,
                x='Categoria',
                y='Impacto',
                title=f'Contribuição por Categoria para {impact_selected}',
                labels={'Impacto': IMPACT_NAMES[impact_selected]},
                color='Categoria',
                color_discrete_sequence=px.colors.qualitative.Bold,
                template="plotly_white"
            )
            
            fig_categories.update_layout(
                xaxis_title="Categoria",
                yaxis_title=f"Impacto ({IMPACT_NAMES[impact_selected].split('(')[1].strip(')')})",
                xaxis={'categoryorder':'total descending'},
                xaxis_tickangle=-45,
                showlegend=False,
                height=500,
                margin=dict(t=50, b=160, l=100, r=30),
                title_font=dict(size=18, family="Arial", color="#333333"),
                font=dict(family="Arial", size=14),
                plot_bgcolor='white',
                bargap=0.3
            )
            
            # Adiciona linhas de grade horizontais
            fig_categories.update_yaxes(
                showgrid=True,
                gridcolor='lightgray',
                gridwidth=0.5
            )
            
            # Remove linhas de grade verticais
            fig_categories.update_xaxes(
                showgrid=False
            )
            
            st.plotly_chart(fig_categories, use_container_width=True)
            st.success("Análise detalhada concluída!")
        else:
            st.warning("Não há dados suficientes para mostrar o gráfico detalhado para esta categoria de impacto.")
        
        # Mostramos a tabela com todos os resultados
        st.table(df_results)
    else:
        st.warning("Nenhuma categoria de impacto selecionada para visualização.")
