# 这段代码实现了一个简单的文件导入功能，具体包括：
# - 'read_some_data'函数：负责从文件中读取数据的函数。它接受Blender上下文、文件路径和一个布尔值作为参数，并在控制台打印读取到的数据。
# - 'ImportSomeData'类：定义了一个导入数据的操作符。这个类继承自'Operator'和'ImportHelper'，因此它具有文件选择器等导入功能。该类包含了一系列属性，如文件名、导入设置等，并实现了'execute'方法，该方法调用了'read_some_data'函数来读取文件数据。
# - 'menu_func_import'函数：用于在顶部栏文件菜单中添加"Text Import Operator"菜单项，用户可以通过此菜单项来调用文件导入操作符。
# - 'register'和'unregister'函数：用于注册和取消注册导入数据的操作符类，并将菜单项添加到文件导入菜单中。
# 最后，通过'if __name__ == "__main__":'部分注册了导入数据的操作符，以便在Blender启动时生效，并提供了一个测试调用来演示如何使用该操作符进行文件导入。

# 导入必要的模块
import bpy
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy.types import Operator

# 定义读取数据的函数
def read_some_data(context, filepath, use_some_setting):
    print("运行 read_some_data 函数...")
    # 打开文件并读取数据
    f = open(filepath, 'r', encoding='utf-8')
    data = f.read()
    f.close()

    # 通常在此处加载数据
    print(data)

    return {'FINISHED'}


class ImportSomeData(Operator, ImportHelper):
    """导入一些数据"""
    bl_idname = "import_test.some_data"  # 操作符的唯一标识符
    bl_label = "导入一些数据"

    # 文件选择器相关属性
    filename_ext = ".txt"
    filter_glob: StringProperty(
        default="*.txt",
        options={'HIDDEN'},
        maxlen=255,  # 最大长度限制
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

    # 执行导入操作
    def execute(self, context):
        return read_some_data(context, self.filepath, self.use_setting)


# 添加到动态菜单
def menu_func_import(self, context):
    self.layout.operator(ImportSomeData.bl_idname, text="文本导入操作符")


# 注册导入操作符并添加到文件导入菜单中
def register():
    bpy.utils.register_class(ImportSomeData)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)


# 注销操作符并移除菜单项
def unregister():
    bpy.utils.unregister_class(ImportSomeData)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)


# 主程序入口，注册操作符并调用测试
if __name__ == "__main__":
    register()

    # 测试调用
    bpy.ops.import_test.some_data('INVOKE_DEFAULT')

