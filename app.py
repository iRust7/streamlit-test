import streamlit as st
from datetime import datetime
from FSM import FSM

st.set_page_config(
    page_title="Perpustakaan Digital",
    page_icon="📚",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────────────────────────────────
# STYLES
# ──────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* ── Base ─────────────────────────────────────────────── */
    .stApp {
        background:
            radial-gradient(circle at 0% 0%,   #EFE3D0 0%, transparent 40%),
            radial-gradient(circle at 100% 0%, #E8DCC4 0%, transparent 40%),
            #F7F1E6;
    }
    html, body, [class*="css"] {
        font-family: 'Inter', 'Segoe UI', system-ui, sans-serif;
    }
    #MainMenu, footer, header { visibility: hidden; }
    .block-container { padding-top: 1.5rem; padding-bottom: 6rem; }

    /* ── Header ───────────────────────────────────────────── */
    .lib-header {
        background: linear-gradient(135deg, #4E342E 0%, #6D4C41 50%, #8D6E63 100%);
        color: white;
        padding: 1.4rem 1.6rem;
        border-radius: 16px;
        margin-bottom: 1rem;
        box-shadow: 0 8px 24px rgba(78,52,46,0.18);
        position: relative;
        overflow: hidden;
    }
    .lib-header::after {
        content: "";
        position: absolute;
        top: -40%; right: -10%;
        width: 220px; height: 220px;
        background: rgba(255,255,255,0.06);
        border-radius: 50%;
    }
    .lib-header h1 {
        margin: 0;
        font-size: 1.65rem;
        font-weight: 700;
        letter-spacing: -0.02em;
        display: flex; align-items: center; gap: 0.5rem;
    }
    .lib-header p {
        margin: 0.3rem 0 0;
        font-size: 0.85rem;
        opacity: 0.85;
    }
    .header-meta {
        position: absolute; top: 1rem; right: 1.2rem;
        display: flex; align-items: center; gap: 0.4rem;
        font-size: 0.72rem; opacity: 0.85;
    }
    .pulse-dot {
        width: 8px; height: 8px; border-radius: 50%;
        background: #7CFC9C;
        box-shadow: 0 0 0 0 rgba(124,252,156,0.7);
        animation: pulse 1.8s infinite;
    }
    @keyframes pulse {
        0%   { box-shadow: 0 0 0 0 rgba(124,252,156,0.7); }
        70%  { box-shadow: 0 0 0 8px rgba(124,252,156,0); }
        100% { box-shadow: 0 0 0 0 rgba(124,252,156,0); }
    }

    /* ── Stats row ───────────────────────────────────────── */
    .stats-row {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 0.6rem;
        margin-bottom: 1rem;
    }
    .stat-card {
        background: white;
        border: 1px solid #E5D9C7;
        border-radius: 12px;
        padding: 0.7rem 0.9rem;
        box-shadow: 0 2px 6px rgba(78,52,46,0.05);
    }
    .stat-card .label {
        font-size: 0.7rem;
        color: #8D6E63;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        font-weight: 600;
    }
    .stat-card .value {
        font-size: 1.4rem;
        color: #3E2723;
        font-weight: 700;
        margin-top: 0.15rem;
    }

    /* ── Chat bubbles ─────────────────────────────────────── */
    .msg-row {
        display: flex;
        align-items: flex-end;
        gap: 0.5rem;
        margin: 0.5rem 0;
        animation: fadeUp 0.28s ease-out;
    }
    .msg-row.user { justify-content: flex-end; }
    @keyframes fadeUp {
        from { opacity: 0; transform: translateY(6px); }
        to   { opacity: 1; transform: translateY(0); }
    }
    .avatar {
        width: 32px; height: 32px;
        border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        font-size: 0.95rem;
        flex-shrink: 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.08);
    }
    .avatar.bot  { background: linear-gradient(135deg,#8D6E63,#5D4037); color: white; }
    .avatar.user { background: linear-gradient(135deg,#3E2723,#5D4037); color: white; }

    .bubble-user {
        background: linear-gradient(135deg, #5D4037, #4E342E);
        color: white;
        padding: 0.7rem 1rem;
        border-radius: 18px 18px 4px 18px;
        max-width: 78%;
        font-size: 0.92rem;
        line-height: 1.45;
        box-shadow: 0 2px 6px rgba(78,52,46,0.18);
    }
    .bubble-bot {
        background: white;
        color: #2c1a0e;
        padding: 0.75rem 1rem;
        border-radius: 18px 18px 18px 4px;
        border: 1px solid #E5D9C7;
        max-width: 82%;
        font-size: 0.92rem;
        line-height: 1.55;
        white-space: pre-line;
        box-shadow: 0 2px 6px rgba(78,52,46,0.06);
    }
    .bubble-bot strong { color: #3E2723; }
    .ts {
        font-size: 0.65rem;
        color: #A1887F;
        margin: 0.1rem 2.5rem 0.4rem;
    }
    .ts.user { text-align: right; margin: 0.1rem 2.5rem 0.4rem 0; }

    /* ── Quick chips ─────────────────────────────────────── */
    .chip-label {
        font-size: 0.7rem;
        color: #8D6E63;
        font-weight: 600;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        margin: 0.6rem 0 0.3rem;
    }
    div[data-testid="stHorizontalBlock"] .stButton > button {
        border-radius: 999px !important;
        background: white !important;
        color: #5D4037 !important;
        border: 1px solid #D7C4A8 !important;
        font-weight: 500 !important;
        font-size: 0.8rem !important;
        padding: 0.35rem 0.9rem !important;
        box-shadow: 0 1px 3px rgba(78,52,46,0.05) !important;
        transition: all 0.18s ease !important;
    }
    div[data-testid="stHorizontalBlock"] .stButton > button:hover {
        background: #5D4037 !important;
        color: white !important;
        border-color: #5D4037 !important;
        transform: translateY(-1px);
        box-shadow: 0 4px 10px rgba(78,52,46,0.18) !important;
    }

    /* ── Sidebar ─────────────────────────────────────────── */
    [data-testid="stSidebar"] {
        background: #FBF6EC;
        border-right: 1px solid #E5D9C7;
    }
    .state-pill {
        display: inline-block;
        padding: 0.25rem 0.8rem;
        border-radius: 999px;
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 0.06em;
    }
    .state-desc {
        font-size: 0.78rem;
        color: #6D4C41;
        margin-top: 0.4rem;
        line-height: 1.4;
    }
    .tip-card {
        background: white;
        border-left: 3px solid #8D6E63;
        border-radius: 8px;
        padding: 0.5rem 0.7rem;
        margin-bottom: 0.4rem;
        font-size: 0.78rem;
        color: #3E2723;
        transition: all 0.18s ease;
    }
    .tip-card:hover {
        border-left-color: #5D4037;
        background: #FFF8EE;
        transform: translateX(2px);
    }
    .tip-card b { color: #4E342E; }
    .tip-card .desc { color: #8D6E63; font-size: 0.72rem; margin-top: 0.1rem; }

    /* sidebar reset button */
    [data-testid="stSidebar"] .stButton > button {
        width: 100% !important;
        border-radius: 10px !important;
        background: #5D4037 !important;
        color: white !important;
        border: none !important;
        font-weight: 600 !important;
        padding: 0.55rem !important;
    }
    [data-testid="stSidebar"] .stButton > button:hover {
        background: #4E342E !important;
        transform: none;
    }

    /* ── Chat input ──────────────────────────────────────── */
    [data-testid="stChatInput"] {
        background: transparent !important;
    }
    [data-testid="stChatInput"] textarea {
        border-radius: 14px !important;
        border: 2px solid #D7C4A8 !important;
        background: white !important;
    }
    [data-testid="stChatInput"] textarea:focus {
        border-color: #5D4037 !important;
        box-shadow: 0 0 0 3px rgba(93,64,55,0.12) !important;
    }

    /* scrollbar */
    ::-webkit-scrollbar { width: 8px; }
    ::-webkit-scrollbar-thumb { background: #D7C4A8; border-radius: 4px; }
    ::-webkit-scrollbar-thumb:hover { background: #8D6E63; }
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────
# STATE
# ──────────────────────────────────────────────────────────────────────────
if "fsm" not in st.session_state:
    st.session_state.fsm = FSM()
if "history" not in st.session_state:
    st.session_state.history = []
if "queued_input" not in st.session_state:
    st.session_state.queued_input = None


def send_message(text: str):
    text = text.strip()
    if not text:
        return
    now = datetime.now().strftime("%H:%M")
    st.session_state.history.append({"role": "user", "text": text, "ts": now})
    reply = st.session_state.fsm.transition(text)
    st.session_state.history.append({
        "role": "bot",
        "text": reply,
        "ts": datetime.now().strftime("%H:%M"),
    })


# ──────────────────────────────────────────────────────────────────────────
# HEADER
# ──────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="lib-header">
    <div class="header-meta"><span class="pulse-dot"></span> online</div>
    <h1>📚 Perpustakaan Digital</h1>
    <p>Asisten cerdas berbasis FSM — cari, pinjam, dan kelola buku</p>
</div>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────
# STATS
# ──────────────────────────────────────────────────────────────────────────
stats = st.session_state.fsm.engine.get_stats()
st.markdown(f"""
<div class="stats-row">
    <div class="stat-card">
        <div class="label">Total Judul</div>
        <div class="value">{stats['titles']}</div>
    </div>
    <div class="stat-card">
        <div class="label">Stok Tersedia</div>
        <div class="value">{stats['stock']}</div>
    </div>
    <div class="stat-card">
        <div class="label">Kategori</div>
        <div class="value">{stats['categories']}</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ──────────────────────────────────────────────────────────────────────────
STATE_INFO = {
    "DEFAULT": ("#9E9E9E", "Menunggu input pertama"),
    "ACTIVE":  ("#5D4037", "Siap menerima perintah"),
    "BROWSE":  ("#1565C0", "Sedang mencari buku"),
    "BORROW":  ("#2E7D32", "Menunggu judul buku"),
    "CONFIRM": ("#E65100", "Menunggu konfirmasi"),
    "END":     ("#6A1B9A", "Sesi telah selesai"),
}

with st.sidebar:
    st.markdown("### Status FSM")
    cur = st.session_state.fsm.state
    col, desc = STATE_INFO.get(cur, ("#5D4037", ""))
    st.markdown(
        f'<span class="state-pill" '
        f'style="background:{col}1F;color:{col};border:1px solid {col}66">'
        f'● {cur}</span>'
        f'<div class="state-desc">{desc}</div>',
        unsafe_allow_html=True,
    )

    st.markdown("---")
    st.markdown("**Perintah yang dikenali**")
    tips = [
        ("halo", "Mulai percakapan"),
        ("cari [judul/kategori]", "Cari buku"),
        ("katalog", "Lihat semua buku"),
        ("kategori", "Lihat kategori"),
        ("pinjam [judul]", "Pinjam buku"),
        ("stok [judul]", "Cek ketersediaan"),
        ("jam buka", "Jam operasional"),
        ("syarat pinjam", "Ketentuan"),
        ("denda", "Info denda"),
        ("reset", "Mulai dari awal"),
    ]
    for cmd, d in tips:
        st.markdown(
            f'<div class="tip-card"><b>{cmd}</b>'
            f'<div class="desc">{d}</div></div>',
            unsafe_allow_html=True,
        )

    st.markdown("---")
    if st.button("🔄 Reset Percakapan"):
        st.session_state.fsm = FSM()
        st.session_state.history = []
        st.rerun()

# ──────────────────────────────────────────────────────────────────────────
# OPENING
# ──────────────────────────────────────────────────────────────────────────
if not st.session_state.history:
    opening = st.session_state.fsm.transition("halo")
    st.session_state.history.append({
        "role": "bot",
        "text": opening,
        "ts": datetime.now().strftime("%H:%M"),
    })

# ──────────────────────────────────────────────────────────────────────────
# CHAT
# ──────────────────────────────────────────────────────────────────────────
for msg in st.session_state.history:
    ts = msg.get("ts", "")
    if msg["role"] == "user":
        st.markdown(
            f'<div class="msg-row user">'
            f'<div class="bubble-user">{msg["text"]}</div>'
            f'<div class="avatar user">🙂</div>'
            f'</div>'
            f'<div class="ts user">{ts}</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f'<div class="msg-row">'
            f'<div class="avatar bot">📖</div>'
            f'<div class="bubble-bot">{msg["text"]}</div>'
            f'</div>'
            f'<div class="ts">{ts}</div>',
            unsafe_allow_html=True,
        )

# ──────────────────────────────────────────────────────────────────────────
# QUICK CHIPS  — context-aware berdasarkan FSM state
# ──────────────────────────────────────────────────────────────────────────
def render_chips():
    state = st.session_state.fsm.state
    if state == "CONFIRM":
        chips = [("✅ ya", "ya"), ("❌ tidak", "tidak")]
    elif state == "BORROW":
        chips = [("Kalkulus", "kalkulus"),
                 ("Pemrograman Python", "pemrograman python"),
                 ("Batal", "tidak")]
    else:
        chips = [
            ("📚 Katalog",      "katalog"),
            ("🏷️ Kategori",     "kategori"),
            ("🔍 Cari kalkulus", "cari kalkulus"),
            ("🕐 Jam buka",     "jam buka"),
            ("📋 Syarat",       "syarat pinjam"),
        ]

    st.markdown('<div class="chip-label">Saran cepat</div>', unsafe_allow_html=True)
    cols = st.columns(len(chips))
    for i, (label, cmd) in enumerate(chips):
        if cols[i].button(label, key=f"chip_{state}_{i}"):
            st.session_state.queued_input = cmd
            st.rerun()

render_chips()

# ──────────────────────────────────────────────────────────────────────────
# INPUT — chat_input (sticky, enter-to-send)
# ──────────────────────────────────────────────────────────────────────────
user_text = st.chat_input("Ketik pesanmu... (contoh: cari buku kalkulus)")

# proses chip yang ter-queue
if st.session_state.queued_input:
    queued = st.session_state.queued_input
    st.session_state.queued_input = None
    send_message(queued)
    st.rerun()

if user_text:
    send_message(user_text)
    st.rerun()
