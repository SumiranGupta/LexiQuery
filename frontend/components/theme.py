"""
LexiQuery Theme & Styling
Enterprise dual-mode theme system: Dark & Light.
Full coverage of all Streamlit native elements + custom components.
"""

import streamlit as st

DARK_COLORS = {
    "bg_primary": "#0a0e1a",
    "bg_secondary": "#111827",
    "bg_card": "rgba(17, 24, 39, 0.8)",
    "bg_card_css": "rgba(15, 23, 42, 0.6)",
    "bg_card_hover_shadow": "rgba(99, 102, 241, 0.12)",
    "bg_input": "rgba(15, 23, 42, 0.7)",
    "bg_app": "linear-gradient(160deg, #0a0e1a 0%, #0f172a 40%, #1e1b4b 100%)",
    "sidebar_bg": "linear-gradient(180deg, #0f172a 0%, #1e1b4b 100%)",
    "accent_primary": "#6366f1",
    "accent_secondary": "#8b5cf6",
    "accent_gradient": "linear-gradient(135deg, #6366f1, #8b5cf6, #a78bfa)",
    "text_primary": "#f1f5f9",
    "text_secondary": "#94a3b8",
    "text_muted": "#64748b",
    "border": "rgba(99, 102, 241, 0.18)",
    "border_hover": "rgba(99, 102, 241, 0.4)",
    "success": "#10b981",
    "warning": "#f59e0b",
    "error": "#ef4444",
    "info": "#3b82f6",
    "chat_bg": "rgba(15, 23, 42, 0.4)",
    "citation_bg": "rgba(99, 102, 241, 0.08)",
    "citation_border": "rgba(99, 102, 241, 0.2)",
    "success_bg": "rgba(16, 185, 129, 0.15)",
    "success_border": "rgba(16, 185, 129, 0.3)",
    "warning_bg": "rgba(245, 158, 11, 0.15)",
    "warning_border": "rgba(245, 158, 11, 0.3)",
    "error_bg": "rgba(239, 68, 68, 0.15)",
    "error_border": "rgba(239, 68, 68, 0.3)",
    "perf_bg": "rgba(99, 102, 241, 0.06)",
    "scrollbar_track": "#0a0e1a",
    "scrollbar_thumb": "rgba(99, 102, 241, 0.25)",
    "shadow_sm": "0 2px 8px rgba(0,0,0,0.3)",
    "shadow_md": "0 8px 32px rgba(0,0,0,0.3)",
    "chart_grid": "rgba(99,102,241,0.08)",
    "chart_text": "#94a3b8",
    "chart_line": "#6366f1",
    "chart_fill": "rgba(99, 102, 241, 0.1)",
    "chart_pie_text": "white",
    "chart_pie": ["#6366f1", "#8b5cf6", "#a78bfa", "#c4b5fd", "#ddd6fe"],
}

LIGHT_COLORS = {
    "bg_primary": "#f8fafc",
    "bg_secondary": "#ffffff",
    "bg_card": "rgba(255, 255, 255, 0.95)",
    "bg_card_css": "rgba(255, 255, 255, 0.8)",
    "bg_card_hover_shadow": "rgba(99, 102, 241, 0.1)",
    "bg_input": "#f1f5f9",
    "bg_app": "linear-gradient(160deg, #f8fafc 0%, #eef2ff 40%, #e0e7ff 100%)",
    "sidebar_bg": "linear-gradient(180deg, #f8fafc 0%, #eef2ff 100%)",
    "accent_primary": "#4f46e5",
    "accent_secondary": "#6d28d9",
    "accent_gradient": "linear-gradient(135deg, #4f46e5, #7c3aed, #8b5cf6)",
    "text_primary": "#0f172a",
    "text_secondary": "#334155",
    "text_muted": "#64748b",
    "border": "rgba(15, 23, 42, 0.1)",
    "border_hover": "rgba(79, 70, 229, 0.3)",
    "success": "#059669",
    "warning": "#d97706",
    "error": "#dc2626",
    "info": "#2563eb",
    "chat_bg": "rgba(241, 245, 249, 0.7)",
    "citation_bg": "rgba(79, 70, 229, 0.04)",
    "citation_border": "rgba(79, 70, 229, 0.12)",
    "success_bg": "rgba(5, 150, 105, 0.06)",
    "success_border": "rgba(5, 150, 105, 0.18)",
    "warning_bg": "rgba(217, 119, 6, 0.06)",
    "warning_border": "rgba(217, 119, 6, 0.18)",
    "error_bg": "rgba(220, 38, 38, 0.06)",
    "error_border": "rgba(220, 38, 38, 0.18)",
    "perf_bg": "rgba(79, 70, 229, 0.04)",
    "scrollbar_track": "#f1f5f9",
    "scrollbar_thumb": "rgba(79, 70, 229, 0.2)",
    "shadow_sm": "0 1px 3px rgba(0,0,0,0.08), 0 1px 2px rgba(0,0,0,0.06)",
    "shadow_md": "0 4px 16px rgba(0,0,0,0.08), 0 2px 8px rgba(0,0,0,0.04)",
    "chart_grid": "rgba(15,23,42,0.06)",
    "chart_text": "#334155",
    "chart_line": "#4f46e5",
    "chart_fill": "rgba(79, 70, 229, 0.08)",
    "chart_pie_text": "#1e293b",
    "chart_pie": ["#4f46e5", "#7c3aed", "#8b5cf6", "#a78bfa", "#c4b5fd"],
}


def get_colors() -> dict:
    """Return the active color palette based on current theme mode."""
    if "theme_mode" not in st.session_state:
        st.session_state.theme_mode = "dark"
    return DARK_COLORS if st.session_state.theme_mode == "dark" else LIGHT_COLORS


# Module-level COLORS dict — updated in-place by apply_theme() so all
# importers see the current palette without needing to re-import.
COLORS = dict(DARK_COLORS)


def apply_theme():
    """Inject the themed CSS into the Streamlit app and update COLORS in-place."""
    active = get_colors()
    COLORS.update(active)
    st.markdown(_build_css(COLORS), unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════
# CSS BUILDER
# ═══════════════════════════════════════════════════════════════════

def _build_css(C: dict) -> str:
    return f"""<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    /* ═══════════════════════════════════════════════════════════════
       GLOBAL FOUNDATIONS
       ═══════════════════════════════════════════════════════════════ */
    html, body, .stApp {{
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }}
    .stApp {{
        background: {C["bg_app"]} !important;
        color: {C["text_primary"]} !important;
    }}

    /* Hide Streamlit chrome */
    #MainMenu {{visibility: hidden;}}
    header {{visibility: visible;}}
    header [data-testid="stDecoration"] {{display: none;}}
    footer {{visibility: hidden;}}
    .stDeployButton {{display: none;}}

    /* ═══════════════════════════════════════════════════════════════
       SIDEBAR — FULL THEME COVERAGE
       ═══════════════════════════════════════════════════════════════ */
    section[data-testid="stSidebar"] {{
        background: {C["sidebar_bg"]} !important;
        border-right: 1px solid {C["border"]} !important;
    }}
    section[data-testid="stSidebar"] > div {{
        background: transparent !important;
    }}
    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] .stMarkdown li,
    section[data-testid="stSidebar"] .stMarkdown span {{
        color: {C["text_secondary"]} !important;
    }}
    section[data-testid="stSidebar"] strong {{
        color: {C["text_primary"]} !important;
    }}

    /* Sidebar nav buttons — outlined style, gradient on hover */
    section[data-testid="stSidebar"] .stButton > button {{
        background: transparent !important;
        border: 1px solid {C["border"]} !important;
        color: {C["text_secondary"]} !important;
        border-radius: 10px !important;
        font-weight: 500 !important;
        transition: all 0.2s ease !important;
        text-align: left !important;
        padding: 8px 16px !important;
        box-shadow: none !important;
    }}
    section[data-testid="stSidebar"] .stButton > button:hover {{
        background: {C["accent_gradient"]} !important;
        color: white !important;
        border-color: transparent !important;
        transform: none !important;
        box-shadow: {C["shadow_sm"]} !important;
    }}

    /* ═══════════════════════════════════════════════════════════════
       GLASSMORPHISM CARDS
       ═══════════════════════════════════════════════════════════════ */
    .glass-card {{
        background: {C["bg_card_css"]} !important;
        backdrop-filter: blur(24px);
        -webkit-backdrop-filter: blur(24px);
        border: 1px solid {C["border"]};
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 16px;
        box-shadow: {C["shadow_sm"]};
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }}
    .glass-card:hover {{
        border-color: {C["border_hover"]};
        box-shadow: {C["shadow_md"]};
    }}

    /* ═══════════════════════════════════════════════════════════════
       METRIC CARDS
       ═══════════════════════════════════════════════════════════════ */
    .metric-card {{
        background: {C["bg_card_css"]} !important;
        backdrop-filter: blur(24px);
        border: 1px solid {C["border"]};
        border-radius: 16px;
        padding: 24px;
        text-align: center;
        box-shadow: {C["shadow_sm"]};
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }}
    .metric-card:hover {{
        transform: translateY(-3px);
        box-shadow: {C["shadow_md"]};
        border-color: {C["border_hover"]};
    }}
    .metric-value {{
        font-size: 2.2rem;
        font-weight: 800;
        background: {C["accent_gradient"]};
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 6px 0;
        line-height: 1.2;
    }}
    .metric-label {{
        font-size: 0.8rem;
        color: {C["text_muted"]} !important;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.8px;
    }}
    .metric-icon {{
        font-size: 1.6rem;
        margin-bottom: 4px;
    }}

    /* ═══════════════════════════════════════════════════════════════
       PAGE HEADERS
       ═══════════════════════════════════════════════════════════════ */
    .page-header {{
        background: {C["accent_gradient"]};
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2rem;
        font-weight: 800;
        margin-bottom: 4px;
        letter-spacing: -0.5px;
    }}
    .page-subtitle {{
        color: {C["text_muted"]} !important;
        font-size: 0.95rem;
        margin-bottom: 28px;
        font-weight: 400;
    }}

    /* ═══════════════════════════════════════════════════════════════
       STREAMLIT NATIVE — ALL MARKDOWN TEXT
       ═══════════════════════════════════════════════════════════════ */
    .main .stMarkdown, .main .stMarkdown p, .main .stMarkdown li,
    .main .stMarkdown span, .main .stMarkdown h1, .main .stMarkdown h2,
    .main .stMarkdown h3, .main .stMarkdown h4, .main .stMarkdown h5,
    .main .stMarkdown h6, .main .stMarkdown strong, .main .stMarkdown em,
    .main .stMarkdown code {{
        color: {C["text_primary"]} !important;
    }}

    /* ═══════════════════════════════════════════════════════════════
       STREAMLIT METRIC WIDGET
       ═══════════════════════════════════════════════════════════════ */
    [data-testid="stMetric"] {{
        background: {C["bg_card_css"]} !important;
        border: 1px solid {C["border"]} !important;
        border-radius: 14px !important;
        padding: 18px !important;
        box-shadow: {C["shadow_sm"]} !important;
    }}
    [data-testid="stMetricValue"] {{
        color: {C["text_primary"]} !important;
        font-weight: 700 !important;
    }}
    [data-testid="stMetricLabel"] {{
        color: {C["text_muted"]} !important;
    }}
    [data-testid="stMetricDelta"] {{
        color: {C["success"]} !important;
    }}

    /* ═══════════════════════════════════════════════════════════════
       CHAT MESSAGES & INPUT
       ═══════════════════════════════════════════════════════════════ */
    .stChatMessage, [data-testid="stChatMessage"] {{
        background: {C["bg_card_css"]} !important;
        border: 1px solid {C["border"]} !important;
        border-radius: 14px !important;
        padding: 18px !important;
        box-shadow: {C["shadow_sm"]} !important;
    }}
    .stChatMessage p, [data-testid="stChatMessage"] p,
    .stChatMessage span, [data-testid="stChatMessage"] span {{
        color: {C["text_primary"]} !important;
    }}

    [data-testid="stChatInput"] textarea,
    .stChatInput textarea {{
        background: {C["bg_input"]} !important;
        color: {C["text_primary"]} !important;
        border: 1px solid {C["border"]} !important;
        border-radius: 12px !important;
    }}
    [data-testid="stChatInput"] textarea::placeholder {{
        color: {C["text_muted"]} !important;
    }}

    /* ═══════════════════════════════════════════════════════════════
       MAIN AREA BUTTONS (gradient)
       ═══════════════════════════════════════════════════════════════ */
    .main .stButton > button {{
        background: {C["accent_gradient"]} !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 10px 24px !important;
        font-weight: 600 !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.88rem !important;
        box-shadow: {C["shadow_sm"]} !important;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }}
    .main .stButton > button:hover {{
        opacity: 0.92 !important;
        box-shadow: 0 6px 24px rgba(99, 102, 241, 0.35) !important;
        transform: translateY(-1px) !important;
    }}
    .main .stButton > button:active {{
        transform: translateY(0) !important;
    }}

    /* ═══════════════════════════════════════════════════════════════
       TEXT INPUTS & TEXT AREAS
       ═══════════════════════════════════════════════════════════════ */
    .stTextArea textarea, .stTextInput input,
    [data-testid="stTextArea"] textarea,
    [data-testid="stTextInput"] input {{
        background: {C["bg_input"]} !important;
        border: 1px solid {C["border"]} !important;
        border-radius: 12px !important;
        color: {C["text_primary"]} !important;
        font-family: 'Inter', sans-serif !important;
    }}
    .stTextArea textarea:focus, .stTextInput input:focus {{
        border-color: {C["accent_primary"]} !important;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.15) !important;
    }}
    .stTextArea textarea::placeholder, .stTextInput input::placeholder {{
        color: {C["text_muted"]} !important;
    }}

    /* ═══════════════════════════════════════════════════════════════
       LABELS (all widget labels)
       ═══════════════════════════════════════════════════════════════ */
    .stTextInput label, .stTextArea label, .stSelectbox label,
    .stSlider label, .stCheckbox label, .stRadio label,
    .stFileUploader label, .stNumberInput label,
    [data-testid="stWidgetLabel"] {{
        color: {C["text_primary"]} !important;
        font-weight: 500 !important;
    }}

    /* ═══════════════════════════════════════════════════════════════
       FILE UPLOADER
       ═══════════════════════════════════════════════════════════════ */
    .stFileUploader, [data-testid="stFileUploader"] {{
        background: {C["chat_bg"]} !important;
        border: 2px dashed {C["border"]} !important;
        border-radius: 16px !important;
        padding: 20px !important;
    }}
    [data-testid="stFileUploader"] p,
    [data-testid="stFileUploader"] span,
    [data-testid="stFileUploader"] small {{
        color: {C["text_secondary"]} !important;
    }}
    [data-testid="stFileUploader"] button {{
        background: {C["accent_gradient"]} !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
    }}

    /* ═══════════════════════════════════════════════════════════════
       SELECTBOX & MULTISELECT
       ═══════════════════════════════════════════════════════════════ */
    .stSelectbox > div > div,
    [data-testid="stSelectbox"] > div > div,
    .stMultiSelect > div > div {{
        background: {C["bg_input"]} !important;
        border: 1px solid {C["border"]} !important;
        border-radius: 12px !important;
        color: {C["text_primary"]} !important;
    }}
    [data-testid="stSelectbox"] svg {{
        fill: {C["text_secondary"]} !important;
    }}

    /* ═══════════════════════════════════════════════════════════════
       SLIDER
       ═══════════════════════════════════════════════════════════════ */
    .stSlider p, .stSlider span {{
        color: {C["text_secondary"]} !important;
    }}
    .stSlider [data-baseweb="slider"] div[role="slider"] {{
        background: {C["accent_primary"]} !important;
    }}

    /* ═══════════════════════════════════════════════════════════════
       CHECKBOX & RADIO
       ═══════════════════════════════════════════════════════════════ */
    .stCheckbox label span,
    .stRadio label span {{
        color: {C["text_secondary"]} !important;
    }}

    /* ═══════════════════════════════════════════════════════════════
       TABS
       ═══════════════════════════════════════════════════════════════ */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 8px;
        background: transparent !important;
    }}
    .stTabs [data-baseweb="tab"] {{
        background: {C["chat_bg"]} !important;
        border: 1px solid {C["border"]} !important;
        border-radius: 10px !important;
        color: {C["text_secondary"]} !important;
        padding: 8px 20px !important;
    }}
    .stTabs [aria-selected="true"] {{
        background: {C["accent_gradient"]} !important;
        color: white !important;
        border: none !important;
    }}

    /* ═══════════════════════════════════════════════════════════════
       EXPANDER
       ═══════════════════════════════════════════════════════════════ */
    .streamlit-expanderHeader,
    [data-testid="stExpander"] summary {{
        background: {C["chat_bg"]} !important;
        border: 1px solid {C["border"]} !important;
        border-radius: 12px !important;
        color: {C["text_primary"]} !important;
    }}
    [data-testid="stExpander"] details {{
        border: 1px solid {C["border"]} !important;
        border-radius: 12px !important;
        background: {C["bg_card_css"]} !important;
    }}
    [data-testid="stExpander"] summary span {{
        color: {C["text_primary"]} !important;
    }}
    [data-testid="stExpander"] summary svg {{
        fill: {C["text_muted"]} !important;
    }}

    /* ═══════════════════════════════════════════════════════════════
       DATAFRAMES / TABLES
       ═══════════════════════════════════════════════════════════════ */
    .stDataFrame {{
        border: 1px solid {C["border"]} !important;
        border-radius: 12px !important;
        overflow: hidden !important;
    }}

    /* ═══════════════════════════════════════════════════════════════
       PROGRESS BAR
       ═══════════════════════════════════════════════════════════════ */
    .stProgress > div > div {{
        background: {C["accent_gradient"]} !important;
        border-radius: 8px !important;
    }}

    /* ═══════════════════════════════════════════════════════════════
       SPINNER
       ═══════════════════════════════════════════════════════════════ */
    .stSpinner > div {{
        color: {C["text_secondary"]} !important;
    }}

    /* ═══════════════════════════════════════════════════════════════
       ALERTS (success, warning, error, info)
       ═══════════════════════════════════════════════════════════════ */
    .stAlert, [data-testid="stAlert"] {{
        border-radius: 12px !important;
    }}
    [data-testid="stAlert"] p {{
        color: {C["text_primary"]} !important;
    }}

    /* ═══════════════════════════════════════════════════════════════
       CITATION CARDS
       ═══════════════════════════════════════════════════════════════ */
    .citation-card {{
        background: {C["citation_bg"]};
        border: 1px solid {C["citation_border"]};
        border-radius: 10px;
        padding: 12px 16px;
        margin: 6px 0;
        font-size: 0.85rem;
    }}
    .citation-source {{
        color: {C["accent_secondary"]} !important;
        font-weight: 600;
    }}
    .citation-preview {{
        color: {C["text_muted"]} !important;
        font-size: 0.8rem;
        margin-top: 4px;
    }}

    /* ═══════════════════════════════════════════════════════════════
       STATUS BADGES
       ═══════════════════════════════════════════════════════════════ */
    .status-badge {{
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
    }}
    .status-active {{
        background: {C["success_bg"]} !important;
        color: {C["success"]} !important;
        border: 1px solid {C["success_border"]};
    }}
    .status-processing {{
        background: {C["warning_bg"]} !important;
        color: {C["warning"]} !important;
        border: 1px solid {C["warning_border"]};
    }}
    .status-error {{
        background: {C["error_bg"]} !important;
        color: {C["error"]} !important;
        border: 1px solid {C["error_border"]};
    }}

    /* ═══════════════════════════════════════════════════════════════
       BRAND & NAVIGATION
       ═══════════════════════════════════════════════════════════════ */
    .brand-title {{
        font-size: 1.5rem;
        font-weight: 800;
        background: {C["accent_gradient"]} !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        margin-bottom: 2px;
    }}
    .brand-subtitle {{
        font-size: 0.7rem;
        color: {C["text_muted"]} !important;
        -webkit-text-fill-color: {C["text_muted"]} !important;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        font-weight: 500;
    }}
    .styled-divider {{
        height: 1px;
        background: {C["border"]};
        margin: 16px 0;
        border: none;
    }}

    /* ═══════════════════════════════════════════════════════════════
       PERFORMANCE BAR
       ═══════════════════════════════════════════════════════════════ */
    .perf-bar {{
        margin-top: 12px;
        padding: 10px 14px;
        background: {C["perf_bg"]};
        border: 1px solid {C["border"]};
        border-radius: 10px;
        font-size: 0.78rem;
        color: {C["text_muted"]} !important;
        font-weight: 500;
    }}

    /* ═══════════════════════════════════════════════════════════════
       ANIMATIONS
       ═══════════════════════════════════════════════════════════════ */
    @keyframes fadeIn {{
        from {{ opacity: 0; transform: translateY(8px); }}
        to   {{ opacity: 1; transform: translateY(0); }}
    }}
    .fade-in {{ animation: fadeIn 0.4s ease-out; }}

    @keyframes pulse {{
        0%, 100% {{ opacity: 1; }}
        50%      {{ opacity: 0.5; }}
    }}
    .pulse {{ animation: pulse 2s ease-in-out infinite; }}

    /* ═══════════════════════════════════════════════════════════════
       SCROLLBAR
       ═══════════════════════════════════════════════════════════════ */
    ::-webkit-scrollbar {{ width: 6px; height: 6px; }}
    ::-webkit-scrollbar-track {{ background: {C["scrollbar_track"]}; }}
    ::-webkit-scrollbar-thumb {{ background: {C["scrollbar_thumb"]}; border-radius: 3px; }}
    ::-webkit-scrollbar-thumb:hover {{ background: {C["accent_primary"]}; }}

    /* ═══════════════════════════════════════════════════════════════
       DROPDOWN / POPOVER MENUS
       ═══════════════════════════════════════════════════════════════ */
    [data-baseweb="popover"], [data-baseweb="menu"],
    [data-baseweb="select"] [role="listbox"] {{
        background: {C["bg_secondary"]} !important;
        border: 1px solid {C["border"]} !important;
        border-radius: 12px !important;
    }}
    [data-baseweb="menu"] li {{
        color: {C["text_primary"]} !important;
    }}
    [data-baseweb="menu"] li:hover {{
        background: {C["chat_bg"]} !important;
    }}

    /* ═══════════════════════════════════════════════════════════════
       TOOLTIP
       ═══════════════════════════════════════════════════════════════ */
    [data-baseweb="tooltip"] {{
        background: {C["bg_secondary"]} !important;
        color: {C["text_primary"]} !important;
        border: 1px solid {C["border"]} !important;
        border-radius: 8px !important;
    }}
</style>"""
