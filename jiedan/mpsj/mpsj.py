import pygame
import math

# 初始化Pygame
pygame.init()

# 定义屏幕尺寸
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("密铺设计游戏")

# 颜色定义
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# 形状类定义
class Shape:
    def __init__(self, vertices, color):
        self.vertices = vertices
        self.color = color
        self.selected = False
        self.angle = 0

    def draw(self, screen):
        rotated_vertices = self.get_rotated_vertices()
        pygame.draw.polygon(screen, self.color, rotated_vertices)

    def get_rotated_vertices(self):
        cx, cy = self.get_center()
        rotated_vertices = []
        for x, y in self.vertices:
            x -= cx
            y -= cy
            new_x = x * math.cos(self.angle) - y * math.sin(self.angle)
            new_y = x * math.sin(self.angle) + y * math.cos(self.angle)
            rotated_vertices.append((new_x + cx, new_y + cy))
        return rotated_vertices

    def get_center(self):
        xs, ys = zip(*self.vertices)
        return sum(xs) / len(xs), sum(ys) / len(ys)

    def move(self, dx, dy):
        self.vertices = [(x + dx, y + dy) for x, y in self.vertices]

    def rotate(self, angle):
        self.angle += angle

    def is_point_inside(self, point):
        return pygame.draw.polygon(screen, self.color, self.vertices).collidepoint(point)

def create_regular_polygon(sides, radius, position):
    angle = math.pi * 2 / sides
    vertices = [
        (position[0] + math.cos(i * angle) * radius,
         position[1] + math.sin(i * angle) * radius)
        for i in range(sides)
    ]
    return vertices

# 创建形状列表
shapes = [
    Shape(create_regular_polygon(3, 50, (100, 100)), RED),
    Shape(create_regular_polygon(4, 50, (200, 100)), GREEN),
    Shape(create_regular_polygon(5, 50, (300, 100)), BLUE),
    Shape(create_regular_polygon(6, 50, (400, 100)), BLACK),
]

# 游戏主循环
running = True
selected_shape = None
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # 左键选择形状
                for shape in shapes:
                    if shape.is_point_inside(event.pos):
                        selected_shape = shape
                        shape.selected = True
                        break

            elif event.button == 3:  # 右键删除形状
                for shape in shapes:
                    if shape.is_point_inside(event.pos):
                        shapes.remove(shape)
                        break

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and selected_shape:  # 左键释放
                selected_shape.selected = False
                selected_shape = None

        elif event.type == pygame.KEYDOWN:
            print(event.key)
            print(pygame.K_r)
            print(selected_shape)
            if event.key == pygame.K_r and selected_shape:
                print("R")
                selected_shape.rotate(math.pi / 12)
            elif event.key == pygame.K_1:  # '1'键新增正三角形
                shapes.append(Shape(create_regular_polygon(3, 50, pygame.mouse.get_pos()), RED))
            elif event.key == pygame.K_2:  # '2'键新增正方形
                shapes.append(Shape(create_regular_polygon(4, 50, pygame.mouse.get_pos()), GREEN))
            elif event.key == pygame.K_3:  # '3'键新增正五边形
                shapes.append(Shape(create_regular_polygon(5, 50, pygame.mouse.get_pos()), BLUE))
            elif event.key == pygame.K_4:  # '4'键新增正六边形
                shapes.append(Shape(create_regular_polygon(6, 50, pygame.mouse.get_pos()), BLACK))

    if selected_shape and pygame.mouse.get_pressed()[0]:  # 拖动形状
        mouse_x, mouse_y = pygame.mouse.get_pos()
        cx, cy = selected_shape.get_center()
        selected_shape.move(mouse_x - cx, mouse_y - cy)

    screen.fill(WHITE)  # 清屏
    for shape in shapes:
        shape.draw(screen)

    pygame.display.flip()

pygame.quit()
