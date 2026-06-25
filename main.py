# main.py
# ============================================================
# COMPILER MINI BAHASA JAWA — PROGRAM UTAMA
# Nglakokake kabeh fase kompilasi:
#   1. Lexer         → mecah kode dadi token
#   2. Parser        → mbangun Parse Tree / AST
#   3. Semantic      → ngecek kebenaran logika
#   4. Optimizer     → ngoptimalake AST
#   5. Code Generator→ ngasilake kode Python
#   6. Eksekusi      → nglakokake kode asil
# ============================================================

from lexer          import Lexer
from parser         import Parser, tampilake_ast
from semantic       import AnalisaSemantik
from optimizer      import Optimizer
from code_generator import CodeGenerator
from desain_bahasa  import TabelSimbol

BANNER = """
╔══════════════════════════════════════════════════╗
║     COMPILER MINI — BAHASA JAWA                  ║
║     Teknik Kompilasi                             ║
╚══════════════════════════════════════════════════╝

KEYWORD KANG BISA DIGUNAKAKE:
  wahana   → deklarasi variabel    (wahana x = 10)
  cetak    → tampilake output      (cetak("Halo"))
  lebokno  → nampa input pangguna  (x = lebokno("Aranmu: "))
  yen      → kondisi if            (yen (x > 5) { ... })
  menawa   → kondisi else          (menawa { ... })
  selawase → perulangan while      (selawase (x < 10) { ... })
  gawea    → deklarasi fungsi      (gawea tambah(a, b) { ... })
  bali     → return nilai          (bali x + 1)
  bener    → nilai true
  salah    → nilai false
"""

def jalanake_compiler(kode_sumber, mode_debug=False):
    """Nglakokake kabeh fase kompilasi."""

    print("=" * 52)
    print("  KODE SUMBER BAHASA JAWA:")
    print("=" * 52)
    for i, baris in enumerate(kode_sumber.strip().split('\n'), 1):
        print(f"  {i:>3} | {baris}")

    tabel_simbol = TabelSimbol()

    # ─── FASE 1: LEXER ────────────────────────────────────────
    print("\n" + "=" * 52)
    print("  FASE 1 — LEXER")
    print("=" * 52)
    lx = Lexer(kode_sumber)
    tokens = lx.tokenize()
    lx.tampilake_token()

    # ─── FASE 2: PARSER ───────────────────────────────────────
    print("\n" + "=" * 52)
    print("  FASE 2 — PARSER (AST)")
    print("=" * 52)
    ps = Parser(tokens)
    ast = ps.parse()
    print("\n[ STRUKTUR AST ]")
    tampilake_ast(ast)

    # ─── FASE 3: SEMANTIC ANALISIS ────────────────────────────
    print("\n" + "=" * 52)
    print("  FASE 3 — SEMANTIC ANALISIS")
    print("=" * 52)
    sem = AnalisaSemantik()
    sem.analisa(ast)
    tabel_simbol.tampilake()

    # ─── FASE 4: CODE OPTIMIZER ───────────────────────────────
    print("\n" + "=" * 52)
    print("  FASE 4 — CODE OPTIMIZER")
    print("=" * 52)
    opt = Optimizer()
    ast_dioptimasi = opt.optimasi(ast)

    # ─── FASE 5: CODE GENERATOR ───────────────────────────────
    print("\n" + "=" * 52)
    print("  FASE 5 — CODE GENERATOR")
    print("=" * 52)
    gen = CodeGenerator()
    kode_python = gen.generate(ast_dioptimasi)
    print("\n[ KODE PYTHON SING DIASILAKE ]")
    print("-" * 40)
    print(kode_python)
    print("-" * 40)

    # Simpen kode asil
    with open("output.py", "w") as f:
        f.write(kode_python)
    print("\n  ✓ Kode kasimpen ing 'output.py'")

    # ─── FASE 6: EKSEKUSI ─────────────────────────────────────
    print("\n" + "=" * 52)
    print("  FASE 6 — EKSEKUSI KODE")
    print("=" * 52)
    print()
    exec(kode_python, {})

    print("\n" + "=" * 52)
    print("  ✓ KOMPILASI RAMPUNG!")
    print("=" * 52)


# ── Contoh Program Bahasa Jawa ───────────────────────────────

CONTOH_1 = """
wahana jeneng = "Budi"
wahana umur = 17
cetak("Sugeng rawuh ing Compiler Bahasa Jawa!")
cetak(jeneng)
cetak(umur)
"""

CONTOH_2 = """
wahana x = 10
wahana y = 3
wahana asil = x + y
cetak(asil)
yen (x > y) {
    cetak("x luwih gedhe tinimbang y")
}
menawa {
    cetak("y luwih gedhe tinimbang x")
}
"""

CONTOH_3 = """
wahana n = 1
selawase (n < 5) {
    cetak(n)
    n = n + 1
}
"""

CONTOH_4 = """
gawea tambah(a, b) {
    bali a + b
}
wahana asil = 5 + 3
cetak(asil)
"""

# ── Program Utama ────────────────────────────────────────────

if __name__ == '__main__':
    print(BANNER)
    print("Pilih contoh program:")
    print("  1. Contoh 1 — Variabel lan Cetak")
    print("  2. Contoh 2 — Kondisi Yen/Menawa")
    print("  3. Contoh 3 — Perulangan Selawase")
    print("  4. Contoh 4 — Fungsi Gawea")
    print("  5. Tulis kode dhewe")
    print()

    pilihan = input("Pilihan (1-5): ").strip()

    if pilihan == '1':
        kode = CONTOH_1
    elif pilihan == '2':
        kode = CONTOH_2
    elif pilihan == '3':
        kode = CONTOH_3
    elif pilihan == '4':
        kode = CONTOH_4
    elif pilihan == '5':
        print("\nTulis kode Bahasa Jawa (ketik 'RAMPUNG' ing baris anyar kanggo mungkasi):")
        baris_kode = []
        while True:
            baris = input()
            if baris.strip() == 'RAMPUNG':
                break
            baris_kode.append(baris)
        kode = "\n".join(baris_kode)
    else:
        print("Pilihan ora valid, nganggo Contoh 2.")
        kode = CONTOH_2

    try:
        jalanake_compiler(kode)
    except (SyntaxError, RuntimeError, NameError) as e:
        print(f"\n✗ KOMPILASI GAGAL: {e}")
