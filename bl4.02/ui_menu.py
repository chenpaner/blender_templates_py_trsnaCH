import bpy


class CustomMenu(bpy.types.Menu):
    bl_label = "自定义菜单"
    bl_idname = "OBJECT_MT_custom_menu"

    def draw(self, context):
        layout = self.layout

        layout.operator("wm.open_mainfile")
        layout.operator("wm.save_as_mainfile").copy = True

        layout.operator("object.shade_smooth")

        layout.label(text="你好，世界！", icon='WORLD_DATA')

        # 使用操作符枚举属性填充子菜单
        layout.operator_menu_enum("object.select_by_type",
                                  property="type",
                                  text="按类型全选",
                                  )

        # 调用另一个菜单
        layout.operator("wm.call_menu", text="展开").name = "VIEW3D_MT_uv_map"


def draw_item(self, context):
    layout = self.layout
    layout.menu(CustomMenu.bl_idname)


def register():
    bpy.utils.register_class(CustomMenu)

    # 将菜单添加到主头部
    bpy.types.INFO_HT_header.append(draw_item)


def unregister():
    bpy.utils.unregister_class(CustomMenu)

    bpy.types.INFO_HT_header.remove(draw_item)


if __name__ == "__main__":
    register()

    # 也可以从脚本中调用菜单
    bpy.ops.wm.call_menu(name=CustomMenu.bl_idname)
