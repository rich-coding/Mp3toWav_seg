import os
import numpy as np
from pydub import AudioSegment

# CREATE WHITE NOISE WAV FILE. (3min)

# Duracion deseada en milisegundos (3 minutos = 180,000 milisegundos)
duracion_deseada_ms = 12500 # 50 segundos para un archivo más corto
# Escala de volumen (0.1 para un volumen muy bajo)
escala_volumen = 0.01
frecuencia_muestreo_objetivo = 44100 # Frecuencia de muestreo utilizada

# Crear un arreglo de numeros aleatorios para el sonido blanco
sonido_blanco = np.random.uniform(-0.001, 0.001, int(duracion_deseada_ms * frecuencia_muestreo_objetivo / 1000))
sonido_blanco *= escala_volumen

# Crear un segmento de audio a partir del arreglo de sonido blanco
silencio = AudioSegment(
    sonido_blanco.tobytes(),
    frame_rate=frecuencia_muestreo_objetivo,
    sample_width=2, # Ancho de muestra de 2 bytes (16 bits)
    channels=1 # 1 canal para mono
)

# Crear tres archivos de silencio idénticos
directorio_entrada = './datain' # Asumiendo que quieres guardarlo aquí también. Ajusta si es necesario.
for i in range(3):
    # Nombre del archivo de salida
    nombre_archivo_salida = f'SILENCIO-0{i + 1}.wav'
    # Ruta completa del archivo de salida
    ruta_salida = os.path.join(directorio_entrada, nombre_archivo_salida)
    # Exportar el segmento de silencio como un archivo WAV
    silencio.export(ruta_salida, format='wav')
    print(f'Se ha creado un archivo de silencio de {(duracion_deseada_ms/1000)/60} minutos: {nombre_archivo_salida}')