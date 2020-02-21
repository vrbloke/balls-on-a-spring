from vpython import *

## VARIABLES

dt = 0.02
spring_constant = 4
default_length = 40
fps = 60
precision = 0.02

## CLASSES

class Spring(helix):
    def __init__(self, start, end, default_length, spring_constant):
        super().__init__(axis = end.pos - start.pos, pos = start.pos, color = color.orange, radius = 6, coils = 10, thickness = 1)
        self.start = start
        self.end = end
        self.default_length = default_length
        self.spring_constant = spring_constant

    def current_length(self):
        return mag(self.end.pos - self.start.pos)

    def adjust(self):
        self.axis = self.end.pos - self.start.pos
        self.pos = self.start.pos

class VelocitySphere(sphere):
    def __init__(self, position, mass):
        super().__init__(pos = position, color = color.blue, radius = 10)
        self.velocity = vector(0, 0, 0)
        self.mass = mass
        self.label = label(text = str(self.mass), pos = self.pos, opacity = 0, height = 40, color = color.white, yoffset = 100)

    def apply_force(self, force):
        self.velocity = self.velocity + force * dt / self.mass

    def move(self):
        self.pos = self.pos + self.velocity * dt
        self.label.pos = self.label.pos + self.velocity * dt

    def adjust(self):
        self.pos = self.pos + precision * self.velocity * dt
        self.label.pos = self.label.pos + precision * self.velocity * dt

## Create the objects

ball1 = VelocitySphere(vector(-90, 0, 0), 1) # Left ball
ball2 = VelocitySphere(vector(90, 0, 0), 1) # Right ball
spring = Spring(ball1, ball2, default_length, spring_constant)

## Simulation

while 1:
    rate(fps)
    # The spring pulls/pushes
    if spring.current_length() != spring.default_length:
        # Calculate how much force
        force = (spring.current_length() - spring.default_length) * spring.spring_constant * vector(1, 0, 0)
        # Positive force correlates with a STRETCHED spring -- it should pull ball1 in the positive direction,
        # and ball 2 in the negative direction -- vice versa for negative force
        ball1.apply_force(force)
        ball2.apply_force(-force)
        # Move balls
        ball1.move()
        ball2.move()
        # Adjust spring
        spring.adjust()

    # The balls collide
    if mag(ball1.pos - ball2.pos) < ball1.radius + ball2.radius:
        helper = ball1.velocity
        ball1.velocity = (ball1.velocity * (ball1.mass - ball2.mass) + 2 * ball2.mass * ball2.velocity) / (ball1.mass + ball2.mass)
        ball2.velocity = (ball2.velocity * (ball2.mass - ball1.mass) + 2 * ball1.mass * helper) / (ball1.mass + ball2.mass)
        while mag(ball1.pos - ball2.pos) < ball1.radius + ball2.radius:
            ball1.adjust()
            ball2.adjust()

