# Día 4 · La web lenta en iPhone: diagnóstico y resultado.
import sys, pathlib
d = pathlib.Path(__file__).parent; sys.path.insert(0, str(d.parent / 'comun'))
from base_html import armar

CSS = '''.mini { display: flex; align-items: baseline; gap: 18px; } .mini .big { font-size: 96px; letter-spacing: -2px; } .mini .u { font-size: 36px; color: #4A5B70; font-weight: 700; }
.fila { display: flex; align-items: center; justify-content: space-between; padding: 18px 0; border-bottom: 2px solid #E3E9F1; } .fila .lab { font-size: 32px; color: #4A5B70; font-weight: 600; width: 230px; }'''

HTML = '''
<div class="card" id="c-diagnostico">
  <div class="kick">DIAGNÓSTICO · IPHONE / SAFARI</div><div class="ttl">¿Por qué tan lenta?</div>
  <div style="margin-top:22px">
    <div class="row" id="d1" style="opacity:0"><span>Respuesta</span><span class="mal">5,5 s</span></div>
    <div class="row" id="d2" style="opacity:0"><span>Secciones visibles</span><span class="mal">10,6 s</span></div>
    <div class="row" id="d3" style="opacity:0;border:0"><span>Culpable</span><span class="pill roja">Efectos blur / mask</span></div>
  </div>
</div>
<div class="card" id="c-resultado">
  <div class="kick">DESPUÉS DEL CAMBIO</div><div class="ttl">Antes → después</div>
  <div style="margin-top:20px">
    <div class="fila"><div class="lab">Respuesta</div><div class="mini"><span class="big antes">5,5</span><span class="flecha" style="font-size:56px">→</span><span class="big despues" id="r1" style="opacity:0">1,1</span><span class="u">s</span></div></div>
    <div class="fila" style="border:0"><div class="lab">Secciones</div><div class="mini"><span class="big antes">10,6</span><span class="flecha" style="font-size:56px">→</span><span class="big despues" id="r2" style="opacity:0">1,6</span><span class="u">s</span></div></div>
  </div>
</div>
<div class="card" id="c-pruebas">
  <div class="kick">ANTES DE CADA PUBLICACIÓN</div><div class="ttl">Pruebas automáticas</div>
  <div style="margin-top:26px">
    <div class="row" id="p1" style="opacity:0"><span>Chrome</span><span class="ok">✓ Aprobado</span></div>
    <div class="row" id="p2" style="opacity:0"><span>Safari (iPhone)</span><span class="ok">✓ Aprobado</span></div>
    <div class="row" id="p3" style="opacity:0;border:0"><span>Publicación</span><span class="pill">✓ Lista</span></div>
  </div>
</div>
<div class="cta" id="cta"><div class="btn">Comenta "WEB" 👇</div><p>vextrumlabs.com</p></div>
'''

JS = '''
function animar(t) {
  sh($('d1'), kw('diagnostico', 'medimos'), t); sh($('d2'), kw('diagnostico', 'usuarios'), t); sh($('d3'), kw('diagnostico', 'culpable'), t);
  sh($('r1'), kw('resultado', ['11', '55a']), t); sh($('r2'), kw('resultado', ['16', '106a']), t);
  sh($('p1'), kw('pruebas', 'chrome'), t); sh($('p2'), kw('pruebas', 'safari'), t); sh($('p3'), kw('pruebas', 'publicarlo'), t);
  const tc = kw('cta', 'comenta'); $('cta').style.opacity = ease((t - tc) / 0.4);
  $('subs').style.visibility = t >= tc ? 'hidden' : 'visible';
}
'''

armar(d, 'DÍA 4 · VELOCIDAD WEB', "{ intro: [1, 0], cta: [0.82, -170] }", HTML, JS, CSS)
