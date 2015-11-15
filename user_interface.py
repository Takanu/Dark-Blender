import bpy
from bpy.props import IntProperty, BoolProperty, FloatProperty, EnumProperty, PointerProperty
from bpy.types import Menu, Panel, AddonPreferences, PropertyGroup, UIList
from rna_prop_ui import PropertyPanel

#Generates the UI panel inside the 3D view
class DB_ObjectMode(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_context = "objectmode" # When the panel will appear
    bl_label = "Tools" # Dropdown Title
    bl_category = "Dark Blender" # Tab category

    def draw(self, context):
        layout = self.layout

        col_export = layout.column(align=True)
        col_export.label("Additional Primitives")
        col_export.operator("scene.db_addpipe")
        col_export.operator("scene.db_addeyes")
        col_export.separator()

        col_export.label("Sculpt/Organic Mesh Tools")
        col_export.operator("scene.db_prepdynatopo")
        col_export.separator()

        col_export.label("Topology Tools")
        col_export.operator("scene.db_generatehp")
        col_export.operator("scene.db_generatelp")
        col_export.operator("scene.db_quickdecimate")
        col_export.operator("scene.db_quickretopo")
        col_export.separator()

        col_export.label("Utilities")
        col_export.operator("scene.db_autoseam")
        col_export.operator("scene.db_resym_x")
        col_export.operator("scene.db_unfoldhalf")
        col_export.separator()

class DB_EditMode(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_context = "mesh_edit"
    bl_label = "Tools"
    bl_category = "Dark Blender"

    def draw(self, context):
        layout = self.layout

        col_export = layout.column(align=True)
        col_export.label("Utilities")
        col_export.operator("scene.gx_extractmesh")
        col_export.separator()
