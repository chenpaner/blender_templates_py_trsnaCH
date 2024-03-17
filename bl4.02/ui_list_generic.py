# 这段代码的作用是创建了一个自定义的面板（Panel），面板中包含一个自定义的列表（List），该列表显示了场景中的自定义属性组（Property Group）。具体来说，代码做了以下几件事情：
# 定义了一个名为 MyPropGroup 的自定义属性组，其中包含一个名为 name 的字符串属性。
# 定义了一个名为 MyPanel 的自定义面板，面板用于在 3D 视图中显示。该面板包含了一个自定义列表，用于显示场景中的自定义属性组。
# 使用 bpy.utils.register_classes_factory 函数注册了自定义类 MyPropGroup 和 MyPanel。
# 在 register 函数中注册了自定义属性组的集合属性 my_list 和一个整数属性 my_list_active_index 到场景中。
# 在 unregister 函数中取消注册了自定义属性组的集合属性。
# 综上所述，该代码创建了一个自定义面板，使用户能够在 3D 视图中管理场景中的自定义属性组

import bpy
from bl_ui.generic_ui_list import draw_ui_list


class MyPropGroup(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty()


class MyPanel(bpy.types.Panel):
    bl_label = "My Label"
    bl_idname = "SCENE_PT_list_demo"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "My Category"

    def draw(self, context):
        layout = self.layout
        # 使用通用的 UI 列表绘制函数来绘制自定义列表
        draw_ui_list(
            layout,
            context,
            list_path="scene.my_list",
            active_index_path="scene.my_list_active_index",
            unique_id="my_list_id",
        )


# 将所有的类组合成一个列表，方便注册
classes = [
    MyPropGroup,
    MyPanel
]

# 使用工厂函数来注册和取消注册类
class_register, class_unregister = bpy.utils.register_classes_factory(classes)


def register():
    class_register()
    # 在场景中添加自定义列表的集合属性
    bpy.types.Scene.my_list = bpy.props.CollectionProperty(type=MyPropGroup)
    bpy.types.Scene.my_list_active_index = bpy.props.IntProperty()


def unregister():
    class_unregister()
    # 删除场景中的自定义列表集合属性
    del bpy.types.Scene.my_list
    del bpy.types.Scene.my_list_active_index


register()
