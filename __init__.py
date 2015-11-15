#This states the metadata for the plugin
bl_info = {
    "name": "Dark Blender R1",
    "author": "Linko, Crocadillian",
    "version": (1, 0),
    "blender": (2, 76),
    "api": 39347,
    "location": "3D View > Object Mode > Tools > Dark Blender",
    "description": "A whole bunch of script goodness for game developers.",
    "warning": "Beta",
    "tracker_url": "",
    "category": "Object"
}

if "bpy" in locals():
    import imp
    print(">>>>>>>>>>> Reloading Plugin", __name__, "<<<<<<<<<<<<")
    if "definitions" in locals():
        imp.reload(definitions)
    if "properties" in locals():
        imp.reload(properties)
    if "user_interface" in locals():
        imp.reload(user_interface)
    if "operators" in locals():
        imp.reload(operators)

print(">>>>>>>>>>> Beginning Import", __name__, "<<<<<<<<<<<<")

import bpy
from . import definitions
from . import properties
from . import user_interface
from . import operators

def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()

print(">>>>>>>>>>> Import Finished", __name__, "<<<<<<<<<<<<")
