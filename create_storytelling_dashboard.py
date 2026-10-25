import os
import json
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

def build_dashboard():
    """
    Genera el Tablero Oficial interactivo del World Happiness Report (WHR) y Gallup Analytics
    con filtros interactivos en tiempo real para mapa, gráficos y tabla de rankings.
    """
    # 1. Cargar y preparar datos con resolución de ruta robusta (raíz o notebooks/)
    posibles_rutas = [
        os.path.join('data', 'raw', 'WHR24_Data_Figure_2.1.xls'),
        os.path.join('..', 'data', 'raw', 'WHR24_Data_Figure_2.1.xls'),
        os.path.join('data', 'WHR24_Data_Figure_2.1.xls'),
        os.path.join('..', 'data', 'WHR24_Data_Figure_2.1.xls'),
        'WHR24_Data_Figure_2.1.xls'
    ]
    ruta_datos = next((r for r in posibles_rutas if os.path.exists(r)), None)
    if not ruta_datos:
        raise FileNotFoundError("Archivo fuente WHR24_Data_Figure_2.1.xls no encontrado en las rutas especificadas.")
    
    df_raw = pd.read_excel(ruta_datos)
    df = df_raw.copy()

    # Códigos ISO-3 y traducción exhaustiva de los 143 países del reporte oficial al español
    paises_info = {
        'Finland': ('Finlandia', 'FIN'), 'Denmark': ('Dinamarca', 'DNK'), 'Iceland': ('Islandia', 'ISL'),
        'Sweden': ('Suecia', 'SWE'), 'Israel': ('Israel', 'ISR'), 'Netherlands': ('Países Bajos', 'NLD'),
        'Norway': ('Noruega', 'NOR'), 'Luxembourg': ('Luxemburgo', 'LUX'), 'Switzerland': ('Suiza', 'CHE'),
        'Australia': ('Australia', 'AUS'), 'New Zealand': ('Nueva Zelanda', 'NZL'), 'Costa Rica': ('Costa Rica', 'CRI'),
        'Kuwait': ('Kuwait', 'KWT'), 'Austria': ('Austria', 'AUT'), 'Canada': ('Canadá', 'CAN'),
        'Belgium': ('Bélgica', 'BEL'), 'Ireland': ('Irlanda', 'IRL'), 'Czechia': ('República Checa', 'CZE'),
        'Lithuania': ('Lituania', 'LTU'), 'United Kingdom': ('Reino Unido', 'GBR'), 'Slovenia': ('Eslovenia', 'SVN'),
        'United Arab Emirates': ('Emiratos Árabes Unidos', 'ARE'), 'United States': ('Estados Unidos', 'USA'),
        'Germany': ('Alemania', 'DEU'), 'Mexico': ('México', 'MEX'), 'Uruguay': ('Uruguay', 'URY'),
        'France': ('Francia', 'FRA'), 'Saudi Arabia': ('Arabia Saudita', 'SAU'), 'Kosovo': ('Kosovo', 'XKX'),
        'Singapore': ('Singapur', 'SGP'), 'Taiwan Province of China': ('Taiwán', 'TWN'), 'Romania': ('Rumania', 'ROU'),
        'El Salvador': ('El Salvador', 'SLV'), 'Estonia': ('Estonia', 'EST'), 'Poland': ('Polonia', 'POL'),
        'Spain': ('España', 'ESP'), 'Serbia': ('Serbia', 'SRB'), 'Chile': ('Chile', 'CHL'),
        'Panama': ('Panamá', 'PAN'), 'Malta': ('Malta', 'MLT'), 'Italy': ('Italia', 'ITA'),
        'Guatemala': ('Guatemala', 'GTM'), 'Nicaragua': ('Nicaragua', 'NIC'), 'Brazil': ('Brasil', 'BRA'),
        'Slovakia': ('Eslovaquia', 'SVK'), 'Latvia': ('Letonia', 'LVA'), 'Uzbekistan': ('Uzbekistán', 'UZB'),
        'Argentina': ('Argentina', 'ARG'), 'Kazakhstan': ('Kazajistán', 'KAZ'), 'Cyprus': ('Chipre', 'CYP'),
        'Japan': ('Japón', 'JPN'), 'South Korea': ('Corea del Sur', 'KOR'), 'Philippines': ('Filipinas', 'PHL'),
        'Vietnam': ('Vietnam', 'VNM'), 'Portugal': ('Portugal', 'PRT'), 'Hungary': ('Hungría', 'HUN'),
        'Paraguay': ('Paraguay', 'PRY'), 'Thailand': ('Tailandia', 'THA'), 'Malaysia': ('Malasia', 'MYS'),
        'China': ('China', 'CHN'), 'Honduras': ('Honduras', 'HND'), 'Bahrain': ('Baréin', 'BHR'),
        'Croatia': ('Croacia', 'HRV'), 'Greece': ('Grecia', 'GRC'), 'Bosnia and Herzegovina': ('Bosnia y Herzegovina', 'BIH'),
        'Libya': ('Libia', 'LBY'), 'Jamaica': ('Jamaica', 'JAM'), 'Peru': ('Perú', 'PER'),
        'Dominican Republic': ('República Dominicana', 'DOM'), 'Mauritius': ('Mauricio', 'MUS'),
        'Moldova': ('Moldavia', 'MDA'), 'Russia': ('Rusia', 'RUS'), 'Bolivia': ('Bolivia', 'BOL'),
        'Ecuador': ('Ecuador', 'ECU'), 'Kyrgyzstan': ('Kirguistán', 'KGZ'), 'Montenegro': ('Montenegro', 'MNE'),
        'Mongolia': ('Mongolia', 'MNG'), 'Colombia': ('Colombia', 'COL'), 'Venezuela': ('Venezuela', 'VEN'),
        'Indonesia': ('Indonesia', 'IDN'), 'Bulgaria': ('Bulgaria', 'BGR'), 'Armenia': ('Armenia', 'ARM'),
        'South Africa': ('Sudáfrica', 'ZAF'), 'North Macedonia': ('Macedonia del Norte', 'MKD'),
        'Algeria': ('Argelia', 'DZA'), 'Hong Kong S.A.R. of China': ('Hong Kong', 'HKG'), 'Albania': ('Albania', 'ALB'),
        'Tajikistan': ('Tayikistán', 'TJK'), 'Congo (Brazzaville)': ('República del Congo', 'COG'),
        'Mozambique': ('Mozambique', 'MOZ'), 'Georgia': ('Georgia', 'GEO'), 'Iraq': ('Irak', 'IRQ'),
        'Nepal': ('Nepal', 'NPL'), 'Laos': ('Laos', 'LAO'), 'Gabon': ('Gabón', 'GAB'),
        'Ivory Coast': ('Costa de Marfil', 'CIV'), 'Guinea': ('Guinea', 'GIN'), 'Turkiye': ('Turquía', 'TUR'),
        'Senegal': ('Senegal', 'SEN'), 'Iran': ('Irán', 'IRN'), 'Azerbaijan': ('Azerbaiyán', 'AZE'),
        'Nigeria': ('Nigeria', 'NGA'), 'State of Palestine': ('Palestina', 'PSE'), 'Cameroon': ('Camerún', 'CMR'),
        'Ukraine': ('Ucrania', 'UKR'), 'Namibia': ('Namibia', 'NAM'), 'Morocco': ('Marruecos', 'MAR'),
        'Pakistan': ('Pakistán', 'PAK'), 'Niger': ('Níger', 'NER'), 'Burkina Faso': ('Burkina Faso', 'BFA'),
        'Mauritania': ('Mauritania', 'MRT'), 'Gambia': ('Gambia', 'GMB'), 'Chad': ('Chad', 'TCD'),
        'Kenya': ('Kenia', 'KEN'), 'Tunisia': ('Túnez', 'TUN'), 'Benin': ('Benín', 'BEN'),
        'Uganda': ('Uganda', 'UGA'), 'Myanmar': ('Birmania (Myanmar)', 'MMR'), 'Cambodia': ('Camboya', 'KHM'),
        'Ghana': ('Ghana', 'GHA'), 'Liberia': ('Liberia', 'LBR'), 'Mali': ('Malí', 'MLI'),
        'Madagascar': ('Madagascar', 'MDG'), 'Togo': ('Togo', 'TGO'), 'Jordan': ('Jordania', 'JOR'),
        'India': ('India', 'IND'), 'Egypt': ('Egipto', 'EGY'), 'Sri Lanka': ('Sri Lanka', 'LKA'),
        'Bangladesh': ('Bangladés', 'BGD'), 'Ethiopia': ('Etiopía', 'ETH'), 'Tanzania': ('Tanzania', 'TZA'),
        'Comoros': ('Comoras', 'COM'), 'Yemen': ('Yemen', 'YEM'), 'Zambia': ('Zambia', 'ZMB'),
        'Eswatini': ('Esuatini', 'SWZ'), 'Malawi': ('Malaui', 'MWI'), 'Botswana': ('Botsuana', 'BWA'),
        'Zimbabwe': ('Zimbabue', 'ZWE'), 'Congo (Kinshasa)': ('R. D. del Congo', 'COD'),
        'Sierra Leone': ('Sierra Leona', 'SLE'), 'Lesotho': ('Lesoto', 'LSO'), 'Lebanon': ('Líbano', 'LBN'),
        'Afghanistan': ('Afganistán', 'AFG')
    }
    
    df['Pais_ES'] = df['Country name'].map(lambda c: paises_info.get(c, (c, 'N/A'))[0])
    df['ISO3'] = df['Country name'].map(lambda c: paises_info.get(c, (c, 'N/A'))[1])
    
    # Ranking global oficial por Ladder score
    df = df.sort_values('Ladder score', ascending=False).reset_index(drop=True)
    df['Rank'] = df.index + 1
    
    # Cortes cuartílicos del 25% (partición empírica)
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
    
    cols_contrib = [c for c in df.columns if c.startswith('Explained by:')]
    df_dims = df.dropna(subset=cols_contrib).copy()
    
    # Condición Socioinstitucional (suma aditiva de soporte, libertad y probidad)
    df_dims['Suma_Socioinstitucional'] = (
        df_dims['Explained by: Social support'] +
        df_dims['Explained by: Freedom to make life choices'] +
        df_dims['Explained by: Perceptions of corruption']
    )
    df['Suma_Socioinstitucional'] = df['Country name'].map(df_dims.set_index('Country name')['Suma_Socioinstitucional']).fillna(0)
    
    # Subconjunto de contraste de extremos (25% Superior vs. 25% Inferior: 36 + 36 = 72 países)
    df_extremos = df_dims[df_dims['Grupo_Bienestar'].isin([G_BAJO, G_ALTO])].copy()
    
    # Nombres técnicos formales en español
    nombres_variables_es = {
        'Explained by: Log GDP per capita': 'PIB per cápita (Económica)',
        'Explained by: Social support': 'Apoyo social (Socioinstitucional)',
        'Explained by: Healthy life expectancy': 'Esperanza de vida saludable (Salud)',
        'Explained by: Freedom to make life choices': 'Libertad de elección vital (Socioinstitucional)',
        'Explained by: Perceptions of corruption': 'Probidad pública (Baja corrupción)',
        'Explained by: Generosity': 'Generosidad y altruismo (Solidaridad)',
        'Dystopia + residual': 'Distopía + residuo (Base no explicada)'
    }

    # =========================================================================
    # PALETA OFICIAL WHR & GALLUP ANALYTICS
    # =========================================================================
    COLOR_WHR_MAGENTA = '#E0288A'
    COLOR_GALLUP_GREEN = '#008559'
    COLOR_TERRACOTTA = '#b91c1c'
    COLOR_STEEL_BLUE = '#0284c7'
    COLOR_AMBER = '#d97706'
    COLOR_SLATE_NEUTRAL = '#64748b'
    COLOR_TEXT_PRIMARY = '#0f172a'
    COLOR_TEXT_MUTED = '#64748b'

    # =========================================================================
    # 1. VISTA MAPA: MAPA COROPLÉTICO INTERACTIVO (DIV CON ID PREDECIBLE)
    # =========================================================================
    escala_whr_map = [
        [0.0, '#7f1d1d'],   # ~1.7 (Vulnerabilidad crítica)
        [0.25, '#c2410c'],  # ~3.2
        [0.45, '#d97706'],  # ~4.6
        [0.65, '#059669'],  # ~5.8
        [0.85, '#008559'],  # ~7.0
        [1.0, '#004830']    # ~7.8 (Máximo)
    ]

    fig_map = px.choropleth(
        df,
        locations='Country name',
        locationmode='country names',
        color='Ladder score',
        color_continuous_scale=escala_whr_map,
        range_color=[1.7, 7.8]
    )
    
    fig_map.data[0].customdata = np.stack((
        df['Pais_ES'],
        df['Rank'],
        df['Ladder score'],
        df['lowerwhisker'],
        df['upperwhisker'],
        df['Grupo_Bienestar'],
        df['Explained by: Log GDP per capita'].fillna(0),
        df['Explained by: Social support'].fillna(0),
        df['ISO3']
    ), axis=-1)
    
    fig_map.data[0].hovertemplate = (
        "<b>[%{customdata[8]}] %{customdata[0]}</b> (Rank #%{customdata[1]})<br><br>"
        "<b>Evaluación de vida (Cantril):</b> %{customdata[2]:.2f} / 10<br>"
        "<b>Intervalo de confianza 95%:</b> [%{customdata[3]:.2f} — %{customdata[4]:.2f}]<br>"
        "<b>Segmento:</b> %{customdata[5]}<br>"
        "• Aporte PIB per cápita: %{customdata[6]:.2f} pts<br>"
        "• Aporte Apoyo social: %{customdata[7]:.2f} pts<br>"
        "<extra></extra>"
    )
    
    fig_map.update_layout(
        template='plotly_white',
        paper_bgcolor='#ffffff',
        plot_bgcolor='#ffffff',
        font=dict(color=COLOR_TEXT_PRIMARY, family='Inter, sans-serif'),
        margin=dict(l=0, r=0, t=10, b=0),
        height=580,
        geo=dict(
            showframe=False,
            showcoastlines=True,
            coastlinecolor='#cbd5e1',
            projection_type='natural earth',
            bgcolor='#ffffff'
        ),
        coloraxis_colorbar=dict(
            title=dict(text='Escalera Cantril (pts)', font=dict(size=11, color=COLOR_TEXT_PRIMARY)),
            thickness=12,
            len=0.75,
            tickfont=dict(color=COLOR_TEXT_MUTED, size=9)
        )
    )

    # =========================================================================
    # 2. VISTA CHARTS: GRÁFICOS ANALÍTICOS
    # =========================================================================
    # A. Descomposición de la Brecha
    prom_alto = df_extremos[df_extremos['Grupo_Bienestar'] == G_ALTO][cols_contrib + ['Dystopia + residual']].mean()
    prom_bajo = df_extremos[df_extremos['Grupo_Bienestar'] == G_BAJO][cols_contrib + ['Dystopia + residual']].mean()
    brecha = (prom_alto - prom_bajo).sort_values(ascending=True)
    
    etiquetas_brecha = [nombres_variables_es.get(k, k) for k in brecha.index]
    colores_brecha = [
        COLOR_STEEL_BLUE if 'Económica' in e else
        COLOR_GALLUP_GREEN if 'Salud' in e else
        COLOR_AMBER if 'Socioinstitucional' in e or 'corrupción' in e else COLOR_SLATE_NEUTRAL
        for e in etiquetas_brecha
    ]
    
    fig_brecha = go.Figure(go.Bar(
        x=brecha.values,
        y=etiquetas_brecha,
        orientation='h',
        marker=dict(color=colores_brecha, line=dict(width=1, color='#e2e8f0')),
        text=[f"+{v:.2f} pts" for v in brecha.values],
        textposition='outside',
        cliponaxis=False,
        hovertemplate='<b>%{y}</b><br>Brecha promedio: <b>+%{x:.2f} puntos</b><extra></extra>'
    ))
    fig_brecha.update_layout(
        template='plotly_white',
        paper_bgcolor='#ffffff',
        plot_bgcolor='#ffffff',
        font=dict(color=COLOR_TEXT_PRIMARY, family='Inter, sans-serif'),
        xaxis=dict(title='Diferencia Promedio en Puntos (25% Superior − 25% Inferior)', range=[0, 1.18], gridcolor='#f1f5f9'),
        yaxis=dict(gridcolor='#f1f5f9', tickfont=dict(size=10)),
        margin=dict(l=10, r=40, t=15, b=40),
        height=400
    )

    # B. Ajuste MCO Condición Socioinstitucional vs Escalera Cantril
    colores_grupos = {
        G_ALTO: COLOR_GALLUP_GREEN,
        G_MEDIO: COLOR_SLATE_NEUTRAL,
        G_BAJO: COLOR_TERRACOTTA
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
        name=f'Ajuste MCO (r = {r_corr:.2f})',
        line=dict(color='#0f172a', dash='dash', width=1.8),
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
                size=8,
                color=color,
                line=dict(width=1, color='#ffffff'),
                opacity=0.88
            ),
            customdata=sub[['Pais_ES', 'Explained by: Log GDP per capita', 'Explained by: Social support', 'Explained by: Freedom to make life choices', 'Explained by: Perceptions of corruption', 'Grupo_Bienestar', 'ISO3']],
            hovertemplate=(
                '<b>[%{customdata[6]}] %{customdata[0]}</b><br>' +
                'Evaluación vital: <b>%{y:.2f} pts</b><br>' +
                'Suma Socioinstitucional: <b>%{x:.2f} pts</b><br>' +
                '  • Apoyo social: %{customdata[2]:.2f} pts<br>' +
                '  • Libertad vital: %{customdata[3]:.2f} pts<br>' +
                '  • Probidad: %{customdata[4]:.2f} pts<br>' +
                'Aporte PIB per cápita: %{customdata[1]:.2f} pts' +
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
                arrowwidth=1.2,
                arrowcolor='#0f172a',
                font=dict(color='#0f172a', size=9.5, family='Inter', weight=600),
                bgcolor='#ffffff',
                bordercolor='#cbd5e1',
                borderwidth=1,
                borderpad=3,
                ay=-24 if actual_y > 4.5 else 24
            )
            
    fig_scatter.update_layout(
        template='plotly_white',
        paper_bgcolor='#ffffff',
        plot_bgcolor='#ffffff',
        font=dict(color=COLOR_TEXT_PRIMARY, family='Inter, sans-serif'),
        xaxis=dict(title='Condición Socioinstitucional (Apoyo + Libertad + Probidad, pts)', gridcolor='#f1f5f9'),
        yaxis=dict(title='Evaluación de Vida (Escalera de Cantril, 0 a 10)', gridcolor='#f1f5f9'),
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='left',
            x=0.0,
            font=dict(size=9.5)
        ),
        margin=dict(l=40, r=20, t=55, b=45),
        height=480
    )

    # C. Boxplots de Componentes
    componentes_dist = [
        ('Explained by: Log GDP per capita', 'PIB per cápita (Económica)', COLOR_STEEL_BLUE),
        ('Explained by: Social support', 'Apoyo social (Socioinstitucional)', COLOR_AMBER),
        ('Explained by: Healthy life expectancy', 'Esperanza de vida (Salud)', COLOR_GALLUP_GREEN),
        ('Explained by: Freedom to make life choices', 'Libertad vital (Socioinstitucional)', '#b45309'),
        ('Explained by: Perceptions of corruption', 'Probidad pública (Baja corrupción)', '#ca8a04'),
        ('Explained by: Generosity', 'Generosidad (Solidaridad)', COLOR_SLATE_NEUTRAL),
        ('Dystopia + residual', 'Distopía + residuo (Base)', '#475569')
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
            marker=dict(color=color, size=4.5, opacity=0.75),
            line=dict(color=color, width=1.5),
            boxmean='sd',
            customdata=c_data,
            hovertemplate='<b>%{customdata[0]}</b><br>' + nombre + ': <b>%{x:.3f} pts</b><br>Evaluación: %{customdata[1]:.2f} pts<extra></extra>',
            visible=True
        ))

    sub_ladder = df.dropna(subset=['Ladder score']).copy()
    c_data_l = np.stack((sub_ladder['Pais_ES'], sub_ladder['Ladder score'], sub_ladder['Grupo_Bienestar']), axis=-1)
    fig_dist.add_trace(go.Box(
        x=sub_ladder['Ladder score'],
        name='Evaluación de Vida (0 a 10 pts)',
        boxpoints='all',
        jitter=0.35,
        pointpos=-1.6,
        marker=dict(color=COLOR_GALLUP_GREEN, size=5, opacity=0.8),
        line=dict(color=COLOR_GALLUP_GREEN, width=1.8),
        boxmean='sd',
        customdata=c_data_l,
        hovertemplate='<b>%{customdata[0]}</b><br>Evaluación: <b>%{x:.2f} pts</b><br>Segmento: %{customdata[2]}<extra></extra>',
        visible=False
    ))

    botones_dist = [
        dict(label='Componentes del Modelo (0 a 3 pts)', method='update', args=[{'visible': [True]*7 + [False]}, {'xaxis.title': 'Puntos en la Escalera de Cantril (Aporte)', 'xaxis.range': [-0.15, 3.15]}]),
        dict(label='Evaluación Global de Vida (0 a 10 pts)', method='update', args=[{'visible': [False]*7 + [True]}, {'xaxis.title': 'Puntaje de Evaluación de Vida (0 a 10 pts)', 'xaxis.range': [1.2, 8.2]}])
    ]

    fig_dist.update_layout(
        template='plotly_white',
        paper_bgcolor='#ffffff',
        plot_bgcolor='#ffffff',
        font=dict(color=COLOR_TEXT_PRIMARY, family='Inter, sans-serif'),
        height=400,
        margin=dict(l=10, r=20, t=55, b=40),
        xaxis=dict(title='Puntos en la Escalera de Cantril (Aporte)', gridcolor='#f1f5f9', range=[-0.15, 3.15]),
        yaxis=dict(gridcolor='#f1f5f9', tickfont=dict(size=9.5)),
        showlegend=False,
        updatemenus=[dict(type='dropdown', active=0, buttons=botones_dist, x=0.0, y=1.16, xanchor='left', bgcolor='#f8fafc', bordercolor='#cbd5e1', font=dict(color=COLOR_TEXT_PRIMARY, size=11, family='Inter'))]
    )

    # D. Descomposición Aditiva por País
    alto_sorted = df_extremos[df_extremos['Grupo_Bienestar'] == G_ALTO].sort_values('Ladder score')
    bajo_sorted = df_extremos[df_extremos['Grupo_Bienestar'] == G_BAJO].sort_values('Ladder score')
    
    mapa_componentes_es = {
        'Explained by: Log GDP per capita': ('PIB per cápita (Económica)', COLOR_STEEL_BLUE),
        'Explained by: Social support': ('Apoyo social (Socioinstitucional)', COLOR_AMBER),
        'Explained by: Healthy life expectancy': ('Esperanza de vida (Salud)', COLOR_GALLUP_GREEN),
        'Explained by: Freedom to make life choices': ('Libertad vital (Socioinstitucional)', '#b45309'),
        'Explained by: Perceptions of corruption': ('Probidad pública (Baja corrupción)', '#ca8a04'),
        'Explained by: Generosity': ('Generosidad (Solidaridad)', COLOR_SLATE_NEUTRAL),
        'Dystopia + residual': ('Distopía + residuo (Base no explicada)', '#475569')
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
        dict(label='25% Superior (Alto Bienestar · 36 países)', method='update', args=[{'x': [alto_sorted[c].tolist() for c in mapa_componentes_es.keys()], 'y': [alto_sorted['Pais_ES'].tolist()] * len(mapa_componentes_es)}, {'yaxis.categoryarray': alto_sorted['Pais_ES'].tolist()}]),
        dict(label='25% Inferior (Bajo Bienestar · 36 países)', method='update', args=[{'x': [bajo_sorted[c].tolist() for c in mapa_componentes_es.keys()], 'y': [bajo_sorted['Pais_ES'].tolist()] * len(mapa_componentes_es)}, {'yaxis.categoryarray': bajo_sorted['Pais_ES'].tolist()}])
    ]
    
    fig_comp.update_layout(
        template='plotly_white',
        paper_bgcolor='#ffffff',
        plot_bgcolor='#ffffff',
        font=dict(color=COLOR_TEXT_PRIMARY, family='Inter, sans-serif'),
        barmode='stack',
        height=480,
        xaxis=dict(title=dict(text='Puntos de la Escalera de Cantril (0 a 8 pts)', standoff=10), range=[0, 8.2], gridcolor='#f1f5f9'),
        yaxis=dict(categoryorder='array', categoryarray=alto_sorted['Pais_ES'].tolist(), tickfont=dict(size=8.5)),
        legend=dict(title=dict(text='<b>Componente:</b>', font=dict(color=COLOR_TEXT_PRIMARY, size=9)), orientation='h', yanchor='top', y=-0.16, xanchor='center', x=0.5, font=dict(size=8.5)),
        margin=dict(l=10, r=20, t=65, b=95),
        updatemenus=[dict(type='dropdown', active=0, buttons=botones_comp, x=0.0, y=1.16, xanchor='left', bgcolor='#f8fafc', bordercolor='#cbd5e1', font=dict(color=COLOR_TEXT_PRIMARY, size=11, family='Inter'))]
    )

    # =========================================================================
    # 3. CONVERSIÓN DE DATOS COMPLETOS A JSON PARA INTERACTIVIDAD TOTAL
    # =========================================================================
    paises_json_data = []
    for idx, row in df.iterrows():
        paises_json_data.append({
            'name_en': str(row['Country name']),
            'name_es': str(row['Pais_ES']),
            'iso3': str(row['ISO3']),
            'rank': int(row['Rank']),
            'score': round(float(row['Ladder score']), 3),
            'lower': round(float(row['lowerwhisker']), 2),
            'upper': round(float(row['upperwhisker']), 2),
            'grupo': str(row['Grupo_Bienestar']),
            'gdp': round(float(row['Explained by: Log GDP per capita']), 3) if not pd.isna(row['Explained by: Log GDP per capita']) else 0.0,
            'soc': round(float(row['Explained by: Social support']), 3) if not pd.isna(row['Explained by: Social support']) else 0.0,
            'health': round(float(row['Explained by: Healthy life expectancy']), 3) if not pd.isna(row['Explained by: Healthy life expectancy']) else 0.0,
            'free': round(float(row['Explained by: Freedom to make life choices']), 3) if not pd.isna(row['Explained by: Freedom to make life choices']) else 0.0,
            'gen': round(float(row['Explained by: Generosity']), 3) if not pd.isna(row['Explained by: Generosity']) else 0.0,
            'corr': round(float(row['Explained by: Perceptions of corruption']), 3) if not pd.isna(row['Explained by: Perceptions of corruption']) else 0.0,
            'dys': round(float(row['Dystopia + residual']), 3) if not pd.isna(row['Dystopia + residual']) else 0.0,
            'socio_total': round(float(row['Suma_Socioinstitucional']), 3) if not pd.isna(row['Suma_Socioinstitucional']) else 0.0
        })
    paises_json_str = json.dumps(paises_json_data, ensure_ascii=False)

    # Generación de filas HTML para la tabla
    filas_ranking_html = ""
    for idx, p in enumerate(paises_json_data):
        row_bg = "bg-white" if idx % 2 == 0 else "bg-grey"
        if G_ALTO in p['grupo']:
            badge_seg = '<span class="seg-chip seg-alto">25% Sup</span>'
        elif G_BAJO in p['grupo']:
            badge_seg = '<span class="seg-chip seg-bajo">25% Inf</span>'
        else:
            badge_seg = '<span class="seg-chip seg-medio">50% Central</span>'

        filas_ranking_html += f"""
        <tr class="table-row {row_bg}" id="row-{p['iso3']}" data-pais="{p['name_es'].lower()} {p['name_en'].lower()} {p['iso3'].lower()}" data-grupo="{p['grupo']}" onclick="abrirFichaPais('{p['iso3']}')">
            <td class="cell-rank"><strong>{p['rank']}</strong></td>
            <td class="cell-country">
                <span class="country-chip"><span class="iso-tag">{p['iso3']}</span><strong>{p['name_es']}</strong></span>
            </td>
            <td class="cell-val cell-main"><strong>{p['score']:.3f}</strong></td>
            <td class="cell-val cell-sub">[{p['lower']:.2f} — {p['upper']:.2f}]</td>
            <td class="cell-val">{p['gdp']:.3f}</td>
            <td class="cell-val">{p['soc']:.3f}</td>
            <td class="cell-val">{p['health']:.3f}</td>
            <td class="cell-val">{p['free']:.3f}</td>
            <td class="cell-val">{p['gen']:.3f}</td>
            <td class="cell-val">{p['corr']:.3f}</td>
            <td class="cell-val cell-dys">{p['dys']:.3f}</td>
            <td class="cell-center">{badge_seg}</td>
        </tr>
        """

    # HTML divs de Plotly con IDs fijos y reproducibles
    html_map_div = fig_map.to_html(full_html=False, include_plotlyjs=False, div_id="plotly-map-whr")
    html_dist_div = fig_dist.to_html(full_html=False, include_plotlyjs=False, div_id="plotly-dist-whr")
    html_brecha_div = fig_brecha.to_html(full_html=False, include_plotlyjs=False, div_id="plotly-brecha-whr")
    html_scatter_div = fig_scatter.to_html(full_html=False, include_plotlyjs=False, div_id="plotly-scatter-whr")
    html_comp_div = fig_comp.to_html(full_html=False, include_plotlyjs=False, div_id="plotly-comp-whr")

    dashboard_html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>WHR Dashboard · World Happiness Report 2024</title>
    <!-- Tipografía Institucional: Inter y IBM Plex Mono -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <!-- Plotly CDN -->
    <script src="https://cdn.plot.ly/plotly-2.30.0.min.js"></script>
    <style>
        :root {{
            --whr-magenta: #E0288A;
            --whr-magenta-hover: #c21873;
            --whr-black: #0f172a;
            --whr-banner: #111827;
            --gallup-green: #008559;
            --bg-page: #f8fafc;
            --bg-surface: #ffffff;
            --border-light: #e2e8f0;
            --border-medium: #cbd5e1;
            --text-dark: #0f172a;
            --text-secondary: #475569;
            --text-muted: #64748b;
            --color-gdp: #0284c7;
            --color-social: #d97706;
            --color-health: #008559;
            --color-free: #b45309;
            --color-corr: #ca8a04;
            --color-gen: #64748b;
        }}
        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}
        body {{
            background-color: var(--bg-page);
            color: var(--text-dark);
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.5;
            -webkit-font-smoothing: antialiased;
        }}
        .container-fluid {{
            width: 100%;
            max-width: 1520px;
            margin: 0 auto;
            padding: 0 1.25rem;
        }}

        /* -------------------------------------------------------------
           1. BANNER OFICIAL GALLUP & WHR (gallup_banner)
           ------------------------------------------------------------- */
        .gallup-banner {{
            background: var(--whr-banner);
            color: #ffffff;
            padding: 0.65rem 1.25rem;
            display: flex;
            flex-wrap: wrap;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid #1f2937;
        }}
        .banner-left {{
            display: flex;
            align-items: center;
            gap: 1.25rem;
            flex-wrap: wrap;
        }}
        .whr-brand-logo {{
            display: flex;
            align-items: center;
            text-decoration: none;
            color: #ffffff;
        }}
        .whr-logo-svg {{
            height: 38px;
            width: auto;
        }}
        .banner-text {{
            font-size: 0.95rem;
            color: #cbd5e1;
        }}
        .banner-text strong {{
            color: #ffffff;
        }}
        .banner-text a {{
            color: #ffffff;
            text-decoration: underline;
            text-underline-offset: 3px;
        }}
        .banner-actions {{
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }}
        .btn-raw-data {{
            background: transparent;
            color: #ffffff;
            border: 1px solid #4b5563;
            border-radius: 9999px;
            padding: 0.4rem 1rem;
            font-size: 0.82rem;
            font-weight: 600;
            cursor: pointer;
            text-decoration: none;
            transition: all 0.2s ease;
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
        }}
        .btn-raw-data:hover {{
            border-color: var(--whr-magenta);
            color: var(--whr-magenta);
            background: rgba(224, 40, 138, 0.08);
        }}
        .banner-close-btn {{
            background: transparent;
            border: none;
            color: var(--whr-magenta);
            cursor: pointer;
            padding: 0.35rem;
            display: flex;
            align-items: center;
        }}

        /* -------------------------------------------------------------
           2. NAVBAR CON SELECTOR DE PÁGINAS OFICIAL (Map / Chart / Rankings)
           ------------------------------------------------------------- */
        .whr-navbar {{
            background: var(--bg-surface);
            border-bottom: 1px solid var(--border-light);
            position: sticky;
            top: 0;
            z-index: 40;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
        }}
        .nav-inner {{
            display: flex;
            flex-wrap: wrap;
            justify-content: space-between;
            align-items: center;
            padding: 0.5rem 0;
            gap: 0.75rem;
        }}
        .nav-buttons-group {{
            display: flex;
            gap: 0.4rem;
        }}
        .nav-btn {{
            display: inline-flex;
            align-items: center;
            gap: 0.55rem;
            background: #ffffff;
            color: var(--text-secondary);
            border: 1px solid var(--border-light);
            border-radius: 6px;
            padding: 0.5rem 1.15rem;
            font-size: 0.88rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.15s ease;
            font-family: 'Inter', sans-serif;
            text-decoration: none;
        }}
        .nav-btn svg {{
            width: 19px;
            height: 19px;
            stroke-width: 1.8;
            stroke: currentColor;
        }}
        .nav-btn:hover {{
            background: #f8fafc;
            color: var(--text-dark);
            border-color: var(--border-medium);
        }}
        .nav-btn.active {{
            background: var(--whr-black);
            color: #ffffff;
            border-color: var(--whr-black);
            box-shadow: 0 2px 4px rgba(15, 23, 42, 0.2);
        }}
        .nav-btn.active svg {{
            stroke: var(--whr-magenta);
        }}

        /* Buscador con Autocompletado */
        .nav-search-container {{
            position: relative;
            min-width: 320px;
        }}
        .nav-search-box {{
            position: relative;
            width: 100%;
        }}
        .nav-search-input {{
            width: 100%;
            padding: 0.5rem 2.2rem 0.5rem 2.25rem;
            border: 1px solid var(--border-light);
            border-radius: 6px;
            font-size: 0.85rem;
            font-family: 'Inter', sans-serif;
            outline: none;
            background: #ffffff;
            transition: border-color 0.15s;
        }}
        .nav-search-input:focus {{
            border-color: var(--whr-magenta);
            box-shadow: 0 0 0 2px rgba(224, 40, 138, 0.12);
        }}
        .search-icon-svg {{
            position: absolute;
            left: 0.75rem;
            top: 50%;
            transform: translateY(-50%);
            width: 16px;
            height: 16px;
            stroke: var(--text-muted);
            pointer-events: none;
        }}
        .search-clear-btn {{
            position: absolute;
            right: 0.65rem;
            top: 50%;
            transform: translateY(-50%);
            background: transparent;
            border: none;
            color: var(--text-muted);
            cursor: pointer;
            font-size: 0.9rem;
            display: none;
        }}
        .search-dropdown-menu {{
            position: absolute;
            top: calc(100% + 4px);
            left: 0;
            right: 0;
            background: #ffffff;
            border: 1px solid var(--border-medium);
            border-radius: 6px;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
            max-height: 320px;
            overflow-y: auto;
            z-index: 100;
            display: none;
        }}
        .search-item {{
            padding: 0.55rem 0.85rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid #f1f5f9;
            cursor: pointer;
            font-size: 0.82rem;
            transition: background 0.1s;
        }}
        .search-item:hover {{
            background: #fdf2f8;
        }}
        .search-item strong {{
            color: var(--text-dark);
        }}
        .search-item-meta {{
            font-size: 0.74rem;
            color: var(--text-muted);
            font-family: 'IBM Plex Mono', monospace;
        }}

        /* -------------------------------------------------------------
           3. BARRA DE FILTROS INSTITUCIONALES (dropdownRow)
           ------------------------------------------------------------- */
        .filter-row {{
            background: #ffffff;
            border-bottom: 1px solid var(--border-light);
            padding: 0.65rem 0;
            font-size: 0.82rem;
        }}
        .filter-row-inner {{
            display: flex;
            flex-wrap: wrap;
            justify-content: space-between;
            align-items: center;
            gap: 1rem;
        }}
        .filter-items {{
            display: flex;
            flex-wrap: wrap;
            align-items: center;
            gap: 1.25rem;
        }}
        .filter-group {{
            display: flex;
            align-items: center;
            gap: 0.45rem;
        }}
        .filter-title {{
            font-size: 0.76rem;
            font-weight: 700;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.04em;
        }}
        .filter-badge {{
            background: #f1f5f9;
            border: 1px solid var(--border-light);
            border-radius: 4px;
            padding: 0.25rem 0.65rem;
            font-size: 0.82rem;
            font-weight: 600;
            color: var(--text-dark);
        }}
        .region-chips {{
            display: flex;
            gap: 0.35rem;
        }}
        .region-chip {{
            background: #f8fafc;
            border: 1px solid var(--border-light);
            border-radius: 9999px;
            padding: 0.25rem 0.75rem;
            font-size: 0.78rem;
            font-weight: 600;
            color: var(--text-secondary);
            cursor: pointer;
            transition: all 0.15s;
        }}
        .region-chip:hover, .region-chip.active {{
            background: var(--whr-magenta);
            color: #ffffff;
            border-color: var(--whr-magenta);
        }}
        .filter-status-badge {{
            font-size: 0.76rem;
            font-weight: 600;
            color: var(--whr-magenta);
            background: #fdf2f8;
            border: 1px solid rgba(224, 40, 138, 0.25);
            padding: 0.2rem 0.55rem;
            border-radius: 4px;
            display: inline-flex;
            align-items: center;
            gap: 0.35rem;
        }}

        /* -------------------------------------------------------------
           4. VISTAS Y CONTENEDORES
           ------------------------------------------------------------- */
        .content-area {{
            padding: 1.5rem 0 3.5rem;
        }}
        .tab-view {{
            display: none;
        }}
        .tab-view.active {{
            display: block;
        }}

        .chart-grid-2col {{
            display: grid;
            grid-template-columns: 1fr;
            gap: 1.25rem;
            margin-bottom: 1.25rem;
        }}
        @media (min-width: 1024px) {{
            .chart-grid-2col {{
                grid-template-columns: 1fr 1fr;
            }}
        }}
        .whr-card {{
            background: var(--bg-surface);
            border: 1px solid var(--border-light);
            border-radius: 8px;
            padding: 1.25rem;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
            display: flex;
            flex-direction: column;
        }}
        .whr-card-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 0.75rem;
            padding-bottom: 0.65rem;
            border-bottom: 1px solid var(--border-light);
        }}
        .whr-card-title {{
            font-size: 0.95rem;
            font-weight: 700;
            color: var(--text-dark);
        }}
        .whr-card-tag {{
            font-size: 0.68rem;
            font-weight: 700;
            text-transform: uppercase;
            padding: 0.2rem 0.55rem;
            border-radius: 4px;
            letter-spacing: 0.04em;
            background: #f1f5f9;
            color: var(--text-secondary);
            border: 1px solid var(--border-light);
        }}
        .whr-card-desc {{
            font-size: 0.8rem;
            color: var(--text-muted);
            margin-bottom: 0.5rem;
        }}

        /* -------------------------------------------------------------
           5. TABLA DATAGRID (RANKINGS)
           ------------------------------------------------------------- */
        .datagrid-container {{
            background: #ffffff;
            border: 1px solid var(--border-light);
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
        }}
        .datagrid-header-top {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1rem 1.25rem;
            border-bottom: 1px solid var(--border-light);
            background: #fafafa;
        }}
        .datagrid-title {{
            font-size: 1.05rem;
            font-weight: 700;
            color: var(--text-dark);
        }}
        .table-responsive {{
            max-height: 640px;
            overflow: auto;
        }}
        .whr-table {{
            width: 100%;
            border-collapse: separate;
            border-spacing: 0;
            font-size: 0.82rem;
            text-align: left;
        }}
        .whr-table th {{
            position: sticky;
            top: 0;
            z-index: 20;
            padding: 0.65rem 0.75rem;
            font-weight: 700;
            font-size: 0.72rem;
            text-transform: uppercase;
            letter-spacing: 0.04em;
            color: #ffffff;
            border-right: 1px solid rgba(255, 255, 255, 0.12);
            white-space: nowrap;
            cursor: pointer;
            user-select: none;
        }}
        .th-life {{ background: #0f172a; }}
        .th-country {{ background: #1e293b; }}
        .th-factors {{ background: #008559; }}
        .th-base {{ background: #475569; }}
        
        .whr-table td {{
            padding: 0.65rem 0.75rem;
            border-bottom: 1px solid var(--border-light);
            border-right: 1px solid #f1f5f9;
            color: var(--text-dark);
            white-space: nowrap;
        }}
        .whr-table tbody tr.bg-white {{ background: #ffffff; }}
        .whr-table tbody tr.bg-grey {{ background: #f8fafc; }}
        .whr-table tbody tr:hover {{ background: #fdf2f8 !important; cursor: pointer; }}
        
        .cell-rank {{ text-align: center; font-weight: 700; font-family: 'IBM Plex Mono', monospace; width: 60px; }}
        .cell-country {{ font-weight: 600; }}
        .country-chip {{ display: inline-flex; align-items: center; gap: 0.45rem; }}
        .iso-tag {{
            font-size: 0.68rem;
            font-weight: 700;
            font-family: 'IBM Plex Mono', monospace;
            background: #e2e8f0;
            color: #334155;
            padding: 0.1rem 0.35rem;
            border-radius: 3px;
        }}
        .cell-val {{ text-align: right; font-family: 'IBM Plex Mono', monospace; font-variant-numeric: tabular-nums; }}
        .cell-main {{ color: var(--whr-black); font-weight: 700; }}
        .cell-sub {{ color: var(--text-muted); font-size: 0.75rem; }}
        .cell-dys {{ color: var(--text-muted); }}
        .cell-center {{ text-align: center; }}
        
        .seg-chip {{
            display: inline-block;
            padding: 0.15rem 0.5rem;
            border-radius: 9999px;
            font-size: 0.68rem;
            font-weight: 700;
            text-transform: uppercase;
        }}
        .seg-alto {{ background: rgba(0, 133, 89, 0.12); color: var(--gallup-green); border: 1px solid rgba(0, 133, 89, 0.3); }}
        .seg-medio {{ background: rgba(100, 116, 139, 0.1); color: var(--text-secondary); border: 1px solid rgba(100, 116, 139, 0.25); }}
        .seg-bajo {{ background: rgba(224, 40, 138, 0.1); color: var(--whr-magenta); border: 1px solid rgba(224, 40, 138, 0.3); }}

        /* -------------------------------------------------------------
           6. FICHA DETALLADA DE PAÍS (SPOTLIGHT MODAL / CARD)
           ------------------------------------------------------------- */
        .country-modal-overlay {{
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(15, 23, 42, 0.5);
            backdrop-filter: blur(4px);
            z-index: 200;
            display: none;
            justify-content: center;
            align-items: center;
            padding: 1rem;
        }}
        .country-modal-card {{
            background: #ffffff;
            border-radius: 10px;
            width: 100%;
            max-width: 580px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
            border: 1px solid var(--border-medium);
            overflow: hidden;
            animation: modalFadeIn 0.15s ease-out;
        }}
        @keyframes modalFadeIn {{
            from {{ opacity: 0; transform: scale(0.96); }}
            to {{ opacity: 1; transform: scale(1); }}
        }}
        .modal-header {{
            background: var(--whr-black);
            color: #ffffff;
            padding: 1.15rem 1.35rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .modal-body {{
            padding: 1.35rem;
        }}
        .modal-kpi-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 0.75rem;
            margin-bottom: 1rem;
        }}
        .modal-kpi {{
            background: #f8fafc;
            border: 1px solid var(--border-light);
            border-radius: 6px;
            padding: 0.65rem 0.85rem;
        }}
        .modal-bars {{
            display: flex;
            flex-direction: column;
            gap: 0.45rem;
            margin-top: 0.75rem;
        }}
        .modal-bar-item {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 0.8rem;
            padding: 0.3rem 0;
            border-bottom: 1px solid #f1f5f9;
        }}
        .modal-bar-item span:first-child {{ color: var(--text-secondary); }}
        .modal-bar-item strong {{ font-family: 'IBM Plex Mono', monospace; }}

        /* -------------------------------------------------------------
           7. METODOLOGÍA & FOOTER
           ------------------------------------------------------------- */
        .metodologia-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
            gap: 1.25rem;
            margin-top: 1rem;
        }}
        .metod-card {{
            background: #ffffff;
            border: 1px solid var(--border-light);
            border-radius: 8px;
            padding: 1.25rem;
        }}
        .metod-badge {{
            display: inline-block;
            font-size: 0.68rem;
            font-weight: 700;
            text-transform: uppercase;
            padding: 0.15rem 0.45rem;
            border-radius: 3px;
            margin-bottom: 0.5rem;
        }}
        .metod-title {{ font-size: 1rem; font-weight: 700; margin-bottom: 0.25rem; }}
        .metod-code {{ font-family: 'IBM Plex Mono', monospace; font-size: 0.74rem; color: var(--whr-magenta); background: #fdf2f8; padding: 0.1rem 0.3rem; border-radius: 3px; }}
        .metod-desc {{ font-size: 0.82rem; color: var(--text-secondary); margin: 0.5rem 0; line-height: 1.5; }}
        .metod-meta {{ font-size: 0.74rem; color: var(--text-muted); border-top: 1px dashed var(--border-light); padding-top: 0.5rem; }}

        .whr-footer {{
            background: var(--whr-banner);
            color: #94a3b8;
            padding: 2rem 0;
            border-top: 1px solid #1f2937;
            font-size: 0.82rem;
        }}
        .footer-inner {{
            display: flex;
            flex-wrap: wrap;
            justify-content: space-between;
            align-items: center;
            gap: 1rem;
        }}
    </style>
</head>
<body>

    <!-- 1. BANNER GALLUP & WHR -->
    <header class="gallup-banner">
        <div class="banner-left">
            <a href="https://worldhappiness.report/" target="_blank" class="whr-brand-logo">
                <svg class="whr-logo-svg" viewBox="0 0 220 42" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <text x="2" y="16" fill="#ffffff" font-family="'Inter', sans-serif" font-weight="800" font-size="14" letter-spacing="0.12em">WORLD</text>
                    <text x="2" y="32" fill="#ffffff" font-family="'Inter', sans-serif" font-weight="800" font-size="14" letter-spacing="0.12em">HAPPINESS</text>
                    <text x="110" y="32" fill="#E0288A" font-family="'Inter', sans-serif" font-weight="900" font-size="15" letter-spacing="0.08em">REPORT</text>
                    <circle cx="204" cy="27" r="4" fill="#E0288A" />
                </svg>
            </a>
            <div class="banner-text">
                The <strong>World Happiness Report</strong> dashboard is powered by <strong>Gallup<sup>©</sup> Analytics</strong>
            </div>
        </div>
        <div class="banner-actions">
            <a href="https://worldhappiness.report/data-sharing" target="_blank" class="btn-raw-data">
                Access the raw data
            </a>
            <button class="banner-close-btn" aria-label="Cerrar" onclick="this.closest('.gallup-banner').style.display='none'">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" style="width: 20px; height: 20px;">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M6 18 18 6M6 6l12 12" />
                </svg>
            </button>
        </div>
    </header>

    <!-- 2. NAVBAR CON SELECTOR DE PÁGINAS (Map / Chart / Rankings / Metodología) -->
    <nav class="whr-navbar">
        <div class="container-fluid nav-inner">
            <div class="nav-buttons-group">
                <!-- Map Button -->
                <button class="nav-btn active" id="btn-nav-map" onclick="switchWHRPage('view-map', this)">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.8" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M15 10.5a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
                        <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 10.5c0 7.142-7.5 11.25-7.5 11.25S4.5 17.642 4.5 10.5a7.5 7.5 0 1 1 15 0Z" />
                    </svg>
                    Map
                </button>
                <!-- Chart Button -->
                <button class="nav-btn" id="btn-nav-chart" onclick="switchWHRPage('view-chart', this)">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.8" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M3 13.125C3 12.504 3.504 12 4.125 12h2.25c.621 0 1.125.504 1.125 1.125v6.75C7.5 20.496 6.996 21 6.375 21h-2.25A1.125 1.125 0 0 1 3 19.875v-6.75ZM9.75 8.625c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125v11.25c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 0 1-1.125-1.125V8.625ZM16.5 4.125c0-.621.504-1.125 1.125-1.125h2.25C20.496 3 21 3.504 21 4.125v15.75c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 0 1-1.125-1.125V4.125Z" />
                    </svg>
                    Chart
                </button>
                <!-- Rankings Button -->
                <button class="nav-btn" id="btn-nav-rankings" onclick="switchWHRPage('view-rankings', this)">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.8" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M3.375 19.5h17.25m-17.25 0a1.125 1.125 0 0 1-1.125-1.125M3.375 19.5h7.5c.621 0 1.125-.504 1.125-1.125m-9.75 0V5.625m0 12.75v-1.5c0-.621.504-1.125 1.125-1.125m18.375 2.625V5.625m0 12.75c0 .621-.504 1.125-1.125 1.125m1.125-1.125v-1.5c0-.621-.504-1.125-1.125-1.125m0 3.75h-7.5A1.125 1.125 0 0 1 12 18.375m9.75-12.75c0-.621-.504-1.125-1.125-1.125H3.375c-.621 0-1.125.504-1.125 1.125m19.5 0v1.5c0 .621-.504 1.125-1.125 1.125M2.25 5.625v1.5c0 .621.504 1.125 1.125 1.125m0 0h17.25m-17.25 0h7.5c.621 0 1.125.504 1.125 1.125M3.375 8.25c-.621 0-1.125.504-1.125 1.125v1.5c0 .621.504 1.125 1.125 1.125m17.25-3.75h-7.5c-.621 0-1.125.504-1.125 1.125m8.625-1.125c.621 0 1.125.504 1.125 1.125v1.5c0 .621-.504 1.125-1.125 1.125m-17.25 0h7.5" />
                    </svg>
                    Rankings
                </button>
                <!-- Metodología Button -->
                <button class="nav-btn" id="btn-nav-metodologia" onclick="switchWHRPage('view-metodologia', this)">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.8" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M12 6.042A8.967 8.967 0 0 0 6 3.75c-1.052 0-2.062.18-3 .512v14.25A8.987 8.987 0 0 1 6 18c2.305 0 4.408.867 6 2.292m0-14.25a8.966 8.966 0 0 1 6-2.292c1.052 0 2.062.18 3 .512v14.25A8.987 8.987 0 0 0 18 18a8.967 8.967 0 0 0-6 2.292m0-14.25v14.25" />
                    </svg>
                    Variables & Metodología
                </button>
            </div>
            
            <!-- Buscador Rápido con Autocompletado y Ficha de País -->
            <div class="nav-search-container">
                <div class="nav-search-box">
                    <svg class="search-icon-svg" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z" />
                    </svg>
                    <input type="text" id="global-search" class="nav-search-input" placeholder="Search for a country (e.g. Colombia, Finland)..." oninput="handleGlobalSearch(this.value)" onfocus="handleGlobalSearch(this.value)">
                    <button id="search-clear" class="search-clear-btn" onclick="limpiarBusqueda()">✕</button>
                </div>
                <!-- Menú Desplegable de Sugerencias -->
                <div id="search-suggestions" class="search-dropdown-menu"></div>
            </div>
        </div>
    </nav>

    <!-- 3. BARRA DE FILTROS INTERACTIVOS -->
    <div class="filter-row">
        <div class="container-fluid filter-row-inner">
            <div class="filter-items">
                <div class="filter-group">
                    <span class="filter-title">Filter by edition</span>
                    <span class="filter-badge">2024 Report (2021–2023)</span>
                </div>
                <div class="filter-group">
                    <span class="filter-title">Select segment</span>
                    <div class="region-chips">
                        <button class="region-chip active" id="chip-todos" onclick="filtrarSegmento('Todos', this)">World (143)</button>
                        <button class="region-chip" id="chip-sup" onclick="filtrarSegmento('25% Superior', this)">25% Superior (36)</button>
                        <button class="region-chip" id="chip-med" onclick="filtrarSegmento('50% Central', this)">50% Central (71)</button>
                        <button class="region-chip" id="chip-inf" onclick="filtrarSegmento('25% Inferior', this)">25% Inferior (36)</button>
                    </div>
                </div>
                <div id="filter-indicator" class="filter-status-badge" style="display: none;">
                    <span id="filter-indicator-text">Filtro activo</span>
                    <span style="cursor: pointer; font-weight: bold; margin-left: 4px;" onclick="restablecerFiltros()">✕</span>
                </div>
            </div>
            <div class="question-tag">
                <strong>Pregunta Analítica:</strong> «¿Qué variables diferencian a los países con alta y baja evaluación vital en el World Happiness Report 2024?»
            </div>
        </div>
    </div>

    <!-- 4. CONTENIDO PRINCIPAL -->
    <main class="container-fluid content-area">

        <!-- =============================================================
             PÁGINA 1: MAPA (WHR MAP VIEW)
             ============================================================= -->
        <div id="view-map" class="tab-view active">
            <div class="whr-card">
                <div class="whr-card-header">
                    <div>
                        <div class="whr-card-title">Distribución Espacial Global de la Escalera de Cantril (0 a 10 pts)</div>
                        <div class="whr-card-desc">
                            <span id="map-counter-text">Mostrando 143 naciones evaluadas en el mapa mundial.</span>
                            Haga clic en un país o use el buscador superior para ver sus indicadores detallados.
                        </div>
                    </div>
                    <span class="whr-card-tag">Gallup World Poll</span>
                </div>
                <div style="width: 100%;">
                    {html_map_div}
                </div>
            </div>
        </div>

        <!-- =============================================================
             PÁGINA 2: GRÁFICOS (WHR CHART VIEW)
             ============================================================= -->
        <div id="view-chart" class="tab-view">
            <div class="chart-grid-2col">
                <div class="whr-card">
                    <div class="whr-card-header">
                        <div>
                            <div class="whr-card-title">Descomposición de la Brecha Promedio (+2,96 pts)</div>
                            <div class="whr-card-desc">Distancia absoluta en puntos entre el 25% Superior y el 25% Inferior.</div>
                        </div>
                        <span class="whr-card-tag">Brecha Empírica</span>
                    </div>
                    {html_brecha_div}
                </div>

                <div class="whr-card">
                    <div class="whr-card-header">
                        <div>
                            <div class="whr-card-title">Variabilidad y Dispersión de Componentes</div>
                            <div class="whr-card-desc">Diagrama de cajas con rango intercuartílico (IQR), media ± desv. est. y observaciones.</div>
                        </div>
                        <span class="whr-card-tag">Distribución</span>
                    </div>
                    {html_dist_div}
                </div>
            </div>

            <div class="chart-grid-2col">
                <div class="whr-card">
                    <div class="whr-card-header">
                        <div>
                            <div class="whr-card-title">Condición Socioinstitucional vs. Escalera de Cantril</div>
                            <div class="whr-card-desc">Ajuste de Mínimos Cuadrados Ordinarios entre tejido social acumulado y bienestar.</div>
                        </div>
                        <span class="whr-card-tag">Regresión MCO</span>
                    </div>
                    {html_scatter_div}
                </div>

                <div class="whr-card">
                    <div class="whr-card-header">
                        <div>
                            <div class="whr-card-title">Anatomía Aditiva por País (Selector Cuartílico)</div>
                            <div class="whr-card-desc">Descomposición país por país del 25% Superior frente al 25% Inferior.</div>
                        </div>
                        <span class="whr-card-tag">Aditividad WHR</span>
                    </div>
                    {html_comp_div}
                </div>
            </div>
        </div>

        <!-- =============================================================
             PÁGINA 3: RANKINGS (WHR TABLE / DATAGRID VIEW)
             ============================================================= -->
        <div id="view-rankings" class="tab-view">
            <div class="datagrid-container">
                <div class="datagrid-header-top">
                    <div>
                        <div class="datagrid-title">Clasificación Global y Descomposición del Modelo (143 Naciones)</div>
                        <div style="font-size: 0.78rem; color: var(--text-muted); margin-top: 0.2rem;">
                            Estructura de datos idéntica a la tabla oficial del World Happiness Report. Haga clic en una fila para ver la ficha completa.
                        </div>
                    </div>
                    <div id="rankings-counter" style="font-size: 0.78rem; color: var(--text-muted); font-family: 'IBM Plex Mono', monospace; font-weight: 600;">
                        Mostrando 143 de 143 países
                    </div>
                </div>

                <div class="table-responsive">
                    <table class="whr-table" id="tabla-rankings">
                        <thead>
                            <tr>
                                <th class="th-life" onclick="ordenarTabla(0, true)">Rank ↕</th>
                                <th class="th-country" onclick="ordenarTabla(1, false)">Country ↕</th>
                                <th class="th-life" onclick="ordenarTabla(2, true)">Life evaluation ↕</th>
                                <th class="th-life">95% CI</th>
                                <th class="th-factors" onclick="ordenarTabla(4, true)">GDP per capita ↕</th>
                                <th class="th-factors" onclick="ordenarTabla(5, true)">Social support ↕</th>
                                <th class="th-factors" onclick="ordenarTabla(6, true)">Healthy life ↕</th>
                                <th class="th-factors" onclick="ordenarTabla(7, true)">Freedom ↕</th>
                                <th class="th-factors" onclick="ordenarTabla(8, true)">Generosity ↕</th>
                                <th class="th-factors" onclick="ordenarTabla(9, true)">Corruption ↕</th>
                                <th class="th-base" onclick="ordenarTabla(10, true)">Dystopia + residual ↕</th>
                                <th class="th-base">Segmento</th>
                            </tr>
                        </thead>
                        <tbody id="tbody-rankings">
                            {filas_ranking_html}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <!-- =============================================================
             PÁGINA 4: VARIABLES & METODOLOGÍA
             ============================================================= -->
        <div id="view-metodologia" class="tab-view">
            <div class="whr-card" style="margin-bottom: 1.25rem;">
                <div class="whr-card-header">
                    <div>
                        <div class="whr-card-title">Alcance de las Variables en el Reporte Oficial vs. Portal Web</div>
                        <div class="whr-card-desc">Aclaración técnica sobre las dimensiones del modelo de descomposición econométrica y los módulos de encuesta Gallup.</div>
                    </div>
                    <span class="whr-card-tag" style="background: rgba(224, 40, 138, 0.1); color: var(--whr-magenta); border-color: rgba(224, 40, 138, 0.3);">Econometría</span>
                </div>
                <div style="font-size: 0.85rem; color: var(--text-secondary); line-height: 1.6;">
                    <p style="margin-bottom: 0.75rem;">
                        El portal web interactivo del World Happiness Report (desarrollado con Gallup Analytics) incorpora variables adicionales de la encuesta mundial, tales como <strong>Emotions</strong> (emociones positivas y negativas del día previo) y <strong>Benevolence</strong> (donaciones monetarias, voluntariado y auxilio a extraños).
                    </p>
                    <p>
                        Por su parte, el modelo formal de descomposición de la <strong>Figura 2.1 oficial</strong> (utilizado en este proyecto y entregables de investigación) desagrega la Evaluación de Vida en seis contribuciones econométricas directas más la base hipotética de <strong>Distopía + residuo</strong>.
                    </p>
                </div>
            </div>

            <!-- Diccionario de Variables -->
            <div class="metodologia-grid">
                <div class="metod-card">
                    <span class="metod-badge" style="background: rgba(15, 23, 42, 0.1); color: #0f172a;">Variable Dependiente</span>
                    <div class="metod-title">Evaluación de Vida <span class="metod-code">Ladder score</span></div>
                    <div class="metod-desc">Medición central de bienestar subjetivo en escala continua de 0 a 10 obtenida de la Encuesta Mundial de Gallup mediante la Escalera de Cantril. Promedio trienal 2021–2023.</div>
                    <div class="metod-meta">Rango: 1,72 a 7,74 pts · Media mundial: 5,53 pts</div>
                </div>

                <div class="metod-card">
                    <span class="metod-badge" style="background: rgba(2, 132, 199, 0.1); color: var(--color-gdp);">Condición Económica</span>
                    <div class="metod-title">PIB per cápita <span class="metod-code">Explained by: Log GDP per capita</span></div>
                    <div class="metod-desc">Aporte del logaritmo del PIB por habitante a Paridad de Poder Adquisitivo (PPA, dólares constantes de 2017) según estadísticas del Banco Mundial.</div>
                    <div class="metod-meta">Rango: 0,00 a 2,14 pts · Explica el 30,4% de la brecha Q4-Q1</div>
                </div>

                <div class="metod-card">
                    <span class="metod-badge" style="background: rgba(217, 119, 6, 0.1); color: var(--color-social);">Condición Socioinstitucional</span>
                    <div class="metod-title">Apoyo Social <span class="metod-code">Explained by: Social support</span></div>
                    <div class="metod-desc">Aporte de la disponibilidad percibida de redes familiares y de amistades a las que recurrir en situaciones de emergencia («¿Cuenta con alguien para ayudarlo?»).</div>
                    <div class="metod-meta">Rango: 0,00 a 1,62 pts · Mayor brecha individual (+0,67 pts)</div>
                </div>

                <div class="metod-card">
                    <span class="metod-badge" style="background: rgba(0, 133, 89, 0.1); color: var(--color-health);">Condición de Salud</span>
                    <div class="metod-title">Esperanza de Vida Saludable <span class="metod-code">Explained by: Healthy life expectancy</span></div>
                    <div class="metod-desc">Años de vida esperados con pleno estado de salud física y mental sin discapacidades crónicas, extraído del Observatorio Global de la Salud (OMS).</div>
                    <div class="metod-meta">Rango: 0,00 a 0,86 pts · Aporte medio mundial: 0,52 pts</div>
                </div>

                <div class="metod-card">
                    <span class="metod-badge" style="background: rgba(180, 83, 9, 0.1); color: var(--color-free);">Condición Socioinstitucional</span>
                    <div class="metod-title">Libertad de Elección <span class="metod-code">Explained by: Freedom to make life choices</span></div>
                    <div class="metod-desc">Sensación de autonomía y control que perciben las personas sobre el rumbo y las decisiones de su propio proyecto vital.</div>
                    <div class="metod-meta">Rango: 0,00 a 0,86 pts · Brecha cuartílica: +0,25 pts</div>
                </div>

                <div class="metod-card">
                    <span class="metod-badge" style="background: rgba(202, 138, 4, 0.1); color: var(--color-corr);">Condición Socioinstitucional</span>
                    <div class="metod-title">Probidad Pública <span class="metod-code">Explained by: Perceptions of corruption</span></div>
                    <div class="metod-desc">Percepción de transparencia y ausencia de sobornos y corrupción tanto en las instituciones públicas del gobierno como en el sector empresarial privado.</div>
                    <div class="metod-meta">Rango: 0,00 a 0,57 pts · Dispersión extrema (CV = 81,9%)</div>
                </div>

                <div class="metod-card">
                    <span class="metod-badge" style="background: rgba(100, 116, 139, 0.1); color: var(--color-gen);">Dimensión Solidaria</span>
                    <div class="metod-title">Generosidad y Altruismo <span class="metod-code">Explained by: Generosity</span></div>
                    <div class="metod-desc">Tasa de donaciones monetarias a obras humanitarias y caritativas tras controlar por el nivel de riqueza económica (PIB per cápita).</div>
                    <div class="metod-meta">Rango: 0,00 a 0,40 pts · Media mundial: 0,15 pts</div>
                </div>

                <div class="metod-card">
                    <span class="metod-badge" style="background: rgba(71, 85, 105, 0.1); color: #475569;">Línea Base</span>
                    <div class="metod-title">Distopía + Residuo <span class="metod-code">Dystopia + residual</span></div>
                    <div class="metod-desc">Puntaje del país hipotético con los peores indicadores mundiales (Distopía = 1,714 pts) sumado al término de error no explicado por el modelo.</div>
                    <div class="metod-meta">Rango: -0,07 a 3,00 pts · Media mundial: 1,58 pts</div>
                </div>
            </div>
        </div>

    </main>

    <!-- MODAL / SPOTLIGHT FLOTANTE DE DETALLE DE PAÍS -->
    <div id="country-modal" class="country-modal-overlay" onclick="if(event.target === this) cerrarFichaPais();">
        <div class="country-modal-card">
            <div class="modal-header">
                <div>
                    <span id="modal-iso" class="iso-tag" style="background: #ffffff; color: #0f172a; margin-right: 6px;">FIN</span>
                    <strong id="modal-name" style="font-size: 1.15rem;">Finlandia</strong>
                    <span id="modal-rank" style="font-size: 0.85rem; color: var(--whr-magenta); margin-left: 8px; font-weight: 700;">Rank #1</span>
                </div>
                <button onclick="cerrarFichaPais()" style="background: transparent; border: none; color: #ffffff; cursor: pointer; font-size: 1.25rem;">✕</button>
            </div>
            <div class="modal-body">
                <div class="modal-kpi-grid">
                    <div class="modal-kpi">
                        <div style="font-size: 0.68rem; text-transform: uppercase; color: var(--text-muted); font-weight: 700;">Evaluación de Vida (Cantril)</div>
                        <div id="modal-score" style="font-size: 1.45rem; font-weight: 800; font-family: 'IBM Plex Mono', monospace; color: var(--whr-magenta);">7.741</div>
                        <div id="modal-ci" style="font-size: 0.72rem; color: var(--text-secondary);">IC 95%: [7.67 — 7.81]</div>
                    </div>
                    <div class="modal-kpi">
                        <div style="font-size: 0.68rem; text-transform: uppercase; color: var(--text-muted); font-weight: 700;">Segmento Cuartílico</div>
                        <div id="modal-segment" style="font-size: 0.95rem; font-weight: 700; margin-top: 4px; color: var(--gallup-green);">25% Superior</div>
                        <div id="modal-socio-sum" style="font-size: 0.72rem; color: var(--text-secondary); margin-top: 4px;">Socioinstitucional: 2.98 pts</div>
                    </div>
                </div>

                <div style="font-size: 0.75rem; font-weight: 700; text-transform: uppercase; color: var(--text-muted); margin-bottom: 0.35rem;">
                    Descomposición Aditiva de Factores (WHR Modelo Oficial)
                </div>
                <div class="modal-bars">
                    <div class="modal-bar-item"><span>PIB per cápita (Económica):</span><strong id="modal-gdp" style="color: var(--color-gdp);">1.844 pts</strong></div>
                    <div class="modal-bar-item"><span>Apoyo Social (Socioinstitucional):</span><strong id="modal-soc" style="color: var(--color-social);">1.572 pts</strong></div>
                    <div class="modal-bar-item"><span>Esperanza de Vida (Salud):</span><strong id="modal-health" style="color: var(--color-health);">0.695 pts</strong></div>
                    <div class="modal-bar-item"><span>Libertad de Elección Vital:</span><strong id="modal-free" style="color: var(--color-free);">0.859 pts</strong></div>
                    <div class="modal-bar-item"><span>Generosidad y Solidaridad:</span><strong id="modal-gen" style="color: var(--color-gen);">0.142 pts</strong></div>
                    <div class="modal-bar-item"><span>Probidad Pública (Baja corrupción):</span><strong id="modal-corr" style="color: var(--color-corr);">0.546 pts</strong></div>
                    <div class="modal-bar-item"><span>Distopía + Residuo (Base no explicada):</span><strong id="modal-dys" style="color: #475569;">2.082 pts</strong></div>
                </div>

                <div style="margin-top: 1.15rem; display: flex; gap: 0.6rem; justify-content: flex-end;">
                    <button class="nav-btn" style="padding: 0.4rem 0.85rem; font-size: 0.8rem;" onclick="verPaisEnRankings()">Ver en Tabla de Rankings</button>
                    <button class="nav-btn active" style="padding: 0.4rem 0.85rem; font-size: 0.8rem;" onclick="cerrarFichaPais()">Cerrar</button>
                </div>
            </div>
        </div>
    </div>

    <!-- 5. PIE DE PÁGINA INSTITUCIONAL -->
    <footer class="whr-footer">
        <div class="container-fluid footer-inner">
            <div>
                <strong>World Happiness Report 2024</strong> · Powered by Gallup<sup>©</sup> Analytics
                <div style="font-size: 0.74rem; color: #64748b; margin-top: 0.25rem;">
                    Desarrollado para el Proyecto 2 de Visualización de Datos en Python · Arnold Santiago Torres & Juan David Cruz
                </div>
            </div>
            <div style="font-size: 0.75rem; color: #64748b;">
                Fuentes: Gallup World Poll · OMS · Banco Mundial · UN Sustainable Development Solutions Network
            </div>
        </div>
    </footer>

    <!-- LÓGICA DE INTERACCIÓN INTEGRADA Y FILTROS EN TIEMPO REAL -->
    <script>
        // Dataset maestro de las 143 naciones serializado
        const DATOS_PAISES_WHR = {paises_json_str};

        let currentSegment = 'Todos';
        let searchQuery = '';
        let currentCountrySelected = null;

        // Selector de páginas (Map / Chart / Rankings / Metodología)
        function switchWHRPage(viewId, btnEl) {{
            document.querySelectorAll('.tab-view').forEach(v => v.classList.remove('active'));
            document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
            
            const targetView = document.getElementById(viewId);
            if (targetView) targetView.classList.add('active');
            if (btnEl) btnEl.classList.add('active');

            // Redimensionamiento de Plotly al cambiar de pestaña
            setTimeout(() => {{
                window.dispatchEvent(new Event('resize'));
            }}, 60);
        }}

        // Filtro por Segmento (Afecta simultáneamente al Mapa, Rankings y Gráficos)
        function filtrarSegmento(segmento, btn) {{
            currentSegment = segmento;
            document.querySelectorAll('.region-chip').forEach(c => c.classList.remove('active'));
            if (btn) btn.classList.add('active');

            // Actualizar indicador de filtro activo
            const indicator = document.getElementById('filter-indicator');
            const indText = document.getElementById('filter-indicator-text');
            if (segmento === 'Todos') {{
                indicator.style.display = 'none';
            }} else {{
                indicator.style.display = 'inline-flex';
                indText.innerText = 'Filtro: ' + segmento;
            }}

            aplicarFiltrosGlobales();
        }}

        // Restablecer filtros
        function restablecerFiltros() {{
            currentSegment = 'Todos';
            document.querySelectorAll('.region-chip').forEach(c => c.classList.remove('active'));
            document.getElementById('chip-todos').classList.add('active');
            document.getElementById('filter-indicator').style.display = 'none';
            aplicarFiltrosGlobales();
        }}

        // Búsqueda en tiempo real por país con menú de autocompletado
        function handleGlobalSearch(val) {{
            searchQuery = val.toLowerCase().trim();
            const clearBtn = document.getElementById('search-clear');
            const suggestions = document.getElementById('search-suggestions');
            
            clearBtn.style.display = searchQuery.length > 0 ? 'block' : 'none';

            // Mostrar sugerencias si hay texto
            if (searchQuery.length > 0) {{
                const matches = DATOS_PAISES_WHR.filter(p => 
                    p.name_es.toLowerCase().includes(searchQuery) ||
                    p.name_en.toLowerCase().includes(searchQuery) ||
                    p.iso3.toLowerCase().includes(searchQuery)
                ).slice(0, 8);

                if (matches.length > 0) {{
                    suggestions.innerHTML = matches.map(m => `
                        <div class="search-item" onclick="seleccionarPaisDesdeBusqueda('${{m.iso3}}')">
                            <span><span class="iso-tag">${{m.iso3}}</span> <strong>${{m.name_es}}</strong></span>
                            <span class="search-item-meta">Rank #${{m.rank}} · ${{m.score.toFixed(2)}} pts</span>
                        </div>
                    `).join('');
                    suggestions.style.display = 'block';
                }} else {{
                    suggestions.innerHTML = '<div style="padding: 0.65rem; color: #64748b; font-size: 0.8rem; text-align: center;">No se encontraron países</div>';
                    suggestions.style.display = 'block';
                }}
            }} else {{
                suggestions.style.display = 'none';
            }}

            aplicarFiltrosGlobales();
        }}

        // Limpiar búsqueda
        function limpiarBusqueda() {{
            const input = document.getElementById('global-search');
            input.value = '';
            searchQuery = '';
            document.getElementById('search-clear').style.display = 'none';
            document.getElementById('search-suggestions').style.display = 'none';
            aplicarFiltrosGlobales();
        }}

        // Cerrar menú de sugerencias al hacer clic fuera
        document.addEventListener('click', function(e) {{
            const container = document.querySelector('.nav-search-container');
            if (container && !container.contains(e.target)) {{
                document.getElementById('search-suggestions').style.display = 'none';
            }}
        }});

        // Aplicar filtros sincronizados en Mapa, Tabla de Rankings y Contadores
        function aplicarFiltrosGlobales() {{
            // 1. Filtrar lista de datos
            const filtrados = DATOS_PAISES_WHR.filter(p => {{
                const matchSeg = (currentSegment === 'Todos' || p.grupo.includes(currentSegment));
                const matchQuery = (!searchQuery || 
                    p.name_es.toLowerCase().includes(searchQuery) ||
                    p.name_en.toLowerCase().includes(searchQuery) ||
                    p.iso3.toLowerCase().includes(searchQuery)
                );
                return matchSeg && matchQuery;
            }});

            // 2. Actualizar Tabla de Rankings
            const rows = document.querySelectorAll('#tbody-rankings tr');
            let visibleCount = 0;
            rows.forEach(r => {{
                const dataPais = r.getAttribute('data-pais') || '';
                const grupo = r.getAttribute('data-grupo') || '';
                
                const matchSeg = (currentSegment === 'Todos' || grupo.includes(currentSegment));
                const matchQuery = (!searchQuery || dataPais.includes(searchQuery));

                if (matchSeg && matchQuery) {{
                    r.style.display = '';
                    visibleCount++;
                }} else {{
                    r.style.display = 'none';
                }}
            }});

            // Actualizar contadores
            const rankCounter = document.getElementById('rankings-counter');
            if (rankCounter) {{
                rankCounter.innerText = `Mostrando ${{visibleCount}} de 143 países`;
            }}

            const mapCounter = document.getElementById('map-counter-text');
            if (mapCounter) {{
                if (currentSegment !== 'Todos' || searchQuery) {{
                    mapCounter.innerText = `Filtro activo: mostrando ${{filtrados.length}} de 143 naciones en el mapa.`;
                }} else {{
                    mapCounter.innerText = 'Mostrando 143 naciones evaluadas en el mapa mundial.';
                }}
            }}

            // 3. Actualizar Mapa Coroplético de Plotly en tiempo real
            const mapDiv = document.getElementById('plotly-map-whr');
            if (mapDiv && mapDiv.data && mapDiv.data[0]) {{
                const locs = filtrados.map(d => d.name_en);
                const zs = filtrados.map(d => d.score);
                const custom = filtrados.map(d => [d.name_es, d.rank, d.score, d.lower, d.upper, d.grupo, d.gdp, d.soc, d.iso3]);

                Plotly.restyle(mapDiv, {{
                    locations: [locs],
                    z: [zs],
                    customdata: [custom]
                }}, [0]);
            }}
        }}

        // Selección de país desde autocompletado
        function seleccionarPaisDesdeBusqueda(iso3) {{
            document.getElementById('search-suggestions').style.display = 'none';
            abrirFichaPais(iso3);
        }}

        // Abrir Ficha Detallada Modal de País
        function abrirFichaPais(iso3) {{
            const p = DATOS_PAISES_WHR.find(d => d.iso3 === iso3);
            if (!p) return;
            currentCountrySelected = p;

            document.getElementById('modal-iso').innerText = p.iso3;
            document.getElementById('modal-name').innerText = p.name_es;
            document.getElementById('modal-rank').innerText = 'Rank #' + p.rank;
            document.getElementById('modal-score').innerText = p.score.toFixed(3) + ' pts';
            document.getElementById('modal-ci').innerText = `IC 95%: [${{p.lower.toFixed(2)}} — ${{p.upper.toFixed(2)}}]`;
            document.getElementById('modal-segment').innerText = p.grupo;
            document.getElementById('modal-socio-sum').innerText = `Suma Socioinstitucional: ${{p.socio_total.toFixed(2)}} pts`;

            document.getElementById('modal-gdp').innerText = p.gdp.toFixed(3) + ' pts';
            document.getElementById('modal-soc').innerText = p.soc.toFixed(3) + ' pts';
            document.getElementById('modal-health').innerText = p.health.toFixed(3) + ' pts';
            document.getElementById('modal-free').innerText = p.free.toFixed(3) + ' pts';
            document.getElementById('modal-gen').innerText = p.gen.toFixed(3) + ' pts';
            document.getElementById('modal-corr').innerText = p.corr.toFixed(3) + ' pts';
            document.getElementById('modal-dys').innerText = p.dys.toFixed(3) + ' pts';

            document.getElementById('country-modal').style.display = 'flex';
        }}

        // Cerrar Ficha
        function cerrarFichaPais() {{
            document.getElementById('country-modal').style.display = 'none';
        }}

        // Navegar a la fila del país en la tabla de rankings
        function verPaisEnRankings() {{
            cerrarFichaPais();
            switchWHRPage('view-rankings', document.getElementById('btn-nav-rankings'));
            if (currentCountrySelected) {{
                // Colocar el nombre en el buscador para resaltar la fila
                const input = document.getElementById('global-search');
                input.value = currentCountrySelected.name_es;
                handleGlobalSearch(currentCountrySelected.name_es);
            }}
        }}

        // Interacción con clic en el mapa de Plotly para abrir ficha de país
        document.addEventListener('DOMContentLoaded', function() {{
            const mapDiv = document.getElementById('plotly-map-whr');
            if (mapDiv) {{
                mapDiv.on('plotly_click', function(data) {{
                    if (data && data.points && data.points.length > 0) {{
                        const pt = data.points[0];
                        if (pt.customdata && pt.customdata[8]) {{
                            abrirFichaPais(pt.customdata[8]);
                        }}
                    }}
                }});
            }}
        }});

        // Ordenamiento dinámico de columnas en la tabla
        let ordenAsc = true;
        function ordenarTabla(colIdx, esNumero) {{
            const tbody = document.getElementById('tbody-rankings');
            const rows = Array.from(tbody.querySelectorAll('tr'));
            
            rows.sort((a, b) => {{
                let valA = a.children[colIdx].innerText.replace('[', '').replace(']', '').replace('Rank #', '').trim();
                let valB = b.children[colIdx].innerText.replace('[', '').replace(']', '').replace('Rank #', '').trim();
                
                if (esNumero) {{
                    valA = parseFloat(valA) || 0;
                    valB = parseFloat(valB) || 0;
                    return ordenAsc ? valA - valB : valB - valA;
                }} else {{
                    return ordenAsc ? valA.localeCompare(valB) : valB.localeCompare(valA);
                }}
            }});
            
            ordenAsc = !ordenAsc;
            rows.forEach(r => tbody.appendChild(r));
        }}
    </script>

</body>
</html>
"""

    # Determinar ruta de exportación coherente tanto desde raíz como desde notebooks/
    if os.path.exists('exports') or os.path.exists('data'):
        out_dir = 'exports'
    elif os.path.exists(os.path.join('..', 'exports')) or os.path.exists(os.path.join('..', 'data')):
        out_dir = os.path.join('..', 'exports')
    else:
        out_dir = 'exports'
        
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, 'EquipoX_Proyecto2_Dashboard.html')
    with open(out_file, 'w', encoding='utf-8') as f:
        f.write(dashboard_html)
        
    print(f"[OK] Tablero Oficial WHR generado exitosamente en: {out_file} ({os.path.getsize(out_file)} bytes)")
    return out_file

if __name__ == '__main__':
    build_dashboard()
