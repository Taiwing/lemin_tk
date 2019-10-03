#!/usr/bin/env python3

from lemin_screen import *

# graphical constants
G_FRAMEC_MIN = 10
G_FRAMEC_MAX = 500
G_FRAMEC_DEF = 100
G_FRAMEC_STEP = 10 # increment or decrement speed by this value
G_DELAY_DEF = 300 # wait time at each room
ANT_COLOR = "red"

class lemin_player:
    def __init__(self, lmap, game):
        # lemin screen
        self.lscr = lemin_screen(lmap, self.redraw,\
        self.move, self.refresh, self.wait)
        tag_used_rooms(game, lmap.rooms)
        self.lscr.init_canvas(self.init_player_actions)
        self.lscr.win.after(0, self.play_game)
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

    ## event handling of lemin_player ##
    def init_player_actions(self):
        self.lscr.win.bind("<space>", self.space_handler)
        self.lscr.win.bind("<Left>", self.left_handler)
        self.lscr.win.bind("<Right>", self.right_handler)
        self.lscr.win.bind("<Up>", self.up_handler)
        self.lscr.win.bind("<Down>", self.down_handler)
        self.lscr.win.bind("r", self.r_handler)
        self.lscr.win.bind("e", self.e_handler)
        self.lscr.win.bind("d", self.d_handler)
    
    def space_handler(self, event):
        self.lscr.stack.insert(0, self.play_pause)

    def left_handler(self, event):
        self.lscr.stack.insert(0, self.back_one_turn)

    def right_handler(self, event):
        self.lscr.stack.insert(0, self.forward_one_turn)

    def up_handler(self, event):
        self.lscr.stack.insert(0, self.speed_up)

    def down_handler(self, event):
        self.lscr.stack.insert(0, self.speed_down)

    def r_handler(self, event):
        self.lscr.stack.insert(0, self.reset)

    def e_handler(self, event):
        self.lscr.stack.insert(0, self.go_to_end)

    def d_handler(self, event):
        self.debug()
    
    def play_pause(self):
        self.play = True if self.play == False else False

    def back_one_turn(self):
        if self.step > 0:
            self.step = 0
        elif self.turn > 0:
            self.turn -= 1
        self.play = False
        self.lscr.update = self.lscr.update_update(U_REFRESH)

    def forward_one_turn(self):
        if self.turn < self.game_len - 1:
            self.turn += 1
            self.play = False
            self.step = 0
            self.lscr.update = self.lscr.update_update(U_REFRESH)

    def speed_up(self):
        if self.framec > G_FRAMEC_MIN:
            orig_framec = self.framec
            self.framec -= G_FRAMEC_STEP
            if self.step > 0 and self.turn < self.game_len - 1:
                self.step = (self.step / orig_framec) * self.framec
                self.lscr.update = self.lscr.update_update(U_MOVE)

    def speed_down(self):
        if self.framec < G_FRAMEC_MAX:
            orig_framec = self.framec
            self.framec += G_FRAMEC_STEP
            if self.step > 0:
                self.step = (self.step / orig_framec) * self.framec
                self.lscr.update = self.lscr.update_update(U_MOVE)
    
    def reset(self):
        self.play = False
        self.step = 0
        self.turn = 0
        self.lscr.update = self.lscr.update_update(U_REFRESH)

    def go_to_end(self):
        self.play = False
        self.step = 0
        self.turn = self.game_len - 1
        self.lscr.update = self.lscr.update_update(U_REFRESH)
    
    def debug(self):
        print("self.turn:", self.turn, "/", self.game_len)
        print("self.step:", self.step)
        print("self.play:", "True" if self.play == True else "False")
        print("self.lscr.update:",\
        "U_NONE" if self.lscr.update == U_NONE else\
        "U_WAIT" if self.lscr.update == U_WAIT else\
        "U_REFRESH" if self.lscr.update == U_REFRESH else\
        "U_MOVE" if self.lscr.update == U_MOVE else\
        "U_REDRAW" if self.lscr.update == U_REDRAW else\
        "ERROR")
        print("len(self.lscr.stack)", len(self.lscr.stack))
        print("self.lscr.stack:", self.lscr.stack)
        print("self.lscr.grid.w_comp =", self.lscr.grid.w_comp)
        print("self.lscr.grid.h_comp =", self.lscr.grid.h_comp)

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
            self.lscr.update = U_WAIT

    def wait(self):
        if self.waitc > 0:
            self.waitc -= 1
        else:
            self.lscr.update = U_NONE
    
    ## main loop function ##
    def play_game(self):
        self.lscr.async_actions()
        if self.play == True and self.lscr.update != U_WAIT:
            if self.turn < self.game_len - 1:
                self.step += 1
                if self.step == 1:
                    self.lscr.update = self.lscr.update_update(U_MOVE)
                elif self.step < self.framec:
                    self.lscr.update = self.lscr.update_update(U_REFRESH)
                else:
                    self.step = 0
                    self.turn += 1
                    self.lscr.update = self.lscr.update_update(U_REFRESH)
            else:
                self.play = False
        self.lscr.update_screen()
        self.lscr.win.after(1, self.play_game)

def play_lemin_game(lmap, game):    
   g = lemin_player(lmap, game) 
   g.lscr.win.mainloop()
