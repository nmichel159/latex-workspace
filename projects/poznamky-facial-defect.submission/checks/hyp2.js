'use strict';
// Further tests on small maps (W variant):
//  (4C)  some facially proper 4-edge-colouring has a pair of colours {X,Y} with no pattern XYX on a facial walk
//  (P)   every edge can be coloured c and can be coloured a in some [1,1,2]-colouring
//  (ST)  product construction for bridgeless loopless maps
const pm = require('./pm.js');
const MAXM = parseInt(process.argv[2] || '7', 10);
const res = {};
function bump(k, m) { if (!res[k]) res[k] = {}; res[k][m] = (res[k][m] || 0) + 1; }
const ex = {};
function note(k, sigma) { if (!ex[k]) ex[k] = pm.describe(sigma); }

function fourColTest(sigma) {
  const m = sigma.length / 2;
  const runs = pm.edgeRuns(sigma, 'W', 3);
  const pairs = runs[2], triples = runs[3];
  const adj = Array.from({ length: m }, () => []);
  for (const [a, b] of pairs) { adj[a].push(b); adj[b].push(a); }
  const col = new Int8Array(m).fill(-1);
  let found = false, any = false;
  function test() {
    any = true;
    // pairs of colours appearing as XYX
    const bad = new Set();
    for (const [a, b, c] of triples) if (col[a] === col[c]) bad.add(Math.min(col[a], col[b]) * 4 + Math.max(col[a], col[b]));
    return bad.size < 6;
  }
  function rec(i, maxc) {
    if (found) return;
    if (i === m) { if (test()) found = true; return; }
    for (let c = 0; c <= Math.min(3, maxc + 1); c++) {
      let ok = true;
      for (const j of adj[i]) if (j < i && col[j] === c) { ok = false; break; }
      if (!ok) continue;
      col[i] = c;
      rec(i + 1, Math.max(maxc, c));
      if (found) return;
    }
    col[i] = -1;
  }
  rec(0, -1);
  return { found, any };
}

function productTest(sigma) {
  const { vert, nv } = pm.vertices(sigma);
  const fs = pm.faces(sigma);
  const m = sigma.length / 2;
  const fidx = new Int32Array(sigma.length);
  fs.forEach((w, i) => { for (const d of w) fidx[d] = i; });
  const triples = pm.edgeRuns(sigma, 'W', 3)[3];
  const nn = nv + fs.length;
  for (let chi = 0; chi < (1 << (nn - 1)); chi++) {
    let S = 0;
    for (let e = 0; e < m; e++) {
      const bi = ((chi >> vert[2 * e] & 1) !== (chi >> vert[2 * e + 1] & 1)) && ((chi >> (nv + fidx[2 * e]) & 1) !== (chi >> (nv + fidx[2 * e + 1]) & 1));
      if (!bi) S |= 1 << e;
    }
    let ok = true;
    for (const t of triples) if ((S >> t[0] & 1) && (S >> t[1] & 1) && (S >> t[2] & 1)) { ok = false; break; }
    if (ok) return true;
  }
  return false;
}

function check(sigma) {
  const m = sigma.length / 2;
  const { vert } = pm.vertices(sigma);
  const fs = pm.faces(sigma);
  const fidx = new Int32Array(sigma.length);
  fs.forEach((w, i) => { for (const d of w) fidx[d] = i; });
  let bridgeless = true, loopless = true;
  for (let e = 0; e < m; e++) { if (fidx[2 * e] === fidx[2 * e + 1]) bridgeless = false; if (vert[2 * e] === vert[2 * e + 1]) loopless = false; }
  bump('all', m);
  const r = fourColTest(sigma);
  if (!r.any) bump('no facial 4-colouring (loops)', m);
  else if (!r.found) { bump('4C fails', m); note('4C fails', sigma); if (bridgeless && loopless) { bump('4C fails, bridgeless loopless', m); note('4C fails, bridgeless loopless', sigma); } }
  for (let e = 0; e < m; e++) {
    if (pm.edgeColoring(sigma, [1, 1, 2], 'W', [[e, 4]]) === null) { bump('edge never c', m); note('edge never c', sigma); }
    if (pm.edgeColoring(sigma, [1, 1, 2], 'W', [[e, 1]]) === null) { bump('edge always c', m); note('edge always c', sigma); }
  }
  if (bridgeless && loopless) { bump('bridgeless loopless', m); if (!productTest(sigma)) { bump('product fails', m); note('product fails', sigma); } }
}

let level = new Map();
for (const s of [Int32Array.from([0, 1]), Int32Array.from([1, 0])]) level.set(pm.canonKey(s), s);
for (const s of level.values()) check(s);
const t0 = Date.now();
for (let m = 2; m <= MAXM; m++) {
  const next = new Map();
  for (const g of level.values()) for (const h of pm.childrenAll(g)) { const key = pm.canonKey(h); if (!next.has(key)) { next.set(key, h); check(h); } }
  console.log(`m=${m}: ${next.size} maps, ${((Date.now() - t0) / 1000).toFixed(1)} s`);
  level = next;
}
for (const k of Object.keys(res)) console.log('  ', k, JSON.stringify(res[k]));
for (const k of Object.keys(ex)) console.log('EX', k, ex[k]);
