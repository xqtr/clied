# clied
'''  
  --------------------------------------------------------------------------
  CliEdit v1.0 - Made by XQTR of Another Droid BBS // andr01d.zapto.org:9999
  --------------------------------------------------------------------------
                        
                           Press ESC or F1 to go back
                        
       * Sections with an asterisk are not supported yet in this version.
                        
  ------------------
  Keyboard Shortcuts
  ------------------
  
      CTRL-Q : Exit
      CTRL-X : Enter Command Prompt
         ESC : Enter Command Prompt
      CTRL-O : Open/Load file
      CTRL-N : New file / Resets current window
      CTRL-S : Save document
      CTRL-F : Find
      CTRL-G : Find next
      CTRL-E : Clear to End Of Line (EOL)
      CTRL-D : Delete current line
      CTRL-W : Delete previous word
      CTRL-H : This help screen
      CTRL-T : Strip space in right side for current line
      CTRL-B : Toggle bookmark
      CTRL-R : Repeat last command
      CTRL-V : Paste from clipboard
      CTRL-C : Copy to clipboard
      CTRL-A : Toggle AutoIndent/Spaces
      CTRL-L : Jump to line
          F1 : Change to Window #1
          F2 : Change to Window #2
          F3 : Change to Window #3
          F4 : Change to Window #4
          F5 : Edit source code of this script
          F7 : Compile code in current window
          F9 : Go to previous bookmark
         F10 : Go to next bookmark 
         INS : Toggle Insert/Overwrite mode
    CTRL-END : Go to end of document
   CTRL-HOME : Go to start of document   
   CTRL-LEFT : Move cursor to previous word
  CTRL-RIGHT : Move cursor to next word
  --------------------------------------------------------------------------
    
  -----------------------
  Command Prompt Commands
  -----------------------
  
  Pressing  ESC  or  CTRL-X, will invoke the command prompt. In there you can
  type  various supported commands to format the document and not only. While
  in the command prompt, press ESC to cancel and/or leave the command prompt.
  Below  is  a  list  with  all  supported commands and their paramaters. The
  commands are case insensitive.
  --------------------------------------------------------------------------
  
  align <left|right|center> [lines] 
  al <left|right|center> [lines] 
    
    Aligns text for n line(s). If the number of lines is not given, it will 
    align the current line, only.
    
    Example: align center 10
    Aligns the text in center, from the current line and for the next 10 
    lines.
  --------------------------------------------------------------------------
    
  justify <lines> 
  just <lines> 
  
    Justifies text for n line(s). The number must be greater from 2. It 
    will justify the text from current line and for the n next lines. 
    Because, the resulted justified text could be less lines than the 
    original, the command will not erase the previous lines and it will 
    insert the new justified text in the current position.
    
    Example: justify 10
    It will justify and insert the text from the current line and for the 
    next 10 lines.
  --------------------------------------------------------------------------
    
  strip <left|right|center> [lines|all] 
  st <left|right|center> [lines|all] 
    
    Strips empty space from text, for n lines. If no number of lines is 
    given it will strip only the current line. If the ALL paramater is 
    given it will strip spaces from the whole document.
    
    Example: strip right all
    Will strip spaces from the right side of text, for the whole document.
  --------------------------------------------------------------------------
  
  format <lower|caps|upper> [lines]
  
    Change capitalization for n line(s) or current line if no number is 
    given. The format can be:
    
    caps or upper - All capital
    lower         - All lower case
    title         - Make the first letter of each word in capital
  --------------------------------------------------------------------------  
  
  insert <gpl|bsd|blog|script|html|python|pascal> 
  ins <gpl|bsd|blog|script|html|python|pascal> 
  
    Inserts text templates for various things, like a BSD license, a Python 
    script or even a text blog post.
    
    Example: insert html
    It will insert a HTML template
  --------------------------------------------------------------------------
  
  filetype <pascal|python|c|bas|delphi|text|bbcode|html|none|bash|mpy|mpl>
  fl <pascal|python|c|bas|delphi|text|bbcode|html|none|bash|mpy|mpl>
  
    Changes the file type for current document. This is used for the syntax 
    highlighting feature.
    
    Example: fl bash
    Will highlight the text, based on BASH syntax
  --------------------------------------------------------------------------
   
  ascii
  
    It will give you a prompt to enter an ASCII number, to insert the 
    specific ASCII character. If you type 254, it will enter the 254th 
    char. from the ASCII table.
  --------------------------------------------------------------------------
  
  width <num> 
  
    Sets document width to <num> cols.
  
    Example: width 80
    Will set the width to 80 character per line.
  --------------------------------------------------------------------------
  
  indent <rows> <cols> [+/-] 
    
    Adds or removes spaces for y rows and x cols after the current 
    position.
    
    Example: indent 3 2 +
    Will add 2 spaces in each line, for the current line and two more (3 in 
    total). If you give: indent 3 2 -, it will remove them
  --------------------------------------------------------------------------  
    
  repeat <cols> <char> 
  rep <cols> <char> 
  line <cols> <char> 
  
    Repeats the <char> for <cols> columns. Great to make ascii lines like 
    the ones in here :)
    
    line 80 -
    Repeats the character - for 80 times
  --------------------------------------------------------------------------
  
  open 
  load 
  
    Loads a text document to current window. After the command a prompt 
    will ask for the filename.
  --------------------------------------------------------------------------
  
  crlf <win|dos|linux|unix>
  
    Changes the format of the line ending in file. When you open a file the 
    editor detects the line ending format and displays that in the status 
    bar. If you want to save the file in a different format, use this 
    command.
    
    Example: crlf dos
    Changes the line ending to \r\n
    
    Windows and DOS uses the same line ending format, the parameters DOS 
    and WIN will result in the same format. There are there just for 
    convenience.
  --------------------------------------------------------------------------  

  comment <num> 
  cm <num> : comment <num> lines
  
    Will add the comment symbol # from the current line and for <num> lines 
    next.
  --------------------------------------------------------------------------
  
  uncomment <num> 
  
    Removes the comment symbol # for the next <num> lines.
  --------------------------------------------------------------------------
  
  extract <num|all> : saves <num> lines to a file
  
    Extracts <num> lines from the current position to another file.
  --------------------------------------------------------------------------
  
  bash
  
    Lets you insert the output of a SHELL command in the current document.
  --------------------------------------------------------------------------
  
  delete <num|all> 
  del <num|all> 
  
    Deletes the next <num> lines, from current position
  --------------------------------------------------------------------------
  
  copy <num|all> 
  cp <num|all> 
  
    Copies to clipboard <num> lines or the whole document  
  --------------------------------------------------------------------------
  
  paste
  pt
  
    Pastes clipboard in current postion.
  --------------------------------------------------------------------------
  
  get <url|file> [codepage]
  
    Inserts a local file or a file from the internet. Default codepage is 
    UTF8. If you get a codepage error try another one, like ascii, cp437 
    etc.
    
    Example: get https://16colo.rs/pack/laz16/raw/FILE_ID.DIZ cp437
    Inserts the specified file from the internet.
  --------------------------------------------------------------------------
  
  spell <on|off> 
  
    Turns on/off spell suggestions. You can't insert a suggestion, only see 
    them.
  --------------------------------------------------------------------------
  
  ansi <param>
  
    Inserts an ANSI Code for the given parameter. The paramater can be a 
    color or a special ansi code. Acceptable paramaters are:
    
    black, blue, green, cyan, red, magenta, brown, grey, darkgrey, lightblue,
    lightgreen, lightcyan, lightred, lightmagenta, yellow, white, reset, 
    clear, cls, goto, reverse and also integer values of colors.
    
    Example: ansi 14
    Will insert the equivelant ansi code for color yellow
  --------------------------------------------------------------------------
  
  mci <code> 
  
    Inserts a mystic bbs MCI code. Supported MCI codes are:
    
    00 to 23 for colors
    TI - current time
    US - height of terminal
    DA - current date
    UX - hostname
    UY - local ip
  --------------------------------------------------------------------------
  
  box <type> 
  
    Inserts a predefined ASCII box. <type> is an integer from 1.    
  --------------------------------------------------------------------------
  
  bookmark 
    
    Toggles, sets or unsets a bookmark in current line.
  --------------------------------------------------------------------------
  
  menuc [header] [option1] [option2] ..
  menul [header] [option1] [option2] ..
  
    Inserts a menu box with [header] and as many options/items you like. 
    menuc is for centered items and menul for left aligned items.
    
    Example: menuc PopUp item1 item2 item3
    Will insert the following ascii box.
    .----- PopUp -----.
    |      item1      |
    |      item2      |
    |      item3      |
    `-----------------'
  --------------------------------------------------------------------------
  
  saveas <type> *
  
    Saves/exports the document in a different format. Currently supported 
    formats are:
    
    gopher: saves the document as a gophermap file
    ansi  : saves the document as an ansi file, will ask for SAUCE data.
  --------------------------------------------------------------------------

  ----------
  Status Bar
  ----------
  
  Lets explain a bit the indications of the status bar.
  
 ^H:Help|^test.pas............|30 lines|     |WIN|#...|PAS|INS|AUTO| 80|B 24:1
         |  |                   |              |   |    |   |   |    |  | |
         |  |                   |    line ending   |    |   |   |    |  | |
         |  |                   |                  |    |   |   |    |  | |
         |  |                   |            windows    |   | indent |  | |
         |  |                   |                       |   |        |  | |
         |  |                   |                filetype   |        |  | |
         |  |                   |                           |        |  | |
         |  |                   |       insert/overwrite mode        |  | |
         |  |                   |                                    |  | |
         |  |                   total lines          width of document  | |
         |  |                                                           | |
         |  filename                       a bookmark is set in this line |
         |                                                                |
         file is changed and not saved                      cursor position
  ----------------------------------------------------------------------------


  -----------------
  About this editor
  -----------------
  
  Because  i  am  making  mods  for  the  BBS  scene  and  in  general i like
  ANSI/ASCII/Terminal  stuff,  i  had  the  need for a text editor like this.
  Plain and simple, but powerful for the things i do. RMDOK, "real men, do it
  on  keyboard"  they  say, so i wanted an editor that uses only the keyboard
  and  not  even  light bar menus. Every function is either set on a keyboard
  shortcut or in a command typed in the prompt. Some may like it, others will
  definitely wont. For sure it's not for everyone.
  
  I  made it with Python, not because i like Python or i think it's powerful.
  I  only did it, because Python is everywhere now days. In every PC and even
  smartphones.  So  with only a git command, you can have this editor in your
  system,  in  seconds. Also, because Python is a scripting language, you can
  have  the  source  code at your hands and change everything on the fly! You
  can  change colors, syntax highlighting scheme, commands, anything! You can
  even edit the script from inside the editor.
  ----------------------------------------------------------------------------
  
  
  ------------
  Installation
  ------------
  
  First download the editor from my github repo. Just give the command:
  
  git clone https://github.com/xqtr/clied
  
  Then, install some additional Python libraries, like SpellChecker and 
  Pyperclip with these commands:
  
  pip install spellchecker
  pip install pyperclip
  
  Try run it, it should be ok. You could remove the spell suggestion and 
  the use of the clipboard, if you want to have a version of the editor 
  with only default Python packages.
  ----------------------------------------------------------------------------


  ---------
  Functions
  ---------
  
  Let see what this editor can do:
  
  - Align left/center/right text
  - Justify text
  - Strip spaces from text
  - Insert ANSI codes
  - Insert upper ASCII codes
  - Format text (lower, upper, title)
  - Insert text templates for various formats
  - Insert strings like Date, Time, Colors, MCI codes and even Shell 
    commands output.
  - Support syntax highlight for many languages and also Mystic BBS, MPY and 
    MPS. You can also add your own and/or extend the ones used.
  - Spell suggestions and on the fly help for commands
  - Apply functions to blocks of text
  - Extract block of text in external file and clipboard\
  - Insert text from external file or even from a downloaded file in the 
    Internet.
  - Insert predefined ASCII boxes
  - Create ASCII menus with a simple command
  - Can handle and navigate Bookmarks, for easy navigation in the text

'''
