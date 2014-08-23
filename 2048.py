#!/usr/bin/env python
import curses
from random import randint
import re

stdscr = curses.initscr()
screen_mask = list('''
            +---+---+---+---+
            | 1 | 1 | 1 | 1 |
            +---+---+---+---+
            | 1 | 1 | 1 | 1 |
            +---+---+---+---+
            | 1 | 1 | 1 | 1 |
            +---+---+---+---+
            | 1 | 1 | 1 | 1 |
            +---+---+---+---+
            
            ''')

chairs = [45, 49, 53, 57, 105, 109, 113, 117, 165, 169, 173, 177, 225, 229, 233, 237]
up_index_list = [[0, 1, 2, 3], [1, 2, 3, 4], [2, 3, 4, 5], [3, 4, 5, 6]]
down_index_list = [[12, 8, 4, 0], [13, 9, 5, 1], [14, 10, 6, 2], [15, 11, 7, 3]]
left_index_list = [[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15]]
right_index_list = [[3, 2, 1, 0], [7, 6, 5, 4], [11, 10, 9, 8], [15, 14, 13, 12]]
index_lists = { curses.KEY_UP:up_index_list,curses.KEY_DOWN:down_index_list, \
               curses.KEY_LEFT:left_index_list,curses.KEY_RIGHT:right_index_list }

def debug(s):
    stdscr.addstr(12,0,str(s))

class My_2048(object):
    
    def __init__(self):
        self.content=[' ']*16
    
    def set_list_char(self, str_list, post, popup_char):
        str_list[post] = popup_char
    
    def do_popup(self):
        if not self.content.count(' '):
            return
        post = randint(0, len(self.content)-1)
        popup_char = ['a', 'b'][randint(0, 1)]        
        if ' ' == self.content[post]:
            self.content[post] = popup_char
        else:
            self.do_popup()
            
    def do_punch(self,index_list):
        #get all lists
        temp_list = [ ''.join([ self.content[i] for i in j ]) for j in  index_list ]
        #do punch in every line
        temp_list = [ i.replace(' ','')+' '*i.count(' ') for i in temp_list ]
        #assign lists back to content
        for i in xrange(4):
            for j in xrange(4):
                self.content[index_list[i][j]] = temp_list[i][j]
    
    def do_merge(self,index_list):
        #get all lists
        temp_list = [ [ self.content[i] for i in j ] for j in  index_list ]
        #do merge in every line
        for i in xrange(len(temp_list)):
            for j in xrange(len(temp_list[i]) - 1 ):
                if temp_list[i][j] == temp_list[i][j+1] and temp_list[i][j] != ' ':
                    temp_list[i][j] = chr(ord(temp_list[i][j]) + 1)
                    temp_list[i] = temp_list[i][:j+1] + temp_list[i][j+2:] + [' ']
                    break
        #assign lists back to content
        for i in xrange(4):
            for j in xrange(4):
                self.content[index_list[i][j]] = temp_list[i][j]
    
    def do_slide(self, slide):        
        curr_view = list(self.content)
        self.do_punch(index_lists[slide])
        self.do_merge(index_lists[slide])        
        the_same = True
        if curr_view != self.content :
            the_same = False
        if not the_same:
            self.do_popup()
        return the_same
    
    def is_game_over(self):
        #backup
        backup_view_contant = list(self.content)
        if self.do_slide(curses.KEY_UP) and self.do_slide(curses.KEY_DOWN) and self.do_slide(curses.KEY_LEFT) and self.do_slide(curses.KEY_RIGHT):
            stdscr.addstr(11,0,'game over !!',curses.color_pair(1))
        self.content = list(backup_view_contant)
            
    def disp_init(self):
        curses.start_color()
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.noecho()
        curses.cbreak()

    def do_quit(self,key):
        curses.echo()
        curses.nocbreak()
        curses.endwin()
        exit()

    def do_restart(self,key=0):
        self.__init__()
        #pop twice
        self.do_popup()
        self.do_popup()
        stdscr.clear()
        self.do_refresh()

    def do_refresh(self):
        global screen_mask
        for i in xrange(len(chairs)):
            self.set_list_char(screen_mask, chairs[i], self.content[i])
        stdscr.addstr(0,0,''.join(screen_mask),curses.color_pair(1))
        stdscr.addstr(10,0,'up: i down: k left: j right: l restart: r quit: q',curses.color_pair(1))
 
    key_lists = { curses.KEY_UP:do_slide, curses.KEY_DOWN:do_slide, curses.KEY_LEFT:do_slide, \
            curses.KEY_RIGHT:do_slide, ord('r'):do_restart, ord('q'):do_quit}

    def start(self):
        self.disp_init()
        self.do_restart()
        while True:
            #get key
            key = stdscr.getch()
            debug('               ')
            #debug(str(key))
            if not key in self.key_lists.keys():
                continue
            self.key_lists[key](self,key)
            #do refresh
            self.do_refresh()
            self.is_game_over()
         

def main(win):
    game = My_2048();
    game.start()

if __name__ == '__main__':
    curses.wrapper(main) 
