/* Minimal DOM stub. The widget writes its whole UI into body.innerHTML and wires buttons
   through body.querySelectorAll, so stubbing those two is enough to drive it and read the
   numbers it reports. */
const fs = require('fs');
const core = fs.readFileSync('courseware/widgets/core.js', 'utf8');
const item = fs.readFileSync('courseware/widgets/items/label_rules.js', 'utf8');
const DATA = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));

let handlers = {};
const body = {
  innerHTML: '',
  querySelectorAll(sel) {
    if (sel !== '.cw-rule') return [];
    const keys = [...body.innerHTML.matchAll(/data-k="([a-z]+)"/g)].map(m => m[1]);
    return keys.map(k => ({
      getAttribute: () => k,
      addEventListener: (_, fn) => { handlers[k] = fn; },
    }));
  },
};
const root = {id: 'x', querySelector: () => body};
global.document = {getElementById: () => ({addEventListener: () => {}}), querySelectorAll: () => []};
global.window = global;
eval(core);
const fn = eval('(' + item.trim().replace(/;$/, '') + ')');
fn(root, DATA, {question: 'q', top: 12, rare_below: 5, reveal_lines: [], note: ''});

function readout() {
  const sp = body.innerHTML.match(/holds <b>(\d+)<\/b> different spelling/);
  const mv = body.innerHTML.match(/and <b>(\d+)<\/b> rows? have been set aside/);
  return {spellings: +sp[1], moved: mv ? +mv[1] : 0};
}
const steps = [Object.assign({rule: 'none'}, readout())];
for (const k of ['dedupe', 'order', 'junk', 'substrate', 'rare']) {
  handlers[k]();
  steps.push(Object.assign({rule: k}, readout()));
}
const bars = [...body.innerHTML.matchAll(/<title>([^<]+)<\/title>/g)].map(m => m[1]);
console.log(JSON.stringify({steps, bars}));
