// Son Durak: Plüton — B1 görsel dilimi: sprite çizim kütüphanesi (Canvas2D, bağımlılıksız).
// Tüm ölçüler DÜNYA BİRİMİ (B0 fiziğiyle aynı: roket r = 4, balon r = 12, zeplin r = 22 ...).
// Sprite uzayı: y AŞAĞI, ışık sol üstten. Üretici (uret.py → uretici.html) her sprite'ı D piksel/birim ile çizer,
// dış konturu (siluet) alfa genişletmeyle ekler ve atlasa dizer. İç çizgiler burada çizilir.
'use strict';

const INK = '#241f4d';                  // kontur: saf siyah değil, koyu çivit (yumuşak hat)
const ST = { kontur: true, golge: 'yumusak' };   // tarz: golge = yumusak | duz | parlak  (karşılaştırma için)
const IL = 0.42;                         // iç çizgi kalınlığı (birim)

// ---------------------------------------------------------------- renk
function rgb(h) { h = h.replace('#', ''); return [0, 2, 4].map(i => parseInt(h.slice(i, i + 2), 16)); }
function karis(a, b, t) { const x = rgb(a), y = rgb(b); return '#' + x.map((v, i) => Math.round(v + (y[i] - v) * t).toString(16).padStart(2, '0')).join(''); }
const ac = (h, t) => karis(h, '#ffffff', t);
const ko = (h, t) => karis(h, '#2a1d5c', t);        // gölge soğuk mora kayar (düz kararmaz)
const RENK = {
  kirmizi: '#ff3346', beyaz: '#f4f6fb', sari: '#ffcc22', turuncu: '#ff8a1f', mavi: '#2f8cff', mor: '#8f5bff',
  yesil: '#3fcf5a', turkuaz: '#22e0d0', metal: '#b9c4d8', koyuMetal: '#5b6580', ten: '#ffcfa6', sac: '#7a4526',
};

// ---------------------------------------------------------------- boyama yardımcıları
function dikey(c, renk, y0, y1) {
  const g = c.createLinearGradient(0, y0, 0, y1);
  if (ST.golge === 'duz') { g.addColorStop(0, renk); g.addColorStop(0.6, renk); g.addColorStop(0.6, ko(renk, 0.2)); g.addColorStop(1, ko(renk, 0.2)); }
  else if (ST.golge === 'parlak') { g.addColorStop(0, ac(renk, 0.6)); g.addColorStop(0.28, renk); g.addColorStop(1, ko(renk, 0.5)); }
  else { g.addColorStop(0, ac(renk, 0.35)); g.addColorStop(0.2, renk); g.addColorStop(0.5, renk); g.addColorStop(0.68, ko(renk, 0.18)); g.addColorStop(1, ko(renk, 0.3)); }
  return g;
}
function kure(c, renk, x, y, r) {
  const g = c.createRadialGradient(x - r * 0.35, y - r * 0.4, 0, x - r * 0.1, y - r * 0.1, r * 1.25);
  if (ST.golge === 'duz') { g.addColorStop(0, renk); g.addColorStop(0.72, renk); g.addColorStop(0.72, ko(renk, 0.2)); g.addColorStop(1, ko(renk, 0.2)); }
  else if (ST.golge === 'parlak') { g.addColorStop(0, ac(renk, 0.7)); g.addColorStop(0.3, renk); g.addColorStop(1, ko(renk, 0.55)); }
  else { g.addColorStop(0, ac(renk, 0.3)); g.addColorStop(0.25, renk); g.addColorStop(0.62, renk); g.addColorStop(0.82, ko(renk, 0.2)); g.addColorStop(1, ko(renk, 0.32)); }
  return g;
}
function cizgi(c, w, renk) {
  c.lineJoin = 'round'; c.lineCap = 'round';
  if (ST.kontur) { c.strokeStyle = INK; c.lineWidth = w ?? IL; c.stroke(); }
  else if (renk) { c.save(); c.globalAlpha = 0.5; c.strokeStyle = ko(renk, 0.45); c.lineWidth = (w ?? IL) * 0.6; c.stroke(); c.restore(); }
}
function parla(c, x, y, rx, ry, rot, a = 0.75) {
  c.save(); c.globalAlpha = ST.golge === 'duz' ? 0.95 : ST.golge === 'parlak' ? Math.min(1, a + 0.15) : a; c.fillStyle = '#fff';
  c.beginPath(); c.ellipse(x, y, ST.golge === 'duz' ? rx * 0.8 : rx, ry, rot, 0, 6.2832); c.fill(); c.restore();
}
function daire(c, x, y, r) { c.beginPath(); c.arc(x, y, r, 0, 6.2832); }
function elips(c, x, y, rx, ry, rot = 0) { c.beginPath(); c.ellipse(x, y, rx, ry, rot, 0, 6.2832); }
function poli(c, p) { c.beginPath(); c.moveTo(p[0], p[1]); for (let i = 2; i < p.length; i += 2) c.lineTo(p[i], p[i + 1]); c.closePath(); }
function dol(c, f) { c.fillStyle = f; c.fill(); }
function rastgele(s) { return () => { s = (s * 16807) % 2147483647; return (s - 1) / 2147483646; }; }

// ---------------------------------------------------------------- ROKET (burun +x; merkez = çarpışma merkezi)
function kanat(c, s, p, renk) {   // s = +1 alt, −1 üst
  const q = p.map((v, i) => (i % 2 ? v * s : v));
  poli(c, q); const ys = q.filter((_, i) => i % 2); dol(c, dikey(c, renk, Math.min(...ys), Math.max(...ys))); cizgi(c, IL, renk);
}
function govde(c, x0, x1, h, sis, renk) {
  c.beginPath(); c.moveTo(x0, -h); c.quadraticCurveTo((x0 + x1) / 2, -h - sis, x1, -h); c.lineTo(x1, h);
  c.quadraticCurveTo((x0 + x1) / 2, h + sis, x0, h); c.closePath(); if (renk) dol(c, dikey(c, renk, -h - sis, h + sis));
}
function roketUst(c) {
  // meme
  poli(c, [-5.4, -1.7, -6.9, -2.3, -6.9, 2.3, -5.4, 1.7]); dol(c, dikey(c, RENK.koyuMetal, -2.3, 2.3)); cizgi(c, IL, RENK.koyuMetal);
  // küçük kanatçıklar
  for (const s of [-1, 1]) kanat(c, s, [-1.6, 3.6, -5.9, 7.0, -6.9, 7.3, -6.6, 6.0, -5.6, 3.6], RENK.kirmizi);
  // gövde (beyaz)
  govde(c, -5.6, 4.6, 4.2, 0.35, RENK.beyaz); c.save(); c.clip();
  c.fillStyle = dikey(c, RENK.kirmizi, -4.6, 4.6); c.fillRect(-5.8, -5, 1.25, 10);          // arka kırmızı bant
  c.restore(); govde(c, -5.6, 4.6, 4.2, 0.35, null); cizgi(c, IL, RENK.beyaz);
  c.beginPath(); c.moveTo(-4.35, -4.4); c.lineTo(-4.35, 4.4); cizgi(c, IL * 0.7, RENK.kirmizi);
  // burun (kırmızı)
  c.beginPath(); c.moveTo(4.4, -4.2); c.bezierCurveTo(8.6, -4.1, 11.6, -2.2, 12.5, 0); c.bezierCurveTo(11.6, 2.2, 8.6, 4.1, 4.4, 4.2); c.closePath();
  dol(c, dikey(c, RENK.kirmizi, -4.2, 4.2)); cizgi(c, IL, RENK.kirmizi);
  parla(c, 7.4, -2.5, 2.2, 0.55, 0.28, 0.7);
  parla(c, -1.5, -3.3, 2.6, 0.45, 0, 0.8);
  // pencere çerçevesi ve camı (pilot ayrı sprite, cam parlaması ayrı sprite)
  daire(c, 0.3, -0.1, 3.3); dol(c, kure(c, RENK.metal, 0.3, -0.1, 3.3)); cizgi(c, IL, RENK.metal);
  daire(c, 0.3, -0.1, 2.6); const g = c.createRadialGradient(-0.4, -0.9, 0.2, 0.3, -0.1, 2.8);
  g.addColorStop(0, '#5f8fe0'); g.addColorStop(1, '#1b2c6b'); dol(c, g); cizgi(c, IL * 0.8, '#1b2c6b');
  c.fillStyle = ST.kontur ? INK : '#59627a';
  for (let i = 0; i < 8; i++) { const a = i * Math.PI / 4 + 0.39; daire(c, 0.3 + Math.cos(a) * 2.95, -0.1 + Math.sin(a) * 2.95, 0.17); c.fill(); }
}
function roketAlt(c) {
  poli(c, [-18.3, -2.2, -20.3, -3.1, -20.3, 3.1, -18.3, 2.2]); dol(c, dikey(c, RENK.koyuMetal, -3.1, 3.1)); cizgi(c, IL, RENK.koyuMetal);
  c.fillStyle = ko(RENK.koyuMetal, 0.4); c.fillRect(-20.5, -3.3, 0.6, 6.6);
  for (const s of [-1, 1]) kanat(c, s, [-11.2, 4.2, -17.0, 9.3, -18.9, 9.9, -18.9, 8.2, -18.1, 4.2], RENK.kirmizi);
  govde(c, -18.4, -5.0, 4.5, 0.3, RENK.beyaz); c.save(); c.clip();
  c.fillStyle = dikey(c, RENK.kirmizi, -4.8, 4.8); c.fillRect(-10.6, -5, 1.6, 10); c.fillRect(-8.3, -5, 0.6, 10);
  c.fillStyle = dikey(c, RENK.metal, -4.8, 4.8); c.fillRect(-6.1, -5, 1.2, 10);
  c.restore(); govde(c, -18.4, -5.0, 4.5, 0.3, null); cizgi(c, IL, RENK.beyaz);
  c.beginPath(); c.moveTo(-6.1, -4.7); c.lineTo(-6.1, 4.7); cizgi(c, IL * 0.7, RENK.metal);
  parla(c, -13, -3.5, 3.2, 0.45, 0, 0.8);
  // ortadaki kanat (yandan görünür, ince)
  c.beginPath(); c.roundRect(-18.9, -0.85, 7.2, 1.7, 0.85); dol(c, dikey(c, RENK.kirmizi, -0.85, 0.85)); cizgi(c, IL, RENK.kirmizi);
}
function camParlak(c) {
  c.save(); c.globalAlpha = 0.14; daire(c, 0.3, -0.1, 2.55); c.fillStyle = '#9fd0ff'; c.fill(); c.restore();
  c.save(); c.globalAlpha = 0.8; c.strokeStyle = '#fff'; c.lineCap = 'round'; c.lineWidth = 0.42;
  c.beginPath(); c.arc(0.3, -0.1, 2.05, Math.PI * 1.08, Math.PI * 1.42); c.stroke();
  daire(c, 1.75, 1.2, 0.22); c.fillStyle = '#fff'; c.fill(); c.restore();
}

// ---------------------------------------------------------------- PİLOT (maskot astronot) — yüz sağa (buruna) bakar
function pilotKafa(c, R, ifade, anten = true) {
  const k = (v) => v * R;
  if (anten) {
    c.beginPath(); c.moveTo(k(-0.25), k(-0.9)); c.quadraticCurveTo(k(-0.45), k(-1.15), k(-0.38), k(-1.32));
    c.strokeStyle = ST.kontur ? INK : RENK.koyuMetal; c.lineWidth = k(0.16); c.lineCap = 'round'; c.stroke();
    c.strokeStyle = RENK.metal; c.lineWidth = k(0.07); c.stroke();
    daire(c, k(-0.38), k(-1.36), k(0.15)); dol(c, kure(c, RENK.kirmizi, k(-0.38), k(-1.36), k(0.15))); cizgi(c, k(0.06), RENK.kirmizi);
  }
  daire(c, 0, 0, R); dol(c, kure(c, '#ffffff', 0, 0, R)); cizgi(c, k(0.075), RENK.beyaz);
  daire(c, k(-0.7), k(0.12), k(0.3)); dol(c, kure(c, '#dfe5ef', k(-0.7), k(0.12), k(0.3))); cizgi(c, k(0.06), RENK.metal);
  daire(c, k(-0.7), k(0.12), k(0.15)); dol(c, RENK.kirmizi);
  // vizör (açık; yüz görünür)
  const vx = k(0.2), vy = k(0.07), vrx = k(0.7), vry = k(0.68);
  elips(c, vx, vy, vrx, vry); dol(c, kure(c, RENK.ten, vx, vy, vrx)); c.save(); c.clip();
  // saç perçemi
  c.beginPath(); c.moveTo(k(-0.6), k(-0.7)); c.lineTo(k(1.0), k(-0.7)); c.lineTo(k(1.0), k(-0.38));
  c.quadraticCurveTo(k(0.75), k(-0.22), k(0.55), k(-0.4)); c.quadraticCurveTo(k(0.35), k(-0.2), k(0.12), k(-0.38));
  c.quadraticCurveTo(k(-0.15), k(-0.18), k(-0.6), k(-0.3)); c.closePath(); dol(c, dikey(c, RENK.sac, k(-0.7), k(-0.2)));
  // yanak
  c.globalAlpha = 0.45; c.fillStyle = '#ff7a8a'; elips(c, k(-0.08), k(0.3), k(0.13), k(0.08)); c.fill(); elips(c, k(0.66), k(0.3), k(0.11), k(0.08)); c.fill(); c.globalAlpha = 1;
  yuz(c, k, ifade);
  c.restore();
  elips(c, vx, vy, vrx, vry); cizgi(c, k(0.075), RENK.ten);
  c.save(); c.globalAlpha = 0.6; c.strokeStyle = '#fff'; c.lineWidth = k(0.07); c.lineCap = 'round';
  c.beginPath(); c.ellipse(vx, vy, vrx * 0.86, vry * 0.86, 0, Math.PI * 1.1, Math.PI * 1.4); c.stroke(); c.restore();
}
function goz(c, k, x, y, rx, ry, px, py, pr) {
  elips(c, k(x), k(y), k(rx), k(ry)); dol(c, '#fff'); cizgi(c, k(0.05));
  daire(c, k(x + px), k(y + py), k(pr)); dol(c, INK);
  daire(c, k(x + px - pr * 0.35), k(y + py - pr * 0.4), k(pr * 0.35)); dol(c, '#fff');
}
function kas(c, k, x0, y0, x1, y1, b = 0) { c.beginPath(); c.moveTo(k(x0), k(y0)); c.quadraticCurveTo(k((x0 + x1) / 2), k((y0 + y1) / 2 - b), k(x1), k(y1)); c.strokeStyle = INK; c.lineWidth = k(0.075); c.lineCap = 'round'; c.stroke(); }
function yuz(c, k, ifade) {
  const L = k(0.075);
  if (ifade === 'notr') {
    goz(c, k, 0.02, -0.02, 0.13, 0.18, 0.04, 0.02, 0.085); goz(c, k, 0.45, -0.02, 0.12, 0.17, 0.04, 0.02, 0.08);
    kas(c, k, -0.08, -0.27, 0.1, -0.29, 0.03); kas(c, k, 0.37, -0.29, 0.55, -0.27, 0.03);
    c.beginPath(); c.arc(k(0.27), k(0.2), k(0.14), 0.35, Math.PI - 0.5); c.strokeStyle = INK; c.lineWidth = L; c.stroke();
  } else if (ifade === 'heyecan') {
    for (const x of [0.02, 0.45]) { c.beginPath(); c.arc(k(x), k(0.04), k(0.12), Math.PI * 1.1, Math.PI * 1.9); c.strokeStyle = INK; c.lineWidth = k(0.09); c.lineCap = 'round'; c.stroke(); }
    kas(c, k, -0.1, -0.32, 0.1, -0.36, 0.04); kas(c, k, 0.36, -0.36, 0.56, -0.32, 0.04);
    c.beginPath(); c.moveTo(k(0.04), k(0.17)); c.lineTo(k(0.54), k(0.17)); c.quadraticCurveTo(k(0.5), k(0.55), k(0.28), k(0.55)); c.quadraticCurveTo(k(0.06), k(0.55), k(0.04), k(0.17)); c.closePath();
    dol(c, '#7a1f33'); c.save(); c.clip(); elips(c, k(0.3), k(0.52), k(0.15), k(0.1)); dol(c, '#ff6f8a'); c.fillStyle = '#fff'; c.fillRect(k(0.04), k(0.15), k(0.5), k(0.07)); c.restore();
    c.beginPath(); c.moveTo(k(0.04), k(0.17)); c.lineTo(k(0.54), k(0.17)); c.quadraticCurveTo(k(0.5), k(0.55), k(0.28), k(0.55)); c.quadraticCurveTo(k(0.06), k(0.55), k(0.04), k(0.17)); c.closePath(); cizgi(c, L);
  } else if (ifade === 'saskin') {
    goz(c, k, 0.0, -0.04, 0.16, 0.22, 0.02, 0.0, 0.06); goz(c, k, 0.46, -0.04, 0.15, 0.21, 0.02, 0.0, 0.055);
    kas(c, k, -0.12, -0.36, 0.12, -0.38, 0.08); kas(c, k, 0.35, -0.38, 0.58, -0.36, 0.08);
    elips(c, k(0.27), k(0.36), k(0.08), k(0.11)); dol(c, '#7a1f33'); cizgi(c, L);
    // ter damlası
    c.beginPath(); c.moveTo(k(0.78), k(-0.42)); c.quadraticCurveTo(k(0.9), k(-0.22), k(0.84), k(-0.16)); c.quadraticCurveTo(k(0.74), k(-0.12), k(0.73), k(-0.24)); c.closePath(); dol(c, '#8fd6ff'); cizgi(c, k(0.04));
  } else if (ifade === 'kararli') {
    goz(c, k, 0.02, 0.0, 0.13, 0.15, 0.05, 0.03, 0.08); goz(c, k, 0.45, 0.0, 0.12, 0.14, 0.05, 0.03, 0.075);
    c.fillStyle = RENK.ten; c.fillRect(k(-0.14), k(-0.2), k(0.75), k(0.11));
    kas(c, k, -0.12, -0.24, 0.13, -0.12, -0.02); kas(c, k, 0.34, -0.12, 0.58, -0.24, -0.02);
    c.beginPath(); c.roundRect(k(0.08), k(0.2), k(0.4), k(0.17), k(0.06)); dol(c, '#fff'); cizgi(c, L);
    c.beginPath(); c.moveTo(k(0.08), k(0.285)); c.lineTo(k(0.48), k(0.285)); for (const x of [0.18, 0.28, 0.38]) { c.moveTo(k(x), k(0.2)); c.lineTo(k(x), k(0.37)); } c.strokeStyle = INK; c.lineWidth = k(0.035); c.stroke();
  }
}
// Alternatif pilot (karşılaştırma için): kapalı koyu vizör, vizörde parlayan "ekran yüz"
function pilotVizor(c, R, ifade) {
  const k = (v) => v * R;
  daire(c, 0, 0, R); dol(c, kure(c, '#ffffff', 0, 0, R)); cizgi(c, k(0.075), RENK.beyaz);
  daire(c, k(-0.7), k(0.12), k(0.3)); dol(c, kure(c, '#dfe5ef', k(-0.7), k(0.12), k(0.3))); cizgi(c, k(0.06));
  elips(c, k(0.2), k(0.07), k(0.7), k(0.62)); const g = c.createLinearGradient(0, -R, 0, R); g.addColorStop(0, '#2b3f7a'); g.addColorStop(1, '#0d1438'); dol(c, g); cizgi(c, k(0.075));
  c.save(); c.shadowColor = '#5ff'; c.shadowBlur = k(0.25); c.strokeStyle = '#7ff7ff'; c.fillStyle = '#7ff7ff'; c.lineWidth = k(0.1); c.lineCap = 'round';
  if (ifade === 'heyecan') { for (const x of [0.02, 0.45]) { c.beginPath(); c.arc(k(x), k(0.02), k(0.12), Math.PI * 1.1, Math.PI * 1.9); c.stroke(); } c.beginPath(); c.arc(k(0.25), k(0.18), k(0.18), 0.2, Math.PI - 0.2); c.closePath(); c.fill(); }
  else if (ifade === 'saskin') { for (const x of [0.02, 0.45]) { daire(c, k(x), k(-0.02), k(0.12)); c.stroke(); } elips(c, k(0.25), k(0.32), k(0.07), k(0.1)); c.stroke(); }
  else { for (const x of [0.02, 0.45]) { elips(c, k(x), k(-0.02), k(0.07), k(0.13)); c.fill(); } c.beginPath(); c.arc(k(0.25), k(0.18), k(0.13), 0.4, Math.PI - 0.4); c.stroke(); }
  c.restore();
  c.save(); c.globalAlpha = 0.5; c.strokeStyle = '#fff'; c.lineWidth = k(0.07); c.beginPath(); c.ellipse(k(0.2), k(0.07), k(0.6), k(0.52), 0, Math.PI * 1.1, Math.PI * 1.4); c.stroke(); c.restore();
}

// ---------------------------------------------------------------- ALEV (sağ uç = meme; sola uzar)
function alev(c, kare, dalis) {
  const r = rastgele(17 + kare * 31 + (dalis ? 7 : 0));
  const L = (dalis ? 19 : 11) * (0.9 + 0.2 * r()), H = dalis ? 3.6 : 2.9;
  const katlar = dalis ? [['#ff5a2a', 1], ['#ffb02e', 0.78], ['#fff3a0', 0.55], ['#ffffff', 0.32]] : [['#ff4d2e', 1], ['#ff9a2e', 0.76], ['#ffe066', 0.5], ['#fffbe0', 0.26]];
  for (const [renk, s] of katlar) {
    const l = L * s, h = H * (0.55 + 0.45 * s), w1 = (r() - 0.5) * 1.4 * s, w2 = (r() - 0.5) * 1.4 * s;
    c.beginPath(); c.moveTo(0.4, -h); c.bezierCurveTo(-l * 0.35, -h * 1.25 + w1, -l * 0.75, -h * 0.5 + w2, -l, w1 * 0.4);
    c.bezierCurveTo(-l * 0.75, h * 0.5 + w1, -l * 0.35, h * 1.25 + w2, 0.4, h); c.closePath(); c.fillStyle = renk; c.fill();
  }
  if (dalis) { c.save(); c.globalAlpha = 0.9; c.fillStyle = '#bff4ff'; elips(c, -1.2, 0, 2.2, 1.1); c.fill(); c.restore(); }
}

// ---------------------------------------------------------------- BALON (şişme reklam balonu, r = 12, yüzü sola bakar)
function balon(c, ifade) {
  const R = 12, ez = ifade === 'ezik';
  // ip + afiş (reklam yazısı kodla konur)
  c.beginPath(); c.moveTo(0.8, 12.6); c.bezierCurveTo(2.6, 15, -1.2, 16.5, 0.6, 18.6); c.strokeStyle = INK; c.lineWidth = 0.35; c.stroke();
  c.beginPath(); c.moveTo(-5.5, 18.4); c.lineTo(6.5, 18.4); c.lineTo(5.6, 21.6); c.lineTo(-6.2, 21.9); c.closePath(); dol(c, dikey(c, '#ffffff', 18.4, 21.9)); cizgi(c, IL * 0.8, '#ffffff');
  c.fillStyle = RENK.kirmizi; c.fillRect(-5.2, 18.9, 1.0, 2.6); c.fillRect(4.9, 18.9, 1.0, 2.5);
  poli(c, [-0.6, 11.7, 2.1, 11.7, 1.9, 13.2, -0.4, 13.2]); dol(c, '#ff8a1f'); cizgi(c, IL * 0.8);
  // dilimler (plaj topu): eğik eksenli boylam elipsleri
  c.save(); daire(c, 0, 0, R); c.clip();
  c.rotate(-0.38);
  const dilim = ['#ff3346', '#ffcc22', '#ff3346', '#ffcc22', '#ffffff', '#2f8cff'];
  const sin = Math.sin, cos = Math.cos;
  for (let i = 0; i < 6; i++) {
    const t0 = -Math.PI / 2 + i * Math.PI / 6 - 0.6, t1 = t0 + Math.PI / 6;
    c.beginPath();
    for (let j = 0; j <= 24; j++) { const la = -Math.PI / 2 + Math.PI * j / 24; c.lineTo(R * 1.3 * sin(Math.max(-1.57, Math.min(1.57, t0))) * cos(la), R * 1.3 * sin(la)); }
    for (let j = 24; j >= 0; j--) { const la = -Math.PI / 2 + Math.PI * j / 24; c.lineTo(R * 1.3 * sin(Math.max(-1.57, Math.min(1.57, t1))) * cos(la), R * 1.3 * sin(la)); }
    c.closePath(); c.fillStyle = dilim[i]; c.fill();
  }
  daire(c, 0, -R * 1.02, 2.4); dol(c, '#b05cff');
  c.restore();
  // hacim gölgesi (dilimlerin üstüne)
  c.save(); daire(c, 0, 0, R); c.clip();
  const g = c.createRadialGradient(-4, -5, 1, -1, -1, R * 1.25);
  if (ST.golge === 'duz') { g.addColorStop(0, 'rgba(42,29,92,0)'); g.addColorStop(0.74, 'rgba(42,29,92,0)'); g.addColorStop(0.74, 'rgba(42,29,92,.22)'); g.addColorStop(1, 'rgba(42,29,92,.22)'); }
  else { g.addColorStop(0, 'rgba(255,255,255,.35)'); g.addColorStop(0.3, 'rgba(255,255,255,0)'); g.addColorStop(0.62, 'rgba(42,29,92,0)'); g.addColorStop(1, `rgba(42,29,92,${ST.golge === 'parlak' ? 0.55 : 0.35})`); }
  c.fillStyle = g; c.fillRect(-R, -R, 2 * R, 2 * R);
  // trambolin şekil kodu: üstte beyaz yay şeridi
  c.beginPath(); c.arc(0, 0, R * 0.8, Math.PI * 1.2, Math.PI * 1.8); c.strokeStyle = ST.kontur ? INK : 'rgba(42,29,92,.4)'; c.lineWidth = 2.7; c.lineCap = 'round'; c.stroke();
  c.strokeStyle = '#fff'; c.lineWidth = 1.9; c.stroke();
  c.restore();
  daire(c, 0, 0, R); cizgi(c, IL, '#ff3346');
  parla(c, -5.6, -5.6, 2.6, 1.3, -0.75, 0.8);
  // yüz (sola, rokete bakar)
  c.save(); c.translate(-3.2, 2.0);
  const k = v => v;
  if (ez) {
    for (const [x, s] of [[-2.4, 1], [1.8, -1]]) { c.beginPath(); c.moveTo(x - 1.0, -1.1); c.lineTo(x + 0.3 * s, -0.2); c.lineTo(x - 1.0, 0.7); c.strokeStyle = INK; c.lineWidth = 0.55; c.lineCap = 'round'; c.lineJoin = 'round'; c.stroke(); }
    c.beginPath(); c.moveTo(-2.6, 2.6); c.quadraticCurveTo(-1.2, 1.8, 0, 2.6); c.quadraticCurveTo(1.2, 3.4, 2.2, 2.4); c.strokeStyle = INK; c.lineWidth = 0.5; c.stroke();
  } else {
    goz(c, k, -2.6, -0.6, 1.55, 2.0, -0.5, 0.2, 0.85); goz(c, k, 1.8, -0.6, 1.4, 1.85, -0.5, 0.2, 0.78);
    c.beginPath(); c.moveTo(-2.6, 2.0); c.quadraticCurveTo(-0.6, 4.6, 1.8, 2.3); c.quadraticCurveTo(-0.5, 3.0, -2.6, 2.0); c.closePath(); dol(c, '#7a1f33'); cizgi(c, 0.4);
    kas(c, k, -3.3, -2.6, -1.4, -2.7, 0.4); kas(c, k, 0.9, -2.6, 2.6, -2.3, 0.4);
  }
  c.restore();
}

// ---------------------------------------------------------------- ZEPLİN (trambolin sırtlı, r = 22, burnu sola)
function zeplin(c, ifade, renk = RENK.mor) {
  const X = 19.5, Y = 15, cy = 2;
  // kuyruk kanatları
  for (const s of [-1, 1]) {
    const p = [12.5, cy + 5 * s, 22, cy + 13 * s, 24.6, cy + 12.2 * s, 23.4, cy + 4 * s, 18.5, cy + 1.5 * s];
    poli(c, p); dol(c, dikey(c, RENK.kirmizi, cy - 14 * (s < 0), cy + 14 * (s > 0))); cizgi(c, IL, RENK.kirmizi);
  }
  // trambolin ayakları (yaylar)
  c.lineJoin = 'round';
  for (const x of [-10.5, -3.5, 3.5, 10.5]) {
    const yb = cy - Y * Math.sqrt(1 - (x / X) ** 2) + 1.2;
    c.beginPath(); c.moveTo(x, yb); const n = 6, h = (yb - (-19.4)) / n;
    for (let i = 1; i <= n; i++) c.lineTo(x + (i === n ? 0 : i % 2 ? 0.9 : -0.9), yb - h * i);
    c.strokeStyle = ST.kontur ? INK : RENK.koyuMetal; c.lineWidth = 0.75; c.stroke(); c.strokeStyle = '#dfe6f2'; c.lineWidth = 0.32; c.stroke();
  }
  // gövde
  elips(c, 0, cy, X, Y); c.save(); dol(c, dikey(c, renk, cy - Y, cy + Y)); c.clip();
  c.globalAlpha = 0.9; c.fillStyle = dikey(c, RENK.sari, cy + 4, cy + 10); c.fillRect(-X, cy + 5.2, 2 * X, 3.4); c.globalAlpha = 1;
  c.strokeStyle = ST.kontur ? INK : ko(renk, 0.4); c.lineWidth = IL * 0.5; c.globalAlpha = 0.3;
  for (const f of [0.45, 0.82]) { c.beginPath(); c.ellipse(0, cy, X * f, Y, 0, -Math.PI / 2, Math.PI / 2); c.stroke(); c.beginPath(); c.ellipse(0, cy, X * f, Y, 0, Math.PI / 2, Math.PI * 1.5); c.stroke(); }
  c.globalAlpha = 1;
  const g = c.createRadialGradient(-8, cy - 9, 2, -4, cy - 2, X * 1.1); g.addColorStop(0, 'rgba(255,255,255,.25)'); g.addColorStop(0.4, 'rgba(255,255,255,0)'); g.addColorStop(1, 'rgba(42,29,92,.25)'); c.fillStyle = g; c.fillRect(-X, cy - Y, 2 * X, 2 * Y);
  c.restore();
  elips(c, 0, cy, X, Y); cizgi(c, IL, renk);
  parla(c, -4, cy - 10.5, 7, 1.3, -0.1, 0.75);
  // trambolin minderi (şekil kodu: üstte beyaz yay şeridi)
  c.beginPath(); c.roundRect(-13.5, -21.6, 27, 2.6, 1.3); dol(c, dikey(c, RENK.kirmizi, -21.6, -19)); cizgi(c, IL, RENK.kirmizi);
  c.beginPath(); c.moveTo(-11.6, -20.3); c.quadraticCurveTo(0, -19.0, 11.6, -20.3); c.strokeStyle = '#fff'; c.lineWidth = 1.2; c.lineCap = 'round'; c.stroke();
  // gondol
  c.beginPath(); c.roundRect(-8, cy + 13.2, 14, 4.9, 2.2); dol(c, dikey(c, RENK.sari, cy + 13, cy + 18)); cizgi(c, IL, RENK.sari);
  for (const x of [-5.2, -1.6, 2]) { c.beginPath(); c.roundRect(x, cy + 14.4, 2.4, 2, 0.8); dol(c, '#7fc8ff'); cizgi(c, IL * 0.6); }
  // pervane
  c.beginPath(); c.moveTo(6, cy + 15.5); c.lineTo(8.2, cy + 15.5); cizgi(c, 0.6, RENK.koyuMetal);
  elips(c, 8.6, cy + 15.5, 0.6, 2.6); c.save(); c.globalAlpha = 0.7; dol(c, '#c6cede'); c.restore(); cizgi(c, IL * 0.6);
  // yüz (burun, sola)
  c.save(); c.translate(-12.6, cy - 1); c.scale(0.92, 0.92);
  const k = v => v;
  if (ifade === 'ezik') {
    c.beginPath(); c.moveTo(-2.6, -0.8); c.quadraticCurveTo(0, 0.8, 2.2, -0.9); c.strokeStyle = INK; c.lineWidth = 0.6; c.lineCap = 'round'; c.stroke();
    c.beginPath(); c.moveTo(-3, -2.8); c.lineTo(1.8, -2.4); c.stroke();
    c.beginPath(); c.moveTo(-2.2, 5.2); c.quadraticCurveTo(-1, 4.2, 0.2, 5.2); c.quadraticCurveTo(1.4, 6.2, 2.4, 5.0); c.stroke();
  } else if (ifade === 'yama') {
    // sersem: spiral göz + yara bandı
    c.beginPath(); for (let a = 0; a < 12; a += 0.3) c.lineTo(Math.cos(a) * a * 0.2, Math.sin(a) * a * 0.2 - 0.5); c.strokeStyle = INK; c.lineWidth = 0.45; c.stroke();
    c.beginPath(); c.moveTo(-2.4, 5.6); c.quadraticCurveTo(0, 4.0, 2.4, 5.6); c.stroke();
  } else {
    elips(c, -0.2, -0.4, 2.5, 3.0); dol(c, '#fff'); cizgi(c, 0.42);
    daire(c, -1.0, -0.2, 1.35); dol(c, INK); daire(c, -1.5, -0.8, 0.45); dol(c, '#fff');
    c.beginPath(); c.moveTo(-2.9, -3.0); c.quadraticCurveTo(-0.5, -4.6, 2.0, -3.4); c.lineTo(2.2, -2.2); c.quadraticCurveTo(0, -2.9, -2.6, -1.8); c.closePath(); dol(c, ko(renk, 0.1)); cizgi(c, 0.35);
    c.beginPath(); c.moveTo(-2.8, 4.3); c.quadraticCurveTo(-0.2, 7.2, 2.6, 4.6); c.strokeStyle = INK; c.lineWidth = 0.55; c.lineCap = 'round'; c.stroke();
  }
  c.restore();
  if (ifade === 'yama') {
    c.save(); c.translate(-2, cy - 6); c.rotate(-0.5);
    for (const r of [0, Math.PI / 2]) { c.save(); c.rotate(r); c.beginPath(); c.roundRect(-3.2, -0.9, 6.4, 1.8, 0.6); dol(c, '#ffd9a8'); cizgi(c, IL * 0.7); c.restore(); }
    c.restore();
  }
}

// ---------------------------------------------------------------- MARTI (sola bakar)
function marti(c, kare) {
  const gri = '#d3dcec', uc = '#3b4466';
  const K = {   // [p0, kontrol, uç, kontrol, kök] + uç bölgesi (dikdörtgen: x0,y0,x1,y1)
    yukari: [[-0.2, -0.7, -1.2, -5.4, 1.4, -9.8, 2.6, -5.6, 3.4, -0.7, [-3, -12, 6, -7.2]], [-1.6, -0.6, -2.8, -5.2, -0.6, -10.4, 1.2, -5.8, 2.4, -0.6, [-4, -12, 5, -7.6]]],
    orta: [[0.2, -1.0, 3.2, -4.6, 8.6, -4.4, 5.0, -2.2, 3.0, -0.6, [6.2, -7, 10, 0]], [-1.6, -0.8, 1.8, -3.6, 8.2, -3.0, 4.4, -0.8, 2.8, 0.2, [5.8, -6, 10, 2]]],
    asagi: [null, [-1.4, -0.3, -1.2, 4.0, 2.0, 8.0, 3.6, 3.6, 3.0, 0.0, [-3, 5.6, 6, 10]]],
    sersem: [[0.6, -0.8, 4.6, -5.2, 7.8, -5.6, 5.0, -2.6, 3.0, -0.2, [5.8, -8, 10, -3.6]], [-1.4, 0.4, -4.4, 3.4, -2.2, 7.6, 0.4, 4.0, 1.6, 0.6, [-6, 5.4, 2, 10]]],
  }[kare];
  const kanat = (p, renk) => {
    const yol = () => { c.beginPath(); c.moveTo(p[0], p[1]); c.quadraticCurveTo(p[2], p[3], p[4], p[5]); c.quadraticCurveTo(p[6], p[7], p[8], p[9]); c.closePath(); };
    yol(); dol(c, dikey(c, renk, Math.min(p[1], p[5]), Math.max(p[1], p[5]) + 1)); c.save(); c.clip();
    const r = p[10]; c.fillStyle = uc; c.fillRect(r[0], r[1], r[2] - r[0], r[3] - r[1]); c.restore(); yol(); cizgi(c, IL, renk);
  };
  if (K[0]) kanat(K[0], ko(gri, 0.18));
  poli(c, [3.4, -0.6, 6.4, -1.3, 6.1, 1.0, 3.6, 1.3]); dol(c, dikey(c, '#ffffff', -1.3, 1.3)); cizgi(c, IL, '#fff');
  c.fillStyle = uc; c.beginPath(); c.moveTo(6.4, -1.3); c.lineTo(6.1, 1.0); c.lineTo(5.3, 0.9); c.lineTo(5.6, -1.1); c.closePath(); c.fill();
  elips(c, 0.6, 0.3, 4.0, 2.0, -0.06); dol(c, dikey(c, '#ffffff', -1.7, 2.3)); cizgi(c, IL, '#fff');
  daire(c, -3.1, -0.8, 2.0); dol(c, kure(c, '#ffffff', -3.1, -0.8, 2.0)); cizgi(c, IL, '#fff');
  const acik = kare === 'sersem';
  poli(c, acik ? [-4.7, -1.2, -7.3, -1.4, -4.8, -0.4] : [-4.7, -1.3, -7.4, -0.5, -4.8, 0.0]); dol(c, dikey(c, '#ffc21a', -1.4, 0)); cizgi(c, IL * 0.8, '#ffc21a');
  if (acik) { poli(c, [-4.8, -0.2, -6.8, 0.8, -4.6, 0.5]); dol(c, '#ffae1a'); cizgi(c, IL * 0.8); }
  else { daire(c, -6.4, -0.45, 0.32); dol(c, '#ff3346'); }
  if (acik) {
    c.beginPath(); for (let a = 0; a < 10; a += 0.3) c.lineTo(-3.3 + Math.cos(a) * a * 0.08, -1.2 + Math.sin(a) * a * 0.08); c.strokeStyle = INK; c.lineWidth = 0.24; c.stroke();
  } else {
    elips(c, -3.4, -1.2, 0.8, 0.95); dol(c, '#fff'); cizgi(c, 0.22);
    daire(c, -3.7, -1.05, 0.45); dol(c, INK); daire(c, -3.85, -1.25, 0.15); dol(c, '#fff');
    c.beginPath(); c.moveTo(-4.5, -2.4); c.lineTo(-2.6, -1.85); c.strokeStyle = INK; c.lineWidth = 0.4; c.lineCap = 'round'; c.stroke();
  }
  c.beginPath(); c.moveTo(1.2, 2.2); c.lineTo(2.6, 2.9); c.moveTo(2.0, 2.0); c.lineTo(3.4, 2.6); c.strokeStyle = '#ff8a1f'; c.lineWidth = 0.5; c.stroke();
  kanat(K[1], gri);
}

// ---------------------------------------------------------------- UÇURTMA (baklava, r = 7; ip çalışma anında çizilir)
function ucurtma(c, ifade, kare) {
  // kuyruk
  const dal = kare === 'b' ? 1 : -1;
  c.beginPath(); c.moveTo(0, 8.4); c.bezierCurveTo(2.5 * dal, 11, -2.5 * dal, 14, 0.5 * dal, 17.5); c.strokeStyle = INK; c.lineWidth = 0.32; c.stroke();
  const fy = [[0.9 * dal, 11.3, '#ff3346'], [-0.6 * dal, 14.2, '#2f8cff'], [0.6 * dal, 17.2, '#ffcc22']];
  for (const [x, y, r] of fy) { poli(c, [x - 1.5, y - 0.9, x + 1.5, y + 0.9, x + 1.5, y - 0.9, x - 1.5, y + 0.9]); dol(c, r); cizgi(c, 0.28, r); }
  const P = [0, -8.6, 6, -1.6, 0, 8.6, -6, -1.6];
  const parca = [['#ff3346', [0, -8.6, 6, -1.6, 0, -1.6]], ['#ffcc22', [0, -8.6, -6, -1.6, 0, -1.6]], ['#2f8cff', [-6, -1.6, 0, 8.6, 0, -1.6]], ['#3fcf5a', [6, -1.6, 0, 8.6, 0, -1.6]]];
  for (const [r, p] of parca) { poli(c, p); dol(c, dikey(c, r, -8.6, 8.6)); }
  c.beginPath(); c.moveTo(0, -8.6); c.lineTo(0, 8.6); c.moveTo(-6, -1.6); c.lineTo(6, -1.6); c.strokeStyle = ST.kontur ? INK : '#7a5a2a'; c.lineWidth = 0.3; c.stroke();
  poli(c, P); cizgi(c, IL, '#ff3346');
  parla(c, -1.8, -4.6, 1.4, 0.5, -0.9, 0.7);
  const k = v => v;
  c.save(); c.translate(0, 1.4);
  if (ifade === 'saskin') {
    goz(c, k, -1.5, -0.3, 0.95, 1.2, -0.1, 0, 0.35); goz(c, k, 1.5, -0.3, 0.95, 1.2, -0.1, 0, 0.35);
    elips(c, 0, 2.3, 0.55, 0.75); dol(c, '#7a1f33'); cizgi(c, 0.3);
  } else {
    goz(c, k, -1.5, -0.2, 0.8, 1.05, -0.35, 0.1, 0.45); goz(c, k, 1.4, -0.2, 0.8, 1.05, -0.35, 0.1, 0.45);
    c.beginPath(); c.arc(-0.1, 1.4, 1.3, 0.3, Math.PI - 0.3); c.strokeStyle = INK; c.lineWidth = 0.38; c.lineCap = 'round'; c.stroke();
  }
  c.restore();
}

// ---------------------------------------------------------------- YAKIT DRONU (r = 9)
function dron(c, kare, bidonlu = true) {
  if (bidonlu) {
    c.beginPath(); c.moveTo(0, 1.6); c.lineTo(0, 3.4); c.strokeStyle = INK; c.lineWidth = 0.4; c.stroke();
    c.beginPath(); c.arc(0, 3.6, 0.7, Math.PI, 0); c.stroke();
    bidon(c, 0, 4.0);
  }
  // kollar
  for (const s of [-1, 1]) { c.beginPath(); c.roundRect(Math.min(0, s * 8), -2.6, 8, 1.2, 0.6); dol(c, dikey(c, RENK.koyuMetal, -2.6, -1.4)); cizgi(c, IL * 0.8, RENK.koyuMetal); }
  for (const s of [-1, 1]) {
    c.beginPath(); c.roundRect(s * 8 - 0.9, -4.0, 1.8, 2.2, 0.5); dol(c, dikey(c, RENK.koyuMetal, -4, -1.8)); cizgi(c, IL * 0.8);
    // pervane bulanıklığı (iki kare)
    c.save(); c.globalAlpha = 0.55; elips(c, s * 8, -4.4, 4.6, 0.75); dol(c, '#e8eef8'); c.restore();
    c.beginPath(); const a = kare === 'a' ? 1 : -1; c.moveTo(s * 8 - 4.2 * a, -4.6); c.lineTo(s * 8 + 4.2 * a, -4.2); c.strokeStyle = ST.kontur ? INK : RENK.koyuMetal; c.lineWidth = 0.45; c.stroke();
  }
  // gövde
  c.beginPath(); c.roundRect(-4.8, -3.2, 9.6, 5.0, 2.4); dol(c, dikey(c, '#ffc531', -3.2, 1.8)); cizgi(c, IL, '#ffc531');
  c.beginPath(); c.roundRect(-4.8, -0.2, 9.6, 1.1, 0.5); c.save(); c.clip(); c.fillStyle = INK; c.globalAlpha = 0.85; c.fillRect(-5, -0.2, 10, 1.1); c.restore();
  parla(c, -1.8, -2.4, 2.0, 0.4, 0, 0.8);
  // tek göz (kamera)
  daire(c, -2.2, -1.0, 1.55); dol(c, '#ffffff'); cizgi(c, 0.32);
  daire(c, -2.5, -0.9, 0.95); const g = c.createRadialGradient(-2.8, -1.2, 0.1, -2.5, -0.9, 1); g.addColorStop(0, '#5ff7ff'); g.addColorStop(1, '#155a8a'); dol(c, g);
  daire(c, -2.8, -1.25, 0.3); dol(c, '#fff');
  // anten
  c.beginPath(); c.moveTo(2.4, -3.1); c.lineTo(3.2, -4.6); c.strokeStyle = INK; c.lineWidth = 0.3; c.stroke(); daire(c, 3.2, -4.7, 0.4); dol(c, RENK.turkuaz); cizgi(c, 0.2);
}
function bidon(c, x, y) {
  c.save(); c.translate(x, y);
  c.beginPath(); c.roundRect(-2.4, 0, 4.8, 5.2, 1.0); dol(c, dikey(c, RENK.kirmizi, 0, 5.2)); cizgi(c, IL * 0.9, RENK.kirmizi);
  c.beginPath(); c.roundRect(-1.0, -0.6, 2.0, 0.9, 0.3); dol(c, RENK.koyuMetal); cizgi(c, IL * 0.6);
  // yakıt damlası simgesi
  c.beginPath(); c.moveTo(0, 1.3); c.quadraticCurveTo(1.3, 2.8, 1.0, 3.4); c.arc(0, 3.3, 1.0, 0, Math.PI); c.quadraticCurveTo(-1.3, 2.8, 0, 1.3); c.closePath(); dol(c, '#fff');
  parla(c, -1.4, 1.6, 0.3, 1.2, 0, 0.6);
  c.restore();
}

// ---------------------------------------------------------------- EFEKTLER
function toz(c, kare) {   // sekme tozu / duman puf'u: 4 kare, büyür ve dağılır
  const r = rastgele(91), n = 6, b = 1 + kare * 0.55;   // saydamlık çalışma anında (kontur gri görünmesin)
  const top = [];
  for (let i = 0; i < n; i++) { const t = i / n * 6.283 + r(); top.push([Math.cos(t) * 2.6 * b, Math.sin(t) * 1.6 * b, (1.6 + r() * 1.2) * (1 + kare * 0.3)]); }
  c.beginPath(); for (const [x, y, s] of top) { c.moveTo(x + s, y); c.arc(x, y, s, 0, 6.283); } dol(c, '#c8c3ea');
  c.save(); c.clip(); c.beginPath(); for (const [x, y, s] of top) { c.moveTo(x - 0.3 + s * 0.85, y - 0.5); c.arc(x - 0.3, y - 0.5, s * 0.85, 0, 6.283); } dol(c, '#ffffff'); c.restore();
  c.beginPath(); for (const [x, y, s] of top) { c.moveTo(x + s, y); c.arc(x, y, s, 0, 6.283); }
  c.globalAlpha = 1;
}
function yildiz5(c, x, y, R, r, rot) { c.beginPath(); for (let i = 0; i < 10; i++) { const a = rot + i * Math.PI / 5 - Math.PI / 2, q = i % 2 ? r : R; c.lineTo(x + Math.cos(a) * q, y + Math.sin(a) * q); } c.closePath(); }
function yildizPatlama(c, kare) {   // sekme/çarpma: 3 kare
  const n = 10, L = [6, 10, 11][kare], w = [0.9, 0.7, 0.35][kare], a0 = [0, 0.2, 0.35][kare];
  c.fillStyle = '#ffffff'; c.globalAlpha = [1, 0.9, 0.6][kare];
  for (let i = 0; i < n; i++) { const a = a0 + i * 6.283 / n, l = L * (i % 2 ? 0.7 : 1), r0 = kare === 2 ? L * 0.55 : 1.5;
    c.beginPath(); c.moveTo(Math.cos(a - 0.12 * w) * r0, Math.sin(a - 0.12 * w) * r0); c.lineTo(Math.cos(a) * l, Math.sin(a) * l); c.lineTo(Math.cos(a + 0.12 * w) * r0, Math.sin(a + 0.12 * w) * r0); c.closePath(); c.fill(); }
  c.globalAlpha = 1;
  if (kare === 0) { daire(c, 0, 0, 3.6); const g = c.createRadialGradient(0, 0, 0, 0, 0, 3.6); g.addColorStop(0, '#fff'); g.addColorStop(0.6, '#fff7c0'); g.addColorStop(1, 'rgba(255,220,80,0)'); dol(c, g); }
  if (kare === 1) { yildiz5(c, 0, 0, 4.6, 2.1, 0.15); dol(c, kure(c, '#ffd23f', 0, 0, 4.6)); cizgi(c, 0.45, '#ffd23f'); parla(c, -1.1, -1.3, 0.9, 0.5, -0.6, 0.85); }
  if (kare === 2) for (const [x, y, s, r] of [[-5, -4, 1.6, 0.3], [5.5, -2.5, 1.3, -0.4], [-3, 5, 1.1, 0.6], [4, 5.2, 1.4, 0.1]]) { yildiz5(c, x, y, s, s * 0.45, r); dol(c, '#ffd23f'); cizgi(c, 0.3, '#ffd23f'); }
}
function parilti(c) {
  c.beginPath(); const R = 2.6, r = 0.55; for (let i = 0; i < 8; i++) { const a = i * Math.PI / 4 - Math.PI / 2, q = i % 2 ? r : R * (i % 4 === 0 ? 1 : 0.7); c.lineTo(Math.cos(a) * q, Math.sin(a) * q); } c.closePath();
  dol(c, '#ffffff'); c.strokeStyle = '#ffd23f'; c.lineWidth = 0.35; c.stroke();
}
function tuy(c) {
  c.beginPath(); c.moveTo(-2, 0); c.quadraticCurveTo(0, -1.4, 2.2, -0.2); c.quadraticCurveTo(0, 1.1, -2, 0); c.closePath(); dol(c, '#fff'); cizgi(c, 0.25, '#fff');
  c.beginPath(); c.moveTo(-2.6, 0.3); c.quadraticCurveTo(0, -0.3, 2.0, -0.2); c.strokeStyle = '#9aa6bd'; c.lineWidth = 0.2; c.stroke();
}
function sesKonisi(c) {   // ses duvarı buhar konisi: tepe (0,0) sağda = roket burnu; geriye açılır
  for (const [s, a] of [[1, 0.8], [0.8, 0.7], [0.6, 0.7]]) {
    c.beginPath(); c.moveTo(1, 0); c.bezierCurveTo(-4 * s, -3 * s, -9 * s, -9 * s, -15 * s, -10.5 * s);
    c.bezierCurveTo(-13 * s, -4 * s, -13 * s, 4 * s, -15 * s, 10.5 * s); c.bezierCurveTo(-9 * s, 9 * s, -4 * s, 3 * s, 1, 0); c.closePath();
    const g = c.createLinearGradient(0, 0, -15 * s, 0); g.addColorStop(0, 'rgba(255,255,255,0)'); g.addColorStop(0.7, `rgba(235,248,255,${a * 0.6})`); g.addColorStop(1, `rgba(255,255,255,${a})`);
    c.fillStyle = g; c.fill();
  }
  c.beginPath(); c.ellipse(-14.6, 0, 1.6, 10.3, 0, 0, 6.283); c.strokeStyle = 'rgba(255,255,255,.95)'; c.lineWidth = 0.7; c.stroke();
}
function jeton(c) {
  daire(c, 0, 0, 2.4); dol(c, kure(c, '#ffcc22', 0, 0, 2.4)); cizgi(c, 0.35, '#ffcc22');
  daire(c, 0, 0, 1.75); c.strokeStyle = '#e09a00'; c.lineWidth = 0.22; c.stroke();
  yildiz5(c, 0, 0.1, 1.2, 0.5, 0); dol(c, '#fff3a8');
}
function parasut(c) {   // ayrılan kademe paraşütü; bağlantı noktası (0,0) altta
  c.beginPath(); c.moveTo(-7, -9); c.lineTo(0, 0); c.lineTo(7, -9); c.moveTo(-2.5, -9.8); c.lineTo(0, 0); c.lineTo(2.5, -9.8); c.strokeStyle = INK; c.lineWidth = 0.25; c.stroke();
  c.beginPath(); c.moveTo(-7.4, -9); c.bezierCurveTo(-7.4, -17, 7.4, -17, 7.4, -9);
  for (let i = 3; i >= -3; i--) c.quadraticCurveTo(i * 2.1 + 1.05, -10.4, i * 2.1 - 1.05 + 0 * i, -9);
  c.closePath(); c.save(); dol(c, dikey(c, '#ffffff', -15, -9)); c.clip();
  c.fillStyle = dikey(c, RENK.kirmizi, -15, -9); for (const x of [-5.2, 1.0]) c.fillRect(x, -17, 4.2 - (x > 0 ? 0 : 0), 9);
  c.restore(); c.beginPath(); c.moveTo(-7.4, -9); c.bezierCurveTo(-7.4, -17, 7.4, -17, 7.4, -9); for (let i = 3; i >= -3; i--) c.quadraticCurveTo(i * 2.1 + 1.05, -10.4, i * 2.1 - 1.05, -9); c.closePath(); cizgi(c, IL * 2.4, '#fff');
}
function balonParca(c) {
  c.beginPath(); c.moveTo(-1.8, -0.8); c.quadraticCurveTo(0, -1.8, 2.0, -0.6); c.lineTo(1.2, 0.9); c.quadraticCurveTo(0, 0.2, -1.1, 0.9); c.closePath(); dol(c, '#ff3346'); cizgi(c, 0.3);
}

// ---------------------------------------------------------------- ARKA PLAN
function bulut(c, w, h, tohum, uzak) {
  const r = rastgele(tohum);
  if (uzak) {   // uzak katman: yassı, lavanta-beyaz şeritler (yakın kümülüslerden farklı)
    const el = [];
    for (let i = 0; i < 5; i++) el.push([(i / 4 - 0.5) * w * 0.5 + (r() - 0.5) * w * 0.08, (r() - 0.5) * h * 0.4, w * (0.12 + r() * 0.1), h * (0.22 + r() * 0.16)]);
    c.beginPath(); for (const [x, y, rx, ry] of el) { c.moveTo(x + rx, y); c.ellipse(x, y, rx, ry, 0, 0, 6.283); }
    const g = c.createLinearGradient(0, -h * 0.5, 0, h * 0.5); g.addColorStop(0, '#fbf8ff'); g.addColorStop(1, '#d9d2f0'); c.fillStyle = g; c.fill();
    return;
  }
  const top = [], n = Math.max(3, Math.round(w / h * 1.6));
  for (let i = 0; i < n; i++) top.push([((i + 0.5) / n - 0.5) * w * 0.8, h * 0.18, h * 0.3 * (0.9 + 0.2 * r())]);
  for (let i = 0; i < n - 1; i++) { const t = (i + 1) / n, tepe = Math.sin(Math.PI * t) ** 0.6, sx = h * (0.3 + 0.32 * tepe) * (0.85 + 0.3 * r()); top.push([(t - 0.5) * w * 0.8, h * 0.18 - sx * 0.75, sx]); }
  const yol = (dx, dy, k) => { c.beginPath(); for (const [x, y, s] of top) { c.moveTo(x + dx + s * k, y + dy); c.arc(x + dx, y + dy, s * k, 0, 6.283); } };
  yol(0, 0, 1); dol(c, '#c4d8f6');
  c.save(); yol(0, 0, 1); c.clip(); yol(-h * 0.04, -h * 0.12, 0.92); dol(c, '#ffffff');
  yol(-h * 0.08, -h * 0.2, 0.72); c.save(); c.globalAlpha = 0.55; dol(c, '#ffffff'); c.restore(); c.restore();
}
function zemin(c, W) {   // yatayda döşenebilir: tüm dalgalar W'nin tam katı periyotlu
  const T = (x, ks) => ks.reduce((t, [a, k, f]) => t + a * Math.sin(2 * Math.PI * k * x / W + f), 0);
  const tepe = (ks, taban, renk1, renk2) => {
    c.beginPath(); c.moveTo(0, 5); for (let x = 0; x <= W; x += 1) c.lineTo(x, taban - T(x, ks)); c.lineTo(W, 5); c.closePath();
    const g = c.createLinearGradient(0, taban - 10, 0, 3); g.addColorStop(0, renk1); g.addColorStop(1, renk2); c.fillStyle = g; c.fill();
    c.beginPath(); for (let x = 0; x <= W; x += 1) c.lineTo(x, taban - T(x, ks)); c.strokeStyle = ko(renk2, 0.3); c.lineWidth = 0.45; c.stroke();
  };
  const agacKume = (x, y, n, r) => {
    for (let i = 0; i < n; i++) { const dx = (i - (n - 1) / 2) * r * 1.3, dy = (i % 2) * r * 0.35, rr = r * (0.85 + 0.3 * ((i * 7) % 3) / 2);
      c.fillStyle = '#7a5a3a'; c.fillRect(x + dx - 0.25, y + dy - 0.2, 0.5, 1.6);
      daire(c, x + dx, y + dy - rr * 0.9, rr); c.fillStyle = '#6fa868'; c.fill(); c.strokeStyle = '#3f6f48'; c.lineWidth = 0.35; c.stroke();
      daire(c, x + dx - rr * 0.3, y + dy - rr * 1.15, rr * 0.4); c.fillStyle = '#8fc082'; c.fill(); }
  };
  tepe([[6, 2, 0.4], [3, 5, 1.3], [1.5, 9, 2]], -6, '#b4d7a2', '#8fbf84');
  const r = rastgele(5), arka = [[3, 3, 0.2], [1.2, 7, 1]];
  for (let i = 0; i < 6; i++) { const x = (i + 0.2 + r() * 0.6) * W / 6; agacKume(x, -T(x, arka) - 0.6, 2 + (i % 3), 1.4 + r() * 0.5); }
  const ex_ = W * 0.62, ey_ = -T(W * 0.62, arka) - 0.6;
  c.fillStyle = '#e8846f'; c.fillRect(ex_ - 3, ey_ - 3.6, 6, 3.6); c.strokeStyle = INK; c.lineWidth = 0.3; c.strokeRect(ex_ - 3, ey_ - 3.6, 6, 3.6);
  poli(c, [ex_ - 3.6, ey_ - 3.5, ex_, ey_ - 6.6, ex_ + 3.6, ey_ - 3.5]); dol(c, '#9a5a48'); cizgi(c, 0.3);
  c.fillStyle = '#fff'; c.fillRect(ex_ - 0.8, ey_ - 2.4, 1.6, 2.4);
  tepe([[2.2, 3, 0.2], [1.2, 7, 1], [0.5, 13, 0.3]], 0, '#a2cf92', '#7fb57a');
  // tarlalar: dalgalı sınırlı şeritler, her şerit eğri ayraçlarla parsellere bölünür
  const renkler = ['#a3c98f', '#c3d39a', '#d9d0a0', '#94bf88', '#b9cf9c', '#cfc795'];
  const sinir = (k, x) => { let y = 1.5; for (let i = 0; i < k; i++) y += 4 + i * 1.7; return y + (k ? 1.6 * Math.sin(2 * Math.PI * (k % 3 + 1) * x / W + k) : 0); };
  for (let k = 0; k < 9; k++) {
    const n = 3 + (k % 3), ofs = r();
    for (let p = 0; p < n; p++) {
      const xa = ((p + ofs) / n) * W, xb = ((p + 1 + ofs) / n) * W;
      c.beginPath();
      for (let x = xa; x <= xb + 0.01; x += 2) c.lineTo(x, sinir(k, x));
      for (let x = xb; x >= xa - 0.01; x -= 2) c.lineTo(x + 1.5 * Math.sin((x - xb) * 0.2 + k), sinir(k + 1, x));
      c.closePath(); c.fillStyle = renkler[(k * 2 + p) % renkler.length]; c.fill();
      // sürüm izleri
      c.save(); c.clip(); c.strokeStyle = 'rgba(70,110,60,.18)'; c.lineWidth = 0.3;
      for (let j = 1; j < 6; j++) { c.beginPath(); for (let x = xa - 2; x <= xb + 2; x += 3) c.lineTo(x, lerp(sinir(k, x), sinir(k + 1, x), j / 6)); c.stroke(); }
      c.restore();
      if (xb > W) { c.save(); c.translate(-W, 0); c.beginPath(); for (let x = xa; x <= xb + 0.01; x += 2) c.lineTo(x, sinir(k, x)); for (let x = xb; x >= xa - 0.01; x -= 2) c.lineTo(x + 1.5 * Math.sin((x - xb) * 0.2 + k), sinir(k + 1, x)); c.closePath(); c.fillStyle = renkler[(k * 2 + p) % renkler.length]; c.fill(); c.restore(); }
    }
    c.beginPath(); for (let x = 0; x <= W; x += 2) c.lineTo(x, sinir(k + 1, x)); c.strokeStyle = '#7fa871'; c.lineWidth = 0.5; c.stroke();
  }
  // yol (kıvrımlı, döşenebilir)
  const yol = x => 16 + 5 * Math.sin(2 * Math.PI * 2 * x / W + 0.7) + 2 * Math.sin(2 * Math.PI * 5 * x / W);
  c.beginPath(); for (let x = 0; x <= W; x += 1) c.lineTo(x, yol(x)); c.strokeStyle = '#b8a77f'; c.lineWidth = 3.2; c.stroke(); c.strokeStyle = '#e9dfc4'; c.lineWidth = 2.4; c.stroke();
  // tarla aralarında ağaç kümeleri
  for (let i = 0; i < 5; i++) { const x = (i + 0.5) * W / 5 + 7, k = 2 + (i % 4) * 2; agacKume(x, sinir(k, x) + 0.6, 2 + (i % 2), 1.5); }
}
function lerp(a, b, t) { return a + (b - a) * t; }
function uzakTepe(c, W) {   // soluk mor-yeşil tepe siluetleri (deniz değil); alt kısım sahnede sisle zemine erir
  const sirt = (ks, taban, ust, alt) => {
    const T = (x) => ks.reduce((t, [a, k, f]) => t + a * Math.sin(2 * Math.PI * k * x / W + f), 0);
    c.beginPath(); c.moveTo(0, 30); for (let x = 0; x <= W; x += 1) c.lineTo(x, taban - T(x)); c.lineTo(W, 30); c.closePath();
    const g = c.createLinearGradient(0, taban - 12, 0, 26); g.addColorStop(0, ust); g.addColorStop(1, alt); c.fillStyle = g; c.fill();
  };
  sirt([[6, 2, 1], [3, 5, 0], [1.5, 11, 2]], -8, '#b3a9da', '#c9c8e0');
  sirt([[4, 3, 0.4], [2, 7, 1.1], [1, 13, 0.2]], -1, '#9fbfa6', '#bcd0c0');
}
function rampa(c) {   // rampa: ray (−76.8, 0) → (0, 60) dünya; sprite'ta y aşağı
  const bx = -76.8;
  c.lineCap = 'round'; c.lineJoin = 'round';
  const kiris = (x0, y0, x1, y1, w, renk) => { c.beginPath(); c.moveTo(x0, y0); c.lineTo(x1, y1); c.strokeStyle = ST.kontur ? INK : ko(renk, 0.4); c.lineWidth = w + IL * 2; c.stroke(); c.strokeStyle = renk; c.lineWidth = w; c.stroke(); };
  // kafes ayaklar
  for (const [x, y] of [[-4, -57], [-24, -42], [-44, -26.5]]) { kiris(x, 0, x, y, 1.6, '#5b8fd6'); }
  kiris(-4, -10, -24, 0, 0.8, '#7fa8e6'); kiris(-4, -10, -24, -20, 0.8, '#7fa8e6'); kiris(-4, -30, -24, -20, 0.8, '#7fa8e6'); kiris(-4, -30, -24, -40, 0.8, '#7fa8e6');
  kiris(-24, -10, -44, 0, 0.8, '#7fa8e6'); kiris(-24, -10, -44, -22, 0.8, '#7fa8e6');
  // ray (kırmızı-beyaz şeritli kiriş)
  const L = Math.hypot(76.8, 60), a = Math.atan2(-60, 76.8);
  c.save(); c.translate(bx, 0); c.rotate(a);
  c.beginPath(); c.roundRect(-1, -2.2, L + 2, 3.4, 1.4); dol(c, '#ffffff'); c.save(); c.clip();
  c.fillStyle = RENK.kirmizi; for (let x = 0; x < L; x += 8) c.fillRect(x, -3, 4, 6);
  c.fillStyle = 'rgba(42,29,92,.18)'; c.fillRect(-2, 0.2, L + 4, 2); c.restore();
  c.beginPath(); c.roundRect(-1, -2.2, L + 2, 3.4, 1.4); cizgi(c, IL);
  c.restore();
  // taban
  c.beginPath(); c.roundRect(-52, -1.2, 54, 3.2, 1); dol(c, dikey(c, '#9aa6bd', -1.2, 2)); cizgi(c, IL);
  c.beginPath(); c.roundRect(bx - 3, -1.2, 8, 3.2, 1); dol(c, dikey(c, '#9aa6bd', -1.2, 2)); cizgi(c, IL);
}

// ---------------------------------------------------------------- SPRITE TANIMLARI
// x0,y0,x1,y1: sınır (birim). d: yoğunluk çarpanı. ol: dış kontur (birim; 0 = yok).
const SPRITE = [];
const OLPX = 2.5, KN = 1.9, ol = (m = 1) => OLPX / (KN * m);   // dış kontur (birim) = 2,5 px / (1,9 px/birim × görüntüleme çarpanı)
const ekle = (ad, x0, y0, x1, y1, ciz, o = {}) => SPRITE.push({ ad, x0, y0, x1, y1, ciz, d: o.d ?? 1, ol: o.ol ?? ol(1), olRenk: o.olRenk || null });
ekle('roket_ust', -7.4, -7.8, 13, 7.8, roketUst);
ekle('roket_alt', -21, -10.4, -4.6, 10.4, roketAlt);
ekle('cam', -2.5, -2.8, 3, 2.6, camParlak, { ol: 0 });
for (const f of ['notr', 'heyecan', 'saskin', 'kararli']) {
  ekle('pilot_' + f, -2.6, -2.6, 2.6, 2.6, c => pilotKafa(c, 2.35, f, false), { ol: 0, d: 1.5 });
  ekle('portre_' + f, -17.5, -23.5, 17.5, 16.5, c => pilotKafa(c, 15, f, true), { ol: ol(1.75 / 1.9) });
}
for (let i = 0; i < 4; i++) { ekle('alev_' + i, -13, -4, 1, 4, c => alev(c, i, false), { ol: 0 }); ekle('alev_dalis_' + i, -21, -5, 1, 5, c => alev(c, i, true), { ol: 0 }); }
ekle('balon', -13, -13, 13, 23, c => balon(c, 'normal'));
ekle('balon_ezik', -13, -13, 13, 23, c => balon(c, 'ezik'));
for (const f of ['normal', 'ezik', 'yama']) ekle('zeplin_' + f, -21, -23, 25.5, 21, c => zeplin(c, f));
for (const f of ['yukari', 'orta', 'asagi', 'sersem']) ekle('marti_' + f, -8, -11, 10.5, 8.6, c => marti(c, f), { ol: ol(0.85) });
for (const [f, k] of [['a', 'a'], ['b', 'b'], ['saskin', 'a']]) ekle('ucurtma_' + f, -6.6, -9.2, 6.6, 18.6, c => ucurtma(c, f === 'saskin' ? 'saskin' : 'normal', k));
ekle('dron_a', -13, -5.6, 13, 9.8, c => dron(c, 'a'));
ekle('dron_b', -13, -5.6, 13, 9.8, c => dron(c, 'b'));
ekle('dron_bos', -13, -5.6, 13, 2.6, c => dron(c, 'a', false));
ekle('bidon', -2.8, -1, 2.8, 5.6, c => bidon(c, 0, 0));
for (let i = 0; i < 4; i++) ekle('toz_' + i, -13, -11, 13, 11, c => toz(c, i), { ol: ol(0.9) });
for (let i = 0; i < 3; i++) ekle('yildiz_' + i, -11.5, -11.5, 11.5, 11.5, c => yildizPatlama(c, i), { ol: i === 1 ? ol(1.1) : 0 });
ekle('parilti', -2.8, -2.8, 2.8, 2.8, parilti, { ol: 0 });
ekle('tuy', -2.8, -1.4, 2.6, 1.3, tuy);
ekle('balon_parca', -2.2, -1.6, 2.4, 1.3, balonParca, { ol: ol(1.2) });
ekle('ses_konisi', -17, -11.5, 1.5, 11.5, sesKonisi, { ol: 0 });
ekle('jeton', -2.6, -2.6, 2.6, 2.6, jeton, { ol: ol(1.1) });
ekle('parasut', -8.5, -16.5, 8.5, 0.8, parasut, { ol: 0 });
ekle('bulut_0', -31, -19, 31, 10, c => bulut(c, 60, 16, 3, false), { ol: 1.2 / 1.9, olRenk: '#a8c8f0', d: 0.6 });
ekle('bulut_1', -23, -16.5, 23, 9, c => bulut(c, 44, 14, 8, false), { ol: 1.2 / 1.9, olRenk: '#a8c8f0', d: 0.6 });
ekle('bulut_2', -37.5, -21, 37.5, 11, c => bulut(c, 76, 18, 21, false), { ol: 1.2 / 1.9, olRenk: '#a8c8f0', d: 0.6 });
ekle('bulut_uzak_0', -39, -6, 39, 6, c => bulut(c, 80, 10, 5, true), { ol: 0, d: 0.35 });
ekle('bulut_uzak_1', -30, -5.5, 30, 5.5, c => bulut(c, 60, 9, 13, true), { ol: 0, d: 0.35 });
ekle('zemin', 0, -16, 200, 90, c => zemin(c, 200), { ol: 0, d: 0.5 });
ekle('uzak_tepe', 0, -14, 300, 30, c => uzakTepe(c, 300), { ol: 0, d: 0.3 });
ekle('rampa', -80, -61, 4, 2.5, rampa, { d: 0.6 });

if (typeof module !== 'undefined') module.exports = { SPRITE, ST, INK };
