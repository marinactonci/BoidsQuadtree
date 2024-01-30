import pygame
import random


screen_width, screen_height = 800, 600  # 0, 0 for fullscreen
MARGIN = screen_width * 0.1


class Boid:
    NUM_BOIDS = 100
    DISTANCE_VISIBLE = 42
    DISTANCE_SEPERATION = 20
    MAX_SPEED = 0.5
    COHERENCE_FACTOR  = 0.0001
    ALIGNMENT_FACTOR  = 0.008
    SEPARATION_FACTOR = 0.001
    SEPARATION_MULTIPLIER = 16
    
    def __init__(self, color=(0,255,255)):
        self.position = pygame.math.Vector2(random.randint(0, screen_width), random.randint(0, screen_height))
        self.velocity = pygame.math.Vector2(random.uniform(-Boid.MAX_SPEED, Boid.MAX_SPEED), random.uniform(-Boid.MAX_SPEED, Boid.MAX_SPEED))
        self.velocity_buffer = self.velocity.copy()
        self.color = color
    
    # Find the center of mass of the visible boids and slightly adjust velocity (`velocity_buffer`)
        # to point more towards the center of mass.
        # You will need `position` of each boid.
        # Use `Boid.COHERENCE_FACTOR` to control how much each boid "wants" to go towards that center.
    def cohere(self, boids):
        if not boids:
            return

        center_of_mass = pygame.math.Vector2(0, 0)
        for other in boids:
            center_of_mass += other.position

        center_of_mass /= len(boids)

        direction_to_center = center_of_mass - self.position
        self.velocity_buffer += direction_to_center * Boid.COHERENCE_FACTOR
    
    # Find the average velocity (speed and direction) of the visible boids and
        # slightly adjust velocity (`velocity_buffer`) to match.
        # You will need `velocity` of each boid.
        # Use `Boid.ALIGNMENT_FACTOR` to control how much each boid "wants" to go in the same direction and speed as the visible boids.
    def align(self, boids):
        if not boids:
            return

        average_velocity = pygame.math.Vector2(0, 0)
        for other in boids:
            average_velocity += other.velocity

        average_velocity /= len(boids)

        adjustment = average_velocity - self.velocity
        self.velocity_buffer += adjustment * Boid.ALIGNMENT_FACTOR
    
    # Move away from other visible boids that are too close (to avoid colliding)
        # by slightly adjusting velocity (`velocity_buffer`).
        # You will need `position` of each boid.
        # Use `Boid.SEPARATION_FACTOR` to control how much each boid "wants" to go away from neighboring boids.
        # Hint: opposite of `cohere()`
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
        TURN_FACTOR = 0.01
        turn = Boid.MAX_SPEED * TURN_FACTOR
        if self.position.x < MARGIN:
            self.velocity_buffer.x += turn
        if self.position.x > screen_width - MARGIN:
            self.velocity_buffer.x -= turn
        if self.position.y < MARGIN:
            self.velocity_buffer.y += turn
        if self.position.y > screen_height - MARGIN:
            self.velocity_buffer.y -= turn
    
    def update_position(self):
        if self.velocity_buffer.length() > Boid.MAX_SPEED:
            self.velocity_buffer *= 0.9
        self.velocity = self.velocity_buffer.copy()
        self.position += self.velocity


def main():
    global screen_width, screen_height
    pygame.init()
    screen = None
    if screen_width and screen_height:
        screen = pygame.display.set_mode((screen_width, screen_height))
    else:
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        infoObject = pygame.display.Info()
        screen_width = infoObject.current_w
        screen_height = infoObject.current_h
    
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

        for boid in boids:
            
            #### YOUR CODE HERE ####
            
            visible_boids = []  # Could be useful to have for `far_visible_boids`
            close_boids = []
            far_visible_boids = []
            
            # boid.cohere(far_visible_boids) -> Each boid flies towards the the other boids. But they don't just immediately fly directly at each other. They gradually steer towards each other.
            # boid.align(far_visible_boids) -> Each boid tries to match the velocity (speed and direction) of the other boids around it.
            # boid.seperate(close_boids) -> Each boid tries to avoid running into the other boids. If it gets too close to another boid it will steer away from it.
            
            visible_boids = [other for other in boids if boid.position.distance_to(other.position) < Boid.DISTANCE_VISIBLE and boid != other]   
            close_boids = [other for other in visible_boids if boid.position.distance_to(other.position) < Boid.DISTANCE_SEPERATION]
            far_visible_boids = [other for other in visible_boids if boid.position.distance_to(other.position) >= Boid.DISTANCE_SEPERATION]

            boid.cohere(far_visible_boids)
            boid.align(far_visible_boids)
            boid.seperate(close_boids)

            #### END OF YOUR CODE ####

            # Keep within window bounds
            boid.keep_in_bounds()
            # Update the position based on the current velocity.
            boid.update_position()
            # Draw on screen
            pygame.draw.circle(screen, boid.color, (int(boid.position.x), int(boid.position.y)), 6)

        pygame.display.update()


main()
