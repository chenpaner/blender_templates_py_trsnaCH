import bpy


class HelloWorldPanel(bpy.types.Panel):
    """在对象属性窗口中创建一个面板"""
    bl_label = "你好世界面板"
    bl_idname = "OBJECT_PT_hello"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"

    def draw(self, context):
        layout = self.layout

        obj = context.object

        row = layout.row()
        row.label(text="你好，世界！", icon='WORLD_DATA')

        row = layout.row()
        row.label(text="活动对象是：" + obj.name)
        row = layout.row()
        row.prop(obj, "name")

        row = layout.row()
        row.operator("mesh.primitive_cube_add")


def register():
    bpy.utils.register_class(HelloWorldPanel)


def unregister():
    bpy.utils.unregister_class(HelloWorldPanel)


if __name__ == "__main__":
    register()
