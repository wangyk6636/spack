# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Hipsparse(CMakePackage):
    """hipSPARSE is a SPARSE marshalling library, with
       multiple supported backends"""

    homepage = "https://github.com/ROCmSoftwarePlatform/hipSPARSE"
    git      = "https://github.com/ROCmSoftwarePlatform/hipSPARSE.git"
    url      = "https://github.com/ROCmSoftwarePlatform/hipSPARSE/archive/rocm-4.3.0.tar.gz"

    maintainers = ['srekolam', 'arjun-raj-kuppala', 'haampie']

    version('4.3.0', sha256='194fbd589ce34471f3255f71ea5fca2d27bee47a464558a86d0713b4d26237ea')
    version('4.2.0', sha256='cdedf3766c10200d3ebabe86cbb9c0fe6504e4b3317dccca289327d7c189bb3f')
    version('4.1.0', sha256='66710c390489922f0bd1ac38fd8c32fcfb5b7760b92c2d282f7d1abf214742ee')
    version('4.0.0', sha256='fc3736b2ea203209021616b2ffbcdd664781d692b07b8e8bb7f78b42dabbd5e5')
    version('3.10.0', sha256='7fd863ebf6eed09325c23ba06d9008b2f2c1345283d1a331e329e1a512b602f7')
    version('3.9.0', sha256='ab0ea3dd9b68a126291ed5a35e50fc85d0aeb35fe862f5d9e544435e4262c435')
    version('3.8.0', sha256='8874c100e9ba54587a6057c2a0e555a0903254a16e9e01c2385bae1b027f83b5')
    version('3.7.0', sha256='a2f02d8fc6ad9a561f06dacde54ecafd30563c5c95f93819a5694e5b650dad7f')
    version('3.5.0', sha256='fa16b2a307a5d9716066c2876febcbc1cef855bf0c96d235d2d8f2206a0fb69d')

    depends_on('cmake@3:', type='build')
    depends_on('git', type='build')

    for ver in ['3.5.0', '3.7.0', '3.8.0', '3.9.0', '3.10.0', '4.0.0', '4.1.0',
                '4.2.0', '4.3.0']:
        depends_on('rocm-cmake@' + ver, type='build', when='@' + ver)
        depends_on('hip@' + ver,                      when='@' + ver)
        depends_on('rocsparse@' + ver,                when='@' + ver)

    for ver in ['3.8.0', '3.9.0', '3.10.0', '4.0.0', '4.1.0', '4.2.0', '4.3.0']:
        depends_on('rocprim@' + ver, when='@' + ver)

    patch('e79985dccde22d826aceb3badfc643a3227979d2.patch', when='@3.5.0')
    patch('530047af4a0f437dafc02f76b3a17e3b1536c7ec.patch', when='@3.5.0')

    def cmake_args(self):
        args = [
            # Make sure find_package(HIP) finds the module.
            self.define('CMAKE_MODULE_PATH', self.spec['hip'].prefix.cmake),
            self.define('CMAKE_CXX_STANDARD', '14'),
            self.define('BUILD_CLIENTS_SAMPLES', 'OFF'),
            self.define('BUILD_CLIENTS_TESTS', 'OFF'),
        ]

        if self.spec.satisfies('^cmake@3.21:'):
            args.append(self.define('__skip_rocmclang', 'ON'))

        return args

    def setup_build_environment(self, env):
        env.set('CXX', self.spec['hip'].hipcc)
