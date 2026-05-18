import streamlit as st
from datetime import datetime
from FSM import FSM

st.set_page_config(
    page_title="Perpustakaan Digital",
    page_icon="L",
    layout="wide",
    initial_sidebar_state="expanded",
)

ICON_BOT = """<svg viewBox='0 0 24 24' width='18' height='18' fill='none' stroke='currentColor' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><path d='M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1 0-5H20'/></svg>"""
ICON_USER = """<svg viewBox='0 0 24 24' width='16' height='16' fill='none' stroke='currentColor' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><path d='M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2'/><circle cx='12' cy='7' r='4'/></svg>"""
ICON_BOOK = """<svg viewBox='0 0 24 24' width='14' height='14' fill='none' stroke='currentColor' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><path d='M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z'/><path d='M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z'/></svg>"""
ICON_LAYERS = """<svg viewBox='0 0 24 24' width='14' height='14' fill='none' stroke='currentColor' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><polygon points='12 2 2 7 12 12 22 7 12 2'/><polyline points='2 17 12 22 22 17'/><polyline points='2 12 12 17 22 12'/></svg>"""
ICON_TAG = """<svg viewBox='0 0 24 24' width='14' height='14' fill='none' stroke='currentColor' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><path d='M20.59 13.41l-7.17 7.17a2 2 0 0 1-2.83 0L2 12V2h10l8.59 8.59a2 2 0 0 1 0 2.82z'/><line x1='7' y1='7' x2='7.01' y2='7'/></svg>"""
ICON_SEARCH = """<svg viewBox='0 0 24 24' width='14' height='14' fill='none' stroke='currentColor' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><circle cx='11' cy='11' r='8'/><line x1='21' y1='21' x2='16.65' y2='16.65'/></svg>"""
ICON_CLOCK = """<svg viewBox='0 0 24 24' width='14' height='14' fill='none' stroke='currentColor' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><circle cx='12' cy='12' r='10'/><polyline points='12 6 12 12 16 14'/></svg>"""
ICON_LIST = """<svg viewBox='0 0 24 24' width='14' height='14' fill='none' stroke='currentColor' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><line x1='8' y1='6' x2='21' y2='6'/><line x1='8' y1='12' x2='21' y2='12'/><line x1='8' y1='18' x2='21' y2='18'/><line x1='3' y1='6' x2='3.01' y2='6'/><line x1='3' y1='12' x2='3.01' y2='12'/><line x1='3' y1='18' x2='3.01' y2='18'/></svg>"""
ICON_CHECK = """<svg viewBox='0 0 24 24' width='14' height='14' fill='none' stroke='currentColor' stroke-width='2.5' stroke-linecap='round' stroke-linejoin='round'><polyline points='20 6 9 17 4 12'/></svg>"""
ICON_X = """<svg viewBox='0 0 24 24' width='14' height='14' fill='none' stroke='currentColor' stroke-width='2.5' stroke-linecap='round' stroke-linejoin='round'><line x1='18' y1='6' x2='6' y2='18'/><line x1='6' y1='6' x2='18' y2='18'/></svg>"""
ICON_REFRESH = """<svg viewBox='0 0 24 24' width='14' height='14' fill='none' stroke='currentColor' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><polyline points='23 4 23 10 17 10'/><polyline points='1 20 1 14 7 14'/><path d='M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15'/></svg>"""
ICON_SPARK = """<svg viewBox='0 0 24 24' width='14' height='14' fill='none' stroke='currentColor' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><polygon points='13 2 3 14 12 14 11 22 21 10 12 10 13 2'/></svg>"""
ICON_INFO = """<svg viewBox='0 0 24 24' width='14' height='14' fill='none' stroke='currentColor' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><circle cx='12' cy='12' r='10'/><line x1='12' y1='16' x2='12' y2='12'/><line x1='12' y1='8' x2='12.01' y2='8'/></svg>"""

st.markdown(f"""
<style>
    :root {{
        --bg:        #F4F6FB;
        --surface:   #FFFFFF;
        --border:    #E4E7EE;
        --text:      #1B2333;
        --muted:     #6B7280;
        --primary:   #4F46E5;
        --primary-2: #6366F1;
        --accent:    #10B981;
        --warn:      #F59E0B;
        --pink:      #EC4899;
        --sky:       #0EA5E9;
        --violet:    #8B5CF6;
    }}
    .stApp {{ background: var(--bg); }}
    html, body, [class*="css"] {{
        font-family: 'Inter', system-ui, -apple-system, sans-serif;
        color: var(--text);
    }}
    #MainMenu, footer, header {{ visibility: hidden; }}
    .block-container {{ padding-top: 1rem; padding-bottom: 7rem; max-width: 1100px; }}

    .lib-header {{
        background: linear-gradient(120deg, #4F46E5 0%, #6366F1 50%, #8B5CF6 100%);
        color: white;
        padding: 1.4rem 1.6rem;
        border-radius: 18px;
        margin-bottom: 1rem;
        box-shadow: 0 10px 30px rgba(79,70,229,0.25);
        position: relative;
        overflow: hidden;
    }}
    .lib-header::before {{
        content: ""; position: absolute; inset: 0;
        background: radial-gradient(circle at 90% 10%, rgba(255,255,255,0.18), transparent 40%);
    }}
    .lib-header h1 {{
        margin: 0; font-size: 1.5rem; font-weight: 700;
        letter-spacing: -0.02em; display: flex; align-items: center; gap: 0.6rem;
        position: relative;
    }}
    .lib-header p {{ margin: 0.3rem 0 0; font-size: 0.85rem; opacity: 0.9; position: relative; }}
    .lib-header .brand-mark {{
        width: 36px; height: 36px; border-radius: 10px;
        background: rgba(255,255,255,0.18); display: inline-flex;
        align-items: center; justify-content: center;
    }}
    .header-meta {{
        position: absolute; top: 1.1rem; right: 1.4rem;
        display: inline-flex; align-items: center; gap: 0.4rem;
        font-size: 0.72rem; opacity: 0.95;
        background: rgba(255,255,255,0.15);
        padding: 0.25rem 0.65rem; border-radius: 999px;
        backdrop-filter: blur(6px);
    }}
    .pulse-dot {{
        width: 7px; height: 7px; border-radius: 50%; background: #34D399;
        box-shadow: 0 0 0 0 rgba(52,211,153,0.7);
        animation: pulse 1.8s infinite;
    }}
    @keyframes pulse {{
        0%   {{ box-shadow: 0 0 0 0 rgba(52,211,153,0.7); }}
        70%  {{ box-shadow: 0 0 0 8px rgba(52,211,153,0); }}
        100% {{ box-shadow: 0 0 0 0 rgba(52,211,153,0); }}
    }}

    .stats-row {{
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 0.7rem;
        margin-bottom: 1rem;
    }}
    .stat-card {{
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: 0.85rem 1rem;
        display: flex; align-items: center; gap: 0.85rem;
        transition: transform 0.18s ease, box-shadow 0.18s ease;
    }}
    .stat-card:hover {{
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(27,35,51,0.08);
    }}
    .stat-icon {{
        width: 38px; height: 38px; border-radius: 10px;
        display: inline-flex; align-items: center; justify-content: center;
        flex-shrink: 0;
    }}
    .stat-icon.indigo  {{ background: #EEF2FF; color: var(--primary); }}
    .stat-icon.emerald {{ background: #ECFDF5; color: var(--accent);  }}
    .stat-icon.amber   {{ background: #FFFBEB; color: var(--warn);    }}
    .stat-text .label {{ font-size: 0.7rem; color: var(--muted); font-weight: 600; letter-spacing: 0.04em; text-transform: uppercase; }}
    .stat-text .value {{ font-size: 1.35rem; font-weight: 700; color: var(--text); line-height: 1.1; margin-top: 2px; }}

    .chat-shell {{
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 18px;
        padding: 1rem 1.1rem;
        min-height: 360px;
        box-shadow: 0 4px 16px rgba(27,35,51,0.04);
    }}
    .msg-row {{
        display: flex; align-items: flex-end; gap: 0.55rem;
        margin: 0.4rem 0; animation: fadeUp 0.28s ease-out;
    }}
    .msg-row.user {{ justify-content: flex-end; }}
    @keyframes fadeUp {{
        from {{ opacity: 0; transform: translateY(6px); }}
        to   {{ opacity: 1; transform: translateY(0); }}
    }}
    .avatar {{
        width: 32px; height: 32px; border-radius: 10px;
        display: inline-flex; align-items: center; justify-content: center;
        flex-shrink: 0; color: white;
    }}
    .avatar.bot  {{ background: linear-gradient(135deg, #4F46E5, #6366F1); }}
    .avatar.user {{ background: linear-gradient(135deg, #10B981, #059669); }}

    .bubble-wrap {{ display: flex; flex-direction: column; max-width: 78%; }}
    .bubble-wrap.user {{ align-items: flex-end; }}
    .bubble {{
        padding: 0.7rem 0.95rem;
        font-size: 0.92rem; line-height: 1.55;
    }}
    .bubble-user {{
        background: linear-gradient(135deg, #4F46E5, #6366F1);
        color: white;
        border-radius: 16px 16px 4px 16px;
        box-shadow: 0 4px 10px rgba(79,70,229,0.18);
    }}
    .bubble-bot {{
        background: #F8FAFC;
        color: var(--text);
        border: 1px solid #E2E8F0;
        border-radius: 16px 16px 16px 4px;
    }}
    .bubble-bot strong {{ color: var(--primary); font-weight: 600; }}
    .bubble-bot code {{
        background: #EEF2FF; color: var(--primary);
        padding: 1px 6px; border-radius: 5px; font-size: 0.85em;
    }}
    .ts {{ font-size: 0.65rem; color: var(--muted); margin-top: 0.25rem; padding: 0 0.3rem; }}

    .chip-label {{
        font-size: 0.68rem; color: var(--muted); font-weight: 600;
        letter-spacing: 0.08em; text-transform: uppercase;
        margin: 1rem 0 0.4rem; display: flex; align-items: center; gap: 0.35rem;
    }}
    div[data-testid="stHorizontalBlock"] .stButton > button {{
        border-radius: 999px !important;
        background: var(--surface) !important;
        color: var(--text) !important;
        border: 1px solid var(--border) !important;
        font-weight: 500 !important;
        font-size: 0.8rem !important;
        padding: 0.4rem 0.95rem !important;
        box-shadow: 0 1px 2px rgba(27,35,51,0.04) !important;
        transition: all 0.18s ease !important;
    }}
    div[data-testid="stHorizontalBlock"] .stButton > button:hover {{
        background: var(--primary) !important;
        color: white !important;
        border-color: var(--primary) !important;
        transform: translateY(-1px);
        box-shadow: 0 6px 14px rgba(79,70,229,0.25) !important;
    }}

    [data-testid="stSidebar"] {{
        background: var(--surface);
        border-right: 1px solid var(--border);
    }}
    [data-testid="stSidebar"] * {{ color: var(--text) !important; }}
    [data-testid="stSidebar"] h3 {{
        font-size: 0.75rem !important;
        color: var(--muted) !important;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        font-weight: 700 !important;
        margin-bottom: 0.6rem !important;
    }}
    .state-pill {{
        display: inline-flex; align-items: center; gap: 0.4rem;
        padding: 0.35rem 0.85rem;
        border-radius: 999px;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.05em;
    }}
    .state-pill .ind {{ width: 7px; height: 7px; border-radius: 50%; }}
    .state-desc {{
        font-size: 0.78rem;
        color: var(--muted) !important;
        margin-top: 0.45rem;
        line-height: 1.4;
    }}
    .tip-card {{
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 10px;
        padding: 0.55rem 0.75rem;
        margin-bottom: 0.4rem;
        font-size: 0.78rem;
        display: flex; gap: 0.55rem; align-items: flex-start;
        transition: all 0.18s ease;
    }}
    .tip-card:hover {{
        border-color: var(--primary);
        background: #F5F7FF;
        transform: translateX(2px);
    }}
    .tip-card .tip-ico {{
        width: 26px; height: 26px; border-radius: 7px;
        background: #EEF2FF; color: var(--primary);
        display: inline-flex; align-items: center; justify-content: center;
        flex-shrink: 0;
    }}
    .tip-card b {{ color: var(--text) !important; font-weight: 600; }}
    .tip-card .desc {{ color: var(--muted) !important; font-size: 0.7rem; margin-top: 1px; }}

    [data-testid="stSidebar"] .stButton > button {{
        width: 100% !important;
        border-radius: 10px !important;
        background: var(--primary) !important;
        color: white !important;
        border: none !important;
        font-weight: 600 !important;
        padding: 0.6rem !important;
        font-size: 0.85rem !important;
    }}
    [data-testid="stSidebar"] .stButton > button:hover {{
        background: #4338CA !important;
    }}
    [data-testid="stSidebar"] .stButton > button * {{ color: white !important; }}

    [data-testid="stChatInput"] {{ background: transparent !important; }}
    [data-testid="stChatInput"] > div {{
        background: var(--surface) !important;
        border: 1px solid var(--border) !important;
        border-radius: 14px !important;
        box-shadow: 0 -2px 14px rgba(27,35,51,0.05) !important;
    }}
    [data-testid="stChatInput"] textarea {{
        background: transparent !important;
        color: var(--text) !important;
        font-size: 0.92rem !important;
    }}
    [data-testid="stChatInput"] textarea::placeholder {{ color: var(--muted) !important; }}
    [data-testid="stChatInput"] button {{
        background: var(--primary) !important;
        color: white !important;
        border-radius: 10px !important;
    }}
    [data-testid="stChatInput"] button:hover {{ background: #4338CA !important; }}
    [data-testid="stBottom"] {{ background: var(--bg) !important; }}
    [data-testid="stBottomBlockContainer"] {{ background: var(--bg) !important; padding-bottom: 1rem !important; }}

    ::-webkit-scrollbar {{ width: 8px; height: 8px; }}
    ::-webkit-scrollbar-thumb {{ background: #CBD5E1; border-radius: 4px; }}
    ::-webkit-scrollbar-thumb:hover {{ background: var(--primary); }}
</style>
""", unsafe_allow_html=True)

if "fsm" not in st.session_state:
    st.session_state.fsm = FSM()
if "history" not in st.session_state:
    st.session_state.history = []
if "queued_input" not in st.session_state:
    st.session_state.queued_input = None


def render_markdown(text: str) -> str:
    import re
    safe = (text.replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;"))
    safe = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", safe, flags=re.DOTALL)
    safe = re.sub(r"`([^`]+)`", r"<code>\1</code>", safe)
    safe = safe.replace("\n", "<br>")
    return safe


def send_message(text: str):
    text = text.strip()
    if not text:
        return
    st.session_state.history.append({
        "role": "user",
        "text": text,
        "ts": datetime.now().strftime("%H:%M"),
    })
    reply = st.session_state.fsm.transition(text)
    st.session_state.history.append({
        "role": "bot",
        "text": reply,
        "ts": datetime.now().strftime("%H:%M"),
    })


st.markdown(f"""
<div class="lib-header">
    <div class="header-meta"><span class="pulse-dot"></span> online</div>
    <h1><span class="brand-mark">{ICON_BOT}</span> Perpustakaan Digital</h1>
    <p>Asisten cerdas berbasis Finite State Machine</p>
</div>
""", unsafe_allow_html=True)

stats = st.session_state.fsm.engine.get_stats()
st.markdown(f"""
<div class="stats-row">
    <div class="stat-card">
        <div class="stat-icon indigo">{ICON_BOOK}</div>
        <div class="stat-text">
            <div class="label">Total Judul</div>
            <div class="value">{stats['titles']}</div>
        </div>
    </div>
    <div class="stat-card">
        <div class="stat-icon emerald">{ICON_LAYERS}</div>
        <div class="stat-text">
            <div class="label">Stok Tersedia</div>
            <div class="value">{stats['stock']}</div>
        </div>
    </div>
    <div class="stat-card">
        <div class="stat-icon amber">{ICON_TAG}</div>
        <div class="stat-text">
            <div class="label">Kategori</div>
            <div class="value">{stats['categories']}</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

STATE_INFO = {
    "DEFAULT": ("#9CA3AF", "Menunggu input pertama"),
    "ACTIVE":  ("#4F46E5", "Siap menerima perintah"),
    "BROWSE":  ("#0EA5E9", "Sedang mencari buku"),
    "BORROW":  ("#10B981", "Menunggu judul buku"),
    "CONFIRM": ("#F59E0B", "Menunggu konfirmasi"),
    "END":     ("#8B5CF6", "Sesi telah selesai"),
}

with st.sidebar:
    st.markdown("### Status FSM")
    cur = st.session_state.fsm.state
    col, desc = STATE_INFO.get(cur, ("#4F46E5", ""))
    st.markdown(
        f'<span class="state-pill" '
        f'style="background:{col}1A;color:{col};border:1px solid {col}55">'
        f'<span class="ind" style="background:{col}"></span>{cur}</span>'
        f'<div class="state-desc">{desc}</div>',
        unsafe_allow_html=True,
    )

    st.markdown("### Perintah")
    tips = [
        (ICON_SPARK,  "halo",                   "Mulai percakapan"),
        (ICON_SEARCH, "cari [judul/kategori]",  "Cari buku"),
        (ICON_LIST,   "katalog",                "Lihat semua buku"),
        (ICON_TAG,    "kategori",               "Lihat kategori"),
        (ICON_BOOK,   "pinjam [judul]",         "Pinjam buku"),
        (ICON_LAYERS, "stok [judul]",           "Cek ketersediaan"),
        (ICON_CLOCK,  "jam buka",               "Jam operasional"),
        (ICON_INFO,   "syarat pinjam",          "Ketentuan"),
        (ICON_INFO,   "denda",                  "Info denda"),
        (ICON_REFRESH,"reset",                  "Mulai dari awal"),
    ]
    for ic, cmd, d in tips:
        st.markdown(
            f'<div class="tip-card">'
            f'<span class="tip-ico">{ic}</span>'
            f'<div><b>{cmd}</b><div class="desc">{d}</div></div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    st.markdown("### Sesi")
    if st.button("Reset Percakapan", key="reset_btn"):
        st.session_state.fsm = FSM()
        st.session_state.history = []
        st.rerun()

if not st.session_state.history:
    opening = st.session_state.fsm.transition("halo")
    st.session_state.history.append({
        "role": "bot",
        "text": opening,
        "ts": datetime.now().strftime("%H:%M"),
    })

chat_html = ['<div class="chat-shell">']
for msg in st.session_state.history:
    ts = msg.get("ts", "")
    body = render_markdown(msg["text"])
    if msg["role"] == "user":
        chat_html.append(
            f'<div class="msg-row user">'
            f'<div class="bubble-wrap user">'
            f'<div class="bubble bubble-user">{body}</div>'
            f'<div class="ts">{ts}</div>'
            f'</div>'
            f'<div class="avatar user">{ICON_USER}</div>'
            f'</div>'
        )
    else:
        chat_html.append(
            f'<div class="msg-row">'
            f'<div class="avatar bot">{ICON_BOT}</div>'
            f'<div class="bubble-wrap">'
            f'<div class="bubble bubble-bot">{body}</div>'
            f'<div class="ts">{ts}</div>'
            f'</div>'
            f'</div>'
        )
chat_html.append('</div>')
st.markdown("".join(chat_html), unsafe_allow_html=True)

st.markdown(
    f'<div class="chip-label">{ICON_SPARK} Saran cepat</div>',
    unsafe_allow_html=True,
)

state = st.session_state.fsm.state
if state == "CONFIRM":
    chips = [("Ya, lanjutkan", "ya"), ("Batalkan", "tidak")]
elif state == "BORROW":
    chips = [
        ("Kalkulus", "kalkulus"),
        ("Pemrograman Python", "pemrograman python"),
        ("Batal", "tidak"),
    ]
else:
    chips = [
        ("Lihat katalog", "katalog"),
        ("Kategori",      "kategori"),
        ("Cari kalkulus", "cari kalkulus"),
        ("Jam buka",      "jam buka"),
        ("Syarat pinjam", "syarat pinjam"),
    ]

cols = st.columns(len(chips))
for i, (label, cmd) in enumerate(chips):
    if cols[i].button(label, key=f"chip_{state}_{i}"):
        st.session_state.queued_input = cmd
        st.rerun()

user_text = st.chat_input("Ketik pesanmu... contoh: cari buku kalkulus")

if st.session_state.queued_input:
    queued = st.session_state.queued_input
    st.session_state.queued_input = None
    send_message(queued)
    st.rerun()

if user_text:
    send_message(user_text)
    st.rerun()
