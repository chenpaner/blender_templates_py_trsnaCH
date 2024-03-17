#这段代码定义了一个模态操作器 ModalDrawOperator，
#它允许在3D视图中用鼠标绘制线条。操作器可通过在视图菜单中添加快捷方式或使用F3搜索功能来调用。

import bpy
import blf
import gpu
from gpu_extras.batch import batch_for_shader

def draw_callback_px(self, context):
    print("鼠标点数", len(self.mouse_path))

    font_id = 0  # XXX, 需要找出最佳方式来获取此值。

    # 绘制一些文本
    blf.position(font_id, 15, 30, 0)
    blf.size(font_id, 20.0)
    blf.draw(font_id, "你好世界 " + str(len(self.mouse_path)))

    # 50% alpha, 2像素宽的线
    shader = gpu.shader.from_builtin('UNIFORM_COLOR')
    gpu.state.blend_set('ALPHA')
    gpu.state.line_width_set(2.0)
    batch = batch_for_shader(shader, 'LINE_STRIP', {"pos": self.mouse_path})
    shader.uniform_float("color", (0.0, 0.0, 0.0, 0.5))
    batch.draw(shader)

    # 恢复 OpenGL 默认设置
    gpu.state.line_width_set(1.0)
    gpu.state.blend_set('NONE')


class ModalDrawOperator(bpy.types.Operator):
    """使用鼠标绘制线条"""
    bl_idname = "view3d.modal_draw_operator"
    bl_label = "简单模态 View3D 操作器"

    def modal(self, context, event):
        context.area.tag_redraw()

        if event.type == 'MOUSEMOVE':
            self.mouse_path.append((event.mouse_region_x, event.mouse_region_y))

        elif event.type == 'LEFTMOUSE':
            bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
            return {'FINISHED'}

        elif event.type in {'RIGHTMOUSE', 'ESC'}:
            bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
            return {'CANCELLED'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        if context.area.type == 'VIEW_3D':
            # 传递给回调函数的参数
            args = (self, context)
            # 添加区域 OpenGL 绘制回调
            # 使用 'POST_PIXEL' 在视图空间中绘制
            self._handle = bpy.types.SpaceView3D.draw_handler_add(draw_callback_px, args, 'WINDOW', 'POST_PIXEL')

            self.mouse_path = []

            context.window_manager.modal_handler_add(self)
            return {'RUNNING_MODAL'}
        else:
            self.report({'WARNING'}, "未找到 View3D，无法运行操作")
            return {'CANCELLED'}


def menu_func(self, context):
    self.layout.operator(ModalDrawOperator.bl_idname, text="模态绘制操作器")


def register():
    bpy.utils.register_class(ModalDrawOperator)
    bpy.types.VIEW3D_MT_view.append(menu_func)


def unregister():
    bpy.utils.unregister_class(ModalDrawOperator)
    bpy.types.VIEW3D_MT_view.remove(menu_func)


if __name__ == "__main__":
    register()
