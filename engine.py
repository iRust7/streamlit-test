import re

BOOK_CATALOG = {
    "pemrograman python": {
        "author": "Guido van Rossum",
        "category": "Teknologi",
        "stock": 3,
        "code": "TK-001"
    },
    "algoritma dan struktur data": {
        "author": "Thomas H. Cormen",
        "category": "Teknologi",
        "stock": 2,
        "code": "TK-002"
    },
    "kalkulus": {
        "author": "James Stewart",
        "category": "Matematika",
        "stock": 4,
        "code": "MT-001"
    },
    "fisika dasar": {
        "author": "Serway & Jewett",
        "category": "Sains",
        "stock": 1,
        "code": "SN-001"
    },
    "pengantar ekonomi": {
        "author": "N. Gregory Mankiw",
        "category": "Ekonomi",
        "stock": 5,
        "code": "EK-001"
    },
    "sejarah dunia": {
        "author": "J.M. Roberts",
        "category": "Sejarah",
        "stock": 2,
        "code": "SJ-001"
    },
    "psikologi umum": {
        "author": "Atkinson",
        "category": "Sosial",
        "stock": 3,
        "code": "SS-001"
    },
    "database sistem": {
        "author": "Ramez Elmasri",
        "category": "Teknologi",
        "stock": 0,
        "code": "TK-003"
    },
}

LIBRARY_INFO = {
    "jam_buka": "Senin - Jumat: 08.00 - 20.00\nSabtu: 09.00 - 15.00\nMinggu: Tutup",
    "syarat_pinjam": (
        "Syarat meminjam buku:\n"
        "1. Tunjukkan kartu mahasiswa / KTP\n"
        "2. Maksimal pinjam 3 buku sekaligus\n"
        "3. Durasi pinjam: 7 hari\n"
        "4. Denda keterlambatan: Rp500/hari/buku"
    ),
    "cara_kembali": (
        "Cara mengembalikan buku:\n"
        "1. Datang ke meja sirkulasi\n"
        "2. Serahkan buku beserta kartu anggota\n"
        "3. Petugas akan memproses pengembalian\n"
        "4. Simpan struk pengembalian sebagai bukti"
    ),
    "denda": "Denda keterlambatan: Rp500 per hari per buku.\nMaksimal denda: Rp50.000 per buku.",
    "keanggotaan": (
        "Cara daftar anggota perpustakaan:\n"
        "1. Isi formulir di meja pendaftaran\n"
        "2. Lampirkan fotokopi KTP / kartu mahasiswa\n"
        "3. Pas foto 3x4 (1 lembar)\n"
        "4. Biaya: Gratis untuk mahasiswa"
    ),
}

CATEGORIES = list(set(b["category"] for b in BOOK_CATALOG.values()))


class Engine:
    def __init__(self):
        self.catalog = BOOK_CATALOG
        self.info = LIBRARY_INFO
        self.categories = CATEGORIES
        book_keys = [re.escape(k) for k in self.catalog.keys()]
        self.re_book = rf"({'|'.join(book_keys)})"
        self.re_split = r"[,]|\bdan\b|\b&\b"

    def detect_intent(self, text: str) -> str:
        t = text.lower().strip()

        if re.search(r"\b(reset|mulai ulang|restart)\b", t):
            return "RESET"
        if re.search(r"\b(halo|hai|hi|hello|hey|selamat|permisi)\b", t):
            return "GREET"
        if re.search(r"\b(cari|search|ada buku|cek buku|temukan|lihat buku|mau buku)\b", t):
            return "SEARCH"
        if re.search(r"\b(pinjam|borrow|ambil|minta)\b", t):
            return "BORROW"
        if re.search(r"\b(kembalikan|kembali|return)\b", t):
            return "RETURN"
        if re.search(r"\b(stok|tersedia|available|ketersediaan|ada ga|ada tidak)\b", t):
            return "CHECK_STOCK"
        if re.search(r"\b(jam|buka|tutup|operasional|jadwal)\b", t):
            return "ASK_HOURS"
        if re.search(r"\b(syarat|ketentuan|cara pinjam|aturan|prosedur pinjam)\b", t):
            return "ASK_RULES"
        if re.search(r"\b(denda|terlambat|telat|bayar)\b", t):
            return "ASK_FINE"
        if re.search(r"\b(daftar|registrasi|anggota|member|keanggotaan)\b", t):
            return "ASK_MEMBERSHIP"
        if re.search(r"\b(cara kembali|prosedur kembali|gimana kembali)\b", t):
            return "ASK_RETURN_INFO"
        if re.search(r"\b(katalog|daftar buku|semua buku|koleksi|list buku)\b", t):
            return "LIST_CATALOG"
        if re.search(r"\b(kategori|bidang|jenis buku)\b", t):
            return "LIST_CATEGORY"
        if re.search(r"\b(ya|yes|oke|betul|siap|lanjut|benar|iya|setuju)\b", t):
            return "YES"
        if re.search(r"\b(tidak|enggak|nggak|batal|cancel|no)\b", t):
            return "NO"
        if re.search(r"\b(terima kasih|makasih|thanks)\b", t):
            return "THANKS"
        if re.search(r"\b(selesai|keluar|exit|bye|sampai jumpa)\b", t):
            return "EXIT"
        if re.search(self.re_book, t):
            return "BOOK_MENTIONED"

        return "UNKNOWN"

    def find_books(self, text: str) -> list:
        t = text.lower()
        found = []
        for key, data in self.catalog.items():
            if key in t or data["category"].lower() in t:
                found.append({"title": key, **data})
        return found

    def get_book(self, text: str):
        t = text.lower()
        for key, data in self.catalog.items():
            if key in t:
                return {"title": key, **data}
        return None

    def format_book_card(self, book: dict) -> str:
        status = f"Tersedia ({book['stock']} buku)" if book["stock"] > 0 else "Tidak tersedia (habis)"
        return (
            f"**{book['title'].title()}**\n"
            f"Penulis : {book['author']}\n"
            f"Kategori: {book['category']}\n"
            f"Kode    : {book['code']}\n"
            f"Status  : {status}"
        )

    def format_catalog(self) -> str:
        lines = ["**Koleksi Buku Perpustakaan:**\n"]
        current_cat = None
        for title, data in sorted(self.catalog.items(), key=lambda x: x[1]["category"]):
            if data["category"] != current_cat:
                current_cat = data["category"]
                lines.append(f"\n**{current_cat}**")
            stock_label = f"({data['stock']} tersedia)" if data["stock"] > 0 else "(habis)"
            lines.append(f"  [{data['code']}] {title.title()} — {stock_label}")
        return "\n".join(lines)

    def format_categories(self) -> str:
        lines = ["**Kategori buku yang tersedia:**\n"]
        for cat in sorted(self.categories):
            count = sum(1 for b in self.catalog.values() if b["category"] == cat)
            lines.append(f"- {cat} ({count} judul)")
        lines.append("\nKetik nama kategori untuk mencari buku.")
        return "\n".join(lines)

    def get_info(self, key: str) -> str:
        return self.info.get(key, "")
