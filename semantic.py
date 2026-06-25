# semantic.py
# ============================================================
# ANALISA SEMANTIK — COMPILER MINI BASA JAWA
# Ngecek kebenaran logika kode sumber:
#   - Variabel kudu dideklarasi sadurunge digunakake
#   - Ora oleh mbagi karo nol
#   - Tipe data kudu cocok
#   - Fungsi kudu dideklarasi sadurunge dipanggil
# ============================================================

from ast_node import (
    ProgramNode, DeklarasiNode, AssignNode, BinOpNode,
    AngkaNode, StringNode, BoolNode, VarNode,
    CetakNode, LeboknoNode, YenNode, SelawaseNode,
    GaweaNode, BaliNode, KondisiNode
)

class AnalisaSemantik:
    """Kelas kanggo nindakake analisa semantik ing AST."""

    def __init__(self):
        self.variabel_dideklarasi = {}  # { jeneng: tipe } variabel kang wis didaftarake
        self.fungsi_dideklarasi   = {}  # { jeneng: params } fungsi kang wis didaftarake
        self.kesalahan            = []  # daftar kesalahan kang ditemokake
        self.peringatan           = []  # daftar peringatan kang ditemokake

    # ── Titik Mlebu ─────────────────────────────────────────

    def analisa(self, program_node):
        """Mlebu saka simpul akar ProgramNode."""
        for stmt in program_node.statements:
            self.analisa_statement(stmt)
        self.laporan()

    # ── Analisa Statement ───────────────────────────────────

    def analisa_statement(self, node):
        """Milih cara analisa adhedhasar jinis simpul."""
        if isinstance(node, DeklarasiNode):
            self.analisa_deklarasi(node)
        elif isinstance(node, AssignNode):
            self.analisa_assign(node)
        elif isinstance(node, CetakNode):
            self.analisa_ekspresi(node.ekspresi)
        elif isinstance(node, LeboknoNode):
            # Input saka pangguna tansah dianggep ukara (string)
            self.variabel_dideklarasi[node.nama] = 'ukara'
        elif isinstance(node, YenNode):
            self.analisa_yen(node)
        elif isinstance(node, SelawaseNode):
            self.analisa_selawase(node)
        elif isinstance(node, GaweaNode):
            self.analisa_gawea(node)
        elif isinstance(node, BaliNode):
            self.analisa_ekspresi(node.ekspresi)

    # ── Analisa Deklarasi Variabel ──────────────────────────

    def analisa_deklarasi(self, node):
        """Nyimpen variabel anyar ing tabel simbol."""
        tipe = self.analisa_ekspresi(node.ekspresi)
        if node.nama in self.variabel_dideklarasi:
            # Variabel kang wis ana, uncal peringatan
            self.peringatan.append(
                f"[PERINGATAN] Variabel '{node.nama}' dideklarasi kaping pindho."
            )
        self.variabel_dideklarasi[node.nama] = tipe

    # ── Analisa Assignment ──────────────────────────────────

    def analisa_assign(self, node):
        """Ngecek yen variabel wis dideklarasi sadurunge diisi."""
        if node.nama not in self.variabel_dideklarasi:
            self.kesalahan.append(
                f"[KESALAHAN SEMANTIK] Variabel '{node.nama}' "
                f"durung dideklarasi! Gunakake 'wahana {node.nama} = ...'"
            )
        self.analisa_ekspresi(node.ekspresi)

    # ── Analisa Kondisi Yen ─────────────────────────────────

    def analisa_yen(self, node):
        """Analisa blok yen lan menawa."""
        self.analisa_kondisi(node.kondisi)
        for stmt in node.blok_bener:
            self.analisa_statement(stmt)
        if node.blok_salah:
            for stmt in node.blok_salah:
                self.analisa_statement(stmt)

    # ── Analisa Perulangan Selawase ─────────────────────────

    def analisa_selawase(self, node):
        """Analisa blok perulangan selawase."""
        self.analisa_kondisi(node.kondisi)
        for stmt in node.blok:
            self.analisa_statement(stmt)

    # ── Analisa Fungsi Gawea ────────────────────────────────

    def analisa_gawea(self, node):
        """Nyimpen fungsi anyar lan analisa isine."""
        if node.nama in self.fungsi_dideklarasi:
            self.peringatan.append(
                f"[PERINGATAN] Fungsi '{node.nama}' dideklarasi kaping pindho."
            )
        self.fungsi_dideklarasi[node.nama] = node.params

        # Simpen parameter fungsi minangka variabel lokal
        for param in node.params:
            self.variabel_dideklarasi[param] = 'angka'

        for stmt in node.blok:
            self.analisa_statement(stmt)

    # ── Analisa Kondisi Bandingan ───────────────────────────

    def analisa_kondisi(self, node):
        """Analisa loro sisih kondisi bandingan."""
        if isinstance(node, KondisiNode):
            self.analisa_ekspresi(node.kiwa)
            self.analisa_ekspresi(node.tengen)

    # ── Analisa Ekspresi ────────────────────────────────────

    def analisa_ekspresi(self, node):
        """Ngitung tipe ekspresi lan ngecek kesalahan logika."""
        if isinstance(node, AngkaNode):
            return 'angka'

        if isinstance(node, StringNode):
            return 'ukara'

        if isinstance(node, BoolNode):
            return 'garis'

        if isinstance(node, VarNode):
            # Priksa yen variabel wis dideklarasi
            if node.nama not in self.variabel_dideklarasi:
                self.kesalahan.append(
                    f"[KESALAHAN SEMANTIK] Variabel '{node.nama}' "
                    f"durung dideklarasi!"
                )
                return 'ora_dikenal'
            return self.variabel_dideklarasi[node.nama]

        if isinstance(node, BinOpNode):
            tipe_kiwa   = self.analisa_ekspresi(node.kiwa)
            tipe_tengen = self.analisa_ekspresi(node.tengen)

            # Priksa bagi karo nol
            if node.operator == '/' and isinstance(node.tengen, AngkaNode):
                if node.tengen.nilai == 0:
                    self.kesalahan.append(
                        "[KESALAHAN SEMANTIK] Ora oleh mbagi karo nol!"
                    )

            # Priksa tipe data cocok
            if tipe_kiwa == 'ukara' and node.operator in ('-', '*', '/'):
                self.kesalahan.append(
                    f"[KESALAHAN SEMANTIK] Operator '{node.operator}' "
                    f"ora bisa digunakake kanggo ukara (teks)."
                )

            # Ukara + apa wae = ukara (penggabungan teks)
            if tipe_kiwa == 'ukara' or tipe_tengen == 'ukara':
                return 'ukara'
            return 'angka'

        return 'ora_dikenal'

    # ── Laporan Asil Analisa ────────────────────────────────

    def laporan(self):
        """Nampilake laporan asil analisa semantik."""
        print("\n[ LAPORAN ANALISA SEMANTIK ]")
        if not self.kesalahan and not self.peringatan:
            print("  ✓ Ora ana kesalahan semantik!")
        if self.peringatan:
            for p in self.peringatan:
                print(f"  ⚠  {p}")
        if self.kesalahan:
            for k in self.kesalahan:
                print(f"  ✗  {k}")
            raise RuntimeError(
                f"\n[ANALISA SEMANTIK GAGAL] Ketemu {len(self.kesalahan)} kesalahan."
            )
        print(f"\n  Variabel kang dideklarasi : {list(self.variabel_dideklarasi.keys())}")
        print(f"  Fungsi kang dideklarasi   : {list(self.fungsi_dideklarasi.keys())}")
