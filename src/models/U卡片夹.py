from solid import *
from solid.utils import *
import os,sys
sys.path.insert(0,os.path.dirname(os.path.dirname(__file__)))
from tool import *


# 定义基本参数
base_length = 15
base_width = 20
base_height = 3
plat_width = 3
height1 = 15
height2 = 5

base = cube([base_length, base_width, base_height]) # 1.5 * 2厘米的底片

platform1 = translate([0, 0, base_height])(cube([plat_width, base_width, height1]))
platform2 = translate([base_length - plat_width, 0, base_height])(cube([plat_width, base_width, height2]))

model = base + platform1 + platform2

# 导出为 STL 文件
stl = export_stl(model, py=__file__)
render_stl(stl)
