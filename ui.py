import streamlit as st
from ui_utils import (
    apply_login_theme, check_password, show_logout_button, transform, create_navigation_header, create_stats_card,
    create_progress_bar, create_game_result_card, create_ranking_item,
    create_study_group_card, create_game_mode_card, get_game_mode_options,
    create_notification_card, load_user_progress, save_user_progress,
    calculate_level_from_points, create_level_badge, create_points_badge
)
from pdf_to_quizz import pdf_to_quizz
from text_to_quizz import txt_to_quizz
from generate_pdf import generate_pdf_quiz
import json
import asyncio
import time
from datetime import datetime
import os

# Configuración inicial de la página
st.set_page_config(
    page_title="EduPlay - Plataforma Educativa Gamificada",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS personalizado mejorado
st.markdown("""
<style>
    .main-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
        padding: 2rem;
    }

    .welcome-card {
        background: rgba(255, 255, 255, 0.95);
        padding: 3rem;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        backdrop-filter: blur(10px);
        margin: 2rem 0;
        color: black;
    }

    .game-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }

    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin: 2rem 0;
    }

    .question-interface {
        background: rgba(255, 255, 255, 0.95);
        padding: 2rem;
        border-radius: 20px;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }

    .answer-option {
        background: white;
        border: 2px solid #e0e0e0;
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
        transition: all 0.3s ease;
        cursor: pointer;
    }

    .answer-option:hover {
        border-color: #667eea;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    }

    .correct-option {
        background: #d4edda !important;
        border-color: #28a745 !important;
        color: #155724;
    }

    .incorrect-option {
        background: #f8d7da !important;
        border-color: #dc3545 !important;
        color: #721c24;
    }

    .timer-circle {
        width: 80px;
        height: 80px;
        border-radius: 50%;
        border: 4px solid #e0e0e0;
        border-top: 4px solid #667eea;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        font-size: 1.2rem;
        animation: spin 2s linear infinite;
    }

    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }

    .navigation-tabs {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 15px;
        padding: 1rem;
        margin-bottom: 2rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }

    .stButton > button {
        background: linear-gradient(45deg, #667eea 0%, #764ba2 100%);
        color: black;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: bold;
        transition: all 0.3s ease;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }

    .sidebar .stSelectbox {
        background: black;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Inicializar session state
def init_session_state():
    if 'user_data' not in st.session_state:
        st.session_state.user_data = load_user_progress()

    if 'games_library' not in st.session_state:
        st.session_state.games_library = []

    if 'current_game' not in st.session_state:
        st.session_state.current_game = None

    if 'game_state' not in st.session_state:
        st.session_state.game_state = 'menu'

    if 'current_question_index' not in st.session_state:
        st.session_state.current_question_index = 0

    if 'game_score' not in st.session_state:
        st.session_state.game_score = 0

    if 'game_answers' not in st.session_state:
        st.session_state.game_answers = []

    if 'game_start_time' not in st.session_state:
        st.session_state.game_start_time = None

def ensure_data_directory():
    if not os.path.exists("data"):
        os.makedirs("data")

def create_game_from_questions(questions, title, subject, filename, game_mode="cuestionario"):
    """Crea un juego a partir de las preguntas generadas"""
    game = {
        'id': len(st.session_state.games_library) + 1,
        'title': title,
        'subject': subject,
        'questions': questions,
        'created_at': datetime.now().strftime("%Y-%m-%d %H:%M"),
        'difficulty': determine_difficulty(questions),
        'total_questions': len(questions),
        'best_score': 0,
        'times_played': 0,
        'filename': filename,
        'game_mode': game_mode
    }
    return game

def determine_difficulty(questions):
    """Determina la dificultad basada en el número de preguntas"""
    num_questions = len(questions)
    if num_questions <= 5:
        return "Fácil"
    elif num_questions <= 10:
        return "Medio"
    else:
        return "Difícil"

def show_welcome_screen():
    """Pantalla de bienvenida principal"""
    user_data = st.session_state.user_data

    # Header de navegación
    st.markdown(create_navigation_header(), unsafe_allow_html=True)

    # Contenido principal de bienvenida
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("""
        <div class="welcome-card">
            <h1>🎮 Transforma tus PDFs en Juegos Educativos</h1>
            <p style="font-size: 1.2rem; color: #666; margin: 1rem 0;">
                Con el poder de la Inteligencia Artificial, convierte automáticamente tus materiales de
                estudio en experiencias interactivas y divertidas
            </p>
            <div style="margin: 2rem 0;">
                <span style="background: #4CAF50; color: black; padding: 0.5rem 1rem; border-radius: 20px; margin: 0.5rem;">
                    📄 Sube PDF
                </span>
                <span style="margin: 0 1rem; font-size: 1.5rem;">→</span>
                <span style="background: #2196F3; color: black; padding: 0.5rem 1rem; border-radius: 20px; margin: 0.5rem;">
                    🤖 IA Procesa
                </span>
                <span style="margin: 0 1rem; font-size: 1.5rem;">→</span>
                <span style="background: #FF9800; color: black; padding: 0.5rem 1rem; border-radius: 20px; margin: 0.5rem;">
                    🎮 Juego Listo
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        # Menú de navegación principal
        st.markdown("""
        <div style="background: rgba(255,255,255,0.9); padding: 2rem; border-radius: 20px; box-shadow: 0 8px 32px rgba(0,0,0,0.1);">
            <h3 style="text-align: center; margin-bottom: 1.5rem; color: black;">📋 Menú Principal</h3>
        """, unsafe_allow_html=True)

        if st.button("📚 Crear Nuevo Juego", use_container_width=True):
            st.session_state.page = "crear_juego"
            st.rerun()

        if st.button("🎮 Mis Juegos", use_container_width=True):
            st.session_state.page = "mis_juegos"
            st.rerun()

        if st.button("👥 Grupos de Estudio", use_container_width=True):
            st.session_state.page = "grupos_estudio"
            st.rerun()

        if st.button("🏆 Rankings", use_container_width=True):
            st.session_state.page = "rankings"
            st.rerun()

        if st.button("⚙️ Configuración", use_container_width=True):
            st.session_state.page = "configuracion"
            st.rerun()

        if st.button("📢 Novedades", use_container_width=True):
            st.session_state.page = "novedades"
            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    # Estadísticas del usuario
    st.markdown("### 📊 Tu Progreso")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(create_stats_card(
            "Nivel", f"{user_data['level']}", "🎖️", "#FF6B6B"
        ), unsafe_allow_html=True)

    with col2:
        st.markdown(create_stats_card(
            "Puntos", f"{user_data['points']}", "⭐", "#4ECDC4"
        ), unsafe_allow_html=True)

    with col3:
        st.markdown(create_stats_card(
            "Juegos Jugados", f"{user_data['total_games']}", "🎮", "#45B7D1"
        ), unsafe_allow_html=True)

    with col4:
        accuracy = (user_data['correct_answers'] / user_data['total_questions'] * 100) if user_data['total_questions'] > 0 else 0
        st.markdown(create_stats_card(
            "Precisión", f"{accuracy:.1f}%", "🎯", "#96CEB4"
        ), unsafe_allow_html=True)

    # Progreso al siguiente nivel
    if user_data['points'] > 0:
        next_level_points = calculate_level_from_points(user_data['points']) * 100
        current_level_progress = user_data['points'] - ((calculate_level_from_points(user_data['points']) - 1) * 100)
        st.markdown(create_progress_bar(
            current_level_progress, 100,
            f"Progreso al Nivel {calculate_level_from_points(user_data['points']) + 1}",
            "#667eea"
        ), unsafe_allow_html=True)

def show_crear_juego():
    """Pantalla para crear nuevos juegos"""
    st.markdown(create_navigation_header(), unsafe_allow_html=True)

    st.markdown("## 📚 Crear Nuevo Juego")

    # Tabs para diferentes métodos de creación
    tab1, tab2 = st.tabs(["📄 Desde PDF", "✏️ Desde Texto"])

    with tab1:
        st.markdown("""
        <div class="welcome-card">
            <h3>📄 Crear Juego desde PDF</h3>
            <p>Sube tu archivo PDF y nuestra IA generará automáticamente un juego educativo</p>
        </div>
        """, unsafe_allow_html=True)

        # Metadatos del juego
        col1, col2 = st.columns(2)
        with col1:
            game_title = st.text_input("🏷️ Título del juego", placeholder="Ej: Historia del Perú - Independencia")
        with col2:
            game_subject = st.selectbox("📚 Materia", ["Historia", "Matemáticas", "Ciencias", "Literatura", "Geografía", "Física", "Química", "Otro"])

        # Selección de modo de juego
        game_modes = get_game_mode_options()
        selected_mode = st.selectbox(
            "🎮 Modo de Juego",
            options=[mode["value"] for mode in game_modes],
            format_func=lambda x: next(mode["label"] for mode in game_modes if mode["value"] == x)
        )

        # Mostrar descripción del modo selecido
        mode_description = next(mode["description"] for mode in game_modes if mode["value"] == selected_mode)
        st.info(f"📝 {mode_description}")

        # Upload de archivo
        uploaded_file = st.file_uploader("📎 Selecciona tu archivo PDF", type=["pdf"])

        if uploaded_file is not None:
            old_file_name = st.session_state.get('uploaded_file_name', None)
            if (old_file_name != uploaded_file.name):
                with st.spinner("🤖 Procesando PDF con IA..."):
                    with open(f"data/{uploaded_file.name}", "wb") as f:
                        f.write(uploaded_file.getvalue())

                    st.session_state['uploaded_file_name'] = uploaded_file.name
                    st.session_state['questions'] = asyncio.run(pdf_to_quizz(f"data/{uploaded_file.name}"))

                    st.success("✅ ¡Quiz generado exitosamente!")
                    st.balloons()

        # Crear el juego
        if 'questions' in st.session_state and game_title:
            if st.button("🎮 Crear Juego", type="primary"):
                questions = transform(st.session_state['questions']) if isinstance(st.session_state['questions'][0], dict) else st.session_state['questions']
                game = create_game_from_questions(questions, game_title, game_subject, uploaded_file.name, selected_mode)
                st.session_state.games_library.append(game)

                st.success("🎉 ¡Juego creado y agregado a tu biblioteca!")

                # Preview del juego
                col1, col2 = st.columns([2, 1])
                with col1:
                    st.markdown(create_game_mode_card(
                        "🎮", game['title'],
                        f"📚 {game['subject']} | 🎯 {game['difficulty']}",
                        game['difficulty'], game['total_questions']
                    ), unsafe_allow_html=True)

                with col2:
                    if st.button("▶️ Jugar Ahora"):
                        start_game(game)

    with tab2:
        st.markdown("""
        <div class="welcome-card">
            <h3>✏️ Crear Juego desde Texto</h3>
            <p>Ingresa texto directamente y genera preguntas automáticamente</p>
        </div>
        """, unsafe_allow_html=True)

        # Metadatos del juego
        col1, col2 = st.columns(2)
        with col1:
            text_game_title = st.text_input("🏷️ Título del juego", placeholder="Ej: Conceptos de Física", key="text_title")
        with col2:
            text_game_subject = st.selectbox("📚 Materia", ["Historia", "Matemáticas", "Ciencias", "Literatura", "Geografía", "Física", "Química", "Otro"], key="text_subject")

        # Selección de modo de juego para texto
        text_selected_mode = st.selectbox(
            "🎮 Modo de Juego",
            options=[mode["value"] for mode in game_modes],
            format_func=lambda x: next(mode["label"] for mode in game_modes if mode["value"] == x),
            key="text_mode"
        )

        # Input de texto
        txt = st.text_area('✏️ Ingresa el texto para generar el quiz:', height=200)

        if st.button("🚀 Generar Quiz desde Texto", key="button_generar"):
            if txt and text_game_title:
                with st.spinner("🤖 Generando preguntas con IA..."):
                    st.session_state['text_questions'] = asyncio.run(txt_to_quizz(txt))

                    questions = transform(st.session_state['text_questions']) if isinstance(st.session_state['text_questions'][0], dict) else st.session_state['text_questions']
                    game = create_game_from_questions(questions, text_game_title, text_game_subject, "texto_manual", text_selected_mode)
                    st.session_state.games_library.append(game)

                    st.success("✅ ¡Juego creado exitosamente desde texto!")
                    st.balloons()

def show_mis_juegos():
    """Pantalla de mis juegos"""
    st.markdown(create_navigation_header(), unsafe_allow_html=True)

    st.markdown("## 🎮 Mi Biblioteca de Juegos")

    if not st.session_state.games_library:
        st.markdown("""
        <div class="welcome-card">
            <h3>📚 No tienes juegos creados aún</h3>
            <p>¡Crea tu primer juego subiendo un PDF o ingresando texto!</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("📚 Crear Primer Juego"):
            st.session_state.page = "crear_juego"
            st.rerun()
        return

    # Mostrar juegos en grid
    for i, game in enumerate(st.session_state.games_library):
        if i % 2 == 0:
            col1, col2 = st.columns(2)

        with col1 if i % 2 == 0 else col2:
            st.markdown(f"""
            <div style="
                background: white;
                padding: 1.5rem;
                border-radius: 15px;
                margin: 1rem 0;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                border-left: 4px solid #667eea;
            ">
                <h3 style="margin: 0 0 0.5rem 0; color: #333;">{game['title']}</h3>
                <p style="margin: 0.5rem 0; color: #666;">
                    📚 {game['subject']} | 🎯 {game['difficulty']} | ❓ {game['total_questions']} preguntas
                </p>
                <p style="margin: 0.5rem 0; color: #666;">
                    🏆 Mejor puntuación: {game['best_score']} | 🎮 Jugado {game['times_played']} veces
                </p>
                <p style="margin: 0.5rem 0; color: #888; font-size: 0.9rem;">
                    🕒 Creado: {game['created_at']}
                </p>
            </div>
            """, unsafe_allow_html=True)

            # Botones de acción
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                if st.button(f"🎮 Jugar", key=f"play_{game['id']}"):
                    start_game(game)
            with col_b:
                if st.button(f"📝 Práctica", key=f"practice_{game['id']}"):
                    show_practice_mode(game)
            with col_c:
                if st.button(f"📄 PDF", key=f"pdf_{game['id']}"):
                    generate_game_pdf(game)

def show_grupos_estudio():
    """Pantalla de grupos de estudio"""
    st.markdown(create_navigation_header(), unsafe_allow_html=True)

    st.markdown("## 👥 Grupos de Estudio")

    # Grupos destacados
    st.markdown("### 🌟 Grupos Destacados")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(create_study_group_card("Razonamiento Verbal", 80, "📝"), unsafe_allow_html=True)

    with col2:
        st.markdown(create_study_group_card("Razonamiento Matemático", 80, "🔢"), unsafe_allow_html=True)

    with col3:
        st.markdown(create_study_group_card("Matemática", 80, "📐"), unsafe_allow_html=True)

    # Lista de todos los grupos
    st.markdown("### 📋 Todos los Grupos")

    grupos = [
        {"name": "Física", "participants": 50, "icon": "⚛️"},
        {"name": "Química", "participants": 60, "icon": "🧪"},
        {"name": "Historia", "participants": 30, "icon": "🏛️"},
        {"name": "Literatura", "participants": 25, "icon": "📖"},
        {"name": "Biología", "participants": 45, "icon": "🧬"}
    ]

    for i, grupo in enumerate(grupos, 1):
        st.markdown(f"""
        <div style="
            background: white;
            padding: 1rem;
            border-radius: 10px;
            margin: 0.5rem 0;
            display: flex;
            align-items: center;
            justify-content: space-between;
            color: black;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        ">
            <div style="display: flex; align-items: center; gap: 1rem;">
                <div style="
                    width: 30px;
                    height: 30px;
                    border-radius: 50%;
                    background: #667eea;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-weight: bold;
                    color: black;
                ">{i}</div>
                <div style="font-size: 1.5rem;">{grupo['icon']}</div>
                <span style="font-weight: bold;">{grupo['name']}</span>
            </div>
            <div style="
                background: linear-gradient(45px, #4facfe 0%, #00f2fe 100%);
                color: black;
                padding: 0.3rem 0.8rem;
                border-radius: 15px;
                font-size: 0.9rem;
            ">
                👥 {grupo['participants']} Participantes
            </div>
        </div>
        """, unsafe_allow_html=True)

def show_rankings():
    """Pantalla de rankings"""
    st.markdown(create_navigation_header(), unsafe_allow_html=True)

    st.markdown("## 🏆 Rankings y Estadísticas")

    # Resumen de salas (simulado)
    st.markdown("### 📊 Resumen de Salas")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 1.5rem;
            border-radius: 15px;
            color: black;
            text-align: center;
        ">
            <h3 style="margin: 0; color: black;">Reacciones Químicas</h3>
            <h2 style="margin: 0.5rem 0; color: black;">56%</h2>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
            padding: 1.5rem;
            border-radius: 15px;
            color: #333;
            text-align: center;
        ">
            <h3 style="margin: 0;">Tabla Periódica</h3>
            <h2 style="margin: 0.5rem 0;">82%</h2>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div style="
            background: linear-gradient(135px, #a8edea 0%, #fed6e3 100%);
            padding: 1.5rem;
            border-radius: 15px;
            color: #333;
            text-align: center;
        ">
            <h3 style="margin: 0;">Valencias</h3>
            <h2 style="margin: 0.5rem 0;">95%</h2>
        </div>
        """, unsafe_allow_html=True)

    # Ranking global
    st.markdown("### 🌍 Ranking Global")

    # Datos simulados del ranking
    ranking_data = [
        {"name": "Gabriel Steven Machicao Quispe", "points": 1020, "avatar": "G"},
        {"name": "Ana María González", "points": 985, "avatar": "A"},
        {"name": "Carlos Eduardo Pérez", "points": 920, "avatar": "C"},
        {"name": "María José Rodríguez", "points": 890, "avatar": "M"},
        {"name": "Luis Alberto Mendoza", "points": 875, "avatar": "L"}
    ]

    for i, player in enumerate(ranking_data, 1):
        st.markdown(create_ranking_item(i, player["name"], player["points"], player["avatar"]), unsafe_allow_html=True)

def show_configuracion():
    """Pantalla de configuración"""
    st.markdown(create_navigation_header(), unsafe_allow_html=True)

    st.markdown("## ⚙️ Configuración")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 👤 Usuario")

        email = st.text_input("📧 Correo", value="user1@gmail.com")
        password = st.text_input("🔒 Contraseña", type="password", value="............")

        # Mostrar avatar del usuario
        st.markdown("""
        <div style="
            width: 80px;
            height: 80px;
            border-radius: 50%;
            background: #4CAF50;
            display: flex;
            align-items: center;
            justify-content: center;
            color: black;
            font-weight: bold;
            font-size: 2rem;
            margin: 1rem 0;
        ">G</div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("### 📱 Aplicación")

        notifications = st.toggle("🔔 Notificaciones", value=True)
        personalized_ads = st.toggle("📢 Anuncios personalizados", value=True)
        dark_mode = st.toggle("🌙 Modo oscuro", value=False)

        st.markdown("### ⚠️ Zona de Peligro")
        if st.button("🗑️ Desactivar Cuenta", type="secondary"):
            st.warning("Esta acción no se puede deshacer. ¿Estás seguro?")

    # Botones de acción
    col1, col2 = st.columns(2)
    with col1:
        if st.button("↩️ Retroceder"):
            st.session_state.page = "inicio"
            st.rerun()
    with col2:
        if st.button("💾 Guardar Cambios", type="primary"):
            st.success("✅ Configuración guardada exitosamente")

def show_novedades():
    """Pantalla de novedades"""
    st.markdown(create_navigation_header(), unsafe_allow_html=True)

    st.markdown("## 📢 Novedades")

    # Material universitario
    st.markdown("### 📚 Material Universitario")
    st.markdown("""
    <div style="
        background: black;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border-left: 4px solid #4CAF50;
    ">
        <p>Hola amigos, hoy les traemos materiales extras que contiene los siguientes:
        formularios, exámenes de admisión, banco de preguntas, ...</p>
    </div>
    """, unsafe_allow_html=True)

    # Videos informativos
    st.markdown("### 🎥 Videos Informativos")
    st.markdown("""
    <div style="
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border-left: 4px solid #2196F3;
        color: black;
    ">
        <p>Nuevos tutoriales sobre cómo aprovechar al máximo las funcionalidades de EduPlay.
        Aprende tips y trucos para mejorar tu experiencia de estudio.</p>
    </div>
    """, unsafe_allow_html=True)

    # Futuras actualizaciones
    st.markdown("### 🚀 Futuras Actualizaciones")
    st.markdown("""
    <div style="
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border-left: 4px solid #FF9800;
        color: black;
    ">
        <p>Próximamente: Modo multijugador en tiempo real, nuevos tipos de juegos,
        integración con redes sociales y mucho más. ¡Mantente atento!</p>
    </div>
    """, unsafe_allow_html=True)

def show_puntajes():
    """Pantalla de puntajes detallados"""
    st.markdown(create_navigation_header(), unsafe_allow_html=True)

    st.markdown("## 📊 Resumen de Puntajes")

    # Resumen de puntajes obtenidos
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 1.5rem;
            border-radius: 15px;
            color: black;
            text-align: center;
        ">
            <h3 style="margin: 0; color: black;">Crucigrama</h3>
            <p style="margin: 0.5rem 0; color: black;">Tiempo: 8 min.</p>
            <h2 style="margin: 0.5rem 0; color: black;">92%</h2>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
            padding: 1.5rem;
            border-radius: 15px;
            color: #333;
            text-align: center;
        ">
            <h3 style="margin: 0;">Quiz</h3>
            <h2 style="margin: 0.5rem 0;">82%</h2>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #96fbc4 0%, #f9f586 100%);
            padding: 1.5rem;
            border-radius: 15px;
            color: #333;
            text-align: center;
        ">
            <h3 style="margin: 0;">Juego del Ahorcado</h3>
            <h2 style="margin: 0.5rem 0;">100%</h2>
        </div>
        """, unsafe_allow_html=True)

    # Detalles de los juegos
    st.markdown("### 📋 Detalles")

    games_detail = [
        {"icon": "🧩", "name": "Crucigrama", "detail": "Tiempo: 8 min"},
        {"icon": "❓", "name": "Quiz", "detail": "Correctas: 8/10"},
        {"icon": "🎯", "name": "Juego del Ahorcado", "detail": "Errores: 4"}
    ]

    for game in games_detail:
        st.markdown(f"""
        <div style="
            background: #f5f5f5;
            padding: 1rem;
            border-radius: 10px;
            margin: 0.5rem 0;
            display: flex;
            align-items: center;
            gap: 1rem;
            color: black;
        ">
            <div style="font-size: 1.5rem;">{game['icon']}</div>
            <div>
                <strong>{game['name']}</strong>
                <p style="margin: 0; color: #666; font-size: 0.9rem;">{game['detail']}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

def start_game(game):
    """Inicia un juego en modo gamificado"""
    st.session_state.current_game = game
    st.session_state.current_question_index = 0
    st.session_state.game_score = 0
    st.session_state.current_game_answers = []
    st.session_state.game_state = 'playing'
    st.session_state.game_start_time = time.time()
    st.rerun()

def show_game_interface():
    """Interfaz del juego en curso"""
    game = st.session_state.current_game
    question_index = st.session_state.current_question_index
    questions = game['questions']

    if question_index >= len(questions):
        st.session_state.game_state = 'results'
        st.rerun()
        return

    question = questions[question_index]

    # Header del juego con estilo espacial
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 2rem;
        border-radius: 20px;
        color: black;
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
    ">
        <div style="
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><circle cx="20" cy="20" r="1" fill="white" opacity="0.3"/><circle cx="80" cy="40" r="0.5" fill="white" opacity="0.5"/><circle cx="40" cy="80" r="1.5" fill="white" opacity="0.2"/></svg>');
        "></div>
        <div style="position: relative; z-index: 1;">
            <h2 style="margin: 0; color: black;">🎮 {game['title']}</h2>
            <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 1rem;">
                <span>Pregunta {question_index + 1} de {len(questions)}</span>
                <span>Puntuación: {st.session_state.game_score}</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Barra de progreso
    progress = (question_index) / len(questions)
    st.progress(progress)

    # Interfaz de pregunta con estilo similar al PDF
    st.markdown(f"""
    <div class="question-interface">
        <h3 style="color: #1e3c72; margin-bottom: 2rem; font-size: 1.4rem;">
            {question.get("question", "")}
        </h3>
    </div>
    """, unsafe_allow_html=True)

    # Opciones de respuesta con estilo mejorado
    choices = ['A', 'B', 'C', 'D']
    selected_answer = None

    for choice in choices:
        option_text = question.get(choice, 'Opción no disponible')
        if st.button(
            f"{choice}) {option_text}",
            key=f"option_{choice}_{question_index}",
            use_container_width=True
        ):
            selected_answer = choice
            result = process_answer(question, selected_answer)
            if result == 'answered':
                time.sleep(2)  # Dar tiempo para leer el resultado
                st.session_state.current_question_index += 1
                st.rerun()

    # Botones de control
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⏭️ Saltar", type="secondary"):
            st.session_state.current_question_index += 1
            st.rerun()

    with col2:
        if st.button("🚪 Salir del Juego", type="secondary"):
            st.session_state.game_state = 'menu'
            st.session_state.page = "inicio"
            st.rerun()

def process_answer(question, selected_answer):
    """Procesa la respuesta en modo juego"""
    correct_answer = question.get("reponse")
    is_correct = selected_answer == correct_answer

    # Guardar respuesta
    answer_data = {
        'question': question.get("question"),
        'selected': selected_answer,
        'correct': correct_answer,
        'is_correct': is_correct,
        'explanation': question.get('explanation', '')
    }

    if 'current_game_answers' not in st.session_state:
        st.session_state.current_game_answers = []

    st.session_state.current_game_answers.append(answer_data)

    # Mostrar resultado
    if is_correct:
        points = 10
        st.session_state.game_score += points
        st.success(f"🎉 ¡Correcto! +{points} puntos")
    else:
        st.error(f"❌ Incorrecto. La respuesta correcta es {correct_answer}")

    # Mostrar explicación si existe
    if question.get('explanation'):
        st.info(f"💡 {question.get('explanation')}")

    return 'answered'

def show_game_results():
    """Pantalla de resultados del juego"""
    game = st.session_state.current_game
    answers = st.session_state.current_game_answers

    correct_count = sum(1 for a in answers if a['is_correct'])
    total_questions = len(answers)
    accuracy = (correct_count / total_questions) * 100 if total_questions > 0 else 0
    final_points = st.session_state.game_score

    # Calcular tiempo total
    if st.session_state.game_start_time:
        total_time = time.time() - st.session_state.game_start_time
        time_str = f"{int(total_time // 60)}:{int(total_time % 60):02d}"
    else:
        time_str = "N/A"

    # Pantalla de resultados estilo celebración
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem;
        border-radius: 20px;
        color: black;
        text-align: center;
        margin: 2rem 0;
        position: relative;
        overflow: hidden;
    ">
        <div style="font-size: 4rem; margin-bottom: 1rem;">🏆</div>
        <h1 style="margin: 0; color: black;">¡Juego Completado!</h1>
        <h2 style="margin: 1rem 0; color: black;">{final_points} puntos</h2>
        <p style="margin: 0; opacity: 0.9;">Respondiste correctamente {correct_count} de {total_questions} preguntas</p>
    </div>
    """, unsafe_allow_html=True)

    # Estadísticas detalladas
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        <div style="
            background: white;
            padding: 1.5rem;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        ">
            <div style="font-size: 2rem; color: #4CAF50;">⭐</div>
            <h3 style="color: #4CAF50;">Precisión</h3>
            <h2 style="color: #333;">{accuracy:.1f}%</h2>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div style="
            background: white;
            padding: 1.5rem;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        ">
            <div style="font-size: 2rem; color: #FF9800;">⚡</div>
            <h3 style="color: #FF9800;">Puntos Ganados</h3>
            <h2 style="color: #333;">+{final_points}</h2>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        level_up = calculate_level_from_points(st.session_state.user_data['points'] + final_points) > calculate_level_from_points(st.session_state.user_data['points'])
        st.markdown(f"""
        <div style="
            background: white;
            padding: 1.5rem;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        ">
            <div style="font-size: 2rem; color: #9C27B0;">🎖️</div>
            <h3 style="color: #9C27B0;">Nuevo Nivel</h3>
            <h2 style="color: #333;">{calculate_level_from_points(st.session_state.user_data['points'] + final_points)}</h2>
        </div>
        """, unsafe_allow_html=True)

    # Mostrar nivel up si corresponde
    if level_up:
        st.balloons()
        st.success("🎉 ¡Felicidades! ¡Has subido de nivel!")

    # Actualizar estadísticas del usuario
    user_data = st.session_state.user_data
    user_data['points'] += final_points
    user_data['total_games'] += 1
    user_data['correct_answers'] += correct_count
    user_data['total_questions'] += total_questions
    user_data['level'] = calculate_level_from_points(user_data['points'])

    # Actualizar mejor puntuación del juego
    if final_points > game['best_score']:
        game['best_score'] = final_points
        st.success("🎉 ¡Nuevo récord personal!")

    game['times_played'] += 1

    # Guardar progreso
    save_user_progress(user_data)

    # Botones de acción
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🔄 Jugar de Nuevo"):
            start_game(game)

    with col2:
        if st.button("🏠 Volver al Inicio"):
            st.session_state.game_state = 'menu'
            st.session_state.page = "inicio"
            st.rerun()

    with col3:
        if st.button("🎮 Otros Juegos"):
            st.session_state.game_state = 'menu'
            st.session_state.page = "mis_juegos"
            st.rerun()

def show_practice_mode(game):
    """Modo práctica usando interfaz mejorada"""
    st.markdown(create_navigation_header(), unsafe_allow_html=True)

    st.markdown(f"## 📝 Modo Práctica: {game['title']}")

    questions = game['questions']

    # Mostrar todas las preguntas en modo práctica
    for i, question in enumerate(questions):
        st.markdown(f"""
        <div class="question-interface">
            <h4 style="color: #1e3c72;">Pregunta {i + 1}</h4>
            <h3 style="color: #333; margin-bottom: 1rem;">{question.get('question', '')}</h3>
        </div>
        """, unsafe_allow_html=True)

        # Opciones de respuesta
        choices = ['A', 'B', 'C', 'D']
        selected = st.selectbox(
            "Selecciona tu respuesta:",
            choices,
            format_func=lambda x: f"{x}. {question.get(x, 'None')}",
            key=f"practice_select_{i}"
        )

        if st.button("Verificar", key=f"practice_submit_{i}"):
            correct_answer = question.get("reponse")
            if selected == correct_answer:
                st.success(f'✅ ¡Correcto! La respuesta es {correct_answer}')
            else:
                st.error(f'❌ Incorrecto. La respuesta correcta es {correct_answer}')

            # Mostrar explicación si existe
            if question.get('explanation'):
                st.info(f"💡 {question.get('explanation')}")

        st.markdown("---")

    if st.button("↩️ Volver a Mis Juegos"):
        st.session_state.page = "mis_juegos"
        st.rerun()

def generate_game_pdf(game):
    """Genera PDF del juego"""
    with st.spinner("📄 Generando PDF del quiz..."):
        try:
            # Crear archivo JSON temporal
            json_filename = f"data/quiz-{game['filename']}.json"
            with open(json_filename, "w", encoding='latin-1', errors='ignore') as f:
                json_data = json.dumps(game['questions'])
                f.write(json_data)

            # Generar PDF usando función original
            generate_pdf_quiz(json_filename, game['questions'])

            st.success("📄 ¡PDF generado exitosamente!")

        except Exception as e:
            st.error(f"Error generando PDF: {e}")

def main():
    """Función principal de la aplicación"""

    # Aplicar tema personalizado
    apply_login_theme()

    # Configurar página
    

    # Verificar contraseña PRIMERO
    if not check_password():
        return  # Si no está autenticado, salir de la función

    # Solo ejecutar el resto si está autenticado
    init_session_state()
    ensure_data_directory()

    # Inicializar página si no existe
    if 'page' not in st.session_state:
        st.session_state.page = "inicio"

    # Navegación principal
    if st.session_state.game_state == 'playing':
        show_game_interface()
    elif st.session_state.game_state == 'results':
        show_game_results()
    elif st.session_state.page == "inicio":
        show_welcome_screen()
    elif st.session_state.page == "crear_juego":
        show_crear_juego()
    elif st.session_state.page == "mis_juegos":
        show_mis_juegos()
    elif st.session_state.page == "grupos_estudio":
        show_grupos_estudio()
    elif st.session_state.page == "rankings":
        show_rankings()
    elif st.session_state.page == "configuracion":
        show_configuracion()
    elif st.session_state.page == "novedades":
        show_novedades()
    elif st.session_state.page == "puntajes":
        show_puntajes()

    # Sidebar con navegación rápida (solo si está autenticado)
    with st.sidebar:
        st.markdown("## 🎯 Navegación Rápida")

        user_data = st.session_state.user_data

        # Mostrar progreso del usuario en sidebar
        st.markdown(create_level_badge(user_data['level']), unsafe_allow_html=True)
        st.markdown(create_points_badge(user_data['points']), unsafe_allow_html=True)

        if user_data['total_questions'] > 0:
            accuracy = (user_data['correct_answers'] / user_data['total_questions']) * 100
            st.metric("🎯 Precisión Global", f"{accuracy:.1f}%")

        st.metric("🎮 Juegos Completados", user_data['total_games'])

        st.markdown("---")

        # Navegación rápida
        pages = {
            "🏠 Inicio": "inicio",
            "📚 Crear Juego": "crear_juego",
            "🎮 Mis Juegos": "mis_juegos",
            "👥 Grupos de Estudio": "grupos_estudio",
            "🏆 Rankings": "rankings",
            "📊 Puntajes": "puntajes",
            "⚙️ Configuración": "configuracion",
            "📢 Novedades": "novedades"
        }

        for label, page_key in pages.items():
            if st.button(label, use_container_width=True, key=f"nav_{page_key}"):
                st.session_state.page = page_key
                st.session_state.game_state = 'menu'
                st.rerun()

        # Mostrar botón de cerrar sesión
        show_logout_button()

if __name__ == "__main__":
    main()
