import os

import pytest

debian_os = ['debian', 'ubuntu']
rhel_os = ['redhat', 'centos', 'ol', 'rocky', 'almalinux']
# 'archarm' is what the Arch Linux ARM images report.
arch_os = ['arch', 'archarm', 'archlinux', 'arch linux']


@pytest.fixture()
def distro_family(host):
    """Return 'debian', 'rhel' or 'arch' for the host under test."""
    distribution = host.system_info.distribution.lower()
    if distribution in debian_os:
        return 'debian'
    if distribution in rhel_os:
        return 'rhel'
    if distribution in arch_os:
        return 'arch'
    raise AssertionError('unsupported distribution {}'.format(distribution))


@pytest.fixture()
def component_version():
    """The release under test, as named by the PowerDNS repositories."""
    # A set-but-empty variable must fall back, which os.environ.get does not do.
    return os.environ.get('DNSDIST_VERSION') or '21'


@pytest.fixture()
def component_version_string(component_version):
    """The release under test as dnsdist reports it, for example '2.1'."""
    if not component_version.isdigit() or len(component_version) != 2:
        # Release names such as 'master' have no dotted form.
        return component_version
    return '{}.{}'.format(component_version[0], component_version[1])


@pytest.fixture()
def repo_file(host, distro_family):
    """The repository file the role writes. Its name carries no version."""
    if distro_family == 'debian':
        return host.file('/etc/apt/sources.list.d/powerdns-dnsdist.sources')
    return host.file('/etc/yum.repos.d/powerdns-dnsdist.repo')


@pytest.fixture()
def config_location(distro_family):
    if distro_family == 'arch':
        return '/etc/dnsdist.conf'
    return '/etc/dnsdist/dnsdist.conf'


@pytest.fixture()
def additional_package(distro_family):
    """The package the scenario installs through dnsdist_additional_packages."""
    if distro_family == 'arch':
        # Arch ships the telnet client as part of inetutils.
        return 'inetutils'
    return 'telnet'


@pytest.fixture()
def config_owner(distro_family):
    """The owner and group of the configuration files."""
    if distro_family == 'debian':
        return ('_dnsdist', '_dnsdist')
    return ('dnsdist', 'dnsdist')
