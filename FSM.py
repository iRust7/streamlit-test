from engine import Engine

STATE_DEFAULT  = "DEFAULT"
STATE_ACTIVE   = "ACTIVE"
STATE_BROWSE   = "BROWSE"
STATE_BORROW   = "BORROW"
STATE_CONFIRM  = "CONFIRM"
STATE_END      = "END"


class FSM:
    def __init__(self):
        self.engine         = Engine()
        self.state          = STATE_DEFAULT
        self.pending_book   = None

    def transition(self, user_input: str) -> str:
        intent = self.engine.detect_intent(user_input)

        if intent == "RESET":
            self.state        = STATE_DEFAULT
            self.pending_book = None
            return "Sesi direset. Ketik **halo** untuk memulai kembali."

        if self.state == STATE_DEFAULT:
            return self._from_default(intent, user_input)

        if self.state == STATE_ACTIVE:
            return self._from_active(intent, user_input)

        if self.state == STATE_BROWSE:
            return self._from_browse(intent, user_input)

        if self.state == STATE_BORROW:
            return self._from_borrow(intent, user_input)

        if self.state == STATE_CONFIRM:
            return self._from_confirm(intent, user_input)

        if self.state == STATE_END:
            if intent == "GREET":
                self.state = STATE_ACTIVE
                return "Selamat datang kembali! Ada yang bisa dibantu?"
            return "Ketik **halo** untuk memulai sesi baru."

        return "Terjadi kesalahan. Ketik **reset** untuk memulai ulang."

    def _from_default(self, intent: str, text: str) -> str:
        self.state = STATE_ACTIVE
        if intent == "GREET":
            return (
                "Halo! Selamat datang di **Perpustakaan Digital**\n\n"
                "Saya siap membantu kamu mencari, meminjam, dan mengembalikan buku.\n\n"
                "Yang bisa saya bantu:\n"
                "- Cari buku atau lihat katalog\n"
                "- Pinjam buku\n"
                "- Kembalikan buku\n"
                "- Info jam buka, denda, syarat pinjam\n\n"
                "Mau mulai dari mana?"
            )
        return self._from_active(intent, text)

    def _from_active(self, intent: str, text: str) -> str:
        if intent in ("SEARCH", "LIST_CATALOG", "BOOK_MENTIONED"):
            self.state = STATE_BROWSE
            return self._handle_search(text)

        if intent == "LIST_CATEGORY":
            self.state = STATE_BROWSE
            return self.engine.format_categories()

        if intent == "BORROW":
            book = self.engine.get_book(text)
            if book:
                self.state        = STATE_CONFIRM
                self.pending_book = book
                return (
                    f"Kamu ingin meminjam:\n\n"
                    f"{self.engine.format_book_card(book)}\n\n"
                    f"Konfirmasi peminjaman? Ketik **ya** atau **tidak**."
                )
            self.state = STATE_BORROW
            return "Buku apa yang ingin dipinjam? Sebutkan judul bukunya."

        if intent == "RETURN":
            return (
                self.engine.get_info("cara_kembali")
                + "\n\nSilakan datang ke meja sirkulasi untuk proses pengembalian."
            )

        if intent == "CHECK_STOCK":
            return self._handle_stock(text)

        if intent == "ASK_HOURS":
            return "**Jam Operasional Perpustakaan:**\n\n" + self.engine.get_info("jam_buka")

        if intent == "ASK_RULES":
            return self.engine.get_info("syarat_pinjam")

        if intent == "ASK_FINE":
            return self.engine.get_info("denda")

        if intent == "ASK_MEMBERSHIP":
            return self.engine.get_info("keanggotaan")

        if intent == "ASK_RETURN_INFO":
            return self.engine.get_info("cara_kembali")

        if intent == "THANKS":
            self.state = STATE_END
            return (
                "Sama-sama! Semoga bermanfaat.\n\n"
                "Sampai jumpa di Perpustakaan Digital. Selamat belajar!"
            )

        if intent == "EXIT":
            self.state = STATE_END
            return "Sampai jumpa! Selamat belajar."

        return (
            "Maaf, saya kurang mengerti. Yang bisa saya bantu:\n\n"
            "- **cari [judul buku]** — mencari buku\n"
            "- **katalog** — lihat semua buku\n"
            "- **pinjam [judul buku]** — meminjam buku\n"
            "- **jam buka** — info operasional\n"
            "- **syarat pinjam** — ketentuan peminjaman"
        )

    def _from_browse(self, intent: str, text: str) -> str:
        if intent == "BORROW":
            book = self.engine.get_book(text)
            if book:
                self.state        = STATE_CONFIRM
                self.pending_book = book
                return (
                    f"Kamu ingin meminjam:\n\n"
                    f"{self.engine.format_book_card(book)}\n\n"
                    f"Konfirmasi peminjaman? Ketik **ya** atau **tidak**."
                )
            self.state = STATE_BORROW
            return "Sebutkan judul buku yang ingin dipinjam."

        if intent in ("SEARCH", "BOOK_MENTIONED", "LIST_CATALOG"):
            return self._handle_search(text)

        if intent == "LIST_CATEGORY":
            return self.engine.format_categories()

        if intent == "CHECK_STOCK":
            return self._handle_stock(text)

        self.state = STATE_ACTIVE
        return self._from_active(intent, text)

    def _from_borrow(self, intent: str, text: str) -> str:
        book = self.engine.get_book(text)
        if book:
            self.state        = STATE_CONFIRM
            self.pending_book = book
            return (
                f"Kamu ingin meminjam:\n\n"
                f"{self.engine.format_book_card(book)}\n\n"
                f"Konfirmasi peminjaman? Ketik **ya** atau **tidak**."
            )
        if intent == "NO":
            self.state = STATE_ACTIVE
            return "Oke, peminjaman dibatalkan. Ada yang bisa dibantu lagi?"
        return "Sebutkan judul buku yang ingin dipinjam, atau ketik **tidak** untuk batal."

    def _from_confirm(self, intent: str, text: str) -> str:
        if intent == "YES" and self.pending_book:
            book = self.pending_book
            if book["stock"] > 0:
                self.engine.catalog[book["title"]]["stock"] -= 1
                self.pending_book = None
                self.state = STATE_ACTIVE
                return (
                    f"Peminjaman berhasil!\n\n"
                    f"**{book['title'].title()}** [{book['code']}]\n\n"
                    f"Silakan ambil buku di meja sirkulasi dengan menunjukkan kartu anggota.\n"
                    f"Batas pinjam: **7 hari**. Denda: Rp500/hari jika terlambat.\n\n"
                    f"Ada yang bisa dibantu lagi?"
                )
            self.pending_book = None
            self.state = STATE_ACTIVE
            return (
                f"Maaf, stok **{book['title'].title()}** habis saat ini.\n\n"
                f"Coba cari buku lain atau datang kembali beberapa hari ke depan."
            )

        if intent == "NO":
            self.pending_book = None
            self.state = STATE_ACTIVE
            return "Peminjaman dibatalkan. Ada yang bisa dibantu lagi?"

        return "Ketik **ya** untuk konfirmasi peminjaman atau **tidak** untuk batal."

    def _handle_search(self, text: str) -> str:
        books = self.engine.find_books(text)
        if books:
            lines = [f"Ditemukan {len(books)} buku:\n"]
            for b in books:
                lines.append(self.engine.format_book_card(b))
                lines.append("---")
            lines.append("Ketik **pinjam [judul]** untuk meminjam.")
            return "\n".join(lines)
        return (
            self.engine.format_catalog()
            + "\n\nTidak ditemukan buku yang cocok. Berikut katalog lengkap."
        )

    def _handle_stock(self, text: str) -> str:
        book = self.engine.get_book(text)
        if book:
            if book["stock"] > 0:
                return f"**{book['title'].title()}** tersedia: **{book['stock']} buku**.\nKetik **pinjam {book['title']}** untuk meminjam."
            return f"**{book['title'].title()}** sedang tidak tersedia (stok habis).\nCoba kembali beberapa hari lagi."
        return self.engine.format_catalog() + "\n\nSebutkan judul buku untuk cek ketersediaannya."
