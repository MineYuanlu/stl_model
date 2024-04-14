import os
from typing import TYPE_CHECKING
import tempfile
from solid import scad_render_to_file
import pyvista as pv


ROOT_DIR=os.path.dirname(os.path.dirname(__file__))
MODEL_DIR = os.path.join(ROOT_DIR, "model")
IMG_DIR = os.path.join(ROOT_DIR, "imgs")
TMP_DIR=os.path.join(ROOT_DIR,"tmp")
VIEW_INFO_DIR = os.path.join(ROOT_DIR, "view_info")

os.makedirs(IMG_DIR,exist_ok=True)
os.makedirs(TMP_DIR,exist_ok=True)
os.makedirs(VIEW_INFO_DIR,exist_ok=True)

if TYPE_CHECKING:
    from solid import OpenSCADObject

def get_name(path:"str",type:"str"):
    filename = os.path.basename(path)
    filename = (filename[:filename.rindex(".")] if "." in filename else filename)+f".{type}"
    return filename

def export_stl(model:"OpenSCADObject",filename:"str"=None,py:"str"=None):
    if py and not filename:
        filename = get_name(py,"stl")
    assert filename

    tmp = tempfile.mktemp(suffix=".scad",prefix=f"tmp-model",dir=TMP_DIR)
    print(tmp)
    scad_render_to_file(model, tmp)
    output=os.path.join(MODEL_DIR,filename)
    os.system(f"openscad -o \"{output}\" \"{tmp}\"")
    os.remove(tmp)
    return output


def render_stl(stl:"str",force_show=False,camera_pos:"list[tuple]|None"=None,load_cp=True,save_cp=True):
    cp_name = os.path.join(VIEW_INFO_DIR,get_name(stl,"cam"))
    img_name = os.path.join(IMG_DIR,get_name(stl,"png"))
    non_cam=False
    if camera_pos is None:
        if load_cp and os.path.exists(cp_name):
                with open(cp_name,'r') as f:
                    camera_pos = eval(f.read())
        else:
            camera_pos = [(100, 100, 100), (0, 0, 0), (0, 0, 1)]
            non_cam=True
    def display(): 
        mesh = pv.read(stl)
        plotter = pv.Plotter()
        plotter.add_mesh(mesh)
        plotter.set_background('white')
        plotter.camera_position = [(100, 100, 100), (0, 0, 0), (0, 0, 1)]
        plotter.window_size = (1920, 1080)
        plotter.show()
        cam = plotter.camera_position
        return cam

    if non_cam or force_show:
        cam = display()
    else:
        cam = camera_pos
    if save_cp:
        with open(cp_name,'w+') as f:
            f.write(str(cam))
    mesh = pv.read(stl)
    plotter = pv.Plotter(off_screen=True)
    plotter.add_mesh(mesh)
    plotter.camera_position = cam
    plotter.render()
    plotter.screenshot(img_name)
    plotter.close()
