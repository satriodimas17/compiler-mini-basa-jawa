// lexer_node.js
// ============================================================
// LEXER — COMPILER MINI BASA JAWA
// Mecah kode sumber dadi 7 jinis token nganggo Node.js
// ============================================================

// ── 7 JINIS TOKEN ────────────────────────────────────────────
// 1. NUMBER     → angka bulat lan desimal   (tuladha: 42, 3)
// 2. STRING     → teks kang diapit petik    (tuladha: "halo")
// 3. KEYWORD    → tembung kunci Basa Jawa   (tuladha: yen, cetak)
// 4. IDENTIFIER → jeneng variabel / fungsi  (tuladha: x, asil)
// 5. OPERATOR   → tandha operasi aritmetika (tuladha: +, -, *, /)
// 6. COMPARATOR → tandha bandingan          (tuladha: ==, !=, <, >)
// 7. DELIMITER  → tandha kurung lan koma    (tuladha: ( ) { } , ;)

// Daftar tembung kunci Basa Jawa
const KEYWORDS = [
    'yen',       // yen   → if (kondisi)
    'menawa',    // menawa → else (kondisi liyane)
    'selawase',  // selawase → while (perulangan)
    'baleni',    // baleni → for (perulangan cacah)
    'bali',      // bali  → return (ngasilake nilai)
    'cetak',     // cetak → print (tampilake menyang layar)
    'lebokno',   // lebokno → input (jaluk data saka pangguna)
    'wahana',    // wahana → var (wadhah variabel)
    'gawea',     // gawea → function (gawe fungsi anyar)
    'bener',     // bener → true (nilai bener)
    'salah',     // salah → false (nilai salah)
    'kosong',    // kosong → null (ora ana nilai)
];

// Pola token — COMPARATOR kudu sadurunge OPERATOR
// supaya '==' ora kepotong dadi '=' + '='
const POLA = [
    { type: 'NUMBER',     regex: /^\d+(\.\d+)?/          }, // angka bulat utawa desimal
    { type: 'STRING',     regex: /^"[^"]*"/               }, // teks diapit tandha petik
    { type: 'COMPARATOR', regex: /^(==|!=|<=|>=|<|>)/    }, // tandha bandingan
    { type: 'OPERATOR',   regex: /^[+\-*/=]/              }, // tandha operasi
    { type: 'DELIMITER',  regex: /^[(){},;]/              }, // tandha kurung lan koma
    { type: 'IDENTIFIER', regex: /^[a-zA-Z_][a-zA-Z0-9_]*/ }, // jeneng variabel
];

// ── FUNGSI LEXER ─────────────────────────────────────────────
function lexer(code) {
    /**
     * Mecah kode sumber dadi daftar token.
     * Ngasilake array objek { tipe, nilai, baris }
     */
    let result = [];
    let pos    = 0;
    let baris  = 1;

    while (pos < code.length) {

        // Dilangkahi — spasi lan tab
        if (code[pos] === ' ' || code[pos] === '\t') {
            pos++;
            continue;
        }

        // Itung ganti baris
        if (code[pos] === '\n') {
            baris++;
            pos++;
            continue;
        }

        // Dilangkahi — komentar diawali //
        if (code.slice(pos, pos + 2) === '//') {
            while (pos < code.length && code[pos] !== '\n') pos++;
            continue;
        }

        let matchFound = false;

        for (let pola of POLA) {
            let substring = code.slice(pos);
            let match = substring.match(pola.regex);

            if (match) {
                let nilai = match[0];
                let tipe  = pola.type;

                // Priksa yen IDENTIFIER iku KEYWORD
                if (tipe === 'IDENTIFIER' && KEYWORDS.includes(nilai)) {
                    tipe = 'KEYWORD';
                }

                result.push({ tipe, nilai, baris });
                pos += nilai.length;
                matchFound = true;
                break;
            }
        }

        // Penanganan kesalahan — karakter ora dikenal
        if (!matchFound) {
            console.log(`[KESALAHAN LEXER] Karakter ilegal '${code[pos]}' ing baris ${baris}`);
            pos++;
        }
    }

    return result;
}

// ── TAMPILAKE ASIL TOKEN ─────────────────────────────────────
function tampilakeToken(tokens) {
    /**
     * Nampilake daftar token kanthi rapi ing layar.
     */
    console.log('\n[ ASIL LEXER — DAFTAR TOKEN ]');
    console.log('  NO   TIPE           NILAI                BARIS');
    console.log('  ' + '-'.repeat(55));
    tokens.forEach((tok, i) => {
        const no    = String(i + 1).padEnd(5);
        const tipe  = tok.tipe.padEnd(15);
        const nilai = String(tok.nilai).padEnd(20);
        console.log(`  ${no} ${tipe} ${nilai} ${tok.baris}`);
    });
    console.log(`\n  Cacah token: ${tokens.length}`);

    // Ringkasan saben jinis token
    console.log('\n[ RINGKASAN TOKEN ]');
    const cacah = {};
    tokens.forEach(t => {
        cacah[t.tipe] = (cacah[t.tipe] || 0) + 1;
    });
    Object.entries(cacah).forEach(([tipe, n]) => {
        console.log(`  ${tipe.padEnd(15)} : ${n} token`);
    });
}

// ── INPUT SAKA PANGGUNA ──────────────────────────────────────
const readline = require('readline').createInterface({
    input: process.stdin,
    output: process.stdout
});

console.log('============================================');
console.log('  LEXER — COMPILER MINI BASA JAWA');
console.log('============================================');
console.log('Tuladha: wahana x = 10 + 5');
console.log('         yen (x > 3) { cetak("gedhe") }');
console.log();

readline.question('Tulis ekspresi: ', function(input) {
    try {
        const asil = lexer(input);
        tampilakeToken(asil);
    } catch (e) {
        console.log(`[KESALAHAN] ${e.message}`);
    }
    readline.close();
});
