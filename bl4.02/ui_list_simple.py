import bpy


class MATERIAL_UL_matslots_example(bpy.types.UIList):
    # 对于列表中可见的每个项目，都会调用 draw_item 函数。
    #   data 是包含集合的 RNA 对象，
    #   item 是集合中当前绘制的项目，
    #   icon 是项目的“计算”图标（作为整数，因为一些对象，如材质或纹理，具有自定义图标 ID，这些图标不可用作枚举项）。
    #   active_data 是包含集合的活动属性的 RNA 对象（即指向集合中活动项目的整数）。
    #   active_propname 是活动属性的名称（使用 'getattr(active_data, active_propname)'）。
    #   index 是集合中当前项目的索引。
    #   flt_flag 是此项目的过滤结果。
    #   注意：如果不需要 index 和 flt_flag，则不必在此处使用/声明它们。
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        ob = data
        slot = item
        ma = slot.material
        # draw_item 必须处理三种布局类型... 通常 'DEFAULT' 和 'COMPACT' 可以共享相同的代码。
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            # 您应该始终通过标签（图标 + 文本）或非凹陷文本字段开始行布局，这样也可以使行在列表中易于选择！后者还启用了 ctrl-click 重命名。
            # 我们使用标签的 icon_value，因为我们给定的图标是一个整数值，而不是一个枚举 ID。
            # 注意 "data" 名称不应翻译！
            if ma:
                layout.prop(ma, "name", text="", emboss=False, icon_value=icon)
            else:
                layout.label(text="", translate=False, icon_value=icon)
        # 'GRID' 布局类型应尽可能紧凑（通常是单个图标！）。
        elif self.layout_type == 'GRID':
            layout.alignment = 'CENTER'
            layout.label(text="", icon_value=icon)


# 现在我们可以在 Blender 中的任何地方使用这个列表。下面是一个小例子面板。
class UIListPanelExample(bpy.types.Panel):
    """在对象属性窗口中创建一个面板"""
    bl_label = "UIList Panel"
    bl_idname = "OBJECT_PT_ui_list_example"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"

    def draw(self, context):
        layout = self.layout

        obj = context.object

        # template_list 现在需要两个新参数。
        # 第一个参数是要使用的注册 UIList 的标识符（如果只想使用默认列表，没有自定义绘制代码，则使用 "UI_UL_list"）。
        layout.template_list("MATERIAL_UL_matslots_example", "", obj, "material_slots", obj, "active_material_index")

        # 第二个参数通常可以留为空字符串。
        # 它是一个额外的 ID，用于在同一区域多次使用相同的列表时进行区分。
        layout.template_list("MATERIAL_UL_matslots_example", "compact", obj, "material_slots",
                             obj, "active_material_index", type='COMPACT')


def register():
    bpy.utils.register_class(MATERIAL_UL_matslots_example)
    bpy.utils.register_class(UIListPanelExample)


def unregister():
    bpy.utils.unregister_class(MATERIAL_UL_matslots_example)
    bpy.utils.unregister_class(UIListPanelExample)


if __name__ == "__main__":
    register()
