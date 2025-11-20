# 🌿 Network Optimizer Pro

**Sistema Profesional de Optimización de Redes Multinivel de Distribución Multiproducto**

Aplicación interactiva avanzada para resolver problemas complejos de cadenas de suministro mediante programación lineal con Pyomo y visualizaciones interactivas en Streamlit.

---

## 🎯 Problema Resuelto

### Descripción

Optimización de una red de distribución multinivel que conecta:
- **Plantas de Producción** → **Centros de Distribución (CeDis)** → **Clientes Finales**

Con múltiples productos, capacidades limitadas y costos variables en cada nivel de la red.

### Objetivo

**Minimizar el costo total** de la operación satisfaciendo simultáneamente:
- ✅ Demanda completa de todos los clientes
- ✅ Capacidades de producción en plantas
- ✅ Capacidades de almacenamiento en centros
- ✅ Balance de flujos en toda la red

---

## 🔧 Modelo Matemático

### Variables de Decisión

```
x[p,c,k] = Cantidad del producto k enviada desde planta p a centro c
y[c,j,k] = Cantidad del producto k enviada desde centro c a cliente j

Dominio: x, y ≥ 0 (variables continuas no-negativas)
```

### Función Objetivo

```
Minimizar Z = Σ(Costo_Producción[p,k] × x[p,c,k])
            + Σ(Costo_Transporte_PC[p,c,k] × x[p,c,k])
            + Σ(Costo_Transporte_CJ[c,j,k] × y[c,j,k])
```

**Donde:**
- Primer término: Costos de producción en plantas
- Segundo término: Costos de transporte Planta→Centro
- Tercer término: Costos de transporte Centro→Cliente

---

## 📋 Restricciones del Modelo

### 1. **Satisfacción de Demanda**
```
Σ(y[c,j,k] para todo c) = Demanda[j,k]  ∀ clientes j, productos k
```
✅ Cada cliente recibe exactamente la cantidad demandada de cada producto

### 2. **Balance en Centros de Distribución**
```
Σ(x[p,c,k] para todo p) = Σ(y[c,j,k] para todo j)  ∀ centros c, productos k
```
✅ Conservación de flujo: lo que entra a un centro debe salir (sin inventario)

### 3. **Capacidad de Producción**
```
Σ(x[p,c,k] para todo c) ≤ Capacidad_Producción[p,k]  ∀ plantas p, productos k
```
✅ No se puede producir más allá de la capacidad instalada

### 4. **Capacidad de Almacenamiento**
```
Σ(y[c,j,k] para todo j) ≤ Capacidad_Almacenamiento[c,k]  ∀ centros c, productos k
```
✅ Los centros no pueden exceder su capacidad de almacenamiento

### 5. **No-negatividad**
```
x[p,c,k] ≥ 0,  y[c,j,k] ≥ 0  ∀ p,c,j,k
```

---

## 🗺️ Estructura de la Red

```
                    PLANTA 1 ─┐
                    PLANTA 2 ─┼─→ CENTRO 1 ─┬─→ CLIENTE 1
                    PLANTA 3 ─┤             ├─→ CLIENTE 2
                              ├─→ CENTRO 2 ─┼─→ CLIENTE 3
                              │             └─→ CLIENTE ...
                              └─→ CENTRO 3
```

**Niveles de la Red:**
- **Nivel 0:** Plantas (Producción + Costos de fabricación)
- **Nivel 1:** Centros de Distribución (Almacenamiento + Transferencia)
- **Nivel 2:** Clientes (Demanda final)

---

## 🎨 Características de la Interfaz

### ✨ Diseño Profesional
- **Tema oscuro premium** con paleta de colores verde vibrante
- **Glassmorphism** y efectos de gradiente
- **Tarjetas métricas interactivas** con animaciones
- **Tipografía moderna** (Inter font family)
- **Responsive design** adaptable a diferentes pantallas

### 📊 Sistema de Pestañas (8 Vistas Especializadas)

#### 1. 📈 **Resumen Ejecutivo**
- KPIs principales del costo total
- Desglose de costos por categoría
- Gráfico de distribución (pie chart)
- Estadísticas generales de la solución

#### 2. 🏭 **Asignación Planta → Centro**
- Tabla detallada de flujos P→C
- Costos de transporte y producción
- Totales por planta y centro
- Exportable a CSV

#### 3. 🚛 **Asignación Centro → Cliente**
- Tabla completa de flujos C→J
- Análisis de entregas
- Costos de última milla
- Verificación de demanda satisfecha

#### 4. 📦 **Análisis por Producto**
- **Filtros interactivos** por producto
- KPIs específicos del producto seleccionado
- Visualizaciones multi-tab:
  - 📈 Distribución de costos (pie + bar charts)
  - 🌊 Diagrama de Sankey de flujos
  - 🏆 Top rutas más costosas
  - 🏭 Utilización de capacidad por planta

#### 5-7. **Análisis por Planta / Centro / Cliente**
- Misma estructura de 4 sub-tabs por dimensión
- Filtros dinámicos específicos
- Métricas calculadas en tiempo real
- Visualizaciones adaptadas al contexto

#### 8. 🌍 **Análisis Global**
- Vista completa de toda la red
- Diagramas Sankey globales
- Análisis comparativo integral
- Resumen de eficiencia total

---

## 🔄 Métodos de Carga de Datos

### 1. **📊 Generación Aleatoria**
- Datos sintéticos realistas
- Parámetros configurables:
  - Número de plantas (2-10)
  - Número de centros (2-15)
  - Número de clientes (3-20)
  - Número de productos (2-10)
- Seed para reproducibilidad
- Costos y capacidades balanceados automáticamente

### 2. **☁️ Google Drive**
- Integración directa con IDs de archivo
- Descarga automática mediante `gdown`
- IDs preconfigurados para:
  - `plantas.csv`
  - `centros.csv`
  - `clientes.csv`
  - `Costos Plantas x CeDis.csv`
  - `Costos CeDis x Cliente.csv`
- Sin necesidad de autenticación manual

### 3. **📁 Archivos CSV Locales**
- Carga mediante drag & drop en sidebar
- Validación automática de formato
- Detección de errores en datos
- Preview de datos cargados

---

## 📄 Formato de Archivos Requeridos

### 1. **plantas.csv**
```csv
Planta,Producto,Capacidad_Produccion,Costo_Produccion
P1,K1,5000,10.5
P1,K2,3000,15.2
P2,K1,4000,11.0
...
```

### 2. **centros.csv**
```csv
Centro,Producto,Capacidad_Almacenamiento,Costo_Almacenamiento
C1,K1,4000,2.0
C1,K2,3500,2.5
C2,K1,3000,1.8
...
```

### 3. **clientes.csv**
```csv
Cliente,Producto,Demanda
J1,K1,800
J1,K2,600
J2,K1,1200
...
```

### 4. **Costos Plantas x CeDis.csv**
```csv
Planta,Centro,Producto,Costo_Plant_Centro
P1,C1,K1,3.5
P1,C1,K2,4.0
P1,C2,K1,5.2
...
```

### 5. **Costos CeDis x Cliente.csv**
```csv
Centro,Cliente,Producto,Costo_Centro_Cliente
C1,J1,K1,2.0
C1,J1,K2,2.5
C1,J2,K1,3.0
...
```

---

## 🎯 Visualizaciones Avanzadas

### 📊 Gráficos Implementados

1. **Pie Charts (Donut)**
   - Distribución porcentual de costos
   - Colores personalizados por categoría
   - Interactividad con tooltips

2. **Bar Charts (Apilados/Agrupados)**
   - Comparación de costos por producto
   - Análisis multi-dimensional
   - Gradientes de color

3. **Diagramas de Sankey**
   - Flujo completo de la red
   - Visualización de top rutas
   - Grosor proporcional a cantidad
   - Colores con transparencia

4. **Tablas con Formato Condicional**
   - Gradientes de color (background_gradient)
   - Formato de moneda
   - Formato de cantidades
   - Resaltado de valores extremos

5. **Gráficos de Utilización**
   - Barras agrupadas por producto
   - Línea de referencia al 100%
   - Colores por entidad

---

## 🚀 Instalación y Uso

### Opción 1: Local

```bash
# Clonar repositorio
git clone https://github.com/jrebull/miaad-network-optimizer-pro.git
cd miaad-network-optimizer-pro

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar aplicación
streamlit run UACJ_MIAAD_OptimizarRed.py
```

### Opción 2: Streamlit Cloud

🌐 **App desplegada:** `https://miaad-network-optimizer-pro.streamlit.app`

---

## 🛠️ Stack Tecnológico

| Componente | Tecnología | Versión |
|-----------|-----------|---------|
| **Framework Web** | Streamlit | 1.28+ |
| **Optimización** | Pyomo | 6.7+ |
| **Solver LP** | GLPK | Latest |
| **Visualización** | Plotly | 5.18+ |
| **Data Science** | Pandas | 2.1+ |
| **Matemáticas** | NumPy | 1.24+ |
| **Cloud Storage** | gdown | Latest |

---

## 📈 Resultados y Análisis

### KPIs Principales

1. **Costo Total Optimizado**
   - Valor agregado de todos los componentes
   - Comparativa visual entre categorías

2. **Desglose de Costos**
   - Costo de producción (%)
   - Costo transporte P→C (%)
   - Costo transporte C→J (%)

3. **Eficiencia Operativa**
   - Utilización de capacidad por planta
   - Tasa de llenado de centros
   - Satisfacción de demanda (debe ser 100%)

4. **Identificación de Cuellos de Botella**
   - Plantas al límite de capacidad
   - Centros sobrecargados
   - Rutas más costosas

### Outputs Exportables

- ✅ Tablas en formato CSV
- ✅ Gráficos interactivos (HTML)
- ✅ Solución óptima detallada
- ✅ Reportes por dimensión

---

## 🔍 Validaciones Implementadas

### Validación de Datos

```python
✓ Capacidades suficientes vs demanda total
✓ Costos no negativos
✓ Integridad referencial entre archivos
✓ Formato correcto de columnas
✓ Detección de valores faltantes
```

### Validación de Solución

```python
✓ Optimalidad verificada por el solver
✓ Restricciones satisfechas al 100%
✓ Balance de flujos en cada nodo
✓ No violación de capacidades
✓ Demanda completamente satisfecha
```

---

## 🎓 Información Académica

### Institución
**Universidad Autónoma de Ciudad Juárez (UACJ)**

### Programa
**Maestría en Inteligencia Artificial y Analítica de Datos (MIAAD)**

### Materia
**Programación para la Analítica Prescriptiva y de la Decisión**

### Instructor
**Dr. Gilberto Rivera Zarate**

### Equipo de Desarrollo

| Integrante | Matrícula |
|-----------|-----------|
| 👤 **Javier Augusto Rebull Saucedo** | 263483 |
| 👤 **Manuel Flores Cacho** | 263178 |
| 👤 **Patricia María Rosas Calderón** | 261538 |

---

## 📂 Estructura del Proyecto

```
miaad-network-optimizer-pro/
├── UACJ_MIAAD_OptimizarRed.py  # Aplicación principal
├── requirements.txt             # Dependencias Python
├── packages.txt                 # Dependencias del sistema (GLPK)
├── README.md                    # Este archivo
├── .gitignore                   # Archivos ignorados por Git
└── .streamlit/
    └── config.toml             # Configuración Streamlit
```

---

## 💡 Metodología de Solución

```
┌─────────────────────────────────────────────┐
│  1. ENTRADA DE DATOS                        │
│     ├─ Generación aleatoria                 │
│     ├─ Google Drive                         │
│     └─ CSV local                            │
└─────────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────┐
│  2. VALIDACIÓN Y PREPROCESAMIENTO           │
│     ├─ Verificar integridad                 │
│     ├─ Validar factibilidad                 │
│     └─ Construir estructuras de datos       │
└─────────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────┐
│  3. CONSTRUCCIÓN DEL MODELO PYOMO           │
│     ├─ Declaración de conjuntos             │
│     ├─ Declaración de parámetros            │
│     ├─ Variables de decisión                │
│     ├─ Función objetivo                     │
│     └─ Restricciones                        │
└─────────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────┐
│  4. RESOLUCIÓN (GLPK)                       │
│     ├─ Formulación estándar LP              │
│     ├─ Algoritmo Simplex                    │
│     └─ Validación de optimalidad            │
└─────────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────┐
│  5. ANÁLISIS DE RESULTADOS                  │
│     ├─ Extracción de variables              │
│     ├─ Cálculo de KPIs                      │
│     ├─ Análisis multi-dimensional           │
│     └─ Generación de visualizaciones        │
└─────────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────┐
│  6. PRESENTACIÓN INTERACTIVA                │
│     ├─ Dashboard dinámico                   │
│     ├─ Filtros y navegación                 │
│     ├─ Exportación de datos                 │
│     └─ Reportes especializados              │
└─────────────────────────────────────────────┘
```

---

## ⚙️ Configuración Avanzada

### Parámetros de Generación de Datos

```python
# En la aplicación (sidebar)
n_plantas = 3-10       # Número de plantas
n_centros = 3-15       # Número de centros
n_clientes = 5-20      # Número de clientes
n_productos = 2-10     # Número de productos
seed = 42              # Para reproducibilidad
```

### Solvers Soportados

| Solver | Tipo | Licencia | Uso |
|--------|------|----------|-----|
| **GLPK** | LP/MIP | GPL | Predeterminado |
| **CBC** | LP/MIP | EPL | Alternativo |
| **IPOPT** | NLP | EPL | Problemas no lineales |
| **Gurobi** | LP/MIP/QP | Comercial | Alto rendimiento |

---

## 📊 Casos de Uso

### 1. **Planificación Estratégica**
- Diseño de nuevas redes de distribución
- Evaluación de escenarios "what-if"
- Análisis de sensibilidad

### 2. **Optimización Operativa**
- Minimización de costos logísticos
- Balanceo de carga entre plantas
- Mejora de utilización de capacidad

### 3. **Análisis de Impacto**
- Evaluación de nuevos productos
- Impacto de cambio en capacidades
- Análisis de cuellos de botella

### 4. **Reporting Ejecutivo**
- KPIs para alta dirección
- Dashboards interactivos
- Exportación de resultados

---

## 🔧 Solución de Problemas

### Error: "Solver not found"
```bash
# Instalar GLPK
# macOS: brew install glpk
# Ubuntu: sudo apt-get install glpk-utils
# Windows: Descargar binarios desde GNU
```

### Error: "Data format mismatch"
```python
# Verificar que los archivos CSV tengan:
✓ Codificación UTF-8
✓ Separador: coma (,)
✓ Columnas con nombres exactos
✓ Sin filas vacías
```

### Error: "Infeasible model"
```python
# Causas comunes:
✗ Capacidad total < Demanda total
✗ Costos negativos o nulos
✗ Productos sin ruta posible
```

---

## 📚 Referencias Teóricas

### Libros
- Chopra, S. & Meindl, P. (2016). *Supply Chain Management: Strategy, Planning, and Operation*
- Winston, W. L. (2022). *Operations Research: Applications and Algorithms*
- Hillier, F. S. & Lieberman, G. J. (2020). *Introduction to Operations Research*

### Artículos
- Hart, W. E., et al. (2017). "Pyomo–optimization modeling in python"
- Dantzig, G. B. (1963). *Linear Programming and Extensions*

### Documentación
- [Pyomo Documentation](https://pyomo.readthedocs.io/)
- [GLPK Manual](https://www.gnu.org/software/glpk/)
- [Streamlit Docs](https://docs.streamlit.io/)

---

## 🎨 Paleta de Colores

```css
Primary:    #4ade80  /* Verde vibrante */
Secondary:  #22c55e  /* Verde sólido */
Accent:     #86efac  /* Verde claro */
Background: #1a1c20  /* Oscuro profundo */
Cards:      #2d3035  /* Gris oscuro */
Text:       #f3f4f6  /* Blanco suave */
```

---

## 🚦 Estado del Proyecto

| Feature | Estado |
|---------|--------|
| Modelo LP básico | ✅ Completo |
| Interfaz Streamlit | ✅ Completo |
| Visualizaciones | ✅ Completo |
| Google Drive | ✅ Completo |
| Filtros dinámicos | ✅ Completo |
| Exportación CSV | ✅ Completo |
| Documentación | ✅ Completo |
| Deploy Cloud | ✅ Completo |

---

## 📞 Soporte y Contacto

### Reportar Issues
- Crear issue en GitHub
- Incluir logs de error
- Adjuntar archivos de prueba

### Sugerencias
- Pull requests bienvenidos
- Documentar cambios propuestos
- Seguir estilo de código existente

---

## 📄 Licencia

Proyecto académico desarrollado para la **Universidad Autónoma de Ciudad Juárez**.

Uso educativo y de investigación permitido con atribución apropiada.

---

## 🔄 Changelog

### v2.0 (19 Nov 2025)
- ✨ Interfaz completamente rediseñada con tema oscuro premium
- 🎨 Sistema de 8 pestañas especializadas
- 📊 Visualizaciones avanzadas con Plotly
- 🔧 Filtros dinámicos en múltiples vistas
- ☁️ Integración con Google Drive
- 🚀 Deploy en Streamlit Cloud

### v1.0 (13 Nov 2025)
- 🎯 Versión inicial funcional
- ⚙️ Modelo de optimización básico
- 📈 Visualizaciones iniciales

---

**Última actualización:** 19 de noviembre del 2025  
**Versión:** 2.0  
**Repositorio:** https://github.com/jrebull/miaad-network-optimizer-pro

---

```
╔════════════════════════════════════════════════════════════╗
║  Network Optimizer Pro - MIAAD UACJ                        ║
║  Sistema Profesional de Optimización de Redes Multinivel  ║
║  Desarrollado con 💚 por el Equipo MIAAD                   ║
╚════════════════════════════════════════════════════════════╝
```
