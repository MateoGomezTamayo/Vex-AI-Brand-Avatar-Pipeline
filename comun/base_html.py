# Base para el HTML de cada video: toma avatar.html, agrega estilos de tarjetas y un motor de escenas.
# Cada video llama armar(...) con su etiqueta, sus tarjetas (div.card id="c-<seccion>") y su JS de animación.
import io, pathlib
RAIZ = pathlib.Path(__file__).parent.parent

CSS = '''.card { position: absolute; left: 70px; right: 70px; top: 905px; height: 600px; background: #fff; color: #0B1B2E; border-radius: 40px; padding: 44px 50px; box-shadow: 0 50px 100px -30px rgba(0,0,0,.7); opacity: 0; }
.kick { font-weight: 800; font-size: 30px; letter-spacing: 5px; color: #0070EB; }
.ttl { font-weight: 800; font-size: 52px; line-height: 1.1; margin-top: 10px; letter-spacing: -1px; }
.row { display: flex; justify-content: space-between; align-items: center; font-size: 36px; color: #4A5B70; padding: 16px 0; border-bottom: 2px solid #E3E9F1; }
.row b { color: #0B1B2E; }
.ok { font-weight: 800; color: #047857; }
.mal { font-weight: 800; color: #DC2626; }
.pill { display: inline-block; font-weight: 800; font-size: 32px; background: #D1FAE5; color: #047857; border-radius: 999px; padding: 10px 26px; }
.pill.roja { background: #FEE2E2; color: #DC2626; }
.big { font-weight: 800; font-size: 150px; line-height: 1; letter-spacing: -4px; font-variant-numeric: tabular-nums; }
.antes { color: #DC2626; } .despues { color: #047857; }
.flecha { font-size: 80px; color: #8A9BB0; font-weight: 800; }
.par { display: flex; align-items: center; justify-content: space-between; margin-top: 30px; }
.par .l { font-size: 32px; color: #4A5B70; font-weight: 600; margin-top: 8px; }
.cta { position: absolute; left: 70px; right: 70px; top: 1500px; text-align: center; opacity: 0; }
.cta .btn { display: inline-block; background: #0070EB; border-radius: 30px; padding: 34px 54px; font-weight: 800; font-size: 56px; box-shadow: 0 20px 50px rgba(0,112,235,.5); }
.cta p { margin-top: 34px; font-size: 44px; color: #C3CFDA; font-weight: 600; }
</style>'''

MOTOR = '''
// ---- Motor de escenas: Vex se encoge cuando hay tarjeta; cada tarjeta c-<id> aparece en su sección ----
const ease = x => { x = Math.max(0, Math.min(1, x)); return 1 - Math.pow(1 - x, 3); };
const norm = x => x.normalize('NFD').replace(/[^a-zA-Z0-9]/g, '').toLowerCase();
const PAL = DATOS.grupos.flat();
const sec = id => DATOS.secciones.find(s => s.id === id);
// kw: momento en que empieza la palabra w (o la primera que aparezca de una lista de alternativas) dentro de la sección
const kw = (id, w, n = 0) => {
  const s = sec(id);
  for (const c of [].concat(w)) { const ps = PAL.filter(p => p[0] >= s.start - 0.05 && p[0] < s.end && norm(p[2]).startsWith(c)); if (ps[n]) return ps[n][0]; }
  return s.start;
};
const sh = (el, t0, t) => { el.style.opacity = ease((t - t0) / 0.35); el.style.transform = `translateY(${(1 - ease((t - t0) / 0.35)) * 24}px)`; };
function escenas(t) {
  const S = DATOS.secciones; let i = 0; while (i < S.length - 1 && t >= S[i + 1].start - 0.45) i++;
  const m = id => MODO[id] || [0.5, -330];
  const prev = m(S[Math.max(0, i - 1)].id), cur = m(S[i].id), k = ease((t - (S[i].start - 0.45)) / 0.6);
  const sc = i ? prev[0] + (cur[0] - prev[0]) * k : cur[0], ty = i ? prev[1] + (cur[1] - prev[1]) * k : cur[1];
  $('vex').setAttribute('transform', `translate(540 ${950 + ty}) scale(${sc}) translate(-540 -950)`);
  S.forEach((s, j) => {
    const el = $('c-' + s.id); if (!el) return; const nxt = S[j + 1];
    const fin = nxt ? 1 - ease((t - (nxt.start - 0.5)) / 0.35) : 1;
    el.style.opacity = Math.min(ease((t - s.start + 0.2) / 0.5), fin);
    el.style.transform = `translateY(${(1 - ease((t - s.start + 0.2) / 0.5)) * 60}px)`;
  });
  animar(t);
}
'''

def armar(carpeta, etiqueta, modo, html, js, css=''):
    s = io.open(RAIZ / 'avatar.html', encoding='utf-8').read()
    s = s.replace('url(montserrat-latin.woff2)', 'url(../montserrat-latin.woff2)').replace('src="fondo.png"', 'src="../fondo.png"')
    s = s.replace('DÍA 1 · AUTOMATIZACIÓN', etiqueta)
    s = s.replace('<ellipse cx="540" cy="1500" rx="330" ry="60" fill="url(#piso)"/>', '<g id="vex">\n  <ellipse cx="540" cy="1500" rx="330" ry="60" fill="url(#piso)"/>')
    s = s.replace('</svg>\n\n<div class="subs"', '</g>\n</svg>\n\n<div class="subs"')
    s = s.replace('</style>', css + '\n' + CSS, 1)
    s = s.replace('<div class="subs" id="subs"></div>', html + '\n<div class="subs" id="subs"></div>')
    assert 'function render(t) {' in s and '<g id="vex">' in s
    s = s.replace('function render(t) {', f'const MODO = {modo};\n' + MOTOR + js + '\nfunction render(t) {\n  escenas(t);', 1)
    io.open(carpeta / 'video.html', 'w', encoding='utf-8').write(s)
    print('html ok')
