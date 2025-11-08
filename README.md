# 📦 Network Optimizer Pro

**Optimización de Redes Multinivel de Distribución Multiproducto**

Aplicación interactiva para resolver problemas complejos de cadenas de suministro mediante programación lineal con Pyomo y Streamlit.

---

## 🎯 Problema Resuelto

### Descripción

Se busca optimizar una red de distribución multinivel que conecta:
- **Plantas de Producción** → **Centros de Distribución** → **Clientes Finales**

Con múltiples productos, capacidades limitadas y costos variables en cada nivel.

### Objetivo

**Minimizar el costo total** de la operación satisfaciendo:
- Demanda de todos los clientes
- Capacidades de producción en plantas
- Capacidades de almacenamiento en centros
- Balance de flujos en la red

---

## 🔧 Modelo Matemático

### Variables de Decisión

```
x[p,c,k] = Cantidad del producto k enviada desde planta p a centro c
y[c,j,k] = Cantidad del producto k enviada desde centro c a cliente j

Dominio: x, y ≥ 0 (no-negativos)
```

### Función Objetivo

```
Minimizar Z = Σ(Costo_Producción[p,k] × x[p,c,k])
            + Σ(Costo_Transporte_PC[p,c,k] × x[p,c,k])
            + Σ(Costo_Transporte_CJ[c,j,k] × y[c,j,k])
```

---

## 📋 Restricciones

### 1. **Satisfacción de Demanda**
```
Σ(y[c,j,k] para c) = Demanda[j,k]  ∀ clientes j, productos k
```
✓ Todo cliente recibe exactamente lo que demanda

### 2. **Balance en Centros de Distribución**
```
Σ(x[p,c,k] para p) = Σ(y[c,j,k] para j)  ∀ centros c, productos k
```
✓ Lo que entra = lo que sale (sin inventario acumulado)

### 3. **Capacidad de Producción**
```
Σ(x[p,c,k] para c) ≤ Capacidad_Producción[p,k]  ∀ plantas p, productos k
```
✓ No se puede producir más de la capacidad instalada

### 4. **Capacidad de Almacenamiento**
```
Σ(y[c,j,k] para j) ≤ Capacidad_Almacenamiento[c,k]  ∀ centros c, productos k
```
✓ Los centros no pueden almacenar más de su capacidad

### 5. **No-negatividad**
```
x[p,c,k] ≥ 0,  y[c,j,k] ≥ 0
```

---

## 🏗️ Estructura de la Red

```
                    PLANTA 1 ─┐
                    PLANTA 2 ─┼─→ CENTRO 1 ─┬─→ CLIENTE 1
                    PLANTA 3 ─┤             ├─→ CLIENTE 2
                              ├─→ CENTRO 2 ─┼─→ CLIENTE 3
                              │             └─→ CLIENTE ...
                              └─→ CENTRO 3
```

**Niveles:**
- **Nivel 0:** Plantas (Producción)
- **Nivel 1:** Centros de Distribución (Almacenamiento)
- **Nivel 2:** Clientes (Demanda final)

---

## 📊 Características

✅ **Generación de datos realistas**  
✅ **Carga de datos desde múltiples fuentes:**
   - Datos aleatorios generados
   - Google Drive (via API)
   - Archivos CSV locales

✅ **Optimización automática**  
✅ **Análisis detallado de costos**  
✅ **Visualizaciones interactivas:**
   - Gráficos de distribución de costos
   - Análisis por producto
   - Análisis por planta
   - Análisis por centro
   - Análisis por cliente
   - Flujos completos de la red

---

## 🔐 Datos Requeridos

### Archivos CSV necesarios:

1. **productos.csv**
   ```
   Producto, Descripcion
   ```

2. **plantas.csv**
   ```
   Planta, Producto, Capacidad_Produccion, Costo_Produccion
   ```

3. **centros.csv**
   ```
   Centro, Producto, Capacidad_Almacenamiento, Costo_Almacenamiento
   ```

4. **clientes.csv**
   ```
   Cliente, Producto, Demanda
   ```

5. **costos.csv**
   ```
   Planta, Centro, Producto, Costo_Plant_Centro, Cliente, Costo_Centro_Cliente
   ```

---

## 🚀 Uso Rápido

### Local

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar app
streamlit run app_descriptiva.py
```

### Online (Streamlit Cloud)

```
https://miaad-network-optimizer-pro.streamlit.app
```

---

## 🛠️ Stack Tecnológico

| Componente | Tecnología |
|-----------|-----------|
| **Framework Web** | Streamlit 1.28.1 |
| **Optimización** | Pyomo 6.7.4 |
| **Solver** | GLPK |
| **Visualización** | Plotly 5.18.0 |
| **Data Science** | Pandas 2.1.3, NumPy 1.24.3 |

---

## 📈 Resultados

La aplicación proporciona:

1. **Costo Total Optimizado**
   - Desglose por concepto (producción, transporte)
   - Comparativa visual

2. **Asignación Óptima**
   - Flujos de producción por planta
   - Distribución hacia centros
   - Entregas a clientes

3. **Análisis de Utilización**
   - Porcentaje de capacidad usado
   - Productos prioritarios
   - Cuellos de botella identificados

4. **Exportabilidad**
   - Tablas descargables
   - Gráficos interactivos
   - Reportes por nivel

---

## 🎓 Información Académica

**Programa:** Maestría en Inteligencia Artificial y Analítica de Datos (MIAAD)  
**Institución:** Universidad Autónoma de Ciudad Juárez  
**Materia:** Programación para la Analítica Prescriptiva y de la Decisión  
**Instructor:** Dr. Gilberto Rivera Zarate  

**Equipo de Desarrollo:**
- 👤 Javier Augusto Rebull Saucedo (Matrícula: 263483)
- 👤 Manuel Flores Cacho (Matrícula: 263178)
- 👤 Patricia María Rosas Calderón (Matrícula: 261538)

---

## 📁 Estructura del Proyecto

```
miaad-network-optimizer-pro/
├── app_descriptiva.py           # Aplicación principal
├── requirements.txt             # Dependencias Python
├── packages.txt                 # Dependencias del sistema
├── README.md                    # Este archivo
├── .gitignore                   # Archivos ignorados por Git
└── .streamlit/
    └── config.toml             # Configuración Streamlit
```

---

## 💡 Metodología de Solución

```
1. ENTRADA DE DATOS
   ↓
2. VALIDACIÓN DE DATOS
   ↓
3. CONSTRUCCIÓN DEL MODELO (Pyomo)
   ├─ Declaración de conjuntos
   ├─ Declaración de variables
   ├─ Función objetivo
   └─ Restricciones
   ↓
4. RESOLUCIÓN (GLPK Solver)
   ├─ Formulación estándar
   ├─ Búsqueda de solución
   └─ Validación de optimalidad
   ↓
5. ANÁLISIS DE RESULTADOS
   ├─ Cálculo de costos
   ├─ Análisis por dimensión
   └─ Visualizaciones
   ↓
6. SALIDA INTERACTIVA
```

---

## ⚙️ Configuración

### Parámetros Configurables

- Número de plantas: 2-10
- Número de centros: 2-15
- Número de clientes: 3-20
- Número de productos: 2-10
- Seed para reproducibilidad

### Solvers Soportados

- ✅ **GLPK** (por defecto - gratuito)
- ✅ **IPOPT** (alternativo)
- ✅ **Gurobi** (premium)

---

## 🔍 Interpretación de Resultados

### Métricas Principales

**Costo Total:** Suma de todos los costos de operación  
**Costo de Producción:** Gasto en manufactura  
**Transporte P→C:** Logística planta-centro  
**Transporte C→J:** Logística centro-cliente  

### KPIs

- **Utilización de Capacidad:** % de capacidad usada
- **Cumplimiento de Demanda:** % de demanda satisfecha
- **Costo por Unidad:** Costo promedio por producto

---

## 📚 Referencias Teóricas

- **Programación Lineal:** Dantzig, G. (1963)
- **Supply Chain Optimization:** Chopra & Meindl (2016)
- **Pyomo Documentation:** Hart, W. E., et al. (2017)

---

## 📞 Soporte

Para reportes de errores o sugerencias:
- Revisa los logs de Streamlit Cloud
- Valida los archivos CSV de entrada
- Verifica capacidades vs demanda

---

## 📄 Licencia

Proyecto académico - Universidad Autónoma de Ciudad Juárez

---

**Última actualización:** 13 de noviembre del 2025

```
╔════════════════════════════════════════════════════════════╗
║  Network Optimizer Pro - MIAAD UACJ                       ║
║  Optimización de Redes Multinivel de Distribución         ║
║  Multiproducto con Programación Lineal                    ║
╚════════════════════════════════════════════════════════════╝
```