#这段代码定义了一个模态操作器 ViewOperatorRayCast，用于在视图中执行射线投射，
#并将游标位置设置为最近的命中位置。操作器可通过在视图菜单中添加快捷方式或使用F3搜索功能来调用

import bpy
from bpy_extras import view3d_utils


def main(context, event):
    """在鼠标左键点击时执行射线投射"""
    # 获取上下文参数
    scene = context.scene
    region = context.region
    rv3d = context.region_data
    coord = event.mouse_region_x, event.mouse_region_y

    # 从视口和鼠标获取射线
    view_vector = view3d_utils.region_2d_to_vector_3d(region, rv3d, coord)
    ray_origin = view3d_utils.region_2d_to_origin_3d(region, rv3d, coord)

    ray_target = ray_origin + view_vector

    def visible_objects_and_duplis():
        """遍历（对象，矩阵）对（仅限于网格）"""

        depsgraph = context.evaluated_depsgraph_get()
        for dup in depsgraph.object_instances:
            if dup.is_instance:  # 真实的复制实例
                obj = dup.instance_object
                yield (obj, dup.matrix_world.copy())
            else:  # 普通对象
                obj = dup.object
                yield (obj, obj.matrix_world.copy())

    def obj_ray_cast(obj, matrix):
        """射线投射的包装器，将射线移动到对象空间"""

        # 获取相对于对象的射线
        matrix_inv = matrix.inverted()
        ray_origin_obj = matrix_inv @ ray_origin
        ray_target_obj = matrix_inv @ ray_target
        ray_direction_obj = ray_target_obj - ray_origin_obj

        # 进行射线投射
        success, location, normal, face_index = obj.ray_cast(ray_origin_obj, ray_direction_obj)

        if success:
            return location, normal, face_index
        else:
            return None, None, None

    # 进行射线投射并找到最接近的对象
    best_length_squared = -1.0
    best_obj = None

    for obj, matrix in visible_objects_and_duplis():
        if obj.type == 'MESH':
            hit, normal, face_index = obj_ray_cast(obj, matrix)
            if hit is not None:
                hit_world = matrix @ hit
                scene.cursor.location = hit_world
                length_squared = (hit_world - ray_origin).length_squared
                if best_obj is None or length_squared < best_length_squared:
                    best_length_squared = length_squared
                    best_obj = obj

    # 现在我们得到了鼠标指针下的对象，可以进行很多操作，但本示例仅选择对象。
    if best_obj is not None:
        # 对于选择等操作，我们需要原始对象，评估后的对象不在视图图层中。
        best_original = best_obj.original
        best_original.select_set(True)
        context.view_layer.objects.active = best_original


class ViewOperatorRayCast(bpy.types.Operator):
    """使用射线投射的模态对象选择"""
    bl_idname = "view3d.modal_operator_raycast"
    bl_label = "射线投射视图操作器"

    def modal(self, context, event):
        if event.type in {'MIDDLEMOUSE', 'WHEELUPMOUSE', 'WHEELDOWNMOUSE'}:
            # 允许导航
            return {'PASS_THROUGH'}
        elif event.type == 'LEFTMOUSE':
            main(context, event)
            return {'RUNNING_MODAL'}
        elif event.type in {'RIGHTMOUSE', 'ESC'}:
            return {'CANCELLED'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        if context.space_data.type == 'VIEW_3D':
            context.window_manager.modal_handler_add(self)
            return {'RUNNING_MODAL'}
        else:
            self.report({'WARNING'}, "活动空间必须为 View3d")
            return {'CANCELLED'}


def menu_func(self, context):
    self.layout.operator(ViewOperatorRayCast.bl_idname, text="射线投射视图模态操作器")


# 注册并添加到“视图”菜单（还需使用 F3 搜索“射线投射视图模态操作器”进行快速访问）。
def register():
    bpy.utils.register_class(ViewOperatorRayCast)
    bpy.types.VIEW3D_MT_view.append(menu_func)


def unregister():
    bpy.utils.unregister_class(ViewOperatorRayCast)
    bpy.types.VIEW3D_MT_view.remove(menu_func)


if __name__ == "__main__":
    register()
