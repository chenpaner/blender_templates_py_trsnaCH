#这段代码定义了一个模态操作器 ModalTimerOperator，
#它会定时更新3D视图中的主题颜色。操作器可通过在视图菜单中添加快捷方式或使用F3搜索功能来调用。

import bpy

class ModalTimerOperator(bpy.types.Operator):
    """定时器驱动的操作器"""
    bl_idname = "wm.modal_timer_operator"
    bl_label = "模态定时器操作器"

    _timer = None

    def modal(self, context, event):
        if event.type in {'RIGHTMOUSE', 'ESC'}:
            self.cancel(context)
            return {'CANCELLED'}

        if event.type == 'TIMER':
            # 更改主题颜色，有点傻！
            color = context.preferences.themes[0].view_3d.space.gradients.high_gradient
            color.s = 1.0
            color.h += 0.01

        return {'PASS_THROUGH'}

    def execute(self, context):
        wm = context.window_manager
        self._timer = wm.event_timer_add(0.1, window=context.window)
        wm.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def cancel(self, context):
        wm = context.window_manager
        wm.event_timer_remove(self._timer)


def menu_func(self, context):
    self.layout.operator(ModalTimerOperator.bl_idname, text=ModalTimerOperator.bl_label)


def register():
    bpy.utils.register_class(ModalTimerOperator)
    bpy.types.VIEW3D_MT_view.append(menu_func)


# 注册并添加到“视图”菜单（还需使用 F3 搜索“模态定时器操作器”进行快速访问）。
def unregister():
    bpy.utils.unregister_class(ModalTimerOperator)
    bpy.types.VIEW3D_MT_view.remove(menu_func)


if __name__ == "__main__":
    register()

    # 测试调用
    bpy.ops.wm.modal_timer_operator()
