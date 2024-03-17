# 这个脚本定义了一些函数，可以直接在驱动表达式中使用，以扩展内置的 Python 函数集。
#
# 可以手动执行此脚本，也可以将其设置为 "注册"，
# 在文件加载时初始化这些函数。

# 两个示例函数
def invert(f):
    """ 简单的函数调用：

            invert(val)
    """
    return 1.0 - f


uuid_store = {}


def slow_value(value, fac, uuid):
    """ 延迟值一段因子，使用唯一字符串允许在多个驱动程序中使用而不冲突：

            slow_value(val, 0.5, "my_value")
    """
    value_prev = uuid_store.get(uuid, value)
    uuid_store[uuid] = value_new = (value_prev * fac) + (value * (1.0 - fac))
    return value_new


import bpy

# 将此脚本中定义的函数添加到驱动程序命名空间中。
bpy.app.driver_namespace["invert"] = invert
bpy.app.driver_namespace["slow_value"] = slow_value

#这个脚本定义了两个函数 invert 和 slow_value，
#它们可以直接在驱动表达式中使用。invert 函数会返回输入值的反转（1.0 减去输入值），而 slow_value 函数会将输入值延迟一定因子。