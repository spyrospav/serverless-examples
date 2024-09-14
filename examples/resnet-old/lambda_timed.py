import time
IMPORT_START_TIME = time.time()
import numpy as np
import torch
from PIL import Image
from torchvision import transforms
IMPORT_END_TIME = time.time()
print(f"<import {IMPORT_END_TIME - IMPORT_START_TIME} seconds>")
img_tranforms = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406],
                         [0.229, 0.224, 0.225])
])

def classify_image(model_path, img):

    model = torch.jit.load(model_path)
    img = img_tranforms(img).unsqueeze(0)
    cl = model(img).argmax().item()

    return cl

def lambda_handler(event, context):

    img = Image.fromarray(np.random.rand(224, 224, 3).astype(np.uint8))

    # classify image
    model_path = "./examples/resnet/resnet34.pt"
    cl = classify_image(model_path, img)

    return {
        'statusCode': 200,
        'class': cl
    }
    
if __name__ == '__main__':
    print(lambda_handler(None, None))
