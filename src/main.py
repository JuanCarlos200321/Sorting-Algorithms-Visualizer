import pygame
from random import randint
from time import time
from algs import algorithmsDict
import display as display

# Declared in display.py
# 1. global variables : numBars, delay, do_sorting, paused, timer_space_bar
# 2. widgets : sizeBox, delayBox, algorithmBox, playButton, stopButton


def main():
    numbers = []
    running = True
    display.algorithmBox.add_options(list(algorithmsDict.keys()))

    alg_iterator = None

    clock = pygame.time.Clock()

    total_elapsed_time = 0  # Variable to store total elapsed time

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and display.do_sorting:
                display.paused = not display.paused
                if display.paused:
                    # Pause the timer
                    total_elapsed_time += time() - start_time if start_time else 0
                    start_time = None
                else:
                    # Resume the timer
                    start_time = time()
                display.timer_space_bar = time()

            display.updateWidgets(event)

        display.delay = (display.delayBox.value - display.delayBox.rect.x - 6) / 1000  # delay is in ms

        if display.playButton.isActive:  # play button clicked
            display.playButton.isActive = False
            display.do_sorting = True
            current_alg = display.algorithmBox.get_active_option()
            display.numBars = int(display.sizeBox.text)
            numbers = [randint(10, 400) for _ in range(display.numBars)]  # random list to be sorted
            alg_iterator = algorithmsDict[current_alg](numbers, 0, display.numBars - 1)  # initialize iterator
            start_time = time()  # Record the starting time when play button is clicked

        if display.stopButton.isActive:  # stop button clicked
            display.stopButton.isActive = False
            display.do_sorting = False
            display.paused = False
            total_elapsed_time = 0
            try:  # deplete generator to display sorted numbers
                while True:
                    numbers, redBar1, redBar2, blueBar1, blueBar2 = next(alg_iterator)
            except StopIteration:
                pass

        if display.do_sorting and not display.paused:  # sorting animation
            try:
                if time() - start_time >= display.delay:
                    numbers, redBar1, redBar2, blueBar1, blueBar2 = next(alg_iterator)
                    display.drawInterface(numbers, redBar1, redBar2, blueBar1, blueBar2)

                    elapsed_time = time() - start_time  # Calculate elapsed time
                    total_elapsed_time += elapsed_time  # Accumulate total elapsed time
                    display.elapsed_time_box.text = f"{total_elapsed_time:.2f}"  # Update elapsed time text


                    start_time = time()  # Update start time

            except StopIteration:
                display.do_sorting = False
                total_elapsed_time = 0;

        elif display.do_sorting and display.paused:  # animation paused
            display.drawInterface(numbers, -1, -1, -1, -1)

        else:  # no animation
            a_set = set(range(display.numBars))
            display.drawInterface(numbers, -1, -1, -1, -1, greenRows=a_set)

        clock.tick(60)


if __name__ == '__main__':
    main()
