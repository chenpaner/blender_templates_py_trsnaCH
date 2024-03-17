# 该段代码创建了一个名为 `MyAssetShelf` 的类，继承自 `bpy.types.AssetShelf`，
# 用于在3D视图中添加自定义的资产架。`poll` 方法用于检查上下文是否处于对象模式下，
# `asset_poll` 方法用于检查资产是否符合特定条件。最后，通过注册和注销函数将该类注册到Blender中。

import bpy

class MyAssetShelf(bpy.types.AssetShelf):
    # 将资产架添加到3D视图中
    bl_space_type = 'VIEW_3D'
    # 定义资产架的ID名称
    bl_idname = "VIEW3D_AST_my_asset_shelf"

    @classmethod
    def poll(cls, context):
        # 检查上下文是否处于对象模式下
        return context.mode == 'OBJECT'

    @classmethod
    def asset_poll(cls, asset):
        # 检查资产是否符合特定条件
        return asset.id_type in {'MATERIAL', 'OBJECT'}


def register():
    # 注册资产架类
    bpy.utils.register_class(MyAssetShelf)


def unregister():
    # 注销资产架类
    bpy.utils.unregister_class(MyAssetShelf)


if __name__ == "__main__":
    register()


