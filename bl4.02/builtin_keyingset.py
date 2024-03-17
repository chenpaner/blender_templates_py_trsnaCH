#这段代码定义了一个名为 "Hello World KeyingSet" 的键集（KeyingSet），它会将一些属性路径添加到键集中
#这个键集类会将位置属性路径、五个图层属性路径和一个 show_in_front 属性路径添加到键集中。
import bpy

# 定义一个名为 BUILTIN_KSI_hello 的键集类
class BUILTIN_KSI_hello(bpy.types.KeyingSetInfo):
    bl_label = "Hello World KeyingSet"  # 键集的标签

    # poll - 检查是否可以使用键集
    def poll(ksi, context):
        return context.active_object or context.selected_objects  # 检查是否有活动对象或选定对象

    # iterator - 遍历所有相关的数据，调用 generate()
    def iterator(ksi, context, ks):
        for ob in context.selected_objects:
            ksi.generate(context, ks, ob)  # 调用 generate() 方法生成属性路径

    # generator - 向键集中填充要使用的属性路径
    def generate(ksi, context, ks, data):
        id_block = data.id_data

        # 添加属性路径到键集中
        ks.paths.add(id_block, "location")  # 添加 "location" 属性路径

        # 添加五个 "layers" 属性路径，使用 'NAMED' 方法和指定的组名
        for i in range(5):
            ks.paths.add(id_block, "layers", i, group_method='NAMED', group_name="5x Hello Layers")

        # 添加 "show_in_front" 属性路径，使用 'NONE' 方法


# 注册键集类
def register():
    bpy.utils.register_class(BUILTIN_KSI_hello)


# 注销键集类
def unregister():
    bpy.utils.unregister_class(BUILTIN_KSI_hello)


if __name__ == '__main__':
    register()  # 在脚本作为独立程序运行时注册键集类
