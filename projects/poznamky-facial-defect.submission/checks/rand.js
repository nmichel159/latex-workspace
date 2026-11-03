'use strict';
// Random plane maps (grown by pendant edges and chords), tested for facial-defect colorings.
const pm = require('./pm.js');
const SEED = parseInt(process.argv[2] || '1', 10);
const COUNT = parseInt(process.argv[3] || '10000', 10);
const MMIN = parseInt(process.argv[4] || '12', 10);
const MMAX = parseInt(process.argv[5] || '40', 10);
const MODE = process.argv[6] || 'simple'; // simple | multi

let state = SEED >>> 0;
function rnd() { // mulberry32
  state = (state + 0x6D2B79F5) >>> 0;
  let t = state;
  t = Math.imul(t ^ (t >>> 15), t | 1);
  t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
  return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
}
const ri = (n) => Math.floor(rnd() * n);

function randomMap(m, pPend, maxFace) {
  let s = Int32Array.from([0, 1]);
  while (s.length / 2 < m) {
    const n = s.length;
    if (rnd() < pPend) { s = pm.addPendant(s, ri(n)); continue; }
    const fs = pm.faces(s);
    const { vert } = pm.vertices(s);
    const w = fs[ri(fs.length)];
    if (w.length < 2) continue;
    // corners of the face w: corner after dart d belongs to face of sigma[d]; darts x in w leave vertex vert[x];
    // the corner before x at its origin is the corner after inv(x); use dart x^1's successor relation: corner after (prev ^ 1)
    const i = ri(w.length);
    let j = ri(w.length);
    if (maxFace) { const off = 2 + ri(Math.min(maxFace, w.length - 1)); j = (i + off) % w.length; }
    if (i === j && MODE === 'simple') continue;
    // corner at origin of w[i] inside this face: between dart (w[i-1]^1) and w[i]
    const d1 = w[(i + w.length - 1) % w.length] ^ 1, d2 = w[(j + w.length - 1) % w.length] ^ 1;
    if (MODE === 'simple') {
      const u = vert[w[i]], v = vert[w[j]];
      if (u === v) continue;
      let dup = false;
      for (let d = 0; d < n; d += 2) if ((vert[d] === u && vert[d + 1] === v) || (vert[d] === v && vert[d + 1] === u)) { dup = true; break; }
      if (dup) continue;
    }
    s = pm.addChord(s, d1, d2);
  }
  return s;
}

const TESTS = [
  ['E[1,1,2] W', (s) => pm.edgeColoring(s, [1, 1, 2], 'W')],
  ['V[1,1,2]', (s) => pm.vertexColoring(s, [1, 1, 2])],
  ['V[1,2,2]', (s) => pm.vertexColoring(s, [1, 2, 2])],
  ['E[2,3] W', (s) => pm.edgeColoring(s, [2, 3], 'W')],
  ['E[3,3] W', (s) => pm.edgeColoring(s, [3, 3], 'W')],
  ['V[3,3]', (s) => pm.vertexColoring(s, [3, 3])],
  ['V[2,3]', (s) => pm.vertexColoring(s, [2, 3])],
  ['T[1,1,1,1,2] W', (s) => pm.totalColoring(s, [1, 1, 1, 1, 2], 'W')],
];
const fails = {};
const t0 = Date.now();
let not111 = 0;
for (let it = 0; it < COUNT; it++) {
  const m = MMIN + ri(MMAX - MMIN + 1);
  const pPend = [0.05, 0.15, 0.3, 0.45][ri(4)];
  const maxFace = [0, 0, 2, 3, 4][ri(5)];
  const s = randomMap(m, pPend, maxFace);
  if (pm.vertices(s).nv - s.length / 2 + pm.faces(s).length !== 2) throw new Error('not planar');
  if (pm.edgeColoring(s, [1, 1, 1], 'W') === null) not111++;
  for (const [name, f] of TESTS) {
    if (f(s) === null) {
      fails[name] = (fails[name] || 0) + 1;
      if (fails[name] <= 2) console.log('FAIL', name, pm.describe(s));
    }
  }
}
console.log(`seed ${SEED} mode ${MODE}: ${COUNT} maps with ${MMIN}..${MMAX} edges, ${((Date.now() - t0) / 1000).toFixed(0)} s; not E[1,1,1]: ${not111}; fails: ${JSON.stringify(fails)}`);
