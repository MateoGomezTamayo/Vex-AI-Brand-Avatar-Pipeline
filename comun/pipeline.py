# Arma un video de Vex de punta a punta: voz → boca (Rhubarb) → datos → HTML → MP4.
# Uso: pipeline.py <carpeta_video> <salida.mp4>              (video completo)
#      pipeline.py <carpeta_video> - 3.0,15.2               (solo cuadros de muestra en PNG, en <carpeta>/tmp)
# La carpeta del video tiene guion.json (frases con tono) y armar_html.py (tarjetas propias del video).
import sys, json, wave, re, time, unicodedata, subprocess, pathlib, numpy as np
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from voz_vex import voz, FF
from rutas import RHUBARB
MUSICA = pathlib.Path(__file__).parent.parent / 'musica' / 'fondo-vex.wav'  # se genera con musica.py; si no existe, el video va sin música
VOL_MUSICA = 0.14

def datos(carpeta, tmp):
    """Une voz.json + boca.json + energía del audio en datos.json (subtítulos con la puntuación del guion)."""
    v = json.load(open(tmp / 'voz.json', encoding='utf-8'))
    guion = json.loads((carpeta / 'guion.json').read_text(encoding='utf-8'))
    w = wave.open(str(tmp / 'voz.wav')); a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
    hop = w.getframerate() // 30; n = len(a) // hop
    rms = np.sqrt(np.array([np.mean(a[i*hop:(i+1)*hop] ** 2) for i in range(n)]))
    env = np.convolve(np.clip(rms / np.percentile(rms[rms > 0.01], 95), 0, 1), np.ones(3) / 3, 'same')
    norm = lambda s: re.sub(r'[^a-z0-9]', '', unicodedata.normalize('NFD', s.lower()).encode('ascii', 'ignore').decode())
    tokens = ' '.join(f for s in guion for f, _ in s['frases']).split()
    pal, k = [], 0
    for a0, b0, wtxt in [p for p in v['palabras'] if norm(p[2])]:  # algunas voces emiten "palabras" vacías  # alinea cada palabra de la voz con el token del guion (con tildes y signos)
        obj = norm(wtxt); acc, j = '', k
        while j < len(tokens) and len(acc) < len(obj): acc += norm(tokens[j]); j += 1
        pal.append([a0, b0, ' '.join(tokens[k:j]) if acc == obj else wtxt]); k = j if acc == obj else k + 1
    numeros = {'dos': '2', 'tres': '3', 'cuatro': '4', 'cinco': '5'}  # "Día dos" se lee así, pero se subtitula "Día 2"
    for i in range(1, len(pal)):
        if norm(pal[i - 1][2]) == 'dia' and norm(pal[i][2]) in numeros:
            pal[i][2] = re.sub(r'[a-zA-Z]+', numeros[norm(pal[i][2])], pal[i][2])
    grupos, g = [], []
    for p in pal:
        g.append(p)
        if len(g) == 4 or p[2][-1] in '.?!,:…': grupos.append(g); g = []
    if g: grupos.append(g)
    boca = json.load(open(tmp / 'boca.json'))['mouthCues']
    json.dump({'env': [round(float(x), 3) for x in env], 'boca': boca, 'grupos': grupos, 'secciones': v['secciones'], 'dur': v['dur']},
              open(tmp / 'datos.json', 'w', encoding='utf-8'), ensure_ascii=False)
    sin = [p[2] for p in pal if norm(p[2]) not in {norm(t) for t in tokens}]
    print(len(grupos), 'grupos de subtítulos', '· sin alinear:', sin if sin else 'ninguna')

def render(html, tmp, salida, muestras=None):
    from playwright.sync_api import sync_playwright
    d = (tmp / 'datos.json').read_text(encoding='utf-8')
    with sync_playwright() as pw:
        b = pw.chromium.launch(channel='chrome'); pg = b.new_page(viewport={'width': 1080, 'height': 1920})
        pg.add_init_script(f'window.DATOS = {d};')
        pg.goto(html.as_uri()); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(400)
        if muestras:
            for t in muestras: pg.evaluate(f'render({t})'); pg.screenshot(path=str(tmp / f'muestra-{t}.png'))
            b.close(); return
        dur = json.loads(d)['dur']; total = round(dur * 30)
        audio = ['-i', str(tmp / 'voz.wav')]; mapa = ['-map', '1:a']
        if MUSICA.exists():  # música bajita que se agacha cuando Vex habla (sidechain) y se desvanece al final
            audio += ['-stream_loop', '-1', '-i', str(MUSICA)]
            filtro = (f'[1:a]aformat=sample_rates=44100:channel_layouts=stereo,asplit[v1][v2];'
                      f'[2:a]volume={VOL_MUSICA},afade=t=out:st={max(0, dur - 2):.2f}:d=2[m];'
                      f'[m][v1]sidechaincompress=threshold=0.02:ratio=6:attack=30:release=500[md];'
                      f'[v2][md]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11,aresample=44100[a]')
            audio += ['-filter_complex', filtro]; mapa = ['-map', '[a]']
        enc = subprocess.Popen([FF, '-v', 'error', '-y', '-f', 'image2pipe', '-framerate', '30', '-c:v', 'mjpeg', '-i', '-', *audio,
                                '-map', '0:v', *mapa, '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p',
                                '-c:a', 'aac', '-b:a', '192k', '-t', f'{dur:.3f}', '-movflags', '+faststart', str(salida)], stdin=subprocess.PIPE)
        t0 = time.time()
        for i in range(total):
            pg.evaluate(f'render({i / 30})'); enc.stdin.write(pg.screenshot(type='jpeg', quality=92))
            if i % 300 == 0: print(f'{i}/{total} cuadros', flush=True)
        enc.stdin.close(); enc.wait(); b.close()
        print('listo:', salida, f'({total} cuadros en {round(time.time() - t0)} s)')

if __name__ == '__main__':
    carpeta, salida = pathlib.Path(sys.argv[1]).resolve(), sys.argv[2]
    muestras = [float(x) for x in sys.argv[3].split(',')] if len(sys.argv) > 3 else None
    tmp = carpeta / 'tmp'; tmp.mkdir(exist_ok=True)
    dur, n = voz(carpeta, tmp); print(f'voz: {dur:.1f} s · {n} palabras')
    subprocess.run([RHUBARB, '-q', '-r', 'phonetic', '-f', 'json', '-o', str(tmp / 'boca.json'), str(tmp / 'voz16.wav')], check=True)
    datos(carpeta, tmp)
    subprocess.run([sys.executable, str(carpeta / 'armar_html.py')], check=True)
    render(carpeta / 'video.html', tmp, salida, muestras)
