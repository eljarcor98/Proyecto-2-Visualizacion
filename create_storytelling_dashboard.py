import os
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

def build_dashboard():
    # 1. Cargar y preparar datos
    posibles_rutas = [
        os.path.join('data', 'raw', 'WHR24_Data_Figure_2.1.xls'),
        os.path.join('..', 'data', 'raw', 'WHR24_Data_Figure_2.1.xls'),
        os.path.join('data', 'WHR24_Data_Figure_2.1.xls'),
        'WHR24_Data_Figure_2.1.xls'
    ]
    ruta_datos = next((r for r in posibles_rutas if os.path.exists(r)), None)
    if not ruta_datos:
        raise FileNotFoundError("Archivo WHR24_Data_Figure_2.1.xls no encontrado.")
    
    df_raw = pd.read_excel(ruta_datos)
    df = df_raw.copy()

    # Diccionario exhaustivo de los 143 países del reporte oficial traducidos al español
    traduccion_paises = {
        'Finland': 'Finlandia', 'Denmark': 'Dinamarca', 'Iceland': 'Islandia', 'Sweden': 'Suecia',
        'Israel': 'Israel', 'Netherlands': 'Países Bajos', 'Norway': 'Noruega', 'Luxembourg': 'Luxemburgo',
        'Switzerland': 'Suiza', 'Australia': 'Australia', 'New Zealand': 'Nueva Zelanda', 'Costa Rica': 'Costa Rica',
        'Kuwait': 'Kuwait', 'Austria': 'Austria', 'Canada': 'Canadá', 'Belgium': 'Bélgica',
        'Ireland': 'Irlanda', 'Czechia': 'República Checa', 'Lithuania': 'Lituania', 'United Kingdom': 'Reino Unido',
        'Slovenia': 'Eslovenia', 'United Arab Emirates': 'Emiratos Árabes Unidos', 'United States': 'Estados Unidos',
        'Germany': 'Alemania', 'Mexico': 'México', 'Uruguay': 'Uruguay', 'France': 'Francia',
        'Saudi Arabia': 'Arabia Saudita', 'Kosovo': 'Kosovo', 'Singapore': 'Singapur',
        'Taiwan Province of China': 'Taiwán', 'Romania': 'Rumania', 'El Salvador': 'El Salvador',
        'Estonia': 'Estonia', 'Poland': 'Polonia', 'Spain': 'España', 'Serbia': 'Serbia', 'Chile': 'Chile',
        'Panama': 'Panamá', 'Malta': 'Malta', 'Italy': 'Italia', 'Guatemala': 'Guatemala',
        'Nicaragua': 'Nicaragua', 'Brazil': 'Brasil', 'Slovakia': 'Eslovaquia', 'Latvia': 'Letonia',
        'Uzbekistan': 'Uzbekistán', 'Argentina': 'Argentina', 'Kazakhstan': 'Kazajistán', 'Cyprus': 'Chipre',
        'Japan': 'Japón', 'South Korea': 'Corea del Sur', 'Philippines': 'Filipinas', 'Vietnam': 'Vietnam',
        'Portugal': 'Portugal', 'Hungary': 'Hungría', 'Paraguay': 'Paraguay', 'Thailand': 'Tailandia',
        'Malaysia': 'Malasia', 'China': 'China', 'Honduras': 'Honduras', 'Bahrain': 'Baréin',
        'Croatia': 'Croacia', 'Greece': 'Grecia', 'Bosnia and Herzegovina': 'Bosnia y Herzegovina',
        'Libya': 'Libia', 'Jamaica': 'Jamaica', 'Peru': 'Perú', 'Dominican Republic': 'República Dominicana',
        'Mauritius': 'Mauricio', 'Moldova': 'Moldavia', 'Russia': 'Rusia', 'Bolivia': 'Bolivia',
        'Ecuador': 'Ecuador', 'Kyrgyzstan': 'Kirguistán', 'Montenegro': 'Montenegro', 'Mongolia': 'Mongolia',
        'Colombia': 'Colombia', 'Venezuela': 'Venezuela', 'Indonesia': 'Indonesia', 'Bulgaria': 'Bulgaria',
        'Armenia': 'Armenia', 'South Africa': 'Sudáfrica', 'North Macedonia': 'Macedonia del Norte',
        'Algeria': 'Argelia', 'Hong Kong S.A.R. of China': 'Hong Kong', 'Albania': 'Albania',
        'Tajikistan': 'Tayikistán', 'Congo (Brazzaville)': 'República del Congo', 'Mozambique': 'Mozambique',
        'Georgia': 'Georgia', 'Iraq': 'Irak', 'Nepal': 'Nepal', 'Laos': 'Laos', 'Gabon': 'Gabón',
        'Ivory Coast': 'Costa de Marfil', 'Guinea': 'Guinea', 'Turkiye': 'Turquía', 'Senegal': 'Senegal',
        'Iran': 'Irán', 'Azerbaijan': 'Azerbaiyán', 'Nigeria': 'Nigeria', 'State of Palestine': 'Palestina',
        'Cameroon': 'Camerún', 'Ukraine': 'Ucrania', 'Namibia': 'Namibia', 'Morocco': 'Marruecos',
        'Pakistan': 'Pakistán', 'Niger': 'Níger', 'Burkina Faso': 'Burkina Faso', 'Mauritania': 'Mauritania',
        'Gambia': 'Gambia', 'Chad': 'Chad', 'Kenya': 'Kenia', 'Tunisia': 'Túnez', 'Benin': 'Benín',
        'Uganda': 'Uganda', 'Myanmar': 'Birmania (Myanmar)', 'Cambodia': 'Camboya', 'Ghana': 'Ghana',
        'Liberia': 'Liberia', 'Mali': 'Malí', 'Madagascar': 'Madagascar', 'Togo': 'Togo', 'Jordan': 'Jordania',
        'India': 'India', 'Egypt': 'Egipto', 'Sri Lanka': 'Sri Lanka', 'Bangladesh': 'Bangladés',
        'Ethiopia': 'Etiopía', 'Tanzania': 'Tanzania', 'Comoros': 'Comoras', 'Yemen': 'Yemen',
        'Zambia': 'Zambia', 'Eswatini': 'Esuatini', 'Malawi': 'Malaui', 'Botswana': 'Botsuana',
        'Zimbabwe': 'Zimbabue', 'Congo (Kinshasa)': 'R. D. del Congo', 'Sierra Leone': 'Sierra Leona',
        'Lesotho': 'Lesoto', 'Lebanon': 'Líbano', 'Afghanistan': 'Afganistán'
    }
    
    df['Pais_ES'] = df['Country name'].map(lambda c: traduccion_paises.get(c, c))
    
    # Cortes del 25% (Cuartiles empíricos sobre la distribución global de la Escalera de Cantril)
    corte_inferior_25 = df['Ladder score'].quantile(0.25)  # 4.726 pts
    corte_superior_25 = df['Ladder score'].quantile(0.75)  # 6.416 pts
    
    G_BAJO = '25% Inferior (Bajo Bienestar)'
    G_ALTO = '25% Superior (Alto Bienestar)'
    G_MEDIO = '50% Central (Bienestar Intermedio)'
    
    def asignar_grupo(s):
        if s <= corte_inferior_25:
            return G_BAJO
        elif s >= corte_superior_25:
            return G_ALTO
        else:
            return G_MEDIO
            
    df['Grupo_Bienestar'] = df['Ladder score'].apply(asignar_grupo)
    
    # Columnas explicadas
    cols_contrib = [c for c in df.columns if c.startswith('Explained by:')]
    df_dims = df.dropna(subset=cols_contrib).copy()
    
    # Condición Socioinstitucional (suma de soporte, libertad y baja corrupción)
    df_dims['Suma_Socioinstitucional'] = (
        df_dims['Explained by: Social support'] +
        df_dims['Explained by: Freedom to make life choices'] +
        df_dims['Explained by: Perceptions of corruption']
    )
    
    # Subconjunto de contraste de extremos (25% Superior vs. 25% Inferior: 36 + 36 = 72 países)
    df_extremos = df_dims[df_dims['Grupo_Bienestar'].isin([G_BAJO, G_ALTO])].copy()
    
    # Nombres formales y amigables en español de las variables
    nombres_variables_es = {
        'Explained by: Log GDP per capita': 'PIB per cápita (Condición Económica)',
        'Explained by: Social support': 'Apoyo social (Condición Socioinstitucional)',
        'Explained by: Healthy life expectancy': 'Esperanza de vida saludable (Condición de Salud)',
        'Explained by: Freedom to make life choices': 'Libertad de elección vital (Condición Socioinstitucional)',
        'Explained by: Perceptions of corruption': 'Confianza institucional (Baja corrupción)',
        'Explained by: Generosity': 'Generosidad y altruismo (Solidaridad)',
        'Dystopia + residual': 'Distopía + residuo (Base no explicada)'
    }

    # =========================================================================
    # GRÁFICO 1: MAPA MUNDIAL COROPLÉTICO (Z-PATTERN: POSICIÓN TOP-RIGHT)
    # =========================================================================
    fig_map = px.choropleth(
        df,
        locations='Country name',
        locationmode='country names',
        color='Ladder score',
        color_continuous_scale='Plasma',
    )
    
    fig_map.data[0].customdata = np.stack((
        df['Pais_ES'],
        df['Ladder score'],
        df['lowerwhisker'],
        df['upperwhisker'],
        df['Grupo_Bienestar'],
        df['Explained by: Log GDP per capita'].fillna(0),
        df['Explained by: Social support'].fillna(0)
    ), axis=-1)
    
    fig_map.data[0].hovertemplate = (
        "<b>%{customdata[0]}</b><br><br>"
        "<b>Evaluación de vida (Escalera Cantril):</b> %{customdata[1]:.2f} / 10<br>"
        "<b>Intervalo 95%:</b> [%{customdata[2]:.2f} — %{customdata[3]:.2f}]<br>"
        "<b>Segmento:</b> %{customdata[4]}<br>"
        "• PIB per cápita (Económica): %{customdata[5]:.2f} pts<br>"
        "• Apoyo social (Socioinstitucional): %{customdata[6]:.2f} pts<br>"
        "<extra></extra>"
    )
    
    fig_map.update_layout(
        template='plotly_dark',
        paper_bgcolor='#111827',
        plot_bgcolor='#111827',
        font=dict(color='#e2e8f0', family='Plus Jakarta Sans, sans-serif'),
        margin=dict(l=0, r=0, t=10, b=0),
        height=430,
        geo=dict(
            showframe=False,
            showcoastlines=True,
            coastlinecolor='#374151',
            projection_type='natural earth',
            bgcolor='#111827'
        ),
        coloraxis_colorbar=dict(
            title='Escalera Cantril',
            thickness=12,
            len=0.75,
            tickfont=dict(color='#cbd5e1', size=10)
        )
    )

    # =========================================================================
    # GRÁFICO 2: DISTRIBUCIÓN Y DISPERSIÓN (Z-PATTERN: POSICIÓN MIDDLE-LEFT)
    # =========================================================================
    componentes_dist = [
        ('Explained by: Log GDP per capita', 'PIB per cápita (Económica)', '#38bdf8'),
        ('Explained by: Social support', 'Apoyo social (Socioinstitucional)', '#f59e0b'),
        ('Explained by: Healthy life expectancy', 'Esperanza de vida (Salud)', '#10b981'),
        ('Explained by: Freedom to make life choices', 'Libertad para decidir', '#fbbf24'),
        ('Explained by: Perceptions of corruption', 'Confianza / Probidad', '#d97706'),
        ('Explained by: Generosity', 'Generosidad (Solidaridad)', '#cbd5e1'),
        ('Dystopia + residual', 'Distopía + residuo (Base)', '#818cf8')
    ]

    fig_dist = go.Figure()

    for col, nombre, color in componentes_dist:
        sub = df.dropna(subset=[col]).copy()
        c_data = np.stack((sub['Pais_ES'], sub['Ladder score'], sub['Grupo_Bienestar']), axis=-1)
        fig_dist.add_trace(go.Box(
            x=sub[col],
            name=nombre,
            boxpoints='all',
            jitter=0.35,
            pointpos=-1.6,
            marker=dict(color=color, size=5, opacity=0.75),
            line=dict(color=color, width=1.6),
            boxmean='sd',
            customdata=c_data,
            hovertemplate='<b>%{customdata[0]}</b><br>' + nombre + ': <b>%{x:.3f} pts</b><br>Evaluación: %{customdata[1]:.2f} pts<extra></extra>',
            visible=True
        ))

    sub_ladder = df.dropna(subset=['Ladder score']).copy()
    c_data_l = np.stack((sub_ladder['Pais_ES'], sub_ladder['Ladder score'], sub_ladder['Grupo_Bienestar']), axis=-1)
    fig_dist.add_trace(go.Box(
        x=sub_ladder['Ladder score'],
        name='Evaluación de Vida (0 a 10)',
        boxpoints='all',
        jitter=0.35,
        pointpos=-1.6,
        marker=dict(color='#38bdf8', size=6, opacity=0.8),
        line=dict(color='#38bdf8', width=2),
        boxmean='sd',
        customdata=c_data_l,
        hovertemplate='<b>%{customdata[0]}</b><br>Evaluación: <b>%{x:.2f} pts</b><br>Segmento: %{customdata[2]}<extra></extra>',
        visible=False
    ))

    botones_dist = [
        dict(
            label='7 Componentes (0 a 3 pts)',
            method='update',
            args=[
                {'visible': [True]*7 + [False]},
                {
                    'xaxis.title': 'Puntos en la Escalera de Cantril',
                    'xaxis.range': [-0.15, 3.15]
                }
            ]
        ),
        dict(
            label='Evaluación Total (0 a 10 pts)',
            method='update',
            args=[
                {'visible': [False]*7 + [True]},
                {
                    'xaxis.title': 'Evaluación de Vida (Escalera Cantril, 0 a 10 pts)',
                    'xaxis.range': [1.2, 8.2]
                }
            ]
        )
    ]

    fig_dist.update_layout(
        template='plotly_dark',
        paper_bgcolor='#111827',
        plot_bgcolor='#111827',
        font=dict(color='#e2e8f0', family='Plus Jakarta Sans, sans-serif'),
        height=430,
        margin=dict(l=10, r=20, t=55, b=40),
        xaxis=dict(title='Puntos en la Escalera de Cantril', gridcolor='#1f2937', range=[-0.15, 3.15]),
        yaxis=dict(gridcolor='#1f2937', tickfont=dict(size=10)),
        showlegend=False,
        updatemenus=[
            dict(
                type='dropdown',
                active=0,
                buttons=botones_dist,
                x=0.0,
                y=1.16,
                xanchor='left',
                bgcolor='#1e293b',
                bordercolor='#475569',
                font=dict(color='#f8fafc', size=11)
            )
        ]
    )

    # =========================================================================
    # GRÁFICO 3: BRECHAS PROMEDIO (Z-PATTERN: POSICIÓN MIDDLE-RIGHT)
    # =========================================================================
    prom_alto = df_extremos[df_extremos['Grupo_Bienestar'] == G_ALTO][cols_contrib + ['Dystopia + residual']].mean()
    prom_bajo = df_extremos[df_extremos['Grupo_Bienestar'] == G_BAJO][cols_contrib + ['Dystopia + residual']].mean()
    brecha = (prom_alto - prom_bajo).sort_values(ascending=True)
    
    etiquetas_brecha = [nombres_variables_es.get(k, k) for k in brecha.index]
    colores_brecha = [
        '#38bdf8' if 'Económica' in e else
        '#10b981' if 'Salud' in e else
        '#f59e0b' if 'Socioinstitucional' in e or 'corrupción' in e else '#94a3b8'
        for e in etiquetas_brecha
    ]
    
    fig_brecha = go.Figure(go.Bar(
        x=brecha.values,
        y=etiquetas_brecha,
        orientation='h',
        marker=dict(color=colores_brecha, line=dict(width=1, color='#1e293b')),
        text=[f"+{v:.2f} pts" for v in brecha.values],
        textposition='outside',
        cliponaxis=False,
        hovertemplate='<b>%{y}</b><br>Brecha promedio: <b>+%{x:.2f} puntos</b><extra></extra>'
    ))
    fig_brecha.update_layout(
        template='plotly_dark',
        paper_bgcolor='#111827',
        plot_bgcolor='#111827',
        font=dict(color='#e2e8f0', family='Plus Jakarta Sans, sans-serif'),
        xaxis=dict(title='Diferencia Promedio en Puntos (25% Sup. − 25% Inf.)', range=[0, 1.15], gridcolor='#1f2937'),
        yaxis=dict(gridcolor='#1f2937', tickfont=dict(size=10)),
        margin=dict(l=10, r=40, t=15, b=40),
        height=430
    )

    # =========================================================================
    # GRÁFICO 4: DISPERSIÓN MULTIDIMENSIONAL (Z-PATTERN: POSICIÓN BOTTOM-LEFT)
    # =========================================================================
    colores_grupos = {
        G_ALTO: '#38bdf8',
        G_MEDIO: '#64748b',
        G_BAJO: '#f43f5e'
    }
    
    fig_scatter = go.Figure()
    
    x_vals = df_dims['Suma_Socioinstitucional']
    y_vals = df_dims['Ladder score']
    m, b = np.polyfit(x_vals, y_vals, 1)
    r_corr = np.corrcoef(x_vals, y_vals)[0, 1]
    
    x_line = np.linspace(x_vals.min(), x_vals.max(), 100)
    y_line = m * x_line + b
    
    fig_scatter.add_trace(go.Scatter(
        x=x_line,
        y=y_line,
        mode='lines',
        name=f'Ajuste OLS (r = {r_corr:.2f})',
        line=dict(color='#cbd5e1', dash='dash', width=2),
        hoverinfo='skip'
    ))
    
    for grupo, color in colores_grupos.items():
        sub = df_dims[df_dims['Grupo_Bienestar'] == grupo]
        fig_scatter.add_trace(go.Scatter(
            x=sub['Suma_Socioinstitucional'],
            y=sub['Ladder score'],
            mode='markers',
            name=grupo,
            marker=dict(
                size=10,
                color=color,
                line=dict(width=1, color='#0f172a'),
                opacity=0.88
            ),
            customdata=sub[['Pais_ES', 'Explained by: Log GDP per capita', 'Explained by: Social support', 'Explained by: Freedom to make life choices', 'Explained by: Perceptions of corruption', 'Grupo_Bienestar']],
            hovertemplate=(
                '<b>%{customdata[0]}</b><br>' +
                '<b>Evaluación vital:</b> %{y:.2f} pts<br>' +
                '<b>Socioinstitucional total:</b> %{x:.2f} pts<br>' +
                '  • Apoyo social: %{customdata[2]:.2f} pts<br>' +
                '  • Libertad vital: %{customdata[3]:.2f} pts<br>' +
                '  • Probidad: %{customdata[4]:.2f} pts<br>' +
                '<b>PIB per cápita:</b> %{customdata[1]:.2f} pts' +
                '<extra></extra>'
            )
        ))
        
    casos_destacados = [
        ('Botswana', 'Botsuana'),
        ('Lebanon', 'Líbano'),
        ('Afghanistan', 'Afganistán'),
        ('Costa Rica', 'Costa Rica'),
        ('Finland', 'Finlandia')
    ]
    
    for pais_orig, pais_es in casos_destacados:
        match = df_dims[df_dims['Country name'] == pais_orig]
        if not match.empty:
            actual_x = match['Suma_Socioinstitucional'].values[0]
            actual_y = match['Ladder score'].values[0]
            fig_scatter.add_annotation(
                x=actual_x,
                y=actual_y,
                text=pais_es,
                showarrow=True,
                arrowhead=2,
                arrowsize=1,
                arrowwidth=1.5,
                arrowcolor='#f59e0b',
                font=dict(color='#f8fafc', size=10, family='Plus Jakarta Sans'),
                bgcolor='rgba(15, 23, 42, 0.9)',
                bordercolor='#f59e0b',
                borderwidth=1,
                borderpad=3,
                ay=-26 if actual_y > 4.5 else 26
            )
            
    fig_scatter.update_layout(
        template='plotly_dark',
        paper_bgcolor='#111827',
        plot_bgcolor='#111827',
        font=dict(color='#e2e8f0', family='Plus Jakarta Sans, sans-serif'),
        xaxis=dict(title='Condición Socioinstitucional (Apoyo + Libertad + Probidad, pts)', gridcolor='#1f2937'),
        yaxis=dict(title='Evaluación de Vida (Cantril, 0 a 10)', gridcolor='#1f2937'),
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='left',
            x=0.0,
            font=dict(size=9.5)
        ),
        margin=dict(l=40, r=20, t=55, b=45),
        height=520
    )

    # =========================================================================
    # GRÁFICO 5: DESCOMPOSICIÓN ADITIVA (Z-PATTERN: POSICIÓN BOTTOM-RIGHT)
    # =========================================================================
    alto_sorted = df_extremos[df_extremos['Grupo_Bienestar'] == G_ALTO].sort_values('Ladder score')
    bajo_sorted = df_extremos[df_extremos['Grupo_Bienestar'] == G_BAJO].sort_values('Ladder score')
    
    mapa_componentes_es = {
        'Explained by: Log GDP per capita': ('PIB per cápita (Económica)', '#38bdf8'),
        'Explained by: Social support': ('Apoyo social (Socioinstitucional)', '#f59e0b'),
        'Explained by: Healthy life expectancy': ('Esperanza de vida (Salud)', '#10b981'),
        'Explained by: Freedom to make life choices': ('Libertad vital (Socioinstitucional)', '#fbbf24'),
        'Explained by: Perceptions of corruption': ('Confianza institucional (Probidad)', '#d97706'),
        'Explained by: Generosity': ('Generosidad (Solidaridad)', '#cbd5e1'),
        'Dystopia + residual': ('Distopía + residuo (Base común)', '#818cf8')
    }
    
    fig_comp = go.Figure()
    
    for col, (nombre_es, color) in mapa_componentes_es.items():
        fig_comp.add_trace(go.Bar(
            name=nombre_es,
            y=alto_sorted['Pais_ES'],
            x=alto_sorted[col],
            orientation='h',
            marker_color=color,
            hovertemplate='<b>%{y}</b><br>' + nombre_es + ': <b>%{x:.2f} pts</b><extra></extra>'
        ))
        
    botones_comp = [
        dict(
            label='25% Superior (Alto Bienestar · 36 países)',
            method='update',
            args=[
                {
                    'x': [alto_sorted[c].tolist() for c in mapa_componentes_es.keys()],
                    'y': [alto_sorted['Pais_ES'].tolist()] * len(mapa_componentes_es)
                },
                {
                    'yaxis.categoryarray': alto_sorted['Pais_ES'].tolist()
                }
            ]
        ),
        dict(
            label='25% Inferior (Bajo Bienestar · 36 países)',
            method='update',
            args=[
                {
                    'x': [bajo_sorted[c].tolist() for c in mapa_componentes_es.keys()],
                    'y': [bajo_sorted['Pais_ES'].tolist()] * len(mapa_componentes_es)
                },
                {
                    'yaxis.categoryarray': bajo_sorted['Pais_ES'].tolist()
                }
            ]
        )
    ]
    
    fig_comp.update_layout(
        template='plotly_dark',
        paper_bgcolor='#111827',
        plot_bgcolor='#111827',
        font=dict(color='#e2e8f0', family='Plus Jakarta Sans, sans-serif'),
        barmode='stack',
        height=520,
        xaxis=dict(
            title=dict(text='Puntos de Calidad de Vida (0 a 8 pts)', standoff=12),
            range=[0, 8.2],
            gridcolor='#1f2937'
        ),
        yaxis=dict(categoryorder='array', categoryarray=alto_sorted['Pais_ES'].tolist(), tickfont=dict(size=8.5)),
        legend=dict(
            title=dict(text='<b>Componente:</b>', font=dict(color='#f8fafc', size=9)),
            orientation='h',
            yanchor='top',
            y=-0.17,
            xanchor='center',
            x=0.5,
            font=dict(size=8.5)
        ),
        margin=dict(l=10, r=20, t=65, b=105),
        updatemenus=[
            dict(
                type='dropdown',
                active=0,
                buttons=botones_comp,
                x=0.0,
                y=1.16,
                xanchor='left',
                bgcolor='#1e293b',
                bordercolor='#475569',
                font=dict(color='#f8fafc', size=11)
            )
        ]
    )

    # =========================================================================
    # MATRIZ DE ESTADÍSTICOS DESCRIPTIVOS ROBUSTOS (TABLA HTML)
    # =========================================================================
    columnas_analisis = [
        ('Ladder score', 'Evaluación de Vida (Cantril)', 'Variable Objetivo / Dependiente', '#38bdf8'),
        ('Explained by: Log GDP per capita', 'PIB per cápita (Log)', 'Condición Económica', '#38bdf8'),
        ('Explained by: Social support', 'Apoyo Social (Auxilio)', 'Condición Socioinstitucional', '#f59e0b'),
        ('Explained by: Healthy life expectancy', 'Esperanza de Vida Saludable', 'Condición de Salud', '#10b981'),
        ('Explained by: Freedom to make life choices', 'Libertad para Decidir', 'Condición Socioinstitucional', '#fbbf24'),
        ('Explained by: Perceptions of corruption', 'Confianza Institucional', 'Condición Socioinstitucional', '#d97706'),
        ('Explained by: Generosity', 'Generosidad (Solidaridad)', 'Dimensión Solidaria', '#cbd5e1'),
        ('Dystopia + residual', 'Distopía + Residuo', 'Línea Base y Residuo', '#818cf8')
    ]

    filas_tabla_stats = ""
    for col_key, nombre_es, dim_es, col_hex in columnas_analisis:
        s = df[col_key].dropna()
        media = s.mean()
        mediana = s.median()
        std = s.std()
        min_v = s.min()
        q1 = s.quantile(0.25)
        q3 = s.quantile(0.75)
        max_v = s.max()
        iqr = q3 - q1
        cv = (std / media) * 100 if media != 0 else 0
        asimetria = s.skew()

        if cv < 28:
            cv_class = "cv-low"
            cv_label = f"{cv:.1f}% (Baja)"
        elif cv <= 40:
            cv_class = "cv-mid"
            cv_label = f"{cv:.1f}% (Moderada)"
        elif cv <= 60:
            cv_class = "cv-high"
            cv_label = f"{cv:.1f}% (Alta)"
        else:
            cv_class = "cv-extreme"
            cv_label = f"{cv:.1f}% (Extrema)"

        if asimetria < -0.8:
            forma = "Sesgo a la izquierda (concentración alta con cola crítica)"
        elif asimetria < -0.2:
            forma = "Sesgo moderado a la izquierda (cola vulnerable)"
        elif asimetria <= 0.2:
            forma = "Aproximadamente simétrica"
        elif asimetria <= 0.8:
            forma = "Sesgo moderado a la derecha"
        else:
            forma = "Sesgo muy positivo (el 80% percibe alta corrupción)"

        filas_tabla_stats += f"""
        <tr>
            <td>
                <div style="font-weight: 700; color: #f8fafc;">{nombre_es}</div>
                <div style="font-size: 0.72rem; color: var(--text-muted); font-family: 'JetBrains Mono';">{col_key}</div>
            </td>
            <td><span class="dim-badge" style="background: {col_hex}22; color: {col_hex}; border-color: {col_hex}55;">{dim_es}</span></td>
            <td><strong style="color: #f8fafc;">{media:.2f}</strong> <span style="color: var(--text-muted);">± {std:.2f}</span></td>
            <td><strong style="color: var(--accent-blue);">{mediana:.2f}</strong></td>
            <td>[{min_v:.2f} — {max_v:.2f}]</td>
            <td>[{q1:.2f} — {q3:.2f}] <span style="font-size: 0.7rem; color: var(--text-muted);">(IQR: {iqr:.2f})</span></td>
            <td><span class="cv-badge {cv_class}">{cv_label}</span></td>
            <td style="font-size: 0.78rem; color: var(--text-secondary);">{forma}</td>
        </tr>
        """

    # =========================================================================
    # DICCIONARIO DE VARIABLES METADATA
    # =========================================================================
    variables_metadata = [
        {
            'col_en': 'Country name', 'nombre_es': 'País o Territorio', 'dim': 'Identificador Geográfico', 'color': '#94a3b8',
            'fuente': 'Naciones Unidas / ISO', 'rango': '143 naciones', 'media': 'N/A',
            'def_corta': 'Nombre del país o territorio soberano objeto de análisis comparativo.',
            'metodologia': 'Muestras probabilísticas nacionales de adultos representativas a nivel de país (Gallup World Poll).'
        },
        {
            'col_en': 'Ladder score', 'nombre_es': 'Evaluación de Vida (Escalera de Cantril)', 'dim': 'Variable Objetivo / Bienestar', 'color': '#38bdf8',
            'fuente': 'Gallup World Poll (2021–2023)', 'rango': '1,72 a 7,74 pts', 'media': '5,53 pts',
            'def_corta': 'Medida central del bienestar evaluativo en escala continua de 0 (peor vida posible) a 10 (mejor vida posible).',
            'metodologia': '«Imagine una escalera con peldaños del 0 al 10. ¿En qué peldaño siente que está hoy?». Promedio trienal ponderado.'
        },
        {
            'col_en': 'upperwhisker / lowerwhisker', 'nombre_es': 'Intervalo de Confianza al 95%', 'dim': 'Precisión Muestral', 'color': '#64748b',
            'fuente': 'Gallup World Poll', 'rango': '[1,67 a 7,82] pts', 'media': 'Amplitud ±0,11 pts',
            'def_corta': 'Cotas que delimitan la incertidumbre estadística muestral al 95% para la estimación media del Ladder Score.',
            'metodologia': 'Calculado a partir de los errores estándar del diseño de muestreo complejo de cada país.'
        },
        {
            'col_en': 'Explained by: Log GDP per capita', 'nombre_es': 'PIB per cápita (Log) — Condición Económica', 'dim': 'Condición Económica', 'color': '#38bdf8',
            'fuente': 'Banco Mundial (WDI) / Penn', 'rango': '0,00 a 2,14 pts', 'media': '1,38 pts',
            'def_corta': 'Aporte del nivel de ingreso real y productividad por habitante a la evaluación de vida.',
            'metodologia': 'Logaritmo del PIB per cápita a Paridad de Poder Adquisitivo (PPA, dólares constantes 2017) ponderado en el modelo de panel.'
        },
        {
            'col_en': 'Explained by: Social support', 'nombre_es': 'Apoyo Social — Condición Socioinstitucional', 'dim': 'Condición Socioinstitucional', 'color': '#f59e0b',
            'fuente': 'Gallup World Poll', 'rango': '0,00 a 1,62 pts', 'media': '1,13 pts',
            'def_corta': 'Aporte de la disponibilidad percibida de redes de contención y ayuda en momentos de dificultad.',
            'metodologia': '«Si estuviera en problemas, ¿cuenta con familiares o amigos con quienes pueda contar para que lo ayuden cuando lo necesite?»'
        },
        {
            'col_en': 'Explained by: Healthy life expectancy', 'nombre_es': 'Esperanza de Vida Saludable — Condición de Salud', 'dim': 'Condición de Salud', 'color': '#10b981',
            'fuente': 'OMS (Global Health Obs.)', 'rango': '0,00 a 0,86 pts', 'media': '0,52 pts',
            'def_corta': 'Aporte de los años esperados de vida en buen estado de salud física y mental libre de discapacidad.',
            'metodologia': 'Años de vida saludable al nacer (HALE) normalizados respecto al mínimo teórico y ponderados en la regresión.'
        },
        {
            'col_en': 'Explained by: Freedom to make life choices', 'nombre_es': 'Libertad para Decidir — Condición Socioinstitucional', 'dim': 'Condición Socioinstitucional', 'color': '#fbbf24',
            'fuente': 'Gallup World Poll', 'rango': '0,00 a 0,86 pts', 'media': '0,62 pts',
            'def_corta': 'Aporte de la sensación de autonomía personal para orientar y decidir sobre el propio proyecto de vida.',
            'metodologia': '«¿Está satisfecho o insatisfecho con su libertad para elegir lo que hace con su vida?» (Tasa de respuesta afirmativa).'
        },
        {
            'col_en': 'Explained by: Generosity', 'nombre_es': 'Generosidad — Solidaridad y Altruismo', 'dim': 'Dimensión Solidaria', 'color': '#94a3b8',
            'fuente': 'Gallup World Poll', 'rango': '0,00 a 0,40 pts', 'media': '0,15 pts',
            'def_corta': 'Aporte de las prácticas prosociales y disposición a donar dinero para causas humanitarias.',
            'metodologia': 'Residuo de la tasa de donaciones monetarias en el último mes tras controlar por el nivel de PIB per cápita.'
        },
        {
            'col_en': 'Explained by: Perceptions of corruption', 'nombre_es': 'Confianza Institucional — Condición Socioinstitucional', 'dim': 'Condición Socioinstitucional', 'color': '#d97706',
            'fuente': 'Gallup World Poll', 'rango': '0,00 a 0,57 pts', 'media': '0,15 pts',
            'def_corta': 'Aporte de la probidad pública y ausencia de prácticas corruptas en el gobierno y el sector privado.',
            'metodologia': 'Promedio inverso de dos preguntas: «¿Está la corrupción extendida en el gobierno?» y «¿en las empresas?». Mayor puntaje = mayor probidad.'
        },
        {
            'col_en': 'Dystopia + residual', 'nombre_es': 'Distopía + Residuo — Línea Base y No Explicado', 'dim': 'Línea Base y Residuo', 'color': '#818cf8',
            'fuente': 'WHR 2024 (Econométrico)', 'rango': '-0,07 a 3,00 pts', 'media': '1,58 pts',
            'def_corta': 'Puntaje base del país hipotético con los peores indicadores del mundo (Distopía = 1,714 pts) más el error no modelado.',
            'metodologia': 'Suma del valor hipotético de Distopía más el residuo nacional específico de la regresión lineal multivariada.'
        }
    ]

    cards_html = ""
    for v in variables_metadata:
        cards_html += f"""
        <div class="dict-card" data-dim="{v['dim']}">
            <div class="dict-card-header">
                <span class="dim-badge" style="background: {v['color']}22; color: {v['color']}; border-color: {v['color']}44;">{v['dim']}</span>
                <span class="type-tag">{v['fuente']}</span>
            </div>
            <div class="dict-name-es">{v['nombre_es']}</div>
            <div class="dict-name-en"><code>{v['col_en']}</code></div>
            <p class="dict-desc">{v['def_corta']}</p>
            <div class="dict-meta-grid">
                <div class="dict-meta-item">
                    <span class="meta-label">Rango:</span>
                    <span class="meta-val">{v['rango']}</span>
                </div>
                <div class="dict-meta-item">
                    <span class="meta-label">Promedio:</span>
                    <span class="meta-val">{v['media']}</span>
                </div>
            </div>
            <div class="dict-method">
                <strong>Medición:</strong> {v['metodologia']}
            </div>
        </div>
        """

    # HTML divs de Plotly
    html_map_div = fig_map.to_html(full_html=False, include_plotlyjs=False)
    html_dist_div = fig_dist.to_html(full_html=False, include_plotlyjs=False)
    html_brecha_div = fig_brecha.to_html(full_html=False, include_plotlyjs=False)
    html_scatter_div = fig_scatter.to_html(full_html=False, include_plotlyjs=False)
    html_comp_div = fig_comp.to_html(full_html=False, include_plotlyjs=False)

    dashboard_html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Tablero BI: Radiografía Global del Bienestar 2024</title>
    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
    <!-- Plotly CDN -->
    <script src="https://cdn.plot.ly/plotly-2.30.0.min.js"></script>
    <style>
        :root {{
            --bg-main: #0b0f19;
            --bg-card: #111827;
            --bg-card-hover: #1f2937;
            --border-card: #1f2937;
            --border-highlight: #374151;
            --text-primary: #f8fafc;
            --text-secondary: #94a3b8;
            --text-muted: #64748b;
            --accent-blue: #38bdf8;
            --accent-green: #10b981;
            --accent-amber: #f59e0b;
            --accent-rose: #f43f5e;
            --accent-purple: #818cf8;
        }}
        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}
        body {{
            background-color: var(--bg-main);
            color: var(--text-primary);
            font-family: 'Plus Jakarta Sans', sans-serif;
            line-height: 1.5;
            -webkit-font-smoothing: antialiased;
        }}
        .container {{
            max-width: 1440px;
            margin: 0 auto;
            padding: 0 1.25rem;
        }}
        
        /* Barra de Control Superior Estilo BI (Header Cockpit) */
        .bi-topbar {{
            background: rgba(17, 24, 39, 0.95);
            backdrop-filter: blur(12px);
            border-bottom: 1px solid var(--border-card);
            position: sticky;
            top: 0;
            z-index: 50;
            padding: 0.75rem 0;
        }}
        .bi-nav-wrap {{
            display: flex;
            flex-wrap: wrap;
            justify-content: space-between;
            align-items: center;
            gap: 1rem;
        }}
        .bi-brand {{
            display: flex;
            flex-direction: column;
        }}
        .bi-brand-meta {{
            font-size: 0.72rem;
            color: var(--accent-blue);
            text-transform: uppercase;
            letter-spacing: 0.08em;
            font-weight: 700;
        }}
        .bi-brand-title {{
            font-size: 1.15rem;
            font-weight: 800;
            background: linear-gradient(135deg, #f8fafc 0%, #cbd5e1 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        .bi-tabs {{
            display: flex;
            gap: 0.4rem;
            background: #0f172a;
            padding: 0.25rem;
            border-radius: 0.5rem;
            border: 1px solid var(--border-card);
        }}
        .bi-tab-btn {{
            background: transparent;
            color: var(--text-secondary);
            border: none;
            border-radius: 0.35rem;
            padding: 0.45rem 0.9rem;
            font-size: 0.8rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s ease;
            display: flex;
            align-items: center;
            gap: 0.4rem;
        }}
        .bi-tab-btn:hover {{
            color: var(--text-primary);
        }}
        .bi-tab-btn.active {{
            background: #1e293b;
            color: var(--accent-blue);
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
            border: 1px solid rgba(56, 189, 248, 0.25);
        }}

        /* Franja de Contexto Metodológico & Pregunta Analítica */
        .context-strip {{
            background: rgba(17, 24, 39, 0.6);
            border-bottom: 1px solid var(--border-card);
            padding: 0.85rem 0;
            font-size: 0.85rem;
        }}
        .context-flex {{
            display: flex;
            flex-wrap: wrap;
            justify-content: space-between;
            align-items: center;
            gap: 1rem;
        }}
        .analytical-q {{
            display: flex;
            align-items: center;
            gap: 0.5rem;
            color: var(--text-primary);
            font-size: 0.85rem;
            max-width: 950px;
        }}
        .q-badge {{
            font-size: 0.68rem;
            font-weight: 800;
            padding: 0.2rem 0.5rem;
            border-radius: 0.25rem;
            background: rgba(245, 158, 11, 0.15);
            color: var(--accent-amber);
            border: 1px solid rgba(245, 158, 11, 0.3);
            text-transform: uppercase;
            flex-shrink: 0;
        }}
        .meta-chips {{
            display: flex;
            gap: 0.75rem;
            font-size: 0.75rem;
            color: var(--text-muted);
        }}
        .meta-chips strong {{
            color: var(--text-secondary);
        }}

        /* Grid BI Symmetrical & Z-Pattern (Región Común y Simetría Gestalt) */
        .bi-board {{
            padding: 1.5rem 0 3rem;
        }}
        .bi-grid-2col {{
            display: grid;
            grid-template-columns: 1fr;
            gap: 1.25rem;
            margin-bottom: 1.25rem;
        }}
        @media (min-width: 1024px) {{
            .bi-grid-2col {{
                grid-template-columns: 1fr 1fr;
            }}
        }}

        /* Widgets BI (Región Común / Enclosure de Gestalt) */
        .bi-widget {{
            background: var(--bg-card);
            border: 1px solid var(--border-card);
            border-radius: 0.75rem;
            padding: 1.15rem;
            display: flex;
            flex-direction: column;
            box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.4);
            transition: border-color 0.2s ease;
        }}
        .bi-widget:hover {{
            border-color: var(--border-highlight);
        }}
        .bi-widget-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 0.75rem;
            padding-bottom: 0.5rem;
            border-bottom: 1px solid var(--border-card);
        }}
        .bi-widget-title {{
            font-size: 0.925rem;
            font-weight: 700;
            color: var(--text-primary);
            display: flex;
            align-items: center;
            gap: 0.45rem;
        }}
        .bi-widget-tag {{
            font-size: 0.68rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            padding: 0.18rem 0.5rem;
            border-radius: 9999px;
            background: rgba(56, 189, 248, 0.12);
            color: var(--accent-blue);
            border: 1px solid rgba(56, 189, 248, 0.25);
        }}
        .bi-widget-body {{
            flex-grow: 1;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }}
        .bi-widget-desc {{
            font-size: 0.78rem;
            color: var(--text-secondary);
            margin-bottom: 0.5rem;
            line-height: 1.4;
        }}

        /* Tarjeta Ejecutiva Top-Left (KPIs + Criterio 25% Proximidad Gestalt) */
        .kpi-grid-2x2 {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 0.65rem;
            margin-bottom: 0.75rem;
        }}
        .kpi-box {{
            background: rgba(15, 23, 42, 0.6);
            border: 1px solid var(--border-card);
            border-radius: 0.5rem;
            padding: 0.65rem 0.75rem;
        }}
        .kpi-box-label {{
            font-size: 0.66rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: var(--text-muted);
            margin-bottom: 0.15rem;
        }}
        .kpi-box-val {{
            font-size: 1.35rem;
            font-weight: 800;
            font-family: 'JetBrains Mono', monospace;
            line-height: 1.1;
            margin-bottom: 0.15rem;
        }}
        .kpi-box-sub {{
            font-size: 0.68rem;
            color: var(--text-secondary);
            line-height: 1.25;
        }}
        .criterio-box {{
            background: rgba(30, 41, 59, 0.4);
            border-left: 3px solid var(--accent-blue);
            border-radius: 0 0.5rem 0.5rem 0;
            padding: 0.65rem 0.75rem;
            font-size: 0.74rem;
            color: var(--text-secondary);
            line-height: 1.4;
            margin-top: auto;
        }}
        .criterio-box strong {{
            color: var(--text-primary);
        }}

        /* Gestalt Nav Strip & Badges */
        .gestalt-nav-strip {{
            background: rgba(15, 23, 42, 0.75);
            border: 1px solid var(--border-card);
            border-radius: 0.5rem;
            padding: 0.65rem 1rem;
            margin-bottom: 1.25rem;
            display: flex;
            flex-wrap: wrap;
            justify-content: space-between;
            align-items: center;
            gap: 0.75rem;
        }}
        .gestalt-nav-title {{
            display: flex;
            align-items: center;
            gap: 0.45rem;
            flex-wrap: wrap;
            font-size: 0.78rem;
            color: var(--text-primary);
        }}
        .gestalt-pill {{
            font-size: 0.66rem;
            font-weight: 700;
            padding: 0.15rem 0.45rem;
            border-radius: 9999px;
            background: rgba(56, 189, 248, 0.1);
            color: var(--accent-blue);
            border: 1px solid rgba(56, 189, 248, 0.25);
        }}
        .gestalt-flow-steps {{
            display: flex;
            align-items: center;
            gap: 0.35rem;
            flex-wrap: wrap;
            font-size: 0.72rem;
            font-weight: 600;
        }}
        .flow-step {{
            background: #1e293b;
            color: var(--text-secondary);
            padding: 0.2rem 0.5rem;
            border-radius: 0.25rem;
            border: 1px solid var(--border-card);
        }}
        .flow-step.active {{
            color: #f8fafc;
            border-color: rgba(56, 189, 248, 0.3);
            background: rgba(56, 189, 248, 0.12);
        }}
        .flow-arrow {{
            color: var(--accent-blue);
            font-weight: 800;
        }}
        .z-badge {{
            font-size: 0.68rem;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            padding: 0.2rem 0.55rem;
            border-radius: 0.25rem;
            background: rgba(56, 189, 248, 0.15);
            color: var(--accent-blue);
            border: 1px solid rgba(56, 189, 248, 0.35);
        }}
        .gestalt-tag {{
            font-size: 0.65rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.04em;
            color: var(--accent-amber);
            background: rgba(245, 158, 11, 0.12);
            border: 1px solid rgba(245, 158, 11, 0.3);
            padding: 0.18rem 0.45rem;
            border-radius: 0.25rem;
        }}

        /* Tablas y Estilos de Estadísticos */
        .stats-table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 0.82rem;
            text-align: left;
        }}
        .stats-table th {{
            background: #1e293b;
            color: var(--text-primary);
            font-weight: 700;
            text-transform: uppercase;
            font-size: 0.7rem;
            letter-spacing: 0.05em;
            padding: 0.75rem 0.85rem;
            border-bottom: 2px solid var(--border-highlight);
        }}
        .stats-table td {{
            padding: 0.75rem 0.85rem;
            border-bottom: 1px solid var(--border-card);
            color: var(--text-secondary);
        }}
        .stats-table tbody tr:hover {{
            background: rgba(30, 41, 59, 0.45);
        }}
        .cv-badge {{
            display: inline-block;
            padding: 0.15rem 0.45rem;
            border-radius: 9999px;
            font-size: 0.72rem;
            font-family: 'JetBrains Mono', monospace;
            font-weight: 700;
        }}
        .cv-low {{ background: rgba(16, 185, 129, 0.15); color: var(--accent-green); border: 1px solid rgba(16, 185, 129, 0.3); }}
        .cv-mid {{ background: rgba(56, 189, 248, 0.15); color: var(--accent-blue); border: 1px solid rgba(56, 189, 248, 0.3); }}
        .cv-high {{ background: rgba(245, 158, 11, 0.15); color: var(--accent-amber); border: 1px solid rgba(245, 158, 11, 0.3); }}
        .cv-extreme {{ background: rgba(244, 63, 94, 0.15); color: var(--accent-rose); border: 1px solid rgba(244, 63, 94, 0.3); }}
        
        .dim-badge {{
            font-size: 0.65rem;
            font-weight: 700;
            padding: 0.2rem 0.5rem;
            border-radius: 9999px;
            border: 1px solid;
            text-transform: uppercase;
        }}

        /* Tarjetas de Diccionario */
        .dict-controls {{
            display: flex;
            flex-wrap: wrap;
            gap: 0.4rem;
            margin: 1rem 0;
        }}
        .dict-filter-btn {{
            background: #1e293b;
            color: var(--text-secondary);
            border: 1px solid var(--border-highlight);
            border-radius: 9999px;
            padding: 0.35rem 0.85rem;
            font-size: 0.78rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s ease;
        }}
        .dict-filter-btn:hover, .dict-filter-btn.active {{
            background: var(--accent-blue);
            color: #0f172a;
            border-color: var(--accent-blue);
        }}
        .dict-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
            gap: 1rem;
        }}
        .dict-card {{
            background: var(--bg-card);
            border: 1px solid var(--border-card);
            border-radius: 0.65rem;
            padding: 1rem;
            display: flex;
            flex-direction: column;
        }}
        .dict-card-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 0.5rem;
        }}
        .type-tag {{ font-size: 0.7rem; color: var(--text-muted); font-family: 'JetBrains Mono'; }}
        .dict-name-es {{ font-size: 1rem; font-weight: 700; color: var(--text-primary); margin-bottom: 0.15rem; }}
        .dict-name-en code {{ background: rgba(15, 23, 42, 0.8); padding: 0.15rem 0.35rem; border-radius: 0.25rem; font-size: 0.75rem; color: var(--accent-blue); }}
        .dict-desc {{ font-size: 0.8rem; color: var(--text-secondary); margin: 0.5rem 0; flex-grow: 1; }}
        .dict-meta-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 0.4rem;
            background: rgba(15, 23, 42, 0.5);
            padding: 0.5rem;
            border-radius: 0.35rem;
            font-size: 0.72rem;
            margin-bottom: 0.5rem;
        }}
        .meta-label {{ color: var(--text-muted); font-size: 0.62rem; text-transform: uppercase; }}
        .meta-val {{ color: var(--text-primary); font-weight: 600; font-family: 'JetBrains Mono'; }}
        .dict-method {{ font-size: 0.75rem; color: var(--text-muted); border-top: 1px dashed var(--border-card); padding-top: 0.4rem; font-style: italic; }}

        .spotlight-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 1rem;
            margin: 1rem 0;
        }}
        .spotlight-card {{
            background: var(--bg-card);
            border: 1px solid var(--border-card);
            border-radius: 0.65rem;
            padding: 1.1rem;
        }}
        .spotlight-card.insight {{ border-top: 3px solid var(--accent-amber); }}
        .spotlight-card.resilient {{ border-top: 3px solid var(--accent-green); }}
        .spotlight-card.vulnerable {{ border-top: 3px solid var(--accent-rose); }}
        .spotlight-tag {{ font-size: 0.68rem; font-weight: 700; text-transform: uppercase; margin-bottom: 0.35rem; }}
        .insight .spotlight-tag {{ color: var(--accent-amber); }}
        .resilient .spotlight-tag {{ color: var(--accent-green); }}
        .vulnerable .spotlight-tag {{ color: var(--accent-rose); }}
        .spotlight-title {{ font-size: 0.95rem; font-weight: 700; color: var(--text-primary); margin-bottom: 0.35rem; }}
        .spotlight-desc {{ font-size: 0.8rem; color: var(--text-secondary); line-height: 1.45; }}

        footer {{
            padding: 2rem 0;
            color: var(--text-muted);
            font-size: 0.8rem;
            text-align: center;
            border-top: 1px solid var(--border-card);
        }}
    </style>
</head>
<body>

    <!-- Barra de Control Cockpit BI -->
    <header class="bi-topbar">
        <div class="container bi-nav-wrap">
            <div class="bi-brand">
                <span class="bi-brand-meta">PNUD · OCDE | Observatorio de Políticas Públicas</span>
                <span class="bi-brand-title">Tablero de Control: Radiografía Global del Bienestar (WHR 2024)</span>
            </div>
            <nav class="bi-tabs">
                <button class="bi-tab-btn active" onclick="cambiarPestana('tab-ejecutivo')">📊 Tablero Ejecutivo (Lectura en Z)</button>
                <button class="bi-tab-btn" onclick="cambiarPestana('tab-estadistica')">📋 Estadística & Diccionario</button>
                <button class="bi-tab-btn" onclick="cambiarPestana('tab-estrategia')">💡 Implicaciones Estratégicas</button>
            </nav>
        </div>
    </header>

    <!-- Franja de Contexto Metodológico y Pregunta Central -->
    <div class="context-strip">
        <div class="container context-flex">
            <div class="analytical-q">
                <span class="q-badge">Pregunta Analítica</span>
                <span>«¿Qué variables se asocian con la calidad de vida y evaluación del bienestar de los países, qué diferencias se evidencian entre naciones y de qué manera las condiciones económicas, de salud y socioinstitucionales diferencian a los países con alta y baja evaluación vital en el World Happiness Report 2024?»</span>
            </div>
            <div class="meta-chips">
                <div><strong>Muestra:</strong> 143 Países</div>
                <div><strong>Extremos:</strong> n = 72 (36 vs 36)</div>
                <div><strong>Diseño:</strong> Transversal Observacional</div>
            </div>
        </div>
    </div>

    <main class="container bi-board">

        <!-- ===================================================================
             PESTAÑA 1: TABLERO EJECUTIVO BI (PATRÓN DE LECTURA EN Z)
             =================================================================== -->
        <div id="tab-ejecutivo" class="tab-content" style="display: block;">

            <!-- Franja Guía Gestalt & Flujo de Escaneo en Z -->
            <div class="gestalt-nav-strip">
                <div class="gestalt-nav-title">
                    <span>📐 <strong>Arquitectura BI Gestalt:</strong></span>
                    <span class="gestalt-pill">Región Común</span>
                    <span class="gestalt-pill">Proximidad</span>
                    <span class="gestalt-pill">Semejanza Cromática</span>
                    <span class="gestalt-pill">Simetría y Orden</span>
                    <span class="gestalt-pill">Lectura en Z</span>
                    <span class="gestalt-pill">Figura-Fondo</span>
                </div>
                <div class="gestalt-flow-steps">
                    <span class="flow-step active">1. KPIs & Metodología</span>
                    <span class="flow-arrow">➔</span>
                    <span class="flow-step active">2. Geografía Global</span>
                    <span class="flow-arrow" style="color: var(--accent-amber);">↘</span>
                    <span class="flow-step active">3. Dispersión Variables</span>
                    <span class="flow-arrow">➔</span>
                    <span class="flow-step active">4. Brecha +2,96 pts</span>
                    <span class="flow-arrow" style="color: var(--accent-amber);">↘</span>
                    <span class="flow-step active">5. Relación Multidimensional</span>
                    <span class="flow-arrow">➔</span>
                    <span class="flow-step active">6. Descomposición Aditiva</span>
                </div>
            </div>

            <!-- FILA 1 DE LA Z: INICIO (TOP-LEFT A TOP-RIGHT) -->
            <div class="bi-grid-2col">
                <!-- 1. TOP-LEFT: KPIs Estratégicos & Criterio 25% (Punto de Entrada Visual) -->
                <div class="bi-widget">
                    <div class="bi-widget-header">
                        <div class="bi-widget-title">📌 1. Indicadores Ejecutivos & Criterio del 25%</div>
                        <div style="display: flex; gap: 0.4rem; align-items: center;">
                            <span class="z-badge">Paso 1 · Z-Top Left</span>
                            <span class="gestalt-tag">Región Común</span>
                        </div>
                    </div>
                    <div class="bi-widget-body">
                        <div class="kpi-grid-2x2">
                            <div class="kpi-box">
                                <div class="kpi-box-label">Rango Global Cantril</div>
                                <div class="kpi-box-val" style="color: var(--accent-blue);">1,72 — 7,74</div>
                                <div class="kpi-box-sub">Afganistán (mín) a Finlandia (#1 mundial)</div>
                            </div>
                            <div class="kpi-box">
                                <div class="kpi-box-label">La Gran Brecha (Extremos)</div>
                                <div class="kpi-box-val" style="color: var(--accent-amber);">+2,96 pts</div>
                                <div class="kpi-box-sub">Distancia entre 25% Sup (6,88) y 25% Inf (3,91)</div>
                            </div>
                            <div class="kpi-box">
                                <div class="kpi-box-label">Brecha Socioinstitucional</div>
                                <div class="kpi-box-val" style="color: var(--accent-green);">+1,09 pts</div>
                                <div class="kpi-box-sub">Apoyo (+0,67) + Libertad (+0,25) + Transp (+0,17)</div>
                            </div>
                            <div class="kpi-box">
                                <div class="kpi-box-label">Brecha Económica (PIB)</div>
                                <div class="kpi-box-val" style="color: var(--accent-purple);">+0,90 pts</div>
                                <div class="kpi-box-sub">30% de la brecha; lo no económico explica 70%</div>
                            </div>
                        </div>

                        <div class="criterio-box">
                            <strong>💡 Justificación Metodológica de la Partición por 25%:</strong><br>
                            El archivo oficial contiene solo la variable continua de Cantril. Para contrastar a los países de <strong>alta</strong> y <strong>baja</strong> evaluación de vida de forma objetiva (sin sesgos subjetivos), se ordenaron las 143 naciones y se dividieron en <strong>cuartiles empíricos (partición por 25%)</strong>:
                            <div style="margin-top: 0.35rem; display: flex; gap: 0.6rem; flex-wrap: wrap;">
                                <span style="color: var(--accent-blue); font-weight: 700;">• 25% Sup: ≥ 6,42 pts (36 países)</span>
                                <span style="color: var(--text-muted); font-weight: 600;">• 50% Medio: 4,73–6,41 pts (71 países)</span>
                                <span style="color: var(--accent-rose); font-weight: 700;">• 25% Inf: ≤ 4,73 pts (36 países)</span>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- 2. TOP-RIGHT: Geografía Global del Bienestar (Contexto Macro Espacial) -->
                <div class="bi-widget">
                    <div class="bi-widget-header">
                        <div class="bi-widget-title">🌍 2. Geografía Global del Bienestar Subjetivo</div>
                        <div style="display: flex; gap: 0.4rem; align-items: center;">
                            <span class="z-badge">Paso 2 · Z-Top Right</span>
                            <span class="gestalt-tag">Figura-Fondo</span>
                        </div>
                    </div>
                    <div class="bi-widget-desc">
                        Distribución espacial de la calidad de vida en 143 naciones. Mediana mundial en <strong>5,79 puntos</strong> con asimetría pronunciada hacia naciones vulnerables.
                    </div>
                    <div class="bi-widget-body">
                        {html_map_div}
                    </div>
                </div>
            </div>

            <!-- FILA 2 DE LA Z: DIAGONAL (MIDDLE-LEFT A MIDDLE-RIGHT) -->
            <div class="bi-grid-2col">
                <!-- 3. MIDDLE-LEFT: Distribución & Dispersión de Variables -->
                <div class="bi-widget">
                    <div class="bi-widget-header">
                        <div class="bi-widget-title">📊 3. Variabilidad y Dispersión de Componentes</div>
                        <div style="display: flex; gap: 0.4rem; align-items: center;">
                            <span class="z-badge">Paso 3 · Z-Diag Left</span>
                            <span class="gestalt-tag">Semejanza</span>
                        </div>
                    </div>
                    <div class="bi-widget-desc">
                        Diagrama de cajas con rango intercuartílico (IQR), media ± desv. est. y puntos de cada país. Use el menú desplegable para alternar de escala.
                    </div>
                    <div class="bi-widget-body">
                        {html_dist_div}
                    </div>
                </div>

                <!-- 4. MIDDLE-RIGHT: Descomposición de la Gran Brecha -->
                <div class="bi-widget">
                    <div class="bi-widget-header">
                        <div class="bi-widget-title">⚖️ 4. Descomposición de la Brecha (+2,96 pts)</div>
                        <div style="display: flex; gap: 0.4rem; align-items: center;">
                            <span class="z-badge">Paso 4 · Z-Diag Right</span>
                            <span class="gestalt-tag">Proximidad</span>
                        </div>
                    </div>
                    <div class="bi-widget-desc">
                        Diferencia promedio en puntos entre ambos bloques. La condición socioinstitucional (+1,09 pts) supera al PIB (+0,90 pts) en la separación.
                    </div>
                    <div class="bi-widget-body">
                        {html_brecha_div}
                    </div>
                </div>
            </div>

            <!-- FILA 3 DE LA Z: FINAL (BOTTOM-LEFT A BOTTOM-RIGHT) -->
            <div class="bi-grid-2col">
                <!-- 5. BOTTOM-LEFT: Relación Multidimensional & Resiliencia -->
                <div class="bi-widget">
                    <div class="bi-widget-header">
                        <div class="bi-widget-title">🤝 5. Condición Socioinstitucional vs. Calidad de Vida</div>
                        <div style="display: flex; gap: 0.4rem; align-items: center;">
                            <span class="z-badge">Paso 5 · Z-Base Left</span>
                            <span class="gestalt-tag">Continuidad</span>
                        </div>
                    </div>
                    <div class="bi-widget-desc">
                        Asociación lineal entre el tejido social acumulado (apoyo + libertad + probidad) y la evaluación vital. Casos atípicos revelan resiliencias y fracturas.
                    </div>
                    <div class="bi-widget-body">
                        {html_scatter_div}
                    </div>
                </div>

                <!-- 6. BOTTOM-RIGHT: Anatomía Aditiva País por País -->
                <div class="bi-widget">
                    <div class="bi-widget-header">
                        <div class="bi-widget-title">🧬 6. Descomposición Aditiva País por País</div>
                        <div style="display: flex; gap: 0.4rem; align-items: center;">
                            <span class="z-badge">Paso 6 · Z-Base Right</span>
                            <span class="gestalt-tag">Simetría & Cierre</span>
                        </div>
                    </div>
                    <div class="bi-widget-desc">
                        Estructura aditiva de la escalera en cada nación. Use el selector para contrastar los 36 países de Alto Bienestar frente a los 36 de Bajo Bienestar.
                    </div>
                    <div class="bi-widget-body">
                        {html_comp_div}
                    </div>
                </div>
            </div>

        </div>

        <!-- ===================================================================
             PESTAÑA 2: ESTADÍSTICA DESCRIPTIVA & DICCIONARIO OFICIAL
             =================================================================== -->
        <div id="tab-estadistica" class="tab-content" style="display: none;">
            
            <div class="bi-widget" style="margin-bottom: 1.5rem;">
                <div class="bi-widget-header">
                    <div class="bi-widget-title">📋 Matriz de Estadísticos Descriptivos Robustos (WHR 2024)</div>
                    <span class="bi-widget-tag">N = 143/140 Naciones</span>
                </div>
                <div class="bi-widget-desc">
                    Medidas de tendencia central, dispersión absoluta (Desv. Est., IQR) y dispersión relativa (Coeficiente de Variación CV%) para las 8 variables del reporte.
                </div>
                <div style="overflow-x: auto; margin-top: 0.5rem;">
                    <table class="stats-table">
                        <thead>
                            <tr>
                                <th>Variable</th>
                                <th>Condición Analítica</th>
                                <th>Media ± Desv.</th>
                                <th>Mediana</th>
                                <th>Rango [Mín — Máx]</th>
                                <th>IQR [Q1 — Q3]</th>
                                <th>Dispersión (CV%)</th>
                                <th>Forma y Asimetría</th>
                            </tr>
                        </thead>
                        <tbody>
                            {filas_tabla_stats}
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- Spotlight Cards de Dispersión -->
            <div class="spotlight-grid">
                <div class="spotlight-card insight">
                    <div class="spotlight-tag">💥 Dispersión Extrema (CV = 81,9%)</div>
                    <div class="spotlight-title">Confianza Institucional / Probidad</div>
                    <div class="spotlight-desc">
                        Es la variable más heterogénea del planeta (Asimetría = +1,53). El 80% del mundo percibe altos niveles de corrupción institucional (Q3 = 0,19 pts); solo naciones líderes como Dinamarca o Singapur logran valores superiores a 0,40 pts.
                    </div>
                </div>
                <div class="spotlight-card insight">
                    <div class="spotlight-tag">🛡️ Cohesión con Cola Crítica (Asim = -0,99)</div>
                    <div class="spotlight-title">Apoyo Social y Libertad de Elección</div>
                    <div class="spotlight-desc">
                        Ambas condiciones exhiben sesgo negativo pronunciado: la mayoría de los países gozan de niveles aceptables (medianas de 1,24 y 0,64 pts). No obstante, existe una cola izquierda extrema donde el tejido se derrumba (Afganistán = 0,00 pts).
                    </div>
                </div>
                <div class="spotlight-card insight">
                    <div class="spotlight-tag">📈 Mayor Amplitud Absoluta (IQR = 0,66 pts)</div>
                    <div class="spotlight-title">PIB per cápita (Condición Económica)</div>
                    <div class="spotlight-desc">
                        Presenta la mayor distancia intercuartílica absoluta (1,08 a 1,74 pts), evidenciando la profunda fractura estructural en productividad material entre países desarrollados y economías de bajos ingresos.
                    </div>
                </div>
            </div>

            <!-- Diccionario de Variables con Filtros -->
            <div class="bi-widget" style="margin-top: 1.5rem;">
                <div class="bi-widget-header">
                    <div class="bi-widget-title">📖 Diccionario Oficial de Variables (Inglés ↔ Español)</div>
                    <span class="bi-widget-tag">Filtro Interactivo</span>
                </div>
                <div class="dict-controls">
                    <button class="dict-filter-btn active" onclick="filtrarVariables('Todas')">Todas las Variables (10)</button>
                    <button class="dict-filter-btn" onclick="filtrarVariables('Condición Económica')">Condición Económica</button>
                    <button class="dict-filter-btn" onclick="filtrarVariables('Condición Socioinstitucional')">Condición Socioinstitucional</button>
                    <button class="dict-filter-btn" onclick="filtrarVariables('Condición de Salud')">Condición de Salud</button>
                    <button class="dict-filter-btn" onclick="filtrarVariables('Variable Objetivo / Bienestar')">Evaluación de Vida</button>
                    <button class="dict-filter-btn" onclick="filtrarVariables('Línea Base y Residuo')">Línea Base</button>
                </div>
                <div class="dict-grid" id="dict-container">
                    {cards_html}
                </div>
            </div>

        </div>

        <!-- ===================================================================
             PESTAÑA 3: IMPLICACIONES ESTRATÉGICAS Y METODOLOGÍA
             =================================================================== -->
        <div id="tab-estrategia" class="tab-content" style="display: none;">
            
            <div class="bi-grid-2col">
                <div class="bi-widget">
                    <div class="bi-widget-header">
                        <div class="bi-widget-title" style="color: var(--accent-green);">📋 Respuestas Clave a la Pregunta Analítica</div>
                        <span class="bi-widget-tag" style="background: rgba(16, 185, 129, 0.15); color: var(--accent-green); border-color: rgba(16, 185, 129, 0.3);">Políticas Públicas</span>
                    </div>
                    <div class="bi-widget-body" style="font-size: 0.85rem; color: var(--text-secondary); line-height: 1.6;">
                        <ul style="padding-left: 1.25rem; display: flex; flex-direction: column; gap: 0.75rem;">
                            <li><strong>Diferenciación Multidimensional:</strong> Las naciones con alta evaluación de vida no solo son más ricas; disfrutan de redes de apoyo social donde más del 90% de la población cuenta con auxilio en crisis y perciben amplia autonomía para decidir el rumbo de su vida.</li>
                            <li><strong>El Peso de la Cohesión Social:</strong> En conjunto, las condiciones socioinstitucionales (+1,09 pts) explican el 36,8% de la brecha entre el 25% superior y el 25% inferior, superando el impacto del PIB per cápita individual (+0,90 pts, 30,4%).</li>
                            <li><strong>El Lastre de la Corrupción:</strong> La desconfianza institucional opera como un techo invisible que penaliza el bienestar, afectando de manera especialmente severa a naciones de ingreso medio.</li>
                        </ul>
                    </div>
                </div>

                <div class="bi-widget">
                    <div class="bi-widget-header">
                        <div class="bi-widget-title" style="color: var(--accent-amber);">⚖️ Cautela Inferencial y Limitaciones Técnicas</div>
                        <span class="bi-widget-tag" style="background: rgba(245, 158, 11, 0.15); color: var(--accent-amber); border-color: rgba(245, 158, 11, 0.3);">Rigor Econométrico</span>
                    </div>
                    <div class="bi-widget-body" style="font-size: 0.85rem; color: var(--text-secondary); line-height: 1.6;">
                        <ul style="padding-left: 1.25rem; display: flex; flex-direction: column; gap: 0.75rem;">
                            <li><strong>Asociación, no Causalidad:</strong> Los resultados corresponden a un estudio transversal observacional con promedios trienales (2021–2023). Las asociaciones identificadas no deben presentarse como causalidades directas.</li>
                            <li><strong>Identidad Aditiva del Modelo:</strong> Las variables descompuestas provienen de coeficientes de panel multiplicados por la distancia a Distopía; su valor absoluto responde a la especificación de regresión del reporte.</li>
                            <li><strong>Datos Agregados a Nivel País:</strong> El archivo oficial no desagrega por edad, género ni niveles subnacionales, por lo que describe exclusivamente disparidades macro entre naciones.</li>
                        </ul>
                    </div>
                </div>
            </div>

            <!-- Spotlight de Casos Paradigmáticos -->
            <div class="spotlight-grid" style="margin-top: 1.5rem;">
                <div class="spotlight-card resilient">
                    <div class="spotlight-tag">🌟 Resiliencia Social</div>
                    <div class="spotlight-title">Costa Rica & América Latina</div>
                    <div class="spotlight-desc">
                        Costa Rica (Cantril = 7,34) y países como El Salvador alcanzan niveles de bienestar propios de economías del G7 gracias a una estructura comunitaria excepcionalmente sólida y alta autonomía percibida, compensando un PIB moderado.
                    </div>
                </div>
                <div class="spotlight-card vulnerable">
                    <div class="spotlight-tag">⚠️ Déficit Institucional</div>
                    <div class="spotlight-title">Botsuana & África del Sur</div>
                    <div class="spotlight-desc">
                        Botsuana cuenta con uno de los PIB más altos de la región, pero su evaluación de vida (3,81) se ubica en el 25% inferior debido a severas carencias en redes de apoyo comunitario y desconfianza en el entorno.
                    </div>
                </div>
                <div class="spotlight-card vulnerable">
                    <div class="spotlight-tag">💥 Fractura y Conflicto</div>
                    <div class="spotlight-title">Líbano & Afganistán</div>
                    <div class="spotlight-desc">
                        Líbano (2,71) exhibe un residuo de Distopía negativo producto del colapso bancario y la crisis institucional. Afganistán (1,72) registra el mínimo histórico ante la pérdida generalizada de libertades y auxilio social.
                    </div>
                </div>
            </div>

        </div>

    </main>

    <!-- Footer -->
    <footer>
        <div class="container">
            <p>Proyecto 2: Visualización Reproducible en Python · Maestría / Especialización en Analítica</p>
            <p style="margin-top: 0.35rem; font-size: 0.75rem;">
                Desarrollado por: Arnold Santiago Torres Anzola · Juan David Cruz Romero
            </p>
            <p style="margin-top: 0.2rem; font-size: 0.7rem; color: #475569;">
                Fuente Oficial: World Happiness Report 2024 · Gallup World Poll · OMS · Banco Mundial
            </p>
        </div>
    </footer>

    <script>
        function cambiarPestana(idTab) {{
            document.querySelectorAll('.tab-content').forEach(el => el.style.display = 'none');
            document.querySelectorAll('.bi-tab-btn').forEach(btn => btn.classList.remove('active'));
            
            const target = document.getElementById(idTab);
            if (target) target.style.display = 'block';
            
            const activeBtn = Array.from(document.querySelectorAll('.bi-tab-btn'))
                .find(b => b.getAttribute('onclick').includes(idTab));
            if (activeBtn) activeBtn.classList.add('active');

            // Forzar redimensionamiento de Plotly para evitar cortes en pestañas ocultas
            setTimeout(() => {{
                window.dispatchEvent(new Event('resize'));
            }}, 50);
        }}

        function filtrarVariables(categoria) {{
            const cards = document.querySelectorAll('.dict-card');
            const btns = document.querySelectorAll('.dict-filter-btn');
            
            btns.forEach(b => {{
                if (b.innerText.includes(categoria) || (categoria === 'Todas' && b.innerText.includes('Todas'))) {{
                    b.classList.add('active');
                }} else {{
                    b.classList.remove('active');
                }}
            }});

            cards.forEach(card => {{
                const dim = card.getAttribute('data-dim');
                if (categoria === 'Todas' || dim.includes(categoria)) {{
                    card.style.display = 'flex';
                }} else {{
                    card.style.display = 'none';
                }}
            }});
        }}
    </script>

</body>
</html>
"""

    out_dir = os.path.join('exports')
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, 'EquipoX_Proyecto2_Dashboard.html')
    with open(out_file, 'w', encoding='utf-8') as f:
        f.write(dashboard_html)
        
    print(f"[OK] Dashboard BI estructurado en Z con principios de Gestalt generado en: {out_file} ({os.path.getsize(out_file)} bytes)")

if __name__ == '__main__':
    build_dashboard()
