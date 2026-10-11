# Día 2 · Inventario con NFC: tarjetas sincronizadas con la voz.
import sys, pathlib
d = pathlib.Path(__file__).parent; sys.path.insert(0, str(d.parent / 'comun'))
from base_html import armar

CSS = '''.nfc { display: flex; align-items: center; gap: 40px; margin-top: 26px; height: 250px; }
.stock { flex: 1; } .stock .n { font-weight: 800; font-size: 120px; line-height: 1; font-variant-numeric: tabular-nums; } .stock .l { font-size: 32px; color: #4A5B70; }
.tallas { display: flex; gap: 18px; margin-top: 34px; }
.talla { flex: 1; text-align: center; background: #EEF3F9; border-radius: 24px; padding: 22px 0; }
.talla b { display: block; font-size: 52px; } .talla span { font-size: 26px; color: #4A5B70; font-weight: 600; }
.talla.out { background: #F3F4F6; color: #9CA3AF; } .talla.out span { color: #DC2626; font-weight: 800; }
.tienda { font-size: 32px; color: #4A5B70; margin-top: 8px; }'''

HTML = '''
<div class="card" id="c-problema">
  <div class="kick">EL PROBLEMA</div><div class="ttl">Pedido #1043</div>
  <div class="row"><span>Tenis blanco · talla 38</span><b>$189.900</b></div>
  <div class="row" id="pago" style="opacity:0"><span>Pago</span><span class="ok">✓ Recibido</span></div>
  <div class="row" id="busca" style="opacity:0;border:0"><span>En bodega</span><span class="pill roja">✗ Agotado</span></div>
</div>
<div class="card" id="c-nfc">
  <div class="kick">LA SOLUCIÓN</div><div class="ttl">Un toque y se descuenta</div>
  <div class="nfc">
    <svg width="330" height="250" viewBox="0 0 330 250">
      <rect x="20" y="60" width="200" height="130" rx="18" fill="#111827"/><text x="120" y="135" text-anchor="middle" font-family="M" font-weight="800" font-size="30" fill="#fff">NFC</text>
      <g id="ondas" fill="none" stroke="#0070EB" stroke-width="7" stroke-linecap="round" opacity="0"><path d="M235 95 Q255 125 235 155"/><path d="M255 80 Q285 125 255 170"/></g>
      <g id="cel"><rect x="0" y="0" width="110" height="200" rx="20" fill="#0B1B2E"/><rect x="9" y="16" width="92" height="160" rx="10" fill="#3D9BFF"/><circle cx="55" cy="188" r="6" fill="#4A5B70"/></g>
    </svg>
    <div class="stock"><div class="l">Tenis blanco · talla 38</div><div class="n" id="stockN">1</div><div class="l">en inventario</div></div>
  </div>
  <div class="row" id="vendido" style="opacity:0;border:0"><span>Venta registrada</span><span class="pill">✓ Al instante</span></div>
</div>
<div class="card" id="c-web">
  <div class="kick">TIENDA EN LÍNEA</div><div class="ttl">Siempre al día</div>
  <div class="tienda">Tenis blanco · elige tu talla</div>
  <div class="tallas">
    <div class="talla"><b>36</b><span>4 disp.</span></div>
    <div class="talla"><b>37</b><span>6 disp.</span></div>
    <div class="talla" id="t38"><b>38</b><span id="t38s">1 disp.</span></div>
    <div class="talla"><b>39</b><span>3 disp.</span></div>
  </div>
  <div class="row" id="sync" style="opacity:0;border:0;margin-top:30px"><span>Base de datos</span><span class="pill">✓ Tiempo real</span></div>
</div>
<div class="cta" id="cta"><div class="btn">Comenta "NFC" 👇</div><p>vextrumlabs.com</p></div>
'''

JS = '''
function animar(t) {
  sh($('pago'), kw('problema', 'paga'), t); sh($('busca'), kw('problema', 'esta'), t);
  const tap = kw('nfc', 'toque'), ap = ease((t - (tap - 1.2)) / 1.1);
  $('cel').setAttribute('transform', `translate(${210 - 60 * ap} ${30 - 10 * ap}) rotate(${-14 + 14 * ap} 55 100)`);
  $('ondas').setAttribute('opacity', t >= tap ? 0.5 + 0.5 * Math.sin((t - tap) * 12) : 0);
  const baja = kw('nfc', 'descuenta'); $('stockN').textContent = t >= baja ? 0 : 1;
  $('stockN').style.color = t >= baja ? '#0070EB' : '#0B1B2E';
  sh($('vendido'), kw('nfc', 'instante'), t);
  const out = t >= kw('web', 'tienda'); $('t38').classList.toggle('out', out); $('t38s').textContent = out ? 'Agotada' : '1 disp.';
  sh($('sync'), kw('web', 'tiempo'), t);
  const tc = kw('cta', 'comenta'); $('cta').style.opacity = ease((t - tc) / 0.4);
  $('subs').style.visibility = t >= tc ? 'hidden' : 'visible';
}
'''

armar(d, 'DÍA 2 · INVENTARIO', "{ intro: [1, 0], cta: [0.82, -170] }", HTML, JS, CSS)
