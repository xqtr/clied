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
#from subprocess import check_output
import subprocess
import datetime
from time import sleep
import pyperclip
import socket
import re
from spellchecker import SpellChecker

#change the language to your liking: English - ‘en’, Spanish - ‘es’, French - ‘fr’,
# Portuguese - ‘pt’, German - ‘de’, Russian - ‘ru’, Arabic - ‘ar’
spell = SpellChecker(language='en')

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
  'pas':'fpc -gl '
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

COLOR_STATUS = colors[0]+colors[23]
COLOR_SUGGEST = colors[0]+colors[22]

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
 
GPL_NOTICE = '''
 /*
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

def writetext(ln):
  sys.stdout.write(ln)
  sys.stdout.flush()

def stripansi(line):
  ansi_escape = re.compile(r'(?:\x1B[@-_]|[\x80-\x9F])[0-?]*[ -/]*[@-~]')
  return ansi_escape.sub('', line)
  
def ljustansi(line,w):
  while len(stripansi(line)) < w: line+=' '
  return line

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

class Editor():
  def __init__(self):
    self.screen = curses.initscr()
    self.screen.keypad(True)
    self.screen.nodelay(1)
    self.msg=""
    self.autoindent = True
    self.autosuggest = False
    self.modified = False
    self.tab = 2
    self.seperators = " ,.()+-/*=~%<>[];{}"
    self.ROWS, self.COLS = self.screen.getmaxyx()
    self.bottom = self.ROWS-1
    self.statusy = self.ROWS
    self.suggesty = self.ROWS-1
    self.insert = True
    curses.raw()
    curses.noecho()
    self.history = []
    self.filetype = 'txt'
    self.lexers = { 'py': PythonLexer, 'c': CLexer, 'bb':BBCodeLexer, 'pas':DelphiLexer, \
                    'htm':HtmlLexer, 'bas':QBasicLexer, 'sh':BashLexer, 'mpl':MPLLexer, \
                    'mpy':MPYLexer}
                    
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
      'modified':False,
      'filetype':'txt',
      'offx':0,
      'offy':0
      })

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
    self.search_results = []
    self.search_index = 0
    
  def is_separator(self, c):
    for ch in self.seperators:
      if c == ch:
        return True
    return False
  
  def insert_char(self, c):
    global spell
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
    if self.curx<=len(self.buff[self.cury])-1:
      del self.buff[self.cury][self.curx]
      self.modified += 1
  
  def delete_char(self):
    if self.curx:
      self.curx -= 1
      del self.buff[self.cury][self.curx]
    elif self.curx == 0 and self.cury:
      oldline = self.buff[self.cury][self.curx:]
      del self.buff[self.cury]
      self.cury -= 1
      self.curx = len(self.buff[self.cury])
      self.buff[self.cury] += oldline
      self.total_lines -= 1
    self.modified += 1
  
  def jumpto(self):
    cmd = self.command_prompt('line:')
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
    if self.active == 4: return
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
    if self.active == 4: return
    cmd = self.command_prompt('command:')
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
    self.cury += 1
    self.curx = 0
    self.buff.insert(self.cury, [] + list(line))
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
    if self.active == 4: return
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
    if len(self.buff[self.cury])>0:
      while self.buff[self.cury][spaces] == ' ': spaces += 1
      if self.curx != spaces:
        self.curx = spaces
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
    status = '\x1b[' + str(self.statusy) + ';1H'+COLOR_STATUS
    status += "^H:Help |"
    status += '^' if self.modified else ' '
    status += self.filename[:20].ljust(20) + ' | ' + str(self.total_lines) + ' lines'+'|'+self.msg 
    
    i = 0
    ps = ' | '
    while i < 4:
      if self.active == i: ps += '#'
      elif len(self.windows[i]['buff'][0])>0: ps += str(i+1)
      else: ps += '.'
      i+=1
      
    
    ps += ' | '+self.filetype.upper()+' '
    
    if self.insert:
      ps+="| INS "
    else:
      ps+="| OVR "
      
    if self.autoindent:
      ps+="AUTO "
    else:
      ps+="---- "
    
    ps += str(self.width).zfill(2)+' '
    ps += str(self.cury+1).rjust(3,' ') + ':' + str(self.curx+1).rjust(2,'0')
    while len(stripansi(status)) < self.COLS - len(ps) -1: status += ' '
    status += ps + ' '
    status += '\x1b[m'
    status += '\x1b[' + str(self.cury - self.offy+1) + ';' + str(self.curx - self.offx+1) + 'H'
    status += '\x1b[?25h'+colors['reset']
    return status
    
  def print_suggest(self):
    #check spelling of last word
    line = '\x1b['+str(self.suggesty)+';1H'+COLOR_SUGGEST
    ln = ''.join(self.buff[self.cury])
    if ln[-1:] != ' ': return ljustansi(line,self.COLS)
    
    ln = ln.strip()
    if not ln: return ljustansi(line,self.COLS)
    
    wrd = ln[ln[:-1].rfind(' ')+1:] #find the last word after having a space at the end
    # check if word is very big or has symbols inside, if so drop the function as it will take too much time
    if len(wrd)>20: return ljustansi(line,self.COLS)
    for s in self.seperators:
      if s in wrd:
        return ljustansi(line,self.COLS)

    suggs = spell.candidates(wrd)
    if not suggs: return ljustansi(line,self.COLS)
    for w in suggs:
      line += w+' '
    #str(spell.candidates(wrd))
    return ljustansi(line,self.COLS)

  def print_buffer(self):
    print_buffer = '\x1b[?25l'
    print_buffer += '\x1b[H\x1b[2J'
    for row in range(self.bottom):
      buffrow = row + self.offy;
      if buffrow < self.total_lines:
        rowlen = len(self.buff[buffrow]) - self.offx
        if rowlen < 0: rowlen = 0;
        if rowlen > self.COLS: rowlen = self.COLS;
        try:
          print_buffer += highlight(
          ''.join([c if c!=chr(27) else '^' for c in self.buff[buffrow][self.offx: self.offx + rowlen]]),
          self.lexers[self.filetype](),
          TerminalFormatter(bg='dark', colorscheme=COLOR_SCHEME))[:-1]
        except: print_buffer += ''.join([c if c!=chr(27) else '^' for c in self.buff[buffrow][self.offx: self.offx + rowlen]])
      print_buffer += '\x1b[K'
      print_buffer += '\r\n'
    return print_buffer
    
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
  
  def set_suggest(self,value):
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
    self.set_suggest(self.autosuggest)
    self.screen.refresh()
    self.update_screen()
    
  def docommand(self):
    if self.active == 4: return
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
    elif c == ctrl(ord('e')): self.del_eol()
    elif c == ctrl(ord('g')): self.find_next()
    elif c == ctrl(ord('d')): self.delete_line()
    elif c == ctrl(ord('w')): self.delb_word()
    elif c == ctrl(ord('h')): self.inhelp()
    elif c == ctrl(ord('t')): self.strip('right 1')
    elif c == ctrl(ord('b')): self.bashcmd()
    elif c == ctrl(ord('r')): self.command(self.history[-1]) # repeat last command
    elif c == ctrl(ord('v')): self.paste_lines('')
    elif c == ctrl(ord('c')): self.copy_lines('1')
    elif c == ctrl(ord('a')): self.autoindent=not self.autoindent
    elif c == ctrl(ord('l')): self.jumpto()
    elif c == curses.KEY_F1: self.changewindow(0)
    elif c == curses.KEY_F2: self.changewindow(1)
    elif c == curses.KEY_F3: self.changewindow(2)
    elif c == curses.KEY_F4: self.changewindow(3)
    elif c == curses.KEY_F7: self.compile()
    elif c == curses.KEY_IC: self.insert=not self.insert
    elif c == curses.KEY_DC: self.del_char()
    elif c == curses.KEY_RESIZE: self.resize_window()
    elif c == curses.KEY_HOME: self.move_home()
    elif c == curses.KEY_END: self.curx = len(self.buff[self.cury])
    elif c == curses.KEY_LEFT: self.move_cursor(c)
    elif c == curses.KEY_RIGHT: self.move_cursor(c)
    elif c == curses.KEY_UP: self.move_cursor(c)
    elif c == curses.KEY_DOWN: self.move_cursor(c)
    elif c == curses.KEY_BACKSPACE: self.delete_char()
    elif c == curses.KEY_NPAGE: self.scroll_page(c)
    elif c == curses.KEY_PPAGE: self.scroll_page(c)
    elif c == 530: self.scroll_end()
    elif c == 535: self.scroll_home()
    elif c == 560: self.skip_word(560)
    elif c == 545: self.skip_word(545)
    elif c == ord('\n'): self.insert_line()
    elif ctrl(c) != c: self.insert_char(chr(c))

  def changewindow(self,win):
    if win == self.active: return
    #save previous state
    self.windows[self.active]['buff'].clear()
    self.windows[self.active]['buff'] = self.buff.copy()
    self.windows[self.active]['filename'] = self.filename
    self.windows[self.active]['filetype'] = self.filetype
    self.windows[self.active]['curx'] = self.curx
    self.windows[self.active]['cury'] = self.cury
    self.windows[self.active]['offx'] = self.offx
    self.windows[self.active]['offy'] = self.offy
    self.windows[self.active]['indent'] = self.autoindent
    self.windows[self.active]['suggest'] = self.autosuggest
    self.windows[self.active]['tab'] = self.tab
    self.windows[self.active]['insert'] = self.insert
    self.windows[self.active]['total'] = self.total_lines
    self.windows[self.active]['modified'] = self.modified
    self.windows[self.active]['width'] = self.width
    #activate new window
    self.active = win
    self.buff.clear()
    self.buff = self.windows[self.active]['buff'].copy()
    self.filename = self.windows[self.active]['filename']
    self.filetype = self.windows[self.active]['filetype']
    self.curx = self.windows[self.active]['curx']
    self.cury = self.windows[self.active]['cury']
    self.offx = self.windows[self.active]['offx']
    self.offy = self.windows[self.active]['offy']
    self.autoindent = self.windows[self.active]['indent']
    self.autosuggest = self.windows[self.active]['suggest']
    self.tab = self.windows[self.active]['tab']
    self.insert = self.windows[self.active]['insert']
    self.total_lines = self.windows[self.active]['total']
    self.modified = self.windows[self.active]['modified']
    self.width = self.windows[self.active]['width']
    
    self.scroll_buffer()
    self.update_screen()
    
  
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
            'align','al','strip','st','ascii','ansi','clear','reset','commend','cm',\
            'uncomment','date','dt','line','repeat','rep','indent','ind','delete','del',\
            'copy','cp','paste','pt','get','insert','mci','box','menul','menuc','saveas',
            'spell','open','load','bash']
            self.dorecommend(word,pos+len(prompt),RECOMEND=recomended)
          else:
            if keyword[:keyword.find(' ')] in ['ALIGN','AL']:
              recomended=['align <left|right|center> [lines] : align text for line(s)']
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
            elif keyword[:keyword.find(' ')] in ['ANSI']:
              recomended=['black','blue','red','grey','...','lightblue','lightred','...','white','reset','cls','reverse']
              self.dorecommend(word,pos+len(prompt),True,RECOMEND=recomended)
            elif keyword[:keyword.find(' ')] in ['MCI']:
              recomended=['mci <code> : inserts a mystic bbs MCI code, if supported']
              self.dorecommend(word,pos+len(prompt),True,RECOMEND=recomended)
            elif keyword[:keyword.find(' ')] in ['BOX']:
              recomended=['box <type> : inserts an ASCII box']
              self.dorecommend(word,pos+len(prompt),True,RECOMEND=recomended)
            elif keyword[:keyword.find(' ')] in ['MENUC','MENUL']:
              recomended=['menu [header] [option1] [option2] .. : inserts a menu box']
              self.dorecommend(word,pos+len(prompt),True,RECOMEND=recomended)
            elif keyword[:keyword.find(' ')] in ['SAVEAS']:
              recomended=['saveas <type> : saves/export the doc in a different format']
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
    global BSD_NOTICE, GPL_NOTICE, HTML_BODY
    if self.active == 4: return
    cmd = command
    if not cmd: return
    cmd = cmd.split()
    params = " ".join(cmd[1:])
    cmd = cmd[0].upper()
    
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
    elif cmd == 'STRIP' or cmd == 'ST':
      self.strip(params)
    elif cmd == 'SAVEAS':
      self.saveas(params)
    elif cmd == 'ASCII': # ASCII [char-num]
      self.insert_char(chr(int(params)))
    elif cmd == 'ANSI': # ANSI Color
      self.ansistring(params)
    elif cmd == 'MCI': 
      self.mci(params)
    elif cmd == 'MENUC': 
      self.box(params,1)
    elif cmd == 'MENUL': 
      self.box(params,2)
    elif cmd == 'SPELL':   
      self.dosuggest(params)
    elif cmd == 'BOX': 
      self.box2(params)
    elif cmd == 'OPEN' or cmd == 'LOAD': 
      self.load_file(params)
    elif cmd == 'CLEAR' or cmd == 'RESET': # Reset the editor
      self.new_file()
    elif cmd == 'COMMENT' or cmd == 'CM':
      self.comment(params+' +')
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
      self.show_prompt('Command not recognized!')

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
    
  def saveas(self,params):
    params = params.upper()
    if params == 'ANSI': self.saveas_ansi()

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
  
  def dosuggest(self,params):
    val = params.upper().strip()
    if val == 'ON':
      self.set_suggest(True)
    else:
      self.set_suggest(False)
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
    elif params == 'RESET': self.insert_str(colors['reset'])
    elif params == 'REVERSE': self.insert_str(colors['reverse'])
    else:
      try:
        self.insert_str(colors[int(params)])
      except:
        pass
        
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
    else:
       self.filetype = 'NONE'
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
    try: # format: [rows] [+/-]
      start_row = self.cury
      
      if params.split()[0].upper() == 'ALL':
        start_row = 0
        end_row = len(self.buff)
      else:
        end_row = self.cury + int(params.split()[0])
      
      dir = params.split()[1]
      for row in range(start_row, end_row):
        if dir == '+': self.buff[row].insert(0, '#')
        if dir == '-': del self.buff[row][0]
      self.modified += 1        
    except: pass
  
  def delete_lines(self,param):
    param = param.split()
    end = 1
    if len(param)==1:
      end = param[0].upper()
    
    if end == 'ALL':
      start_row = 0
      end_row = len(self.buff)
    else:
      start_row = self.cury
      end_row = self.cury + int(end)
      
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
    else:
      start_row = self.cury
      end_row = self.cury + int(end)
    
    content = ''
    for row in range(start_row, end_row):
      if row>len(self.buff)-1: break
      content += ''.join(self.buff[row])+'\r\n'
    
    pyperclip.copy(content)
    
  def paste_lines(self,params):
    if self.active == 4: return
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
    else:
      start_row = self.cury
      end_row = self.cury + int(end)
      
    for row in range(start_row, end_row):
      if row>len(self.buff)-1: break
      line = ''.join(self.buff[row]).strip()
      if altype == 'LEFT':
        self.buff[row]=list(line.ljust(self.width,char))
      elif altype == 'RIGHT':
        self.buff[row]=list(line.rjust(self.width,char))
      elif altype == 'CENTER':
        self.buff[row]=list(line.center(self.width,char))
      self.modified += 1
    
  def del_eol(self):
    if self.active == 4: return
    line = ''.join(self.buff[self.cury])
    line = line[:self.curx]
    self.buff[self.cury]=list(line)
      
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
    else:
      start_row = self.cury
      end_row = self.cury + int(end)
      
    
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
    word = self.command_prompt('search:')
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
    if self.active == 4: return
    if self.modified:
      ans = self.getkey('current document is modified. save? y/n','YN')
      if chr(ans) in 'Yy':
        self.save_file('')
    
    fn = self.command_prompt('load file: ')
    if os.path.isfile(fn):
      self.open_file(fn)
    else:
      self.show_prompt('file not found!')
    
  def open_file(self, filename):
    self.reset()
    try:
      with open(filename) as f:
        content = f.read().split('\n')
        for row in content[:-1]:
          self.buff.append([c for c in row])
    except: self.buff.append([])
    if filename:
      self.filename = filename
      self.filetype = self.filename.split('.')[-1]
      if '.txt' in filename: self.highlight = False
      else: self.highlight = True
    self.total_lines = len(self.buff)
    self.update_screen()
  
  def saveas_ansi(self):
    fn = self.command_prompt('filename:',self.filename)
    if fn:
      self.filename = fn
    else:
      self.show_prompt('Aborting...')
      return
    prep = self.getkey('video preparation? [C]lear Screen, [H]ome Cursor, [N]one: ','CHN')
    with open(self.filename, 'w') as f:
      content = ''
      for row in self.buff:
        content += ''.join([c for c in row]) + '\n'
        
      if chr(prep) in 'Cc': content = ansi['clear']+content
      elif chr(prep) in 'Hh': content = ansi['home']+content
      
      f.write(content)
    self.modified = 0
  
  def quicksave_file(self):
    with open(self.filename, 'w') as f:
      content = ''
      for row in self.buff:
        content += ''.join([c for c in row]) + '\n'
      f.write(content)
    self.modified = 0
    
  def save_buff(self,buf,filename):
    with open(filename, 'w') as f:
      content = ''
      for row in buf:
        content += ''.join([c for c in row]) + '\n'
      f.write(content)
   
  def save_file(self,params):
    if self.active == 4: return
    fn = self.command_prompt('filename:',self.filename)
    if fn:
      self.filename = fn 
      self.quicksave_file()
      
  def extract_lines(self,params):
    fn = self.command_prompt('filename:',self.filename)
    if fn:
      end = params.upper()
      start_row = self.cury
      if end == 'ALL':
        start_row = 0
        end_row = len(self.buff)
      else:
        try: end_row = self.cury + int(end)
        except: end_row = self.cury + 1

      if end_row > len(self.buff)-1: end_row = len(self.buff)-1
      with open(fn, 'w') as f:
        content = ''
        for row in range(start_row, end_row):
          line = ''.join(self.buff[row])
          content += ''.join([c for c in line]) + '\n'
        f.write(content)
      

  def new_file(self):
    if self.active == 4: return
    self.reset()
    self.buff.append([])
    self.total_lines = 1

  def exit(self):
    for i in range(4):
      if i == self.active:
        if self.modified:
          cmd = self.getkey('save current text before exit? y/n: ','YN')
          if chr(cmd) in 'Yy':
            self.quicksave_file()
      else:
        if self.windows[i]['modified']:
          cmd = self.getkey('save text from window['+str(i)+'] before exit? y/n: ','YN')
          if chr(cmd) in 'Yy':
            fn = self.command_prompt('window['+str(i)+'] filename:',self.windows[i]['filename'])
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
    else: editor.open_file('')
    editor.start()

  os.environ['ESCDELAY'] = "25"
  curses.wrapper(main)

#` Help and Shortcuts...
#` ---------------------
#`
#`
#`CTRL-N    : New File                CTRL-F : Find String
#`CTRL-S    : Save File               CTRL-G : Search Again
#`
#`CTRL-D    : Delete Line             CTRL-W : Delete to prev. word
#`                                    CTRL-C : Enter Editor/App. Command
#`CTRL-A    : Auto Indent             CTRL-B : Insert Command Output
#`
#`CTRL-END  : End of Document         CTRL-RIGHT Cursor : Next Word
#`CTRL-HOME : Start of Document       CTRL-LEFT Cursor  : Prev. Word
#`                                    CTRL-SHIFT-TAB    : Backward TAB
#`
#` Commands...
#` -----------
#`
#`date [format]           : insert current date - formats: ymd, mdy, dmy
#`time                    : insert current time
#`width <cols>            : set width for document
#`filetype <type>         : set filetype, for highlighting
#`                          types: pascal, python, basic, c, html, bbcode
#`align <side> [char]     : align current line text, with giver char
#`                          side: left, right, center
#`ascii <num>             : insert ascii char
#`comment <n>             : comment the n next lines
#`uncomment <n>           : uncomment the n next lines
#`repeat <width> <char>   : repeat the given character to given width
#`line <width> <char>     : same us repeat
#`indent <rows> <cols> [+/-] : un/indent the following lines with <cols> spaces,
