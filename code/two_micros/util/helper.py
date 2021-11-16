#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import csv
import urllib.request
from urllib import parse
from PIL import Image

def read_csv(file_name):
    records = []
    with open(file_name) as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            id = row['id']
            path = row['path']
            new_record = {'id': id, 'path': path}
            records.append(new_record)
    return records

def get_file_extension(file_path):
    path = parse.urlparse(file_path).path
    ext = os.path.splitext(path)[1]
    return ext

def download_file(url, file_path):
    ext = get_file_extension(file_path)
    with urllib.request.urlopen(url) as response, open(file_path, 'wb') as out_file:
        data = response.read()
        out_file.write(data)

def concat_two_images(img_left_path, img_right_path, img_final_path):
    img_left = Image.open(img_left_path)
    img_right = Image.open(img_right_path)

    img_width, img_height = img_left.size
    img_final = Image.new('RGB', (img_width*2, img_height))

    img_final.paste(img_left,(0,0))
    img_final.paste(img_right,(img_width, 0))
    img_final.save(img_final_path)

def check_local_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)