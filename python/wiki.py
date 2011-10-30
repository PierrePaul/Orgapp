#!/usr/bin/env python2
import os
try:
  import io
except:
  import StringIO 
  io = StringIO
try:
  import textile
except Exception:
  pass
from bottle import route, run, static_file, redirect
from bottle import view, template
from bottle import get, post, request, error

@route('/home')
def home():
  return redirect('/')

@route('/')
@view('base')
def home(page='home'):
    return dict(content='<p>Hello, how are you?</p>',
                page=page)

def render_textile(raw):
  return textile.textile(raw)

@route('/wiki')
@route('/wiki/')
@route('/wiki/:page#.+#')
@view('wiki_2col')
def wiki(page=''):
  fullpath = './wiki/%s' % page
  if not os.path.isfile(fullpath):
    if os.path.isdir(fullpath):
      files = os.listdir(fullpath)
      dirname = fullpath
      if os.path.exists(fullpath+'index'): page = page + 'index'
      else: page = page +'/'+ files[0]
    else:
      dirname = '/wiki'
  else: 
    files = os.listdir(os.path.dirname(fullpath))
    dirname = os.path.dirname(fullpath)
  if not page: page = 'index' 
  input_str = static_file(page, root='./wiki').output.read()
  try:
    import textile
  except Exception:
    input_str = input_str.decode().replace('\n','<br/>')
    return dict(page=page,content=input_str, files=files, path=dirname)
  else:
    return dict(page=page+"_textile",content=render_textile(input_str), files=files, path=dirname)

@route('/static/:filename#.+#')
def server_static(filename):
    return static_file(filename, root='./static')

@error(404)
def error404(error):
    return 'you might be looking for something you won\'t get'

import bottle
bottle.debug(True)
run(host='localhost', port=8080,reloader=True)
#run(host='172.16.0.163', port=8080)
