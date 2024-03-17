# 将每个选定的对象导出到单独的文件中

import bpy
import os

# 导出到 blend 文件所在位置
basedir = os.path.dirname(bpy.data.filepath)

if not basedir:
    raise Exception("未保存 blend 文件")

view_layer = bpy.context.view_layer

obj_active = view_layer.objects.active
selection = bpy.context.selected_objects

bpy.ops.object.select_all(action='DESELECT')

for obj in selection:

    obj.select_set(True)

    # 一些导出器仅使用活动对象
    view_layer.objects.active = obj

    name = bpy.path.clean_name(obj.name)
    fn = os.path.join(basedir, name)

    bpy.ops.export_scene.fbx(filepath=fn + ".fbx", use_selection=True)

    # 也可用于多种格式
    # bpy.ops.export_scene.x3d(filepath=fn + ".x3d", use_selection=True)

    obj.select_set(False)

    print("已写入:", fn)


view_layer.objects.active = obj_active

for obj in selection:
    obj.select_set(True)
