import click
from app import datasets, utils

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

# @click.group(context_settings=['-v', '--version'])
# def print_version(ctx, param, value):
#   if not value or ctx.resilient_parsing:
#     return
#   click.echo('Version 0.01')
#   ctx.exit()


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option()
@click.pass_context
def cli(ctx):
    pass


@cli.group()
def build():
  pass

@build.command()
@click.option('-i', '--input', type=str, help='directory where images, and annotation (Pascal VOC XML)', callback=utils.validate_input)
@click.option('-o', '--output', type=str, help='output directory images each labels', callback=utils.validate_output)
def similar(input, output):
  datasets.build_similar(input, output)

@build.command()
@click.option('-i', '--input', type=str, help='directory where images, and annotation (Pascal VOC XML)', callback=utils.validate_input)
@click.option('-o', '--output', type=str, help='output directory images each labels', callback=utils.validate_output)
def detection(input, output):
  datasets.build_detection(input, output)
