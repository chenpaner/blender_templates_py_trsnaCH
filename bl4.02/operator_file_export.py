#这段代码实现了在 Blender 中添加一个自定义的导出操作符，可以将数据写入到一个文本文件中。具体功能包括：

# 1. 用户可以通过菜单或者搜索功能快速找到并使用该导出操作符。
# 2. 用户可以在导出时选择文件保存的路径和文件名。
# 3. 用户可以选择一些设置，如布尔值和枚举类型。
# 4. 用户执行导出操作后，会调用 `write_some_data` 函数将数据写入到指定的文本文件中。
# 5. 在执行导出操作时，会在控制台输出一条消息来确认操作已执行。
# 6. 如果用户取消了操作或者出现了错误，会在控制台输出相应的提示消息。


import bpy

# 定义写入数据的函数
def write_some_data(context, filepath, use_some_setting):
    print("运行 write_some_data 函数...")
    f = open(filepath, 'w', encoding='utf-8')
    f.write("你好，世界 %s" % use_some_setting)
    f.close()

    return {'FINISHED'}


# ExportHelper 是一个辅助类，定义了文件名和 invoke() 函数，用于调用文件选择器。
from bpy_extras.io_utils import ExportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy.types import Operator


class ExportSomeData(Operator, ExportHelper):
    """导出一些数据"""
    bl_idname = "export_test.some_data"  # 重要的是这是如何构造 bpy.ops.import_test.some_data 的标识符
    bl_label = "导出一些数据"

    # ExportHelper 混合类使用这些
    filename_ext = ".txt"

    filter_glob: StringProperty(
        default="*.txt",
        options={'HIDDEN'},
        maxlen=255,  # 最大内部缓冲区长度，更长会被截断。
    )

    # 操作符的属性
    use_setting: BoolProperty(
        name="示例布尔值",
        description="示例工具提示",
        default=True,
    )

    type: EnumProperty(
        name="示例枚举",
        description="在两个选项之间进行选择",
        items=(
            ('OPT_A', "第一个选项", "描述一"),
            ('OPT_B', "第二个选项", "描述二"),
        ),
        default='OPT_A',
    )

    # 执行导出操作
    def execute(self, context):
        return write_some_data(context, self.filepath, self.use_setting)


# 添加到动态菜单
def menu_func_export(self, context):
    self.layout.operator(ExportSomeData.bl_idname, text="文本导出操作符")


# 注册并添加到“文件选择器”菜单中（需要使用 F3 搜索“文本导出操作符”快速访问）。
def register():
    bpy.utils.register_class(ExportSomeData)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)


# 注销并移除菜单项
def unregister():
    bpy.utils.unregister_class(ExportSomeData)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)


# 主程序入口，注册操作符并调用测试
if __name__ == "__main__":
    register()

    # 测试调用
    bpy.ops.export_test.some_data('INVOKE_DEFAULT')
