
debian_os = ['debian', 'ubuntu']
rhel_os = ['redhat', 'centos', 'ol', 'rocky', 'almalinux']


def test_repo_file(host):
    f = None
    if host.system_info.distribution.lower() in debian_os:
        f = host.file('/etc/apt/sources.list.d/powerdns-dnsdist-21.sources')
    if host.system_info.distribution.lower() in rhel_os:
        f = host.file('/etc/yum.repos.d/powerdns-dnsdist-21.repo')

    assert f.exists
    assert f.user == 'root'
    assert f.group == 'root'


def test_pdns_repo(host):
    f = None
    if host.system_info.distribution.lower() in debian_os:
        f = host.file('/etc/apt/sources.list.d/powerdns-dnsdist-21.sources')
    if host.system_info.distribution.lower() in rhel_os:
        f = host.file('/etc/yum.repos.d/powerdns-dnsdist-21.repo')

    assert f.exists
    assert f.contains('dnsdist-21')


def test_pdns_repo_architecture(host):
    if host.system_info.distribution.lower() in debian_os:
        f = host.file('/etc/apt/sources.list.d/powerdns-dnsdist-21.sources')
        apt_arch = host.check_output('dpkg --print-architecture').strip()

        assert f.contains(f'Architectures: {apt_arch}')


def test_pdns_version(host):
    cmd = host.run('/usr/bin/dnsdist --version')

    assert 'dnsdist 2.1' in cmd.stdout
