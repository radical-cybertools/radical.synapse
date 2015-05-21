
__author__    = 'RADICAL Team'
__email__     = 'radical@rutgers.edu'
__copyright__ = 'Copyright 2013/14, RADICAL Research, Rutgers University'
__license__   = 'MIT'


""" Setup script. Used by easy_install and pip. """

import os
import sys
import glob
import subprocess as sp

from setuptools           import setup, Command, find_packages
from setuptools.extension import Extension

name     = 'radical.synapse'
mod_root = 'src/radical/synapse'

# ------------------------------------------------------------------------------
#
# versioning mechanism:
#
#   - version:          1.2.3            - is used for installation
#   - version_detail:  v1.2.3-9-g0684b06 - is used for debugging
#   - version is read from VERSION file in src_root, which then is copied to
#     module dir, and is getting installed from there.
#   - version_detail is derived from the git tag, and only available when
#     installed from git.  That is stored in mod_root/VERSION in the install
#     tree.
#   - The VERSION file is used to provide the runtime version information.
#
def get_version (mod_root):
    """
    mod_root
        a VERSION file containes the version strings is created in mod_root,
        during installation.  That file is used at runtime to get the version
        information.  
        """

    try:

        version        = None
        version_detail = None

        # get version from './VERSION'
        src_root = os.path.dirname (__file__)
        if  not src_root :
            src_root = '.'

        with open (src_root + '/VERSION', 'r') as f :
            version = f.readline ().strip()


        # attempt to get version detail information from git
        p   = sp.Popen ('cd %s ; '\
                        'tag=`git describe --tags --always` 2>/dev/null ; '\
                        'branch=`git branch | grep -e "^*" | cut -f 2 -d " "` 2>/dev/null ; '\
                        'echo $tag@$branch'  % src_root,
                        stdout=sp.PIPE, stderr=sp.STDOUT, shell=True)
        version_detail = p.communicate()[0].strip()

        if  p.returncode   !=  0  or \
            version_detail == '@' or \
            'fatal'        in version_detail :
            version_detail =  'v%s' % version

        print 'version: %s (%s)' % (version, version_detail)


        # make sure the version files exist for the runtime version inspection
        path = '%s/%s' % (src_root, mod_root)
        print 'creating %s/VERSION' % path
        with open (path + "/VERSION", "w") as f : f.write (version_detail + "\n")

        sdist_name = "%s-%s.tar.gz" % (name, version_detail)
        sdist_name = sdist_name.replace ('/', '-')
        sdist_name = sdist_name.replace ('@', '-')
        sdist_name = sdist_name.replace ('#', '-')
        if '--record'  in sys.argv or 'bdist_egg' in sys.argv :   
           # pip install stage 2      easy_install stage 1
           # NOTE: pip install will untar the sdist in a tmp tree.  In that tmp
           # tree, we won't be able to derive git version tags -- so we pack the
           # formerly derived version as ./VERSION
            os.system ("mv VERSION VERSION.bak")        # backup version
            os.system ("cp %s/VERSION VERSION" % path)  # use full version instead
            os.system ("python setup.py sdist")         # build sdist
            os.system ("cp 'dist/%s' '%s/%s'" % \
                    (sdist_name, mod_root, sdist_name)) # copy into tree
            os.system ("mv VERSION.bak VERSION")        # restore version

        print 'creating %s/SDIST' % path
        with open (path + "/SDIST", "w") as f : f.write (sdist_name + "\n")

        return version, version_detail, sdist_name

    except Exception as e :
        raise RuntimeError ('Could not extract/set version: %s' % e)


# ------------------------------------------------------------------------------
# get version info -- this will create VERSION and srcroot/VERSION
version, version_detail, sdist_name = get_version (mod_root)


# ------------------------------------------------------------------------------
# check python version. we need > 2.6, <3.x
if  sys.hexversion < 0x02060000 or sys.hexversion >= 0x03000000:
    raise RuntimeError('%s requires Python 2.x (2.6 or higher)' % name)


# ------------------------------------------------------------------------------
class our_test(Command):
    user_options = []
    def initialize_options (self) : pass
    def finalize_options   (self) : pass
    def run (self) :
        testdir = "%s/tests/" % os.path.dirname(os.path.realpath(__file__))
        retval  = sp.call([sys.executable,
                          '%s/run_tests.py'               % testdir,
                          '%s/configs/default.cfg'        % testdir])
        raise SystemExit(retval)


# ------------------------------------------------------------------------------
#
def read(*rnames):
    try :
        return open(os.path.join(os.path.dirname(__file__), *rnames)).read()
    except Exception :
        return ''


# -------------------------------------------------------------------------------
c_ext = Extension("radical/synapse/atoms/_atoms" ,
                  sources = glob.glob('src/radical/synapse/atoms/*.c'))
setup_args = {
    'name'               : name,
    'version'            : version,
    'description'        : 'SYNthetic APplicationS Emulator -- A RADICAL Project '
                           '(http://radical.rutgers.edu/)',
    'long_description'   : (read('README.md') + '\n\n' + read('CHANGES.md')),
    'author'             : 'RADICAL Group at Rutgers University',
    'author_email'       : 'radical@rutgers.edu',
    'maintainer'         : 'The RADICAL Group',
    'maintainer_email'   : 'radical@rutgers.edu',
    'url'                : 'https://www.github.com/radical-cybertools/radical.utils/',
    'license'            : "LGPLv3+",
    'keywords'           : "radical emulate workload",
    'classifiers'        : [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Environment :: Console',
        'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Utilities',
        'Topic :: System :: Distributed Computing',
        'Topic :: Scientific/Engineering',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX',
        'Operating System :: Unix'
    ],
    
    'ext_modules'        : [c_ext],
    'namespace_packages' : ['radical'],
    'packages'           : find_packages('src'),
    'package_dir'        : {'': 'src'},
    'scripts'            : ['bin/radical-synapse-version',
                            'bin/radical-synapse-profile',
                            'bin/radical-synapse-stats',
                            'bin/radical-synapse-stats.plot',
                            'bin/radical-synapse-execute',
                            'bin/radical-synapse-emulate',
                            'bin/radical-synapse-fixdocs',
                            'bin/radical-synapse-mandelbrot-dummy.py',
                            'bin/radical-synapse-mandelbrot-master.py',
                            'bin/radical-synapse-mandelbrot-worker.py',
                            'bin/radical-synapse-mandelbrot-profile.py',
                            'bin/radical-synapse-mandelbrot-emulate.py',
                            'bin/radical-synapse-iotrace.sh'
                           ],
    'package_data'       : {'': ['*.sh', '*.json', '*.gz', 'VERSION', 'SDIST', sdist_name, '*.c']},
    'cmdclass'           : {
        'test'           : our_test,
    },
    'install_requires'   : [
        'pymongo', 
        'radical.utils', 
        'psutil'
    ],
    'extras_require'     : {
    },
    'tests_require'      : [],
    'test_suite'         : 'radical.synapse.tests',
    'zip_safe'           : False,
#   'build_sphinx'       : {
#       'source-dir'     : 'docs/',
#       'build-dir'      : 'docs/build',
#       'all_files'      : 1,
#   },
#   'upload_sphinx'      : {
#       'upload-dir'     : 'docs/build/html',
#   }
}

# ------------------------------------------------------------------------------

setup (**setup_args)

# ------------------------------------------------------------------------------

