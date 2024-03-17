# 示例代码，演示了如何使用 gizmos 控制操作符的属性。
#
# 使用方法：运行此脚本，然后在编辑模式下按 F3，
# 激活操作符 "Select Side of Plane"。
# 然后可以使用 gizmos 调整平面在 3D 视图中的位置。

import bpy
import bmesh

from bpy.types import (
    Operator,
    GizmoGroup,
)

from bpy.props import (
    FloatVectorProperty,
)


def main(context, plane_co, plane_no):
    """
    核心函数，用于选择平面的一侧。

    参数:
    - context: 上下文对象，包含了脚本运行的环境信息和相关数据。
    - plane_co: 平面的位置（三维向量）。
    - plane_no: 平面的法线方向（三维向量）。
    """

    # 获取当前激活的对象
    obj = context.active_object
    # 获取对象的世界变换矩阵的副本
    matrix = obj.matrix_world.copy()
    # 获取对象的编辑模式下的网格数据
    me = obj.data
    # 创建网格编辑器
    bm = bmesh.from_edit_mesh(me)

    # 计算平面方程中的点乘项
    plane_dot = plane_no.dot(plane_co)

    # 遍历所有的顶点
    for v in bm.verts:
        # 将顶点坐标转换到世界坐标系下
        co = matrix @ v.co
        # 根据顶点在平面的哪一侧来设置选择状态
        v.select = (plane_no.dot(co) > plane_dot)

    # 刷新网格选择状态
    bm.select_flush_mode()

    # 更新编辑网格
    bmesh.update_edit_mesh(me)


class SelectSideOfPlane(Operator):
    """选择平面一侧的所有顶点"""
    bl_idname = "mesh.select_side_of_plane"
    bl_label = "Select Side of Plane"
    bl_options = {'REGISTER', 'UNDO'}

    plane_co: FloatVectorProperty(
        name="平面位置",
        description="平面的位置",
        size=3,
        default=(0, 0, 0),
    )
    plane_no: FloatVectorProperty(
        name="平面法线",
        description="平面的法线方向",
        size=3,
        default=(0, 0, 1),
    )

    @classmethod
    def poll(cls, context):
        return (context.mode == 'EDIT_MESH')

    def invoke(self, context, event):

        if not self.properties.is_property_set("plane_co"):
            self.plane_co = context.scene.cursor.location

        if not self.properties.is_property_set("plane_no"):
            if context.space_data.type == 'VIEW_3D':
                rv3d = context.space_data.region_3d
                view_inv = rv3d.view_matrix.to_3x3()
                # 视图 Y 轴
                self.plane_no = view_inv[1].normalized()

        self.execute(context)

        if context.space_data.type == 'VIEW_3D':
            wm = context.window_manager
            wm.gizmo_group_type_ensure(SelectSideOfPlaneGizmoGroup.bl_idname)

        return {'FINISHED'}

    def execute(self, context):
        from mathutils import Vector
        main(context, Vector(self.plane_co), Vector(self.plane_no))
        return {'FINISHED'}


class SelectSideOfPlaneGizmoGroup(GizmoGroup):
    """用于在 3D 视图中控制平面位置和法线方向的小部件"""
    bl_idname = "MESH_GGT_select_side_of_plane"
    bl_label = "Side of Plane Gizmo"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_options = {'3D', 'EXCLUDE_MODAL'}

    # 辅助函数
    @staticmethod
    def my_target_operator(context):
        wm = context.window_manager
        op = wm.operators[-1] if wm.operators else None
        if isinstance(op, SelectSideOfPlane):
            return op
        return None

    @staticmethod
    def my_view_orientation(context):
        rv3d = context.space_data.region_3d
        view_inv = rv3d.view_matrix.to_3x3()
        return view_inv.normalized()

    @classmethod
    def poll(cls, context):
        op = cls.my_target_operator(context)
        if op is None:
            wm = context.window_manager
            wm.gizmo_group_type_unlink_delayed(SelectSideOfPlaneGizmoGroup.bl_idname)
            return False
        return True

    def setup(self, context):
        from mathutils import Matrix, Vector

        # ----
        # 移动

        def move_get_cb():
            op = SelectSideOfPlaneGizmoGroup.my_target_operator(context)
            return op.plane_co

        def move_set_cb(value):
            op = SelectSideOfPlaneGizmoGroup.my_target_operator(context)
            op.plane_co = value
            # XXX, 这可能会改变!
            op.execute(context)

        gz = self.gizmos.new("GIZMO_GT_move_3d")
        gz.target_set_handler("offset", get=move_get_cb, set=move_set_cb)

        gz.use_draw_value = True

        gz.color = 0.8, 0.8, 0.8
        gz.alpha = 0.5

        gz.color_highlight = 1.0, 1.0, 1.0
        gz.alpha_highlight = 1.0

        gz.scale_basis = 0.2

        self.gizmo_move = gz

        # ----
        # 旋转

        def direction_get_cb():
            op = SelectSideOfPlaneGizmoGroup.my_target_operator(context)

            no_a = self.gizmo_dial.matrix_basis.col[1].xyz
            no_b = Vector(op.plane_no)

            no_a = (no_a @ self.view_inv).xy.normalized()
            no_b = (no_b @ self.view_inv).xy.normalized()
            return no_a.angle_signed(no_b)

        def direction_set_cb(value):
            op = SelectSideOfPlaneGizmoGroup.my_target_operator(context)
            matrix_rotate = Matrix.Rotation(-value, 3, self.rotate_axis)
            no = matrix_rotate @ self.gizmo_dial.matrix_basis.col[1].xyz
            op.plane_no = no
            op.execute(context)

        gz = self.gizmos.new("GIZMO_GT_dial_3d")
        gz.target_set_handler("offset", get=direction_get_cb, set=direction_set_cb)
        gz.draw_options = {'ANGLE_START_Y'}

        gz.use_draw_value = True

        gz.color = 0.8, 0.8, 0.8
        gz.alpha = 0.5

        gz.color_highlight = 1.0, 1.0, 1.0
        gz.alpha_highlight = 1.0

        self.gizmo_dial = gz

    def draw_prepare(self, context):
        from mathutils import Vector

        view_inv = self.my_view_orientation(context)

        self.view_inv = view_inv
        self.rotate_axis = view_inv[2].xyz
        self.rotate_up = view_inv[1].xyz

        op = self.my_target_operator(context)

        co = Vector(op.plane_co)
        no = Vector(op.plane_no).normalized()

        # 移动
        no_z = no
        no_y = no_z.orthogonal()
        no_x = no_z.cross(no_y)

        matrix = self.gizmo_move.matrix_basis
        matrix.identity()
        matrix.col[0].xyz = no_x
        matrix.col[1].xyz = no_y
        matrix.col[2].xyz = no_z
        # 位置回调函数处理位置。
        # `matrix.col[3].xyz = co`.

        # 旋转
        no_z = self.rotate_axis
        no_y = (no - (no.project(no_z))).normalized()
        no_x = self.rotate_axis.cross(no_y)

        matrix = self.gizmo_dial.matrix_basis
        matrix.identity()
        matrix.col[0].xyz = no_x
        matrix.col[1].xyz = no_y
        matrix.col[2].xyz = no_z
        matrix.col[3].xyz = co


classes = (
    SelectSideOfPlane,
    SelectSideOfPlaneGizmoGroup,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
