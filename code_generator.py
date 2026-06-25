# code_generator.py
# ============================================================
# CODE GENERATOR — COMPILER MINI BASA JAWA
# Ngowahi AST dadi kode Python sing bisa dieksekusi
# Tuladha owahan:
#   wahana x = 10      →  x = 10
#   cetak(x)           →  print(x)
#   yen (x > y) { }   →  if x > y:
#   menawa { }         →  else:
#   selawase (n<10){}  →  while n < 10:
#   gawea tambah(a,b)  →  def tambah(a, b):
#   bali x + 1         →  return x + 1
# ============================================================

from ast_node import (
    ProgramNode, DeklarasiNode, AssignNode, BinOpNode,
    AngkaNode, StringNode, BoolNode, VarNode,
    CetakNode, LeboknoNode, YenNode, SelawaseNode,
    GaweaNode, BaliNode, KondisiNode
)

class CodeGenerator:
    """Kelas kanggo ngowahi AST dadi kode Python."""

    def __init__(self):
        self.kode_output = []  # wadhah baris-baris kode Python
        self.indentasi   = 0   # level inden saiki

    # ── Helper Nulis Kode ───────────────────────────────────

    def tabs(self):
        """Ngasilake spasi inden adhedhasar level saiki."""
        return "    " * self.indentasi

    def tambah(self, baris):
        """Nambah siji baris kode menyang output."""
        self.kode_output.append(self.tabs() + baris)

    def hasilake(self):
        """Ngasilake kabeh kode Python minangka teks."""
        return "\n".join(self.kode_output)

    # ── Titik Mlebu ─────────────────────────────────────────

    def generate(self, program_node):
        """Mulai generate saka simpul akar ProgramNode."""
        self.tambah("# ============================================")
        self.tambah("# KODE ASIL GENERATE — COMPILER BASA JAWA")
        self.tambah("# ============================================")
        self.tambah("")

        # Generate saben statement ing program
        for stmt in program_node.statements:
            self.gen_statement(stmt)

        return self.hasilake()

    # ── Generate Statement ──────────────────────────────────

    def gen_statement(self, node):
        """Milih cara generate adhedhasar jinis simpul."""
        if isinstance(node, DeklarasiNode):
            self.gen_deklarasi(node)
        elif isinstance(node, AssignNode):
            self.gen_assign(node)
        elif isinstance(node, CetakNode):
            self.gen_cetak(node)
        elif isinstance(node, LeboknoNode):
            self.gen_lebokno(node)
        elif isinstance(node, YenNode):
            self.gen_yen(node)
        elif isinstance(node, SelawaseNode):
            self.gen_selawase(node)
        elif isinstance(node, GaweaNode):
            self.gen_gawea(node)
        elif isinstance(node, BaliNode):
            self.gen_bali(node)
        elif isinstance(node, ProgramNode):
            # Simpul program ing njero (asil dead code removal)
            for s in node.statements:
                self.gen_statement(s)

    # ── wahana x = nilai → x = nilai ────────────────────────

    def gen_deklarasi(self, node):
        """Ngowahi deklarasi wahana dadi assignment Python."""
        self.tambah(f"{node.nama} = {self.gen_ekspresi(node.ekspresi)}")

    # ── x = ekspresi → x = ekspresi ─────────────────────────

    def gen_assign(self, node):
        """Ngowahi assignment dadi kode Python."""
        self.tambah(f"{node.nama} = {self.gen_ekspresi(node.ekspresi)}")

    # ── cetak(x) → print(x) ─────────────────────────────────

    def gen_cetak(self, node):
        """Ngowahi cetak dadi print Python."""
        self.tambah(f"print({self.gen_ekspresi(node.ekspresi)})")

    # ── x = lebokno("pesen") → x = input("pesen") ───────────

    def gen_lebokno(self, node):
        """Ngowahi lebokno dadi input Python."""
        self.tambah(f"{node.nama} = input({node.pesen!r})")

    # ── yen (kondisi) { } → if kondisi: ─────────────────────

    def gen_yen(self, node):
        """Ngowahi yen/menawa dadi if/else Python."""
        kondisi = self.gen_kondisi(node.kondisi)
        self.tambah(f"if {kondisi}:")
        self.indentasi += 1
        for stmt in node.blok_bener:
            self.gen_statement(stmt)
        if not node.blok_bener:
            self.tambah("pass")
        self.indentasi -= 1
        if node.blok_salah:
            self.tambah("else:")
            self.indentasi += 1
            for stmt in node.blok_salah:
                self.gen_statement(stmt)
            self.indentasi -= 1

    # ── selawase (kondisi) { } → while kondisi: ─────────────

    def gen_selawase(self, node):
        """Ngowahi selawase dadi while Python."""
        kondisi = self.gen_kondisi(node.kondisi)
        self.tambah(f"while {kondisi}:")
        self.indentasi += 1
        for stmt in node.blok:
            self.gen_statement(stmt)
        if not node.blok:
            self.tambah("pass")
        self.indentasi -= 1

    # ── gawea nama(params) { } → def nama(params): ──────────

    def gen_gawea(self, node):
        """Ngowahi gawea dadi def Python."""
        params = ", ".join(node.params)
        self.tambah(f"def {node.nama}({params}):")
        self.indentasi += 1
        for stmt in node.blok:
            self.gen_statement(stmt)
        if not node.blok:
            self.tambah("pass")
        self.indentasi -= 1
        self.tambah("")  # baris kosong sawise fungsi

    # ── bali ekspresi → return ekspresi ─────────────────────

    def gen_bali(self, node):
        """Ngowahi bali dadi return Python."""
        self.tambah(f"return {self.gen_ekspresi(node.ekspresi)}")

    # ── Generate Ekspresi ───────────────────────────────────

    def gen_ekspresi(self, node):
        """Ngowahi simpul ekspresi dadi teks kode Python."""
        if isinstance(node, AngkaNode):
            return str(node.nilai)
        if isinstance(node, StringNode):
            return repr(node.nilai)
        if isinstance(node, BoolNode):
            return "True" if node.nilai else "False"
        if isinstance(node, VarNode):
            return node.nama
        if isinstance(node, BinOpNode):
            kiwa   = self.gen_ekspresi(node.kiwa)
            tengen = self.gen_ekspresi(node.tengen)
            return f"({kiwa} {node.operator} {tengen})"
        return "None"

    # ── Generate Kondisi ────────────────────────────────────

    def gen_kondisi(self, node):
        """Ngowahi simpul kondisi dadi teks kode Python."""
        if isinstance(node, KondisiNode):
            kiwa   = self.gen_ekspresi(node.kiwa)
            tengen = self.gen_ekspresi(node.tengen)
            return f"{kiwa} {node.operator} {tengen}"
        if isinstance(node, BoolNode):
            return "True" if node.nilai else "False"
        return "True"
