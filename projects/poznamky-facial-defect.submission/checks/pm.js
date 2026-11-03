'use strict';
// Plane maps as rotation systems; generation; facial-defect colorings.
// Edge i has darts 2i and 2i+1 (alpha(d) = d ^ 1). sigma[d] = next dart around the origin of d.
// phi(d) = sigma[d ^ 1] = next dart on the boundary walk of the face of d.

function vertices(sigma) {
  const n = sigma.length;
  const vert = new Int32Array(n).fill(-1);
  let nv = 0;
  for (let d = 0; d < n; d++) {
    if (vert[d] < 0) {
      let x = d;
      while (vert[x] < 0) { vert[x] = nv; x = sigma[x]; }
      nv++;
    }
  }
  return { vert, nv };
}

function faces(sigma) {
  const n = sigma.length;
  const seen = new Uint8Array(n);
  const out = [];
  for (let d = 0; d < n; d++) {
    if (!seen[d]) {
      const walk = [];
      let x = d;
      while (!seen[x]) { seen[x] = 1; walk.push(x); x = sigma[x ^ 1]; }
      out.push(walk);
    }
  }
  return out;
}

// canonical key up to orientation-preserving and -reversing isomorphism
function canonKey(sigma) {
  const n = sigma.length;
  const inv = new Int32Array(n);
  for (let d = 0; d < n; d++) inv[sigma[d]] = d;
  let best = null;
  const label = new Int32Array(n);
  const order = new Int32Array(n);
  const code = new Int32Array(2 * n);
  for (let o = 0; o < 2; o++) {
    const s = o === 0 ? sigma : inv;
    for (let root = 0; root < n; root++) {
      label.fill(-1);
      order[0] = root; label[root] = 0;
      let cnt = 1, i = 0, k = 0, cmp = 0; // cmp: 0 equal so far, -1 smaller than best
      let worse = false;
      while (i < cnt) {
        const x = order[i++];
        let y = s[x];
        if (label[y] < 0) { label[y] = cnt; order[cnt++] = y; }
        code[k] = label[y];
        if (best !== null && cmp === 0) {
          if (code[k] < best[k]) cmp = -1; else if (code[k] > best[k]) { worse = true; break; }
        }
        k++;
        y = x ^ 1;
        if (label[y] < 0) { label[y] = cnt; order[cnt++] = y; }
        code[k] = label[y];
        if (best !== null && cmp === 0) {
          if (code[k] < best[k]) cmp = -1; else if (code[k] > best[k]) { worse = true; break; }
        }
        k++;
      }
      if (worse) continue;
      if (best === null || cmp < 0) best = Int32Array.from(code);
    }
  }
  let str = '';
  for (let i = 0; i < best.length; i++) str += String.fromCharCode(48 + best[i]);
  return str;
}

function addPendant(sigma, d) {
  const n = sigma.length;
  const s = new Int32Array(n + 2);
  s.set(sigma);
  s[n] = s[d]; s[d] = n; s[n + 1] = n + 1;
  return s;
}

function addChord(sigma, d1, d2) {
  const n = sigma.length;
  const s = new Int32Array(n + 2);
  s.set(sigma);
  const a = n, b = n + 1;
  if (d1 === d2) { const nx = s[d1]; s[d1] = a; s[a] = b; s[b] = nx; }
  else { s[a] = s[d1]; s[d1] = a; s[b] = s[d2]; s[d2] = b; }
  return s;
}

function cornerFace(sigma) {
  const n = sigma.length;
  const fidx = new Int32Array(n);
  const fs = faces(sigma);
  for (let i = 0; i < fs.length; i++) for (const x of fs[i]) fidx[x] = i;
  const cf = new Int32Array(n);
  for (let d = 0; d < n; d++) cf[d] = fidx[sigma[d]];
  return cf;
}

// all maps with one more edge
function* childrenAll(sigma) {
  const n = sigma.length;
  for (let d = 0; d < n; d++) yield addPendant(sigma, d);
  const cf = cornerFace(sigma);
  for (let d1 = 0; d1 < n; d1++) for (let d2 = d1; d2 < n; d2++) if (cf[d1] === cf[d2]) yield addChord(sigma, d1, d2);
}

// ---------------------------------------------------------------- polyhedra (Tutte)
function wheel(k) { // hub 0, rim 1..k ; edges: spokes i (hub-rim i), rim edges
  // darts: spoke i: 2i (at hub), 2i+1 (at rim i); rim edge i (rim i -> rim i+1): 2(k+i) at rim i, 2(k+i)+1 at rim i+1
  const s = new Int32Array(4 * k);
  for (let i = 0; i < k; i++) {
    s[2 * i] = 2 * ((i + 1) % k);                 // around hub
    const sp = 2 * i + 1, out = 2 * (k + i), inn = 2 * (k + (i + k - 1) % k) + 1;
    // around rim vertex i: spoke, rim edge to i+1 ... orientation: hub ccw i -> i+1 means at rim i: (to i-1), spoke, (to i+1) clockwise
    s[sp] = inn; s[inn] = out; s[out] = sp;
  }
  return s;
}

function isSimple3Plausible(sigma) { // simple graph and min degree >= 3
  const { vert, nv } = vertices(sigma);
  const n = sigma.length;
  const deg = new Int32Array(nv);
  const seen = new Set();
  for (let d = 0; d < n; d += 2) {
    const u = vert[d], v = vert[d + 1];
    if (u === v) return false;
    const key = u < v ? u * 65536 + v : v * 65536 + u;
    if (seen.has(key)) return false;
    seen.add(key);
    deg[u]++; deg[v]++;
  }
  for (let v = 0; v < nv; v++) if (deg[v] < 3) return false;
  return true;
}

// 3-connected check for small simple graphs: remove every pair of vertices, test connectivity
function is3Connected(sigma) {
  const { vert, nv } = vertices(sigma);
  if (nv < 4) return false;
  const n = sigma.length;
  const adj = Array.from({ length: nv }, () => []);
  for (let d = 0; d < n; d += 2) { adj[vert[d]].push(vert[d + 1]); adj[vert[d + 1]].push(vert[d]); }
  const mark = new Int32Array(nv);
  let stamp = 0;
  const stack = new Int32Array(nv);
  for (let a = 0; a < nv; a++) for (let b = a + 1; b < nv; b++) {
    stamp++;
    mark[a] = stamp; mark[b] = stamp;
    let s0 = 0; while (s0 === a || s0 === b) s0++;
    let top = 0, cnt = 1; stack[top++] = s0; mark[s0] = stamp;
    while (top > 0) {
      const x = stack[--top];
      for (const y of adj[x]) if (mark[y] !== stamp) { mark[y] = stamp; cnt++; stack[top++] = y; }
    }
    if (cnt !== nv - 2) return false;
  }
  return true;
}

// children for the polyhedral closure: add an edge inside a face between non-consecutive corners;
// split a vertex of degree >= 4 into two adjacent vertices of degree >= 3.
function* childrenPoly(sigma) {
  const n = sigma.length;
  const cf = cornerFace(sigma);
  const { vert } = vertices(sigma);
  for (let d1 = 0; d1 < n; d1++) for (let d2 = d1 + 1; d2 < n; d2++) {
    if (cf[d1] !== cf[d2] || vert[d1] === vert[d2]) continue;
    yield addChord(sigma, d1, d2);
  }
  // vertex split: vertex with rotation x0..x_{k-1}; choose arc x_i..x_{j} (length >= 2, rest >= 2)
  const seenV = new Set();
  for (let d = 0; d < n; d++) {
    const v = vert[d];
    if (seenV.has(v)) continue;
    seenV.add(v);
    const rot = [];
    let x = d;
    do { rot.push(x); x = sigma[x]; } while (x !== d);
    const k = rot.length;
    if (k < 4) continue;
    for (let i = 0; i < k; i++) for (let len = 2; len <= k - 2; len++) {
      const j = (i + len - 1) % k; // arc rot[i..j] goes to the new vertex
      if (len * 2 === k && i >= k / 2) continue; // symmetric duplicate
      const s = new Int32Array(n + 2);
      s.set(sigma);
      const a = n, b = n + 1; // a stays at old vertex, b at new vertex
      const before = rot[(i + k - 1) % k], after = rot[(j + 1) % k];
      // old vertex: ... before, a, after ...
      s[before] = a; s[a] = after;
      // new vertex: rot[i] ... rot[j], b
      s[rot[j]] = b; s[b] = rot[i];
      yield s;
    }
  }
}

// ---------------------------------------------------------------- constraints
// runs of k consecutive edges on boundary walks. variant 'P': path (k+1 distinct vertices), 'W': k distinct edges.
function edgeRuns(sigma, variant, maxk) {
  const { vert } = vertices(sigma);
  const fs = faces(sigma);
  const runs = {};
  for (let k = 2; k <= maxk; k++) {
    const S = new Map();
    for (const walk of fs) {
      const L = walk.length;
      for (let i = 0; i < L; i++) {
        const es = [];
        let ok = true;
        const vs = [];
        for (let j = 0; j < k; j++) {
          const d = walk[(i + j) % L];
          const e = d >> 1;
          if (es.includes(e)) { ok = false; break; }
          es.push(e);
          vs.push(vert[d]);
          if (j === k - 1) vs.push(vert[d ^ 1]);
        }
        if (!ok) continue;
        if (variant === 'P' && k >= 3) { if (new Set(vs).size < k + 1) continue; }
        const r = es.slice().reverse();
        let t = es;
        for (let q = 0; q < k; q++) { if (r[q] < es[q]) { t = r; break; } if (r[q] > es[q]) break; }
        S.set(t.join(','), t);
      }
    }
    runs[k] = Array.from(S.values());
  }
  return runs;
}

function vertexRuns(sigma, maxk) {
  const { vert } = vertices(sigma);
  const fs = faces(sigma);
  const runs = {};
  for (let k = 2; k <= maxk; k++) {
    const S = new Map();
    for (const walk of fs) {
      const L = walk.length;
      for (let i = 0; i < L; i++) {
        const vs = [];
        let ok = true;
        for (let j = 0; j < k; j++) {
          const v = vert[walk[(i + j) % L]];
          if (vs.includes(v)) { ok = false; break; }
          vs.push(v);
        }
        if (!ok) continue;
        const r = vs.slice().reverse();
        let t = vs;
        for (let q = 0; q < k; q++) { if (r[q] < vs[q]) { t = r; break; } if (r[q] > vs[q]) break; }
        S.set(t.join(','), t);
      }
    }
    runs[k] = Array.from(S.values());
  }
  return runs;
}

// generic solver. cons: array of {c: color, t: array of vars} meaning "not all of t have color c".
function solveCSP(nvars, ncol, cons, fixed) {
  const watch = new Array(nvars * ncol);
  for (let i = 0; i < watch.length; i++) watch[i] = [];
  for (let ci = 0; ci < cons.length; ci++) { const { c, t } = cons[ci]; for (const v of t) watch[v * ncol + c].push(ci); }
  const full = (1 << ncol) - 1;
  const dom = new Int32Array(nvars).fill(full);
  if (fixed) for (const [v, mask] of fixed) dom[v] &= mask;
  for (let v = 0; v < nvars; v++) if (dom[v] === 0) return null;
  const trailV = [], trailD = [];
  const isSingle = (x) => (x & (x - 1)) === 0;
  const colorOf = (x) => 31 - Math.clz32(x);
  function propagate(queue) {
    while (queue.length) {
      const v = queue.pop();
      const bit = dom[v], c = colorOf(bit);
      const ws = watch[v * ncol + c];
      for (let wi = 0; wi < ws.length; wi++) {
        const t = cons[ws[wi]].t;
        let nfree = 0, free = -1;
        for (let q = 0; q < t.length; q++) { const w = t[q]; if (dom[w] !== bit) { nfree++; free = w; if (nfree > 1) break; } }
        if (nfree === 0) return false;
        if (nfree === 1 && (dom[free] & bit)) {
          trailV.push(free); trailD.push(dom[free]);
          dom[free] &= ~bit;
          if (dom[free] === 0) return false;
          if (isSingle(dom[free])) queue.push(free);
        }
      }
    }
    return true;
  }
  function popc(x) { let c = 0; while (x) { x &= x - 1; c++; } return c; }
  function rec() {
    let best = -1, bs = 99;
    for (let v = 0; v < nvars; v++) { const x = dom[v]; if (!isSingle(x)) { const s = popc(x); if (s < bs) { bs = s; best = v; if (s === 2) break; } } }
    if (best < 0) return true;
    const d0 = dom[best];
    for (let c = 0; c < ncol; c++) if (d0 & (1 << c)) {
      const mark = trailV.length;
      trailV.push(best); trailD.push(dom[best]);
      dom[best] = 1 << c;
      if (propagate([best]) && rec()) return true;
      while (trailV.length > mark) { dom[trailV.pop()] = trailD.pop(); }
    }
    return false;
  }
  const init = [];
  for (let v = 0; v < nvars; v++) if (isSingle(dom[v])) init.push(v);
  if (!propagate(init)) return null;
  if (!rec()) return null;
  const col = new Array(nvars);
  for (let v = 0; v < nvars; v++) col[v] = colorOf(dom[v]);
  return col;
}

function consFromRuns(runs, defects, offset) {
  const cons = [];
  for (let c = 0; c < defects.length; c++) {
    const k = defects[c] + 1;
    for (const t of runs[k]) cons.push({ c, t: offset ? t.map((x) => x + offset) : t });
  }
  return cons;
}

function edgeColoring(sigma, defects, variant, fixed) {
  const maxk = Math.max(...defects) + 1;
  const runs = edgeRuns(sigma, variant, maxk);
  return solveCSP(sigma.length / 2, defects.length, consFromRuns(runs, defects, 0), fixed);
}

function vertexColoring(sigma, defects, fixed) {
  const maxk = Math.max(...defects) + 1;
  const runs = vertexRuns(sigma, maxk);
  const { nv } = vertices(sigma);
  return solveCSP(nv, defects.length, consFromRuns(runs, defects, 0), fixed);
}

// total coloring, type-wise definition: vertex runs, edge runs, and incident elements always differ.
// variables: vertices 0..nv-1, edges nv..nv+m-1
function totalColoring(sigma, defects, variant) {
  const maxk = Math.max(...defects) + 1;
  const { vert, nv } = vertices(sigma);
  const vr = vertexRuns(sigma, maxk), er = edgeRuns(sigma, variant, maxk);
  const cons = consFromRuns(vr, defects, 0).concat(consFromRuns(er, defects, nv));
  const m = sigma.length / 2;
  for (let e = 0; e < m; e++) {
    const u = vert[2 * e], v = vert[2 * e + 1];
    for (let c = 0; c < defects.length; c++) {
      cons.push({ c, t: [u, nv + e] });
      if (v !== u) cons.push({ c, t: [v, nv + e] });
    }
  }
  return solveCSP(nv + m, defects.length, cons, null);
}

function describe(sigma) {
  const { vert, nv } = vertices(sigma);
  const m = sigma.length / 2;
  const edges = [];
  for (let e = 0; e < m; e++) edges.push([vert[2 * e], vert[2 * e + 1]]);
  const fs = faces(sigma).map((w) => w.map((d) => vert[d]));
  const rot = {};
  for (let d = 0; d < sigma.length; d++) {
    const v = vert[d];
    if (rot[v]) continue;
    const cyc = []; let x = d;
    do { cyc.push(vert[x ^ 1]); x = sigma[x]; } while (x !== d);
    rot[v] = cyc;
  }
  return JSON.stringify({ n: nv, m, edges, faces: fs, rotation: rot, sigma: Array.from(sigma) });
}

module.exports = {
  vertices, faces, canonKey, addPendant, addChord, childrenAll, childrenPoly, wheel, isSimple3Plausible, is3Connected,
  edgeRuns, vertexRuns, solveCSP, consFromRuns, edgeColoring, vertexColoring, totalColoring, describe, cornerFace,
};
