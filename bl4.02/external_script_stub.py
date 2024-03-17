#这个脚本是一个存根，用于在当前打开的.blend文件的相对位置运行一个Python脚本。它可以在外部编辑脚本时很有用。

import bpy
import os

# 在这里使用你自己的脚本名字:
filename = "my_script.py"

# 获取脚本的完整路径
filepath = os.path.join(os.path.dirname(bpy.data.filepath), filename)

# 定义全局命名空间
global_namespace = {"__file__": filepath, "__name__": "__main__"}

# 打开脚本文件并执行
with open(filepath, 'rb') as file:
    exec(compile(file.read(), filepath, 'exec'), global_namespace)
```

#这段代码会运行指定的Python脚本文件，文件的路径相对于当前打开的.blend文件。