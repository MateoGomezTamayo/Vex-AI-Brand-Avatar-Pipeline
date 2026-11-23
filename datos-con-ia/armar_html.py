# "Datos con IA" explicado por Vex: el curso gratis de análisis de datos que Mateo creó como asistencia, de parte de Vextrum Labs.
# Usa capturas reales del sitio (tmp/capturas, se generan con capturas.py) dentro de un celular, con dedo que toca, chips y checks.
import sys, pathlib
d = pathlib.Path(__file__).parent; sys.path.insert(0, str(d.parent / 'comun'))
from base_html import armar

CSS = '''.esc { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; opacity: 0; pointer-events: none; }
#flash { position: absolute; inset: 0; background: #fff; opacity: 0; z-index: 50; pointer-events: none; }
#barra { position: absolute; top: 40px; left: 70px; right: 70px; display: flex; gap: 10px; z-index: 40; }
#barra i { flex: 1; height: 8px; border-radius: 8px; background: rgba(255,255,255,.18); overflow: hidden; }
#barra i b { display: block; height: 100%; width: 0; background: #3D9BFF; }
.slam { position: absolute; left: 0; right: 0; text-align: center; font-weight: 800; letter-spacing: -3px; line-height: 1.02; text-shadow: 0 16px 50px rgba(0,0,0,.55); opacity: 0; }
.slam b { color: #3D9BFF; font-weight: 800; }
.cod { position: absolute; background: #0B1B2E; color: #7FDBFF; font-family: Consolas, monospace; font-weight: 700; font-size: 34px; border: 3px solid #1C3D63; border-radius: 14px; padding: 14px 22px; white-space: nowrap; box-shadow: 0 24px 50px -16px rgba(0,0,0,.7); opacity: 0; }
.cod.rojo { color: #FCA5A5; border-color: #7F1D1D; }
.phone { position: absolute; left: 70px; top: 265px; width: 540px; height: 1130px; border-radius: 70px; background: #0B1B2E; padding: 16px; box-shadow: 0 60px 120px -30px rgba(0,0,0,.85), 0 0 0 3px #1C3D63; }
.phone .scr { position: relative; width: 100%; height: 100%; border-radius: 56px; overflow: hidden; background: #F5F8FC; }
.phone img { position: absolute; left: 0; top: 0; width: 100%; }
.chip { position: absolute; left: 660px; width: 360px; background: rgba(0,123,255,.22); border: 3px solid rgba(61,155,255,.75); color: #fff; font-weight: 800; font-size: 34px; line-height: 1.15; border-radius: 28px; padding: 18px 24px; opacity: 0; }
.chip.verde { background: rgba(37,211,102,.2); border-color: rgba(37,211,102,.85); }
.dedo { position: absolute; width: 96px; height: 96px; border-radius: 50%; border: 7px solid #fff; background: rgba(61,155,255,.35); box-shadow: 0 10px 30px rgba(0,0,0,.5); opacity: 0; z-index: 30; }
.ok { position: absolute; width: 84px; height: 84px; border-radius: 50%; background: #34D399; color: #0B1B2E; font-weight: 900; font-size: 52px; display: grid; place-items: center; box-shadow: 0 10px 30px rgba(52,211,153,.6); opacity: 0; z-index: 31; }
.ej { position: absolute; left: 70px; top: 1420px; font-size: 24px; font-weight: 700; letter-spacing: 3px; color: #8FB4DA; }
.hex { width: 150px; height: 150px; margin: 0 auto 26px; display: block; }
.firma { position: absolute; left: 90px; right: 90px; top: 720px; text-align: center; background: #fff; color: #0B1B2E; border-radius: 34px; padding: 30px 36px; font-weight: 800; font-size: 40px; box-shadow: 0 40px 90px -30px rgba(0,0,0,.75); opacity: 0; }
.firma small { display: block; font-size: 30px; color: #4A5B70; font-weight: 600; margin-top: 8px; }
.cta .btn.wa { background: #25D366; color: #06331A; }'''

def celular(cid, img):
    return f'<div class="phone" id="{cid}"><div class="scr"><img src="tmp/capturas/{img}" alt=""></div></div>'

LOGO = ('<svg class="hex" viewBox="0 0 36 36"><polygon points="18,2 34,10 34,26 18,34 2,26 2,10" fill="#001F3F" stroke="#3D9BFF" stroke-width="1"/>'
        '<polygon points="18,8 28,13 28,23 18,28 8,23 8,13" fill="#007BFF"/><polygon points="18,14 24,17 24,21 18,24 12,21 12,17" fill="#fff"/></svg>')
CODIGOS = [('import pandas', 80, 560, -6, ''), ('df.head()', 640, 520, 5, ''), ('SyntaxError', 90, 860, 4, 'rojo'), ('groupby', 680, 830, -5, ''),
           ('NaN', 160, 1150, -3, 'rojo'), ('plt.show()', 600, 1130, 6, '')]
COD = ''.join(f'<div class="cod {c}" id="cd{i}">{n}</div>' for i, (n, *_r, c) in enumerate(CODIGOS))

HTML = f'''
<div id="barra">{''.join('<i><b></b></i>' for _ in range(10))}</div>
<div class="esc" id="c-hook">
  <div class="slam" id="qq" style="top:290px;font-size:104px">¿NUNCA HAS<br>PROGRAMADO?</div>
  {COD}
</div>
<div class="esc" id="c-mateo">
  <div class="slam" id="mt" style="top:280px;font-size:110px">{LOGO}Creado por<br><b>Mateo</b></div>
  <div class="firma" id="fm">Asistencia para el curso<small>de parte de Vextrum Labs</small></div>
</div>
<div class="esc" id="c-curso">
  {celular('p1', '1-inicio.png')}
  <div class="chip" id="k10" style="top:300px">📚 6 lecciones</div>
  <div class="chip" id="k11" style="top:440px">💸 Gratis</div>
  <div class="chip" id="k12" style="top:580px">🗣️ En español</div>
  <div class="chip" id="k13" style="top:720px">📓 Paso a paso en Jupyter</div>
</div>
<div class="esc" id="c-ejecuta">
  {celular('p2', '2-ejecutar.png')}
  <div class="dedo" id="dd2"></div>
  <div class="chip" id="k20" style="top:340px">🐍 Python en tu navegador</div>
  <div class="chip verde" id="k21" style="top:520px">✓ Sin instalar nada</div>
  <div class="ej">DATOS DE PRÁCTICA SIMULADOS</div>
</div>
<div class="esc" id="c-palabras">
  {celular('p3', '3-palabra.png')}
  <div class="dedo" id="dd3"></div>
  <div class="chip" id="k30" style="top:420px">👆 Tocas la palabra</div>
  <div class="chip verde" id="k31" style="top:580px">💡 Te explica qué significa</div>
</div>
<div class="esc" id="c-vex">
  {celular('p4', '4-vex.png')}
  <div class="chip" id="k40" style="top:300px">👀 Ve tu código</div>
  <div class="chip" id="k41" style="top:440px">⚠️ Ve tu error</div>
  <div class="chip verde" id="k42" style="top:580px">💬 Te explica sin enredos</div>
</div>
<div class="esc" id="c-quiz">
  {celular('p5', '5-quiz.png')}
  <div class="ok" id="ok5">✓</div>
  <div class="chip" id="k50" style="top:380px">🧩 Quiz en cada lección</div>
  <div class="chip verde" id="k51" style="top:560px">¿Lo tienes claro?</div>
</div>
<div class="esc" id="c-whatsapp">
  {celular('p6', '6-whatsapp.png')}
  <div class="dedo" id="dd6"></div>
  <div class="chip" id="k60" style="top:360px">📈 Los datos de tu negocio</div>
  <div class="chip verde" id="k61" style="top:540px">💬 Asesoría por WhatsApp</div>
</div>
<div class="cta" id="cta"><div class="btn">Datos con IA · gratis</div><p>Entra desde vextrumlabs.com</p></div>
<div id="flash"></div>
'''

JS = '''
const cl = x => Math.max(0, Math.min(1, x));
const back = x => { x = cl(x); const c1 = 1.9, c3 = c1 + 1; return 1 + c3 * Math.pow(x - 1, 3) + c1 * Math.pow(x - 1, 2); };
const pop = (el, t0, t, extra = '', d = 0.42) => { el.style.opacity = cl((t - t0) / 0.12); el.style.transform = `${extra} scale(${t < t0 ? 0.3 : 0.3 + 0.7 * back((t - t0) / d)})`; };
const SEC = DATOS.secciones;
const POS = { hook: [1.0, 0, -20], intro: [0.95, 0, 40], mateo: [0.5, 0, 470], curso: [0.4, 340, 380], ejecuta: [0.4, 340, 420],
              palabras: [0.4, 340, 420], vex: [0.4, 340, 420], quiz: [0.4, 340, 420], whatsapp: [0.4, 340, 420], cta: [0.82, 0, -170] };
function vexLugar(t) {
  let i = 0; while (i < SEC.length - 1 && t >= SEC[i + 1].start - 0.45) i++;
  const a = POS[SEC[Math.max(0, i - 1)].id], b = POS[SEC[i].id], k = i ? back((t - (SEC[i].start - 0.45)) / 0.6) : 1;
  let salto = i ? Math.sin(cl((t - (SEC[i].start - 0.45)) / 0.6) * Math.PI) * 70 : 0;
  (window.BRINCOS || []).forEach(h => { if (t >= h && t < h + 0.45) salto += Math.sin((t - h) / 0.45 * Math.PI) * 55; });
  const s = a[0] + (b[0] - a[0]) * k, x = a[1] + (b[1] - a[1]) * k, y = a[2] + (b[2] - a[2]) * k - salto;
  $('vex').setAttribute('transform', `translate(${540 + x} ${950 + y}) scale(${s}) translate(-540 -950)`);
}
// el celular entra desde abajo y la captura hace un acercamiento lento (Ken Burns) hacia el punto que importa
function celular(id, sid, foco = 0.3, zoom = 1.12) {
  const t0 = sec(sid).start, el = $(id), e = cl((T - t0 + 0.2) / 0.55);
  el.style.transform = `translateY(${(1 - back(e)) * 700}px) rotate(${(1 - e) * -5}deg)`;
  const img = el.querySelector('img'), k = cl((T - t0) / (sec(sid).end - t0));
  img.style.transformOrigin = `50% ${foco * 100}%`; img.style.transform = `scale(${1 + (zoom - 1) * k})`;
}
// dedo que toca un punto del celular (x, y relativos a la pantalla)
function dedo(id, cel, rx, ry, at) {
  const dd = $(id);
  if (T < at - 0.5 || T > at + 0.9) { dd.style.opacity = 0; return; }
  const r = $(cel).querySelector('.scr').getBoundingClientRect(), f = cl((T - at + 0.25) / 0.25);
  const lleg = cl((T - at + 0.5) / 0.3);
  dd.style.left = (r.left + r.width * rx - 48 + (1 - lleg) * 160) + 'px'; dd.style.top = (r.top + r.height * ry - 48 + (1 - lleg) * 120) + 'px';
  dd.style.opacity = 0.92 * lleg; dd.style.transform = `scale(${1.25 - 0.45 * Math.sin(f * Math.PI)})`;
}
let T = 0, GOLPES = null;
function animar(t) {
  T = t;
  if (!GOLPES) GOLPES = { cortes: SEC.slice(1).map(s => s.start - 0.06), fuertes: [kw('mateo', 'mateo'), kw('ejecuta', 'instalar'), kw('whatsapp', 'whatsapp')] };
  if (!window.BRINCOS) window.BRINCOS = [kw('mateo', 'mateo'), kw('ejecuta', 'navegador'), kw('vex', 'mi'), kw('quiz', 'claro'), kw('cta', 'entra')];
  vexLugar(t);
  let fl = 0, z = 0, sx = 0, sy = 0;
  GOLPES.cortes.forEach(h => { if (t >= h) { const e = Math.exp(-(t - h) * 13); fl = Math.max(fl, 0.5 * e); z += 0.035 * Math.exp(-(t - h) * 8); } });
  GOLPES.fuertes.forEach(h => { if (t >= h) { const e = Math.exp(-(t - h) * 9); z += 0.03 * e; sx += Math.sin((t - h) * 80) * 12 * e; sy += Math.cos((t - h) * 67) * 9 * e; } });
  $('flash').style.opacity = fl;
  document.body.style.transform = `translate(${sx}px, ${sy}px) scale(${1 + z})`;
  [...$('barra').children].forEach((el, i) => { const s = SEC[i]; el.firstChild.style.width = (s ? cl((t - s.start) / (s.end - s.start)) * 100 : 0) + '%'; });

  // 1. Gancho: pedazos de código que asustan; con "mira" se los traga el centro
  const h0 = sec('hook').start, mira = kw('hook', 'mira');
  pop($('qq'), h0 + 0.05, t);
  const base = [[80, 560, -6], [640, 520, 5], [90, 860, 4], [680, 830, -5], [160, 1150, -3], [600, 1130, 6]];
  base.forEach(([bx, by, r], i) => {
    const el = $('cd' + i), g = cl((t - mira) / 0.45), gg = g * g;
    const x = bx + Math.sin(t * 1.7 + i) * 22, y = by + Math.cos(t * 1.3 + i * 2) * 18;
    el.style.left = (x + (440 - x) * gg) + 'px'; el.style.top = (y + (900 - y) * gg) + 'px';
    pop(el, h0 + 0.35 + i * 0.16, t, `rotate(${r + Math.sin(t * 2 + i) * 5 + gg * 220}deg)`);
    if (t > mira) el.style.opacity = 1 - gg;
  });
  if (t > mira) $('qq').style.opacity = 1 - cl((t - mira) / 0.3);

  // 2. Mateo: firma de Vextrum Labs
  pop($('mt'), kw('mateo', 'mateo'), t);
  pop($('fm'), kw('mateo', 'asistencia'), t, 'rotate(-1.5deg)');

  // 3. El curso
  celular('p1', 'curso', 0.2, 1.06);
  pop($('k10'), kw('curso', 'seis'), t, 'rotate(-2deg)'); pop($('k11'), kw('curso', 'gratis'), t, 'rotate(2deg)');
  pop($('k12'), kw('curso', 'espanol'), t, 'rotate(-1deg)'); pop($('k13'), kw('curso', 'jupyter'), t, 'rotate(1deg)');

  // 4. Ejecutar: el dedo toca el botón azul y aparece el resultado
  celular('p2', 'ejecuta', 0.25, 1.1);
  dedo('dd2', 'p2', 0.43, 0.205, kw('ejecuta', 'ejecutar'));
  pop($('k20'), kw('ejecuta', 'navegador'), t, 'rotate(-2deg)'); pop($('k21'), kw('ejecuta', 'instalar'), t, 'rotate(2deg)');

  // 5. Palabras: tocar "notebook"
  celular('p3', 'palabras', 0.35, 1.12);
  dedo('dd3', 'p3', 0.52, 0.325, kw('palabras', 'tocas'));
  pop($('k30'), kw('palabras', 'tocas'), t, 'rotate(-2deg)'); pop($('k31'), kw('palabras', 'explica'), t, 'rotate(2deg)');

  // 6. Vex responde
  celular('p4', 'vex', 0.4, 1.08);
  pop($('k40'), kw('vex', 'codigo'), t, 'rotate(-2deg)'); pop($('k41'), kw('vex', 'error'), t, 'rotate(2deg)'); pop($('k42'), kw('vex', 'enredos'), t, 'rotate(-1deg)');

  // 7. Quiz: check en la respuesta correcta
  celular('p5', 'quiz', 0.35, 1.08);
  const r5 = $('p5').querySelector('.scr').getBoundingClientRect();
  $('ok5').style.left = (r5.left + r5.width * 0.86 - 42) + 'px'; $('ok5').style.top = (r5.top + r5.height * 0.39 - 42) + 'px';
  pop($('ok5'), kw('quiz', 'claro'), t, '', 0.4);
  pop($('k50'), kw('quiz', 'quiz'), t, 'rotate(-2deg)'); pop($('k51'), kw('quiz', 'claro'), t, 'rotate(2deg)');

  // 8. WhatsApp
  celular('p6', 'whatsapp', 0.3, 1.08);
  dedo('dd6', 'p6', 0.33, 0.535, kw('whatsapp', 'whatsapp'));
  pop($('k60'), kw('whatsapp', 'negocio'), t, 'rotate(-2deg)'); pop($('k61'), kw('whatsapp', 'asesoramos'), t, 'rotate(2deg)');

  // 9. Cierre
  const tc = kw('cta', 'entra'); $('cta').style.opacity = ease((t - tc) / 0.4); $('cta').style.transform = `scale(${0.8 + 0.2 * back((t - tc) / 0.45)})`;
  $('subs').style.visibility = t >= tc ? 'hidden' : 'visible';
}
'''

MODO = "{ hook: [1.0, -20], intro: [0.95, 40], mateo: [0.5, 470], curso: [0.4, 420], ejecuta: [0.4, 420], palabras: [0.4, 420], vex: [0.4, 420], quiz: [0.4, 420], whatsapp: [0.4, 420], cta: [0.82, -170] }"
armar(d, 'CURSO · DATOS CON IA', MODO, HTML, JS, CSS)
