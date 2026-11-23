# Música de moda propia, generada por código (sin samples ni derechos de terceros) para los reels de tiendas (Katrina).
# Dos estilos:
#   urbano   96 BPM: ritmo dembow (bombo en cada tiempo, redoblante en el 3 y el 6 de cada 8), bajo 808 con caída,
#            pluck en arpegio y "vocal chop" sintético (vocal formada a mano, no es una voz grabada). Am–F–C–G.
#   pasarela 122 BPM: house de pasarela con toque afro: bombo 4x4, hi-hat abierto en contratiempo, congas, bajo funky en
#            octavas y stabs de cuerdas. Am7–Dm7–Em7–Am7.
# Estructura: 2 compases de intro sin batería (filtrada), luego todo; cada 8 compases un respiro de 1 compás.
# Uso: musica_moda.py urbano|pasarela [salida.wav] [segundos]
import sys, wave, pathlib, numpy as np
SR = 44100
ESTILO = sys.argv[1] if len(sys.argv) > 1 else 'urbano'
salida = pathlib.Path(sys.argv[2]) if len(sys.argv) > 2 else pathlib.Path(__file__).parent.parent / 'musica' / f'moda-{ESTILO}.wav'
DUR = float(sys.argv[3]) if len(sys.argv) > 3 else 70.0
nota = lambda n: 440 * 2 ** ((n - 69) / 12)
rng = np.random.default_rng(23 if ESTILO == 'urbano' else 31)
N = int(DUR * SR); t = np.arange(N) / SR
L = np.zeros(N); R = np.zeros(N); DL = np.zeros(N); DR = np.zeros(N)   # melódico (con bombeo) y batería

def add(sig, t0, gan=1.0, pan=0.0, bateria=False):
    i0 = int(t0 * SR); n = min(len(sig), N - i0)
    if n <= 0 or i0 < 0: return
    a, b = (DL, DR) if bateria else (L, R)
    a[i0:i0 + n] += sig[:n] * gan * (1 - max(0, pan)); b[i0:i0 + n] += sig[:n] * gan * (1 + min(0, pan))

def env(n_s, ataque=0.005, caida=0.3):
    tt = np.arange(n_s) / SR; return np.minimum(1, tt / ataque) * np.exp(-tt / caida)
def saw(f, n_s, brillo=1.0):   # sierra aditiva (sin aliasing); brillo < 1 = como un filtro paso bajo
    tt = np.arange(n_s) / SR; s = np.zeros(n_s)
    for k in range(1, min(40, int(16000 / f)) + 1): s += np.sin(2 * np.pi * k * f * tt) / k * brillo ** (k - 1)
    return s / 1.6
def ruido(n_s, agudo=2):
    r = rng.standard_normal(n_s)
    for _ in range(agudo): r = np.diff(r, prepend=0)
    return r / (2 ** agudo)
def bombo(f0=50, golpe=120, caida=0.16):
    n_s = int(0.35 * SR); tt = np.arange(n_s) / SR
    return np.exp(-tt / caida) * np.sin(2 * np.pi * np.cumsum(f0 + golpe * np.exp(-tt / 0.03)) / SR)
def redoble():
    n_s = int(0.2 * SR); tt = np.arange(n_s) / SR
    return 0.55 * np.sin(2 * np.pi * 190 * tt) * np.exp(-tt / 0.05) + ruido(n_s, 1) * np.exp(-tt / 0.07)
def hat(abierto=False):
    n_s = int((0.22 if abierto else 0.05) * SR); return ruido(n_s, 2) * np.exp(-np.arange(n_s) / SR / (0.08 if abierto else 0.014))
def conga(f=280):
    n_s = int(0.25 * SR); tt = np.arange(n_s) / SR
    return np.sin(2 * np.pi * np.cumsum(f * (1 + 0.25 * np.exp(-tt / 0.02))) / SR) * np.exp(-tt / 0.09)
def vocal(f, n_s, vocal='a'):   # "vocal chop": armónicos con formantes de una vocal (sintético)
    form = {'a': (800, 1150, 2900), 'o': (450, 800, 2830), 'e': (400, 2000, 2550)}[vocal]
    tt = np.arange(n_s) / SR; s = np.zeros(n_s); vib = 1 + 0.004 * np.sin(2 * np.pi * 5.5 * tt)
    for k in range(1, int(4500 / f) + 1):
        g = sum(np.exp(-((k * f - F) / (90 + 0.06 * F)) ** 2) for F in form) + 0.02
        s += g * np.sin(2 * np.pi * k * f * np.cumsum(vib) / SR)
    return s / max(1e-9, np.abs(s).max()) * np.minimum(1, tt / 0.01) * np.minimum(1, (tt[-1] - tt) / 0.04 + 1e-9)

if ESTILO == 'urbano':
    BPM = 96; ACORDES = [[57, 60, 64], [53, 57, 60], [48, 52, 55], [55, 59, 62]]       # Am F C G
else:
    BPM = 122; ACORDES = [[57, 60, 64, 67], [50, 53, 57, 60], [52, 55, 59, 62], [57, 60, 64, 67]]   # Am7 Dm7 Em7 Am7
BEAT = 60 / BPM; COMPAS = 4 * BEAT; S16 = BEAT / 4
INICIO = 2 * COMPAS
respiro = lambda tk: tk >= INICIO and int((tk - INICIO) / COMPAS) % 8 == 7          # 1 compás sin bombo cada 8
acorde = lambda tk: ACORDES[int(tk / COMPAS) % 4]

# pad de fondo (todo el tema)
for c in range(int(DUR / COMPAS) + 1):
    n_s = int((COMPAS + 0.3) * SR); tt = np.arange(n_s) / SR
    e = np.minimum(1, tt / 0.6) * np.minimum(1, (tt[-1] - tt) / 0.3 + 1e-9)
    s = sum(saw(nota(n) * (1 + 0.003 * d), n_s, 0.55) for n in ACORDES[c % 4][:3] for d in (-1, 1)) / 6
    add(e * s, c * COMPAS, 0.16)

if ESTILO == 'urbano':
    ARP = [0, 1, 2, 1, 0, 2, 1, 2]                    # arpegio del pluck en corcheas
    CHOP = [(0, 'a', 12), (3, 'o', 7), (6, 'a', 12), (10, 'e', 14), (11, 'a', 12)]   # (semicorchea, vocal, intervalo)
    for k in range(int(DUR / S16) + 1):
        tk = k * S16; ac = acorde(tk); p16 = k % 16
        if p16 % 2 == 0:                                                               # pluck
            n = ac[ARP[(p16 // 2) % 8]] + 12; n_s = int(0.28 * SR)
            add(saw(nota(n), n_s, 0.7) * env(n_s, 0.003, 0.09), tk, 0.17 if tk >= INICIO else 0.14, 0.25 if p16 % 4 else -0.25)
        if tk >= 4 * COMPAS and int(tk / (2 * COMPAS)) % 2 == 0:                      # vocal chop cada 2 compases
            for p, v, iv in CHOP:
                if p16 == p: add(vocal(nota(ac[0] + iv), int(0.16 * SR), v), tk, 0.18, 0.1)
        if tk < INICIO or respiro(tk): continue
        if p16 % 4 == 0: add(bombo(52, 110, 0.18), tk, 0.34, bateria=True)            # bombo en cada tiempo
        if p16 in (3, 6, 11, 14): add(redoble(), tk, 0.20, bateria=True)              # patrón dembow
        if p16 % 2 == 1: add(hat(), tk, 0.05, 0.3, bateria=True)
        if p16 in (0, 6, 8, 14):                                                       # 808: raíz con caída larga
            n_s = int(BEAT * 1.4 * SR); tt = np.arange(n_s) / SR; f = nota(ac[0] - 24)
            s = np.tanh(2.2 * np.sin(2 * np.pi * np.cumsum(f * (1 + 0.35 * np.exp(-tt / 0.03))) / SR)) * np.exp(-tt / 0.45)
            add(s, tk, 0.26)
else:
    for k in range(int(DUR / S16) + 1):
        tk = k * S16; ac = acorde(tk); p16 = k % 16
        if p16 in (2, 6, 10, 13) and tk >= INICIO:                                     # stabs de cuerdas
            n_s = int(0.22 * SR)
            for j, n in enumerate(ac): add(saw(nota(n + 12), n_s, 0.8) * env(n_s, 0.004, 0.08), tk, 0.10, (-0.4, 0.4, -0.2, 0.2)[j])
        if p16 % 2 == 0 and tk >= INICIO:                                              # bajo funky en octavas
            n = ac[0] - 24 + (12 if p16 % 4 == 2 else 0); n_s = int(S16 * 1.7 * SR)
            add(saw(nota(n), n_s, 0.45) * env(n_s, 0.004, 0.12), tk, 0.22)
        if tk < INICIO or respiro(tk):
            if p16 % 4 == 2: add(hat(True), tk, 0.05, 0.2, bateria=True)               # en la intro solo el hat abierto
            continue
        if p16 % 4 == 0: add(bombo(48, 120, 0.15), tk, 0.34, bateria=True)            # 4x4
        if p16 % 4 == 2: add(hat(True), tk, 0.08, 0.2, bateria=True)                  # hat abierto en contratiempo
        if p16 % 2 == 1: add(hat(), tk, 0.035, -0.3, bateria=True)
        if p16 in (4, 12): add(redoble() * 0.6, tk, 0.16, bateria=True)               # palma/redoble suave en 2 y 4
        if p16 in (3, 7, 10, 15): add(conga(300 if p16 in (3, 10) else 220), tk, 0.12, 0.45 if p16 % 2 else -0.45, bateria=True)
        if p16 == 8 and int(tk / COMPAS) % 2: add(vocal(nota(ac[0] + 12), int(0.3 * SR), 'o'), tk, 0.15, -0.15)

# bombeo (sidechain) en lo melódico y mezcla
bomb = 1 - 0.5 * np.exp(-((t % BEAT) / 0.1))
L *= np.where(t >= INICIO, bomb, 1); R *= np.where(t >= INICIO, bomb, 1)
L += DL; R += DR
# intro "filtrada": promedio móvil (paso bajo simple) que se abre al entrar la batería
k = 24; suave = lambda x: np.convolve(x, np.ones(k) / k, 'same'); mezcla = np.clip((t - INICIO + 0.6) / 0.6, 0, 1)
L = L * mezcla + suave(L) * (1 - mezcla); R = R * mezcla + suave(R) * (1 - mezcla)
fade = np.minimum(1, (DUR - t) / 3.0); L *= fade; R *= fade
L, R = np.tanh(L * 1.3), np.tanh(R * 1.3)   # un poco de saturación para que suene más "lleno"
pico = max(np.abs(L).max(), np.abs(R).max()); L, R = L / pico * 0.89, R / pico * 0.89
salida.parent.mkdir(parents=True, exist_ok=True)
with wave.open(str(salida), 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.stack([L, R], 1) * 32767).astype(np.int16).tobytes())
print('listo:', salida)
