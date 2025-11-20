import streamlit as st
import pandas as pd
import numpy as np
from pyomo.environ import *
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import gdown
import os
import random

# ============================================================================
# CONFIGURACIÓN DE PÁGINA
# ============================================================================
st.set_page_config(
    page_title="Network Optimizer Pro - UACJ MIAAD",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# PALETA DE COLORES Y ESTILOS PREMIUM
# ============================================================================
COLORS = {
    'dust_grey': '#dad7cd',
    'dry_sage': '#a3b18a',
    'fern': '#588157',
    'hunter_green': '#3a5a40',
    'pine_teal': '#344e41',
    'white': '#ffffff',
    'light_grey': '#f8f9fa'
}

# CSS Premium con Montserrat
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700;800&display=swap');
    
    * {{
        font-family: 'Montserrat', sans-serif !important;
    }}
    
    .main {{
        background: linear-gradient(135deg, {COLORS['dust_grey']} 0%, {COLORS['white']} 100%);
    }}
    
    /* Header Premium */
    .premium-header {{
        background: linear-gradient(135deg, {COLORS['pine_teal']} 0%, {COLORS['hunter_green']} 50%, {COLORS['fern']} 100%);
        padding: 2rem 2rem;
        border-radius: 20px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(52, 78, 65, 0.3);
        position: relative;
        overflow: hidden;
    }}
    
    .premium-header::before {{
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: pulse 8s ease-in-out infinite;
    }}
    
    @keyframes pulse {{
        0%, 100% {{ transform: scale(1); opacity: 0.5; }}
        50% {{ transform: scale(1.1); opacity: 0.8; }}
    }}
    
    .premium-header h1 {{
        margin: 0;
        font-size: 2.5rem;
        font-weight: 800;
        letter-spacing: -0.5px;
        position: relative;
        z-index: 1;
    }}
    
    .premium-header p {{
        margin: 0.5rem 0 0 0;
        font-size: 1.1rem;
        font-weight: 400;
        opacity: 0.95;
        position: relative;
        z-index: 1;
    }}
    
    /* Metric Cards Glassmorphism */
    .metric-glass {{
        background: rgba(255, 255, 255, 0.75);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(88, 129, 87, 0.2);
        padding: 1.5rem;
        border-radius: 16px;
        box-shadow: 0 8px 32px rgba(52, 78, 65, 0.15);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }}
    
    .metric-glass:hover {{
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(52, 78, 65, 0.25);
        border-color: {COLORS['fern']};
    }}
    
    .metric-glass::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
        background: linear-gradient(180deg, {COLORS['fern']} 0%, {COLORS['hunter_green']} 100%);
    }}
    
    .metric-label {{
        font-size: 0.75rem;
        color: {COLORS['hunter_green']};
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-bottom: 0.5rem;
    }}
    
    .metric-value {{
        font-size: 2rem;
        font-weight: 800;
        color: {COLORS['pine_teal']};
        line-height: 1;
    }}
    
    .metric-subtitle {{
        font-size: 0.85rem;
        color: {COLORS['dry_sage']};
        font-weight: 500;
        margin-top: 0.5rem;
    }}
    
    /* Botones Premium */
    .stButton > button {{
        background: linear-gradient(135deg, {COLORS['fern']} 0%, {COLORS['hunter_green']} 100%);
        color: white;
        font-weight: 600;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-size: 1rem;
        letter-spacing: 0.5px;
        box-shadow: 0 4px 15px rgba(88, 129, 87, 0.3);
        transition: all 0.3s ease;
    }}
    
    .stButton > button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(88, 129, 87, 0.4);
    }}
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 8px;
        background-color: transparent;
    }}
    
    .stTabs [data-baseweb="tab"] {{
        background-color: rgba(255, 255, 255, 0.6);
        border-radius: 10px 10px 0 0;
        color: {COLORS['hunter_green']};
        font-weight: 600;
        padding: 0.75rem 1.5rem;
        border: 1px solid {COLORS['dust_grey']};
    }}
    
    .stTabs [aria-selected="true"] {{
        background: linear-gradient(135deg, {COLORS['fern']} 0%, {COLORS['hunter_green']} 100%);
        color: white;
        border-color: {COLORS['fern']};
    }}
    
    /* Sidebar - ARREGLADO */
    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, {COLORS['dust_grey']} 0%, {COLORS['white']} 100%);
    }}
    
    .section-header {{
        background: linear-gradient(135deg, {COLORS['fern']} 0%, {COLORS['hunter_green']} 100%);
        color: white;
        padding: 0.75rem 1rem;
        border-radius: 10px;
        margin: 1rem 0 0.5rem 0;
        font-weight: 700;
        font-size: 0.95rem;
        text-align: center;
        letter-spacing: 0.5px;
    }}
    
    /* DataFrames */
    .dataframe {{
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }}
    
    /* Info boxes */
    .stAlert {{
        border-radius: 12px;
        border-left: 4px solid {COLORS['fern']};
        background-color: rgba(163, 177, 138, 0.1);
    }}
    
    /* Number inputs */
    .stNumberInput > div > div > input {{
        text-align: center;
        font-weight: 600;
    }}
    
    /* Radio buttons */
    .stRadio > label {{
        font-weight: 600;
        color: {COLORS['pine_teal']};
        font-size: 1rem;
    }}
</style>
""", unsafe_allow_html=True)

# ============================================================================
# CONFIGURACIÓN Y NOMBRES ESTÁNDAR
# ============================================================================
FILENAMES = {
    'plantas': 'plantas.csv',
    'centros': 'centros.csv',
    'clientes': 'clientes.csv',
    'costos_pc': 'Costos Plantas x CeDis.csv',
    'costos_cj': 'Costos CeDis x Cliente.csv'
}

DRIVE_IDS = {
    FILENAMES['plantas']: '1sm2UYkaeETYnh-nIykTHO3jrRUVzMbmP',
    FILENAMES['centros']: '1weTwr_qTtHqpTbscixP-6FweCpvySiOv',
    FILENAMES['clientes']: '1RRlz8U0f-TOmYL_1EovJJKlw-DC2YRLI',
    FILENAMES['costos_pc']: '1JiYe20Y0lq5LJOHgNjlB0cOk7augwyZl',
    FILENAMES['costos_cj']: '1MU5Y-vY_Xv_X7AlP_xYsw8p9opqVtkDX'
}

# ============================================================================
# FUNCIONES DE UTILIDAD
# ============================================================================

def resetear_todo():
    """Limpia todos los archivos y session state"""
    for filename in FILENAMES.values():
        if os.path.exists(filename):
            os.remove(filename)
    
    keys_to_clear = list(st.session_state.keys())
    for key in keys_to_clear:
        del st.session_state[key]

def generar_datos_configurables(config):
    """Genera datos aleatorios basados en configuración del usuario"""
    n_plantas = config['n_plantas']
    n_centros = config['n_centros']
    n_clientes = config['n_clientes']
    productos = [f'Producto_{chr(65+i)}' for i in range(config['n_productos'])]
    
    # 1. Plantas
    data_p = []
    for i in range(1, n_plantas + 1):
        for p in productos:
            data_p.append({
                'Planta': f'Planta_{i}',
                'Producto': p,
                'Capacidad_Produccion': random.randint(config['cap_prod_min'], config['cap_prod_max']),
                'Costo_Produccion': random.randint(config['costo_prod_min'], config['costo_prod_max'])
            })
    df_plantas = pd.DataFrame(data_p)
    df_plantas.to_csv(FILENAMES['plantas'], index=False)
    
    # 2. Centros
    data_c = []
    for i in range(1, n_centros + 1):
        for p in productos:
            data_c.append({
                'Centro': f'Centro_{i}',
                'Producto': p,
                'Capacidad_Almacenamiento': random.randint(config['cap_alm_min'], config['cap_alm_max'])
            })
    df_centros = pd.DataFrame(data_c)
    df_centros.to_csv(FILENAMES['centros'], index=False)
    
    # 3. Clientes
    data_j = []
    for i in range(1, n_clientes + 1):
        for p in productos:
            data_j.append({
                'Cliente': f'Cliente_{i}',
                'Producto': p,
                'Demanda': random.randint(config['demanda_min'], config['demanda_max'])
            })
    df_clientes = pd.DataFrame(data_j)
    df_clientes.to_csv(FILENAMES['clientes'], index=False)
    
    # 4. Costos P-C
    data_pc = []
    for i in range(1, n_plantas + 1):
        for idx_p, prod in enumerate(productos):
            row = {'Planta': i, 'Producto ': idx_p + 1}
            for c in range(1, n_centros + 1):
                row[f'centro{c}'] = random.randint(config['costo_tpc_min'], config['costo_tpc_max'])
            data_pc.append(row)
    df_pc = pd.DataFrame(data_pc)
    df_pc.to_csv(FILENAMES['costos_pc'], index=False)
    
    # 5. Costos C-J
    data_cj = []
    for c in range(1, n_centros + 1):
        for idx_p, prod in enumerate(productos):
            row = {'Centro': c, 'Producto': idx_p + 1}
            for j in range(1, n_clientes + 1):
                row[f'Cliente{j}'] = random.randint(config['costo_tcj_min'], config['costo_tcj_max'])
            data_cj.append(row)
    df_cj = pd.DataFrame(data_cj)
    df_cj.to_csv(FILENAMES['costos_cj'], index=False)
    
    return df_plantas, df_centros, df_clientes, df_pc, df_cj

def descargar_drive():
    """Descarga archivos desde GDrive"""
    for name, fid in DRIVE_IDS.items():
        url = f'https://drive.google.com/uc?id={fid}'
        gdown.download(url, name, quiet=True)

def identificar_y_guardar_archivos(uploaded_files):
    """Identifica archivos subidos"""
    contados = 0
    for uploaded_file in uploaded_files:
        name = uploaded_file.name.lower()
        df = pd.read_csv(uploaded_file)
        
        if 'planta' in name and 'costo' not in name:
            df.to_csv(FILENAMES['plantas'], index=False)
            contados += 1
        elif 'centro' in name and 'costo' not in name:
            df.to_csv(FILENAMES['centros'], index=False)
            contados += 1
        elif 'cliente' in name and 'costo' not in name:
            df.to_csv(FILENAMES['clientes'], index=False)
            contados += 1
        elif 'costo' in name and 'planta' in name:
            df.to_csv(FILENAMES['costos_pc'], index=False)
            contados += 1
        elif 'costo' in name and ('cedis' in name or 'centro' in name):
            df.to_csv(FILENAMES['costos_cj'], index=False)
            contados += 1
            
    return contados == 5

def estandarizar_id(valor, prefijo):
    """Estandariza IDs"""
    s_val = str(valor).strip()
    if prefijo in s_val and "_" in s_val:
        return s_val.replace(" ", "")
    numeros = ''.join(filter(str.isdigit, s_val))
    return f"{prefijo}_{numeros}"

def preparar_datos_robusto():
    """Lee y limpia datos"""
    try:
        df_p = pd.read_csv(FILENAMES['plantas'])
        df_c = pd.read_csv(FILENAMES['centros'])
        df_j = pd.read_csv(FILENAMES['clientes'])
        df_cost_pc = pd.read_csv(FILENAMES['costos_pc'])
        df_cost_cj = pd.read_csv(FILENAMES['costos_cj'])
        
        for df in [df_p, df_c, df_j, df_cost_pc, df_cost_cj]:
            df.columns = df.columns.str.strip()

        df_p['Planta'] = df_p['Planta'].apply(lambda x: estandarizar_id(x, 'Planta'))
        df_p['Producto'] = df_p['Producto'].apply(lambda x: estandarizar_id(x, 'Producto'))
        df_c['Centro'] = df_c['Centro'].apply(lambda x: estandarizar_id(x, 'Centro'))
        df_c['Producto'] = df_c['Producto'].apply(lambda x: estandarizar_id(x, 'Producto'))
        df_j['Cliente'] = df_j['Cliente'].apply(lambda x: estandarizar_id(x, 'Cliente'))
        df_j['Producto'] = df_j['Producto'].apply(lambda x: estandarizar_id(x, 'Producto'))

        cols_c = [c for c in df_cost_pc.columns if 'centro' in c.lower()]
        df_cost_pc['Planta'] = df_cost_pc['Planta'].apply(lambda x: estandarizar_id(x, 'Planta'))
        col_prod_pc = 'Producto' if 'Producto' in df_cost_pc.columns else 'Producto '
        df_cost_pc[col_prod_pc] = df_cost_pc[col_prod_pc].apply(lambda x: estandarizar_id(x, 'Producto'))
        df_pc_long = df_cost_pc.melt(id_vars=['Planta', col_prod_pc], value_vars=cols_c, var_name='C_Raw', value_name='Costo')
        df_pc_long['Centro'] = df_pc_long['C_Raw'].apply(lambda x: estandarizar_id(x, 'Centro'))
        df_pc_long.rename(columns={col_prod_pc: 'Producto'}, inplace=True)

        cols_j = [c for c in df_cost_cj.columns if 'cliente' in c.lower()]
        df_cost_cj['Centro'] = df_cost_cj['Centro'].apply(lambda x: estandarizar_id(x, 'Centro'))
        df_cost_cj['Producto'] = df_cost_cj['Producto'].apply(lambda x: estandarizar_id(x, 'Producto'))
        df_cj_long = df_cost_cj.melt(id_vars=['Centro', 'Producto'], value_vars=cols_j, var_name='J_Raw', value_name='Costo')
        df_cj_long['Cliente'] = df_cj_long['J_Raw'].apply(lambda x: estandarizar_id(x, 'Cliente'))

        return df_p, df_c, df_j, df_pc_long, df_cj_long
    except Exception as e:
        st.error(f"❌ Error en limpieza: {e}")
        return None

def resolver_modelo():
    """Resuelve el modelo de optimización"""
    datos = preparar_datos_robusto()
    if not datos:
        return None
    
    df_p, df_c, df_j, df_pc, df_cj = datos
    
    P = sorted(df_p['Planta'].unique())
    C = sorted(df_c['Centro'].unique())
    J = sorted(df_j['Cliente'].unique())
    K = sorted(df_p['Producto'].unique())
    
    cap_prod = df_p.set_index(['Planta', 'Producto'])['Capacidad_Produccion'].to_dict()
    cost_prod = df_p.set_index(['Planta', 'Producto'])['Costo_Produccion'].to_dict()
    cap_almacen = df_c.set_index(['Centro', 'Producto'])['Capacidad_Almacenamiento'].to_dict()
    demanda = df_j.set_index(['Cliente', 'Producto'])['Demanda'].to_dict()
    cost_tpc = df_pc.set_index(['Planta', 'Centro', 'Producto'])['Costo'].to_dict()
    cost_tcj = df_cj.set_index(['Centro', 'Cliente', 'Producto'])['Costo'].to_dict()
    
    m = ConcreteModel()
    m.P, m.C, m.J, m.K = Set(initialize=P), Set(initialize=C), Set(initialize=J), Set(initialize=K)
    m.x = Var(m.P, m.C, m.K, within=NonNegativeReals)
    m.y = Var(m.C, m.J, m.K, within=NonNegativeReals)
    
    def obj_rule(model):
        c1 = sum((cost_prod.get((p,k),0) + cost_tpc.get((p,c,k),0)) * model.x[p,c,k] for p in P for c in C for k in K)
        c2 = sum(cost_tcj.get((c,j,k),0) * model.y[c,j,k] for c in C for j in J for k in K)
        return c1 + c2
    m.obj = Objective(rule=obj_rule, sense=minimize)
    
    m.bal = Constraint(m.C, m.K, rule=lambda mod, c, k: sum(mod.x[p,c,k] for p in P) == sum(mod.y[c,j,k] for j in J))
    m.dem = Constraint(m.J, m.K, rule=lambda mod, j, k: sum(mod.y[c,j,k] for c in C) == demanda.get((j,k),0))
    m.cap_p = Constraint(m.P, m.K, rule=lambda mod, p, k: sum(mod.x[p,c,k] for c in C) <= cap_prod.get((p,k),0))
    m.cap_c = Constraint(m.C, m.K, rule=lambda mod, c, k: sum(mod.y[c,j,k] for j in J) <= cap_almacen.get((c,k),0))
    
    solver = SolverFactory('glpk')
    res = solver.solve(m, tee=False)
    
    if res.solver.termination_condition == TerminationCondition.optimal:
        prod_val = sum(cost_prod.get((p,k),0) * value(m.x[p,c,k]) for p in P for c in C for k in K)
        trans_pc_val = sum(cost_tpc.get((p,c,k),0) * value(m.x[p,c,k]) for p in P for c in C for k in K)
        trans_cj_val = sum(cost_tcj.get((c,j,k),0) * value(m.y[c,j,k]) for c in C for j in J for k in K)
        
        # Extraer flujos para análisis
        flujos_pc = []
        for p in P:
            for c in C:
                for k in K:
                    val = value(m.x[p,c,k])
                    if val > 0.01:
                        flujos_pc.append({
                            'Planta': p, 'Centro': c, 'Cliente': '', 'Producto': k,
                            'Cantidad': val,
                            'Costo_Unit': cost_tpc.get((p,c,k),0),
                            'Costo_Total': val * cost_tpc.get((p,c,k),0)
                        })
        
        flujos_cj = []
        for c in C:
            for j in J:
                for k in K:
                    val = value(m.y[c,j,k])
                    if val > 0.01:
                        flujos_cj.append({
                            'Planta': '', 'Centro': c, 'Cliente': j, 'Producto': k,
                            'Cantidad': val,
                            'Costo_Unit': cost_tcj.get((c,j,k),0),
                            'Costo_Total': val * cost_tcj.get((c,j,k),0)
                        })
        
        return {
            'modelo': m, 'total': value(m.obj),
            'c_prod': prod_val, 'c_tpc': trans_pc_val, 'c_tcj': trans_cj_val,
            'P': P, 'C': C, 'J': J, 'K': K,
            'flujos_pc': pd.DataFrame(flujos_pc),
            'flujos_cj': pd.DataFrame(flujos_cj),
            'df_plantas': df_p,
            'df_centros': df_c,
            'df_clientes': df_j,
            'cost_prod_dict': cost_prod  # AGREGADO AQUÍ
        }


        
    return None

# ============================================================================
# INTERFAZ DE USUARIO
# ============================================================================

# Header Premium
st.markdown(f"""
<div class="premium-header">
    <h1>🌿 Network Optimizer Pro</h1>
    <p>Sistema Avanzado de Optimización de Cadena de Suministro | UACJ MIAAD</p>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# SIDEBAR - CONFIGURACIÓN (SIN EXPANDERS)
# ============================================================================

with st.sidebar:
    st.markdown('<div class="section-header">⚙️ CONFIGURACIÓN</div>', unsafe_allow_html=True)
    
    # BOTÓN DE RESET PROMINENTE
    if st.button("🔄 RESETEAR TODO", use_container_width=True, type="secondary"):
        resetear_todo()
        st.success("✅ Sistema reseteado")
        st.rerun()
    
    st.markdown("---")
    
    fuente = st.radio(
        "**Origen de Datos:**",
        ["🎲 Generar Datos", "📤 Subir CSV", "☁️ Google Drive"],
        index=0,
        label_visibility="visible"
    )
    
    st.markdown("---")
    
    # CONFIGURACIÓN PARA GENERACIÓN RANDOM (SIN EXPANDERS)
    if fuente == "🎲 Generar Datos":
        st.markdown('<div class="section-header">🏢 RED DE DISTRIBUCIÓN</div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            n_plantas = st.number_input("Plantas", 2, 10, 3, key='n_p')
            n_centros = st.number_input("Centros", 2, 15, 4, key='n_c')
        with col2:
            n_clientes = st.number_input("Clientes", 5, 50, 15, key='n_cl')
            n_productos = st.number_input("Productos", 1, 5, 2, key='n_pr')
        
        st.markdown('<div class="section-header">🏭 PRODUCCIÓN</div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            cap_prod_min = st.number_input("Cap Mín", 1000, 20000, 5000, 500, key='cp_min')
            costo_prod_min = st.number_input("Costo Mín", 10, 100, 20, key='cprod_min')
        with col2:
            cap_prod_max = st.number_input("Cap Máx", cap_prod_min, 50000, 10000, 500, key='cp_max')
            costo_prod_max = st.number_input("Costo Máx", costo_prod_min, 200, 50, key='cprod_max')
        
        st.markdown('<div class="section-header">📦 ALMACENAMIENTO</div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            cap_alm_min = st.number_input("Cap Mín ", 1000, 10000, 3000, 500, key='ca_min')
        with col2:
            cap_alm_max = st.number_input("Cap Máx ", cap_alm_min, 20000, 6000, 500, key='ca_max')
        
        st.markdown('<div class="section-header">👥 DEMANDA</div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            demanda_min = st.number_input("Mínima", 50, 1000, 200, 50, key='d_min')
        with col2:
            demanda_max = st.number_input("Máxima", demanda_min, 2000, 800, 50, key='d_max')
        
        st.markdown('<div class="section-header">💰 COSTOS TRANSPORTE</div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.caption("**P → C**")
            costo_tpc_min = st.number_input("Mín", 1, 50, 5, key='tpc_min')
            costo_tpc_max = st.number_input("Máx", costo_tpc_min, 100, 15, key='tpc_max')
        with col2:
            st.caption("**C → J**")
            costo_tcj_min = st.number_input("Mín ", 1, 50, 5, key='tcj_min')
            costo_tcj_max = st.number_input("Máx ", costo_tcj_min, 100, 20, key='tcj_max')
        
        config = {
            'n_plantas': n_plantas, 'n_centros': n_centros, 'n_clientes': n_clientes,
            'n_productos': n_productos, 'cap_prod_min': cap_prod_min, 'cap_prod_max': cap_prod_max,
            'cap_alm_min': cap_alm_min, 'cap_alm_max': cap_alm_max,
            'demanda_min': demanda_min, 'demanda_max': demanda_max,
            'costo_prod_min': costo_prod_min, 'costo_prod_max': costo_prod_max,
            'costo_tpc_min': costo_tpc_min, 'costo_tpc_max': costo_tpc_max,
            'costo_tcj_min': costo_tcj_min, 'costo_tcj_max': costo_tcj_max
        }
        
        st.markdown("---")
        if st.button("🎲 Generar Escenario", use_container_width=True):
            with st.spinner("Generando datos..."):
                generar_datos_configurables(config)
                st.session_state['datos_cargados'] = True
                st.success("✅ Escenario generado")
                st.rerun()
    
    elif fuente == "📤 Subir CSV":
        st.info("Arrastra tus 5 archivos CSV aquí")
        files = st.file_uploader("Archivos CSV", accept_multiple_files=True, type="csv", label_visibility="collapsed")
        if st.button("📥 Cargar Archivos", use_container_width=True):
            if files and len(files) == 5:
                if identificar_y_guardar_archivos(files):
                    st.session_state['datos_cargados'] = True
                    st.success("✅ Archivos cargados")
                    st.rerun()
                else:
                    st.error("❌ Error al identificar archivos")
            else:
                st.warning("⚠️ Se requieren exactamente 5 archivos")
    
    elif fuente == "☁️ Google Drive":
        if st.button("☁️ Descargar desde Drive", use_container_width=True):
            with st.spinner("Descargando archivos..."):
                descargar_drive()
                st.session_state['datos_cargados'] = True
                st.success("✅ Datos descargados")
                st.rerun()

# ============================================================================
# ÁREA PRINCIPAL
# ============================================================================

if st.session_state.get('datos_cargados', False):
    
    st.markdown("### 📊 Datos del Escenario")
    
    try:
        df_p = pd.read_csv(FILENAMES['plantas'])
        df_c = pd.read_csv(FILENAMES['centros'])
        df_j = pd.read_csv(FILENAMES['clientes'])
        
        tab1, tab2, tab3 = st.tabs(["🏭 Plantas", "📦 Centros de Distribución", "👥 Clientes"])
        
        with tab1:
            st.markdown("##### Edita los datos de plantas:")
            edited_p = st.data_editor(df_p, num_rows="dynamic", use_container_width=True, key='editor_p')
            if st.button("💾 Guardar Cambios - Plantas", key='save_p'):
                edited_p.to_csv(FILENAMES['plantas'], index=False)
                st.success("✅ Plantas actualizadas")
        
        with tab2:
            st.markdown("##### Edita los datos de centros:")
            edited_c = st.data_editor(df_c, num_rows="dynamic", use_container_width=True, key='editor_c')
            if st.button("💾 Guardar Cambios - Centros", key='save_c'):
                edited_c.to_csv(FILENAMES['centros'], index=False)
                st.success("✅ Centros actualizados")
        
        with tab3:
            st.markdown("##### Edita los datos de clientes:")
            edited_j = st.data_editor(df_j, num_rows="dynamic", use_container_width=True, key='editor_j')
            if st.button("💾 Guardar Cambios - Clientes", key='save_j'):
                edited_j.to_csv(FILENAMES['clientes'], index=False)
                st.success("✅ Clientes actualizados")
        
        st.markdown("---")
        
        # BOTÓN DE OPTIMIZAR
        st.markdown("### 🚀 Ejecutar Optimización")
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            if st.button("⚡ OPTIMIZAR RED", use_container_width=True, type="primary"):
                with st.spinner("🔄 Resolviendo modelo matemático..."):
                    resultado = resolver_modelo()
                    if resultado:
                        st.session_state['resultado'] = resultado
                        st.success("✅ ¡Optimización completada!")
                        st.rerun()
                    else:
                        st.error("❌ No se encontró solución factible")
    
    except Exception as e:
        st.error(f"Error al cargar datos: {e}")

else:
    st.info("👈 Selecciona una fuente de datos en el panel izquierdo para comenzar")

# ============================================================================
# RESULTADOS CON FILTROS COMPLETOS
# ============================================================================

# Solo necesito cambiar la sección de RESULTADOS - aquí está el fix:

# Reemplaza toda la sección desde "if 'resultado' in st.session_state:" hasta el footer

if 'resultado' in st.session_state:
    res = st.session_state['resultado']
    
    st.markdown("---")
    st.markdown("## 📈 Resultados de la Optimización")
    
    # FILTROS GLOBALES
    st.markdown("### 🔍 Panel de Filtros Avanzados")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        productos_filter = st.multiselect(
            "**Productos:**",
            options=res['K'],
            default=res['K'],
            key='filter_productos'
        )
    
    with col2:
        plantas_filter = st.multiselect(
            "**Plantas:**",
            options=res['P'],
            default=res['P'],
            key='filter_plantas'
        )
    
    with col3:
        centros_filter = st.multiselect(
            "**Centros:**",
            options=res['C'],
            default=res['C'],
            key='filter_centros'
        )
    
    with col4:
        # ARREGLADO: Ahora por defecto TODOS los clientes están seleccionados
        clientes_filter = st.multiselect(
            "**Clientes:**",
            options=res['J'],
            default=res['J'],  # TODOS seleccionados por defecto
            key='filter_clientes'
        )
    
    with col5:
        top_n = st.slider(
            "**Top N Rutas:**",
            min_value=3,
            max_value=50,
            value=10,
            key='filter_topn'
        )
    
    # DETECTAR SI TODOS LOS FILTROS ESTÁN EN DEFAULT - ARREGLADO
    todos_productos = len(productos_filter) == len(res['K']) and set(productos_filter) == set(res['K'])
    todas_plantas = len(plantas_filter) == len(res['P']) and set(plantas_filter) == set(res['P'])
    todos_centros = len(centros_filter) == len(res['C']) and set(centros_filter) == set(res['C'])
    todos_clientes = len(clientes_filter) == len(res['J']) and set(clientes_filter) == set(res['J'])
    
    sin_filtros = todos_productos and todas_plantas and todos_centros and todos_clientes
    
    # SI NO HAY FILTROS, USAR VALORES ORIGINALES DIRECTAMENTE
    m = res['modelo']
    if sin_filtros:
        costo_filt_total = res['total']
        prod_filt = res['c_prod']
        costo_filt_pc = res['c_tpc']
        costo_filt_cj = res['c_tcj']
        df_pc_filt = res['flujos_pc'].copy()
        df_cj_filt = res['flujos_cj'].copy()
    else:
        # APLICAR FILTROS Y RECALCULAR
        df_pc_filt = res['flujos_pc'][
            (res['flujos_pc']['Producto'].isin(productos_filter)) &
            (res['flujos_pc']['Planta'].isin(plantas_filter)) &
            (res['flujos_pc']['Centro'].isin(centros_filter))
        ].copy()
        
        df_cj_filt = res['flujos_cj'][
            (res['flujos_cj']['Producto'].isin(productos_filter)) &
            (res['flujos_cj']['Centro'].isin(centros_filter)) &
            (res['flujos_cj']['Cliente'].isin(clientes_filter))
        ].copy()
        
        # Recalcular costos de transporte
        costo_filt_pc = df_pc_filt['Costo_Total'].sum()
        costo_filt_cj = df_cj_filt['Costo_Total'].sum()
        
        # Calcular producción filtrada CORRECTAMENTE
        m = res['modelo']
        cost_prod_dict = res['cost_prod_dict']
        prod_filt = 0
        
        for p in plantas_filter:
            for c in centros_filter:
                for k in productos_filter:
                    if (p,c,k) in m.x:
                        cantidad = value(m.x[p,c,k])
                        costo_produccion = cost_prod_dict.get((p,k), 0)
                        prod_filt += costo_produccion * cantidad
        
        costo_filt_total = prod_filt + costo_filt_pc + costo_filt_cj
    
    st.markdown("---")
    
    # MÉTRICAS PREMIUM
    col1, col2, col3, col4 = st.columns(4)
    
    # MÉTRICAS PREMIUM - SIMPLIFICADAS

    with col1:
        st.markdown(f"""
        <div class="metric-glass">
            <div class="metric-label">💰 Costo Total</div>
            <div class="metric-value">${costo_filt_total:,.0f}</div>
            <div class="metric-subtitle">Según filtros aplicados</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        pct_prod = (prod_filt/costo_filt_total*100) if costo_filt_total > 0 else 0
        st.markdown(f"""
        <div class="metric-glass">
            <div class="metric-label">🏭 Producción</div>
            <div class="metric-value">${prod_filt:,.0f}</div>
            <div class="metric-subtitle">{pct_prod:.1f}% del total</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        pct_pc = (costo_filt_pc/costo_filt_total*100) if costo_filt_total > 0 else 0
        st.markdown(f"""
        <div class="metric-glass">
            <div class="metric-label">🚚 Transp. P→C</div>
            <div class="metric-value">${costo_filt_pc:,.0f}</div>
            <div class="metric-subtitle">{len(df_pc_filt)} rutas | {pct_pc:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        pct_cj = (costo_filt_cj/costo_filt_total*100) if costo_filt_total > 0 else 0
        st.markdown(f"""
        <div class="metric-glass">
            <div class="metric-label">📦 Transp. C→J</div>
            <div class="metric-value">${costo_filt_cj:,.0f}</div>
            <div class="metric-subtitle">{len(df_cj_filt)} rutas | {pct_cj:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # TABS DE ANÁLISIS COMPLETOS
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Análisis de Costos",
        "🌊 Flujos de Distribución",
        "🏆 Top Rutas Críticas",
        "📈 Utilización de Capacidades",
        "📋 Datos Detallados"
    ])
    
    # TAB 1: ANÁLISIS DE COSTOS MEJORADO
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("##### 🥧 Distribución de Costos")
            df_costos = pd.DataFrame({
                'Categoría': ['Producción', 'Transp. P→C', 'Transp. C→J'],
                'Costo': [prod_filt, costo_filt_pc, costo_filt_cj]
            })
            
            fig_pie = go.Figure(data=[go.Pie(
                labels=df_costos['Categoría'],
                values=df_costos['Costo'],
                hole=0.5,
                marker=dict(
                    colors=[COLORS['fern'], COLORS['dry_sage'], COLORS['hunter_green']],
                    line=dict(color='white', width=3)
                ),
                textposition='inside',
                textinfo='percent+label',
                textfont=dict(size=14, family='Montserrat', color='white', weight='bold'),
                hovertemplate='<b>%{label}</b><br>$%{value:,.0f}<br>%{percent}<extra></extra>'
            )])
            
            fig_pie.update_layout(
                showlegend=True,
                height=400,
                font=dict(family="Montserrat", size=12),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1.1)
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            st.markdown("##### 📊 Comparativo de Categorías")
            fig_bar = go.Figure(data=[go.Bar(
                x=df_costos['Categoría'],
                y=df_costos['Costo'],
                text=df_costos['Costo'],
                texttemplate='$%{text:,.0f}',
                textposition='outside',
                textfont=dict(size=14, family='Montserrat', weight='bold'),
                marker=dict(
                    color=df_costos['Costo'],
                    colorscale=[[0, COLORS['dry_sage']], [0.5, COLORS['fern']], [1, COLORS['hunter_green']]],
                    line=dict(color=COLORS['pine_teal'], width=2)
                ),
                hovertemplate='<b>%{x}</b><br>$%{y:,.0f}<extra></extra>'
            )])
            
            fig_bar.update_layout(
                showlegend=False,
                height=400,
                font=dict(family="Montserrat", size=12),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                yaxis=dict(title="Costo ($)", gridcolor='rgba(0,0,0,0.1)'),
                xaxis=dict(title="")
            )
            st.plotly_chart(fig_bar, use_container_width=True)
        
        # Breakdown por producto
        st.markdown("##### 💡 Desglose por Producto")
        if len(productos_filter) > 0:
            costos_prod = []
            for prod in productos_filter:
                c_pc = df_pc_filt[df_pc_filt['Producto']==prod]['Costo_Total'].sum()
                c_cj = df_cj_filt[df_cj_filt['Producto']==prod]['Costo_Total'].sum()
                costos_prod.append({'Producto': prod, 'P→C': c_pc, 'C→J': c_cj, 'Total': c_pc+c_cj})
            
            df_costos_prod = pd.DataFrame(costos_prod)
            
            fig_prod = go.Figure()
            fig_prod.add_trace(go.Bar(
                name='P→C', x=df_costos_prod['Producto'], y=df_costos_prod['P→C'],
                marker_color=COLORS['fern'], text=df_costos_prod['P→C'],
                texttemplate='$%{text:,.0f}', textposition='inside',
                textfont=dict(color='white', weight='bold')
            ))
            fig_prod.add_trace(go.Bar(
                name='C→J', x=df_costos_prod['Producto'], y=df_costos_prod['C→J'],
                marker_color=COLORS['dry_sage'], text=df_costos_prod['C→J'],
                texttemplate='$%{text:,.0f}', textposition='inside',
                textfont=dict(color='white', weight='bold')
            ))
            
            fig_prod.update_layout(
                barmode='stack',
                height=350,
                font=dict(family="Montserrat", size=12),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                yaxis=dict(title="Costo ($)", gridcolor='rgba(0,0,0,0.1)'),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            st.plotly_chart(fig_prod, use_container_width=True)
    
    # TAB 2: FLUJOS MEJORADO
    with tab2:
        st.markdown("##### 🌊 Diagrama de Sankey - Flujo Completo de la Red")
        
        if len(productos_filter) > 0 and len(plantas_filter) > 0 and len(centros_filter) > 0:
            P_f, C_f, J_f = plantas_filter, centros_filter, clientes_filter
            
            labels = P_f + C_f + J_f
            idx = {l: i for i, l in enumerate(labels)}
            s, t, v, c, custom = [], [], [], [], []
            
            # P → C
            for p in P_f:
                for cen in C_f:
                    val = sum(value(m.x[p,cen,k]) for k in productos_filter if (p,cen,k) in m.x)
                    if val > 1:
                        s.append(idx[p])
                        t.append(idx[cen])
                        v.append(val)
                        c.append(f"rgba(88, 129, 87, 0.5)")
                        custom.append(f"{p} → {cen}: {val:,.0f} unidades")
            
            # C → J (Top N filtrado)
            rutas = []
            for cen in C_f:
                for cli in J_f:
                    val = sum(value(m.y[cen,cli,k]) for k in productos_filter if (cen,cli,k) in m.y)
                    if val > 1:
                        rutas.append((cen, cli, val))
            rutas = sorted(rutas, key=lambda x: x[2], reverse=True)[:top_n*3]
            
            for cen, cli, val in rutas:
                s.append(idx[cen])
                t.append(idx[cli])
                v.append(val)
                c.append(f"rgba(163, 177, 138, 0.5)")
                custom.append(f"{cen} → {cli}: {val:,.0f} unidades")
            
            fig_sankey = go.Figure(go.Sankey(
                node=dict(
                    pad=20,
                    thickness=25,
                    line=dict(color=COLORS['pine_teal'], width=2),
                    label=labels,
                    color=COLORS['hunter_green'],
                    customdata=labels,
                    hovertemplate='<b>%{customdata}</b><extra></extra>'
                ),
                link=dict(
                    source=s,
                    target=t,
                    value=v,
                    color=c,
                    customdata=custom,
                    hovertemplate='%{customdata}<extra></extra>'
                )
            ))
            
            fig_sankey.update_layout(
                height=700,
                font=dict(family="Montserrat", size=13, color=COLORS['pine_teal']),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_sankey, use_container_width=True)
        else:
            st.warning("⚠️ Selecciona al menos un elemento de cada categoría en los filtros para visualizar el diagrama")
    
    # TAB 3: TOP RUTAS MEJORADO
    with tab3:
        st.markdown("##### 🏆 Rutas Más Costosas")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"###### 🏭→📦 Top {top_n} Rutas Planta-Centro")
            if len(df_pc_filt) > 0:
                top_pc = df_pc_filt.nlargest(top_n, 'Costo_Total')
                
                fig_pc = go.Figure(go.Bar(
                    y=[f"{r['Planta']}→{r['Centro']}<br>({r['Producto']})" for _, r in top_pc.iterrows()],
                    x=top_pc['Costo_Total'],
                    orientation='h',
                    text=top_pc['Costo_Total'],
                    texttemplate='$%{text:,.0f}',
                    textposition='outside',
                    textfont=dict(size=11, weight='bold'),
                    marker=dict(
                        color=top_pc['Costo_Total'],
                        colorscale=[[0, COLORS['dry_sage']], [1, COLORS['hunter_green']]],
                        line=dict(color=COLORS['pine_teal'], width=1)
                    ),
                    hovertemplate='<b>%{y}</b><br>Costo: $%{x:,.0f}<extra></extra>'
                ))
                
                fig_pc.update_layout(
                    height=400,
                    font=dict(family="Montserrat", size=11),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    xaxis=dict(title="Costo ($)", gridcolor='rgba(0,0,0,0.1)'),
                    yaxis=dict(title=""),
                    showlegend=False
                )
                st.plotly_chart(fig_pc, use_container_width=True)
                
                # Tabla detallada
                st.dataframe(
                    top_pc[['Planta', 'Centro', 'Producto', 'Cantidad', 'Costo_Total']].style.format({
                        'Cantidad': '{:,.0f}',
                        'Costo_Total': '${:,.0f}'
                    }).background_gradient(subset=['Costo_Total'], cmap='Greens'),
                    use_container_width=True,
                    height=250
                )
            else:
                st.info("No hay rutas P→C con los filtros seleccionados")
        
        with col2:
            st.markdown(f"###### 📦→👥 Top {top_n} Rutas Centro-Cliente")
            if len(df_cj_filt) > 0:
                top_cj = df_cj_filt.nlargest(top_n, 'Costo_Total')
                
                fig_cj = go.Figure(go.Bar(
                    y=[f"{r['Centro']}→{r['Cliente']}<br>({r['Producto']})" for _, r in top_cj.iterrows()],
                    x=top_cj['Costo_Total'],
                    orientation='h',
                    text=top_cj['Costo_Total'],
                    texttemplate='$%{text:,.0f}',
                    textposition='outside',
                    textfont=dict(size=11, weight='bold'),
                    marker=dict(
                        color=top_cj['Costo_Total'],
                        colorscale=[[0, COLORS['dry_sage']], [1, COLORS['fern']]],
                        line=dict(color=COLORS['pine_teal'], width=1)
                    ),
                    hovertemplate='<b>%{y}</b><br>Costo: $%{x:,.0f}<extra></extra>'
                ))
                
                fig_cj.update_layout(
                    height=400,
                    font=dict(family="Montserrat", size=11),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    xaxis=dict(title="Costo ($)", gridcolor='rgba(0,0,0,0.1)'),
                    yaxis=dict(title=""),
                    showlegend=False
                )
                st.plotly_chart(fig_cj, use_container_width=True)
                
                # Tabla detallada
                st.dataframe(
                    top_cj[['Centro', 'Cliente', 'Producto', 'Cantidad', 'Costo_Total']].style.format({
                        'Cantidad': '{:,.0f}',
                        'Costo_Total': '${:,.0f}'
                    }).background_gradient(subset=['Costo_Total'], cmap='Greens'),
                    use_container_width=True,
                    height=250
                )
            else:
                st.info("No hay rutas C→J con los filtros seleccionados")
    
    # TAB 4: UTILIZACIÓN DE CAPACIDADES
    with tab4:
        st.markdown("##### 📊 Análisis de Utilización de Capacidades")
        
        df_plantas = res['df_plantas'].copy()
        
        # Calcular utilización para plantas filtradas
        util_plantas = []
        for p in plantas_filter:
            for k in productos_filter:
                try:
                    cap = df_plantas[(df_plantas['Planta']==p) & (df_plantas['Producto']==k)]['Capacidad_Produccion'].values[0]
                    usado = sum(value(m.x[p,c,k]) for c in res['C'] if (p,c,k) in m.x)
                    util_plantas.append({
                        'Planta': p,
                        'Producto': k,
                        'Capacidad': cap,
                        'Usado': usado,
                        'Disponible': cap - usado,
                        'Utilización %': (usado/cap*100) if cap > 0 else 0
                    })
                except:
                    continue
        
        if len(util_plantas) > 0:
            df_util_p = pd.DataFrame(util_plantas)
            
            # Gráfico de utilización
            fig_util = px.bar(
                df_util_p,
                x='Planta',
                y='Utilización %',
                color='Producto',
                barmode='group',
                text='Utilización %',
                color_discrete_sequence=[COLORS['fern'], COLORS['dry_sage'], COLORS['hunter_green'], COLORS['pine_teal']],
                hover_data=['Usado', 'Capacidad', 'Disponible']
            )
            
            fig_util.update_traces(
                texttemplate='%{text:.1f}%',
                textposition='outside',
                textfont=dict(size=11, weight='bold')
            )
            
            fig_util.update_layout(
                height=400,
                font=dict(family="Montserrat", size=12),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                yaxis=dict(title="Utilización (%)", gridcolor='rgba(0,0,0,0.1)', range=[0, max(105, df_util_p['Utilización %'].max()+10)]),
                xaxis=dict(title="Planta"),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            
            # Línea de referencia al 100%
            fig_util.add_hline(
                y=100, 
                line_dash="dash", 
                line_color=COLORS['hunter_green'], 
                line_width=2,
                annotation_text="Capacidad Máxima", 
                annotation_position="right"
            )
            
            st.plotly_chart(fig_util, use_container_width=True)
            
            # Estadísticas y tabla
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.markdown("###### 📌 Estadísticas Clave")
                avg_util = df_util_p['Utilización %'].mean()
                max_util = df_util_p['Utilización %'].max()
                min_util = df_util_p['Utilización %'].min()
                
                st.metric("Utilización Promedio", f"{avg_util:.1f}%", 
                         delta=f"{avg_util-50:.1f}% vs target 50%")
                st.metric("Máxima Utilización", f"{max_util:.1f}%",
                         delta="⚠️ Sobre capacidad" if max_util > 100 else "✅ OK")
                st.metric("Mínima Utilización", f"{min_util:.1f}%",
                         delta="⚠️ Subutilizado" if min_util < 30 else "✅ OK")
            
            with col2:
                st.markdown("###### 📋 Detalle de Utilización")
                st.dataframe(
                    df_util_p.style.format({
                        'Capacidad': '{:,.0f}',
                        'Usado': '{:,.0f}',
                        'Disponible': '{:,.0f}',
                        'Utilización %': '{:.1f}%'
                    }).background_gradient(subset=['Utilización %'], cmap='RdYlGn', vmin=0, vmax=100),
                    use_container_width=True,
                    height=300
                )
        else:
            st.info("No hay datos de utilización con los filtros seleccionados")
    
    # TAB 5: DATOS DETALLADOS
    with tab5:
        st.markdown("##### 📋 Tablas de Datos Completas")
        
        subtab1, subtab2 = st.tabs(["🏭→📦 Flujos Planta-Centro", "📦→👥 Flujos Centro-Cliente"])
        
        with subtab1:
            st.markdown(f"**Total de rutas filtradas:** {len(df_pc_filt)} | **Costo total:** ${costo_filt_pc:,.0f}")
            
            if len(df_pc_filt) > 0:
                st.dataframe(
                    df_pc_filt.sort_values('Costo_Total', ascending=False).style.format({
                        'Cantidad': '{:,.2f}',
                        'Costo_Unit': '${:,.2f}',
                        'Costo_Total': '${:,.2f}'
                    }).background_gradient(subset=['Costo_Total'], cmap='Greens'),
                    use_container_width=True,
                    height=500
                )
                
                # Botón de descarga
                csv_pc = df_pc_filt.to_csv(index=False).encode('utf-8')
                st.download_button(
                    "📥 Descargar CSV Completo",
                    csv_pc,
                    "flujos_planta_centro_filtrado.csv",
                    "text/csv",
                    key='download_pc_tab'
                )
            else:
                st.info("No hay flujos P→C con los filtros actuales")
        
        with subtab2:
            st.markdown(f"**Total de rutas filtradas:** {len(df_cj_filt)} | **Costo total:** ${costo_filt_cj:,.0f}")
            
            if len(df_cj_filt) > 0:
                st.dataframe(
                    df_cj_filt.sort_values('Costo_Total', ascending=False).style.format({
                        'Cantidad': '{:,.2f}',
                        'Costo_Unit': '${:,.2f}',
                        'Costo_Total': '${:,.2f}'
                    }).background_gradient(subset=['Costo_Total'], cmap='Greens'),
                    use_container_width=True,
                    height=500
                )
                
                # Botón de descarga
                csv_cj = df_cj_filt.to_csv(index=False).encode('utf-8')
                st.download_button(
                    "📥 Descargar CSV Completo",
                    csv_cj,
                    "flujos_centro_cliente_filtrado.csv",
                    "text/csv",
                    key='download_cj_tab'
                )
            else:
                st.info("No hay flujos C→J con los filtros actuales")

# Footer
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; color: {COLORS['hunter_green']}; font-size: 0.9rem; padding: 1rem;">
    <p><strong>Network Optimizer Pro</strong> | Desarrollado para UACJ MIAAD<br>
    Equipo: Javier Rebull, Manuel Flores Cacho, Patricia María Rosas Calderón</p>
</div>
""", unsafe_allow_html=True)