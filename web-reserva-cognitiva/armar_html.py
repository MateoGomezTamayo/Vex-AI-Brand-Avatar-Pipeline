# La web del podcast "Reserva cognitiva" explicada por Vex: capturas reales de tureservacognitiva.vercel.app (capturas.py)
# dentro de un celular que se desplaza, Vex cambiando de lugar en cada escena y fichas con los colores del podcast.
import sys, pathlib
d = pathlib.Path(__file__).parent; sys.path.insert(0, str(d.parent / 'comun'))
from base_html import armar

CSS = '''.esc { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; opacity: 0; pointer-events: none; }
#flash { position: absolute; inset: 0; background: #fff; opacity: 0; z-index: 50; pointer-events: none; }
#barra { position: absolute; top: 40px; left: 70px; right: 70px; display: flex; gap: 10px; z-index: 40; }
#barra i { flex: 1; height: 8px; border-radius: 8px; background: rgba(255,255,255,.18); overflow: hidden; }
#barra i b { display: block; height: 100%; width: 0; background: #F2C230; }
.slam { position: absolute; left: 0; right: 0; text-align: center; font-weight: 800; letter-spacing: -3px; line-height: 1; text-shadow: 0 16px 50px rgba(0,0,0,.55); opacity: 0; }
.slam em { font-style: normal; color: #F2C230; }
.coin { position: absolute; width: 110px; height: 110px; border-radius: 50%; background: #F2C230; border: 9px solid #111; display: grid; place-items: center; font-weight: 800; font-size: 60px; color: #111; box-shadow: inset 0 0 0 8px #F7D774, 0 20px 40px rgba(0,0,0,.45); opacity: 0; }
.portada { position: absolute; left: 270px; top: 250px; width: 540px; height: 540px; border-radius: 44px; box-shadow: 0 50px 100px -30px rgba(0,0,0,.8); opacity: 0; }
.phone { position: absolute; left: 470px; top: 250px; width: 560px; height: 1200px; border-radius: 70px; background: #111; padding: 16px; box-shadow: 0 60px 120px -30px rgba(0,0,0,.85), 0 0 0 4px #F4A9C8; }
.phone .scr { position: relative; width: 100%; height: 100%; border-radius: 56px; overflow: hidden; background: #F6E3B4; }
.phone .scr img { position: absolute; left: 0; top: 0; width: 100%; opacity: 0; }
.chip { position: absolute; left: 60px; max-width: 390px; background: #F6E3B4; color: #111; font-weight: 800; font-size: 34px; line-height: 1.15; border-radius: 26px; padding: 18px 26px; box-shadow: 0 20px 40px rgba(0,0,0,.45); opacity: 0; }
.chip.azul { background: #2B44A8; color: #fff; } .chip.rosa { background: #F4A9C8; }
.toque { position: absolute; width: 110px; height: 110px; border-radius: 50%; border: 8px solid #fff; background: rgba(43,68,168,.4); opacity: 0; z-index: 3; }
.url { position: absolute; left: 60px; right: 60px; top: 1290px; text-align: center; opacity: 0; }
.url span { display: inline-block; background: #F6E3B4; color: #111; font-weight: 800; font-size: 50px; letter-spacing: -1px; border-radius: 999px; padding: 22px 40px; box-shadow: 0 24px 50px rgba(0,0,0,.5); }
.url small { display: block; font-size: 34px; color: #F2C230; font-weight: 800; letter-spacing: 3px; margin-bottom: 18px; }'''

BARRA = ''.join('<i><b></b></i>' for _ in range(8))
MONEDAS = ''.join(f'<div class="coin" id="co{i}">$</div>' for i in range(6))
HTML = f'''
<div id="barra">{BARRA}</div>
<div class="esc" id="c-hook">
  <div class="slam" id="qq" style="top:300px;font-size:116px">¿TU CEREBRO<br>TIENE <em>PENSIÓN</em>?</div>
  {MONEDAS}
</div>
<div class="esc" id="c-intro">
  <img class="portada" id="pt" src="img/portada.jpg" alt="">
  <div class="slam" id="pts" style="top:830px;font-size:56px;letter-spacing:0;color:#F6E3B4">La web del podcast</div>
</div>
<div class="phone" id="ph" style="opacity:0"><div class="scr">
  <img id="i-hero0" src="img/hero-0.webp" alt=""><img id="i-hero1" src="img/hero-1.webp" alt="">
  <img id="i-def" src="img/definicion.webp" alt=""><img id="i-hab" src="img/habitos.webp" alt=""><img id="i-ext" src="img/extracto.webp" alt="">
  <img id="i-hor" src="img/hormiga.webp" alt=""><img id="i-eps" src="img/episodios.webp" alt=""><img id="i-mit" src="img/mitos.webp" alt="">
  <div class="toque" id="tq" style="left:150px;top:330px"></div>
</div></div>
<div class="esc" id="c-cerebrito">
  <div class="chip" id="k-ce0" style="top:330px">Toca al cerebrito</div>
  <div class="chip azul" id="k-ce1" style="top:470px">Cada moneda suma a tu saldo</div>
</div>
<div class="esc" id="c-definicion">
  <div class="chip rosa" id="k-de0" style="top:330px">7 ideas que se abren</div>
  <div class="chip" id="k-de1" style="top:470px">En lenguaje sencillo</div>
  <div class="chip azul" id="k-de2" style="top:610px">Stern (2002, 2009)</div>
</div>
<div class="esc" id="c-extracto">
  <div class="chip" id="k-ex0" style="top:330px">10 hábitos</div>
  <div class="chip azul" id="k-ex1" style="top:470px">Tu extracto cerebral</div>
  <div class="chip rosa" id="k-ex2" style="top:610px">Consejos para ahorrar más</div>
</div>
<div class="esc" id="c-hormiga">
  <div class="chip" id="k-ho0" style="top:330px">3 ahorros hormiga</div>
  <div class="chip rosa" id="k-ho1" style="top:470px">Tu plan de la semana</div>
</div>
<div class="esc" id="c-mitos">
  <div class="chip azul" id="k-mi0" style="top:330px">6 episodios</div>
  <div class="chip rosa" id="k-mi1" style="top:470px">¿Mito o realidad?</div>
</div>
<div class="url" id="url"><small>PRUÉBALA</small><span>tureservacognitiva.vercel.app</span></div>
<div class="cta" id="cta"><div class="btn">¿Quieres una web así?</div><p>vextrumlabs.com</p></div>
<div id="flash"></div>
'''

JS = '''
const cl = x => Math.max(0, Math.min(1, x));
const back = x => { x = cl(x); const c1 = 1.9, c3 = c1 + 1; return 1 + c3 * Math.pow(x - 1, 3) + c1 * Math.pow(x - 1, 2); };
const pop = (el, t0, t, extra = '', d = 0.42) => { el.style.opacity = cl((t - t0) / 0.12); el.style.transform = `${extra} scale(${t < t0 ? 0.3 : 0.3 + 0.7 * back((t - t0) / d)})`; };
const SEC = DATOS.secciones;
// Vex cambia de lugar en cada escena: [escala, x, y]
const POS = { hook: [1.0, 0, 60], intro: [0.5, 0, 400], cerebrito: [0.42, -330, 330], definicion: [0.42, -330, 330], extracto: [0.42, -330, 330],
              hormiga: [0.42, -330, 330], mitos: [0.42, -330, 330], cta: [0.82, 0, -200] };
function vexLugar(t) {
  let i = 0; while (i < SEC.length - 1 && t >= SEC[i + 1].start - 0.45) i++;
  const a = POS[SEC[Math.max(0, i - 1)].id], b = POS[SEC[i].id], k = i ? back((t - (SEC[i].start - 0.45)) / 0.6) : 1;
  const salto = i && a !== b ? Math.sin(cl((t - (SEC[i].start - 0.45)) / 0.6) * Math.PI) * 70 : 0;
  const s = a[0] + (b[0] - a[0]) * k, x = a[1] + (b[1] - a[1]) * k, y = a[2] + (b[2] - a[2]) * k - salto;
  $('vex').setAttribute('transform', `translate(${540 + x} ${950 + y}) scale(${s}) translate(-540 -950)`);
}
// una captura visible en el celular, que se desplaza de a (0 = arriba) a b (1 = abajo) entre t0 y t1
const SCR = 1168;
function pantalla(id, t, t0, t1, a = 0, b = 1) {
  const el = $(id), h = el.offsetHeight || SCR, max = Math.max(0, h - SCR), k = cl((t - t0) / (t1 - t0)), e = k < .5 ? 2 * k * k : 1 - Math.pow(-2 * k + 2, 2) / 2;
  el.style.opacity = 1; el.style.top = (h < SCR ? (SCR - h) / 2 : -max * (a + (b - a) * e)) + 'px';
}
let GOLPES = null;
function animar(t) {
  if (!GOLPES) GOLPES = { cortes: SEC.slice(1).map(s => s.start - 0.06), fuertes: [kw('hook', 'mira'), kw('intro', 'reserva'), kw('cta', 'quieres')] };
  vexLugar(t);
  let fl = 0, z = 0, sx = 0, sy = 0;
  GOLPES.cortes.forEach(h => { if (t >= h) { const e = Math.exp(-(t - h) * 13); fl = Math.max(fl, 0.5 * e); z += 0.03 * Math.exp(-(t - h) * 8); } });
  GOLPES.fuertes.forEach(h => { if (t >= h) { const e = Math.exp(-(t - h) * 9); z += 0.03 * e; sx += Math.sin((t - h) * 80) * 12 * e; sy += Math.cos((t - h) * 67) * 9 * e; } });
  $('flash').style.opacity = fl;
  document.body.style.transform = `translate(${sx}px, ${sy}px) scale(${1 + z})`;
  [...$('barra').children].forEach((el, i) => { const s = SEC[i]; el.firstChild.style.width = (s ? cl((t - s.start) / (s.end - s.start)) * 100 : 0) + '%'; });

  // 1. Gancho: la pregunta cae de golpe y llueven monedas
  const h0 = sec('hook').start; pop($('qq'), h0 + 0.05, t);
  [[120, 760], [820, 700], [60, 1120], [880, 1080], [200, 1380], [760, 1400]].forEach(([x, y], i) => {
    const t0 = h0 + 0.3 + i * 0.16, c = $('co' + i), f = cl((t - t0) / 0.5);
    c.style.left = x + 'px'; c.style.top = (y - 500 * (1 - back(f)) + Math.sin(t * 2 + i) * 14) + 'px';
    c.style.opacity = t >= t0 ? 1 : 0; c.style.transform = `rotate(${Math.sin(t * 1.5 + i) * 18}deg) scaleX(${Math.abs(Math.cos(t * 2.4 + i)) * .5 + .5})`;
  });

  // 2. Presentación: la portada entra girando
  const ir = kw('intro', 'reserva'); pop($('pt'), sec('intro').start + 0.1, t, `rotate(${-4 + Math.sin(t) * 2}deg)`); pop($('pts'), ir, t);

  // 3. El celular entra con el cerebrito y sale antes del cierre; cada escena muestra su captura
  const c0 = sec('cerebrito').start, fin = sec('cta').start - 0.45, ph = cl((t - c0 + 0.3) / 0.55), out = cl((t - fin) / 0.4);
  $('ph').style.opacity = t < c0 - 0.3 ? 0 : 1 - out;
  $('ph').style.transform = `translateX(${(1 - back(ph)) * 640 + out * 700}px) rotate(${(1 - ph) * 12}deg)`;
  document.querySelectorAll('.scr img').forEach(im => im.style.opacity = 0);
  const dep = kw('cerebrito', 'depositas'), d0 = sec('definicion').start, e0 = sec('extracto').start, o0 = sec('hormiga').start, m0 = sec('mitos').start;
  const rec = kw('extracto', 'recibes'), jg = kw('mitos', 'juego');
  if (t < d0 - 0.3) {
    pantalla(t < dep + 0.25 ? 'i-hero0' : 'i-hero1', t, 0, 1);
    const tk = cl((t - dep + 0.2) / 0.5); $('tq').style.opacity = Math.sin(tk * Math.PI); $('tq').style.transform = `scale(${0.6 + tk * 0.6})`;
  } else {
    $('tq').style.opacity = 0;
    if (t < e0 - 0.3) pantalla('i-def', t, d0, e0);
    else if (t < rec) pantalla('i-hab', t, e0 - 0.3, rec, 0, .5);
    else if (t < o0 - 0.3) pantalla('i-ext', t, rec, o0 - 0.4);
    else if (t < m0 - 0.3) pantalla('i-hor', t, o0, m0 - 0.4);
    else if (t < jg) pantalla('i-eps', t, m0 - 0.3, jg, 0, .7);
    else pantalla('i-mit', t, 0, 1);
  }
  pop($('k-ce0'), kw('cerebrito', 'tocas'), t, 'rotate(-3deg)'); pop($('k-ce1'), kw('cerebrito', 'saldo'), t, 'rotate(2deg)');
  pop($('k-de0'), kw('definicion', 'palabra'), t, 'rotate(-2deg)'); pop($('k-de1'), kw('definicion', 'lenguaje'), t, 'rotate(2deg)'); pop($('k-de2'), kw('definicion', 'sencillo'), t, 'rotate(-2deg)');
  pop($('k-ex0'), kw('extracto', 'habitos'), t, 'rotate(-3deg)'); pop($('k-ex1'), kw('extracto', 'extracto'), t, 'rotate(2deg)'); pop($('k-ex2'), kw('extracto', 'consejos'), t, 'rotate(-2deg)');
  pop($('k-ho0'), kw('hormiga', 'alcancia'), t, 'rotate(-3deg)'); pop($('k-ho1'), kw('hormiga', 'plan'), t, 'rotate(2deg)');
  pop($('k-mi0'), kw('mitos', 'episodios'), t, 'rotate(-3deg)'); pop($('k-mi1'), kw('mitos', 'mito'), t, 'rotate(2deg)');

  // 4. Cierre: el enlace y la invitación
  const pr = kw('cta', 'pruebala'), q = kw('cta', 'quieres');
  pop($('url'), pr, t); $('url').style.opacity = Math.min(cl((t - pr) / 0.12), 1 - cl((t - q) / 0.3));
  $('cta').style.opacity = ease((t - q) / 0.4); $('cta').style.transform = `scale(${0.8 + 0.2 * back((t - q) / 0.45)})`;
  $('subs').style.visibility = t >= pr ? 'hidden' : 'visible';
}
'''

MODO = "{ hook: [1.0, 60], intro: [0.5, 400], cta: [0.82, -200] }"
armar(d, 'PROYECTO · WEB INTERACTIVA', MODO, HTML, JS, CSS)
