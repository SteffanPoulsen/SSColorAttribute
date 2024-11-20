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

bl_info = {
    "name": "Select Similar Attribute Color",
    "description": "Adds an option to select faces, edges, or vertices with a similar color attribute",
    "author": "ChatGPT & Steffan Poulsen",
    "version": (1, 0, 0),
    "blender": (4, 2, 0),
    "location": "View3D > Edit Mode > Select > Select Similar",
    "wiki_url": "https://github.com/SteffanPoulsen/SSAC",
    "tracker_url": "https://github.com/SteffanPoulsen/SSAC",
    "support": "COMMUNITY",
    "category": "Edit Mesh",
}

from . import select_similar_color_attribute  # Import your operator module

def register():
    select_similar_color_attribute.register()

def unregister():
    select_similar_color_attribute.unregister()