import streamlit as st
from datetime import datetime
from FSM import FSM

st.set_page_config(
    page_title="Perpustakaan Digital",
    page_icon="P",
    layout="wide",
    initial_sidebar_state="expanded",
)

ICON_BOT = """<svg viewBox='0 0 24 24' width='16' height='16' fill='none' stroke='currentColor' stroke-width='1.5' stroke-linecap='round' stroke-linejoin='round'><rect x='3' y='11' width='18' height='10' rx='2'/><circle cx='12' cy='5' r='2'/><path d='M12 7v4'/><line x1='8' y1='16' x2='8' y2='16'/><line x1='16' y1='16' x2='16' y2='16'/></svg>"""
ICON_USER = """<svg viewBox='0 0 24 24' width='14' height='14' fill='none' stroke='currentColor' stroke-width='1.5' stroke-linecap='round' stroke-linejoin='round'><path d='M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2'/><circle cx='12' cy='7' r='4'/></svg>"""
ICON_BOOK = """<svg viewBox='0 0 24 24' width='14' height='14' fill='none' stroke='currentColor' stroke-width='1.5' stroke-linecap='round' stroke-linejoin='round'><path d='M4 19.5A2.5 2.5 0 0 1 6.5 17H20'/><path d='M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z'/></svg>"""
ICON_LAYERS = """<svg viewBox='0 0 24 24' width='14' height='14' fill='none' stroke='currentColor' stroke-width='1.5' stroke-linecap='round' stroke-linejoin='round'><polygon points='12 2 2 7 12 12 22 7 12 2'/><polyline points='2 17 12 22 22 17'/><polyline points='2 12 12 17 22 12'/></svg>"""
ICON_TAG = """<svg viewBox='0 0 24 24' width='14' height='14' fill='none' stroke='currentColor' stroke-width='1.5' stroke-linecap='round' stroke-linejoin='round'><path d='M20.59 13.41l-7.17 7.17a2 2 0 0 1-2.83 0L2 12V2h10l8.59 8.59a2 2 0 0 1 0 2.82z'/><line x1='7' y1='7' x2='7.01' y2='7'/></svg>"""
ICON_SEARCH = """<svg viewBox='0 0 24 24' width='14' height='14' fill='none' stroke='currentColor' stroke-width='1.5' stroke-linecap='round' stroke-linejoin='round'><circle cx='11' cy='11' r='8'/><line x1='21' y1='21' x2='16.65' y2='16.65'/></svg>"""
ICON_LIST = """<svg viewBox='0 0 24 24' width='14' height='14' fill='none' stroke='currentColor' stroke-width='1.5' stroke-linecap='round' stroke-linejoin='round'><line x1='8' y1='6' x2='21' y2='6'/><line x1='8' y1='12' x2='21' y2='12'/><line x1='8' y1='18' x2='21' y2='18'/><line x1='3' y1='6' x2='3.01' y2='6'/><line x1='3' y1='12' x2='3.01' y2='12'/><line x1='3' y1='18' x2='3.01' y2='18'/></svg>"""
ICON_REFRESH = """<svg viewBox='0 0 24 24' width='14' height='14' fill='none' stroke='currentColor' stroke-width='1.5' stroke-linecap='round' stroke-linejoin='round'><polyline points='23 4 23 10 17 10'/><polyline points='1 20 1 14 7 14'/><path d='M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15'/></svg>"""
ICON_SPARK = """<svg viewBox='0 0 24 24' width='14' height='14' fill='none' stroke='currentColor' stroke-width='1.5' stroke-linecap='round' stroke-linejoin='round'><path d='M9.937 15.5A2 2 0 0 0 8.5 14.063l-6.135-1.582a.5.5 0 0 1 0-.962L8.5 9.936A2 2 0 0 0 9.937 8.5l1.582-6.135a.5.5 0 0 1 .963 0L14.063 8.5A2 2 0 0 0 15.5 9.937l6.135 1.581a.5.5 0 0 1 0 .964L15.5 14.063a2 2 0 0 0-1.437 1.437l-1.582 6.135a.5.5 0 0 1-.963 0z'/></svg>"""
ICON_SUNRISE = """<svg viewBox='0 0 24 24' width='14' height='14' fill='none' stroke='currentColor' stroke-width='1.5' stroke-linecap='round' stroke-linejoin='round'><path d='M17 18a5 5 0 0 0-10 0'/><line x1='12' y1='2' x2='12' y2='9'/><line x1='4.22' y1='10.22' x2='5.64' y2='11.64'/><line x1='1' y1='18' x2='3' y2='18'/><line x1='21' y1='18' x2='23' y2='18'/><line x1='18.36' y1='11.64' x2='19.78' y2='10.22'/><line x1='23' y1='22' x2='1' y2='22'/><polyline points='8 6 12 2 16 6'/></svg>"""
ICON_SHIELD = """<svg viewBox='0 0 24 24' width='14' height='14' fill='none' stroke='currentColor' stroke-width='1.5' stroke-linecap='round' stroke-linejoin='round'><path d='M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z'/></svg>"""
ICON_RECEIPT = """<svg viewBox='0 0 24 24' width='14' height='14' fill='none' stroke='currentColor' stroke-width='1.5' stroke-linecap='round' stroke-linejoin='round'><path d='M4 2v20l2-1 2 1 2-1 2 1 2-1 2 1 2-1 2 1V2l-2 1-2-1-2 1-2-1-2 1-2-1-2 1-2-1z'/><line x1='8' y1='8' x2='16' y2='8'/><line x1='8' y1='12' x2='16' y2='12'/><line x1='8' y1='16' x2='12' y2='16'/></svg>"""

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Inter:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap');

:root {{
    --bg:        #F5F0E8;
    --bg-2:      #EDE6D6;
    --surface:   #FAF6EC;
    --paper:     #FFFFFF;
    --ink:       #1A1612;
    --ink-2:     #3A2F25;
    --muted:     #8B7B66;
    --line:      #1A161220;
    --line-soft: #1A161210;
    --accent:    #C8A97E;
    --accent-2:  #8B5E3C;
    --leaf:      #6B7A4A;
}}

.stApp {{ background: var(--bg); }}
html, body, [class*="css"] {{
    font-family: 'Inter', system-ui, sans-serif;
    color: var(--ink);
    -webkit-font-smoothing: antialiased;
}}
#MainMenu, footer, header[data-testid="stHeader"] {{ display: none; }}
.block-container {{
    padding-top: 2rem;
    padding-bottom: 8rem;
    max-width: 1180px;
}}

.serif {{ font-family: 'Instrument Serif', Georgia, serif; font-weight: 400; }}
.label {{
    font-size: 0.68rem;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: var(--muted);
    font-weight: 500;
}}

.masthead {{
    border-top: 1px solid var(--ink);
    border-bottom: 1px solid var(--line);
    padding: 1.4rem 0 1.1rem;
    margin-bottom: 0.4rem;
    display: grid;
    grid-template-columns: auto 1fr auto;
    align-items: end;
    gap: 1.4rem;
}}
.masthead .issue {{
    font-size: 0.7rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--muted);
}}
.masthead .wordmark {{
    font-family: 'Instrument Serif', Georgia, serif;
    font-size: clamp(2rem, 4vw, 2.9rem);
    line-height: 1;
    letter-spacing: -0.02em;
    color: var(--ink);
}}
.masthead .wordmark em {{
    font-style: italic;
    color: var(--accent-2);
}}
.masthead .meta {{
    text-align: right;
    font-size: 0.7rem;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: var(--muted);
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    justify-content: flex-end;
}}
.dot-live {{
    width: 6px; height: 6px; border-radius: 50%;
    background: var(--leaf);
    box-shadow: 0 0 0 0 rgba(107,122,74,0.6);
    animation: pulse 2s infinite;
}}
@keyframes pulse {{
    0%   {{ box-shadow: 0 0 0 0 rgba(107,122,74,0.55); }}
    70%  {{ box-shadow: 0 0 0 6px rgba(107,122,74,0); }}
    100% {{ box-shadow: 0 0 0 0 rgba(107,122,74,0); }}
}}

.kicker-row {{
    display: grid;
    grid-template-columns: 1.4fr 1fr 1fr 1fr;
    gap: 0;
    border-bottom: 1px solid var(--line);
    margin-bottom: 1.4rem;
}}
.kicker-row > div {{
    padding: 0.85rem 1rem 0.85rem 0;
    border-right: 1px solid var(--line-soft);
}}
.kicker-row > div:last-child {{ border-right: none; padding-right: 0; }}
.kicker-row > div:not(:first-child) {{ padding-left: 1rem; }}
.kicker .lead {{
    font-family: 'Instrument Serif', Georgia, serif;
    font-size: 1rem;
    font-style: italic;
    color: var(--ink-2);
    line-height: 1.45;
    max-width: 38ch;
}}
.metric .num {{
    font-family: 'Instrument Serif', Georgia, serif;
    font-size: 2.2rem;
    line-height: 1;
    color: var(--ink);
    font-feature-settings: "tnum" 1;
}}
.metric .num em {{
    font-style: italic;
    color: var(--accent-2);
    font-size: 0.7em;
    margin-left: 0.2rem;
}}
.metric .cap {{
    margin-top: 0.4rem;
    font-size: 0.66rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--muted);
    display: inline-flex; align-items: center; gap: 0.35rem;
}}

.transcript-head {{
    display: flex; align-items: baseline; justify-content: space-between;
    border-bottom: 1px solid var(--line);
    padding-bottom: 0.55rem; margin-bottom: 1rem;
}}
.transcript-head h2 {{
    font-family: 'Instrument Serif', Georgia, serif;
    font-size: 1.7rem;
    margin: 0;
    line-height: 1;
    letter-spacing: -0.01em;
}}
.transcript-head .h-meta {{
    font-size: 0.66rem;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: var(--muted);
}}

.thread {{
    display: flex; flex-direction: column; gap: 1.1rem;
    padding: 0.4rem 0 1.2rem;
}}
.entry {{ animation: fadeUp 0.32s cubic-bezier(0.25,0.1,0.25,1); }}
@keyframes fadeUp {{
    from {{ opacity: 0; transform: translateY(4px); }}
    to   {{ opacity: 1; transform: translateY(0); }}
}}
.entry .byline {{
    display: flex; align-items: center; gap: 0.5rem;
    font-size: 0.65rem;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 0.35rem;
}}
.entry .byline .role {{ font-weight: 600; color: var(--ink-2); }}
.entry .byline .ico {{
    width: 18px; height: 18px;
    display: inline-flex; align-items: center; justify-content: center;
    color: var(--ink-2);
}}
.entry .byline .sep {{ color: var(--line); }}
.entry .body {{
    font-size: 0.96rem; line-height: 1.65;
    color: var(--ink);
    max-width: 64ch;
    white-space: pre-line;
}}
.entry .body strong {{
    font-family: 'Instrument Serif', Georgia, serif;
    font-style: italic;
    font-weight: 400;
    color: var(--accent-2);
    font-size: 1.05em;
}}
.entry .body code {{
    font-family: 'IBM Plex Mono', ui-monospace, monospace;
    font-size: 0.85em;
    background: var(--bg-2);
    padding: 1px 6px;
    border-radius: 2px;
    color: var(--ink-2);
}}
.entry.user {{ padding-left: 18%; }}
.entry.user .byline {{ justify-content: flex-end; }}
.entry.user .body {{
    background: var(--ink);
    color: var(--bg);
    padding: 0.85rem 1.05rem;
    border-radius: 2px;
    margin-left: auto;
}}
.entry.bot {{ padding-right: 14%; }}
.entry.bot .body {{
    border-left: 2px solid var(--accent-2);
    padding-left: 1rem;
}}
.entry.bot.opener .body::first-letter {{
    font-family: 'Instrument Serif', Georgia, serif;
    font-size: 3.2rem;
    line-height: 0.85;
    float: left;
    padding: 0.2rem 0.7rem 0 0;
    color: var(--accent-2);
}}

.suggest-band {{
    border-top: 1px solid var(--line);
    border-bottom: 1px solid var(--line);
    padding: 0.7rem 0;
    margin: 0.6rem 0 0.4rem;
    display: flex; align-items: center; gap: 0.9rem;
}}
.suggest-band .lbl {{
    font-size: 0.62rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--muted);
    flex-shrink: 0;
}}
div[data-testid="stHorizontalBlock"] .stButton > button {{
    background: transparent !important;
    color: var(--ink) !important;
    border: 1px solid var(--ink) !important;
    border-radius: 0 !important;
    font-weight: 500 !important;
    font-size: 0.78rem !important;
    padding: 0.4rem 0.95rem !important;
    box-shadow: none !important;
    letter-spacing: 0.02em !important;
    transition: background 0.28s ease, color 0.28s ease, transform 0.28s ease !important;
}}
div[data-testid="stHorizontalBlock"] .stButton > button:hover {{
    background: var(--ink) !important;
    color: var(--bg) !important;
    transform: translateY(-1px);
}}

[data-testid="stSidebar"] {{
    background: var(--surface);
    border-right: 1px solid var(--line);
}}
[data-testid="stSidebar"] > div {{ padding-top: 1rem; }}
[data-testid="stSidebar"] * {{ color: var(--ink) !important; }}
[data-testid="stSidebar"] h3 {{
    font-family: 'Inter', sans-serif !important;
    font-size: 0.66rem !important;
    letter-spacing: 0.2em !important;
    text-transform: uppercase;
    color: var(--muted) !important;
    font-weight: 600 !important;
    margin: 1rem 0 0.55rem !important;
    padding-bottom: 0.45rem;
    border-bottom: 1px solid var(--line);
}}
.fsm-card {{
    padding: 0.85rem 0;
    border-bottom: 1px solid var(--line-soft);
}}
.fsm-card .state-line {{
    display: flex; justify-content: space-between; align-items: baseline;
    margin-bottom: 0.3rem;
}}
.fsm-card .state-tag {{
    font-family: 'Instrument Serif', Georgia, serif;
    font-size: 1.5rem;
    line-height: 1;
    color: var(--ink);
    font-style: italic;
}}
.fsm-card .state-num {{
    font-size: 0.62rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--muted);
}}
.fsm-card .state-desc {{
    font-size: 0.82rem;
    color: var(--muted) !important;
    line-height: 1.45;
}}
.cmd-list {{ display: flex; flex-direction: column; }}
.cmd-row {{
    display: grid;
    grid-template-columns: 18px 1fr;
    gap: 0.65rem;
    align-items: start;
    padding: 0.55rem 0;
    border-bottom: 1px solid var(--line-soft);
    transition: padding-left 0.24s ease;
}}
.cmd-row:hover {{ padding-left: 0.3rem; }}
.cmd-row:last-child {{ border-bottom: none; }}
.cmd-row .ico {{ color: var(--accent-2); margin-top: 2px; }}
.cmd-row .cmd {{
    font-family: 'IBM Plex Mono', ui-monospace, monospace;
    font-size: 0.78rem;
    color: var(--ink);
    font-weight: 500;
}}
.cmd-row .desc {{
    font-size: 0.72rem;
    color: var(--muted) !important;
    margin-top: 1px;
    line-height: 1.4;
}}

[data-testid="stSidebar"] .stButton > button {{
    width: 100% !important;
    background: var(--ink) !important;
    color: var(--bg) !important;
    border: 1px solid var(--ink) !important;
    border-radius: 0 !important;
    font-weight: 500 !important;
    font-size: 0.74rem !important;
    letter-spacing: 0.16em !important;
    text-transform: uppercase !important;
    padding: 0.7rem !important;
    transition: background 0.28s ease, color 0.28s ease !important;
}}
[data-testid="stSidebar"] .stButton > button:hover {{
    background: var(--bg) !important;
    color: var(--ink) !important;
}}
[data-testid="stSidebar"] .stButton > button * {{ color: inherit !important; }}

[data-testid="stChatInput"] {{ background: transparent !important; }}
[data-testid="stChatInput"] > div {{
    background: var(--paper) !important;
    border: 1px solid var(--ink) !important;
    border-radius: 0 !important;
    box-shadow: 0 -2px 0 var(--bg) !important;
}}
[data-testid="stChatInput"] textarea {{
    background: transparent !important;
    color: var(--ink) !important;
    font-size: 0.94rem !important;
    font-family: 'Inter', sans-serif !important;
}}
[data-testid="stChatInput"] textarea::placeholder {{
    color: var(--muted) !important;
    font-style: italic;
}}
[data-testid="stChatInput"] button {{
    background: var(--ink) !important;
    color: var(--bg) !important;
    border-radius: 0 !important;
}}
[data-testid="stChatInput"] button:hover {{ background: var(--accent-2) !important; }}
[data-testid="stBottom"], [data-testid="stBottomBlockContainer"] {{
    background: var(--bg) !important;
    border-top: 1px solid var(--line);
}}

.colophon {{
    margin-top: 2rem;
    padding-top: 1rem;
    border-top: 1px solid var(--line);
    display: flex; justify-content: space-between;
    font-size: 0.65rem;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: var(--muted);
}}

::-webkit-scrollbar {{ width: 6px; }}
::-webkit-scrollbar-track {{ background: var(--bg); }}
::-webkit-scrollbar-thumb {{ background: var(--accent); }}
::-webkit-scrollbar-thumb:hover {{ background: var(--accent-2); }}

@media (max-width: 720px) {{
    .masthead {{ grid-template-columns: 1fr; gap: 0.4rem; }}
    .masthead .meta {{ text-align: left; justify-content: flex-start; }}
    .kicker-row {{ grid-template-columns: 1fr 1fr; }}
    .kicker-row > div {{ border-right: none; border-bottom: 1px solid var(--line-soft); }}
    .entry.user {{ padding-left: 0; }}
    .entry.bot {{ padding-right: 0; }}
}}
</style>
""", unsafe_allow_html=True)

if "fsm" not in st.session_state:
    st.session_state.fsm = FSM()
if "history" not in st.session_state:
    st.session_state.history = []
if "queued_input" not in st.session_state:
    st.session_state.queued_input = None


def render_text(text: str) -> str:
    import re
    out = (text.replace("&", "&amp;")
               .replace("<", "&lt;")
               .replace(">", "&gt;"))
    out = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", out, flags=re.DOTALL)
    out = re.sub(r"`([^`]+)`", r"<code>\1</code>", out)
    return out


def send_message(text: str):
    text = text.strip()
    if not text:
        return
    st.session_state.history.append({
        "role": "user",
        "text": text,
        "ts": datetime.now().strftime("%H.%M"),
    })
    reply = st.session_state.fsm.transition(text)
    st.session_state.history.append({
        "role": "bot",
        "text": reply,
        "ts": datetime.now().strftime("%H.%M"),
    })


today = datetime.now().strftime("%A, %d %B %Y").upper()
clock = datetime.now().strftime("%H.%M")

st.markdown(f"""
<header class="masthead">
    <div class="issue">Vol. I &nbsp;&middot;&nbsp; FSM Edition</div>
    <div class="wordmark">Perpustakaan <em>Digital</em></div>
    <div class="meta"><span class="dot-live"></span> Live &middot; {clock}</div>
</header>
""", unsafe_allow_html=True)

stats = st.session_state.fsm.engine.get_stats()

st.markdown(f"""
<section class="kicker-row">
    <div class="kicker">
        <div class="label">Pengantar</div>
        <p class="lead">Bertanya soal buku, pinjam, atau jam buka. Asisten ini berjalan di atas Finite State Machine, jadi tiap balasan punya konteks.</p>
    </div>
    <div class="metric">
        <div class="num">{stats['titles']:02d}</div>
        <div class="cap">{ICON_BOOK}<span>Judul</span></div>
    </div>
    <div class="metric">
        <div class="num">{stats['stock']:02d}</div>
        <div class="cap">{ICON_LAYERS}<span>Eksemplar</span></div>
    </div>
    <div class="metric">
        <div class="num">{stats['categories']:02d}<em>kat</em></div>
        <div class="cap">{ICON_TAG}<span>Kategori</span></div>
    </div>
</section>
""", unsafe_allow_html=True)

STATE_INFO = {
    "DEFAULT": ("01", "Menunggu input pertama"),
    "ACTIVE":  ("02", "Siap menerima perintah"),
    "BROWSE":  ("03", "Mode pencarian buku"),
    "BORROW":  ("04", "Menunggu judul yang dipinjam"),
    "CONFIRM": ("05", "Menunggu konfirmasi peminjaman"),
    "END":     ("06", "Sesi telah berakhir"),
}

with st.sidebar:
    st.markdown("### Status")
    cur = st.session_state.fsm.state
    num, desc = STATE_INFO.get(cur, ("00", ""))
    st.markdown(
        f'<div class="fsm-card">'
        f'<div class="state-line">'
        f'<span class="state-tag">{cur.lower()}</span>'
        f'<span class="state-num">State {num}/06</span>'
        f'</div>'
        f'<div class="state-desc">{desc}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    st.markdown("### Indeks Perintah")
    tips = [
        (ICON_SPARK,   "halo",                  "Mulai percakapan"),
        (ICON_SEARCH,  "cari [judul]",          "Cari buku berdasarkan judul"),
        (ICON_LIST,    "katalog",               "Lihat seluruh koleksi"),
        (ICON_TAG,     "kategori",              "Daftar kategori"),
        (ICON_BOOK,    "pinjam [judul]",        "Ajukan peminjaman"),
        (ICON_LAYERS,  "stok [judul]",          "Cek ketersediaan"),
        (ICON_SUNRISE, "jam buka",              "Jam operasional"),
        (ICON_SHIELD,  "syarat pinjam",         "Ketentuan peminjaman"),
        (ICON_RECEIPT, "denda",                 "Info keterlambatan"),
        (ICON_REFRESH, "reset",                 "Mulai dari awal"),
    ]
    rows = ['<div class="cmd-list">']
    for ic, cmd, d in tips:
        rows.append(
            f'<div class="cmd-row">'
            f'<span class="ico">{ic}</span>'
            f'<div><div class="cmd">{cmd}</div><div class="desc">{d}</div></div>'
            f'</div>'
        )
    rows.append('</div>')
    st.markdown("".join(rows), unsafe_allow_html=True)

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
        "ts": datetime.now().strftime("%H.%M"),
        "opener": True,
    })

st.markdown(f"""
<div class="transcript-head">
    <h2>Transkrip</h2>
    <div class="h-meta">{today}</div>
</div>
""", unsafe_allow_html=True)

thread = ['<div class="thread">']
for msg in st.session_state.history:
    ts = msg.get("ts", "")
    body = render_text(msg["text"])
    if msg["role"] == "user":
        thread.append(
            f'<article class="entry user">'
            f'<div class="byline">'
            f'<span>{ts}</span>'
            f'<span class="sep">/</span>'
            f'<span class="role">Tamu</span>'
            f'<span class="ico">{ICON_USER}</span>'
            f'</div>'
            f'<div class="body">{body}</div>'
            f'</article>'
        )
    else:
        opener_cls = " opener" if msg.get("opener") else ""
        thread.append(
            f'<article class="entry bot{opener_cls}">'
            f'<div class="byline">'
            f'<span class="ico">{ICON_BOT}</span>'
            f'<span class="role">Pustakawan</span>'
            f'<span class="sep">/</span>'
            f'<span>{ts}</span>'
            f'</div>'
            f'<div class="body">{body}</div>'
            f'</article>'
        )
thread.append('</div>')
st.markdown("".join(thread), unsafe_allow_html=True)

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

st.markdown(
    f'<div class="suggest-band">'
    f'<span class="lbl">Tindakan cepat</span>'
    f'</div>',
    unsafe_allow_html=True,
)

cols = st.columns(len(chips))
for i, (label, cmd) in enumerate(chips):
    if cols[i].button(label, key=f"chip_{state}_{i}"):
        st.session_state.queued_input = cmd
        st.rerun()

st.markdown(f"""
<footer class="colophon">
    <span>Perpustakaan Digital &mdash; FSM Chatbot</span>
    <span>Tugas Teori Bahasa &amp; Otomata</span>
</footer>
""", unsafe_allow_html=True)

user_text = st.chat_input("Tulis pertanyaanmu di sini")

if st.session_state.queued_input:
    queued = st.session_state.queued_input
    st.session_state.queued_input = None
    send_message(queued)
    st.rerun()

if user_text:
    send_message(user_text)
    st.rerun()
