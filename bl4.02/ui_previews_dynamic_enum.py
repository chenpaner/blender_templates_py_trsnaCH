# 这个示例脚本演示了带有自定义图标的动态 EnumProperty。
# EnumProperty 在 'enum_previews_from_directory_items' 中动态填充，其中包含所选目录的缩略图内容。
# 然后，相同的枚举使用不同的界面显示。请注意，生成的图标预览没有 Blender ID，这意味着它们不能与需要 ID 的 UILayout 模板一起使用，
# 如 template_list 和 template_ID_preview。

# 其他用例：
# - 创建一个固定的 enum_items 列表，而不是在函数中计算它们
# - 生成孤立的缩略图以用作按钮和菜单项中的自定义图标

# 对于自定义图标，请参阅模板 "ui_previews_custom_icon.py"。

# 对于可分发的脚本，建议将图标放置在脚本目录内，并相对于 py 脚本文件访问它以实现可移植性：

#    os.path.join(os.path.dirname(__file__), "images")


import os
import bpy


def enum_previews_from_directory_items(self, context):
    """EnumProperty 回调函数"""
    enum_items = []

    if context is None:
        return enum_items

    wm = context.window_manager
    directory = wm.my_previews_dir

    # 获取预览集合（在注册函数中定义）
    pcoll = preview_collections["main"]

    if directory == pcoll.my_previews_dir:
        return pcoll.my_previews

    print("扫描目录：%s" % directory)

    if directory and os.path.exists(directory):
        # 扫描目录中的 `*.png` 文件
        image_paths = []
        for fn in os.listdir(directory):
            if fn.lower().endswith(".png"):
                image_paths.append(fn)

        for i, name in enumerate(image_paths):
            # 为文件生成缩略图预览。
            filepath = os.path.join(directory, name)
            icon = pcoll.get(name)
            if not icon:
                thumb = pcoll.load(name, filepath, 'IMAGE')
            else:
                thumb = pcoll[name]
            enum_items.append((name, name, "", thumb.icon_id, i))

    pcoll.my_previews = enum_items
    pcoll.my_previews_dir = directory
    return pcoll.my_previews


class PreviewsExamplePanel(bpy.types.Panel):
    """在对象属性窗口中创建一个面板"""
    bl_label = "预览示例面板"
    bl_idname = "OBJECT_PT_previews"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"

    def draw(self, context):
        layout = self.layout
        wm = context.window_manager

        row = layout.row()
        row.prop(wm, "my_previews_dir")

        row = layout.row()
        row.template_icon_view(wm, "my_previews")

        row = layout.row()
        row.prop(wm, "my_previews")


# 我们可以在此处存储多个预览集合，
# 但在此示例中，我们仅存储 "main"
preview_collections = {}


def register():
    from bpy.types import WindowManager
    from bpy.props import (
        StringProperty,
        EnumProperty,
    )

    WindowManager.my_previews_dir = StringProperty(
        name="文件夹路径",
        subtype='DIR_PATH',
        default=""
    )

    WindowManager.my_previews = EnumProperty(
        items=enum_previews_from_directory_items,
    )

    # 请注意，由 bpy.utils.previews 返回的预览集合是常规的 Python 对象 - 您可以使用它们存储自定义数据。
    #
    # 这在这里特别有用，因为：
    # - 它避免了我们一遍又一遍地重新生成整个枚举。
    # - 它可以存储 enum_items 的字符串
    #   （请记住，你必须在 py 中的某处保留这些字符串，
    #   否则它们会被释放，而 Blender 引用无效内存！）。
    import bpy.utils.previews
    pcoll = bpy.utils.previews.new()
    pcoll.my_previews_dir = ""
    pcoll.my_previews = ()

    preview_collections["main"] = pcoll

    bpy.utils.register_class(PreviewsExamplePanel)


def unregister():
    from bpy.types import WindowManager

    del WindowManager.my_previews

    for pcoll in preview_collections.values():
        bpy.utils.previews.remove(pcoll)
    preview_collections.clear()

    bpy.utils.unregister_class(PreviewsExamplePanel)


if __name__ == "__main__":
    register()
