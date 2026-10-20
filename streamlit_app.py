import os
import uuid
import html
from datetime import datetime

import streamlit as st

from agent.graph import HNGDAgentGraph

# ============================================================
# Cấu hình trang
# ============================================================
st.set_page_config(
    page_title="Trợ lý Luật Hôn nhân & Gia đình",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----- API key -----
for _k in ("GOOGLE_API_KEY", "GOOGLE_API_KEY_2"):
    try:
        if _k in st.secrets:
            os.environ[_k] = st.secrets[_k]
    except Exception:
        pass  # chạy local: dùng .env

# ============================================================
# CSS — Editorial Stone & Deep Forest · Typography Việt chuẩn mực
# ============================================================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&family=Plus+Jakarta+Sans:wght@500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

    :root, .stApp {
        --primary-color: #1E3A34 !important;
        --background-color: #F6F5F0 !important;
        --secondary-background-color: #ECEAE2 !important;
        --text-color: #141413 !important;
        color-scheme: light !important;
    }

    /* ── Thiết lập phông chữ chuẩn tiếng Việt êm mắt, khử hoàn toàn khoảng cách chữ rời rạc ── */
    html, body, [class*="css"], .stApp {
        font-family: 'Be Vietnam Pro', 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
        background-color: #F6F5F0 !important;
        color: #141413 !important;
        letter-spacing: normal !important;
    }

    .stApp {
        background: #F6F5F0 !important;
    }

    #MainMenu, footer {
        visibility: hidden !important;
    }

    /* giữ header để còn nút mở sidebar, chỉ làm nó trong suốt */
    header[data-testid="stHeader"] {
        background: transparent !important;
    }

    /* ẩn riêng Deploy / menu ba chấm */
    [data-testid="stToolbar"],
    [data-testid="stDecoration"],
    [data-testid="stStatusWidget"] {
        visibility: hidden !important;
    }

    /* đảm bảo nút mở sidebar luôn hiện và đúng màu */
    [data-testid="stExpandSidebarButton"],
    [data-testid="stSidebarCollapsedControl"],
    [data-testid="collapsedControl"] {
        visibility: visible !important;
    }
    [data-testid="stExpandSidebarButton"] *,
    [data-testid="stSidebarCollapsedControl"] *,
    [data-testid="collapsedControl"] * {
        color: #1E3A34 !important;
    }

    /* ── Cột nội dung chính căn giữa chuẩn đọc ── */
    .main .block-container {
        max-width: 820px !important;
        padding-top: 24px !important;
        padding-bottom: 140px !important;
        padding-left: 24px !important;
        padding-right: 24px !important;
        margin: 0 auto !important;
    }

    /* ── Scrollbar thanh lịch ── */
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: #ECEAE2; }
    ::-webkit-scrollbar-thumb { background: #C8C4B8; border-radius: 4px; }
    ::-webkit-scrollbar-thumb:hover { background: #1E3A34; }

    /* ══════════════════════════════════════════════
       SIDEBAR — Tông xám đá ấm, bố cục thanh thoát
       ══════════════════════════════════════════════ */
    section[data-testid="stSidebar"] {
        background: #ECEAE2 !important;
        border-right: 1px solid #D5D1C8 !important;
    }
    section[data-testid="stSidebar"] * {
        color: #141413 !important;
    }

    .sidebar-brand-box {
        padding: 6px 0 16px 0;
        border-bottom: 1.5px solid #D2CEC4;
        margin-bottom: 18px;
    }
    .sidebar-brand-code {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 10.5px;
        font-weight: 700;
        letter-spacing: 0.04em;
        text-transform: uppercase;
        color: #1E3A34 !important;
        margin-bottom: 4px;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    .sidebar-brand-title {
        font-family: 'Plus Jakarta Sans', 'Be Vietnam Pro', sans-serif;
        font-size: 15px;
        font-weight: 700;
        letter-spacing: -0.01em;
        color: #141413 !important;
    }
    .sidebar-brand-desc {
        font-size: 12px;
        color: #5C5A55 !important;
        margin-top: 4px;
        line-height: 1.45;
    }

    /* ── Nút "Cuộc trò chuyện mới" ── */
    div[data-testid="stSidebar"] div[data-testid="stButton"]:first-of-type button {
        background: #1E3A34 !important;
        color: #FFFFFF !important;
        font-family: 'Be Vietnam Pro', sans-serif !important;
        font-weight: 600 !important;
        border: 1px solid #1E3A34 !important;
        border-radius: 10px !important;
        padding: 10px 14px !important;
        font-size: 13px !important;
        letter-spacing: 0.02em !important;
        box-shadow: 0 2px 6px rgba(30, 58, 52, 0.2) !important;
        transition: all 0.2s ease !important;
    }
    div[data-testid="stSidebar"] div[data-testid="stButton"]:first-of-type button * {
        color: #FFFFFF !important;
    }
    div[data-testid="stSidebar"] div[data-testid="stButton"]:first-of-type button:hover {
        background: #142824 !important;
        border-color: #142824 !important;
        transform: translateY(-1px);
        box-shadow: 0 4px 10px rgba(30, 58, 52, 0.3) !important;
    }

    .sidebar-section-header {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 10.5px;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #6E6C66 !important;
        margin: 24px 0 10px 0;
        font-weight: 700;
        border-bottom: 1px solid #D5D1C8;
        padding-bottom: 6px;
    }

    /* ── Nút danh sách hội thoại trong Sidebar ── */
    section[data-testid="stSidebar"] .stButton button {
        background: transparent !important;
        border: 1px solid transparent !important;
        border-radius: 8px !important;
        text-align: left !important;
        font-size: 13px !important;
        font-weight: 400 !important;
        padding: 8px 10px !important;
        color: #383734 !important;
        transition: all 0.15s ease !important;
    }
    section[data-testid="stSidebar"] .stButton button:hover {
        background: #E2DFD5 !important;
        border-color: #C8C4B8 !important;
        color: #141413 !important;
    }

    /* ── Hội thoại đang chọn ── */
    div[class*="st-key-conv_current"] button {
        background: #FFFFFF !important;
        border: 1px solid #C8C4B8 !important;
        border-left: 3px solid #1E3A34 !important;
        color: #141413 !important;
        font-weight: 600 !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04) !important;
    }

    .sidebar-footer-info {
        font-size: 11px;
        color: #6E6C66 !important;
        padding: 16px 0 0 0;
        border-top: 1px solid #D5D1C8;
        margin-top: 20px;
    }

    /* ══════════════════════════════════════════════
       HERO THUMBNAIL CARD — SINH ĐỘNG, BẮT MẮT & SANG TRỌNG
       ══════════════════════════════════════════════ */
    .hero-banner {
        background: linear-gradient(135deg, #FFFFFF 0%, #FAF8F4 55%, #F4EFE6 100%);
        border: 1px solid #D8D4CA;
        border-left: 5px solid #1E3A34;
        border-radius: 14px;
        padding: 22px 24px 18px 24px;
        margin-bottom: 28px;
        box-shadow: 0 4px 20px -2px rgba(30, 58, 52, 0.07), 0 2px 6px -1px rgba(0, 0, 0, 0.03);
        position: relative;
        overflow: hidden;
    }

    .hero-banner::after {
        content: "";
        position: absolute;
        right: -25px;
        bottom: -35px;
        width: 170px;
        height: 170px;
        background: radial-gradient(circle, rgba(30, 58, 52, 0.04) 0%, rgba(30, 58, 52, 0) 70%);
        pointer-events: none;
    }

    .hero-main-row {
        display: flex;
        align-items: flex-start;
        gap: 16px;
    }

    .hero-emblem-box {
        width: 50px;
        height: 50px;
        background: linear-gradient(145deg, #254942 0%, #152C27 100%);
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
        box-shadow: 0 4px 12px rgba(30, 58, 52, 0.22);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }

    .hero-emblem-icon {
        width: 28px;
        height: 28px;
        stroke: #F6F5F0;
        fill: none;
    }

    .hero-content {
        flex: 1;
    }

    .hero-kicker-row {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 6px;
        flex-wrap: wrap;
    }

    .hero-status-pill {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: #EBF2EE;
        border: 1px solid #C5DBD0;
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 600;
        color: #1E3A34;
        letter-spacing: 0.02em;
    }

    .live-dot-pulse {
        width: 6.5px;
        height: 6.5px;
        background: #2E7D32;
        border-radius: 50%;
        display: inline-block;
        box-shadow: 0 0 0 0 rgba(46, 125, 50, 0.7);
        animation: pulseDot 2s infinite;
    }

    @keyframes pulseDot {
        0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(46, 125, 50, 0.7); }
        70% { transform: scale(1); box-shadow: 0 0 0 6px rgba(46, 125, 50, 0); }
        100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(46, 125, 50, 0); }
    }

    .hero-badge-tag {
        background: #ECEAE2;
        border: 1px solid #D0CCC2;
        padding: 3px 9px;
        border-radius: 6px;
        font-size: 11px;
        font-weight: 600;
        color: #4A4844;
        letter-spacing: 0.02em;
    }

    .hero-title {
        font-family: 'Plus Jakarta Sans', 'Be Vietnam Pro', sans-serif;
        font-size: 19px;
        font-weight: 700;
        letter-spacing: -0.015em;
        color: #141413 !important;
        margin: 2px 0 6px 0;
        line-height: 1.35;
    }

    .hero-subtitle {
        font-size: 13.5px;
        color: #55534E !important;
        margin: 0;
        line-height: 1.55;
    }

    .hero-features-bar {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 10px;
        margin-top: 16px;
        padding-top: 14px;
        border-top: 1px solid #E6E2D8;
    }

    .hero-feature-item {
        display: flex;
        align-items: center;
        gap: 9px;
        background: rgba(255, 255, 255, 0.75);
        padding: 8px 12px;
        border-radius: 8px;
        border: 1px solid #EAE5DC;
        transition: background 0.15s ease;
    }
    .hero-feature-item:hover {
        background: #FFFFFF;
        border-color: #D2CDC3;
    }

    .feature-icon {
        font-size: 16px;
        flex-shrink: 0;
    }

    .feature-text {
        display: flex;
        flex-direction: column;
    }

    .feature-text strong {
        font-size: 12px;
        color: #1E3A34;
        font-weight: 600;
        letter-spacing: -0.01em;
    }

    .feature-text span {
        font-size: 11px;
        color: #6E6C64;
    }

    /* ══════════════════════════════════════════════
       KHU VỰC TRÒ CHUYỆN (BONG BÓNG TIN NHẮN)
       ══════════════════════════════════════════════ */
    .user-msg-row {
        display: flex;
        flex-direction: column;
        align-items: flex-end;
        width: 100%;
        margin: 24px 0 20px 0;
    }
    .user-msg-label {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 0.04em;
        text-transform: uppercase;
        color: #706E66;
        margin-bottom: 6px;
    }
    .user-msg-box {
        background: #EAE6DC;
        color: #141413 !important;
        padding: 13px 18px;
        border: 1px solid #D5D1C7;
        border-right: 3.5px solid #1E3A34;
        border-radius: 12px 12px 2px 12px;
        max-width: 80%;
        font-size: 15px;
        line-height: 1.6;
        word-break: break-word;
        box-shadow: 0 1px 4px rgba(0, 0, 0, 0.04);
    }

    /* ── Phản hồi của trợ lý ── */
    .bot-label-bar {
        display: flex;
        align-items: center;
        gap: 8px;
        margin-top: 10px;
        margin-bottom: 12px;
        padding-bottom: 6px;
        border-bottom: 1px solid #E2DFD5;
    }
    .bot-square-marker {
        width: 8px;
        height: 8px;
        background: #1E3A34;
        border-radius: 2px;
        display: inline-block;
    }
    .bot-label-text {
        font-family: 'Plus Jakarta Sans', sans-serif;
        color: #1E3A34 !important;
        font-size: 11.5px;
        font-weight: 700;
        letter-spacing: 0.04em;
        text-transform: uppercase;
    }

    .stMarkdown p {
        font-size: 15px;
        line-height: 1.75;
        color: #141413 !important;
        margin-bottom: 14px;
        letter-spacing: normal;
    }
    .stMarkdown ul, .stMarkdown ol {
        margin: 8px 0 16px 22px;
        color: #141413 !important;
    }
    .stMarkdown li {
        font-size: 15px;
        line-height: 1.75;
        margin-bottom: 6px;
        color: #141413 !important;
    }
    .stMarkdown strong {
        color: #000000 !important;
        font-weight: 600;
    }

    /* ── Expander Căn cứ pháp lý ── */
    div[data-testid="stExpander"] {
        background: #FFFFFF !important;
        border: 1px solid #D8D4CA !important;
        border-radius: 10px !important;
        margin-top: 14px !important;
        margin-bottom: 24px !important;
        overflow: hidden !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03) !important;
    }
    div[data-testid="stExpander"] summary {
        background: #ECEAE2 !important;
        padding: 10px 14px !important;
    }
    div[data-testid="stExpander"] summary span,
    div[data-testid="stExpander"] summary p {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        color: #141413 !important;
        font-size: 12px !important;
        font-weight: 700 !important;
        letter-spacing: 0.03em !important;
        text-transform: uppercase !important;
    }
    div[data-testid="stExpander"] summary span[data-testid="stIconMaterial"] {
        font-family: "Material Symbols Rounded" !important;
        text-transform: none !important;
        letter-spacing: normal !important;
    }
    div[data-testid="stExpanderDetails"] {
        background: #FFFFFF !important;
        border-top: 1px solid #E2DFD5 !important;
        padding: 12px 16px !important;
    }

    .citation-item {
        display: flex;
        align-items: baseline;
        gap: 10px;
        padding: 8px 0;
        border-bottom: 1px solid #ECEAE2;
        font-size: 13.5px;
        color: #2C2B29 !important;
        line-height: 1.5;
    }
    .citation-item:last-child {
        border-bottom: none;
    }
    .citation-num {
        display: inline-block;
        background: #1E3A34;
        color: #FFFFFF !important;
        font-size: 11px;
        font-weight: 600;
        font-family: 'JetBrains Mono', monospace;
        padding: 2px 7px;
        border-radius: 4px;
        flex-shrink: 0;
    }

    /* ══════════════════════════════════════════════
       MÀN HÌNH CHỜ (EMPTY STATE) & GỢI Ý
       ══════════════════════════════════════════════ */
    .empty-state-wrap {
        padding: 4px 0 20px 0;
        border-bottom: 1px solid #D5D1C8;
        margin-bottom: 22px;
    }
    .empty-state-kicker {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 0.04em;
        text-transform: uppercase;
        color: #1E3A34 !important;
        margin-bottom: 6px;
    }
    .empty-state-title {
        font-family: 'Plus Jakarta Sans', 'Be Vietnam Pro', sans-serif;
        font-size: 20px;
        font-weight: 700;
        letter-spacing: -0.015em;
        margin-bottom: 8px;
        color: #141413 !important;
    }
    .empty-state-desc {
        font-size: 14px;
        color: #55534E !important;
        max-width: 680px;
        margin-bottom: 18px;
        line-height: 1.6;
    }

    .topic-badges {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
    }
    .topic-badge-item {
        background: #FFFFFF;
        border: 1px solid #D5D1C8;
        border-radius: 8px;
        padding: 6px 12px;
        font-size: 12.5px;
        font-weight: 500;
        color: #2C2B29 !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03);
        transition: all 0.15s ease;
    }
    .topic-badge-item:hover {
        background: #ECEAE2;
        border-color: #1E3A34;
        color: #1E3A34 !important;
        transform: translateY(-1px);
    }

    .suggest-header {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 11.5px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.04em;
        color: #6E6C66;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        gap: 6px;
    }

    /* ── Nút câu hỏi gợi ý ── */
    div[class*="st-key-suggest_"] button {
        background: #FFFFFF !important;
        color: #141413 !important;
        border: 1px solid #D5D1C8 !important;
        border-left: 3.5px solid #C4C0B4 !important;
        border-radius: 10px !important;
        text-align: left !important;
        padding: 13px 16px !important;
        font-size: 13.5px !important;
        font-weight: 500 !important;
        line-height: 1.5 !important;
        box-shadow: 0 1px 4px rgba(0, 0, 0, 0.03) !important;
        transition: all 0.18s ease !important;
        margin-bottom: 8px !important;
    }
    div[class*="st-key-suggest_"] button:hover {
        background: #FAF8F4 !important;
        border-color: #1E3A34 !important;
        border-left: 3.5px solid #1E3A34 !important;
        color: #000000 !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(30, 58, 52, 0.08) !important;
    }

    /* ══════════════════════════════════════════════
       KHUNG NHẬP LIỆU (CHAT INPUT) — ĐƠN GIẢN, BẮT MẮT, KHỬ NỀN ĐEN
       ══════════════════════════════════════════════ */
    div[data-testid="stBottom"],
    div[data-testid="stBottom"] > div,
    div[data-testid="stBottomBlockContainer"],
    .stChatFloatingInputContainer {
        background: transparent !important;
        background-color: transparent !important;
    }

    div[data-testid="stBottom"] {
        background: linear-gradient(180deg, rgba(246, 245, 240, 0) 0%, rgba(246, 245, 240, 0.95) 24%, #F6F5F0 100%) !important;
        padding-top: 14px !important;
        padding-bottom: 22px !important;
        border-top: none !important;
    }

    div[data-testid="stChatInput"] {
        max-width: 820px !important;
        margin: 0 auto !important;
        background: #FFFFFF !important;
        border: 1.5px solid #D8D4CA !important;
        border-radius: 18px !important;
        padding: 6px 10px 6px 18px !important;
        box-shadow: 0 4px 20px -2px rgba(30, 58, 52, 0.08), 0 2px 6px -1px rgba(0, 0, 0, 0.03) !important;
        transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }

    div[data-testid="stChatInput"]:focus-within {
        border-color: #1E3A34 !important;
        box-shadow: 0 8px 30px -4px rgba(30, 58, 52, 0.16), 0 0 0 3px rgba(30, 58, 52, 0.1) !important;
        transform: translateY(-1px) !important;
    }

    div[data-testid="stChatInput"] * {
        background: transparent !important;
    }

    div[data-testid="stChatInput"] textarea {
        color: #141413 !important;
        border: none !important;
        box-shadow: none !important;
        font-family: 'Be Vietnam Pro', sans-serif !important;
        font-size: 14.5px !important;
        line-height: 1.55 !important;
        letter-spacing: normal !important;
        padding: 10px 4px !important;
        outline: none !important;
    }

    div[data-testid="stChatInput"] textarea::placeholder {
        color: #8C8980 !important;
        font-size: 14px !important;
        font-family: 'Be Vietnam Pro', sans-serif !important;
        font-weight: 400 !important;
    }

    /* Nút gửi: Hiện đại, bo góc mềm mại, hover sắc sảo */
    div[data-testid="stChatInput"] button {
        background: linear-gradient(135deg, #244941 0%, #162E29 100%) !important;
        border: none !important;
        border-radius: 12px !important;
        width: 38px !important;
        height: 38px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        box-shadow: 0 2px 6px rgba(30, 58, 52, 0.25) !important;
        transition: all 0.18s ease !important;
    }

    div[data-testid="stChatInput"] button:hover {
        background: linear-gradient(135deg, #1A3831 0%, #0F201C 100%) !important;
        transform: scale(1.06) translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(30, 58, 52, 0.35) !important;
    }

    div[data-testid="stChatInput"] button svg {
        fill: #FFFFFF !important;
    }

    /* ── Spinner ── */
    div[data-testid="stSpinner"], div[data-testid="stSpinner"] * {
        color: #1E3A34 !important;
        font-size: 13px !important;
        font-weight: 500 !important;
    }

    /* ── Disclaimer dưới cùng ── */
    .disclaimer-note {
        text-align: left;
        font-size: 12px;
        color: #706E66 !important;
        margin-top: 32px;
        padding-top: 14px;
        border-top: 1px solid #DCD8CE;
        line-height: 1.6;
        letter-spacing: normal;
    }
    .disclaimer-inner {
        display: flex;
        align-items: flex-start;
        gap: 8px;
    }
    .disclaimer-icon {
        font-size: 14px;
        flex-shrink: 0;
        margin-top: 1px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# Load agent 1 lần duy nhất
# ============================================================
@st.cache_resource(show_spinner="Đang khởi tạo hệ thống tra cứu...")
def load_agent():
    return HNGDAgentGraph()


agent = load_agent()

# ============================================================
# State quản lý nhiều cuộc trò chuyện
# ============================================================
if "conversations" not in st.session_state:
    st.session_state.conversations = {}

if "current_conv_id" not in st.session_state:
    st.session_state.current_conv_id = None

if "pending_question" not in st.session_state:
    st.session_state.pending_question = None


def new_conversation():
    conv_id = str(uuid.uuid4())
    st.session_state.conversations[conv_id] = {
        "title": "Cuộc trò chuyện mới",
        "messages": [],
        "created_at": datetime.now(),
    }
    st.session_state.current_conv_id = conv_id


def delete_conversation(conv_id: str):
    st.session_state.conversations.pop(conv_id, None)
    if st.session_state.current_conv_id == conv_id:
        if st.session_state.conversations:
            latest = max(
                st.session_state.conversations.items(),
                key=lambda kv: kv[1]["created_at"],
            )[0]
            st.session_state.current_conv_id = latest
        else:
            new_conversation()


if not st.session_state.conversations:
    new_conversation()

EXAMPLE_QUESTIONS = [
    "Điều kiện để kết hôn hợp pháp tại Việt Nam theo Luật hiện hành?",
    "Thủ tục thuận tình ly hôn cần chuẩn bị những hồ sơ, giấy tờ gì?",
    "Tài sản chung và tài sản riêng của vợ chồng được phân định thế nào?",
    "Quyền nuôi con dưới 36 tháng tuổi sau khi ly hôn thuộc về ai?",
]

# ============================================================
# Sidebar
# ============================================================
with st.sidebar:
    st.markdown(
        """
        <div class="sidebar-brand-box">
            <div class="sidebar-brand-code">⚖️ HỆ THỐNG TRA CỨU</div>
            <div class="sidebar-brand-title">LUẬT HÔN NHÂN &amp; GIA ĐÌNH</div>
            <div class="sidebar-brand-desc">Cơ sở dữ liệu văn bản quy phạm pháp luật Việt Nam</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button("➕  CUỘC TRÒ CHUYỆN MỚI", use_container_width=True):
        new_conversation()
        st.rerun()

    st.markdown('<div class="sidebar-section-header">LỊCH SỬ PHIÊN TƯ VẤN</div>', unsafe_allow_html=True)

    sorted_convs = sorted(
        st.session_state.conversations.items(),
        key=lambda kv: kv[1]["created_at"],
        reverse=True,
    )

    for conv_id, conv in sorted_convs:
        is_current = conv_id == st.session_state.current_conv_id
        row_key = "conv_current" if is_current else f"conv_row_{conv_id}"
        label = conv["title"]
        with st.container(key=row_key):
            col_main, col_del = st.columns([5, 1])
            with col_main:
                if st.button(label, key=f"conv_{conv_id}", use_container_width=True):
                    st.session_state.current_conv_id = conv_id
                    st.rerun()
            with col_del:
                if st.button("✕", key=f"del_{conv_id}", help="Xóa phiên này"):
                    delete_conversation(conv_id)
                    st.rerun()

    st.markdown(
        f'<div class="sidebar-footer-info">Tổng số phiên tư vấn: <strong>{len(st.session_state.conversations):02d}</strong></div>',
        unsafe_allow_html=True,
    )

current_conv_id = st.session_state.current_conv_id
current_conv = st.session_state.conversations[current_conv_id]


def render_citations(citations):
    if not citations:
        return
    count = len(citations)
    with st.expander(f"CĂN CỨ PHÁP LÝ THAM CHIẾU ({count:02d} NGUỒN)"):
        for c in citations:
            meta = c.get("metadata", {})
            source = meta.get("source", "Văn bản luật")
            dieu = meta.get("dieu", "?")
            khoan = meta.get("khoan", "")
            khoan_str = f" — Khoản {khoan}" if khoan else ""
            st.markdown(
                f"""
                <div class="citation-item">
                    <span class="citation-num">[{c.get('index', 1):02d}]</span>
                    <span>{html.escape(source)} — Điều {html.escape(str(dieu))}{html.escape(khoan_str)}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )


# ============================================================
# Header trên cùng — Thumbnail Banner Sinh Động & Sang Trọng
# ============================================================
st.markdown(
    """
    <div class="hero-banner">
        <div class="hero-main-row">
            <div class="hero-emblem-box">
                <svg class="hero-emblem-icon" viewBox="0 0 24 24" stroke-width="1.8">
                    <path d="M12 3v17"/>
                    <path d="M5 7h14"/>
                    <path d="M6 7l-3 7h6l-3-7z"/>
                    <path d="M18 7l-3 7h6l-3-7z"/>
                    <circle cx="12" cy="20" r="1.5" fill="#F6F5F0"/>
                </svg>
            </div>
            <div class="hero-content">
                <div class="hero-kicker-row">
                    <span class="hero-status-pill">
                        <span class="live-dot-pulse"></span>
                        HỆ THỐNG TRỰC TUYẾN
                    </span>
                    <span class="hero-badge-tag">LUẬT HNGĐ 2014 &amp; VĂN BẢN HƯỚNG DẪN</span>
                </div>
                <h1 class="hero-title">Trợ Lý Pháp Lý Luật Hôn Nhân &amp; Gia Đình</h1>
                <p class="hero-subtitle">
                    Phân tích tình huống pháp lý, tra cứu quyền &amp; nghĩa vụ, đối chiếu trực tiếp từ cơ sở dữ liệu luật Việt Nam.
                </p>
            </div>
        </div>
        <div class="hero-features-bar">
            <div class="hero-feature-item">
                <span class="feature-icon">⚖️</span>
                <div class="feature-text">
                    <strong>Căn cứ xác thực</strong>
                    <span>Trích dẫn trực tiếp Điều, Khoản</span>
                </div>
            </div>
            <div class="hero-feature-item">
                <span class="feature-icon">⚡</span>
                <div class="feature-text">
                    <strong>Phân tích tức thì</strong>
                    <span>AI bám sát tình huống thực tế</span>
                </div>
            </div>
            <div class="hero-feature-item">
                <span class="feature-icon">🛡️</span>
                <div class="feature-text">
                    <strong>Chính xác &amp; Khách quan</strong>
                    <span>Không bịa điều luật, minh bạch</span>
                </div>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# Khu vực nội dung chat
# ============================================================
has_messages = len(current_conv["messages"]) > 0

if not has_messages:
    st.markdown(
        """
        <div class="empty-state-wrap">
            <div class="empty-state-kicker">CHẾ ĐỘ TRA CỨU TRỰC TUYẾN</div>
            <div class="empty-state-title">Nhập tình huống hoặc câu hỏi pháp lý của bạn</div>
            <div class="empty-state-desc">
                Hệ thống tự động phân tích quy định thuộc Luật Hôn nhân &amp; Gia đình hiện hành, cung cấp nội dung giải đáp kèm trích dẫn điều khoản cụ thể.
            </div>
            <div class="topic-badges">
                <span class="topic-badge-item">💍 Đăng ký kết hôn</span>
                <span class="topic-badge-item">📑 Ly hôn thuận tình / Đơn phương</span>
                <span class="topic-badge-item">💰 Chế độ tài sản vợ chồng</span>
                <span class="topic-badge-item">👶 Quyền nuôi con &amp; Cấp dưỡng</span>
                <span class="topic-badge-item">🏡 Con nuôi &amp; Giám hộ</span>
                <span class="topic-badge-item">⚖️ Xác định cha, mẹ, con</span>
            </div>
        </div>
        <div class="suggest-header">💡 CÂU HỎI TÌNH HUỐNG THAM KHẢO</div>
        """,
        unsafe_allow_html=True,
    )

    cols = st.columns(2)
    for i, q in enumerate(EXAMPLE_QUESTIONS):
        btn_label = f"0{i+1} ── {q}"
        with cols[i % 2]:
            with st.container(key=f"suggest_{i}"):
                if st.button(btn_label, key=f"suggest_btn_{i}", use_container_width=True):
                    st.session_state.pending_question = q

# ── Render lịch sử hội thoại ──
for msg in current_conv["messages"]:
    role = msg["role"]
    if role == "user":
        safe_q = html.escape(msg["content"]).replace("\n", "<br>")
        st.markdown(
            f"""
            <div class="user-msg-row">
                <div class="user-msg-label">NGƯỜI DÙNG</div>
                <div class="user-msg-box">{safe_q}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            """
            <div class="bot-label-bar">
                <span class="bot-square-marker"></span>
                <span class="bot-label-text">PHẢN HỒI PHÁP LÝ</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(msg["content"])
        if msg.get("citations"):
            render_citations(msg["citations"])

# ============================================================
# Nhận input câu hỏi
# ============================================================
question = st.chat_input("Nhập câu hỏi hoặc tình huống pháp lý cần tra cứu...")
if st.session_state.pending_question:
    question = st.session_state.pending_question
    st.session_state.pending_question = None

if question:
    if not current_conv["messages"]:
        title = question.strip()
        current_conv["title"] = title[:35] + ("..." if len(title) > 35 else "")

    current_conv["messages"].append({"role": "user", "content": question})

    safe_q = html.escape(question).replace("\n", "<br>")
    st.markdown(
        f"""
        <div class="user-msg-row">
            <div class="user-msg-label">NGƯỜI DÙNG</div>
            <div class="user-msg-box">{safe_q}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="bot-label-bar">
            <span class="bot-square-marker"></span>
            <span class="bot-label-text">PHẢN HỒI PHÁP LÝ</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.spinner("Đang đối chiếu cơ sở dữ liệu pháp luật..."):
        try:
            final_state = agent.run(question, thread_id=current_conv_id)
            answer = final_state.get(
                "answer",
                "Xin lỗi, hiện tại hệ thống chưa tìm thấy căn cứ pháp lý phù hợp trong kho dữ liệu.",
            )
            citations = final_state.get("citations", [])
        except Exception as e:
            err_str = str(e)
            if "503" in err_str or "high demand" in err_str or "UNAVAILABLE" in err_str:
                answer = "Hệ thống hiện đang chịu tải cao đột biến (503). Vui lòng gửi lại yêu cầu sau vài giây."
            else:
                answer = f"Không thể xử lý yêu cầu lúc này: {err_str}"
            citations = []

    st.markdown(answer)
    render_citations(citations)

    current_conv["messages"].append(
        {"role": "assistant", "content": answer, "citations": citations}
    )
    st.rerun()

st.markdown(
    """
    <div class="disclaimer-note">
        <div class="disclaimer-inner">
            <span class="disclaimer-icon">ℹ️</span>
            <span><strong>Lưu ý:</strong> Nội dung phản hồi được trích xuất tự động từ văn bản pháp luật hiện hành và chỉ mang tính chất tham khảo thông tin, không thay thế văn bản tư vấn pháp lý chính thức từ Luật sư.</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
