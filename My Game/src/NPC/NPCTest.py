from direct.actor.Actor import Actor


class TestNPC:
    def __init__(self):
        self.modeldir = "../resources/Models/TestNPC"
        self.animdir = "../resources/Models/TestNPC/anims"
        self.npc_node = self.CreateNPCNode()
        self.character = self.CreateNPC()

    def CreateNPCNode(self):
        self.npc_node = render.attachNewNode("TestNPC")
        print(self.npc_node)
        return self.npc_node

    def CreateNPC(self):
        self.character = Actor(f"{self.modeldir}/test_npc.egg",{
            "idle": f"{self.animdir}/test_npc-default.egg",
            "move": f"{self.animdir}/test_npc-move.egg",
            "action": f"{self.animdir}/test_npc-action.egg",
        })
        self.character.reparentTo(self.npc_node)
        return self.character