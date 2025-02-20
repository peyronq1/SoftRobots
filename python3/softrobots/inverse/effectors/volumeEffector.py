# -*- coding: utf-8 -*-
import Sofa

def getOraddTheTemplateNode(attachedAsAChildOf=None, attachedTo=None, name=None):
    if attachedTo != None:
        if name != None:
            Sofa.msg_error(attachedTo, "The name parameter cannot be used when a template is attachedTo to an existing node")
            return attachedTo
        if attachedAsAChildOf != None:
            Sofa.msg_error(attachedTo, "Both attachedTo and attachedAsAChildOf are set is not allowed.")
            return attachedTo
        return attachedTo
    return attachedAsAChildOf.addChild(name)

def VolumeEffector(surfaceMeshFileName=None,
                    attachedAsAChildOf=None,
                    attachedTo=None,
                    name="VolumeEffector",
                    rotation=[0.0, 0.0, 0.0],
                    translation=[0.0, 0.0, 0.0],
                    uniformScale=1,
                    initialValue=0,
                    valueType="volumeGrowth"):

    """Adds a volume effector constraint.

    This adds all the components necessary in Sofa to include a cavity model whose volume should be determined by optimizing an external force.

    The constraint apply to a parent mesh.

    Args:
        cavityMeshFile (string): path to the cavity mesh (the mesh should be a surfacic mesh, ie only triangles or quads).

        name (string): name of the added node.

        initialValue (real): value to apply, default is 0.

        valueType (string): type of the parameter value (volumeGrowth or pressure), default is volumeGrowth.

    Structure:
    .. sourcecode:: qml
        Node : {
                name : "VolumeEffector"
                MeshTopology,
                MechanicalObject,
                SurfacePressureConstraint,
                BarycentricMapping
        }

    """
    if attachedAsAChildOf == None and attachedTo == None:
        Sofa.msg_error("Your VolumeEffector isn't link/child of any node, please set the argument attachedTo or attachedAsAChildOf")
        return None

    if surfaceMeshFileName == None:
        Sofa.msg_error("No surfaceMeshFileName specified, please specify one")
        return None

    veffector = getOraddTheTemplateNode(attachedAsAChildOf=attachedAsAChildOf,
                                           attachedTo=attachedTo,
                                           name=name)

    # This add a MeshSTLLoader, a componant loading the topology of the cavity.
    if surfaceMeshFileName.endswith(".stl"):
        veffector.addObject('MeshSTLLoader', name='MeshLoader', filename=surfaceMeshFileName, rotation=rotation, translation=translation, scale=uniformScale)
    elif surfaceMeshFileName.endswith(".obj"):
        veffector.addObject('MeshObjLoader', name='MeshLoader', filename=surfaceMeshFileName, rotation=rotation, translation=translation, scale=uniformScale)
    else :
        Sofa.msg_error("Your surfaceMeshFileName extension is not the right one, you have to give a surfacic mesh with .stl or .obj extension")
        return None

    # This add a MeshTopology, a componant holding the topology of the cavity.
    # veffector.addObject('MeshTopology', name="topology", filename=surfaceMeshFileName)
    veffector.addObject('MeshTopology', name='topology', src='@MeshLoader')

    # This add a MechanicalObject, a componant holding the degree of freedom of our
    # mechanical modelling. In the case of a cavity actuated with veffector, it is a set of positions specifying
    # the points where the pressure is applied.
    veffector.addObject('MechanicalObject', src="@topology")
    veffector.addObject('VolumeEffector', template='Vec3', triangles='@topology.triangles')
    #veffector.addObject('SurfacePressureConstraint',
    #                      value=initialValue,
    #                      valueType=valueType)

    # This add a BarycentricMapping. A BarycentricMapping is a key element as it will add a bi-directional link
    # between the cavity's DoFs and the parents's ones so that the pressure applied on the cavity wall will be mapped
    # to the volume structure and vice-versa;
    veffector.addObject('BarycentricMapping', name="Mapping", mapForces=False, mapMasses=False)
    return veffector

def createScene(node):
    from stlib.scene import MainHeader
    MainHeader(node, plugins=["SoftRobots"])
    node.addObject('MechanicalObject')
    VolumeEffector(surfaceMeshFileName="mesh/cube.obj", attachedAsAChildOf=node)
