# lexer.py
# ============================================================
# LEXER — COMPILER MINI BASA JAWA
# Mecah kode sumber dadi 7 jinis token
# ============================================================

import re
from desain_bahasa import KEYWORDS

# ── 7 JINIS TOKEN ────────────────────────────────────────────
# 1. NUMBER      → angka bulat lan desimal     (tuladha: 42, 3.14)
# 2. STRING      → teks kang diapit tandha petik (tuladha: "halo")
# 3. IDENTIFIER  → jeneng variabel utawa fungsi (tuladha: x, nilai)
# 4. KEYWORD     → tembung kunci Basa Jawa      (tuladha: yen, cetak)
# 5. OPERATOR    → tandha operasi aritmetika    (tuladha: +, -, *, /)
# 6. DELIMITER   → tandha kurung lan koma       (tuladha: ( ) { } ,)
# 7. COMPARATOR  → tandha bandingan             (tuladha: ==, !=, <, >)

# Pola token — COMPARATOR kudu dipriksa sadurunge OPERATOR
# supaya '==' ora kepotong dadi '=' + '='
POLA_TOKEN = [
    ('NUMBER',     r'\d+(\.\d+)?'),   # angka bulat utawa desimal
    ('STRING',     r'"[^"]*"'),        # teks diapit tandha petik
    ('COMPARATOR', r'==|!=|<=|>=|<|>'),# tandha bandingan
    ('OPERATOR',   r'[+\-*/=]'),       # tandha operasi
    ('DELIMITER',  r'[(){},;]'),       # tandha kurung lan koma
    ('NEWLINE',    r'\n'),             # ganti baris
    ('SKIP',       r'[ \t]+'),         # spasi lan tab (dilangkahi)
    ('KOMENTAR',   r'#[^\n]*'),        # komentar (dilangkahi)
    ('IDENTIFIER', r'[a-zA-Z_][a-zA-Z0-9_]*'), # jeneng variabel
]

class Token:
    """Wadhah siji token kang diwaca saka kode sumber."""
    def __init__(self, tipe, nilai, baris=0):
        self.tipe  = tipe    # jinis token (NUMBER, KEYWORD, lsp)
        self.nilai = nilai   # isi token
        self.baris = baris   # ana ing baris pira

    def __repr__(self):
        return f"Token({self.tipe}, {repr(self.nilai)}, baris={self.baris})"

class Lexer:
    """Kelas utama kanggo mecah kode sumber dadi daftar token."""
    def __init__(self, kode):
        self.kode   = kode   # kode sumber Basa Jawa
        self.pos    = 0      # posisi saiki ing kode
        self.baris  = 1      # cacah baris saiki
        self.tokens = []     # wadhah asil token

    def tokenize(self):
        """Mecah kode sumber dadi daftar token."""
        while self.pos < len(self.kode):
            cocok = None

            for tipe, pola in POLA_TOKEN:
                regex = re.compile(pola)
                cocok = regex.match(self.kode, self.pos)

                if cocok:
                    nilai = cocok.group()

                    if tipe == 'NEWLINE':
                        # Itung cacah baris
                        self.baris += 1

                    elif tipe in ('SKIP', 'KOMENTAR'):
                        # Dilangkahi — spasi lan komentar ora dadi token
                        pass

                    elif tipe == 'IDENTIFIER':
                        # Priksa apa jenenge KEYWORD
                        if nilai in KEYWORDS:
                            self.tokens.append(Token('KEYWORD', nilai, self.baris))
                        else:
                            self.tokens.append(Token('IDENTIFIER', nilai, self.baris))

                    else:
                        # Token liyane langsung disimpen
                        self.tokens.append(Token(tipe, nilai, self.baris))

                    self.pos = cocok.end()
                    break

            if not cocok:
                # Karakter ora dikenal — uncal kesalahan
                raise SyntaxError(
                    f"[KESALAHAN LEXER] Karakter ora dikenal: "
                    f"'{self.kode[self.pos]}' ing baris {self.baris}"
                )

        # Tambah tandha pungkasan (End Of File)
        self.tokens.append(Token('EOF', None, self.baris))
        return self.tokens

    def tampilake_token(self):
        """Nampilake kabeh token kanthi rapi ing layar."""
        print("\n[ ASIL LEXER — DAFTAR TOKEN ]")
        print(f"  {'NO':<5} {'TIPE':<15} {'NILAI':<20} {'BARIS'}")
        print("  " + "-" * 50)
        for i, tok in enumerate(self.tokens):
            if tok.tipe != 'EOF':
                print(f"  {i+1:<5} {tok.tipe:<15} {str(tok.nilai):<20} {tok.baris}")
        print(f"\n  Cacah token: {len(self.tokens) - 1}")


if __name__ == '__main__':
    # Kode uji kanggo nyoba lexer
    kode_uji = """
wahana x = 10
wahana y = 20
yen (x < y) {
    cetak("x luwih cilik")
}
"""
    print("=== UJI LEXER BASA JAWA ===")
    print("Kode sumber:")
    print(kode_uji)

    lx = Lexer(kode_uji)
    lx.tokenize()
    lx.tampilake_token()
