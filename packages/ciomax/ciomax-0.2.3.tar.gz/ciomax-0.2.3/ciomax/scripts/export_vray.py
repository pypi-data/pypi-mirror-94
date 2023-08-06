
import pymxs
import os
from ciomax.renderer import Renderer

from contextlib import contextmanager

@contextmanager
def maintain_save_state():
    required = rt.getSaveRequired()
    
    yield
    rt.setSaveRequired(required)


rt = pymxs.runtime
def main(dialog, *args):
    renderer = Renderer.get()
    valid_renderers = ["VrayGPURenderer", "VraySWRenderer"]
    
    if not renderer.__class__.__name__ in valid_renderers:
        raise TypeError("Please the current renderer to one of: {}".format(valid_renderers))

    main_sequence = dialog.main_tab.section("FramesSection").main_sequence

    vrscene_prefix = os.path.splitext(args[0])[0]

    print "Ensure directory ia avalable for vrscene_file"
    _ensure_directory_for(vrscene_prefix)

    print "Closing render setup window if open..."
    if rt.renderSceneDialog.isOpen():
        rt.renderSceneDialog.close()

    print "Setting render time type to use a specified sequence..."
    rt.rendTimeType=4

 
    print "Setting the frame range..."
    rt.rendPickupFrames="{}-{}".format(main_sequence.start, main_sequence.end)

    print "Setting the by frame to 1..."
    rt.rendNThFrame=1

    # Annoyingly, setting rendPickupFrames above is not enough. We have to
    # provide start and end again here.
    print "Exporting vrscene files"
    error = 0
    with maintain_save_state():
        error = rt.vrayExportRTScene( 
            vrscene_prefix, 
            startFrame=main_sequence.start, 
            endFrame=main_sequence.end)

    vray_scene = "{}.vrscene".format(vrscene_prefix)
    if os.path.exists(vray_scene):
        if error:
            print "Scene was exported, but there were some errors during export. Check %temp%/vraylog.txt"
        else:
            print "Scene was exported successfully"
    else:
        raise  ValueError("Vray scene export failed. Check %temp%/vraylog.txt")
    
        # return list of extra dependencies
    print "Done"
    return [vray_scene]
    

def _ensure_directory_for(path):
    """Ensure that the parent directory of `path` exists"""
    dirname = os.path.dirname(path)
    if not os.path.isdir(dirname):
        os.makedirs(dirname)
