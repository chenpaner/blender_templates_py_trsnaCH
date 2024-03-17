# 此示例假设我们已选择了一个网格对象
#这个脚本假设已选择了一个网格对象，并使用 BMesh 进行修改，将每个顶点的 x 坐标增加了 1.0。
import bpy
import bmesh

# 获取活动网格
me = bpy.context.object.data

# 获取 BMesh 表示
bm = bmesh.new()   # 创建一个空的 BMesh
bm.from_mesh(me)   # 从 Mesh 填充进去


# 修改 BMesh，在这里可以做任何操作...
for v in bm.verts:
    v.co.x += 1.0


# 完成，将 bmesh 写回网格
bm.to_mesh(me)
bm.free()  # 释放并防止进一步访问
