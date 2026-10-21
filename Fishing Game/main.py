from direct.showbase.ShowBase import ShowBase
from Player.player import Player

# Main class that inherits from ShowBase, this is what starts the game.
class WalkingGame(ShowBase):
    # Create player and camera, also disable Panda's default camera driver.
    def __init__(self,):
        ShowBase.__init__(self)
        self.disableMouse()
        self.world = {}
        self.player = Player()

    def CreateWorld(self):
        self.worldplane = loader.loadModel("Models/worldplane.bam")
        self.world["Ground"] = self.worldplane
        self.world["Ground"].reparentTo(render)
        self.world["Ground"].setTwoSided(True)
        self.world["Ground"].setScale(5)


# Main loop
if __name__ == "__main__":
    my_game = WalkingGame()
    my_game.CreateWorld()
    print(my_game.world)
    my_game.run()