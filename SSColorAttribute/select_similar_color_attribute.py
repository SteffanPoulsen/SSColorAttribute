# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

import bpy
import bmesh
from mathutils import Vector

class SelectSimilarColor(bpy.types.Operator):
    """Select elements with similar Color Attributes"""
    bl_idname = "mesh.select_similar_color"
    bl_label = "Select Similar Color Attribute"
    bl_options = {'REGISTER', 'UNDO'}

    threshold: bpy.props.FloatProperty(
        name="Color Threshold",
        default=0.01,
        min=0.0,
        max=1.0,
        description="Threshold for color similarity"
    )

    def execute(self, context):
        obj = context.active_object
        if obj is None or obj.mode != 'EDIT' or obj.type != 'MESH':
            self.report({'WARNING'}, "Must be in Edit mode with a mesh selected")
            return {'CANCELLED'}

        # Get mesh and bmesh
        mesh = obj.data
        bm = bmesh.from_edit_mesh(mesh)
        color_layer = bm.loops.layers.color.active

        if not color_layer:
            self.report({'WARNING'}, "No active color layer found")
            return {'CANCELLED'}

        # Determine selection mode
        select_mode = context.tool_settings.mesh_select_mode
        active_color = None

        # Handle Vertex Mode
        if select_mode[0]:  # Vertex mode
            for vert in bm.verts:
                if vert.select:
                    # Use the first selected vertex's loop color as the active color
                    active_color = Vector(vert.link_loops[0][color_layer][:3])
                    break

            if active_color is None:
                self.report({'WARNING'}, "No active vertex with color found")
                return {'CANCELLED'}

            # Compare and select vertices
            for vert in bm.verts:
                select_vertex = False
                for loop in vert.link_loops:
                    loop_color = Vector(loop[color_layer][:3])  # Get loop color
                    color_diff = (active_color - loop_color).length
                    if color_diff <= self.threshold:
                        select_vertex = True
                        break  # No need to check further loops for this vertex
                vert.select = select_vertex


        # Handle Edge Mode
        elif select_mode[1]:  # Edge mode
            for edge in bm.edges:
                if edge.select:
                    # Use the first selected edge's average loop color as the active color
                    active_colors = [
                        Vector(loop[color_layer][:3]) for loop in edge.link_loops
                    ]
                    active_color = sum(active_colors, Vector((0, 0, 0))) / len(active_colors)
                    break

            if active_color is None:
                self.report({'WARNING'}, "No active edge with color found")
                return {'CANCELLED'}

            # Compare and select edges
            for edge in bm.edges:
                select_edge = False
                for loop in edge.link_loops:
                    loop_color = Vector(loop[color_layer][:3])  # Get loop color
                    color_diff = (active_color - loop_color).length
                    if color_diff <= self.threshold:
                        select_edge = True
                        break  # No need to check further loops for this edge
                edge.select = select_edge


        # Handle Face Mode
        elif select_mode[2]:  # Face mode
            for face in bm.faces:
                if face.select:
                    active_color = Vector(face.loops[0][color_layer][:3])  # Convert RGB to Vector
                    break

            if active_color is None:
                self.report({'WARNING'}, "No active face with color found")
                return {'CANCELLED'}

            # Compare and select faces
            for face in bm.faces:
                face_color = Vector(face.loops[0][color_layer][:3])  # Convert RGB to Vector
                color_diff = (active_color - face_color).length
                if color_diff <= self.threshold:
                    face.select = True
                else:
                    face.select = False

        # Update the mesh
        bmesh.update_edit_mesh(mesh)
        return {'FINISHED'}


# Append the operator to the "Select Similar" menu
def menu_func(self, context):
    self.layout.operator(
        SelectSimilarColor.bl_idname, text="Color Attribute", icon='COLOR')


def register():
    bpy.utils.register_class(SelectSimilarColor)
    bpy.types.VIEW3D_MT_edit_mesh_select_similar.append(menu_func)


def unregister():
    bpy.utils.unregister_class(SelectSimilarColor)
    bpy.types.VIEW3D_MT_edit_mesh_select_similar.remove(menu_func)


if __name__ == "__main__":
    register()
