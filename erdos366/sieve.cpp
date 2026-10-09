// Erdős Problemi #366: elek tabanlı hızlı arama (search.cpp ile aynı mantık, aynı çıktı biçimi).
// Sabit K = b^4 c^5 için m = a^3 K. Tek bir p asalı m-1'i (ya da m+1'i) böler <=> a^3 ≡ ±K^{-1} (mod p),
// yani a mod p, ±K^{-1}'in küp köklerinden biridir. Bu sınıflar elenir: p tam bir kez bölüyorsa aday ölür,
// aksi halde p'nin tüm kuvvetleri kalan değerden atılır. Elekten sağ çıkanların kalanı tam kare ya da
// tam küp mü diye bakılır (B^5 > X+1 olduğundan bu yeterli ve gerekli). Kısa a-aralıklarında deneme bölmesi.
//
// Derleme: g++ -O3 -march=native -fopenmp sieve.cpp -o sieve
// Kullanım: ./sieve <X> [count]     count: ara aşama sayaçlarını yazdırır (search ile karşılaştırma için)
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <cmath>
#include <vector>
#include <algorithm>
#include <string>
#include <chrono>
#include <omp.h>
typedef unsigned __int128 u128;
typedef unsigned long long u64;
typedef unsigned u32;

static std::string s128(u128 x) {
    if (x == 0) return "0";
    std::string s;
    while (x) { s += char('0' + (int)(x % 10)); x /= 10; }
    return std::string(s.rbegin(), s.rend());
}
static u128 parse(const char* s) {
    const char* e = strchr(s, 'e');
    u128 m = 0;
    for (const char* p = s; *p && p != e; p++) m = m * 10 + (*p - '0');
    if (e) for (int k = atoi(e + 1); k--;) m *= 10;
    return m;
}
static u128 iroot(u128 n, int k) {  // floor(n^(1/k))
    u128 r = (u128)powl((long double)n, 1.0L / k);
    auto pw = [&](u128 x) { u128 y = 1; for (int i = 0; i < k; i++) { if (x && y > ((u128)-1) / x) return (u128)-1; y *= x; } return y; };
    while (r > 0 && pw(r) > n) r--;
    while (pw(r + 1) <= n) r++;
    return r;
}
static bool sq_or_cube(u128 n) {
    u128 s = iroot(n, 2); if (s * s == n) return true;
    u128 c = iroot(n, 3); return c * c * c == n;
}

static u64 mulm(u64 a, u64 b, u64 p) { return a * b % p; }  // p < 2^32
static u64 powm(u64 a, u64 e, u64 p) { u64 r = 1; a %= p; while (e) { if (e & 1) r = mulm(r, a, p); a = mulm(a, a, p); e >>= 1; } return r; }

struct P {
    u128 inv, lim; u64 p, p2;
    // küp kökü için önhesaplar (p ≡ 1 mod 3)
    int s; u64 t, inv3, c, w;
};
static std::vector<P> PR;  // tek asallar <= B

// x'in mod p küp kökleri (x != 0). Sayısını döndürür.
static int cbrts(const P& q, u64 x, u64* out) {
    u64 p = q.p;
    if (p == 3) { out[0] = x % 3; return 1; }
    if (p % 3 == 2) { out[0] = powm(x, (2 * p - 1) / 3, p); return 1; }
    if (powm(x, (p - 1) / 3, p) != 1) return 0;
    // Adleman–Manders–Miller: p-1 = 3^s t, r0 = x^{inv3}, r0^3 = x*h, h 3-Sylow'da
    u64 r0 = powm(x, q.inv3, p);
    u64 h = mulm(mulm(r0, mulm(r0, r0, p), p), powm(x, p - 2, p), p);  // r0^3 / x
    u64 hi = powm(h, p - 2, p);                                         // y^3 = h^{-1} = c^e
    u64 e = 0, pw3 = 1, ci = powm(q.c, p - 2, p);
    for (int i = 0; i < q.s; i++) {
        u64 cur = mulm(hi, powm(ci, e, p), p);
        u64 v = cur; for (int j = 0; j < q.s - 1 - i; j++) v = powm(v, 3, p);
        int d = (v == 1) ? 0 : (v == q.w ? 1 : 2);
        e += d * pw3; pw3 *= 3;
    }
    u64 r = mulm(r0, powm(q.c, e / 3, p), p);
    out[0] = r; out[1] = mulm(r, q.w, p); out[2] = mulm(out[1], q.w, p);
    return 3;
}

static inline bool divides(const P& q, u128 n) { return n * q.inv <= q.lim; }

// 0: B'ye kadar bir asal tam bir kez bölüyor; 1: hayır ama kalan kare/küp değil; 2: güçlü
static int classify_trial(u128 n, u64 B) {
    int tz = 0; while (!(n & 1)) { n >>= 1; tz++; }
    if (tz == 1) return 0;
    for (const P& q : PR) {
        if ((u128)q.p2 > n) return n == 1 ? 2 : (n <= B ? 0 : 1);
        if (divides(q, n)) {
            n *= q.inv;
            if (!divides(q, n)) return 0;
            do n *= q.inv; while (divides(q, n));
        }
    }
    return (n == 1 || sq_or_cube(n)) ? 2 : 1;
}
static int classify_rest(u128 n) {  // tek asallar elendikten sonra: 2 ve kalan
    int tz = 0; while (!(n & 1)) { n >>= 1; tz++; }
    if (tz == 1) return 0;
    return (n == 1 || sq_or_cube(n)) ? 2 : 1;
}

static bool squarefree(u64 x) { for (u64 p = 2; p * p <= x; p++) if (x % (p * p) == 0) return false; return true; }
static u64 gcd(u64 a, u64 b) { while (b) { u64 t = a % b; a = b; b = t; } return a; }

struct Task { u128 K; u64 alo, ahi; };
static const u64 CH = 1 << 22, BL = 1 << 15;
static u64 LMIN = 1500;  // bu uzunluktan kısa a-aralıklarında deneme bölmesi

int main(int argc, char** argv) {
    if (argc < 2) { fprintf(stderr, "kullanim: %s X [count]\n", argv[0]); return 1; }
    u128 X = parse(argv[1]);
    bool cnt = argc > 2 && !strcmp(argv[2], "count");
    if (getenv("LMIN")) LMIN = strtoull(getenv("LMIN"), 0, 10);
    u64 B = (u64)iroot(X + 1, 5) + 2;
    std::vector<char> comp(B + 1, 0);
    for (u64 i = 2; i <= B; i++) if (!comp[i]) {
        for (u64 j = i * i; j <= B; j += i) comp[j] = 1;
        if (i == 2) continue;
        u128 inv = i; for (int k = 0; k < 7; k++) inv *= 2 - (u128)i * inv;
        P q{inv, ((u128)-1) / i, i, i * i, 0, 0, 0, 0, 0};
        if (i % 3 == 1) {
            u64 t = i - 1; int s = 0; while (t % 3 == 0) { t /= 3; s++; }
            q.s = s; q.t = t;
            for (u64 k = 1; k < t; k++) if ((3 * k) % t == 1) { q.inv3 = k; break; }  // t çift, >= 2
            u64 z = 2; while (powm(z, (i - 1) / 3, i) == 1) z++;   // kübik kalan olmayan
            q.c = powm(z, t, i);                                    // 3-Sylow üreteci (mertebe 3^s)
            u64 w = q.c; for (int j = 0; j < s - 1; j++) w = powm(w, 3, i);
            q.w = w;                                                // ilkel küp birim kökü
        }
        PR.push_back(q);
    }
    if (argc > 2 && !strcmp(argv[2], "cbrttest")) {  // küp köklerini kaba kuvvetle doğrula
        long bad = 0, tot = 0;
        for (const P& q : PR) for (u64 x = 1; x < q.p; x++) {
            u64 r[3]; int k = cbrts(q, x, r), b = 0;
            for (u64 a = 0; a < q.p; a++) b += a * a % q.p * a % q.p == x;
            for (int j = 0; j < k; j++) if (r[j] * r[j] % q.p * r[j] % q.p != x) bad++;
            if (k != b || (k == 3 && (r[0] == r[1] || r[1] == r[2] || r[0] == r[2]))) bad++;
            tot++;
        }
        printf("cbrt test: %ld durum, %ld hata\n", tot, bad); return 0;
    }
    std::vector<u64> two64;  // 2^64 mod p
    for (const P& q : PR) two64.push_back((u64)((((u128)1) << 64) % q.p));
    std::vector<Task> tasks;
    u64 cmax = (u64)iroot(X, 5);
    for (u64 c = 1; c <= cmax; c++) {
        if (!squarefree(c)) continue;
        u128 c5 = (u128)c * c * c * c * c;
        u64 bmax = (u64)iroot(X / c5, 4);
        for (u64 b = 1; b <= bmax; b++) {
            if (!squarefree(b) || gcd(b, c) != 1) continue;
            u128 K = c5 * b * b * b * b;
            u64 amax = (u64)iroot(X / K, 3);
            for (u64 lo = 1; lo <= amax; lo += CH)
                tasks.push_back({K, lo, lo + CH - 1 < amax ? lo + CH - 1 : amax});
        }
    }
    // büyük görevler önce (yük dengesi)
    std::stable_sort(tasks.begin(), tasks.end(), [](const Task& x, const Task& y) { return x.ahi - x.alo > y.ahi - y.alo; });
    fprintf(stderr, "X=%s B=%llu asal=%zu gorev=%zu\n", s128(X).c_str(), B, PR.size(), tasks.size());
    auto t0 = std::chrono::steady_clock::now();
    u64 total = 0, st[2][3] = {{0}};
    #pragma omp parallel reduction(+:total)
    {
        std::vector<u128> rem[2] = {std::vector<u128>(BL), std::vector<u128>(BL)};
        std::vector<char> dead[2] = {std::vector<char>(BL), std::vector<char>(BL)};
        std::vector<u64> nxt[2];  // her kök için sıradaki a (mutlak)
        std::vector<u32> pid[2];
        u64 lst[2][3] = {{0}};
        #pragma omp for schedule(dynamic, 1)
        for (size_t ti = 0; ti < tasks.size(); ti++) {
            const Task& T = tasks[ti];
            u64 L = T.ahi - T.alo + 1;
            total += L;
            auto report = [&](u128 m, int lo, int hi) {
                if (cnt) { lst[0][lo]++; lst[1][hi]++; }
                if (lo == 2 || hi == 2) {
                    #pragma omp critical
                    printf("%s %s%s\n", s128(m).c_str(), lo == 2 ? "-" : "", hi == 2 ? "+" : "");
                }
            };
            if (L < LMIN) {
                for (u64 a = T.alo; a <= T.ahi; a++) {
                    u128 m = (u128)a * a * a * T.K;
                    report(m, m > 1 ? classify_trial(m - 1, B) : 0, classify_trial(m + 1, B));
                }
                continue;
            }
            // kökler: a^3 ≡ sgn * K^{-1} (mod p); side 0: m-1 (sgn=+1), side 1: m+1 (sgn=-1)
            for (int sd = 0; sd < 2; sd++) { nxt[sd].clear(); pid[sd].clear(); }
            u64 Khi = (u64)(T.K >> 64), Klo = (u64)T.K;
            for (u32 i = 0; i < PR.size(); i++) {
                const P& q = PR[i];
                u64 Km = ((Khi % q.p) * two64[i] + Klo % q.p) % q.p;
                if (Km == 0) continue;
                u64 r[3];
                int k = cbrts(q, powm(Km, q.p - 2, q.p), r);  // -x'in kökleri = x'in köklerinin negatifi
                u64 am = T.alo % q.p;
                for (int j = 0; j < k; j++) {
                    nxt[0].push_back(T.alo + (r[j] + q.p - am) % q.p); pid[0].push_back(i);
                    nxt[1].push_back(T.alo + (2 * q.p - r[j] - am) % q.p); pid[1].push_back(i);
                }
            }
            for (u64 blo = T.alo; blo <= T.ahi; blo += BL) {
                u64 bhi = blo + BL - 1 < T.ahi ? blo + BL - 1 : T.ahi, n = bhi - blo + 1;
                for (u64 j = 0; j < n; j++) {
                    u64 a = blo + j; u128 m = (u128)a * a * a * T.K;
                    rem[0][j] = m - 1; rem[1][j] = m + 1; dead[0][j] = (m == 1); dead[1][j] = 0;  // m-1=0 elenmez
                }
                for (int sd = 0; sd < 2; sd++) {
                    u128* R = rem[sd].data(); char* D = dead[sd].data();
                    for (size_t k = 0; k < nxt[sd].size(); k++) {
                        const P& q = PR[pid[sd][k]];
                        u64 a = nxt[sd][k];
                        for (; a <= bhi; a += q.p) {
                            u64 j = a - blo;
                            if (D[j]) continue;
                            u128 v = R[j] * q.inv;
                            if (!divides(q, v)) { D[j] = 1; continue; }
                            do v *= q.inv; while (divides(q, v));
                            R[j] = v;
                        }
                        nxt[sd][k] = a;
                    }
                }
                for (u64 j = 0; j < n; j++) {
                    u64 a = blo + j; u128 m = (u128)a * a * a * T.K;
                    int lo = (m == 1 || dead[0][j]) ? 0 : classify_rest(rem[0][j]);
                    int hi = dead[1][j] ? 0 : classify_rest(rem[1][j]);
                    report(m, lo, hi);
                }
            }
        }
        #pragma omp critical
        for (int i = 0; i < 2; i++) for (int j = 0; j < 3; j++) st[i][j] += lst[i][j];
    }
    double dt = std::chrono::duration<double>(std::chrono::steady_clock::now() - t0).count();
    fprintf(stderr, "3-dolu sayi=%llu sure=%.2fs\n", total, dt);
    if (cnt) fprintf(stderr, "m-1: olu=%llu sag=%llu guclu=%llu | m+1: olu=%llu sag=%llu guclu=%llu\n",
                     st[0][0], st[0][1], st[0][2], st[1][0], st[1][1], st[1][2]);
}
