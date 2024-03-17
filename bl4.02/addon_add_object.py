# 插件信息
bl_info = {
    "name": "新对象",
    "author": "你的名字",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Add > Mesh > New Object",
    "description": "添加一个新的网格对象",
    "warning": "",
    "doc_url": "",
    "category": "添加网格",
}

import bpy
from bpy.types import Operator
from bpy.props import FloatVectorProperty
from bpy_extras.object_utils import AddObjectHelper, object_data_add
from mathutils import Vector

# 定义添加对象的函数
def add_object(self, context):
    scale_x = self.scale.x
    scale_y = self.scale.y

    # 定义顶点坐标
    verts = [
        Vector((-1 * scale_x, 1 * scale_y, 0)),
        Vector((1 * scale_x, 1 * scale_y, 0)),
        Vector((1 * scale_x, -1 * scale_y, 0)),
        Vector((-1 * scale_x, -1 * scale_y, 0)),
    ]

    edges = []
    faces = [[0, 1, 2, 3]]

    # 创建新的网格对象
    mesh = bpy.data.meshes.new(name="New Object Mesh")
    mesh.from_pydata(verts, edges, faces)
    # 在开发中检查网格是否有效
    # mesh.validate(verbose=True)
    object_data_add(context, mesh, operator=self)

# 定义添加对象的操作类
class OBJECT_OT_add_object(Operator, AddObjectHelper):
    """创建一个新的网格对象"""
    bl_idname = "mesh.add_object"
    bl_label = "Add Mesh Object"
    bl_options = {'REGISTER', 'UNDO'}

    scale: FloatVectorProperty(
        name="scale",
        default=(1.0, 1.0, 1.0),
        subtype='TRANSLATION',
        description="缩放",
    )

    def execute(self, context):
        add_object(self, context)
        return {'FINISHED'}

# 注册按钮
def add_object_button(self, context):
    self.layout.operator(
        OBJECT_OT_add_object.bl_idname,
        text="Add Object",
        icon='PLUGIN')

# 添加对象的手册链接
def add_object_manual_map():
    url_manual_prefix = "https://docs.blender.org/manual/en/latest/"
    url_manual_mapping = (
        ("bpy.ops.mesh.add_object", "scene_layout/object/types.html"),
    )
    return url_manual_prefix, url_manual_mapping

# 注册插件
def register():
    bpy.utils.register_class(OBJECT_OT_add_object)
    bpy.utils.register_manual_map(add_object_manual_map)
    bpy.types.VIEW3D_MT_mesh_add.append(add_object_button)

# 取消注册插件
def unregister():
    bpy.utils.unregister_class(OBJECT_OT_add_object)
    bpy.utils.unregister_manual_map(add_object_manual_map)
    bpy.types.VIEW3D_MT_mesh_add.remove(add_object_button)

if __name__ == "__main__":
    register()
