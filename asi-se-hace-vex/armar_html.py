# Detrás de cámaras · Así se hace Vex.
import sys, pathlib
d = pathlib.Path(__file__).parent; sys.path.insert(0, str(d.parent / 'comun'))
from base_html import armar

CSS = '''.doc { margin-top: 24px; background: #F5F8FC; border-radius: 22px; padding: 22px 28px; font-size: 30px; color: #0B1B2E; line-height: 1.5; }
.doc i { font-style: normal; font-weight: 800; color: #0070EB; font-size: 24px; letter-spacing: 2px; margin-left: 10px; }
.onda { display: flex; align-items: center; gap: 7px; height: 120px; margin-top: 24px; } .onda span { flex: 1; background: #0070EB; border-radius: 6px; }
.letras { display: flex; gap: 14px; margin-top: 36px; } .letra { flex: 1; text-align: center; font-weight: 800; font-size: 54px; color: #8A9BB0; background: #EEF3F9; border-radius: 22px; padding: 26px 0; }
.letra.on { background: #0070EB; color: #fff; }'''

HTML = '''
<div class="card" id="c-guion">
  <div class="kick">PASOS 1 Y 2</div><div class="ttl">Guion → voz</div>
  <div class="doc">"¡Día dos automatizando procesos!" <i>GANCHO</i><br>"¿Cuántas veces vendiste algo…?" <i>PREGUNTA</i></div>
  <div class="onda" id="onda" style="opacity:0">''' + ''.join('<span></span>' for _ in range(36)) + '''</div>
</div>
<div class="card" id="c-boca">
  <div class="kick">PASO 3</div><div class="ttl">Boca sincronizada</div>
  <div class="letras">''' + ''.join(f'<div class="letra" data-l="{l}">{l}</div>' for l in 'ABCDEFGH') + '''</div>
  <div class="row" style="border:0;margin-top:26px"><span>Forma de boca ahora</span><b id="ahora">X</b></div>
</div>
<div class="card" id="c-animacion">
  <div class="kick">PASO 4</div><div class="ttl">Cuadro a cuadro</div>
  <div class="par"><div><div class="big" id="cuadro">0</div><div class="l">cuadro actual</div></div><div><div class="big despues" style="font-size:110px">30</div><div class="l">cuadros por segundo</div></div></div>
</div>
<div class="cta" id="cta"><div class="btn">Sábado: tu propio avatar</div><p>vextrumlabs.com</p></div>
'''

JS = '''
function animar(t) {
  sh($('onda'), kw('guion', 'voz'), t);
  const f = Math.min(DATOS.env.length - 1, Math.round(t * 30));
  [...$('onda').children].forEach((b, j) => { const e = DATOS.env[Math.max(0, f - (35 - j))] || 0; b.style.height = (8 + e * 112) + 'px'; });
  const m = forma(t); $('ahora').textContent = m;
  document.querySelectorAll('.letra').forEach(el => el.classList.toggle('on', el.dataset.l === m));
  $('cuadro').textContent = Math.round(t * 30);
  const tc = kw('cta', 'miralo'); $('cta').style.opacity = ease((t - tc) / 0.4);
  $('subs').style.visibility = t >= tc ? 'hidden' : 'visible';
}
'''

armar(d, 'DETRÁS DE CÁMARAS', "{ intro: [1, 0], cta: [0.82, -170] }", HTML, JS, CSS)
