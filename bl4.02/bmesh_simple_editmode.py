# 这个脚本假设我们处于编辑模式，并且有一个网格对象，它使用 BMesh 进行修改，将每个顶点的 x 坐标增加了 1.0，并在视口中显示了更新
#此示例假设我们处于编辑模式，并有一个网格对象

import bpy
import bmesh

# 获取活动网格
obj = bpy.context.edit_object
me = obj.data

# 获取 BMesh 表示
bm = bmesh.from_edit_mesh(me)

bm.faces.active = None

# 修改 BMesh，在这里可以做任何操作...
for v in bm.verts:
    v.co.x += 1.0


# 在视口中显示更新
# 并重新计算 n-gon tessellation。
bmesh.update_edit_mesh(me, loop_triangles=True)
