from direct.showbase.ShowBase import ShowBase
from Player.player import Player
from UserInterface.UI import UI
from World.ObjectWorld import ObjectWorld
from NPC.NPCTest import TestNPC
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
        self.TestNPC = None
        self.UI = None

    def Create_UI(self):
        self.UI = UI()

    def Setup_World(self):
        self.world = self.Obj_world.CreateWorld()
        self.world["Skybox"].reparentTo(self.av)

    def Setup_NPC(self):
        self.TestNPC = TestNPC()
        self.TestNPC.npc_node.setPos(-2,0,0)
        self.TestNPC.npc_node.reparentTo(render)
        self.TestNPC.character.loop("action")


# Main loop
if __name__ == "__main__":
    my_game = WalkingGame()
    my_game.Setup_World()
    my_game.Setup_NPC()
    my_game.Create_UI()
    my_game.run()