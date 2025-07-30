"""
Páginas individuales de la aplicación EduPlay
"""
import streamlit as st
import asyncio
import json
from datetime import datetime

from nuevo.ui_components import *
from ui_config import COLORS, MODERN_STYLES
from ui_utils import db_manager, transform, clean_questions

def show_login_page():
    """Página de login moderna"""
    st.markdown("""
    <div style="
        display: flex;
        min-height: 100vh;
        align-items: center;
        justify-content: center;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    ">
        <div style="
            background: white;
            border-radius: 20px;
            padding: 3rem;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
            width: 100%;
            max-width: 400px;
        ">
            <div style="text-align: center; margin-bottom: 2rem;">
                <div style="
                    width: 80px;
                    height: 80px;
                    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
                    border-radius: 20px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    margin: 0 auto 1.5rem auto;
                    font-size: 2.5rem;
                    color: white;
                ">🎮</div>
                <h1 style="color: #1f2937; margin: 0;">EduPlay</h1>
                <p style="color: #6b7280; margin-top: 0.5rem;">
                    Transforma tu aprendizaje en diversión
                </p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Formulario de login centrado
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        with st.form("login_form"):
            username = st.text_input(
                "Usuario",
                placeholder="Ingresa tu usuario",
                help="Usa 'estudiante_demo' o 'profesor_demo' para acceder"
            )
            password = st.text_input(
                "Contraseña",
                type="password",
                placeholder="Ingresa tu contraseña",
                help="Usa 'demo123' para acceder"
            )

            col_a, col_b = st.columns(2)

            with col_a:
                student_login = st.form_submit_button(
                    "🎓 Estudiante",
                    use_container_width=True
                )

            with col_b:
                teacher_login = st.form_submit_button(
                    "👨‍🏫 Profesor",
                    use_container_width=True
                )

            if student_login:
                login_user("estudiante_demo", "demo123", "student")
            elif teacher_login:
                login_user("profesor_demo", "demo123", "teacher")

def login_user(username, password, user_type):
    """Procesa el login del usuario"""
    user = db_manager.authenticate_user(username, password)

    if user:
        st.session_state.user_logged_in = True
        st.session_state.user_data = user
        st.session_state.page = 'home'
        st.rerun()
    else:
        # Para demo, crear usuario si no existe
        if username in ["estudiante_demo", "profesor_demo"]:
            st.session_state.user_logged_in = True
            st.session_state.user_data = {
                'id': 1,
                'username': username,
                'first_name': 'Demo',
                'last_name': 'Usuario',
                'user_type': user_type,
                'level': 3,
                'points': 250
            }
            st.session_state.page = 'home'
            st.rerun()
        else:
            show_error_message("Usuario o contraseña incorrectos")

def show_home_page():
    """Página principal con dashboard"""
    user = st.session_state.user_data

    # Header con estadísticas
    st.markdown(create_section_header(
        f"¡Bienvenido, {user['first_name']}!",
        "Aquí está tu progreso de aprendizaje"
    ), unsafe_allow_html=True)

    # Estadísticas principales
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(create_stat_card("250", "Puntos Totales", "primary"), unsafe_allow_html=True)

    with col2:
        st.markdown(create_stat_card("3", "Nivel Actual", "success"), unsafe_allow_html=True)

    with col3:
        st.markdown(create_stat_card("12", "Juegos Completados", "info"), unsafe_allow_html=True)

    with col4:
        st.markdown(create_stat_card("85%", "Precisión Promedio", "warning"), unsafe_allow_html=True)

    # Progreso por materia
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(create_section_header("Tu Progreso por Materia"), unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(create_progress_bar(75, "Matemáticas"), unsafe_allow_html=True)
        st.markdown(create_progress_bar(60, "Historia"), unsafe_allow_html=True)
        st.markdown(create_progress_bar(90, "Ciencias"), unsafe_allow_html=True)

    with col2:
        st.markdown(create_progress_bar(45, "Lenguaje"), unsafe_allow_html=True)
        st.markdown(create_progress_bar(80, "Geografía"), unsafe_allow_html=True)
        st.markdown(create_progress_bar(70, "Inglés"), unsafe_allow_html=True)

    # Acciones rápidas
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(create_section_header("Acciones Rápidas"), unsafe_allow_html=True)

    actions_html = '<div class="card-grid">'

    actions = [
        ("📚", "Crear Sala", "Transforma tus PDFs en juegos educativos"),
        ("🎮", "Jugar", "Únete a una sala existente"),
        ("👥", "Grupos", "Estudia con tus compañeros"),
        ("🏆", "Rankings", "Revisa tu posición en la tabla")
    ]

    for icon, title, desc in actions:
        actions_html += create_feature_card(icon, title, desc)

    actions_html += '</div>'

    st.markdown(actions_html, unsafe_allow_html=True)

    # Botones de acción
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("📚 Crear Sala", use_container_width=True):
            st.session_state.page = 'create_room'
            st.rerun()

    with col2:
        if st.button("🎮 Jugar", use_container_width=True):
            st.session_state.page = 'rooms'
            st.rerun()

    with col3:
        if st.button("👥 Grupos", use_container_width=True):
            st.session_state.page = 'groups'
            st.rerun()

    with col4:
        if st.button("🏆 Rankings", use_container_width=True):
            st.session_state.page = 'rankings'
            st.rerun()

def show_create_room_page():
    """Página para crear una nueva sala"""
    st.markdown(create_section_header(
        "Crear Nueva Sala",
        "Transforma tus documentos en experiencias de aprendizaje interactivas"
    ), unsafe_allow_html=True)

    # Indicador de pasos
    current_step = st.session_state.get('creation_step', 1)
    steps = ["Subir Archivo", "Configurar", "Finalizar"]

    st.markdown(create_step_indicator(current_step, steps), unsafe_allow_html=True)

    if current_step == 1:
        show_upload_step()
    elif current_step == 2:
        show_config_step()
    elif current_step == 3:
        show_finalize_step()

def show_upload_step():
    """Paso 1: Subir archivo"""
    st.markdown(create_upload_area(), unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Selecciona tu archivo",
        type=["pdf", "docx", "pptx", "txt"],
        label_visibility="collapsed"
    )

    if uploaded_file:
        st.session_state.uploaded_file = uploaded_file
        show_success_message(f"Archivo '{uploaded_file.name}' cargado correctamente")

    col1, col2, col3 = st.columns([1, 1, 1])

    with col2:
        if st.button("Continuar →", use_container_width=True, disabled=not uploaded_file):
            if uploaded_file:
                st.session_state.creation_step = 2
                st.rerun()

def show_config_step():
    """Paso 2: Configurar sala"""
    col1, col2 = st.columns([2, 1])

    with col1:
        title = st.text_input(
            "Título de la Sala",
            placeholder="Ej: Matemáticas - Ecuaciones Cuadráticas"
        )

        subject = st.selectbox(
            "Materia",
            ["Matemáticas", "Historia", "Ciencias", "Lenguaje", "Geografía", "Inglés"]
        )

        game_mode = st.selectbox(
            "Modo de Juego",
            ["Cuestionario", "Crucigrama", "Ahorcado", "Memoria"]
        )

        difficulty = st.select_slider(
            "Dificultad",
            options=["Fácil", "Medio", "Difícil"]
        )

    with col2:
        st.markdown("""
        <div class="modern-card" style="margin-top: 2rem;">
            <h4 style="color: #1f2937; margin-bottom: 1rem;">Vista Previa</h4>
            <div style="font-size: 3rem; text-align: center; margin-bottom: 1rem;">📚</div>
            <p style="color: #6b7280; font-size: 0.875rem;">
                Los estudiantes podrán jugar con el contenido de tu archivo
            </p>
        </div>
        """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("← Atrás", use_container_width=True):
            st.session_state.creation_step = 1
            st.rerun()

    with col2:
        if st.button("Continuar →", use_container_width=True, disabled=not title):
            if title:
                st.session_state.room_config = {
                    'title': title,
                    'subject': subject,
                    'game_mode': game_mode,
                    'difficulty': difficulty
                }
                st.session_state.creation_step = 3
                st.rerun()

def show_finalize_step():
    """Paso 3: Finalizar y crear sala"""
    config = st.session_state.get('room_config', {})
    file = st.session_state.get('uploaded_file')

    st.markdown("""
    <div class="modern-card" style="max-width: 600px; margin: 0 auto;">
        <h3 style="color: #1f2937; margin-bottom: 1.5rem; text-align: center;">
            Resumen de tu Sala
        </h3>
    """, unsafe_allow_html=True)

    # Resumen
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"""
        <div style="margin-bottom: 1rem;">
            <p style="color: #6b7280; font-size: 0.875rem; margin-bottom: 0.25rem;">Título</p>
            <p style="color: #1f2937; font-weight: 600;">{config.get('title', '')}</p>
        </div>
        <div style="margin-bottom: 1rem;">
            <p style="color: #6b7280; font-size: 0.875rem; margin-bottom: 0.25rem;">Materia</p>
            <p style="color: #1f2937; font-weight: 600;">{config.get('subject', '')}</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div style="margin-bottom: 1rem;">
            <p style="color: #6b7280; font-size: 0.875rem; margin-bottom: 0.25rem;">Modo de Juego</p>
            <p style="color: #1f2937; font-weight: 600;">{config.get('game_mode', '')}</p>
        </div>
        <div style="margin-bottom: 1rem;">
            <p style="color: #6b7280; font-size: 0.875rem; margin-bottom: 0.25rem;">Archivo</p>
            <p style="color: #1f2937; font-weight: 600;">{file.name if file else ''}</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("← Atrás", use_container_width=True):
            st.session_state.creation_step = 2
            st.rerun()

    with col2:
        if st.button("✅ Crear Sala", use_container_width=True, type="primary"):
            create_room()

def create_room():
    """Crea la sala con los datos proporcionados"""
    # Simulación de creación
    with st.spinner("Creando tu sala..."):
        import time
        time.sleep(2)

    # Éxito
    st.balloons()
    show_success_message("¡Sala creada exitosamente!")

    # Resetear estado
    st.session_state.creation_step = 1
    st.session_state.room_config = {}
    st.session_state.uploaded_file = None

    # Ir a salas
    st.session_state.page = 'rooms'
    st.rerun()

def show_rooms_page():
    """Página de salas disponibles"""
    st.markdown(create_section_header(
        "Salas Disponibles",
        "Únete a una sala para comenzar a aprender jugando"
    ), unsafe_allow_html=True)

    # Filtros
    col1, col2, col3, col4 = st.columns([2, 2, 2, 1])

    with col1:
        search = st.text_input("🔍 Buscar", placeholder="Buscar salas...")

    with col2:
        subject_filter = st.selectbox(
            "Materia",
            ["Todas", "Matemáticas", "Historia", "Ciencias", "Lenguaje"]
        )

    with col3:
        difficulty_filter = st.selectbox(
            "Dificultad",
            ["Todas", "Fácil", "Medio", "Difícil"]
        )

    with col4:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔄 Actualizar"):
            st.rerun()

    # Grid de salas
    rooms_html = '<div class="card-grid" style="margin-top: 2rem;">'

    # Salas de ejemplo
    rooms = [
        ("Ecuaciones Cuadráticas", "Matemáticas", "Medio", 45, "🔢"),
        ("Revolución Francesa", "Historia", "Difícil", 32, "📜"),
        ("Sistema Solar", "Ciencias", "Fácil", 67, "🌍"),
        ("Gramática Básica", "Lenguaje", "Fácil", 23, "📝"),
        ("Capitales del Mundo", "Geografía", "Medio", 56, "🗺️"),
        ("Verbos Irregulares", "Inglés", "Medio", 41, "🇬🇧")
    ]

    for title, subject, difficulty, participants, emoji in rooms:
        rooms_html += create_game_card(title, subject, difficulty, participants, emoji)

    rooms_html += '</div>'

    st.markdown(rooms_html, unsafe_allow_html=True)

def show_game_interface():
    """Interfaz del juego"""
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
        st.session_state.score = 0
        st.session_state.answers = []

    # Preguntas de ejemplo
    questions = [
        {
            'question': '¿Cuál es la capital de Francia?',
            'options': ['Londres', 'París', 'Madrid', 'Berlín'],
            'correct': 1
        },
        {
            'question': '¿Cuánto es 2 + 2?',
            'options': ['3', '4', '5', '6'],
            'correct': 1
        }
    ]

    if st.session_state.current_question < len(questions):
        show_question(questions[st.session_state.current_question])
    else:
        show_game_results()

def show_question(question):
    """Muestra una pregunta del juego"""
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 3rem;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 2rem;
    ">
        <h2 style="color: white; margin-bottom: 2rem;">{question['question']}</h2>
        <div style="font-size: 1.5rem;">
            Pregunta {st.session_state.current_question + 1} de 2
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Opciones
    cols = st.columns(2)

    for i, option in enumerate(question['options']):
        with cols[i % 2]:
            if st.button(option, key=f"opt_{i}", use_container_width=True):
                process_answer(i == question['correct'])

def process_answer(is_correct):
    """Procesa la respuesta del usuario"""
    if is_correct:
        st.session_state.score += 10
        show_success_message("¡Correcto! +10 puntos")
    else:
        show_error_message("Incorrecto")

    st.session_state.current_question += 1
    st.rerun()

def show_game_results():
    """Muestra los resultados del juego"""
    st.markdown(f"""
    <div style="text-align: center; padding: 3rem;">
        <div style="font-size: 5rem; margin-bottom: 1rem;">🏆</div>
        <h1 style="color: #1f2937;">¡Juego Completado!</h1>
        <div style="font-size: 3rem; color: #6366f1; margin: 2rem 0;">
            {st.session_state.score} puntos
        </div>
        <p style="color: #6b7280; font-size: 1.125rem;">
            Has respondido correctamente {st.session_state.score // 10} de 2 preguntas
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1, 1])

    with col2:
        if st.button("🎮 Jugar de Nuevo", use_container_width=True):
            st.session_state.current_question = 0
            st.session_state.score = 0
            st.rerun()

        if st.button("🏠 Volver al Inicio", use_container_width=True):
            st.session_state.page = 'home'
            st.rerun()

def show_rankings_page():
    """Página de rankings"""
    st.markdown(create_section_header(
        "Rankings",
        "Los mejores jugadores de EduPlay"
    ), unsafe_allow_html=True)

    # Tabs para diferentes rankings
    tab1, tab2, tab3 = st.tabs(["🏆 Global", "📚 Por Materia", "📅 Semanal"])

    with tab1:
        # Ranking global
        st.markdown("<h3 style='color: #1f2937; margin: 2rem 0;'>Top 10 Global</h3>", unsafe_allow_html=True)

        rankings = [
            ("María García", 2450, 8),
            ("Juan López", 2380, 7),
            ("Ana Martínez", 2290, 7),
            ("Carlos Ruiz", 2150, 6),
            ("Laura Díaz", 2100, 6),
            ("Demo Usuario", 250, 3)
        ]

        for i, (name, points, level) in enumerate(rankings):
            medal = "🥇" if i == 0 else "🥈" if i == 1 else "🥉" if i == 2 else f"{i+1}."

            st.markdown(f"""
            <div class="modern-card" style="
                display: flex;
                align-items: center;
                gap: 1rem;
                margin-bottom: 1rem;
                {'background: linear-gradient(135deg, #fef3c7 0%, #fbbf24 100%);' if i < 3 else ''}
            ">
                <div style="
                    font-size: 2rem;
                    width: 60px;
                    text-align: center;
                ">{medal}</div>
                <div style="flex: 1;">
                    <div style="font-weight: 600; color: #1f2937;">{name}</div>
                    <div style="display: flex; gap: 1rem; margin-top: 0.25rem;">
                        {create_badge(f"Nivel {level}", "info")}
                        {create_badge(f"{points} pts", "success")}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

def show_groups_page():
    """Página de grupos de estudio"""
    st.markdown(create_section_header(
        "Grupos de Estudio",
        "Aprende junto a otros estudiantes"
    ), unsafe_allow_html=True)

    # Grupos destacados
    st.markdown("<h3 style='color: #1f2937; margin: 2rem 0;'>Grupos Destacados</h3>", unsafe_allow_html=True)

    groups_html = '<div class="card-grid">'

    groups = [
        ("Matemáticas Avanzadas", "Cálculo y Álgebra", 156, "🔢"),
        ("Historia Universal", "Todas las épocas", 89, "📜"),
        ("Ciencias Naturales", "Física, Química y Biología", 234, "🔬"),
        ("Literatura", "Análisis y comprensión", 67, "📚")
    ]

    for name, desc, members, emoji in groups:
        groups_html += f"""
        <div class="feature-card">
            <div class="feature-icon">{emoji}</div>
            <div class="feature-title">{name}</div>
            <div class="feature-description">{desc}</div>
            <div style="
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-top: 1rem;
            ">
                <span style="color: #6b7280; font-size: 0.875rem;">
                    👥 {members} miembros
                </span>
                <button style="
                    background: #6366f1;
                    color: white;
                    border: none;
                    padding: 0.5rem 1rem;
                    border-radius: 8px;
                    font-size: 0.875rem;
                    cursor: pointer;
                ">Unirse</button>
            </div>
        </div>
        """

    groups_html += '</div>'

    st.markdown(groups_html, unsafe_allow_html=True)
