import streamlit as st
import pandas as pd
import plotly.express as px

# Valores de referência da tabela para cada cenário #### Tenho que manter o fluxograma de Variaveis, lembrese do mind map da cronstrução do modelo
SCENARIO_VALUES = {
    'UASB Only': {
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
    'Biogas Reuse': {
        'eletricidade': 1.92e-02,
        'dioxido_carbono': 4.08e-02,
        'quantidade_biogas': 4.17e-01
    }
}

# Fatores para impactos # lemrbra doq o Fernando disse sobre os fatores de multiplicação
IMPACT_FACTORS = {
    'eletricidade': {
        'Freshwater Ecotoxicity': 0.00097,
        'Freshwater Eutrophication': 0.00000,
        'Global Warming': 0.25056,
        'Land Use': 0.00142,
        'Marine Ecotoxicity': 0.00144,
        'Marine Eutrophication': 0.00,
        'Terrestrial Ecotoxicity': 0.28,
    },
    'cloreto_ferrico': {
        'Freshwater Ecotoxicity': 0.06756,
        'Freshwater Eutrophication': 1.09053,
        'Global Warming': 0.05594,
        'Land Use': 0.09093,
        'Marine Ecotoxicity': 0.00002,
        'Marine Eutrophication': 0.00,
        'Terrestrial Ecotoxicity': 5.87,
    },
    'sulfato_ferro': {
        'Freshwater Ecotoxicity': 0.02592,
        'Freshwater Eutrophication': 0.27481,
        'Global Warming': 0.02132,
        'Land Use': 0.03479,
        'Marine Ecotoxicity': 0.00001,
        'Marine Eutrophication': 0.00,
        'Terrestrial Ecotoxicity': 0.00,
    },
    'policloreto_aluminio': {
        'Freshwater Ecotoxicity': 0.11691,
        'Freshwater Eutrophication': 0.00051,
        'Global Warming': 1.87017,
        'Land Use': -0.04174,
        'Marine Ecotoxicity': 0.16189,
        'Marine Eutrophication': 0.00,
        'Terrestrial Ecotoxicity': 10.55,
    },
    'sulfato_aluminio': {
        'Freshwater Ecotoxicity': 0.06946,
        'Freshwater Eutrophication': 0.00034,
        'Global Warming': 0.35950,
        'Land Use': 0.02799,
        'Marine Ecotoxicity': 0.09619,
        'Marine Eutrophication': 0.00,
        'Terrestrial Ecotoxicity': 6.44,
    },
    'hipoclorito_sodio': {
        'Freshwater Ecotoxicity': 0.07766,
        'Freshwater Eutrophication': 0.00026,
        'Global Warming': 3.00893,
        'Land Use': 0.07189,
        'Marine Ecotoxicity': 0.10527,
        'Marine Eutrophication': 0.00,
        'Terrestrial Ecotoxicity': 15.28,
    },
    'acido_paracetico': {
        'Freshwater Ecotoxicity': -0.01571,
        'Freshwater Eutrophication': 0.00069,
        'Global Warming': 1.15457,
        'Land Use': -0.03251,
        'Marine Ecotoxicity': -0.01050,
        'Marine Eutrophication': 0.00,
        'Terrestrial Ecotoxicity': 2.73,
    },
    'peroxido_hidrogenio': {
        'Freshwater Ecotoxicity': 0.06871,
        'Freshwater Eutrophication': 0.00037,
        'Global Warming': 1.56913,
        'Land Use': 0.03429,
        'Marine Ecotoxicity': 0.09324,
        'Marine Eutrophication': 0.00,
        'Terrestrial Ecotoxicity': 7.48,
    },
    'cal': {
        'Freshwater Ecotoxicity': 0.00106,
        'Freshwater Eutrophication': 0.00001,
        'Global Warming': 0.96049,
        'Land Use': 0.01615,
        'Marine Ecotoxicity': 0.00250,
        'Marine Eutrophication': 0.00,
        'Terrestrial Ecotoxicity': 1.46,
    },
    'hidroxido_sodio': {
        'Freshwater Ecotoxicity': 0.11233,
        'Freshwater Eutrophication': 0.00279,
        'Global Warming': 1.33577,
        'Land Use': 0.52521,
        'Marine Ecotoxicity': 0.15473,
        'Marine Eutrophication': 0.00,
        'Terrestrial Ecotoxicity': 12.12,
    },
    'nitrato_calcio': {
        'Freshwater Ecotoxicity': 0.09145,
        'Freshwater Eutrophication': 0.00039,
        'Global Warming': 2.93506,
        'Land Use': 0.05360,
        'Marine Ecotoxicity': 0.12332,
        'Marine Eutrophication': 0.00,
        'Terrestrial Ecotoxicity': 18.11,
    },
    'sulfato_sodio': {
        'Freshwater Ecotoxicity': 0.04309,
        'Freshwater Eutrophication': 0.00016,
        'Global Warming': 0.71981,
        'Land Use': 0.06517,
        'Marine Ecotoxicity': 0.05961,
        'Marine Eutrophication': 0.00,
        'Terrestrial Ecotoxicity': 7.72,
    },
    'transportes': {
        'Freshwater Ecotoxicity': 0.01729,
        'Freshwater Eutrophication': 0.00008,
        'Global Warming': 0.59323,
        'Land Use': 0.01975,
        'Marine Ecotoxicity': 0.02558,
        'Marine Eutrophication': 0.00,
        'Terrestrial Ecotoxicity': 6.21,
    },
    'uso_terra': {
        'Land Use': 1.00,
    },
    'fosforo_total': {
        'Freshwater Eutrophication': 1.0000,
    },
    'nitrogenio_total': {
        'Marine Eutrophication': 0.297,
    },
    'bario': {
        'Freshwater Ecotoxicity': 1.5100,
        'Marine Ecotoxicity': 3.47,
        'Terrestrial Ecotoxicity': 6.42e-17,
    },
    'cobre': {
        'Freshwater Ecotoxicity': 6.17,
        'Marine Ecotoxicity': 4.19,
        'Terrestrial Ecotoxicity': 2.24e-16,
    },
    'selenio': {
        'Freshwater Ecotoxicity': 15.3000,
        'Marine Ecotoxicity': 19.1,
        'Terrestrial Ecotoxicity': 8.79e-16,
    },
    'zinco': {
        'Freshwater Ecotoxicity': 5.14,
        'Marine Ecotoxicity': 4.29,
        'Terrestrial Ecotoxicity': 2.15e-16,
    },
    'tolueno': {
        'Freshwater Ecotoxicity': 0.1390,
        'Marine Ecotoxicity': 0.00276,
        'Terrestrial Ecotoxicity': 0.0301,
    },
    'cromo': {
        'Freshwater Ecotoxicity': 0.8530,
        'Marine Ecotoxicity': 0.543,
        'Terrestrial Ecotoxicity': 3.94e-17,
    },
    'cadmio': {
        'Freshwater Ecotoxicity': 2.0400,
        'Marine Ecotoxicity': 1.36,
        'Terrestrial Ecotoxicity': 7.04e-17,
    },
    'chumbo': {
        'Freshwater Ecotoxicity': 0.0074,
        'Marine Ecotoxicity': 0.0039,
        'Terrestrial Ecotoxicity': 2.03e-17,
    },
    'niquel': {
        'Freshwater Ecotoxicity': 3.17,
        'Marine Ecotoxicity': 2.29,
        'Terrestrial Ecotoxicity': 1.35e-16,
    },
    'fosforo': {
        'Freshwater Eutrophication': 0.1000,
    },
    'nitrogenio_amoniacal': {
        'Freshwater Eutrophication': 0.1000,
    },
    'arsenio': {
        'Freshwater Ecotoxicity': 1.6300,
        'Marine Ecotoxicity': 1.33,
        'Terrestrial Ecotoxicity': 6.42e-17,
    },
    'molibdenio': {
        'Freshwater Ecotoxicity': 0.1540,
        'Marine Ecotoxicity': 0.13,
        'Terrestrial Ecotoxicity': 5.89e-18,
    },
    'estanho': {
        'Freshwater Ecotoxicity': 0.0696,
        'Marine Ecotoxicity': 0.0444,
    },
    'diclorobenzeno': {
        'Freshwater Ecotoxicity': 0.0320,
        'Marine Ecotoxicity': 0.0816,
        'Terrestrial Ecotoxicity': 1.00,
    },
    'metano': {
        'Global Warming': 34.0,
    },
    'oxido_nitroso': {
        'Global Warming': 298.0,
    },
    'dioxido_carbono': {
        'Global Warming': 1.00,
    },
    'residuos_trat_preliminar_aterro': {
        'Freshwater Ecotoxicity': 3.09e-04,
        'Freshwater Eutrophication': 1.44e-03,
        'Global Warming': 8.71e-02,
        'Land Use': 7.83e-04,
        'Marine Ecotoxicity': 5.01e-04,
        'Marine Eutrophication': 4.69e-04,
        'Terrestrial Ecotoxicity': 1.08e-01,
    },
    'residuos_trat_preliminar_lixao': {
        'Freshwater Ecotoxicity': 4.80e-01,
        'Freshwater Eutrophication': 7.35e-05,
        'Global Warming': 9.84e-01,
        'Land Use': 0.0026,
        'Marine Ecotoxicity': 6.35e-01,
        'Marine Eutrophication': 8.96e-04,
        'Terrestrial Ecotoxicity': 3.03e-03,
    },
    'lodo_aterro': {
        'Freshwater Ecotoxicity': 3.09e-04,
        'Freshwater Eutrophication': 1.44e-03,
        'Global Warming': 8.71e-02,
        'Land Use': 7.83e-04,
        'Marine Ecotoxicity': 5.01e-04,
        'Marine Eutrophication': 4.69e-04,
        'Terrestrial Ecotoxicity': 1.08e-01,
    },
    'lodo_lixao': {
        'Freshwater Ecotoxicity': 4.80e-01,
        'Freshwater Eutrophication': 7.35e-05,
        'Global Warming': 9.84e-01,
        'Land Use': 0.0026,
        'Marine Ecotoxicity': 6.35e-01,
        'Marine Eutrophication': 8.96e-04,
        'Terrestrial Ecotoxicity': 3.03e-03,
    },
}

IMPACT_NAMES = {
    'Freshwater Ecotoxicity': "Freshwater Ecotoxicity (kg 1,4-DCB)",
    'Freshwater Eutrophication': "Freshwater Eutrophication (kg P eq)",
    'Global Warming': "Global Warming (kg CO2 eq)",
    'Land Use': "Land Use (m2a crop eq)",
    'Marine Ecotoxicity': "Marine Ecotoxicity (kg 1,4-DCB)",
    'Marine Eutrophication': "Marine Eutrophication (kg N eq)",
    'Terrestrial Ecotoxicity': "Terrestrial Ecotoxicity (kg 1,4-DCB)",
}

def format_number_8f(x):
    """Format number to 8 decimal places or scientific notation"""
    if abs(x) < 0.0001 or abs(x) >= 1000000:
        return "{:.8e}".format(x)
    else:
        return "{:.8f}".format(x)

# Adicione as novas funções aqui
def calculate_impacts_by_category(inputs, impact_type):
    category_impacts = {
        'Energy Consumption': 0,
        'Chemical Products': 0,
        'Transportation': 0,
        'Water Emissions': 0,
        'Atmospheric Emissions': 0,
        'Sludge Disposal': 0,
        'Waste Disposal': 0
    }
    
    # Produtos Químicos
    chemical_products = ['cloreto_ferrico', 'sulfato_ferro', 'policloreto_aluminio', 
                        'sulfato_aluminio', 'hipoclorito_sodio', 'acido_paracetico',
                        'peroxido_hidrogenio', 'cal', 'hidroxido_sodio', 'nitrato_calcio',
                        'sulfato_sodio']
    for product in chemical_products:
        if product in inputs:
            category_impacts['Chemical Products'] += inputs[product] * IMPACT_FACTORS.get(product, {}).get(impact_type, 0)

    # Emissões para a Água
    water_emissions = ['fosforo_total', 'nitrogenio_total', 'bario', 'cobre', 'selenio', 
                      'zinco', 'tolueno', 'cromo', 'cadmio', 'chumbo', 'niquel']
    for emission in water_emissions:
        if emission in inputs:
            category_impacts['Water Emissions'] += inputs[emission] * IMPACT_FACTORS.get(emission, {}).get(impact_type, 0)

    # Emissões Atmosféricas
    if 'metano' in inputs:
        category_impacts['Atmospheric Emissions'] += inputs['metano'] * IMPACT_FACTORS.get('metano', {}).get(impact_type, 0)
    if 'dioxido_carbono' in inputs:
        category_impacts['Atmospheric Emissions'] += inputs['dioxido_carbono'] * IMPACT_FACTORS.get('dioxido_carbono', {}).get(impact_type, 0)
    if 'oxido_nitroso' in inputs:
        category_impacts['Atmospheric Emissions'] += inputs['oxido_nitroso'] * IMPACT_FACTORS.get('oxido_nitroso', {}).get(impact_type, 0)

    # Consumo de Energia
    if 'eletricidade' in inputs:
        category_impacts['Energy Consumption'] = inputs['eletricidade'] * IMPACT_FACTORS.get('eletricidade', {}).get(impact_type, 0)

    # Transportes
    if 'ton_km_factor' in inputs:
        category_impacts['Transportation'] += inputs['ton_km_factor'] * IMPACT_FACTORS.get('transportes', {}).get(impact_type, 0)
    if 'ton_km_factor_lodo' in inputs:
        category_impacts['Transportation'] += inputs['ton_km_factor_lodo'] * IMPACT_FACTORS.get('transportes', {}).get(impact_type, 0)
    if 'transportes_quimicos' in inputs:
        category_impacts['Transportation'] += inputs['transportes_quimicos'] * IMPACT_FACTORS.get('transportes', {}).get(impact_type, 0)

    # Disposição de Lodo
    if 'quantidade_lodo' in inputs and 'disposicao_lodo' in inputs:
        if inputs['disposicao_lodo'] == 'Landfill disposal':
            category_impacts['Sludge Disposal'] = inputs['quantidade_lodo'] * IMPACT_FACTORS.get('lodo_aterro', {}).get(impact_type, 0)
        elif inputs['disposicao_lodo'] == 'Dump disposal':
            category_impacts['Sludge Disposal'] = inputs['quantidade_lodo'] * IMPACT_FACTORS.get('lodo_lixao', {}).get(impact_type, 0)

    # Disposição de Resíduos
    if 'quantity' in inputs and 'destination' in inputs:
        if inputs['destination'] == 'Sanitary Landfill':
            category_impacts['Waste Disposal'] = inputs['quantity'] * IMPACT_FACTORS.get('residuos_trat_preliminar_aterro', {}).get(impact_type, 0)
        else:
            category_impacts['Waste Disposal'] = inputs['quantity'] * IMPACT_FACTORS.get('residuos_trat_preliminar_lixao', {}).get(impact_type, 0)

    # Remove categorias com valor zero
    return {k: v for k, v in category_impacts.items() if abs(v) > 1e-10}

def group_parameters_by_category(inputs):
    # Define as categorias e seus respectivos parâmetros
    categories = {
        # Emissões para água inclui todos os parâmetros de qualidade da água
        'Water emissions': [
            'fosforo_total', 'nitrogenio_total', 'bario', 'cobre', 'selenio',
            'zinco', 'tolueno', 'cromo', 'cadmio', 'chumbo', 'niquel'
        ],
        
        # Emissões para o solo inclui todos os parâmetros relacionados ao lodo
        'Soil emissions (Sludge)': [
            'lodo_fosforo', 'lodo_nitrogenio', 'lodo_arsenio', 'lodo_bario',
            'lodo_cadmio', 'lodo_chumbo', 'lodo_cobre', 'lodo_cromo',
            'lodo_molibdenio', 'lodo_niquel', 'lodo_estanho', 'lodo_zinco',
            'lodo_diclorobenzeno'
        ],
        
        # Emissões para o ar inclui gases e compostos voláteis
        'Air emissions': [
            'metano', 'oxido_nitroso', 'nitrogenio_amoniacal', 'dioxido_carbono'
        ],
        
        # Resíduos inclui todos os tipos de disposição, incluindo ferti-irrigação
        'Waste': [
            'residuos_trat_preliminar_aterro', 'residuos_trat_preliminar_lixao',
            'lodo_aterro', 'lodo_lixao'
        ] + [f'ferti_irrigacao_{impact}' for impact in IMPACT_NAMES],  
        
        # Transportes inclui todos os impactos relacionados ao transporte
        'Transportation': [
            'transportes', 'transportes_quimicos'
        ],
        
        # Emissões evitadas inclui fatores que reduzem impactos
        'Avoided emissions': [
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
            df = pd.DataFrame(list(data.items()), columns=['Parameter', 'Value'])
            
            fig = px.bar(
                df,
                x='Parameter',
                y='Value',
                title=f'{category}',
                labels={'Value': 'Impact'},
                color='Parameter'
            )
            
            fig.update_layout(
                xaxis_title="Parameter",
                yaxis_title="Value",
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

def number_input_with_suggestion(label, value=0.0, step=0.1, key=None, selected_scenario='UASB Only'):
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
            if st.button(f"Suggest: {suggested_value:.2e}", key=f"btn_{key}", on_click=update_value):
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
        impact_key = 'residuos_trat_preliminar_aterro' if inputs['destination'] == 'Sanitary Landfill' else 'residuos_trat_preliminar_lixao'
        
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
        if inputs['disposicao_lodo'] == 'Landfill disposal':
            if 'quantidade_lodo' in inputs:
                # Aplica os fatores de impacto do lodo em aterro
                for impact, factor in IMPACT_FACTORS['lodo_aterro'].items():
                    results[impact] += inputs['quantidade_lodo'] * factor
                
                # Adiciona impacto do transporte do lodo
                if 'ton_km_factor_lodo' in inputs and inputs['ton_km_factor_lodo'] > 0:
                    for impact, factor in IMPACT_FACTORS['transportes'].items():
                        results[impact] += inputs['ton_km_factor_lodo'] * factor
        
        # Caso 2: Disposição em Lixão
        elif inputs['disposicao_lodo'] == 'Dump disposal':
            if 'quantidade_lodo' in inputs:
                # Aplica os fatores de impacto do lodo em lixão
                for impact, factor in IMPACT_FACTORS['lodo_lixao'].items():
                    results[impact] += inputs['quantidade_lodo'] * factor
                
                # Adiciona impacto do transporte do lodo
                if 'ton_km_factor_lodo' in inputs and inputs['ton_km_factor_lodo'] > 0:
                    for impact, factor in IMPACT_FACTORS['transportes'].items():
                        results[impact] += inputs['ton_km_factor_lodo'] * factor
        
        # Caso 3: Ferti-irrigação
        elif inputs['disposicao_lodo'] == 'Fertigation or agriculture':
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
    
st.title('FastLCA')  # Título mantido em inglês

# Permitir ao usuário selecionar um cenário de valores de referência
selected_scenario = st.sidebar.selectbox(
    "Select a reference values scenario",
    ["UASB Only", "UASB+FBP", "UASB+Wetland", "UASB+LP", "Biogas Reuse"]
)

# Passo 1: Processo de Tratamento
st.header('Step 1: Treatment Process')

# Tratamento Preliminar (obrigatório)
st.subheader('Preliminary Treatment')
st.write('Preliminary treatment is mandatory.')

col1, col2 = st.columns(2)
with col1:
    distance = number_input_with_suggestion('Transport distance for waste (Round Trip) (km)', value=0.0, step=0.1, key="distance", selected_scenario=selected_scenario)
    quantity = number_input_with_suggestion('Waste quantity (ton/m³)', value=0.0, step=0.001, key="quantity", selected_scenario=selected_scenario)
with col2:
    destination = st.selectbox('Waste destination', ['Dump', 'Sanitary Landfill'])

st.info('Quantity multiplied by km gives the factor in ton.km')
st.info('Impacts in each category differ according to the destination.')

ton_km_factor = distance * quantity
st.write(f'Factor ton.km: {ton_km_factor:.2e}')

# UASB (pré-selecionado)
st.subheader('UASB Treatment')
st.write('UASB treatment is pre-selected.')

# Processos adicionais 
st.subheader('Additional Processes')
additional_processes = st.multiselect(
    'Select Additional Process(es)',
    ['UASB Only',
     'Vertical Flow Wetland', 
     'Trickling Filter + Secondary Clarifier', 
     'Polishing Pond']
)

# Seção para produtos químicos
st.header('Chemical Products')
st.write('Select the chemical products used in treatment:')

show_chemicals = st.checkbox('Show chemical products', value=True)

inputs = {}

if show_chemicals:
    col1, col2, col3 = st.columns(3)
    
    with col1:
        inputs['cloreto_ferrico'] = number_input_with_suggestion('Ferric Chloride (kg/m³)', value=0.0, step=0.001, key="cloreto_ferrico", selected_scenario=selected_scenario)
        inputs['policloreto_aluminio'] = number_input_with_suggestion('Aluminum Polychloride (kg/m³)', value=0.0, step=0.001, key="policloreto_aluminio", selected_scenario=selected_scenario)
        inputs['sulfato_aluminio'] = number_input_with_suggestion('Aluminum Sulfate (kg/m³)', value=0.0, step=0.001, key="sulfato_aluminio", selected_scenario=selected_scenario)
        inputs['acido_paracetico'] = number_input_with_suggestion('Peracetic Acid (kg/m³)', value=0.0, step=0.001, key="acido_paracetico", selected_scenario=selected_scenario)
    
    with col2:
        inputs['hipoclorito_sodio'] = number_input_with_suggestion('Sodium Hypochlorite (kg/m³)', value=0.0, step=0.001, key="hipoclorito_sodio", selected_scenario=selected_scenario)
        inputs['peroxido_hidrogenio'] = number_input_with_suggestion('Hydrogen Peroxide (kg/m³)', value=0.0, step=0.001, key="peroxido_hidrogenio", selected_scenario=selected_scenario)
        inputs['cal'] = number_input_with_suggestion('Lime (kg/m³)', value=0.0, step=0.001, key="cal", selected_scenario=selected_scenario)
        inputs['hidroxido_sodio'] = number_input_with_suggestion('Sodium Hydroxide (kg/m³)', value=0.0, step=0.001, key="hidroxido_sodio", selected_scenario=selected_scenario)
    
    with col3:
        inputs['nitrato_calcio'] = number_input_with_suggestion('Calcium Nitrate (kg/m³)', value=0.0, step=0.001, key="nitrato_calcio", selected_scenario=selected_scenario)
        inputs['sulfato_sodio'] = number_input_with_suggestion('Sodium Sulfate (kg/m³)', value=0.0, step=0.001, key="sulfato_sodio", selected_scenario=selected_scenario)
        inputs['sulfato_ferro'] = number_input_with_suggestion('Iron Sulfate (kg/m³)', value=0.0, step=0.001, key="sulfato_ferro", selected_scenario=selected_scenario)
        inputs['transportes_quimicos'] = number_input_with_suggestion('Chemical Transport (kg.km)', value=0.0, step=0.1, key="transportes_quimicos", selected_scenario=selected_scenario)
    
    st.write('Land Use')
    inputs['uso_terra'] = number_input_with_suggestion('Area used (m²)', value=0.0, step=0.1, key="uso_terra", selected_scenario=selected_scenario)

# Passo 2: Inventário do ciclo de vida
st.header('Step 2: Life Cycle Inventory')

st.subheader('Energy Consumption')
inputs['eletricidade'] = number_input_with_suggestion('Electricity (kWh/m³)', value=0.0, step=0.1, key="eletricidade", selected_scenario=selected_scenario)

st.subheader('Water Emissions')
inputs['fosforo_total'] = number_input_with_suggestion('Total Phosphorus (kg/m³)', value=0.0, step=0.001, key="fosforo_total", selected_scenario=selected_scenario)
inputs['nitrogenio_total'] = number_input_with_suggestion('Total Nitrogen (kg/m³)', value=0.0, step=0.001, key="nitrogenio_total", selected_scenario=selected_scenario)

st.write("Other parameters are optional. Click 'Show more' to display them.")
if st.checkbox('Show more'):
    optional_params = [
        ('bario', 'Barium'),
        ('cobre', 'Copper'),
        ('selenio', 'Selenium'),
        ('zinco', 'Zinc'),
        ('tolueno', 'Toluene'),
        ('cromo', 'Chromium'),
        ('cadmio', 'Cadmium'),
        ('chumbo', 'Lead'),
        ('niquel', 'Nickel')
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
st.header('Step 3: Sludge Disposal')

disposicao_lodo = st.selectbox(
    'Choose the sludge disposal method',
    ['Landfill disposal', 'Dump disposal', 'Fertigation or agriculture']
)

if disposicao_lodo in ['Landfill disposal', 'Dump disposal']:
    st.subheader('Sludge Treatment')
    
    col1, col2 = st.columns(2)
    with col1:
        distancia_lodo = number_input_with_suggestion('Sludge transport distance (Round Trip) (km)', value=0.0, step=0.1, key="distancia_lodo", selected_scenario=selected_scenario)
    with col2:
        quantidade_lodo = number_input_with_suggestion('Sludge quantity (ton/m³)', value=0.0, step=0.001, key="quantidade_lodo", selected_scenario=selected_scenario)
    
    ton_km_factor_lodo = distancia_lodo * quantidade_lodo
    st.write(f'Factor ton.km for sludge: {ton_km_factor_lodo:.2e}')

elif disposicao_lodo == 'Fertigation or agriculture':
    st.subheader('Sludge Composition')
    
    col1, col2 = st.columns(2)
    with col1:
        inputs['lodo_fosforo'] = number_input_with_suggestion('Phosphorus (kg/m³)', value=0.0, step=0.001, key="lodo_fosforo", selected_scenario=selected_scenario)
    with col2:
        inputs['lodo_nitrogenio'] = number_input_with_suggestion('Ammoniacal Nitrogen (kg/m³)', value=0.0, step=0.001, key="lodo_nitrogenio", selected_scenario=selected_scenario)
    
    st.write("Additional elements (optional)")
    if st.checkbox('Show sludge elements'):
        elementos_adicionais = [
            ('arsenio', 'Arsenic'),
            ('bario', 'Barium'),
            ('cadmio', 'Cadmium'),
            ('chumbo', 'Lead'),
            ('cobre', 'Copper'),
            ('cromo', 'Chromium'),
            ('molibdenio', 'Molybdenum'),
            ('niquel', 'Nickel'),
            ('estanho', 'Tin'),
            ('zinco', 'Zinc'),
            ('diclorobenzeno', 'Dichlorobenzene')
        ]
        
        for elemento_key, elemento_display in elementos_adicionais:
            input_key = f'lodo_{elemento_key}'
            inputs[input_key] = number_input_with_suggestion(
                f'Sludge - {elemento_display} (kg/m³)', 
                value=0.0, 
                step=0.0001,
                key=input_key,
                selected_scenario=selected_scenario
            )
    
# Passo 4: Queima de Biogás
st.header('Step 4: Biogas Burning')

tipo_queimador = st.selectbox(
    'Choose the burner type',
    ['Open burner', 'Closed burner with energy reuse']
)

if tipo_queimador == 'Closed burner with energy reuse':
    st.subheader('Closed Burner Emissions')
    inputs['dioxido_carbono'] = number_input_with_suggestion('Carbon Dioxide (kg/m³)', value=0.0, step=0.001, key="dioxido_carbono", selected_scenario=selected_scenario)
    
    st.header('Step 5: Biogas Reuse')
    st.write('Since you selected closed burner with energy reuse, fill in the biogas reuse data to calculate avoided emissions.')
    st.info('The energy conversion efficiency is set to 100%.')
    
    inputs['quantidade_biogas'] = number_input_with_suggestion(
        'Electricity (kWh.m−3)', 
        value=0.0, 
        step=0.1,
        key="quantidade_biogas",
        selected_scenario="Biogas Reuse"
    )
    
    inputs['eficiencia_conversao'] = 100.0

elif tipo_queimador == 'Open burner':
    st.subheader('Open Burner Emissions')
    
    col1, col2 = st.columns(2)
    with col1:
        inputs['metano'] = number_input_with_suggestion('Methane (kg/m³)', value=0.0, step=0.001, key="metano", selected_scenario=selected_scenario)
        inputs['dioxido_carbono'] = number_input_with_suggestion('Carbon Dioxide (kg/m³)', value=0.0, step=0.001, key="dioxido_carbono", selected_scenario=selected_scenario)
    with col2:
        inputs['oxido_nitroso'] = number_input_with_suggestion('Nitrous Oxide (kg/m³)', value=0.0, step=0.001, key="oxido_nitroso", selected_scenario=selected_scenario)

# Visualização
st.markdown("---")
st.subheader("Visualization Options")

viz_col1, viz_col2 = st.columns(2)

with viz_col1:
    st.write("Select impact categories to visualize:")
    impact_options = {}
    for impact in IMPACT_NAMES.keys():
        default_value = impact != 'Land Use'
        impact_options[impact] = st.checkbox(IMPACT_NAMES[impact], value=default_value, key=f"check_{impact}")

with viz_col2:
    st.subheader("Detailed Analysis")
    impact_selected = st.selectbox(
        'Select impact type for detailed view:',
        list(IMPACT_NAMES.keys())
    )

# Botão para calcular os impactos
if st.button('Calculate Impacts'):
    # Primeiro, adicionamos todas as informações do tratamento preliminar ao dicionário inputs
    inputs['quantity'] = quantity
    inputs['destination'] = destination
    inputs['ton_km_factor'] = ton_km_factor
    
    # Adicionamos as informações do lodo dependendo do tipo de disposição
    if disposicao_lodo in ['Landfill disposal', 'Dump disposal']:
        inputs['disposicao_lodo'] = disposicao_lodo
        inputs['quantidade_lodo'] = quantidade_lodo
        inputs['ton_km_factor_lodo'] = ton_km_factor_lodo
    elif disposicao_lodo == 'Fertigation or agriculture':
        inputs['disposicao_lodo'] = disposicao_lodo
    
    # Adicionamos as informações do queimador
    inputs['tipo_queimador'] = tipo_queimador
    
    # Calculamos os impactos
    results = calculate_impacts(inputs)
    
    # Filtramos os resultados com base nas categorias selecionadas
    selected_impacts = [impact for impact, selected in impact_options.items() if selected]
    filtered_results = {k: v for k, v in results.items() if k in selected_impacts}
    
    # Criamos DataFrame com as categorias selecionadas
    df_results = pd.DataFrame(
        list(filtered_results.items()), 
        columns=['Impact Category', 'Value']
    )
    
    # Mapeamos os nomes das categorias
    df_results['Impact Category'] = df_results['Impact Category'].map(IMPACT_NAMES)
    df_results['Value'] = pd.to_numeric(df_results['Value'], errors='coerce')
    
    # Verificamos se temos dados para mostrar
    if len(df_results) > 0:
        # Gráfico principal
        fig = px.bar(
            df_results, 
            x='Impact Category', 
            y='Value',
            title='Environmental Impacts by Category',
            labels={'Value': 'Impact Value'},
            color='Impact Category',
            color_discrete_sequence=px.colors.qualitative.Bold,
            template="plotly_white"
        )
        fig.update_layout(
            xaxis_title="Impact Category",
            yaxis_title="Impact Value",
            xaxis={'categoryorder':'total descending'},
            showlegend=False,
            height=500,
            margin=dict(t=50, b=100, l=100, r=30),
            title_font=dict(size=20, family="Arial", color="#333333"),
            font=dict(family="Arial", size=14),
            xaxis_tickangle=-45,
            plot_bgcolor='white',
            bargap=0.3
        )
        fig.update_yaxes(showgrid=True, gridcolor='lightgray', gridwidth=0.5)
        fig.update_xaxes(showgrid=False)
        st.plotly_chart(fig, use_container_width=True)
        
        # Análise Detalhada por Categoria
        category_impacts = calculate_impacts_by_category(inputs, impact_selected)
        
        if category_impacts:
            # Criar DataFrame para a tabela de categorias
            df_categories_all = pd.DataFrame({
                'Category': ['Energy Consumption', 'Chemical Products', 'Transportation', 
                             'Water Emissions', 'Atmospheric Emissions', 
                             'Sludge Disposal', 'Waste Disposal'],
                'Impact': [category_impacts.get('Energy Consumption', 0),
                           category_impacts.get('Chemical Products', 0),
                           category_impacts.get('Transportation', 0),
                           category_impacts.get('Water Emissions', 0),
                           category_impacts.get('Atmospheric Emissions', 0),
                           category_impacts.get('Sludge Disposal', 0),
                           category_impacts.get('Waste Disposal', 0)]
            })
            
            # Tabela de resultados formatada com 8 casas decimais
            st.subheader("Environmental Impacts by Category")
            df_results_formatted = df_results.copy()
            df_results_formatted['Value'] = df_results_formatted['Value'].apply(format_number_8f)
            st.table(df_results_formatted)
            

            
            # Gráfico de categorias
            fig_categories = px.bar(
                df_categories_all,
                x='Category',
                y='Impact',
                title=f'Contribution by Category for {impact_selected}',
                labels={'Impact': IMPACT_NAMES[impact_selected]},
                color='Category',
                color_discrete_sequence=px.colors.qualitative.Bold,
                template="plotly_white"
            )
            fig_categories.update_layout(
                xaxis_title="Category",
                yaxis_title=f"Impact ({IMPACT_NAMES[impact_selected].split('(')[1].strip(')')})",
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
            fig_categories.update_yaxes(showgrid=True, gridcolor='lightgray', gridwidth=0.5)
            fig_categories.update_xaxes(showgrid=False)
            st.plotly_chart(fig_categories, use_container_width=True)
                        # Tabela de categorias formatada com 8 casas decimais
            st.subheader("Contribution by Category")
            df_categories_formatted = df_categories_all.copy()
            df_categories_formatted['Impact'] = df_categories_formatted['Impact'].apply(format_number_8f)
            st.table(df_categories_formatted)
            
            st.success("Detailed analysis completed!")
        else:
            st.warning("Insufficient data to show detailed graph for this impact category.")
    else:
        st.warning("No impact category selected for visualization.")
