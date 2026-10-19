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
if "GOOGLE_API_KEY" in st.secrets:
    os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]

# ============================================================
# CSS — Dark Monochrome · Gemini Chat Style · Rectangular Header
# ============================================================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

    /* ── Ép Dark Mode đơn sắc cao cấp toàn hệ thống ── */
    :root, .stApp {
        --background-color: #131314 !important;
        --secondary-background-color: #1e1f20 !important;
        --text-color: #e3e3e3 !important;
        --primary-color: #ffffff !important;
        color-scheme: dark !important;
    }

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
        background-color: #131314 !important;
        color: #e3e3e3 !important;
    }

    /* ── App background ── */
    .stApp {
        background: #131314 !important;
    }

    #MainMenu, footer, header { visibility: hidden !important; }

    /* ── Khung nội dung chính căn giữa chuẩn đọc (reading column) ── */
    .main .block-container {
        max-width: 820px !important;
        padding-top: 24px !important;
        padding-bottom: 120px !important;
        padding-left: 20px !important;
        padding-right: 20px !important;
        margin: 0 auto !important;
    }

    /* ── Scrollbar tối giản ── */
    ::-webkit-scrollbar { width: 5px; height: 5px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: #2e3032; border-radius: 0; }
    ::-webkit-scrollbar-thumb:hover { background: #444746; }

    /* ══════════════════════════════════════════════
       SIDEBAR — Đơn sắc sang trọng
       ══════════════════════════════════════════════ */
    section[data-testid="stSidebar"] {
        background: #18191a !important;
        border-right: 1px solid #262729 !important;
    }
    section[data-testid="stSidebar"] * {
        color: #c4c7c5 !important;
    }

    .sidebar-brand-box {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 4px 0 16px 0;
        border-bottom: 1px solid #262729;
        margin-bottom: 20px;
    }
    .sidebar-logo {
        width: 32px; height: 32px;
        background: #282a2c;
        display: flex;
        align-items: center;
        justify-content: center;
        border: 1px solid #3c4043;
        flex-shrink: 0;
    }
    .sidebar-brand-title {
        font-size: 13.5px;
        font-weight: 700;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        color: #f0f0f0 !important;
    }
    .sidebar-brand-desc {
        font-size: 11px;
        color: #8e918f !important;
    }

    /* ── Nút "Cuộc trò chuyện mới" ── */
    div[data-testid="stSidebar"] div[data-testid="stButton"]:first-of-type button {
        background: #282a2c !important;
        color: #f2f2f2 !important;
        font-weight: 600 !important;
        border: 1px solid #3c4043 !important;
        border-radius: 6px !important;
        padding: 10px 14px !important;
        font-size: 13px !important;
        letter-spacing: 0.02em;
        transition: all 0.15s ease;
    }
    div[data-testid="stSidebar"] div[data-testid="stButton"]:first-of-type button:hover {
        background: #333538 !important;
        border-color: #55585d !important;
        color: #ffffff !important;
    }

    .sidebar-section-header {
        font-size: 10px;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        color: #727775 !important;
        margin: 24px 0 8px 2px;
        font-weight: 700;
    }

    /* ── Nút danh sách đoạn chat ── */
    section[data-testid="stSidebar"] .stButton button {
        background: transparent;
        border: 1px solid transparent;
        border-radius: 6px;
        text-align: left;
        font-size: 13px;
        font-weight: 400;
        padding: 8px 10px;
        color: #c4c7c5 !important;
        transition: background 0.15s ease;
    }
    section[data-testid="stSidebar"] .stButton button:hover {
        background: #232527 !important;
        border-color: #2e3032 !important;
        color: #f0f0f0 !important;
    }

    /* ── Cuộc trò chuyện đang chọn ── */
    div[class*="st-key-conv_current"] button {
        background: #282a2c !important;
        border: 1px solid #3c4043 !important;
        color: #ffffff !important;
        font-weight: 500 !important;
    }

    .sidebar-footer-info {
        font-size: 11px;
        color: #727775 !important;
        font-family: 'JetBrains Mono', monospace;
        padding: 16px 2px 0 2px;
    }

    /* ══════════════════════════════════════════════
       HEADER TRÊN CÙNG — HÌNH CHỮ NHẬT SẮC NÉT
       ══════════════════════════════════════════════ */
    .header-rectangle {
        background: #18191a;
        border: 1px solid #282a2c;
        border-radius: 0px !important; /* Góc vuông hoàn toàn */
        padding: 18px 22px;
        margin-bottom: 24px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .header-left {
        display: flex;
        align-items: center;
        gap: 14px;
    }
    .header-icon-box {
        width: 36px; height: 36px;
        background: #232527;
        border: 1px solid #333538;
        border-radius: 0px !important;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #e3e3e3;
        flex-shrink: 0;
    }
    .header-title-box h1 {
        font-size: 16px;
        font-weight: 700;
        letter-spacing: -0.01em;
        margin: 0;
        color: #f0f0f0 !important;
    }
    .header-title-box p {
        font-size: 12.5px;
        color: #8e918f !important;
        margin: 3px 0 0 0;
    }
    .header-badge {
        font-size: 11px;
        font-weight: 500;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        padding: 4px 10px;
        background: #232527;
        border: 1px solid #333538;
        border-radius: 0px !important;
        color: #a8aba9 !important;
        font-family: 'JetBrains Mono', monospace;
    }

    /* ══════════════════════════════════════════════
       KHU VỰC TRÒ CHUYỆN (CHUẨN CHAT PHỔ BIẾN)
       ══════════════════════════════════════════════ */

    /* ── Người hỏi: Nằm bên PHẢI, bubble gọn gàng ── */
    .user-msg-row {
        display: flex;
        justify-content: flex-end;
        width: 100%;
        margin: 20px 0 24px 0;
    }
    .user-msg-pill {
        background: #2b2d30;
        color: #f3f4f6 !important;
        padding: 11px 18px;
        border-radius: 18px;
        max-width: 75%;
        font-size: 14.5px;
        line-height: 1.6;
        word-break: break-word;
        box-shadow: 0 1px 3px rgba(0,0,0,0.25);
    }

    /* ── Người trả lời: Căn giữa khung, KHÔNG CÓ KHUNG BAO ── */
    .bot-msg-container {
        width: 100%;
        margin-bottom: 30px;
    }
    .bot-label-bar {
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 8px;
        color: #a8aba9 !important;
        font-size: 12.5px;
        font-weight: 600;
        letter-spacing: 0.02em;
    }
    .bot-sparkle-svg {
        width: 15px; height: 15px;
        color: #e3e3e3;
    }
    .bot-msg-content {
        color: #e3e3e3 !important;
        font-size: 15px;
        line-height: 1.75;
        font-weight: 400;
        padding-left: 2px;
    }
    .bot-msg-content p {
        margin-bottom: 12px;
        color: #e3e3e3 !important;
    }
    .bot-msg-content ul, .bot-msg-content ol {
        margin: 8px 0 14px 20px;
        padding: 0;
        color: #e3e3e3 !important;
    }
    .bot-msg-content li {
        margin-bottom: 6px;
        color: #e3e3e3 !important;
    }
    .bot-msg-content strong {
        color: #ffffff !important;
        font-weight: 600;
    }

    /* ── Trích dẫn căn cứ (Expander phẳng, tối giản) ── */
    div[data-testid="stExpander"] {
        background: #18191a !important;
        border: 1px solid #282a2c !important;
        border-radius: 4px !important;
        margin-top: 12px !important;
        margin-bottom: 20px !important;
    }
    div[data-testid="stExpander"] summary {
        background: #18191a !important;
        padding: 8px 12px !important;
    }
    div[data-testid="stExpander"] summary span,
    div[data-testid="stExpander"] summary p {
        color: #8e918f !important;
        font-size: 12.5px !important;
        font-weight: 500 !important;
    }
    div[data-testid="stExpander"] summary:hover span {
        color: #c4c7c5 !important;
    }
    div[data-testid="stExpanderDetails"] {
        background: #18191a !important;
        border-top: 1px solid #282a2c !important;
        padding: 10px 14px !important;
    }

    .citation-item {
        display: flex;
        align-items: baseline;
        gap: 8px;
        padding: 6px 0;
        border-bottom: 1px solid #202224;
        font-size: 12.5px;
        color: #a8aba9 !important;
    }
    .citation-item:last-child {
        border-bottom: none;
    }
    .citation-num {
        display: inline-block;
        background: #282a2c;
        border: 1px solid #3c4043;
        color: #e3e3e3 !important;
        font-size: 11px;
        font-weight: 600;
        font-family: 'JetBrains Mono', monospace;
        padding: 1px 6px;
        border-radius: 3px;
        flex-shrink: 0;
    }

    /* ══════════════════════════════════════════════
       CHAT INPUT — THIẾT KẾ ĐẸP & ĐƠN GIẢN NHƯ GEMINI
       ══════════════════════════════════════════════ */
    div[data-testid="stBottom"] {
        background: linear-gradient(180deg, rgba(19, 19, 20, 0) 0%, #131314 35%, #131314 100%) !important;
        border-top: none !important;
        padding-bottom: 24px !important;
    }

    div[data-testid="stChatInput"] {
        max-width: 820px !important;
        margin: 0 auto !important;
        background: #1e1f20 !important;
        border: 1px solid #333538 !important;
        border-radius: 28px !important;
        padding: 6px 14px !important;
        box-shadow: 0 4px 18px rgba(0, 0, 0, 0.45) !important;
        transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
    }
    div[data-testid="stChatInput"]:focus-within {
        border-color: #55585d !important;
        box-shadow: 0 4px 22px rgba(0, 0, 0, 0.6) !important;
    }

    /* Triệt tiêu triệt để mọi lỗi nền trắng che chữ */
    div[data-testid="stChatInput"] * {
        background: transparent !important;
    }
    div[data-testid="stChatInput"] textarea {
        background: transparent !important;
        color: #f0f0f0 !important;
        border: none !important;
        box-shadow: none !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-size: 15px !important;
        line-height: 1.5 !important;
        padding: 10px 8px !important;
        outline: none !important;
    }
    div[data-testid="stChatInput"] textarea::placeholder {
        color: #8e918f !important;
        font-size: 14.5px !important;
    }

    /* Nút gửi mũi tên tròn tinh tế */
    div[data-testid="stChatInput"] button {
        background: #2b2d30 !important;
        border: 1px solid #444746 !important;
        border-radius: 50% !important;
        width: 34px !important;
        height: 34px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        transition: background 0.15s ease !important;
    }
    div[data-testid="stChatInput"] button:hover {
        background: #3c4043 !important;
    }
    div[data-testid="stChatInput"] button svg {
        fill: #e3e3e3 !important;
    }

    /* ── Spinner ── */
    div[data-testid="stSpinner"], div[data-testid="stSpinner"] * {
        color: #8e918f !important;
        font-size: 13.5px !important;
        font-weight: 400 !important;
    }

    /* ══════════════════════════════════════════════
       EMPTY STATE (TRẠNG THÁI KHI CHƯA CHAT)
       ══════════════════════════════════════════════ */
    .empty-state-wrap {
        text-align: center;
        padding: 50px 16px 20px 16px;
    }
    .empty-state-symbol {
        width: 48px; height: 48px;
        margin: 0 auto 16px;
        background: #1e1f20;
        border: 1px solid #282a2c;
        border-radius: 0px !important;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #e3e3e3;
    }
    .empty-state-title {
        font-size: 19px;
        font-weight: 700;
        letter-spacing: -0.01em;
        margin-bottom: 8px;
        color: #f0f0f0 !important;
    }
    .empty-state-desc {
        font-size: 13.5px;
        color: #8e918f !important;
        max-width: 480px;
        margin: 0 auto 24px;
        line-height: 1.6;
    }

    .topic-badges {
        display: flex;
        flex-wrap: wrap;
        gap: 6px;
        justify-content: center;
        margin-bottom: 28px;
    }
    .topic-badge-item {
        background: #18191a;
        border: 1px solid #282a2c;
        border-radius: 0px !important;
        padding: 5px 12px;
        font-size: 12px;
        color: #a8aba9 !important;
    }

    /* ── Nút câu hỏi gợi ý — Chữ nhật sắc nét ── */
    div[class*="st-key-suggest_"] button {
        background: #18191a !important;
        color: #c4c7c5 !important;
        border: 1px solid #282a2c !important;
        border-radius: 0px !important; /* Góc vuông */
        text-align: left !important;
        padding: 14px 16px !important;
        font-size: 13.5px !important;
        font-weight: 400 !important;
        line-height: 1.5 !important;
        transition: all 0.15s ease !important;
    }
    div[class*="st-key-suggest_"] button:hover {
        background: #232527 !important;
        border-color: #444746 !important;
        color: #ffffff !important;
    }

    .disclaimer-note {
        text-align: center;
        font-size: 11.5px;
        color: #5f6368 !important;
        margin-top: 24px;
        padding-top: 14px;
        border-top: 1px solid #202224;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# Load agent 1 lần duy nhất
# ============================================================
@st.cache_resource(show_spinner="Khởi tạo mô hình...")
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
    "Điều kiện để kết hôn hợp pháp tại Việt Nam là gì?",
    "Thủ tục ly hôn thuận tình cần những giấy tờ gì?",
    "Tài sản chung và tài sản riêng trong hôn nhân được phân chia ra sao?",
    "Quyền nuôi con dưới 36 tháng tuổi sau khi ly hôn thuộc về ai?",
]

# ============================================================
# Sidebar
# ============================================================
with st.sidebar:
    st.markdown(
        """
        <div class="sidebar-brand-box">
            <div class="sidebar-logo">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#e3e3e3" stroke-width="2" stroke-linecap="square">
                    <path d="M12 3v18M6 8l6-5 6 5M4 14l4-6 4 6H4zm12 0l4-6 4 6h-8z"/>
                </svg>
            </div>
            <div>
                <div class="sidebar-brand-title">HNGĐ LEGAL</div>
                <div class="sidebar-brand-desc">Tư vấn pháp lý thông minh</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button("＋  Cuộc trò chuyện mới", use_container_width=True):
        new_conversation()
        st.rerun()

    st.markdown('<div class="sidebar-section-header">Lịch sử tư vấn</div>', unsafe_allow_html=True)

    sorted_convs = sorted(
        st.session_state.conversations.items(),
        key=lambda kv: kv[1]["created_at"],
        reverse=True,
    )

    for conv_id, conv in sorted_convs:
        is_current = conv_id == st.session_state.current_conv_id
        row_key = "conv_current" if is_current else f"conv_row_{conv_id}"
        prefix = "• " if is_current else "  "
        label = prefix + conv["title"]
        with st.container(key=row_key):
            col_main, col_del = st.columns([5, 1])
            with col_main:
                if st.button(label, key=f"conv_{conv_id}", use_container_width=True):
                    st.session_state.current_conv_id = conv_id
                    st.rerun()
            with col_del:
                if st.button("×", key=f"del_{conv_id}", help="Xóa cuộc trò chuyện"):
                    delete_conversation(conv_id)
                    st.rerun()

    st.markdown(
        f'<div class="sidebar-footer-info">{len(st.session_state.conversations)} hội thoại lưu trữ</div>',
        unsafe_allow_html=True,
    )

current_conv_id = st.session_state.current_conv_id
current_conv = st.session_state.conversations[current_conv_id]


def render_citations(citations):
    if not citations:
        return
    count = len(citations)
    with st.expander(f"Căn cứ pháp lý tham chiếu ({count} nguồn)"):
        for c in citations:
            meta = c.get("metadata", {})
            source = meta.get("source", "Văn bản luật")
            dieu = meta.get("dieu", "?")
            khoan = meta.get("khoan", "")
            khoan_str = f" — Khoản {khoan}" if khoan else ""
            st.markdown(
                f"""
                <div class="citation-item">
                    <span class="citation-num">[{c.get('index', 1)}]</span>
                    <span>{html.escape(source)} — Điều {html.escape(str(dieu))}{html.escape(khoan_str)}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )


# ============================================================
# Header trên cùng — HÌNH CHỮ NHẬT SẮC NÉT
# ============================================================
st.markdown(
    """
    <div class="header-rectangle">
        <div class="header-left">
            <div class="header-icon-box">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="square">
                    <path d="M12 2v20M5 7l7-5 7 5M3 13l4-6 4 6H3zm14 0l4-6 4 6h-8z"/>
                </svg>
            </div>
            <div class="header-title-box">
                <h1>TRỢ LÝ LUẬT HÔN NHÂN &amp; GIA ĐÌNH</h1>
                <p>Hỏi đáp tra cứu căn cứ pháp lý chính xác theo quy định pháp luật Việt Nam</p>
            </div>
        </div>
        <div class="header-badge">VĂN BẢN HIỆN HÀNH</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# Khu vực nội dung chat
# ============================================================
has_messages = len(current_conv["messages"]) > 0

if not has_messages:
    # ── Màn hình chào đón khi chưa có tin nhắn ──
    st.markdown(
        """
        <div class="empty-state-wrap">
            <div class="empty-state-symbol">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
                    <path d="M12 2L14.5 9.5L22 12L14.5 14.5L12 22L9.5 14.5L2 12L9.5 9.5L12 2Z"/>
                </svg>
            </div>
            <div class="empty-state-title">Bạn cần tìm hiểu quy định pháp luật nào?</div>
            <div class="empty-state-desc">
                Nhập câu hỏi liên quan đến Luật Hôn nhân &amp; Gia đình. Trợ lý sẽ phân tích và trích dẫn trực tiếp Điều, Khoản cụ thể từ văn bản luật.
            </div>
            <div class="topic-badges">
                <span class="topic-badge-item">Đăng ký kết hôn</span>
                <span class="topic-badge-item">Thuận tình / Đơn phương ly hôn</span>
                <span class="topic-badge-item">Phân chia tài sản</span>
                <span class="topic-badge-item">Quyền nuôi con &amp; Cấp dưỡng</span>
                <span class="topic-badge-item">Nhận con nuôi</span>
                <span class="topic-badge-item">Giám hộ</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    cols = st.columns(2)
    for i, q in enumerate(EXAMPLE_QUESTIONS):
        with cols[i % 2]:
            with st.container(key=f"suggest_{i}"):
                if st.button(q, key=f"suggest_btn_{i}", use_container_width=True):
                    st.session_state.pending_question = q

# ── Render tin nhắn đã có ──
for msg in current_conv["messages"]:
    role = msg["role"]
    if role == "user":
        # Người hỏi: Căn phải, bong bóng xám đen gọn gàng, không icon rườm rà
        safe_q = html.escape(msg["content"]).replace("\n", "<br>")
        st.markdown(
            f"""
            <div class="user-msg-row">
                <div class="user-msg-pill">{safe_q}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        # Người trả lời: Căn giữa theo khung, KHÔNG CÓ KHUNG BAO bọc quanh, chữ trực tiếp chuẩn markdown
        st.markdown(
            """
            <div class="bot-label-bar">
                <svg class="bot-sparkle-svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M12 2L14.5 9.5L22 12L14.5 14.5L12 22L9.5 14.5L2 12L9.5 9.5L12 2Z"/>
                </svg>
                <span>Trợ lý Pháp lý</span>
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
question = st.chat_input("Nhập câu hỏi về Luật Hôn nhân và Gia đình...")
if st.session_state.pending_question:
    question = st.session_state.pending_question
    st.session_state.pending_question = None

if question:
    # Cập nhật tiêu đề đoạn chat nếu là câu hỏi đầu tiên
    if not current_conv["messages"]:
        title = question.strip()
        current_conv["title"] = title[:35] + ("..." if len(title) > 35 else "")

    # Thêm câu hỏi người dùng
    current_conv["messages"].append({"role": "user", "content": question})

    # Render ngay câu hỏi của user
    safe_q = html.escape(question).replace("\n", "<br>")
    st.markdown(
        f"""
        <div class="user-msg-row">
            <div class="user-msg-pill">{safe_q}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Bot xử lý và trả lời
    st.markdown(
        """
        <div class="bot-label-bar">
            <svg class="bot-sparkle-svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M12 2L14.5 9.5L22 12L14.5 14.5L12 22L9.5 14.5L2 12L9.5 9.5L12 2Z"/>
            </svg>
            <span>Trợ lý Pháp lý</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.spinner("Đang tra cứu văn bản luật..."):
        try:
            final_state = agent.run(question, thread_id=current_conv_id)
            answer = final_state.get("answer", "Xin lỗi, hiện tại tôi chưa tìm thấy căn cứ pháp lý phù hợp trong kho dữ liệu.")
            citations = final_state.get("citations", [])
        except Exception as e:
            err_str = str(e)
            if "503" in err_str or "high demand" in err_str or "UNAVAILABLE" in err_str:
                answer = "Hệ thống AI hiện đang chịu tải cao đột biến (503). Vui lòng gửi lại câu hỏi sau vài giây."
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
        Thông tin phản hồi dựa trên văn bản pháp luật hiện hành và chỉ mang tính chất tham khảo, không thay thế văn bản pháp lý chính thức hoặc tư vấn từ Luật sư.
    </div>
    """,
    unsafe_allow_html=True,
)