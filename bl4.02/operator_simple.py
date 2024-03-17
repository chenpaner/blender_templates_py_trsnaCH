import bpy
#这段代码定义了一个名为 SimpleOperator 的操作器，
#用于在控制台打印当前场景中所有对象的名称。
#操作器可通过在对象菜单中添加快捷方式或使用F3搜索功能来调用。

def main(context):
    # 遍历场景中的所有对象并打印它们的名称
    for ob in context.scene.objects:
        print(ob)


class SimpleOperator(bpy.types.Operator):
    """简单的对象操作器"""
    bl_idname = "object.simple_operator"
    bl_label = "简单对象操作器"

    @classmethod
    def poll(cls, context):
        # 检查是否存在活动对象
        return context.active_object is not None

    def execute(self, context):
        # 执行主要功能
        main(context)
        return {'FINISHED'}


def menu_func(self, context):
    # 将操作添加到对象菜单中
    self.layout.operator(SimpleOperator.bl_idname, text=SimpleOperator.bl_label)


# 注册操作并添加到“对象”菜单中（也可使用F3搜索“Simple Object Operator”进行快速访问）。
def register():
    bpy.utils.register_class(SimpleOperator)
    bpy.types.VIEW3D_MT_object.append(menu_func)


def unregister():
    bpy.utils.unregister_class(SimpleOperator)
    bpy.types.VIEW3D_MT_object.remove(menu_func)


if __name__ == "__main__":
    register()

    # 测试调用
    bpy.ops.object.simple_operator()
