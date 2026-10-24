# Música enérgica para reels: los instrumentos y el sonido del lanzamiento de LetSprint (120 BPM, La menor), en un arreglo de 2 minutos
# que sirve de fondo en bucle. Original, hecha en código: sin derechos de autor.
# Uso: python musica_energia.py   → musica/energia.wav
import pathlib, wave
import numpy as np

SR = 44100
DUR = 120.0
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


# ---- Arreglo de 2 minutos: colchón, subida, ritmo con un remate cada 16 compases y un respiro a la mitad ----
add(pad([45] + AM, 4.2), 0.0, 1.0)
for i, t0 in enumerate([1.0, 1.5, 2.0, 2.5]):
    add(kick(0.9), t0, 0.8); add(stab([m + 12 for m in PROG[i % 4]]), t0, 0.8, -0.2 + i * 0.13)
n = int(1.5 * SR); tt = np.arange(n) / SR
riser = hp(noise(n)) * (tt / 1.5) ** 2 * 0.35 + np.sin(2 * np.pi * (200 + 900 * (tt / 1.5) ** 2) * tt) * (tt / 1.5) ** 2 * 0.08
add(riser, 2.5, 1.0)
INICIO = 4.0
b = 0
while INICIO + b * BEAT < DUR - 2:
    t0 = INICIO + b * BEAT; ciclo = b % 64; respiro = 56 <= (b % 128) < 64   # 4 compases de solo bombo y bajo cada 64 compases
    if ciclo == 0: add(impact(), t0, 0.7)
    add(kick(), t0, 1.0)
    if b % 2 == 1 and not respiro: add(clap(), t0, 0.8)
    if not respiro: add(hat(), t0 + BEAT / 2, 1.0, 0.25); add(hat(), t0, 0.5, -0.25)
    if ciclo == 62: [add(clap(), t0 + k * 0.0625, 0.2 + k * 0.05) for k in range(16)]
    bar = (b // 4) % 4
    bass = saw(note(BASS[bar]), BEAT * 0.45, 8) * env(int(BEAT * 0.45 * SR), 0.003, 0.18) * 0.22
    add(bass, t0, 1.0); add(bass, t0 + BEAT / 2, 0.7)
    if b % 4 == 0:
        add(pad(PROG[bar], 2.05), t0, 0.8)
        if not respiro: add(stab([m + 12 for m in PROG[bar]], 0.25), t0, 0.5, 0.3)
    b += 1

mix = np.stack([L, R], axis=1)
mix = np.tanh(mix * 1.4) / np.tanh(1.4)
mix /= max(1e-9, np.abs(mix).max()) / 0.89
salida = pathlib.Path(__file__).parent.parent / 'musica' / 'energia.wav'
with wave.open(str(salida), 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix * 32767).astype(np.int16).tobytes())
print('musica ok', salida)
