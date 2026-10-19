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
# CSS — Monochrome · Sharp · Premium
# ============================================================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap');

    /* ── Force light mode ── */
    :root, .stApp {
        --background-color: #ffffff !important;
        --secondary-background-color: #fafafa !important;
        --text-color: #171717 !important;
        --primary-color: #171717 !important;
        color-scheme: light !important;
    }

    html, body, [class*="css"] {
        font-family: 'IBM Plex Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }

    :root {
        --black:        #000000;
        --ink:          #171717;
        --ink-2:        #262626;
        --ink-3:        #404040;
        --gray-5:       #525252;
        --gray-4:       #737373;
        --gray-3:       #a3a3a3;
        --gray-2:       #d4d4d4;
        --gray-1:       #e5e5e5;
        --gray-0:       #f5f5f5;
        --white:        #ffffff;
        --bg:           #ffffff;
        --bg-alt:       #fafafa;
        --border:       #e5e5e5;
        --border-soft:  #f0f0f0;
    }

    /* ── App background ── */
    .stApp { background: var(--bg); }

    #MainMenu, footer { visibility: hidden; }

    /* ── Scrollbar ── */
    ::-webkit-scrollbar { width: 5px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: var(--gray-2); border-radius: 0; }
    ::-webkit-scrollbar-thumb:hover { background: var(--gray-3); }

    /* ══════════════════════════════════════════════
       SIDEBAR
       ══════════════════════════════════════════════ */
    section[data-testid="stSidebar"] {
        background: var(--ink);
        border-right: 1px solid #2a2a2a;
    }
    section[data-testid="stSidebar"] * {
        color: #d4d4d4 !important;
    }

    section[data-testid="stSidebar"] .stButton button {
        background: transparent;
        border: 1px solid #333333;
        border-radius: 0;
        text-align: left;
        font-size: 13px;
        font-weight: 400;
        padding: 10px 12px;
        transition: background .15s ease, border-color .15s ease;
        letter-spacing: 0.01em;
    }
    section[data-testid="stSidebar"] .stButton button:hover {
        background: #262626;
        border-color: #525252;
    }

    .sidebar-brand {
        font-size: 15px;
        font-weight: 600;
        color: #ffffff !important;
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 2px 0;
        letter-spacing: 0.06em;
        text-transform: uppercase;
    }
    .sidebar-brand-mark {
        width: 32px; height: 32px;
        background: #ffffff;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 15px;
        color: var(--ink) !important;
        font-weight: 700;
    }
    .sidebar-sub {
        font-size: 11.5px;
        color: #737373 !important;
        margin-bottom: 24px;
        padding-left: 42px;
        font-weight: 400;
        letter-spacing: 0.02em;
    }
    .sidebar-section-label {
        font-size: 10px;
        text-transform: uppercase;
        letter-spacing: .14em;
        color: #525252 !important;
        margin: 28px 0 10px 0;
        font-weight: 600;
    }

    /* ── "New chat" button ── */
    div[data-testid="stSidebar"] div[data-testid="stButton"]:first-of-type button {
        background: #ffffff !important;
        color: #171717 !important;
        font-weight: 600 !important;
        border: none !important;
        border-radius: 0 !important;
        padding: 11px 16px !important;
        font-size: 13px !important;
        letter-spacing: 0.04em;
        text-transform: uppercase;
    }
    div[data-testid="stSidebar"] div[data-testid="stButton"]:first-of-type button:hover {
        background: #e5e5e5 !important;
    }

    /* ── Active conversation ── */
    div[class*="st-key-conv_current"] button {
        background: #262626 !important;
        border-color: #525252 !important;
        color: #ffffff !important;
        font-weight: 500 !important;
        border-left: 3px solid #ffffff !important;
    }
    div[class*="st-key-conv_current"] button:hover {
        background: #333333 !important;
    }

    .sidebar-count {
        text-align: left;
        font-size: 11px;
        color: #525252 !important;
        padding: 8px 0;
        font-weight: 400;
        font-family: 'IBM Plex Mono', monospace;
        letter-spacing: 0.02em;
    }

    /* ══════════════════════════════════════════════
       HEADER BAR
       ══════════════════════════════════════════════ */
    .header-bar {
        border-bottom: 1px solid var(--border);
        padding: 20px 0 18px 0;
        margin-bottom: 24px;
    }
    .header-bar-inner {
        display: flex;
        align-items: center;
        gap: 16px;
    }
    .header-mark {
        width: 44px; height: 44px;
        background: var(--ink);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 18px;
        flex-shrink: 0;
    }
    .header-mark span { color: #ffffff !important; }
    .header-text h1, .header-text h1 * { color: var(--ink) !important; }
    .header-text h1 {
        font-size: 18px;
        font-weight: 700;
        margin: 0;
        line-height: 1.3;
        letter-spacing: -0.01em;
    }
    .header-text p, .header-text p * { color: var(--gray-4) !important; }
    .header-text p {
        font-size: 13px;
        margin: 3px 0 0 0;
        font-weight: 400;
    }

    /* ══════════════════════════════════════════════
       CHAT MESSAGES
       ══════════════════════════════════════════════ */

    /* ── User message ── */
    .msg-user {
        padding: 16px 20px;
        line-height: 1.7;
        font-size: 14.5px;
        font-weight: 400;
        background: var(--ink);
        color: #ffffff !important;
        border-radius: 0;
    }
    .msg-user, .msg-user * { color: #ffffff !important; }

    /* ── Assistant message ── */
    .msg-assistant {
        padding: 20px 24px;
        line-height: 1.8;
        font-size: 14.5px;
        font-weight: 400;
        background: var(--bg-alt);
        border: 1px solid var(--border);
        border-left: 3px solid var(--ink);
        border-radius: 0;
    }
    .msg-assistant, .msg-assistant * { color: var(--ink) !important; }

    /* ══════════════════════════════════════════════
       EXPANDER (citations)
       ══════════════════════════════════════════════ */
    div[data-testid="stExpander"],
    div[data-testid="stExpander"] details,
    div[data-testid="stExpander"] summary {
        background: var(--white) !important;
        border-radius: 0 !important;
    }
    div[data-testid="stExpander"] {
        border: 1px solid var(--border) !important;
        border-radius: 0 !important;
        overflow: hidden;
        margin-top: 10px;
    }
    div[data-testid="stExpander"] summary,
    div[data-testid="stExpander"] summary *,
    div[data-testid="stExpander"] summary span,
    div[data-testid="stExpander"] summary p {
        color: var(--ink) !important;
        font-weight: 600 !important;
        font-size: 13px !important;
        letter-spacing: 0.02em;
    }
    div[data-testid="stExpander"] svg { fill: var(--ink) !important; }
    div[data-testid="stExpanderDetails"],
    div[data-testid="stExpanderDetails"] * {
        color: var(--ink) !important;
        background: var(--white) !important;
    }

    /* ══════════════════════════════════════════════
       CITATION CARDS
       ══════════════════════════════════════════════ */
    .citation-card, .citation-card * { color: var(--ink) !important; }
    .citation-card {
        background: var(--bg-alt) !important;
        border: 1px solid var(--border);
        border-left: 3px solid var(--ink);
        border-radius: 0;
        padding: 10px 14px;
        margin-bottom: 6px;
        font-size: 13px;
        transition: background .12s ease;
    }
    .citation-card:hover {
        background: var(--gray-0) !important;
    }
    .citation-idx {
        display: inline-block;
        background: var(--ink) !important;
        color: #ffffff !important;
        font-weight: 700;
        padding: 1px 8px;
        margin-right: 10px;
        font-size: 11px;
        font-family: 'IBM Plex Mono', monospace;
        letter-spacing: 0.04em;
    }
    .citation-meta, .citation-meta * {
        font-weight: 400;
        font-size: 12.5px;
        color: var(--gray-5) !important;
    }

    /* ══════════════════════════════════════════════
       CHAT INPUT
       ══════════════════════════════════════════════ */
    div[data-testid="stChatInput"] {
        background: var(--white) !important;
        border-radius: 0 !important;
    }
    div[data-testid="stChatInput"] textarea {
        background: var(--white) !important;
        color: var(--ink) !important;
        border-radius: 0 !important;
        border: 1px solid var(--border) !important;
        font-family: 'IBM Plex Sans', sans-serif !important;
        font-size: 14.5px !important;
        padding: 14px 16px !important;
        min-height: 48px !important;
        line-height: 1.5 !important;
    }
    div[data-testid="stChatInput"] textarea:focus {
        border-color: var(--ink) !important;
        box-shadow: none !important;
        outline: none !important;
    }
    div[data-testid="stChatInput"] textarea::placeholder {
        color: var(--gray-3) !important;
        font-weight: 400;
    }
    /* Fix: đảm bảo khung input không che chữ */
    div[data-testid="stChatInput"] {
        padding: 0 !important;
        box-shadow: none !important;
    }
    div[data-testid="stBottom"] {
        background: var(--white) !important;
        border-top: 1px solid var(--border);
    }

    /* ── Spinner ── */
    div[data-testid="stSpinner"], div[data-testid="stSpinner"] * {
        color: var(--gray-4) !important;
        font-weight: 500;
        font-size: 13px;
    }

    /* ══════════════════════════════════════════════
       EMPTY STATE
       ══════════════════════════════════════════════ */
    .welcome-block {
        text-align: center;
        padding: 56px 20px 20px;
    }
    .welcome-mark {
        width: 56px; height: 56px;
        margin: 0 auto 20px;
        background: var(--ink);
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .welcome-mark span {
        color: #ffffff !important;
        font-size: 22px;
        font-weight: 700;
        font-family: 'IBM Plex Mono', monospace;
    }
    .welcome-block h2, .welcome-block h2 * { color: var(--ink) !important; }
    .welcome-block h2 {
        font-size: 20px;
        font-weight: 700;
        margin: 0 0 8px 0;
        letter-spacing: -0.02em;
    }
    .welcome-block .welcome-desc, .welcome-block .welcome-desc * { color: var(--gray-4) !important; }
    .welcome-block .welcome-desc {
        font-size: 14px;
        line-height: 1.6;
        max-width: 480px;
        margin: 0 auto;
    }

    /* ── Topic tags ── */
    .topic-tags {
        display: flex;
        flex-wrap: wrap;
        gap: 0;
        justify-content: center;
        margin: 24px auto 0;
        max-width: 560px;
    }
    .topic-tag, .topic-tag * { color: var(--gray-5) !important; }
    .topic-tag {
        background: transparent !important;
        border: 1px solid var(--border);
        padding: 6px 14px;
        font-size: 12px;
        font-weight: 500;
        letter-spacing: 0.02em;
        margin: -0.5px;
    }

    /* ── Section divider ── */
    .section-divider {
        display: flex;
        align-items: center;
        gap: 12px;
        margin: 32px 0 16px;
    }
    .section-divider::before, .section-divider::after {
        content: '';
        flex: 1;
        height: 1px;
        background: var(--border);
    }
    .section-divider-text, .section-divider-text * {
        color: var(--gray-3) !important;
    }
    .section-divider-text {
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        white-space: nowrap;
    }

    /* ── Suggestion buttons ── */
    div[class*="st-key-suggestion_"] { position: relative; z-index: 1; }
    div[class*="st-key-suggestion_"] button {
        background: var(--white) !important;
        color: var(--ink) !important;
        border: 1px solid var(--border) !important;
        border-radius: 0 !important;
        text-align: left !important;
        padding: 16px 18px !important;
        font-size: 13.5px !important;
        font-weight: 400 !important;
        width: 100%;
        transition: all .12s ease;
        line-height: 1.5 !important;
    }
    div[class*="st-key-suggestion_"] button:hover,
    div[class*="st-key-suggestion_"] button:focus {
        border-color: var(--ink) !important;
        background: var(--bg-alt) !important;
        color: var(--ink) !important;
        z-index: 5;
        position: relative;
    }
    div[class*="st-key-suggestion_"] button:active {
        background: var(--gray-0) !important;
    }

    /* ══════════════════════════════════════════════
       DISCLAIMER
       ══════════════════════════════════════════════ */
    .disclaimer-bar, .disclaimer-bar * { color: var(--gray-3) !important; }
    .disclaimer-bar {
        text-align: center;
        font-size: 11px;
        padding: 20px 0 6px 0;
        border-top: 1px solid var(--border-soft);
        margin-top: 20px;
        font-weight: 400;
        letter-spacing: 0.01em;
    }

    /* ══════════════════════════════════════════════
       CHAT AVATAR OVERRIDES
       ══════════════════════════════════════════════ */
    /* Ẩn avatar mặc định của Streamlit, dùng avatar custom trong bubble */
    div[data-testid="stChatMessage"] img[data-testid="chatAvatarIcon-assistant"],
    div[data-testid="stChatMessage"] img[data-testid="chatAvatarIcon-user"] {
        display: none !important;
    }

    /* Custom avatar styling */
    .avatar-box {
        width: 28px; height: 28px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-size: 12px;
        font-weight: 700;
        font-family: 'IBM Plex Mono', monospace;
        flex-shrink: 0;
        margin-bottom: 6px;
        letter-spacing: 0.02em;
    }
    .avatar-user {
        background: var(--ink);
        color: #ffffff !important;
    }
    .avatar-user * { color: #ffffff !important; }
    .avatar-bot {
        background: transparent;
        border: 2px solid var(--ink);
        color: var(--ink) !important;
    }
    .avatar-bot * { color: var(--ink) !important; }

    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# Load agent 1 lần duy nhất
# ============================================================
@st.cache_resource(show_spinner="Đang khởi tạo mô hình...")
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
    ("01", "Điều kiện để kết hôn hợp pháp tại Việt Nam là gì?"),
    ("02", "Thủ tục ly hôn thuận tình cần những giấy tờ gì?"),
    ("03", "Tài sản chung và tài sản riêng trong hôn nhân được xác định thế nào?"),
    ("04", "Quyền nuôi con sau khi ly hôn được quy định ra sao?"),
]

# ============================================================
# Sidebar
# ============================================================
with st.sidebar:
    st.markdown(
        '<div class="sidebar-brand">'
        '<div class="sidebar-brand-mark">§</div>'
        'HNGĐ Legal'
        '</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="sidebar-sub">Luật Hôn nhân &amp; Gia đình</div>',
        unsafe_allow_html=True,
    )

    if st.button("＋  Cuộc trò chuyện mới", use_container_width=True):
        new_conversation()
        st.rerun()

    st.markdown(
        '<div class="sidebar-section-label">Lịch sử</div>',
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
        prefix = "▸ " if is_current else "  "
        label = prefix + conv["title"]
        with st.container(key=row_key):
            col_main, col_del = st.columns([5, 1])
            with col_main:
                if st.button(label, key=f"conv_{conv_id}", use_container_width=True):
                    st.session_state.current_conv_id = conv_id
                    st.rerun()
            with col_del:
                if st.button("×", key=f"del_{conv_id}", help="Xóa"):
                    delete_conversation(conv_id)
                    st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        f'<div class="sidebar-count">{len(st.session_state.conversations)} conversations</div>',
        unsafe_allow_html=True,
    )

current_conv_id = st.session_state.current_conv_id
current_conv = st.session_state.conversations[current_conv_id]


def render_citations(citations):
    if not citations:
        return
    with st.expander(f"Trích dẫn pháp lý — {len(citations)} nguồn"):
        for c in citations:
            meta = c["metadata"]
            st.markdown(
                f'<div class="citation-card">'
                f'<span class="citation-idx">{c["index"]}</span>'
                f'<span class="citation-meta">{meta.get("source", "")} · '
                f'Điều {meta.get("dieu", "?")} · Khoản {meta.get("khoan", "?")}</span>'
                f'</div>',
                unsafe_allow_html=True,
            )


# ============================================================
# Header
# ============================================================
st.markdown(
    """
    <div class="header-bar">
        <div class="header-bar-inner">
            <div class="header-mark"><span>§</span></div>
            <div class="header-text">
                <h1>Trợ lý Luật Hôn nhân &amp; Gia đình</h1>
                <p>Hỏi đáp dựa trên văn bản pháp luật · Trích dẫn điều khoản cụ thể</p>
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
    st.markdown(
        """
        <div class="welcome-block">
            <div class="welcome-mark"><span>§</span></div>
            <h2>Bạn cần tư vấn vấn đề gì?</h2>
            <p class="welcome-desc">
                Đặt câu hỏi về Luật Hôn nhân và Gia đình — hệ thống sẽ tra cứu
                văn bản luật và trả lời kèm trích dẫn điều khoản.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="topic-tags">
            <span class="topic-tag">Kết hôn</span>
            <span class="topic-tag">Ly hôn</span>
            <span class="topic-tag">Tài sản</span>
            <span class="topic-tag">Nuôi con</span>
            <span class="topic-tag">Cấp dưỡng</span>
            <span class="topic-tag">Con nuôi</span>
            <span class="topic-tag">Giám hộ</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-divider"><span class="section-divider-text">Câu hỏi mẫu</span></div>',
        unsafe_allow_html=True,
    )

    cols = st.columns(2)
    for i, (num, q) in enumerate(EXAMPLE_QUESTIONS):
        with cols[i % 2]:
            with st.container(key=f"suggestion_{i}"):
                if st.button(
                    f"{num}  {q}",
                    key=f"suggestion_btn_{i}",
                    use_container_width=True,
                ):
                    st.session_state.pending_question = q

for msg in current_conv["messages"]:
    role = msg["role"]
    with st.chat_message(role):
        if role == "user":
            st.markdown(
                '<div class="avatar-box avatar-user">Bạn</div>'
                f'<div class="msg-user">{msg["content"]}</div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                '<div class="avatar-box avatar-bot">§</div>'
                f'<div class="msg-assistant">{msg["content"]}</div>',
                unsafe_allow_html=True,
            )
        if msg.get("citations"):
            render_citations(msg["citations"])

# Câu hỏi từ gợi ý (nếu có) hoặc từ ô nhập
question = st.chat_input("Nhập câu hỏi của bạn...")
if st.session_state.pending_question:
    question = st.session_state.pending_question
    st.session_state.pending_question = None

if question:
    if not current_conv["messages"]:
        title = question.strip()
        current_conv["title"] = title[:40] + ("..." if len(title) > 40 else "")

    current_conv["messages"].append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(
            '<div class="avatar-box avatar-user">Bạn</div>'
            f'<div class="msg-user">{question}</div>',
            unsafe_allow_html=True,
        )

    with st.chat_message("assistant"):
        with st.spinner("Đang tra cứu văn bản luật..."):
            try:
                final_state = agent.run(question, thread_id=current_conv_id)
                answer = final_state.get("answer", "Xin lỗi, tôi chưa có câu trả lời.")
                citations = final_state.get("citations", [])
            except Exception as e:
                answer = f"Đã có lỗi xảy ra: {e}"
                citations = []

        st.markdown(
            '<div class="avatar-box avatar-bot">§</div>'
            f'<div class="msg-assistant">{answer}</div>',
            unsafe_allow_html=True,
        )
        render_citations(citations)

    current_conv["messages"].append(
        {"role": "assistant", "content": answer, "citations": citations}
    )
    st.rerun()

st.markdown(
    '<div class="disclaimer-bar">'
    'Thông tin chỉ mang tính tham khảo — không thay thế tư vấn pháp lý chính thức.'
    '</div>',
    unsafe_allow_html=True,
)