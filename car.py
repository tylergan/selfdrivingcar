import pygame
import math
import os


class Car:
    SPEED = 15
    IMG = pygame.transform.scale(pygame.image.load(os.path.join("imgs", "car.png")), (100, 100))

    def __init__(self):
        self.img = self.IMG
        self.pos = [700, 650]
        self.angle = 0
        self.speed = self.SPEED
        self.distance = 0
        self.center = (self.pos[0] + 50, self.pos[1] + 50)  # where radars will be placed
        self.radars = []
        self.is_alive = True

    def draw(self, win):
        '''Draw method takes in a window and draws the radars and the car onto that window.'''
        win.blit(self.img, self.pos)

        for radar in self.radars:
            pos, _ = radar
            pygame.draw.line(win, (0, 255, 0), self.center, pos, 1)
            pygame.draw.circle(win, (0, 255, 0), pos, 5)

    def rotate_img(self):
        '''Rotate method which uses the ORIGINAL image of the car and rotates it by the angle which is not confined to a limit. Hence, we must use the original image so that
           we can use the angle to rotate by RELATIVE (or with respect) to the original image.'''
        rotated_img = pygame.transform.rotate(self.IMG, self.angle)  # rotate img
        rotated_rect = self.IMG.get_rect()
        rotated_rect.center = rotated_img.get_rect().center  # set new rectangle center
        return rotated_img.subsurface(rotated_rect)  # create new object with new rectangle center

    def update_radar(self, degree, track):
        '''Update radar method will take a degree (ranging from -90 to 120) and have it detect the distance from the car to a out-of-bounds (white pixel).
           We do self.angle + degree to have a constant separation of 45 degrees per radar.'''
        # set initial radar to length of 0
        len = 0
        x = int(self.center[0] + math.cos(math.radians(360 - (self.angle + degree))) * len)
        y = int(self.center[1] + math.sin(math.radians(360 - (self.angle + degree))) * len)

        while not track.get_at((x, y)) == (255, 255, 255, 255) and len < 300:  # set max radar length of 300 pixels
            len += 1  # adjust the radar until either it detects a white pixel or is at max length
            # decision to use cos and sin graphs given there is no limit to the range of the angle.
            x = int(self.center[0] + math.cos(math.radians(360 - (self.angle + degree))) * len)
            y = int(self.center[1] + math.sin(math.radians(360 - (self.angle + degree))) * len)

        dist = int(math.sqrt((x - self.center[0])**2 + (y - self.center[1])**2))  # distance of car to white pixel detecetd by radar
        self.radars.append(((x, y), dist))

    def collide(self, track, collision_points):
        '''Uses the four corners of the car to determine whether any of it touches a white pixel. The car is destroyed if it does.'''
        for point in collision_points:
            if track.get_at((int(point[0]), int(point[1]))) == (255, 255, 255, 255):  # detect whether one of the four corners touch a white pixel
                self.is_alive = False
                break

    def conduct_checks(self, track):
        '''This method will calculate the four collision points and reset the radars of the car. The four offsets are used to define each corner of the car.'''
        # check for car collision
        len = 40
        collision_points = []

        for i in range(4):
            # decision to use cos and sin graphs given there is no limit to the range of the angle.
            offset = 30 if i == 0 else 150 if i == 1 else 210 if i == 2 else 330
            collision_points.append((self.center[0] + math.cos(math.radians(360 - (self.angle + offset))) * len,
                                     self.center[1] + math.sin(math.radians(360 - (self.angle + offset))) * len))

        self.collide(track, collision_points)

        self.radars.clear()
        for degree in range(-90, 120, 45):  # update radars each with a 45 degree difference
            self.update_radar(degree, track)

    def move(self, track):
        '''This method will move the car'''
        self.img = self.rotate_img()

        # calculating position
        self.pos[0] += math.cos(math.radians(360 - self.angle)) * self.speed  # move x-pos relative to angle along cosine function.
        self.pos[1] += math.sin(math.radians(360 - self.angle)) * self.speed  # move y-pos relative to angle along cosine function.

        # add some boundaries to speed up the learning
        if self.pos[0] < 20:
            self.pos[0] = 20
        elif self.pos[0] > WIN_WIDTH - 120:  # 1500 is screen width
            self.pos[0] = WIN_WIDTH - 120

        if self.pos[1] < 20:
            self.pos[1] = 20
        elif self.pos[1] > WIN_HEIGHT - 120:  # 800 is screen height
            self.pos[1] = WIN_HEIGHT - 120

        self.center = (int(self.pos[0] + 50), int(self.pos[1] + 50))  # update radar starting position
        self.distance += self.speed

        self.conduct_checks(track)

    def ann_input(self):
        '''This function uses the five radars' distance as input to determine what move it should make.'''
        res = [0 for _ in range(5)]
        for i, radar in enumerate(self.radars):
            res[i] = int(radar[1] / 30)  # add inputs of distances found by the radars
        return res


WIN_WIDTH = 1500
WIN_HEIGHT = 800
