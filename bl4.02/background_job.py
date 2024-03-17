# 这个脚本是一个示例，演示了如何从命令行运行 Blender（在后台模式下无界面），以自动化任务。
# 在这个示例中，它创建一个文本对象、相机和灯光，然后渲染和/或保存它。
# 这个示例还展示了如何解析命令行选项给脚本使用。

# 这个测试的示例用法。
#  blender --background --factory-startup --python $HOME/background_job.py -- \
#          --text="Hello World" \
#          --render="/tmp/hello" \
#          --save="/tmp/hello.blend"
#
# 注意：
# '--factory-startup' 用于避免用户默认设置干扰自动化场景生成。
#
# '--' 导致 Blender 忽略所有后续参数，以便 Python 可以使用它们。
#
# 详情请参阅 blender --help。


import bpy


def example_function(text, save_path, render_path):
    # 清除现有对象。
    bpy.ops.wm.read_factory_settings(use_empty=True)

    scene = bpy.context.scene

    txt_data = bpy.data.curves.new(name="MyText", type='FONT')

    # 文本对象
    txt_ob = bpy.data.objects.new(name="MyText", object_data=txt_data)
    scene.collection.objects.link(txt_ob)   # 将数据添加到场景中作为对象
    txt_data.body = text         # 使用命令行参数给出的文本内容
    txt_data.align_x = 'CENTER'  # 文本居中

    # 相机
    cam_data = bpy.data.cameras.new("MyCam")
    cam_ob = bpy.data.objects.new(name="MyCam", object_data=cam_data)
    scene.collection.objects.link(cam_ob)  # 在场景中实例化相机对象
    scene.camera = cam_ob       # 设置活动相机
    cam_ob.location = 0.0, 0.0, 10.0

    # 灯光
    light_data = bpy.data.lights.new("MyLight", 'POINT')
    light_ob = bpy.data.objects.new(name="MyLight", object_data=light_data)
    scene.collection.objects.link(light_ob)
    light_ob.location = 2.0, 2.0, 5.0

    bpy.context.view_layer.update()

    if save_path:
        bpy.ops.wm.save_as_mainfile(filepath=save_path)

    if render_path:
        render = scene.render
        render.use_file_extension = True
        render.filepath = render_path
        bpy.ops.render.render(write_still=True)


def main():
    import sys       # 获取命令行参数
    import argparse  # 解析选项并打印漂亮的帮助消息

    # 获取传递给 blender 的 "--" 后面的参数，这些参数会被 blender 忽略，以便脚本可以接收自己的参数
    argv = sys.argv

    if "--" not in argv:
        argv = []  # 就像没有传递参数一样
    else:
        argv = argv[argv.index("--") + 1:]  # 获取 "--" 后面的所有参数

    # 当未给出 --help 或没有参数时，打印此帮助信息
    usage_text = (
        "在后台模式下运行此脚本的 Blender："
        "  blender --background --python " + __file__ + " -- [options]"
    )

    parser = argparse.ArgumentParser(description=usage_text)

    # 示例实用程序，添加一些文本并渲染或保存它（带有选项）
    # 可能的类型有：string、int、long、choice、float 和 complex。
    parser.add_argument(
        "-t", "--text", dest="text", type=str, required=True,
        help="此文本将用于渲染图像",
    )

    parser.add_argument(
        "-s", "--save", dest="save_path", metavar='FILE',
        help="将生成的文件保存到指定路径",
    )
    parser.add_argument(
        "-r", "--render", dest="render_path", metavar='FILE',
        help="将图像渲染到指定路径",
    )

    args = parser.parse_args(argv)  # 在这个示例中，我们不会使用这些参数

    if not argv:
        parser.print_help()
        return

    if not args.text:
        print("错误：未给出 --text=\"some string\" 参数，中止。")
        parser.print_help()
        return

    # 运行示例函数
    example_function(args.text, args.save_path, args.render_path)

    print("批处理任务完成，退出")


if __name__ == "__main__":
    main()
