'use strict';
// All 3-connected simple plane graphs (polyhedra) with at most MAXM edges, by Tutte's theorem:
// every 3-connected graph other than a wheel arises from a smaller 3-connected graph by adding an edge
// or by splitting a vertex. Checks facial-defect colorings on each.
const pm = require('./pm.js');
const MAXM = parseInt(process.argv[2] || '14', 10);
const MODE = process.argv[3] || 'full';

const TESTS_FULL = [
  ['E[1,1,1]', 'e', [1, 1, 1]], ['E[1,1,2]', 'e', [1, 1, 2]], ['E[1,2,2]', 'e', [1, 2, 2]],
  ['E[1,2]', 'e', [1, 2]], ['E[2,2]', 'e', [2, 2]], ['E[1,3]', 'e', [1, 3]], ['E[2,3]', 'e', [2, 3]], ['E[3,3]', 'e', [3, 3]], ['E[1,4]', 'e', [1, 4]],
  ['V[1,1,2]', 'v', [1, 1, 2]], ['V[1,2,2]', 'v', [1, 2, 2]], ['V[2,2,2]', 'v', [2, 2, 2]],
  ['V[2,2]', 'v', [2, 2]], ['V[1,3]', 'v', [1, 3]], ['V[2,3]', 'v', [2, 3]], ['V[3,3]', 'v', [3, 3]], ['V[1,4]', 'v', [1, 4]],
  ['T[1,1,1,1,1]', 't', [1, 1, 1, 1, 1]], ['T[1,1,1,1,2]', 't', [1, 1, 1, 1, 2]], ['T[1,1,1,2,2]', 't', [1, 1, 1, 2, 2]],
];
const TESTS_MAIN = [
  ['E[1,1,2]', 'e', [1, 1, 2]], ['E[2,2]', 'e', [2, 2]], ['E[1,3]', 'e', [1, 3]],
  ['V[1,1,2]', 'v', [1, 1, 2]], ['V[1,2,2]', 'v', [1, 2, 2]], ['V[3,3]', 'v', [3, 3]], ['V[2,3]', 'v', [2, 3]], ['V[1,3]', 'v', [1, 3]],
];
const TESTS = MODE === 'full' ? TESTS_FULL : TESTS_MAIN;
const stats = {}, examples = {};
function record(name, variant, m, sigma) {
  const key = name + (variant ? ' ' + variant : '');
  if (!stats[key]) stats[key] = {};
  stats[key][m] = (stats[key][m] || 0) + 1;
  if (!examples[key]) examples[key] = [];
  if (examples[key].length < 2) examples[key].push(pm.describe(sigma));
}
function check(sigma) {
  const m = sigma.length / 2;
  for (const [name, kind, defects] of TESTS) {
    if (kind === 'e') {
      // W is the stronger requirement: test W first, P only if W fails
      if (pm.edgeColoring(sigma, defects, 'W') === null) {
        record(name, 'W', m, sigma);
        if (pm.edgeColoring(sigma, defects, 'P') === null) record(name, 'P', m, sigma);
      }
    } else if (kind === 'v') {
      if (pm.vertexColoring(sigma, defects) === null) record(name, '', m, sigma);
    } else {
      if (pm.totalColoring(sigma, defects, 'W') === null) {
        record(name, 'W', m, sigma);
        if (pm.totalColoring(sigma, defects, 'P') === null) record(name, 'P', m, sigma);
      }
    }
  }
}
function euler(s) { return pm.vertices(s).nv - s.length / 2 + pm.faces(s).length; }

let level = new Map();
const t0 = Date.now();
const counts = {};
for (let m = 6; m <= MAXM; m++) {
  const next = new Map();
  if (m % 2 === 0) {
    const w = pm.wheel(m / 2);
    if (euler(w) !== 2) throw new Error('wheel not planar');
    next.set(pm.canonKey(w), w);
  }
  for (const g of level.values()) {
    for (const h of pm.childrenPoly(g)) {
      if (!pm.isSimple3Plausible(h)) continue;
      const key = pm.canonKey(h);
      if (next.has(key)) continue;
      if (!pm.is3Connected(h)) continue;
      next.set(key, h);
    }
  }
  for (const h of next.values()) check(h);
  counts[m] = next.size;
  console.log(`m=${m}: ${next.size} polyhedra, ${((Date.now() - t0) / 1000).toFixed(1)} s`);
  level = next;
}
console.log('counts', JSON.stringify(counts));
console.log('NOT colorable (number of polyhedra per m):');
for (const key of Object.keys(stats)) console.log('  ', key, JSON.stringify(stats[key]));
for (const key of Object.keys(examples)) console.log('EX', key, examples[key][0]);
