#!/usr/bin/env python3

from lemin_screen import *
from lemin_help import *

# graphical constants
G_FRAMEC_MIN = 10
G_FRAMEC_MAX = 500
G_FRAMEC_DEF = 100
G_FRAMEC_STEP = 10 # increment or decrement speed by this value
G_DELAY_DEF = 300 # wait time at each room
ANT_COLOR = "red"

## event handling of lemin_player ##
class player_events:
    def __init__(self, player, lwin):
        self.player = player
        self.init_player_actions(lwin)

    def init_player_actions(self, lwin):
        lwin.win.bind("<space>", self.space_handler)
        lwin.win.bind("<Left>", self.left_handler)
        lwin.win.bind("<Right>", self.right_handler)
        lwin.win.bind("<Up>", self.up_handler)
        lwin.win.bind("<Down>", self.down_handler)
        lwin.win.bind("r", self.r_handler)
        lwin.win.bind("e", self.e_handler)
        lwin.win.bind("d", self.d_handler)
        lwin.win.bind("<F1>", self.f1_handler)

    def unbind(self, lwin):
        lwin.win.unbind("<space>")
        lwin.win.unbind("<Left>")
        lwin.win.unbind("<Right>")
        lwin.win.unbind("<Up>")
        lwin.win.unbind("<Down>")
        lwin.win.unbind("r")
        lwin.win.unbind("e")
        lwin.win.unbind("d")
        lwin.win.unbind("<F1>")
    
    def space_handler(self, event):
        self.player.lscr.lwin.stack.insert(0, self.player.play_pause)

    def left_handler(self, event):
        self.player.lscr.lwin.stack.insert(0, self.player.back_one_turn)

    def right_handler(self, event):
        self.player.lscr.lwin.stack.insert(0, self.player.forward_one_turn)

    def up_handler(self, event):
        self.player.lscr.lwin.stack.insert(0, self.player.speed_up)

    def down_handler(self, event):
        self.player.lscr.lwin.stack.insert(0, self.player.speed_down)

    def r_handler(self, event):
        self.player.lscr.lwin.stack.insert(0, self.player.reset)

    def e_handler(self, event):
        self.player.lscr.lwin.stack.insert(0, self.player.go_to_end)

    def d_handler(self, event):
        self.player.debug()

    def f1_handler(self, event):
        self.player.lscr.lwin.stack.insert(0, self.player.show_help)

class lemin_player:
    def __init__(self, lwin, lmap, game):
        # lemin screen
        self.lscr = lemin_screen(lwin, lmap, self.redraw,\
        self.move, self.refresh, self.wait)
        tag_used_rooms(game, lmap.rooms)
        self.lscr.init_canvas()
        # events and main loop
        self.lscr.init_events()
        self.events = player_events(self, lwin)
        self.lscr.lwin.win.after(0, self.mainf)
        # graphical objects
        self.ants = []
        # movements
        self.framec = G_FRAMEC_DEF # number of frames by ant movement (speed)
        self.steps = [] # last room coordinates and x,y increments for each ant
        self.step = 0
        self.waitc = 0
        # game data
        self.game = game
        self.game_len = len(self.game)
        self.play = False
        self.turn = 0
        # output
        self.file = None # will not be used but is needed in lemin_data
    
    def play_pause(self):
        self.play = True if self.play == False else False

    def back_one_turn(self):
        if self.step > 0:
            self.step = 0
        elif self.turn > 0:
            self.turn -= 1
        self.play = False
        self.lscr.lwin.update = self.lscr.lwin.update_update(U_REFRESH)

    def forward_one_turn(self):
        if self.turn < self.game_len - 1:
            self.turn += 1
            self.play = False
            self.step = 0
            self.lscr.lwin.update = self.lscr.lwin.update_update(U_REFRESH)

    def speed_up(self):
        if self.framec > G_FRAMEC_MIN:
            orig_framec = self.framec
            self.framec -= G_FRAMEC_STEP
            if self.step > 0 and self.turn < self.game_len - 1:
                self.step = (self.step / orig_framec) * self.framec
                self.lscr.lwin.update = self.lscr.lwin.update_update(U_MOVE)

    def speed_down(self):
        if self.framec < G_FRAMEC_MAX:
            orig_framec = self.framec
            self.framec += G_FRAMEC_STEP
            if self.step > 0:
                self.step = (self.step / orig_framec) * self.framec
                self.lscr.lwin.update = self.lscr.lwin.update_update(U_MOVE)
    
    def reset(self):
        self.play = False
        self.step = 0
        self.turn = 0
        self.lscr.lwin.update = self.lscr.lwin.update_update(U_REFRESH)

    def go_to_end(self):
        self.play = False
        self.step = 0
        self.turn = self.game_len - 1
        self.lscr.lwin.update = self.lscr.lwin.update_update(U_REFRESH)
    
    def debug(self):
        print("self.turn:", self.turn, "/", self.game_len)
        print("self.step:", self.step)
        print("self.play:", "True" if self.play == True else "False")
        print("self.lscr.lwin.update:",\
        "U_NONE" if self.lscr.lwin.update == U_NONE else\
        "U_WAIT" if self.lscr.lwin.update == U_WAIT else\
        "U_REFRESH" if self.lscr.lwin.update == U_REFRESH else\
        "U_MOVE" if self.lscr.lwin.update == U_MOVE else\
        "U_REDRAW" if self.lscr.lwin.update == U_REDRAW else\
        "ERROR")
        print("len(self.lscr.lwin.stack)", len(self.lscr.lwin.stack))
        print("self.lscr.lwin.stack:", self.lscr.lwin.stack)
        print("self.lscr.grid.w_comp =", self.lscr.grid.w_comp)
        print("self.lscr.grid.h_comp =", self.lscr.grid.h_comp)

    def show_help(self):
        top = Toplevel()
        label1 = Label(top, text="Lemin_tk player commands:")
        label1.grid(row=0, column=0, columnspan=2)
        label2 = Label(top, text=PLAYER_COMMANDS, justify=LEFT)
        label2.grid(row=1, column=0)
        label3 = Label(top, text=PLAYER_DESC, justify=RIGHT)
        label3.grid(row=1, column=1)
        top.resizable(width=False, height=False)

    ## drawing functions specific to lemin_player ##
    def ant_coords(self, g_x, g_y):
        x, y = self.lscr.grid_to_graphical(g_x, g_y)
        return x - (self.lscr.side / 8), y - (self.lscr.side / 8),\
        x + (self.lscr.side / 8), y + (self.lscr.side / 8) 

    def delete_ants(self):
        for ant in self.ants:
            self.lscr.can.delete(ant)
        self.ants.clear()
    
    def draw_ants(self):
        self.delete_ants()
        for i in range(self.lscr.lmap.antn):
            r = self.game[self.turn][i]
            x1, y1, x2, y2 = self.ant_coords(self.lscr.lmap.rooms[r].x,\
            self.lscr.lmap.rooms[r].y)
            ant = self.lscr.can.create_oval(x1, y1, x2, y2, fill=ANT_COLOR)
            self.ants.append(ant)
        self.lscr.can.pack()
    
    def get_steps(self):
        self.steps.clear()
        for i in range(self.lscr.lmap.antn):
            # get the coordinates of the target room
            xy = self.ant_coords(\
            self.lscr.lmap.rooms[self.game[self.turn + 1][i]].x,\
            self.lscr.lmap.rooms[self.game[self.turn + 1][i]].y)
            # get the coordinates of the current room
            cur = self.ant_coords(\
            self.lscr.lmap.rooms[self.game[self.turn][i]].x,\
            self.lscr.lmap.rooms[self.game[self.turn][i]].y)
            # get increments
            ix = (xy[0] - cur[0]) / self.framec
            iy = (xy[1] - cur[1]) / self.framec
            self.steps.append([cur[0], cur[1], cur[2], cur[3], ix, iy])

    def draw_step(self):
        for i in range(self.lscr.lmap.antn):
            # move ant one frame toward the next node
            self.lscr.can.coords(self.ants[i],\
            self.steps[i][0] + (self.steps[i][4] * self.step),\
            self.steps[i][1] + (self.steps[i][5] * self.step),\
            self.steps[i][2] + (self.steps[i][4] * self.step),\
            self.steps[i][3] + (self.steps[i][5] * self.step))

    def fix(self):
        for i in range(self.lscr.lmap.antn):
            # fix ant precisely on the node
            xy = self.ant_coords(\
            self.lscr.lmap.rooms[self.game[self.turn][i]].x,\
            self.lscr.lmap.rooms[self.game[self.turn][i]].y)
            self.lscr.can.coords(self.ants[i], xy[0], xy[1], xy[2], xy[3])

    ## update_screen functions ##
    def redraw(self):
        self.lscr.get_side_size()
        self.lscr.draw_map()
        self.draw_ants()
        if self.step > 0:
            self.get_steps()
            self.draw_step()
    
    def move(self):
        if self.step > 0:
            self.get_steps()
            self.draw_step()
        else:
            self.fix()

    def refresh(self):
        if self.step > 0:
            self.draw_step()
        else:
            self.fix()
            self.waitc = G_DELAY_DEF
            self.lscr.lwin.update = U_WAIT

    def wait(self):
        if self.waitc > 0:
            self.waitc -= 1
        else:
            self.lscr.lwin.update = U_NONE
    
    ## main loop function ##
    def mainf(self):
        self.lscr.lwin.async_actions()
        if self.play == True and self.lscr.lwin.update != U_WAIT:
            if self.turn < self.game_len - 1:
                self.step += 1
                if self.step == 1:
                    self.lscr.lwin.update = self.lscr.lwin.update_update(U_MOVE)
                elif self.step < self.framec:
                    self.lscr.lwin.update = self.lscr.lwin.update_update(U_REFRESH)
                else:
                    self.step = 0
                    self.turn += 1
                    self.lscr.lwin.update = self.lscr.lwin.update_update(U_REFRESH)
            else:
                self.play = False
        if self.lscr.lwin.quit == True:
            self.lscr.lwin.quit = False
        elif self.lscr.lwin.valid_drawf():
            self.lscr.lwin.update_screen()
            self.lscr.lwin.win.after(1, self.mainf)
