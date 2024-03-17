#这段代码定义了自定义节点树（MyCustomTree）、自定义节点（MyCustomNode）、自定义节点插座（MyCustomSocket）等，
#并创建了自定义节点类别（MyNodeCategory）以在Blender的节点编辑器中进行展示。
import bpy
from bpy.types import NodeTree, Node, NodeSocket, NodeTreeInterfaceSocket
import nodeitems_utils
from nodeitems_utils import NodeCategory, NodeItem

# 自定义节点树
class MyCustomTree(NodeTree):
    # 描述字符串
    '''自定义节点树类型，将显示在编辑器类型列表中'''
    # 可选的标识符字符串，如果未明确定义，则使用 Python 类名。
    bl_idname = 'CustomTreeType'
    # 漂亮名称显示的标签
    bl_label = "自定义节点树"
    # 图标标识符
    bl_icon = 'NODETREE'

# 自定义节点插座类型
class MyCustomSocket(NodeSocket):
    # 描述字符串
    """自定义节点插座类型"""
    # 可选的标识符字符串，如果未明确定义，则使用 Python 类名。
    bl_idname = 'CustomSocketType'
    # 漂亮名称显示的标签
    bl_label = "自定义节点插座"

    input_value: bpy.props.FloatProperty(
        name="Value",
        description="未连接时的值",
    )

    # 可选的函数用于绘制插座输入值
    def draw(self, context, layout, node, text):
        if self.is_output or self.is_linked:
            layout.label(text=text)
        else:
            layout.prop(self, "input_value", text=text)

    # 插座颜色
    @classmethod
    def draw_color_simple(cls):
        return (1.0, 0.4, 0.216, 0.5)

# 自定义节点树界面插座类型
class MyCustomInterfaceSocket(NodeTreeInterfaceSocket):
    # 生成的插座类型
    bl_socket_idname = 'CustomSocketType'

    default_value: bpy.props.FloatProperty(default=1.0, description="新插座的默认输入值",)

    def draw(self, context, layout):
        # 显示界面属性
        layout.prop(self, "default_value")

    # 设置新创建的插座的属性
    def init_socket(self, node, socket, data_path):
        socket.input_value = self.default_value

    # 使用现有插座初始化组接口
    def from_socket(self, node, socket):
        # 插座的当前值成为默认值
        self.default_value = socket.input_value

# 自定义节点基类，用于所有自定义节点
# 定义一个用于启用实例化的 poll 函数
class MyCustomTreeNode:
    @classmethod
    def poll(cls, ntree):
        return ntree.bl_idname == 'CustomTreeType'

# 自定义节点
class MyCustomNode(MyCustomTreeNode, Node):
    # === 基础 ===
    # 描述字符串
    '''自定义节点'''
    # 可选的标识符字符串，如果未明确定义，则使用 Python 类名。
    bl_idname = 'CustomNodeType'
    # 漂亮名称显示的标签
    bl_label = "自定义节点"
    # 图标标识符
    bl_icon = 'SOUND'

    # === 自定义属性 ===
    # 这些工作原理与 ID 数据块中的自定义属性相同
    # 可以在 https://docs.blender.org/api/current/bpy.props.html 找到详细信息
    my_string_prop: bpy.props.StringProperty()
    my_float_prop: bpy.props.FloatProperty(default=3.1415926)

    # === 可选函数 ===
    # 初始化函数，在创建新节点时调用
    # 这是创建节点插座的最常见的地方，如下所示。
    # 注意：这与 Python 中的标准 __init__ 函数不同，
    #       后者是一个纯粹的内部 Python 方法，不为节点系统所知！
    def init(self, context):
        self.inputs.new('CustomSocketType', "Hello")
        self.inputs.new('NodeSocketFloat', "World")
        self.inputs.new('NodeSocketVector', "!")

        self.outputs.new('NodeSocketColor', "How")
        self.outputs.new('NodeSocketColor', "are")
        self.outputs.new('NodeSocketFloat', "you")

    # 复制函数，用于从现有节点初始化复制的节点
    def copy(self, node):
        print("Copying from node ", node)

    # 释放函数，在移除时进行清理
    def free(self):
        print("Removing node ", self, ", Goodbye!")

    # 节点上显示的额外按钮
    def draw_buttons(self, context, layout):
        layout.label(text="节点设置")
        layout.prop(self, "my_float_prop")

    # 侧边栏中的详细按钮
    # 如果未定义此函数，则使用 draw_buttons 函数
    def draw_buttons_ext(self, context, layout):
        layout.prop(self, "my_float_prop")
        # my_string_prop 按钮仅在侧边栏中可见
        layout.prop(self, "my_string_prop")

    # 可选：自定义标签
    # 显式用户标签会覆盖此，但此处可以动态定义标签
    def draw_label(self):
        return "我是一个自定义节点"

# 节点类别
class MyNodeCategory(NodeCategory):
    @classmethod
    def poll(cls, context):
        return context.space_data.tree_type == 'CustomTreeType'

# 所有节点类别的列表
node_categories = [
    MyNodeCategory('SOMENODES', "一些节点", items=[
        # 我们的基本节点
        NodeItem("CustomNodeType"),
    ]),
    MyNodeCategory('OTHERNODES', "其他节点", items=[
        # 节点项可以有附加设置，将应用于新节点
        # 注意：设置值存储为字符串表达式，
        #      因此应使用 repr() 将其转换为字符串
        NodeItem("CustomNodeType", label="节点 A", settings={
            "my_string_prop": repr("Lorem ipsum dolor sit amet"),
            "my_float_prop": repr(1.0),
        }),
        NodeItem("CustomNodeType", label="节点 B", settings={
            "my_string_prop": repr("consectetur adipisicing elit"),
            "my_float_prop": repr(2.0),
        }),
    ]),
]

# 注册函数
def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

    nodeitems_utils.register_node_categories('CUSTOM_NODES', node_categories)

# 注销函数
def unregister():
    nodeitems_utils.unregister_node_categories('CUSTOM_NODES')

    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)

# 注册脚本为插件
if __name__ == "__main__":
    register()
