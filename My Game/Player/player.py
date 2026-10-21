from direct.task import Task
from direct.actor.Actor import Actor
from Player import Controls


# It also handles the player controls, and the avatar FSM.
# todo: Split these classes into separate files where appropriate.

class Player:
    # Player class: handles creating the player reference node, the avatar actor, and the third person camera.
    def __init__(self):
        self.player_node = None
        self.av = self.CreatePlayer()
        self.av.setScale(0.8)
        self.av.loop("idle")
        self.camera = self.InitializeCamera()
        self.controls = Controls.PlayerControls(self.av, self.player_node)
        taskMgr.add(self.mouseTask,"MouseResetPos")

    # Doing it this way lets us move/rotate the camera and avatar,
    # independent of each other and the 'actual' position of the player, for animation and such.
    def CreatePlayer(self):
        self.player_node = render.attachNewNode("Player")
        self.av = Actor("Models/Melody/melody.bam", {
            "idle": "Models/Melody/anims/melody-Idle.bam",
            "walk": "Models/Melody/anims/melody-Walk.bam",
        })
        self.av.reparentTo(self.player_node)
        return self.av

    def InitializeCamera(self):
        self.cam_node = self.player_node.attachNewNode("camnode")
        base.camera.setPos(0, -5, 0)
        self.cam_node.setPos(0,0,1.5)
        base.camera.reparentTo(self.cam_node)
        self.cam_node.setH(180)
        base.camLens.setFov(70)
        return self.cam_node

    # We need to keep the mouse cursor locked to the center of the screen for a mouselook control scheme.
    def mouseTask(self,task):
        self.mw = base.mouseWatcherNode

        if self.mw.hasMouse():
            # get the position, which at center is (0, 0)
            self.x = round(self.mw.getMouseX(),3)
            self.y = round(self.mw.getMouseY(),3)

            # move mouse back to center
            props = base.win.getProperties()
            base.win.movePointer(0,
                                 props.getXSize() // 2,
                                 props.getYSize() // 2)
            # now, x and y can be considered relative movements
            if abs(self.x) > 0.001:
                self.cam_node.setH(self.cam_node,-(self.x*60))
            if abs(self.y) > 0.001:
                self.cam_node.setP(self.cam_node, (self.y*60))
            self.cam_node.setR(0)
            self.av.setH(self.cam_node,180)
            self.av.setP(0)
            self.av.setR(0)
        return Task.cont

    def getAvatar(self):
        return self.av