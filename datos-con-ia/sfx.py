# Datos con IA: efectos de sonido sincronizados con las animaciones (mismas palabras clave que armar_html.py) y mezcla final.
# Uso: sfx.py <video_sin_efectos.mp4> <salida.mp4>
# Los efectos se sintetizan aquí mismo (sin archivos externos ni licencias): pop, tic, ding, vibración, caja, alerta, barrido.
import sys, json, re, unicodedata, subprocess, wave, pathlib, numpy as np
d = pathlib.Path(__file__).parent; sys.path.insert(0, str(d.parent / 'comun'))
from rutas import FF
SR = 48000
D = json.load(open(d / 'tmp' / 'datos.json', encoding='utf-8'))
PAL = [p for g in D['grupos'] for p in g]
SEC = {s['id']: s for s in D['secciones']}
norm = lambda x: re.sub(r'[^a-z0-9]', '', unicodedata.normalize('NFD', x.lower()).encode('ascii', 'ignore').decode())
def kw(sid, w, n=0):
    s = SEC[sid]; ps = [p for p in PAL if s['start'] - 0.05 <= p[0] < s['end'] and norm(p[2]).startswith(w)]
    return ps[n][0] if len(ps) > n else s['start']

t = np.arange(int(SR * 1.2)) / SR
env = lambda dur, k: np.exp(-t[:int(SR * dur)] * k)
def tono(f, dur, k, f2=None):
    tt = t[:int(SR * dur)]; ff = f if f2 is None else np.linspace(f, f2, len(tt))
    return np.sin(2 * np.pi * np.cumsum(ff) / SR) * env(dur, k)
rng = np.random.default_rng(7)
SONIDO = {
    'pop': 0.5 * tono(520, 0.09, 45, 1150),
    'tic': 0.35 * tono(2200, 0.03, 160),
    'ding': 0.35 * (tono(1318, 0.9, 5) + 0.6 * tono(1976, 0.9, 6)),
    'vibra': 0.35 * np.sign(np.sin(2 * np.pi * 150 * t[:int(SR * 0.5)])) * (0.6 + 0.4 * np.sin(2 * np.pi * 9 * t[:int(SR * 0.5)])) * np.minimum(1, (0.5 - t[:int(SR * 0.5)]) * 12),
    'caja': 0.32 * np.concatenate([tono(2637, 0.12, 25), tono(3520, 0.5, 8)]),
    'alerta': 0.35 * np.concatenate([tono(330, 0.14, 8), tono(262, 0.22, 7)]),
    'barrido': 0.25 * np.convolve(rng.normal(0, 1, int(SR * 0.35)), np.ones(40) / 40, 'same') * np.sin(np.linspace(0, np.pi, int(SR * 0.35))),
}

ev = []
for s in D['secciones'][1:]: ev.append(('barrido', s['start'] - 0.2))
h0 = SEC['hook']['start']; ev += [('pop', h0 + 0.35 + i * 0.16) for i in range(6)]
ev += [('pop', kw('mateo', 'mateo')), ('ding', kw('mateo', 'asistencia'))]
ev += [('pop', kw('curso', w)) for w in ('seis', 'gratis', 'espanol', 'jupyter')]
ev += [('tic', kw('ejecuta', 'ejecutar')), ('pop', kw('ejecuta', 'navegador')), ('caja', kw('ejecuta', 'instalar'))]
ev += [('tic', kw('palabras', 'tocas')), ('pop', kw('palabras', 'tocas')), ('pop', kw('palabras', 'explica'))]
ev += [('pop', kw('vex', w)) for w in ('codigo', 'error')] + [('ding', kw('vex', 'enredos'))]
ev += [('pop', kw('quiz', 'quiz')), ('caja', kw('quiz', 'claro'))]
ev += [('pop', kw('whatsapp', 'negocio')), ('tic', kw('whatsapp', 'whatsapp')), ('vibra', kw('whatsapp', 'whatsapp') + 0.05), ('pop', kw('whatsapp', 'asesoramos'))]
ev.append(('ding', kw('cta', 'entra')))

dur = D['dur']; pista = np.zeros(int(SR * (dur + 1.5)))
for nombre, at in ev:
    s = SONIDO[nombre]; a = int(max(0, at) * SR); pista[a:a + len(s)] += s[:len(pista) - a]
pista = np.clip(pista, -1, 1)
wav = d / 'tmp' / 'sfx.wav'
with wave.open(str(wav), 'wb') as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((pista * 32767).astype(np.int16).tobytes())
subprocess.run([FF, '-v', 'error', '-y', '-i', sys.argv[1], '-i', str(wav), '-filter_complex',
                '[1:a]aformat=sample_rates=44100:channel_layouts=stereo,volume=0.55[s];[0:a][s]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[a]',
                '-map', '0:v', '-map', '[a]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', sys.argv[2]], check=True)
print(len(ev), 'efectos ·', sys.argv[2])
