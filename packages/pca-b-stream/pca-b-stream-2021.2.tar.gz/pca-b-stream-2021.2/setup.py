# Copyright CNRS/Inria/UCA
# Contributor(s): Eric Debreuve (since 2021)
#
# eric.debreuve@cnrs.fr
#
# This software is governed by the CeCILL  license under French law and
# abiding by the rules of distribution of free software.  You can  use,
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info".
#
# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.
#
# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and,  more generally, to use and operate it in the
# same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.

from setuptools import setup
import pathlib


here = pathlib.Path(__file__).parent.resolve()

long_description = (here / 'README.rst').read_text(encoding='utf-8')

setup(
    # $ pip install pca-b-stream
    # On PyPI: https://pypi.org/project/pca-b-stream
    name='pca-b-stream',
    description='Byte Stream Representation of Piecewise-constant Array',
    long_description=long_description,
    long_description_content_type='text/x-rst',

    version='2021.2',

    url='https://gitlab.inria.fr/edebreuv/pca-b-stream',
    project_urls={
        'Source': 'https://gitlab.inria.fr/edebreuv/pca-b-stream',
    },

    author='Eric Debreuve',
    author_email='eric.debreuve@univ-cotedazur.fr',

    classifiers=[
        'Topic :: Scientific/Engineering :: Image Recognition',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: CEA CNRS Inria Logiciel Libre License, version 2.1 (CeCILL-2.1)',
        'Programming Language :: Python :: 3.8',
        'Development Status :: 4 - Beta',
    ],
    keywords='array, image, piecewise constant, byte stream',

    py_modules=["pca_b_stream", "test"],
    python_requires='>=3.8, <4',
    install_requires=['numpy', 'leb128', 'tqdm'],
    entry_points={
        'console_scripts': [
            'test_pca_b_stream=test:Main',
        ],
    },
)
