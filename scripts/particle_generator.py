import pygame
import scripts.settings as settings
import math
import random


last_particle_going_right = False


class Particle:
    def __init__(self, main, particle_surface, position):
        global last_particle_going_right

        self.main = main
        self.position = position
        self.surface = particle_surface
        self.angle = math.radians(random.randrange(0, 15) * (-1 if last_particle_going_right else 1))  # angle in radians with Y
        last_particle_going_right = not last_particle_going_right


class ParticleCollision:
    def __init__(self, main, particle_collision_surface, position):
        self.main = main
        self.particle_collision_surface = particle_collision_surface
        self.position = position

        self.timer = 2  # how long the particle collision will be draw


class ParticleGenerator:
    def __init__(self, main, particle_surface, particle_collision_surface, fire_surface=None):
        self.main = main
        self.particle_surface = particle_surface
        self.particle_collision_surface = particle_collision_surface
        self.fire_surface = fire_surface
        self.player_position = ()
        self.is_moving_up = False
        self.fire_on = False
        self.velocity = 1300
        self.particles_list = []
        self.particle_collision_list = []
        self.spawn_cooldown = 0

    def update(self, player_position, is_moving_up):
        self.player_position = player_position
        self.is_moving_up = is_moving_up

        # move and destroy if needed
        # particles
        if self.particles_list is not []:
            for i, particle in enumerate(self.particles_list):
                particle.position = (particle.position[0] + self.velocity * self.main.dt * math.sin(particle.angle), particle.position[1] + self.velocity * self.main.dt * math.cos(particle.angle))

                # destroy if needed and spawn particle collision
                if particle.position[1] > settings.MIN_HEIGHT - 20:
                    self.particles_list.pop(i)

                    # create ParticleCollision
                    self.particle_collision_list.append(ParticleCollision(self.main, self.particle_collision_surface, particle.position))

        # particles collision
        if self.particle_collision_list is not []:
            for i, particle_collision in enumerate(self.particle_collision_list):
                particle_collision.position = (particle_collision.position[0] - self.main.game.player_vel_x * self.main.dt, particle_collision.position[1])

                # deduce time
                particle_collision.timer -= self.main.dt

                # destroy if needed
                if particle_collision.timer <= 0:
                    self.particle_collision_list.pop(i)

        # spawn if needed
        if self.is_moving_up and self.spawn_cooldown <= 0:
            self.particles_list.append(Particle(self.main, self.particle_surface, self.player_position))
            self.spawn_cooldown = 0.08
        else:
            self.spawn_cooldown -= self.main.dt

        # fire control on/off
        if self.is_moving_up and self.fire_surface is not None and not self.main.dt == 0:
            self.fire_on = True
        elif not self.main.dt == 0:
            self.fire_on = False

        # draw
        # particle / particle_collision
        for particle in self.particles_list:
            self.main.screen.blit(particle.surface, particle.position)
        for particle_collision in self.particle_collision_list:
            self.main.screen.blit(self.particle_collision_surface, particle_collision.position)
        # fire
        if self.fire_on:
            self.main.screen.blit(self.fire_surface, (player_position[0] - self.fire_surface.get_width()/2.6, player_position[1] + 7))
