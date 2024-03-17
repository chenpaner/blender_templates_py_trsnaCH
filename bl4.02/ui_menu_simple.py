import bpy


class SimpleCustomMenu(bpy.types.Menu):
    bl_label = "简单自定义菜单"
    bl_idname = "OBJECT_MT_simple_custom_menu"

    def draw(self, context):
        layout = self.layout

        layout.operator("wm.open_mainfile")
        layout.operator("wm.save_as_mainfile")


def register():
    bpy.utils.register_class(SimpleCustomMenu)


def unregister():
    bpy.utils.unregister_class(SimpleCustomMenu)


if __name__ == "__main__":
    register()

    # 也可以从脚本中调用菜单
    bpy.ops.wm.call_menu(name=SimpleCustomMenu.bl_idname)
