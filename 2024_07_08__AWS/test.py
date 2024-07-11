import subprocess
import os

def extract_frames(video_path, output_folder, fps=1):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Construir el comando ffmpeg
    command = [
        'ffmpeg',
        '-i', video_path,
        '-vf', f'fps={fps}',
        f'{output_folder}/frame_%04d.png'
    ]
    
    # Ejecutar el comando ffmpeg
    subprocess.run(command, check=True)

# Ruta del video y carpeta de salida
video_path = "videos/test.webm"
output_folder = "output_frames"

# Extraer frames
extract_frames(video_path, output_folder, fps=1)
