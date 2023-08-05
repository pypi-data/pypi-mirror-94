from distutils.core import setup
from io import open

__author__ = "Tobias Rawald"
__copyright__ = "Copyright 2015-2021 The PyRQA project"
__credits__ = ["Tobias Rawald",
               "Mike Sips"]
__license__ = "Apache-2.0"
__maintainer__ = "Tobias Rawald"
__email__ = "pyrqa@gmx.net"
__status__ = "Development"


with open("README",
          "r",
          encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="PyRQA",
    packages=[
        "pyrqa",
        "pyrqa.operators",
        "pyrqa.operators.create_matrix",
        "pyrqa.operators.create_matrix.radius",
        "pyrqa.operators.create_matrix.unthresholded",
        "pyrqa.operators.detect_diagonal_lines",
        "pyrqa.operators.detect_diagonal_lines.radius",
        "pyrqa.operators.detect_vertical_lines",
        "pyrqa.operators.detect_vertical_lines.radius",
        "pyrqa.operators.join_matrices",
        "pyrqa.tests",
        "pyrqa.variants",
        "pyrqa.variants.jrp",
        "pyrqa.variants.jrp.radius",
        "pyrqa.variants.jrqa",
        "pyrqa.variants.jrqa.radius",
        "pyrqa.variants.rp",
        "pyrqa.variants.rp.radius",
        "pyrqa.variants.rp.unthresholded",
        "pyrqa.variants.rqa",
        "pyrqa.variants.rqa.radius",
    ],
    package_data={
        "pyrqa": [
            "config.ini",
            "kernels/clear_buffer/*.cl",
            "kernels/create_matrix/radius/euclidean_metric/*.cl.mako",
            "kernels/create_matrix/radius/maximum_metric/*.cl.mako",
            "kernels/create_matrix/radius/taxicab_metric/*.cl.mako",
            "kernels/create_matrix/unthresholded/euclidean_metric/*.cl.mako",
            "kernels/create_matrix/unthresholded/maximum_metric/*.cl.mako",
            "kernels/create_matrix/unthresholded/taxicab_metric/*.cl.mako",
            "kernels/detect_diagonal_lines/*.cl.mako",
            "kernels/detect_diagonal_lines/radius/euclidean_metric/*.cl.mako",
            "kernels/detect_diagonal_lines/radius/maximum_metric/*.cl.mako",
            "kernels/detect_diagonal_lines/radius/taxicab_metric/*.cl.mako",
            "kernels/detect_vertical_lines/*.cl.mako",
            "kernels/detect_vertical_lines/radius/euclidean_metric/*.cl.mako",
            "kernels/detect_vertical_lines/radius/maximum_metric/*.cl.mako",
            "kernels/detect_vertical_lines/radius/taxicab_metric/*.cl.mako",
            "kernels/join_matrices/*.cl",
        ],
    },
    version="8.0.0",
    description="Recurrence analysis in a massively parallel manner using the OpenCL framework.",
    long_description=long_description,
    author="Tobias Rawald",
    author_email="pyrqa@gmx.net",
    license="Apache License 2.0",
    keywords=[
        "nonlinear",
        "time series analysis",
        "dynamical system",
        "recurrence quantification analysis", 
        "RQA",
        "cross recurrence quantification analysis",
        "CRQA",
        "joint recurrence quantification analysis",
        "JRQA",
        "recurrence plot",
        "RP",
        "cross recurrence plot",
        "CRP",
        "joint recurrence plot",
        "JRP",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Financial and Insurance Industry",
        "Intended Audience :: Healthcare Industry",
        "Intended Audience :: Manufacturing",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Scientific/Engineering :: Physics"
    ],
    install_requires=[
        'Mako',
        'numpy', 
        'Pillow', 
        'pyopencl', 
        'scipy'
    ],
)