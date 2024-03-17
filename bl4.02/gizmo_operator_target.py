# 示例代码，演示了如何使用预定义的旋钮 gizmo 来改变相机的倾斜角度。
#
# 使用方法：运行此脚本，然后在 3D 视图中选择一个相机。

import bpy
from bpy.types import (
    GizmoGroup,  # 导入 GizmoGroup 类
)


class MyCameraWidgetGroup(GizmoGroup):
    """相机测试小部件"""
    bl_idname = "OBJECT_GGT_test_camera"  # 小部件的 ID 名称
    bl_label = "Object Camera Test Widget"  # 小部件的标签名称
    bl_space_type = 'VIEW_3D'  # 空间类型为 3D 视图
    bl_region_type = 'WINDOW'  # 区域类型为窗口
    bl_options = {'3D', 'PERSISTENT'}  # 小部件选项为 3D 和持久

    @classmethod
    def poll(cls, context):
        """检查当前上下文是否符合小部件的要求"""
        ob = context.object
        return (ob and ob.type == 'CAMERA')

    def setup(self, context):
        """设置小部件"""
        # 使用旋钮 gizmo 运行一个操作符
        ob = context.object
        gz = self.gizmos.new("GIZMO_GT_dial_3d")  # 创建一个新的旋钮 gizmo
        props = gz.target_set_operator("transform.rotate")  # 将旋钮 gizmo 的目标设置为 "transform.rotate" 操作符
        props.constraint_axis = False, False, True  # 约束旋转轴
        props.orient_type = 'LOCAL'  # 设置旋转方向为局部坐标系
        props.release_confirm = True  # 设置释放确认为真

        gz.matrix_basis = ob.matrix_world.normalized()  # 将旋钮 gizmo 的基矩阵设置为相机的世界矩阵的标准化版本
        gz.line_width = 3  # 设置线宽为 3

        gz.color = 0.8, 0.8, 0.8  # 设置颜色
        gz.alpha = 0.5  # 设置透明度

        gz.color_highlight = 1.0, 1.0, 1.0  # 设置高亮颜色
        gz.alpha_highlight = 1.0  # 设置高亮透明度

        self.roll_gizmo = gz  # 将旋钮 gizmo 分配给 roll_gizmo 属性

    def refresh(self, context):
        """刷新小部件"""
        ob = context.object
        gz = self.roll_gizmo
        gz.matrix_basis = ob.matrix_world.normalized()  # 将旋钮 gizmo 的基矩阵设置为相机的世界矩阵的标准化版本


bpy.utils.register_class(MyCameraWidgetGroup)  # 注册自定义的相机小部件类
