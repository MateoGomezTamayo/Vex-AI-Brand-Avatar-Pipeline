# Ubica FFmpeg y Rhubarb: variable de entorno → PATH → instalaciones conocidas en Windows (WinGet, ~/tools).
import os, glob, shutil, pathlib

def _buscar(env, nombre, patrones):
    if os.environ.get(env): return os.environ[env]
    en_path = shutil.which(nombre)
    if en_path: return en_path
    for p in patrones:
        hallados = sorted(glob.glob(os.path.expandvars(os.path.expanduser(p))))
        if hallados: return hallados[-1]
    raise FileNotFoundError(f'No encontré {nombre}. Instálalo o define la variable de entorno {env} con su ruta.')

FF = _buscar('FFMPEG', 'ffmpeg', [r'%LOCALAPPDATA%\Microsoft\WinGet\Packages\Gyan.FFmpeg*\ffmpeg-*\bin\ffmpeg.exe'])
RHUBARB = _buscar('RHUBARB', 'rhubarb', [r'~\tools\rhubarb\rhubarb.exe', '~/tools/rhubarb/rhubarb'])
