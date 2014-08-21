#!/usr/bin/env python
import curses
from random import randint

stdscr = curses.initscr()

def debug(s):
    stdscr.addstr(12,0,str(s))

class My_2048(object):
    
    def __init__(self):
        self.view_contant = ['    ', '    ', '    ', '    ']
        self.sort_list = ['', '', '', '']
    
    def get_view_str(self):
        return ''.join(self.view_contant)
    
    def set_list_char(self, str_list, post, popup_char):
        return str_list[:post] + popup_char + str_list[post + 1:]
    
    def popup_post_char(self, post, popup_char):
        curr_post = 0
        for i in xrange(len(self.view_contant)):
            for j in xrange(len(self.view_contant[0])):
                if ' ' == self.view_contant[i][j]:
                    if curr_post == post:
                        self.view_contant[i] = self.set_list_char(self.view_contant[i], j, popup_char)
                        return
                    curr_post += 1
    
    def do_popup_single(self, blank_count):
        post = randint(0, blank_count - 1)
        popup_char = ['a', 'b'][randint(0, 1)]
        self.popup_post_char(post, popup_char)
    
    def do_popup_twice(self, blank_count):
        self.do_popup_single(blank_count)
        self.do_popup_single(blank_count - 1)
    
    def get_blank_count(self):
        return sum([ i.count(' ') for i in self.view_contant ])
    
    def do_popup(self):
        blank_count = self.get_blank_count()
        self.do_popup_single(blank_count)
    
    def unsparse_line(self, l):
        # print '**************'
        # print self.sort_list[l]
        result = False
        no_blank_line = ''
        for i in self.sort_list[l]:
            if not ' ' == i:
                no_blank_line += i
        if (not no_blank_line == self.sort_list[l][:len(no_blank_line)] and
            not 4 == len(no_blank_line)):
            self.sort_list[l] = no_blank_line + '   '[len(no_blank_line) - 1:]
            result = True
            # print '**************'
            # print self.sort_list[l]
        return result
    
    def do_sort_line(self, l):
        self.unsparse_line(l)
        
        for i in xrange(len(self.sort_list[l]) - 1):
            curr_char = self.sort_list[l][i]
            if not ' ' == curr_char and curr_char == self.sort_list[l][i + 1]:
                self.sort_list[l] = self.set_list_char(self.sort_list[l], i, chr(ord(curr_char) + 1))
                self.sort_list[l] = self.set_list_char(self.sort_list[l], i + 1, ' ')
        
        return self.unsparse_line(l)
    
    def do_sort_list(self):
        go_on_sort = False
        for i in xrange(len(self.sort_list)):
            go_on_sort = self.do_sort_line(i)
        if go_on_sort:
            self.do_sort_list()
    
    def do_slide_up(self):
        self.sort_list = ['', '', '', '']
        for i in xrange(len(self.view_contant)):
            for j in xrange(len(self.view_contant[0])):
                self.sort_list[i] += self.view_contant[j][i]
        self.do_sort_list()
        for i in xrange(len(self.view_contant)):
            for j in xrange(len(self.view_contant[0])):
                self.view_contant[j] = self.set_list_char(self.view_contant[j], i,
                                                          self.sort_list[i][j])
    
    def do_slide_down(self):
        self.sort_list = ['', '', '', '']
        for i in xrange(len(self.view_contant)):
            for j in xrange(len(self.view_contant[0])):
                self.sort_list[i] += self.view_contant[len(self.view_contant[0]) - 1 - j][i]
        self.do_sort_list()
        for i in xrange(len(self.view_contant)):
            for j in xrange(len(self.view_contant[0])):
                self.view_contant[j] = self.set_list_char(self.view_contant[j], i,
                                                          self.sort_list[i][len(self.view_contant[0]) - 1 - j])
    
    def do_slide_left(self):
        self.sort_list = ['', '', '', '']
        for i in xrange(len(self.view_contant)):
            self.sort_list[i] = self.view_contant[i]
        self.do_sort_list()
        for i in xrange(len(self.view_contant)):
            self.view_contant[i] = self.sort_list[i]
    
    def do_slide_right(self):
        self.sort_list = ['', '', '', '']
        for i in xrange(len(self.view_contant)):
            for j in xrange(len(self.view_contant[0])):
                self.sort_list[i] += self.view_contant[i][len(self.view_contant[0]) - 1 - j]
        self.do_sort_list()
        for i in xrange(len(self.view_contant)):
            for j in xrange(len(self.view_contant[0])):
                self.view_contant[i] = self.set_list_char(self.view_contant[i], j,
                                                          self.sort_list[i][len(self.view_contant[0]) - 1 - j])
    
    def do_slide(self, slide):
        
        curr_view = [i for i in self.view_contant]
        if curses.KEY_UP == slide:
            self.do_slide_up()
        elif curses.KEY_DOWN == slide:
            self.do_slide_down()
        elif curses.KEY_LEFT == slide:
            self.do_slide_left()
        elif curses.KEY_RIGHT == slide:
            self.do_slide_right()
        the_same = True
        if curr_view != self.view_contant :
            the_same = False

        if not the_same:
            self.do_popup()
            
        return the_same
    
    def is_game_over(self):
        #backup
        backup_view_contant = list(self.view_contant)
        backup_sort_list = list(self.sort_list)
        over = False
        if self.do_slide(curses.KEY_UP) and self.do_slide(curses.KEY_DOWN) and self.do_slide(curses.KEY_LEFT) and self.do_slide(curses.KEY_RIGHT):
            over = True
        self.view_contant = list(backup_view_contant)
        self.sort_list = list(backup_sort_list)
        return over
    
    def disp_init(self):
        curses.start_color()
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.noecho()
        curses.cbreak()

    def do_quit(self,key):
        curses.echo()
        curses.nocbreak()
        curses.endwin()
        quit()

    def do_restart(self,key=0):
        self.__init__()
        self.do_popup_twice(16)
        stdscr.clear()
        self.do_refresh()

    def do_refresh(self):
        view = ('''
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
        
        post_list = []
        for i in xrange(len(view)):
            if '1' == view[i]:
                post_list.append(i)
        
        view_str = self.get_view_str()
        for i in xrange(len(post_list)):
            view = self.set_list_char(view, post_list[i], view_str[i])
        
        stdscr.addstr(0,0,view,curses.color_pair(1))
        stdscr.addstr(10,0,'up: i down: k left: j right: l restart: r quit: q',curses.color_pair(1))
 
    key_lists = { curses.KEY_UP:do_slide, curses.KEY_DOWN:do_slide, curses.KEY_LEFT:do_slide, \
            curses.KEY_RIGHT:do_slide, ord('r'):do_restart, ord('q'):do_quit}

    def start(self):
        self.disp_init()
        self.do_restart()
        while True:
            #get key
            key = stdscr.getch()
            #stdscr.clear()
            debug('               ')
            debug(str(key))
            if not key in self.key_lists.keys():
                continue
            self.key_lists[key](self,key)
            #do refresh
            self.do_refresh()
            if self.is_game_over():
                stdscr.addstr(11,0,'game over !!',curses.color_pair(1))
         

def main(win):
    a = My_2048();
    a.start()

if __name__ == '__main__':
    curses.wrapper(main) 
