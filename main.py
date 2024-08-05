# imports
import sys
import pygame
import ctypes

# increase dots per inch so it looks sharper
ctypes.windll.shcore.SetProcessDpiAwareness(True)

# pygame configuration
pygame.init()
fps = 300
fps_clock = pygame.time.Clock()
width, height = 640, 480
screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
font = pygame.font.SysFont("Arial", 20)

# variables
# buttons will append themself to the list
objects = []
# initial color
draw_color = [0, 0, 0]
# initial brush size
brush_size = 30
brush_size_steps = 3
# drawing area size
canvas_size = [800, 800]


# button class
class Button:
    def __init__(
        self,
        x,
        y,
        width,
        height,
        button_text="Button",
        onclick_function=None,
        one_press=False,
    ):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onclick_function = onclick_function
        self.one_press = one_press
        self.already_pressed = False

        self.fill_colors = {
            "normal": "#ffffff",
            "hover": "#666666",
            "pressed": "#333333",
        }

        self.button_surface = pygame.Surface((self.width, self.height))
        self.button_rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.button_surf = font.render(button_text, True, (20, 20, 20))

        objects.append(self)

    def process(self):
        mouse_pos = pygame.mouse.get_pos()
        self.button_surface.fill(self.fill_colors["normal"])
        if self.button_rect.collidepoint(mouse_pos):
            self.button_surface.fill(self.fill_colors["hover"])
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.button_surface.fill(self.fill_colors["pressed"])
                if self.one_press:
                    self.onclick_function()
                elif not self.already_pressed:
                    self.onclick_function()
                    self.already_pressed = True
            else:
                self.already_pressed = False

        self.button_surface.blit(
            self.button_surf,
            [
                self.button_rect.width / 2 - self.button_surf.get_rect().width / 2,
                self.button_rect.height / 2 - self.button_surf.get_rect().height / 2,
            ],
        )
        screen.blit(self.button_surface, self.button_rect)


# changing color
def change_Color(color):
    global draw_color
    draw_color = color


# brush size
def change_brush_Size(dir):
    global brush_size
    if dir == "greater":
        brush_size += brush_size_steps
    else:
        brush_size -= brush_size_steps


# save the surface to the disk
def save():
    pygame.image.save(canvas, "canvas.png")


# button variables
button_width = 120
button_height = 35

# buttons and their respective functions
buttons = [
    ["Black", lambda: change_Color([0, 0, 0])],
    ["White", lambda: change_Color([255, 255, 255])],
    ["Blue", lambda: change_Color([0, 0, 255])],
    ["Green", lambda: change_Color([0, 255, 0])],
    ["Brush Larger", lambda: change_brush_Size("greater")],
    ["Brush Smaller", lambda: change_brush_Size("smaller")],
    ["Save", save],
]

# making buttons
for index, button_name in enumerate(buttons):
    Button(
        index * (button_width + 10) + 10,
        10,
        button_width,
        button_height,
        button_name[0],
        button_name[1],
    )

# canvas
canvas = pygame.Surface(canvas_size)
canvas.fill((255, 255, 255))

# game loop
while True:
    screen.fill((30, 30, 30))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # drawing buttons
    for object in objects:
        object.process()
    # draw the canvas
    x, y = screen.get_size()
    screen.blit(canvas, [x / 2 - canvas_size[0] / 2, y / 2 - canvas_size[1] / 2])

    # drawing with the mouse
    if pygame.mouse.get_pressed()[0]:
        mx, my = pygame.mouse.get_pos()
        # calculate position on the canvas
        dx = mx - x / 2 + canvas_size[0] / 2
        dy = my - y / 2 + canvas_size[0] / 2
        pygame.draw.circle(canvas, draw_color, [dx, dy], brush_size)
        # Reference Dot
        pygame.draw.circle(
            screen,
            draw_color,
            [100, 100],
            brush_size,
        )
        pygame.display.flip()
        fps_clock.tick(fps)
