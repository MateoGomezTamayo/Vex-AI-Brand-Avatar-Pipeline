# Voz de Vex con entonación por frase (Edge TTS, gratis): cada frase del guion lleva un tono que cambia velocidad, tono y volumen.
# guion.json: [{"id": "intro", "frases": [["¡Día dos automatizando procesos!", "gancho"], ["Hoy: inventario.", "remate"]]}, ...]
import json, asyncio, subprocess, wave, pathlib, numpy as np, edge_tts
from rutas import FF
VOZ, SR = 'es-CO-GonzaloNeural', 24000
# La voz pareja (misma velocidad y tono en todo el texto) sonó más natural que la entonación por frase; ENTONACION = True la activa.
ENTONACION = False
PAREJA = ('+6%', '+8Hz', '+0%', 0.25)
TONOS = {  # (rate, pitch, volume, pausa después en s)
    'gancho':   ('+14%', '+16Hz', '+15%', 0.35),
    'pregunta': ('+6%',  '+22Hz', '+5%',  0.45),
    'normal':   ('+8%',  '+6Hz',  '+0%',  0.2),
    'dato':     ('-4%',  '-4Hz',  '+10%', 0.4),
    'remate':   ('+2%',  '+12Hz', '+15%', 0.3),
}
PAUSA_SECCION = 0.35 if ENTONACION else 0.9
prosodia = lambda tono: TONOS[tono] if ENTONACION else PAREJA

async def sintetizar(texto, tono, mp3):
    rate, pitch, volume, _ = prosodia(tono)
    com = edge_tts.Communicate(texto, VOZ, rate=rate, pitch=pitch, volume=volume, boundary='WordBoundary')
    audio, palabras = bytearray(), []
    async for c in com.stream():
        if c['type'] == 'audio': audio += c['data']
        elif c['type'] == 'WordBoundary': palabras.append([c['offset'] / 1e7, (c['offset'] + c['duration']) / 1e7, c['text']])
    mp3.write_bytes(audio)
    raw = subprocess.run([FF, '-v', 'error', '-i', str(mp3), '-f', 's16le', '-ac', '1', '-ar', str(SR), '-'], capture_output=True).stdout
    return np.frombuffer(raw, np.int16), palabras

async def generar(guion, tmp):
    pista, palabras, secciones, t = [np.zeros(int(0.4 * SR), np.int16)], [], [], 0.4
    for i, s in enumerate(guion):
        inicio = t
        for j, (texto, tono) in enumerate(s['frases']):
            a, ws = await sintetizar(texto, tono, tmp / f'sec{i}-{j}.mp3')
            palabras += [[round(t + a0, 3), round(t + b0, 3), w] for a0, b0, w in ws]
            pausa = prosodia(tono)[3]
            pista += [a, np.zeros(int(pausa * SR), np.int16)]; t += len(a) / SR + pausa
        secciones.append({'id': s['id'], 'start': round(inicio, 3), 'end': round(t, 3)})
        extra = 1.4 if i == len(guion) - 1 else s.get('pausa', PAUSA_SECCION)  # una sección puede pedir menos pausa (videos más rápidos)
        pista.append(np.zeros(int(extra * SR), np.int16)); t += extra
    audio = np.concatenate(pista)
    with wave.open(str(tmp / 'voz.wav'), 'wb') as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(audio.tobytes())
    subprocess.run([FF, '-v', 'error', '-y', '-i', str(tmp / 'voz.wav'), '-ar', '16000', str(tmp / 'voz16.wav')])
    json.dump({'palabras': palabras, 'secciones': secciones, 'dur': len(audio) / SR}, open(tmp / 'voz.json', 'w', encoding='utf-8'), ensure_ascii=False)
    return len(audio) / SR, len(palabras)

def voz(carpeta, tmp):
    guion = json.loads((carpeta / 'guion.json').read_text(encoding='utf-8'))
    return asyncio.run(generar(guion, tmp))
