# optimizer.py
# ============================================================
# CODE OPTIMIZER — COMPILER MINI BASA JAWA
# Ngoptimalake AST supaya kode luwih cepet lan efisien
# Teknik kang digunakake:
#   1. Constant Folding      → 2+3 langsung dadi 5
#   2. Constant Propagation  → variabel konstan diganti nilaine
#   3. Dead Code Removal     → kode kang ora keeksekusi dibuang
# ============================================================

from ast_node import (
    BinOpNode, AngkaNode, StringNode, BoolNode,
    DeklarasiNode, AssignNode, ProgramNode,
    CetakNode, YenNode, SelawaseNode, BaliNode,
    GaweaNode, LeboknoNode, KondisiNode, VarNode
)

class Optimizer:
    """Kelas kanggo ngoptimalake AST sadurunge code generation."""

    def __init__(self):
        self.konstanta      = {}  # { jeneng_var: simpul_nilai } kanggo constant propagation
        self.cacah_optimasi = 0   # cacah optimasi kang diterapake

    # ── Titik Mlebu ─────────────────────────────────────────

    def optimasi(self, program_node):
        """Optimasi kabeh AST, ngasilake AST anyar kang luwih ringkes."""
        print("\n[ CODE OPTIMIZER ]")
        stmt_dioptimasi = []
        for stmt in program_node.statements:
            hasil = self.optimasi_statement(stmt)
            if hasil is not None:
                stmt_dioptimasi.append(hasil)

        print(f"  Total optimasi diterapake : {self.cacah_optimasi}")
        return ProgramNode(stmt_dioptimasi)

    # ── Optimasi Statement ──────────────────────────────────

    def optimasi_statement(self, node):
        """Milih cara optimasi adhedhasar jinis simpul."""
        if isinstance(node, DeklarasiNode):
            return self.optimasi_deklarasi(node)
        elif isinstance(node, AssignNode):
            return self.optimasi_assign(node)
        elif isinstance(node, CetakNode):
            return CetakNode(self.optimasi_ekspresi(node.ekspresi))
        elif isinstance(node, YenNode):
            return self.optimasi_yen(node)
        elif isinstance(node, SelawaseNode):
            return self.optimasi_selawase(node)
        elif isinstance(node, GaweaNode):
            blok_anyar = [self.optimasi_statement(s) for s in node.blok]
            return GaweaNode(node.nama, node.params, blok_anyar)
        elif isinstance(node, BaliNode):
            return BaliNode(self.optimasi_ekspresi(node.ekspresi))
        return node

    # ── Optimasi Deklarasi ──────────────────────────────────

    def optimasi_deklarasi(self, node):
        """Optimasi nilai awal variabel. Simpen yen konstan."""
        ekspresi_anyar = self.optimasi_ekspresi(node.ekspresi)
        # Constant propagation: simpen yen nilaine wis mesthi
        if isinstance(ekspresi_anyar, (AngkaNode, StringNode, BoolNode)):
            self.konstanta[node.nama] = ekspresi_anyar
        return DeklarasiNode(node.nama, ekspresi_anyar)

    # ── Optimasi Assignment ─────────────────────────────────

    def optimasi_assign(self, node):
        """Optimasi nilai assignment. Ngowahi nilai konstan ing tabel."""
        ekspresi_anyar = self.optimasi_ekspresi(node.ekspresi)
        if isinstance(ekspresi_anyar, (AngkaNode, StringNode, BoolNode)):
            self.konstanta[node.nama] = ekspresi_anyar
        return AssignNode(node.nama, ekspresi_anyar)

    # ── Optimasi Yen — Dead Code Removal ────────────────────

    def optimasi_yen(self, node):
        """
        Optimasi blok yen/menawa.
        Yen kondisi wis mesthi bener/salah, blok kang ora perlu dibuang.
        """
        kondisi_anyar = self.optimasi_kondisi(node.kondisi)

        # Dead code removal: kondisi wis mesthi bener
        if isinstance(kondisi_anyar, BoolNode) and kondisi_anyar.nilai:
            self.cacah_optimasi += 1
            print("  ✓ Dead code removal: blok 'menawa' dibuang (kondisi tansah bener)")
            blok = [self.optimasi_statement(s) for s in node.blok_bener]
            return ProgramNode(blok)

        # Dead code removal: kondisi wis mesthi salah
        if isinstance(kondisi_anyar, BoolNode) and not kondisi_anyar.nilai:
            self.cacah_optimasi += 1
            print("  ✓ Dead code removal: blok 'yen' dibuang (kondisi tansah salah)")
            if node.blok_salah:
                blok = [self.optimasi_statement(s) for s in node.blok_salah]
                return ProgramNode(blok)
            return None

        blok_bener = [self.optimasi_statement(s) for s in node.blok_bener]
        blok_salah = None
        if node.blok_salah:
            blok_salah = [self.optimasi_statement(s) for s in node.blok_salah]
        return YenNode(kondisi_anyar, blok_bener, blok_salah)

    # ── Optimasi Selawase ───────────────────────────────────

    def optimasi_selawase(self, node):
        """
        Optimasi perulangan selawase.
        Yen kondisi wis mesthi salah, perulangan dibuang.
        """
        kondisi_anyar = self.optimasi_kondisi(node.kondisi)

        # Dead code removal: selawase(salah) langsung dibuang
        if isinstance(kondisi_anyar, BoolNode) and not kondisi_anyar.nilai:
            self.cacah_optimasi += 1
            print("  ✓ Dead code removal: blok 'selawase' dibuang (kondisi tansah salah)")
            return None

        blok_anyar = [self.optimasi_statement(s) for s in node.blok]
        return SelawaseNode(kondisi_anyar, blok_anyar)

    # ── Optimasi Kondisi ────────────────────────────────────

    def optimasi_kondisi(self, node):
        """Ngitung kondisi yen loro sisih wis mesthi nilaine."""
        if isinstance(node, KondisiNode):
            kiwa   = self.optimasi_ekspresi(node.kiwa)
            tengen = self.optimasi_ekspresi(node.tengen)

            # Constant folding kondisi: loro-lorone wis angka
            if isinstance(kiwa, AngkaNode) and isinstance(tengen, AngkaNode):
                hasil = self.evaluasi_kondisi(kiwa.nilai, node.operator, tengen.nilai)
                self.cacah_optimasi += 1
                print(f"  ✓ Constant folding kondisi: {kiwa.nilai} {node.operator} {tengen.nilai} = {hasil}")
                return BoolNode(hasil)
            return KondisiNode(kiwa, node.operator, tengen)
        return node

    def evaluasi_kondisi(self, kiwa, op, tengen):
        """Ngitung asil kondisi bandingan."""
        if op == '==': return kiwa == tengen
        if op == '!=': return kiwa != tengen
        if op == '<':  return kiwa < tengen
        if op == '>':  return kiwa > tengen
        if op == '<=': return kiwa <= tengen
        if op == '>=': return kiwa >= tengen
        return False

    # ── Optimasi Ekspresi ───────────────────────────────────

    def optimasi_ekspresi(self, node):
        """
        Ngoptimalake ekspresi kanthi:
        - Constant folding: operasi angka langsung dihitung
        - Constant propagation: variabel diganti karo nilaine
        """
        if isinstance(node, BinOpNode):
            kiwa   = self.optimasi_ekspresi(node.kiwa)
            tengen = self.optimasi_ekspresi(node.tengen)

            # Constant folding: loro angka langsung dihitung
            if isinstance(kiwa, AngkaNode) and isinstance(tengen, AngkaNode):
                hasil = self.hitung(kiwa.nilai, node.operator, tengen.nilai)
                self.cacah_optimasi += 1
                print(f"  ✓ Constant folding: {kiwa.nilai} {node.operator} {tengen.nilai} = {hasil}")
                return AngkaNode(hasil)

            # Constant folding ukara: loro teks langsung digabung
            if isinstance(kiwa, StringNode) and isinstance(tengen, StringNode) and node.operator == '+':
                hasil = kiwa.nilai + tengen.nilai
                self.cacah_optimasi += 1
                print(f"  ✓ Constant folding ukara: \"{kiwa.nilai}\" + \"{tengen.nilai}\"")
                return StringNode(hasil)

            return BinOpNode(kiwa, node.operator, tengen)

        # Constant propagation: ganti variabel karo nilaine
        if isinstance(node, VarNode):
            if node.nama in self.konstanta:
                self.cacah_optimasi += 1
                print(f"  ✓ Constant propagation: '{node.nama}' diganti karo {self.konstanta[node.nama].nilai}")
                return self.konstanta[node.nama]

        return node

    def hitung(self, kiwa, op, tengen):
        """Nindakake operasi aritmetika."""
        if op == '+': return kiwa + tengen
        if op == '-': return kiwa - tengen
        if op == '*': return kiwa * tengen
        if op == '/': return kiwa / tengen if tengen != 0 else 0
        return 0
