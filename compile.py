from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
ext_modules = [
    Extension("augmentation",  ["augmentation.py", "augmentation_sequence.py"]),
    Extension("background",  ["back_grabber.py"]),
#   ... all your modules that need be compiled ...
]
setup(
    name = 'MarkerTrainerC',
    cmdclass = {'build_ext': build_ext},
    ext_modules = ext_modules
)