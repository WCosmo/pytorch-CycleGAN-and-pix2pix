'''

Simple CycleGAN Dataset Creator
Based on info from: https://github.com/junyanz/pytorch-CycleGAN-and-pix2pix/blob/master/docs/datasets.md

Creates a dataset for CycleGAN training using two sets of JPG files (Domain A and B), with the option to aply some geometric data augmentation (flip and rotate).

Parameters:
--path_A: Path to input folder A
--path_B: Path to input folder B
--dataset_path: Dataset destination path
--dataset_name: Dataset name
--data_augmentation: Type of data augmentation: N (none), F (flip), R (rotate), FR (flip and rotate)

'''

import os
import shutil
import random
from PIL import Image
import argparse

def data_augmentation_info(p):
    if p == 'N':
        aug = 'None'
    if p == 'F':
        aug = 'Flip'
    if p == 'R':
        aug = 'Rotate'
    if p == 'FR':
        aug = 'Flip and Rotate'

    return aug

def count_jpg_files(folder):
    count = 0
    for file in os.listdir(folder):
        if file.endswith('.jpg'):
            count += 1
    return count

def resize_and_transfer(files, source_folder, destination_folder, data_augmentation, new_size=(256, 256)):
    for file in files:
        source = os.path.join(source_folder, file)
        destination_original = os.path.join(destination_folder, file)

        image = Image.open(source)
        resized_image = image.resize(new_size)
        resized_image.save(destination_original)

        if data_augmentation == 'F':
            flipped_image = resized_image.transpose(Image.FLIP_LEFT_RIGHT)
            destination_flip = os.path.join(destination_folder, os.path.splitext(file)[0] + '_flip.jpg')
            flipped_image.save(destination_flip)
        elif data_augmentation == 'R':
            rotated_image = resized_image.transpose(Image.ROTATE_90)
            destination_rotated = os.path.join(destination_folder, os.path.splitext(file)[0] + '_rotated.jpg')
            rotated_image.save(destination_rotated)
        elif data_augmentation == 'FR':
            flipped_image = resized_image.transpose(Image.FLIP_LEFT_RIGHT)
            destination_flip = os.path.join(destination_folder, os.path.splitext(file)[0] + '_flip.jpg')
            flipped_image.save(destination_flip)
            rotated_image = resized_image.transpose(Image.ROTATE_90)
            destination_rotated = os.path.join(destination_folder, os.path.splitext(file)[0] + '_rotated.jpg')
            rotated_image.save(destination_rotated)


def split_train_test(source_folder, train_destination, test_destination, proportion=0.7, data_augmentation='N'):

    os.makedirs(train_destination, exist_ok=True)
    os.makedirs(test_destination, exist_ok=True)

    files = os.listdir(source_folder)
    random.shuffle(files)
    num_train = int(proportion * len(files))

    train_files = files[:num_train]
    test_files = files[num_train:]

    resize_and_transfer(train_files, source_folder, train_destination, data_augmentation)
    resize_and_transfer(test_files, source_folder, test_destination, data_augmentation)

    return len(train_files), len(test_files)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Split folders A and B into training and test sets')
    parser.add_argument('--path_A', type=str, default='./A', help='Path to folder A')
    parser.add_argument('--path_B', type=str, default='./B', help='Path to folder B')
    parser.add_argument('--dataset_path', type=str, default='./', help='Dataset path')
    parser.add_argument('--dataset_name', type=str, default='dataset', help='Dataset name')
    parser.add_argument('--data_augmentation', type=str, default='N', choices=['N', 'F', 'R', 'FR'],
                        help='Type of data augmentation: N (none), F (flip), R (rotate), FR (flip and rotate)')
    args = parser.parse_args()

    print('\nSimple CycleGAN dataset creator\n')
    print('Dataset name: ', args.dataset_name)
    print('Domain A folder: ', args.path_A)
    print('Domain B folder: ', args.path_B)
    print('Data Augmentation: ', data_augmentation_info(args.data_augmentation))

    folder_A = args.path_A
    folder_B = args.path_B
    train_folder_A = os.path.join(os.path.dirname(folder_A), str(args.dataset_path + args.dataset_name), 'trainA')
    test_folder_A = os.path.join(os.path.dirname(folder_A), str(args.dataset_path + args.dataset_name), 'testA')
    train_folder_B = os.path.join(os.path.dirname(folder_B), str(args.dataset_path + args.dataset_name), 'trainB')
    test_folder_B = os.path.join(os.path.dirname(folder_B), str(args.dataset_path + args.dataset_name), 'testB')

    num_train_A, num_test_A = split_train_test(folder_A, train_folder_A, test_folder_A, data_augmentation=args.data_augmentation)
    num_train_B, num_test_B = split_train_test(folder_B, train_folder_B, test_folder_B, data_augmentation=args.data_augmentation)

    num_jpg_train_A = count_jpg_files(train_folder_A)
    num_jpg_test_A = count_jpg_files(test_folder_A)
    num_jpg_train_B = count_jpg_files(train_folder_B)
    num_jpg_test_B = count_jpg_files(test_folder_B)

    print('\nDataset created: ', str(args.dataset_path + args.dataset_name))
