
#-*- coding: UTF-8 -*

################################################################################################
###################################### CXFREEZE SETUP FILE #####################################
################################################################################################


from cx_Freeze import setup, Executable

setup(
    name = "PyWriterControl",
    version = "1.0",
    description = "Simple frontend that allow to control Thermo Carousel MicroWriter and Slide MicroWriter machines",
    executables = [Executable("pywritercontrol.py")],
)

