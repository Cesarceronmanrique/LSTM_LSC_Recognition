from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from dotenv import load_dotenv
import os
from fastapi.responses import JSONResponse
import subprocess
import numpy as np
from PIL import Image
import uuid
from datetime import datetime
from fastapi.responses import RedirectResponse
import mysql.connector
from mysql.connector import Error
from fastapi.responses import HTMLResponse
from Detection import Detection 
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todas las orígenes
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos
    allow_headers=["*"],  # Permitir todos los encabezados
)


# Configurar las credenciales de AWS
load_dotenv()
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = 'us-east-1'  # Reemplaza con tu región de AWS
S3_BUCKET_NAME = 'tesisreconocimientovideos'  # Reemplaza con el nombre de tu bucket
FRAMES_DIRECTORY="frames"
UPLOAD_DIRECTORY = "videos"
s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION
)



class PresignedUrlRequest(BaseModel):
    fileName: str
    fileType: str

@app.post("/presigned-url/")
async def get_presigned_url(request: PresignedUrlRequest):
    try:
        presigned_url = s3_client.generate_presigned_url(
            'put_object',
            Params={
                'Bucket': S3_BUCKET_NAME,
                'Key': request.fileName,
                'ContentType': request.fileType,
            },
            ExpiresIn=3600  # Tiempo en segundos para que la URL expire
        )
        return {"presignedUrl": presigned_url}
    except (NoCredentialsError, PartialCredentialsError) as e:
        raise HTTPException(status_code=500, detail="Error generating presigned URL")

@app.post("/upload/")
async def upload_video(file: UploadFile = File(...)):
    file_location = os.path.join(UPLOAD_DIRECTORY, file.filename)
    try:
        # Guardar el archivo subido
        with open(file_location, "wb+") as file_object:
            file_object.write(file.file.read())
        
        # Subir el archivo a S3
        #upload_to_s3(file_location, file.filename, "videos")
        
        # Extraer frames del video
        output_folder = os.path.join(UPLOAD_DIRECTORY, os.path.splitext(file.filename)[0])
        frames, s3_folder, local_frame_folder = extract_frames(file_location, output_folder, fps=1)
        print("CARPETAS FRAMES LOCAL: ", local_frame_folder)
        
        # Detección
        detect = Detection()
        prediction = detect.detection(local_frame_folder)
        print("Predicción: ", prediction)
        
        # Obtener datos de la base de datos
        if len(prediction) > 0:
            resultado = fetch_data_db("prediction")
            video_url = resultado["res_url"]
            texto = resultado["res_texto"]
            print(f"VIDEO: {video_url}, TEXTO: {texto}")
        else:
            video_url = "no se encontro video"
            texto = "No se identificaron señas en el banco de preguntas."
            print("No se identificaron señas en el banco de preguntas.")
        
        # Crear URL de redirección
        redirect_url = f"https://grabacionvidetesis.s3.amazonaws.com/index_resultados.html?videoUrl={video_url}&texto={texto}"
        print("Redirect URL: ", redirect_url)
        
        # Devolver una respuesta JSON con la URL de redirección
        return JSONResponse(content={"redirect_url": redirect_url})
    
    except subprocess.CalledProcessError as e:
        print("Error de subprocess: ", str(e))
        raise HTTPException(status_code=500, detail=f"ffmpeg error: {str(e)}")
    except Exception as e:
        print("Error general: ", str(e))
        raise HTTPException(status_code=500, detail=str(e))


def extract_frames(video_path, s3_folder, fps=10):  # Aumentar el valor de fps para obtener más frames
    try:
        # Crear un array para almacenar los frames
        frames = []
        
        # Generar una carpeta única basada en la fecha y hora actual
        if s3_folder is None:
            s3_folder = datetime.now().strftime('%Y%m%d%H%M%S') + "_" + str(uuid.uuid4())
        
        # Crear el directorio para los frames si no existe
        local_frame_folder = os.path.join(FRAMES_DIRECTORY, s3_folder)
        if not os.path.exists(local_frame_folder):
            os.makedirs(local_frame_folder)
        
        # Construir el comando ffmpeg
        command = [
            'ffmpeg',
            '-i', video_path,
            '-vf', f'fps={fps}',
            os.path.join(local_frame_folder, '%d.jpg')
        ]
        
        # Ejecutar el comando ffmpeg
        subprocess.run(command, check=True)
        
        # Leer los frames del directorio y subirlos a S3
        for frame_file in sorted(os.listdir(local_frame_folder)):
            frame_path = os.path.join(local_frame_folder, frame_file)
            frame = Image.open(frame_path)
            frames.append(np.array(frame))
            
            # Subir a S3
            upload_to_s3(frame_path, frame_file, s3_folder)
        
        return frames, s3_folder, local_frame_folder
    except Exception as e:
        print(f"Error extracting frames: {e}")
        raise
    

def upload_to_s3(file_path, file_name, s3_folder):
    s3_file_path = f"{s3_folder}/{file_name}"
    print(s3_file_path)
    with open(file_path, 'rb') as data:
        s3_client.upload_fileobj(data, S3_BUCKET_NAME, s3_file_path)


def fetch_data_db(categoria):
    connection = None
    try:
        print("ENTRO A FETCH DATA")
        # Conectar a la base de datos MySQL
        connection = mysql.connector.connect(
            host='aws-rds-mysql-tfe.cvgi8c20w6iv.us-east-1.rds.amazonaws.com',  # Reemplaza con tu host
            database='tfe',  # Reemplaza con tu base de datos
            user='admin_mysql_tfe',  # Reemplaza con tu usuario
            password='passmysql2024'  # Reemplaza con tu contraseña
        )
        if connection.is_connected():
            cursor = connection.cursor()
            # Ejecutar la consulta para obtener solo res_texto y res_uri, limitando a un registro
            query = "SELECT res_texto, res_url FROM tfe_respuesta WHERE categoria LIKE %s LIMIT 1"
            cursor.execute(query, ('%' + categoria + '%',))
            # Obtener el registro
            result = cursor.fetchone()
            
            if result:
                # Retornar el resultado como un diccionario
                return {"res_texto": result[0], "res_url": result[1]}
            else:
                return {"error": "No se encontró ningún registro que coincida con la consulta."}

    except Error as e:
        return {"error": f"Error al conectar a MySQL: {e}"}
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
            print("La conexión a MySQL se ha cerrado")
