import streamlit as st
import pandas as pd
import numpy as np
from pyomo.environ import *
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import gdown
import os
from io import BytesIO

st.set_page_config(
    page_title="Network Optimizer Pro - UACJ MIAAD",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items=None
)

# ============================================================================
# SISTEMA DE DISEÑO PROFESIONAL
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
    
    :root {
        --primary: #1e40af;
        --primary-light: #3b82f6;
        --accent: #10b981;
        --accent-warn: #f59e0b;
        --accent-danger: #ef4444;
    }
    
    .main {
        background: #ffffff !important;
        color: #1f2937 !important;
    }
    
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
        transition: all 0.2s ease !important;
    }
    
    .stButton > button:hover {
        background: #1e40af !important;
        box-shadow: 0 4px 12px rgba(30, 64, 175, 0.3) !important;
        transform: translateY(-1px) !important;
    }
    
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
    
    .stDataFrame {
        border-radius: 10px !important;
        border: 1px solid #e2e8f0 !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1) !important;
    }
    
    [data-testid="stSidebar"] {
        background: #f8fafc !important;
        border-right: 1px solid #e2e8f0 !important;
    }
    
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
        color: #b91c1c !important;
    }
    
    [data-testid="stInfo"] {
        background: rgba(59, 130, 246, 0.1) !important;
        border: 1px solid #3b82f6 !important;
        border-radius: 8px !important;
        color: #1e40af !important;
    }
    
    .run-button {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
        font-size: 1.1rem !important;
        padding: 1rem 2rem !important;
        margin: 1rem 0 !important;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# HEADER
# ============================================================================
st.markdown("""
<div class="header-container">
    <h1>🚀 Network Optimizer Pro</h1>
    <p class="subtitle">Sistema Avanzado de Optimización de Red de Distribución Multinivel | UACJ MIAAD</p>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# FUNCIONES AUXILIARES
# ============================================================================

def generar_datos_aleatorios(num_plantas, num_centros, num_clientes, num_productos):
    """Genera datos aleatorios para pruebas"""
    
    # Plantas
    plantas_data = []
    for p in range(1, num_plantas + 1):
        for k in range(1, num_productos + 1):
            plantas_data.append({
                'Planta': f'Planta_{p}',
                'Producto': f'Producto_{k}',
                'Capacidad_Produccion': np.random.randint(5000, 15000),
                'Costo_Produccion': round(np.random.uniform(10, 40), 2)
            })
    df_plantas = pd.DataFrame(plantas_data)
    
    # Centros
    centros_data = []
    for c in range(1, num_centros + 1):
        for k in range(1, num_productos + 1):
            centros_data.append({
                'Centro': f'Centro_{c}',
                'Producto': f'Producto_{k}',
                'Capacidad_Almacenamiento': np.random.randint(3000, 10000)
            })
    df_centros = pd.DataFrame(centros_data)
    
    # Clientes
    clientes_data = []
    for j in range(1, num_clientes + 1):
        for k in range(1, num_productos + 1):
            clientes_data.append({
                'Cliente': f'Cliente_{j}',
                'Producto': f'Producto_{k}',
                'Demanda': np.random.randint(50, 150)
            })
    df_clientes = pd.DataFrame(clientes_data)
    
    # Costos Plantas → Centros
    costos_pc_data = []
    for p in range(1, num_plantas + 1):
        for k in range(1, num_productos + 1):
            row = {'Planta': p, 'Producto ': k}
            for c in range(1, num_centros + 1):
                row[f'centro{c}'] = np.random.randint(3, 21)
            costos_pc_data.append(row)
    df_costos_pc = pd.DataFrame(costos_pc_data)
    
    # Costos Centros → Clientes
    costos_cj_data = []
    for k in range(1, num_productos + 1):
        for c in range(1, num_centros + 1):
            row = {'Producto': k, 'Centro': c}
            for j in range(1, num_clientes + 1):
                row[f'Cliente{j}'] = np.random.randint(2, 10)
            costos_cj_data.append(row)
    df_costos_cj = pd.DataFrame(costos_cj_data)
    
    return df_plantas, df_centros, df_clientes, df_costos_pc, df_costos_cj


def descargar_desde_drive():
    """Descarga archivos desde Google Drive"""
    archivos = {
        'plantas.csv': '1sm2UYkaeETYnh-nIykTHO3jrRUVzMbmP',
        'centros.csv': '1weTwr_qTtHqpTbscixP-6FweCpvySiOv',
        'clientes.csv': '1RRlz8U0f-TOmYL_1EovJJKlw-DC2YRLI',
        'Costos Plantas x CeDis.csv': '1JiYe20Y0lq5LJOHgNjlB0cOk7augwyZl',
        'Costos CeDis x Cliente.csv': '1MU5Y-vY_Xv_X7AlP_xYsw8p9opqVtkDX'
    }
    
    for nombre, file_id in archivos.items():
        if not os.path.exists(nombre):
            url = f'https://drive.google.com/uc?id={file_id}'
            gdown.download(url, nombre, quiet=True)
    
    df_plantas = pd.read_csv('plantas.csv')
    df_centros = pd.read_csv('centros.csv')
    df_clientes = pd.read_csv('clientes.csv')
    df_costos_pc = pd.read_csv('Costos Plantas x CeDis.csv')
    df_costos_cj = pd.read_csv('Costos CeDis x Cliente.csv')
    
    return df_plantas, df_centros, df_clientes, df_costos_pc, df_costos_cj


def resolver_modelo_optimizacion(df_plantas, df_centros, df_clientes, df_costos_plantas, df_costos_centros):
    """Resuelve el modelo de optimización"""
    
    # Extraer conjuntos únicos
    P = sorted(df_plantas['Planta'].unique())
    C = sorted(df_centros['Centro'].unique())
    J = sorted(df_clientes['Cliente'].unique())
    K = sorted(df_plantas['Producto'].unique())
    
    # Crear diccionarios de parámetros
    demanda = {}
    for _, row in df_clientes.iterrows():
        demanda[(row['Cliente'], row['Producto'])] = row['Demanda']
    
    cap_produccion = {}
    for _, row in df_plantas.iterrows():
        cap_produccion[(row['Planta'], row['Producto'])] = row['Capacidad_Produccion']
    
    cap_almacenamiento = {}
    for _, row in df_centros.iterrows():
        cap_almacenamiento[(row['Centro'], row['Producto'])] = row['Capacidad_Almacenamiento']
    
    costo_produccion = {}
    for _, row in df_plantas.iterrows():
        costo_produccion[(row['Planta'], row['Producto'])] = row['Costo_Produccion']
    
    # Costos Planta → Centro
    costo_planta_centro = {}
    for _, row in df_costos_plantas.iterrows():
        planta = f"Planta_{int(row['Planta'])}"
        producto = f"Producto_{int(row['Producto '])}"
        for i in range(1, len(C) + 1):
            if f'centro{i}' in row:
                centro = f"Centro_{i}"
                costo = row[f'centro{i}']
                costo_planta_centro[(planta, centro, producto)] = costo
    
    # Costos Centro → Cliente
    costo_centro_cliente = {}
    for _, row in df_costos_centros.iterrows():
        producto = f"Producto_{int(row['Producto'])}"
        centro = f"Centro_{int(row['Centro'])}"
        for i in range(1, len(J) + 1):
            if f'Cliente{i}' in row:
                cliente = f"Cliente_{i}"
                costo = row[f'Cliente{i}']
                costo_centro_cliente[(centro, cliente, producto)] = costo
    
    # Crear modelo
    modelo = ConcreteModel(name="Red_Distribucion_Multinivel")
    
    # Conjuntos
    modelo.P = Set(initialize=P)
    modelo.C = Set(initialize=C)
    modelo.J = Set(initialize=J)
    modelo.K = Set(initialize=K)
    
    # Variables
    modelo.x = Var(modelo.P, modelo.C, modelo.K, within=NonNegativeReals)
    modelo.y = Var(modelo.C, modelo.J, modelo.K, within=NonNegativeReals)
    
    # Función objetivo
    def funcion_objetivo(m):
        costo_plantas = sum(
            (costo_produccion.get((p, k), 0) + costo_planta_centro.get((p, c, k), 0)) * m.x[p, c, k]
            for p in m.P for c in m.C for k in m.K
        )
        costo_centros = sum(
            costo_centro_cliente.get((c, j, k), 0) * m.y[c, j, k]
            for c in m.C for j in m.J for k in m.K
        )
        return costo_plantas + costo_centros
    
    modelo.objetivo = Objective(rule=funcion_objetivo, sense=minimize)
    
    # Restricciones
    def restriccion_demanda(m, j, k):
        return sum(m.y[c, j, k] for c in m.C) == demanda.get((j, k), 0)
    modelo.demanda = Constraint(modelo.J, modelo.K, rule=restriccion_demanda)
    
    def restriccion_balance(m, c, k):
        entrada = sum(m.x[p, c, k] for p in m.P)
        salida = sum(m.y[c, j, k] for j in m.J)
        return entrada == salida
    modelo.balance_centros = Constraint(modelo.C, modelo.K, rule=restriccion_balance)
    
    def restriccion_capacidad_planta(m, p, k):
        if (p, k) in cap_produccion:
            return sum(m.x[p, c, k] for c in m.C) <= cap_produccion[(p, k)]
        else:
            return Constraint.Skip
    modelo.capacidad_plantas = Constraint(modelo.P, modelo.K, rule=restriccion_capacidad_planta)
    
    def restriccion_capacidad_centro(m, c, k):
        if (c, k) in cap_almacenamiento:
            return sum(m.y[c, j, k] for j in m.J) <= cap_almacenamiento[(c, k)]
        else:
            return Constraint.Skip
    modelo.capacidad_centros = Constraint(modelo.C, modelo.K, rule=restriccion_capacidad_centro)
    
    # Resolver
    solver = SolverFactory('glpk')
    resultado = solver.solve(modelo, tee=False)
    
    # Verificar solución óptima
    from pyomo.opt import SolverStatus, TerminationCondition
    if resultado.solver.status != SolverStatus.ok or \
       resultado.solver.termination_condition != TerminationCondition.optimal:
        return None
    
    # Calcular desglose de costos
    costo_produccion_total = sum(
        costo_produccion.get((p, k), 0) * value(modelo.x[p, c, k])
        for p in P for c in C for k in K
        if value(modelo.x[p, c, k]) and value(modelo.x[p, c, k]) > 0.01
    )
    
    costo_transporte_pc = sum(
        costo_planta_centro.get((p, c, k), 0) * value(modelo.x[p, c, k])
        for p in P for c in C for k in K
        if value(modelo.x[p, c, k]) and value(modelo.x[p, c, k]) > 0.01
    )
    
    costo_transporte_cj = sum(
        costo_centro_cliente.get((c, j, k), 0) * value(modelo.y[c, j, k])
        for c in C for j in J for k in K
        if value(modelo.y[c, j, k]) and value(modelo.y[c, j, k]) > 0.01
    )
    
    return {
        'modelo': modelo,
        'P': P, 'C': C, 'J': J, 'K': K,
        'costo_total': value(modelo.objetivo),
        'costo_produccion': costo_produccion_total,
        'costo_transporte_pc': costo_transporte_pc,
        'costo_transporte_cj': costo_transporte_cj,
        'demanda': demanda,
        'cap_produccion': cap_produccion,
        'cap_almacenamiento': cap_almacenamiento,
        'costo_prod_param': costo_produccion,
        'costo_pc_param': costo_planta_centro,
        'costo_cj_param': costo_centro_cliente
    }

# ============================================================================
# SIDEBAR - CONFIGURACIÓN
# ============================================================================
with st.sidebar:
    st.markdown("### ⚙️ Configuración del Sistema")
    
    metodo_carga = st.radio(
        "Método de Carga de Datos:",
        ["📥 Google Drive (Proyecto Real)", "🎲 Generar Aleatorios", "📁 Subir Archivos"],
        index=0
    )
    
    st.markdown("---")
    
    # Inicializar variables en session_state
    if 'datos_cargados' not in st.session_state:
        st.session_state.datos_cargados = False
    if 'datos_editados' not in st.session_state:
        st.session_state.datos_editados = False
    if 'modelo_resuelto' not in st.session_state:
        st.session_state.modelo_resuelto = False
    
    # MÉTODO 1: Google Drive
    if metodo_carga == "📥 Google Drive (Proyecto Real)":
        if st.button("🔽 Descargar desde Google Drive", use_container_width=True):
            with st.spinner("Descargando archivos..."):
                try:
                    df_plantas, df_centros, df_clientes, df_costos_pc, df_costos_cj = descargar_desde_drive()
                    st.session_state.df_plantas = df_plantas
                    st.session_state.df_centros = df_centros
                    st.session_state.df_clientes = df_clientes
                    st.session_state.df_costos_pc = df_costos_pc
                    st.session_state.df_costos_cj = df_costos_cj
                    st.session_state.datos_cargados = True
                    st.session_state.modelo_resuelto = False
                    st.success("✅ Datos descargados correctamente")
                except Exception as e:
                    st.error(f"Error al descargar: {e}")
    
    # MÉTODO 2: Generar Aleatorios
    elif metodo_carga == "🎲 Generar Aleatorios":
        st.markdown("**Parámetros de Generación:**")
        num_plantas = st.number_input("Plantas:", 1, 20, 10, key="num_p")
        num_centros = st.number_input("Centros:", 1, 20, 10, key="num_c")
        num_clientes = st.number_input("Clientes:", 1, 200, 100, key="num_j")
        num_productos = st.number_input("Productos:", 1, 10, 5, key="num_k")
        
        if st.button("🎲 Generar Datos", use_container_width=True):
            with st.spinner("Generando datos aleatorios..."):
                df_plantas, df_centros, df_clientes, df_costos_pc, df_costos_cj = generar_datos_aleatorios(
                    num_plantas, num_centros, num_clientes, num_productos
                )
                st.session_state.df_plantas = df_plantas
                st.session_state.df_centros = df_centros
                st.session_state.df_clientes = df_clientes
                st.session_state.df_costos_pc = df_costos_pc
                st.session_state.df_costos_cj = df_costos_cj
                st.session_state.datos_cargados = True
                st.session_state.modelo_resuelto = False
                st.success("✅ Datos generados correctamente")
    
    # MÉTODO 3: Subir Archivos
    else:
        st.markdown("**Sube los 5 archivos CSV:**")
        
        file_plantas = st.file_uploader("Plantas:", type=['csv'], key="up_plantas")
        file_centros = st.file_uploader("Centros:", type=['csv'], key="up_centros")
        file_clientes = st.file_uploader("Clientes:", type=['csv'], key="up_clientes")
        file_costos_pc = st.file_uploader("Costos P→C:", type=['csv'], key="up_pc")
        file_costos_cj = st.file_uploader("Costos C→J:", type=['csv'], key="up_cj")
        
        if all([file_plantas, file_centros, file_clientes, file_costos_pc, file_costos_cj]):
            if st.button("✅ Cargar Archivos", use_container_width=True):
                try:
                    st.session_state.df_plantas = pd.read_csv(file_plantas)
                    st.session_state.df_centros = pd.read_csv(file_centros)
                    st.session_state.df_clientes = pd.read_csv(file_clientes)
                    st.session_state.df_costos_pc = pd.read_csv(file_costos_pc)
                    st.session_state.df_costos_cj = pd.read_csv(file_costos_cj)
                    st.session_state.datos_cargados = True
                    st.session_state.modelo_resuelto = False
                    st.success("✅ Archivos cargados correctamente")
                except Exception as e:
                    st.error(f"Error al cargar archivos: {e}")
    
    st.markdown("---")
    
    # Estado del sistema
    if st.session_state.datos_cargados:
        st.success("✅ Datos cargados")
        if st.session_state.modelo_resuelto:
            st.success("✅ Modelo optimizado")
        else:
            st.warning("⏳ Modelo no optimizado")
    else:
        st.info("📋 Carga datos para comenzar")

# ============================================================================
# CONTENIDO PRINCIPAL
# ============================================================================

if not st.session_state.datos_cargados:
    st.info("👈 **Selecciona un método de carga de datos en el panel lateral para comenzar**")
    st.markdown("""
    ### 🎯 Opciones Disponibles:
    
    1. **📥 Google Drive**: Descarga automática de los datos del proyecto real
    2. **🎲 Generar Aleatorios**: Crea datos sintéticos para pruebas
    3. **📁 Subir Archivos**: Sube tus propios archivos CSV
    
    Una vez cargados los datos, podrás:
    - ✏️ Editar y revisar los datos
    - 🚀 Ejecutar la optimización
    - 📊 Visualizar resultados con gráficos interactivos
    """)
    st.stop()

# ============================================================================
# TABS DE DATOS Y OPTIMIZACIÓN
# ============================================================================
tab_datos, tab_optimizar, tab_resultados = st.tabs(["📋 Datos", "🚀 Optimizar", "📊 Resultados"])

with tab_datos:
    st.markdown("### 📋 Revisión y Edición de Datos")
    
    st.info("💡 **Tip**: Puedes editar las tablas haciendo doble clic en las celdas. Los cambios se aplicarán al modelo.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🏭 Plantas")
        edited_plantas = st.data_editor(
            st.session_state.df_plantas,
            use_container_width=True,
            num_rows="dynamic",
            key="editor_plantas"
        )
        st.session_state.df_plantas = edited_plantas
        
        st.markdown("#### 🏢 Centros de Distribución")
        edited_centros = st.data_editor(
            st.session_state.df_centros,
            use_container_width=True,
            num_rows="dynamic",
            key="editor_centros"
        )
        st.session_state.df_centros = edited_centros
        
        st.markdown("#### 👥 Clientes")
        edited_clientes = st.data_editor(
            st.session_state.df_clientes.head(50),
            use_container_width=True,
            key="editor_clientes"
        )
        st.caption(f"Mostrando primeros 50 de {len(st.session_state.df_clientes)} clientes")
    
    with col2:
        st.markdown("#### 💰 Costos Planta → Centro")
        st.dataframe(st.session_state.df_costos_pc.head(20), use_container_width=True)
        st.caption(f"Mostrando primeros 20 de {len(st.session_state.df_costos_pc)} registros")
        
        st.markdown("#### 💰 Costos Centro → Cliente")
        st.dataframe(st.session_state.df_costos_cj.head(20), use_container_width=True)
        st.caption(f"Mostrando primeros 20 de {len(st.session_state.df_costos_cj)} registros")
    
    # Resumen de datos
    st.markdown("---")
    st.markdown("### 📊 Resumen de Datos Cargados")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        num_plantas = len(st.session_state.df_plantas['Planta'].unique())
        st.metric("Plantas", num_plantas)
    with col2:
        num_centros = len(st.session_state.df_centros['Centro'].unique())
        st.metric("Centros", num_centros)
    with col3:
        num_clientes = len(st.session_state.df_clientes['Cliente'].unique())
        st.metric("Clientes", num_clientes)
    with col4:
        num_productos = len(st.session_state.df_plantas['Producto'].unique())
        st.metric("Productos", num_productos)

with tab_optimizar:
    st.markdown("### 🚀 Ejecutar Optimización")
    
    st.info("""
    **El modelo resolverá:**
    - ✅ Minimización de costos totales (producción + transporte)
    - ✅ Satisfacción de toda la demanda
    - ✅ Respeto de capacidades de plantas y centros
    - ✅ Balance de flujo en centros de distribución
    """)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🎯 EJECUTAR OPTIMIZACIÓN", use_container_width=True, type="primary"):
            with st.spinner("🔄 Resolviendo modelo de optimización..."):
                try:
                    resultado = resolver_modelo_optimizacion(
                        st.session_state.df_plantas,
                        st.session_state.df_centros,
                        st.session_state.df_clientes,
                        st.session_state.df_costos_pc,
                        st.session_state.df_costos_cj
                    )
                    
                    if resultado:
                        st.session_state.resultado = resultado
                        st.session_state.modelo_resuelto = True
                        st.success("✅ ¡Optimización completada exitosamente!")
                        st.balloons()
                    else:
                        st.error("❌ No se encontró solución óptima")
                except Exception as e:
                    st.error(f"❌ Error en la optimización: {e}")
    
    if st.session_state.modelo_resuelto:
        st.markdown("---")
        st.markdown("### 💰 Resultado de la Optimización")
        
        resultado = st.session_state.resultado
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <p class="metric-label">Costo Total</p>
                <p class="metric-value">${resultado['costo_total']:,.0f}</p>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <p class="metric-label">Producción</p>
                <p class="metric-value">${resultado['costo_produccion']:,.0f}</p>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <p class="metric-label">Transp. P→C</p>
                <p class="metric-value">${resultado['costo_transporte_pc']:,.0f}</p>
            </div>
            """, unsafe_allow_html=True)
        with col4:
            st.markdown(f"""
            <div class="metric-card">
                <p class="metric-label">Transp. C→J</p>
                <p class="metric-value">${resultado['costo_transporte_cj']:,.0f}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Gráfico de costos
        st.markdown("#### Composición de Costos")
        datos_costos = pd.DataFrame({
            'Tipo': ['Producción', 'Transporte P→C', 'Transporte C→J'],
            'Costo': [
                resultado['costo_produccion'],
                resultado['costo_transporte_pc'],
                resultado['costo_transporte_cj']
            ],
            'Porcentaje': [
                resultado['costo_produccion'] / resultado['costo_total'] * 100,
                resultado['costo_transporte_pc'] / resultado['costo_total'] * 100,
                resultado['costo_transporte_cj'] / resultado['costo_total'] * 100
            ]
        })
        
        fig = px.pie(
            datos_costos,
            values='Costo',
            names='Tipo',
            title="Distribución de Costos",
            color_discrete_sequence=['#3b82f6', '#10b981', '#f59e0b'],
            hole=0.4
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(
            height=400,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Inter')
        )
        st.plotly_chart(fig, use_container_width=True)

with tab_resultados:
    if not st.session_state.modelo_resuelto:
        st.warning("⚠️ **Primero debes ejecutar la optimización en la pestaña 🚀 Optimizar**")
        st.stop()
    
    resultado = st.session_state.resultado
    modelo = resultado['modelo']
    P = resultado['P']
    C = resultado['C']
    J = resultado['J']
    K = resultado['K']
    
    st.markdown("### 📊 Análisis Detallado de Resultados")
    
    # Subtabs para diferentes visualizaciones
    subtabs = st.tabs([
        "🌊 Flujo Sankey",
        "🔥 Mapas de Calor",
        "🎯 Utilización",
        "🕸️ Red de Flujos",
        "📊 Análisis Comparativo",
        "🎨 Distribución",
        "💰 Costos Detallados",
        "🔍 Consultas"
    ])
    
    # TAB 1: SANKEY
    with subtabs[0]:
        st.markdown("#### Flujo Completo de la Red")
        
        # Filtros
        col1, col2 = st.columns(2)
        with col1:
            top_clientes_sankey = st.slider("Top clientes a mostrar:", 10, 100, 50, 10, key="sankey_top")
        with col2:
            flujo_minimo = st.slider("Flujo mínimo:", 0.0, 100.0, 0.1, 0.1, key="sankey_min")
        
        # Preparar datos para Sankey
        labels = list(P) + list(C) + list(J)
        label_indices = {label: i for i, label in enumerate(labels)}
        
        source = []
        target = []
        flow_values = []
        colors = []
        
        # Flujos P → C
        for p in P:
            for c in C:
                flujo_total = sum(value(modelo.x[p, c, k]) or 0 for k in K)
                if flujo_total > flujo_minimo:
                    source.append(label_indices[p])
                    target.append(label_indices[c])
                    flow_values.append(flujo_total)
                    colors.append('rgba(59, 130, 246, 0.4)')
        
        # Flujos C → J
        flujos_cj = []
        for c in C:
            for j in J:
                flujo_total = sum(value(modelo.y[c, j, k]) or 0 for k in K)
                if flujo_total > flujo_minimo:
                    flujos_cj.append((c, j, flujo_total))
        
        flujos_cj = sorted(flujos_cj, key=lambda x: x[2], reverse=True)[:top_clientes_sankey]
        
        for c, j, flujo_total in flujos_cj:
            source.append(label_indices[c])
            target.append(label_indices[j])
            flow_values.append(flujo_total)
            colors.append('rgba(16, 185, 129, 0.4)')
        
        fig = go.Figure(data=[go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color='white', width=0.5),
                label=labels,
                color=['#3b82f6'] * len(P) + ['#10b981'] * len(C) + ['#f59e0b'] * len(J)
            ),
            link=dict(
                source=source,
                target=target,
                value=flow_values,
                color=colors
            )
        )])
        
        fig.update_layout(
            title=f"Flujo de Productos en la Red (Top {top_clientes_sankey} rutas C→J)",
            font=dict(size=12, family='Inter'),
            height=600,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # TAB 2: MAPAS DE CALOR
    with subtabs[1]:
        st.markdown("#### Intensidad de Flujos")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Planta → Centro**")
            
            # Matriz P x C
            matriz_pc = pd.DataFrame(index=P, columns=C, dtype=float)
            for p in P:
                for c in C:
                    matriz_pc.loc[p, c] = sum(value(modelo.x[p, c, k]) or 0 for k in K)
            
            fig = px.imshow(
                matriz_pc,
                labels=dict(x="Centro", y="Planta", color="Flujo"),
                x=C,
                y=P,
                color_continuous_scale='Blues',
                aspect='auto'
            )
            fig.update_layout(
                height=400,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(family='Inter')
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("**Centro → Cliente (Top clientes)**")
            
            # Filtro de top clientes
            top_n_clientes = st.slider("Top clientes:", 10, 50, 20, 5, key="heatmap_top")
            
            # Calcular total por cliente
            totales_cliente = {}
            for j in J:
                totales_cliente[j] = sum(value(modelo.y[c, j, k]) or 0 for c in C for k in K)
            
            top_clientes = sorted(totales_cliente.items(), key=lambda x: x[1], reverse=True)[:top_n_clientes]
            J_top = [j for j, _ in top_clientes]
            
            # Matriz C x J (top)
            matriz_cj = pd.DataFrame(index=C, columns=J_top, dtype=float)
            for c in C:
                for j in J_top:
                    matriz_cj.loc[c, j] = sum(value(modelo.y[c, j, k]) or 0 for k in K)
            
            fig = px.imshow(
                matriz_cj,
                labels=dict(x="Cliente", y="Centro", color="Flujo"),
                x=J_top,
                y=C,
                color_continuous_scale='Greens',
                aspect='auto'
            )
            fig.update_layout(
                height=400,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(family='Inter')
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # TAB 3: UTILIZACIÓN
    with subtabs[2]:
        st.markdown("#### Análisis de Utilización de Capacidad")
        
        # Filtros
        col1, col2 = st.columns(2)
        with col1:
            productos_filtro = st.multiselect(
                "Filtrar productos:",
                K,
                default=K[:3] if len(K) >= 3 else K,
                key="util_productos"
            )
        with col2:
            mostrar_tabla = st.checkbox("Mostrar tabla detallada", value=True, key="util_tabla")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Utilización de Plantas**")
            
            datos_util_plantas = []
            for p in P:
                for k in productos_filtro:
                    producido = sum(value(modelo.x[p, c, k]) or 0 for c in C)
                    capacidad = resultado['cap_produccion'].get((p, k), 0)
                    if capacidad > 0:
                        util = (producido / capacidad) * 100
                        datos_util_plantas.append({
                            'Planta': p,
                            'Producto': k,
                            'Utilización %': round(util, 1),
                            'Producido': round(producido, 2),
                            'Capacidad': capacidad
                        })
            
            df_util_plantas = pd.DataFrame(datos_util_plantas)
            
            if not df_util_plantas.empty:
                fig = px.bar(
                    df_util_plantas,
                    x='Planta',
                    y='Utilización %',
                    color='Producto',
                    barmode='group',
                    title="Utilización de Capacidad por Planta"
                )
                fig.update_layout(
                    height=400,
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(family='Inter')
                )
                st.plotly_chart(fig, use_container_width=True)
                
                if mostrar_tabla:
                    resumen_plantas = df_util_plantas.groupby('Planta').agg({
                        'Utilización %': 'mean',
                        'Producido': 'sum',
                        'Capacidad': 'sum'
                    }).reset_index()
                    resumen_plantas['Utilización %'] = resumen_plantas['Utilización %'].round(1)
                    st.dataframe(resumen_plantas, use_container_width=True, hide_index=True)
        
        with col2:
            st.markdown("**Utilización de Centros**")
            
            datos_util_centros = []
            for c in C:
                for k in productos_filtro:
                    almacenado = sum(value(modelo.y[c, j, k]) or 0 for j in J)
                    capacidad = resultado['cap_almacenamiento'].get((c, k), 0)
                    if capacidad > 0:
                        util = (almacenado / capacidad) * 100
                        datos_util_centros.append({
                            'Centro': c,
                            'Producto': k,
                            'Utilización %': round(util, 1),
                            'Almacenado': round(almacenado, 2),
                            'Capacidad': capacidad
                        })
            
            df_util_centros = pd.DataFrame(datos_util_centros)
            
            if not df_util_centros.empty:
                fig = px.bar(
                    df_util_centros,
                    x='Centro',
                    y='Utilización %',
                    color='Producto',
                    barmode='group',
                    title="Utilización de Almacenamiento por Centro"
                )
                fig.update_layout(
                    height=400,
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(family='Inter')
                )
                st.plotly_chart(fig, use_container_width=True)
                
                if mostrar_tabla:
                    resumen_centros = df_util_centros.groupby('Centro').agg({
                        'Utilización %': 'mean',
                        'Almacenado': 'sum',
                        'Capacidad': 'sum'
                    }).reset_index()
                    resumen_centros['Utilización %'] = resumen_centros['Utilización %'].round(1)
                    st.dataframe(resumen_centros, use_container_width=True, hide_index=True)
    
    # TAB 4: RED DE FLUJOS
    with subtabs[3]:
        st.markdown("#### Visualización de Red de Distribución")
        
        # Filtro
        top_clientes_red = st.slider("Top clientes a mostrar:", 10, 50, 20, 5, key="red_top")
        
        # Calcular top clientes
        totales_cliente = {}
        for j in J:
            totales_cliente[j] = sum(value(modelo.y[c, j, k]) or 0 for c in C for k in K)
        top_clientes = sorted(totales_cliente.items(), key=lambda x: x[1], reverse=True)[:top_clientes_red]
        
        # Crear posiciones de nodos
        pos = {}
        
        for i, p in enumerate(P):
            pos[p] = (0, i * 2)
        
        for i, c in enumerate(C):
            pos[c] = (1, i * 4)
        
        for i, (j, _) in enumerate(top_clientes):
            pos[j] = (2, i * 2)
        
        # Crear aristas
        edges = []
        
        for p in P:
            for c in C:
                flujo = sum(value(modelo.x[p, c, k]) or 0 for k in K)
                if flujo > 0.1:
                    edges.append({'source': p, 'target': c, 'weight': flujo, 'tipo': 'pc'})
        
        for c in C:
            for j, _ in top_clientes:
                flujo = sum(value(modelo.y[c, j, k]) or 0 for k in K)
                if flujo > 0.1:
                    edges.append({'source': c, 'target': j, 'weight': flujo, 'tipo': 'cj'})
        
        # Crear trazos de aristas
        edge_traces = []
        for edge in edges:
            x0, y0 = pos[edge['source']]
            x1, y1 = pos[edge['target']]
            
            edge_traces.append(go.Scatter(
                x=[x0, x1, None],
                y=[y0, y1, None],
                mode='lines',
                line=dict(width=max(1, edge['weight']/50), color='rgba(125, 125, 125, 0.3)'),
                hoverinfo='text',
                hovertext=f"{edge['source']} → {edge['target']}<br>Flujo: {edge['weight']:.1f}",
                showlegend=False
            ))
        
        # Crear trazos de nodos
        node_trace_plantas = go.Scatter(
            x=[pos[p][0] for p in P],
            y=[pos[p][1] for p in P],
            mode='markers+text',
            marker=dict(size=20, color='#3b82f6', line=dict(width=2, color='white')),
            text=P,
            textposition='middle left',
            hoverinfo='text',
            hovertext=[f"Planta: {p}" for p in P],
            name='Plantas',
            showlegend=True
        )
        
        node_trace_centros = go.Scatter(
            x=[pos[c][0] for c in C],
            y=[pos[c][1] for c in C],
            mode='markers+text',
            marker=dict(size=20, color='#10b981', line=dict(width=2, color='white')),
            text=C,
            textposition='top center',
            hoverinfo='text',
            hovertext=[f"Centro: {c}" for c in C],
            name='Centros',
            showlegend=True
        )
        
        node_trace_clientes = go.Scatter(
            x=[pos[j][0] for j, _ in top_clientes],
            y=[pos[j][1] for j, _ in top_clientes],
            mode='markers+text',
            marker=dict(size=15, color='#f59e0b', line=dict(width=2, color='white')),
            text=[j for j, _ in top_clientes],
            textposition='middle right',
            hoverinfo='text',
            hovertext=[f"Cliente: {j}<br>Demanda Total: {tot:.1f}" for j, tot in top_clientes],
            name='Clientes',
            showlegend=True
        )
        
        fig = go.Figure(data=edge_traces + [node_trace_plantas, node_trace_centros, node_trace_clientes])
        
        fig.update_layout(
            title=f"Red de Distribución (Top {top_clientes_red} Clientes por Demanda)",
            showlegend=True,
            hovermode='closest',
            margin=dict(b=20, l=20, r=20, t=60),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            height=600,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Inter', size=10),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Conexiones P→C", len([e for e in edges if e['tipo'] == 'pc']))
        with col2:
            st.metric("Conexiones C→J", len([e for e in edges if e['tipo'] == 'cj']))
        with col3:
            st.metric("Total Aristas", len(edges))
    
    # TAB 5: ANÁLISIS COMPARATIVO
    with subtabs[4]:
        st.markdown("#### Comparación Entre Nodos")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Top Plantas por Producción**")
            
            top_n = st.slider("Top N:", 5, len(P), min(10, len(P)), key="comp_top_p")
            
            produccion_plantas = {}
            for p in P:
                produccion_plantas[p] = sum(value(modelo.x[p, c, k]) or 0 for c in C for k in K)
            
            df_prod = pd.DataFrame(list(produccion_plantas.items()), columns=['Planta', 'Producción Total'])
            df_prod = df_prod.sort_values('Producción Total', ascending=False).head(top_n)
            
            fig = px.bar(
                df_prod,
                x='Planta',
                y='Producción Total',
                title=f"Top {top_n} Plantas por Volumen",
                color='Producción Total',
                color_continuous_scale='Blues'
            )
            fig.update_layout(
                height=400,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(family='Inter'),
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("**Top Centros por Flujo**")
            
            top_n_c = st.slider("Top N:", 5, len(C), min(10, len(C)), key="comp_top_c")
            
            flujo_centros = {}
            for c in C:
                flujo_centros[c] = sum(value(modelo.y[c, j, k]) or 0 for j in J for k in K)
            
            df_flujo = pd.DataFrame(list(flujo_centros.items()), columns=['Centro', 'Flujo Total'])
            df_flujo = df_flujo.sort_values('Flujo Total', ascending=False).head(top_n_c)
            
            fig = px.bar(
                df_flujo,
                x='Centro',
                y='Flujo Total',
                title=f"Top {top_n_c} Centros por Volumen",
                color='Flujo Total',
                color_continuous_scale='Greens'
            )
            fig.update_layout(
                height=400,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(family='Inter'),
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Gráfico de radar
        st.markdown("**Análisis de Eficiencia por Producto**")
        
        datos_radar = []
        for k in K:
            produccion = sum(value(modelo.x[p, c, k]) or 0 for p in P for c in C)
            demanda_total = sum(resultado['demanda'].get((j, k), 0) for j in J)
            cumplimiento = (produccion / demanda_total * 100) if demanda_total > 0 else 0
            
            datos_radar.append({
                'Producto': k,
                'Producción': produccion,
                'Demanda': demanda_total,
                'Cumplimiento %': round(cumplimiento, 1)
            })
        
        df_radar = pd.DataFrame(datos_radar)
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=df_radar['Producción'].tolist(),
            theta=df_radar['Producto'].tolist(),
            fill='toself',
            name='Producción',
            line_color='#3b82f6'
        ))
        
        fig.add_trace(go.Scatterpolar(
            r=df_radar['Demanda'].tolist(),
            theta=df_radar['Producto'].tolist(),
            fill='toself',
            name='Demanda',
            line_color='#f59e0b'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, max(df_radar['Demanda'].max(), df_radar['Producción'].max())])
            ),
            showlegend=True,
            title="Producción vs Demanda por Producto",
            height=500,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Inter')
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # TAB 6: DISTRIBUCIÓN
    with subtabs[5]:
        st.markdown("#### Distribución de Productos por Nodo")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Distribución en Plantas**")
            
            datos_sunburst_plantas = []
            for p in P:
                for k in K:
                    flujo = sum(value(modelo.x[p, c, k]) or 0 for c in C)
                    if flujo > 0.1:
                        datos_sunburst_plantas.append({
                            'Planta': p,
                            'Producto': k,
                            'Cantidad': flujo
                        })
            
            if datos_sunburst_plantas:
                df_sun_plantas = pd.DataFrame(datos_sunburst_plantas)
                
                fig = px.sunburst(
                    df_sun_plantas,
                    path=['Planta', 'Producto'],
                    values='Cantidad',
                    title="Distribución de Producción",
                    color='Cantidad',
                    color_continuous_scale='Blues'
                )
                fig.update_layout(
                    height=500,
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(family='Inter')
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("**Distribución en Centros**")
            
            datos_sunburst_centros = []
            for c in C:
                for k in K:
                    flujo = sum(value(modelo.y[c, j, k]) or 0 for j in J)
                    if flujo > 0.1:
                        datos_sunburst_centros.append({
                            'Centro': c,
                            'Producto': k,
                            'Cantidad': flujo
                        })
            
            if datos_sunburst_centros:
                df_sun_centros = pd.DataFrame(datos_sunburst_centros)
                
                fig = px.sunburst(
                    df_sun_centros,
                    path=['Centro', 'Producto'],
                    values='Cantidad',
                    title="Distribución de Almacenamiento",
                    color='Cantidad',
                    color_continuous_scale='Greens'
                )
                fig.update_layout(
                    height=500,
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(family='Inter')
                )
                st.plotly_chart(fig, use_container_width=True)
        
        # Treemap
        st.markdown("**Vista Jerárquica Completa**")
        
        flujo_min_tree = st.slider("Flujo mínimo:", 0.0, 50.0, 1.0, key="tree_min")
        
        datos_treemap = []
        for p in P:
            for c in C:
                for k in K:
                    flujo = value(modelo.x[p, c, k]) or 0
                    if flujo > flujo_min_tree:
                        datos_treemap.append({
                            'Planta': p,
                            'Centro': c,
                            'Producto': k,
                            'Flujo': flujo
                        })
        
        if datos_treemap:
            df_treemap = pd.DataFrame(datos_treemap)
            
            fig = px.treemap(
                df_treemap,
                path=['Planta', 'Centro', 'Producto'],
                values='Flujo',
                title="Jerarquía de Flujos: Planta → Centro → Producto",
                color='Flujo',
                color_continuous_scale='Viridis'
            )
            fig.update_layout(
                height=600,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(family='Inter')
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # TAB 7: COSTOS DETALLADOS
    with subtabs[6]:
        st.markdown("#### Desglose Detallado de Costos")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Composición del Costo Total**")
            
            datos_costos = pd.DataFrame({
                'Tipo': ['Producción', 'Transporte P→C', 'Transporte C→J'],
                'Costo': [
                    resultado['costo_produccion'],
                    resultado['costo_transporte_pc'],
                    resultado['costo_transporte_cj']
                ]
            })
            
            fig = px.pie(
                datos_costos,
                values='Costo',
                names='Tipo',
                title="Distribución de Costos",
                color_discrete_sequence=['#3b82f6', '#10b981', '#f59e0b']
            )
            fig.update_layout(
                height=400,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(family='Inter')
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("**Costos por Categoría**")
            
            fig = go.Figure()
            
            fig.add_trace(go.Bar(
                x=['Producción', 'Transp. P→C', 'Transp. C→J'],
                y=[resultado['costo_produccion'], resultado['costo_transporte_pc'], resultado['costo_transporte_cj']],
                marker_color=['#3b82f6', '#10b981', '#f59e0b'],
                text=[f"${resultado['costo_produccion']:,.0f}", 
                      f"${resultado['costo_transporte_pc']:,.0f}", 
                      f"${resultado['costo_transporte_cj']:,.0f}"],
                textposition='auto'
            ))
            
            fig.update_layout(
                title="Costos por Categoría",
                height=400,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(family='Inter'),
                showlegend=False
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Costos por planta
        st.markdown("**Costos de Producción por Planta**")
        
        top_n_plantas = st.slider("Top plantas:", 5, len(P), min(10, len(P)), key="costos_top")
        
        costos_por_planta = {}
        for p in P:
            costo = sum(
                resultado['costo_prod_param'].get((p, k), 0) * (value(modelo.x[p, c, k]) or 0)
                for c in C for k in K
            )
            costos_por_planta[p] = costo
        
        df_costos_planta = pd.DataFrame(list(costos_por_planta.items()), columns=['Planta', 'Costo'])
        df_costos_planta = df_costos_planta.sort_values('Costo', ascending=False).head(top_n_plantas)
        
        fig = px.bar(
            df_costos_planta,
            x='Planta',
            y='Costo',
            title=f"Top {top_n_plantas} Plantas por Costo de Producción",
            color='Costo',
            color_continuous_scale='Reds'
        )
        fig.update_layout(
            height=400,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Inter'),
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # TAB 8: CONSULTAS
    with subtabs[7]:
        st.markdown("#### Consultas Detalladas")
        
        tipo_consulta = st.selectbox("Tipo de análisis:", 
                                      ["Por Producto", "Por Planta", "Por Centro", "Por Cliente"])
        
        if tipo_consulta == "Por Producto":
            producto_sel = st.selectbox("Producto:", K)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"**Producción de {producto_sel}**")
                
                datos_prod = []
                for p in P:
                    for c in C:
                        flujo = value(modelo.x[p, c, producto_sel]) or 0
                        if flujo > 0.1:
                            datos_prod.append({
                                'Planta': p,
                                'Centro': c,
                                'Cantidad': round(flujo, 2)
                            })
                
                if datos_prod:
                    st.dataframe(pd.DataFrame(datos_prod), use_container_width=True, hide_index=True)
                    
                    df_p = pd.DataFrame(datos_prod)
                    fig = px.bar(df_p, x='Planta', y='Cantidad', color='Centro', title=f"Distribución de {producto_sel}")
                    fig.update_layout(height=300, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(family='Inter'))
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("Sin producción para este producto")
            
            with col2:
                st.markdown(f"**Distribución de {producto_sel}**")
                
                datos_dist = []
                for c in C:
                    for j in J:
                        flujo = value(modelo.y[c, j, producto_sel]) or 0
                        if flujo > 0.1:
                            datos_dist.append({
                                'Centro': c,
                                'Cliente': j,
                                'Cantidad': round(flujo, 2)
                            })
                
                if datos_dist:
                    df_d = pd.DataFrame(datos_dist).head(20)
                    st.dataframe(df_d, use_container_width=True, hide_index=True)
                    st.caption(f"Mostrando top 20 de {len(datos_dist)} rutas")
                else:
                    st.info("Sin distribución para este producto")
        
        elif tipo_consulta == "Por Planta":
            planta_sel = st.selectbox("Planta:", P)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"**Productos de {planta_sel}**")
                
                datos_prod_planta = []
                for k in K:
                    flujo = sum(value(modelo.x[planta_sel, c, k]) or 0 for c in C)
                    cap = resultado['cap_produccion'].get((planta_sel, k), 0)
                    if flujo > 0.1 or cap > 0:
                        util = (flujo / cap) * 100 if cap > 0 else 0
                        datos_prod_planta.append({
                            'Producto': k,
                            'Cantidad': round(flujo, 2),
                            'Capacidad': cap,
                            'Utilización %': round(util, 1)
                        })
                
                if datos_prod_planta:
                    st.dataframe(pd.DataFrame(datos_prod_planta), use_container_width=True, hide_index=True)
                    
                    df_pp = pd.DataFrame(datos_prod_planta)
                    fig = px.bar(df_pp, x='Producto', y='Utilización %', title=f"Utilización en {planta_sel}")
                    fig.update_layout(height=300, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(family='Inter'))
                    st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.markdown(f"**Envíos desde {planta_sel}**")
                
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
        
        elif tipo_consulta == "Por Centro":
            centro_sel = st.selectbox("Centro:", C)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"**Recepciones en {centro_sel}**")
                
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
            
            with col2:
                st.markdown(f"**Envíos desde {centro_sel}**")
                
                datos_env = []
                for j in J:
                    for k in K:
                        flujo = value(modelo.y[centro_sel, j, k]) or 0
                        if flujo > 0.1:
                            datos_env.append({
                                'Cliente': j,
                                'Producto': k,
                                'Cantidad': round(flujo, 2)
                            })
                
                if datos_env:
                    df_e = pd.DataFrame(datos_env).head(20)
                    st.dataframe(df_e, use_container_width=True, hide_index=True)
                    st.caption(f"Mostrando top 20 de {len(datos_env)} envíos")
        
        else:  # Por Cliente
            cliente_sel = st.selectbox("Cliente:", J)
            
            st.markdown(f"**Recepciones de {cliente_sel}**")
            
            datos_cliente = []
            for c in C:
                for k in K:
                    flujo = value(modelo.y[c, cliente_sel, k]) or 0
                    demanda_real = resultado['demanda'].get((cliente_sel, k), 0)
                    if flujo > 0.1 or demanda_real > 0:
                        datos_cliente.append({
                            'Centro': c if flujo > 0.1 else '-',
                            'Producto': k,
                            'Recibido': round(flujo, 2),
                            'Demanda': demanda_real,
                            'Cumplimiento %': round((flujo / demanda_real * 100) if demanda_real > 0 else 0, 1)
                        })
            
            if datos_cliente:
                df_cliente = pd.DataFrame(datos_cliente).groupby(['Producto', 'Demanda']).agg(
                    Recibido=('Recibido', 'sum'),
                    Centros=('Centro', lambda x: ', '.join(x[x != '-']))
                ).reset_index()
                
                df_cliente['Cumplimiento %'] = df_cliente.apply(
                    lambda row: (row['Recibido'] / row['Demanda'] * 100) if row['Demanda'] > 0 else 0, axis=1
                )
                df_cliente['Cumplimiento %'] = df_cliente['Cumplimiento %'].round(1)
                
                st.dataframe(df_cliente, use_container_width=True, hide_index=True)
                
                fig = px.bar(
                    df_cliente,
                    x='Producto',
                    y=['Recibido', 'Demanda'],
                    barmode='group',
                    title=f"Cumplimiento de Demanda - {cliente_sel}",
                    color_discrete_map={'Recibido': '#10b981', 'Demanda': '#f59e0b'}
                )
                fig.update_layout(
                    height=400,
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(family='Inter')
                )
                st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# FOOTER
# ============================================================================
st.markdown("---")
st.markdown("### ▸ Optimización de una Red Multinivel de Distribución Multiproducto")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Equipo de Desarrollo**")
    st.write("👤 Javier Augusto Rebull Saucedo — 263483")
    st.write("👤 Manuel Flores Cacho — 263178")
    st.write("👤 Patricia María Rosas Calderón — 261538")

with col2:
    st.markdown("**Información Académica**")
    st.write("🏫 **Programa:** MIAAD")
    st.write("🏛️ **Institución:** UACJ")
    st.write("📁 **Materia:** Programación para la Analítica Prescriptiva y de la Decisión")
    st.write("👨‍🏫 **Instructor:** Dr. Gilberto Rivera Zarate")

st.write("📅 **Fecha:** Noviembre 2025")