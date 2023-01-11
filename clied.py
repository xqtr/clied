#!/bin/python3
import curses
import sys,os
import urllib.request
from pygments.lexer import RegexLexer, inherit, words, bygroups
from pygments.lexers import PythonLexer, CLexer, BBCodeLexer, DelphiLexer, \
     HtmlLexer,QBasicLexer,BashLexer
from pygments.formatters import TerminalFormatter
from pygments.token import Keyword, Name, Comment, String, Error, \
     Number, Operator, Generic, Token, Whitespace, Text, Punctuation
from pygments import highlight
import subprocess
import datetime
from time import sleep
import string
import json
import shlex
import pyperclip
import socket
import re
from spellchecker import SpellChecker

#change the language to your liking: English - ‘en’, Spanish - ‘es’, French - ‘fr’,
# Portuguese - ‘pt’, German - ‘de’, Russian - ‘ru’, Arabic - ‘ar’
spell = SpellChecker(language='en')

GOPHER = {"host":"localhost","port":"70","width":76,"hr":"-"*76}
PATHSEP = {"win32":"\r\n", 'linux':"\n" } 
PLATFORM = sys.platform

COLOR_SCHEME = {
  Token:              ('gray',                 'gray'),
  Comment:            ('magenta',     'red'),
  Comment.Preproc:    ('magenta',     'brightmagenta'),
  Keyword:            ('blue',            'brightcyan'),
  Keyword.Type:       ('green',       '*brightgreen*'),
  Operator.Word:      ('**',                     '**'),
  Name.Builtin:       ('*',           '*'),
  Name.Function:      ('blue',           'blue'),
  Name.Class:         ('_green_',        'brightblue'),
  Name.Decorator:     ('magenta',     'brightmagenta'),
  Name.Variable:      ('blue',           'brightblue'),
  String:             ('yellow',       'yellow'),
  Number:             ('brightcyan',     'green')
}

COMPILE = {
  'py':'python3 -m py_compile ',
  'pas':'fpc -gl ',
  'mpl':'/home/x/mys47b/mplc ',
  'mpy':'/home/x/mys47b/mplc '
}

ansi = {
  'clear':"\033[2J",
  'ceol':"\033[K",
  'cbol':"\033[1K",
  'cline':"\033[2K",
  'home':"\033[1;1H",
  'goto':"\033[y;xH",
  'hide':'\033[?25l',
  'show':'\033[?25h',
  'up':'\033[A',
  'down':'\033[B',
  'right':'\033[C',
  'left':'\033[D',
  'next':'\033[E',
  'pos':'\033[6n',
  'save':'\033[s',
  'restore':'\033[u',
  'bold':'\033[1m',
  'faint':'\033[2m',
  'italic':'\033[3m',
  'underline':'\033[4m',
  'blink':'\033[5m'
}

colors = {
  'reverse':'\x1b[7m',
  'reset':"\033[0m",
  0:"\033[0;30m",
  1:"\033[0;34m",
  2:"\033[0;32m",
  3:"\033[0;36m",
  4:"\033[0;31m",
  5:"\033[0;35m",
  6:"\033[0;33m",
  7:"\033[0;37m",
  8:"\033[1;30m",
  9:"\033[1;34m",
  10:"\033[1;32m",
  11:"\033[1;36m",
  12:"\033[1;31m",
  13:"\033[1;35m",       
  14:"\033[1;33m",
  15:"\033[1;37m",
  16:"\033[40m",
  17:"\033[44m",
  18:"\033[42m",
  19:"\033[46m",
  20:"\033[41m",
  21:"\033[45m",
  22:"\033[43m",      
  23:"\033[47m"
}

colornames = {
  0:"black",
  1:"blue",
  2:"green",
  3:"cyan",
  4:"red",
  5:"magenta",
  6:"brown",
  7:"grey",
  8:"darkgrey",
  9:"lightblue",
  10:"lightgreen",
  11:"lightcyan",
  12:"lightred",
  13:"lightmagenta",       
  14:"yellow",
  15:"white"
}

colorsbg = {
  0:"\033[1;30m",
  1:"\033[1;34m",
  2:"\033[1;32m",
  3:"\033[1;36m",
  4:"\033[1;31m",
  5:"\033[1;35m",
  6:"\033[1;33m",
  7:"\033[1;37m",
}

COLOR_TEXT = colors[7]+colors[16]
COLOR_STATUS = colors[0]+colors[23]
COLOR_SUGGEST_NORMAL = colors[0]+colors[22]
COLOR_SUGGEST_CODE = colors[0]+colors[18]
COLOR_SUGGEST_ERROR = colors[0]+colors[20]

BLOG_POST = '''===============================================================================
 Title  :
 Date   : 
 Author :
===============================================================================



- Links -----------------------------------------------------------------------


= END ========================================================================='''

SCRIPT_BODY = '''#!/bin/bash
       
#title        :
#description  : 
#author       :
#date         :
#version      :
#usage        :
#notes        :'''

PYTHON_PROGRAM = '''#!/usr/bin/python3

# -*- coding: utf-8 -*-

import os, sys

if __name__ == '__main__':
    print('hello world')'''

PASCAL_UNIT = '''Unit unitname;

Interface

Uses
  crt;

{$I include.pas}

Var
  i:byte;


Implementation

Uses
  dos;

begin

end.'''
HTML_BODY = '''<!doctype html>
<html>
<head>
  <link rel="stylesheet" href="styles.css">
  <meta charset="utf-8">
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
</head>
<body>
  
</body>
</html>'''

BSD_NOTICE = '''/*
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are
 * met:
 * 
 * * Redistributions of source code must retain the above copyright
 *   notice, this list of conditions and the following disclaimer.
 * * Redistributions in binary form must reproduce the above
 *   copyright notice, this list of conditions and the following disclaimer
 *   in the documentation and/or other materials provided with the
 *   distribution.
 * * Neither the name of the  nor the names of its
 *   contributors may be used to endorse or promote products derived from
 *   this software without specific prior written permission.
 * 
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
 * "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
 * LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
 * A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
 * OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
 * SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
 * LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
 * DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
 * THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
 * OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 * 
 */'''
 
GPL_NOTICE = '''/*
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 * 
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
 * MA 02110-1301, USA.
 * 
 */
'''

class MPLLexer(DelphiLexer):
    name = 'mpl'
    aliases = ['mpl']
    filenames = ['*.mpl']
    EXTRA_KEYWORDS = set(('clrscr','clreol','gotoxy','wherex','wherey','dispfile','disptemplate','outbs','textcolor',
'outpipe','outpipeln','outraw','outrawln','bufaddstr','bufflush','readkey','getkey','getyn',
'getstr','pause','more','onekey','stuffkey','delay','mci2str','sysoplog','acs','hangup',
'keypressed','upuser','nodenum','strpadr','strpadl','strpadc','strrep','strcomma','stri2s',
'strs2i','stri2h','strwordget','strwordpos','strwordnum','strstripl','strstripr','strstripb',
'strstriplow','strstripmci','strmcilen','strinitials','strwrap','strreplace','readenv',
'fileexist','fileerase','direxist','timermin','timersec','datedos','datejulian','datedos2str',
'datejulian2str','datestr2dos','datestr2julian','dateg2j','datej2g','datevalid','timedos2str',
'daysago','justfile','justfilename','justfileext','fassign','freset','frewrite','fclose',
'fseek','feof','fread','fwrite','freadln','fwriteln','pathsep','menucmd','bitcheck','bittoggle',
'bitset','getprompt','getpromptinfo','getscreeninfo','getscreenchar','getscreenattr',
'getthisuser','putthisuser','getuser','putuser','getuserbyname','getuserbyid','getsauce',
'isuser','justpath','settimeleft','setpromptinfo'))

    def get_tokens_unprocessed(self, text):
        for index, token, value in DelphiLexer.get_tokens_unprocessed(self, text):
            if token is Name and value in self.EXTRA_KEYWORDS:
                yield index, Keyword, value
            else:
                yield index, token, value
                
class MPYLexer(PythonLexer):
    name = 'mpy'
    aliases = ['mpy']
    filenames = ['*.mpy']
    EXTRA_KEYWORDS = set(('dated2u','datestr','dateu2d','delay','charxy','flush','gotoxy','mci2str','pause',
'pwrite','pwriteln','rwrite','rwriteln','showfile','termsize','textattr','textcolor',
'wherex','wherey','write','writeln','writexy','backspace','getkey','getyn',
'keypressed','onekey','purgeinput','stuffkey','getprompt','setpinfo','setprompt',
'access','acsnogroup','getmbase','getmbaseid','getmgroup','getmgroupid','msg_close',
'msg_delete','msg_found','msg_gethdr','msg_gettxt','msg_next','msg_open','msg_prev',
'msg_seek','msg_getlr','msg_setlr','msg_stats','fl_close','fl_found','fl_getdesc',
'fl_getfile','fl_next','fl_open','fl_prev','fl_seek','getfbase','getfbaseid',
'getfgroup','getfgroupid','getnetaddr','logerror','mci2str','menucmd','param_count',
'param_str','shutdown','sysoplog','upuser','getcfg','getfbase','getfbaseid',
'getfgroup','getfgroupid','getmbase','getmbaseid','getmgroup','getmgroupid',
'getnetaddr','getuserid','msg_gethdr'))

    def get_tokens_unprocessed(self, text):
        for index, token, value in PythonLexer.get_tokens_unprocessed(self, text):
            if token is Name and value in self.EXTRA_KEYWORDS:
                yield index, Keyword, value
            else:
                yield index, token, value

# adds a path delimeter at the end of the path, if doesn't exist
def dirslash(d):
  if d[-1:]!=os.sep:
    d = d+os.sep
  return d
  
# a regex simple replace function used in the gophermap function
def replace(s,old,new):
  a = re.sub(old, new, s, flags=re.IGNORECASE)
  return a
  
# return the output of figlet, used for the [h1], [h2] bbcodes for gopher files
def figleth1(text):
  k = subprocess.check_output('figlet '+text, shell=True)
  return k.decode().splitlines()
  
def figleth2(text):
  k = subprocess.check_output('figlet '+text+' -f small', shell=True)
  return k.decode().splitlines()

# checks if a CRLF is in file, if it is, then the file is in DOS/WIN format    
def isdosfile(fn): #
  if "\r\n" in open(fn,"rb").read().decode():
    return 'win32'
  else:
    return 'linux'

# sets and returns the correct CRLF type, according to the choosing of the user
def crlf(default=None):
  global PATHSEP, PLATFORM
  if default:
    s = default.upper()
    if s == 'WIN' or s == 'WINDOWS' or s == 'WIN32':
      PLATFORM = 'win32'
    elif s == 'DOS':
      PLATFORM = 'win32'
    elif s == 'LINUX' or s == 'LIN' or s == 'UNIX':
      PLATFORM = 'linux'
    elif s == '\n':
      PLATFORM = 'linux'
    elif s == '\r\n':
      PLATFORM = 'win32'
  return PATHSEP[PLATFORM]

# full paragraph justify function. 
# the function is from here: https://github.com/KonstantinosAng/CodeWars/blob/master/Python/%5B4%20kyu%5D%20Text%20align%20justify.py  
def justify(text, width):
    if not text: return ''
    if width == 0: return ''
    if not isinstance(text, str): return ''
    if len(text.split()) == 1: return text.strip() + '\n'
    t, l, ret = text.split(), [], ''
    for i, w in enumerate(t):
        l.append(w + ' ')
        if i + 1 <= len(t) - 1:
          if len(''.join(x for x in l) + t[i + 1]) > width:
              j, l[-1] = 0, l[-1].strip()
              if len(l) > 2:
                  while len(''.join(x for x in l)) < width:
                      l[j] += ' '
                      if j == len(l) - 2:
                          j = 0
                          continue
                      j += 1
              else:
                  if len(l) == 2:
                      l[1] = ''.join(c for c in l[1] if c != ' ')
                      while len(''.join(x for x in l)) < width:
                          l[0] += ' '
                  if len(l) == 1:
                      l[0] = l[0].strip()
              ret += ''.join(x for x in l) + '\n'
              l = []
        else:
            ret += (''.join(x for x in l)).strip() + '\n'
            l = []
    return ret
# writes text to the screen
def writetext(ln):
  sys.stdout.write(ln)
  sys.stdout.flush()
# strips any ansi codes from a string
def stripansi(line):
  ansi_escape = re.compile(r'(?:\x1B[@-_]|[\x80-\x9F])[0-?]*[ -/]*[@-~]')
  return ansi_escape.sub('', line)
# left justifies a line that may contain ansi codes, so the actual text has the preferred width
def ljustansi(line,w):
  dx = len(line) - len(stripansi(line))
  if len(stripansi(line))>w:
    return line[:w+dx]
  while len(stripansi(line)) < w: line+=' '
  return line
# gets the actual local ip
def get_ip():
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  s.settimeout(0)
  try:
    # doesn't even have to be reachable
    s.connect(('10.254.254.254', 1))
    IP = s.getsockname()[0]
  except Exception:
    IP = '127.0.0.1'
  finally:
    s.close()
  return IP
# this function translates a bbcode file to a gophermap file. read help text.
def gophermap(sfile,dfile,ismap=True):
  global GOPHER
  f = open(sfile,'r')
  lines = f.read().splitlines()
  f.close()
  i = 0
  l = ''
  output = []
  while i<len(lines):
    l = lines[i]
    linetype = ""
    # this code is to ignore the text between in gophermap files
    if '[#WWW]' in l.upper():
      i += 1
      l = lines[i]
    #INCLUDE, includes an external file
    if '[INCLUDE]' in l.upper():
      l= replace(l,'\[include\]','')
      l= replace(l,'\[/include\]','')
      incfile = l
      if not os.path.isfile(incfile):
        incfile=programpath+incfile
        if not os.path.isfile(incfile):
          incfile = dirslash(home_folder)+ l
      if os.path.isfile(incfile):
        inc = open(incfile,'r')
        alist = inc.read().splitlines()
        for a in alist:
          output.append('i'+a+'\t\n')
        lines[i]=' '
        l=' '
        linetype = 'include'
      else:
        print('! Included file: '+l.ljust(30,' ')+' not found')
     # VARIOUS REPLACES
    l = replace(l,'\[#gopher\]','') # ignores the text when translating in www mode
    l = replace(l,'\[/#gopher\]','')
    # insert date and time
    l = replace(l,'\[date\]',datetime.datetime.now().strftime("%Y/%m/%d")) 
    l = replace(l,'\[time\]',datetime.datetime.now().strftime("%H:%M:%S"))
    # inserts an ascii ruler
    l = replace(l,'\[hr\]',GOPHER['hr'])
    l = replace(l,'\[host\]',GOPHER['host'])
    l = replace(l,'\[port\]',GOPHER['port'])
    # makes a shell type line in gopher
    l = replace(l,'\[shell\]','=')
    l = replace(l,'\[/shell\]','')
    #H1, uses figlet to make some nice font
    if '[H1]' in l.upper():
      l= replace(l,'\[h1\]','')
      l= replace(l,'\[/h1\]','')
      #l = l.strip()
      h1 = figleth1(l)
      for h in h1:
        if h.strip()!="":
          #output.append('i'+h+'\t\n')
          output.append(h+'\n')
      linetype = "include"
    if '[H2]' in l.upper():
      l= replace(l,'\[h2\]','')
      l= replace(l,'\[/h2\]','')
      #l = l.strip()
      h2 = figleth2(l)
      for h in h2:
        if h.strip()!="":
          #output.append('i'+h+'\t\n')
          output.append(h+'\n')
      linetype = "include"
    # used to insert an empty line
    if '[EMPTY]' in l.upper():
      linetype = "include"
      output.append('\n')
    #CENTER, center align text
    if '[CENTER]' in l.upper():
      l= replace(l,'\[center\]','')
      l= replace(l,'\[/center\]','')
      l = l.strip()
      l = l.center(WIDTH,' ')
    #RIGHT, right align text
    if '[RIGHT]' in l.upper():
      l= replace(l,'\[right\]','')
      l= replace(l,'\[/right\]','')
      l = l.strip()
      l = l.rjust(WIDTH,' ')
    # marks a file, gopher item
    if '[FILE]' in l.upper():
      l = replace(l,'\[file\]','0')
      l = replace(l,'\[/file\]','')
    # marks a binfile, gopher item
    if '[BIN]' in l.upper():
      l = replace(l,'\[bin\]','9')
      l = replace(l,'\[/bin\]','')
      linetype = 'bin'
    # marks an image gopher item
    if '[IMG]' in l.upper():
      l = replace(l,'\[img\]','I')
      l = replace(l,'\[/img\]','')
      linetype = 'bin'
    # marks a directory gopher item
    if '[DIR]' in l.upper():
      l = replace(l,'\[dir\]','1')
      l = replace(l,'\[/dir\]','')
    # marks  a url gopher item
    if '[URL]' in l.upper():
      l = replace(l,'\[url\]','1')
      l = replace(l,'\[/url\]','')
    # inserts a tab character
    l = replace(l,'\[tab\]','\t')
    
    if l.strip()[0:1]=='=':
      linetype = "shell"
      l = l
    elif l.strip()[0:1]=='0':
      linetype = "textfile"
      l = l
    elif l.strip()[0:1]=='1':
      linetype = "dir"
      l = l+'\t'
    elif l.strip()[0:1]=='!':
      linetype = "title"
      l = l+'\t'
    elif linetype == "":
      if ismap:
        #l = 'i'+l+'\t'
        l = l
      else:
        l = l
    if linetype != 'include':
      output.append(l+'\n')
    i += 1  
  f = open(dfile,'w+')
  f.writelines(output)
  f.close

class Editor():
  def __init__(self):
    self.screen = curses.initscr()
    self.screen.keypad(True)
    self.screen.nodelay(1)
    self.msg=""
    self.autoindent = True
    self.autosuggest = False
    self.autohint = False
    self.modified = False
    self.tab = 2
    self.seperators = " ,.()+-/*=~%<>[];{}"
    self.ROWS, self.COLS = self.screen.getmaxyx()
    self.bottom = self.ROWS-1
    self.statusy = self.ROWS
    self.suggesty = self.ROWS-1
    self.insert = True
    self.code_hints = {}
    curses.raw()
    curses.noecho()
    self.history = []
    self.filetype = 'txt'
    self.lexers = { 'py': PythonLexer, 'c': CLexer, 'bb':BBCodeLexer, 'pas':DelphiLexer, \
                    'htm':HtmlLexer, 'bas':QBasicLexer, 'sh':BashLexer, 'mpl':MPLLexer, \
                    'mpy':MPYLexer}
    #comment symbols for filetypes. 'type':'single','multi-start','multi-end',has-multi
    self.comments = {'py':["#","'''","'''",True],'mpy':["#","'''","'''",True],\
                      'pas':['//','{','}',True],'mpl':['//','(*','*)',True],\
                      'sh':['#','#','#',False],'bas':["'","'","'",False],'bb':['#','#','#',False],
                      'htm':['','<!--','-->',True],'c':['//','/*','*/',True]
                      }
    self.windows = []
    self.active = 0
    for i in range(5):
      self.windows.append({'filename':'untitled.txt',
      'curx':0,
      'cury':0,
      'indent':True,
      'width':80,
      'suggest':False,
      'tab':2,
      'insert':True,
      'buff':[[]],
      'total':1,
      'hint':False,
      'modified':False,
      'filetype':'txt',
      'offx':0,
      'offy':0,
      'bookmarks':[],
      'bookindex':0
      })
    #undo stuff
    self.uindex = 0
    self.umax   = 10
    self.ucount = 0
    self.usteps = 20
    self.ustates = []

  def reset(self):
    self.curx = 0
    self.cury = 0
    self.offx = 0
    self.offy = 0
    self.width = 80
    self.history.clear()
    self.msg=""
    self.autoindent = True
    self.seperators = " ,.()+-/*=~%<>[];"
    self.buff = []
    self.total_lines = 0
    self.filename = 'untitled.txt'
    self.modified = 0
    self.code_hints.clear()
    self.filetype = 'txt'
    self.search_results = []
    self.search_index = 0
    self.bookmarks = []
    self.bookindex = 0
  
  def addstate(self):
    self.ucount = 0
    self.uindex += 1
    if self.uindex >= self.umax: 
      del self.ustates[0]
      self.uindex = self.umax - 1
    elif self.uindex < self.umax:
      del self.ustates[self.uindex:]
    state = [self.buff.copy(),self.curx,self.cury,self.offx,self.offy,self.total_lines]
    self.ustates.append(state)
    #self.msg = str(self.uindex)+'/'+str(len(self.ustates))
  
  def undo(self):
    if self.uindex == 0: return
    if len(self.ustates) == 0: return
    self.ucount = 0
    self.uindex -= 1
    self.curx = self.ustates[self.uindex][1]
    self.cury = self.ustates[self.uindex][2]
    self.offx = self.ustates[self.uindex][3]
    self.offy = self.ustates[self.uindex][4]
    self.total_lines = self.ustates[self.uindex][5]
    del self.buff[:]
    self.buff = self.ustates[self.uindex][0].copy()
    #self.msg = str(self.uindex)+'/'+str(len(self.ustates))
    self.scroll_buffer()
    self.update_screen()
    
  def addstep(self,step=1):
    self.ucount += step
    if self.ucount >= self.usteps:
      self.addstate()
      self.ucount = 0
    
  def is_separator(self, c):
    for ch in self.seperators:
      if c == ch:
        return True
    return False
  
  def insert_char(self, c):
    global spell
    self.addstep()
    if self.insert:
      if len(self.buff[self.cury])+1<=self.width:
        self.buff[self.cury].insert(self.curx, c)
        self.curx += 1
        self.modified += 1
      if self.curx == self.width:
        self.insert_line()      
        self.modified += 1
    else:
      self.move_cursor(curses.KEY_RIGHT)
      self.delete_char()
      self.buff[self.cury].insert(self.curx, c)
      self.move_cursor(curses.KEY_RIGHT)
      self.modified += 1
  
  def del_char(self):
    if self.cury == len(self.buff)-1 and len(self.buff[self.cury])==0: return
    if self.curx<=len(self.buff[self.cury])-1:
      self.addstep()
      del self.buff[self.cury][self.curx]
      self.modified += 1
    #elif self.curx == 0 and self.cury and len(self.buff[self.cury])==0:
    elif self.cury and len(self.buff[self.cury])==0:
      self.addstate()
      oldline = self.buff[self.cury][self.curx:]
      del self.buff[self.cury]
      #self.cury -= 1
      self.curx = 0
      self.buff[self.cury] += oldline
      self.total_lines -= 1
    elif self.curx == len(self.buff[self.cury]) and self.cury<len(self.buff)-1:
      self.addstate();
      oldline = self.buff[self.cury+1]
      del self.buff[self.cury+1]
      #self.cury -= 1
      self.buff[self.cury] += oldline
      self.total_lines -= 1
  
  def delete_char(self):
    if self.curx:
      self.addstep()
      self.curx -= 1
      del self.buff[self.cury][self.curx]
    elif self.curx == 0 and self.cury:
      self.addstate()
      oldline = self.buff[self.cury][self.curx:]
      del self.buff[self.cury]
      self.cury -= 1
      self.curx = len(self.buff[self.cury])
      self.buff[self.cury] += oldline
      self.total_lines -= 1
    self.modified += 1
  
  def goto_bookmark(self,to):
    if len(self.bookmarks) == 0: return
    if to == '-':
      self.bookindex -= 1
      if self.bookindex < 0:
        self.bookindex = len(self.bookmarks)-1
    else:
      self.bookindex += 1
      if self.bookindex > len(self.bookmarks)-1:
        self.bookindex = 0
        
    self.curx = 0
    self.cury = self.bookmarks[self.bookindex]
    self.scroll_buffer()
  
  def jumpto(self):
    cmd = self.command_prompt('line: ')
    if not cmd: return
    if cmd.upper() == 'END': 
      self.scroll_end()
      return
    try: cmd = int(cmd)
    except: return
    if cmd<1: cmd = 1
    if cmd<=self.total_lines:
      self.cury = cmd-1
      self.scroll_buffer()
    else:
      self.show_prompt('Value is greater than total lines.')
    
  def compile(self):
    ext = self.filename.split('.')[-1].lower()
    if not (ext in COMPILE): 
      self.show_prompt('no compile command for this filetype...')
      return
    if not os.path.isfile(self.filename):
      self.show_prompt("file doesn't exist. save it first.")
      return

    proc = subprocess.Popen(

    COMPILE[ext] + self.filename,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    shell=True,
    text=True
    )
    while proc.poll() is None:
      sleep(1)

    output, error = proc.communicate()
    ln = colors['reset']+ansi['clear']
    ln += '--- OUTPUT '+'-'*69+'\r'
    for l in output.splitlines():
      ln += l+'\n'
    ln += '--- ERRORS '+'-'*69+'\r'
    for l in error.splitlines():
      ln += l+'\n'
    ln += '--- RETURN VALUE \n'
    ln += str(proc.poll())
    writetext(ln)
    self.show_prompt('press a key to continue...')
    self.pause()
  
  def bashcmd(self):
    cmd = self.command_prompt('shell cmd: ')
    cmd = cmd.split()
    try:
      if len(cmd) == 1:
        k = subprocess.check_output(cmd[0])
      else:
        k = subprocess.check_output([cmd[0], " ".join(cmd[1:])])
    except:
      return
    
    for line in k.decode().splitlines():
      for c in line:
        self.insert_char(c)
      self.insert_line()

  def insert_strln(self,line):
    self.curx = 0
    self.buff.insert(self.cury, [] + list(line))
    self.cury += 1
    self.total_lines += 1
  
  def insert_line(self):
    oldline = self.buff[self.cury][self.curx:]
    self.buff[self.cury] = self.buff[self.cury][:self.curx]
    self.cury += 1
    self.curx = 0
    self.buff.insert(self.cury, [] + oldline)
    self.total_lines += 1
    if self.autoindent == True:
      spaces = 0
      try:
        while self.buff[self.cury-1][spaces] == ' ': spaces += 1
      except:
        pass
      for a in range(spaces):
        self.insert_char(' ')
    self.modified += 1
  
  def delete_line(self):
    if len(self.buff) == 1: return
    try:
      del self.buff[self.cury]
      self.curx = 0
      self.total_lines -= 1
    except: pass
    self.modified += 1
    if self.cury >= self.total_lines:
      self.cury = self.total_lines-1

  def move_home(self):
    spaces = 0
    if len(''.join(self.buff[self.cury]).strip())>0:
      while self.buff[self.cury][spaces] == ' ': spaces += 1
      if self.curx != spaces:
        self.curx = spaces
      else:    
        self.curx = 0
    else:
      self.curx = 0
    
  def move_cursor(self, key):
    row = self.buff[self.cury] if self.cury < self.total_lines else None
    if key == curses.KEY_LEFT:
      if self.curx != 0: self.curx -= 1
      elif self.cury > 0:
        self.cury -= 1
        self.curx = len(self.buff[self.cury])
    elif key == curses.KEY_RIGHT:
      if row is not None and self.curx < len(row):
        self.curx += 1
      elif row is not None and self.curx == len(row) and self.cury != self.total_lines-1:
        self.cury += 1
        self.curx = 0
    elif key == curses.KEY_UP:
      if self.cury != 0: self.cury -= 1
      else: self.curx = 0
    elif key == curses.KEY_DOWN:
      if self.cury < self.total_lines-1: self.cury += 1
      else: self.curx = len(self.buff[self.cury])
    row = self.buff[self.cury] if self.cury < self.total_lines else None
    rowlen = len(row) if row is not None else 0
    if self.curx > rowlen: self.curx = rowlen
    
  def delb_word(self):
    try:
      if self.is_separator(self.buff[self.cury][self.curx-1]):
        self.delete_char()
      while self.is_separator(self.buff[self.cury][self.curx-1]) == False:
        if self.curx == 0: break
        self.delete_char()
    except: pass
  
  def skip_word(self, key):
    if key == 545:
      self.move_cursor(curses.KEY_LEFT)
      try:
        if self.is_separator(self.buff[self.cury][self.curx]) == False:
          while self.is_separator(self.buff[self.cury][self.curx]) == False:
            if self.curx == 0: break
            self.move_cursor(curses.KEY_LEFT)
        elif self.is_separator(self.buff[self.cury][self.curx]):
          while self.is_separator(self.buff[self.cury][self.curx]):
            if self.curx == 0: break
            self.move_cursor(curses.KEY_LEFT)
      except: pass
    if key == 560:
      self.move_cursor(curses.KEY_RIGHT)
      try:
        if self.is_separator(self.buff[self.cury][self.curx]) == False:
          while self.is_separator(self.buff[self.cury][self.curx]) == False:
            self.move_cursor(curses.KEY_RIGHT)
        elif self.is_separator(self.buff[self.cury][self.curx]):
          while self.is_separator(self.buff[self.cury][self.curx]):
            self.move_cursor(curses.KEY_RIGHT)
      except: pass

  def scroll_end(self):
    while self.cury < self.total_lines-1:
      self.scroll_page(curses.KEY_NPAGE)

  def scroll_home(self):
    while self.cury:
      self.scroll_page(curses.KEY_PPAGE)

  def scroll_page(self, key):
    count = 0
    while count != self.bottom:
      if key == curses.KEY_NPAGE:
        self.move_cursor(curses.KEY_DOWN)
        if self.offy < self.total_lines - self.bottom: self.offy += 1
      elif key == curses.KEY_PPAGE:
        self.move_cursor(curses.KEY_UP)
        if self.offy: self.offy -= 1
      count += 1

  def scroll_buffer(self):
    if self.cury < self.offy: self.offy = self.cury
    if self.cury >= self.offy + self.bottom: self.offy = self.cury - self.bottom+1
    if self.curx < self.offx: self.offx = self.curx
    if self.curx >= self.offx + self.COLS: self.offx = self.curx - self.COLS+1

  def print_status_bar(self):
    global PLATFORM
    status = '\x1b[' + str(self.statusy) + ';1H'+COLOR_STATUS
    status += "^H:Help|"
    status += '^' if self.modified else ' '
    status += self.filename[:20].ljust(20,'.') + '|' + str(self.total_lines) + ' lines'+'|'+self.msg 
    ps = ''
    if self.COLS>70:
      ps += '|'+PLATFORM[:3].upper()
      i = 0
      ps += '|'
      while i < 4:
        if self.active == i: ps += '#'
        elif len(self.windows[i]['buff'][0])>0: ps += str(i+1)
        else: ps += '.'
        i+=1
      ps += '|'+self.filetype.upper()
      if self.autoindent:
        ps+="|AUTO"
      else:
        ps+="|----"
    if self.insert:
      ps+="|INS"
    else:
      ps+="|OVR"
    ps += str(self.width).rjust(3)+'|'
    if self.cury in self.bookmarks:
      ps += 'B'
    else:
      ps += ' '
    ps += str(self.cury+1).rjust(3) + ':' + str(self.curx+1).ljust(3)
    while len(stripansi(status)) < self.COLS - len(ps) -1: status += ' '
    status += ps + ' '
    status += '\x1b[m'
    status += '\x1b[' + str(self.cury - self.offy+1) + ';' + str(self.curx - self.offx+1) + 'H'
    status += '\x1b[?25h'+colors['reset']
    return status
    
  def print_suggest(self):
    #check spelling of last word
    line = '\x1b['+str(self.suggesty)+';1H'
    ln = ''.join(self.buff[self.cury])
    #if ln[-1:] != ' ': return ljustansi(line,self.COLS)
    
    #ln = ln.strip()
    if not ln: return ljustansi(COLOR_SUGGEST_NORMAL+line,self.COLS)
    #find the last word after having a space at the end
    i = self.curx-1
    while ln[i] not in self.seperators:
      i -= 1
      if i<0:
        i=0
        break
    part1 = ln[i:self.curx]
    i = self.curx-1
    while ln[i] not in self.seperators:
      i += 1
      if i>=len(self.buff[self.cury])-1:
        break
    part2 = ln[self.curx:i]
    wrd = str(part1+part2).strip()
    # check if word is very big or has symbols inside, if so drop the function as it will take too much time
    a = len(wrd)
    if a>20 and a<3 and not wrd: return ljustansi(COLOR_SUGGEST_NORMAL+line,self.COLS)
    #for s in self.seperators:
    #  if s in wrd:
    #    return ljustansi(COLOR_SUGGEST_NORMAL+line,self.COLS)
    if self.autohint:
      wrd = wrd.lower()
      res = []
      for key in self.code_hints:
        if key == wrd:
          line += self.code_hints[key]
          return ljustansi(COLOR_SUGGEST_CODE+line,self.COLS)
        elif key.startswith(wrd): 
          res.append(key)
      if len(res)>1:
        for r in res: line += r+' '
      else:
        if wrd in self.code_hints:
          line += self.code_hints[wrd]
        elif len(res)==1: 
          line += res[0]
      return ljustansi(COLOR_SUGGEST_CODE+line,self.COLS)
    else:
      suggs = spell.candidates(wrd)
      if suggs: suggs = list(suggs)
      else: return ljustansi(COLOR_SUGGEST_NORMAL+line,self.COLS)
      for w in suggs:
        line += w+' '
      #str(spell.candidates(wrd))
      if len(suggs) == 1 and suggs[0] == wrd:
        return ljustansi(COLOR_SUGGEST_NORMAL+line,self.COLS)
      else:
        return ljustansi(COLOR_SUGGEST_ERROR+line,self.COLS)

  def print_buffer(self):
    print_buffer = '\x1b[?25l'+COLOR_TEXT
    print_buffer += '\x1b[H\x1b[2J'
    for row in range(self.bottom):
      buffrow = row + self.offy;
      if buffrow < self.total_lines:
        rowlen = len(self.buff[buffrow]) - self.offx
        if rowlen < 0: rowlen = 0;
        if rowlen > self.COLS: rowlen = self.COLS;
        try:
          line = ''.join([c if c!=chr(27) else '^' for c in self.buff[buffrow][self.offx: self.offx + rowlen]])
          print_buffer += highlight(
          #''.join([c if c!=chr(27) else '^' for c in self.buff[buffrow][self.offx: self.offx + rowlen]]),
          line,
          self.lexers[self.filetype](),
          TerminalFormatter(bg='dark', colorscheme=COLOR_SCHEME))[:-1]
        except:
          print_buffer += ''.join([c if c!=chr(27) else '^' for c in self.buff[buffrow][self.offx: self.offx + rowlen]])
          
      print_buffer += '\x1b[K'
      print_buffer += '\r\n'
    return print_buffer
  
  def getyn(self,text):
    cmd = self.getkey(text,'YN')
    if chr(cmd) in 'Yy':
      return True
    else:
      return False
  
  def pause(self):
    c = -1
    while (c == -1): c = self.screen.getch()
    
  def getkey(self,prompt,valid):
    while True:
      c = -1
      self.clear_prompt(prompt)
      self.screen.refresh()
      while (c == -1): c = self.screen.getch()
      if chr(c).upper() in valid.upper():
        break
    return c

  def inhelp(self):
    self.changewindow(4)
    self.reset()
    self.buff.append([])
    with open(sys.argv[0]) as f:
      content = f.read().split('\n')
      for line in content:
        if line.startswith('#`'):
          self.insert_strln(line[2:])
    self.curx = 0
    self.cury = 0
    self.scroll_buffer()
  
  def edit_script(self):
    self.changewindow(4)
    self.reset()
    self.buff.append([])
    self.width = 120
    self.filename = 'clied.py'
    with open(sys.argv[0]) as f:
      content = f.read().split('\n')
      for line in content:
        self.insert_strln(line)
    self.filetype = 'py'
    self.curx = 0
    self.cury = 0
    self.scroll_buffer()
  
  def set_suggestline(self,value):
    self.autosuggest = value
    if self.autosuggest:
      self.bottom = self.ROWS - 2
      self.suggesty = self.ROWS - 1
      self.statusy  = self.ROWS 
    else:
      self.bottom = self.ROWS - 1
      self.suggesty = self.ROWS - 1
      self.statusy  = self.ROWS 

  def update_screen(self):
    self.scroll_buffer()
    print_buffer = self.print_buffer()
    if self.autosuggest:
      suggest = self.print_suggest()
    else: suggest = ''
    status_bar = self.print_status_bar()
    sys.stdout.write(print_buffer + suggest + status_bar)
    sys.stdout.flush()

  def resize_window(self):
    self.ROWS, self.COLS = self.screen.getmaxyx()
    self.set_suggestline(self.autosuggest or self.autohint)
    self.screen.refresh()
    self.update_screen()
    
  def docommand(self):
    cmd = self.command_prompt('command: ',recomend=True)
    if cmd:
      self.history.append(cmd)
      self.command(cmd)

  def read_keyboard(self):
    def ctrl(c): return ((c) & 0x1f)
    c = -1
    while (c == -1): c = self.screen.getch()
    
    if c == ctrl(ord('q')): self.exit()
    elif c == ctrl(ord('x')): self.docommand()
    elif c == 27: 
      if self.active == 4: self.changewindow(0)
      else: self.docommand()
    elif c == 9: [self.insert_char(' ') for i in range(self.tab)] #TAB KEY
    elif c == curses.KEY_BTAB: [self.delete_char() for i in range(self.tab) if self.curx]
    elif c == ctrl(ord('o')): self.load_file()
    elif c == ctrl(ord('n')): self.new_file()
    elif c == ctrl(ord('s')): self.save_file('')
    elif c == ctrl(ord('f')): self.search()
    elif c == ctrl(ord('e')): self.addstate();self.del_eol()
    elif c == ctrl(ord('g')): self.find_next()
    elif c == ctrl(ord('d')): self.addstate();self.delete_line()
    elif c == ctrl(ord('w')): self.addstate();self.delb_word()
    elif c == ctrl(ord('h')): self.inhelp()
    elif c == ctrl(ord('t')): self.addstate();self.strip('right 1')
    elif c == ctrl(ord('b')): self.toggle_bookmark()
    elif c == ctrl(ord('r')): self.command(self.history[-1]) # repeat last command
    elif c == ctrl(ord('v')): self.addstate();self.paste_lines('')
    elif c == ctrl(ord('c')): self.copy_lines('1')
    elif c == ctrl(ord('a')): self.autoindent=not self.autoindent
    elif c == ctrl(ord('l')): self.jumpto()
    elif c == ctrl(ord('z')): self.undo()
    elif c == curses.KEY_F1: self.changewindow(0)
    elif c == curses.KEY_F2: self.changewindow(1)
    elif c == curses.KEY_F3: self.changewindow(2)
    elif c == curses.KEY_F4: self.changewindow(3)
    elif c == curses.KEY_F7: self.compile()
    elif c == curses.KEY_F5: self.edit_script()
    elif c == curses.KEY_F9:  self.goto_bookmark('-')
    elif c == curses.KEY_F10: self.goto_bookmark('+')
    elif c == curses.KEY_IC: self.insert=not self.insert
    elif c == curses.KEY_DC: self.del_char()
    elif c == curses.KEY_RESIZE: self.resize_window()
    elif c == curses.KEY_HOME: self.move_home()
    elif c == curses.KEY_END: self.curx = len(self.buff[self.cury])
    elif c == curses.KEY_LEFT: self.move_cursor(c)
    elif c == curses.KEY_RIGHT: self.move_cursor(c)
    elif c == curses.KEY_UP: self.move_cursor(c)
    elif c == curses.KEY_DOWN: self.move_cursor(c)
    elif c == curses.KEY_BACKSPACE or chr(c) == '\b' or chr(c) == '\x7f': self.delete_char()
    elif c == curses.KEY_NPAGE: self.scroll_page(c)
    elif c == curses.KEY_PPAGE: self.scroll_page(c)
    elif c == 530: self.scroll_end()
    elif c == 535: self.scroll_home()
    elif c == 560: self.skip_word(560)
    elif c == 545: self.skip_word(545)
    elif c == ord('\n'): self.insert_line()
    elif ctrl(c) != c: self.insert_char(chr(c))
  
  def savetowindow(self,num):
    self.windows[num]['buff'].clear()
    #self.windows[num]['buff'] = self.buff.copy()
    self.windows[num]['buff'] = self.buff[:]
    self.windows[num]['filename'] = self.filename
    self.windows[num]['filetype'] = self.filetype
    self.windows[num]['curx'] = self.curx
    self.windows[num]['cury'] = self.cury
    self.windows[num]['offx'] = self.offx
    self.windows[num]['offy'] = self.offy
    self.windows[num]['indent'] = self.autoindent
    self.windows[num]['suggest'] = self.autosuggest
    self.windows[num]['hint'] = self.autohint
    self.windows[num]['tab'] = self.tab
    self.windows[num]['insert'] = self.insert
    self.windows[num]['total'] = self.total_lines
    self.windows[num]['modified'] = self.modified
    self.windows[num]['width'] = self.width
    self.windows[num]['bookmarks'] = self.bookmarks.copy()
    self.windows[num]['bookindex'] = self.bookindex
  
  def changewindow(self,win):
    if win == self.active: return
    #save previous state
    self.savetowindow(self.active)
    #activate new window
    self.active = win
    self.buff.clear()
    self.bookmarks.clear()
    self.buff = self.windows[win]['buff'].copy()
    self.filename = self.windows[win]['filename']
    self.filetype = self.windows[win]['filetype']
    self.curx = self.windows[win]['curx']
    self.cury = self.windows[win]['cury']
    self.offx = self.windows[win]['offx']
    self.offy = self.windows[win]['offy']
    self.autoindent = self.windows[win]['indent']
    self.autosuggest = self.windows[win]['suggest']
    self.autohint = self.windows[win]['hint']
    self.tab = self.windows[win]['tab']
    self.insert = self.windows[win]['insert']
    self.total_lines = self.windows[win]['total']
    self.modified = self.windows[win]['modified']
    self.width = self.windows[win]['width']
    self.bookmarks = self.windows[win]['bookmarks'].copy()
    self.bookindex = self.windows[win]['bookindex']
    
    self.scroll_buffer()
    self.update_screen()
  
  def toggle_bookmark(self):
    if self.cury in self.bookmarks:
      self.bookmarks.remove(self.cury)
    else:
      self.bookmarks.append(self.cury)
      self.bookmarks.sort()
      self.bookmarks = list(set(self.bookmarks.copy()))
  
  def clear_prompt(self, line):
    command_line = line
    ps = str(len(self.buff))+' lines '    
    ps += str(self.cury+1).rjust(3,' ') + ':' + str(self.curx+1).rjust(2,'0')
    while (len(command_line) + len(ps)) < self.COLS-1: command_line += ' '
    command_line = '\x1b[' + str(self.statusy) + ';' + '0' + 'H' + command_line
    command_line = COLOR_STATUS + command_line
    command_line += ps 
    command_line += '\x1b[' + str(self.statusy) + ';' + str(len(line)+1) + 'H'
    sys.stdout.write(command_line)
    sys.stdout.flush()
    
  def show_prompt(self,line):
    self.clear_prompt(line)
    sleep(2)
    #sys.stdout.write(command_line)
    #sys.stdout.flush()
    
  def dorecommend(self,word,cursorpos,force=False,RECOMEND=[]):
    if not RECOMEND: return
    rec = []
    word = word.upper()
    words = ''
    
    if force:
      for w in RECOMEND:
        rec.append(w)
        if len(words)+len(w)+1<self.COLS:
          words += ' '+w
    else:
      for w in RECOMEND:
        if word in w.upper():
          rec.append(w)
          if len(words)+len(w)+1<self.COLS:
            words += ' '+w
    
    while len(words)<self.COLS: words += ' '
    
    if not rec: return
    
    line = '\x1b['+str(self.suggesty)+';1H'
    line += colors[0]+colors[22]+words
    line += '\x1b['+str(self.statusy)+';'+str(cursorpos+1)+'H'+COLOR_STATUS
    sys.stdout.write(line)
    sys.stdout.flush()
    
  def command_prompt(self, prompt,value='',recomend=False):
    recomended = []
    self.clear_prompt(prompt)
    self.screen.refresh()
    word = ''; c = -1; pos = 0
    index = len(self.history)
    
    def backspace():
      nonlocal pos
      nonlocal word
      pos -= 1
      if pos < 0: pos = 0; return
      sys.stdout.write('\b')
      sys.stdout.write(' ')
      sys.stdout.write('\b')
      sys.stdout.flush()
      word = word[:len(word)-1]
    
    if value:
      word = value
      pos = len(word)
      sys.stdout.write(word)
      sys.stdout.flush()
      
    while c != 0x1b:
      c = -1
      while (c == -1): c = self.screen.getch()
      if c == 10 : break
      if c == 27: return ''
      if c == curses.KEY_BACKSPACE:
        backspace()
      elif c == curses.KEY_UP:
        while pos>0: backspace()
        try:
          index-=1
          if index<0: index = 0
          word = self.history[index]
          pos = len(word)
          sys.stdout.write(word)
          sys.stdout.flush()
        except: pass
      elif c == curses.KEY_DC:
        while pos>0: backspace()
      elif c == curses.KEY_DOWN:
        while pos>0: backspace()
        try:
          index+=1
          if index>len(self.history)-1:index=len(self.history)-1
          word = self.history[index]
          pos = len(word)
          sys.stdout.write(word)
          sys.stdout.flush()
        except: pass
      elif (c>= 32 and c<=126): #c != curses.KEY_BACKSPACE:
        pos += 1
        sys.stdout.write(chr(c))
        sys.stdout.flush()
        word += chr(c)
        
      try:
        if recomend:
          recomended.clear()
          keyword = str(word).upper()
          if keyword.find(' ') == -1:
            recomended = ['time','save','extract','exit','quit','width','filetype','fl', \
            'align','al','strip','st','ascii','ansi','attr','clear','reset','commend','cm',\
            'uncomment','date','dt','line','repeat','rep','indent','ind','delete','del',\
            'copy','cp','paste','pt','get','insert','mci','box','menul','menuc','saveas',
            'spell','code','open','load','bash','justify','just','shell','bookmark','book','format',\
            'fmt','crlf','gopher','help','duplicate','dupe','regex']
            self.dorecommend(word,pos+len(prompt),RECOMEND=recomended)
          else:
            if keyword[:keyword.find(' ')] in ['ALIGN','AL']:
              recomended=['align <left|right|center> [lines] : align text for line(s)']
              self.dorecommend(word,pos+len(prompt),True,RECOMEND=recomended)
            elif keyword[:keyword.find(' ')] in ['REGEX']:
              recomended=['regex <find> <replace> [lines] : regex replace/insert string']
              self.dorecommend(word,pos+len(prompt),True,RECOMEND=recomended)
            elif keyword[:keyword.find(' ')] in ['FORMAT','FMT']:
              recomended=['format <lower|caps|upper|title> [lines] : change capitalization for line(s)']
              self.dorecommend(word,pos+len(prompt),True,RECOMEND=recomended)
            elif keyword[:keyword.find(' ')] in ['JUSTIFY','JUST']:
              recomended=['justify <lines> : justify text for line(s), at least 2!']
              self.dorecommend(word,pos+len(prompt),True,RECOMEND=recomended)
            elif keyword[:keyword.find(' ')] in ['STRIP','ST']:
              recomended=['strip <left|right|center> [lines|all] : strip text for line(s)']
              self.dorecommend(word,pos+len(prompt),True,RECOMEND=recomended)
            elif keyword[:keyword.find(' ')] in ['INSERT','INS']:
              recomended=['insert <gpl|bsd|blog|script|html|python|pascal> : insert text template']
              self.dorecommend(word,pos+len(prompt),True,RECOMEND=recomended)
            elif keyword[:keyword.find(' ')] in ['FILETYPE','FL']:
              recomended=['pascal','python','c','bas','delphi','text','bbcode','html','none','bash']
              self.dorecommend(word,pos+len(prompt),True,RECOMEND=recomended)
            elif keyword[:keyword.find(' ')] in ['ASCII']:
              recomended=['type ascii number of the character you want']
              self.dorecommend(word,pos+len(prompt),True,RECOMEND=recomended)
            elif keyword[:keyword.find(' ')] in ['WIDTH']:
              recomended=['width <num> : set document width to <num> cols']
              self.dorecommend(word,pos+len(prompt),True,RECOMEND=recomended)
            elif keyword[:keyword.find(' ')] in ['INDENT','IND']:
              recomended=['indent <rows> <cols> [+/-] : indent <cols> for <rows> from current position']
              self.dorecommend(word,pos+len(prompt),True,RECOMEND=recomended)
            elif keyword[:keyword.find(' ')] in ['LINE','REPEAT','REP']:
              recomended=['repeat <cols> <char> : repeat <char> for <cols> times']
              self.dorecommend(word,pos+len(prompt),True,RECOMEND=recomended)
            elif keyword[:keyword.find(' ')] in ['OPEN','LOAD']:
              recomended=['open : load a file']
              self.dorecommend(word,pos+len(prompt),True,RECOMEND=recomended)
            elif keyword[:keyword.find(' ')] in ['COMMENT','CM']:
              recomended=['comment <num> : comment <num> lines']
              self.dorecommend(word,pos+len(prompt),True,RECOMEND=recomended)
            elif keyword[:keyword.find(' ')] in ['UNCOMMENT']:
              recomended=['uncomment <num> : comment <num> lines']
              self.dorecommend(word,pos+len(prompt),True,RECOMEND=recomended)
            elif keyword[:keyword.find(' ')] in ['EXTRACT']:
              recomended=['extract <num|all> : saves <num> lines to a file']
              self.dorecommend(word,pos+len(prompt),True,RECOMEND=recomended)
            elif keyword[:keyword.find(' ')] in ['BASH']:
              recomended=['bash : inserts output of a BASH command']
              self.dorecommend(word,pos+len(prompt),True,RECOMEND=recomended)
            elif keyword[:keyword.find(' ')] in ['DELETE','DEL']:
              recomended=['delete <num|all> : delete <num> lines']
              self.dorecommend(word,pos+len(prompt),True,RECOMEND=recomended)
            elif keyword[:keyword.find(' ')] in ['COPY','CP']:
              recomended=['copy <num|all> : copy <num> lines to clipboard']
              self.dorecommend(word,pos+len(prompt),True,RECOMEND=recomended)
            elif keyword[:keyword.find(' ')] in ['PASTE','PT']:
              recomended=['paste : paste from clipboard in current position']
              self.dorecommend(word,pos+len(prompt),True,RECOMEND=recomended)
            elif keyword[:keyword.find(' ')] in ['GET']:
              recomended=['get <url|file> : inserts a local file or from the internet']
              self.dorecommend(word,pos+len(prompt),True,RECOMEND=recomended)
            elif keyword[:keyword.find(' ')] in ['SPELL']:
              recomended=['spell <on|off> : turn on/off spell checking']
              self.dorecommend(word,pos+len(prompt),True,RECOMEND=recomended)
            elif keyword[:keyword.find(' ')] in ['CODE']:
              recomended=['code <on|off> : turn on/off code hints, if available']
              self.dorecommend(word,pos+len(prompt),True,RECOMEND=recomended)
            elif keyword[:keyword.find(' ')] in ['ANSI']:
              recomended=['black','blue','red','grey','...','lightblue','lightred','...','white','reset','cls','reverse']
              self.dorecommend(word,pos+len(prompt),True,RECOMEND=recomended)
            elif keyword[:keyword.find(' ')] in ['MCI']:
              recomended=['mci <code> : inserts a mystic bbs MCI code, if supported']
              self.dorecommend(word,pos+len(prompt),True,RECOMEND=recomended)
            elif keyword[:keyword.find(' ')] in ['ATTR']:
              recomended=['attr <code> : expands a color attribute to string and fg/bg nums']
              self.dorecommend(word,pos+len(prompt),True,RECOMEND=recomended)
            elif keyword[:keyword.find(' ')] in ['BOX']:
              recomended=['box <type> : inserts an ASCII box']
              self.dorecommend(word,pos+len(prompt),True,RECOMEND=recomended)
            elif keyword[:keyword.find(' ')] in ['CRLF']:
              recomended=['CRLF <dos|win|linux> : changes the ending line method']
              self.dorecommend(word,pos+len(prompt),True,RECOMEND=recomended)
            elif keyword[:keyword.find(' ')] in ['BOOKMARK','BOOK']:
              recomended=['bookmark : toggles, sets or unsets a bookmark in current line']
              self.dorecommend(word,pos+len(prompt),True,RECOMEND=recomended)
            elif keyword[:keyword.find(' ')] in ['MENUC','MENUL']:
              recomended=['menu [header] [option1] [option2] .. : inserts a menu box']
              self.dorecommend(word,pos+len(prompt),True,RECOMEND=recomended)
            elif keyword[:keyword.find(' ')] in ['DUPLICATE','DUPE']:
              recomended=['duplicate : duplicates current document to a new window']
              self.dorecommend(word,pos+len(prompt),True,RECOMEND=recomended)
            elif keyword[:keyword.find(' ')] in ['SAVEAS']:
              recomended=['saveas <gopher|ansi> : saves/export the doc in a different format']
              self.dorecommend(word,pos+len(prompt),True,RECOMEND=recomended)
            elif keyword[:keyword.find(' ')] in ['GOPHER']:
              recomended=['gopher <link|file|image|dir> : helps you insert a gopher item']
              self.dorecommend(word,pos+len(prompt),True,RECOMEND=recomended)
      except: pass
    self.update_screen()
    self.screen.refresh()
    return word
    
  def insert_str(self,s):
    for i,c in enumerate(s):
      self.buff[self.cury].insert(self.curx+i, c)
    self.curx += len(s)
      
    
  def command(self,command):
    global BSD_NOTICE, GPL_NOTICE, HTML_BODY, PLATFORM
    cmd = command
    if not cmd: return
    cmd = cmd.split()
    params = " ".join(cmd[1:])
    cmd = cmd[0].upper()
    
    self.addstate()
    
    if cmd == 'TIME':
      self.insert_str(datetime.datetime.now().strftime("%H:%M"))
    elif cmd == 'SAVE':
      self.save_file(params)
    elif cmd == 'EXTRACT':
      self.extract_lines(params)
    elif cmd == 'EXIT' or cmd == 'QUIT':
      self.exit()
    elif cmd == 'WIDTH': # WIDTH [cols]
      try: self.width = int(params)
      except: pass
    elif cmd == 'FILETYPE' or cmd == 'FL': # FILETYPE [ext]
      self.setfiletype(params.lower())
    elif cmd == 'ALIGN' or cmd == 'AL':
      self.align(params)
    elif cmd == 'REGEX':
      self.regex(params)
    elif cmd == 'FORMAT' or cmd == 'FMT':
      self.format(params)
    elif cmd == 'JUSTIFY' or cmd == 'JUST':
      self.justify(params)
    elif cmd == 'STRIP' or cmd == 'ST':
      self.strip(params)
    elif cmd == 'SAVEAS':
      self.saveas(params)
    elif cmd == 'DUPLICATE' or cmd == 'DUPE':
      self.duplicate()
    elif cmd == 'GOPHER':
      self.gopher(params)
    elif cmd == 'ASCII': # ASCII [char-num]
      self.insert_char(chr(int(params)))
    elif cmd == 'ANSI': # ANSI Color
      self.ansistring(params)
    elif cmd == 'ATTR': # expand attribute to string
      self.attr_string(params)
    elif cmd == 'HELP': 
      self.inhelp()
    elif cmd == 'MCI': 
      self.mci(params)
    elif cmd == 'MENUC': 
      self.box(params,1)
    elif cmd == 'MENUL': 
      self.box(params,2)
    elif cmd == 'SPELL':   
      self.dosuggest('spell',params)
    elif cmd == 'CODE':   
      self.dosuggest('code',params)
    elif cmd == 'BOX': 
      self.box2(params)
    elif cmd == 'CRLF': 
      crlf(params)
    elif cmd == 'BASH' or cmd == 'SHELL': 
      self.bashcmd()
    elif cmd == 'OPEN' or cmd == 'LOAD': 
      self.load_file(params)
    elif cmd == 'CLEAR' or cmd == 'RESET': # Reset the editor
      self.new_file()
    elif cmd == 'COMMENT' or cmd == 'CM':
      self.comment(params+' +')
    elif cmd == 'BOOKMARK' or cmd == 'BOOK':
      self.toggle_bookmark()
    elif cmd == 'UNCOMMENT':
      self.comment(params+' -')
    elif cmd == 'DATE' or cmd == 'DT':
      self.insert_date(params)
    elif cmd == 'LINE' or cmd == 'REPEAT' or cmd == 'REP':  # LINE [cols] [char]
      self.insert_str(params.split()[1]*int(params.split()[0]))
    elif cmd == 'INDENT' or cmd == 'IND':  # INDENT [rows] [cols] [+/-]
      self.indent(params)
    elif cmd == 'INSERT' or cmd == 'INS':
      self.insert_text(params)
    elif cmd == 'DELETE' or cmd == 'DEL':
      self.delete_lines(params)
    elif cmd == 'COPY' or cmd == 'CP':
      self.copy_lines(params)
    elif cmd == 'PASTE' or cmd == 'PT':
      self.paste_lines(params)
    elif cmd == 'GET':
      self.get_file(params)
    else:
      if not self.calculator(command): self.show_prompt('Command not recognized!')

  def box2(self,params):
    if params=='1':
      line='''   + --- --  -   .     -        ---    ---    ---        -     .    - -- --- ´
   |                                                                         |
   ;                                                                         ;
   :                                                                         :
   .                                                                         .
   ;                                                                         ;
   |                                                                         |
   + --- --  -   .     -        ---    ---    ---        -     .    - -- --- ´'''
    elif params=='2':
      line='''           █▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀ Command Options ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▄
           █                                                         █
           █ Command    │ (  )                                       █
           █ Data       │                                            █
           █ Access     │                                            █
           █ Grid Event │ Selected                                   █
           █                                                         █
           ▀▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█'''
   
    self.insert_paragraph(line)
    
  def gopher(self,params):
    global GOPHER
    p = params.upper()
    if p == 'LINK' or p == 'URL': # inserts a link to another host
      '[url]'+editname+'[tab][/tab]'+editpath+'[tab][/tab]'+edittext+'[tab][/tab]'+editport+'[/url]'
      txt = self.command_prompt('enter text: ','')
      dr  = self.command_prompt('enter path: ','/path')
      url = self.command_prompt('enter host only: ','localhost')
      prt = self.command_prompt('enter port: ','70')
      if txt and url and dr and prt:
        self.insert_str('[dir]'+txt+'[tab]'+dr+'[tab]'+url+'[tab]'+prt+'[/dir]')
    elif p == 'DIR': # directory link
      txt = self.command_prompt('enter text: ','')
      dr  = self.command_prompt('enter path: ','')
      if txt and dr:
        self.insert_str('[dir]'+txt+'[tab]'+dr+'[tab][host][tab][port][/dir]')
    elif p == 'FILE': # local text file
      txt = self.command_prompt('enter text: ','')
      fl  = self.command_prompt('enter filename: ','')
      if txt and fl:
        self.insert_str('[file]'+txt+'[tab]'+fl+'[/file]')
    elif p == 'INCLUDE' or p == 'INC': # include bbcode for local text file
      txt = self.command_prompt('enter text: ','')
      fl  = self.command_prompt('enter filename: ','')
      if txt and fl:
        self.insert_str('[include]'+txt+'[tab]'+fl+'[/include]')
    elif p == 'BIN': # local binary file
      txt = self.command_prompt('enter text: ','')
      fl  = self.command_prompt('enter filename: ','')
      if txt and fl:
        self.insert_str('[bin]'+txt+'[tab]'+fl+'[/bin]')
    elif p == 'IMAGE' or p == 'IMG': #local image link
      txt = self.command_prompt('enter text: ','')
      fl  = self.command_prompt('enter filename: ','')
      if txt and fl:
        self.insert_str('[img]'+txt+'[tab]'+fl+'[/img]')
    elif p == 'EMPTY': 
      self.insert_str('[empty]')
    elif p == 'HR' or p == 'RULER': 
      self.insert_str('[hr]')
    elif p == 'DATE': 
      self.insert_str('[date]')
    elif p == 'TIME': 
      self.insert_str('[time]')
    elif p == 'H1': 
      self.insert_str('[h1][/h1]')
    elif p == 'H2': 
      self.insert_str('[h2][/h2]')
    elif p == 'CENTER': 
      self.insert_str('[center][/center]')
    elif p == 'RIGHT': 
      self.insert_str('[right][/right]')
    else:
      self.show_prompt('unrecognized gopher item...')
  
  def duplicate(self):
    for i in range(4):
      if self.windows[i]['buff']==[[]] and i!=self.active:
        self.savetowindow(i)
        self.show_prompt('duplicated to window['+str(i+1)+']...')
        return
    self.show_prompt("all windows are not empty, couldn't duplicate document")
    
  def saveas(self,params):
    global GOPHER
    params = params.upper()
    if params == 'ANSI': self.saveas_ansi()
    elif params == 'GOPHER':
      self.show_prompt('saving current document...')
      self.save_file('')
      gp = self.command_prompt('save [gopher] filename: ','gopher.map')
      ismap = False
      if self.getyn('is the file going to be a map file? y/n '):
        ismap = True
      host = self.command_prompt('enter hostname: ',GOPHER['host'])
      port = self.command_prompt('enter port: ',GOPHER['port'])
      if os.path.isfile(self.filename) and host and port:
        GOPHER['host'] = host
        GOPHER['port'] = port
        gophermap(self.filename,gp,ismap)
        self.show_prompt('gopher file exported!')        

  def box(self,params,align=1):
    parts = params.split()
    items=[]
    line = ''
    header = 'Header'
    if len(parts)>=1:
      header = parts[0]
    width = len(header)+14
    
    if len(parts)>=2:
      for p in range(1,len(parts)):
        items.append(parts[p])
        if len(parts[p])+2>width: width = len(parts[p])+2
    
    if not items: items.append(' ')
    
    line = ' '+header+' '
    if align == 1:
      line = '.' +line.center(width-2,'-')+ '.\n'
      for item in items:
        line += "|" + item.center(width-2,' ')+"|\n"
      line += "`" + "".center(width-2,'-')+"'\n"
    elif align == 2:
      line = '.-' +line.ljust(width-3,'-')+ '.\n'
      for item in items:
        line += "| " + item.ljust(width-3,' ')+"|\n"
      line += "`" + "".ljust(width-2,'-')+"'\n"
    self.insert_paragraph(line)
    
      
  def insert_paragraph(self,s):
    for line in s.splitlines():
      self.insert_strln(line)
      self.modified+=1
  
  def dosuggest(self,tp,params):
    val = params.upper().strip()
    if tp.upper() == 'SPELL':
      if val == 'ON':
        self.autosuggest = True
        self.set_suggestline(True)
      else:
        self.autosuggest = False
        self.set_suggestline(False)
    elif tp.upper() == 'CODE':
      if val == 'ON':
        if len(self.code_hints) == 0:
          self.show_prompt('no hints were loaded! perhaps change filetype.')
          return
        self.autohint = True
        self.set_suggestline(True)
      else:
        self.autohint = False
        self.set_suggestline(False)
    
    self.update_screen()
          
  def mci(self,params):
    codes = params.upper()
    index = 0
    while index<len(codes):
      code = codes[index:index+2]
      self.msg = code
      if code=='00': self.insert_str(colors[int(code)])
      elif code=='01': self.insert_str(colors[int(code)])
      elif code=='02': self.insert_str(colors[int(code)])
      elif code=='03': self.insert_str(colors[int(code)])
      elif code=='04': self.insert_str(colors[int(code)])
      elif code=='05': self.insert_str(colors[int(code)])
      elif code=='06': self.insert_str(colors[int(code)])
      elif code=='07': self.insert_str(colors[int(code)])
      elif code=='08': self.insert_str(colors[int(code)])
      elif code=='09': self.insert_str(colors[int(code)])
      elif code=='10': self.insert_str(colors[int(code)])
      elif code=='11': self.insert_str(colors[int(code)])
      elif code=='12': self.insert_str(colors[int(code)])
      elif code=='13': self.insert_str(colors[int(code)])
      elif code=='14': self.insert_str(colors[int(code)])
      elif code=='15': self.insert_str(colors[int(code)])
      elif code=='16': self.insert_str(colors[int(code)])
      elif code=='17': self.insert_str(colors[int(code)])
      elif code=='18': self.insert_str(colors[int(code)])
      elif code=='19': self.insert_str(colors[int(code)])
      elif code=='20': self.insert_str(colors[int(code)])
      elif code=='21': self.insert_str(colors[int(code)])
      elif code=='22': self.insert_str(colors[int(code)])
      elif code=='23': self.insert_str(colors[int(code)])
      elif code=='TI': self.insert_str(datetime.datetime.now().strftime("%H:%M"))
      elif code=='US': self.insert_str(str(self.ROWS))
      elif code=='DA': self.insert_str(datetime.date.today().strftime("%c"))
      elif code=='UX': self.insert_str(socket.gethostname())
      elif code=='UY': self.insert_str(get_ip())
      elif code=='[0': self.insert_str(ansi['hide'])
      elif code=='[1': self.insert_str(ansi['show'])
      elif code=='CL': self.insert_str(ansi['clear'])
      
      else:
        self.show_prompt('Wrong MCI code. Aborting...')
        break
      
      index += 2
  
  def insert_text(self,params):
    cmd = params.upper()
    if cmd == 'BSD':
      self.insert_paragraph(BSD_NOTICE)
    elif cmd == 'HTML':
      self.insert_paragraph(HTML_BODY)
    elif cmd == 'GPL':
      self.insert_paragraph(GPL_NOTICE)
    elif cmd == 'PASCAL':
      self.insert_paragraph(PASCAL_UNIT)
    elif cmd == 'PYTHON':
      self.insert_paragraph(PYTHON_PROGRAM)
    elif cmd == 'BLOG':
      self.insert_paragraph(BLOG_POST)
    elif cmd == 'BASH' or cmd == 'SCRIPT':
      self.insert_paragraph(SCRIPT_BODY)
    
  def attr_string(self,params):
    if not params.isdigit() or not params:
      self.show_prompt('attr: paramater not valid!')
      return
    i = int(params)
    fg = i % 16
    bg = i // 16
    self.insert_str(str(fg)+'/'+colornames[fg]+' text on '+str(bg)+'/'+colornames[bg]+' background')
      
  def ansistring(self,params):
    params = params.upper()
    if params == 'BLACK': self.insert_str('\x1b[0;30m')
    elif params == 'BLUE': self.insert_str('\x1b[0;34m')
    elif params == 'GREEN': self.insert_str('\x1b[0;32m')
    elif params == 'CYAN': self.insert_str('\x1b[0;36m')
    elif params == 'RED': self.insert_str('\x1b[0;31m')
    elif params == 'MAGENTA': self.insert_str('\x1b[0;35m')
    elif params == 'BROWN': self.insert_str('\x1b[0;33m')
    elif params == 'GREY': self.insert_str('\x1b[0;37m')
    elif params == 'DARKGREY': self.insert_str('\x1b[1;30m')
    elif params == 'LIGHTBLUE': self.insert_str('\x1b[1;34m')
    elif params == 'LIGHTGREEN': self.insert_str('\x1b[1;32m')
    elif params == 'LIGHTCYAN': self.insert_str('\x1b[1;36m')
    elif params == 'LIGHTRED': self.insert_str('\x1b[1;31m')
    elif params == 'LIGHTMAGENTA': self.insert_str('\x1b[1;35m')
    elif params == 'YELLOW': self.insert_str('\x1b[1;33m')
    elif params == 'WHITE': self.insert_str('\x1b[1;37m')
    elif params == 'RESET': self.insert_str(colors['reset'])
    elif params == 'CLEAR': self.insert_str(ansi['clear'])
    elif params == 'CLS': self.insert_str(ansi['clear'])
    elif params == 'GOTO': self.insert_str(ansi['goto'])
    elif params == 'REVERSE': self.insert_str(colors['reverse'])
    elif params.isdigit():
      i = int(params)
      if i<0: return
      if i in range(16):
        self.insert_str(colors[int(params)])
      else:
        fg = i % 16
        bg = i // 16
        self.insert_str(colors[fg]+colorsbg[bg])

        
  def get_file(self,params):
    params = params.split()
    url = params[0]
    codec = 'utf8'
    if len(params)==2: codec = params[1] 
    
    url = os.path.expanduser(url)
    
    if os.path.isfile(url): #local file
      try:
        with open(url) as f:
          content = f.read().split('\n')
          for row in content[:-1]:
            self.insert_strln(row)
      except: self.show_prompt('Error reading file...')
      
    else: #internet file
      try:
        response = urllib.request.urlopen(url)
        data = response.read()
      except:
        self.show_prompt('Error getting file...')
      try:
        for line in data.decode(codec).splitlines():
          self.insert_strln(line)
      except:
        self.show_prompt('Error decoding file...')

  def setfiletype(self,typeof):
    typeof = typeof.lower()
    if typeof == 'dpr': typeof = 'pas'
    elif typeof == 'delphi': typeof = 'pas'
    elif typeof == 'bbcode': typeof = 'bb'
    elif typeof == 'mpl': typeof = 'mpl'
    elif typeof == 'python': typeof = 'py'
    elif typeof == 'pyw': typeof = 'py'
    elif typeof == 'basic': typeof = 'bas'
    elif typeof == 'mpy': typeof = 'mpy'
    elif typeof == 'pascal': typeof = 'pas'
    elif typeof == 'htm': typeof = 'htm'
    elif typeof == 'html': typeof = 'htm'
    elif typeof == 'zsh': typeof = 'sh'
    elif typeof == 'bash': typeof = 'sh'
    elif typeof == 'xhtml': typeof = 'htm'
    elif typeof == 'c': typeof = 'c'
    elif typeof == 'h': typeof = 'c'
    elif typeof == 'none': typeof = 'txt'
    elif typeof == 'text': typeof = 'txt'
   
    if typeof in self.lexers:
      self.filetype = typeof
      
      if os.path.isfile(typeof+'.jsn'):
        with open(typeof+'.jsn') as json_file:
          self.code_hints.clear()
          self.code_hints = json.load(json_file)
    else:
       self.filetype = 'txt'
       self.code_hints.clear()
       self.highlight = False
      
  def insert_date(self,params):
    if params.upper() == 'YMD':
      self.insert_str(datetime.date.today().strftime("%Y/%m/%d"))
    elif params.upper() == 'DMY':
      self.insert_str(datetime.date.today().strftime("%d/%m/%Y"))
    elif params.upper() == 'MDY':
      self.insert_str(datetime.date.today().strftime("%m/%d/%Y"))
    elif params.upper() == 'LOCAL':
      self.insert_str(datetime.date.today().strftime("%c"))
    else:
      self.insert_str(datetime.date.today().strftime("%Y/%m/%d"))
    
  def comment(self,params):
    # format: [rows] [+/-]
    start_row = self.cury
    params = params.split()
    if params[0]=='+' or params[0] == '-': 
      end_row = self.cury
      dir = params[0]
    else:
      if params[0].upper() == 'ALL':
        start_row = 0
        end_row = len(self.buff)
      elif params[0].isdigit():
        end_row = self.cury + int(params[0]) - 1
        if end_row >= len(self.buff): end_row = len(self.buff)-1
      else:
        end_row = 1
      
      dir = params[1]
    
    if start_row == end_row: #single line
      if dir == '+': self.buff[start_row].insert(0, self.comments[self.filetype][0])
      if dir == '-': 
        for i in range(len(self.comments[self.filetype][0])-1):
          del self.buff[start_row][0]
      self.modified += 1
    else:
      if self.comments[self.filetype][3]:
        if dir == '+':
          self.buff[start_row].insert(0, self.comments[self.filetype][1])
          self.buff[end_row].insert(len(self.buff[end_row]), self.comments[self.filetype][2])
          self.modified += end_row - start_row + 1
        else:
          for i in range(len(self.comments[self.filetype][0])-1): del self.buff[start_row][0]
          for i in range(len(self.comments[self.filetype][0])-1): del self.buff[end_row][-1]
      else:
        for row in range(start_row, end_row):
          if dir == '+': self.buff[row].insert(0, self.comments[self.filetype][0])
          if dir == '-': del self.buff[row][0]
        self.modified += 1
    
  
  def delete_lines(self,param):
    param = param.split()
    end = 1
    if len(param)==1:
      end = param[0].upper()
    
    if end == 'ALL':
      start_row = 0
      end_row = len(self.buff)
    elif end.isdigit():
      start_row = self.cury
      end_row = self.cury + int(end)
    else:
      self.show_prompt('delete: wrong value for [lines].')
      return     
      
    for row in range(start_row, end_row):
      if row>len(self.buff)-1: break
      self.delete_line()      
      
  def copy_lines(self,param):
    param = param.split()
    end = 1
    if len(param)==1:
      end = param[0].upper()
    
    if end == 'ALL':
      start_row = 0
      end_row = len(self.buff)
    elif end.isdigit():
      start_row = self.cury
      end_row = self.cury + int(end)
    else:
      self.show_prompt('copy: wrong value for [lines].')
      return
    
    content = ''
    for row in range(start_row, end_row):
      if row>len(self.buff)-1: break
      content += ''.join(self.buff[row])+'\r\n'
    
    pyperclip.copy(content)
    
  def paste_lines(self,params):
    self.insert_paragraph(pyperclip.paste())
    
  def align(self,param):
    #indent = self.command_prompt('indent:')
    # format: [rows] [cols] [+/-]
    param = param.split()
    altype = param[0].upper()
    char = ' ' 
    end = 1
    if len(param)==2:
      end = param[1].upper()
    if len(param)==3:
      char = param[2]
    
    if end == 'ALL':
      start_row = 0
      end_row = len(self.buff)
    elif end.isdigit():
      start_row = self.cury
      end_row = self.cury + int(end)
    else:
      self.show_prompt('align: wrong value for [lines].')
      return
      
    for row in range(start_row, end_row):
      if row>len(self.buff)-1: break
      line = ''.join(self.buff[row]).strip()
      if altype == 'LEFT':
        self.buff[row]=list(line.ljust(self.width,char))
      elif altype == 'RIGHT':
        self.buff[row]=list(line.rjust(self.width,char))
      elif altype == 'CENTER':
        self.buff[row]=list(line.center(self.width,char).rstrip())
      self.modified += 1
      
  def regex(self,param):
    param = shlex.split(param)
    if len(param)<2:
      self.show_prompt('regex: not enough paramaters...')
      return
    end = 1
    search = param[0]
    rep    = param[1]
    if len(param)==3:
      end = param[2].upper()
    
    if end == 'ALL':
      start_row = 0
      end_row = len(self.buff)
    elif end.isdigit():
      start_row = self.cury
      end_row = self.cury + int(end)
    else:
      self.show_prompt('regex: wrong value for [lines].')
      return
      
    for row in range(start_row, end_row):
      if row>len(self.buff)-1: break
      line = ''.join(self.buff[row]).strip()
      self.buff[row]=list(re.sub(search,rep,line))
      self.modified += 1
      
  def format(self, param):
    param = param.split()
    altype = param[0].upper()
    char = ' ' 
    end = 1
    if len(param)==2:
      end = param[1].upper()
    if len(param)==3:
      char = param[2]
    
    if end == 'ALL':
      start_row = 0
      end_row = len(self.buff)
    elif end.isdigit():
      start_row = self.cury
      end_row = self.cury + int(end)
    else:
      self.show_prompt('format: wrong value for [lines].')
      return
      
    for row in range(start_row, end_row):
      if row>len(self.buff)-1: break
      line = ''.join(self.buff[row]).strip()
      if altype == 'LOWER':
        self.buff[row]=list(line.lower())
      elif altype == 'UPPER' or altype == 'CAPITAL':
        self.buff[row]=list(line.upper())
      elif altype == 'TITLE':
        self.buff[row]=list(string.capwords(line))
      self.modified += 1
  
  def justify(self,params):
    start_row = self.cury
    end_row = 2
    if params:
      if params.split()[0].upper() == 'ALL':
        start_row = 0
        end_row = len(self.buff)
      elif params.split()[0].isdigit():
        end_row = self.cury + int(params.split()[0])
      else:
        self.show_prompt('justify: wrong value for [lines].')
        return
    else: end_row = self.cury+1
    content = ''
    for row in range(start_row, end_row):
      line = ''.join(self.buff[row]).strip()+'\n'
      content += line
      self.modified += 1
    self.insert_paragraph(justify(content,self.width))
    
  def del_eol(self):
    line = ''.join(self.buff[self.cury])
    line = line[:self.curx]
    self.buff[self.cury]=list(line)
    
  def calculator(self,calc):
    #calc = self.command_prompt('input expression: ')
    if not calc: return
    sym = '0123456789.-=+/*%() '
    for c in calc: 
      if c not in sym:
        #self.show_prompt('unacceptable character: '+c)
        return False
    self.insert_str(str(eval(calc)))
    return True
      
  def strip(self,param):
    #indent = self.command_prompt('indent:')
    # format: [rows] [cols] [+/-]
    param = param.split()
    altype = param[0].upper()
    char = ' ' 
    end = 1
    if len(param)==2:
      end = param[1].upper()
    if len(param)==3:
      end = param[1].upper()
      char = param[2]
    
    if end == 'ALL':
      start_row = 0
      end_row = len(self.buff)
    elif end.isdigit():
      start_row = self.cury
      end_row = self.cury + int(end)
    else:
      self.show_prompt('strip: wrong value for [lines].')
      return
    
    for row in range(start_row, end_row):
      line = ''.join(self.buff[row])
      if altype == 'LEFT':
        self.buff[row]=list(line.lstrip(char))
      elif altype == 'RIGHT':
        self.buff[row]=list(line.rstrip(char))
      elif altype == 'CENTER':
        self.buff[row]=list(line.strip(char))
      self.modified += 1
    self.cury = end_row-1
    self.curx = len(self.buff[end_row-1])
    self.scroll_buffer()
  
  def indent(self,indent):
    #indent = self.command_prompt('indent:')
    try: # format: [rows] [cols] [+/-]
      start_row = self.cury
      end_row = self.cury + int(indent.split()[0])
      start_col = self.curx
      end_col = self.curx + int(indent.split()[1])
      dir = indent.split()[2]
      try: char = indent.split()[3]
      except: char = ''
      for row in range(start_row, end_row):
        for col in range(start_col, end_col):
          if dir == '+': self.buff[row].insert(col, char if char != '' else ' ')
          if dir == '-': del self.buff[row][self.curx]
      self.modified += 1        
    except: pass

  def search(self):
    self.search_results = []
    self.search_index = 0
    word = self.command_prompt('search: ')
    for row in range(len(self.buff)):
      buffrow = self.buff[row]
      for col in range(len(buffrow)):
        if ''.join([c for c in buffrow[col:col+len(word)]]) == word:
          self.search_results.append([row, col])
    if len(self.search_results):
      self.cury, self.curx = self.search_results[self.search_index]
      self.search_index += 1

  def find_next(self):
    if len(self.search_results):
      if self.search_index == len(self.search_results):
        self.search_index = 0
      try: self.cury, self.curx = self.search_results[self.search_index]
      except: pass
      self.search_index += 1

  def load_file(self):
    if self.modified:
      if self.getyn('current document is modified. save? y/n'):
        self.save_file('')
    
    fn = self.command_prompt('load file: ')
    if os.path.isfile(fn):
      self.open_file(fn)
    else:
      self.show_prompt('file not found!')
    
  def open_file(self, filename):
    global PLATFORM
    self.reset()
    try:
      with open(filename) as f:
        content = f.read().split('\n')
        for row in content[:-1]:
          self.buff.append([c for c in row])
    except: self.buff.append([])
    if filename and os.path.isfile(filename):
      self.filename = filename
      self.filetype = self.filename.split('.')[-1]
      PLATFORM = isdosfile(filename)
      if '.txt' in filename: self.highlight = False
      else: self.highlight = True
    self.total_lines = len(self.buff)
    self.update_screen()
  
  def saveas_ansi(self):
    fn = self.command_prompt('filename: ',self.filename)
    if fn:
      self.filename = fn
    else:
      self.show_prompt('Aborting...')
      return
    prep = self.getkey('video preparation? [C]lear Screen, [H]ome Cursor, [N]one: ','CHN')
    with open(self.filename, 'w', newline=crlf()) as f:
      content = ''
      for row in self.buff:
        content += ''.join([c for c in row]) + '\n'
        
      if chr(prep) in 'Cc': content = ansi['clear']+content
      elif chr(prep) in 'Hh': content = ansi['home']+content
      
      f.write(content)
    self.modified = 0
  
  def quicksave_file(self):
    #open('tmpfile', 'w', newline='\r\n') as f:
    with open(self.filename, 'w', newline=crlf()) as f:
      content = ''
      for row in self.buff:
        content += ''.join([c for c in row]) + '\n'
      f.write(content)
    self.modified = 0
    
  def save_buff(self,buf,filename):
    with open(filename, 'w', newline=crlf()) as f:
      content = ''
      for row in buf:
        content += ''.join([c for c in row]) + '\n'
      f.write(content)
   
  def save_file(self,params):
    fn = self.command_prompt('save ['+self.filetype+'] filename: ',self.filename)
    if fn:
      self.filename = fn 
      self.quicksave_file()
      
  def extract_lines(self,params):
    fn = self.command_prompt('filename: ',self.filename)
    if fn:
      end = params.upper()
      start_row = self.cury
      if end == 'ALL':
        start_row = 0
        end_row = len(self.buff)
      elif end.isdigit():
        try: end_row = self.cury + int(end)
        except: end_row = self.cury + 1
      else:
        self.show_prompt('extract: wrong value for [lines].')
        return

      if end_row > len(self.buff)-1: end_row = len(self.buff)-1
      with open(fn, 'w', newline=crlf()) as f:
        content = ''
        for row in range(start_row, end_row):
          line = ''.join(self.buff[row])
          content += ''.join([c for c in line]) + '\n'
        f.write(content)
      

  def new_file(self):
    self.reset()
    self.buff.append([])
    self.total_lines = 1

  def exit(self):
    for i in range(4):
      if i == self.active:
        if self.modified:
          if self.getyn('save current text before exit? y/n: '):
            self.quicksave_file()
      else:
        if self.windows[i]['modified']:
          if self.getyn('save text from window['+str(i)+'] before exit? y/n: '):
            fn = self.command_prompt('window['+str(i)+'] filename: ',self.windows[i]['filename'])
            if fn:
              self.save_buff(self.windows[i]['buff'],fn)
            
    curses.endwin()
    sys.exit(0)

  def start(self):
    self.update_screen()
    while(True):
      self.read_keyboard()
      self.update_screen()

if __name__ == '__main__':
  def main(stdscr):
    editor = Editor()
    if len(sys.argv) >= 2: editor.open_file(sys.argv[1])
    else: editor.open_file('untitled.txt')
    editor.start()

  os.environ['ESCDELAY'] = "25"
  curses.wrapper(main)

#`  
#`  --------------------------------------------------------------------------
#`  CliEdit v1.0 - Made by XQTR of Another Droid BBS // andr01d.zapto.org:9999
#`  --------------------------------------------------------------------------
#`                        
#`                           Press ESC or F1 to go back
#`                        
#`       * Sections with an asterisk are not supported yet in this version.
#`                        
#`  ------------------
#`  Keyboard Shortcuts
#`  ------------------
#`  
#`      CTRL-Q : Exit
#`      CTRL-X : Enter Command Prompt
#`         ESC : Enter Command Prompt
#`      CTRL-O : Open/Load file
#`      CTRL-N : New file / Resets current window
#`      CTRL-S : Save document
#`      CTRL-F : Find
#`      CTRL-G : Find next
#`      CTRL-E : Clear to End Of Line (EOL)
#`      CTRL-D : Delete current line
#`      CTRL-W : Delete previous word
#`      CTRL-H : This help screen
#`      CTRL-T : Strip space in right side for current line
#`      CTRL-B : Toggle bookmark
#`      CTRL-R : Repeat last command
#`      CTRL-V : Paste from clipboard
#`      CTRL-C : Copy to clipboard
#`      CTRL-A : Toggle AutoIndent/Spaces
#`      CTRL-L : Jump to line
#`          F1 : Change to Window #1
#`          F2 : Change to Window #2
#`          F3 : Change to Window #3
#`          F4 : Change to Window #4
#`          F5 : Edit source code of this script
#`          F7 : Compile code in current window
#`          F9 : Go to previous bookmark
#`         F10 : Go to next bookmark 
#`         INS : Toggle Insert/Overwrite mode
#`    CTRL-END : Go to end of document
#`   CTRL-HOME : Go to start of document   
#`   CTRL-LEFT : Move cursor to previous word
#`  CTRL-RIGHT : Move cursor to next word
#`  --------------------------------------------------------------------------
#`    
#`  -----------------------
#`  Command Prompt Commands
#`  -----------------------
#`  
#`  Pressing  ESC  or  CTRL-X, will invoke the command prompt. In there you can
#`  type  various supported commands to format the document and not only. While
#`  in the command prompt, press ESC to cancel and/or leave the command prompt.
#`  Below  is  a  list  with  all  supported commands and their paramaters. The
#`  commands are case insensitive.
#`  
#`  Except from the commands, if you enter a simple math expression, it will 
#`  calculate the result and insert it in the text. It's very useful, when 
#`  you want to calculate a color attribute like: 14+(4*16), yellow on red 
#`  background ;)
#`  --------------------------------------------------------------------------
#`  
#`  align <left|right|center> [lines] 
#`  al <left|right|center> [lines] 
#`    
#`    Aligns text for n line(s). If the number of lines is not given, it will 
#`    align the current line, only.
#`    
#`    Example: align center 10
#`    Aligns the text in center, from the current line and for the next 10 
#`    lines.
#`  --------------------------------------------------------------------------
#`  
#`  regex <search> <replace> [lines]
#`  
#`    This is a regular expression search and replace function. You can give 
#`    a regex pattern to find and replace with a given string, for n lines or 
#`    the whole document.
#`    
#`    If the parameters have space in them, put them inside double-quotes.
#`    
#`    Example: regex ^ # all
#`    It will insert a hash character in front of each line, for the whole 
#`    document. The ^ char. in regex means "in the beginning of the line"
#`    
#`    Example: regex "[oO]" "0" all
#`    Will replace all letters o and O with number 0, for a more elit theme 
#`    ;) Double-Quotes are also acceptable.
#`  --------------------------------------------------------------------------
#`    
#`  justify <lines> 
#`  just <lines> 
#`  
#`    Justifies text for n line(s). The number must be greater from 2. It 
#`    will justify the text from current line and for the n next lines. 
#`    Because, the resulted justified text could be less lines than the 
#`    original, the command will not erase the previous lines and it will 
#`    insert the new justified text in the current position.
#`    
#`    Example: justify 10
#`    It will justify and insert the text from the current line and for the 
#`    next 10 lines.
#`  --------------------------------------------------------------------------
#`    
#`  strip <left|right|center> [lines|all] 
#`  st <left|right|center> [lines|all] 
#`    
#`    Strips empty space from text, for n lines. If no number of lines is 
#`    given it will strip only the current line. If the ALL paramater is 
#`    given it will strip spaces from the whole document.
#`    
#`    Example: strip right all
#`    Will strip spaces from the right side of text, for the whole document.
#`  --------------------------------------------------------------------------
#`  
#`  format <lower|caps|upper> [lines]
#`  
#`    Change capitalization for n line(s) or current line if no number is 
#`    given. The format can be:
#`    
#`    caps or upper - All capital
#`    lower         - All lower case
#`    title         - Make the first letter of each word in capital
#`  --------------------------------------------------------------------------  
#`  
#`  insert <gpl|bsd|blog|script|html|python|pascal> 
#`  ins <gpl|bsd|blog|script|html|python|pascal> 
#`  
#`    Inserts text templates for various things, like a BSD license, a Python 
#`    script or even a text blog post.
#`    
#`    Example: insert html
#`    It will insert a HTML template
#`  --------------------------------------------------------------------------
#`  
#`  filetype <pascal|python|c|bas|delphi|text|bbcode|html|none|bash|mpy|mpl>
#`  fl <pascal|python|c|bas|delphi|text|bbcode|html|none|bash|mpy|mpl>
#`  
#`    Changes the file type for current document. This is used for the syntax 
#`    highlighting feature.
#`    
#`    Example: fl bash
#`    Will highlight the text, based on BASH syntax
#`  --------------------------------------------------------------------------
#`   
#`  ascii
#`  
#`    It will give you a prompt to enter an ASCII number, to insert the 
#`    specific ASCII character. If you type 254, it will enter the 254th 
#`    char. from the ASCII table.
#`  --------------------------------------------------------------------------
#`  
#`  width <num> 
#`  
#`    Sets document width to <num> cols.
#`  
#`    Example: width 80
#`    Will set the width to 80 character per line.
#`  --------------------------------------------------------------------------
#`  
#`  indent <rows> <cols> [+/-] 
#`    
#`    Adds or removes spaces for y rows and x cols after the current 
#`    position.
#`    
#`    Example: indent 3 2 +
#`    Will add 2 spaces in each line, for the current line and two more (3 in 
#`    total). If you give: indent 3 2 -, it will remove them
#`  --------------------------------------------------------------------------  
#`    
#`  repeat <cols> <char> 
#`  rep <cols> <char> 
#`  line <cols> <char> 
#`  
#`    Repeats the <char> for <cols> columns. Great to make ascii lines like 
#`    the ones in here :)
#`    
#`    line 80 -
#`    Repeats the character - for 80 times
#`  --------------------------------------------------------------------------
#`  
#`  open 
#`  load 
#`  
#`    Loads a text document to current window. After the command a prompt 
#`    will ask for the filename.
#`  --------------------------------------------------------------------------
#`  
#`  duplicate
#`  dupe
#`  
#`    Duplicates current window document, to the first available empty one.
#`  --------------------------------------------------------------------------
#`  
#`  crlf <win|dos|linux|unix>
#`  
#`    Changes the format of the line ending in file. When you open a file the 
#`    editor detects the line ending format and displays that in the status 
#`    bar. If you want to save the file in a different format, use this 
#`    command.
#`    
#`    Example: crlf dos
#`    Changes the line ending to \r\n
#`    
#`    Windows and DOS uses the same line ending format, the parameters DOS 
#`    and WIN will result in the same format. There are there just for 
#`    convenience.
#`  --------------------------------------------------------------------------  
#`
#`  comment <num> 
#`  cm <num> : comment <num> lines
#`  
#`    Will add the comment symbol # from the current line and for <num> lines 
#`    next.
#`  --------------------------------------------------------------------------
#`  
#`  uncomment <num> 
#`  
#`    Removes the comment symbol # for the next <num> lines.
#`  --------------------------------------------------------------------------
#`  
#`  extract <num|all> : saves <num> lines to a file
#`  
#`    Extracts <num> lines from the current position to another file.
#`  --------------------------------------------------------------------------
#`  
#`  bash
#`  
#`    Lets you insert the output of a SHELL command in the current document.
#`  --------------------------------------------------------------------------
#`  
#`  delete <num|all> 
#`  del <num|all> 
#`  
#`    Deletes the next <num> lines, from current position
#`  --------------------------------------------------------------------------
#`  
#`  copy <num|all> 
#`  cp <num|all> 
#`  
#`    Copies to clipboard <num> lines or the whole document  
#`  --------------------------------------------------------------------------
#`  
#`  paste
#`  pt
#`  
#`    Pastes clipboard in current postion.
#`  --------------------------------------------------------------------------
#`  
#`  get <url|file> [codepage]
#`  
#`    Inserts a local file or a file from the internet. Default codepage is 
#`    UTF8. If you get a codepage error try another one, like ascii, cp437 
#`    etc.
#`    
#`    Example: get https://16colo.rs/pack/laz16/raw/FILE_ID.DIZ cp437
#`    Inserts the specified file from the internet.
#`  --------------------------------------------------------------------------
#`  
#`  spell <on|off> 
#`  
#`    Turns on/off spell suggestions. You can't insert a suggestion, only see 
#`    them.
#`  --------------------------------------------------------------------------
#`  
#`  code <on|off> 
#`  
#`    Turns on/off code hints, if available for the file type of the 
#`    document.
#`  --------------------------------------------------------------------------
#`  
#`  ansi <param>
#`  
#`    Inserts an ANSI Code for the given parameter. The paramater can be a 
#`    color or a special ansi code. Acceptable paramaters are:
#`    
#`    black, blue, green, cyan, red, magenta, brown, grey, darkgrey, lightblue,
#`    lightgreen, lightcyan, lightred, lightmagenta, yellow, white, reset, 
#`    clear, cls, goto, reverse and also integer values of colors.
#`    
#`    Example: ansi 14
#`    Will insert the equivelant ansi code for color yellow
#`  --------------------------------------------------------------------------
#`  
#`  mci <code> 
#`  
#`    Inserts a mystic bbs MCI code. Supported MCI codes are:
#`    
#`    00 to 23 for colors
#`    TI - current time
#`    US - height of terminal
#`    DA - current date
#`    UX - hostname
#`    UY - local ip
#`  --------------------------------------------------------------------------
#`  
#`  box <type> 
#`  
#`    Inserts a predefined ASCII box. <type> is an integer from 1.    
#`  --------------------------------------------------------------------------
#`  
#`  bookmark 
#`    
#`    Toggles, sets or unsets a bookmark in current line.
#`  --------------------------------------------------------------------------
#`  
#`  menuc [header] [option1] [option2] ..
#`  menul [header] [option1] [option2] ..
#`  
#`    Inserts a menu box with [header] and as many options/items you like. 
#`    menuc is for centered items and menul for left aligned items.
#`    
#`    Example: menuc PopUp item1 item2 item3
#`    Will insert the following ascii box.
#`    .----- PopUp -----.
#`    |      item1      |
#`    |      item2      |
#`    |      item3      |
#`    `-----------------'
#`  --------------------------------------------------------------------------
#`  
#`  saveas <type> *
#`  
#`    Saves/exports the document in a different format. Currently supported 
#`    formats are:
#`    
#`    gopher: saves the document as a gophermap file
#`    ansi  : saves the document as an ansi file, will ask for SAUCE data.
#`  --------------------------------------------------------------------------
#`  
#`  gopher <link|file|image|dir|url|bin|img|include|shell> 
#`  
#`    With this command you can insert gophermap items in a more easy way, as 
#`    the program asks you about the link, host, port etc. and then formats 
#`    the text to be inserted appropriate.
#`    
#`    link or url : enters a gopher link
#`    file        : inserts a local text file as a link
#`    image or img: inserts a local image file as a link
#`    bin         : inserts a local binary file as a link
#`    include     : inserts the text from a local text file, it's helpful to 
#`                  use for headers/footers in map files
#`    dir         : inserts a local directory as a link
#`    shell       : inserts a shell command item
#`    empty       : inserts an empty line item
#`    date        : inserts a date bbcode
#`    time        : inserts a time bbcode
#`    center      : inserts a center text bbcode
#`    right       : inserts a right bbcode
#`    h1          : inserts a h1/header bbcode
#`    h2          : inserts a h2/header bbcode
#`    hr          : inserts a hr/ruler bbcode
#`    
#`    Example: gopher image
#`    Will ask you about the path and filename of the image and then insert a 
#`    formatted string, that when the file is exported into a gophermap file, 
#`    it will have the correct format.
#`  --------------------------------------------------------------------------
#`  
#`  
#`  ---------------------------------------  
#`  Color numbers for MCI and ANSI commands
#`  ---------------------------------------
#`  
#`  00 : Sets the current foreground to Black
#`  01 : Sets the current foreground to Dark Blue
#`  02 : Sets the current foreground to Dark Green
#`  03 : Sets the current foreground to Dark Cyan
#`  04 : Sets the current foreground to Dark Red
#`  05 : Sets the current foreground to Dark Magenta
#`  06 : Sets the current foreground to Brown
#`  07 : Sets the current foreground to Grey
#`  08 : Sets the current foreground to Dark Grey
#`  09 : Sets the current foreground to Light Blue
#`  10 : Sets the current foreground to Light Green
#`  11 : Sets the current foreground to Light Cyan
#`  12 : Sets the current foreground to Light Red
#`  13 : Sets the current foreground to Light Magenta
#`  14 : Sets the current foreground to Yellow
#`  15 : Sets the current foreground to White
#`
#`  16 : Sets the current background to Black
#`  17 : Sets the current background to Blue
#`  18 : Sets the current background to Green
#`  19 : Sets the current background to Cyan
#`  20 : Sets the current background to Red
#`  21 : Sets the current background to Magenta
#`  22 : Sets the current background to Brown
#`  23 : Sets the current background to Grey
#`  --------------------------------------------------------------------------
#`  
#`  
#`  ----------
#`  Status Bar
#`  ----------
#`  
#`  Lets explain a bit the indications of the status bar.
#`  
#` ^H:Help|^test.pas............|30 lines|     |WIN|#...|PAS|INS|AUTO| 80|B 24:1
#`         |  |                   |              |   |    |   |   |    |  | |
#`         |  |                   |    line ending   |    |   |   |    |  | |
#`         |  |                   |                  |    |   |   |    |  | |
#`         |  |                   |            windows    |   | indent |  | |
#`         |  |                   |                       |   |        |  | |
#`         |  |                   |                filetype   |        |  | |
#`         |  |                   |                           |        |  | |
#`         |  |                   |       insert/overwrite mode        |  | |
#`         |  |                   |                                    |  | |
#`         |  |                   total lines          width of document  | |
#`         |  |                                                           | |
#`         |  filename                       a bookmark is set in this line |
#`         |                                                                |
#`         file is changed and not saved                      cursor position
#`  ----------------------------------------------------------------------------
#`
#`
#`  -----------------
#`  About this editor
#`  -----------------
#`  
#`  Because  i  am  making  mods  for  the  BBS  scene  and  in  general i like
#`  ANSI/ASCII/Terminal  stuff,  i  had  the  need for a text editor like this.
#`  Plain and simple, but powerful for the things i do. RMDOK, "real men, do it
#`  on  keyboard"  they  say, so i wanted an editor that uses only the keyboard
#`  and  not  even  light bar menus. Every function is either set on a keyboard
#`  shortcut or in a command typed in the prompt. Some may like it, others will
#`  definitely wont. For sure it's not for everyone.
#`  
#`  I  made it with Python, not because i like Python or i think it's powerful.
#`  I  only did it, because Python is everywhere now days. In every PC and even
#`  smartphones.  So  with only a git command, you can have this editor in your
#`  system,  in  seconds. Also, because Python is a scripting language, you can
#`  have  the  source  code at your hands and change everything on the fly! You
#`  can  change colors, syntax highlighting scheme, commands, anything! You can
#`  even edit the script from inside the editor.
#`  
#`  Another thing you may notice, is that the whole editor is in one! file. Even
#`  the  help  text  is included inside the script. I wanted to be this way, for
#`  portability of the program. This way, you can get the program to any system,
#`  use  it  and  then  perhaps  delete it or throw it inside a script folder of
#`  yours, with no external files to be left in the system.
#`    
#`  The  editor  is  usable  also  under  Termux in Android phones. In case your
#`  screen is less than 70 columns, the status bar will show less information.
#`  ----------------------------------------------------------------------------
#`  
#`  
#`  ------------
#`  Installation
#`  ------------
#`  
#`  First download the editor from my github repo. Just give the command:
#`  
#`  git clone https://github.com/xqtr/clied
#`  
#`  Then, install some additional Python libraries, like SpellChecker and 
#`  Pyperclip with these commands:
#`  
#`  pip install spellchecker
#`  pip install pyperclip
#`  
#`  There  is a case that the spellchecker library doesn't work for you and when
#`  you  try to run the program, you will get an error about the indexer lib. In
#`  that  case  instead  of  installing  the  spellchecker  library, install the
#`  pyspellchecker library.
#`    
#`  Try  run  it, it should be ok. You could remove the spell suggestion and the
#`  use  of the clipboard, if you want to have a version of the editor with only
#`  default Python packages.
#`  ----------------------------------------------------------------------------
#`
#`
#`  ---------
#`  Functions
#`  ---------
#`  
#`  Let see what this editor can do:
#`  
#`  - Align left/center/right text
#`  - Justify text
#`  - Strip spaces from text
#`  - Insert ANSI codes
#`  - Insert upper ASCII codes
#`  - Format text (lower, upper, title)
#`  - Insert text templates for various formats
#`  - Insert strings like Date, Time, Colors, MCI codes and even Shell 
#`    commands output.
#`  - Support syntax highlight for many languages and also Mystic BBS, MPY and 
#`    MPS. You can also add your own and/or extend the ones used.
#`  - Spell suggestions and on the fly help for commands
#`  - Apply functions to blocks of text
#`  - Extract block of text in external file and clipboard\
#`  - Insert text from external file or even from a downloaded file in the 
#`    Internet.
#`  - Insert predefined ASCII boxes
#`  - Create ASCII menus with a simple command
#`  - Can handle and navigate Bookmarks, for easy navigation in the text
#`  - You can write Gopher map files, with BBCODEs, more below...
#`  - Can make simple calculations and insert the result into the text, from 
#`    the command prompt.
#`  
#`  ----------------------------------------------------------------------------
#`
#`  
#`  ------
#`  Gopher
#`  ------
#`  
#`  With  CliEd,  you  can  edit  and  create  Gophermap files! It uses a set of
#`  BBCodes  to  insert specific gopher items, like files, images, links etc. to
#`  make  gophermap  creation easier. If you learn and know the bbcodes, you can
#`  speed  up  the  process, but until you memorize them, you can use the gopher
#`  <item>, command to insert the bbcodes. You will find a list of the supported
#`  items in the section about the GOPHER command.
#`    
#`  When you finish editing the page/text, you enter the: SAVEAS GOPHER command,
#`  which  will  guide  you  to enter the needed information and at the end will
#`  export  the  gophermap  file,  as a gopher server wants it to be, with tabs,
#`  server address, port etc.
#`    
#`  You can then move the file to your gopher site and use it. If you don't know
#`  what Gopher is... google it! :) You can also download a copy of lynx browser
#`  and visit my gopher site like: lynx gopher://andr01d.zapto.org:7070
#`    
#`  If you like textmode, you will love Gopher!  
#`  ----------------------------------------------------------------------------
#`
#`  
#`  -------
#`  Credits
#`  -------
#`  
#`  The core of this editor was found from a github project (link below). So 
#`  many thanks to the orginal author who open sourced his project.
#`  
#`  Kudos to the author of the justify function, very useful and rare to find 
#`  a working solution like this. You can get the function here:
#`  https://github.com/KonstantinosAng/CodeWars/blob/master/Python/
#`  %5B4%20kyu%5D%20Text%20align%20justify.py
#`  
