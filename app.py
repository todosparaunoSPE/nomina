# -*- coding: utf-8 -*-
"""
Created on Tue May  6 16:56:13 2025

@author: jahop
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Título
title = "Dashboard de Compensaciones y Nómina"
st.title(title)
st.markdown("---")

# Sidebar - Ayuda y Nombre
with st.sidebar:
    st.header("Ayuda")
    st.markdown("""
    Esta aplicación permite:
    - Visualizar y analizar datos ficticios de compensaciones y nómina.
    - Filtrar por puesto y área.
    - Ver comparativos gráficos de sueldos y componentes.
    - Simular ajustes salariales y comparar los resultados.
    - Descargar los datos generados en formato Excel.
    """)
    st.markdown("---")
    st.markdown("**Creado por Javier Horacio Pérez Ricárdez**")

# Simulación de datos ficticios
np.random.seed(42)
puestos = ['Analista', 'Coordinador', 'Gerente', 'Director']
areas = ['RH', 'Finanzas', 'TI', 'Ventas']
nombres = [f"Empleado {i+1}" for i in range(50)]

data = {
    'Nombre': nombres,
    'Puesto': np.random.choice(puestos, size=50),
    'Area': np.random.choice(areas, size=50),
    'Sueldo Base': np.random.randint(18000, 60000, size=50),
    'Bono Puntualidad': np.random.randint(800, 2000, size=50),
    'Bono Asistencia': np.random.randint(800, 2000, size=50),
    'Vales Despensa': np.random.randint(1000, 2500, size=50),
    'Fondo de Ahorro': np.random.randint(1000, 3000, size=50),
}
df = pd.DataFrame(data)
df['Compensacion Total'] = df[['Sueldo Base', 'Bono Puntualidad', 'Bono Asistencia', 'Vales Despensa', 'Fondo de Ahorro']].sum(axis=1)

# Filtro por puesto y área
with st.sidebar:
    st.header("Filtros")
    selected_puesto = st.multiselect("Selecciona Puesto", options=df['Puesto'].unique(), default=df['Puesto'].unique())
    selected_area = st.multiselect("Selecciona Área", options=df['Area'].unique(), default=df['Area'].unique())

filtered_df = df[(df['Puesto'].isin(selected_puesto)) & (df['Area'].isin(selected_area))]

# Tabla de datos
st.subheader("Datos de Empleados")
st.dataframe(filtered_df)

# Visualización 1: Compensación por empleado
st.subheader("Compensación Total por Empleado")
fig1 = px.bar(filtered_df, x='Nombre', y='Compensacion Total', color='Puesto', title='Comparativo de Compensaciones')
st.plotly_chart(fig1)

# Visualización 2: Distribución por Puesto
st.subheader("Distribución Salarial por Puesto")
fig2 = px.box(filtered_df, x='Puesto', y='Compensacion Total', color='Puesto')
st.plotly_chart(fig2)

# Visualización 3: Porcentaje por componente
st.subheader("Análisis de Componentes de la Compensación")
componentes = ['Sueldo Base', 'Bono Puntualidad', 'Bono Asistencia', 'Vales Despensa', 'Fondo de Ahorro']
avg_componentes = filtered_df[componentes].mean()
fig3 = px.pie(values=avg_componentes.values, names=avg_componentes.index, title='Promedio de Componentes por Empleado')
st.plotly_chart(fig3)

# Nueva funcionalidad: Simulador de Ajuste Salarial
st.subheader("Simulador de Ajuste Salarial")
st.markdown("Ajusta el porcentaje de incremento salarial para simular nuevas compensaciones.")
porcentaje_ajuste = st.slider("% de ajuste salarial", min_value=-20, max_value=30, value=0, step=1)

filtered_df['Sueldo Ajustado'] = filtered_df['Sueldo Base'] * (1 + porcentaje_ajuste / 100)
filtered_df['Compensacion Ajustada'] = filtered_df[['Sueldo Ajustado', 'Bono Puntualidad', 'Bono Asistencia', 'Vales Despensa', 'Fondo de Ahorro']].sum(axis=1)

fig4 = go.Figure()
fig4.add_trace(go.Bar(x=filtered_df['Nombre'], y=filtered_df['Compensacion Total'], name='Compensación Actual'))
fig4.add_trace(go.Bar(x=filtered_df['Nombre'], y=filtered_df['Compensacion Ajustada'], name='Compensación Ajustada'))
fig4.update_layout(barmode='group', title="Comparativo Antes vs. Después del Ajuste Salarial")
st.plotly_chart(fig4)

# Exportar a Excel
st.download_button(
    label="📄 Descargar Excel con Datos",
    data=filtered_df.to_csv(index=False).encode('utf-8'),
    file_name="compensaciones_ficticias.csv",
    mime="text/csv"
)

st.markdown("---")
st.markdown("**Aplicación demostrativa con datos simulados para vacante de Coordinador de Compensaciones y Nómina.**")
