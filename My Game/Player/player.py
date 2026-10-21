from direct.showbase import DirectObject
from direct.fsm.FSM import FSM
from panda3d.core import LVector3f
from direct.task import Task
from direct.actor.Actor import Actor
import sys


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
        self.controls = PlayerControls(self.av, self.player_node, self.camera)
        taskMgr.add(self.mouseTask,"MouseResetPos")

    # Doing it this way lets us move/rotate the camera and avatar,
    # independent of each other and the 'actual' position of the player, for animation and such.
    def CreatePlayer(self):
        self.player_node = render.attachNewNode("Player")
        self.av = Actor("Models/melody.bam", {
            "idle": "Models/melody-Idle.bam",
            "walk": "Models/melody-Walk.bam",
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


class PlayerControls(DirectObject.DirectObject):
    # PlayerControls: Handles the event listener and velocity for the player's actual movement.
    def __init__(self, av, playernode, camnode):
        super().__init__()
        self.vector_math = {
            1: (-1, "Y"),  # North down, South up
            2: (1, "Y"),  # North up, South down
            3: (-1, "X"),  # East down, West up
            4: (1, "X")  # East up, West down
        }
        self.avatar = av
        self.camera = camnode
        self.X_vel = 0
        self.Y_vel = 0
        self.movementV = LVector3f(0, 0, 0)
        self.player = playernode

        taskMgr.add(self.velocity, "Velocity")
        self.acceptOnce("escape", self.exitGame)
        self.accept("w", self.walk, extraArgs=[1])
        self.accept("w-up", self.walk, extraArgs=[2])
        self.accept("d", self.walk, extraArgs=[3])
        self.accept("d-up", self.walk, extraArgs=[4])
        self.accept("s", self.walk, extraArgs=[2])
        self.accept("s-up", self.walk, extraArgs=[1])
        self.accept("a", self.walk, extraArgs=[4])
        self.accept("a-up", self.walk, extraArgs=[3])
        self.av_fsm = AvatarFSM(av)

    def walk(self,direction):
        if self.vector_math[direction][1] == "X":
            self.X_vel += self.vector_math[direction][0]
        if self.vector_math[direction][1] == "Y":
            self.Y_vel += self.vector_math[direction][0]

        if abs(self.X_vel) + abs(self.Y_vel) == 0:
            self.av_fsm.request("Idle")
        elif self.Y_vel < 0:
            self.av_fsm.request("Walk","forward")
        elif self.Y_vel > 0:
            self.av_fsm.request("Walk","back")

    def velocity(self, task):
        if abs(self.X_vel) + abs(self.Y_vel) == 0:
            pass
        else:
            self.movementV = LVector3f(self.X_vel, self.Y_vel,0)
            self.player.setPos(self.avatar, self.movementV.normalized() * 0.06)
        return Task.cont

    # Todo: replace with a close button
    def exitGame(self):
        sys.exit(0)


class AvatarFSM(FSM):
    # Finite State Machine that manages the avatar's animations and sounds.
    def __init__(self, av):
        FSM.__init__(self, AvatarFSM)
        self.avatar = av

    def enterIdle(self):
        if self.avatar.getCurrentAnim() != "idle":
            self.avatar.loop("idle")

    def exitIdle(self):
        pass

    def enterWalk(self,direction):
        if direction == "forward":
            self.avatar.loop("walk")
            self.avatar.setPlayRate(1,"walk")
        elif direction == "back":
            self.avatar.loop("walk")
            self.avatar.setPlayRate(-1,"walk")

    def exitWalk(self):
        pass