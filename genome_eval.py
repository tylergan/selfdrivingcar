import pygame
import neat
import os
from car import Car
from draw_window import draw_window

pygame.font.init()


def eval_genomes(genomes, config):
    '''This function evaluates the genomes of the ANN (using NEAT).'''
    global gen
    gen += 1
    
    # Initialise NEAT
    nets = []
    cars = []

    for _, genome in genomes:
        nets.append(neat.nn.FeedForwardNetwork.create(genome, config))
        genome.fitness = 0

        # create car object
        cars.append(Car())

    # game setup
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()
    track = pygame.image.load(os.path.join("imgs", "map.png"))

    # main
    while len(cars) > 0:
        clock.tick(0)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        for i, car in enumerate(cars):
            data = nets[i].activate(car.ann_input())
            output = data.index(max(data))
            car.angle = car.angle + 10 if output == 0 else car.angle - 10

            if car.is_alive:
                car.move(track)
                genomes[i][1].fitness += (car.distance / 50)  # reward the car for staying alive
            else:  # remove the car from the neural net.
                cars.pop(i)
                nets.pop(i)

        draw_window(win, track, cars, gen)


gen = 0
WIN_WIDTH = 1500
WIN_HEIGHT = 800
