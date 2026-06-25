# desain_bahasa.py
# ============================================================
# DESAIN BASA JAWA — COMPILER MINI
# Tabel Simbol, Grammar, Tembung Kunci, Fungsi Gawan
# ============================================================

# ── 1. TEMBUNG KUNCI (KEYWORD) BASA JAWA ────────────────────
# Owahan tembung kunci saka basa umum menyang Basa Jawa

KEYWORDS = {
    'yen'       : 'IF',        # yen   → yen/menawa (kondisi)
    'menawa'    : 'ELSE',      # menawa → yen ora (kondisi liyane)
    'selawase'  : 'WHILE',     # selawase → selawase (perulangan)
    'baleni'    : 'FOR',       # baleni → mbaleni (perulangan)
    'bali'      : 'RETURN',    # bali → bali (ngasilake nilai)
    'cetak'     : 'PRINT',     # cetak → tampilake menyang layar
    'lebokno'   : 'INPUT',     # lebokno → lebokno data saka pangguna
    'wahana'    : 'VAR',       # wahana → wadhah variabel
    'gawea'     : 'FUNC',      # gawea → gawe fungsi anyar
    'bener'     : 'TRUE',      # bener → nilai bener (true)
    'salah'     : 'FALSE',     # salah → nilai salah (false)
    'kosong'    : 'NULL',      # kosong → ora ana nilai (null)
}

# ── 2. TIPE DATA ─────────────────────────────────────────────
TIPE_DATA = {
    'angka'  : 'NUMBER',   # angka → bilangan bulat utawa desimal
    'ukara'  : 'STRING',   # ukara → teks utawa tulisan
    'garis'  : 'BOOL',     # garis → nilai bener utawa salah
}

# ── 3. FUNGSI GAWAN (FUNGSI BAWAAN) ─────────────────────────
FUNGSI_BAWAAN = {
    'cetak'   : 'PRINT',    # cetak(x)   → tampilake menyang layar
    'lebokno' : 'INPUT',    # lebokno(x) → jaluk input saka pangguna
    'output'  : 'OUTPUT',   # output(x)  → padha karo cetak
}

# ── 4. TABEL SIMBOL (Symbol Table) ──────────────────────────
# Kelas kanggo nyimpen variabel lan fungsi sing wis dideklarasi

class TabelSimbol:
    def __init__(self):
        self.tabel  = {}   # { jeneng_variabel: { tipe, nilai } }
        self.fungsi = {}   # { jeneng_fungsi: { params, isi } }

    def set_variabel(self, nama, tipe, nilai=None):
        """Nyimpen variabel anyar utawa ngowahi sing wis ana."""
        self.tabel[nama] = {'tipe': tipe, 'nilai': nilai}

    def get_variabel(self, nama):
        """Njupuk data variabel. Uncal kesalahan yen ora ketemu."""
        if nama not in self.tabel:
            raise NameError(f"[KESALAHAN] Variabel '{nama}' durung dideklarasi!")
        return self.tabel[nama]

    def set_fungsi(self, nama, params, body):
        """Nyimpen deklarasi fungsi anyar."""
        self.fungsi[nama] = {'params': params, 'isi': body}

    def get_fungsi(self, nama):
        """Njupuk data fungsi. Uncal kesalahan yen ora ketemu."""
        if nama not in self.fungsi:
            raise NameError(f"[KESALAHAN] Fungsi '{nama}' durung ditemokake!")
        return self.fungsi[nama]

    def tampilake(self):
        """Nampilake kabeh isi tabel simbol."""
        print("\n[ TABEL SIMBOL ]")
        print(f"  {'NAMA':<15} {'TIPE':<10} {'NILAI'}")
        print("  " + "-" * 35)
        if not self.tabel:
            print("  (kosong)")
        for nama, info in self.tabel.items():
            print(f"  {nama:<15} {info['tipe']:<10} {info['nilai']}")
        if self.fungsi:
            print(f"\n  {'FUNGSI':<15} {'PARAMS'}")
            print("  " + "-" * 35)
            for nama, info in self.fungsi.items():
                print(f"  {nama:<15} {info['params']}")

# ── 5. GRAMMAR BASA JAWA (BNF) ──────────────────────────────
# Aturan tata basa kanggo nulis program Basa Jawa
GRAMMAR = """
=== GRAMMAR BASA JAWA (BNF) ===

<program>      ::= <statement>*

<statement>    ::= <deklarasi>
                 | <assignment>
                 | <cetak>
                 | <lebokno>
                 | <yen_stmt>
                 | <selawase_stmt>
                 | <gawea_stmt>
                 | <bali_stmt>

<deklarasi>    ::= 'wahana' IDENTIFIER '=' <expr>

<assignment>   ::= IDENTIFIER '=' <expr>

<cetak>        ::= 'cetak' '(' <expr> ')'

<lebokno>      ::= IDENTIFIER '=' 'lebokno' '(' STRING ')'

<yen_stmt>     ::= 'yen' '(' <kondisi> ')' '{' <statement>* '}'
                   [ 'menawa' '{' <statement>* '}' ]

<selawase_stmt>::= 'selawase' '(' <kondisi> ')' '{' <statement>* '}'

<gawea_stmt>   ::= 'gawea' IDENTIFIER '(' <params> ')' '{' <statement>* '}'

<bali_stmt>    ::= 'bali' <expr>

<kondisi>      ::= <expr> <op_bandingan> <expr>

<op_bandingan> ::= '==' | '!=' | '<' | '>' | '<=' | '>='

<expr>         ::= <term> ( ('+' | '-') <term> )*

<term>         ::= <factor> ( ('*' | '/') <factor> )*

<factor>       ::= NUMBER | STRING | IDENTIFIER | '(' <expr> ')'
                 | 'bener' | 'salah'

<params>       ::= IDENTIFIER (',' IDENTIFIER)*
"""

if __name__ == '__main__':
    print("=== DESAIN BASA JAWA ===")
    print("\n[ TEMBUNG KUNCI ]")
    for jawa, eng in KEYWORDS.items():
        print(f"  {jawa:<12} → {eng}")
    print("\n[ FUNGSI GAWAN ]")
    for jawa, eng in FUNGSI_BAWAAN.items():
        print(f"  {jawa:<12} → {eng}")
    print(GRAMMAR)
