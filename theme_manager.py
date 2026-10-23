import streamlit as st

THEMES = {
    "Ocean": {
        "light": {
            "primary": "#0078D4",
            "background": "#F4FAFE",
            "secondary": "#E4F2FA",
            "text": "#123248",
            "button_text": "#FFFFFF",
        },
        "dark": {
            "primary": "#42B9F5",
            "background": "#0B1B26",
            "secondary": "#142C3B",
            "text": "#E8F5FC",
            "button_text": "#071923",
        },
    },
    "Forest": {
        "light": {
            "primary": "#2D7A46",
            "background": "#F4FAF4",
            "secondary": "#E6F1E7",
            "text": "#173820",
            "button_text": "#FFFFFF",
        },
        "dark": {
            "primary": "#63C47B",
            "background": "#101D14",
            "secondary": "#1C3021",
            "text": "#E5F3E8",
            "button_text": "#102417",
        },
    },
    "Desert": {
        "light": {
            "primary": "#B76A2D",
            "background": "#FFF8EF",
            "secondary": "#F4E8D7",
            "text": "#432D20",
            "button_text": "#FFFFFF",
        },
        "dark": {
            "primary": "#E89A55",
            "background": "#211810",
            "secondary": "#36271B",
            "text": "#F8EBDD",
            "button_text": "#2A1B10",
        },
    },
}


def apply_theme() -> None:
    """Render shared theme controls and apply their colors across the app."""
    st.session_state.setdefault("color_theme", "Ocean")
    st.session_state.setdefault("dark_mode", False)

    st.sidebar.divider()
    st.sidebar.subheader("🎨 Appearance")
    st.sidebar.selectbox("Color theme", list(THEMES), key="color_theme")
    st.sidebar.toggle("Dark mode", key="dark_mode")

    mode = "dark" if st.session_state.dark_mode else "light"
    palette = THEMES[st.session_state.color_theme][mode]

    st.markdown(
        f"""
        <style>
        :root {{
            color-scheme: {mode};
        }}
        .stApp,
        [data-testid="stAppViewContainer"] {{
            background-color: {palette["background"]} !important;
            color: {palette["text"]} !important;
        }}
        [data-testid="stSidebar"] {{
            background-color: {palette["secondary"]} !important;
        }}
        [data-testid="stHeader"] {{
            background-color: {palette["background"]} !important;
        }}
        .stApp,
        .stApp p,
        .stApp label,
        .stApp h1,
        .stApp h2,
        .stApp h3,
        .stApp h4,
        [data-testid="stSidebar"] {{
            color: {palette["text"]};
        }}
        [data-testid="stWidgetLabel"] p {{
            color: {palette["text"]} !important;
        }}
        .stButton > button,
        .stDownloadButton > button {{
            background-color: {palette["primary"]} !important;
            color: {palette["button_text"]} !important;
            border: 1px solid {palette["primary"]} !important;
            border-radius: 0.6rem;
        }}
        .stButton > button:hover,
        .stDownloadButton > button:hover {{
            filter: brightness(1.12);
            border-color: {palette["primary"]} !important;
        }}
        .stTextInput input,
        .stNumberInput input,
        .stDateInput input,
        .stTextArea textarea,
        [data-baseweb="select"] > div {{
            background-color: {palette["secondary"]} !important;
            color: {palette["text"]} !important;
            border-color: {palette["primary"]} !important;
        }}
        [data-testid="stDataFrame"],
        [data-testid="stTable"] {{
            color: {palette["text"]};
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )
