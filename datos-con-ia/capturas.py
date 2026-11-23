# Captura pantallas reales de https://datos-con-ia.vercel.app (vista de celular, alta resolución) para el video.
# Salen en tmp/capturas/ (fuera de git). Hace una pregunta real a Vex (Claude Haiku, cuesta una fracción de centavo).
import pathlib
from playwright.sync_api import sync_playwright

D = pathlib.Path(__file__).parent / 'tmp' / 'capturas'; D.mkdir(parents=True, exist_ok=True)
URL = 'https://datos-con-ia.vercel.app'

with sync_playwright() as pw:
    b = pw.chromium.launch(channel='chrome')
    pg = b.new_page(viewport={'width': 390, 'height': 844}, device_scale_factor=2.5, color_scheme='light')

    # 1. Inicio
    pg.goto(URL + '/'); pg.wait_for_timeout(1200)
    pg.screenshot(path=str(D / '1-inicio.png'))

    # 2. Lección 2: una celda ejecutada con Python en el navegador
    pg.goto(URL + '/carga-y-conoce'); pg.wait_for_timeout(800)
    celda = pg.locator('[data-celda]').nth(1)            # df.head()
    celda.scroll_into_view_if_needed()
    celda.locator('[data-run]').click()
    pg.wait_for_function("() => { const v = document.querySelectorAll('[data-celda]')[1].nextElementSibling; return v && v.querySelector('.out__tabla'); }", timeout=180000)
    pg.wait_for_timeout(500)
    pg.evaluate("() => { const c = document.querySelectorAll('[data-celda]')[1]; window.scrollTo(0, c.getBoundingClientRect().top + scrollY - 150); }")
    pg.wait_for_timeout(300); pg.screenshot(path=str(D / '2-ejecutar.png'))

    # 3. Palabra explicada al tocarla (glosario)
    t = pg.locator('.intro .term, .paso .term').first
    t.scroll_into_view_if_needed()
    pg.evaluate("() => { const t = document.querySelector('.intro .term, .paso .term'); window.scrollTo(0, t.getBoundingClientRect().top + scrollY - 260); }")
    pg.wait_for_timeout(200); t.click(); pg.wait_for_timeout(300)
    pg.screenshot(path=str(D / '3-palabra.png'))
    pg.keyboard.press('Escape')

    # 4. Vex respondiendo (pregunta real)
    pg.locator('[data-vex-abrir]').click(); pg.wait_for_timeout(300)
    pg.fill('#vex-q', '¿Qué es un DataFrame? Nunca he programado.')
    pg.locator('[data-vex-form] button').click()
    pg.wait_for_function("() => { const m = [...document.querySelectorAll('.vex-msg')].pop(); return m && !m.classList.contains('vex-msg--pensando') && m.classList.contains('vex-msg--vex') && document.querySelectorAll('.vex-msg').length >= 3; }", timeout=60000)
    pg.wait_for_timeout(500)
    pg.evaluate("() => { const m = document.querySelector('.vex-msgs'); m.scrollTop = 0; }")
    pg.screenshot(path=str(D / '4-vex.png'))
    pg.locator('[data-vex-cerrar]').click()

    # 5. Quiz respondido
    q = pg.locator('[data-quiz]').first
    q.scroll_into_view_if_needed()
    q.locator('.quiz__op[data-ok="1"]').click(); pg.wait_for_timeout(300)
    pg.evaluate("() => { const q = document.querySelector('[data-quiz]'); window.scrollTo(0, q.getBoundingClientRect().top + scrollY - 120); }")
    pg.wait_for_timeout(200); pg.screenshot(path=str(D / '5-quiz.png'))

    # 6. Asesoría por WhatsApp (bloque del inicio)
    pg.goto(URL + '/'); pg.wait_for_timeout(800)
    pg.evaluate("() => { const a = document.querySelector('.asesoria'); window.scrollTo(0, a.getBoundingClientRect().top + scrollY - 200); }")
    pg.wait_for_timeout(300); pg.screenshot(path=str(D / '6-whatsapp.png'))
    b.close()
print('capturas en', D)
