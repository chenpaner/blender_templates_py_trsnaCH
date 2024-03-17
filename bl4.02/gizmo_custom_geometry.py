# 该脚本定义了一个自定义小部件，用于在3D视图中选择光源并拖动箭头来改变其能量值。

import bpy
from bpy.types import (
    Gizmo,
    GizmoGroup,
)

# 定义坐标（每个坐标是一个三角形）。
custom_shape_verts = (
    (3.0, 1.0, -1.0), (2.0, 2.0, -1.0), (3.0, 3.0, -1.0),
    (1.0, 3.0, 1.0), (3.0, 3.0, -1.0), (1.0, 3.0, -1.0),
    (3.0, 3.0, 1.0), (3.0, 1.0, -1.0), (3.0, 3.0, -1.0),
    (2.0, 0.0, 1.0), (3.0, 1.0, -1.0), (3.0, 1.0, 1.0),
    (2.0, 0.0, -1.0), (2.0, 2.0, 1.0), (2.0, 2.0, -1.0),
    (2.0, 2.0, -1.0), (0.0, 2.0, 1.0), (0.0, 2.0, -1.0),
    (1.0, 3.0, 1.0), (2.0, 2.0, 1.0), (3.0, 3.0, 1.0),
    (0.0, 2.0, -1.0), (1.0, 3.0, 1.0), (1.0, 3.0, -1.0),
    (2.0, 2.0, 1.0), (3.0, 1.0, 1.0), (3.0, 3.0, 1.0),
    (2.0, 2.0, -1.0), (1.0, 3.0, -1.0), (3.0, 3.0, -1.0),
    (-3.0, -1.0, -1.0), (-2.0, -2.0, -1.0), (-3.0, -3.0, -1.0),
    (-1.0, -3.0, 1.0), (-3.0, -3.0, -1.0), (-1.0, -3.0, -1.0),
    (-3.0, -3.0, 1.0), (-3.0, -1.0, -1.0), (-3.0, -3.0, -1.0),
    (-2.0, 0.0, 1.0), (-3.0, -1.0, -1.0), (-3.0, -1.0, 1.0),
    (-2.0, 0.0, -1.0), (-2.0, -2.0, 1.0), (-2.0, -2.0, -1.0),
    (-2.0, -2.0, -1.0), (0.0, -2.0, 1.0), (0.0, -2.0, -1.0),
    (-1.0, -3.0, 1.0), (-2.0, -2.0, 1.0), (-3.0, -3.0, 1.0),
    (0.0, -2.0, -1.0), (-1.0, -3.0, 1.0), (-1.0, -3.0, -1.0),
    (-2.0, -2.0, 1.0), (-3.0, -1.0, 1.0), (-3.0, -3.0, 1.0),
    (-2.0, -2.0, -1.0), (-1.0, -3.0, -1.0), (-3.0, -3.0, -1.0),
    (1.0, -1.0, 0.0), (-1.0, -1.0, 0.0), (0.0, 0.0, -5.0),
    (-1.0, -1.0, 0.0), (1.0, -1.0, 0.0), (0.0, 0.0, 5.0),
    (1.0, -1.0, 0.0), (1.0, 1.0, 0.0), (0.0, 0.0, 5.0),
    (1.0, 1.0, 0.0), (-1.0, 1.0, 0.0), (0.0, 0.0, 5.0),
    (-1.0, 1.0, 0.0), (-1.0, -1.0, 0.0), (0.0, 0.0, 5.0),
    (-1.0, -1.0, 0.0), (-1.0, 1.0, 0.0), (0.0, 0.0, -5.0),
    (-1.0, 1.0, 0.0), (1.0, 1.0, 0.0), (0.0, 0.0, -5.0),
    (1.0, 1.0, 0.0), (1.0, -1.0, 0.0), (0.0, 0.0, -5.0),
    (3.0, 1.0, -1.0), (2.0, 0.0, -1.0), (2.0, 2.0, -1.0),
    (1.0, 3.0, 1.0), (3.0, 3.0, 1.0), (3.0, 3.0, -1.0),
    (3.0, 3.0, 1.0), (3.0, 1.0, 1.0), (3.0, 1.0, -1.0),
    (2.0, 0.0, 1.0), (2.0, 0.0, -1.0), (3.0, 1.0, -1.0),
    (2.0, 0.0, -1.0), (2.0, 0.0, 1.0), (2.0, 2.0, 1.0),
    (2.0, 2.0, -1.0), (2.0, 2.0, 1.0), (0.0, 2.0, 1.0),
    (1.0, 3.0, 1.0), (0.0, 2.0, 1.0), (2.0, 2.0, 1.0),
    (0.0, 2.0, -1.0), (0.0, 2.0, 1.0), (1.0, 3.0, 1.0),
    (2.0, 2.0, 1.0), (2.0, 0.0, 1.0), (3.0, 1.0, 1.0),
    (2.0, 2.0, -1.0), (0.0, 2.0, -1.0), (1.0, 3.0, -1.0),
    (-3.0, -1.0, -1.0), (-2.0, 0.0, -1.0), (-2.0, -2.0, -1.0),
    (-1.0, -3.0, 1.0), (-3.0, -3.0, 1.0), (-3.0, -3.0, -1.0),
    (-3.0, -3.0, 1.0), (-3.0, -1.0, 1.0), (-3.0, -1.0, -1.0),
    (-2.0, 0.0, 1.0), (-2.0, 0.0, -1.0), (-3.0, -1.0, -1.0),
    (-2.0, 0.0, -1.0), (-2.0, 0.0, 1.0), (-2.0, -2.0, 1.0),
    (-2.0, -2.0, -1.0), (-2.0, -2.0, 1.0), (0.0, -2.0, 1.0),
    (-1.0, -3.0, 1.0), (0.0, -2.0, 1.0), (-2.0, -2.0, 1.0),
    (0.0, -2.0, -1.0), (0.0, -2.0, 1.0), (-1.0, -3.0, 1.0),
    (-2.0, -2.0, 1.0), (-2.0, 0.0, 1.0), (-3.0, -1.0, 1.0),
    (-2.0, -2.0, -1.0), (0.0, -2.0, -1.0), (-1.0, -3.0, -1.0),
)


class MyCustomShapeWidget(Gizmo):
    bl_idname = "VIEW3D_GT_custom_shape_widget"  # 小部件的唯一标识符
    bl_target_properties = (  # 定义目标属性，用于与其他对象进行交互
        {"id": "offset", "type": 'FLOAT', "array_length": 1},  # 目标属性名称为 "offset"，类型为 FLOAT，数组长度为 1
    )

    __slots__ = (  # 使用 __slots__ 以节省内存
        "custom_shape",  # 自定义形状的存储变量
        "init_mouse_y",  # 初始鼠标 Y 坐标
        "init_value",  # 初始值
    )

    def _update_offset_matrix(self):
        # 将偏移放在光源后面
        self.matrix_offset.col[3][2] = self.target_get_value("offset") / -10.0

    def draw(self, context):
        # 更新偏移矩阵
        self._update_offset_matrix()
        # 绘制自定义形状
        self.draw_custom_shape(self.custom_shape)

    def draw_select(self, context, select_id):
        # 更新偏移矩阵
        self._update_offset_matrix()
        # 绘制选择状态下的自定义形状
        self.draw_custom_shape(self.custom_shape, select_id=select_id)

    def setup(self):
        if not hasattr(self, "custom_shape"):
            # 如果不存在自定义形状，则创建
            self.custom_shape = self.new_custom_shape('TRIS', custom_shape_verts)

    def invoke(self, context, event):
        # 记录初始鼠标 Y 坐标和初始值
        self.init_mouse_y = event.mouse_y
        self.init_value = self.target_get_value("offset")
        return {'RUNNING_MODAL'}

    def exit(self, context, cancel):
        # 退出时，清除头部文本，并根据取消状态恢复初始值
        context.area.header_text_set(None)
        if cancel:
            self.target_set_value("offset", self.init_value)

    def modal(self, context, event, tweak):
        # 计算鼠标移动距离，根据鼠标移动调整值，并设置新值
        delta = (event.mouse_y - self.init_mouse_y) / 10.0
        if 'SNAP' in tweak:
            delta = round(delta)
        if 'PRECISE' in tweak:
            delta /= 10.0
        value = self.init_value - delta
        self.target_set_value("offset", value)
        # 设置头部文本显示新值
        context.area.header_text_set("My Gizmo: %.4f" % value)
        return {'RUNNING_MODAL'}


class MyCustomShapeWidgetGroup(GizmoGroup):
    bl_idname = "OBJECT_GGT_light_test"  # 小部件组的唯一标识符
    bl_label = "Test Light Widget"  # 小部件组的标签
    bl_space_type = 'VIEW_3D'  # 小部件组的空间类型
    bl_region_type = 'WINDOW'  # 小部件组的区域类型
    bl_options = {'3D', 'PERSISTENT'}  # 小部件组的选项

    @classmethod
    def poll(cls, context):
        # 检查是否存在光源对象
        ob = context.object
        return (ob and ob.type == 'LIGHT')

    def setup(self, context):
        # 设置小部件组
        ob = context.object
        gz = self.gizmos.new(MyCustomShapeWidget.bl_idname)
        gz.target_set_prop("offset", ob.data, "energy")

        gz.color = 1.0, 0.5, 1.0  # 设置颜色
        gz.alpha = 0.5  # 设置透明度

        gz.color_highlight = 1.0, 1.0, 1.0  # 设置高亮颜色
        gz.alpha_highlight = 0.5  # 设置高亮透明度

        gz.scale_basis = 0.1  # 缩放大小
        gz.use_draw_modal = True  # 使用模态绘制

        self.energy_gizmo = gz

    def refresh(self, context):
        # 刷新小部件组
        ob = context.object
        gz = self.energy_gizmo
        gz.matrix_basis = ob.matrix_world.normalized()


classes = (
    MyCustomShapeWidget,  # 注册自定义小部件类
    MyCustomShapeWidgetGroup,  # 注册自定义小部件组类
)

for cls in classes:
    bpy.utils.register_class(cls)  # 注册类
