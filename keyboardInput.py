import pygame


class KeyboardInput:
    def __init__(self):
        self.holding = []
        self.keys_down = []
        self.keys_up = []
        self.terminate = False

    def update(self):
        self.keys_up = []
        self.keys_down = []
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.terminate = True
            elif event.type == pygame.KEYDOWN:
                if event.key not in self.holding:
                    self.holding.append(event.key)
                    self.keys_down.append(event.key)
            elif event.type == pygame.KEYUP:
                if event.key in self.holding:
                    self.holding.remove(event.key)
                    self.keys_up.append(event.key)

    def isHolding(self, key):
        return key in self.holding

    def isKeyDown(self, key):
        return key in self.keys_down

    def isKeyUp(self, key):
        return key in self.keys_up