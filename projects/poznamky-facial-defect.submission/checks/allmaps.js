'use strict';
// Exhaustive check of facial-defect colorings on all connected plane maps with at most MAXM edges.
const pm = require('./pm.js');
const MAXM = parseInt(process.argv[2] || '7', 10);
const KEEP = parseInt(process.argv[3] || String(MAXM), 10); // last level whose maps are stored

// lists to test; each: name, kind, defects, variant
const TESTS = [
  ['E[1,1,1]', 'e', [1, 1, 1]], ['E[1,1,2]', 'e', [1, 1, 2]], ['E[1,2,2]', 'e', [1, 2, 2]],
  ['E[1,1]', 'e', [1, 1]], ['E[1,2]', 'e', [1, 2]], ['E[2,2]', 'e', [2, 2]], ['E[1,3]', 'e', [1, 3]], ['E[1,4]', 'e', [1, 4]],
  ['E[2,3]', 'e', [2, 3]], ['E[3,3]', 'e', [3, 3]],
  ['V[1,1,1]', 'v', [1, 1, 1]], ['V[1,1,2]', 'v', [1, 1, 2]], ['V[1,2,2]', 'v', [1, 2, 2]], ['V[2,2,2]', 'v', [2, 2, 2]],
  ['V[2,2]', 'v', [2, 2]], ['V[1,3]', 'v', [1, 3]], ['V[2,3]', 'v', [2, 3]], ['V[3,3]', 'v', [3, 3]], ['V[1,4]', 'v', [1, 4]],
  ['T[1,1,1,1,1]', 't', [1, 1, 1, 1, 1]], ['T[1,1,1,1,2]', 't', [1, 1, 1, 1, 2]], ['T[1,1,1,2,2]', 't', [1, 1, 1, 2, 2]],
];
const stats = {};
const examples = {};
function record(name, variant, m, sigma) {
  const key = name + (variant ? ' ' + variant : '');
  if (!stats[key]) stats[key] = {};
  stats[key][m] = (stats[key][m] || 0) + 1;
  if (!examples[key]) examples[key] = [];
  if (examples[key].length < 3) examples[key].push(pm.describe(sigma));
}
function check(sigma) {
  const m = sigma.length / 2;
  for (const [name, kind, defects] of TESTS) {
    if (kind === 'e') {
      for (const variant of ['P', 'W']) if (pm.edgeColoring(sigma, defects, variant) === null) record(name, variant, m, sigma);
    } else if (kind === 'v') {
      if (pm.vertexColoring(sigma, defects) === null) record(name, '', m, sigma);
    } else {
      for (const variant of ['P', 'W']) if (pm.totalColoring(sigma, defects, variant) === null) record(name, variant, m, sigma);
    }
  }
}

let level = new Map();
for (const s of [Int32Array.from([0, 1]), Int32Array.from([1, 0])]) level.set(pm.canonKey(s), s);
const counts = { 1: level.size };
for (const s of level.values()) check(s);
const t0 = Date.now();
for (let m = 2; m <= MAXM; m++) {
  const store = m <= KEEP;
  const next = store ? new Map() : new Set();
  let cnt = 0;
  for (const g of level.values()) {
    for (const h of pm.childrenAll(g)) {
      const key = pm.canonKey(h);
      if (next.has(key)) continue;
      if (store) next.set(key, h); else next.add(key);
      cnt++;
      check(h);
    }
  }
  counts[m] = cnt;
  console.log(`m=${m}: ${cnt} maps, ${((Date.now() - t0) / 1000).toFixed(1)} s`);
  if (!store) break;
  level = next;
}
console.log('counts', JSON.stringify(counts));
console.log('NOT colorable (number of maps per m):');
for (const key of Object.keys(stats)) console.log('  ', key, JSON.stringify(stats[key]));
for (const key of Object.keys(examples)) console.log('EX', key, examples[key][0]);
