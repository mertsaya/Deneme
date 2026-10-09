#!/usr/bin/env python3
"""search/sieve çıktısını sympy ile tam çarpanlara ayırarak doğrular ve sınıflandırır.

Kullanım: python3 verify.py out_1e24.txt [...]
Her satır: "<m> <işaretler>"; m 3-dolu, '-' ise m-1 güçlü, '+' ise m+1 güçlü.
"""
import sys
from sympy import factorint


def kfull(n, k):
    return n >= 1 and all(e >= k for e in factorint(n).values())


def fmt(n):
    return " * ".join(f"{p}^{e}" if e > 1 else str(p) for p, e in sorted(factorint(n).items()))


for path in sys.argv[1:]:
    for line in open(path):
        m_str, flags = (line.split() + [""])[:2]
        m = int(m_str)
        assert kfull(m, 3), f"{m} 3-dolu değil"
        for sgn, ch in ((-1, "-"), (1, "+")):
            assert (ch in flags) == (m + sgn >= 1 and kfull(m + sgn, 2)), f"{m}{ch} hatalı"
        if "-" in flags:
            print(f"#366 ÇÖZÜMÜ: n={m-1} = {fmt(m-1)} (2-dolu), n+1={m} = {fmt(m)} (3-dolu)")
        if "+" in flags:
            kind = "ARDIŞIK İKİ 3-DOLU!" if kfull(m + 1, 3) else "ters yön"
            print(f"{kind}: n={m} = {fmt(m)}, n+1={m+1} = {fmt(m+1)}")
