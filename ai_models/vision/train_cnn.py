import os
import json
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, models, transforms
from torch.utils.data import DataLoader
import kagglehub

def find_dataset_dirs(base_path):
    train_dir = None
    valid_dir = None
    # Kaggle extracted paths can have nested folders. E.g.
    # New Plant Diseases Dataset(Augmented)/New Plant Diseases Dataset(Augmented)/train
    for root, dirs, files in os.walk(base_path):
        if 'train' in dirs and train_dir is None:
            train_dir = os.path.join(root, 'train')
        if 'valid' in dirs and valid_dir is None:
            valid_dir = os.path.join(root, 'valid')
            
    return train_dir, valid_dir

def train_model(epochs=3, batch_size=32, save_path="offline_weights.pth"):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Training on device: {device}")

    print("Downloading dataset using kagglehub...")
    path = kagglehub.dataset_download("vipoooool/new-plant-diseases-dataset")
    print(f"Dataset downloaded to: {path}")

    train_dir, valid_dir = find_dataset_dirs(path)
    
    if not train_dir or not valid_dir:
        print("Could not find 'train' and 'valid' directories in the dataset.")
        return

    print(f"Found Train Dir: {train_dir}")
    print(f"Found Valid Dir: {valid_dir}")

    # Data augmentation and normalization for training
    data_transforms = {
        'train': transforms.Compose([
            transforms.RandomResizedCrop(224),
            transforms.RandomHorizontalFlip(),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ]),
        'valid': transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ]),
    }

    image_datasets = {
        'train': datasets.ImageFolder(train_dir, data_transforms['train']),
        'valid': datasets.ImageFolder(valid_dir, data_transforms['valid'])
    }
    
    dataloaders = {
        'train': DataLoader(image_datasets['train'], batch_size=batch_size, shuffle=True, num_workers=0),
        'valid': DataLoader(image_datasets['valid'], batch_size=batch_size, shuffle=False, num_workers=0)
    }

    class_names = image_datasets['train'].classes
    num_classes = len(class_names)
    print(f"Found {num_classes} classes.")
    
    # Save the classes mapping for the inference script
    with open('classes.json', 'w') as f:
        json.dump(class_names, f)

    model = models.mobilenet_v2(weights=models.MobileNet_V2_Weights.DEFAULT)
    # Freeze early layers
    for param in model.parameters():
        param.requires_grad = False
        
    # Replace the classifier
    model.classifier[1] = nn.Linear(model.classifier[1].in_features, num_classes)
    model = model.to(device)

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.classifier[1].parameters(), lr=0.001)

    print("Starting training loop...")
    for epoch in range(epochs):
        print(f'Epoch {epoch+1}/{epochs}')
        print('-' * 10)

        for phase in ['train', 'valid']:
            if phase == 'train':
                model.train()
            else:
                model.eval()

            running_loss = 0.0
            running_corrects = 0

            # Iterate over data. Limit for faster B.Tech demo prototype (e.g. 50 batches max)
            max_batches = 100
            for i, (inputs, labels) in enumerate(dataloaders[phase]):
                if i > max_batches:
                    break
                inputs = inputs.to(device)
                labels = labels.to(device)

                optimizer.zero_grad()

                with torch.set_grad_enabled(phase == 'train'):
                    outputs = model(inputs)
                    _, preds = torch.max(outputs, 1)
                    loss = criterion(outputs, labels)

                    if phase == 'train':
                        loss.backward()
                        optimizer.step()

                running_loss += loss.item() * inputs.size(0)
                running_corrects += torch.sum(preds == labels.data)

                if i % 20 == 0:
                    print(f"Batch {i}/{min(len(dataloaders[phase]), max_batches)}")

            epoch_loss = running_loss / (min(len(dataloaders[phase]), max_batches) * batch_size)
            epoch_acc = running_corrects.double() / (min(len(dataloaders[phase]), max_batches) * batch_size)

            print(f'{phase} Loss: {epoch_loss:.4f} Acc: {epoch_acc:.4f}')

    print(f"Training complete. Saving weights to {save_path}")
    torch.save(model.state_dict(), save_path)
    print("Done!")

if __name__ == "__main__":
    train_model(epochs=3)
