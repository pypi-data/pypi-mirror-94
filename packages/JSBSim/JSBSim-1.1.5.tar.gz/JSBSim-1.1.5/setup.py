# This script has been automatically built from /Users/runner/work/jsbsim/jsbsim/python/setup.py.in
#
# Copyright (c) 2014-2021 Bertrand Coconnier
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, see <http://www.gnu.org/licenses/>
#

import os, sys, argparse

from argparse import ArgumentError
from setuptools import setup
from setuptools.extension import Extension
from setuptools.command.build_ext import build_ext
from setuptools.command.install_lib import install_lib
from distutils import log
from distutils.ccompiler import new_compiler
from distutils.unixccompiler import UnixCCompiler
from distutils.dist import Distribution


# Performs a build which verbosity is driven by VERBOSE
class QuietBuild(build_ext):
    def run(self):
        if "VERBOSE" not in os.environ:
            name = self.extensions[0].name
            log.info("building '{}' extension".format(name))

            if not os.path.exists(self.build_lib):
                log.info('creating {}'.format(self.build_lib))
                os.makedirs(self.build_lib)

            self.oldstdout = os.dup(sys.stdout.fileno())
            self.devnull = open(os.path.join(self.build_lib, name+'-build.log'), 'w')
            os.dup2(self.devnull.fileno(), sys.stdout.fileno())

        build_ext.run(self)

        if "VERBOSE" not in os.environ:
            os.dup2(self.oldstdout, sys.stdout.fileno())
            self.devnull.close()

# The standard install_lib class installs every single file it finds in the
# build directory. Here, we just want to install the JSBSim module so that it
# can be accessed everywhere on the platform. This class is therefore
# specializing the standard install_lib to do just that.
# It also takes care of extra dependencies for Windows systems.
class InstallJSBSimModule(install_lib):
    def __init__(self, dist):
        install_lib.__init__(self, dist)
        # Get the name of the JSBSim Python module (on some platforms this name
        # can be quite complicated).
        build_ext = self.get_finalized_command('build_ext')
        self.module_name = build_ext.get_ext_filename(build_ext.extensions[0].name)
        self.module_fullpath = build_ext.get_ext_fullpath(build_ext.extensions[0].name)

    def install(self):
        if not os.path.exists(self.install_dir):
            log.info('creating {}'.format(self.install_dir))
            os.makedirs(self.install_dir)

        self.copy_file(self.module_fullpath, os.path.join(self.install_dir,
                                                          self.module_name))

        # When compiled with Microsoft Visual C++, the JSBSim Python module is
        # linked with the dynamically linked library msvcp140.dll which is not a
        # standard library on Windows. So this code allows msvcp140.dll to be
        # shipped with the Python module.
        if compiler.compiler_type == 'msvc':
            import win32api

            path = win32api.GetEnvironmentVariable('PATH')
            # Use a set below to remove duplication.
            dirs = set([win32api.GetSystemDirectory(),
                        win32api.GetWindowsDirectory()] + path.split(';'))

            for d in dirs:
                libpath = os.path.join(d, 'msvcp140.dll')
                if os.path.exists(libpath):
                    self.copy_file(libpath, os.path.join(self.install_dir,
                                                         'msvcp140.dll'))
                    break

# distutils assumes that all the files must be compiled with the same compiler
# flags regardless of their file extension .c or .cpp.
# JSBSim C++ files must be compiled with -std=c++1x but compilation on MacOSX
# fails when trying to compile C files with -std=c++1x.
# The class C_CxxCompiler adds C++ flags to compilation flags for C++ files only.
class C_CxxCompiler(UnixCCompiler):
    def _compile(self, obj, src, ext, cc_args, extra_postargs, pp_opts):
        _cc_args = cc_args
        # Add the C++ flags to the compile flags if we are dealing with a C++
        # source file.
        if os.path.splitext(src)[-1] in ('.cpp', '.cxx', '.cc'):
            _cc_args = cpp_compile_flag + cc_args

        UnixCCompiler._compile(self, obj, src, ext, _cc_args,
                                extra_postargs, pp_opts)

# The class BuildC_CxxExtension intercepts the build of the Python module and
# replaces the compiler by an instance of C_CxxCompiler that select the compile
# flags depending on whether it is a C++ source file or not.
class BuildC_CxxExtension(build_ext):
    def build_extension(self, ext):
        if self.compiler.compiler_type == 'unix':

            old_compiler = self.compiler
            self.compiler = C_CxxCompiler()
            # Copy the attributes to the new compiler instance
            for attr, value in old_compiler.__dict__.items():
                setattr(self.compiler, attr, value)
        return build_ext.build_extension(self, ext)

# Process the path to the JSBSim library.
library_path = os.path.join('../', 'src')

# Move to the directory in which the script setup.py is located.
os.chdir(os.path.dirname(__file__))

# Intercept the --config option that we set for msbuild
parser = argparse.ArgumentParser(add_help=False)
parser.add_argument("--config", help="Build mode used by Visual C++",
                    choices=['Debug', 'Release', 'RelWithDebInfo'])
args, extra = parser.parse_known_args()

if args.config:
    # Remove the option from the command line to prevent complaints from
    # distutils
    sys.argv[1:] = extra

# Determine which compiler will be used to build the package.
dist = Distribution({'script_name': __file__})

if dist.parse_command_line() and 'build_ext' in dist.commands:
    compiler_name = dist.get_command_obj('build_ext').compiler
else:
    compiler_name = None

compiler = new_compiler(compiler=compiler_name)

if compiler.compiler_type == 'unix':
    cpp_compile_flag = ['-std=c++11']
else:
    cpp_compile_flag = []

if compiler.compiler_type == 'msvc':
    link_libraries = ['wsock32', 'ws2_32']
else:
    link_libraries = ['m',]

# Update the JSBSim library path according to the --config option
if args.config:
    if compiler.compiler_type == 'msvc':
        library_path=os.path.join(library_path, args.config)
    else:
        raise ArgumentError(None, 'option --config not recognized.')

# Check if the library exists and build the Python module accordingly.
if 'sdist' not in dist.commands and compiler.find_library_file([library_path],
                                                               'JSBSim'):
    # OK, the JSBSim library has already been compiled so let's use it to build
    # the Python module.
    ext_kwargs = { 'sources': ['jsbsim.cxx'],
                   'include_dirs': ['src'],
                   'libraries': ['JSBSim'] + link_libraries,
                   'library_dirs': [library_path],
                   'extra_compile_args': cpp_compile_flag }
    setup_kwargs = { 'cmdclass' : {'build_ext': QuietBuild,
                                   'install_lib': InstallJSBSimModule}}
else:
    # We cannot find the JSBSim library so the Python module must be built from
    # the sources.
    if compiler.compiler_type == 'msvc':
        compile_flags = ['/D'+flag for flag in ['_USE_MATH_DEFINES', 'NOMINMAX', 'JSBSIM_VERSION="1.1.5 [GitHub build 277/commit e407a683c05fd03bab8b1da1c0c88b2465a30c8b]"','HAVE_EXPAT_CONFIG_H',]]
        if sys.version_info < (3,9):
            compile_flags = [flag.replace('"', '\\"') for flag in compile_flags]
    else:
        compile_flags = ['-D'+flag for flag in ['JSBSIM_VERSION="1.1.5 [GitHub build 277/commit e407a683c05fd03bab8b1da1c0c88b2465a30c8b]"','HAVE_EXPAT_CONFIG_H',]]


    ext_kwargs = { 'sources': ['jsbsim.pyx', 'src/FGFDMExec.cpp','src/FGJSBBase.cpp','src/initialization/FGInitialCondition.cpp','src/initialization/FGTrim.cpp','src/initialization/FGTrimAxis.cpp','src/models/atmosphere/FGMSIS.cpp','src/models/atmosphere/FGMSISData.cpp','src/models/atmosphere/FGMars.cpp','src/models/atmosphere/FGStandardAtmosphere.cpp','src/models/atmosphere/FGWinds.cpp','src/models/flight_control/FGDeadBand.cpp','src/models/flight_control/FGFCSComponent.cpp','src/models/flight_control/FGFilter.cpp','src/models/flight_control/FGGain.cpp','src/models/flight_control/FGKinemat.cpp','src/models/flight_control/FGSummer.cpp','src/models/flight_control/FGSwitch.cpp','src/models/flight_control/FGFCSFunction.cpp','src/models/flight_control/FGSensor.cpp','src/models/flight_control/FGPID.cpp','src/models/flight_control/FGActuator.cpp','src/models/flight_control/FGAccelerometer.cpp','src/models/flight_control/FGGyro.cpp','src/models/flight_control/FGMagnetometer.cpp','src/models/flight_control/FGAngles.cpp','src/models/flight_control/FGWaypoint.cpp','src/models/flight_control/FGDistributor.cpp','src/models/flight_control/FGLinearActuator.cpp','src/models/propulsion/FGElectric.cpp','src/models/propulsion/FGEngine.cpp','src/models/propulsion/FGForce.cpp','src/models/propulsion/FGNozzle.cpp','src/models/propulsion/FGPiston.cpp','src/models/propulsion/FGPropeller.cpp','src/models/propulsion/FGRocket.cpp','src/models/propulsion/FGTank.cpp','src/models/propulsion/FGThruster.cpp','src/models/propulsion/FGTurbine.cpp','src/models/propulsion/FGTurboProp.cpp','src/models/propulsion/FGTransmission.cpp','src/models/propulsion/FGRotor.cpp','src/models/FGAerodynamics.cpp','src/models/FGAircraft.cpp','src/models/FGAtmosphere.cpp','src/models/FGAuxiliary.cpp','src/models/FGFCS.cpp','src/models/FGSurface.cpp','src/models/FGGroundReactions.cpp','src/models/FGInertial.cpp','src/models/FGLGear.cpp','src/models/FGMassBalance.cpp','src/models/FGModel.cpp','src/models/FGOutput.cpp','src/models/FGPropagate.cpp','src/models/FGPropulsion.cpp','src/models/FGInput.cpp','src/models/FGExternalReactions.cpp','src/models/FGExternalForce.cpp','src/models/FGBuoyantForces.cpp','src/models/FGGasCell.cpp','src/models/FGAccelerations.cpp','src/math/FGColumnVector3.cpp','src/math/FGFunction.cpp','src/math/FGLocation.cpp','src/math/FGMatrix33.cpp','src/math/FGPropertyValue.cpp','src/math/FGQuaternion.cpp','src/math/FGRealValue.cpp','src/math/FGTable.cpp','src/math/FGCondition.cpp','src/math/FGRungeKutta.cpp','src/math/FGModelFunctions.cpp','src/math/FGTemplateFunc.cpp','src/input_output/FGGroundCallback.cpp','src/input_output/FGPropertyManager.cpp','src/input_output/FGScript.cpp','src/input_output/FGXMLElement.cpp','src/input_output/FGXMLParse.cpp','src/input_output/FGfdmSocket.cpp','src/input_output/FGOutputType.cpp','src/input_output/FGOutputFG.cpp','src/input_output/FGOutputSocket.cpp','src/input_output/FGOutputFile.cpp','src/input_output/FGOutputTextFile.cpp','src/input_output/FGPropertyReader.cpp','src/input_output/FGModelLoader.cpp','src/input_output/FGInputType.cpp','src/input_output/FGInputSocket.cpp','src/input_output/FGUDPInputSocket.cpp','src/simgear/props/props.cxx','src/simgear/props/propertyObject.cxx','src/simgear/xml/easyxml.cxx','src/simgear/xml/xmlparse.c','src/simgear/xml/xmltok.c','src/simgear/xml/xmlrole.c','src/simgear/magvar/coremag.cxx','src/simgear/misc/sg_path.cxx','src/simgear/misc/strutils.cxx','src/simgear/io/iostreams/sgstream.cxx',],
                   'libraries': link_libraries,
                   'include_dirs': ['src', 'src/simgear/xml'],
                   'extra_compile_args': compile_flags }
    # List of required modules to build the JSBSim module from the sources.
    setup_kwargs = {'cmdclass' : {'build_ext': BuildC_CxxExtension,},
                    'setup_requires': ["setuptools>=18.0", "cython>=0.25"]}

# Build & installation process for the JSBSim Python module
setup(
    name="JSBSim",
    version="1.1.5",
    url="https://github.com/JSBSim-Team/jsbsim",
    author="Jon S. Berndt et al.",
    author_email="jsbsim-users@lists.sourceforge.net",
    license="LGPL 2.1",
    description="An open source flight dynamics & control software library",
    long_description="JSBSim is a multi-platform, general purpose object-oriented Flight Dynamics Model (FDM) written in C++. The FDM is essentially the physics & math model that defines the movement of an aircraft, rocket, etc., under the forces and moments applied to it using the various control mechanisms and from the forces of nature. JSBSim can be run in a standalone batch mode flight simulator (no graphical displays) for testing and study, or integrated with [FlightGear](http://home.flightgear.org/) or other flight simulator.",
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Other Audience",
        "License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)",
        "Operating System :: Microsoft",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOS X",
        "Programming Language :: C++",
        "Programming Language :: Python :: 3",
        "Topic :: Education",
        "Topic :: Games/Entertainment :: Simulation",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    scripts=['JSBSim'],
    install_requires=['numpy'],
    ext_modules=[Extension('jsbsim', language='c++', **ext_kwargs)],
    **setup_kwargs)
