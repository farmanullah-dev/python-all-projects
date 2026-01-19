import os
from torch.utils.data import Dataset
from PIL import Image
import torchvision.transforms as transforms

class UnlabeledImageDataset(Dataset):
    def __init__(self, root_dir, transform=None):
        self.root_dir = root_dir
        self.image_files = [f for f in os.listdir(root_dir) if f.endswith(('.png', '.jpg', '.jpeg'))]
        self.transform = transform if transform else transforms.ToTensor()

    def __len__(self):
        return len(self.image_files)

    def __getitem__(self, idx):
        img_path = os.path.join(self.root_dir, self.image_files[idx])
        image = Image.open(img_path).convert("RGB")
        if self.transform:
            image = self.transform(image)
        return image

# Example usage
if __name__ == "__main__":
    dataset = UnlabeledImageDataset(root_dir="D:/unlabeled")
    print(f"Dataset size: {len(dataset)}")
    sample = dataset[0]
    print(f"Sample image shape: {sample.shape}")
