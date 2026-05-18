# Chatbot Perpustakaan Digital

Chatbot layanan perpustakaan berbasis **FSM (Finite State Machine)** dibangun dengan Python dan Streamlit.
Dibuat untuk tugas mata kuliah **Teori Bahasa dan Otomata**.

---

## Cara Menjalankan

```bash
pip install streamlit
streamlit run app.py
```

---

## Struktur File

```
streamlit/
├── app.py       # Tampilan UI Streamlit
├── FSM.py       # Logika Finite State Machine
├── engine.py    # Deteksi intent + katalog buku + info perpustakaan
└── README.md    # Dokumentasi ini
```

---

## Fitur Chatbot

| Fitur                  | Contoh Perintah                          |
|------------------------|------------------------------------------|
| Salam pembuka          | `halo`                                   |
| Cari buku              | `cari kalkulus` / `cari buku teknologi`  |
| Lihat semua katalog    | `katalog`                                |
| Lihat kategori         | `kategori`                               |
| Pinjam buku            | `pinjam kalkulus`                        |
| Cek stok               | `stok fisika dasar`                      |
| Info pengembalian      | `kembalikan` / `cara kembali`            |
| Jam buka               | `jam buka`                               |
| Syarat pinjam          | `syarat pinjam`                          |
| Info denda             | `denda`                                  |
| Info keanggotaan       | `daftar anggota`                         |
| Reset sesi             | `reset`                                  |

---

## FSM — Finite State Machine Chatbot

Chatbot ini adalah **implementasi nyata dari DFA** dengan 6 state:

```
DEFAULT → ACTIVE → BROWSE   → ACTIVE
                 → BORROW   → CONFIRM → ACTIVE
                 → CONFIRM  → ACTIVE
                 → END
```

### Tabel State

| State     | Keterangan                                              |
|-----------|---------------------------------------------------------|
| `DEFAULT` | State awal, menunggu input pertama                      |
| `ACTIVE`  | Siap menerima perintah apapun                           |
| `BROWSE`  | Sedang mode pencarian buku                              |
| `BORROW`  | Menunggu user menyebut judul buku untuk dipinjam        |
| `CONFIRM` | Menunggu konfirmasi (`ya`/`tidak`) sebelum meminjam     |
| `END`     | Percakapan selesai                                      |

### Diagram Transisi

```
          ┌─────────┐
   ───────► DEFAULT │
          └────┬────┘
      GREET /  │ (input apapun)
       lainnya │
          ┌────▼────┐
   ┌──────► ACTIVE  │◄──────────────────┐
   │      └────┬────┘                   │
   │  SEARCH / │BORROW        YES / NO  │
   │  CATALOG  │              (konfirm) │
   │      ┌────┼──────────────────┐     │
   │      │    │                  │     │
   │  ┌───▼──┐ ┌▼──────┐ ┌───────▼──┐  │
   │  │BROWSE│ │BORROW │ │ CONFIRM  ├──┘
   │  └───┬──┘ └───┬───┘ └──────────┘
   │      │        │
   └──────┴────────┘ (THANKS/EXIT → END)
               ↓
           ┌───▼───┐
           │  END  │
           └───────┘

   (dari state manapun, "reset" → DEFAULT)
```

---

## Cara Kerja Deteksi Intent (engine.py)

Engine menggunakan **Regular Expression** untuk mengenali maksud user:

```
Input teks user → regex matching → intent string → FSM.transition() → balasan bot
```

Contoh pola regex:

| Intent          | Pola Regex                                         |
|-----------------|----------------------------------------------------|
| `GREET`         | `\b(halo\|hai\|hi\|hello)\b`                       |
| `SEARCH`        | `\b(cari\|search\|ada buku\|lihat buku)\b`         |
| `BORROW`        | `\b(pinjam\|borrow\|ambil)\b`                      |
| `RETURN`        | `\b(kembalikan\|kembali\|return)\b`                |
| `CHECK_STOCK`   | `\b(stok\|tersedia\|available)\b`                  |
| `ASK_HOURS`     | `\b(jam\|buka\|tutup\|operasional)\b`              |
| `BOOK_MENTIONED`| regex dinamis dari semua judul di katalog          |

---

## Katalog Buku

| Kode    | Judul                        | Kategori   | Stok |
|---------|------------------------------|------------|------|
| TK-001  | Pemrograman Python           | Teknologi  | 3    |
| TK-002  | Algoritma dan Struktur Data  | Teknologi  | 2    |
| TK-003  | Database Sistem              | Teknologi  | 0    |
| MT-001  | Kalkulus                     | Matematika | 4    |
| SN-001  | Fisika Dasar                 | Sains      | 1    |
| EK-001  | Pengantar Ekonomi            | Ekonomi    | 5    |
| SJ-001  | Sejarah Dunia                | Sejarah    | 2    |
| SS-001  | Psikologi Umum               | Sosial     | 3    |

---

## Kaitan dengan Materi Teori Bahasa & Otomata

### 1. Chatbot sebagai DFA
Seluruh alur chatbot ini **adalah** sebuah DFA:
- **Q** = `{DEFAULT, ACTIVE, BROWSE, BORROW, CONFIRM, END}`
- **Σ** = intent yang dideteksi dari teks user
- **δ** = fungsi `FSM.transition()` dan method `_from_*`
- **q0** = `DEFAULT`
- **F** = `{END}`

### 2. Intent Detection sebagai Bahasa Reguler
Setiap pola deteksi intent adalah **bahasa reguler** yang dideskripsikan dengan **Regular Expression** — yang diakui oleh DFA.

### 3. Regex sebagai Finite Automaton
Setiap regex dikompilasi oleh Python menjadi internal automaton untuk pencocokan pola — inilah aplikasi nyata dari teori bahasa reguler.
