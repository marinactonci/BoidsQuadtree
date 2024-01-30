import pygame
import random
from quadtree import QuadTree, Point, Rectangle


screen_size = 800
MARGIN = screen_size * 0.05


class Boid:
    NUM_BOIDS = 800
    DISTANCE_VISIBLE = 20
    DISTANCE_SEPERATION = 8
    MAX_SPEED = 2.0
    COHERENCE_FACTOR  = 0.01
    ALIGNMENT_FACTOR  = 0.05
    SEPARATION_FACTOR = 0.1
    SEPARATION_MULTIPLIER = 8
    
    def __init__(self, color=(0,255,255)):
        self.position = pygame.math.Vector2(random.randint(0, screen_size), random.randint(0, screen_size))
        self.velocity = pygame.math.Vector2(random.uniform(-Boid.MAX_SPEED, Boid.MAX_SPEED), random.uniform(-Boid.MAX_SPEED, Boid.MAX_SPEED))
        self.velocity_buffer = self.velocity.copy()
        self.color = color
    
    def cohere(self, boids):
        if not boids:
            return

        center_of_mass = pygame.math.Vector2(0, 0)
        for other in boids:
            center_of_mass += other.position

        center_of_mass /= len(boids)

        direction_to_center = center_of_mass - self.position
        self.velocity_buffer += direction_to_center * Boid.COHERENCE_FACTOR

    def align(self, boids):
        if not boids:
            return

        average_velocity = pygame.math.Vector2(0, 0)
        for other in boids:
            average_velocity += other.velocity

        average_velocity /= len(boids)

        adjustment = average_velocity - self.velocity
        self.velocity_buffer += adjustment * Boid.ALIGNMENT_FACTOR

    def seperate(self, boids):
        if not boids:
            return

        move_away = pygame.math.Vector2(0, 0)
        for other in boids:
            distance = self.position.distance_to(other.position)
            if distance < Boid.DISTANCE_SEPERATION and distance > 0:
                move_away += (self.position - other.position)  / distance

        self.velocity_buffer += Boid.SEPARATION_MULTIPLIER * (move_away * Boid.SEPARATION_FACTOR)
    
    def keep_in_bounds(self):
        TURN_FACTOR = 0.1
        turn = Boid.MAX_SPEED * TURN_FACTOR
        if self.position.x < MARGIN:
            self.velocity_buffer.x += turn
        if self.position.x > screen_size - MARGIN:
            self.velocity_buffer.x -= turn
        if self.position.y < MARGIN:
            self.velocity_buffer.y += turn
        if self.position.y > screen_size - MARGIN:
            self.velocity_buffer.y -= turn
    
    def update_position(self):
        if self.velocity_buffer.length() > Boid.MAX_SPEED:
            self.velocity_buffer *= 0.9
        self.velocity = self.velocity_buffer.copy()
        self.position += self.velocity


def closest_boids(boid, dist, boids):
    return [b for b in boids if b.position.distance_to(boid.position) <= dist and b != boid]


def main():
    global screen_size, screen_size
    pygame.init()
    screen = pygame.display.set_mode((screen_size, screen_size))
    
    color_range = {"a": 50, "b": 255}
    boids = [Boid((random.randint(**color_range),
                   random.randint(**color_range),
                   random.randint(**color_range))) for _ in range(Boid.NUM_BOIDS)]
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return

        # background color
        screen.fill((0,0,0))
        
        # QuadTree root node
        qtree = QuadTree(Rectangle(screen_size/2, screen_size/2, screen_size/2, screen_size/2))
        # Inserting all boids (as points) into the quad tree
        for boid in boids:
            qtree.insert(Point(boid))

        for boid in boids:
            rect_range = Rectangle(boid.position.x, boid.position.y, Boid.DISTANCE_VISIBLE/2, Boid.DISTANCE_VISIBLE/2)
            # Retrieve only the boids located within quadrants that intersect with the specified rect_range
            inrange_boids = qtree.query(rect_range)
            
            #### YOUR CODE HERE (copy from boids.py) ####
            # use `inrange_boids` instead of `boids`

            boid.cohere(inrange_boids)
            boid.align(inrange_boids)
            boid.seperate(inrange_boids)
            
            # Each boid flies towards the the other boids. But they don't just immediately fly directly at each other. They gradually steer towards each other.
            # Each boid tries to match the velocity (speed and direction) of the other boids around it.
            # Each boid tries to avoid running into the other boids. If it gets too close to another boid it will steer away from it.
            
            #### END OF YOUR CODE ####
            
            # Keep within window bounds
            boid.keep_in_bounds()
            # Update the position based on the current velocity.
            boid.update_position()
            # Draw on screen
            pygame.draw.circle(screen, boid.color, (int(boid.position.x), int(boid.position.y)), 2)
            
        # Draw QuadTree on screen
        qtree.draw(screen)
        
        # Draw rect_range around the zeroth boid
        #rect_range = Rectangle(boids[0].position.x, boids[0].position.y, Boid.DISTANCE_VISIBLE/2, Boid.DISTANCE_VISIBLE/2)
        #rect = pygame.Rect(rect_range.x - rect_range.hw, rect_range.y - rect_range.hh, rect_range.hw * 2, rect_range.hh * 2)
        #pygame.draw.rect(screen, (255,255,100), rect, 4)

        pygame.display.update()


main()
