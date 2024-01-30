import pygame


class Point:
    def __init__(self, boid):
        self.x = boid.position.x
        self.y = boid.position.y
        self.boid = boid


class Rectangle:
    def __init__(self, x, y, hw, hh):
        self.x = x  # center of the rectangle on x-axis
        self.y = y  # center of the rectangle on y-axis
        self.hw = hw  # half width
        self.hh = hh  # half height
    
    def contains(self, point):
        does_contain = \
            point.x >= self.x - self.hw and \
            point.x < self.x + self.hw and \
            point.y >= self.y - self.hh and \
            point.y < self.y + self.hh
        return does_contain
    
    def intersects(self, rect_range):
        doesnt_intersect = \
            rect_range.x - rect_range.hw > self.x + self.hw or \
            rect_range.x + rect_range.hw < self.x - self.hw or \
            rect_range.y - rect_range.hh > self.y + self.hh or \
            rect_range.y + rect_range.hh < self.y - self.hh
        return not doesnt_intersect


class QuadTree:
    CAPACITY = 16
    
    def __init__(self, rectangle):
        self.rectangle = rectangle
        self.points = []
        self.divided = False
        self.subqtrees = {}  # keys: "northwest", "northeast", "southwest", "southeast" -> values: QuadTree objects
    
    #### subdivide():
    # Instantiate northwest, northeast, southwest, and southeast sub-rectangles using `Rectangle()`,
    #   pass them to `QuadTree()` to instantiate the four sub-quadtrees that you will store in `self.subqtrees`
    #     with keys: "northwest", "northeast", "southwest", "southeast".
    def subdivide(self):
        hw = self.rectangle.hw / 2
        hh = self.rectangle.hh / 2
        x = self.rectangle.x
        y = self.rectangle.y

        self.subqtrees["northwest"] = QuadTree(Rectangle(x - hw, y - hh, hw, hh))
        self.subqtrees["northeast"] = QuadTree(Rectangle(x + hw, y - hh, hw, hh))
        self.subqtrees["southwest"] = QuadTree(Rectangle(x - hw, y + hh, hw, hh))
        self.subqtrees["southeast"] = QuadTree(Rectangle(x + hw, y + hh, hw, hh))
        self.divided = True
    
    #### insert(point):
    # If this node didn't reach `QuadTree.CAPACITY` and it isn't already subdivided:
    #   append the `point` to this node. (this part is already implemented)
    # Else:
    #   If this node is not subdivided:
    #     subdivide it and move all points from the current node into the subnodes with `insert()`
    #   Insert the `point` into the subnode that contains it
    #     help: `self.subqtrees["northwest"].rectangle.contains(point)`
    #           `self.subqtrees["northwest"].insert(point)`
    def insert(self, point):
        if len(self.points) < QuadTree.CAPACITY and not self.divided:
            self.points.append(point)
        else:
            if not self.divided:
                self.subdivide()
                for existing_point in self.points:
                    self.insert(existing_point)
                self.points = []
            for subqt in self.subqtrees.values():
                if subqt.rectangle.contains(point):
                    subqt.insert(point)
    
    #### query(rect_range):
    # Recursiveley traverse nodes that intersect the `rect_range`
    #   help: `self.rectangle.intersects(rect_range)`
    #         and do that recursevely for each subqtree
    #         and append all boids in those nodes to the list `found`
    #           help: `found.append(point.boid)`
    def query(self, rect_range):
        found = []  # list of boids to be returned
        if self.rectangle.intersects(rect_range):
            found.extend([point.boid for point in self.points])

            if self.divided:
                found.extend(self.subqtrees["northwest"].query(rect_range))
                found.extend(self.subqtrees["northeast"].query(rect_range))
                found.extend(self.subqtrees["southwest"].query(rect_range))
                found.extend(self.subqtrees["southeast"].query(rect_range))
        return found
    
    def draw(self, screen):
        rect = pygame.Rect(self.rectangle.x - self.rectangle.hw, self.rectangle.y - self.rectangle.hh, self.rectangle.hw * 2, self.rectangle.hh * 2)
        pygame.draw.rect(screen, (100,100,0), rect, 1)
        if self.divided:
            self.subqtrees["northwest"].draw(screen)
            self.subqtrees["northeast"].draw(screen)
            self.subqtrees["southwest"].draw(screen)
            self.subqtrees["southeast"].draw(screen)