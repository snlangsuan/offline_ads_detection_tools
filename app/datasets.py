import os
import glob
import uuid
import click
import shutil
import xml.etree.ElementTree as ET
from PIL import Image
from tqdm import tqdm
from tabulate import tabulate

def build_similar(input, output):
  files = glob.glob(os.path.join(input, '*.xml'))
  labels = set()
  img_count = 0
  object_count = 0
  labels_count = {}
  for f in tqdm(files):
    fname = os.path.basename(f).replace('.xml', '')
    source = os.path.join(input, '{}.jpg'.format(fname))
    tree = ET.parse(f)
    root = tree.getroot()
    img = Image.open(source)
    img_count += 1

    for boxes in root.iter('object'):
      label = boxes.find('name').text
      labels.add(label)
      if label not in labels_count:
        labels_count[label] = 0
      labels_count[label] += 1
      target_path = os.path.join(output, label)
      if not os.path.exists(target_path):
        os.mkdir(target_path)
      ymin, xmin, ymax, xmax = None, None, None, None
      ymin = float(boxes.find('bndbox/ymin').text)
      xmin = float(boxes.find('bndbox/xmin').text)
      ymax = float(boxes.find('bndbox/ymax').text)
      xmax = float(boxes.find('bndbox/xmax').text)
      im1 = img.crop((xmin, ymin, xmax, ymax))
      crop_name = '{}.jpg'.format(str(uuid.uuid4()))
      im1.save(os.path.join(target_path, crop_name))
      object_count += 1

  click.echo('\nSummary: {} images, {} objects'.format(img_count, object_count))
  click.echo(tabulate([[x, labels_count[x]] for x in labels_count], headers=['Class', 'Objects']) + '\n')

def voc2yolo(size, box):
  dw = 1./(size[0])
  dh = 1./(size[1])
  x = (box[0] + box[1])/2.0 - 1
  y = (box[2] + box[3])/2.0 - 1
  w = box[1] - box[0]
  h = box[3] - box[2]
  x = x*dw
  w = w*dw
  y = y*dh
  h = h*dh
  return (x,y,w,h)

def build_detection(input, output):
  files = glob.glob(os.path.join(input, '*.xml'))
  labels = { 'poster' }
  image_path = os.path.join(output, 'images')
  label_path = os.path.join(output, 'labels')

  if not os.path.exists(image_path):
    os.makedirs(image_path)
  if not os.path.exists(label_path):
    os.makedirs(label_path)

  for f in tqdm(files):
    fname = os.path.basename(f).replace('.xml', '')
    source = os.path.join(input, '{}.jpg'.format(fname))
    target_image_path = os.path.join(image_path, '{}.jpg'.format(fname))
    target_label_path = os.path.join(label_path, '{}.txt'.format(fname))
    target_label_file = open(target_label_path, 'w')
    if not os.path.exists(source):
      continue

    shutil.copyfile(source, target_image_path)
    tree = ET.parse(f)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    for boxes in root.iter('object'):
      cls_id = 0
      ymin, xmin, ymax, xmax = None, None, None, None
      ymin = float(boxes.find('bndbox/ymin').text)
      xmin = float(boxes.find('bndbox/xmin').text)
      ymax = float(boxes.find('bndbox/ymax').text)
      xmax = float(boxes.find('bndbox/xmax').text)
      b = (xmin, xmax, ymin, ymax)
      bb = voc2yolo((w,h), b)
      target_label_file.write('{} {}\n'.format(cls_id, ' '.join([str(a) for a in bb])))
    target_label_file.close()

  target_class_path = open(os.path.join(output, 'classes.txt'), 'w')
  target_class_path.write('\n'.join(list(labels)))
  target_class_path.close()


