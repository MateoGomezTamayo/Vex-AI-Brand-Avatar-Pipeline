# Música del video: los mismos instrumentos y sonido del lanzamiento de LetSprint (videos/letsprint-launch/musica.py, 120 BPM, La menor),
# extendida a la duración de la voz y sincronizada con sus cortes. Escribe tmp/musica.wav; el render la usa en vez de la música general.
# Uso: python musica.py   (después de generar la voz, porque lee tmp/datos.json)
import json, pathlib, wave
import numpy as np

SR = 44100
DUR = json.load(open(pathlib.Path(__file__).parent / 'tmp' / 'datos.json', encoding='utf-8'))['dur']
BEAT = 0.5
N = int(SR * DUR)
L = np.zeros(N)
R = np.zeros(N)
rng = np.random.default_rng(7)


def add(sig, t0, gain=1.0, pan=0.0):
    i = int(t0 * SR)
    if i >= N:
        return
    sig = sig[: N - i]
    L[i:i + len(sig)] += sig * gain * (1 - max(0, pan))
    R[i:i + len(sig)] += sig * gain * (1 + min(0, pan))


def env(n, a=0.002, d=0.2):
    t = np.arange(n) / SR
    return np.minimum(1, t / a) * np.exp(-t / d)


def kick(power=1.0):
    n = int(0.45 * SR)
    t = np.arange(n) / SR
    f = 45 + 110 * np.exp(-t * 28)
    ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * env(n, 0.001, 0.16 * power) * 1.1


def noise(n):
    return rng.standard_normal(n)


def hp(x):  # crude high-pass: first difference
    return np.diff(x, prepend=0)


def clap():
    n = int(0.25 * SR)
    x = hp(noise(n)) * env(n, 0.001, 0.06)
    return x * 0.5


def hat(open_=False):
    n = int((0.18 if open_ else 0.05) * SR)
    x = hp(hp(noise(n))) * env(n, 0.0005, 0.06 if open_ else 0.015)
    return x * 0.18


def note(f):
    return 440 * 2 ** ((f - 69) / 12)


def saw(freq, dur, harmonics=12):
    n = int(dur * SR)
    t = np.arange(n) / SR
    x = sum(np.sin(2 * np.pi * freq * k * t) / k for k in range(1, harmonics + 1))
    return x


def pad(chord, dur):
    n = int(dur * SR)
    t = np.arange(n) / SR
    x = np.zeros(n)
    for m in chord:
        for det in (-0.12, 0.12):
            f = note(m + det)
            x += np.sin(2 * np.pi * f * t) + 0.3 * np.sin(2 * np.pi * 2 * f * t)
    a = np.minimum(1, t / 0.6) * np.minimum(1, (dur - t) / 0.8)
    return x * a * 0.05


def stab(chord, dur=0.35):
    n = int(dur * SR)
    x = sum(saw(note(m), dur, 10) for m in chord)
    return x * env(n, 0.002, 0.12) * 0.09


def impact():
    n = int(1.6 * SR)
    t = np.arange(n) / SR
    boom = np.sin(2 * np.pi * (38 + 60 * np.exp(-t * 9)) * t) * np.exp(-t / 0.5)
    crash = hp(noise(n)) * np.exp(-t / 0.45) * 0.25
    return boom * 0.9 + crash


AM, F, C, G = [57, 60, 64], [53, 57, 60], [48, 52, 55], [55, 59, 62]
PROG = [AM, F, C, G]
BASS = [45, 41, 36, 43]  # A1 F1 C2 G1


# ---- Arreglo para este video: se lee de tmp/datos.json (secciones y palabras de la voz) ----
import json, re, unicodedata, pathlib
D = json.load(open(pathlib.Path(__file__).parent / 'tmp' / 'datos.json', encoding='utf-8'))
SEC = {s['id']: s for s in D['secciones']}
PAL = [p for g in D['grupos'] for p in g]
norm = lambda s: re.sub(r'[^a-z0-9]', '', unicodedata.normalize('NFD', s.lower()).encode('ascii', 'ignore').decode())
def kw(sec, w, n=0):
    s = SEC[sec]; ps = [p for p in PAL if s['start'] - 0.05 <= p[0] < s['end'] and norm(p[2]).startswith(w)]
    return ps[n][0] if len(ps) > n else s['start']

DROP = SEC['intro']['start']            # la caída entra con la presentación
CALMA = (SEC['control']['start'], SEC['cta']['start'])  # solo bombo y bajo en "tú decides"
FIN = SEC['cta']['start']
FUERTES = [kw('intro', 'letsprint'), kw('reglas', 'p1'), kw('control', 'tu')]

# Gancho: colchón y un golpe por cada tarea que aparece; subida hacia la caída
add(pad([45] + AM, DROP), 0.0, 1.0)
for i in range(6):
    t0 = SEC['hook']['start'] + 0.3 + i * 0.5
    if t0 > DROP - 1.6: break
    add(kick(0.9), t0, 0.8); add(stab([m + 12 for m in PROG[i % 4]]), t0, 0.8, -0.3 + i * 0.12); add(clap(), t0, 0.5)
n = int(1.5 * SR); tt = np.arange(n) / SR
riser = hp(noise(n)) * (tt / 1.5) ** 2 * 0.35 + np.sin(2 * np.pi * (200 + 900 * (tt / 1.5) ** 2) * tt) * (tt / 1.5) ** 2 * 0.08
add(riser, DROP - 1.5, 1.0)
for k in range(8): add(clap(), DROP - 0.5 + k * 0.0625, 0.25 + k * 0.06)

# Ritmo completo a 120 BPM desde la caída hasta el cierre
add(impact(), DROP, 0.9)
b = 0
while DROP + b * BEAT < FIN:
    t0 = DROP + b * BEAT; calma = CALMA[0] <= t0 < CALMA[1]
    add(kick(), t0, 1.0)
    if b % 2 == 1 and not calma: add(clap(), t0, 0.8)
    if not calma: add(hat(), t0 + BEAT / 2, 1.0, 0.25); add(hat(), t0, 0.5, -0.25)
    bar = (b // 4) % 4
    bass = saw(note(BASS[bar]), BEAT * 0.45, 8) * env(int(BEAT * 0.45 * SR), 0.003, 0.18) * 0.22
    add(bass, t0, 1.0); add(bass, t0 + BEAT / 2, 0.7)
    if b % 4 == 0:
        add(pad(PROG[bar], 2.05), t0, 0.8)
        if not calma: add(stab([m + 12 for m in PROG[bar]], 0.25), t0, 0.5, 0.3)
    b += 1

# Un golpe en cada corte y uno más fuerte en el logo, el P1 y "tú decides"
for s in D['secciones'][2:]: add(impact(), s['start'] - 0.06, 0.45); add(hat(True), s['start'] - 0.06, 0.8, 0.3)
for h in FUERTES: add(impact(), h, 0.8); add(stab([69, 72, 76], 0.5), h, 1.0)

# Cierre: impacto y colchón largo que se desvanece
add(impact(), FIN, 0.8)
add(pad([45] + AM + [69], DUR - FIN), FIN, 1.3)

mix = np.stack([L, R], axis=1)
mix = np.tanh(mix * 1.4) / np.tanh(1.4)
fade = np.ones(N); fs = int((DUR - 1.2) * SR); fade[fs:] = np.linspace(1, 0, N - fs)
mix *= fade[:, None]
mix /= max(1e-9, np.abs(mix).max()) / 0.89
with wave.open(str(pathlib.Path(__file__).parent / 'tmp' / 'musica.wav'), 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix * 32767).astype(np.int16).tobytes())
print('musica ok', round(DUR, 1), 's')
