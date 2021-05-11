import click
import yaml
from fspathtree import fspathtree
import lxml
import lxml.html
import html5print

import os
import sys
import stat
import fnmatch
import shutil
import platform
import logging
import itertools
from pathlib import Path
import subprocess
import locale
import importlib.util
import inspect
import urllib.parse
import tempfile
import re
import configparser
import json
import pprint
import time
import hashlib
import shlex

locale.setlocale(locale.LC_ALL,'')
encoding = locale.getpreferredencoding()





def error(msg):
  click.echo(click.style(msg,fg='red'))

def sucess(msg):
  click.echo(click.style(msg,fg='green'))

def info(msg):
  click.echo(msg)


def stringify_html(elem, pretty=False):
  text = lxml.html.tostring(elem).decode(encoding)
  if pretty:
    text = html5print.HTMLBeautifier.beautify(text)
  return text

def to_kabab(text):
  return text.lower().replace(" ","-")

def make_input_element(desc):
    '''Build an HTML input element from a tree description.'''
    if desc is None or desc.get('elem_type',None) is None:
      return None
    

    elem = lxml.etree.Element(desc['elem_type'])

    if desc['elem_type'] == "input":
      if desc.get('default',None):
        elem.attrib['value'] = desc['default']
      if desc.get('placeholder',None):
        elem.attrib['placeholder'] = desc['placeholder']
    if desc['elem_type'] == "select":
      for opt in desc.get('options',[]):
        option = lxml.etree.Element("option")
        option.text = opt
        option.attrib['value'] = to_kabab(opt)
        elem.append(option)

    for attr in desc.get('attributes',[]):
      elem.attrib[attr['name']] = attr['value']

    return elem





@click.group(context_settings=dict(ignore_unknown_options=True))
@click.option("--verbose","-v",is_flag=True,help="Print verbose messages.")
@click.pass_context
def main(ctx,verbose):
  '''
  Clark's Web UI Utilities
  '''


@main.command()
@click.argument("ui-description",type=click.File('r'))
@click.option("--output","-o",default='-',type=click.File('w'))
@click.pass_context
def parameter_input_ui(ctx,ui_description,output):
  ui_description = fspathtree(yaml.safe_load(ui_description))

  
  ui_element = lxml.etree.Element("div")
  ui_element.attrib['class'] = 'user-input-area'
  ui_element.attrib['id'] = 'user-input'
  ui_element.attrib['style'] = f'display:grid;grid-gap:10px;grid-template-columns:auto 2fr auto;grid-template-rows:repeat({len(ui_description.get("inputs",[]))}, 30px)'

  for item in ui_description.get("inputs",[]):


    label_elem = lxml.etree.Element("label")
    input_elem = make_input_element(item)
    metad_elem = make_input_element(item.get("metadata",None))


    # create label
    if item.get("label",None):
      label_elem.text = item["label"]
      label_elem.attrib['class'] = 'user-input-lbl'
      ui_element.append(label_elem)

    id = None
    if item.get("id-prefix",None):
      id = f"{item['id-prefix']}-val"
    else:
      if item.get("label",None):
        id = f"{to_kabab(item['label'])}-val"

    if id:
      input_elem.attrib['id'] = f"{id}-val"

    input_elem.attrib['class'] = 'user-input-val'
    ui_element.append(input_elem)

    if metad_elem is not None:
      metad_elem.attrib['class'] = 'user-input-meta'
      ui_element.append(metad_elem)
    







  output.write(stringify_html(ui_element,True))



