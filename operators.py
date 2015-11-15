import bpy, bmesh
from bpy.types import Operator
from .definitions import SelectObject, FocusObject, ActivateObject, DuplicateObject, DuplicateObjects, DeleteObject, MoveObject, MoveObjects

class DB_Add_Pipe(Operator):
    """Creates a path from the menu."""

    bl_idname = "scene.db_addpipe"
    bl_label = "Add Pipe"

    def execute(self, context):
        print(self)

        #Add Pipe
        bpy.ops.object.mode_set(mode = 'OBJECT')
        bpy.ops.curve.primitive_bezier_curve_add(radius=1, view_align=False, enter_editmode=False, location=(0, 0, 0), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
        bpy.context.object.data.resolution_u = 10
        bpy.context.object.data.fill_mode = 'FULL'
        bpy.context.object.data.bevel_depth = 0.1
        bpy.context.object.data.bevel_resolution = 4

        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
        bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN')

        self.report({'INFO'}, "Added Pipe.")

        return {'FINISHED'}


class DB_Auto_Seam(Operator):
    """Automatically generates seams for hard-surface models."""

    bl_idname = "scene.db_autoseam"
    bl_label = "Generate Seams"

    def execute(self, context):
        print(self)

        bpy.ops.object.mode_set(mode = 'OBJECT')

        for obj in bpy.context.selected_objects:

            bpy.context.scene.objects.active = obj

            bpy.ops.object.mode_set(mode = 'EDIT')
            bpy.ops.mesh.select_mode(type="EDGE")
            bpy.ops.mesh.select_all(action = 'DESELECT')
            bpy.ops.mesh.edges_select_sharp(sharpness=0.525344)
            bpy.ops.mesh.mark_seam(clear=False)
            bpy.ops.mesh.select_all(action = 'SELECT')

            bpy.ops.mesh.remove_doubles()

            bpy.ops.uv.unwrap(method='ANGLE_BASED', margin=0.02)
            bpy.ops.mesh.select_all(action = 'DESELECT')
            bpy.ops.object.mode_set(mode = 'OBJECT')

        self.report({'INFO'}, "Auto Seam Complete.")

        return {'FINISHED'}


class DB_Prep_Dynatopo(Operator):
    """Prepares the selected mesh for dynamic topology."""

    bl_idname = "scene.db_prepdynatopo"
    bl_label = "Prepare for Dynatopo"

    def execute(self, context):
        print(self)

        #Dyntopo Sculpt
        bpy.ops.object.mode_set(mode = 'OBJECT')
        bpy.ops.object.convert(target='MESH')

        bpy.ops.object.mode_set(mode = 'EDIT')
        bpy.ops.mesh.select_all(action = 'SELECT')
        bpy.ops.mesh.remove_doubles()
        bpy.ops.mesh.normals_make_consistent(inside=False)

        bpy.ops.object.mode_set(mode = 'SCULPT')
        bpy.ops.sculpt.dynamic_topology_toggle()

        self.report({'INFO'}, "Prepared mesh for Dymanic Topology.")

        return {'FINISHED'}


class DB_Extract_Mesh(Operator):
    """...ill get back to you on that one."""

    bl_idname = "scene.gx_extractmesh"
    bl_label = "Extract Mesh"

    def execute(self, context):
        print(self)

        #Extract Mesh
        bpy.ops.object.mode_set(mode = 'OBJECT')
        bpy.ops.object.duplicate()

        bpy.ops.object.mode_set(mode = 'EDIT')
        bpy.ops.mesh.select_all(action='INVERT')
        bpy.ops.mesh.delete(type='FACE')
        bpy.ops.object.mode_set(mode = 'OBJECT')
        bpy.ops.object.modifier_add(type='SOLIDIFY')
        bpy.context.object.modifiers["Solidify"].thickness = -0.1

        self.report({'INFO'}, "Extracted Mesh.")

        return {'FINISHED'}

class DB_Generate_HP(Operator):
    """Adds a subdivision modifier and applies additional settings to help create a high-poly mesh."""

    bl_idname = "scene.db_generatehp"
    bl_label = "Generate HP"

    def execute(self, context):
        print(self)

        #Generate HP
        bpy.ops.object.mode_set(mode = 'OBJECT')

        for obj in bpy.context.selected_objects:

            bpy.context.scene.objects.active = obj

            bpy.ops.object.mode_set(mode = 'EDIT')
            bpy.ops.mesh.select_all(action = 'DESELECT')
            bpy.ops.mesh.edges_select_sharp(sharpness=0.525344)
            bpy.ops.mesh.bevel(offset=0.05, segments=2, profile=1, vertex_only=False)
            bpy.ops.mesh.select_all(action = 'DESELECT')
            bpy.ops.object.mode_set(mode = 'OBJECT')
            bpy.ops.object.subdivision_set(level=3)
            bpy.ops.object.shade_smooth()
            bpy.ops.object.mode_set(mode = 'OBJECT')

        self.report({'INFO'}, "High-Poly Mesh Prepared.")

        return {'FINISHED'}

class DB_Generate_LP(Operator):
    """Decimates and simplifies a high-poly mesh to a low-poly mesh."""

    bl_idname = "scene.db_generatelp"
    bl_label = "Generate LP"

    def execute(self, context):
        print(self)

        #Generate LP

        bpy.ops.object.mode_set(mode= 'OBJECT')

        bpy.ops.object.convert(target='MESH')

        bpy.ops.object.join()

        bpy.context.object.location[0]= 0
        bpy.ops.object.transform_apply(location=False,rotation=True, scale=False)

        bpy.ops.object.modifier_add(type='EDGE_SPLIT')
        bpy.context.object.modifiers["EdgeSplit"].split_angle = 0.525344
        bpy.ops.object.modifier_apply(apply_as='DATA', modifier="EdgeSplit")

        bpy.ops.object.mode_set(mode = 'EDIT')
        bpy.ops.mesh.reveal()
        bpy.ops.mesh.select_mode(type="EDGE")
        bpy.ops.mesh.select_all(action= 'SELECT')

        bpy.ops.mesh.region_to_loop()
        bpy.ops.mesh.mark_seam(clear=False)

        bpy.ops.mesh.select_all(action= 'SELECT')
        bpy.ops.mesh.dissolve_limited()

        bpy.ops.mesh.quads_convert_to_tris()
        bpy.ops.mesh.tris_convert_to_quads()

        bpy.ops.mesh.remove_doubles()

        bpy.ops.mesh.bisect(plane_co=(0,0, 0), plane_no=(1, 0, 0), clear_inner=True, clear_outer=False,xstart=376, xend=381, ystart=133, yend=62)

        bpy.ops.mesh.delete(type='FACE')

        bpy.ops.mesh.select_all(action= 'SELECT')

        bpy.ops.mesh.bisect(plane_co=(0,0, 0), plane_no=(1, 0, 0), clear_inner=True, clear_outer=False,xstart=376, xend=381, ystart=133, yend=62)
        bpy.ops.mesh.mark_seam(clear=False)

        bpy.ops.mesh.select_all(action= 'SELECT')
        bpy.ops.uv.unwrap(method='ANGLE_BASED',margin=0.02)
        bpy.ops.mesh.select_all(action= 'DESELECT')

        bpy.ops.object.mode_set(mode= 'OBJECT')
        bpy.ops.object.shade_smooth()

        bpy.ops.object.modifier_add(type='MIRROR')
        bpy.ops.object.modifier_apply(apply_as='DATA',modifier="Mirror")

        bpy.ops.object.modifier_add(type='SHRINKWRAP')
        bpy.context.object.modifiers["Shrinkwrap"].show_on_cage = True
        bpy.context.object.modifiers["Shrinkwrap"].use_keep_above_surface = True

        bpy.ops.object.modifier_add(type='EDGE_SPLIT')
        bpy.context.object.modifiers["EdgeSplit"].split_angle= 0.525344

        bpy.ops.object.mode_set(mode= 'EDIT')
        bpy.ops.mesh.select_all(action= 'SELECT')
        bpy.ops.mesh.normals_make_consistent(inside=False)

        bpy.ops.object.mode_set(mode= 'OBJECT')

        self.report({'INFO'}, "Low-Poly Mesh Prepared.")

        return {'FINISHED'}

class DB_Quick_Decimate(Operator):
    """Uses the decimate modifier with other settings to quickly decimate a mesh."""

    bl_idname = "scene.db_quickdecimate"
    bl_label = "Quick Decimate"

    def execute(self, context):
        print(self)

        #Quick Decimation
        bpy.ops.object.mode_set(mode = 'OBJECT')

        bpy.ops.object.convert(target='MESH')

        bpy.ops.object.mode_set(mode = 'EDIT')
        bpy.ops.mesh.select_all(action = 'SELECT')
        bpy.ops.mesh.remove_doubles()
        bpy.ops.mesh.normals_make_consistent(inside=False)

        bpy.ops.object.mode_set(mode = 'OBJECT')

        bpy.ops.object.modifier_add(type='DECIMATE')
        bpy.context.object.modifiers["Decimate"].ratio = 0.8
        bpy.context.object.modifiers["Decimate"].use_collapse_triangulate = True
        bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Decimate")

        bpy.ops.object.mode_set(mode = 'OBJECT')

        self.report({'INFO'}, "Mesh successfully decimated.")

        return {'FINISHED'}

class DB_ResymmetriseX(Operator):
    """...ill get back to you on that one."""

    bl_idname = "scene.db_resym_x"
    bl_label = "Rebuild Symmetry X"

    def execute(self, context):
        print(self)

        #Resym X
        bpy.ops.object.mode_set(mode = 'OBJECT')

        for obj in bpy.context.selected_objects:

            bpy.context.scene.objects.active = obj

            bpy.ops.object.transform_apply(location=True, rotation=True, scale=False)

            bpy.ops.object.mode_set(mode = 'EDIT')
            bpy.ops.mesh.select_all(action = 'SELECT')
            bpy.ops.mesh.bisect(plane_co=(0, 0, 0), plane_no=(1, 0, 0), clear_inner=True, clear_outer=False, xstart=376, xend=381, ystart=133, yend=62)

            bpy.ops.mesh.delete(type='FACE')

            bpy.ops.mesh.select_all(action= 'SELECT')

            bpy.ops.mesh.bisect(plane_co=(0,0, 0), plane_no=(1, 0, 0), clear_inner=True, clear_outer=False,xstart=376, xend=381, ystart=133, yend=62)

            bpy.ops.object.mode_set(mode = 'OBJECT')

            bpy.ops.object.modifier_add(type='MIRROR')
            bpy.context.object.modifiers["Mirror"].use_clip = True

            bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Mirror")

        self.report({'INFO'}, "Objects re-symmetrised.")

        return {'FINISHED'}

class DB_Quick_Retopo(Operator):
    """...ill get back to you on that one."""

    bl_idname = "scene.db_quickretopo"
    bl_label = "Quick Retopology"

    def execute(self, context):
        print(self)

        #Retopo
        bpy.ops.object.mode_set(mode = 'OBJECT')

        bpy.ops.object.mode_set(mode = 'OBJECT')

        bpy.ops.object.convert(target='MESH')

        bpy.ops.object.mode_set(mode = 'EDIT')
        bpy.ops.mesh.select_all(action = 'SELECT')
        bpy.ops.mesh.remove_doubles()
        bpy.ops.mesh.normals_make_consistent(inside=False)

        bpy.ops.object.mode_set(mode = 'OBJECT')

        bpy.context.scene.tool_settings.use_snap = True
        bpy.context.scene.tool_settings.snap_element = 'FACE'

        bpy.ops.object.modifier_add(type='WIREFRAME')
        bpy.context.object.modifiers["Wireframe"].show_in_editmode = True

        bpy.context.object.modifiers["Wireframe"].thickness = 0.0015
        bpy.context.object.modifiers["Wireframe"].offset = 15
        bpy.context.object.modifiers["Wireframe"].use_boundary = True
        bpy.context.object.modifiers["Wireframe"].use_replace = False

        bpy.ops.object.mode_set(mode = 'EDIT')
        bpy.ops.mesh.select_all(action = 'SELECT')
        bpy.ops.mesh.bisect(plane_co=(0, 0, 0), plane_no=(1, 0, 0), clear_inner=True, clear_outer=False, xstart=376, xend=381, ystart=133, yend=62)

        bpy.ops.mesh.delete(type='FACE')

        bpy.ops.mesh.select_all(action= 'SELECT')

        bpy.ops.mesh.bisect(plane_co=(0,0, 0), plane_no=(1, 0, 0), clear_inner=True, clear_outer=False,xstart=376, xend=381, ystart=133, yend=62)

        bpy.ops.mesh.select_all(action = 'DESELECT')

        bpy.ops.object.mode_set(mode = 'OBJECT')

        bpy.ops.object.modifier_add(type='MIRROR')
        bpy.context.object.modifiers["Mirror"].use_clip = True
        bpy.context.object.modifiers["Mirror"].show_in_editmode = False

        bpy.context.object.name = "Retopo"

        self.report({'INFO'}, "Retopology Complete.")

        return {'FINISHED'}

class DB_Unfold_Half(Operator):
    """...ill get back to you on that one."""

    bl_idname = "scene.db_unfoldhalf"
    bl_label = "Unfold Half"

    def execute(self, context):
        print(self)

        #Unfold Half
        bpy.ops.object.mode_set(mode = 'OBJECT')

        for obj in bpy.context.selected_objects:

            bpy.context.scene.objects.active = obj

            bpy.context.object.location[0] = 0

            bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
            bpy.ops.object.mode_set(mode = 'EDIT')
            bpy.ops.mesh.select_all(action = 'SELECT')
            bpy.ops.mesh.bisect(plane_co=(0, 0, 0), plane_no=(1, 0, 0), clear_inner=True, clear_outer=False, xstart=376, xend=381, ystart=133, yend=62)

            bpy.ops.mesh.delete(type='FACE')

            bpy.ops.mesh.select_all(action= 'SELECT')

            bpy.ops.mesh.bisect(plane_co=(0,0, 0), plane_no=(1, 0, 0), clear_inner=True, clear_outer=False,xstart=376, xend=381, ystart=133, yend=62)

            bpy.ops.mesh.mark_seam(clear=False)
            bpy.ops.mesh.select_all(action = 'SELECT')
            bpy.ops.uv.unwrap(method='ANGLE_BASED', margin=0.02)
            bpy.ops.mesh.select_all(action = 'DESELECT')

            bpy.ops.object.mode_set(mode = 'OBJECT')
            bpy.ops.object.modifier_add(type='MIRROR')
            bpy.context.object.modifiers["Mirror"].use_clip = True
            bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Mirror")

        self.report({'INFO'}, "Mesh Unfolded.")

        return {'FINISHED'}
