import bpy
from bpy.types import Menu

# 生成一个编辑模式选择饼菜单（在对象处于编辑模式时运行以获取有效输出）


class VIEW3D_MT_PIE_template(Menu):
    # 标签显示在饼菜单中心。
    bl_label = "选择模式"

    def draw(self, context):
        layout = self.layout

        pie = layout.menu_pie()
        # operator_enum 只会将操作符的类型枚举中的所有可用选项分散在饼菜单上
        pie.operator_enum("mesh.select_mode", "type")


def register():
    bpy.utils.register_class(VIEW3D_MT_PIE_template)


def unregister():
    bpy.utils.unregister_class(VIEW3D_MT_PIE_template)


if __name__ == "__main__":
    register()

    bpy.ops.wm.call_menu_pie(name="VIEW3D_MT_PIE_template")
