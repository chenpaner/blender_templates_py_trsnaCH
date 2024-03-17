# 这个示例脚本演示了如何在按钮或菜单项上放置自定义图标。

# 重要提示：如果你运行这个示例，按钮中将没有图标。
# 你需要用真实存在的图标路径替换图像路径。
# 对于可分发的脚本，建议将图标放置在插件文件夹内，并相对于 py 脚本文件访问它以实现可移植性。

# 其他 UI 预览的用例：
# - 提供一个固定的预览列表进行选择
# - 提供一个动态的预览列表（例如从读取目录计算而来）

# 对于上述用例，请参见模板 'ui_previews_dynamic_enum.py'


import os
import bpy


class PreviewsExamplePanel(bpy.types.Panel):
    """在对象属性窗口中创建一个面板"""
    bl_label = "预览示例面板"
    bl_idname = "OBJECT_PT_previews"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"

    def draw(self, context):
        layout = self.layout
        pcoll = preview_collections["main"]

        row = layout.row()
        my_icon = pcoll["my_icon"]
        row.operator("render.render", icon_value=my_icon.icon_id)

        # my_icon.icon_id 可以在接受 icon_value 的任何 UI 函数中使用
        # 尝试将 text="" 也设置为获取仅图标的操作按钮


# 我们可以在此处存储多个预览集合，
# 但在此示例中，我们仅存储 "main"
preview_collections = {}


def register():

    # 请注意，由 bpy.utils.previews 返回的预览集合是常规的 Python 对象 - 您可以使用它们存储自定义数据。
    import bpy.utils.previews
    pcoll = bpy.utils.previews.new()

    # 图标所在文件夹的路径
    # 路径相对于插件文件夹内的此 py 文件计算
    my_icons_dir = os.path.join(os.path.dirname(__file__), "icons")

    # 加载文件的预览缩略图并存储在预览集合中
    pcoll.load("my_icon", os.path.join(my_icons_dir, "icon-image.png"), 'IMAGE')

    preview_collections["main"] = pcoll

    bpy.utils.register_class(PreviewsExamplePanel)


def unregister():

    for pcoll in preview_collections.values():
        bpy.utils.previews.remove(pcoll)
    preview_collections.clear()

    bpy.utils.unregister_class(PreviewsExamplePanel)


if __name__ == "__main__":
    register()
