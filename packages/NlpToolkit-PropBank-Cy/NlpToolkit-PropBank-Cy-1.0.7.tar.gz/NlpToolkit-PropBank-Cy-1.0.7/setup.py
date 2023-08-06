from distutils.core import setup
from Cython.Build import cythonize

setup(
    ext_modules=cythonize(["PropBank/*.pyx"],
                          compiler_directives={'language_level': "3"}),
    name='NlpToolkit-PropBank-Cy',
    version='1.0.7',
    packages=['PropBank'],
    package_data={'PropBank': ['*.pxd', '*.pyx', '*.c', '*.py']},
    url='https://github.com/StarlangSoftware/TurkishPropbank-Cy',
    license='',
    author='olcaytaner',
    author_email='olcay.yildiz@ozyegin.edu.tr',
    description='Turkish PropBank'
)
