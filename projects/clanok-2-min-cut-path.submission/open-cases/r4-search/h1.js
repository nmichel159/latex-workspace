// Theorem H search with t = 1 (dc-hardness.md), a port of dc-hardness/helly2ch.py (search, helly_solve) with the
// same semantics, written for speed (agent r4-search).  The BFS over states (side, parity, stored set) is run per
// stored set with bit-mask closures over sides.
// Input: JSON lines {"N":..,"E":[[nodes]],"F":[[nodes]],"s":..,"t":..}; output: JSON lines {"h1":bool,"phi":[..]}.
// Limit: at most 30 sides (non-empty E- and F-sides together).
'use strict';
const readline = require('readline');

function popcount(x) {
  x = x - ((x >>> 1) & 0x55555555);
  x = (x & 0x33333333) + ((x >>> 2) & 0x33333333);
  return (((x + (x >>> 4)) & 0x0F0F0F0F) * 0x01010101) >>> 24;
}

function solve(inst) {
  const N = inst.N, s = inst.s, t = inst.t;
  const n = inst.E.length;
  // sides in the order of helly2ch.sides_list
  const sides = [];
  for (let w = 0; w < n; w++) {
    if (inst.E[w].length) sides.push({ w: w, typ: 0, nodes: inst.E[w], partner: inst.F[w] });
    if (inst.F[w].length) sides.push({ w: w, typ: 1, nodes: inst.F[w], partner: inst.E[w] });
  }
  const S = sides.length;
  if (S > 30) throw new Error('too many sides');
  const SW = new Array(N).fill(0);   // sides containing node x
  const PH = new Array(N).fill(0);   // sides whose partner contains x
  let PE = 0;                        // sides with empty partner
  const typeMask = [0, 0];
  for (let i = 0; i < S; i++) {
    for (const x of sides[i].nodes) SW[x] |= (1 << i);
    for (const x of sides[i].partner) PH[x] |= (1 << i);
    if (sides[i].partner.length === 0) PE |= (1 << i);
    typeMask[sides[i].typ] |= (1 << i);
  }
  const nb = new Array(S).fill(0);
  const other = new Array(S).fill(0);
  for (let i = 0; i < S; i++) {
    for (let j = 0; j < S; j++) {
      const a = new Set(sides[i].nodes);
      if (sides[j].nodes.some(x => a.has(x))) nb[i] |= (1 << j);
      if (j !== i && sides[j].w === sides[i].w) other[i] |= (1 << j);
    }
  }
  const start = SW[s], goal = SW[t];
  const choices = [-1];
  for (let x = 0; x < N; x++) choices.push(x);
  // allowed contribution of group (typ, par) with phi = c
  function A(typ, c) { return (c < 0 ? PE : (PE | PH[c])) & typeMask[typ]; }
  function nbrUnion(F) {
    let r = 0;
    while (F) { const low = F & -F; const i = 31 - Math.clz32(low); r |= nb[i]; F ^= low; }
    return r;
  }
  function relaxed(al0, al1) {
    let V0 = 0, V1 = 0, F0 = 0, F1 = start & al1;
    while (F0 | F1) {
      V0 |= F0; V1 |= F1;
      if ((F0 | F1) & goal) return true;
      const n1 = nbrUnion(F0) & al1 & ~V1;
      const n0 = nbrUnion(F1) & al0 & ~V0;
      F0 = n0; F1 = n1;
    }
    return false;
  }
  function full(al0, al1, phiNodes) {
    let storing = 0;
    for (const x of phiNodes) storing |= SW[x];
    function add(j, St) {
      if (!((storing >>> j) & 1)) return St;
      if ((St >>> j) & 1) return St;
      if (St & other[j]) return -1;
      const nst = (St | (1 << j));
      for (const x of phiNodes) if (popcount(nst & SW[x]) > 2) return -1;
      return nst;
    }
    const vis = new Map();
    const queue = [];
    function seed(St, f0, f1) { queue.push([St, f0, f1]); }
    let st0 = start & al1;
    while (st0) {
      const low = st0 & -st0; const i = 31 - Math.clz32(low); st0 ^= low;
      const st = add(i, 0);
      if (st >= 0) seed(st, 0, (1 << i));
    }
    while (queue.length) {
      const [St, s0, s1] = queue.pop();
      let V = vis.get(St);
      if (!V) { V = [0, 0]; vis.set(St, V); }
      let F0 = s0 & ~V[0], F1 = s1 & ~V[1];
      const keep = (~storing) | St;
      while (F0 | F1) {
        V[0] |= F0; V[1] |= F1;
        if ((F0 | F1) & goal) return true;
        const n0src = nbrUnion(F0);   // next at parity 1
        const n1src = nbrUnion(F1);   // next at parity 0
        const newF1 = n0src & al1 & keep & ~V[1];
        const newF0 = n1src & al0 & keep & ~V[0];
        let ch1 = n0src & al1 & storing & ~St;
        while (ch1) {
          const low = ch1 & -ch1; const j = 31 - Math.clz32(low); ch1 ^= low;
          const st2 = add(j, St);
          if (st2 >= 0) seed(st2, 0, (1 << j));
        }
        let ch0 = n1src & al0 & storing & ~St;
        while (ch0) {
          const low = ch0 & -ch0; const j = 31 - Math.clz32(low); ch0 ^= low;
          const st2 = add(j, St);
          if (st2 >= 0) seed(st2, (1 << j), 0);
        }
        F0 = newF0; F1 = newF1;
      }
    }
    return false;
  }
  // groups order as helly2ch: (0,0),(0,1),(1,0),(1,1) = (typ, par)
  const C = choices.length;
  const A00 = choices.map(c => A(0, c)), A01 = choices.map(c => A(0, c));
  const A10 = choices.map(c => A(1, c)), A11 = choices.map(c => A(1, c));
  for (let a = 0; a < C; a++) {
    for (let b = 0; b < C; b++) {
      for (let c = 0; c < C; c++) {
        const al0 = A00[a] | A10[c];
        for (let d = 0; d < C; d++) {
          const al1 = A01[b] | A11[d];
          if (!relaxed(al0, al1)) continue;
          const phi = [choices[a], choices[b], choices[c], choices[d]];
          const nodes = [...new Set(phi.filter(x => x >= 0))];
          if (full(al0, al1, nodes)) return { h1: true, phi: phi };
        }
      }
    }
  }
  return { h1: false };
}

const rl = readline.createInterface({ input: process.stdin, terminal: false });
rl.on('line', line => {
  line = line.trim();
  if (!line) return;
  const inst = JSON.parse(line);
  const t0 = Date.now();
  let out;
  try { out = solve(inst); } catch (e) { out = { error: String(e) }; }
  out.ms = Date.now() - t0;
  process.stdout.write(JSON.stringify(out) + '\n');
});
