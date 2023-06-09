# -*- coding: utf-8 -*-
"""LAB_Hw2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1LYqL2rcD51pURKnT7kng9RRDt2h_83c3
"""

import zipfile
import os
import shutil

def unzip_file(file_path, destination_path):
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        zip_ref.extractall(destination_path)

file_path = 'train.zip'  
destination_path = '/content/'

unzip_file(file_path, destination_path)


file_path = 'val.zip'  
destination_path = '/content/'

unzip_file(file_path, destination_path)

##merging the val and train datasets

import os
import shutil


folder1 = 'train'
folder2 = 'val'
merged_folder = 'merged_data'

os.makedirs(merged_folder, exist_ok=True)

# Iterate through each subfolder in folder1
for subfolder in os.listdir(folder1):
    subfolder_path = os.path.join(folder1, subfolder)
    if os.path.isdir(subfolder_path):
        merged_subfolder_path = os.path.join(merged_folder, subfolder)
        os.makedirs(merged_subfolder_path, exist_ok=True)
        
        for image in os.listdir(subfolder_path):
            image_path = os.path.join(subfolder_path, image)
            destination_path = os.path.join(merged_subfolder_path, image)
            shutil.copy2(image_path, destination_path)

# Iterate through each subfolder in folder2
for subfolder in os.listdir(folder2):
    subfolder_path = os.path.join(folder2, subfolder)
    if os.path.isdir(subfolder_path):
        merged_subfolder_path = os.path.join(merged_folder, subfolder)
        os.makedirs(merged_subfolder_path, exist_ok=True)
        
        for image in os.listdir(subfolder_path):
            image_path = os.path.join(subfolder_path, image)
            destination_path = os.path.join(merged_subfolder_path, image)
            shutil.copy2(image_path, destination_path)

!pip install imgaug

import os
import imgaug as ia
from imgaug import augmenters as iaa
from PIL import Image
import numpy as np

def augment_data(folder_path, output_folder, num_augmentations):
    seq = iaa.Sequential([
        iaa.Rotate(rotate=(-10, 10)),
        iaa.Flipud(0.5),
        iaa.Affine(rotate=(-10, 10), scale=(0.8, 1.2)),
        iaa.GaussianBlur(sigma=(0.0, 1.0)),
        iaa.AdditiveGaussianNoise(scale=(0.0, 0.05)),
        iaa.ContrastNormalization(alpha=(0.8, 1.2)),
        iaa.ElasticTransformation(alpha=(0.5, 3.0), sigma=(0.25, 0.5))
    ])

    for root, dirs, files in os.walk(folder_path):
        for dir_name in dirs:
            digit_folder_path = os.path.join(root, dir_name)
            output_digit_folder = os.path.join(output_folder, dir_name)
            os.makedirs(output_digit_folder, exist_ok=True)

            for file_name in os.listdir(digit_folder_path):
                file_path = os.path.join(digit_folder_path, file_name)
                if file_name.endswith('.png'):
                    image = Image.open(file_path)
                    output_file_name = f"original_{file_name}"
                    output_file_path = os.path.join(output_digit_folder, output_file_name)
                    image.save(output_file_path)
                    image_array = np.array(image)  # Convert PIL image to numpy array

                    # Generate augmented images
                    for i in range(num_augmentations):
                        image_aug_array = seq.augment_image(image_array)
                        image_aug = Image.fromarray(image_aug_array)  # Convert back to PIL image
                        output_file_name = f"augmented_{i}_{file_name}"
                        output_file_path = os.path.join(output_digit_folder, output_file_name)
                        image_aug.save(output_file_path)

input_folder_path = 'train'  
output_folder_path = 'augmented_datatrain'  
num_augmentations = 10  

augment_data(input_folder_path, output_folder_path, num_augmentations)

def count_items(folder_path):
    count = 0

    for root, dirs, files in os.walk(folder_path):
        count += len(dirs) 
        count += len(files) 

    return count

# Example usage
folder_path = 'augmented_datatrain' 

total_count = count_items(folder_path)
print(f"Total number of items: {total_count}")

import os
import random
import shutil

desired_count = 999

main_folder = 'augmented_datatrain'

# Iterate through each subfolder
for subfolder in os.listdir(main_folder):
    subfolder_path = os.path.join(main_folder, subfolder)
    if os.path.isdir(subfolder_path):
        augmented_images = [image for image in os.listdir(subfolder_path) if not image.startswith('original_')]
        augmented_count = len(os.listdir(subfolder_path))
        
        # If the count is greater than the desired count, remove excess images
        if augmented_count > desired_count:
            excess_images = augmented_count - desired_count
            images_to_remove = random.sample(augmented_images, excess_images)
            for image in images_to_remove:
                image_path = os.path.join(subfolder_path, image)
                os.remove(image_path)

folder_path = 'augmented_datatrain' 
total_count = count_items(folder_path)
print(f"Total number of items: {total_count}")

import shutil
import zipfile

def zip_folder(folder_path, output_path):
    shutil.make_archive(output_path, 'zip', folder_path)

folder_path = '/content/augmented_data' 


output_zip_path = '/content/augmented_data'  

zip_folder(folder_path, output_zip_path)

import os
import shutil

big_folder = 'augmented_datatrain'


train_folder = 'augmented_train'
val_folder = 'augmented_val'

s.makedirs(train_folder, exist_ok=True)
os.makedirs(val_folder, exist_ok=True)


for subfolder in os.listdir(big_folder):
    subfolder_path = os.path.join(big_folder, subfolder)
    if os.path.isdir(subfolder_path):
        train_subfolder_path = os.path.join(train_folder, subfolder)
        val_subfolder_path = os.path.join(val_folder, subfolder)
        os.makedirs(train_subfolder_path, exist_ok=True)
        os.makedirs(val_subfolder_path, exist_ok=True)
        
        # Iterate through the images in the subfolder
        for image in os.listdir(subfolder_path):
            image_path = os.path.join(subfolder_path, image)
            
            if random.random() < 0.8: 
                destination_folder = train_subfolder_path
            else:
                destination_folder = val_subfolder_path
            
            # Copy the image to the destination folder
            shutil.copy2(image_path, destination_folder)

folder_path = 'augmented_train' 
total_count = count_items(folder_path)
print(f"Total number of items: {total_count}")

folder_path = 'augmented_val' 
total_count = count_items(folder_path)
print(f"Total number of items: {total_count}")

import shutil
import zipfile

def zip_folder(folder_path, output_path):
    shutil.make_archive(output_path, 'zip', folder_path)

# Specify the folder path you want to download
train_path = '/content/augmented_train'  
val_path = '/content/augmented_val'  

# Specify the output zip file path
train_zip_path = '/content/augmented_train'  
val_zip_path = '/content/augmented_val'  

# Call the zip_folder function to create the zip file
zip_folder(train_path, train_zip_path)
zip_folder(val_path, val_zip_path)

import zipfile
import os
import shutil

def unzip_file(file_path, destination_path):
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        zip_ref.extractall(destination_path)

file_path = 'augmented_train.zip'  
destination_path = '/content/augmented_train'

unzip_file(file_path, destination_path)


file_path = 'augmented_val.zip'  
destination_path = '/content/augmented_val'

unzip_file(file_path, destination_path)

import torch
import torchvision.models as models
import torchvision.transforms as transforms
from torchvision import datasets, models, transforms
import numpy as np
import matplotlib.pyplot as plt
import os
from sklearn.decomposition import PCA


model = models.resnet50(pretrained=False)
num_classes = 10  # Number of classes in your training dataset
model.fc = torch.nn.Linear(model.fc.in_features, num_classes)
model.load_state_dict(torch.load('trained_model.pt', map_location=torch.device('cpu')))
model.eval()

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

def load_datasets(train_dir, val_dir):
    """Loads and transforms the datasets."""
    # Resize the samples and transform them into tensors
    data_transforms = transforms.Compose([transforms.Resize([64, 64]), transforms.ToTensor()])

    # Create a pytorch dataset from a directory of images
    train_dataset = datasets.ImageFolder(train_dir, data_transforms)
    val_dataset = datasets.ImageFolder(val_dir, data_transforms)

    return train_dataset, val_dataset

train_dir = os.path.join("augmented_train")
val_dir = os.path.join("augmented_val")
train_dataset, val_dataset = load_datasets(train_dir, val_dir)

class_names = train_dataset.classes
print("The classes are: ", class_names)

# Dataloaders initialization
train_dataloader = torch.utils.data.DataLoader(train_dataset, batch_size=64, shuffle=True)
val_dataloader = torch.utils.data.DataLoader(val_dataset, batch_size=64, shuffle=True)

features = []
with torch.no_grad():
    for images, _ in val_dataloader:
        features.append(model(images))
features = torch.cat(features).squeeze()

pca = PCA(n_components=2)
latent_space = pca.fit_transform(features.numpy())

plt.scatter(latent_space[:, 0], latent_space[:, 1], c=val_dataset.targets, cmap='tab10')
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.title('Latent Space Visualization')
plt.colorbar()
plt.show()

pca = PCA(n_components=3)
latent_space = pca.fit_transform(features.numpy())
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(latent_space[:, 0], latent_space[:, 1], latent_space[:, 2], c=val_dataset.targets, cmap='tab10')
ax.set_xlabel('Principal Component 1')
ax.set_ylabel('Principal Component 2')
ax.set_zlabel('Principal Component 3')
ax.set_title('Latent Space Visualization')
plt.show()