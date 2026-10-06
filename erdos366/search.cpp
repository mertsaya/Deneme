// Erdős Problemi #366 araması.
// X'e kadar her 3-dolu m için m-1 ve m+1'in 2-dolu (güçlü) olup olmadığını test eder.
//   m-1 güçlü  -> n = m-1 2-dolu, n+1 = m 3-dolu   (#366'nın aradığı yön)
//   m+1 güçlü  -> n = m 3-dolu, n+1 2-dolu          (ters yön: (8,9), (12167,12168))
// Bulunan her aday yazdırılır; son sınıflandırma verify.py ile tam çarpanlara ayırarak yapılır.
//
// 3-dolu sayılar tek biçimde m = a^3 * b^4 * c^5 (b, c karesiz, gcd(b,c)=1) yazılır.
// Güçlülük testi: B^5 > X+1 olacak şekilde B'ye kadar asallarla bölünür; geriye kalan r'nin
// tüm asal çarpanları > B'dir, dolayısıyla r güçlüyse r = 1, tam kare ya da tam küp olmalıdır.
//
// Derleme: g++ -O3 -march=native -fopenmp search.cpp -o search
// Kullanım: ./search <X> [ayrıntı]   (X ondalık ya da 1e24 biçiminde, X < 2^126)
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <cmath>
#include <vector>
#include <string>
#include <chrono>
#include <omp.h>
typedef unsigned __int128 u128;
typedef unsigned long long u64;

static std::string s128(u128 x) {
    if (x == 0) return "0";
    std::string s;
    while (x) { s += char('0' + (int)(x % 10)); x /= 10; }
    return std::string(s.rbegin(), s.rend());
}
static u128 parse(const char* s) {
    const char* e = strchr(s, 'e');
    if (e) {
        u128 m = 0; for (const char* p = s; p < e; p++) m = m * 10 + (*p - '0');
        int k = atoi(e + 1); while (k--) m *= 10; return m;
    }
    u128 m = 0; for (const char* p = s; *p; p++) m = m * 10 + (*p - '0'); return m;
}
static u128 isqrt(u128 n) {
    u128 r = (u128)sqrtl((long double)n);
    while (r * r > n) r--;
    while ((r + 1) * (r + 1) <= n) r++;
    return r;
}
static u128 icbrt(u128 n) {
    u128 r = (u128)cbrtl((long double)n);
    while (r > 0 && r * r * r > n) r--;
    while ((r + 1) * (r + 1) * (r + 1) <= n) r++;
    return r;
}
static u128 iroot(u128 n, int k) {  // floor(n^(1/k))
    u128 r = (u128)powl((long double)n, 1.0L / k);
    auto pw = [&](u128 x) { u128 y = 1; for (int i = 0; i < k; i++) { if (x && y > ((u128)-1) / x) return (u128)-1; y *= x; } return y; };
    while (r > 0 && pw(r) > n) r--;
    while (pw(r + 1) <= n) r++;
    return r;
}

struct P { u128 inv, lim; u64 p; u64 p2; };
static std::vector<P> PR;  // tek asallar

static inline bool divides(const P& q, u128 n) { return n * q.inv <= q.lim; }
static inline u128 divexact(const P& q, u128 n) { return n * q.inv; }

// n güçlü mü (n >= 1)?
static bool powerful(u128 n) {
    if (n == 0) return false;
    int tz = 0; while (!(n & 1)) { n >>= 1; tz++; }
    if (tz == 1) return false;
    for (const P& q : PR) {
        if ((u128)q.p2 > n) return n == 1;  // kalan 1 ya da asal
        if (divides(q, n)) {
            n = divexact(q, n);
            if (!divides(q, n)) return false;
            do n = divexact(q, n); while (divides(q, n));
        }
    }
    if (n == 1) return true;
    u128 s = isqrt(n); if (s * s == n) return true;
    u128 c = icbrt(n); if (c * c * c == n) return true;
    return false;
}

static bool squarefree(u64 x) {
    for (u64 p = 2; p * p <= x; p++) if (x % (p * p) == 0) return false;
    return true;
}
static u64 gcd(u64 a, u64 b) { while (b) { u64 t = a % b; a = b; b = t; } return a; }

struct Task { u128 K; u64 alo, ahi; };

int main(int argc, char** argv) {
    if (argc < 2) { fprintf(stderr, "kullanim: %s X\n", argv[0]); return 1; }
    u128 X = parse(argv[1]);
    u64 B = (u64)iroot(X + 1, 5) + 2;
    // B'ye kadar asallar
    std::vector<char> comp(B + 1, 0);
    for (u64 i = 2; i <= B; i++) if (!comp[i]) {
        for (u64 j = i * i; j <= B; j += i) comp[j] = 1;
        if (i == 2) continue;
        u128 inv = i;  // Newton ile 2^128 modunda ters
        for (int k = 0; k < 7; k++) inv *= 2 - (u128)i * inv;
        PR.push_back({inv, ((u128)-1) / i, i, i * i});
    }
    if (argc > 2 && !strcmp(argv[2], "test")) {  // stdin'den sayi oku, guclu mu yaz
        char buf[64];
        while (scanf("%63s", buf) == 1) printf("%d\n", (int)powerful(parse(buf)));
        return 0;
    }
    // görevler: (K = b^4 c^5, a aralığı)
    std::vector<Task> tasks;
    const u64 CH = 1 << 20;
    u64 cmax = (u64)iroot(X, 5);
    for (u64 c = 1; c <= cmax; c++) {
        if (!squarefree(c)) continue;
        u128 c5 = (u128)c * c * c * c * c;
        u64 bmax = (u64)iroot(X / c5, 4);
        for (u64 b = 1; b <= bmax; b++) {
            if (!squarefree(b) || gcd(b, c) != 1) continue;
            u128 K = c5 * b * b * b * b;
            u64 amax = (u64)icbrt(X / K);
            for (u64 lo = 1; lo <= amax; lo += CH)
                tasks.push_back({K, lo, lo + CH - 1 < amax ? lo + CH - 1 : amax});
        }
    }
    fprintf(stderr, "X=%s B=%llu asal=%zu gorev=%zu\n", s128(X).c_str(), B, PR.size(), tasks.size());
    auto t0 = std::chrono::steady_clock::now();
    u64 total = 0;
    #pragma omp parallel for schedule(dynamic, 1) reduction(+:total)
    for (size_t t = 0; t < tasks.size(); t++) {
        const Task& T = tasks[t];
        for (u64 a = T.alo; a <= T.ahi; a++) {
            u128 m = (u128)a * a * a * T.K;
            total++;
            bool lo = m > 1 && powerful(m - 1);
            bool hi = powerful(m + 1);
            if (lo || hi) {
                #pragma omp critical
                printf("%s %s%s\n", s128(m).c_str(), lo ? "-" : "", hi ? "+" : "");
            }
        }
    }
    double dt = std::chrono::duration<double>(std::chrono::steady_clock::now() - t0).count();
    fprintf(stderr, "3-dolu sayi=%llu sure=%.2fs\n", total, dt);
}
