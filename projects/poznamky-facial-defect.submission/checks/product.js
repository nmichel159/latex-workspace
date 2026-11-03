'use strict';
// Product construction: 2-colourings sigma of the vertices and tau of the faces such that every facial trail of
// three edges contains an edge whose ends differ in sigma and whose sides differ in tau.
// Tested on all 3-connected plane graphs with at most MAXM edges (mode poly) or on all 2-edge-connected
// loopless plane multigraphs with at most MAXM edges (mode maps).
const pm = require('./pm.js');
const MODE = process.argv[2] || 'poly';
const MAXM = parseInt(process.argv[3] || '16', 10);

function productExists(sigma) {
  const { vert, nv } = pm.vertices(sigma);
  const fs = pm.faces(sigma);
  const m = sigma.length / 2;
  const fidx = new Int32Array(sigma.length);
  fs.forEach((w, i) => { for (const d of w) fidx[d] = i; });
  const nf = fs.length;
  // variables: chi(vertex) 0..nv-1, chi(face) nv..nv+nf-1, n_e, then not-n_e
  const X = nv + nf, NE = X, NN = X + m;
  const cons = [];
  for (let e = 0; e < m; e++) {
    const u = vert[2 * e], v = vert[2 * e + 1], f = nv + fidx[2 * e], g = nv + fidx[2 * e + 1];
    cons.push({ c: 0, t: [NE + e, NN + e] }, { c: 1, t: [NE + e, NN + e] });
    cons.push({ c: 1, t: [NE + e, u, v] }, { c: 0, t: [NN + e, u, v] });
    cons.push({ c: 1, t: [NE + e, f, g] }, { c: 0, t: [NN + e, f, g] });
  }
  for (const t of pm.edgeRuns(sigma, 'W', 3)[3]) cons.push({ c: 0, t: t.map((e) => NE + e) });
  return pm.solveCSP(X + 2 * m, 2, cons, [[0, 1], [nv, 1]]) !== null;
}

const res = {};
function bump(k, m) { if (!res[k]) res[k] = {}; res[k][m] = (res[k][m] || 0) + 1; }
let example = null;
function check(s) {
  const m = s.length / 2;
  bump('tested', m);
  if (!productExists(s)) { bump('no product', m); if (!example) example = pm.describe(s); }
}
const t0 = Date.now();
if (MODE === 'poly') {
  let level = new Map();
  for (let m = 6; m <= MAXM; m++) {
    const next = new Map();
    if (m % 2 === 0) { const w = pm.wheel(m / 2); next.set(pm.canonKey(w), w); }
    for (const g of level.values()) for (const h of pm.childrenPoly(g)) {
      if (!pm.isSimple3Plausible(h)) continue;
      const key = pm.canonKey(h);
      if (next.has(key) || !pm.is3Connected(h)) continue;
      next.set(key, h);
    }
    for (const h of next.values()) check(h);
    console.log(`m=${m}: ${next.size} polyhedra, ${((Date.now() - t0) / 1000).toFixed(1)} s`);
    level = next;
  }
} else {
  let level = new Map();
  for (const s of [Int32Array.from([0, 1]), Int32Array.from([1, 0])]) level.set(pm.canonKey(s), s);
  for (let m = 2; m <= MAXM; m++) {
    const next = new Map();
    for (const g of level.values()) for (const h of pm.childrenAll(g)) {
      const key = pm.canonKey(h);
      if (next.has(key)) continue;
      next.set(key, h);
      const { vert } = pm.vertices(h);
      const fs = pm.faces(h);
      const fidx = new Int32Array(h.length);
      fs.forEach((w, i) => { for (const d of w) fidx[d] = i; });
      let ok = true;
      for (let e = 0; e < m && ok; e++) if (fidx[2 * e] === fidx[2 * e + 1] || vert[2 * e] === vert[2 * e + 1]) ok = false;
      if (ok) check(h);
    }
    console.log(`m=${m}: ${next.size} maps, ${((Date.now() - t0) / 1000).toFixed(1)} s`);
    level = next;
  }
}
for (const k of Object.keys(res)) console.log('  ', k, JSON.stringify(res[k]));
if (example) console.log('EX no product:', example);
