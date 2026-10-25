# Radiografía Global del Bienestar Subjetivo (World Happiness Report 2024)
## Proyecto 2: Visualización Reproducible en Python

**Curso:** Visualización I  
**Programa:** Maestría / Especialización en Analítica  
**Docentes:** Adriana Pineda · Paola Moreno  
**Equipo de Trabajo:**
- **Arnold Santiago Torres Anzola**
- **Juan David Cruz Romero**

---

## 🎯 Pregunta Analítica y Audiencia Técnica

* **Audiencia Objetivo:** Equipo Técnico de Análisis Comparativo de Bienestar y Políticas Públicas de un Organismo Multilateral de Desarrollo (homólogo a unidades técnicas de PNUD / OCDE).
* **Pregunta Central de Investigación:**
  > *«¿Qué variables se asocian con la calidad de vida y evaluación del bienestar de los países, qué diferencias se evidencian entre naciones y de qué manera las condiciones económicas, de salud y socioinstitucionales diferencian a los países con alta y baja evaluación vital en el World Happiness Report 2024?»*

---

## 📁 Estructura del Repositorio

El repositorio adopta una arquitectura modular y orientada a la reproducibilidad analítica:

```text
Proyecto-2-Visualizacion/
├── data/
│   └── raw/
│       └── WHR24_Data_Figure_2.1.xls          <- Archivo fuente oficial de Gallup / WHR 2024
├── notebooks/
│   └── EquipoX_Proyecto2_Visualizacion.ipynb  <- Cuaderno principal con EDA, Seaborn, Plotly y narrativa
├── exports/
│   └── EquipoX_Proyecto2_Dashboard.html       <- Tablero BI interactivo (Gestalt y lectura en Z)
├── docs/
│   ├── fase1_audiencia_pregunta/
│   │   ├── Comprension_Contexto_...tex        <- Documento técnico de delimitación (Fase 1)
│   │   └── Comprension_Contexto_...pdf        <- PDF compilado de la Fase 1
│   ├── entregables/                           <- Resúmenes y memorandos ejecutivos
│   └── instrucciones/                         <- Rúbrica y directrices del curso
├── create_storytelling_dashboard.py           <- Generador autónomo del Tablero BI interactivo
└── README.md                                  <- Documentación general del proyecto
```

---

## 📦 Entregables Principales

### 1. Cuaderno Principal (`notebooks/EquipoX_Proyecto2_Visualizacion.ipynb`)
Implementa el ciclo completo de análisis y visualización reproducible:
* **Fase 4 (Ingesta y Preparación):** Validación estructural (0 duplicados, consistencia de intervalos y tolerancia matemática $\text{MAE} < 0,00003$ pts), traducción exhaustiva de los 143 países y variables al español, cálculo de cuartiles empíricos (partición por 25%), construcción de la condición socioinstitucional y matriz de estadísticos descriptivos robustos (Media $\pm$ Desv, Mediana, Mín-Máx, IQR, CV% y Asimetría).
* **Fase 5 (Planificación):** Diseño comparativo orientado a responder la pregunta analítica.
* **Fase 6 (Visualizaciones Estáticas e Interactivas):**
  * *Figura 1 (Seaborn):* Histograma y curva KDE con delimitación de cortes empíricos de bienestar.
  * *Figura 2 (Seaborn):* Brechas promedio ordenadas por magnitud (+0,90 pts en PIB vs +1,09 pts socioinstitucional).
  * *Figura 3 (Seaborn):* Anatomía aditiva acumulada del puntaje medio entre bloques.
  * *Figura 4 (Seaborn):* Dispersión de bienestar vs. PIB per cápita con detección de atípicos y resiliencias.
  * *Figura 5 (Plotly):* Mapa coroplético interactivo mundial con escala perceptualmente uniforme.
  * *Figura 6 (Plotly):* Descomposición aditiva país por país con selector dinámico de segmento.
* **Fase 7 (Síntesis y Gestalt):** Respuestas a la pregunta analítica y formalización de principios de percepción visual.
* **Fase 8 (Limitaciones):** Reconocimiento de no causalidad, datos de panel y agregaciones nacionales.
* **Fase 9 (Anexo IA):** Declaración de transparencia y uso asistido de inteligencia artificial.

### 2. Tablero BI Ejecutivo (`exports/EquipoX_Proyecto2_Dashboard.html`)
Diseñado como un *cockpit* directivo de inteligencia de negocios (conmutación instantánea mediante barra de control superior):
* **📊 Tablero Ejecutivo (Lectura en Z):** Cuadrícula simétrica 2×2 que guía el escaneo visual en Z:
  1. *Paso 1 (Top-Left):* KPIs estratégicos y justificación de la regla del 25%.
  2. *Paso 2 (Top-Right):* Mapa coroplético mundial de calidad de vida.
  3. *Paso 3 (Diag-Left):* Boxplots de dispersión e IQR con países jittereados y selector de escala.
  4. *Paso 4 (Diag-Right):* Descomposición de la Gran Brecha (+2,96 pts entre extremos).
  5. *Paso 5 (Base-Left):* Relación socioinstitucional vs. bienestar ($r = 0,88$, OLS) con países singulares destacados (Costa Rica, Finlandia, Botsuana, Líbano y Afganistán).
  6. *Paso 6 (Base-Right):* Gráfico de barras apiladas de los 36 países de cada extremo con selector interactivo.
* **📋 Estadística & Diccionario:** Matriz de estadísticos descriptivos, tarjetas de alerta de dispersión (Corrupción CV = 81,9%) y catálogo de 10 variables con filtros por condición.
* **💡 Implicaciones Estratégicas:** Respuestas para políticas públicas, panel de cautela inferencial y casos de estudio.

---

## 🔬 Metodología Analítica

### Criterio de Segmentación por 25% (Cuartiles Empíricos)
El archivo oficial del *World Happiness Report 2024* contiene únicamente la variable continua de la Escalera de Cantril. Para contrastar de manera reproducible y neutral a los países con **alta** y **baja** evaluación de vida (sin fijar umbrales subjetivos), se ordenaron las 143 naciones y se dividieron en cuartiles empíricos:
* **25% Superior (Alto Bienestar):** 36 naciones con puntaje $\ge 6,42$ pts (desde Finlandia con 7,74 hasta España y Polonia con 6,44).
* **50% Central (Bienestar Intermedio):** 71 naciones con puntajes entre 4,73 y 6,41 pts (como Colombia, Brasil, Grecia y Japón).
* **25% Inferior (Bajo Bienestar):** 36 naciones con puntaje $\le 4,73$ pts (desde Jordania con 4,64 hasta Afganistán con 1,72).

### La Gran Brecha (+2,96 pts)
La separación promedio entre el 25% Superior (6,88 pts) y el 25% Inferior (3,91 pts) es de **+2,96 puntos**. La descomposición demuestra que:
1. **La Condición Socioinstitucional (+1,09 pts, 36,8% de la brecha):** Sumando apoyo social (+0,67), libertad vital (+0,25) y confianza/probidad (+0,17), supera al impacto del ingreso individual.
2. **La Condición Económica (+0,90 pts, 30,4% de la brecha):** Constituye la mayor brecha de un componente aislado.
3. **La Condición de Salud (+0,32 pts, 10,8% de la brecha):** Refleja la disparidad en años de vida saludable.
4. **Distopía + residuo (+0,65 pts, 22,0% de la brecha):** Componente no modelado que refleja crisis humanitarias y choques idiosincrásicos.

---

## 🎨 Principios de Percepción Gestalt Aplicados

* **Región Común (*Common Region*):** Cada visualización se encuentra encapsulada en una tarjeta `.bi-widget` con bordes nítidos (`#1f2937`) y fondo uniforme (`#111827`), delimitando claramente cada mensaje.
* **Proximidad (*Proximity*):** Las tarjetas de KPIs están contiguas a la justificación metodológica; los controles de alternancia (dropdowns) residen en el encabezado de cada tarjeta respectiva.
* **Semejanza Cromática (*Similarity*):** Paleta semántica transversal e idéntica en gráficos estáticos, mapas y barras:
  * *Económica (PIB):* Azul cian (`#38bdf8`)
  * *Socioinstitucional (Apoyo, Libertad, Probidad):* Gama cálida ámbar (`#f59e0b`, `#fbbf24`, `#d97706`)
  * *Salud (Esperanza de vida):* Verde esmeralda (`#10b981`)
  * *Referencia (Generosidad y Residuo):* Gris neutro y lavanda (`#94a3b8`, `#818cf8`)
  * *Extremos:* 25% Superior en cian (`#38bdf8`) frente a 25% Inferior en carmesí (`#f43f5e`).
* **Simetría y Orden (*Symmetry & Prägnanz*):** Rejilla balanceada de dos columnas pares con alturas uniformes (430 px en filas superiores, 520 px en la fila inferior).
* **Continuidad (*Continuity*) y Lectura en Z:** Trayectoria visual planificada para análisis directivo (Top-Left $\rightarrow$ Top-Right $\searrow$ Diag-Left $\rightarrow$ Diag-Right $\searrow$ Base-Left $\rightarrow$ Base-Right).
* **Figura-Fondo (*Figure-Ground*):** Contraste calibrado entre un fondo oscuro inmersivo (`#0b0f19`) y visualizaciones luminosas, evitando la fatiga visual.

---

## 🚀 Instrucciones de Reproducción y Ejecución

### 1. Clonar el repositorio
```bash
git clone https://github.com/eljarcor98/Proyecto-2-Visualizacion.git
cd Proyecto-2-Visualizacion
```

### 2. Configurar entorno de Python
Se recomienda Python 3.10 o superior.
```bash
pip install pandas numpy matplotlib seaborn plotly openpyxl nbformat nbclient
```

### 3. Ejecutar el Cuaderno Principal
Para ejecutar el cuaderno completo y regenerar las salidas:
```bash
python -c "import nbformat; from nbclient import NotebookClient; nb = nbformat.read('notebooks/EquipoX_Proyecto2_Visualizacion.ipynb', as_version=4); client = NotebookClient(nb, timeout=600); client.execute(); nbformat.write(nb, 'notebooks/EquipoX_Proyecto2_Visualizacion.ipynb'); print('[OK] Notebook ejecutado con éxito')"
```

### 4. Generar o Visualizar el Tablero BI
Para compilar directamente el tablero HTML:
```bash
python create_storytelling_dashboard.py
```
El archivo resultante puede abrirse en cualquier navegador web moderno:
`exports/EquipoX_Proyecto2_Dashboard.html`
