# ast_node.py
# ============================================================
# SIMPUL-SIMPUL AST — COMPILER MINI BASA JAWA
# Saben kelas nggambarake siji jinis simpul ing wit AST
# ============================================================

class ASTNode:
    """Simpul dhasar kanggo kabeh jinis simpul ing AST."""
    def __repr__(self):
        return self.__class__.__name__

# ── Simpul Program (akar saka kabeh wit) ─────────────────────
class ProgramNode(ASTNode):
    def __init__(self, statements):
        self.statements = statements  # daftar kabeh statement

# ── Simpul Deklarasi Variabel (wahana x = 10) ────────────────
class DeklarasiNode(ASTNode):
    def __init__(self, nama, ekspresi):
        self.nama     = nama       # jeneng variabel
        self.ekspresi = ekspresi   # nilai awal variabel

# ── Simpul Assignment (x = 20) ───────────────────────────────
class AssignNode(ASTNode):
    def __init__(self, nama, ekspresi):
        self.nama     = nama       # jeneng variabel
        self.ekspresi = ekspresi   # nilai anyar

# ── Simpul Operasi Biner (+, -, *, /) ────────────────────────
class BinOpNode(ASTNode):
    def __init__(self, kiwa, operator, tengen):
        self.kiwa     = kiwa       # ekspresi sisih kiwa
        self.operator = operator   # tandha operator
        self.tengen   = tengen     # ekspresi sisih tengen

# ── Simpul Angka ─────────────────────────────────────────────
class AngkaNode(ASTNode):
    def __init__(self, nilai):
        self.nilai = nilai         # nilai angka (int utawa float)

# ── Simpul Teks/String ───────────────────────────────────────
class StringNode(ASTNode):
    def __init__(self, nilai):
        self.nilai = nilai         # isi teks tanpa tandha petik

# ── Simpul Boolean (bener/salah) ─────────────────────────────
class BoolNode(ASTNode):
    def __init__(self, nilai):
        self.nilai = nilai         # True utawa False

# ── Simpul Variabel (jeneng variabel ing ekspresi) ───────────
class VarNode(ASTNode):
    def __init__(self, nama):
        self.nama = nama           # jeneng variabel kang dirujuk

# ── Simpul Cetak / Print ─────────────────────────────────────
class CetakNode(ASTNode):
    def __init__(self, ekspresi):
        self.ekspresi = ekspresi   # nilai kang arep ditampilake

# ── Simpul Lebokno / Input ───────────────────────────────────
class LeboknoNode(ASTNode):
    def __init__(self, nama, pesen):
        self.nama  = nama          # variabel kang nampa input
        self.pesen = pesen         # teks pitakon kanggo pangguna

# ── Simpul Yen / If ──────────────────────────────────────────
class YenNode(ASTNode):
    def __init__(self, kondisi, blok_bener, blok_salah=None):
        self.kondisi    = kondisi      # ekspresi kondisi
        self.blok_bener = blok_bener   # dieksekusi yen kondisi bener
        self.blok_salah = blok_salah   # dieksekusi yen kondisi salah (menawa)

# ── Simpul Selawase / While ──────────────────────────────────
class SelawaseNode(ASTNode):
    def __init__(self, kondisi, blok):
        self.kondisi = kondisi     # kondisi perulangan
        self.blok    = blok        # isi perulangan

# ── Simpul Gawea / Fungsi ────────────────────────────────────
class GaweaNode(ASTNode):
    def __init__(self, nama, params, blok):
        self.nama   = nama         # jeneng fungsi
        self.params = params       # daftar parameter
        self.blok   = blok         # isi fungsi

# ── Simpul Bali / Return ─────────────────────────────────────
class BaliNode(ASTNode):
    def __init__(self, ekspresi):
        self.ekspresi = ekspresi   # nilai kang dibali

# ── Simpul Kondisi Bandingan (==, !=, <, >, <=, >=) ─────────
class KondisiNode(ASTNode):
    def __init__(self, kiwa, operator, tengen):
        self.kiwa     = kiwa       # ekspresi sisih kiwa
        self.operator = operator   # tandha bandingan
        self.tengen   = tengen     # ekspresi sisih tengen
