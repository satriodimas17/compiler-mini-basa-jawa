# parser.py
# ============================================================
# PARSER — COMPILER MINI BAHASA JAWA
# Ngecek urutan token lan mbangun Parse Tree / AST
# ============================================================

from ast_node import (
    ProgramNode, DeklarasiNode, AssignNode, BinOpNode,
    AngkaNode, StringNode, BoolNode, VarNode,
    CetakNode, LeboknoNode, YenNode, SelawaseNode,
    GaweaNode, BaliNode, KondisiNode
)

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos    = 0

    # ── Helper ──────────────────────────────────────────────

    def token_saiki(self):
        """Njupuk token saiki tanpa maju."""
        return self.tokens[self.pos]

    def maju(self):
        """Njupuk token saiki lan maju menyang token sabanjure."""
        tok = self.tokens[self.pos]
        if tok.tipe != 'EOF':
            self.pos += 1
        return tok

    def cocokake(self, tipe, nilai=None):
        """Mriksa token saiki, yen cocok maju. Yen ora, lempar error."""
        tok = self.token_saiki()
        if tok.tipe != tipe:
            raise SyntaxError(
                f"[KESALAHAN PARSER] Ngenteni '{tipe}' "
                f"nanging ketemu '{tok.tipe}' ('{tok.nilai}') "
                f"ing baris {tok.baris}"
            )
        if nilai and tok.nilai != nilai:
            raise SyntaxError(
                f"[KESALAHAN PARSER] Ngenteni '{nilai}' "
                f"nanging ketemu '{tok.nilai}' ing baris {tok.baris}"
            )
        return self.maju()

    # ── Entry Point ─────────────────────────────────────────

    def parse(self):
        """Mulai parsing — ngasilake ProgramNode (root AST)."""
        statements = []
        while self.token_saiki().tipe != 'EOF':
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
        return ProgramNode(statements)

    # ── Statement ───────────────────────────────────────────

    def parse_statement(self):
        tok = self.token_saiki()

        # Keyword statements
        if tok.tipe == 'KEYWORD':
            if tok.nilai == 'wahana':
                return self.parse_deklarasi()
            elif tok.nilai == 'cetak':
                return self.parse_cetak()
            elif tok.nilai == 'yen':
                return self.parse_yen()
            elif tok.nilai == 'selawase':
                return self.parse_selawase()
            elif tok.nilai == 'gawea':
                return self.parse_gawea()
            elif tok.nilai == 'bali':
                return self.parse_bali()

        # Assignment: IDENTIFIER = expr
        if tok.tipe == 'IDENTIFIER':
            next_tok = self.tokens[self.pos + 1]
            if next_tok.tipe == 'OPERATOR' and next_tok.nilai == '=':
                return self.parse_assignment()

        # Lewati token yang tidak dikenal
        self.maju()
        return None

    # ── Deklarasi Variabel ──────────────────────────────────

    def parse_deklarasi(self):
        """wahana x = ekspresi"""
        self.cocokake('KEYWORD', 'wahana')
        nama = self.cocokake('IDENTIFIER').nilai
        self.cocokake('OPERATOR', '=')
        ekspresi = self.parse_expr()
        return DeklarasiNode(nama, ekspresi)

    # ── Assignment ──────────────────────────────────────────

    def parse_assignment(self):
        """x = ekspresi"""
        nama = self.cocokake('IDENTIFIER').nilai
        self.cocokake('OPERATOR', '=')

        # Cek lebokno (input)
        if self.token_saiki().tipe == 'KEYWORD' and self.token_saiki().nilai == 'lebokno':
            return self.parse_lebokno(nama)

        ekspresi = self.parse_expr()
        return AssignNode(nama, ekspresi)

    # ── Cetak ────────────────────────────────────────────────

    def parse_cetak(self):
        """cetak(ekspresi)"""
        self.cocokake('KEYWORD', 'cetak')
        self.cocokake('DELIMITER', '(')
        ekspresi = self.parse_expr()
        self.cocokake('DELIMITER', ')')
        return CetakNode(ekspresi)

    # ── Lebokno (Input) ──────────────────────────────────────

    def parse_lebokno(self, nama):
        """x = lebokno("pesen")"""
        self.cocokake('KEYWORD', 'lebokno')
        self.cocokake('DELIMITER', '(')
        pesen = self.cocokake('STRING').nilai
        self.cocokake('DELIMITER', ')')
        return LeboknoNode(nama, pesen)

    # ── Yen (If) ─────────────────────────────────────────────

    def parse_yen(self):
        """yen (kondisi) { ... } menawa { ... }"""
        self.cocokake('KEYWORD', 'yen')
        self.cocokake('DELIMITER', '(')
        kondisi = self.parse_kondisi()
        self.cocokake('DELIMITER', ')')
        self.cocokake('DELIMITER', '{')
        blok_bener = self.parse_blok()
        self.cocokake('DELIMITER', '}')

        blok_salah = None
        if self.token_saiki().tipe == 'KEYWORD' and self.token_saiki().nilai == 'menawa':
            self.maju()
            self.cocokake('DELIMITER', '{')
            blok_salah = self.parse_blok()
            self.cocokake('DELIMITER', '}')

        return YenNode(kondisi, blok_bener, blok_salah)

    # ── Selawase (While) ─────────────────────────────────────

    def parse_selawase(self):
        """selawase (kondisi) { ... }"""
        self.cocokake('KEYWORD', 'selawase')
        self.cocokake('DELIMITER', '(')
        kondisi = self.parse_kondisi()
        self.cocokake('DELIMITER', ')')
        self.cocokake('DELIMITER', '{')
        blok = self.parse_blok()
        self.cocokake('DELIMITER', '}')
        return SelawaseNode(kondisi, blok)

    # ── Gawea (Function) ─────────────────────────────────────

    def parse_gawea(self):
        """gawea jeneng(params) { ... }"""
        self.cocokake('KEYWORD', 'gawea')
        nama = self.cocokake('IDENTIFIER').nilai
        self.cocokake('DELIMITER', '(')
        params = []
        while self.token_saiki().tipe == 'IDENTIFIER':
            params.append(self.cocokake('IDENTIFIER').nilai)
            if self.token_saiki().nilai == ',':
                self.maju()
        self.cocokake('DELIMITER', ')')
        self.cocokake('DELIMITER', '{')
        blok = self.parse_blok()
        self.cocokake('DELIMITER', '}')
        return GaweaNode(nama, params, blok)

    # ── Bali (Return) ────────────────────────────────────────

    def parse_bali(self):
        """bali ekspresi"""
        self.cocokake('KEYWORD', 'bali')
        ekspresi = self.parse_expr()
        return BaliNode(ekspresi)

    # ── Blok ─────────────────────────────────────────────────

    def parse_blok(self):
        """Kumpulan statement ing njero { }"""
        statements = []
        while (self.token_saiki().tipe != 'EOF' and
               self.token_saiki().nilai != '}'):
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
        return statements

    # ── Kondisi ──────────────────────────────────────────────

    def parse_kondisi(self):
        """ekspresi operator ekspresi (tuladha: x > 5)"""
        kiwa = self.parse_expr()
        op   = self.cocokake('COMPARATOR').nilai
        tengen = self.parse_expr()
        return KondisiNode(kiwa, op, tengen)

    # ── Ekspresi ─────────────────────────────────────────────

    def parse_expr(self):
        """Ekspresi aritmetika: term (+|-) term"""
        kiwa = self.parse_term()
        while (self.token_saiki().tipe == 'OPERATOR' and
               self.token_saiki().nilai in ('+', '-')):
            op = self.maju().nilai
            tengen = self.parse_term()
            kiwa = BinOpNode(kiwa, op, tengen)
        return kiwa

    def parse_term(self):
        """Term: factor (*|/) factor"""
        kiwa = self.parse_factor()
        while (self.token_saiki().tipe == 'OPERATOR' and
               self.token_saiki().nilai in ('*', '/')):
            op = self.maju().nilai
            tengen = self.parse_factor()
            kiwa = BinOpNode(kiwa, op, tengen)
        return kiwa

    def parse_factor(self):
        """Factor: angka, string, variabel, ekspresi kurung"""
        tok = self.token_saiki()

        if tok.tipe == 'NUMBER':
            self.maju()
            val = float(tok.nilai) if '.' in tok.nilai else int(tok.nilai)
            return AngkaNode(val)

        if tok.tipe == 'STRING':
            self.maju()
            return StringNode(tok.nilai[1:-1])  # Buang tanda petik

        if tok.tipe == 'KEYWORD' and tok.nilai == 'bener':
            self.maju()
            return BoolNode(True)

        if tok.tipe == 'KEYWORD' and tok.nilai == 'salah':
            self.maju()
            return BoolNode(False)

        if tok.tipe == 'IDENTIFIER':
            self.maju()
            return VarNode(tok.nilai)

        if tok.tipe == 'DELIMITER' and tok.nilai == '(':
            self.maju()
            ekspresi = self.parse_expr()
            self.cocokake('DELIMITER', ')')
            return ekspresi

        raise SyntaxError(
            f"[KESALAHAN PARSER] Token ora dikenal: "
            f"'{tok.nilai}' ing baris {tok.baris}"
        )


# ── Visualisasi Parse Tree ───────────────────────────────────

def tampilake_ast(node, level=0, prefix=""):
    """Nampilake struktur AST kanthi garis wit."""
    indent = "    " * level
    nama_kelas = type(node).__name__

    info = ""
    if hasattr(node, 'nama'):    info = f" → {node.nama}"
    elif hasattr(node, 'nilai'): info = f" → {node.nilai}"
    elif hasattr(node, 'operator'): info = f" [{node.operator}]"

    print(indent + prefix + nama_kelas + info)

    anak = []
    if hasattr(node, 'statements'): anak = node.statements
    elif hasattr(node, 'blok_bener'):
        if node.kondisi: anak.append(node.kondisi)
        anak += node.blok_bener
        if node.blok_salah: anak += node.blok_salah
    elif hasattr(node, 'blok'): anak = [node.kondisi] + node.blok
    elif hasattr(node, 'kiwa'):
        anak = [node.kiwa, node.tengen]
    elif hasattr(node, 'ekspresi') and node.ekspresi is not None:
        anak = [node.ekspresi]

    for i, a in enumerate(anak):
        if a and isinstance(a, object) and hasattr(a, '__class__'):
            p = "└── " if i == len(anak) - 1 else "├── "
            tampilake_ast(a, level + 1, p)
