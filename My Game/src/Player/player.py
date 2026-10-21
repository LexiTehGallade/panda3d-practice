from direct.actor.Actor import Actor
from Player import Controls
from Player import Camera


# Instantiates the player, avatar, and camera
class Player:
    # Player class: handles creating the player reference node, the avatar actor, and the third person camera.
    def __init__(self):
        self.player_node = None
        self.av = self.CreatePlayer()
        self.av.setScale(0.8)
        self.av.loop("idle")
        self.camera = Camera.ThirdPersonCam(self.player_node, self.av)
        self.camera.InitializeCamera()
        self.controls = Controls.PlayerControls(self.av, self.player_node)

    # Doing it this way lets us move/rotate the camera and avatar,
    # independent of each other and the 'actual' position of the player, for animation and such.
    def CreatePlayer(self):
        self.player_node = render.attachNewNode("Player")
        self.av = Actor("../resources/Models/Melody/melody.bam", {
            "idle": "../resources/Models/Melody/anims/melody-Idle.bam",
            "walk": "../resources/Models/Melody/anims/melody-Walk.bam",
        })
        self.av.reparentTo(self.player_node)
        return self.av

    def getAvatar(self):
        return self.av