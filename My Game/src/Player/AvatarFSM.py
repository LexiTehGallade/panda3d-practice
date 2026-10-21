from direct.fsm.FSM import FSM


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