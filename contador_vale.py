#!/usr/bin/env python3
"""Escucha el micrófono y suma +1 al contador cada vez que alguien dice "vale".

El reconocimiento es 100 % local (Vosk), no se envía audio a ningún servidor.
El total se guarda en contador.json para que no se pierda entre ejecuciones.
"""

import argparse
import json
import queue
import sys
from datetime import datetime
from pathlib import Path

import sounddevice as sd
from vosk import KaldiRecognizer, Model, SetLogLevel

PALABRA = "vale"
FICHERO_CONTADOR = Path(__file__).with_name("contador.json")


def cargar_contador(ruta: Path) -> int:
    try:
        return int(json.loads(ruta.read_text())["total"])
    except (FileNotFoundError, KeyError, ValueError):
        return 0


def guardar_contador(ruta: Path, total: int) -> None:
    ruta.write_text(json.dumps({"total": total, "actualizado": datetime.now().isoformat(timespec="seconds")}, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser(description=f'Cuenta cuántas veces se dice "{PALABRA}".')
    parser.add_argument("--modelo", help="Ruta a un modelo Vosk descargado (por defecto se descarga el pequeño en español).")
    parser.add_argument("--dispositivo", help="Índice o nombre del micrófono (ver --listar).")
    parser.add_argument("--listar", action="store_true", help="Lista los dispositivos de audio y sale.")
    parser.add_argument("--reset", action="store_true", help="Pone el contador a 0 antes de empezar.")
    args = parser.parse_args()

    if args.listar:
        print(sd.query_devices())
        return

    dispositivo = int(args.dispositivo) if args.dispositivo and args.dispositivo.isdigit() else args.dispositivo

    SetLogLevel(-1)
    modelo = Model(args.modelo) if args.modelo else Model(lang="es")
    frecuencia = int(sd.query_devices(dispositivo, "input")["default_samplerate"])
    # Limitar la gramática a la palabra clave mejora mucho la precisión y la velocidad.
    reconocedor = KaldiRecognizer(modelo, frecuencia, json.dumps([PALABRA, "[unk]"]))

    total = 0 if args.reset else cargar_contador(FICHERO_CONTADOR)
    guardar_contador(FICHERO_CONTADOR, total)

    audio: "queue.Queue[bytes]" = queue.Queue()

    def callback(datos, _frames, _tiempo, estado):
        if estado:
            print(estado, file=sys.stderr)
        audio.put(bytes(datos))

    print(f'Escuchando... di "{PALABRA}". Contador actual: {total}. (Ctrl+C para salir)')
    with sd.RawInputStream(samplerate=frecuencia, blocksize=8000, device=dispositivo,
                           dtype="int16", channels=1, callback=callback):
        try:
            while True:
                if reconocedor.AcceptWaveform(audio.get()):
                    texto = json.loads(reconocedor.Result()).get("text", "")
                    veces = texto.split().count(PALABRA)
                    if veces:
                        total += veces
                        guardar_contador(FICHERO_CONTADOR, total)
                        print(f'[{datetime.now():%H:%M:%S}] "{PALABRA}" +{veces}  ->  total: {total}')
        except KeyboardInterrupt:
            print(f"\nFin. Total de \"{PALABRA}\": {total}")


if __name__ == "__main__":
    main()
