import streamlit as st
import pandas as pd
import numpy as np
from pyomo.environ import *
import tempfile
import os
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import random
import requests

st.set_page_config(
    page_title="UACJ MIAAD Network Optimizer",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items=None
)

# ============================================================================
# SISTEMA DE DISEÑO PROFESIONAL - Tema Claro y Legible
# ============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }
    
    code, .monospace {
        font-family: 'JetBrains Mono', monospace !important;
    }
    
    /* ─────────────── COLORES ─────────────── */
    :root {
        --primary: #1e40af;
        --primary-light: #3b82f6;
        --accent: #10b981;
        --accent-warn: #f59e0b;
        --accent-danger: #ef4444;
    }
    
    /* ─────────────── BASE STYLES ─────────────── */
    .main {
        background: #ffffff !important;
        color: #1f2937 !important;
    }
    
    /* ─────────────── HEADER ─────────────── */
    .header-container {
        background: linear-gradient(135deg, #3b82f6 0%, #1e40af 100%);
        border-radius: 16px;
        padding: 3rem 2.5rem;
        margin-bottom: 2.5rem;
        box-shadow: 0 4px 12px rgba(30, 64, 175, 0.15);
    }
    
    .header-container h1 {
        margin: 0 !important;
        font-size: 2.75rem !important;
        font-weight: 800 !important;
        color: #ffffff !important;
        letter-spacing: -0.5px;
        line-height: 1.2;
    }
    
    .header-container .subtitle {
        margin: 0.75rem 0 0 0 !important;
        font-size: 1.125rem !important;
        font-weight: 400 !important;
        color: rgba(255, 255, 255, 0.9) !important;
    }
    
    /* ─────────────── METRIC CARDS ─────────────── */
    .metric-card {
        background: #f8fafc;
        border: 2px solid #e2e8f0;
        border-left: 4px solid #3b82f6;
        border-radius: 12px;
        padding: 1.5rem;
        height: 100%;
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        border-left-color: #1e40af;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.1);
        transform: translateY(-2px);
        border-color: #cbd5e1;
    }
    
    .metric-icon {
        font-size: 1.75rem;
        margin-bottom: 0.5rem;
        color: #64748b;
    }
    
    .metric-label {
        font-size: 0.75rem !important;
        color: #64748b !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
        margin: 0 0 0.5rem 0 !important;
    }
    
    .metric-value {
        font-size: 2.25rem !important;
        font-weight: 800 !important;
        color: #1e40af !important;
        margin: 0 !important;
        line-height: 1;
        font-variant-numeric: tabular-nums;
    }
    
    /* ─────────────── BUTTONS ─────────────── */
    .stButton > button {
        background: #3b82f6 !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 600 !important;
        font-size: 0.9375rem !important;
        box-shadow: 0 2px 8px rgba(59, 130, 246, 0.2) !important;
        letter-spacing: 0.01em;
    }
    
    .stButton > button:hover {
        background: #1e40af !important;
        box-shadow: 0 4px 12px rgba(30, 64, 175, 0.3) !important;
        transform: translateY(-1px) !important;
    }
    
    /* ─────────────── TABS ─────────────── */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px !important;
        background: #f1f5f9;
        padding: 0.5rem !important;
        border-radius: 10px !important;
        border: 1px solid #e2e8f0;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: white !important;
        border-radius: 6px !important;
        padding: 0.625rem 1.25rem !important;
        font-weight: 500 !important;
        color: #64748b !important;
        font-size: 0.875rem !important;
        border: 1px solid #e2e8f0 !important;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: #f8fafc !important;
        color: #1e40af !important;
        border-color: #cbd5e1 !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: #3b82f6 !important;
        color: white !important;
        border-color: #1e40af !important;
        font-weight: 600 !important;
    }
    
    /* ─────────────── DATAFRAMES ─────────────── */
    .stDataFrame {
        border-radius: 10px !important;
        border: 1px solid #e2e8f0 !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1) !important;
    }
    
    /* ─────────────── SIDEBAR ─────────────── */
    [data-testid="stSidebar"] {
        background: #f8fafc !important;
        border-right: 1px solid #e2e8f0 !important;
    }
    
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #1e40af !important;
        font-weight: 700 !important;
    }
    
    [data-testid="stSidebar"] .stRadio > div {
        background: white;
        padding: 1rem !important;
        border-radius: 8px !important;
        border: 1px solid #e2e8f0 !important;
    }
    
    [data-testid="stSidebar"] input[type="number"],
    [data-testid="stSidebar"] .stNumberInput input {
        background: white !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 6px !important;
        color: #1f2937 !important;
        font-weight: 500 !important;
    }
    
    [data-testid="stSidebar"] input[type="number"]:focus,
    [data-testid="stSidebar"] .stNumberInput input:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
        outline: none !important;
    }
    
    [data-testid="stSidebar"] label {
        font-weight: 600 !important;
        color: #1f2937 !important;
        font-size: 0.875rem !important;
    }
    
    /* ─────────────── ALERTS ─────────────── */
    [data-testid="stSuccess"] {
        background: rgba(16, 185, 129, 0.1) !important;
        border: 1px solid #10b981 !important;
        border-radius: 8px !important;
        color: #047857 !important;
    }
    
    [data-testid="stError"] {
        background: rgba(239, 68, 68, 0.1) !important;
        border: 1px solid #ef4444 !important;
        border-radius: 8px !important;
        color: #dc2626 !important;
    }
    
    [data-testid="stInfo"] {
        background: rgba(59, 130, 246, 0.1) !important;
        border: 1px solid #3b82f6 !important;
        border-radius: 8px !important;
        color: #1e40af !important;
    }
    
    [data-testid="stWarning"] {
        background: rgba(245, 158, 11, 0.1) !important;
        border: 1px solid #f59e0b !important;
        border-radius: 8px !important;
        color: #b45309 !important;
    }
    
    /* ─────────────── HEADINGS ─────────────── */
    .main h2 {
        color: #1e40af !important;
        font-weight: 700 !important;
        padding-bottom: 0.75rem !important;
        border-bottom: 2px solid #e2e8f0;
        margin-bottom: 1.5rem !important;
        font-size: 1.75rem !important;
    }
    
    .main h3 {
        color: #1f2937 !important;
        font-weight: 600 !important;
        font-size: 1.25rem !important;
        margin-bottom: 1rem !important;
    }
    
    .main h4 {
        color: #1f2937 !important;
        font-weight: 600 !important;
    }
    
    /* ─────────────── DIVIDER ─────────────── */
    hr {
        border: none !important;
        height: 1px !important;
        background: #e2e8f0 !important;
        margin: 2rem 0 !important;
    }
    
    /* ─────────────── FOOTER ─────────────── */
    .footer-container {
        background: linear-gradient(135deg, #f1f5f9 0%, #e0e7ff 100%);
        border: 1px solid #cbd5e1;
        border-radius: 12px;
        padding: 2.5rem;
        margin-top: 3rem;
    }
    
    .footer-container h3 {
        color: #1e40af !important;
        margin: 0 0 1.5rem 0 !important;
        font-weight: 700 !important;
        font-size: 1.5rem !important;
    }
    
    .footer-container h4 {
        color: #1e40af !important;
        margin: 1.5rem 0 0.75rem 0 !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
    }
    
    .footer-container p {
        color: #475569 !important;
        margin: 0.5rem 0 !important;
        font-size: 0.9375rem !important;
        line-height: 1.6;
    }
    
    .team-member {
        color: #1f2937 !important;
        font-weight: 600 !important;
    }
    
    .matricula {
        color: #94a3b8 !important;
        font-size: 0.875rem !important;
    }
    
    /* ─────────────── COST CARDS ─────────────── */
    .cost-card-success {
        border-left-color: #10b981 !important;
    }
    
    .cost-card-primary {
        border-left-color: #3b82f6 !important;
    }
    
    .cost-card-warning {
        border-left-color: #f59e0b !important;
    }
    
    .cost-card-info {
        border-left-color: #06b6d4 !important;
    }
    
    /* ─────────────── SELECTBOX ─────────────── */
    [data-testid="stSelectbox"] {
        color: #1f2937 !important;
    }

</style>
""", unsafe_allow_html=True)

# ============================================================================
# SESSION STATE
# ============================================================================
if 'data' not in st.session_state:
    st.session_state.data = None
if 'modelo' not in st.session_state:
    st.session_state.modelo = None

# ============================================================================
# FUNCIONES
# ============================================================================

def generar_datos_aleatorios(num_plantas=3, num_centros=4, num_clientes=8, num_productos=5, seed=None):
    """Genera datos realistas y coherentes"""
    if seed:
        np.random.seed(seed)
        random.seed(seed)
    
    productos = [f"Producto_{i+1}" for i in range(num_productos)]
    plantas = [f"Planta_{i+1}" for i in range(num_plantas)]
    centros = [f"Centro_{i+1}" for i in range(num_centros)]
    clientes = [f"Cliente_{i+1}" for i in range(num_clientes)]
    
    df_productos = pd.DataFrame({
        'Producto': productos,
        'Descripcion': [f'Producto de categoría {i%3+1}' for i in range(num_productos)]
    })
    
    df_plantas = []
    for p in plantas:
        for k in productos:
            df_plantas.append({
                'Planta': p,
                'Producto': k,
                'Capacidad_Produccion': np.random.randint(500, 2000),
                'Costo_Produccion': round(np.random.uniform(10, 50), 2)
            })
    df_plantas = pd.DataFrame(df_plantas)
    
    df_centros = []
    for c in centros:
        for k in productos:
            df_centros.append({
                'Centro': c,
                'Producto': k,
                'Capacidad_Almacenamiento': np.random.randint(800, 3000),
                'Costo_Almacenamiento': round(np.random.uniform(2, 8), 2)
            })
    df_centros = pd.DataFrame(df_centros)
    
    df_clientes = []
    for j in clientes:
        for k in productos:
            df_clientes.append({
                'Cliente': j,
                'Producto': k,
                'Demanda': np.random.randint(100, 500)
            })
    df_clientes = pd.DataFrame(df_clientes)
    
    df_costos = []
    for p in plantas:
        for c in centros:
            for k in productos:
                df_costos.append({
                    'Planta': p,
                    'Centro': c,
                    'Producto': k,
                    'Costo_Plant_Centro': round(np.random.uniform(5, 25), 2),
                    'Cliente': np.random.choice(clientes),
                    'Costo_Centro_Cliente': round(np.random.uniform(3, 15), 2)
                })
    df_costos = pd.DataFrame(df_costos)
    
    return {
        'productos': df_productos,
        'plantas': df_plantas,
        'centros': df_centros,
        'clientes': df_clientes,
        'costos': df_costos
    }


def resolver_modelo_optimizacion(datos):
    """Resuelve el modelo de optimización"""
    try:
        df_productos = datos['productos']
        df_plantas = datos['plantas']
        df_centros = datos['centros']
        df_clientes = datos['clientes']
        df_costos = datos['costos']
        
        P = list(df_plantas['Planta'].unique())
        C = list(df_centros['Centro'].unique())
        J = list(df_clientes['Cliente'].unique())
        K = list(df_productos['Producto'].unique())
        
        demanda = {(row['Cliente'], row['Producto']): row['Demanda'] 
                   for _, row in df_clientes.iterrows()}
        
        cap_produccion = {(row['Planta'], row['Producto']): row['Capacidad_Produccion'] 
                          for _, row in df_plantas.iterrows()}
        
        cap_almacenamiento = {(row['Centro'], row['Producto']): row['Capacidad_Almacenamiento'] 
                              for _, row in df_centros.iterrows()}
        
        costo_produccion = {(row['Planta'], row['Producto']): row['Costo_Produccion'] 
                            for _, row in df_plantas.iterrows()}
        
        costo_almacenamiento = {(row['Centro'], row['Producto']): row.get('Costo_Almacenamiento', 0) 
                                for _, row in df_centros.iterrows()}
        
        costo_planta_centro = {}
        for (p, c, k), group in df_costos.groupby(['Planta', 'Centro', 'Producto']):
            try:
                val = group['Costo_Plant_Centro'].iloc[0]
                if pd.notna(p) and pd.notna(c) and pd.notna(val):
                    costo_planta_centro[(p, c, k)] = val
            except:
                pass
        
        costo_centro_cliente = {(c, j, k): group['Costo_Centro_Cliente'].iloc[0]
                                for (c, j, k), group in df_costos.groupby(['Centro', 'Cliente', 'Producto'])}
        
        modelo = ConcreteModel()
        modelo.P = Set(initialize=P)
        modelo.C = Set(initialize=C)
        modelo.J = Set(initialize=J)
        modelo.K = Set(initialize=K)
        
        modelo.x = Var(modelo.P, modelo.C, modelo.K, domain=NonNegativeReals)
        modelo.y = Var(modelo.C, modelo.J, modelo.K, domain=NonNegativeReals)
        
        def funcion_objetivo(m):
            costo_prod_transp = sum(
                (costo_produccion.get((p, k), 0) + costo_planta_centro.get((p, c, k), 0)) * m.x[p, c, k]
                for p in m.P for c in m.C for k in m.K
            )
            costo_dist = sum(
                costo_centro_cliente.get((c, j, k), 0) * m.y[c, j, k]
                for c in m.C for j in m.J for k in m.K
            )
            return costo_prod_transp + costo_dist
        
        modelo.objetivo = Objective(rule=funcion_objetivo, sense=minimize)
        
        def restriccion_demanda(m, j, k):
            if demanda.get((j, k), 0) > 0:
                return sum(m.y[c, j, k] for c in m.C) == demanda.get((j, k), 0)
            return Constraint.Skip
        
        modelo.satisfacer_demanda = Constraint(modelo.J, modelo.K, rule=restriccion_demanda)
        
        def restriccion_balance(m, c, k):
            return sum(m.x[p, c, k] for p in m.P) == sum(m.y[c, j, k] for j in m.J)
        
        modelo.balance_centros = Constraint(modelo.C, modelo.K, rule=restriccion_balance)
        
        def restriccion_capacidad_planta(m, p, k):
            if (p, k) in cap_produccion:
                return sum(m.x[p, c, k] for c in m.C) <= cap_produccion[(p, k)]
            return Constraint.Skip
        
        modelo.capacidad_plantas = Constraint(modelo.P, modelo.K, rule=restriccion_capacidad_planta)
        
        def restriccion_capacidad_centro(m, c, k):
            if (c, k) in cap_almacenamiento:
                return sum(m.y[c, j, k] for j in m.J) <= cap_almacenamiento[(c, k)]
            return Constraint.Skip
        
        modelo.capacidad_centros = Constraint(modelo.C, modelo.K, rule=restriccion_capacidad_centro)
        
        solver = SolverFactory('glpk')
        resultado = solver.solve(modelo, tee=False)
        
        if resultado.solver.termination_condition == TerminationCondition.optimal:
            info_extra = {
                'P': P, 'C': C, 'J': J, 'K': K,
                'demanda': demanda,
                'cap_produccion': cap_produccion,
                'cap_almacenamiento': cap_almacenamiento,
                'costo_produccion': costo_produccion,
                'costo_almacenamiento': costo_almacenamiento,
                'costo_planta_centro': costo_planta_centro,
                'costo_centro_cliente': costo_centro_cliente
            }
            return modelo, info_extra, resultado.solver.termination_condition
        else:
            return None, None, resultado.solver.termination_condition
    
    except Exception as e:
        st.error(f"Error construyendo el modelo: {str(e)}")
        return None, None, None


def calcular_desglose_costos(modelo, info_extra):
    """Calcula desglose detallado de costos"""
    P = info_extra['P']
    C = info_extra['C']
    J = info_extra['J']
    K = info_extra['K']
    costo_produccion = info_extra['costo_produccion']
    costo_planta_centro = info_extra['costo_planta_centro']
    costo_centro_cliente = info_extra['costo_centro_cliente']
    
    costo_prod = sum(
        costo_produccion.get((p, k), 0) * (value(modelo.x[p, c, k]) or 0)
        for p in P for c in C for k in K
    )
    
    costo_pc = sum(
        costo_planta_centro.get((p, c, k), 0) * (value(modelo.x[p, c, k]) or 0)
        for p in P for c in C for k in K
    )
    
    costo_cj = sum(
        costo_centro_cliente.get((c, j, k), 0) * (value(modelo.y[c, j, k]) or 0)
        for c in C for j in J for k in K
    )
    
    costo_total = value(modelo.objetivo)
    
    return {
        'produccion': round(costo_prod, 2),
        'transporte_pc': round(costo_pc, 2),
        'almacenamiento': 0,
        'transporte_cj': round(costo_cj, 2),
        'total': round(costo_total, 2)
    }


# ============================================================================
# HEADER
# ============================================================================
st.markdown("""
<div class="header-container">
    <h1>▸ Optimización de Redes Multinivel de Distribución Multiproducto</h1>
    <p class="subtitle">Programación para Analítica Prescriptiva y de Apoyo a la Decisión</p>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# SIDEBAR
# ============================================================================
with st.sidebar:
    st.markdown("## ▸ CARGA DE DATOS")
    st.markdown("---")
    
    data_source = st.radio(
        "Selecciona origen:",
        ["▹ Datos Aleatorios", "▹ Google Drive", "▹ Subir CSV"],
        label_visibility="collapsed"
    )
    
    if data_source == "▹ Datos Aleatorios":
        st.markdown("### ▸ Configuración")
        col1, col2 = st.columns(2)
        with col1:
            num_plantas = st.number_input("Plantas", 2, 10, 3, step=1)
            num_centros = st.number_input("Centros", 2, 15, 4, step=1)
        with col2:
            num_clientes = st.number_input("Clientes", 3, 20, 8, step=1)
            num_productos = st.number_input("Productos", 2, 10, 5, step=1)
        
        seed = st.number_input("Seed", 0, 10000, 42, step=1)
        
        if st.button("▸ Generar Datos", use_container_width=True, type="primary"):
            with st.spinner("Generando datos..."):
                st.session_state.data = generar_datos_aleatorios(
                    num_plantas, num_centros, num_clientes, num_productos, seed
                )
                st.success("✓ Datos generados correctamente")
                st.rerun()
    
    elif data_source == "▹ Google Drive":
        st.info("▸ Esta opción descargará un set de datos de ejemplo.")
        if st.button("▸ Descargar desde Drive", use_container_width=True, type="primary"):
            with st.spinner("Descargando datos..."):
                try:
                    archivos = {
                        'productos.csv': '1B1UGqYzLTE3uh_1-MdvuT22eAGA6BXNx',
                        'plantas.csv': '1Mq1C4Q5BXX-RUP6RyLlRDXMsLIxJPkMX',
                        'centros.csv': '1OxMfsW98iIfm8hqiul23Pmo8Iec1roX2',
                        'clientes.csv': '1v7UchVRnrKYPgYsir_0aCqk4W1Nj8o0O',
                        'costos.csv': '1Y4M_U7i_7k0-MVjU8itzGK4kYxzXdNFT'
                    }
                    
                    datos = {}
                    for nombre, file_id in archivos.items():
                        url = f'https://drive.google.com/uc?id={file_id}&export=download'
                        with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as tmp:
                            tmp_path = tmp.name
                        
                        try:
                            response = requests.get(url, timeout=30)
                            response.raise_for_status()
                            with open(tmp_path, 'wb') as f:
                                f.write(response.content)
                            datos[nombre.replace('.csv', '').lower()] = pd.read_csv(tmp_path)
                            os.remove(tmp_path)
                        except Exception as e:
                            st.error(f"Error descargando {nombre}")
                            if os.path.exists(tmp_path):
                                os.remove(tmp_path)
                            continue
                    
                    st.session_state.data = datos
                    st.success("✓ Datos cargados desde Drive")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {str(e)}")
    
    else:
        uploaded = st.file_uploader("Sube 5 CSVs", type=['csv'], accept_multiple_files=True)
        if uploaded and st.button("▸ Cargar Archivos", use_container_width=True, type="primary"):
            try:
                datos = {}
                for f in uploaded:
                    name = f.name.replace('.csv','').lower()
                    datos[name] = pd.read_csv(f)
                st.session_state.data = datos
                st.success("✓ Archivos cargados")
                st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")
    
    st.markdown("---")
    st.markdown("### ▸ ESTADO")
    
    if st.session_state.data:
        st.success("✓ Datos disponibles")
        if st.button("▸ Limpiar Datos", use_container_width=True):
            st.session_state.data = None
            st.session_state.modelo = None
            st.rerun()
    else:
        st.info("▸ Carga datos para comenzar")

# ============================================================================
# RESUMEN EJECUTIVO
# ============================================================================
if st.session_state.data:
    st.markdown("## ▸ RESUMEN EJECUTIVO")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        num_plantas = len(st.session_state.data.get('plantas', pd.DataFrame())['Planta'].unique())
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon">◼</div>
            <p class="metric-label">PLANTAS</p>
            <p class="metric-value">{num_plantas}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        num_centros = len(st.session_state.data.get('centros', pd.DataFrame())['Centro'].unique())
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon">◻</div>
            <p class="metric-label">CENTROS</p>
            <p class="metric-value">{num_centros}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        num_clientes = len(st.session_state.data.get('clientes', pd.DataFrame())['Cliente'].unique())
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon">◆</div>
            <p class="metric-label">CLIENTES</p>
            <p class="metric-value">{num_clientes}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        num_productos = len(st.session_state.data.get('productos', pd.DataFrame())['Producto'].unique())
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon">▣</div>
            <p class="metric-label">PRODUCTOS</p>
            <p class="metric-value">{num_productos}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        demanda_total = st.session_state.data.get('clientes', pd.DataFrame(columns=['Demanda']))['Demanda'].sum()
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon">▲</div>
            <p class="metric-label">DEMANDA</p>
            <p class="metric-value">{demanda_total:,.0f}</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("## ▸ DATOS DETALLADOS")
    
    tab_prod, tab_plant, tab_cent, tab_client, tab_costos = st.tabs(
        ["▹ Productos", "▹ Plantas", "▹ Centros", "▹ Clientes", "▹ Costos"]
    )
    
    with tab_prod:
        st.dataframe(st.session_state.data['productos'], use_container_width=True, hide_index=True)
    with tab_plant:
        st.dataframe(st.session_state.data['plantas'], use_container_width=True, hide_index=True)
    with tab_cent:
        st.dataframe(st.session_state.data['centros'], use_container_width=True, hide_index=True)
    with tab_client:
        st.dataframe(st.session_state.data['clientes'], use_container_width=True, hide_index=True)
    with tab_costos:
        st.dataframe(st.session_state.data['costos'], use_container_width=True, hide_index=True)
    
    st.markdown("---")
    st.markdown("## ▸ OPTIMIZACIÓN")
    
    col_btn = st.columns([1, 4, 1])
    with col_btn[1]:
        if st.button("▸ RESOLVER MODELO", use_container_width=True, type="primary"):
            with st.spinner("Resolviendo modelo de optimización..."):
                modelo, info_extra, status = resolver_modelo_optimizacion(st.session_state.data)
                
                if status == TerminationCondition.optimal:
                    st.session_state.modelo = (modelo, info_extra)
                    st.balloons()
                    st.success("✓ Modelo resuelto óptimamente")
                    st.rerun()
                else:
                    st.error(f"Error: No se encontró solución óptima, Por Favor Considere si es necesario una nueva planta o satisfacer a menos clientes/productos")

# ============================================================================
# RESULTADOS
# ============================================================================
if st.session_state.modelo:
    st.markdown("---")
    st.markdown("## ▸ RESULTADOS DE OPTIMIZACIÓN")
    
    modelo, info_extra = st.session_state.modelo
    costos = calcular_desglose_costos(modelo, info_extra)
    
    P = info_extra['P']
    C = info_extra['C']
    J = info_extra['J']
    K = info_extra['K']
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card cost-card-success">
            <p class="metric-label">● COSTO TOTAL</p>
            <p class="metric-value">${costos['total']:,.2f}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card cost-card-primary">
            <p class="metric-label">● PRODUCCIÓN</p>
            <p class="metric-value">${costos['produccion']:,.2f}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card cost-card-warning">
            <p class="metric-label">● TRANSPORTE P→C</p>
            <p class="metric-value">${costos['transporte_pc']:,.2f}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card cost-card-info">
            <p class="metric-label">● TRANSPORTE C→J</p>
            <p class="metric-value">${costos['transporte_cj']:,.2f}</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    col_graph, col_table = st.columns([2, 1])
    
    with col_graph:
        st.markdown("### ▸ Distribución de Costos")
        df_costos_pie = pd.DataFrame([
            {'Tipo': 'Producción', 'Costo': costos['produccion']},
            {'Tipo': 'Transporte P→C', 'Costo': costos['transporte_pc']},
            {'Tipo': 'Transporte C→J', 'Costo': costos['transporte_cj']},
        ])
        df_costos_pie = df_costos_pie[df_costos_pie['Costo'] > 0]
        
        fig = px.pie(
            df_costos_pie,
            names='Tipo',
            values='Costo',
            color='Tipo',
            color_discrete_map={
                'Producción': '#3b82f6',
                'Transporte P→C': '#f59e0b',
                'Transporte C→J': '#10b981'
            },
            hole=0.4
        )
        fig.update_traces(
            textposition='inside',
            textinfo='percent+label',
            marker=dict(line=dict(color='#ffffff', width=2)),
            textfont=dict(size=13, family='Inter', color='white')
        )
        fig.update_layout(
            height=400,
            showlegend=True,
            font=dict(color='#1f2937', size=12, family='Inter'),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            legend=dict(
                bgcolor='rgba(248, 250, 252, 0.8)',
                bordercolor='rgba(226, 232, 240, 0.5)',
                borderwidth=1
            )
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col_table:
        st.markdown("### ▸ Resumen")
        st.dataframe(
            pd.DataFrame([
                {'Concepto': k.replace('_', ' ').title(), 'Costo': f"${v:,.2f}"}
                for k, v in costos.items()
            ]),
            use_container_width=True,
            hide_index=True
        )
    
    st.markdown("---")
    st.markdown("## ▸ ANÁLISIS DETALLADO")
    
    tab_producto, tab_planta, tab_centro, tab_cliente, tab_flujos = st.tabs(
        ["▹ Por Producto", "▹ Por Planta", "▹ Por Centro", "▹ Por Cliente", "▹ Flujos"]
    )
    
    with tab_producto:
        st.markdown("### ▸ Análisis por Producto")
        producto_sel = st.selectbox("Selecciona producto:", K, key="prod_sel")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Producción por Planta")
            datos_prod = []
            for p in P:
                flujo = sum(value(modelo.x[p, c, producto_sel]) or 0 for c in C)
                cap = info_extra['cap_produccion'].get((p, producto_sel), 0)
                if cap > 0 or flujo > 0:
                    util = (flujo / cap) * 100 if cap > 0 else 0
                    datos_prod.append({
                        'Planta': p,
                        'Producción': round(flujo, 2),
                        'Capacidad': cap,
                        'Util. %': round(util, 1)
                    })
            
            if datos_prod:
                df_prod = pd.DataFrame(datos_prod)
                st.dataframe(df_prod, use_container_width=True, hide_index=True)
                
                fig = px.bar(
                    df_prod,
                    x='Planta',
                    y=['Producción', 'Capacidad'],
                    barmode='group',
                    title=f"Producción vs Capacidad - {producto_sel}",
                    color_discrete_map={'Producción': '#3b82f6', 'Capacidad': '#cbd5e1'}
                )
                fig.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#1f2937', family='Inter'),
                    hovermode='x unified'
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Sin datos de producción para este producto")
        
        with col2:
            st.markdown("#### Distribución a Centros")
            datos_dist = []
            for p in P:
                for c in C:
                    flujo = value(modelo.x[p, c, producto_sel]) or 0
                    if flujo > 0.1:
                        datos_dist.append({
                            'Planta': p,
                            'Centro': c,
                            'Cantidad': round(flujo, 2)
                        })
            
            if datos_dist:
                st.dataframe(pd.DataFrame(datos_dist), use_container_width=True, hide_index=True)
            else:
                st.info("Sin distribución de este producto")
    
    with tab_planta:
        st.markdown("### ▸ Análisis por Planta")
        planta_sel = st.selectbox("Selecciona planta:", P, key="plant_sel")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Productos a Producir")
            datos_prod_planta = []
            for k in K:
                flujo = sum(value(modelo.x[planta_sel, c, k]) or 0 for c in C)
                cap = info_extra['cap_produccion'].get((planta_sel, k), 0)
                if flujo > 0.1 or cap > 0:
                    util = (flujo / cap) * 100 if cap > 0 else 0
                    datos_prod_planta.append({
                        'Producto': k,
                        'Cantidad': round(flujo, 2),
                        'Capacidad': cap,
                        'Util. %': round(util, 1)
                    })
            
            if datos_prod_planta:
                st.dataframe(pd.DataFrame(datos_prod_planta), use_container_width=True, hide_index=True)
            else:
                st.info("Sin producción asignada")
        
        with col2:
            st.markdown("#### Envíos a Centros")
            datos_envios = []
            for c in C:
                for k in K:
                    flujo = value(modelo.x[planta_sel, c, k]) or 0
                    if flujo > 0.1:
                        datos_envios.append({
                            'Centro': c,
                            'Producto': k,
                            'Cantidad': round(flujo, 2)
                        })
            
            if datos_envios:
                st.dataframe(pd.DataFrame(datos_envios), use_container_width=True, hide_index=True)
            else:
                st.info("Sin envíos desde esta planta")
    
    with tab_centro:
        st.markdown("### ▸ Análisis por Centro")
        centro_sel = st.selectbox("Selecciona centro:", C, key="cent_sel")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Recepciones de Plantas")
            datos_recep = []
            for p in P:
                for k in K:
                    flujo = value(modelo.x[p, centro_sel, k]) or 0
                    if flujo > 0.1:
                        datos_recep.append({
                            'Planta': p,
                            'Producto': k,
                            'Cantidad': round(flujo, 2)
                        })
            
            if datos_recep:
                st.dataframe(pd.DataFrame(datos_recep), use_container_width=True, hide_index=True)
            else:
                st.info("Sin recepciones")
        
        with col2:
            st.markdown("#### Envíos a Clientes")
            datos_env_cli = []
            for j in J:
                for k in K:
                    flujo = value(modelo.y[centro_sel, j, k]) or 0
                    if flujo > 0.1:
                        datos_env_cli.append({
                            'Cliente': j,
                            'Producto': k,
                            'Cantidad': round(flujo, 2),
                            'Demanda': info_extra['demanda'].get((j, k), 0)
                        })
            
            if datos_env_cli:
                st.dataframe(pd.DataFrame(datos_env_cli), use_container_width=True, hide_index=True)
            else:
                st.info("Sin envíos a clientes")
    
    with tab_cliente:
        st.markdown("### ▸ Análisis por Cliente")
        cliente_sel = st.selectbox("Selecciona cliente:", J, key="client_sel")
        
        st.markdown("#### Recepciones desde Centros")
        datos_cliente = []
        for c in C:
            for k in K:
                flujo = value(modelo.y[c, cliente_sel, k]) or 0
                demanda_real = info_extra['demanda'].get((cliente_sel, k), 0)
                if flujo > 0.1 or demanda_real > 0:
                    datos_cliente.append({
                        'Centro': c if flujo > 0.1 else '-',
                        'Producto': k,
                        'Recibido': round(flujo, 2),
                        'Demanda': demanda_real,
                        'Cumpl. %': round((flujo / demanda_real * 100) if demanda_real > 0 else 0, 1)
                    })
        
        if datos_cliente:
            df_cliente = pd.DataFrame(datos_cliente).groupby(['Producto', 'Demanda']).agg(
                Recibido=('Recibido', 'sum'),
                Centros=('Centro', lambda x: ', '.join(x[x != '-']))
            ).reset_index()
            
            df_cliente['Cumpl. %'] = df_cliente.apply(
                lambda row: (row['Recibido'] / row['Demanda'] * 100) if row['Demanda'] > 0 else 0, axis=1
            )
            df_cliente['Cumpl. %'] = df_cliente['Cumpl. %'].round(1)
            
            st.dataframe(df_cliente[['Producto', 'Centros', 'Recibido', 'Demanda', 'Cumpl. %']], use_container_width=True, hide_index=True)
            
            fig = px.bar(
                df_cliente,
                x='Producto',
                y=['Recibido', 'Demanda'],
                barmode='group',
                title=f"Cumplimiento - {cliente_sel}",
                color_discrete_map={'Recibido': '#10b981', 'Demanda': '#f59e0b'}
            )
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#1f2937', family='Inter')
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Sin datos para este cliente")
    
    with tab_flujos:
        st.markdown("### ▸ Flujos Completos")
        flujo_tipo = st.radio("Tipo:", ["Planta → Centro", "Centro → Cliente"], horizontal=True, label_visibility="collapsed")
        
        if flujo_tipo == "Planta → Centro":
            datos_pc = []
            for p in P:
                for c in C:
                    for k in K:
                        flujo = value(modelo.x[p, c, k]) or 0
                        if flujo > 0.1:
                            datos_pc.append({
                                'Planta': p,
                                'Centro': c,
                                'Producto': k,
                                'Cantidad': round(flujo, 2)
                            })
            
            if datos_pc:
                st.dataframe(pd.DataFrame(datos_pc), use_container_width=True, hide_index=True)
                st.info(f"Total de flujos P→C: {len(datos_pc)}")
            else:
                st.info("Sin flujos Planta → Centro")
        
        else:
            datos_cj = []
            for c in C:
                for j in J:
                    for k in K:
                        flujo = value(modelo.y[c, j, k]) or 0
                        if flujo > 0.1:
                            datos_cj.append({
                                'Centro': c,
                                'Cliente': j,
                                'Producto': k,
                                'Cantidad': round(flujo, 2)
                            })
            
            if datos_cj:
                st.dataframe(pd.DataFrame(datos_cj), use_container_width=True, hide_index=True)
                st.info(f"Total de flujos C→J: {len(datos_cj)}")
            else:
                st.info("Sin flujos Centro → Cliente")

# ============================================================================
# FOOTER
# ============================================================================
st.markdown("---")

with st.container():
    st.markdown("### ▸ Optimización de una Red Multinivel de Distribución Multiproducto")
    
    st.markdown("**Equipo de Desarrollo**")
    st.write("👤 Javier Augusto Rebull Saucedo — Matrícula: 263483")
    st.write("👤 Manuel Flores Cacho — Matrícula: 263178")
    st.write("👤 Patricia María Rosas Calderón — Matrícula: 261538")
    
    st.markdown("**Información Académica**")
    col1, col2 = st.columns(2)
    with col1:
        st.write("🏫 **Programa:** Maestría en Inteligencia Artificial y Analítica de Datos (MIAAD)")
        st.write("🏛️ **Institución:** Universidad Autónoma de Ciudad Juárez")
    with col2:
        st.write("📁 **Materia:** Programación para la Analítica Prescriptiva y de la Decisión")
        st.write("‍📄 **Instructor:** Dr. Gilberto Rivera Zarate")
    
    st.write("📅 **Fecha:** 13 de noviembre del 2025")