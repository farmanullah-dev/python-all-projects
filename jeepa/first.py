import os
import torch
import torchvision.transforms as transforms
from PIL import Image
from i_jepa.models.vision_transformer import vit_large 

# Load I-JEPA model
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = vit_large(img_size=224, patch_size=16).to(device)
model.eval()

# Image transformations
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

# Path to your dataset
dataset_path = r"D:\unlabeled"
image_files = [f for f in os.listdir(dataset_path) if f.endswith(('.jpg', '.jpeg', '.png'))]

# Extract feature embeddings
for img_name in image_files[:5]:  # Process first 5 images
    img_path = os.path.join(dataset_path, img_name)
    image = Image.open(img_path).convert("RGB")
    image = transform(image).unsqueeze(0).to(device)

    with torch.no_grad():
        features = model(image)  # Extract I-JEPA features

    print(f"Image: {img_name}, Feature Vector Shape: {features.shape}")
