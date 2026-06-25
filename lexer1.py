# lexer1.py
# ============================================================
# LEXER — COMPILER MINI BASA JAWA
# Mecah kode sumber dadi 7 jinis token nganggo Python
# ============================================================

import re

# ── 7 JINIS TOKEN ────────────────────────────────────────────
# 1. NUMBER     → angka bulat lan desimal   (tuladha: 42, 3.14)
# 2. STRING     → teks kang diapit petik    (tuladha: "halo")
# 3. KEYWORD    → tembung kunci Basa Jawa   (tuladha: yen, cetak)
# 4. IDENTIFIER → jeneng variabel / fungsi  (tuladha: x, asil)
# 5. OPERATOR   → tandha operasi aritmetika (tuladha: +, -, *, /)
# 6. COMPARATOR → tandha bandingan          (tuladha: ==, !=, <, >)
# 7. DELIMITER  → tandha kurung lan koma    (tuladha: ( ) { } , ;)

# Daftar tembung kunci Basa Jawa
KEYWORDS = {
    'yen',       # yen   → if (kondisi)
    'menawa',    # menawa → else (kondisi liyane)
    'selawase',  # selawase → while (perulangan)
    'baleni',    # baleni → for (perulangan cacah)
    'bali',      # bali  → return (ngasilake nilai)
    'cetak',     # cetak → print (tampilake menyang layar)
    'lebokno',   # lebokno → input (jaluk data saka pangguna)
    'wahana',    # wahana → var (wadhah variabel)
    'gawea',     # gawea → function (gawe fungsi anyar)
    'bener',     # bener → true (nilai bener)
    'salah',     # salah → false (nilai salah)
    'kosong',    # kosong → null (ora ana nilai)
}

# Pola token — COMPARATOR kudu sadurunge OPERATOR
# supaya '==' ora kepotong dadi '=' + '='
POLA_TOKEN = [
    ('NUMBER',     r'\d+(\.\d+)?'),     # angka bulat utawa desimal
    ('STRING',     r'"[^"]*"'),          # teks diapit tandha petik
    ('COMPARATOR', r'==|!=|<=|>=|<|>'), # tandha bandingan
    ('OPERATOR',   r'[+\-*/=]'),         # tandha operasi
    ('DELIMITER',  r'[(){},;]'),         # tandha kurung lan koma
    ('IDENTIFIER', r'[a-zA-Z_][a-zA-Z0-9_]*'), # jeneng variabel
]

# ── FUNGSI LEXER ─────────────────────────────────────────────
def lexer(code):
    """Mecah kode sumber dadi daftar token."""
    result = []
    pos    = 0
    baris  = 1

    while pos < len(code):

        # Itung ganti baris
        if code[pos] == '\n':
            baris += 1
            pos += 1
            continue

        # Dilangkahi — spasi lan tab
        if code[pos] in (' ', '\t'):
            pos += 1
            continue

        # Dilangkahi — komentar diawali #
        if code[pos] == '#':
            while pos < len(code) and code[pos] != '\n':
                pos += 1
            continue

        match_found = False

        for token_name, pattern in POLA_TOKEN:
            regex = re.compile(pattern)
            match = regex.match(code, pos)

            if match:
                nilai = match.group()
                tipe  = token_name

                # Priksa yen IDENTIFIER iku KEYWORD
                if tipe == 'IDENTIFIER' and nilai in KEYWORDS:
                    tipe = 'KEYWORD'

                result.append((tipe, nilai, baris))
                pos = match.end()
                match_found = True
                break

        # Penanganan kesalahan — karakter ora dikenal
        if not match_found:
            print(f"[KESALAHAN LEXER] Karakter ilegal '{code[pos]}' ing baris {baris}")
            pos += 1

    return result

# ── TAMPILAKE ASIL TOKEN ─────────────────────────────────────
def tampilake_token(tokens):
    """Nampilake daftar token kanthi rapi ing layar."""
    print("\n[ ASIL LEXER — DAFTAR TOKEN ]")
    print(f"  {'NO':<5} {'TIPE':<15} {'NILAI':<20} {'BARIS'}")
    print("  " + "-" * 50)
    for i, (tipe, nilai, baris) in enumerate(tokens):
        print(f"  {i+1:<5} {tipe:<15} {nilai:<20} {baris}")
    print(f"\n  Cacah token: {len(tokens)}")

    # Ringkasan saben jinis token
    print("\n[ RINGKASAN TOKEN ]")
    cacah = {}
    for tipe, _, _ in tokens:
        cacah[tipe] = cacah.get(tipe, 0) + 1
    for tipe, n in cacah.items():
        print(f"  {tipe:<15} : {n} token")

# ── PROGRAM UTAMA ─────────────────────────────────────────────
if __name__ == '__main__':
    print("=" * 50)
    print("  LEXER — COMPILER MINI BASA JAWA")
    print("=" * 50)
    print("Tuladha: wahana x = 10 + 5")
    print("         yen (x > 3) { cetak(x) }")
    print()

    code = input("Tulis ekspresi: ")
    asil = lexer(code)
    tampilake_token(asil)
