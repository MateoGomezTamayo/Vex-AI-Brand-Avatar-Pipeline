#!/bin/bash
# Renderiza los videos indicados (carpetas del repo) a $SALIDA/vex-<carpeta>.mp4 sin regenerar la voz.
# Por defecto: ../../videos/salida si existe (estudio Vextrum), si no ./salida.
B="$(cd "$(dirname "$0")/.." && pwd)"; PY="${PYTHON:-python}"; [ -x "$B/../../.venv-3/Scripts/python.exe" ] && PY="$B/../../.venv-3/Scripts/python.exe"
OUT="${SALIDA:-$B/../../videos/salida}"; [ -d "$OUT" ] || OUT="$B/salida"; export OUT
for v in "$@"; do cd "$B/$v" && "$PY" armar_html.py && "$PY" -c "
import sys,pathlib;sys.path.insert(0,'../comun');from pipeline import render
d=pathlib.Path('.').resolve();import os;o=pathlib.Path(os.environ['OUT']);o.mkdir(parents=True,exist_ok=True);render(d/'video.html',d/'tmp',o/('vex-'+d.name+'.mp4'))"; done
