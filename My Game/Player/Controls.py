from direct.showbase import DirectObject
from panda3d.core import LVector3f
import sys


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