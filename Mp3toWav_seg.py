import os
import random
import shutil
import numpy as np
from pydub import AudioSegment

# INITIAL CONFIGURATION.
directorio_entrada = './datain'
directorio_salida = './dataout'
frecuencia_muestreo_objetivo = 44100  # TARGET SAMPLING RATE (44.1 kHz)
duracion_segmento = 5000  # EACH SEGMENT DURATION IN MILLISECONDS (5 seg = 5000 ms)
cantidad_segmentos = 50  # SEGMENTS TO GENERATE FOR EACH SONG
extension_a_eliminar = '.wav' # FILE EXTENSION TO REMOVE IN LIST DATA (".wav")

# DELETE WAV FILES.
if os.path.exists(directorio_entrada):
    # Iterar sobre los archivos en el directorio
    for archivo in os.listdir(directorio_entrada):
        # Verificar si el archivo tiene la extension deseada
        if archivo.endswith(extension_a_eliminar):
            # Construir la ruta completa del archivo
            ruta_completa = os.path.join(directorio_entrada, archivo)
            # Eliminar el archivo
            os.remove(ruta_completa)
            print(f'Se ha eliminado {ruta_completa}')

# DATAIN MP3 FILES
archivos_mp3 = [archivo for archivo in os.listdir(directorio_entrada) if archivo.endswith('.mp3')]

# DATAOUT FOLDER CHECK.
# Verificar si la carpeta de salida existe
if os.path.exists(directorio_salida):
    # Eliminar la carpeta y su contenido
    shutil.rmtree(directorio_salida)
    print(f'Se ha eliminado la carpeta: {directorio_salida}')
else:
    print(f'La carpeta {directorio_salida} no existe.')

# Crear el directorio de salida si no existe
if not os.path.exists(directorio_salida):
    os.makedirs(directorio_salida)

# MP3 TO WAV.
# Procesar cada archivo MP3 a WAV
for archivo_mp3 in archivos_mp3:
    # Ruta completa del archivo de entrada
    ruta_entrada = os.path.join(directorio_entrada, archivo_mp3)
    # Cargar el archivo MP3
    audio_mp3 = AudioSegment.from_mp3(ruta_entrada)
    # Crear el nombre del archivo de salida (sin .mp3)
    nombre_archivo_salida = os.path.splitext(archivo_mp3)[0] + '.wav'
    # Ruta completa del archivo de salida
    ruta_salida = os.path.join(directorio_entrada, nombre_archivo_salida)
    # Exportar el MP3 como WAV
    audio_mp3.export(ruta_salida, format="wav")
    print(f"Se ha convertido {archivo_mp3} a archivo .wav")

# Lista de archivos WAV en el directorio de entrada
archivos_wav = [archivo for archivo in os.listdir(directorio_entrada) if archivo.endswith('.wav')]

# SEGMENTS GENERATION.
# Procesar cada archivo WAV
for archivo_wav in archivos_wav:
    # Ruta completa del archivo de entrada
    ruta_entrada = os.path.join(directorio_entrada, archivo_wav)
    # Cargar el archivo de audio
    audio_original = AudioSegment.from_wav(ruta_entrada)
    # Obtener la tasa de muestreo
    tasa_muestreo = audio_original.frame_rate
    print(archivo_wav, f'Tasa de muestreo: {tasa_muestreo} Hz')
    # Obtener la duracion total del audio original en milisegundos
    duracion_total = len(audio_original)
    # Generar {cantidad_segmentos} segmentos aleatorios
    for i in range(cantidad_segmentos):
        # Calcular un punto de inicio aleatorio dentro de la duracion total - duracion del segmento
        inicio = random.randint(0, duracion_total - duracion_segmento)
        # Extraer el segmento de audio
        segmento = audio_original[inicio : inicio + duracion_segmento]
        # Crear el nombre del archivo de salida
        nombre_archivo_salida = os.path.splitext(archivo_wav)[0] + f'-s{i + 1}.wav'
        # Ruta completa del archivo de salida
        ruta_salida = os.path.join(directorio_salida, nombre_archivo_salida)
        # Exportar el segmento como un nuevo archivo WAV
        segmento.export(ruta_salida, format='wav', parameters=["-ac", "1", "-ar", str(frecuencia_muestreo_objetivo)])
        print(f'Se han generado {cantidad_segmentos} segmentos de 5 segundos cada uno para cada cancion.')