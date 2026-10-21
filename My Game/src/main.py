from direct.showbase.ShowBase import ShowBase
from Player.player import Player
from UserInterface.UI import UI
from World.ObjectWorld import ObjectWorld
from panda3d.core import loadPrcFile

# Main class that inherits from ShowBase, this is what starts the game.
class WalkingGame(ShowBase):
    # Create player and camera, also disable Panda's default camera driver.
    def __init__(self,):
        loadPrcFile("config/Config.prc")
        ShowBase.__init__(self)
        self.disableMouse()
        self.player = Player()
        self.av = self.player.getAvatar()
        self.Obj_world = ObjectWorld()
        self.world = {}
        self.UI = None

    def Create_UI(self):
        self.UI = UI()

    def Setup_World(self):
        self.world = self.Obj_world.CreateWorld()
        self.world["Skybox"].reparentTo(self.av)


# Main loop
if __name__ == "__main__":
    my_game = WalkingGame()
    my_game.Setup_World()
    my_game.Create_UI()
    my_game.run()