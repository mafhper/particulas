import pygame
import random
import math
from datetime import datetime

pygame.init()

# Configurar para tela cheia
info = pygame.display.Info()
INIT_WIDTH, INIT_HEIGHT = info.current_w, info.current_h
screen = pygame.display.set_mode((INIT_WIDTH, INIT_HEIGHT), 
          pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF)
pygame.display.set_caption("Simulação de Partículas - Tela Cheia")

# Variáveis globais
WIDTH, HEIGHT = INIT_WIDTH, INIT_HEIGHT
trail_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

class Particle:
    def __init__(self, x, y):
        self.pos = pygame.Vector2(x, y)
        self.vel = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
        self.acc = pygame.Vector2(0, 0)
        self.mass = random.uniform(0.5, 5.0)
        self.radius = int((self.mass ** (1/3)) * 2)  # Parêntese FECHADO
        self.color = (
            random.randint(50, 255),
            random.randint(50, 255),
            random.randint(50, 255)
        )

    def apply_force(self, force):
        self.acc += force / self.mass

    def update(self, dt):
        self.vel += self.acc * dt
        self.pos += self.vel * dt
        self.acc *= 0
        
        # Limites físicos com colisão
        self.pos.x = max(self.radius, min(self.pos.x, WIDTH - self.radius))
        self.pos.y = max(self.radius, min(self.pos.y, HEIGHT - self.radius))
        if self.pos.x in (self.radius, WIDTH - self.radius):
            self.vel.x *= -0.8
        if self.pos.y in (self.radius, HEIGHT - self.radius):
            self.vel.y *= -0.8

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.pos.x), int(self.pos.y)), self.radius)

def gravitational_force(p1, p2, G=0.1):
    direction = p2.pos - p1.pos
    distance = direction.length()
    if distance < (p1.radius + p2.radius) * 0.8:
        return pygame.Vector2(0, 0)
    try:
        direction.normalize_ip()
    except ValueError:
        return pygame.Vector2(0, 0)
    force_magnitude = G * p1.mass * p2.mass / (distance**2)
    return direction * force_magnitude

def create_particles(num):
    return [Particle(random.uniform(0, WIDTH), random.uniform(0, HEIGHT)) for _ in range(num)]

def merge_particles(p1, p2):
    total_mass = p1.mass + p2.mass
    new_vel = (p1.vel * p1.mass + p2.vel * p2.mass) / total_mass
    new_pos = (p1.pos * p1.mass + p2.pos * p2.mass) / total_mass
    
    merged = Particle(new_pos.x, new_pos.y)
    merged.mass = total_mass
    merged.vel = new_vel
    merged.radius = int((total_mass ** (1/3)) * 2)  # Parêntese FECHADO
    merged.color = (
        (p1.color[0] + p2.color[0]) // 2,
        (p1.color[1] + p2.color[1]) // 2,
        (p1.color[2] + p2.color[2]) // 2
    )
    return merged

# Sistema principal
particles = create_particles(300)
clock = pygame.time.Clock()
running = True
paused = False
show_time = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                particles = create_particles(300)
            elif event.key == pygame.K_p:
                paused = not paused
            elif event.key == pygame.K_a:
                for p in particles:
                    p.pos.update(random.uniform(0, WIDTH), random.uniform(0, HEIGHT))
            elif event.key == pygame.K_h:
                show_time = not show_time
            elif event.key == pygame.K_ESCAPE:
                running = False

    if not paused:
        trail_surface.fill((0, 0, 0, 20))
        
        # Física e fusão
        new_particles = []
        merged = set()
        for i in range(len(particles)):
            if i in merged:
                continue
            p1 = particles[i]
            for j in range(i+1, len(particles)):
                if j in merged:
                    continue
                p2 = particles[j]
                if p1.pos.distance_to(p2.pos) < (p1.radius + p2.radius):
                    new_particles.append(merge_particles(p1, p2))
                    merged.update([i, j])
                    break
            else:
                new_particles.append(p1)
        particles = new_particles

        # Atualizar partículas
        for p in particles:
            p.update(1)
            pygame.draw.circle(trail_surface, (*p.color, 100),
                             (int(p.pos.x), int(p.pos.y)), 
                             max(1, p.radius//2))

        # Renderização
        screen.fill((0, 0, 0))
        screen.blit(trail_surface, (0, 0))
        for p in particles:
            p.draw(screen)

        # Hora atual
        if show_time:
            font = pygame.font.SysFont("Consolas", 30)
            time_text = font.render(datetime.now().strftime("%H:%M:%S"), True, (200, 200, 200))
            screen.blit(time_text, (20, 20))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
