#!/bin/python3
import curses
import sys,os
import urllib.request
from pygments.lexers import PythonLexer, CLexer, BBCodeLexer, DelphiLexer,HtmlLexer,QBasicLexer,BashLexer
from pygments.formatters import TerminalFormatter
from pygments.token import Keyword, Name, Comment, String, Error, \
    Number, Operator, Generic, Token, Whitespace
from pygments import highlight
from subprocess import check_output
import datetime
from time import sleep
import pyperclip
import socket

COLOR_SCHEME = {
  Token:              ('gray',                 'gray'),
  Comment:            ('magenta',     'brightmagenta'),
  Comment.Preproc:    ('magenta',     'brightmagenta'),
  Keyword:            ('blue',                   '**'),
  Keyword.Type:       ('green',       '*brightgreen*'),
  Operator.Word:      ('**',                     '**'),
  Name.Builtin:       ('cyan',           'brightblue'),
  Name.Function:      ('blue',           'brightblue'),
  Name.Class:         ('_green_',        'brightblue'),
  Name.Decorator:     ('magenta',     'brightmagenta'),
  Name.Variable:      ('blue',           'brightblue'),
  String:             ('yellow',       'brightyellow'),
  Number:             ('blue',         'brightyellow')
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

# -*- coding: ascii -*-

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
    self.tab = 2
    self.seperators = " ,.()+-/*=~%<>[];{}"
    self.ROWS, self.COLS = self.screen.getmaxyx()
    self.ROWS -= 1
    self.insert = True
    curses.raw()
    curses.noecho()
    self.history = []
    self.filetype = 'txt'
    self.lexers = { 'py': PythonLexer, 'c': CLexer, 'bb':BBCodeLexer, 'pas':DelphiLexer, 'htm':HtmlLexer, 'bas':QBasicLexer, 'sh':BashLexer}

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
    
  def bashcmd(self):
    cmd = self.command_prompt('command:')
    cmd = cmd.split()
    if len(cmd) == 1:
      k = check_output(cmd[0])
    else:
      k = check_output([cmd[0], " ".join(cmd[1:])])
    
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
    if len(self.buff) == 1: return
    try:
      del self.buff[self.cury]
      self.curx = 0
      self.total_lines -= 1
    except: pass
    self.modified += 1
    if self.cury >= self.total_lines:
      self.cury = self.total_lines-1

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
    while count != self.ROWS:
      if key == curses.KEY_NPAGE:
        self.move_cursor(curses.KEY_DOWN)
        if self.offy < self.total_lines - self.ROWS: self.offy += 1
      elif key == curses.KEY_PPAGE:
        self.move_cursor(curses.KEY_UP)
        if self.offy: self.offy -= 1
      count += 1

  def scroll_buffer(self):
    if self.cury < self.offy: self.offy = self.cury
    if self.cury >= self.offy + self.ROWS: self.offy = self.cury - self.ROWS+1
    if self.curx < self.offx: self.offx = self.curx
    if self.curx >= self.offx + self.COLS: self.offx = self.curx - self.COLS+1

  def print_status_bar(self):
    status = '\x1b[7m'
    status += "^H:Help |"
    status += '^' if self.modified else ' '
    status += self.filename[:20].ljust(20) + ' | ' + str(self.total_lines) + ' lines'+'|'+self.msg 
    
    
    ps = '| '+self.filetype.upper()+' '
    
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
    while len(status) < self.COLS - len(ps) + 3: status += ' '
    status += ps + ' '
    status += '\x1b[m'
    status += '\x1b[' + str(self.cury - self.offy+1) + ';' + str(self.curx - self.offx+1) + 'H'
    status += '\x1b[?25h'+colors['reset']
    return status

  def print_buffer(self):
    print_buffer = '\x1b[?25l'
    print_buffer += '\x1b[H\x1b[2J'
    for row in range(self.ROWS):
      buffrow = row + self.offy;
      if buffrow < self.total_lines:
        rowlen = len(self.buff[buffrow]) - self.offx
        if rowlen < 0: rowlen = 0;
        if rowlen > self.COLS: rowlen = self.COLS;
        try:
          print_buffer += highlight(
          ''.join([c for c in self.buff[buffrow][self.offx: self.offx + rowlen]]),
          self.lexers[self.filetype](),
          TerminalFormatter(bg='dark', colorscheme=COLOR_SCHEME))[:-1]
        except: print_buffer += ''.join([c for c in self.buff[buffrow][self.offx: self.offx + rowlen]])
      print_buffer += '\x1b[K'
      print_buffer += '\r\n'
    return print_buffer
    
  def pause(self):
    c = -1
    while (c == -1): c = self.screen.getch()
  
  def inhelp(self):
    scr = 1
    
    while True:
      if scr == 1:
        print_buffer = '\x1b[?25l'
        print_buffer += '\x1b[H\x1b[2J'
        print_buffer += ' Help and Shortcuts...\r\n'
        print_buffer += ' ---------------------\r\n'
        print_buffer += '\r\n'

        print_buffer += 'CTRL-N    : New File                CTRL-F : Find String\r\n'
        print_buffer += 'CTRL-S    : Save File               CTRL-G : Search Again\r\n'
        print_buffer += '\r\n'
        print_buffer += 'CTRL-D    : Delete Line             CTRL-W : Delete to prev. word\r\n'
        print_buffer += '                                    CTRL-C : Enter Editor/App. Command\r\n'
        print_buffer += 'CTRL-A    : Auto Indent             CTRL-B : Insert Command Output\r\n'
        print_buffer += '\r\n'
        print_buffer += 'CTRL-END  : End of Document         CTRL-RIGHT Cursor : Next Word\r\n'
        print_buffer += 'CTRL-HOME : Start of Document       CTRL-LEFT Cursor  : Prev. Word\r\n'
        print_buffer += '                                    CTRL-SHIFT-TAB    : Backward TAB\r\n'
      elif scr == 2:
        print_buffer = '\x1b[?25l'
        print_buffer += '\x1b[H\x1b[2J'
        print_buffer += ' Commands...\r\n'
        print_buffer += ' -----------\r\n'
        print_buffer += '\r\n'
        print_buffer += 'date [format]           : insert current date - formats: ymd, mdy, dmy\r\n'
        print_buffer += 'time                    : insert current time\r\n'
        print_buffer += 'width <cols>            : set width for document\r\n'
        print_buffer += 'filetype <type>         : set filetype, for highlighting\r\n'
        print_buffer += '                          types: pascal, python, basic, c, html, bbcode\r\n'
        print_buffer += 'align <side> [char]     : align current line text, with giver char\r\n'
        print_buffer += '                          side: left, right, center\r\n'
        print_buffer += 'ascii <num>             : insert ascii char\r\n'
        print_buffer += 'comment <n>             : comment the n next lines\r\n'
        print_buffer += 'uncomment <n>           : uncomment the n next lines\r\n'
        print_buffer += 'repeat <width> <char>   : repeat the given character to given width\r\n'
        print_buffer += 'line <width> <char>     : same us repeat\r\n'
        print_buffer += 'indent <rows> <cols> [+/-] : un/indent the following lines with <cols> spaces,\r\n'
        print_buffer += '                             from the current x position.\r\n'
      
      for row in range(self.ROWS - len(print_buffer.split('\n'))):
        print_buffer += '\x1b[K'
        print_buffer += '\r\n'
      print_buffer += '\x1b['+str(self.ROWS)+';13HPress 1 for shortcuts, 2 for commands, any other to exit.'
      
      sys.stdout.write(print_buffer)
      sys.stdout.flush()
      
      c = -1
      while (c == -1): c = self.screen.getch()
      
      if c == ord('1'): scr = 1
      elif c==ord('2'): scr = 2
      else:
        break
    self.update_screen()
    self.screen.refresh()
    

  def update_screen(self):
    self.scroll_buffer()
    print_buffer = self.print_buffer()
    status_bar = self.print_status_bar()
    sys.stdout.write(print_buffer + status_bar)
    sys.stdout.flush()

  def resize_window(self):
    self.ROWS, self.COLS = self.screen.getmaxyx()
    self.ROWS -= 1
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
    elif c == ctrl(ord('x')) or c == 27: self.docommand()      
    elif c == 9: [self.insert_char(' ') for i in range(self.tab)] #TAB KEY
    elif c == curses.KEY_BTAB: [self.delete_char() for i in range(self.tab) if self.curx]
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
    elif c == curses.KEY_IC: self.insert=not self.insert
    elif c == curses.KEY_DC: self.del_char()
    elif c == curses.KEY_RESIZE: self.resize_window()
    elif c == curses.KEY_HOME: self.curx = 0
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

  def clear_prompt(self, line):
    command_line = line
    ps = str(len(self.buff))+' lines '    
    ps += str(self.cury+1).rjust(3,' ') + ':' + str(self.curx+1).rjust(2,'0')
    while (len(command_line) + len(ps)) < self.COLS-1: command_line += ' '
    command_line = '\x1b[' + str(self.ROWS+1) + ';' + '0' + 'H' + command_line
    command_line = '\x1b[7m' + command_line
    command_line += ps 
    command_line += '\x1b[' + str(self.ROWS+1) + ';' + str(len(line)+1) + 'H'
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
    
    line = '\x1b['+str(self.ROWS)+';1H'
    line += colors[0]+colors[22]+words
    line += '\x1b['+str(self.ROWS+1)+';'+str(cursorpos+1)+'H'+colors['reset']+colors['reverse']
    sys.stdout.write(line)
    sys.stdout.flush()
    
  def command_prompt(self, prompt,value='',recomend=False):
    recomended = []
    self.clear_prompt(prompt)
    self.screen.refresh()
    word = ''; c = -1; pos = 0
    index = len(self.history)
    
    def backspace():
      nonlocal pos,word
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
          parts = str(word).split()
          if len(parts)==1:
            recomended = ['time','save','extract','exit','quit','width','filetype','fl', \
            'align','al','strip','st','ascii','ansi','clear','reset','commend','cm',\
            'uncomment','date','dt','line','repeat','rep','indent','ind','delete','del',\
            'copy','cp','paste','pt','get','insert','mci','box','menul','menuc']
            self.dorecommend(word,pos+len(prompt),RECOMEND=recomended)
          else:
            if parts[0].upper() in ['ALIGN','AL']:
              recomended=['align <left|right|center> [lines] : align text for line(s)']
              self.dorecommend(word,pos+len(prompt),True,RECOMEND=recomended)
            elif parts[0].upper() in ['STRIP','ST']:
              recomended=['strip <left|right|center> [lines|all] : strip text for line(s)']
              self.dorecommend(word,pos+len(prompt),True,RECOMEND=recomended)
            elif parts[0].upper() in ['INSERT','INS']:
              recomended=['insert <gpl|bsd|blog|script|html|python|pascal> : insert text template']
              self.dorecommend(word,pos+len(prompt),True,RECOMEND=recomended)
            elif parts[0].upper() in ['FILETYPE','FL']:
              recomended=['pascal','python','c','bas','delphi','text','bbcode','html','none','bash']
              self.dorecommend(word,pos+len(prompt),True,RECOMEND=recomended)
            elif parts[0].upper() in ['ASCII']:
              recomended=['type ascii number of the character you want']
              self.dorecommend(word,pos+len(prompt),True,RECOMEND=recomended)
            elif parts[0].upper() in ['WIDTH']:
              recomended=['width <num> : set document width to <num> cols']
              self.dorecommend(word,pos+len(prompt),True,RECOMEND=recomended)
            elif parts[0].upper() in ['INDENT','IND']:
              recomended=['indent <rows> <cols> [+/-] : indent <cols> for <rows> from current position']
              self.dorecommend(word,pos+len(prompt),True,RECOMEND=recomended)
            elif parts[0].upper() in ['LINE','REPEAT','REP']:
              recomended=['repeat <cols> <char> : repeat <char> for <cols> times']
              self.dorecommend(word,pos+len(prompt),True,RECOMEND=recomended)
            elif parts[0].upper() in ['COMMENT','CM']:
              recomended=['comment <num> : comment <num> lines']
              self.dorecommend(word,pos+len(prompt),True,RECOMEND=recomended)
            elif parts[0].upper() in ['UNCOMMENT']:
              recomended=['uncomment <num> : comment <num> lines']
              self.dorecommend(word,pos+len(prompt),True,RECOMEND=recomended)
            elif parts[0].upper() in ['EXTRACT']:
              recomended=['extract <num|all> : saves <num> lines to a file']
              self.dorecommend(word,pos+len(prompt),True,RECOMEND=recomended)
            elif parts[0].upper() in ['BASH']:
              recomended=['bash : inserts output of a BASH command']
              self.dorecommend(word,pos+len(prompt),True,RECOMEND=recomended)
            elif parts[0].upper() in ['DELETE','DEL']:
              recomended=['delete <num|all> : delete <num> lines']
              self.dorecommend(word,pos+len(prompt),True,RECOMEND=recomended)
            elif parts[0].upper() in ['COPY','CP']:
              recomended=['copy <num|all> : copy <num> lines to clipboard']
              self.dorecommend(word,pos+len(prompt),True,RECOMEND=recomended)
            elif parts[0].upper() in ['PASTE','PT']:
              recomended=['paste : paste from clipboard in current position']
              self.dorecommend(word,pos+len(prompt),True,RECOMEND=recomended)
            elif parts[0].upper() in ['GET']:
              recomended=['get <url|file> : inserts a local file or from the internet']
              self.dorecommend(word,pos+len(prompt),True,RECOMEND=recomended)
            elif parts[0].upper() in ['ANSI']:
              recomended=['black','blue','red','grey','...','lightblue','lightred','...','white','reset']
              self.dorecommend(word,pos+len(prompt),True,RECOMEND=recomended)
            elif parts[0].upper() in ['MCI']:
              recomended=['mci <code> : inserts a mystic bbs MCI code, if supported']
              self.dorecommend(word,pos+len(prompt),True,RECOMEND=recomended)
            elif parts[0].upper() in ['BOX']:
              recomended=['box <type> : inserts an ASCII box']
              self.dorecommend(word,pos+len(prompt),True,RECOMEND=recomended)
            elif parts[0].upper() in ['MENUC','MENUL']:
              recomended=['menu [header] [option1] [option2] .. : inserts a menu box']
              self.dorecommend(word,pos+len(prompt),True,RECOMEND=recomended)
      except: pass
    self.update_screen()
    self.screen.refresh()
    return word
    
  def insert_str(self,s):
    for i,c in enumerate(s):
      self.buff[self.cury].insert(self.curx+i, c)
    
  def command(self,command):
    global BSD_NOTICE, GPL_NOTICE, HTML_BODY
    
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
    elif cmd == 'ASCII': # ASCII [char-num]
      self.insert_char(chr(int(params)))
    elif cmd == 'ANSI': # ANSI Color
      self.ansicolor(params)
    elif cmd == 'MCI': 
      self.mci(params)
    elif cmd == 'MENUC': 
      self.box(params,1)
    elif cmd == 'MENUL': 
      self.box(params,2)
    elif cmd == 'BOX': 
      self.box2(params)
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
      
  def ansicolor(self,params):
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
    elif typeof == 'mpl': typeof = 'pas'
    elif typeof == 'python': typeof = 'py'
    elif typeof == 'pyw': typeof = 'py'
    elif typeof == 'basic': typeof = 'bas'
    elif typeof == 'mpy': typeof = 'py'
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
    else:
      start_row = self.cury
      end_row = self.cury + int(end)
      
    for row in range(start_row, end_row):
      line = ''.join(self.buff[row]).strip()
      if altype == 'LEFT':
        self.buff[row]=list(line.ljust(self.width,char))
      elif altype == 'RIGHT':
        self.buff[row]=list(line.rjust(self.width,char))
      elif altype == 'CENTER':
        self.buff[row]=list(line.center(self.width,char))
      self.modified += 1
    
  def del_eol(self):
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
  
  def quicksave_file(self):
    with open(self.filename, 'w') as f:
      content = ''
      for row in self.buff:
        content += ''.join([c for c in row]) + '\n'
      f.write(content)
    self.modified = 0
    
  def save_file(self,params):
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
    self.reset()
    self.buff.append([])
    self.total_lines = 1

  def exit(self):
    if self.modified:
      cmd = self.command_prompt('save before exit? y/n:')
      if cmd.upper() == 'Y':
        self.quicksave_file()
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

