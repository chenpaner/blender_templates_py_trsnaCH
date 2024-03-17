#这段代码定义了一个操作器 UvOperator，
#它用于在编辑模式下将网格对象的顶点坐标映射到 UV 坐标。操作器可通过在 UV 菜单中添加快捷方式或使用 F3 搜索功能来调用。

import bpy
import bmesh

def main(context):
    obj = context.active_object
    me = obj.data
    bm = bmesh.from_edit_mesh(me)

    # 确保 UV 层存在
    uv_layer = bm.loops.layers.uv.verify()

    # 调整 UV 坐标
    for face in bm.faces:
        for loop in face.loops:
            loop_uv = loop[uv_layer]
            # 将顶点的 xy 位置用作 UV 坐标
            loop_uv.uv = loop.vert.co.xy

    bmesh.update_edit_mesh(me)


class UvOperator(bpy.types.Operator):
    """UV 操作器描述"""
    bl_idname = "uv.simple_operator"
    bl_label = "简单 UV 操作器"

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return obj and obj.type == 'MESH' and obj.mode == 'EDIT'

    def execute(self, context):
        main(context)
        return {'FINISHED'}


def menu_func(self, context):
    self.layout.operator(UvOperator.bl_idname, text="简单 UV 操作器")


# 注册并添加到“UV”菜单（还需要使用 F3 搜索“简单 UV 操作器”以快速访问）。
def register():
    bpy.utils.register_class(UvOperator)
    bpy.types.IMAGE_MT_uvs.append(menu_func)


def unregister():
    bpy.utils.unregister_class(UvOperator)
    bpy.types.IMAGE_MT_uvs.remove(menu_func)


if __name__ == "__main__":
    register()

    # 测试调用
    bpy.ops.uv.simple_operator()
