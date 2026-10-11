# Genera la música de fondo de Vex por código (propia: sin derechos de autor de terceros).
# Ritmo tecnológico suave: pad + arpegio + bajo + bombo y hi-hat, progresión Am–F–C–G a 110 BPM.
# Uso: musica.py [salida.wav] [segundos]   → por defecto ../musica/fondo-vex.wav, 70 s
import sys, wave, pathlib, numpy as np
SR = 44100
salida = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path(__file__).parent.parent / 'musica' / 'fondo-vex.wav'
DUR = float(sys.argv[2]) if len(sys.argv) > 2 else 70.0
BPM = 110; BEAT = 60 / BPM; COMPAS = 4 * BEAT
nota = lambda n: 440 * 2 ** ((n - 69) / 12)  # MIDI → Hz
ACORDES = [[57, 60, 64], [53, 57, 60], [48, 52, 55], [55, 59, 62]]  # Am F C G
rng = np.random.default_rng(7)
N = int(DUR * SR); t = np.arange(N) / SR; mezcla = np.zeros(N)

def suave(x, a):  # filtro pasa bajos de un polo
    y = np.empty_like(x); acc = 0.0
    for i, v in enumerate(x): acc += a * (v - acc); y[i] = acc
    return y

def env(n, ataque, caida):
    e = np.ones(n); a = max(1, int(ataque * SR)); e[:a] = np.linspace(0, 1, a)
    return e * np.exp(-np.arange(n) / SR / caida) if caida else e

# Pad: cada acorde dura un compás, con armónicos suaves y fundido
pad = np.zeros(N)
for c in range(int(DUR / COMPAS) + 1):
    i0, i1 = int(c * COMPAS * SR), min(N, int((c + 1) * COMPAS * SR + 0.3 * SR))
    if i0 >= N: break
    tt = np.arange(i1 - i0) / SR; e = np.minimum(1, tt / 0.6) * np.minimum(1, (tt[-1] - tt) / 0.4 + 1e-9)
    for n in ACORDES[c % 4]:
        f = nota(n); pad[i0:i1] += e * (np.sin(2 * np.pi * f * tt) + 0.35 * np.sin(2 * np.pi * 2 * f * tt + 0.3) + 0.12 * np.sin(2 * np.pi * 3 * f * tt)) / 3
mezcla += 0.22 * pad

# Arpegio en corcheas, una octava arriba
paso = BEAT / 2
for k in range(int(DUR / paso)):
    c = int(k * paso / COMPAS) % 4; n = ACORDES[c][[0, 1, 2, 1][k % 4]] + 12
    i0 = int(k * paso * SR); n_s = min(int(0.45 * SR), N - i0)
    if n_s <= 0: break
    tt = np.arange(n_s) / SR
    mezcla[i0:i0 + n_s] += 0.13 * env(n_s, 0.005, 0.18) * (np.sin(2 * np.pi * nota(n) * tt) + 0.2 * np.sin(2 * np.pi * 2 * nota(n) * tt))

# Bajo: raíz del acorde en cada tiempo
for k in range(int(DUR / BEAT)):
    c = int(k * BEAT / COMPAS) % 4; f = nota(ACORDES[c][0] - 24)
    i0 = int(k * BEAT * SR); n_s = min(int(BEAT * 0.9 * SR), N - i0)
    if n_s <= 0: break
    tt = np.arange(n_s) / SR
    mezcla[i0:i0 + n_s] += 0.20 * env(n_s, 0.01, 0.35) * np.sin(2 * np.pi * f * tt)

# Bombo en cada tiempo y hi-hat en contratiempos (entra después de 2 compases)
inicio_ritmo = 2 * COMPAS
for k in range(int(DUR / BEAT)):
    tk = k * BEAT
    if tk < inicio_ritmo: continue
    i0 = int(tk * SR); n_s = min(int(0.25 * SR), N - i0)
    if n_s <= 0: break
    tt = np.arange(n_s) / SR; fase = 2 * np.pi * np.cumsum(50 + 90 * np.exp(-tt / 0.03)) / SR
    mezcla[i0:i0 + n_s] += 0.32 * np.exp(-tt / 0.12) * np.sin(fase)
    h0 = int((tk + BEAT / 2) * SR); h_s = min(int(0.05 * SR), N - h0)
    if h_s > 0:
        ruido = rng.standard_normal(h_s); ruido = ruido - suave(ruido, 0.15)
        mezcla[h0:h0 + h_s] += 0.05 * np.exp(-np.arange(h_s) / SR / 0.015) * ruido

# Fundido de entrada y salida, normalizado
f_in, f_out = int(1.5 * SR), int(2.5 * SR)
mezcla[:f_in] *= np.linspace(0, 1, f_in); mezcla[-f_out:] *= np.linspace(1, 0, f_out)
mezcla = mezcla / np.max(np.abs(mezcla)) * 0.85
salida.parent.mkdir(parents=True, exist_ok=True)
estereo = np.stack([mezcla, np.roll(mezcla, int(0.012 * SR))], 1)  # leve ensanche estéreo
with wave.open(str(salida), 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((estereo * 32767).astype(np.int16).tobytes())
print('música:', salida, f'{DUR:.0f} s')
