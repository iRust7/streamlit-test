import streamlit as st
from FSM import FSM

st.set_page_config(
    page_title="Perpustakaan Digital",
    page_icon="📚",
    layout="centered",
)

st.markdown("""
<style>
    .stApp { background-color: #F5F0E8; }
    html, body, [class*="css"] { font-family: 'Segoe UI', sans-serif; }

    .lib-header {
        background: linear-gradient(135deg, #4E342E, #8D6E63);
        color: white;
        padding: 1.2rem 1.5rem;
        border-radius: 12px;
        margin-bottom: 1rem;
        text-align: center;
    }
    .lib-header h1 { margin: 0; font-size: 1.7rem; }
    .lib-header p  { margin: 0.2rem 0 0; font-size: 0.85rem; opacity: 0.85; }

    .bubble-user {
        background: #5D4037;
        color: white;
        padding: 0.7rem 1rem;
        border-radius: 18px 18px 4px 18px;
        margin: 0.4rem 0 0.4rem 3rem;
        text-align: right;
    }
    .bubble-bot {
        background: white;
        color: #2c1a0e;
        padding: 0.7rem 1rem;
        border-radius: 18px 18px 18px 4px;
        margin: 0.4rem 3rem 0.4rem 0;
        border: 1px solid #D7CCC8;
        white-space: pre-line;
    }
    .state-pill {
        display: inline-block;
        padding: 0.2rem 0.75rem;
        border-radius: 999px;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.05em;
        margin-bottom: 0.5rem;
    }
    .tip-card {
        background: white;
        border-left: 4px solid #8D6E63;
        border-radius: 8px;
        padding: 0.55rem 0.8rem;
        margin-bottom: 0.45rem;
        font-size: 0.82rem;
        color: #333;
    }
    .stTextInput > div > div > input {
        border-radius: 999px !important;
        border: 2px solid #BCAAA4 !important;
        padding: 0.5rem 1rem !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: #5D4037 !important;
        box-shadow: 0 0 0 2px rgba(93,64,55,0.15) !important;
    }
    .stButton > button {
        border-radius: 999px !important;
        background: #5D4037 !important;
        color: white !important;
        border: none !important;
        font-weight: 600 !important;
    }
    .stButton > button:hover {
        background: #4E342E !important;
    }
</style>
""", unsafe_allow_html=True)

if "fsm" not in st.session_state:
    st.session_state.fsm = FSM()

if "history" not in st.session_state:
    st.session_state.history = []

st.markdown("""
<div class="lib-header">
    <h1>📚 Perpustakaan Digital</h1>
    <p>Cari, pinjam, dan kelola buku dengan mudah</p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### Info Sistem")

    state_colors = {
        "DEFAULT": "#9E9E9E",
        "ACTIVE":  "#5D4037",
        "BROWSE":  "#1565C0",
        "BORROW":  "#2E7D32",
        "CONFIRM": "#E65100",
        "END":     "#6A1B9A",
    }
    cur = st.session_state.fsm.state
    col = state_colors.get(cur, "#5D4037")
    st.markdown(
        f'<span class="state-pill" style="background:{col}22;color:{col};border:1px solid {col}88">'
        f'State: {cur}</span>',
        unsafe_allow_html=True
    )

    st.markdown("---")
    st.markdown("**Perintah yang dikenali**")
    tips = [
        ("halo", "Mulai percakapan"),
        ("cari [judul/kategori]", "Cari buku"),
        ("katalog", "Lihat semua buku"),
        ("kategori", "Lihat kategori buku"),
        ("pinjam [judul]", "Pinjam buku"),
        ("kembalikan", "Info cara kembali"),
        ("stok [judul]", "Cek ketersediaan"),
        ("jam buka", "Jam operasional"),
        ("syarat pinjam", "Ketentuan peminjaman"),
        ("denda", "Info denda"),
        ("reset", "Mulai dari awal"),
    ]
    for cmd, desc in tips:
        st.markdown(
            f'<div class="tip-card"><b>{cmd}</b><br>{desc}</div>',
            unsafe_allow_html=True
        )

    st.markdown("---")
    if st.button("Reset Percakapan"):
        st.session_state.fsm = FSM()
        st.session_state.history = []
        st.rerun()

if not st.session_state.history:
    opening = st.session_state.fsm.transition("halo")
    st.session_state.history.append({"role": "bot", "text": opening})

with st.container():
    for msg in st.session_state.history:
        if msg["role"] == "user":
            st.markdown(
                f'<div class="bubble-user">{msg["text"]}</div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f'<div class="bubble-bot">{msg["text"]}</div>',
                unsafe_allow_html=True
            )

st.markdown("---")
col_input, col_btn = st.columns([5, 1])

with col_input:
    user_text = st.text_input(
        label="Pesan",
        placeholder="Contoh: cari buku kalkulus",
        label_visibility="collapsed",
        key="user_input",
    )

with col_btn:
    send = st.button("Kirim")

if send and user_text.strip():
    st.session_state.history.append({"role": "user", "text": user_text.strip()})
    reply = st.session_state.fsm.transition(user_text.strip())
    st.session_state.history.append({"role": "bot", "text": reply})
    st.rerun()
