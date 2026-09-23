# Contador de "vale"

Script que escucha el micrófono y suma **+1** a un contador cada vez que alguien dice **"vale"**.

El reconocimiento de voz es local y sin conexión ([Vosk](https://alphacephei.com/vosk/)): el audio no sale de tu ordenador.

## Instalación

```bash
python3 -m venv .venv
source .venv/bin/activate      # En Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

En Linux puede hacer falta PortAudio: `sudo apt install libportaudio2`.

## Uso

```bash
python contador_vale.py
```

La primera vez se descarga automáticamente el modelo pequeño de español (~40 MB).

```
Escuchando... di "vale". Contador actual: 0. (Ctrl+C para salir)
[10:32:05] "vale" +1  ->  total: 1
[10:32:11] "vale" +2  ->  total: 3
```

El total se guarda en `contador.json`, así que se mantiene entre ejecuciones.

### Opciones

| Opción | Descripción |
| --- | --- |
| `--reset` | Pone el contador a 0 antes de empezar |
| `--listar` | Muestra los micrófonos disponibles |
| `--dispositivo N` | Usa el micrófono con índice (o nombre) `N` |
| `--modelo RUTA` | Usa un modelo Vosk ya descargado (p. ej. el grande de español, más preciso) |
