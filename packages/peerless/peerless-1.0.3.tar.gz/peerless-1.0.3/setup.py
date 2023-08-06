# Copyright 2019, 2020 Eve Utils S.L.
#
# Licensed under the EUPL, Version 1.2 or – as soon they
# will be approved by the European Commission - subsequent
# versions of the EUPL (the "Licence");
#
# You may not use this work except in compliance with the
# Licence.
#
# You may obtain a copy of the Licence at:
#
# https://joinup.ec.europa.eu/software/page/eupl
#
# Unless required by applicable law or agreed to in
# writing, software distributed under the Licence is
# distributed on an "AS IS" basis,
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
# express or implied.
#
# See the Licence for the specific language governing
# permissions and limitations under the Licence.

import setuptools

with open("README.md", "r") as fid:
    long_description = fid.read()

setuptools.setup(
    name="peerless",
    version="1.0.3",
    author="Eve Utils S.L.",
    author_email="support@eveutils.com",
    description="Peerless Optimizer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://www.eveutils.com/peerless",
    python_requires=">=3.8",
    license="EUPL-1.2",
    keywords="mathematical optimization operations research numerical analysis",
    classifiers=["Development Status :: 5 - Production/Stable",
                 "Environment :: Console",
                 "Intended Audience :: Developers",
                 "Intended Audience :: Science/Research",
                 "License :: OSI Approved :: European Union Public Licence 1.2 (EUPL 1.2)",
                 "Natural Language :: English",
                 "Operating System :: OS Independent",
                 "Programming Language :: Python :: 3",
                 "Programming Language :: Python :: 3 :: Only",
                 "Topic :: Scientific/Engineering :: Mathematics",
                 "Topic :: Software Development :: Libraries"],
    package_dir={"": "src"},
    py_modules=["eut.__init__",
                "eut.abba.__init__",
                "eut.abba.processor.__init__",
                "eut.abba.processor.statuses",
                "eut.abba.processor.priority",
                "eut.peerless.__init__",
                "eut.peerless.model",
                "eut.peerless.solver"],
    data_files=[(".", ["LICENSE.txt", "README.md"])],
    scripts=["scripts/peerless_manager"]
)
