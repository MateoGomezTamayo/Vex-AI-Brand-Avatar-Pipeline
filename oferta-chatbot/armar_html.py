# Oferta · Chatbot o asistente con IA (precios desde el cotizador, catalogo.js).
import sys, pathlib
d = pathlib.Path(__file__).parent; sys.path.insert(0, str(d.parent / 'comun'))
from base_html import armar

CSS = '''.precio { margin-top: 30px; } .precio .l { font-size: 32px; color: #4A5B70; font-weight: 600; } .precio .big { font-size: 110px; color: #0070EB; letter-spacing: -3px; }
.lista { margin-top: 18px; font-size: 34px; color: #4A5B70; line-height: 1.55; } .lista b { color: #047857; }'''

HTML = '''
<div class="card" id="c-basico">
  <div class="kick">CHATBOT BÁSICO</div><div class="ttl">Reglas y botones</div>
  <div class="lista"><div id="b1" style="opacity:0"><b>✓</b> Preguntas frecuentes</div><div id="b2" style="opacity:0"><b>✓</b> Captura de datos</div><div id="b3" style="opacity:0"><b>✓</b> Paso a un asesor</div></div>
  <div class="precio" id="bp" style="opacity:0"><div class="l">Desde</div><div class="big">$1.200.000</div></div>
</div>
<div class="card" id="c-ia">
  <div class="kick">ASISTENTE CON IA</div><div class="ttl">Responde natural</div>
  <div class="lista"><div id="i1" style="opacity:0"><b>✓</b> Entrenado con tus catálogos</div><div id="i2" style="opacity:0"><b>✓</b> Y con tus documentos</div></div>
  <div class="precio" id="ip" style="opacity:0"><div class="l">Desde</div><div class="big">$2.500.000</div></div>
</div>
<div class="cta" id="cta"><div class="btn">Cotiza en vextrumlabs.com</div><p>Plan y precio en minutos</p></div>
'''

JS = '''
function animar(t) {
  sh($('b1'), kw('basico', 'preguntas'), t); sh($('b2'), kw('basico', 'toma'), t); sh($('b3'), kw('basico', 'asesor'), t); sh($('bp'), kw('basico', 'desde'), t);
  sh($('i1'), kw('ia', 'catalogos'), t); sh($('i2'), kw('ia', 'documentos'), t); sh($('ip'), kw('ia', 'desde'), t);
  const tc = kw('cta', 'cotiza'); $('cta').style.opacity = ease((t - tc) / 0.4);
  $('subs').style.visibility = t >= tc ? 'hidden' : 'visible';
}
'''

armar(d, 'CHATBOTS CON IA', "{ intro: [1, 0], cta: [0.82, -170] }", HTML, JS, CSS)
