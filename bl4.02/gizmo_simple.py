# 示例代码，演示了如何使用预定义的箭头 gizmo 来编辑单个属性。
#
# 使用方法：在 3D 视图中选择一个灯光，然后拖动箭头的尾部来改变它的能量值。

import bpy
from bpy.types import (
    GizmoGroup,  # 导入 GizmoGroup 类
)


class MyLightWidgetGroup(GizmoGroup):
    """灯光测试小部件"""
    bl_idname = "OBJECT_GGT_light_test"  # 小部件的 ID 名称
    bl_label = "Test Light Widget"  # 小部件的标签名称
    bl_space_type = 'VIEW_3D'  # 空间类型为 3D 视图
    bl_region_type = 'WINDOW'  # 区域类型为窗口
    bl_options = {'3D', 'PERSISTENT'}  # 小部件选项为 3D 和持久

    @classmethod
    def poll(cls, context):
        """检查当前上下文是否符合小部件的要求"""
        ob = context.object
        return (ob and ob.type == 'LIGHT')

    def setup(self, context):
        """设置小部件"""
        # 箭头 gizmo 有一个我们可以分配到灯光能量的 'offset' 属性。
        ob = context.object
        gz = self.gizmos.new("GIZMO_GT_arrow_3d")  # 创建一个新的箭头 gizmo
        gz.target_set_prop("offset", ob.data, "energy")  # 将箭头 gizmo 的目标属性设置为灯光的能量值
        gz.matrix_basis = ob.matrix_world.normalized()  # 将箭头 gizmo 的基矩阵设置为灯光的世界矩阵的标准化版本
        gz.draw_style = 'BOX'  # 设置绘制样式为 'BOX'

        gz.color = 1.0, 0.5, 0.0  # 设置颜色
        gz.alpha = 0.5  # 设置透明度

        gz.color_highlight = 1.0, 0.5, 1.0  # 设置高亮颜色
        gz.alpha_highlight = 0.5  # 设置高亮透明度

        self.energy_gizmo = gz  # 将箭头 gizmo 分配给 energy_gizmo 属性

    def refresh(self, context):
        """刷新小部件"""
        ob = context.object
        gz = self.energy_gizmo
        gz.matrix_basis = ob.matrix_world.normalized()  # 将箭头 gizmo 的基矩阵设置为灯光的世界矩阵的标准化版本


bpy.utils.register_class(MyLightWidgetGroup)  # 注册自定义的灯光小部件类
