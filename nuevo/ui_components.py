"""
Componentes UI reutilizables para EduPlay
"""
import streamlit as st
from ui_config import COLORS, MODERN_STYLES

def render_header(user_data=None):
    """Renderiza el header principal de la aplicación"""
    st.markdown("""
    <div class="modern-header">
        <div class="header-content">
            <div class="logo-section">
                <div class="logo-icon">🎮</div>
                <div class="logo-text">EduPlay</div>
            </div>
            {}
        </div>
    </div>
    """.format(
        f"""
        <div style="display: flex; align-items: center; gap: 1.5rem;">
            <span style="color: #6b7280; font-weight: 500;">
                Hola, {user_data['first_name']}
            </span>
            <div class="user-avatar">{user_data['first_name'][0]}</div>
        </div>
        """ if user_data else ""
    ), unsafe_allow_html=True)

def render_navigation(active_tab="Inicio"):
    """Renderiza la barra de navegación"""
    tabs = ["Inicio", "Salas", "Crear Sala", "Historial", "Grupos"]

    nav_html = '<div class="nav-container"><div class="nav-tabs">'

    for tab in tabs:
        active_class = "active" if tab == active_tab else ""
        nav_html += f'<div class="nav-tab {active_class}">{tab}</div>'

    nav_html += '</div></div>'

    st.markdown(nav_html, unsafe_allow_html=True)

def create_feature_card(icon, title, description, action=None):
    """Crea una tarjeta de característica"""
    card_html = f"""
    <div class="feature-card">
        <div class="feature-icon">{icon}</div>
        <div class="feature-title">{title}</div>
        <div class="feature-description">{description}</div>
    </div>
    """

    return card_html

def create_stat_card(value, label, color="primary"):
    """Crea una tarjeta de estadística"""
    return f"""
    <div class="stat-card">
        <div class="stat-value" style="color: {COLORS[color]};">{value}</div>
        <div class="stat-label">{label}</div>
    </div>
    """

def create_progress_bar(percentage, label=""):
    """Crea una barra de progreso"""
    return f"""
    <div style="margin-bottom: 1rem;">
        {f'<div style="font-size: 0.875rem; color: #6b7280; margin-bottom: 0.5rem;">{label}</div>' if label else ''}
        <div class="progress-container">
            <div class="progress-bar" style="width: {percentage}%;"></div>
        </div>
        <div style="text-align: right; font-size: 0.875rem; color: #6b7280; margin-top: 0.25rem;">
            {percentage}%
        </div>
    </div>
    """

def create_badge(text, type="info"):
    """Crea un badge/etiqueta"""
    badge_types = {
        "success": "badge-success",
        "warning": "badge-warning",
        "info": "badge-info"
    }

    return f'<span class="badge {badge_types.get(type, "badge-info")}">{text}</span>'

def create_user_card(name, level, points, avatar_letter):
    """Crea una tarjeta de usuario"""
    return f"""
    <div class="modern-card" style="display: flex; align-items: center; gap: 1rem;">
        <div class="user-avatar" style="width: 60px; height: 60px; font-size: 1.5rem;">
            {avatar_letter}
        </div>
        <div style="flex: 1;">
            <div style="font-weight: 600; color: #1f2937; font-size: 1.125rem;">{name}</div>
            <div style="display: flex; gap: 1rem; margin-top: 0.25rem;">
                {create_badge(f"Nivel {level}", "info")}
                {create_badge(f"{points} pts", "success")}
            </div>
        </div>
    </div>
    """

def create_game_card(title, subject, difficulty, participants, image_emoji="📚"):
    """Crea una tarjeta de juego/sala"""
    difficulty_colors = {
        "Fácil": "success",
        "Medio": "warning",
        "Difícil": "error"
    }

    return f"""
    <div class="modern-card" style="cursor: pointer; transition: all 0.3s ease;">
        <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem;">
            <div style="font-size: 2.5rem;">{image_emoji}</div>
            <div style="flex: 1;">
                <h3 style="margin: 0; font-size: 1.25rem; color: #1f2937;">{title}</h3>
                <p style="margin: 0.25rem 0 0 0; color: #6b7280; font-size: 0.875rem;">{subject}</p>
            </div>
        </div>
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div style="display: flex; gap: 0.5rem;">
                {create_badge(difficulty, difficulty_colors.get(difficulty, "info"))}
            </div>
            <div style="color: #6b7280; font-size: 0.875rem;">
                👥 {participants} participantes
            </div>
        </div>
    </div>
    """

def create_section_header(title, subtitle=""):
    """Crea un encabezado de sección"""
    return f"""
    <div style="margin-bottom: 2rem;">
        <h2 class="section-title">{title}</h2>
        {f'<p class="section-subtitle">{subtitle}</p>' if subtitle else ''}
    </div>
    """

def show_success_message(message):
    """Muestra un mensaje de éxito"""
    st.markdown(f"""
    <div style="
        background: #d1fae5;
        border: 1px solid #a7f3d0;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        display: flex;
        align-items: center;
        gap: 0.75rem;
    ">
        <span style="font-size: 1.5rem;">✅</span>
        <span style="color: #065f46; font-weight: 500;">{message}</span>
    </div>
    """, unsafe_allow_html=True)

def show_error_message(message):
    """Muestra un mensaje de error"""
    st.markdown(f"""
    <div style="
        background: #fee2e2;
        border: 1px solid #fecaca;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        display: flex;
        align-items: center;
        gap: 0.75rem;
    ">
        <span style="font-size: 1.5rem;">❌</span>
        <span style="color: #991b1b; font-weight: 500;">{message}</span>
    </div>
    """, unsafe_allow_html=True)

def create_empty_state(icon, title, description, action_text=None, action_callback=None):
    """Crea un estado vacío con llamada a la acción"""
    empty_html = f"""
    <div style="
        text-align: center;
        padding: 4rem 2rem;
        color: #6b7280;
    ">
        <div style="
            font-size: 4rem;
            margin-bottom: 1rem;
            opacity: 0.5;
        ">{icon}</div>
        <h3 style="
            color: #374151;
            font-size: 1.5rem;
            margin-bottom: 0.5rem;
        ">{title}</h3>
        <p style="
            max-width: 400px;
            margin: 0 auto 2rem auto;
            line-height: 1.6;
        ">{description}</p>
    </div>
    """

    st.markdown(empty_html, unsafe_allow_html=True)

    if action_text and action_callback:
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button(action_text, use_container_width=True):
                action_callback()

def create_upload_area():
    """Crea un área de carga de archivos estilizada"""
    return """
    <div style="
        border: 2px dashed #e5e7eb;
        border-radius: 16px;
        padding: 3rem 2rem;
        text-align: center;
        background: #fafafa;
        transition: all 0.3s ease;
        cursor: pointer;
    " onmouseover="this.style.borderColor='#6366f1'; this.style.background='#f5f3ff';"
       onmouseout="this.style.borderColor='#e5e7eb'; this.style.background='#fafafa';">
        <div style="font-size: 3rem; color: #6366f1; margin-bottom: 1rem;">📄</div>
        <h3 style="color: #374151; margin-bottom: 0.5rem;">Arrastra tu archivo aquí</h3>
        <p style="color: #6b7280; font-size: 0.875rem;">o haz clic para seleccionar</p>
        <p style="color: #9ca3af; font-size: 0.75rem; margin-top: 1rem;">
            Soporta: PDF, DOCX, PPT, TXT (máx. 10MB)
        </p>
    </div>
    """

def create_step_indicator(current_step, steps):
    """Crea un indicador de pasos"""
    html = '<div style="display: flex; align-items: center; justify-content: center; margin: 2rem 0;">'

    for i, step in enumerate(steps, 1):
        # Círculo del paso
        if i < current_step:
            status = "completed"
            bg_color = COLORS['success']
            icon = "✓"
        elif i == current_step:
            status = "active"
            bg_color = COLORS['primary']
            icon = str(i)
        else:
            status = "inactive"
            bg_color = COLORS['gray_light']
            icon = str(i)

        html += f"""
        <div style="
            width: 50px;
            height: 50px;
            border-radius: 50%;
            background: {bg_color};
            color: white;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            font-size: 1.25rem;
        ">{icon}</div>
        """

        # Línea conectora
        if i < len(steps):
            line_color = COLORS['success'] if i < current_step else COLORS['gray_light']
            html += f"""
            <div style="
                width: 100px;
                height: 2px;
                background: {line_color};
                margin: 0 1rem;
            "></div>
            """

    html += '</div>'

    # Labels de los pasos
    html += '<div style="display: flex; justify-content: center; gap: 8rem; margin-top: 0.5rem;">'
    for step in steps:
        html += f'<span style="color: #6b7280; font-size: 0.875rem;">{step}</span>'
    html += '</div>'

    return html
