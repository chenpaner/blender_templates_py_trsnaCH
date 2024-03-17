import bpy


class LayoutDemoPanel(bpy.types.Panel):
    """在属性编辑器的场景上下文中创建一个面板"""
    bl_label = "布局演示"
    bl_idname = "SCENE_PT_layout"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"

    def draw(self, context):
        layout = self.layout

        scene = context.scene

        # 创建一个简单的行。
        layout.label(text="简单行:")

        row = layout.row()
        row.prop(scene, "frame_start")
        row.prop(scene, "frame_end")

        # 创建一个行，其中的按钮是对齐的。
        layout.label(text="对齐行:")

        row = layout.row(align=True)
        row.prop(scene, "frame_start")
        row.prop(scene, "frame_end")

        # 使用分割布局创建两列。
        split = layout.split()

        # 第一列
        col = split.column()
        col.label(text="第一列:")
        col.prop(scene, "frame_end")
        col.prop(scene, "frame_start")

        # 第二列，对齐
        col = split.column(align=True)
        col.label(text="第二列:")
        col.prop(scene, "frame_start")
        col.prop(scene, "frame_end")

        # 大型渲染按钮
        layout.label(text="大按钮:")
        row = layout.row()
        row.scale_y = 3.0
        row.operator("render.render")

        # 不同大小的按钮在一行中
        layout.label(text="不同大小的按钮:")
        row = layout.row(align=True)
        row.operator("render.render")

        sub = row.row()
        sub.scale_x = 2.0
        sub.operator("render.render")

        row.operator("render.render")


def register():
    bpy.utils.register_class(LayoutDemoPanel)


def unregister():
    bpy.utils.unregister_class(LayoutDemoPanel)


if __name__ == "__main__":
    register()
