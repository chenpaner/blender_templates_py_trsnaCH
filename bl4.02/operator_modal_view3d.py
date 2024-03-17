#这段代码定义了一个模态操作器 ViewOperator，
#用于在3D视图中使用鼠标事件平移视图。操作器可通过在视图菜单中添加快捷方式或使用F3搜索功能来调用。

import bpy
from mathutils import Vector
from bpy.props import FloatVectorProperty


class ViewOperator(bpy.types.Operator):
    """使用鼠标事件平移视图"""
    bl_idname = "view3d.modal_operator"
    bl_label = "简单视图操作器"

    offset: FloatVectorProperty(
        name="偏移量",
        size=3,
    )

    def execute(self, context):
        v3d = context.space_data
        rv3d = v3d.region_3d

        rv3d.view_location = self._initial_location + Vector(self.offset)

    def modal(self, context, event):
        v3d = context.space_data
        rv3d = v3d.region_3d

        if event.type == 'MOUSEMOVE':
            self.offset = (self._initial_mouse - Vector((event.mouse_x, event.mouse_y, 0.0))) * 0.02
            self.execute(context)
            context.area.header_text_set("偏移量 %.4f %.4f %.4f" % tuple(self.offset))

        elif event.type == 'LEFTMOUSE':
            context.area.header_text_set(None)
            return {'FINISHED'}

        elif event.type in {'RIGHTMOUSE', 'ESC'}:
            rv3d.view_location = self._initial_location
            context.area.header_text_set(None)
            return {'CANCELLED'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):

        if context.space_data.type == 'VIEW_3D':
            v3d = context.space_data
            rv3d = v3d.region_3d

            if rv3d.view_perspective == 'CAMERA':
                rv3d.view_perspective = 'PERSP'

            self._initial_mouse = Vector((event.mouse_x, event.mouse_y, 0.0))
            self._initial_location = rv3d.view_location.copy()

            context.window_manager.modal_handler_add(self)
            return {'RUNNING_MODAL'}
        else:
            self.report({'WARNING'}, "活动空间必须为 View3d")
            return {'CANCELLED'}


def menu_func(self, context):
    self.layout.operator(ViewOperator.bl_idname, text="简单视图模态操作器")


# 注册并添加到“视图”菜单（还需使用 F3 搜索“简单视图模态操作器”进行快速访问）。
def register():
    bpy.utils.register_class(ViewOperator)
    bpy.types.VIEW3D_MT_view.append(menu_func)


def unregister():
    bpy.utils.unregister_class(ViewOperator)
    bpy.types.VIEW3D_MT_view.remove(menu_func)


if __name__ == "__main__":
    register()
