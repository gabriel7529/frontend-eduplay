"""
Configuración de estilos y temas para EduPlay
"""

# Paleta de colores principal
COLORS = {
    'primary': '#6366f1',        # Indigo principal
    'primary_dark': '#4f46e5',   # Indigo oscuro
    'primary_light': '#818cf8',  # Indigo claro
    'secondary': '#8b5cf6',      # Violeta
    'accent': '#fbbf24',         # Amarillo dorado
    'success': '#10b981',        # Verde
    'error': '#ef4444',          # Rojo
    'warning': '#f59e0b',        # Naranja
    'info': '#3b82f6',          # Azul

    # Escala de grises
    'dark': '#1f2937',          # Texto principal
    'gray_dark': '#374151',     # Texto secundario
    'gray': '#6b7280',          # Texto deshabilitado
    'gray_light': '#d1d5db',    # Bordes
    'light': '#f3f4f6',         # Fondos secundarios
    'white': '#ffffff',         # Fondo principal

    # Fondos de cards
    'card_bg': '#ffffff',
    'card_hover': '#f9fafb',
    'card_border': '#e5e7eb'
}

# Estilos CSS modernos
MODERN_STYLES = """
<style>
    /* Reset y configuración base */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }

    .main {
        background-color: #f9fafb;
        min-height: 100vh;
    }

    .main .block-container {
        padding: 0 !important;
        max-width: 100% !important;
    }

    /* Tipografía */
    body {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
        color: #1f2937;
        line-height: 1.6;
    }

    h1, h2, h3, h4, h5, h6 {
        color: #111827;
        font-weight: 600;
        line-height: 1.2;
    }

    /* Header moderno */
    .modern-header {
        background: white;
        border-bottom: 1px solid #e5e7eb;
        padding: 1rem 2rem;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
        position: sticky;
        top: 0;
        z-index: 100;
    }

    .header-content {
        max-width: 1280px;
        margin: 0 auto;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .logo-section {
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }

    .logo-icon {
        width: 40px;
        height: 40px;
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 1.5rem;
        font-weight: bold;
    }

    .logo-text {
        font-size: 1.5rem;
        font-weight: 700;
        color: #1f2937;
    }

    /* Cards modernas */
    .modern-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        border: 1px solid #e5e7eb;
        transition: all 0.3s ease;
    }

    .modern-card:hover {
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.08);
        transform: translateY(-2px);
    }

    /* Botones modernos */
    .btn-primary {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 10px;
        font-weight: 600;
        font-size: 1rem;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(99, 102, 241, 0.2);
    }

    .btn-primary:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 12px rgba(99, 102, 241, 0.3);
    }

    .btn-secondary {
        background: white;
        color: #6366f1;
        border: 2px solid #e5e7eb;
        padding: 0.75rem 1.5rem;
        border-radius: 10px;
        font-weight: 600;
        font-size: 1rem;
        cursor: pointer;
        transition: all 0.3s ease;
    }

    .btn-secondary:hover {
        background: #f9fafb;
        border-color: #6366f1;
    }

    /* Input fields */
    .modern-input {
        width: 100%;
        padding: 0.75rem 1rem;
        border: 2px solid #e5e7eb;
        border-radius: 10px;
        font-size: 1rem;
        transition: all 0.3s ease;
        background: white;
        color: #1f2937;
    }

    .modern-input:focus {
        outline: none;
        border-color: #6366f1;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
    }

    /* Navigation tabs */
    .nav-container {
        background: white;
        border-bottom: 1px solid #e5e7eb;
        padding: 0 2rem;
    }

    .nav-tabs {
        display: flex;
        gap: 2rem;
        max-width: 1280px;
        margin: 0 auto;
    }

    .nav-tab {
        padding: 1rem 0;
        color: #6b7280;
        text-decoration: none;
        font-weight: 500;
        border-bottom: 3px solid transparent;
        transition: all 0.3s ease;
        cursor: pointer;
    }

    .nav-tab:hover {
        color: #4b5563;
    }

    .nav-tab.active {
        color: #6366f1;
        border-bottom-color: #6366f1;
    }

    /* Content sections */
    .content-section {
        max-width: 1280px;
        margin: 0 auto;
        padding: 2rem;
    }

    .section-title {
        font-size: 2rem;
        font-weight: 700;
        color: #1f2937;
        margin-bottom: 0.5rem;
    }

    .section-subtitle {
        font-size: 1.125rem;
        color: #6b7280;
        margin-bottom: 2rem;
    }

    /* Grid layouts */
    .card-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
        gap: 1.5rem;
    }

    /* Feature cards */
    .feature-card {
        background: white;
        border-radius: 16px;
        padding: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
        border: 1px solid #f3f4f6;
        transition: all 0.3s ease;
        cursor: pointer;
    }

    .feature-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 24px rgba(0, 0, 0, 0.1);
    }

    .feature-icon {
        width: 60px;
        height: 60px;
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        border-radius: 16px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        margin-bottom: 1rem;
        color: white;
    }

    .feature-title {
        font-size: 1.25rem;
        font-weight: 600;
        color: #1f2937;
        margin-bottom: 0.5rem;
    }

    .feature-description {
        color: #6b7280;
        line-height: 1.6;
    }

    /* Stat cards */
    .stat-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        border: 1px solid #e5e7eb;
    }

    .stat-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: #6366f1;
        margin-bottom: 0.25rem;
    }

    .stat-label {
        color: #6b7280;
        font-size: 0.875rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    /* Progress bars */
    .progress-container {
        background: #f3f4f6;
        border-radius: 999px;
        height: 12px;
        overflow: hidden;
        margin: 1rem 0;
    }

    .progress-bar {
        background: linear-gradient(90deg, #6366f1 0%, #8b5cf6 100%);
        height: 100%;
        border-radius: 999px;
        transition: width 0.5s ease;
    }

    /* User avatar */
    .user-avatar {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        background: #e5e7eb;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 600;
        color: #6b7280;
        border: 2px solid white;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }

    /* Badges */
    .badge {
        display: inline-flex;
        align-items: center;
        padding: 0.25rem 0.75rem;
        border-radius: 999px;
        font-size: 0.875rem;
        font-weight: 500;
    }

    .badge-success {
        background: #d1fae5;
        color: #065f46;
    }

    .badge-warning {
        background: #fed7aa;
        color: #92400e;
    }

    .badge-info {
        background: #dbeafe;
        color: #1e40af;
    }

    /* Animations */
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    .fade-in {
        animation: fadeIn 0.5s ease-out;
    }

    /* Responsive design */
    @media (max-width: 768px) {
        .header-content {
            padding: 0 1rem;
        }

        .nav-tabs {
            overflow-x: auto;
            -webkit-overflow-scrolling: touch;
        }

        .card-grid {
            grid-template-columns: 1fr;
        }

        .content-section {
            padding: 1rem;
        }
    }

    /* Ocultar elementos de Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}

    /* Personalización de elementos Streamlit */
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 10px;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(99, 102, 241, 0.2);
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 12px rgba(99, 102, 241, 0.3);
    }

    .stTextInput > div > div > input {
        border-radius: 10px;
        border: 2px solid #e5e7eb;
        padding: 0.75rem 1rem;
        font-size: 1rem;
        color: #1f2937;
    }

    .stTextInput > div > div > input:focus {
        border-color: #6366f1;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
    }

    .stSelectbox > div > div > div {
        border-radius: 10px;
        border: 2px solid #e5e7eb;
    }
</style>
"""
