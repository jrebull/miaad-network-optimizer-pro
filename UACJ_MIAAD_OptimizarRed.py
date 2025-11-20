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
    page_title="Network Optimizer Pro",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# TEMA Y ESTILOS (CSS MEJORADO)
# ============================================================================
# Paleta de colores refinada
COLORS = {
    'bg_dark': '#1a1c20',
    'bg_card': '#2d3035',
    'primary': '#4ade80',      # Verde vibrante
    'secondary': '#22c55e',    # Verde sólido
    'accent': '#86efac',       # Verde claro
    'text_main': '#f3f4f6',
    'text_sub': '#9ca3af',
    'border': '#374151',
    'success': '#34d399',
    'warning': '#fbbf24',
    'error': '#f87171'
}

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Reset y Base */
    .stApp {{
        background-color: {COLORS['bg_dark']};
        font-family: 'Inter', sans-serif;
    }}
    
    h1, h2, h3, h4, h5, h6 {{
        color: {COLORS['text_main']} !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600;
    }}
    
    p, label, .stMarkdown {{
        color: {COLORS['text_sub']} !important;
    }}
    
    /* Sidebar */
    [data-testid="stSidebar"] {{
        background-color: {COLORS['bg_card']};
        border-right: 1px solid {COLORS['border']};
    }}
    
    /* Cards y Contenedores */
    .css-1r6slb0, .stDataFrame, .stPlotlyChart {{
        background-color: {COLORS['bg_card']};
        border-radius: 12px;
        border: 1px solid {COLORS['border']};
        padding: 1rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }}
    
    /* Botones */
    .stButton > button {{
        background: linear-gradient(135deg, {COLORS['secondary']} 0%, {COLORS['primary']} 100%);
        color: #000000;
        font-weight: 600;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 1.2rem;
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-size: 0.9rem;
    }}
    
    .stButton > button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(74, 222, 128, 0.3);
        color: #000000;
    }}
    
    /* Botón Secundario (Reset) */
    button[kind="secondary"] {{
        background: transparent !important;
        border: 1px solid {COLORS['error']} !important;
        color: {COLORS['error']} !important;
    }}
    
    /* Inputs */
    .stTextInput > div > div > input, .stNumberInput > div > div > input {{
        background-color: {COLORS['bg_dark']};
        color: {COLORS['text_main']};
        border: 1px solid {COLORS['border']};
        border-radius: 8px;
    }}
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 20px;
        background-color: transparent;
        border-bottom: 1px solid {COLORS['border']};
    }}
    
    .stTabs [data-baseweb="tab"] {{
        background-color: transparent;
        color: {COLORS['text_sub']};
        font-weight: 500;
        padding-bottom: 10px;
        border: none;
    }}
    
    .stTabs [aria-selected="true"] {{
        color: {COLORS['primary']} !important;
        border-bottom: 2px solid {COLORS['primary']} !important;
    }}
    
    /* Custom Header Class */
    .hero-header {{
        background: linear-gradient(135deg, rgba(34, 197, 94, 0.1) 0%, rgba(74, 222, 128, 0.05) 100%);
        border: 1px solid rgba(74, 222, 128, 0.2);
        border-radius: 16px;
        padding: 3rem 2rem;
        text-align: center;
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
    }}
    
    .hero-title {{
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(to right, {COLORS['primary']}, {COLORS['accent']});
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }}
    
    .hero-subtitle {{
        font-size: 1.1rem;
        color: {COLORS['text_sub']};
    }}
    
    /* Metric Cards */
    .metric-card {{
        background-color: {COLORS['bg_card']};
        border: 1px solid {COLORS['border']};
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        transition: transform 0.2s;
    }}
    
    .metric-card:hover {{
        border-color: {COLORS['primary']};
        transform: translateY(-2px);
    }}
    
    .metric-value {{
        font-size: 2rem;
        font-weight: 700;
        color: {COLORS['text_main']};
    }}
    
    .metric-label {{
        font-size: 0.85rem;
        color: {COLORS['text_sub']};
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 0.5rem;
    }}
    
    /* Data Editor */
    [data-testid="stDataEditor"] {{
        border: 1px solid {COLORS['border']};
        border-radius: 8px;
        overflow: hidden;
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
# LÓGICA DEL NEGOCIO (MANTENIDA)
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
    
    # Intentar resolver con GLPK, si falla, mostrar mensaje amigable
    try:
        solver = SolverFactory('glpk')
        if not solver.available():
            st.error("⚠️ El solver GLPK no está instalado o no se encuentra en el PATH.")
            return None
            
        res = solver.solve(m, tee=False)
        
        if res.solver.termination_condition == TerminationCondition.optimal:
            prod_val = sum(cost_prod.get((p,k),0) * value(m.x[p,c,k]) for p in P for c in C for k in K)
            trans_pc_val = sum(cost_tpc.get((p,c,k),0) * value(m.x[p,c,k]) for p in P for c in C for k in K)
            trans_cj_val = sum(cost_tcj.get((c,j,k),0) * value(m.y[c,j,k]) for c in C for j in J for k in K)
            
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
                'cost_prod_dict': cost_prod
            }
        else:
            return None
    except Exception as e:
        st.error(f"Error al ejecutar el solver: {str(e)}")
        return None

# ============================================================================
# INTERFAZ DE USUARIO
# ============================================================================

# Header Hero (Imagen Banner - Reducida al 50% y Centrada)
# Creamos 3 columnas: una para el espacio izquierdo (25%), una para la imagen (50%), y otra para el espacio derecho (25%)
col_left, col_image, col_right = st.columns([1, 2, 1]) # Proporción 1/4, 2/4, 1/4 = 25%, 50%, 25%

with col_image:
    st.image("https://iili.io/f2qf89p.png", use_container_width=True) # use_container_width=True ahora aplica al 50% de la página

# ============================================================================
# SIDEBAR
# ============================================================================

with st.sidebar:
    st.markdown("### ⚙️ Configuración")
    
    # Botón Reset con estilo de alerta
    if st.button("🔄 Resetear Todo", use_container_width=True, type="secondary"):
        resetear_todo()
        st.success("Sistema reseteado")
        st.rerun()
    
    st.markdown("---")
    
    fuente = st.radio(
        "Origen de Datos",
        ["🎲 Generar Datos", "📤 Subir CSV", "☁️ Google Drive"],
        index=0
    )
    
    st.markdown("---")
    
    if fuente == "🎲 Generar Datos":
        with st.expander("🏢 Red de Distribución", expanded=True):
            col1, col2 = st.columns(2)
            n_plantas = col1.number_input("Plantas", 2, 10, 3, key='n_p')
            n_centros = col2.number_input("Centros", 2, 15, 4, key='n_c')
            n_clientes = col1.number_input("Clientes", 5, 50, 15, key='n_cl')
            n_productos = col2.number_input("Productos", 1, 5, 2, key='n_pr')
        
        with st.expander("🏭 Producción"):
            col1, col2 = st.columns(2)
            cap_prod_min = col1.number_input("Cap Mín", 1000, 20000, 5000, 500, key='cp_min')
            cap_prod_max = col2.number_input("Cap Máx", cap_prod_min, 50000, 10000, 500, key='cp_max')
            costo_prod_min = col1.number_input("Costo Mín", 10, 100, 20, key='cprod_min')
            costo_prod_max = col2.number_input("Costo Máx", costo_prod_min, 200, 50, key='cprod_max')
        
        with st.expander("📦 Almacenamiento"):
            col1, col2 = st.columns(2)
            cap_alm_min = col1.number_input("Cap Mín ", 1000, 10000, 3000, 500, key='ca_min')
            cap_alm_max = col2.number_input("Cap Máx ", cap_alm_min, 20000, 6000, 500, key='ca_max')
        
        with st.expander("👥 Demanda"):
            col1, col2 = st.columns(2)
            demanda_min = col1.number_input("Mínima", 50, 1000, 200, 50, key='d_min')
            demanda_max = col2.number_input("Máxima", demanda_min, 2000, 800, 50, key='d_max')
        
        with st.expander("💰 Costos Transporte"):
            st.caption("Planta → Centro")
            col1, col2 = st.columns(2)
            costo_tpc_min = col1.number_input("Mín", 1, 50, 5, key='tpc_min')
            costo_tpc_max = col2.number_input("Máx", costo_tpc_min, 100, 15, key='tpc_max')
            
            st.caption("Centro → Cliente")
            col1, col2 = st.columns(2)
            costo_tcj_min = col1.number_input("Mín ", 1, 50, 5, key='tcj_min')
            costo_tcj_max = col2.number_input("Máx ", costo_tcj_min, 100, 20, key='tcj_max')
        
        config = {
            'n_plantas': n_plantas, 'n_centros': n_centros, 'n_clientes': n_clientes,
            'n_productos': n_productos, 'cap_prod_min': cap_prod_min, 'cap_prod_max': cap_prod_max,
            'cap_alm_min': cap_alm_min, 'cap_alm_max': cap_alm_max,
            'demanda_min': demanda_min, 'demanda_max': demanda_max,
            'costo_prod_min': costo_prod_min, 'costo_prod_max': costo_prod_max,
            'costo_tpc_min': costo_tpc_min, 'costo_tpc_max': costo_tpc_max,
            'costo_tcj_min': costo_tcj_min, 'costo_tcj_max': costo_tcj_max
        }
        
        if st.button("🎲 Generar Escenario", use_container_width=True):
            with st.spinner("Generando datos..."):
                generar_datos_configurables(config)
                st.session_state['datos_cargados'] = True
                st.success("Escenario generado")
                st.rerun()
    
    elif fuente == "📤 Subir CSV":
        st.info("Sube tus 5 archivos CSV requeridos")
        files = st.file_uploader("Archivos CSV", accept_multiple_files=True, type="csv", label_visibility="collapsed")
        if st.button("Procesar Archivos", use_container_width=True):
            if files and len(files) == 5:
                if identificar_y_guardar_archivos(files):
                    st.session_state['datos_cargados'] = True
                    st.success("Archivos cargados correctamente")
                    st.rerun()
                else:
                    st.error("No se pudieron identificar todos los archivos necesarios")
            else:
                st.warning("Por favor sube exactamente 5 archivos")
    
    elif fuente == "☁️ Google Drive":
        if st.button("Descargar desde Drive", use_container_width=True):
            with st.spinner("Conectando con Drive..."):
                descargar_drive()
                st.session_state['datos_cargados'] = True
                st.success("Datos descargados")
                st.rerun()

# ============================================================================
# ÁREA PRINCIPAL
# ============================================================================

if st.session_state.get('datos_cargados', False):
    
    try:
        df_p = pd.read_csv(FILENAMES['plantas'])
        df_c = pd.read_csv(FILENAMES['centros'])
        df_j = pd.read_csv(FILENAMES['clientes'])
        
        st.markdown("### 📝 Gestión de Datos")
        
        tab1, tab2, tab3 = st.tabs(["🏭 Plantas", "📦 Centros", "👥 Clientes"])
        
        with tab1:
            edited_p = st.data_editor(df_p, num_rows="dynamic", use_container_width=True, key='editor_p')
            if st.button("Guardar Plantas", key='save_p'):
                edited_p.to_csv(FILENAMES['plantas'], index=False)
                st.toast("Plantas actualizadas", icon="✅")
        
        with tab2:
            edited_c = st.data_editor(df_c, num_rows="dynamic", use_container_width=True, key='editor_c')
            if st.button("Guardar Centros", key='save_c'):
                edited_c.to_csv(FILENAMES['centros'], index=False)
                st.toast("Centros actualizados", icon="✅")
        
        with tab3:
            edited_j = st.data_editor(df_j, num_rows="dynamic", use_container_width=True, key='editor_j')
            if st.button("Guardar Clientes", key='save_j'):
                edited_j.to_csv(FILENAMES['clientes'], index=False)
                st.toast("Clientes actualizados", icon="✅")
        
        st.markdown("---")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🚀 EJECUTAR OPTIMIZACIÓN", use_container_width=True):
                with st.spinner("Optimizando red logística..."):
                    resultado = resolver_modelo()
                    if resultado:
                        st.session_state['resultado'] = resultado
                        st.success("¡Optimización exitosa!")
                        st.rerun()
                    else:
                        st.error("No se encontró solución factible o hubo un error en el solver")
    
    except Exception as e:
        st.error(f"Error al cargar datos: {e}")

else:
    st.markdown("""
    <div style="text-align: center; padding: 3rem; color: #6b7280;">
        <h3>👋 Bienvenido al Optimizador</h3>
        <p>Para comenzar, selecciona una fuente de datos en el menú lateral.</p>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# RESULTADOS
# ============================================================================

if 'resultado' in st.session_state:
    res = st.session_state['resultado']
    
    st.markdown("---")
    st.markdown("### 📊 Resultados del Análisis")
    
    # Filtros en un contenedor estilizado
    with st.container():
        st.markdown("#### 🔍 Filtros de Visualización")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            productos_filter = st.multiselect("Productos", options=res['K'], default=res['K'])
        with col2:
            plantas_filter = st.multiselect("Plantas", options=res['P'], default=res['P'])
        with col3:
            centros_filter = st.multiselect("Centros", options=res['C'], default=res['C'])
        with col4:
            clientes_filter = st.multiselect("Clientes", options=res['J'], default=res['J'])
            
        top_n = st.slider("Top Rutas a Mostrar", 3, 50, 10)

    # Lógica de filtrado
    todos_productos = len(productos_filter) == len(res['K']) and set(productos_filter) == set(res['K'])
    todas_plantas = len(plantas_filter) == len(res['P']) and set(plantas_filter) == set(res['P'])
    todos_centros = len(centros_filter) == len(res['C']) and set(centros_filter) == set(res['C'])
    todos_clientes = len(clientes_filter) == len(res['J']) and set(clientes_filter) == set(res['J'])
    sin_filtros = todos_productos and todas_plantas and todos_centros and todos_clientes
    
    m = res['modelo']
    if sin_filtros:
        costo_filt_total = res['total']
        prod_filt = res['c_prod']
        costo_filt_pc = res['c_tpc']
        costo_filt_cj = res['c_tcj']
        df_pc_filt = res['flujos_pc'].copy()
        df_cj_filt = res['flujos_cj'].copy()
    else:
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
        
        costo_filt_pc = df_pc_filt['Costo_Total'].sum()
        costo_filt_cj = df_cj_filt['Costo_Total'].sum()
        
        cost_prod_dict = res['cost_prod_dict']
        prod_filt = 0
        for p in plantas_filter:
            for c in centros_filter:
                for k in productos_filter:
                    if (p,c,k) in m.x:
                        cantidad = value(m.x[p,c,k])
                        prod_filt += cost_prod_dict.get((p,k), 0) * cantidad
        
        costo_filt_total = prod_filt + costo_filt_pc + costo_filt_cj

    # KPIs
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Costo Total</div>
            <div class="metric-value">${costo_filt_total:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        pct_prod = (prod_filt/costo_filt_total*100) if costo_filt_total > 0 else 0
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Producción</div>
            <div class="metric-value">${prod_filt:,.0f}</div>
            <div style="color: {COLORS['primary']}; font-size: 0.8rem;">{pct_prod:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        pct_pc = (costo_filt_pc/costo_filt_total*100) if costo_filt_total > 0 else 0
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Transp. P→C</div>
            <div class="metric-value">${costo_filt_pc:,.0f}</div>
            <div style="color: {COLORS['primary']}; font-size: 0.8rem;">{pct_pc:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        pct_cj = (costo_filt_cj/costo_filt_total*100) if costo_filt_total > 0 else 0
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Transp. C→J</div>
            <div class="metric-value">${costo_filt_cj:,.0f}</div>
            <div style="color: {COLORS['primary']}; font-size: 0.8rem;">{pct_cj:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Visualizaciones
    tab_viz1, tab_viz2, tab_viz3, tab_viz4 = st.tabs([
        "📈 Costos", "🌊 Flujos", "🏆 Top Rutas", "🏭 Capacidad"
    ])
    
    # Configuración común para gráficos
    layout_config = dict(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Inter", color=COLORS['text_sub']),
        margin=dict(t=30, l=10, r=10, b=10)
    )

    with tab_viz1:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("##### Distribución de Costos")
            df_costos = pd.DataFrame({
                'Categoría': ['Producción', 'Transp. P→C', 'Transp. C→J'],
                'Costo': [prod_filt, costo_filt_pc, costo_filt_cj]
            })
            fig_pie = go.Figure(data=[go.Pie(
                labels=df_costos['Categoría'],
                values=df_costos['Costo'],
                hole=0.6,
                marker=dict(colors=[COLORS['primary'], COLORS['secondary'], COLORS['accent']])
            )])
            fig_pie.update_layout(**layout_config, height=350)
            st.plotly_chart(fig_pie, use_container_width=True)
            
        with col2:
            st.markdown("##### Costos por Producto")
            if len(productos_filter) > 0:
                costos_prod = []
                for prod in productos_filter:
                    c_pc = df_pc_filt[df_pc_filt['Producto']==prod]['Costo_Total'].sum()
                    c_cj = df_cj_filt[df_cj_filt['Producto']==prod]['Costo_Total'].sum()
                    costos_prod.append({'Producto': prod, 'P→C': c_pc, 'C→J': c_cj})
                
                df_cp = pd.DataFrame(costos_prod)
                fig_bar = go.Figure()
                fig_bar.add_trace(go.Bar(name='P→C', x=df_cp['Producto'], y=df_cp['P→C'], marker_color=COLORS['primary']))
                fig_bar.add_trace(go.Bar(name='C→J', x=df_cp['Producto'], y=df_cp['C→J'], marker_color=COLORS['secondary']))
                fig_bar.update_layout(barmode='stack', **layout_config, height=350)
                st.plotly_chart(fig_bar, use_container_width=True)

    with tab_viz2:
        st.markdown("##### Diagrama de Sankey")
        if len(productos_filter) > 0 and len(plantas_filter) > 0 and len(centros_filter) > 0:
            labels = plantas_filter + centros_filter + clientes_filter
            idx = {l: i for i, l in enumerate(labels)}
            s, t, v, c = [], [], [], []
            
            # P -> C
            for p in plantas_filter:
                for cen in centros_filter:
                    val = sum(value(m.x[p,cen,k]) for k in productos_filter if (p,cen,k) in m.x)
                    if val > 1:
                        s.append(idx[p])
                        t.append(idx[cen])
                        v.append(val)
                        c.append("rgba(74, 222, 128, 0.4)")
            
            # C -> J (Top N)
            rutas_cj = []
            for cen in centros_filter:
                for cli in clientes_filter:
                    val = sum(value(m.y[cen,cli,k]) for k in productos_filter if (cen,cli,k) in m.y)
                    if val > 1:
                        rutas_cj.append((cen, cli, val))
            
            rutas_cj = sorted(rutas_cj, key=lambda x: x[2], reverse=True)[:top_n*3]
            for cen, cli, val in rutas_cj:
                s.append(idx[cen])
                t.append(idx[cli])
                v.append(val)
                c.append("rgba(34, 197, 94, 0.4)")
                
            fig_sankey = go.Figure(go.Sankey(
                node=dict(
                    pad=15, thickness=20,
                    line=dict(color="black", width=0.5),
                    label=labels,
                    color=COLORS['primary']
                ),
                link=dict(source=s, target=t, value=v, color=c)
            ))
            fig_sankey.update_layout(**layout_config, height=600)
            st.plotly_chart(fig_sankey, use_container_width=True)
        else:
            st.info("Selecciona elementos en los filtros para ver el diagrama")

    with tab_viz3:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("###### Top Rutas Planta → Centro")
            if not df_pc_filt.empty:
                top_pc = df_pc_filt.nlargest(top_n, 'Costo_Total')
                st.dataframe(
                    top_pc[['Planta', 'Centro', 'Producto', 'Cantidad', 'Costo_Total']].style.format({
                        'Cantidad': '{:,.0f}', 'Costo_Total': '${:,.0f}'
                    }).background_gradient(subset=['Costo_Total'], cmap='Greens'),
                    use_container_width=True
                )
        with col2:
            st.markdown("###### Top Rutas Centro → Cliente")
            if not df_cj_filt.empty:
                top_cj = df_cj_filt.nlargest(top_n, 'Costo_Total')
                st.dataframe(
                    top_cj[['Centro', 'Cliente', 'Producto', 'Cantidad', 'Costo_Total']].style.format({
                        'Cantidad': '{:,.0f}', 'Costo_Total': '${:,.0f}'
                    }).background_gradient(subset=['Costo_Total'], cmap='Greens'),
                    use_container_width=True
                )

    with tab_viz4:
        st.markdown("##### Utilización de Plantas")
        df_plantas = res['df_plantas']
        util_data = []
        for p in plantas_filter:
            for k in productos_filter:
                try:
                    cap = df_plantas[(df_plantas['Planta']==p) & (df_plantas['Producto']==k)]['Capacidad_Produccion'].values[0]
                    usado = sum(value(m.x[p,c,k]) for c in res['C'] if (p,c,k) in m.x)
                    util_data.append({'Planta': p, 'Producto': k, 'Uso %': (usado/cap*100) if cap > 0 else 0})
                except: pass
        
        if util_data:
            df_util = pd.DataFrame(util_data)
            fig_util = px.bar(df_util, x='Planta', y='Uso %', color='Producto', barmode='group',
                            color_discrete_sequence=[COLORS['primary'], COLORS['secondary']])
            fig_util.add_hline(y=100, line_dash="dash", line_color="white")
            fig_util.update_layout(**layout_config, height=400)
            st.plotly_chart(fig_util, use_container_width=True)



# --- FOOTER FINAL (NATIVO Y ROBUSTO) ---
st.markdown("---")

# 1. CABECERA: Logo y Título alineados
# Usamos columnas: una angosta para el logo (1.5) y una ancha para el texto (8.5)
col_logo, col_header = st.columns([1.5, 8.5])

with col_logo:
    # Logo de la UACJ
    st.image("https://www.uacj.mx/acerca_de/Imagen-Institucional-UACJ_files/Escudo%20uacj%202015-fondo%20negro.jpg", width=80)

with col_header:
    st.markdown("### 🚀 Optimización de Red Multinivel")
    st.caption("Sistema de Apoyo a la Decisión | Distribución Multiproducto")

st.write("") # Espacio vacío para separar

# 2. CONTENIDO: Dos columnas (Equipo y Academia)
c_team, c_info = st.columns(2)

with c_team:
    st.markdown("#### 👥 Equipo de Desarrollo")
    # Usamos Markdown estándar, es más limpio
    st.markdown("""
    * **Javier Augusto Rebull Saucedo** `263483`
    * **Manuel Flores Cacho** `263178`
    * **Patricia María Rosas Calderón** `261538`
    """)

with c_info:
    st.markdown("#### 🏫 Información Académica")
    st.markdown("""
    * **Programa:** MIAAD - UACJ
    * **Materia:** Analítica Prescriptiva
    * **Instructor:** Dr. Gilberto Rivera Zarate
    """)

# 3. PIE DE PÁGINA FINAL
st.markdown("---")
st.caption("📅 Última actualización: 19 de noviembre del 2025 | Network Optimizer Pro v2.0")