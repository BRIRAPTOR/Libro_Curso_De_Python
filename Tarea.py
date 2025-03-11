import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Carga del archivo CSV
df = pd.read_csv('housing.csv')

# 2. Cálculo de estadísticas descriptivas para la columna "median_house_value"
col = 'median_house_value'
media = df[col].mean()
mediana = df[col].median()
moda = df[col].mode()[0]  # Se toma la primera moda en caso de haber más de una
rango = df[col].max() - df[col].min()
varianza = df[col].var()
desviacion = df[col].std()

# Crear un DataFrame para mostrar las estadísticas de forma tabular
estadisticas = pd.DataFrame({
    'Estadística': ['Media', 'Mediana', 'Moda', 'Rango', 'Varianza', 'Desviación Estándar'],
    'Valor': [media, mediana, moda, rango, varianza, desviacion]
})

print("Estadísticas descriptivas para", col)
print(estadisticas)

# 3. Creación de la tabla de frecuencias (agrupando en intervalos)
# Se definen 10 intervalos (bins)
df['value_bin'] = pd.cut(df[col], bins=10)
tabla_frecuencias = df['value_bin'].value_counts().sort_index()

print("\nTabla de frecuencias para", col)
print(tabla_frecuencias)

# 4. Gráfico de barras

# Se asume que el dataset tiene la columna "ocean_proximity" para agrupar.
if 'ocean_proximity' in df.columns:
    # Agrupar por "ocean_proximity" y calcular la media de median_house_value y population
    grupo = df.groupby('ocean_proximity').agg({
        'median_house_value': 'mean',
        'population': 'mean'
    }).reset_index()
    
    # Crear gráfico de barras con doble eje y:
    fig, ax1 = plt.subplots(figsize=(10,6))
    
    # Barras para median_house_value
    barras1 = ax1.bar(grupo['ocean_proximity'], grupo['median_house_value'], 
                      color='blue', alpha=0.6, label='Median House Value')
    ax1.set_ylabel('Median House Value', color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')
    
    # Línea horizontal para la media general de median_house_value
    ax1.axhline(y=media, color='red', linestyle='--', label='Media General')
    
    # Segundo eje para population
    ax2 = ax1.twinx()
    barras2 = ax2.bar(grupo['ocean_proximity'], grupo['population'], 
                      color='green', alpha=0.4, label='Population')
    ax2.set_ylabel('Population', color='green')
    ax2.tick_params(axis='y', labelcolor='green')
    
    # Título y leyendas
    plt.title('Comparación de Median House Value y Population por Ocean Proximity')
    # Combinar leyendas de ambos ejes
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper right')
    
    plt.tight_layout()
    plt.show()

else:
    # Si no se encuentra la columna "ocean_proximity", se grafican las primeras 20 filas
    fig, ax = plt.subplots(figsize=(10,6))
    df_sample = df.head(20)
    ax.bar(df_sample.index, df_sample['median_house_value'], color='blue', alpha=0.6, label='Median House Value')
    ax.set_ylabel('Median House Value')
    ax.axhline(y=media, color='red', linestyle='--', label='Media General')
    plt.title('Median House Value (Primeras 20 filas)')
    plt.legend()
    plt.show()
