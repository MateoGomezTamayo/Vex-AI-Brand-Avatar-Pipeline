# Contabilidad con agentes en Gmail, explicada por Vex: los avisos de pago llegan al correo, un agente los clasifica,
# los anota en la hoja de cuentas, los cruza con los pedidos y manda un resumen nocturno al celular.
# Es el servicio "Conciliación de pagos" de la carta (aún sin casos): todo lo que se ve son DATOS DE EJEMPLO y lo dice.
import sys, pathlib
d = pathlib.Path(__file__).parent; sys.path.insert(0, str(d.parent / 'comun'))
from base_html import armar

CSS = '''.esc { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; opacity: 0; pointer-events: none; }
#flash { position: absolute; inset: 0; background: #fff; opacity: 0; z-index: 50; pointer-events: none; }
#barra { position: absolute; top: 40px; left: 70px; right: 70px; display: flex; gap: 10px; z-index: 40; }
#barra i { flex: 1; height: 8px; border-radius: 8px; background: rgba(255,255,255,.18); overflow: hidden; }
#barra i b { display: block; height: 100%; width: 0; background: #3D9BFF; }
.slam { position: absolute; left: 0; right: 0; text-align: center; font-weight: 800; letter-spacing: -3px; line-height: 1; text-shadow: 0 16px 50px rgba(0,0,0,.55); opacity: 0; }
.papel { position: absolute; background: #FFFDF5; color: #33445A; font-weight: 700; font-size: 32px; border-radius: 10px; padding: 16px 22px; box-shadow: 0 24px 50px -16px rgba(0,0,0,.7); white-space: nowrap; font-family: Consolas, monospace; opacity: 0; }
.ej { position: absolute; font-size: 24px; font-weight: 700; letter-spacing: 3px; color: #8FB4DA; }
/* Bandeja tipo Gmail */
.inbox { position: absolute; left: 70px; right: 70px; top: 270px; background: #fff; color: #0B1B2E; border-radius: 34px; padding: 26px 0 12px; box-shadow: 0 50px 100px -30px rgba(0,0,0,.75); overflow: hidden; }
.inbox .hd { display: flex; align-items: center; gap: 16px; padding: 0 34px 20px; font-weight: 800; font-size: 34px; border-bottom: 2px solid #E3E9F1; }
.inbox .hd i { width: 46px; height: 34px; border-radius: 6px; background: linear-gradient(135deg, #EA4335 0 33%, #FBBC05 33% 66%, #34A853 66%); }
.msg { position: relative; display: flex; align-items: center; gap: 20px; padding: 22px 34px; border-bottom: 2px solid #EEF2F7; opacity: 0; }
.msg .av { width: 64px; height: 64px; border-radius: 50%; color: #fff; font-weight: 800; font-size: 30px; display: grid; place-items: center; flex: none; }
.msg .tx { flex: 1; min-width: 0; }
.msg .de { font-weight: 800; font-size: 30px; }
.msg .as { font-size: 27px; color: #4A5B70; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.etq { font-weight: 800; font-size: 26px; border-radius: 999px; padding: 8px 18px; color: #fff; opacity: 0; flex: none; }
.ing { background: #047857; } .gas { background: #DC2626; } .ped { background: #2563EB; }
.scan { position: absolute; left: 0; right: 0; height: 130px; background: linear-gradient(180deg, rgba(61,155,255,0), rgba(61,155,255,.35), rgba(61,155,255,0)); opacity: 0; }
/* Hoja de cuentas */
.hoja { position: absolute; left: 70px; right: 70px; top: 290px; background: #fff; color: #0B1B2E; border-radius: 30px; overflow: hidden; box-shadow: 0 50px 100px -30px rgba(0,0,0,.75); }
.hoja .tt { background: #0F9D58; color: #fff; font-weight: 800; font-size: 32px; padding: 20px 30px; display: flex; justify-content: space-between; }
.fila { display: grid; grid-template-columns: 150px 1fr 200px 230px; gap: 0; font-size: 30px; border-bottom: 2px solid #E3E9F1; opacity: 0; }
.fila > span { padding: 18px 22px; border-right: 2px solid #E3E9F1; white-space: nowrap; overflow: hidden; }
.fila > span:last-child { border-right: 0; text-align: right; font-weight: 800; font-variant-numeric: tabular-nums; }
.fila.cab { background: #F1F5F9; font-weight: 800; font-size: 26px; color: #4A5B70; opacity: 1; }
.verde { color: #047857; } .rojo { color: #DC2626; }
/* Cruce pagos ↔ pedidos */
.col { position: absolute; top: 300px; width: 420px; }
.col .k { font-weight: 800; font-size: 28px; letter-spacing: 4px; color: #8FB4DA; margin-bottom: 18px; }
.blo { background: #fff; color: #0B1B2E; border-radius: 24px; padding: 22px 26px; margin-bottom: 26px; font-weight: 800; font-size: 34px; box-shadow: 0 30px 60px -20px rgba(0,0,0,.7); opacity: 0; }
.blo small { display: block; font-size: 24px; color: #4A5B70; font-weight: 600; margin-top: 4px; }
.lin { position: absolute; height: 8px; border-radius: 8px; background: #34D399; transform-origin: 0 50%; transform: scaleX(0); }
.alerta { position: absolute; left: 70px; right: 70px; top: 1000px; background: #DC2626; color: #fff; font-weight: 800; font-size: 40px; border-radius: 26px; padding: 26px 34px; text-align: center; box-shadow: 0 30px 80px rgba(220,38,38,.55); opacity: 0; }
/* Notificación en el celular */
.phone { position: absolute; left: 480px; top: 300px; width: 500px; height: 960px; border-radius: 70px; background: #0B1B2E; padding: 16px; box-shadow: 0 60px 120px -30px rgba(0,0,0,.85), 0 0 0 3px #1C3D63; }
.phone .scr { position: relative; width: 100%; height: 100%; border-radius: 56px; overflow: hidden; background: linear-gradient(160deg, #1E3A5F, #0B1B2E 60%); }
.phone .hora { position: absolute; top: 120px; left: 0; right: 0; text-align: center; font-weight: 300; font-size: 130px; color: #fff; letter-spacing: -4px; }
.phone .fec { position: absolute; top: 280px; left: 0; right: 0; text-align: center; font-size: 30px; color: #BFE3FF; }
.noti { position: absolute; left: 22px; right: 22px; top: 380px; background: rgba(255,255,255,.95); color: #0B1B2E; border-radius: 30px; padding: 22px 24px; opacity: 0; }
.noti .ap { font-size: 22px; font-weight: 800; color: #4A5B70; letter-spacing: 2px; }
.noti .t { font-weight: 800; font-size: 30px; margin: 8px 0 10px; }
.noti .r { display: flex; justify-content: space-between; font-size: 27px; padding: 5px 0; }
.noti .r b { font-variant-numeric: tabular-nums; }
.chip { position: absolute; left: 70px; background: rgba(0,123,255,.22); border: 3px solid rgba(61,155,255,.75); color: #fff; font-weight: 800; font-size: 36px; border-radius: 999px; padding: 16px 30px; white-space: nowrap; opacity: 0; }
.chip.no { background: rgba(220,38,38,.18); border-color: rgba(252,165,165,.8); }
.logo { font-weight: 800; font-size: 120px; letter-spacing: -4px; }
.dedo { position: absolute; width: 96px; height: 96px; border-radius: 50%; border: 7px solid #fff; background: rgba(61,155,255,.35); box-shadow: 0 10px 30px rgba(0,0,0,.5); opacity: 0; z-index: 30; }
.cnt { margin-left: auto; background: #DC2626; color: #fff; font-size: 26px; font-weight: 800; border-radius: 999px; padding: 4px 16px; min-width: 50px; text-align: center; }
.total { display: grid; grid-template-columns: 1fr 230px; background: #0B1B2E; color: #fff; font-weight: 800; font-size: 32px; }
.total span { padding: 20px 22px; } .total span:last-child { text-align: right; font-variant-numeric: tabular-nums; }
.ok { position: absolute; width: 74px; height: 74px; border-radius: 50%; background: #34D399; color: #0B1B2E; font-weight: 900; font-size: 46px; display: grid; place-items: center; box-shadow: 0 10px 30px rgba(52,211,153,.6); opacity: 0; }
.barras { display: flex; align-items: flex-end; gap: 18px; height: 110px; margin-top: 12px; padding: 0 6px; }
.barras i { flex: 1; border-radius: 10px 10px 4px 4px; height: 0; }
.barras small { display: block; text-align: center; font-size: 20px; color: #4A5B70; font-weight: 700; margin-top: 6px; }
.candado { position: absolute; left: 110px; top: 1000px; font-size: 150px; opacity: 0; }
.logo b { color: #3D9BFF; font-weight: 800; }'''

PAPELES = [('$85.000', 90, 640, -8), ('Transferencia', 600, 600, 6), ('Nequi $40.000', 60, 900, 5), ('Factura #318', 640, 880, -5),
           ('$1.200.000', 120, 1180, -4), ('Pedido #1042', 620, 1160, 7)]
PAP = ''.join(f'<div class="papel" id="pp{i}">{n}</div>' for i, (n, *_ ) in enumerate(PAPELES))
CORREOS = [('B', '#FDDA24', '#0B1B2E', 'Bancolombia', 'Recibiste una transferencia por $350.000', 'ing', 'Ingreso'),
           ('N', '#8A2BE2', '#fff', 'Nequi', 'Te enviaron $85.000', 'ing', 'Ingreso'),
           ('T', '#2563EB', '#fff', 'Tu tienda', 'Nuevo pedido #1042 por $350.000', 'ped', 'Pedido'),
           ('P', '#64748B', '#fff', 'Proveedor', 'Factura #318 por $1.200.000', 'gas', 'Gasto')]
MSGS = ''.join(f'<div class="msg" id="m{i}"><div class="av" style="background:{bg};color:{fg}">{a}</div>'
               f'<div class="tx"><div class="de">{de}</div><div class="as">{asu}</div></div><span class="etq {c}" id="e{i}">{lab}</span></div>'
               for i, (a, bg, fg, de, asu, c, lab) in enumerate(CORREOS))
FILAS = [('20 nov', 'Transferencia · Ana R.', 'Ingreso', '+$350.000', 'verde'), ('20 nov', 'Nequi · Luis P.', 'Ingreso', '+$85.000', 'verde'),
         ('20 nov', 'Proveedor · Fact. 318', 'Gasto', '−$1.200.000', 'rojo')]
FIL = ''.join(f'<div class="fila" id="r{i}"><span>{f}</span><span>{c}</span><span>{k}</span><span class="{cl}">{v}</span></div>' for i, (f, c, k, v, cl) in enumerate(FILAS))

HTML = f'''
<div id="barra">{''.join('<i><b></b></i>' for _ in range(8))}</div>
<div class="esc" id="c-hook">
  <div class="slam" id="qq" style="top:300px;font-size:120px">¿A MANO?</div>
  {PAP}
</div>
<div class="esc" id="c-intro">
  <div class="slam logo" id="lg" style="top:330px">Contabilidad<br>en <b>piloto</b><br><b>automático</b></div>
</div>
<div class="esc" id="c-correo">
  <div class="inbox" id="ib"><div class="hd"><i></i>Recibidos<span class="cnt" id="ibc">0</span></div>{MSGS}<div class="scan" id="sc"></div></div>
  <div class="ej" style="left:70px;top:1010px">DATOS DE EJEMPLO</div>
  <div class="dedo" id="dd"></div>
</div>
<div class="esc" id="c-registro">
  <div class="hoja" id="hj"><div class="tt"><span>Cuentas · noviembre</span><span>Google Sheets</span></div>
    <div class="fila cab"><span>Fecha</span><span>Concepto</span><span>Tipo</span><span>Valor</span></div>{FIL}<div class="total"><span>Saldo del día</span><span id="tot">$0</span></div></div>
  <div class="ej" style="left:70px;top:900px">DATOS DE EJEMPLO</div>
</div>
<div class="esc" id="c-cruce">
  <div class="col" style="left:70px"><div class="k">PAGOS</div>
    <div class="blo" id="pa0">$350.000<small>Transferencia · Ana R.</small></div>
    <div class="blo" id="pa1">$85.000<small>Nequi · Luis P.</small></div></div>
  <div class="col" style="left:590px"><div class="k">PEDIDOS</div>
    <div class="blo" id="pe0">#1042<small>$350.000 · Ana R.</small></div>
    <div class="blo" id="pe1" style="background:#FEE2E2;color:#DC2626">?<small style="color:#DC2626">sin pedido</small></div></div>
  <div class="lin" id="ln0" style="left:490px;top:395px;width:100px"></div>
  <div class="ok" id="ok0" style="left:503px;top:362px">✓</div>
  <div class="alerta" id="al">⚠ Pago de $85.000 sin pedido</div>
</div>
<div class="esc" id="c-aviso">
  <div class="phone" id="ph"><div class="scr"><div class="hora">9:00</div><div class="fec">viernes, 20 de noviembre</div>
    <div class="noti" id="nt"><div class="ap">VEXTRUM · CUENTAS</div><div class="t">Resumen de hoy</div>
      <div class="r"><span>Entró</span><b class="verde" id="n0">$0</b></div>
      <div class="r"><span>Salió</span><b class="rojo" id="n1">$0</b></div>
      <div class="r"><span>Por cobrar</span><b id="n2">0 pedidos</b></div>
      <div class="barras"><div style="flex:1"><i id="b0" style="background:#047857;display:block"></i><small>Entró</small></div><div style="flex:1"><i id="b1" style="background:#DC2626;display:block"></i><small>Salió</small></div></div></div>
  </div></div>
  <div class="ej" style="left:480px;top:1285px">DATOS DE EJEMPLO</div>
</div>
<div class="esc" id="c-control">
  <div class="slam" id="sl" style="top:300px;font-size:120px">SOLO LEE<br>Y AVISA</div>
  <div class="chip no" id="k0" style="top:620px">✕ No envía correos</div>
  <div class="chip no" id="k1" style="top:740px">✕ No borra nada</div>
  <div class="chip no" id="k2" style="top:860px">✕ No mueve tu dinero</div>
  <div class="candado" id="lk">🔒</div>
</div>
<div class="cta" id="cta"><div class="btn">Tu contabilidad, en automático</div><p>vextrumlabs.com</p></div>
<div id="flash"></div>
'''

JS = '''
const cl = x => Math.max(0, Math.min(1, x));
const back = x => { x = cl(x); const c1 = 1.9, c3 = c1 + 1; return 1 + c3 * Math.pow(x - 1, 3) + c1 * Math.pow(x - 1, 2); };
const pop = (el, t0, t, extra = '', d = 0.42) => { el.style.opacity = cl((t - t0) / 0.12); el.style.transform = `${extra} scale(${t < t0 ? 0.3 : 0.3 + 0.7 * back((t - t0) / d)})`; };
const pesos = v => '$' + Math.round(v).toString().replace(/\\B(?=(\\d{3})+(?!\\d))/g, '.');
const SEC = DATOS.secciones;
const POS = { hook: [1.0, 0, -20], intro: [0.8, 0, 220], correo: [0.42, 330, 360], registro: [0.42, -330, 330],
              cruce: [0.42, 330, 360], aviso: [0.42, -340, 360], control: [0.5, 260, 300], cta: [0.82, 0, -170] };
function vexLugar(t) {
  let i = 0; while (i < SEC.length - 1 && t >= SEC[i + 1].start - 0.45) i++;
  const a = POS[SEC[Math.max(0, i - 1)].id], b = POS[SEC[i].id], k = i ? back((t - (SEC[i].start - 0.45)) / 0.6) : 1;
  let salto = i ? Math.sin(cl((t - (SEC[i].start - 0.45)) / 0.6) * Math.PI) * 70 : 0;
  (window.BRINCOS || []).forEach(h => { if (t >= h && t < h + 0.45) salto += Math.sin((t - h) / 0.45 * Math.PI) * 55; });
  const s = a[0] + (b[0] - a[0]) * k, x = a[1] + (b[1] - a[1]) * k, y = a[2] + (b[2] - a[2]) * k - salto;
  $('vex').setAttribute('transform', `translate(${540 + x} ${950 + y}) scale(${s}) translate(-540 -950)`);
}
let GOLPES = null;
function animar(t) {
  if (!GOLPES) GOLPES = { cortes: SEC.slice(1).map(s => s.start - 0.06), fuertes: [kw('intro', 'piloto'), kw('cruce', 'avisa'), kw('control', 'solo')] };
  if (!window.BRINCOS) window.BRINCOS = [kw('correo', 'clasifica'), kw('cruce', 'avisa'), kw('aviso', 'celular'), kw('control', 'solo'), kw('cta', 'escribenos')];
  vexLugar(t);
  let fl = 0, z = 0, sx = 0, sy = 0;
  GOLPES.cortes.forEach(h => { if (t >= h) { const e = Math.exp(-(t - h) * 13); fl = Math.max(fl, 0.55 * e); z += 0.035 * Math.exp(-(t - h) * 8); } });
  GOLPES.fuertes.forEach(h => { if (t >= h) { const e = Math.exp(-(t - h) * 9); z += 0.03 * e; sx += Math.sin((t - h) * 80) * 12 * e; sy += Math.cos((t - h) * 67) * 9 * e; } });
  $('flash').style.opacity = fl;
  document.body.style.transform = `translate(${sx}px, ${sy}px) scale(${1 + z})`;
  [...$('barra').children].forEach((el, i) => { const s = SEC[i]; el.firstChild.style.width = (s ? cl((t - s.start) / (s.end - s.start)) * 100 : 0) + '%'; });

  // 1. Gancho: papelitos de pagos en desorden; con "mira" se los traga el centro
  const h0 = sec('hook').start, mira = kw('hook', 'mira');
  pop($('qq'), h0 + 0.05, t);
  const base = [[90, 640, -8], [600, 600, 6], [60, 900, 5], [640, 880, -5], [120, 1180, -4], [620, 1160, 7]];
  base.forEach(([bx, by, r], i) => {
    const el = $('pp' + i), g = cl((t - mira) / 0.45), gg = g * g;
    const x = bx + Math.sin(t * 1.7 + i) * 24, y = by + Math.cos(t * 1.3 + i * 2) * 20;
    el.style.left = (x + (430 - x) * gg) + 'px'; el.style.top = (y + (900 - y) * gg) + 'px';
    pop(el, h0 + 0.3 + i * 0.15, t, `rotate(${r + Math.sin(t * 2 + i) * 6 + gg * 200}deg)`);
    if (t > mira) el.style.opacity = 1 - gg;
  });
  if (t > mira) $('qq').style.opacity = 1 - cl((t - mira) / 0.3);

  // 2. Presentación
  pop($('lg'), kw('intro', 'contabilidad'), t);

  // 3. Correo: llegan los avisos uno a uno; con "lee" pasa el barrido y salen las etiquetas
  const c0 = sec('correo').start, ib = cl((t - c0 + 0.2) / 0.5);
  $('ib').style.transform = `translateY(${(1 - back(ib)) * 300}px)`;
  [0, 1, 2, 3].forEach(i => { const k = c0 + 0.2 + i * 0.32; $('m' + i).style.opacity = cl((t - k) / 0.2); $('m' + i).style.transform = `translateX(${(1 - back(cl((t - k) / 0.4))) * 260}px)`; });
  const lee = kw('correo', 'lee'); $('sc').style.opacity = t > lee && t < lee + 1.3 ? 1 : 0; $('sc').style.top = (60 + cl((t - lee) / 1.3) * 480) + 'px';
  const tipo = { 0: 'ingreso', 1: 'ingreso', 2: 'pedido', 3: 'gasto' };
  [0, 1, 2, 3].forEach(i => pop($('e' + i), kw('correo', tipo[i]) + i * 0.08, t, '', 0.35));
  $('ibc').textContent = [0, 1, 2, 3].filter(i => t >= c0 + 0.2 + i * 0.32).length;
  const taps = [0, 1, 2, 3].map(i => kw('correo', tipo[i]) + i * 0.08);
  let k = -1; taps.forEach((h, i) => { if (t >= h - 0.25) k = i; });
  const dd = $('dd');
  if (k >= 0 && t < taps[3] + 0.8) {
    const ib = $('ib').getBoundingClientRect(), row = $('m' + k).getBoundingClientRect(), f = cl((t - taps[k] + 0.25) / 0.25);
    dd.style.left = (row.right - 140) + 'px'; dd.style.top = (row.top + row.height / 2 - 48) + 'px';
    dd.style.opacity = 0.9; dd.style.transform = `scale(${1.25 - 0.45 * Math.sin(f * Math.PI)})`;
  } else dd.style.opacity = 0;

  // 4. Registro: la hoja entra y cada fila se escribe sola
  const r0 = sec('registro').start, hj = cl((t - r0 + 0.2) / 0.5);
  $('hj').style.transform = `translateX(${(1 - back(hj)) * -700}px) rotate(${(1 - hj) * -6}deg)`;
  const fe = kw('registro', 'fecha'), cli = kw('registro', 'cliente'), va = kw('registro', 'valor');
  const VAL = [350000, 85000, -1200000]; let tot = 0;
  [fe, cli, va].forEach((k, i) => { const f = $('r' + i), w = cl((t - k) / 0.55); f.style.opacity = t >= k ? 1 : 0; f.style.clipPath = `inset(0 ${(1 - w) * 100}% 0 0)`; f.style.background = t > k && t < k + 0.9 ? '#DCFCE7' : '#fff'; tot += VAL[i] * cl((t - k - 0.3) / 0.5); });
  $('tot').textContent = (tot < 0 ? '−' : '') + pesos(Math.abs(tot)); $('tot').style.color = tot < 0 ? '#FCA5A5' : '#6EE7B7';

  // 5. Cruce: pago y pedido se unen con una línea; el pago sin pedido dispara la alerta
  const x0 = sec('cruce').start;
  pop($('pa0'), x0 + 0.1, t); pop($('pa1'), x0 + 0.35, t); pop($('pe0'), kw('cruce', 'pedidos'), t);
  const une = kw('cruce', 'pedidos') + 0.25, u = Math.sin(cl((t - une) / 0.7) * Math.PI);
  $('pa0').style.transform += ` translateX(${u * 60}px)`; $('pe0').style.transform += ` translateX(${-u * 60}px)`;
  pop($('ok0'), une + 0.45, t, '', 0.4);
  const sacude = kw('cruce', 'avisa'); if (t > sacude) $('pa1').style.transform += ` translateX(${Math.sin((t - sacude) * 40) * 14 * Math.exp(-(t - sacude) * 4)}px)`;
  $('ln0').style.transform = `scaleX(${cl((t - kw('cruce', 'pedidos') - 0.25) / 0.35)})`;
  const sin = kw('cruce', 'pago'); pop($('pe1'), sin, t);
  pop($('al'), kw('cruce', 'avisa'), t, `rotate(${Math.sin(Math.max(0, t - kw('cruce', 'avisa')) * 18) * 3 * Math.exp(-(t - kw('cruce', 'avisa')) * 3)}deg)`);

  // 6. Aviso nocturno: la notificación baja y los valores cuentan
  const a0 = sec('aviso').start, ph = cl((t - a0 + 0.2) / 0.55);
  $('ph').style.transform = `translateY(${(1 - back(ph)) * 500}px)`;
  const nt = kw('aviso', 'celular'); $('nt').style.opacity = cl((t - nt) / 0.2); $('nt').style.transform = `translateY(${(1 - back(cl((t - nt) / 0.45))) * -160}px)`;
  const vib = t > nt && t < nt + 0.7 ? Math.sin((t - nt) * 90) * 3.5 : 0;
  $('ph').style.transform += ` rotate(${vib}deg)`;
  const en = kw('aviso', 'entro'), sa = kw('aviso', 'salio'), co = kw('aviso', 'cobrar');
  $('n0').textContent = pesos(435000 * cl((t - en) / 0.6)); $('n1').textContent = pesos(1200000 * cl((t - sa) / 0.6));
  $('n2').textContent = (t >= co ? 1 : 0) + ' pedido' + (t >= co ? '' : 's');
  $('b0').style.height = (cl((t - en) / 0.6) * 0.27 * 100) + 'px'; $('b1').style.height = (cl((t - sa) / 0.6) * 100) + 'px';

  // 7. Control: "SOLO LEE Y AVISA" cae de golpe; las tres garantías aparecen al nombrarlas
  pop($('sl'), kw('control', 'solo'), t);
  pop($('k0'), kw('control', 'envia'), t, 'rotate(-2deg)'); pop($('k1'), kw('control', 'borra'), t, 'rotate(2deg)'); pop($('k2'), kw('control', 'mueve'), t, 'rotate(-1deg)');
  pop($('lk'), kw('control', 'dinero') + 0.25, t, '', 0.4);

  // 8. Cierre
  const tc = kw('cta', 'escribenos'); $('cta').style.opacity = ease((t - tc) / 0.4); $('cta').style.transform = `scale(${0.8 + 0.2 * back((t - tc) / 0.45)})`;
  $('subs').style.visibility = t >= tc ? 'hidden' : 'visible';
}
'''

MODO = "{ hook: [1.0, -20], intro: [0.8, 220], correo: [0.42, 360], registro: [0.42, 330], cruce: [0.42, 360], aviso: [0.42, 360], control: [0.5, 300], cta: [0.82, -170] }"
armar(d, 'IDEA · CONTABILIDAD CON IA', MODO, HTML, JS, CSS)
