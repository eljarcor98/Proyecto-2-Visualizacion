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

* **Audiencia Objetivo:** Equipo Técnico de Análisis Comparativo de Bienestar y Políticas Públicas de un Organismo Multilateral de Desarrollo (homólogo a unidades técnicas especializadas de PNUD, Banco Mundial o la OCDE).
* **Pregunta Central de Investigación:**
  > *«¿Qué variables se asocian con la calidad de vida y evaluación del bienestar de los países, qué diferencias se evidencian entre naciones y de qué manera las condiciones económicas, de salud y socioinstitucionales diferencian a los países con alta y baja evaluación vital en el World Happiness Report 2024?»*
* **Instrumento Psicométrico Base:**
  La variable dependiente principal (`Ladder score`) proviene de la **Escala de Autoanclaje y Esfuerzo de Cantril** (*Cantril Self-Anchoring Striving Scale*, desarrollada por Hadley Cantril en 1965 y aplicada globalmente por el *Gallup World Poll*). Dicho instrumento pide al ciudadano evaluar su vida en una escala de 0 (*peor vida posible*) a 10 (*mejor vida posible*).

---

## 📁 Estructura del Repositorio

El repositorio adopta una arquitectura modular, orientada a la reproducibilidad analítica y documental:

```text
Proyecto-2-Visualizacion/
├── data/
│   └── raw/
│       └── WHR24_Data_Figure_2.1.xls          <- Archivo fuente oficial de Gallup / WHR 2024 (143 países)
├── notebooks/
│   └── EquipoX_Proyecto2_Visualizacion.ipynb  <- Cuaderno Jupyter ejecutable de principio a fin (Fases 1 a 10)
├── exports/
│   └── EquipoX_Proyecto2_Dashboard.html       <- Plataforma interactiva de inteligencia de datos (WHR & Gallup)
├── docs/
│   ├── fase1_audiencia_pregunta/
│   │   ├── Comprension_Contexto_Audiencia_Tecnica_Proyecto2.tex <- Documento técnico maestro en LaTeX (8 págs.)
│   │   ├── Comprension_Contexto_Audiencia_Tecnica_Proyecto2.pdf <- PDF oficial compilado con Tectonic
│   │   ├── compilar.py                        <- Script Python para compilación reproducible del PDF
│   │   └── figura_resumen_brechas.png         <- Infografía analítica de brechas y correlación OLS
│   ├── entregables/
│   │   ├── EquipoX_Proyecto2_Resumen.tex      <- Resumen ejecutivo multilateral de 3 páginas (LaTeX)
│   │   ├── EquipoX_Proyecto2_Resumen.pdf      <- PDF del resumen ejecutivo compilado
│   │   ├── compilar.py                        <- Compilador automatizado del resumen
│   │   ├── compilar_pdf.bat                   <- Lanzador por lotes Windows para compilar
│   │   └── figura_resumen_brechas.png         <- Copia de respaldo de la infografía
│   └── instrucciones/
│       └── Instrucciones_Proyecto_2_Visualizacion_Python.pdf <- Guía y rúbrica oficial de evaluación
├── bin/
│   └── tectonic.exe                           <- Motor autónomo de compilación LaTeX XeTeX (sin dependencias)
├── create_storytelling_dashboard.py           <- Generador Python del portal interactivo WHR / Gallup
└── README.md                                  <- Documentación general del proyecto y guía de ejecución
```

---

## 📦 Entregables Principales

### 1. Documento Técnico Maestro (`docs/fase1_audiencia_pregunta/`)
Documento institucional formal en formato LaTeX (`Comprension_Contexto_Audiencia_Tecnica_Proyecto2.pdf`, 8 páginas exactas sin desbordes):
* **Secciones 1 a 4:** Contexto multilateral, delimitación de la audiencia técnica, pregunta analítica y diccionario de variables completo (`xltabular`).
* **Sección 5 (Numeral 8):** Interpretación técnica pormenorizada de las 6 visualizaciones (Seaborn Figs. 1–4, Plotly Figs. 5–6), matriz comparativa de brechas $Q4$ vs. $Q1$, panel con figura resumen y análisis de casos de resiliencia (Nicaragua, El Salvador, Costa Rica) y vulnerabilidad (Botsuana, Líbano, Afganistán).
* **Sección 6 (Numeral 9):** Síntesis de hallazgos empíricos y respuesta directa y categórica a la pregunta de investigación.
* **Sección 7:** Cautela inferencial y limitaciones metodológicas (datos transversales, naturaleza no causal y agregaciones ecológicas).
* **Sección 8:** Trazabilidad de reproducibilidad computacional y especificación de la plataforma interactiva.
* **Sección 9:** Declaración de uso asistido de Inteligencia Artificial (con desglose de actividades asistidas y validaciones humanas independientes).
* **Bibliografía:** Referencias al WHR 2024, SDSN, Gallup World Poll y la obra psicométrica original de Hadley Cantril (1965).

### 2. Resumen Ejecutivo Multilateral (`docs/entregables/`)
Documento sintético de exactamente 3 páginas (`EquipoX_Proyecto2_Resumen.pdf`) orientado a directores de organismos de desarrollo con diagnóstico macroeconómico, gráfico de brechas e implicaciones operativas.

### 3. Cuaderno Principal Reproducible (`notebooks/EquipoX_Proyecto2_Visualizacion.ipynb`)
Implementa el ciclo analítico integral de 10 fases ejecutables secuencialmente:
* **Fases 1–3:** Formulación de audiencia, pregunta de investigación y catálogo de variables.
* **Fase 4 (Ingesta y Preparación):** Validación de consistencia matemática ($\text{MAE} < 0,00003$ pts frente al total reportado), traducción exhaustiva al español de las 143 naciones, segmentación cuartílica neutra ($Q1$, Central, $Q4$), cálculo de la condición socioinstitucional agregada y matriz de estadísticos descriptivos robustos (Media $\pm$ Desv, Mediana, Mín-Máx, IQR, CV% y Asimetría).
* **Fase 5:** Planificación del repertorio gráfico orientado a la toma de decisiones.
* **Fase 6 (Visualizaciones Estáticas e Interactivas):**
  * *Figura 1 (Seaborn):* Distribución empírica y curva KDE con líneas de corte cuartílicas.
  * *Figura 2 (Seaborn):* Brechas promedio ordenadas por magnitud (+0,90 pts en PIB vs +1,09 pts socioinstitucional).
  * *Figura 3 (Seaborn):* Anatomía aditiva acumulada del puntaje medio entre bloques.
  * *Figura 4 (Seaborn):* Dispersión de bienestar vs. PIB per cápita con detección de atípicos.
  * *Figura 5 (Plotly):* Mapa coroplético interactivo mundial con escala perceptualmente calibrada.
  * *Figura 6 (Plotly):* Descomposición aditiva apilada país por país con selector dinámico.
* **Fases 7–10:** Respuestas empíricas, enlace a la plataforma interactiva oficial, limitaciones y anexo IA.

### 4. Plataforma Interactiva de Inteligencia de Datos (`exports/EquipoX_Proyecto2_Dashboard.html`)
Diseñada bajo los estándares visuales e institucionales oficiales del *World Happiness Report* y *Gallup Analytics*:
* **Identidad Institucional:** Paleta oficial (*WHR Magenta* `#E0288A` y *Gallup Green* `#008559`), tipografía técnica (*Inter* y *IBM Plex Mono*) y eliminación de emojis o elementos animados para asegurar máxima sobriedad.
* **Navegación Multidimensional (Selector de Vistas WHR):**
  1. **Vista Geoespacial (Map):** Cartografía coroplética interactiva a escala global con codificación continua de la escalera de Cantril (1,7 a 7,8 pts).
  2. **Vistas Analíticas (Chart):** Cuadrícula comparativa con la descomposición de la brecha (+2,96 pts), diagramas de dispersión e IQR, ajuste econométrico MCO socioinstitucional ($r = 0,88$) y anatomía apilada de los 143 países.
  3. **Clasificación Integral (Rankings):** Tabla de datos completa de las 143 naciones con ordenamiento dinámico multi-columna, intervalos al 95% y los 7 componentes aditivos.
  4. **Metodología y Definiciones (Variables & Metodología):** Fichas técnicas de cada indicador, fuentes primarias y formulación del modelo de Distopía.
* **Filtros Reactivos y Ficha de País:** Buscador con menú predictivo y chips de segmentación cuartílica (*World*, *25% Superior*, *50% Central*, *25% Inferior*) que filtran en tiempo real todas las vistas y despliegan fichas técnicas detalladas (*modal*) para cualquier nación.

---

## 🔬 Metodología Analítica: La Gran Brecha (+2,96 pts)

Para contrastar de forma reproducible y neutral a los países con **alta** y **baja** evaluación de vida (sin umbrales arbitrarios), se dividieron las 143 naciones en cuartiles empíricos:
* **25% Superior ($Q4$):** 36 naciones con puntaje $\ge 6,42$ pts (desde Finlandia con 7,74 hasta España y Polonia con 6,44). Promedio: **6,88 pts**.
* **50% Central:** 71 naciones con puntajes entre 4,73 y 6,41 pts (como Colombia con 5,70 pts, Brasil, Grecia y Japón).
* **25% Inferior ($Q1$):** 36 naciones con puntaje $\le 4,73$ pts (desde Jordania con 4,19 hasta Afganistán con 1,72). Promedio: **3,91 pts**.

### Descomposición de la Brecha Promedio:
$$\Delta_{\text{Total}} = 6,88 - 3,91 = +2,96 \text{ puntos}$$

| Factor / Condición | Brecha Absoluta | % Brecha Total | Impacto Estandarizado ($z$) | Hallazgo Clave |
| :--- | :---: | :---: | :---: | :--- |
| **Condición Socioinstitucional** (Apoyo + Libertad + Probidad) | **+1,09 pts** | **36,8 %** | **3,5 $z$** | Factor colectivo más diferenciador; correlación $r = 0,88$ con la evaluación de vida. |
| **Condición Económica** (PIB per cápita logarítmico) | **+0,90 pts** | **30,4 %** | **3,9 $z$** | Mayor brecha individual; base indispensable para financiar servicios de bienestar. |
| **Condición de Salud** (Esperanza de vida saludable) | **+0,32 pts** | **10,8 %** | **3,2 $z$** | Brecha biológica acumulativa entre sistemas sanitarios avanzados y frágiles. |
| **Distopía + residuo** (Crisis, conflicto y choque no modelado) | **+0,65 pts** | **22,0 %** | --- | Residuos fuertemente negativos en naciones colapsadas (Líbano $-2,80$, Afganistán $-2,05$). |
| **Generosidad** (Donaciones caritativas) | **+0,02 pts** | **0,7 %** | **0,2 $z$** | No discrimina el nivel de bienestar agregado de las naciones. |

---

## 🚀 Instrucciones de Reproducción y Ejecución

### 1. Clonar el repositorio
```bash
git clone https://github.com/eljarcor98/Proyecto-2-Visualizacion.git
cd Proyecto-2-Visualizacion
```

### 2. Configurar entorno de Python
Se requiere Python 3.10 o superior:
```bash
pip install pandas numpy matplotlib seaborn plotly openpyxl nbformat nbclient
```

### 3. Ejecutar el Cuaderno Principal
El cuaderno se ejecuta de principio a fin de manera 100% desatendida:
```bash
python -c "import nbformat; from nbclient import NotebookClient; nb = nbformat.read('notebooks/EquipoX_Proyecto2_Visualizacion.ipynb', as_version=4); client = NotebookClient(nb, timeout=600); client.execute(); nbformat.write(nb, 'notebooks/EquipoX_Proyecto2_Visualizacion.ipynb'); print('[OK] Notebook ejecutado con exito')"
```

### 4. Compilar los Documentos en PDF (LaTeX)
El repositorio incluye el motor ejecutable autónomo `tectonic.exe` en `bin/`, por lo que **no se requiere instalar MiKTeX ni TeX Live**:
* Para compilar el informe técnico maestro:
  ```bash
  python docs/fase1_audiencia_pregunta/compilar.py
  ```
* Para compilar el resumen ejecutivo de 3 páginas:
  ```bash
  python docs/entregables/compilar.py
  ```

### 5. Generar o Visualizar el Portal Interactivo
Para compilar y exportar el tablero interactivo HTML:
```bash
python create_storytelling_dashboard.py
```
El archivo se abre en cualquier navegador web moderno:
`exports/EquipoX_Proyecto2_Dashboard.html`
