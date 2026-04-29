import streamlit as st

st.set_page_config(
    page_title="ForgeScan",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Clean Professional Dark Theme ───
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    /* ── Base ── */
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    [data-testid="stAppViewContainer"] {
        background: #09090b;
    }
    [data-testid="stHeader"] {
        background: transparent;
    }

    /* ── Sidebar ── */
    section[data-testid="stSidebar"] {
        background: #09090b;
        border-right: 1px solid #1c1c22;
        width: 260px !important;
    }
    section[data-testid="stSidebar"] * {
        color: #a1a1aa !important;
    }
    .sidebar-brand {
        padding: 0.25rem 0 1.75rem 0;
        border-bottom: 1px solid #1c1c22;
        margin-bottom: 1.25rem;
    }
    .sidebar-brand-name {
        font-size: 18px;
        font-weight: 700;
        color: #fafafa !important;
        letter-spacing: -0.03em;
    }
    .sidebar-brand-dot {
        display: inline-block;
        width: 8px;
        height: 8px;
        background: #f97316;
        border-radius: 50%;
        margin-right: 10px;
        position: relative;
        top: -1px;
    }
    .sidebar-version {
        font-size: 11px;
        color: #52525b !important;
        padding: 0 0.25rem;
        margin-top: 0.5rem;
    }

    /* Sidebar radio buttons */
    section[data-testid="stSidebar"] .stRadio > div {
        gap: 2px;
    }
    section[data-testid="stSidebar"] .stRadio > div > label {
        padding: 0.5rem 0.75rem;
        border-radius: 8px;
        transition: background 0.15s;
        font-size: 14px;
        font-weight: 500;
    }
    section[data-testid="stSidebar"] .stRadio > div > label:hover {
        background: #18181b;
    }
    section[data-testid="stSidebar"] .stRadio > div > label[data-checked="true"] {
        background: #18181b;
        color: #fafafa !important;
    }

    /* ── Typography ── */
    .fs-h1 {
        font-size: 30px;
        font-weight: 700;
        color: #fafafa;
        letter-spacing: -0.035em;
        line-height: 1.2;
        margin: 0;
    }
    .fs-sub {
        font-size: 15px;
        color: #71717a;
        margin-top: 6px;
        margin-bottom: 2rem;
        font-weight: 400;
    }
    .fs-section {
        font-size: 13px;
        font-weight: 600;
        color: #a1a1aa;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin-bottom: 1rem;
    }
    .fs-label {
        font-size: 13px;
        color: #71717a;
        font-weight: 500;
    }
    .fs-value {
        font-size: 13px;
        color: #d4d4d8;
        font-weight: 600;
    }

    /* ── Cards ── */
    .fs-card {
        background: #0f0f12;
        border: 1px solid #1c1c22;
        border-radius: 12px;
        padding: 1.25rem;
        margin-bottom: 0.75rem;
        transition: border-color 0.2s;
    }
    .fs-card:hover {
        border-color: #27272a;
    }
    .fs-card-title {
        font-size: 14px;
        font-weight: 600;
        color: #e4e4e7;
        margin-bottom: 6px;
    }
    .fs-card-desc {
        font-size: 13px;
        color: #71717a;
        line-height: 1.65;
    }

    /* ── Step indicator ── */
    .fs-step {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 24px;
        height: 24px;
        border-radius: 6px;
        font-size: 12px;
        font-weight: 700;
        margin-bottom: 12px;
        color: #fafafa;
        background: #f97316;
    }

    /* ── Algorithm badge ── */
    .fs-algo-badge {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 28px;
        height: 28px;
        border-radius: 6px;
        font-size: 12px;
        font-weight: 700;
        color: #fafafa;
        background: #27272a;
        border: 1px solid #3f3f46;
        flex-shrink: 0;
    }
    .fs-algo-name {
        font-size: 14px;
        font-weight: 600;
        color: #e4e4e7;
    }

    /* ── Tags ── */
    .fs-tag {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 6px;
        font-size: 12px;
        font-weight: 500;
        color: #a1a1aa;
        background: #18181b;
        border: 1px solid #27272a;
        margin: 3px 2px;
    }

    /* ── Metrics ── */
    .fs-metric-card {
        background: #0f0f12;
        border: 1px solid #1c1c22;
        border-radius: 12px;
        padding: 1.25rem;
        text-align: center;
    }
    .fs-metric-num {
        font-size: 32px;
        font-weight: 700;
        color: #fafafa;
        letter-spacing: -0.03em;
        line-height: 1;
        margin-bottom: 6px;
    }
    .fs-metric-label {
        font-size: 12px;
        color: #71717a;
        font-weight: 500;
    }

    /* ── Verdict cards ── */
    .fs-verdict-safe {
        background: #0f0f12;
        border: 1px solid #166534;
        border-radius: 12px;
        padding: 1.25rem 1.5rem;
    }
    .fs-verdict-safe .fs-verdict-title {
        font-size: 15px;
        font-weight: 600;
        color: #4ade80;
    }
    .fs-verdict-warn {
        background: #0f0f12;
        border: 1px solid #92400e;
        border-radius: 12px;
        padding: 1.25rem 1.5rem;
    }
    .fs-verdict-warn .fs-verdict-title {
        font-size: 15px;
        font-weight: 600;
        color: #f97316;
    }
    .fs-verdict-desc {
        font-size: 13px;
        color: #71717a;
        margin-top: 4px;
    }

    /* ── Status badges ── */
    .fs-status-ok {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 6px;
        font-size: 12px;
        font-weight: 600;
        color: #4ade80;
        background: rgba(34, 197, 94, 0.1);
        border: 1px solid #166534;
    }
    .fs-status-warn {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 6px;
        font-size: 12px;
        font-weight: 600;
        color: #f97316;
        background: rgba(249, 115, 22, 0.1);
        border: 1px solid #92400e;
    }

    /* ── Progress bar ── */
    .fs-progress {
        background: #18181b;
        border-radius: 4px;
        height: 6px;
        overflow: hidden;
        margin: 10px 0;
    }
    .fs-progress-ok {
        height: 100%;
        border-radius: 4px;
        background: #22c55e;
        transition: width 0.5s ease;
    }
    .fs-progress-warn {
        height: 100%;
        border-radius: 4px;
        background: #f97316;
        transition: width 0.5s ease;
    }

    /* ── Divider ── */
    .fs-hr {
        border: none;
        border-top: 1px solid #1c1c22;
        margin: 2rem 0;
    }

    /* ── Info rows ── */
    .fs-info-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 9px 0;
        border-bottom: 1px solid #18181b;
        font-size: 13px;
    }
    .fs-info-row:last-child {
        border-bottom: none;
    }

    /* ── Empty state ── */
    .fs-empty {
        border: 1px dashed #27272a;
        border-radius: 12px;
        padding: 4rem 2rem;
        text-align: center;
    }
    .fs-empty-icon {
        font-size: 36px;
        margin-bottom: 12px;
        opacity: 0.5;
    }
    .fs-empty-title {
        font-size: 15px;
        font-weight: 600;
        color: #71717a;
        margin-bottom: 4px;
    }
    .fs-empty-desc {
        font-size: 13px;
        color: #52525b;
    }

    /* ── Button override ── */
    .stButton > button {
        background: #fafafa;
        color: #09090b;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 1.5rem;
        font-size: 13px;
        font-weight: 600;
        width: 100%;
        transition: all 0.15s;
        letter-spacing: -0.01em;
    }
    .stButton > button:hover {
        background: #e4e4e7;
        color: #09090b;
    }
    .stButton > button:active {
        background: #d4d4d8;
        color: #09090b;
    }

    /* ── File uploader override ── */
    [data-testid="stFileUploader"] {
        border: 1px dashed #27272a;
        border-radius: 12px;
        padding: 0.75rem;
        background: transparent;
    }
    [data-testid="stFileUploader"] label {
        color: #71717a !important;
        font-size: 13px;
    }
    [data-testid="stFileUploader"] small {
        color: #52525b !important;
    }
    [data-testid="stFileUploader"] button {
        background: #18181b !important;
        color: #a1a1aa !important;
        border: 1px solid #27272a !important;
        border-radius: 6px !important;
        font-size: 13px !important;
    }

    /* ── Checkbox ── */
    .stCheckbox label span {
        color: #d4d4d8 !important;
        font-size: 13px;
    }

    /* ── General text color override ── */
    .stMarkdown, .stMarkdown p {
        color: #a1a1aa;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #fafafa !important;
    }

    /* ── Scrollbar ── */
    ::-webkit-scrollbar { width: 5px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: #27272a; border-radius: 3px; }

    /* ── Hide deploy button ── */
    [data-testid="stToolbar"] { display: none; }

    /* ── Spinner ── */
    .stSpinner > div { border-top-color: #f97316 !important; }

    /* ── Alert boxes ── */
    .stAlert { border-radius: 8px; font-size: 13px; }
</style>
""", unsafe_allow_html=True)

# ─── Sidebar ───
st.sidebar.markdown("""
<div class="sidebar-brand">
    <span class="sidebar-brand-dot"></span><span class="sidebar-brand-name">ForgeScan</span>
</div>
""", unsafe_allow_html=True)

page = st.sidebar.radio(
    "",
    ["Ana Sayfa", "Analiz"],
    label_visibility="collapsed"
)

st.sidebar.markdown("---")
st.sidebar.markdown("""
<div class="sidebar-version">v1.0 · Görüntü Sahteciliği Tespit</div>
""", unsafe_allow_html=True)

# ─── Routing ───
if page == "Ana Sayfa":
    from _pages.home import show
    show()
elif page == "Analiz":
    from _pages.analysis import show
    show()