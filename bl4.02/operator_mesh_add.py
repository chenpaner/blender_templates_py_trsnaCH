#这段代码定义了一个名为"AddBox"的操作符，它用于在Blender中添加一个简单的立方体网格。具体来说，它的功能包括：

# 定义了一个名为"AddBox"的操作符类，继承自"bpy.types.Operator"和"AddObjectHelper"，用于添加立方体网格。
# 提供了用于指定立方体宽度、高度和深度的属性，并设置了它们的默认值、描述和取值范围。
# 实现了"execute"方法，在该方法中，通过调用"add_box"函数创建立方体的顶点和面，并使用"object_utils.object_data_add"函数将网格添加到场景中。
# 定义了"menu_func"函数，用于在Blender的"添加网格"菜单中添加"AddBox"操作符。
# 最后，注册了"AddBox"操作符类和"menu_func"函数，以便在Blender启动时生效，并提供了一个测试调用来演示如何在Blender中使用该操作符添加一个立方体网格。

import bpy
import bmesh
from bpy_extras.object_utils import AddObjectHelper

from bpy.props import (
    FloatProperty,
)


def add_box(width, height, depth):
    """
    此函数接受输入并返回顶点和面数组。
    此处不进行实际的网格数据创建。
    """

    verts = [
        (+1.0, +1.0, -1.0),
        (+1.0, -1.0, -1.0),
        (-1.0, -1.0, -1.0),
        (-1.0, +1.0, -1.0),
        (+1.0, +1.0, +1.0),
        (+1.0, -1.0, +1.0),
        (-1.0, -1.0, +1.0),
        (-1.0, +1.0, +1.0),
    ]

    faces = [
        (0, 1, 2, 3),
        (4, 7, 6, 5),
        (0, 4, 5, 1),
        (1, 5, 6, 2),
        (2, 6, 7, 3),
        (4, 0, 3, 7),
    ]

    # 应用大小
    for i, v in enumerate(verts):
        verts[i] = v[0] * width, v[1] * depth, v[2] * height

    return verts, faces


class AddBox(bpy.types.Operator, AddObjectHelper):
    """添加简单的立方体网格"""
    bl_idname = "mesh.primitive_box_add"
    bl_label = "添加立方体"
    bl_options = {'REGISTER', 'UNDO'}

    width: FloatProperty(
        name="宽度",
        description="立方体宽度",
        min=0.01, max=100.0,
        default=1.0,
    )
    height: FloatProperty(
        name="高度",
        description="立方体高度",
        min=0.01, max=100.0,
        default=1.0,
    )
    depth: FloatProperty(
        name="深度",
        description="立方体深度",
        min=0.01, max=100.0,
        default=1.0,
    )

    def execute(self, context):

        verts_loc, faces = add_box(
            self.width,
            self.height,
            self.depth,
        )

        mesh = bpy.data.meshes.new("Box")

        bm = bmesh.new()

        for v_co in verts_loc:
            bm.verts.new(v_co)

        bm.verts.ensure_lookup_table()
        for f_idx in faces:
            bm.faces.new([bm.verts[i] for i in f_idx])

        bm.to_mesh(mesh)
        mesh.update()

        # 使用此实用模块将网格添加为对象到场景中
        from bpy_extras import object_utils
        object_utils.object_data_add(context, mesh, operator=self)

        return {'FINISHED'}


def menu_func(self, context):
    self.layout.operator(AddBox.bl_idname, icon='MESH_CUBE')


# 注册并添加到“添加网格”菜单（需要使用 F3 搜索“添加立方体”以快速访问）。
def register():
    bpy.utils.register_class(AddBox)
    bpy.types.VIEW3D_MT_mesh_add.append(menu_func)


def unregister():
    bpy.utils.unregister_class(AddBox)
    bpy.types.VIEW3D_MT_mesh_add.remove(menu_func)


if __name__ == "__main__":
    register()

    # 测试调用
    bpy.ops.mesh.primitive_box_add()
