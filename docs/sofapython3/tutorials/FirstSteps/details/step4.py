from stlib3.scene import MainHeader, ContactHeader
from stlib3.physics.rigid import Floor
from stlib3.physics.rigid import Cube


def createScene(rootNode):
    """This is my first scene"""
    MainHeader(rootNode, gravity=[0.0, -981.0, 0.0])
    ContactHeader(rootNode, alarmDistance=10, contactDistance=5)
    rootNode.VisualStyle.displayFlags = 'showCollisionModels'
    rootNode.dt = 0.005

    Floor(rootNode,
          translation=[0.0, -160.0, 0.0],
          uniformScale=5.0,
          isAStaticObject=True)

    Floor(rootNode,
          name="FloorObstacle",
          translation=[0.0, -80.0, 0.0],
          color=[0.0, 1.0, 0.0, 1.0],
          uniformScale=0.8,
          isAStaticObject=True)

    for c in range(7):
        cube = Cube(rootNode,
                    name="Cube" + str(-210 + c * 70),
                    translation=[-210 + c * 70, 0.0, 0.0],
                    color=[c / 10.0, c * 0.7 / 10.0, 0.9, 1.0],
                    uniformScale=20.0)
        cube.addObject('UncoupledConstraintCorrection')

    return rootNode
