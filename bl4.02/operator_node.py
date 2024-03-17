import bpy
#这段代码定义了一个名为 NodeOperator 的操作器，
#用于在节点编辑器中连接两个节点。操作器可通过在节点菜单中添加快捷方式或使用F3搜索功能来调用。

def main(operator, context):
    space = context.space_data
    node_tree = space.node_tree
    node_active = context.active_node
    node_selected = context.selected_nodes

    # 现在我们有了上下文，执行一个简单的操作
    if node_active in node_selected:
        node_selected.remove(node_active)
    if len(node_selected) != 1:
        operator.report({'ERROR'}, "必须选择2个节点")
        return

    node_other, = node_selected

    # 现在我们有了两个要操作的节点
    if not node_active.inputs:
        operator.report({'ERROR'}, "活动节点没有输入")
        return

    if not node_other.outputs:
        operator.report({'ERROR'}, "选择的节点没有输出")
        return

    socket_in = node_active.inputs[0]
    socket_out = node_other.outputs[0]

    # 在两个节点之间建立连接
    node_link = node_tree.links.new(socket_in, socket_out)


class NodeOperator(bpy.types.Operator):
    """简单的节点操作器"""
    bl_idname = "node.simple_operator"
    bl_label = "简单节点操作器"

    @classmethod
    def poll(cls, context):
        space = context.space_data
        return space.type == 'NODE_EDITOR'

    def execute(self, context):
        main(self, context)
        return {'FINISHED'}


def menu_func(self, context):
    self.layout.operator(NodeOperator.bl_idname, text=NodeOperator.bl_label)


# 注册操作并添加到“节点”菜单中（也可使用F3搜索“Simple Node Operator”进行快速访问）。
def register():
    bpy.utils.register_class(NodeOperator)
    bpy.types.NODE_MT_node.append(menu_func)


def unregister():
    bpy.utils.unregister_class(NodeOperator)
    bpy.types.NODE_MT_node.remove(menu_func)


if __name__ == "__main__":
    register()
