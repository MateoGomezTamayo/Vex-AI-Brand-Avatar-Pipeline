# Servicio nuevo · Modelado 3D inmobiliario: recorrido, vista desde arriba y agenda de visitas (capturas reales del sitio del Edificio Naranjal).
import sys, pathlib
d = pathlib.Path(__file__).parent; sys.path.insert(0, str(d.parent / 'comun'))
from base_html import armar

CSS = '''.foto { margin-top: 22px; width: 100%; height: 380px; border-radius: 24px; overflow: hidden; position: relative; box-shadow: inset 0 0 0 2px #E3E9F1; }
.foto img { width: 100%; height: 100%; object-fit: cover; display: block; }
.toque { position: absolute; width: 74px; height: 74px; border-radius: 50%; border: 6px solid #fff; background: rgba(0,112,235,.35); box-shadow: 0 0 0 10px rgba(0,112,235,.25); opacity: 0; }
.chip { position: absolute; left: 22px; bottom: 22px; background: rgba(11,27,46,.82); color: #fff; font-weight: 800; font-size: 28px; border-radius: 999px; padding: 10px 24px; opacity: 0; }'''

HTML = '''
<div class="card" id="c-recorrido">
  <div class="kick">RECORRIDO 3D</div><div class="ttl">Camina el apartamento</div>
  <div class="foto"><img src="img/recorrido.webp" id="fr" alt=""><div class="toque" id="tq" style="left:52%;top:62%"></div><div class="chip" id="ch1">Empieza en la puerta de entrada</div></div>
</div>
<div class="card" id="c-maqueta">
  <div class="kick">VISTA DESDE ARRIBA</div><div class="ttl">Cada espacio, a la vista</div>
  <div class="foto"><img src="img/maqueta.webp" id="fm" alt=""><div class="chip" id="ch2">Acabados de las fotos reales</div></div>
</div>
<div class="card" id="c-agenda">
  <div class="kick">AGENDA DE VISITAS</div><div class="ttl">Visita en dos toques</div>
  <div class="foto"><img src="img/agenda.webp" alt=""><div class="chip" id="ch3">Solo horarios disponibles</div></div>
</div>
<div class="card" id="c-caso">
  <div class="kick">CASO REAL · MEDELLÍN</div><div class="ttl">Edificio en Laureles</div>
  <div style="margin-top:26px">
    <div class="row" id="k1" style="opacity:0"><span>Fotos y video</span><span class="ok">✓</span></div>
    <div class="row" id="k2" style="opacity:0"><span>Recorrido 3D</span><span class="ok">✓</span></div>
    <div class="row" id="k3" style="opacity:0;border:0"><span>Agenda de visitas</span><span class="pill">✓ Funcionando</span></div>
  </div>
</div>
<div class="cta" id="cta"><div class="btn">Cotiza tu recorrido 3D</div><p>vextrumlabs.com</p></div>
'''

JS = '''
function animar(t) {
  // recorrido: la imagen avanza despacio (como caminar) y aparece un toque sobre el piso
  const r0 = sec('recorrido').start, z = 1 + Math.max(0, Math.min(1, (t - r0) / 6)) * 0.12; $('fr').style.transform = `scale(${z})`;
  const tq = kw('recorrido', 'camina'); $('tq').style.opacity = Math.max(0, Math.sin(Math.min(1, Math.max(0, (t - tq) / 1.2)) * Math.PI));
  sh($('ch1'), kw('recorrido', 'puerta'), t);
  const m0 = sec('maqueta').start; $('fm').style.transform = `scale(${1.08 - Math.max(0, Math.min(1, (t - m0) / 5)) * 0.08})`;
  sh($('ch2'), kw('maqueta', 'acabados'), t);
  sh($('ch3'), kw('agenda', 'horarios'), t);
  sh($('k1'), kw('caso', 'funcionando'), t); sh($('k2'), kw('caso', 'laureles'), t); sh($('k3'), kw('caso', 'medellin'), t);
  const tc = kw('cta', 'cotiza'); $('cta').style.opacity = ease((t - tc) / 0.4);
  $('subs').style.visibility = t >= tc ? 'hidden' : 'visible';
}
'''

armar(d, 'NUEVO · 3D INMOBILIARIO', "{ intro: [1, 0], cta: [0.82, -170] }", HTML, JS, CSS)
