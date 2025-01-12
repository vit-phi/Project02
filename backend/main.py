import uuid
import cv2
import uvicorn
from fastapi import File, UploadFile, FastAPI
import numpy as np
from PIL import Image
import config
import inference

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome from the API"}

@app.post("/{style}")
def get_image(style: str, file: UploadFile = File(...)):
    try:
        image = np.array(Image.open(file.file))
        model = config.STYLES[style]
        output, resized = inference.inference(model, image)
        
        # Save the output image with a unique name
        name = f"/storage/{str(uuid.uuid4())}.jpg"
        cv2.imwrite(name, output)
        
        # Print debug information
        print(f"Generated image path: {name}")
        
        # Return the path to the saved image
        return {"name": name}
    except Exception as e:
        print(f"Error during inference: {str(e)}")
        return {"error": str(e)}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080)
