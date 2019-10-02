#!/usr/bin/env python3

# For G_FRAMEC_DEF
from lemin_screen import *

class lemin_player:
    def __init__(self, lmap, game):
        # lemin screen
        self.lscr = lemin_screen(lmap, game)
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
