import pyxel
import math
import random

class Clock:
    def __init__(self, x, y, c):


        self.x = x
        self.y = y
        self.c = c

        self.sec = 0
        self.min = 0

    def update(self):
        self.sec = pyxel.frame_count // 30
        self.min = self.sec // 60

    def draw(self):
        pyxel.text(self.x, self.y, "Time: %02d:%02d" % (self.min, self.sec % 60), self.c)

class App:
    def __init__(self):
        pyxel.init(250, 250)
        pyxel.load("my_resource.pyxres")
        
        self.frag = 1

        self.icon_x = 115
        self.icon_y = 220
        self.icon_speed = 0.5
        self.is_space_pressed = False
        self.icon_angle = math.pi / 4  # 45-degree angle
        self.clock = Clock(0, 0, 0)
        self.circles = self.initialize_circles()

    def run(self):
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.is_space_pressed = True

        if self.is_space_pressed:
            # Check if the icon is over any circle
            for circle in self.circles:
                x, y, radius, _ = circle
                if (
                    self.icon_x + 23 >= x - radius
                    and self.icon_x <= x + radius
                    and self.icon_y + 35 >= y - radius
                    and self.icon_y <= y + radius
                ):
                    self.icon_speed = 1.1  # Increase speed if over a circle
                    break
                else:
                    self.icon_speed = 0.5  # Reset speed if not over any circle

            # Update icon position based on both X and Y components of the angle
            if pyxel.btnp(pyxel.KEY_SPACE):
                self.frag+=1

            if  self.frag % 2 ==0:
                self.icon_x += self.icon_speed * math.cos(self.icon_angle) 
                self.icon_y -= self.icon_speed * math.sin(self.icon_angle)
            else:
                self.icon_x -= self.icon_speed * math.cos(self.icon_angle)
                self.icon_y -= self.icon_speed * math.sin(self.icon_angle)

            # Wrap icon around the screen if it goes off the edges
            if self.icon_x < -23:
                self.icon_x = pyxel.width
            elif self.icon_x > pyxel.width:
                self.icon_x = -23

            if self.icon_y < -35:
                self.icon_y = 220
                self.is_space_pressed = False

                # Randomly generate new circles
                self.circles = self.initialize_circles()

        self.clock.update()

    def draw(self):
        pyxel.cls(12)

        # Draw circles
        for circle in self.circles:
            x, y, radius, color = circle
            pyxel.circ(x, y, radius, color)

        # Draw icon
        pyxel.blt(self.icon_x, self.icon_y, 0, 0, 0, 23, 35, 0)

        # Draw goal and start lines
        self.draw_lines()

        self.clock.draw()

    def initialize_circles(self):
        circles = []
        for _ in range(5):
            x = random.randint(0, pyxel.width - 1)
            y = random.choice(range(20, 210))
            radius = random.randint(8, 30)
            color = pyxel.COLOR_NAVY
            circles.append((x, y, radius, color))
        return circles

    def draw_lines(self):
        pyxel.text(20, 10, "GOAL.", 7)
        pyxel.text(20, 210, "START.", 7)
        pyxel.line(30, 20, 230, 20, 8)  # Goal line
        start_line_y = 210 + 10
        pyxel.line(30, start_line_y, 230, start_line_y, 8)  # Start line

        # Additional: Draw points on goal and start lines
        pyxel.pset(30, 20, 8)  # Point on the goal line
        pyxel.pset(230, 20, 8)  # Point on the goal line
        pyxel.pset(30, start_line_y, 8)  # Point on the start line
        pyxel.pset(230, start_line_y, 8)  # Point on the start line

App().run()
