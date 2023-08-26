import os
import glob
import click

def validate_input(ctx, param, value):
  if not value:
    raise click.BadParameter('The input directory is required')

  if not os.path.exists(value):
    raise click.BadParameter('The directory does not exists')
  
  images = glob.glob(os.path.join(value, '*.jpg')) + glob.glob(os.path.join(value, '*.jpeg'))
  xmls = glob.glob(os.path.join(value, '*.xml'))

  if len(xmls) < 1:
    raise click.BadParameter('Not found XML in directory')
  
  if len(images) < 1:
    raise click.BadParameter('Not found image in directory')
  
  return value

def validate_output(ctx, param, value):
  if not value:
    raise click.BadParameter('The output directory is required')

  if not os.path.exists(value):
    os.makedirs(value)

  files = [f for f in os.listdir(value) if os.path.isdir(os.path.join(value, f))]
  if len(files) > 0:
    raise click.BadParameter('The directory is not empty')
  return value