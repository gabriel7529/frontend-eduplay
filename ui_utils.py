import streamlit as st
import json
import os
from datetime import datetime
import time

def check_password():
    """
    Sistema de autenticación mejorado con interfaz atractiva.
    Retorna True si el usuario tiene la contraseña correcta.
    """

    def get_correct_password():
        """Obtiene la contraseña correcta desde secrets o usa la por defecto."""
        try:
            return st.secrets["password"]
        except:
            return "eduplay2024"  # Contraseña por defecto para desarrollo

    def password_entered():
        """Valida la contraseña ingresada por el usuario."""
        correct_password = get_correct_password()

        if st.session_state["password"] == correct_password:
            st.session_state["password_correct"] = True
            st.session_state["login_time"] = datetime.now()
            # Limpiar contraseña por seguridad
            del st.session_state["password"]
            # Mostrar mensaje de éxito temporal
            st.session_state["show_success"] = True
        else:
            st.session_state["password_correct"] = False
            st.session_state["failed_attempts"] = st.session_state.get("failed_attempts", 0) + 1

    def reset_login():
        """Permite al usuario cerrar sesión."""
        for key in ["password_correct", "login_time", "failed_attempts", "show_success"]:
            if key in st.session_state:
                del st.session_state[key]

    def show_login_form():
        """Muestra el formulario de login con diseño atractivo."""

        # Contenedor principal centrado
        col1, col2, col3 = st.columns([1, 2, 1])

        with col2:
            # Header del login
            st.markdown("""
                <div style='text-align: center; padding: 2rem 0;'>
                    <h1 style='color: #1f77b4; margin-bottom: 0.5rem;'>🎓 EduPlay</h1>
                    <p style='color: #666; font-size: 1.1rem; margin-bottom: 2rem;'>
                        Bienvenido de vuelta
                    </p>
                </div>
            """, unsafe_allow_html=True)

            # Mostrar intentos fallidos si existen
            failed_attempts = st.session_state.get("failed_attempts", 0)
            if failed_attempts > 0:
                if failed_attempts >= 3:
                    st.error(f"🚫 Demasiados intentos fallidos ({failed_attempts}). Por favor, verifica tu contraseña.")
                else:
                    st.warning(f"⚠️ Contraseña incorrecta. Intentos: {failed_attempts}")

            # Campo de contraseña
            st.text_input(
                "🔐 Ingresa tu contraseña",
                type="password",
                on_change=password_entered,
                key="password",
                placeholder="Contraseña...",
                help="Ingresa tu contraseña para acceder a EduPlay"
            )

            # Información de desarrollo (solo si no hay muchos intentos fallidos)
            if failed_attempts < 2:
                with st.expander("💡 Información de desarrollo", expanded=False):
                    st.info("**Contraseña de desarrollo:** `eduplay2024`")
                    st.caption("Esta información solo es visible en modo desarrollo.")

    def show_success_message():
        """Muestra mensaje de bienvenida después del login exitoso."""
        if st.session_state.get("show_success", False):
            st.success("✅ ¡Bienvenido a EduPlay! Acceso concedido correctamente.")
            time.sleep(1)  # Breve pausa para mostrar el mensaje
            st.session_state["show_success"] = False
            st.rerun()

    # Lógica principal
    if "password_correct" not in st.session_state:
        # Primera vez, mostrar formulario de login
        show_login_form()
        return False

    elif not st.session_state["password_correct"]:
        # Contraseña incorrecta, mostrar formulario con error
        show_login_form()
        return False

    else:
        # Contraseña correcta
        show_success_message()
        return True


def apply_login_theme():
    """Aplica estilos CSS personalizados para mejorar la apariencia."""
    st.markdown("""
        <style>
        /* Ocultar elementos de Streamlit por defecto solo en login */
        .login-mode #MainMenu {visibility: hidden;}
        .login-mode footer {visibility: hidden;}
        .login-mode header {visibility: hidden;}

        /* Estilo del contenedor principal */
        .main .block-container {
            padding-top: 2rem;
            max-width: 1200px;
        }

        /* Animaciones suaves */
        .stButton > button {
            transition: all 0.3s ease;
            border-radius: 10px;
        }
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }

        /* Colores personalizados */
        .stSuccess {
            background-color: #d4edda;
            border-color: #c3e6cb;
            color: #155724;
            border-radius: 10px;
        }
        .stError {
            background-color: #f8d7da;
            border-color: #f5c6cb;
            color: #721c24;
            border-radius: 10px;
        }
        .stWarning {
            background-color: #fff3cd;
            border-color: #ffeaa7;
            color: #856404;
            border-radius: 10px;
        }

        /* Estilo para el campo de contraseña */
        .stTextInput > div > div > input {
            background-color: black;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            padding: 12px;
            font-size: 16px;
            transition: all 0.3s ease;
        }
        .stTextInput > div > div > input:focus {
            border-color: #1f77b4;
            box-shadow: 0 0 10px rgba(31,119,180,0.3);
        }
        </style>
    """, unsafe_allow_html=True)


def show_logout_button():
    """Muestra el botón de cerrar sesión en el sidebar."""
    with st.sidebar:
        st.markdown("---")
        st.markdown("### 👤 Sesión")

        # Información de login
        login_time = st.session_state.get("login_time")
        if login_time:
            st.caption(f"✅ Conectado desde: {login_time.strftime('%H:%M:%S')}")

        # Botón de cerrar sesión
        if st.button("🚪 Cerrar Sesión", type="secondary", use_container_width=True):
            # Limpiar datos de sesión relacionados con login
            for key in ["password_correct", "login_time", "failed_attempts", "show_success"]:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()



def transform(input_list):
    """
    Transforma la lista de diccionarios del formato original a formato simplificado
    """
    new_list = []

    # Si input_list ya está en el formato correcto, devolverlo tal como está
    if isinstance(input_list, list) and len(input_list) > 0:
        first_item = input_list[0]
        if isinstance(first_item, dict) and 'question' in first_item:
            return input_list

    # Transformar formato original
    for item in input_list:
        if isinstance(item, dict):
            for key in item:
                if 'question1' in key or 'question2' in key or 'question3' in key:
                    question_dict = {}
                    question_num = key[-1]
                    question_dict['question'] = item[key]
                    question_dict['A'] = item[f'A_{question_num}']
                    question_dict['B'] = item[f'B_{question_num}']
                    question_dict['C'] = item[f'C_{question_num}']
                    question_dict['D'] = item[f'D_{question_num}']
                    question_dict['reponse'] = item[f'reponse{question_num}']

                    # Agregar explicación si existe
                    explanation_key = f'explanation{question_num}'
                    if explanation_key in item:
                        question_dict['explanation'] = item[explanation_key]

                    new_list.append(question_dict)
        else:
            # Si el item ya está en formato correcto, agregarlo directamente
            new_list.append(item)

    return new_list

def create_game_mode_card(icon, title, description, difficulty="Medio", questions=10):
    """Crea una tarjeta para modo de juego"""
    return f"""
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    ">
        <div style="font-size: 2rem; margin-bottom: 0.5rem;">{icon}</div>
        <h3 style="margin: 0.5rem 0; color: white;">{title}</h3>
        <p style="margin: 0.5rem 0; opacity: 0.9;">{description}</p>
        <div style="display: flex; justify-content: space-around; margin-top: 1rem;">
            <span style="font-size: 0.8rem;">🎯 {difficulty}</span>
            <span style="font-size: 0.8rem;">❓ {questions} preguntas</span>
        </div>
    </div>
    """

def create_navigation_header(user_name="GABRIEL", active_page="Inicio"):
    """Crea el header de navegación principal"""
    pages = {
        "Inicio": "🏠",
        "Salas": "🎮",
        "Crear Sala": "➕",
        "Historial de Rankings": "🏆",
        "Grupos de Estudio": "👥",
        "Configuración": "⚙️",
        "Novedades": "📢",
        "Puntajes": "📊"
    }

    nav_html = f"""
    <div style="
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        padding: 1rem 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        color: white;
    ">
        <div style="display: flex; align-items: center;">
            <h2 style="margin: 0; color: white;">🎮 EduPlay</h2>
        </div>
        <div style="display: flex; align-items: center; gap: 2rem;">
            <span style="font-size: 1.1rem;">Bienvenido, {user_name}</span>
            <div style="
                width: 40px;
                height: 40px;
                border-radius: 50%;
                background: #4CAF50;
                display: flex;
                align-items: center;
                justify-content: center;
                font-weight: bold;
            ">{user_name[0]}</div>
        </div>
    </div>
    """
    return nav_html

def create_stats_card(title, value, icon, color="#4CAF50"):
    """Crea una tarjeta de estadísticas"""
    return f"""
    <div style="
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border-left: 4px solid {color};
    ">
        <div style="font-size: 2rem; margin-bottom: 0.5rem;">{icon}</div>
        <h3 style="color: {color}; margin: 0.5rem 0;">{value}</h3>
        <p style="color: #666; margin: 0; font-size: 0.9rem;">{title}</p>
    </div>
    """

def create_progress_bar(current, total, title="Progreso", color="#4CAF50"):
    """Crea una barra de progreso"""
    percentage = (current / total) * 100 if total > 0 else 0
    return f"""
    <div style="margin: 1rem 0;">
        <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
            <span style="font-weight: bold;">{title}</span>
            <span>{current}/{total}</span>
        </div>
        <div style="
            background: #e0e0e0;
            border-radius: 10px;
            height: 8px;
            overflow: hidden;
        ">
            <div style="
                background: {color};
                height: 100%;
                width: {percentage}%;
                border-radius: 10px;
                transition: width 0.3s ease;
            "></div>
        </div>
        <div style="text-align: right; font-size: 0.8rem; color: #666; margin-top: 0.2rem;">
            {percentage:.1f}%
        </div>
    </div>
    """

def create_game_result_card(game_title, score, time_spent, questions_correct, total_questions):
    """Crea una tarjeta de resultado de juego"""
    accuracy = (questions_correct / total_questions) * 100 if total_questions > 0 else 0

    if accuracy >= 90:
        color = "#4CAF50"
        icon = "🏆"
    elif accuracy >= 70:
        color = "#FF9800"
        icon = "🥈"
    else:
        color = "#f44336"
        icon = "🥉"

    return f"""
    <div style="
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border-left: 4px solid {color};
    ">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <h3 style="margin: 0; color: #333;">{icon} {game_title}</h3>
                <p style="margin: 0.5rem 0; color: #666;">
                    📊 {accuracy:.1f}% • ⏱️ {time_spent} • ✅ {questions_correct}/{total_questions}
                </p>
            </div>
            <div style="
                background: {color};
                color: white;
                padding: 0.5rem 1rem;
                border-radius: 20px;
                font-weight: bold;
            ">
                {score} pts
            </div>
        </div>
    </div>
    """

def create_ranking_item(position, name, points, avatar_letter="G"):
    """Crea un item para el ranking"""
    colors = {1: "#FFD700", 2: "#C0C0C0", 3: "#CD7F32"}
    color = colors.get(position, "#e0e0e0")

    return f"""
    <div style="
        background: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        color: black;
    ">
        <div style="display: flex; align-items: center; gap: 1rem;">
            <div style="
                width: 30px;
                height: 30px;
                border-radius: 50%;
                background: {color};
                display: flex;
                align-items: center;
                justify-content: center;
                font-weight: bold;
                color: black;
            ">{position}</div>
            <div style="
                width: 40px;
                height: 40px;
                border-radius: 50%;
                background: #4CAF50;
                display: flex;
                align-items: center;
                justify-content: center;
                color: white;
                font-weight: bold;
            ">{avatar_letter}</div>
            <span style="font-weight: bold;">{name}</span>
        </div>
        <div style="
            background: linear-gradient(45deg, #4facfe 0%, #00f2fe 100%);
            color: white;
            padding: 0.3rem 0.8rem;
            border-radius: 15px;
            font-weight: bold;
        ">
            {points} Puntos
        </div>
    </div>
    """

def create_study_group_card(title, participants, subject_icon="📚"):
    """Crea una tarjeta para grupo de estudio"""
    return f"""
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
        text-align: center;
    ">
        <div style="font-size: 2rem; margin-bottom: 0.5rem;">{subject_icon}</div>
        <h3 style="margin: 0.5rem 0; color: white;">{title}</h3>
        <p style="margin: 0; opacity: 0.9;">👥 {participants} Participantes</p>
    </div>
    """

def save_user_progress(user_data, filename="user_progress.json"):
    """Guarda el progreso del usuario en un archivo JSON"""
    import json
    import os

    try:
        os.makedirs("data", exist_ok=True)
        filepath = os.path.join("data", filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(user_data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        st.error(f"Error al guardar progreso: {e}")
        return False

def load_user_progress(filename="user_progress.json"):
    """Carga el progreso del usuario desde un archivo JSON"""
    import json
    import os

    try:
        filepath = os.path.join("data", filename)
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        st.error(f"Error al cargar progreso: {e}")

    # Retorna datos por defecto si no se puede cargar
    return {
        'level': 1,
        'points': 250,
        'total_games': 3,
        'correct_answers': 18,
        'total_questions': 24,
        'achievements': []
    }

def get_game_mode_options():
    """Retorna las opciones de modo de juego"""
    return [
        {"value": "cuestionario", "label": "📝 Cuestionario", "description": "Preguntas de opción múltiple"},
        {"value": "crucigrama", "label": "🧩 Crucigrama", "description": "Resuelve el crucigrama"},
        {"value": "ahorcado", "label": "🎯 Ahorcado", "description": "Adivina la palabra"},
        {"value": "tarjetas", "label": "🃏 Tarjetas", "description": "Memoriza con tarjetas"},
    ]

def create_notification_card(title, message, type="info"):
    """Crea una tarjeta de notificación"""
    colors = {
        "info": "#2196F3",
        "success": "#4CAF50",
        "warning": "#FF9800",
        "error": "#f44336"
    }

    icons = {
        "info": "ℹ️",
        "success": "✅",
        "warning": "⚠️",
        "error": "❌"
    }

    color = colors.get(type, "#2196F3")
    icon = icons.get(type, "ℹ️")

    return f"""
    <div style="
        background: white;
        border-left: 4px solid {color};
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    ">
        <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;">
            <span style="font-size: 1.2rem;">{icon}</span>
            <strong style="color: {color};">{title}</strong>
        </div>
        <p style="margin: 0; color: #666;">{message}</p>
    </div>
    """

def calculate_level_from_points(points):
    """Calcula el nivel basado en los puntos"""
    return min(10, max(1, points // 100 + 1))

def get_next_level_points(current_points):
    """Calcula los puntos necesarios para el siguiente nivel"""
    current_level = calculate_level_from_points(current_points)
    next_level_points = current_level * 100
    return next_level_points - current_points

def create_level_badge(level):
    """Crea una insignia de nivel"""
    return f"""
    <div style="
        background: linear-gradient(45deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
        margin: 0.2rem;
    ">
        🎖️ Nivel {level}
    </div>
    """

def create_points_badge(points):
    """Crea una insignia de puntos"""
    return f"""
    <div style="
        background: linear-gradient(45deg, #4facfe 0%, #00f2fe 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
        margin: 0.2rem;
    ">
        ⭐ {points} Puntos
    </div>
    """

def validate_question_format(question):
    """Valida que una pregunta tenga el formato correcto"""
    required_fields = ['question', 'A', 'B', 'C', 'D', 'reponse']

    if not isinstance(question, dict):
        return False

    for field in required_fields:
        if field not in question or not question[field]:
            return False

    # Validar que la respuesta sea una opción válida
    if question['reponse'] not in ['A', 'B', 'C', 'D']:
        return False

    return True

def clean_questions(questions):
    """Limpia y valida las preguntas, removiendo las que no tienen formato correcto"""
    cleaned_questions = []

    for question in questions:
        if validate_question_format(question):
            cleaned_questions.append(question)
        else:
            st.warning(f"Pregunta con formato incorrecto removida: {question}")

    return cleaned_questions
