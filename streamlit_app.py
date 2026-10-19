import os
import uuid
import html
from datetime import datetime

import streamlit as st

from agent.graph import HNGDAgentGraph

# ============================================================
# Cấu hình trang (Không dùng icon)
# ============================================================
st.set_page_config(
    page_title="Trợ lý Luật Hôn nhân & Gia đình",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----- API key -----
if "GOOGLE_API_KEY" in st.secrets:
    os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]

# ============================================================
# CSS — Editorial Stone & Deep Forest · 100% Square Corners · No Icons
# ============================================================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap');

    /* ── Ép toàn bộ giao diện góc vuông 0px & Khử hoàn toàn màu tím mặc định ── */
    *, *::before, *::after {
        border-radius: 0px !important;
        box-shadow: none;
    }

    :root, .stApp {
        --primary-color: #1E3A34 !important;
        --background-color: #F6F5F0 !important;
        --secondary-background-color: #ECEAE2 !important;
        --text-color: #141413 !important;
        color-scheme: light !important;
    }

    html, body, [class*="css"] {
        font-family: 'IBM Plex Sans', -apple-system, BlinkMacSystemFont, sans-serif;
        background-color: #F6F5F0 !important;
        color: #141413 !important;
    }

    .stApp {
        background: #F6F5F0 !important;
    }

    #MainMenu, footer, header {
        visibility: hidden !important;
    }

    /* ── Cột nội dung chính căn giữa chuẩn Claude / Gemini ── */
    .main .block-container {
        max-width: 800px !important;
        padding-top: 28px !important;
        padding-bottom: 140px !important;
        padding-left: 24px !important;
        padding-right: 24px !important;
        margin: 0 auto !important;
    }

    /* ── Scrollbar vuông tối giản ── */
    ::-webkit-scrollbar { width: 5px; height: 5px; }
    ::-webkit-scrollbar-track { background: #ECEAE2; }
    ::-webkit-scrollbar-thumb { background: #C4C0B6; }
    ::-webkit-scrollbar-thumb:hover { background: #1E3A34; }

    /* ══════════════════════════════════════════════
       SIDEBAR — Tông xám đá ấm, thuần Typography
       ══════════════════════════════════════════════ */
    section[data-testid="stSidebar"] {
        background: #ECEAE2 !important;
        border-right: 1px solid #D5D1C8 !important;
    }
    section[data-testid="stSidebar"] * {
        color: #141413 !important;
    }

    .sidebar-brand-box {
        padding: 4px 0 18px 0;
        border-bottom: 2px solid #141413;
        margin-bottom: 20px;
    }
    .sidebar-brand-code {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 10px;
        font-weight: 600;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        color: #1E3A34 !important;
        margin-bottom: 4px;
    }
    .sidebar-brand-title {
        font-size: 15px;
        font-weight: 700;
        letter-spacing: 0.03em;
        text-transform: uppercase;
        color: #141413 !important;
    }
    .sidebar-brand-desc {
        font-size: 11.5px;
        color: #5C5A55 !important;
        margin-top: 2px;
    }

    /* ── Nút "Cuộc trò chuyện mới" — Góc vuông, xanh rêu đậm ── */
    div[data-testid="stSidebar"] div[data-testid="stButton"]:first-of-type button {
        background: #1E3A34 !important;
        color: #FFFFFF !important;
        font-weight: 600 !important;
        border: 1px solid #1E3A34 !important;
        padding: 11px 14px !important;
        font-size: 12px !important;
        letter-spacing: 0.08em !important;
        text-transform: uppercase !important;
        transition: background 0.15s ease !important;
    }
    div[data-testid="stSidebar"] div[data-testid="stButton"]:first-of-type button * {
        color: #FFFFFF !important;
    }
    div[data-testid="stSidebar"] div[data-testid="stButton"]:first-of-type button:hover {
        background: #142824 !important;
        border-color: #142824 !important;
    }

    .sidebar-section-header {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 10px;
        text-transform: uppercase;
        letter-spacing: 0.14em;
        color: #6E6C66 !important;
        margin: 26px 0 10px 0;
        font-weight: 600;
        border-bottom: 1px solid #D5D1C8;
        padding-bottom: 6px;
    }

    /* ── Nút danh sách hội thoại trong Sidebar ── */
    section[data-testid="stSidebar"] .stButton button {
        background: transparent !important;
        border: 1px solid transparent !important;
        text-align: left !important;
        font-size: 13px !important;
        font-weight: 400 !important;
        padding: 8px 10px !important;
        color: #383734 !important;
        transition: all 0.12s ease !important;
    }
    section[data-testid="stSidebar"] .stButton button:hover {
        background: #E2DFD5 !important;
        border-color: #C8C4B8 !important;
        color: #141413 !important;
    }

    /* ── Hội thoại đang chọn ── */
    div[class*="st-key-conv_current"] button {
        background: #FFFFFF !important;
        border: 1px solid #141413 !important;
        border-left: 3px solid #1E3A34 !important;
        color: #141413 !important;
        font-weight: 600 !important;
    }

    .sidebar-footer-info {
        font-size: 11px;
        color: #6E6C66 !important;
        font-family: 'IBM Plex Mono', monospace;
        padding: 16px 0 0 0;
        border-top: 1px solid #D5D1C8;
        margin-top: 20px;
    }

    /* ══════════════════════════════════════════════
       HEADER TRÊN CÙNG — KHỐI CHỮ NHẬT GÓC VUÔNG
       ══════════════════════════════════════════════ */
    .header-rectangle {
        background: #FFFFFF;
        border: 1px solid #D5D1C8;
        border-left: 4px solid #1E3A34;
        padding: 18px 22px;
        margin-bottom: 32px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .header-title-box h1 {
        font-size: 15.5px;
        font-weight: 700;
        letter-spacing: 0.04em;
        text-transform: uppercase;
        margin: 0;
        color: #141413 !important;
    }
    .header-title-box p {
        font-size: 12.5px;
        color: #5C5A55 !important;
        margin: 4px 0 0 0;
    }
    .header-badge {
        font-size: 10.5px;
        font-weight: 600;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        padding: 5px 10px;
        background: #ECEAE2;
        border: 1px solid #C8C4B8;
        color: #1E3A34 !important;
        font-family: 'IBM Plex Mono', monospace;
        flex-shrink: 0;
    }

    /* ══════════════════════════════════════════════
       KHU VỰC TRÒ CHUYỆN (PHONG CÁCH CLAUDE / GEMINI)
       ══════════════════════════════════════════════ */

    /* ── Câu hỏi của người dùng: Khối góc vuông căn phải ── */
    .user-msg-row {
        display: flex;
         flex-direction: column;
        align-items: flex-end;
        width: 100%;
        margin: 28px 0 24px 0;
    }
    .user-msg-label {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 10px;
        font-weight: 600;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: #6E6C66;
        margin-bottom: 6px;
    }
    .user-msg-box {
        background: #EAE7DF;
        color: #141413 !important;
        padding: 14px 18px;
        border: 1px solid #D5D1C8;
        border-right: 3px solid #1E3A34;
        max-width: 78%;
        font-size: 15px;
        line-height: 1.6;
        word-break: break-word;
    }

    /* ── Câu trả lời của AI: Trải phẳng trên trang, không đóng hộp ── */
    .bot-label-bar {
        display: flex;
        align-items: center;
        gap: 8px;
        margin-top: 8px;
        margin-bottom: 10px;
        padding-bottom: 6px;
        border-bottom: 1px solid #E2DFD5;
    }
    .bot-square-marker {
        width: 7px;
        height: 7px;
        background: #1E3A34;
        display: inline-block;
    }
    .bot-label-text {
        font-family: 'IBM Plex Mono', monospace;
        color: #1E3A34 !important;
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 0.1em;
        text-transform: uppercase;
    }

    /* Định dạng văn bản trả lời */
    .stMarkdown p {
        font-size: 15.5px;
        line-height: 1.78;
        color: #141413 !important;
        margin-bottom: 14px;
    }
    .stMarkdown ul, .stMarkdown ol {
        margin: 8px 0 16px 22px;
        color: #141413 !important;
    }
    .stMarkdown li {
        font-size: 15.5px;
        line-height: 1.75;
        margin-bottom: 6px;
        color: #141413 !important;
    }
    .stMarkdown strong {
        color: #000000 !important;
        font-weight: 600;
    }

    /* ── Trích dẫn căn cứ pháp lý (Expander góc vuông) ── */
    div[data-testid="stExpander"] {
        background: #FFFFFF !important;
        border: 1px solid #D5D1C8 !important;
        margin-top: 14px !important;
        margin-bottom: 28px !important;
    }
    div[data-testid="stExpander"] summary {
        background: #ECEAE2 !important;
        padding: 9px 14px !important;
    }
    div[data-testid="stExpander"] summary span,
    div[data-testid="stExpander"] summary p {
        font-family: 'IBM Plex Mono', monospace !important;
        color: #141413 !important;
        font-size: 11.5px !important;
        font-weight: 600 !important;
        letter-spacing: 0.04em !important;
        text-transform: uppercase !important;
    }
    div[data-testid="stExpanderDetails"] {
        background: #FFFFFF !important;
        border-top: 1px solid #D5D1C8 !important;
        padding: 12px 16px !important;
    }

    .citation-item {
        display: flex;
        align-items: baseline;
        gap: 10px;
        padding: 7px 0;
        border-bottom: 1px solid #ECEAE2;
        font-size: 13px;
        color: #2C2B29 !important;
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
        font-family: 'IBM Plex Mono', monospace;
        padding: 1px 6px;
        flex-shrink: 0;
    }

    /* ══════════════════════════════════════════════
       KHUNG NHẬP LIỆU (CHAT INPUT) — KIỂU CLAUDE GÓC VUÔNG
       ══════════════════════════════════════════════ */
    div[data-testid="stBottom"] {
        background: linear-gradient(180deg, rgba(246, 245, 240, 0) 0%, #F6F5F0 30%, #F6F5F0 100%) !important;
        border-top: none !important;
        padding-bottom: 22px !important;
    }

    div[data-testid="stChatInput"] {
        max-width: 800px !important;
        margin: 0 auto !important;
        background: #FFFFFF !important;
        border: 1px solid #B8B3A8 !important;
        border-top: 2px solid #1E3A34 !important;
        padding: 8px 12px !important;
        box-shadow: 0 6px 20px rgba(20, 20, 19, 0.06) !important;
        transition: border-color 0.15s ease !important;
    }
    div[data-testid="stChatInput"]:focus-within {
        border-color: #1E3A34 !important;
        outline: none !important;
    }

    div[data-testid="stChatInput"] * {
        background: transparent !important;
    }
    div[data-testid="stChatInput"] textarea {
        color: #141413 !important;
        border: none !important;
        box-shadow: none !important;
        font-family: 'IBM Plex Sans', sans-serif !important;
        font-size: 15px !important;
        line-height: 1.5 !important;
        padding: 8px 6px !important;
        outline: none !important;
    }
    div[data-testid="stChatInput"] textarea::placeholder {
        color: #85827A !important;
        font-size: 14.5px !important;
    }

    /* Nút gửi hình vuông sắc nét */
    div[data-testid="stChatInput"] button {
        background: #1E3A34 !important;
        border: 1px solid #1E3A34 !important;
        width: 36px !important;
        height: 36px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        transition: background 0.15s ease !important;
    }
    div[data-testid="stChatInput"] button:hover {
        background: #142824 !important;
    }
    div[data-testid="stChatInput"] button svg {
        fill: #FFFFFF !important;
    }

    /* ── Spinner ── */
    div[data-testid="stSpinner"], div[data-testid="stSpinner"] * {
        color: #5C5A55 !important;
        font-family: 'IBM Plex Mono', monospace !important;
        font-size: 12.5px !important;
    }

    /* ══════════════════════════════════════════════
       MÀN HÌNH CHỜ (EMPTY STATE) — THUẦN CHỮ & KHỐI VUÔNG
       ══════════════════════════════════════════════ */
    .empty-state-wrap {
        padding: 36px 0 20px 0;
        border-bottom: 1px solid #D5D1C8;
        margin-bottom: 24px;
    }
    .empty-state-kicker {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: #1E3A34 !important;
        margin-bottom: 8px;
    }
    .empty-state-title {
        font-size: 22px;
        font-weight: 700;
        letter-spacing: -0.01em;
        margin-bottom: 10px;
        color: #141413 !important;
    }
    .empty-state-desc {
        font-size: 14px;
        color: #5C5A55 !important;
        max-width: 620px;
        margin-bottom: 22px;
        line-height: 1.65;
    }

    .topic-badges {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
    }
    .topic-badge-item {
        background: #ECEAE2;
        border: 1px solid #C8C4B8;
        padding: 5px 12px;
        font-family: 'IBM Plex Mono', monospace;
        font-size: 11.5px;
        color: #2C2B29 !important;
    }

    .suggest-header {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 11px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: #6E6C66;
        margin-bottom: 12px;
    }

    /* ── Nút câu hỏi gợi ý — Hình chữ nhật góc vuông ── */
    div[class*="st-key-suggest_"] button {
        background: #FFFFFF !important;
        color: #141413 !important;
        border: 1px solid #D5D1C8 !important;
        border-left: 3px solid #C8C4B8 !important;
        text-align: left !important;
        padding: 14px 16px !important;
        font-size: 13.5px !important;
        font-weight: 400 !important;
        line-height: 1.5 !important;
        transition: all 0.15s ease !important;
        margin-bottom: 8px !important;
    }
    div[class*="st-key-suggest_"] button:hover {
        background: #ECEAE2 !important;
        border-color: #1E3A34 !important;
        border-left: 3px solid #1E3A34 !important;
        color: #000000 !important;
    }

    .disclaimer-note {
        text-align: left;
        font-family: 'IBM Plex Mono', monospace;
        font-size: 11px;
        color: #6E6C66 !important;
        margin-top: 32px;
        padding-top: 14px;
        border-top: 1px solid #D5D1C8;
        line-height: 1.6;
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
    "01 // Điều kiện để kết hôn hợp pháp tại Việt Nam là gì?",
    "02 // Thủ tục ly hôn thuận tình cần những giấy tờ gì?",
    "03 // Tài sản chung và tài sản riêng trong hôn nhân được phân chia ra sao?",
    "04 // Quyền nuôi con dưới 36 tháng tuổi sau khi ly hôn thuộc về ai?",
]

# ============================================================
# Sidebar (Thuần chữ, không icon)
# ============================================================
with st.sidebar:
    st.markdown(
        """
        <div class="sidebar-brand-box">
            <div class="sidebar-brand-code">HỆ THỐNG TRA CỨU</div>
            <div class="sidebar-brand-title">LUẬT HÔN NHÂN &amp; GIA ĐÌNH</div>
            <div class="sidebar-brand-desc">Cơ sở dữ liệu văn bản quy phạm pháp luật</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button("CUỘC TRÒ CHUYỆN MỚI", use_container_width=True):
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
                if st.button("X", key=f"del_{conv_id}", help="Xóa phiên này"):
                    delete_conversation(conv_id)
                    st.rerun()

    st.markdown(
        f'<div class="sidebar-footer-info">TỔNG SỐ PHIÊN: {len(st.session_state.conversations):02d}</div>',
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
# Header trên cùng — Khối chữ nhật góc vuông, không icon
# ============================================================
st.markdown(
    """
    <div class="header-rectangle">
        <div class="header-title-box">
            <h1>TRỢ LÝ PHÁP LÝ LUẬT HÔN NHÂN &amp; GIA ĐÌNH</h1>
            <p>Phân tích tình huống và đối chiếu điều khoản trực tiếp từ văn bản pháp luật Việt Nam</p>
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
    st.markdown(
        """
        <div class="empty-state-wrap">
            <div class="empty-state-kicker">CHẾ ĐỘ TRA CỨU TRỰC TUYẾN</div>
            <div class="empty-state-title">Nhập nội dung hoặc tình huống pháp lý cần giải đáp</div>
            <div class="empty-state-desc">
                Hệ thống hỗ trợ phân tích quy định thuộc Luật Hôn nhân và Gia đình, cung cấp phản hồi kèm theo trích dẫn Điều, Khoản cụ thể.
            </div>
            <div class="topic-badges">
                <span class="topic-badge-item">ĐĂNG KÝ KẾT HÔN</span>
                <span class="topic-badge-item">LY HÔN THUẬN TÌNH / ĐƠN PHƯƠNG</span>
                <span class="topic-badge-item">CHẾ ĐỘ TÀI SẢN VỢ CHỒNG</span>
                <span class="topic-badge-item">QUYỀN NUÔI CON &amp; CẤP DƯỠNG</span>
                <span class="topic-badge-item">NHẬN CON NUÔI</span>
                <span class="topic-badge-item">GIÁM HỘ</span>
            </div>
        </div>
        <div class="suggest-header">CÂU HỎI MẪU THAM KHẢO</div>
        """,
        unsafe_allow_html=True,
    )

    cols = st.columns(2)
    for i, q in enumerate(EXAMPLE_QUESTIONS):
        clean_q = q.split("// ", 1)[1] if "// " in q else q
        with cols[i % 2]:
            with st.container(key=f"suggest_{i}"):
                if st.button(q, key=f"suggest_btn_{i}", use_container_width=True):
                    st.session_state.pending_question = clean_q

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

    with st.spinner("ĐANG ĐỐI CHIẾU CƠ SỞ DỮ LIỆU PHÁP LUẬT..."):
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
        LƯU Ý: Nội dung phản hồi được trích xuất tự động từ văn bản pháp luật hiện hành và chỉ mang tính chất tham khảo thông tin, không thay thế văn bản tư vấn pháp lý chính thức từ Luật sư.
    </div>
    """,
    unsafe_allow_html=True,
)