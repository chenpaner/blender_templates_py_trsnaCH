# 这段代码定义了一个自定义的 UI 列表（UIList），该列表用于显示网格对象的自定义属性。以下是代码的作用：
# 1. **draw_item 方法：**
#     - 该方法用于绘制列表中的每个项。根据不同的布局类型（DEFAULT、COMPACT、GRID），需要进行相应的绘制处理。目前，代码中只定义了方法，但没有具体的绘制逻辑。
# 2. **draw_filter 方法：**
#     - 该方法用于绘制过滤/重新排序选项，目前代码中并未实现具体的绘制逻辑。
# 3. **filter_items 方法：**
#     - 该方法用于过滤/重新排序列表项。
#     - 根据给定的参数，通过实现自定义的过滤/重新排序逻辑，返回两个列表：flt_flags 和 flt_neworder。
#     - flt_flags 列表用于标记需要过滤的项，每个标记占用 32 位整数，其中包括 self.bitflag_filter_item 用于标记匹配项，其余位可用于自定义需求。
#     - flt_neworder 列表用于指定项的新索引顺序。

# 该代码为创建一个自定义的 UI 列表提供了基础框架，开发者可以根据需要实现绘制、过滤和重新排序逻辑，并将该 UI 列表应用到 Blender 的界面中。

import bpy

class MESH_UL_mylist(bpy.types.UIList):
    # 常量（标志）
    # 谨慎不要遮蔽 FILTER_ITEM（例如，UIList().bitflag_filter_item）！
    # 例如 VGROUP_EMPTY = 1 << 0

    # 自定义属性，保存在 .blend 文件中。例如：
    # use_filter_empty: bpy.props.BoolProperty(
    #     name="Filter Empty", default=False, options=set(),
    #     description="Whether to filter empty vertex groups",
    # )

    # 每个绘制项调用一次。
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index, flt_flag):
        # 'DEFAULT' 和 'COMPACT' 布局类型通常应使用相同的绘制代码。
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            pass
        # 'GRID' 布局类型应尽可能紧凑（通常仅包含一个图标！）。
        elif self.layout_type == 'GRID':
            pass

    # 一次性绘制过滤/重新排序选项。
    def draw_filter(self, context, layout):
        # 这里没有太多可说的，这是常见的 UI 代码...
        pass

    # 一次性过滤/重新排序项。
    def filter_items(self, context, data, propname):
        # 该函数获取集合属性（通常是元组 (data, propname)），必须返回两个列表：
        # * 第一个用于过滤，必须包含 32 位整数，其中 self.bitflag_filter_item 标记匹配项为已过滤（即要显示的项），
        #   其他 31 位可用于自定义需求。在这里我们使用第一个标记来标记 VGROUP_EMPTY。
        # * 第二个用于重新排序，必须返回包含项的新索引的列表（这给我们提供了一个映射 org_idx -> new_idx）。
        # 请注意，默认的 UI_UL_list 定义了常见任务的辅助函数（有关更多信息，请参阅其文档）。
        # 如果您不进行过滤和/或排序，则返回空列表更有效率（而不是返回无用的完整列表！）。

        # 默认返回值。
        flt_flags = []
        flt_neworder = []

        # 在这里进行过滤/重新排序...

        return flt_flags, flt_neworder
