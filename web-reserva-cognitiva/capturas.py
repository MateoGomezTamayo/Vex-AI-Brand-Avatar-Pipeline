# Capturas reales de tureservacognitiva.vercel.app en un celular (390 px, pantalla x2) para el video. Escribe img/*.webp
import pathlib, io
from playwright.sync_api import sync_playwright
from PIL import Image
D = pathlib.Path(__file__).parent / 'img'; URL = 'https://tureservacognitiva.vercel.app/'
def guarda(png, nombre):
    Image.open(io.BytesIO(png)).convert('RGB').save(D / f'{nombre}.webp', quality=88); print(nombre)
with sync_playwright() as pw:
    b = pw.chromium.launch(channel='chrome')
    p = b.new_page(viewport={'width': 390, 'height': 844}, device_scale_factor=2, is_mobile=True, has_touch=True)
    p.goto(URL); p.add_style_tag(content='.guide,.toast{display:none!important}'); p.wait_for_timeout(1800)
    guarda(p.screenshot(), 'hero-0')
    for _ in range(3): p.click('#brainBtn'); p.wait_for_timeout(700)
    p.wait_for_timeout(900); guarda(p.screenshot(), 'hero-1')
    sec = lambda s: p.locator(s).screenshot(animations='disabled')
    for k in ['capacidad', 'prevenir', 'tolerar']: p.click(f'.k[data-k={k}]'); p.wait_for_timeout(200)
    p.wait_for_timeout(600); guarda(p.locator('#que-es .def-grid').screenshot(), 'definicion')
    p.fill('#reserva', '85'); p.dispatch_event('#reserva', 'input'); p.wait_for_timeout(300)
    guarda(p.locator('#que-es .model').screenshot(), 'grafica')
    vals = [2, 1, 2, 1, 0, 2, 0, 1, 2, 1]
    for k, v in zip(['leer', 'aprender', 'retos', 'mover', 'bailar', 'conversar', 'comunidad', 'dormir', 'salud', 'hobby'], vals):
        p.click(f'input[name={k}][value="{v}"]'); p.wait_for_timeout(60)
    p.wait_for_timeout(1500)
    guarda(p.locator('#habits').screenshot(), 'habitos')
    guarda(p.locator('#receipt').screenshot(), 'extracto')
    for k in ['llamar', 'paginas', 'caminar']: p.click(f'.chip[data-k={k}]'); p.wait_for_timeout(300)
    p.wait_for_timeout(1200)
    guarda(p.locator('#hormiga').screenshot(), 'hormiga')
    p.click('.ep >> nth=0'); p.wait_for_timeout(900)
    guarda(p.locator('#cards').screenshot(), 'episodios')
    p.click('.vote.real'); p.wait_for_timeout(900)  # frase 1 es mito: muestra la corrección
    p.click('#nextMyth'); p.wait_for_timeout(700); p.click('.vote.real'); p.wait_for_timeout(1000)
    guarda(p.locator('#mitos .myth-stage').screenshot(), 'mitos')
    b.close()
