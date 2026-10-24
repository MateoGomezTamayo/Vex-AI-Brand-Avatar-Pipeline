# Música reflexiva y esperanzadora para reels de decisiones o historias personales (original, hecha en código: sin derechos de autor).
# Piano en arpegios sobre Am–F–C–G a 84 BPM; entra un colchón, luego un pulso suave y al final bajo y platillos. 2 minutos.
# Uso: python musica_reflexiva.py   → musica/reflexiva.wav
import pathlib, wave
import numpy as np

SR, DUR, BPM = 44100, 120.0, 84
BEAT = 60 / BPM
N = int(SR * DUR)
L, R = np.zeros(N), np.zeros(N)
rng = np.random.default_rng(11)

def add(sig, t0, gain=1.0, pan=0.0):
    i = int(t0 * SR)
    if i >= N: return
    sig = sig[: N - i]
    L[i:i + len(sig)] += sig * gain * (1 - max(0, pan)); R[i:i + len(sig)] += sig * gain * (1 + min(0, pan))

note = lambda m: 440 * 2 ** ((m - 69) / 12)

def piano(m, dur=2.2):
    n = int(dur * SR); t = np.arange(n) / SR; f = note(m)
    x = sum(np.sin(2 * np.pi * f * k * t * (1 + 0.0004 * k * k)) * np.exp(-t * (1.2 + k * 0.9)) / k ** 1.3 for k in range(1, 8))
    return x * np.minimum(1, t / 0.004) * 0.22

def pad(chord, dur):
    n = int(dur * SR); t = np.arange(n) / SR; x = np.zeros(n)
    for m in chord:
        for det in (-0.1, 0.1):
            f = note(m + det); x += np.sin(2 * np.pi * f * t) + 0.25 * np.sin(2 * np.pi * 2 * f * t)
    return x * np.minimum(1, t / 1.2) * np.minimum(1, (dur - t) / 1.2) * 0.035

def kick():
    n = int(0.4 * SR); t = np.arange(n) / SR
    return np.sin(2 * np.pi * np.cumsum(45 + 70 * np.exp(-t * 30)) / SR) * np.exp(-t / 0.18) * 0.8

def rim():
    n = int(0.12 * SR); t = np.arange(n) / SR
    return np.diff(rng.standard_normal(n), prepend=0) * np.exp(-t / 0.03) * 0.18

def hat():
    n = int(0.05 * SR); t = np.arange(n) / SR
    return np.diff(np.diff(rng.standard_normal(n), prepend=0), prepend=0) * np.exp(-t / 0.012) * 0.1

def bajo(m, dur):
    n = int(dur * SR); t = np.arange(n) / SR
    return (np.sin(2 * np.pi * note(m) * t) + 0.3 * np.sin(4 * np.pi * note(m) * t)) * np.exp(-t / 0.9) * np.minimum(1, t / 0.01) * 0.3

ACORDES = [([57, 60, 64], 45), ([53, 57, 60], 41), ([48, 52, 55], 36), ([55, 59, 62], 43)]   # Am F C G
PATRON = [0, 1, 2, 1, 2, 0, 1, 2]   # arpegio en corcheas
compas = 4 * BEAT
c = 0
while c * compas < DUR - 1:
    t0 = c * compas; acorde, raiz = ACORDES[c % 4]
    add(pad(acorde, compas + 0.3), t0, 1.0)
    alto = 12 if c >= 16 else 0
    for k, j in enumerate(PATRON):
        add(piano(acorde[j] + 12 + alto * (k % 2)), t0 + k * BEAT / 2, 0.9 if k == 0 else 0.6, -0.3 + 0.08 * k)
    if c >= 4:   # pulso suave
        for bt in range(4):
            if bt in (0, 2): add(kick(), t0 + bt * BEAT, 0.7)
            if bt in (1, 3): add(rim(), t0 + bt * BEAT, 0.8, 0.2)
    if c >= 8:   # bajo y platillos
        add(bajo(raiz, compas), t0, 1.0)
        for k in range(8): add(hat(), t0 + k * BEAT / 2, 0.9 if k % 2 else 0.5, 0.3)
    c += 1

mix = np.stack([L, R], axis=1)
mix = np.tanh(mix * 1.2) / np.tanh(1.2)
mix /= max(1e-9, np.abs(mix).max()) / 0.89
salida = pathlib.Path(__file__).parent.parent / 'musica' / 'reflexiva.wav'
with wave.open(str(salida), 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix * 32767).astype(np.int16).tobytes())
print('musica ok', salida)
