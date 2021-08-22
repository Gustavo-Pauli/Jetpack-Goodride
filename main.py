# Main program loop

import game

g = game.Game()

while g.running:
    g.playing = True
    g.game_loop()
