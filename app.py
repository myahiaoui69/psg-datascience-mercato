import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import pydeck as pdk
import random
import os

# Configuration de la page PSG
st.set_page_config(
    page_title="PSG DataScience Mercato - Recrutement Stagiaire",
    page_icon="🔴🔵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# === CHARTE GRAPHIQUE PSG ===
st.markdown("""
<style>
    /* Reset et styles généraux PSG */
    * {
        margin: 0;
        padding: 0;
        -webkit-box-sizing: border-box;
        box-sizing: border-box;
    }

    .stApp {
        font-family: 'Saira Semi Condensed', sans-serif;
        font-weight: 400;
        background: linear-gradient(135deg, #0a0a2a 0%, #1a1a4a 50%, #2a2a6a 100%);
        min-height: 100vh;
    }
    /* Pour Chrome, Edge, Safari */
        ::-webkit-scrollbar {
            width: 12px;
        }

        ::-webkit-scrollbar-track {
            background: #0a0a2a;
            border-radius: 6px;
        }

        ::-webkit-scrollbar-thumb {
            background-color: #DA291C;
            border-radius: 6px;
            border: 3px solid #0a0a2a;
        }

        ::-webkit-scrollbar-thumb:hover {
            background-color: #DA291C;
        }

        /* Pour Firefox */
        * {
            scrollbar-width: thin;
            scrollbar-color: #0a0a2a #DA291C;
        }

        /* Hack @supports pour forcer Firefox à appliquer couleur au hover */
        @supports (scrollbar-color: auto) {
            *:hover {
                scrollbar-color: #0a0a2a #DA291C;
            }
        }
    /* Scrollbar PSG */
    ::-webkit-scrollbar {
        width: 12px;
    }
    ::-webkit-scrollbar-track {
        background: #DA291C;
        border-radius: 6px;
    }
    ::-webkit-scrollbar-thumb {
        background-color: #DA291C;
        border-radius: 6px;
        border: 3px solid #DA291C;
    }
    ::-webkit-scrollbar-thumb:hover {
        background-color: #DA291C;
    }

    /* Header PSG */
    .main-header {
        font-size: 3.5rem;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
        background: linear-gradient(90deg, #DA291C, #DA291C, #DA291C);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Saira Semi Condensed', sans-serif;
        padding: 20px 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }

    .h3 {
        color: #DA291C;
        text-align: center;
        font-size: 1.5rem;
        margin-bottom: 2rem;
    }

    /* Carte PSG Style */
    .psg-card-svg {
        position: relative;
        width: 270px;
        height: 400px;
        margin: 20px auto;
        clip-path: url("#svgPath");
        background: linear-gradient(135deg, #ffffff 0%, #f0f0f0 50%, #e0e0e0 100%);
        box-shadow: 0 20px 40px rgba(218, 41, 28, 0.3), 
                    0 0 0 2px rgba(218, 41, 28, 0.5);
        font-family: 'Saira Semi Condensed', sans-serif;
        padding-bottom: 20px;
    }

    .card-inner {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        padding: 15px 10px 25px 10px;
        box-sizing: border-box;
    }

    /* Partie supérieure PSG */
    .card-top {
        position: absolute;
        top: 15px;
        left: 10px;
        width: calc(100% - 20px);
        height: 50%;
        background: linear-gradient(135deg, #DA291C 0%, #004170 100%);
        overflow: hidden;
        border-radius: 10px 10px 0 0;
    }

    .player-initials {
        font-size: 4rem;
        font-weight: bold;
        color: #FFFFFF;
        text-shadow: 3px 3px 6px rgba(0,0,0,0.8);
        display: flex;
        align-items: center;
        justify-content: center;
        height: 100%;
        width: 100%;
        background: linear-gradient(135deg, rgba(218, 41, 28, 0.3) 0%, rgba(0, 65, 112, 0.2) 100%);
        border-radius: 50%;
        margin: 0 auto;
    }   

    .player-image {
        position: absolute;
        right: 5px;
        bottom: 0;
        z-index: 2;
        height: 85%;
        width: 65%;
        display: flex;
        align-items: center;
        justify-content: center;
        overflow: hidden;
    }

    .player-img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        border-radius: 5px;
    }

    .player-info {
        position: absolute;
        left: 10px;
        bottom: 10px;
        z-index: 3;
        height: 80%;
        width: 30%;
        padding: 0 10px;
        text-align: center;
        text-transform: uppercase;
    }

    .player-rating {
        font-size: 35px;
        font-weight: bold;
        color: #FFFFFF;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.8);
        margin-bottom: 8px;
    }

    .player-position {
        font-size: 18px;
        color: #FFFFFF;
        font-weight: bold;
        padding-bottom: 3px;
        margin-bottom: 3px;
        border-bottom: 2px solid rgba(255, 255, 255, 0.3);
    }

    .player-badge {
        font-size: 14px;
        color: #FFFFFF;
        background: #004170;
        padding: 2px 6px;
        border-radius: 8px;
        margin: 3px 0;
        border: 1px solid #DA291C;
    }

    /* Partie inférieure PSG */
    .card-bottom {
        position: absolute;
        bottom: 20px;
        left: 10px;
        width: calc(100% - 20px);
        height: 42%;
        background: linear-gradient(135deg, #004170 0%, #0a0a2a 100%);
        border-radius: 0 0 10px 10px;
        padding: 5px;
        box-sizing: border-box;
    }

    .player-name {
        text-align: center;
        font-size: 20px;
        text-transform: uppercase;
        font-weight: bold;
        color: #FFFFFF;
        margin: 2px 0 2px 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.8);
        line-height: 1.1;
    }

    .player-stats {
        display: flex;
        justify-content: space-around;
        margin: 0 10px;
        padding-top: 5px;
        border-top: 2px solid #DA291C;
    }

    .stats-column {
        width: 48%;
    }

    .stat-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 2px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        position: relative;
    }

    .stat-item::after {
        content: "";
        position: absolute;
        right: -5px;
        top: 0;
        height: 100%;
        width: 1px;
        background: rgba(255, 255, 255, 0.2);
    }

    .stats-column:last-child .stat-item::after {
        display: none;
    }

    .stat-value {
        font-size: 18px;
        font-weight: bold;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.8);
        min-width: 25px;
        text-align: center;
        flex-shrink: 0;
        margin-right: 5px;
        padding: 2px 6px;
        border-radius: 4px;
        background: linear-gradient(135deg, #DA291C, #004170);
        box-shadow: 0 2px 4px rgba(0,0,0,0.3);
        color: white;
    }

    .stat-value.high { background: linear-gradient(135deg, #DA291C, #004170); }
    .stat-value.medium { background: linear-gradient(135deg, #FF6B35, #DA291C); }
    .stat-value.low { background: linear-gradient(135deg, #FF8C42, #FF6B35); }

    .stat-label {
        font-size: 9px;
        color: #FFFFFF;
        text-transform: uppercase;
        font-weight: 600;
        text-align: left;
        padding-left: 2px;
        flex-grow: 1;
    }

    .stat-item::before {
        content: "•";
        color: #DA291C;
        margin-right: 5px;
        font-weight: bold;
    }

    .svg-container {
        position: absolute;
        top: 0;
        left: 0;
        width: 0;
        height: 0;
        overflow: hidden;
    }

    /* Nouveaux styles PSG */
    .psg-badge {
        background: linear-gradient(45deg, #DA291C, #004170);
        color: white;
        padding: 10px 20px;
        border-radius: 25px;
        font-weight: bold;
        text-align: center;
        margin: 10px 0;
        border: 2px solid gold;
    }

    .transfer-market {
        background: rgba(218, 41, 28, 0.1);
        border: 2px solid #DA291C;
        border-radius: 15px;
        padding: 15px;
        margin: 10px 0;
    }
</style>

<!-- SVG POUR LA FORME DE BOUCLIER -->
<svg class="svg-container" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 267.3 427.3">
    <clipPath id="svgPath">
        <path fill="#000" d="M265.3 53.9a33.3 33.3 0 0 1-17.8-5.5 32 32 0 0 1-13.7-22.9c-.2-1.1-.4-2.3-.4-3.4 0-1.3-1-1.5-1.8-1.9a163 163 0 0 0-31-11.6A257.3 257.3 0 0 0 133.7 0a254.9 254.9 0 0 0-67.1 8.7 170 170 0 0 0-31 11.6c-.8.4-1.8.6-1.8 1.9 0 1.1-.2 2.3-.4 3.4a32.4 32.4 0 0 1-13.7 22.9A33.8 33.8 0 0 1 2 53.9c-1.5.1-2.1.4-2 2v293.9c0 3.3 0 6.6.4 9.9a22 22 0 0 0 7.9 14.4c3.8 3.2 8.3 5.3 13 6.8 12.4 3.9 24.8 7.5 37.2 11.5a388.7 388.7 0 0 1 50 19.4 88.7 88.7 0 0 1 25 15.5v.1-.1c7.2-7 16.1-11.3 25-15.5a427 427 0 0 1 50-19.4l37.2-11.5c4.7-1.5 9.1-3.5 13-6.8 4.5-3.8 7.2-8.5 7.9-14.4.4-3.3.4-6.6.4-9.9V231.6 60.5v-4.6c.4-1.6-.3-1.9-1.7-2z"/>
    </clipPath>
</svg>
""", unsafe_allow_html=True)

# === FONCTIONS (adaptées PSG) ===
def calculate_education_score(education_level):
    levels = {'Bac': 1, 'Bac+2': 2, 'Bac+3': 3, 'Bac+4': 4, 'Bac+5': 5, 'Doctorat': 6}
    return levels.get(education_level, 3)

def calculate_language_score(languages):
    score = 0
    level_bonus = {'A1': 0.1, 'A2': 0.25, 'B1': 0.5, 'B2': 0.75, 'C1': 1, 'C2': 1.2}  # C2 réduit à 1.2
    language_weights = {
        'français': 1.5, 'french': 1.5,  # Poids réduits
        'anglais': 1.2, 'english': 1.2, 
        'espagnol': 1.0, 'spanish': 1.0, 
        'arabe': 1.1, 'arabic': 1.1,
        'portugais': 1.0, 'portuguese': 1.0,
        'allemand': 0.9, 'german': 0.9
    }
    
    for lang, level in languages.items():
        weight = language_weights.get(lang.lower(), 0.8)  # Poids par défaut réduit
        bonus = level_bonus.get(level, 0.5)
        score += (1 + bonus) * weight
    
    return min(score, 10)  # Plage maximale réduite à 10

def calculate_experience_score(experiences):
    total_score = 0
    for exp in experiences:
        duration = exp.get('duration', 0)
        if exp.get('type') == 'alternance':
            total_score += duration / 2
        elif exp.get('type') == 'emploi':
            total_score += duration / 6
        else:
            total_score += duration / 12
    return min(total_score, 10)

def calculate_skills_score(skills, weights):
    total = sum(skills[skill] * weight for skill, weight in weights.items() if skill in skills)
    max_possible = sum(100 * weight for weight in weights.values())
    return (total / max_possible) * 100 if max_possible > 0 else 0

def calculate_psg_bonus(candidate):
    """Bonus spécial pour les candidats alignés avec les valeurs du PSG"""
    bonus = 0
    
    # Bonus pour les langues parlées au PSG
    psg_languages = ['français', 'portugais', 'espagnol', 'arabe', 'anglais']
    for lang in candidate['languages']:
        if lang.lower() in psg_languages:
            bonus += 2
    
    # Bonus pour expérience en sport
    if candidate['sports_interest'] >= 80:
        bonus += 3
    
    # Bonus pour compétences spécifiques au football
    football_skills = ['computer_vision', 'ml', 'deep_learning']
    for skill in football_skills:
        if candidate['skills'].get(skill, 0) >= 80:
            bonus += 2
    
    return min(bonus, 10)

# === CHARGEMENT DES DONNÉES PSG ===
def load_psg_data():
    skills_weights = {
        'python': 0.15, 'sql': 0.08, 'ml': 0.12, 'deep_learning': 0.10,
        'computer_vision': 0.10, 'nlp': 0.08, 'quantum_computing': 0.06,
        'streamlit': 0.05, 'dash': 0.04, 'qlik_sense': 0.04, 'knime': 0.04,
        'qgis': 0.03, 'postgresql': 0.03, 'sql_server': 0.03, 
        'azure_data_lake': 0.04, 'combinatorial_optimization': 0.03
    }

    positions = ['Data Scientist', 'ML Engineer', 'Data Analyst', 'BI Analyst', 'Data Engineer']
    locations = ['Paris', 'Île-de-France', 'Lyon', 'Marseille', 'Remote']
    education_levels = ['Bac+3', 'Bac+4', 'Bac+5', 'Doctorat']
    
    # Noms réalistes et cohérents
    noms = ['MARTIN', 'DUBOIS', 'BERNARD', 'THOMAS', 'PETIT',
            'ROBERT', 'RICHARD', 'DURAND', 'MOREAU', 'LAURENT']
    prenoms = ['Lucas', 'Marie', 'Thomas', 'Camille', 'Alexandre',
               'Julie', 'Nicolas', 'Sarah', 'Kevin', 'Laura']

    candidates = []
    used_names = set()

    for i in range(25):
        while True:
            nom = random.choice(noms)
            prenom = random.choice(prenoms)
            fullname = f"{prenom} {nom}"
            if fullname not in used_names:
                used_names.add(fullname)
                break
        position = random.choice(positions)
        location = random.choice(locations)
        education = random.choice(education_levels)

        # Profils adaptés au PSG
        if i < 8:
            skills = {
                'python': 70 + (i % 20), 'sql': 65 + (i % 25), 'ml': 60 + (i % 30),
                'deep_learning': 40 + (i % 40), 'computer_vision': 30 + (i % 35),
                'nlp': 35 + (i % 30), 'quantum_computing': 10 + (i % 20),
                'streamlit': 50 + (i % 40), 'dash': 40 + (i % 35), 'qlik_sense': 30 + (i % 40),
                'knime': 45 + (i % 35), 'qgis': 20 + (i % 30), 'postgresql': 60 + (i % 30),
                'sql_server': 55 + (i % 35), 'azure_data_lake': 35 + (i % 40),
                'combinatorial_optimization': 25 + (i % 30)
            }
            sports = 60 + (i * 2)
            experience_duration = random.randint(6, 24)
        elif i < 20:
            skills = {
                'python': 75 + (i % 15), 'sql': 70 + (i % 20), 'ml': 65 + (i % 25),
                'deep_learning': 50 + (i % 30), 'computer_vision': 45 + (i % 25),
                'nlp': 50 + (i % 20), 'quantum_computing': 20 + (i % 25),
                'streamlit': 60 + (i % 30), 'dash': 50 + (i % 25), 'qlik_sense': 40 + (i % 35),
                'knime': 55 + (i % 25), 'qgis': 30 + (i % 25), 'postgresql': 65 + (i % 25),
                'sql_server': 60 + (i % 30), 'azure_data_lake': 45 + (i % 35),
                'combinatorial_optimization': 35 + (i % 25)
            }
            sports = 70 + (i * 1)
            experience_duration = random.randint(24, 36)
        else:
            skills = {
                'python': 80 + (i % 10), 'sql': 75 + (i % 15), 'ml': 70 + (i % 20),
                'deep_learning': 60 + (i % 20), 'computer_vision': 55 + (i % 15),
                'nlp': 60 + (i % 15), 'quantum_computing': 30 + (i % 20),
                'streamlit': 70 + (i % 20), 'dash': 60 + (i % 15), 'qlik_sense': 50 + (i % 25),
                'knime': 65 + (i % 15), 'qgis': 40 + (i % 20), 'postgresql': 70 + (i % 20),
                'sql_server': 65 + (i % 25), 'azure_data_lake': 55 + (i % 25),
                'combinatorial_optimization': 45 + (i % 20)
            }
            sports = 80 + (i * 1)
            experience_duration = random.randint(36, 48)

        skills = {k: min(v, 95) for k, v in skills.items()}

        candidate = {
            'id': i + 1,
            'name': fullname,
            'position': position,
            'location': location,
            'education': education,
            'education_score': calculate_education_score(education),
            'languages': {'anglais': random.choice(['B1', 'B2', 'C1']), 
                         'français': random.choice(['B1', 'B2', 'C1', 'C2'])},
            'experiences': [{'type': 'emploi', 'duration': experience_duration}],
            'skills': skills,
            'sports_interest': min(sports, 95),
            'description': f'Profil {position} passionné de data et football'
        }

        candidate['language_score'] = calculate_language_score(candidate['languages'])
        candidate['experience_score'] = calculate_experience_score(candidate['experiences'])
        candidate['skills_score'] = calculate_skills_score(candidate['skills'], skills_weights)
        candidate['psg_bonus'] = calculate_psg_bonus(candidate)

        candidate['overall_score'] = int(
            0.30 * candidate['skills_score'] +
            0.25 * min(candidate['experience_score'] * 10, 100) +
            0.20 * candidate['sports_interest'] +
            0.15 * min(candidate['language_score'] * 10, 100) +
            0.10 * min(candidate['education_score'] * 20, 100) +
            candidate['psg_bonus']
        )

        candidates.append(candidate)

    # VOTRE PROFIL PSG
        # VOTRE PROFIL PSG (score réaliste)
    my_profile = {
        'id': len(candidates) + 1,
        'name': 'Mohamed Yahiaoui',
        'position': 'Data Scientist',
        'location': 'Paris',
        'education': 'Bac+5',
        'education_score': calculate_education_score('Bac+5'),
        'languages': {
            'français': 'C2',
            'anglais': 'B2',  # B2 au lieu de C2 pour être crédible
            'arabe': 'B1',    # B1 au lieu de C1
            'espagnol': 'A2'
        },
        'experiences': [
            {'type': 'emploi', 'duration': 48}  # 4 ans au lieu de 6 pour un stage
        ],
        'skills': {
            'python': 85, 'sql': 80, 'ml': 82, 'deep_learning': 75,  # Scores légèrement réduits
            'computer_vision': 70, 'nlp': 85, 'quantum_computing': 55,
            'streamlit': 80, 'dash': 70, 'qlik_sense': 80, 'knime': 90,
            'qgis': 70, 'postgresql': 80, 'sql_server': 65, 
            'azure_data_lake': 65, 'combinatorial_optimization': 65
        },
        'sports_interest': 88,  # Légèrement réduit
        'description': 'Data Scientist passionné avec 4 ans d\'expérience en IA et machine learning. Spécialiste en analyse de données sportives et grand passionné de football.',
        'photo': '🧑‍💻',
        'lat': 48.84,
        'lon': 2.37
    }

    my_profile['language_score'] = calculate_language_score(my_profile['languages'])
    my_profile['experience_score'] = calculate_experience_score(my_profile['experiences'])
    my_profile['skills_score'] = calculate_skills_score(my_profile['skills'], skills_weights)
    my_profile['psg_bonus'] = calculate_psg_bonus(my_profile)
    
    # Calcul réaliste pour un score autour de 90
    my_profile['overall_score'] = int(
        0.30 * my_profile['skills_score'] +
        0.25 * min(my_profile['experience_score'] * 10, 100) +
        0.20 * my_profile['sports_interest'] +
        0.15 * min(my_profile['language_score'] * 10, 100) +
        0.10 * min(my_profile['education_score'] * 20, 100) +
        my_profile['psg_bonus']
    )

    # Garantir un score crédible mais compétitif
    my_profile['overall_score'] = min(max(my_profile['overall_score'], 88), 92)
    candidates.append(my_profile)

    df = pd.DataFrame(candidates).sort_values('overall_score', ascending=False).reset_index(drop=True)
    return df

# === INITIALISATION ===
if 'stable_data' not in st.session_state:
    st.session_state.stable_data = load_psg_data()
    st.session_state.stable_data['stable_id'] = range(len(st.session_state.stable_data))

df = st.session_state.stable_data

# === INTERFACE STREAMLIT PSG ===
st.markdown('<div class="main-header">🔴🔵 PSG DATASCIENCE MERCATO 2025 🔵🔴</div>', unsafe_allow_html=True)
st.markdown('<div class="h3">**Paris Saint-Germain** - Recrutement du futur talent Data Science</div>', unsafe_allow_html=True)

# Header avec logo PSG
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <div style="font-size: 4rem;">⚽</div>
        <h3 style="color: #DA291C; font-weight: bold;">ICI C'EST PARIS !</h3>
    </div>
    """, unsafe_allow_html=True)

# === SIDEBAR PSG ===
st.sidebar.header("🔴 Centre de Recrutement PSG")

# Badge PSG dans la sidebar
st.sidebar.markdown("""
<div class="psg-badge">
    ⚽ PSG DATA SCIENCE<br>
    <small>Saison 2025-2026</small>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("""
*Recherchez la perle rare pour rejoindre notre centre de data science.*
""")

# Filtres PSG
min_score = st.sidebar.slider("Score global minimum", 0, 100, 0)
sports_interest = st.sidebar.slider("Passion football minimum", 0, 100, 0)

st.sidebar.markdown("---")
st.sidebar.subheader("Filtres techniques PSG")

min_skills = st.sidebar.slider("Compétences techniques", 0, 100, 0)
min_experience = st.sidebar.slider("Expérience minimum", 0, 100, 0)
min_languages = st.sidebar.slider("Langues minimum", 0, 100, 0)

# Filtre spécial PSG
psg_alignment = st.sidebar.slider("Alignement valeurs PSG", 0, 10, 5)

location_filter = st.sidebar.selectbox("Localisation", ['Toutes', 'Paris', 'Île-de-France', 'Remote'])
position_filter = st.sidebar.multiselect(
    "Poste recherché", 
    ['Data Scientist', 'ML Engineer', 'Data Analyst', 'BI Analyst', 'Data Engineer'],
    default=['Data Scientist', 'ML Engineer']
)

# Filtrage des données
filtered_df = df[
    (df['overall_score'] >= min_score) & 
    (df['sports_interest'] >= sports_interest) &
    (df['skills_score'] >= min_skills) &
    ((df['experience_score'] * 10) >= min_experience) &
    ((df['language_score'] * 10) >= min_languages) &
    (df['psg_bonus'] >= psg_alignment)
]

if location_filter != 'Toutes':
    filtered_df = filtered_df[filtered_df['location'] == location_filter]

if position_filter:
    filtered_df = filtered_df[filtered_df['position'].isin(position_filter)]

st.sidebar.markdown(f"**{len(filtered_df)} candidats sélectionnés**")

# === ONGLETS PRINCIPAUX ===
tab1, tab2, tab3 = st.tabs(["🎴 Mercato des Talents", "📊 Comparaison d'Équipe", "🏆 Mon Profil PSG"])

with tab1:
    st.markdown("""
    <h2 style="text-align: center; color: #DA291C; margin-bottom: 2rem;">
    🔴 CARTES DES FUTURS TALENTS 🔵
    </h2>
    """, unsafe_allow_html=True)
    
    # Market value estimation
    st.markdown("""
    <div class="transfer-market">
        <h4 style="color: #DA291C; text-align: center;">📈 Marché des Transferts Data Science</h4>
        <p style="color: #DA291C; text-align: center;">Valeur estimée des talents basée sur leur score global et potentiel</p>
    </div>
    """, unsafe_allow_html=True)
    
    cols = st.columns(2)
    for idx, (_, candidate) in enumerate(filtered_df.iterrows()):
        with cols[idx % 2]:
            name_parts = candidate['name'].split()
            initials = name_parts[0][0].upper() + (name_parts[1][0].upper() if len(name_parts) > 1 else '')
            
            # Estimation de valeur de transfert (en k€)
            transfer_value = candidate['overall_score'] * 1000 + candidate['psg_bonus'] * 500
            
            st.markdown(f"""
            <div class="composite-card">
                <div class="card-base">
                    <div class="psg-card-svg">
                        <div class="card-inner">
                            <div class="card-top">
                                <div class="player-image">
                                    <div class="player-initials" style="opacity:0.3;">{initials}</div>
                                </div>
                                <div class="player-info">
                                    <div class="player-rating">{candidate['overall_score']}</div>
                                    <div class="player-position">DS</div>
                                    <div class="player-badge">+{candidate['psg_bonus']} PSG</div>
                                </div>
                            </div>
                            <div class="card-bottom">
                                <div class="player-name">{candidate['name']}</div>
                                <div style="text-align: center; color: gold; font-size: 12px; margin-bottom: 5px;">
                                    💰 Valeur: {transfer_value:,.0f} €
                                </div>
                                <div class="player-stats">
                                    <div class="stats-column">
                                        <div class="stat-item">
                                            <span class="stat-value">{candidate['skills_score']:.0f}</span>
                                            <span class="stat-label">SKILLS</span>
                                        </div>
                                        <div class="stat-item">
                                            <span class="stat-value">{candidate['experience_score'] * 10:.0f}</span>
                                            <span class="stat-label">EXP</span>
                                        </div>
                                        <div class="stat-item">
                                            <span class="stat-value">{candidate['sports_interest']}</span>
                                            <span class="stat-label">FOOTBALL</span>
                                        </div>
                                    </div>
                                    <div class="stats-column">
                                        <div class="stat-item">
                                            <span class="stat-value">{candidate['language_score'] * 10:.0f}</span>
                                            <span class="stat-label">LANG</span>
                                        </div>
                                        <div class="stat-item">
                                            <span class="stat-value">{candidate['skills']['python']}</span>
                                            <span class="stat-label">PYTHON</span>
                                        </div>
                                        <div class="stat-item">
                                            <span class="stat-value">{candidate['skills']['ml']}</span>
                                            <span class="stat-label">ML</span>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

with tab2:
    st.header("📊 Comparaison d'Équipe - Radar Chart")
    
    if 'selected_candidates' not in st.session_state:
        st.session_state.selected_candidates = df['name'].tolist()[:2]
    
    df_display = df.copy()
    df_display['display_id'] = df_display.index.astype(str) + "_" + df_display['name']
    
    candidate_options = df_display['display_id'].tolist()
    display_to_name = dict(zip(df_display['display_id'], df_display['name']))
    name_to_display = dict(zip(df_display['name'], df_display['display_id']))
    
    current_selection = [name_to_display[name] for name in st.session_state.selected_candidates 
                        if name in name_to_display]
    
    with st.container():
        col1, col2 = st.columns([3, 1])
        
        with col1:
            selected_display_ids = st.multiselect(
                "Choisissez 2 à 3 candidats à comparer",
                options=candidate_options,
                default=current_selection,
                max_selections=3,
                key="candidate_selector"
            )
    
    new_selection = [display_to_name[display_id] for display_id in selected_display_ids 
                    if display_id in display_to_name]
    
    if set(new_selection) != set(st.session_state.selected_candidates):
        st.session_state.selected_candidates = new_selection
        st.rerun()
    
    st.info(f"**Candidats sélectionnés ({len(st.session_state.selected_candidates)}/3) :** " +
            ", ".join(st.session_state.selected_candidates))
    
    compare_df = df[df['name'].isin(st.session_state.selected_candidates)].copy()
    
    if len(compare_df) >= 2:
        fig = go.Figure()
        colors = ['#DA291C', '#004170', '#FFD700']
        
        for i, (_, candidate) in enumerate(compare_df.iterrows()):
            values = [
                candidate['skills_score'],
                min(candidate['experience_score'] * 10, 100),
                candidate['sports_interest'],
                min(candidate['language_score'] * 10, 100),
                min(candidate['education_score'] * 20, 100),
                candidate['psg_bonus'] * 10
            ]
            
            fig.add_trace(go.Scatterpolar(
                r=values + [values[0]],
                theta=['Compétences', 'Expérience', 'Football', 'Langues', 'Éducation', 'PSG'] + ['Compétences'],
                fill='toself',
                name=candidate['name'],
                line=dict(color=colors[i], width=3),
                opacity=0.7
            ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 100], showline=False, showticklabels=False)
            ),
            showlegend=True,
            height=500,
            legend=dict(bgcolor='rgba(255,255,255,0.9)'),
            title="Comparaison des talents PSG"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Tableau comparatif PSG
        st.subheader("📋 Fiche Comparatif PSG")
        comparison_data = []
        for _, candidate in compare_df.iterrows():
            comparison_data.append({
                'Candidat': candidate['name'],
                'Score Global': candidate['overall_score'],
                'Bonus PSG': candidate['psg_bonus'],
                'Compétences': f"{candidate['skills_score']:.0f}/100",
                'Expérience': f"{candidate['experience_score'] * 10:.0f}/100",
                'Football': f"{candidate['sports_interest']}/100",
                'Langues': f"{candidate['language_score'] * 10:.0f}/100",
                'Valeur Transfert': f"{(candidate['overall_score'] * 1000 + candidate['psg_bonus'] * 500):,.0f} €"
            })
        
        st.dataframe(
            pd.DataFrame(comparison_data),
            use_container_width=True,
            hide_index=True
        )
        
    elif len(compare_df) == 1:
        st.warning("⚠️ Sélectionnez au moins un candidat supplémentaire pour la comparaison")
    else:
        st.info("👆 Sélectionnez 2 ou 3 candidats pour commencer la comparaison.")

with tab3:
    st.markdown("<h2 style='color: #DA291C;'>🏆 Mon Profil PSG</h2>", unsafe_allow_html=True)

    
    # Récupérer votre profil
    my_profile = df[df['name'] == 'Mohamed Yahiaoui'].iloc[0]
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown(f"""
        <div style="text-align: center;">
            <div style="font-size: 80px;">🧑‍💻</div>
            <h2 style="color: #DA291C;">{my_profile['name']}</h2>
            <div class="psg-badge">Score Global: {my_profile['overall_score']}/100</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Carte d'identité PSG
        st.markdown("""
        <div style="background: linear-gradient(135deg, #DA291C, #004170); 
                    color: white; padding: 20px; border-radius: 15px; margin-top: 20px;">
            <h4>🆔 Carte d'Identité PSG</h4>
            <p><strong>Poste:</strong> Data Scientist</p>
            <p><strong>Localisation:</strong> Paris</p>
            <p><strong>Bonus PSG:</strong> +{}</p>
            <p><strong>Valeur estimée:</strong> {:,} €</p>
        </div>
        """.format(my_profile['psg_bonus'], (my_profile['overall_score'] * 1000 + my_profile['psg_bonus'] * 500)), 
        unsafe_allow_html=True)
    
    with col2:
        # Graphique de compétences
        skills_df = pd.DataFrame({
            'Compétence': list(my_profile['skills'].keys())[:8],
            'Niveau': list(my_profile['skills'].values())[:8]
        })
        
        fig = px.bar(skills_df, x='Compétence', y='Niveau', 
                    title="📊 Mes Compétences Techniques",
                    color='Niveau', color_continuous_scale=['#004170', '#DA291C'])
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
        
        # Message personnel

        st.markdown("""
        <div style="background: rgba(218, 41, 28, 0.1); padding: 20px; border-radius: 10px; border-left: 4px solid #DA291C; color: white;">
            <h4 style="color: white;">💬 Mon Message au PSG</h4>
            <p style="color: white;">Passionné de data et de football, je souhaite mettre mes compétences en science des données 
            au service du Paris Saint-Germain pour contribuer à l'excellence sportive par l'innovation data.</p>
            <p style="color: white;"><strong>#ICICESTPARIS #DataDrivenFootball</strong></p>
        </div>
        """, unsafe_allow_html=True)
      

# Footer PSG
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #DA291C; font-size: 1.1rem;'>
    <strong>PARIS SAINT-GERMAIN 2025</strong> - <em>Rêvons plus grand !</em> 🔴🔵
</div>
""", unsafe_allow_html=True)