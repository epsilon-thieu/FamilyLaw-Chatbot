import os
import uuid
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
if "GOOGLE_API_KEY" in st.secrets:
    os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]

# ============================================================
# Giao diện (CSS) — Thiết kế mới: Thân thiện, hiện đại, dễ dùng
# ============================================================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@300;400;500;600;700;800&display=swap');

    /* ── Force light mode ── */
    :root, .stApp {
        --background-color: #f8f9fc !important;
        --secondary-background-color: #ffffff !important;
        --text-color: #1e293b !important;
        --primary-color: #6366f1 !important;
        color-scheme: light !important;
    }

    html, body, [class*="css"] {
        font-family: 'Be Vietnam Pro', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    :root {
        --ink:          #1e293b;
        --ink-soft:     #64748b;
        --ink-lighter:  #94a3b8;
        --primary:      #6366f1;
        --primary-soft: #818cf8;
        --primary-bg:   #eef2ff;
        --primary-dk:   #4f46e5;
        --warm:         #f59e0b;
        --warm-soft:    #fbbf24;
        --warm-bg:      #fffbeb;
        --warm-dk:      #d97706;
        --success:      #10b981;
        --success-dk:   #059669;
        --bg:           #f8f9fc;
        --card:         #ffffff;
        --border:       #e2e8f0;
        --border-soft:  #f1f5f9;
        --shadow-sm:    0 1px 3px rgba(0,0,0,0.04), 0 1px 2px rgba(0,0,0,0.06);
        --shadow-md:    0 4px 12px rgba(0,0,0,0.05), 0 2px 4px rgba(0,0,0,0.04);
        --shadow-lg:    0 10px 25px rgba(0,0,0,0.07), 0 4px 10px rgba(0,0,0,0.04);
        --radius-sm:    10px;
        --radius-md:    16px;
        --radius-lg:    24px;
    }

    /* ── App background ── */
    .stApp {
        background: linear-gradient(135deg, #f8f9fc 0%, #eef2ff 50%, #fefce8 100%);
    }

    #MainMenu, footer { visibility: hidden; }

    /* ── Scrollbar ── */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 99px; }
    ::-webkit-scrollbar-thumb:hover { background: #94a3b8; }

    /* ══════════════════════════════════════════════
       SIDEBAR
       ══════════════════════════════════════════════ */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e1b4b 0%, #312e81 100%);
        border-right: none;
        box-shadow: 4px 0 24px rgba(30, 27, 75, 0.15);
    }
    section[data-testid="stSidebar"] * {
        color: #e0e7ff !important;
    }

    /* ── Sidebar buttons (conversation list) ── */
    section[data-testid="stSidebar"] .stButton button {
        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: var(--radius-sm);
        text-align: left;
        font-size: 13.5px;
        font-weight: 500;
        padding: 11px 14px;
        transition: all .2s ease;
        backdrop-filter: blur(4px);
    }
    section[data-testid="stSidebar"] .stButton button:hover {
        background: rgba(255,255,255,0.12);
        border-color: rgba(255,255,255,0.2);
        transform: translateX(3px);
    }

    /* ── Sidebar brand ── */
    .sidebar-brand {
        font-size: 21px;
        font-weight: 800;
        color: #ffffff !important;
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 4px 0 2px 0;
        letter-spacing: -0.02em;
    }
    .sidebar-brand-icon {
        width: 38px; height: 38px;
        background: linear-gradient(135deg, var(--warm) 0%, #f97316 100%);
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 18px;
        box-shadow: 0 4px 12px rgba(249, 115, 22, 0.3);
    }
    .sidebar-sub {
        font-size: 12px;
        color: #a5b4fc !important;
        margin-bottom: 20px;
        padding-left: 48px;
        font-weight: 400;
    }
    .sidebar-section-label {
        font-size: 10.5px;
        text-transform: uppercase;
        letter-spacing: .12em;
        color: #818cf8 !important;
        margin: 22px 0 10px 2px;
        font-weight: 700;
    }

    /* ── "New chat" button — warm amber accent ── */
    div[data-testid="stSidebar"] div[data-testid="stButton"]:first-of-type button {
        background: linear-gradient(135deg, #f59e0b 0%, #f97316 100%) !important;
        color: #451a03 !important;
        font-weight: 700 !important;
        border: none !important;
        border-radius: var(--radius-sm) !important;
        box-shadow: 0 4px 16px rgba(245, 158, 11, 0.35);
        padding: 12px 16px !important;
        font-size: 14px !important;
        letter-spacing: -0.01em;
    }
    div[data-testid="stSidebar"] div[data-testid="stButton"]:first-of-type button:hover {
        filter: brightness(1.08);
        transform: translateY(-1px);
        box-shadow: 0 6px 20px rgba(245, 158, 11, 0.45);
    }

    /* ── Active conversation: green highlight ── */
    div[class*="st-key-conv_current"] button {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
        border: none !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        box-shadow: 0 4px 14px rgba(16, 185, 129, 0.35);
    }
    div[class*="st-key-conv_current"] button:hover {
        filter: brightness(1.06);
        transform: translateX(3px);
    }

    .sidebar-count {
        text-align: center;
        font-size: 11.5px;
        color: #818cf8 !important;
        padding: 6px 0;
        font-weight: 500;
    }

    /* ══════════════════════════════════════════════
       WELCOME HEADER (hero banner)
       ══════════════════════════════════════════════ */
    .hero-banner {
        background: linear-gradient(135deg, #6366f1 0%, #4f46e5 40%, #7c3aed 100%);
        border-radius: var(--radius-lg);
        padding: 32px 36px;
        margin-bottom: 24px;
        position: relative;
        overflow: hidden;
        box-shadow: 0 12px 32px rgba(99, 102, 241, 0.2);
    }
    .hero-banner::before {
        content: '';
        position: absolute;
        top: -40%; right: -20%;
        width: 400px; height: 400px;
        background: radial-gradient(circle, rgba(251, 191, 36, 0.15) 0%, transparent 70%);
        pointer-events: none;
    }
    .hero-banner::after {
        content: '';
        position: absolute;
        bottom: -30%; left: -10%;
        width: 300px; height: 300px;
        background: radial-gradient(circle, rgba(167, 139, 250, 0.2) 0%, transparent 70%);
        pointer-events: none;
    }
    .hero-content {
        position: relative;
        z-index: 1;
        display: flex;
        align-items: center;
        gap: 20px;
    }
    .hero-icon {
        width: 64px; height: 64px;
        background: rgba(255,255,255,0.15);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 30px;
        flex-shrink: 0;
        border: 1px solid rgba(255,255,255,0.1);
    }
    .hero-text h1, .hero-text h1 * { color: #ffffff !important; }
    .hero-text h1 {
        font-size: 22px;
        font-weight: 800;
        margin: 0;
        line-height: 1.3;
        letter-spacing: -0.02em;
    }
    .hero-text p, .hero-text p * { color: #c7d2fe !important; }
    .hero-text p {
        font-size: 13.5px;
        margin: 6px 0 0 0;
        font-weight: 400;
        line-height: 1.5;
    }

    /* ══════════════════════════════════════════════
       CHAT BUBBLES
       ══════════════════════════════════════════════ */
    .chat-bubble {
        padding: 16px 20px;
        line-height: 1.75;
        font-size: 15px;
        font-weight: 400;
        letter-spacing: 0.01em;
    }
    .user-bubble, .user-bubble * { color: #ffffff !important; }
    .user-bubble {
        background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
        border-radius: 20px 20px 6px 20px;
        box-shadow: 0 4px 14px rgba(99, 102, 241, 0.2);
    }
    .assistant-bubble, .assistant-bubble * { color: var(--ink) !important; }
    .assistant-bubble {
        background: var(--card);
        border: 1px solid var(--border);
        border-left: 4px solid var(--warm);
        border-radius: 6px 20px 20px 20px;
        box-shadow: var(--shadow-md);
    }

    /* ══════════════════════════════════════════════
       EXPANDER (citations)
       ══════════════════════════════════════════════ */
    div[data-testid="stExpander"],
    div[data-testid="stExpander"] details,
    div[data-testid="stExpander"] summary {
        background: var(--card) !important;
    }
    div[data-testid="stExpander"] {
        border: 1px solid var(--border) !important;
        border-radius: var(--radius-sm) !important;
        overflow: hidden;
        margin-top: 8px;
    }
    div[data-testid="stExpander"] summary,
    div[data-testid="stExpander"] summary *,
    div[data-testid="stExpander"] summary span,
    div[data-testid="stExpander"] summary p {
        color: var(--ink) !important;
        font-weight: 600 !important;
        font-size: 14px !important;
    }
    div[data-testid="stExpander"] svg { fill: var(--ink) !important; }
    div[data-testid="stExpanderDetails"],
    div[data-testid="stExpanderDetails"] * {
        color: var(--ink) !important;
        background: var(--card) !important;
    }

    /* ══════════════════════════════════════════════
       CITATION CARDS
       ══════════════════════════════════════════════ */
    .citation-card, .citation-card * { color: #92400e !important; }
    .citation-card {
        background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%) !important;
        border: 1px solid #fde68a;
        border-left: 4px solid var(--warm);
        border-radius: var(--radius-sm);
        padding: 12px 16px;
        margin-bottom: 8px;
        font-size: 13.5px;
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    .citation-card:hover {
        transform: translateX(4px);
        box-shadow: 0 4px 12px rgba(245, 158, 11, 0.15);
    }
    .citation-index, .citation-index * {
        display: inline-block;
        background: linear-gradient(135deg, var(--warm) 0%, var(--warm-dk) 100%) !important;
        color: #ffffff !important;
        font-weight: 800;
        border-radius: 8px;
        padding: 2px 10px;
        margin-right: 10px;
        font-size: 12px;
        letter-spacing: 0.02em;
    }
    .citation-meta, .citation-meta * {
        font-weight: 500;
        font-size: 13px;
    }

    /* ══════════════════════════════════════════════
       CHAT INPUT
       ══════════════════════════════════════════════ */
    div[data-testid="stChatInput"] {
        background: var(--card) !important;
        border-radius: var(--radius-md) !important;
        box-shadow: var(--shadow-lg);
    }
    div[data-testid="stChatInput"] textarea {
        background: var(--card) !important;
        color: var(--ink) !important;
        border-radius: 14px !important;
        border: 2px solid var(--border) !important;
        font-family: 'Be Vietnam Pro', sans-serif !important;
        font-size: 15px !important;
        transition: border-color 0.2s ease;
    }
    div[data-testid="stChatInput"] textarea:focus {
        border-color: var(--primary-soft) !important;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1) !important;
    }
    div[data-testid="stChatInput"] textarea::placeholder {
        color: #94a3b8 !important;
        font-weight: 400;
    }

    /* ── Spinner ── */
    div[data-testid="stSpinner"], div[data-testid="stSpinner"] * {
        color: var(--primary) !important;
        font-weight: 500;
    }

    /* ══════════════════════════════════════════════
       EMPTY STATE — Welcome Screen
       ══════════════════════════════════════════════ */
    .welcome-container {
        text-align: center;
        padding: 40px 20px 24px;
    }
    .welcome-avatar {
        width: 80px; height: 80px;
        margin: 0 auto 16px;
        background: linear-gradient(135deg, var(--primary) 0%, #7c3aed 100%);
        border-radius: 28px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 38px;
        box-shadow: 0 8px 24px rgba(99, 102, 241, 0.25);
        animation: avatar-float 3s ease-in-out infinite;
    }
    @keyframes avatar-float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-8px); }
    }
    .welcome-container h2, .welcome-container h2 * { color: var(--ink) !important; }
    .welcome-container h2 {
        font-size: 22px;
        font-weight: 700;
        margin: 0 0 6px 0;
        letter-spacing: -0.02em;
    }
    .welcome-container .welcome-desc, .welcome-container .welcome-desc * { color: var(--ink-soft) !important; }
    .welcome-container .welcome-desc {
        font-size: 14.5px;
        line-height: 1.6;
        max-width: 500px;
        margin: 0 auto;
    }

    /* ── Feature pills ── */
    .feature-pills {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        justify-content: center;
        margin: 20px auto 8px;
        max-width: 580px;
    }
    .feature-pill, .feature-pill * { color: var(--primary-dk) !important; }
    .feature-pill {
        background: var(--primary-bg) !important;
        border: 1px solid #c7d2fe;
        border-radius: 99px;
        padding: 6px 16px;
        font-size: 12.5px;
        font-weight: 500;
        display: inline-flex;
        align-items: center;
        gap: 6px;
        transition: transform 0.15s ease;
    }
    .feature-pill:hover {
        transform: scale(1.05);
    }

    /* ── Suggestion section label ── */
    .suggestion-label, .suggestion-label * {
        color: var(--ink-soft) !important;
    }
    .suggestion-label {
        font-size: 13px;
        font-weight: 600;
        text-align: center;
        margin: 28px 0 14px 0;
        letter-spacing: 0.01em;
    }

    /* ── Suggestion buttons ── */
    div[class*="st-key-suggestion_"] { position: relative; z-index: 1; }
    div[class*="st-key-suggestion_"] button {
        background: var(--card) !important;
        color: var(--ink) !important;
        border: 1.5px solid var(--border) !important;
        border-radius: var(--radius-md) !important;
        text-align: left !important;
        padding: 18px 20px !important;
        font-size: 14px !important;
        font-weight: 500 !important;
        width: 100%;
        box-shadow: var(--shadow-sm);
        transition: all .2s ease;
        line-height: 1.5 !important;
    }
    div[class*="st-key-suggestion_"] button:hover,
    div[class*="st-key-suggestion_"] button:focus {
        border-color: var(--primary) !important;
        background: var(--primary-bg) !important;
        color: var(--primary-dk) !important;
        transform: translateY(-3px);
        box-shadow: 0 8px 24px rgba(99, 102, 241, 0.15);
        z-index: 5;
        position: relative;
    }
    div[class*="st-key-suggestion_"] button:active {
        color: var(--primary-dk) !important;
        background: var(--primary-bg) !important;
        transform: translateY(-1px);
    }

    /* ══════════════════════════════════════════════
       DISCLAIMER BAR
       ══════════════════════════════════════════════ */
    .disclaimer-bar, .disclaimer-bar * { color: var(--ink-lighter) !important; }
    .disclaimer-bar {
        text-align: center;
        font-size: 12px;
        padding: 18px 0 6px 0;
        border-top: 1px solid var(--border-soft);
        margin-top: 16px;
        font-weight: 400;
    }
    .disclaimer-bar .disc-icon {
        display: inline-block;
        margin-right: 4px;
        vertical-align: middle;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# Load agent 1 lần duy nhất
# ============================================================
@st.cache_resource(show_spinner="⏳ Đang khởi tạo mô hình (lần đầu có thể mất 1-2 phút)...")
def load_agent():
    return HNGDAgentGraph()


agent = load_agent()

# ============================================================
# State quản lý nhiều cuộc trò chuyện
# ============================================================
if "conversations" not in st.session_state:
    st.session_state.conversations = {}  # {conv_id: {"title": str, "messages": list, "created_at": datetime}}

if "current_conv_id" not in st.session_state:
    st.session_state.current_conv_id = None

if "pending_question" not in st.session_state:
    st.session_state.pending_question = None


def new_conversation():
    conv_id = str(uuid.uuid4())
    st.session_state.conversations[conv_id] = {
        "title": "Đoạn chat mới",
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
    ("💍", "Điều kiện kết hôn", "Điều kiện để kết hôn hợp pháp tại Việt Nam là gì?"),
    ("📄", "Thủ tục ly hôn", "Thủ tục ly hôn thuận tình cần những giấy tờ gì?"),
    ("🏠", "Tài sản hôn nhân", "Tài sản chung và tài sản riêng trong hôn nhân được xác định thế nào?"),
    ("👨‍👩‍👧", "Quyền nuôi con", "Quyền nuôi con sau khi ly hôn được quy định ra sao?"),
]

# ============================================================
# Sidebar: danh sách hội thoại
# ============================================================
with st.sidebar:
    st.markdown(
        '<div class="sidebar-brand">'
        '<div class="sidebar-brand-icon">⚖️</div>'
        'Trợ lý Pháp lý'
        '</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="sidebar-sub">Luật Hôn nhân &amp; Gia đình Việt Nam</div>',
        unsafe_allow_html=True,
    )

    if st.button("✨  Cuộc trò chuyện mới", use_container_width=True):
        new_conversation()
        st.rerun()

    st.markdown(
        '<div class="sidebar-section-label">💬 Lịch sử trò chuyện</div>',
        unsafe_allow_html=True,
    )

    sorted_convs = sorted(
        st.session_state.conversations.items(),
        key=lambda kv: kv[1]["created_at"],
        reverse=True,
    )

    for conv_id, conv in sorted_convs:
        is_current = conv_id == st.session_state.current_conv_id
        # "conv_current" chỉ dùng cho ĐÚNG MỘT hội thoại tại một thời điểm
        # -> an toàn để dùng làm key cố định, CSS bên trên sẽ tô xanh lá.
        row_key = "conv_current" if is_current else f"conv_row_{conv_id}"
        label = ("✅  " if is_current else "💬  ") + conv["title"]
        with st.container(key=row_key):
            col_main, col_del = st.columns([5, 1])
            with col_main:
                if st.button(label, key=f"conv_{conv_id}", use_container_width=True):
                    st.session_state.current_conv_id = conv_id
                    st.rerun()
            with col_del:
                if st.button("🗑️", key=f"del_{conv_id}", help="Xóa đoạn chat này"):
                    delete_conversation(conv_id)
                    st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        f'<div class="sidebar-count">📂 {len(st.session_state.conversations)} đoạn chat</div>',
        unsafe_allow_html=True,
    )

current_conv_id = st.session_state.current_conv_id
current_conv = st.session_state.conversations[current_conv_id]


def render_citations(citations):
    if not citations:
        return
    with st.expander(f"📖 Trích dẫn pháp lý ({len(citations)} nguồn)"):
        for c in citations:
            meta = c["metadata"]
            st.markdown(
                f'<div class="citation-card">'
                f'<span class="citation-index">{c["index"]}</span>'
                f'<span class="citation-meta">{meta.get("source", "")} — '
                f'Điều {meta.get("dieu", "?")} — Khoản {meta.get("khoan", "?")}</span>'
                f'</div>',
                unsafe_allow_html=True,
            )


# ============================================================
# Header chính — Hero Banner
# ============================================================
st.markdown(
    """
    <div class="hero-banner">
        <div class="hero-content">
            <div class="hero-icon">⚖️</div>
            <div class="hero-text">
                <h1>Trợ lý Luật Hôn nhân & Gia đình</h1>
                <p>Hỏi đáp nhanh, chính xác dựa trên văn bản Luật Hôn nhân và Gia đình Việt Nam. Mọi câu trả lời đều có trích dẫn nguồn cụ thể.</p>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# Khu vực chat
# ============================================================
has_messages = len(current_conv["messages"]) > 0

if not has_messages:
    # ── Welcome / Empty State ──
    st.markdown(
        """
        <div class="welcome-container">
            <div class="welcome-avatar">📜</div>
            <h2>Xin chào! Mình có thể giúp gì cho bạn?</h2>
            <p class="welcome-desc">
                Hãy đặt câu hỏi về Luật Hôn nhân và Gia đình — mình sẽ tra cứu
                văn bản luật và trả lời kèm trích dẫn điều khoản cụ thể.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Feature pills ──
    st.markdown(
        """
        <div class="feature-pills">
            <span class="feature-pill">💍 Kết hôn</span>
            <span class="feature-pill">📄 Ly hôn</span>
            <span class="feature-pill">🏠 Tài sản</span>
            <span class="feature-pill">👶 Nuôi con</span>
            <span class="feature-pill">💰 Cấp dưỡng</span>
            <span class="feature-pill">👨‍👩‍👧 Con nuôi</span>
            <span class="feature-pill">🛡️ Giám hộ</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="suggestion-label">✨ Bạn có thể thử hỏi</div>',
        unsafe_allow_html=True,
    )

    cols = st.columns(2)
    for i, (icon, short_title, q) in enumerate(EXAMPLE_QUESTIONS):
        with cols[i % 2]:
            with st.container(key=f"suggestion_{i}"):
                if st.button(
                    f"{icon}  {q}",
                    key=f"suggestion_btn_{i}",
                    use_container_width=True,
                ):
                    st.session_state.pending_question = q

for msg in current_conv["messages"]:
    role = msg["role"]
    avatar = "⚖️" if role == "assistant" else "🧑"
    with st.chat_message(role, avatar=avatar):
        bubble_class = "user-bubble" if role == "user" else "assistant-bubble"
        st.markdown(
            f'<div class="chat-bubble {bubble_class}">{msg["content"]}</div>',
            unsafe_allow_html=True,
        )
        if msg.get("citations"):
            render_citations(msg["citations"])

# Câu hỏi từ gợi ý (nếu có) hoặc từ ô nhập
question = st.chat_input("Nhập câu hỏi về Luật Hôn nhân và Gia đình...")
if st.session_state.pending_question:
    question = st.session_state.pending_question
    st.session_state.pending_question = None

if question:
    if not current_conv["messages"]:
        title = question.strip()
        current_conv["title"] = title[:40] + ("..." if len(title) > 40 else "")

    current_conv["messages"].append({"role": "user", "content": question})
    with st.chat_message("user", avatar="🧑"):
        st.markdown(f'<div class="chat-bubble user-bubble">{question}</div>', unsafe_allow_html=True)

    with st.chat_message("assistant", avatar="⚖️"):
        with st.spinner("🔍 Đang tra cứu văn bản luật..."):
            try:
                final_state = agent.run(question, thread_id=current_conv_id)
                answer = final_state.get("answer", "Xin lỗi, mình chưa có câu trả lời.")
                citations = final_state.get("citations", [])
            except Exception as e:
                answer = f"Đã có lỗi xảy ra: {e}"
                citations = []

        st.markdown(f'<div class="chat-bubble assistant-bubble">{answer}</div>', unsafe_allow_html=True)
        render_citations(citations)

    current_conv["messages"].append(
        {"role": "assistant", "content": answer, "citations": citations}
    )
    st.rerun()

st.markdown(
    '<div class="disclaimer-bar">'
    '<span class="disc-icon">⚠️</span> '
    'Thông tin do trợ lý cung cấp chỉ mang tính tham khảo, '
    'không thay thế tư vấn pháp lý chính thức từ luật sư.'
    '</div>',
    unsafe_allow_html=True,
)