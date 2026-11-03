'use strict';
// Tests on all maps with at most MAXM edges:
//  (PAR)  parity criterion: S valid (M - S bipartite)  <=>  every component of K(S) has an even number of odd nodes
//  (ST)   product construction: 2-colourings sigma of V and tau of F with every facial triple containing an edge
//         that is bichromatic for both
//  (FOR)  forest construction: N a forest hitting every facial triple, no odd vertex N-full
const pm = require('./pm.js');
const MAXM = parseInt(process.argv[2] || '7', 10);
const VARIANT = process.argv[3] || 'W';

function info(sigma) {
  const { vert, nv } = pm.vertices(sigma);
  const fs = pm.faces(sigma);
  const m = sigma.length / 2;
  const fidx = new Int32Array(sigma.length);
  fs.forEach((w, i) => { for (const d of w) fidx[d] = i; });
  const eu = [], ev = [], ef = [], eg = [];
  for (let e = 0; e < m; e++) { eu.push(vert[2 * e]); ev.push(vert[2 * e + 1]); ef.push(fidx[2 * e]); eg.push(fidx[2 * e + 1]); }
  // facial adjacency pairs (distinct edges)
  const pairs = [];
  for (let d = 0; d < sigma.length; d++) { const a = d >> 1, b = sigma[d] >> 1; if (a !== b) pairs.push([a, b]); }
  const triples = pm.edgeRuns(sigma, VARIANT, 3)[3];
  return { vert, nv, fs, m, eu, ev, ef, eg, pairs, triples, nf: fs.length };
}

function bipartiteN(I, Nmask) { // is M[N] bipartite (ignoring self-adjacency)
  const col = new Int8Array(I.m).fill(-1);
  const adj = Array.from({ length: I.m }, () => []);
  for (const [a, b] of I.pairs) if ((Nmask >> a & 1) && (Nmask >> b & 1)) { adj[a].push(b); adj[b].push(a); }
  for (let s = 0; s < I.m; s++) {
    if (!(Nmask >> s & 1) || col[s] >= 0) continue;
    col[s] = 0; const st = [s];
    while (st.length) { const x = st.pop(); for (const y of adj[x]) { if (col[y] < 0) { col[y] = 1 - col[x]; st.push(y); } else if (col[y] === col[x]) return false; } }
  }
  return true;
}

function parityValid(I, Smask, sigma) {
  // nodes: vertices 0..nv-1, faces nv..nv+nf-1 ; weights: number of corners that join two distinct edges
  const nn = I.nv + I.nf;
  const par = new Int32Array(nn).map((_, i) => i);
  const find = (x) => { while (par[x] !== x) { par[x] = par[par[x]]; x = par[x]; } return x; };
  const uni = (a, b) => { a = find(a); b = find(b); if (a !== b) par[a] = b; };
  for (let e = 0; e < I.m; e++) if (Smask >> e & 1) { uni(I.eu[e], I.ev[e]); uni(I.eu[e], I.nv + I.ef[e]); uni(I.eu[e], I.nv + I.eg[e]); }
  const w = new Int32Array(nn);
  // every corner (dart d, sigma[d]) between distinct edges is an edge of M between vertex node and face node
  // count per node the corners whose two edges are distinct
  const fidx = new Int32Array(sigma.length);
  I.fs.forEach((wk, i) => { for (const d of wk) fidx[d] = i; });
  for (let d = 0; d < sigma.length; d++) {
    const a = d >> 1, b = sigma[d] >> 1;
    if (a === b) continue;
    w[I.vert[d]]++; w[I.nv + fidx[sigma[d]]]++;
  }
  const sum = new Int32Array(nn);
  for (let x = 0; x < nn; x++) sum[find(x)] += w[x];
  for (let x = 0; x < nn; x++) if (find(x) === x && (sum[x] & 1)) return false;
  return true;
}

function sparse(I, Smask) { for (const t of I.triples) if ((Smask >> t[0] & 1) && (Smask >> t[1] & 1) && (Smask >> t[2] & 1)) return false; return true; }

function isForest(I, Nmask) {
  const par = new Int32Array(I.nv).map((_, i) => i);
  const find = (x) => { while (par[x] !== x) { par[x] = par[par[x]]; x = par[x]; } return x; };
  for (let e = 0; e < I.m; e++) if (Nmask >> e & 1) { const a = find(I.eu[e]), b = find(I.ev[e]); if (a === b) return false; par[a] = b; }
  return true;
}

let level = new Map();
for (const s of [Int32Array.from([0, 1]), Int32Array.from([1, 0])]) level.set(pm.canonKey(s), s);
const res = {};
function bump(k, m) { if (!res[k]) res[k] = {}; res[k][m] = (res[k][m] || 0) + 1; }
let parityMismatch = 0;
const exST = [];
function check(sigma) {
  const I = info(sigma);
  const m = I.m;
  const full = (1 << m) - 1;
  const deg = new Int32Array(I.nv);
  for (let e = 0; e < m; e++) { deg[I.eu[e]]++; deg[I.ev[e]]++; }
  let bridgeless = true, loopless = true;
  for (let e = 0; e < m; e++) { if (I.ef[e] === I.eg[e]) bridgeless = false; if (I.eu[e] === I.ev[e]) loopless = false; }
  let col = false, forest = false;
  for (let S = 0; S <= full; S++) {
    const N = full & ~S;
    const bip = bipartiteN(I, N);
    if (m <= 7) { if (bip !== parityValid(I, S, sigma)) parityMismatch++; }
    if (!bip || !sparse(I, S)) continue;
    col = true;
    if (!forest && isForest(I, N)) {
      // no odd vertex N-full
      let ok = true;
      for (let v = 0; v < I.nv && ok; v++) if (deg[v] & 1) { let fullv = true; for (let e = 0; e < m; e++) if ((I.eu[e] === v || I.ev[e] === v) && (S >> e & 1)) fullv = false; if (fullv && deg[v] > 1) ok = false; }
      if (ok) forest = true;
    }
  }
  // product construction
  let st = false;
  const nn = I.nv + I.nf;
  for (let chi = 0; chi < (1 << (nn - 1)) && !st; chi++) {
    let S = 0;
    for (let e = 0; e < m; e++) {
      const bi = ((chi >> I.eu[e] & 1) !== (chi >> I.ev[e] & 1)) && ((chi >> (I.nv + I.ef[e]) & 1) !== (chi >> (I.nv + I.eg[e]) & 1));
      if (!bi) S |= 1 << e;
    }
    if (sparse(I, S)) st = true;
  }
  bump('all', m);
  if (!col) bump('NOT [1,1,2]', m);
  if (!forest) bump('no forest N', m);
  if (!st) bump('no product', m);
  if (bridgeless && loopless) { bump('bridgeless loopless', m); if (!st) { bump('bridgeless loopless: no product', m); if (exST.length < 3) exST.push(pm.describe(sigma)); } if (!forest) bump('bridgeless loopless: no forest N', m); }
}
for (const s of level.values()) check(s);
const t0 = Date.now();
for (let m = 2; m <= MAXM; m++) {
  const next = new Map();
  for (const g of level.values()) for (const h of pm.childrenAll(g)) { const key = pm.canonKey(h); if (!next.has(key)) { next.set(key, h); check(h); } }
  console.log(`m=${m}: ${next.size} maps, ${((Date.now() - t0) / 1000).toFixed(1)} s`);
  level = next;
}
console.log('variant', VARIANT, 'parity criterion mismatches (m<=7):', parityMismatch);
for (const k of Object.keys(res)) console.log('  ', k, JSON.stringify(res[k]));
for (const x of exST) console.log('EX no product:', x);
