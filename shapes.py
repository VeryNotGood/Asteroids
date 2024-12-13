import pygame


class Shape(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(getattr(self, "containers", None))

    def draw(self, screen):
        raise NotImplementedError("Only subclasses implement this method")

    def update(self, dt):
        raise NotImplementedError("Only subclasses implement this method")


class CircleShape(Shape):
    def __init__(self, x, y, radius):
        super().__init__()
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = radius

    def draw(self, screen):
        pass

    def update(self, dt):
        pass

    def collisioncheck(self, other):
        if isinstance(other, CircleShape):
            dist = pygame.math.Vector2.distance_to(self.position, other.position)
            if dist <= self.radius + other.radius:
                return True

        elif isinstance(other, TriangleShape):
            return other.triangle_circle_collision(self)

        return False


class TriangleShape(Shape):
    def __init__(self, x, y, radius):
        super().__init__()
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = radius

    def draw(self, screen):
        pass

    def update(self, dt):
        pass

    def triangle_circle_collision(self, circle):
        print("Player position: ", self.position)
        print(circle.position)
        if self.is_point_in_triangle(circle.position):
            return True

        for i in range(3):
            start = self.vertices[i]
            end = self.vertices[(i + 1) % 3]
            if self.distance_to_edge(circle.position, start, end) <= circle.radius:
                return True

        return False

    def is_point_in_triangle(self, point):
        v1, v2, v3 = self.vertices
        d1 = self.sign(point, v1, v2)
        d2 = self.sign(point, v2, v3)
        d3 = self.sign(point, v3, v1)

        has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
        has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)

        return not (has_neg and has_pos)

    def sign(self, p1, p2, p3):
        # Calculate the cross product of vectors (p3 - p2) and (p1 - p2)
        return (p1.x - p3.x) * (p2.y - p3.y) - (p2.x - p3.x) * (p1.y - p3.y)

    def distance_to_edge(self, point, edge_start, edge_end):
        edge = edge_end - edge_start
        point_to_start = point - edge_start

        t = max(0, min(1, point_to_start.dot(edge) / edge.length_squared()))
        projection = edge_start + t * edge

        return (point - projection).length()
