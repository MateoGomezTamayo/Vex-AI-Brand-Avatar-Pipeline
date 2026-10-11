# Día 3 · Atención al cliente: de 30 a 5 minutos.
import sys, pathlib
d = pathlib.Path(__file__).parent; sys.path.insert(0, str(d.parent / 'comun'))
from base_html import armar

HTML = '''
<div class="card" id="c-analisis">
  <div class="kick">CLIENTE E-COMMERCE</div><div class="ttl">Análisis del CRM</div>
  <div style="margin-top:26px">
    <div class="row" id="a1" style="opacity:0"><span>Conversaciones</span><span class="ok">✓ Analizadas</span></div>
    <div class="row" id="a2" style="opacity:0"><span>Cuello de botella</span><b>Encontrado</b></div>
    <div class="row" id="a3" style="opacity:0;border:0"><span>Tiempo de respuesta</span><span class="pill roja">30 min</span></div>
  </div>
</div>
<div class="card" id="c-resultado">
  <div class="kick">RESULTADO</div><div class="ttl">Tiempo de respuesta</div>
  <div class="par"><div><div class="big antes">30</div><div class="l">minutos antes</div></div><div class="flecha">→</div>
  <div id="r5" style="opacity:0"><div class="big despues">5</div><div class="l">minutos después</div></div></div>
</div>
<div class="card" id="c-volumen">
  <div class="kick">MIENTRAS TANTO</div><div class="ttl">Mensajes atendidos</div>
  <div class="par"><div><div class="big" style="font-size:100px">5.000</div><div class="l">al inicio</div></div><div class="flecha">→</div>
  <div id="v20" style="opacity:0"><div class="big despues" style="font-size:100px" id="v20n">20.000</div><div class="l">después</div></div></div>
</div>
<div class="cta" id="cta"><div class="btn">Comenta "BOT" 👇</div><p>vextrumlabs.com</p></div>
'''

JS = '''
function animar(t) {
  sh($('a1'), kw('analisis', 'analizamos'), t); sh($('a2'), kw('analisis', 'encontramos'), t); sh($('a3'), kw('analisis', 'respuestas'), t);
  sh($('r5'), kw('resultado', '5'), t);
  const t20 = kw('volumen', ['a20', '20']); sh($('v20'), t20, t);
  $('v20n').textContent = Math.round(5000 + 15000 * ease((t - t20) / 1.0)).toLocaleString('es-CO');
  const tc = kw('cta', 'comenta'); $('cta').style.opacity = ease((t - tc) / 0.4);
  $('subs').style.visibility = t >= tc ? 'hidden' : 'visible';
}
'''

armar(d, 'DÍA 3 · ATENCIÓN AL CLIENTE', "{ intro: [1, 0], cta: [0.82, -170] }", HTML, JS)
