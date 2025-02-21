import os
import random
import uuid
import shutil
from tqdm import tqdm

# Function to filenames to ensure uniqueness
def unique_filename():
    return str(uuid.uuid4())

# Modified script to organize the structure as train/valid/test -> images/labels and copy files
def separate_and_split_with_structure(source_dir, base_dest, split_ratios=(0.7, 0.2, 0.1)):
    # Ensure destination directories for train, valid, and test, and subdirectories for images and labels exist
    for split in ['train', 'valid', 'test']:
        os.makedirs(os.path.join(base_dest, split, 'images'), exist_ok=True)
        os.makedirs(os.path.join(base_dest, split, 'labels'), exist_ok=True)

    for class_dir in tqdm(os.listdir(source_dir), desc=f'Copying folders'):
        class_path = os.path.join(source_dir, class_dir)
        if os.path.isdir(class_path):
            files = [f for f in os.listdir(class_path) if f.endswith('.jpg') or f.endswith('.png')]
            
            # Shuffle and split files into train, valid, and test
            random.shuffle(files)
            train_split = int(len(files) * split_ratios[0])
            valid_split = int(len(files) * (split_ratios[0] + split_ratios[1]))

            train_files = files[:train_split]
            valid_files = files[train_split:valid_split]
            test_files = files[valid_split:]

            # Function to copy files to their respective directories with progress bar
            def copy_files(file_list, split_type):
                for file in file_list:
                    image_path = os.path.join(class_path, file)
                    label_path = os.path.join(class_path, file.replace('.jpg', '.txt').replace('.png', '.txt'))
                    
                    unique_name = unique_filename()
                    image_dest_path = os.path.join(base_dest, split_type, 'images', unique_name + os.path.splitext(file)[1])
                    label_dest_path = os.path.join(base_dest, split_type, 'labels', unique_name + ".txt")
                    
                    shutil.copy(image_path, image_dest_path)  # Copy the image file
                    if os.path.exists(label_path):
                        shutil.copy(label_path, label_dest_path)  # Copy the label file

            # Copy files for train, valid, and test with progress bars
            copy_files(train_files, 'train')
            copy_files(valid_files, 'valid')
            copy_files(test_files, 'test')

# Example usage:
source_directory = "D:/maghale4/dataset/all_plants_object_detection"
base_directory = "D:/maghale4/dataset/dataset_object_yolo"

# Call the modified function with progress bar
separate_and_split_with_structure(source_directory, base_directory, split_ratios=(0.7, 0.2, 0.1))
