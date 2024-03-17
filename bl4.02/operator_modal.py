#这段代码定义了一个模态操作器 ModalOperator，它允许用户使用鼠标移动选定的对象。该操作器可通过在视图菜单中添加快捷方式或使用 F3 搜索功能来调用。


import bpy
from bpy.props import IntProperty, FloatProperty

class ModalOperator(bpy.types.Operator):
    """使用鼠标移动对象的示例"""
    bl_idname = "object.modal_operator"
    bl_label = "简单模态操作器"

    first_mouse_x: IntProperty()
    first_value: FloatProperty()

    def modal(self, context, event):
        if event.type == 'MOUSEMOVE':
            delta = self.first_mouse_x - event.mouse_x
            context.object.location.x = self.first_value + delta * 0.01

        elif event.type == 'LEFTMOUSE':
            return {'FINISHED'}

        elif event.type in {'RIGHTMOUSE', 'ESC'}:
            context.object.location.x = self.first_value
            return {'CANCELLED'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        if context.object:
            self.first_mouse_x = event.mouse_x
            self.first_value = context.object.location.x

            context.window_manager.modal_handler_add(self)
            return {'RUNNING_MODAL'}
        else:
            self.report({'WARNING'}, "没有活动对象，无法完成操作")
            return {'CANCELLED'}


def menu_func(self, context):
    self.layout.operator(ModalOperator.bl_idname, text=ModalOperator.bl_label)


# 注册并添加到“视图”菜单（还需要使用 F3 搜索“简单模态操作器”以快速访问）。
def register():
    bpy.utils.register_class(ModalOperator)
    bpy.types.VIEW3D_MT_object.append(menu_func)


def unregister():
    bpy.utils.unregister_class(ModalOperator)
    bpy.types.VIEW3D_MT_object.remove(menu_func)


if __name__ == "__main__":
    register()

    # 测试调用
    bpy.ops.object.modal_operator('INVOKE_DEFAULT')
