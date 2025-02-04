import streamlit as st
import pandas as pd
import plotly.express as px

# Fatoresss para impactos
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
# Logo após os imports e definições de IMPACT_FACTORS e IMPACT_NAMES, 
# e antes de começar a interface do usuário:
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
    
    # Processando entradas básicas
    for input_name, value in inputs.items():
        if input_name in IMPACT_FACTORS:
            for impact, factor in IMPACT_FACTORS[input_name].items():
                results[impact] += value * factor
    
    # Processando Uso da Terra
    if 'area_utilizada' in inputs:
        results['Uso da Terra'] += inputs['area_utilizada'] * IMPACT_FACTORS['uso_terra']['Uso da Terra']
    
    # Processando Disposição de Resíduos do Tratamento Preliminar
    if 'quantity' in inputs and 'destination' in inputs:
        if inputs['destination'] == 'Aterro Sanitário':
            impacts = IMPACT_FACTORS['residuos_trat_preliminar_aterro']
        else:  # Lixão
            impacts = IMPACT_FACTORS['residuos_trat_preliminar_lixao']
        
        for impact, factor in impacts.items():
            results[impact] += inputs['quantity'] * factor
    
    # Processando transporte de resíduos
    if 'transportes' in inputs:
        for impact, factor in IMPACT_FACTORS['transportes'].items():
            results[impact] += inputs['transportes'] * factor
    
    # ... resto da função continua igual ...
    
    # Processando Lodo
    if 'disposicao_lodo' in inputs:
        if inputs['disposicao_lodo'] == 'Disposição em aterro':
            lodo_impacts = IMPACT_FACTORS['lodo_aterro']
        elif inputs['disposicao_lodo'] == 'Disposição em lixão':
            lodo_impacts = IMPACT_FACTORS['lodo_lixao']
        
        if 'quantidade_lodo' in inputs:
            for impact, factor in lodo_impacts.items():
                results[impact] += inputs['quantidade_lodo'] * factor
    
    # Processando emissões para água
    water_emissions = ['bario', 'selenio', 'cadmio', 'niquel']
    for emission in water_emissions:
        if emission in inputs and inputs[emission] > 0:
            for impact, factor in IMPACT_FACTORS[emission].items():
                results[impact] += inputs[emission] * factor
    
    # Processando emissões para solo (ferti-irrigação)
    if 'disposicao_lodo' in inputs and inputs['disposicao_lodo'] == 'Ferti-irrigação ou agricultura':
        soil_emissions = [
            'lodo_arsenio', 'lodo_bario', 'lodo_cadmio', 'lodo_chumbo', 
            'lodo_cobre', 'lodo_cromo', 'lodo_molibdenio', 'lodo_niquel', 
            'lodo_estanho', 'lodo_zinco', 'lodo_diclorobenzeno'
        ]
        
        for emission in soil_emissions:
            if emission in inputs and inputs[emission] > 0:
                # Remove o prefixo 'lodo_' para encontrar os fatores corretos
                base_emission = emission.replace('lodo_', '')
                if base_emission in IMPACT_FACTORS:
                    for impact, factor in IMPACT_FACTORS[base_emission].items():
                        results[impact] += inputs[emission] * factor
    
    return results

st.title('Avaliação do Ciclo de Vida para ETE')

# Inicializar o dicionário de inputs no início
inputs = {}

# Tratamento Preliminar (obrigatório)
st.header('Passo 1: Processo de Tratamento')
st.subheader('Tratamento Preliminar')
st.write('O tratamento preliminar é obrigatório.')

col1, col2 = st.columns(2)
with col1:
    distance = number_input_scientific('Distância para o transporte de resíduos (Ida e Volta) (km)', value=0.0, step=0.1)
    quantity = number_input_scientific('Quantidade de resíduos (ton/m³)', value=0.0, step=0.001)
with col2:
    destination = st.selectbox('Destino dos resíduos', ['Lixão', 'Aterro Sanitário'])

st.info('A quantidade é multiplicada pelo km, isso dá o fator em ton.km')
st.info('Os impactos em cada categoria são diferentes de acordo com a destinação.')

# Cálculo do fator ton.km e adição aos inputs
ton_km_factor = distance * quantity
st.write(f'Fator ton.km: {ton_km_factor:.2e}')
inputs['transportes'] = ton_km_factor
inputs['quantity'] = quantity  # Adicionando quantidade aos inputs
inputs['destination'] = destination  # Adicionando destino aos inputs

# UASB (deve ser pré-selecionado segundo o fernando)
st.subheader('Tratamento UASB')
st.write('O tratamento UASB está pré-selecionado.')

# Processos adicionais 
st.subheader('Processos Adicionais')
additional_processes = st.multiselect(
    'Selecione o(s) Processo(s) Adicional(is)',
    ['Wetland de Fluxo Vertical', 'Filtro Biológico percolador + Decantador Segundario', 'Lagoa de Polimento']
)

# Passo 2: Inventário do ciclo de vida não se esqueça dos inputs
st.header('Passo 2: Inventário do ciclo de vida')

inputs = {}

st.subheader('Consumo de Energia')
inputs['eletricidade'] = number_input_scientific('Eletricidade (kWh/m³)', value=0.0, step=0.1)

st.subheader('Uso da Terra')
inputs['area_utilizada'] = number_input_scientific('Área utilizada (m²)', value=0.0, step=0.1)

st.subheader('Emissões para a Água')
inputs['fosforo_total'] = number_input_scientific('Fósforo Total (kg/m³)', value=0.0, step=0.001)
inputs['nitrogenio_total'] = number_input_scientific('Nitrogênio Total (kg/m³)', value=0.0, step=0.001)

st.write("Os outros parâmetros são opcionais. Clique em 'Mostrar mais' para exibi-los.")
if st.checkbox('Mostrar mais'):
    optional_params = ['Bário', 'Cobre', 'Selênio', 'Zinco', 'Tolueno', 'Cromo', 'Cádmio', 'Chumbo', 'Níquel']
    for param in optional_params:
        inputs[param.lower()] = number_input_scientific(f'{param} (kg/m³)', value=0.0, step=0.0001)

# Passo 3: Disposição do Lodo   por categoria
st.header('Passo 3: Disposição do Lodo')

disposicao_lodo = st.selectbox(
    'Escolha o método de disposição do lodo',
    ['Disposição em aterro', 'Disposição em lixão', 'Ferti-irrigação ou agricultura']
)

if disposicao_lodo in ['Disposição em aterro', 'Disposição em lixão']:
    st.subheader('Tratamento do Lodo')
    
    col1, col2 = st.columns(2)
    with col1:
        distancia_lodo = number_input_scientific('Distância para o transporte do lodo (Ida e Volta) (km)', value=0.0, step=0.1)
    with col2:
        quantidade_lodo = number_input_scientific('Quantidade de lodo (ton/m³)', value=0.0, step=0.001)
    
    ton_km_factor_lodo = distancia_lodo * quantidade_lodo
    st.write(f'Fator ton.km para o lodo: {ton_km_factor_lodo:.2e}')

elif disposicao_lodo == 'Ferti-irrigação ou agricultura':
    st.subheader('Composição do Lodo')
    
    col1, col2 = st.columns(2)
    with col1:
        inputs['lodo_fosforo'] = number_input_scientific('Fósforo (kg/m³)', value=0.0, step=0.001)
    with col2:
        inputs['lodo_nitrogenio'] = number_input_scientific('Nitrogênio Amoniacal (kg/m³)', value=0.0, step=0.001)
    
    st.write("Elementos adicionais (opcionais)")
    if st.checkbox('Mostrar elementos do lodo'):
        elementos_adicionais = [
            'arsenio', 'bario', 'cadmio', 'chumbo', 'cobre', 'cromo',
            'molibdenio', 'niquel', 'estanho', 'zinco', 'diclorobenzeno'
        ]
        for elemento in elementos_adicionais:
            inputs[f'lodo_{elemento}'] = number_input_scientific(
                f'Lodo - {elemento.title()} (kg/m³)', 
                value=0.0, 
                step=0.0001
            )
# Passo 4: Queima de Biogás# não esqueça as observações no video do fernando
st.header('Passo 4: Queima de Biogás')

tipo_queimador = st.selectbox(
    'Escolha o tipo de queimador',
    ['Queimador aberto', 'Queimador fechado com reaproveitamento energético']
)

if tipo_queimador == 'Queimador fechado com reaproveitamento energético':
    st.subheader('Emissões do Queimador Fechado')
    inputs['dioxido_carbono'] = number_input_scientific('Dióxido de Carbono (kg/m³)', value=0.0, step=0.001)

elif tipo_queimador == 'Queimador aberto':
    st.subheader('Emissões do Queimador Aberto')
    
    col1, col2 = st.columns(2)
    with col1:
        inputs['metano'] = number_input_scientific('Metano (kg/m³)', value=0.0, step=0.001)
        inputs['dioxido_carbono'] = number_input_scientific('Dióxido de Carbono (kg/m³)', value=0.0, step=0.001)
    with col2:
        inputs['oxido_nitroso'] = number_input_scientific('Óxido Nitroso (kg/m³)', value=0.0, step=0.001)

if st.button('Calcular Impactos'):
    # Adicione as informações do lodo aos inputs
    if disposicao_lodo in ['Disposição em aterro', 'Disposição em lixão']:
        inputs['ton_km_factor_lodo'] = ton_km_factor_lodo
        inputs['disposicao_lodo'] = disposicao_lodo
    
    # Adicione as informações do queimador aos inputs
    inputs['tipo_queimador'] = tipo_queimador
    
    results = calculate_impacts(inputs)
    
    st.header('Resultados')
    
    # Criar um DataFrame para os resultados
    df_results = pd.DataFrame(list(results.items()), columns=['Categoria de Impacto', 'Valor'])
    df_results['Categoria de Impacto'] = df_results['Categoria de Impacto'].map(IMPACT_NAMES)
    
    # Criar gráfico de barras com Plotly
    fig = px.bar(df_results, x='Categoria de Impacto', y='Valor', 
                 title='Impactos Ambientais por Categoria',
                 labels={'Valor': 'Impacto'},
                 color='Categoria de Impacto')
    
    # Personalizar o layout do gráfico
    fig.update_layout(xaxis_title="Categoria de Impacto",
                      yaxis_title="Valor do Impacto",
                      xaxis={'categoryorder':'total descending'})
    
    st.plotly_chart(fig)
    
    # Mostrar resultados em formato de tabela
    st.table(df_results)
