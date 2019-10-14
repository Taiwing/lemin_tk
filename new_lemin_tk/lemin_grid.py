#!/usr/bin/env python3

class lemin_grid:
    def __init__(self, lmap, screen_w, screen_h, G_SIDE_MIN):
        # grid before any modification
        self.orig_w = lmap.orig_w
        self.orig_h = lmap.orig_h
        # current grid
        self.width = self.orig_w
        self.height = self.orig_h
        # smallest grid big enough to fit all rooms
        self.width_min = 2
        self.height_min = 1
        # biggest printable grid
        self.big_width = (screen_w // G_SIDE_MIN) - 2
        self.big_height = (screen_h // G_SIDE_MIN) - 2
        # biggest grid for current map
        self.width_max = self.big_width if self.orig_w > self.big_width\
        else self.orig_w
        self.height_max = self.big_height if self.orig_h > self.big_height\
        else self.orig_h
        # compression values
        self.w_comp = 0
        self.h_comp = 0
        self.w_comp_min = 0
        self.h_comp_min = 0
        # graphical objects
        self.shapes = []

    def get_min(self, screen_w, screen_h, roomn):
        scale = screen_w / screen_h
        roomn = roomn if roomn > 1 else 2 # if the map is empty
        while self.width_min * self.height_min < roomn:
            self.width_min += 1
            self.height_min = int(self.width_min / scale)

    def place_on_orig_grid(self, name, x, y, lmap):
        if self.w_comp == self.w_comp_min and self.h_comp == self.h_comp_min:
            lmap.rooms[name].orig_x = x
            lmap.rooms[name].orig_y = y
        else:
            scale_w = self.orig_w / self.width
            scale_h = self.orig_h / self.height
            new_x = int(x * scale_w) 
            new_y = int(y * scale_h)
            grid = [[0] * self.orig_h for i in range(self.orig_w)] 
            for r in lmap.rooms:
                grid[lmap.rooms[r].orig_x][lmap.rooms[r].orig_y] = 1
            for r in lmap.unused_rooms:
                grid[lmap.unused_rooms[r].orig_x][lmap.unused_rooms[r].orig_y] = 1
            new_x, new_y = self.move_orig_coordinates(new_x, new_y, grid, 0)
            lmap.rooms[name].orig_x = new_x
            lmap.rooms[name].orig_y = new_y

    def move_orig_coordinates(self, s_x, s_y, grid, dist):
        start_x = s_x - dist
        start_y = s_y - dist
        end_x = s_x + dist
        end_y = s_y + dist
        if start_y < 0 and start_x < 0\
        and end_x > self.orig_w - 1\
        and end_y > self.orig_h - 1:
            eprint("error: no place found in grid")
            exit()
        y = max(start_y, 0)
        while y < self.orig_h and y < end_y + 1:
            x = max(start_x, 0)
            while x < self.orig_w and x < end_x + 1:
                on_y = y == start_y or y == end_y
                on_x = x == start_x or x == end_x
                if (on_y or on_x) and grid[x][y] == 0:
                    return x, y
                x = x + 1 if on_y or x == end_x else end_x
            y += 1
        return self.move_orig_coordinates(s_x, s_y, grid, dist + 1)
