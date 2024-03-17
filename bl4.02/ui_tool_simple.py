import bpy
from bpy.types import WorkSpaceTool


# 这个示例在工具栏中添加了一个对象模式工具。
# 这只是圆形选择和套索工具。
class MyTool(WorkSpaceTool):
    # 工具的空间类型为 VIEW_3D，上下文模式为 OBJECT
    bl_space_type = 'VIEW_3D'
    bl_context_mode = 'OBJECT'

    # 工具的唯一标识符，以你的插件名称为前缀
    bl_idname = "my_template.my_circle_select"
    # 工具在工具栏中显示的名称
    bl_label = "我的圆形选择"
    # 工具的描述，显示为工具提示
    bl_description = (
        "这是一个工具提示\n"
        "包含多行"
    )
    # 工具的图标
    bl_icon = "ops.generic.select_circle"
    # 工具不使用小部件
    bl_widget = None
    # 工具的键盘映射
    bl_keymap = (
        ("view3d.select_circle", {"type": 'LEFTMOUSE', "value": 'PRESS'},
         {"properties": [("wait_for_input", False)]}),
        ("view3d.select_circle", {"type": 'LEFTMOUSE', "value": 'PRESS', "ctrl": True},
         {"properties": [("mode", 'SUB'), ("wait_for_input", False)]}),
    )

    # 绘制工具设置面板
    def draw_settings(context, layout, tool):
        props = tool.operator_properties("view3d.select_circle")
        layout.prop(props, "mode")
        layout.prop(props, "radius")


# 定义另一个工具类，表示另一个自定义工具
class MyOtherTool(WorkSpaceTool):
    # 工具的空间类型为 VIEW_3D，上下文模式为 OBJECT
    bl_space_type = 'VIEW_3D'
    bl_context_mode = 'OBJECT'

    # 工具的唯一标识符，以你的插件名称为前缀
    bl_idname = "my_template.my_other_select"
    # 工具在工具栏中显示的名称
    bl_label = "我的套索选择工具"
    # 工具的描述，显示为工具提示
    bl_description = (
        "这是一个工具提示\n"
        "包含多行"
    )
    # 工具的图标
    bl_icon = "ops.generic.select_lasso"
    # 工具不使用小部件
    bl_widget = None
    # 工具的键盘映射
    bl_keymap = (
        ("view3d.select_lasso", {"type": 'LEFTMOUSE', "value": 'PRESS'}, None),
        ("view3d.select_lasso", {"type": 'LEFTMOUSE', "value": 'PRESS', "ctrl": True},
         {"properties": [("mode", 'SUB')]}),
    )

    # 绘制工具设置面板
    def draw_settings(context, layout, tool):
        props = tool.operator_properties("view3d.select_lasso")
        layout.prop(props, "mode")


# 定义另一个工具类，表示另一个自定义工具
class MyWidgetTool(WorkSpaceTool):
    # 工具的空间类型为 VIEW_3D，上下文模式为 OBJECT
    bl_space_type = 'VIEW_3D'
    bl_context_mode = 'OBJECT'

    # 工具的唯一标识符，以你的插件名称为前缀
    bl_idname = "my_template.my_gizmo_translate"
    # 工具在工具栏中显示的名称
    bl_label = "我的小部件工具"
    # 工具的描述，显示为工具提示
    bl_description = "简短描述"
    # 工具的图标
    bl_icon = "ops.transform.translate"
    # 工具使用的小部件
    bl_widget = "VIEW3D_GGT_tool_generic_handle_free"
    # 小部件的属性
    bl_widget_properties = [
        ("radius", 75.0),
        ("backdrop_fill_alpha", 0.0),
    ]
    # 工具的键盘映射
    bl_keymap = (
        ("transform.translate", {"type": 'LEFTMOUSE', "value": 'PRESS'}, None),
    )

    # 绘制工具设置面板
    def draw_settings(context, layout, tool):
        props = tool.operator_properties("transform.translate")
        layout.prop(props, "mode")


# 注册自定义工具
def register():
    bpy.utils.register_tool(MyTool, after={"builtin.scale_cage"}, separator=True, group=True)
    bpy.utils.register_tool(MyOtherTool, after={MyTool.bl_idname})
    bpy.utils.register_tool(MyWidgetTool, after={MyTool.bl_idname})


# 注销自定义工具
def unregister():
    bpy.utils.unregister_tool(MyTool)
    bpy.utils.unregister_tool(MyOtherTool)
    bpy.utils.unregister_tool(MyWidgetTool)


if __name__ == "__main__":
    register()
