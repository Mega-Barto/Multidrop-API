from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
import subprocess
import shutil
import os

app = FastAPI()

INPUT_FILENAME = "file.txt"
TEMP_FILENAME = "temp.txt"
OUTPUT_FILENAME = "ResultsIRRESTRICTO.txt"


def save_uploaded_file(file: UploadFile, destination: str):
    """Guarda un archivo subido en una ubicación específica."""
    with open(destination, "wb") as f:
        shutil.copyfileobj(file.file, f)


def run_megadrop(input_path: str, temp_path: str, output_path: str):
    """Ejecuta el comando Multidrop.exe y verifica su éxito."""
    command = ["powershell", ".\\Multidrop.exe", "file.txt", "1 1 1 3 2 20"]
    result = subprocess.check_call(command)

    if result.returncode != 0:
        raise RuntimeError(f"Error al ejecutar Multidrop.exe: {result.stderr.decode('utf-8')}")

    if not os.path.exists(temp_path):
        raise FileNotFoundError("El archivo temporal temp.txt no fue generado.")

    if not os.path.exists(output_path):
        raise FileNotFoundError("El archivo de salida ResultsIRRESTRICTO.txt no fue generado.")


def clean_up(files: list):
    """Elimina una lista de archivos si existen."""
    for file in files:
        if os.path.exists(file):
            os.remove(file)


@app.post("/process-file/")
async def process_file(file: UploadFile = File(...)):
    # Verifica que el archivo tenga el nombre correcto
    if file.filename != INPUT_FILENAME:
        print("Control 1")
        raise HTTPException(status_code=400, detail=f"El archivo debe llamarse {INPUT_FILENAME}")

    try:
        # Guarda el archivo subido
        print("Control 1")
        save_uploaded_file(file, INPUT_FILENAME)

        # Ejecuta el comando Multidrop.exe
        print("Control 2")
        run_megadrop(INPUT_FILENAME, TEMP_FILENAME, OUTPUT_FILENAME)

        # Devuelve el archivo resultante
        print("Control 3")
        return FileResponse(OUTPUT_FILENAME, media_type="text/plain", filename=OUTPUT_FILENAME)

    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except FileNotFoundError as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Limpia los archivos temporales
        return {"resultado": "corrió todo :v"}
