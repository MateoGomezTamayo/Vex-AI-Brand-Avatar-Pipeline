# LetSprint explicado por Vex, versión dinámica: Vex cambia de lugar en cada escena, cortes con destello y golpe de zoom,
# palabras que entran de golpe y capturas reales de la app (datos de demostración) dentro de un celular.
import sys, pathlib
d = pathlib.Path(__file__).parent; sys.path.insert(0, str(d.parent / 'comun'))
from base_html import armar

CSS = '''.esc { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; opacity: 0; pointer-events: none; }
#flash { position: absolute; inset: 0; background: #fff; opacity: 0; z-index: 50; pointer-events: none; }
#barra { position: absolute; top: 40px; left: 70px; right: 70px; display: flex; gap: 10px; z-index: 40; }
#barra i { flex: 1; height: 8px; border-radius: 8px; background: rgba(255,255,255,.18); overflow: hidden; }
#barra i b { display: block; height: 100%; width: 0; background: #3D9BFF; }
.slam { position: absolute; left: 0; right: 0; text-align: center; font-weight: 800; letter-spacing: -3px; line-height: 1; text-shadow: 0 16px 50px rgba(0,0,0,.55); opacity: 0; }
.ficha { position: absolute; background: #fff; color: #0B1B2E; font-weight: 800; font-size: 34px; border-radius: 22px; padding: 18px 26px; box-shadow: 0 30px 60px -20px rgba(0,0,0,.7); white-space: nowrap; opacity: 0; }
.ficha s { text-decoration: none; display: inline-block; font-size: 24px; color: #fff; border-radius: 10px; padding: 4px 12px; margin-right: 14px; vertical-align: 4px; }
.p1 { background: #DC2626; } .p2 { background: #D97706; } .p3 { background: #2563EB; } .p4 { background: #64748B; }
.logo { font-weight: 800; font-size: 170px; letter-spacing: -6px; }
.logo b { color: #3D9BFF; font-weight: 800; }
.mail { position: absolute; left: 70px; right: 70px; top: 290px; background: #fff; color: #0B1B2E; border-radius: 36px; padding: 36px 44px; box-shadow: 0 50px 100px -30px rgba(0,0,0,.75); }
.mail .de { display: flex; align-items: center; gap: 20px; font-size: 30px; color: #4A5B70; }
.mail .av { width: 70px; height: 70px; border-radius: 50%; background: #D14D72; color: #fff; font-weight: 800; font-size: 34px; display: grid; place-items: center; }
.mail .asunto { font-weight: 800; font-size: 40px; line-height: 1.2; margin: 24px 0 18px; letter-spacing: -.5px; }
.mail .asunto span { color: #0070EB; }
.mail .ln { font-size: 34px; padding: 12px 18px; border-radius: 14px; margin: 4px -18px; font-family: Consolas, monospace; color: #33445A; }
.mail .ln.on { background: #DCEBFF; color: #0B1B2E; font-weight: 700; }
.scan { position: absolute; left: 0; right: 0; height: 120px; background: linear-gradient(180deg, rgba(61,155,255,0), rgba(61,155,255,.35), rgba(61,155,255,0)); opacity: 0; }
.dato { position: absolute; top: 905px; background: #0070EB; color: #fff; font-weight: 800; font-size: 34px; border-radius: 999px; padding: 16px 30px; box-shadow: 0 20px 40px rgba(0,112,235,.5); opacity: 0; }
.nueva { position: absolute; left: 430px; right: 70px; top: 1110px; background: #fff; color: #0B1B2E; border-radius: 30px; padding: 30px 34px; box-shadow: 0 40px 80px -24px rgba(0,0,0,.75); opacity: 0; }
.nueva .k { font-weight: 800; font-size: 24px; letter-spacing: 4px; color: #0070EB; }
.nueva .n { font-weight: 800; font-size: 36px; line-height: 1.2; margin-top: 10px; }
.cont { position: absolute; left: 70px; top: 300px; font-weight: 800; font-size: 300px; line-height: .9; letter-spacing: -12px; font-variant-numeric: tabular-nums; }
.cont small { font-size: 70px; letter-spacing: 0; color: #8FB4DA; margin-left: 12px; }
.badge { position: absolute; right: 80px; top: 330px; background: #DC2626; color: #fff; font-weight: 800; font-size: 150px; border-radius: 40px; padding: 10px 50px; box-shadow: 0 30px 80px rgba(220,38,38,.6); opacity: 0; }
.ya { position: absolute; right: 80px; top: 540px; font-weight: 800; font-size: 54px; color: #FCA5A5; letter-spacing: 6px; opacity: 0; }
.fac { position: absolute; left: 70px; right: 70px; height: 78px; display: flex; align-items: center; gap: 24px; font-size: 36px; font-weight: 700; opacity: 0; }
.fac .nm { width: 300px; color: #DCE8F5; }
.fac .br { flex: 1; height: 26px; border-radius: 26px; background: rgba(255,255,255,.12); overflow: hidden; }
.fac .br b { display: block; height: 100%; width: 0; border-radius: 26px; background: linear-gradient(90deg, #3D9BFF, #7FDBFF); }
.fac .pt { width: 100px; text-align: right; color: #7FDBFF; font-weight: 800; }
.phone { position: absolute; border-radius: 70px; background: #0B1B2E; padding: 16px; box-shadow: 0 60px 120px -30px rgba(0,0,0,.85), 0 0 0 3px #1C3D63; }
.phone .scr { position: relative; width: 100%; height: 100%; border-radius: 56px; overflow: hidden; background: #F4F6FA; }
.phone .scr img { position: absolute; left: 0; top: 0; width: 100%; }
.chip { position: absolute; left: 70px; background: rgba(0,123,255,.22); border: 3px solid rgba(61,155,255,.75); color: #fff; font-weight: 800; font-size: 32px; border-radius: 999px; padding: 14px 28px; white-space: nowrap; opacity: 0; }
.prop { position: absolute; left: 70px; right: 70px; top: 560px; background: #fff; color: #0B1B2E; border-radius: 30px; padding: 30px 34px; display: flex; align-items: center; gap: 24px; box-shadow: 0 40px 80px -24px rgba(0,0,0,.75); }
.prop span { flex: 1; font-size: 36px; font-weight: 600; line-height: 1.25; }
.prop .ap { font-weight: 800; font-size: 36px; color: #fff; background: #2563EB; border-radius: 18px; padding: 18px 30px; white-space: nowrap; }
.toque { position: absolute; width: 110px; height: 110px; border-radius: 50%; border: 8px solid #fff; background: rgba(61,155,255,.35); opacity: 0; }'''

TAREAS = [('p1', 'Error de pago'), ('p2', 'Propuesta retail'), ('p3', 'Dashboard'), ('p2', 'Demo comité'),
          ('p4', 'Documentar API'), ('p1', 'Contrato'), ('p3', 'Soporte'), ('p4', 'Textos landing')]
FICHAS = ''.join(f'<div class="ficha" id="f{i}"><s class="{c}">{c.upper()}</s>{n}</div>' for i, (c, n) in enumerate(TAREAS))
FACT = [('Urgencia', 40), ('Impacto', 30), ('Bloquea a otros', 12), ('Tarea rápida', 4), ('Quién la pide', 8)]
FACS = ''.join(f'<div class="fac" id="fa{i}" style="top:{640 + i * 92}px"><span class="nm">{n}</span><span class="br"><b id="fb{i}"></b></span><span class="pt">+{p}</span></div>' for i, (n, p) in enumerate(FACT))

HTML = f'''
<div id="barra">{''.join('<i><b></b></i>' for _ in range(8))}</div>
<div class="esc" id="c-hook">
  <div class="slam" id="qq" style="top:300px;font-size:110px">¿QUÉ VA<br>PRIMERO?</div>
  {FICHAS}
</div>
<div class="esc" id="c-intro">
  <div class="slam logo" id="lg" style="top:330px">Let<b>Sprint</b></div>
  <div class="slam" id="lgs" style="top:540px;font-size:46px;letter-spacing:1px;color:#BFE3FF;font-weight:700">Prioridades claras para tu equipo</div>
</div>
<div class="esc" id="c-correo">
  <div class="mail" id="ml">
    <div class="de"><div class="av">C</div><div><b style="color:#0B1B2E">cliente@tienda.com</b><br>para sprint@equipo.com</div></div>
    <div class="asunto"><span>[LetSprint]</span> Arreglar error de pago en la tienda</div>
    <div class="ln" id="l0">Fecha límite: hoy 6:00 pm</div>
    <div class="ln" id="l1">Impacto: crítico</div>
    <div class="ln" id="l2">Esfuerzo: unas 2 horas</div>
    <div class="ln" id="l3">Bloquea: sí</div>
    <div class="scan" id="sc"></div>
  </div>
  <div class="dato" id="d0" style="left:70px">Hoy 6 pm</div>
  <div class="dato" id="d1" style="left:345px">Crítico</div>
  <div class="dato" id="d2" style="left:600px">2 horas</div>
  <div class="nueva" id="nv"><div class="k">NUEVA TAREA · ENTRADA</div><div class="n">Arreglar error de pago en la tienda</div></div>
</div>
<div class="esc" id="c-reglas">
  <div class="cont"><span id="num">0</span><small>/100</small></div>
  <div class="badge" id="bd">P1</div>
  <div class="ya" id="ya">SE HACE YA</div>
  {FACS}
</div>
<div class="esc" id="c-tablero">
  <div class="chip" id="t0" style="top:420px">Prioridad visible</div>
  <div class="chip" id="t1" style="top:540px">Quién hace qué</div>
  <div class="chip" id="t2" style="top:660px">Calendario</div>
  <div class="phone" id="ph1" style="left:430px;top:290px;width:580px;height:1210px"><div class="scr">
    <img id="i1" src="img/tablero-doing.webp" alt=""><img id="i2" src="img/calendario.webp" alt="" style="transform:translateX(100%)">
  </div></div>
</div>
<div class="esc" id="c-vex">
  <div class="chip" id="v0" style="top:330px">Organízame el día</div>
  <div class="chip" id="v1" style="top:450px">Balancea la carga</div>
  <div class="chip" id="v2" style="top:570px">Divide tareas</div>
  <div class="chip" id="v3" style="top:690px">Por chat o por voz</div>
  <div class="phone" id="ph2" style="left:500px;top:290px;width:520px;height:1090px"><div class="scr">
    <img id="i3" src="img/vex-resumen.webp" alt=""><img id="i4" src="img/vex-plan.webp" alt="" style="opacity:0">
  </div></div>
</div>
<div class="esc" id="c-control">
  <div class="slam" id="td" style="top:300px;font-size:150px">TÚ DECIDES</div>
  <div class="prop" id="pr"><span>Asignar “Responder dudas de soporte” a Mateo</span><div class="ap" id="ap">Aplicar</div></div>
  <div class="toque" id="tq" style="left:790px;top:610px"></div>
  <div class="slam" id="ns" style="top:830px;font-size:46px;letter-spacing:1px;color:#BFE3FF;font-weight:700">Nada cambia sin tu sí</div>
</div>
<div class="cta" id="cta"><div class="btn">LetSprint para tu equipo</div><p>vextrumlabs.com</p></div>
<div id="flash"></div>
'''

JS = '''
const cl = x => Math.max(0, Math.min(1, x));
const back = x => { x = cl(x); const c1 = 1.9, c3 = c1 + 1; return 1 + c3 * Math.pow(x - 1, 3) + c1 * Math.pow(x - 1, 2); };
// pop: entra de golpe (escala con rebote) y se queda; extra agrega otra transformación (rotación, posición)
const pop = (el, t0, t, extra = '', d = 0.42) => { el.style.opacity = cl((t - t0) / 0.12); el.style.transform = `${extra} scale(${t < t0 ? 0.3 : 0.3 + 0.7 * back((t - t0) / d)})`; };
const SEC = DATOS.secciones;
// Vex cambia de lugar en cada escena: [escala, x, y]
const POS = { hook: [1.0, 0, -20], intro: [0.78, 0, 170], correo: [0.42, -330, 330], reglas: [0.42, 330, 330],
              tablero: [0.42, -330, 330], vex: [0.6, -260, 130], control: [0.5, 0, 300], cta: [0.82, 0, -170] };
function vexLugar(t) {
  let i = 0; while (i < SEC.length - 1 && t >= SEC[i + 1].start - 0.45) i++;
  const a = POS[SEC[Math.max(0, i - 1)].id], b = POS[SEC[i].id], k = i ? back((t - (SEC[i].start - 0.45)) / 0.6) : 1;
  const salto = i ? Math.sin(cl((t - (SEC[i].start - 0.45)) / 0.6) * Math.PI) * 70 : 0;
  const s = a[0] + (b[0] - a[0]) * k, x = a[1] + (b[1] - a[1]) * k, y = a[2] + (b[2] - a[2]) * k - salto;
  $('vex').setAttribute('transform', `translate(${540 + x} ${950 + y}) scale(${s}) translate(-540 -950)`);
}
let GOLPES = null;
function animar(t) {
  if (!GOLPES) GOLPES = { cortes: SEC.slice(1).map(s => s.start - 0.06), fuertes: [kw('intro', 'letsprint'), kw('reglas', 'p1'), kw('control', 'tu')] };
  vexLugar(t);
  // Cortes: destello blanco + golpe de zoom; golpes fuertes: además, sacudida
  let fl = 0, z = 0, sx = 0, sy = 0;
  GOLPES.cortes.forEach(h => { if (t >= h) { const e = Math.exp(-(t - h) * 13); fl = Math.max(fl, 0.55 * e); z += 0.035 * Math.exp(-(t - h) * 8); } });
  GOLPES.fuertes.forEach(h => { if (t >= h) { const e = Math.exp(-(t - h) * 9); z += 0.03 * e; sx += Math.sin((t - h) * 80) * 12 * e; sy += Math.cos((t - h) * 67) * 9 * e; } });
  $('flash').style.opacity = fl;
  document.body.style.transform = `translate(${sx}px, ${sy}px) scale(${1 + z})`;
  // Barra de progreso tipo historias
  [...$('barra').children].forEach((el, i) => { const s = SEC[i]; el.firstChild.style.width = (s ? cl((t - s.start) / (s.end - s.start)) * 100 : 0) + '%'; });

  // 1. Gancho: tareas sueltas flotando en desorden; con "mira" se las traga el centro
  const h0 = sec('hook').start, mira = kw('hook', 'mira');
  pop($('qq'), h0 + 0.05, t);
  const base = [[90, 640, -9], [640, 600, 7], [60, 930, 5], [700, 900, -6], [120, 1220, -4], [660, 1200, 8], [80, 1440, 6], [640, 1460, -7]];
  base.forEach(([bx, by, r], i) => {
    const el = $('f' + i), t0 = h0 + 0.25 + i * 0.13, g = cl((t - mira) / 0.45), gg = g * g;
    const x = bx + Math.sin(t * 1.7 + i) * 26, y = by + Math.cos(t * 1.3 + i * 2) * 22;
    const cx = x + (440 - x) * gg, cy = y + (900 - y) * gg;
    el.style.left = cx + 'px'; el.style.top = cy + 'px';
    pop(el, t0, t, `rotate(${r + Math.sin(t * 2 + i) * 6 + gg * 180}deg)`);
    if (t > mira) el.style.opacity = 1 - gg;
  });
  if (t > mira) $('qq').style.opacity = 1 - cl((t - mira) / 0.3);

  // 2. Presentación: el logo entra de golpe
  const lg = kw('intro', 'letsprint'); pop($('lg'), lg, t); pop($('lgs'), lg + 0.35, t);

  // 3. Correo: la tarjeta entra girando, un barrido la "lee" y cada dato sale como pastilla
  const c0 = sec('correo').start, ml = cl((t - c0 + 0.2) / 0.5);
  $('ml').style.transform = `translateX(${(1 - back(ml)) * 700}px) rotate(${(1 - ml) * 10}deg)`;
  const lee = kw('correo', 'lee'); $('sc').style.opacity = t > lee && t < lee + 1.6 ? 1 : 0; $('sc').style.top = (180 + cl((t - lee) / 1.6) * 360) + 'px';
  ['fecha', 'impacto', 'esfuerzo'].forEach((w, i) => { const k = kw('correo', w); $('l' + i).classList.toggle('on', t >= k); pop($('d' + i), k + 0.12, t, `translateY(${(1 - cl((t - k - 0.12) / 0.3)) * -120}px)`); });
  const nv = kw('correo', 'esfuerzo') + 0.7; pop($('nv'), nv, t, `translateY(${(1 - cl((t - nv) / 0.4)) * 80}px)`);

  // 4. Reglas: cada factor llena su barra y el contador sube hasta 94; P1 cae con sacudida
  const r0 = sec('reglas').start, cien = kw('reglas', 'cien'), p1 = kw('reglas', 'p1');
  const pasos = [r0 + 0.3, r0 + 0.75, r0 + 1.2, r0 + 1.65, r0 + 2.1].map(x => Math.min(x, cien + 0.3));
  const pts = [40, 30, 12, 4, 8]; let total = 0;
  pasos.forEach((p, i) => { pop($('fa' + i), p, t, `translateX(${(1 - cl((t - p) / 0.3)) * -200}px)`, 0.3); const f = cl((t - p) / 0.5); $('fb' + i).style.width = (f * pts[i] / 40 * 100) + '%'; total += pts[i] * f; });
  $('num').textContent = Math.round(total);
  $('num').style.color = t >= kw('reglas', 'noventa') ? '#FCA5A5' : '#fff';
  pop($('bd'), p1, t, 'rotate(-6deg)', 0.35); pop($('ya'), p1 + 0.3, t);

  // 5. Tablero: el celular entra girando, se desplaza y salta al calendario
  const b0 = sec('tablero').start, ph = cl((t - b0 + 0.2) / 0.55);
  $('ph1').style.transform = `translateX(${(1 - back(ph)) * 600}px) rotate(${(1 - ph) * 14}deg)`;
  const cal = kw('tablero', 'calendario'), sw = cl((t - cal + 0.15) / 0.3);
  $('i1').style.transformOrigin = '50% 0'; $('i1').style.transform = `translateX(${-sw * 100}%) scale(${1 + cl((t - b0) / 4) * 0.06})`; $('i2').style.transform = `translateX(${(1 - sw) * 100}%)`;
  pop($('t0'), b0 + 0.2, t); pop($('t1'), kw('tablero', 'quien'), t); pop($('t2'), kw('tablero', 'tablero'), t);

  // 6. Vex organiza: el celular muestra el resumen y luego el plan; las capacidades aparecen al nombrarlas
  const v0 = sec('vex').start, pv = cl((t - v0 + 0.2) / 0.55);
  $('ph2').style.transform = `translateY(${(1 - back(pv)) * 500}px) rotate(${(1 - pv) * -8}deg)`;
  const org = kw('vex', 'organizo'); $('i4').style.opacity = cl((t - org - 0.3) / 0.25); $('i3').style.opacity = 1 - cl((t - org - 0.3) / 0.25);
  pop($('v0'), org, t, 'rotate(-3deg)'); pop($('v1'), kw('vex', 'reparto'), t, 'rotate(2deg)'); pop($('v2'), kw('vex', 'divido'), t, 'rotate(-2deg)'); pop($('v3'), kw('vex', 'voz'), t, 'rotate(3deg)');

  // 7. Control: "TÚ DECIDES" cae de golpe; con "sí" se toca Aplicar
  const tu = kw('control', 'tu'), si = kw('control', 'si', 1);  // la primera es "sin"
  pop($('td'), tu, t); pop($('pr'), sec('control').start + 0.1, t);
  const tq = cl((t - si + 0.25) / 0.5); $('tq').style.opacity = Math.sin(tq * Math.PI); $('tq').style.transform = `scale(${0.6 + tq * 0.6})`;
  const hecho = t >= si; $('ap').textContent = hecho ? 'Aplicado ✓' : 'Aplicar'; $('ap').style.background = hecho ? '#047857' : '#2563EB';
  pop($('ns'), si + 0.2, t);

  // 8. Cierre
  const tc = kw('cta', 'escribenos'); $('cta').style.opacity = ease((t - tc) / 0.4); $('cta').style.transform = `scale(${0.8 + 0.2 * back((t - tc) / 0.45)})`;
  $('subs').style.visibility = t >= tc ? 'hidden' : 'visible';
}
'''

MODO = "{ hook: [1.0, -20], intro: [0.78, 170], correo: [0.42, 330], reglas: [0.42, 330], tablero: [0.42, 330], vex: [0.6, 130], control: [0.5, 300], cta: [0.82, -170] }"
armar(d, 'NUEVO · LETSPRINT', MODO, HTML, JS, CSS)
