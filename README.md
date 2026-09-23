# Contador de "vale"

Script que escucha el micrófono y suma **+1** a un contador cada vez que alguien dice **"vale"**.

Hay dos versiones:

- **📱 iPhone / móvil** (`index.html`): web app que se abre en Safari. Usa el reconocimiento de voz del propio iPhone.
- **💻 Ordenador** (`contador_vale.py`): script de Python con reconocimiento local y sin conexión ([Vosk](https://alphacephei.com/vosk/)).

## 📱 iPhone

1. Abre **https://gutirodrii.github.io/contador-vale/** en **Safari**.
2. Pulsa **Empezar** y acepta los permisos de micrófono y reconocimiento de voz.
3. Cada "vale" suma +1. El contador se guarda en el propio iPhone.
4. (Opcional) Compartir › **Añadir a pantalla de inicio** para tenerlo como una app.

Notas:
- Requiere iOS 14.5+ y tener **Dictado** activado (Ajustes › General › Teclado › Activar dictado).
- La pantalla se mantiene encendida mientras escucha. Si bloqueas el iPhone o cambias de app, iOS corta el micro; al volver, sigue escuchando solo.
- Botones −1 / +1 para corregir a mano, y Reiniciar para ponerlo a 0.

### Publicarlo con GitHub Pages

En el repo: **Settings › Pages › Source: Deploy from a branch › `main` / `(root)` › Save**.
En el plan gratuito de GitHub, Pages solo funciona si el repositorio es público.

## 💻 Ordenador

### Instalación

```bash
python3 -m venv .venv
source .venv/bin/activate      # En Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

En Linux puede hacer falta PortAudio: `sudo apt install libportaudio2`.

### Uso

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

#### Opciones

| Opción | Descripción |
| --- | --- |
| `--reset` | Pone el contador a 0 antes de empezar |
| `--listar` | Muestra los micrófonos disponibles |
| `--dispositivo N` | Usa el micrófono con índice (o nombre) `N` |
| `--modelo RUTA` | Usa un modelo Vosk ya descargado (p. ej. el grande de español, más preciso) |
