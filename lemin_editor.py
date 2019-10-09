#!/usr/bin/env python3

from lemin_screen import *
from lemin_map import *
from tkinter import filedialog

# editor constants
E_GRID_WIDTH_DEF = 160
E_GRID_HEIGHT_DEF = 90
CURSOR_COLOR = "DarkOrange3"

class lemin_editor:
    def __init__(self, lmap=None):
        if lmap == None:
            lmap = self.new_map()
        # lemin screen
        self.lscr = lemin_screen(lmap, self.redraw,\
        self.move, self.refresh, self.wait)
        self.lscr.init_canvas(self.init_editor_actions)
        self.lscr.win.after(0, self.edit_map)
        # cursor data
        self.cur_x = 0
        self.cur_y = 0
        self.cur = []
        # visual grid
        self.grid = []
        self.init_visual_grid(self.lscr.lmap.rooms)
        # actions
        self.lnk = None # connect or disconnect two rooms
        self.move = None # move a room
        # output
        self.file = None

    def new_map(self):
        lmap = lemin_map()
        lmap.orig_w = E_GRID_WIDTH_DEF
        lmap.orig_h = E_GRID_HEIGHT_DEF
        return lmap

    ## visual grid funcions ##
    def init_visual_grid(self, rooms):
        self.grid.clear()
        self.grid = [[None for j in range(self.lscr.grid.height)]\
                for i in range(self.lscr.grid.width)]
        for r in rooms:
            self.grid[rooms[r].x][rooms[r].y] = r

    def find_room(self, direction):
        if direction == "left":
            x = self.cur_x - 1
            while x > -1:
                if self.grid[x][self.cur_y] != None:
                    return x, self.cur_y
                x -= 1
        elif direction == "right":
            x = self.cur_x + 1
            while x < self.lscr.grid.width:
                if self.grid[x][self.cur_y] != None:
                    return x, self.cur_y
                x += 1
        elif direction == "up":
            y = self.cur_y - 1
            while y > -1:
                if self.grid[self.cur_x][y] != None:
                    return self.cur_x, y
                y -= 1
        elif direction == "down":
            y = self.cur_y + 1
            while y < self.lscr.grid.height:
                if self.grid[self.cur_x][y] != None:
                    return self.cur_x, y
                y += 1
        return -1, -1

    ## event handling of lemin_editor ##
    def init_editor_actions(self):
        self.lscr.win.bind("<Left>", self.left_handler)
        self.lscr.win.bind("<Right>", self.right_handler)
        self.lscr.win.bind("<Up>", self.up_handler)
        self.lscr.win.bind("<Down>", self.down_handler)
        self.lscr.win.bind("<Home>", self.home_handler)
        self.lscr.win.bind("<End>", self.end_handler)
        self.lscr.win.bind("<Prior>", self.prior_handler)
        self.lscr.win.bind("<Next>", self.next_handler)
        self.lscr.win.bind("h", self.h_handler)
        self.lscr.win.bind("l", self.l_handler)
        self.lscr.win.bind("k", self.k_handler)
        self.lscr.win.bind("j", self.j_handler)
        self.lscr.win.bind("s", self.s_handler)
        self.lscr.win.bind("e", self.e_handler)
        self.lscr.win.bind("r", self.r_handler)
        self.lscr.win.bind("c", self.c_handler)
        self.lscr.win.bind("d", self.d_handler)
        self.lscr.win.bind("m", self.m_handler)
        self.lscr.win.bind("p", self.p_handler)
        self.lscr.win.bind("<Control-s>", self.control_s_handler)
        self.lscr.win.bind("<Command-s>", self.control_s_handler)
        self.lscr.win.bind("<Control-S>", self.control_shift_s_handler)
        self.lscr.win.bind("<Command-S>", self.control_shift_s_handler)

    def left_handler(self, event):
        self.lscr.stack.insert(0, self.move_left)

    def right_handler(self, event):
        self.lscr.stack.insert(0, self.move_right)

    def up_handler(self, event):
        self.lscr.stack.insert(0, self.move_up)

    def down_handler(self, event):
        self.lscr.stack.insert(0, self.move_down)

    def home_handler(self, event):
        self.lscr.stack.insert(0, self.move_all_left)

    def end_handler(self, event):
        self.lscr.stack.insert(0, self.move_all_right)

    def prior_handler(self, event):
        self.lscr.stack.insert(0, self.move_all_up)

    def next_handler(self, event):
        self.lscr.stack.insert(0, self.move_all_down)

    def h_handler(self, event):
        self.lscr.stack.insert(0, self.move_to_left_room)

    def l_handler(self, event):
        self.lscr.stack.insert(0, self.move_to_right_room)

    def k_handler(self, event):
        self.lscr.stack.insert(0, self.move_to_up_room)

    def j_handler(self, event):
        self.lscr.stack.insert(0, self.move_to_down_room)

    def s_handler(self, event):
        self.lscr.stack.insert(0, self.put_start)

    def e_handler(self, event):
        self.lscr.stack.insert(0, self.put_end)

    def r_handler(self, event):
        self.lscr.stack.insert(0, self.put_room)

    def c_handler(self, event):
        self.lscr.stack.insert(0, self.connect)

    def d_handler(self, event):
        self.lscr.stack.insert(0, self.delete_room)

    def m_handler(self, event):
        self.lscr.stack.insert(0, self.move_room)

    def p_handler(self, event):
        self.debug()
        
    def control_s_handler(self, event):
        self.lscr.stack.insert(0, self.save_map)

    def control_shift_s_handler(self, event):
        self.lscr.stack.insert(0, self.save_map_as)

    def move_left(self):
        if self.cur_x > 0:
            self.cur_x -= 1
            self.lscr.update = self.lscr.update_update(U_REFRESH)

    def move_right(self):
        if self.cur_x < self.lscr.grid.width - 1:
            self.cur_x += 1
            self.lscr.update = self.lscr.update_update(U_REFRESH)

    def move_up(self):
        if self.cur_y > 0:
            self.cur_y -= 1
            self.lscr.update = self.lscr.update_update(U_REFRESH)

    def move_down(self):
        if self.cur_y < self.lscr.grid.height - 1:
            self.cur_y += 1
            self.lscr.update = self.lscr.update_update(U_REFRESH)

    def move_all_left(self):
        if self.cur_x != 0:
            self.cur_x = 0
            self.lscr.update = self.lscr.update_update(U_REFRESH)

    def move_all_right(self):
        if self.cur_x != self.lscr.grid.width - 1:
            self.cur_x = self.lscr.grid.width - 1
            self.lscr.update = self.lscr.update_update(U_REFRESH)

    def move_all_up(self):
        if self.cur_y != 0:
            self.cur_y = 0
            self.lscr.update = self.lscr.update_update(U_REFRESH)

    def move_all_down(self):
        if self.cur_y != self.lscr.grid.height - 1:
            self.cur_y = self.lscr.grid.height - 1
            self.lscr.update = self.lscr.update_update(U_REFRESH)

    def move_to_left_room(self):
        x, y = self.find_room("left")
        if x != -1 and y != -1:
            self.cur_x = x
            self.cur_y = y
            self.lscr.update = self.lscr.update_update(U_REFRESH)
        else:
            self.move_left()

    def move_to_right_room(self):
        x, y = self.find_room("right")
        if x != -1 and y != -1:
            self.cur_x = x
            self.cur_y = y
            self.lscr.update = self.lscr.update_update(U_REFRESH)
        else:
            self.move_right()

    def move_to_up_room(self):
        x, y = self.find_room("up")
        if x != -1 and y != -1:
            self.cur_x = x
            self.cur_y = y
            self.lscr.update = self.lscr.update_update(U_REFRESH)
        else:
            self.move_up()

    def move_to_down_room(self):
        x, y = self.find_room("down")
        if x != -1 and y != -1:
            self.cur_x = x
            self.cur_y = y
            self.lscr.update = self.lscr.update_update(U_REFRESH)
        else:
            self.move_down()

    def put_start(self):
        r = self.grid[self.cur_x][self.cur_y]
        if r == None:
            r = self.put_room()
        if r != None and "start" not in self.lscr.lmap.rooms[r].attrs:
            self.lscr.lmap.commands["start"](self.lscr.lmap, r, "start")
            self.lscr.update = self.lscr.update_update(U_REDRAW)

    def put_end(self):
        r = self.grid[self.cur_x][self.cur_y]
        if r == None:
            r = self.put_room()
        if r != None and "end" not in self.lscr.lmap.rooms[r].attrs:
            self.lscr.lmap.commands["end"](self.lscr.lmap, r, "end")
            self.lscr.update = self.lscr.update_update(U_REDRAW)
    
    def put_room(self):
        if self.grid[self.cur_x][self.cur_y] != None:
            return None
        if self.lscr.grid.orig_w * self.lscr.grid.orig_h <\
                self.lscr.roomn + len(self.lscr.lmap.unused_rooms) + 1:
            return None # TODO: resize the original grid in this case
        name = self.lscr.lmap.generate_room_name(5)
        self.grid[self.cur_x][self.cur_y] = name
        self.lscr.lmap.rooms[name] = room()
        self.lscr.lmap.rooms[name].x = self.cur_x
        self.lscr.lmap.rooms[name].y = self.cur_y
        self.lscr.roomn = len(self.lscr.lmap.rooms)
        self.lscr.lmap.size += 1
        self.lscr.grid.place_on_orig_grid(name, self.cur_x,\
        self.cur_y, self.lscr.lmap)
        self.lscr.grid.get_min(self.lscr.screen_width,\
                self.lscr.screen_height, self.lscr.roomn)
        if self.lnk != None:
            self.connect()
        self.lscr.update = self.lscr.update_update(U_REDRAW)
        return name

    def connect(self):
        r = self.grid[self.cur_x][self.cur_y]
        if r == None:
            return
        elif self.lnk == None or self.lnk not in self.lscr.lmap.rooms:
            self.lnk = r
            return
        name = link_name(r, self.lnk)
        if name in self.lscr.lmap.links:
            self.lscr.can.delete(self.lscr.lmap.links.pop(name).shape)
            self.lscr.lmap.rooms[r].links.remove(self.lnk)
            self.lscr.lmap.rooms[self.lnk].links.remove(r)
        else:
            self.lscr.lmap.links[name] = link()
            self.lscr.lmap.rooms[r].links.append(self.lnk)
            self.lscr.lmap.rooms[self.lnk].links.append(r)
        self.lnk = None
        self.lscr.update = self.lscr.update_update(U_REDRAW)

    def delete_room(self):
        r = self.grid[self.cur_x][self.cur_y]
        if r == None:
            return
        for l in self.lscr.lmap.rooms[r].links:
            self.lscr.lmap.rooms[l].links.remove(r)
            name = link_name(r, l)
            self.lscr.can.delete(self.lscr.lmap.links.pop(name).shape)
        if r == self.lscr.lmap.start:
            self.lscr.lmap.start = ""
        if r == self.lscr.lmap.end:
            self.lscr.lmap.end = ""
        self.lscr.can.delete(self.lscr.lmap.rooms.pop(r).shape)
        self.lscr.lmap.size -= 1
        self.lscr.roomn = len(self.lscr.lmap.rooms)
        self.lscr.grid.get_min(self.lscr.screen_width,\
                self.lscr.screen_height, self.lscr.roomn)
        self.grid[self.cur_x][self.cur_y] = None
        self.lscr.update = self.lscr.update_update(U_REDRAW)

    def move_room(self):
        r = self.grid[self.cur_x][self.cur_y]
        if r == None:
            if self.move != None:
                self.grid[self.cur_x][self.cur_y] = self.move
                self.lscr.lmap.rooms[self.move].x = self.cur_x
                self.lscr.lmap.rooms[self.move].y = self.cur_y
                self.lscr.grid.place_on_orig_grid(self.move, self.cur_x,\
                self.cur_y, self.lscr.lmap)
                self.move = None
                self.lscr.update = self.lscr.update_update(U_REDRAW)
        elif self.move == None:
            self.move = r

    def debug(self):
        print()
        limit_line = "\u001B[31m"
        for i in range(self.lscr.grid.width + 2):
            limit_line += "#"
        limit_line += "\u001B[0m"
        print(limit_line)
        for j in range(self.lscr.grid.height):
            line = "\u001B[31m#\u001B[0m"
            for i in range(self.lscr.grid.width):
                line += " " if self.grid[i][j] == None else "#"
            print(line + "\u001B[31m#\u001B[0m")
        print(limit_line)

    def save_map(self):
        if self.file == None:
            self.save_map_as()
        else:
            self.lscr.lmap.write_to_file(self.file)
    
    def save_map_as(self):
        self.file = filedialog.asksaveasfilename(initialdir = "~", title = "Save map")
        if self.file != None and len(self.file) > 0:
            self.lscr.lmap.write_to_file(self.file)

    ## drawing functions specific to lemin_editor ##
    def draw_cursor(self):
        self.delete_cursor()
        if self.cur_x >= self.lscr.grid.width\
        or self.cur_y >= self.lscr.grid.height:
            self.cur_x = 0
            self.cur_y = 0
        self.draw_cursor_lines()

    def delete_cursor(self):
        for bar in self.cur:
            self.lscr.can.delete(bar)
        self.cur.clear()

    def cursor_coords(self, g_x, g_y):
        x, y = self.lscr.grid_to_graphical(g_x, g_y)
        return x - (self.lscr.side / 2), y - (self.lscr.side / 2),\
        x + (self.lscr.side / 2), y + (self.lscr.side / 2) 

    def draw_cursor_lines(self):
        x1, y1, x2, y2 = self.cursor_coords(self.cur_x, self.cur_y)
        x = x1 + 5
        while x < x2:
            bar = self.lscr.can.create_line(x, y1, x, y2, fill=CURSOR_COLOR)
            self.cur.append(bar)
            x += 5
        y = y1 + 5
        while y < y2:
            bar = self.lscr.can.create_line(x1, y, x2, y, fill=CURSOR_COLOR)
            self.cur.append(bar)
            y += 5

    def move_cursor(self):
        i = 0
        x1, y1, x2, y2 = self.cursor_coords(self.cur_x, self.cur_y)
        x = x1 + 5
        while x < x2:
            self.lscr.can.coords(self.cur[i], x, y1, x, y2)
            x += 5
            i += 1
        y = y1 + 5
        while y < y2:
            self.lscr.can.coords(self.cur[i], x1, y, x2, y)
            y += 5
            i += 1

    ## update_screen functions ##
    def redraw(self):
        self.lscr.get_side_size()
        self.lscr.draw_map()
        self.draw_cursor()
        self.init_visual_grid(self.lscr.lmap.rooms)
    
    def move(self):
        pass

    def refresh(self):
        self.move_cursor() # TODO: maybe move to move (lol) and use refresh for something else

    def wait(self):
        pass
    
    ## main loop function ##
    def edit_map(self):
        self.lscr.async_actions()
        if self.lscr.win == None:
            return
        self.lscr.update_screen()
        self.lscr.win.after(1, self.edit_map)

def edit_lemin_map(lmap):    
   e = lemin_editor(lmap) 
   e.lscr.win.mainloop()
   return e.file # for storing the file in the menu's combobox
