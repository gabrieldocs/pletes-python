import os
import zipfile

import docker
from fastapi import APIRouter, UploadFile
from fastapi.responses import JSONResponse

client = docker.from_env()

router = APIRouter(
    prefix="/projects",
    tags=["projects"]
)

UPLOAD_FOLDER = "uploads"

@router.post("/github/receive-push")
async def upload_file(file: UploadFile):
    try:
        # Create the uploads folder if it doesn't exist
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)

        # Save the uploaded file to the uploads folder
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())

        # Create a folder with the same name as the uploaded file
        extract_folder = os.path.join(UPLOAD_FOLDER, os.path.splitext(file.filename)[0])
        os.makedirs(extract_folder, exist_ok=True)

        # Extract the contents of the ZIP file to the folder
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(extract_folder)

        # Call the build_docker_image function after extraction is completed
        print(os.path.join(extract_folder, os.path.splitext(file.filename)[0]))
        build_result = build_docker_image((os.path.join(extract_folder, os.path.splitext(file.filename)[0])))

        if "error" in build_result:
            # Handle error if Docker image build fails
            return JSONResponse(status_code=500, content={"message": "Failed to build Docker image", "error": build_result["error"]})
        else:
            return JSONResponse(status_code=201, content={"message": "File uploaded, extracted, and Docker image built successfully", "extract_folder": extract_folder})
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": "Internal Server Error", "error": str(e)})

def build_docker_image(folder_path: str):
    try:
        # Check if the Dockerfile exists in the extracted folder
        dockerfile_path = os.path.join(folder_path, "Dockerfile")
        if not os.path.exists(dockerfile_path):
            return {"error": "Dockerfile not found in the extracted folder"}

        # Extract the name of the folder from the folder path
        image_name = os.path.basename(folder_path)

        # Build the Docker image using the Dockerfile in the extracted folder
        build_logs = client.api.build(path=folder_path, dockerfile="Dockerfile", tag=image_name, rm=True, decode=True)

        # Log each line of the build output
        for line in build_logs:
            if 'stream' in line:
                print(line['stream'].strip())

        return {"message": "Docker image built successfully", "image_name": image_name}
    except docker.errors.BuildError as e:
        return {"error": f"Failed to build Docker image: {e}"}
    except Exception as e:
        return {"error": str(e)}
    
    
@router.get("/container/file-content")
def get_file_content(image_name: str, tag: str, file_path: str) -> str:
    try:
        # Specify the Docker image and tag
        image = f'{image_name}:{tag}'
        
        # Specify the container options
        container_options = {
            'image': image,  # Specify the Docker image and tag
            'tty': True,  # Enable TTY to capture the output
            'command': ['cat', file_path],  # Command to execute (read the file)
            'detach': True  # Run the container in the background and return a container object
        }

        # Create and start the container
        container = client.containers.run(**container_options)

        # Retrieve the container logs
        output = container.logs().decode('utf-8').strip()

        # Remove the container after retrieving the output
        container.remove()

        return output
    except Exception as e:
        return str(e)