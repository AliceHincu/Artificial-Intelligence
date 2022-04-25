# import the pygame module, so you can use it
import pygame

from Environment import Environment
from Global_variables import *

# define a main function
from Service import Service


class UI:
    def __init__(self):
        self.__width = 800
        self.__height = 400

    def display_text(self, msg, screen):
        font = pygame.font.SysFont('timesnewroman', 30)
        text = font.render(msg, True, PURPLE)
        text_rect = text.get_rect()
        text_rect.center = (self.__width // 2, self.__height // 2)
        screen.fill(LIGHT_PURPLE)
        screen.blit(text, text_rect)  # blit=draw
        pygame.display.update()

    def main(self):
        # initialize the pygame module
        pygame.init()

        # load and set the logo
        logo = pygame.image.load("logo32x32.png")
        pygame.display.set_icon(logo)
        pygame.display.set_caption("drone exploration")

        # create service instance
        service = Service()

        # create a surface on screen that has the size of 800 x 480
        screen = pygame.display.set_mode((self.__width, self.__height))
        screen.fill(WHITE)
        screen.blit(service.getEnvironmentImage(), (0, 0))

        # main loop
        running = True
        quit = False
        text = "Error"
        while running:
            # event handling, gets all event from the event queue
            for event in pygame.event.get():
                # only do something if the event is of type QUIT
                if event.type == pygame.QUIT:
                    # change the value to False, to exit the main loop
                    quit = True
                    text = "Quiting..."

            if quit:
                running = False
            else:
                if service.droneCanMove():
                    service.markDetectedWalls()
                    screen.blit(service.getDroneMapImage(), (self.__width//2, 0))

                running = service.moveDrone()
                if not running:
                    text = "Finished!!!"
                    pygame.time.delay(1000)
                pygame.display.flip()
                pygame.time.delay(STEP_DURATION)

        self.display_text(text, screen)
        pygame.time.delay(DELAY_DURATION)
        pygame.quit()


if __name__ == "__main__":
    ui = UI()
    ui.main()
