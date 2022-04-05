
debian_os = ['debian', 'ubuntu']
rhel_os = ['redhat', 'centos']


def test_repo_file(host):
    f = None
    if host.system_info.distribution.lower() in debian_os:
        f = host.file('/etc/apt/sources.list.d/powerdns-dnsdist-17.list')
    if host.system_info.distribution.lower() in rhel_os:
        f = host.file('/etc/yum.repos.d/powerdns-dnsdist-17.repo')

    assert f.exists
    assert f.user == 'root'
    assert f.group == 'root'


def test_pdns_repo(host):
    f = None
    if host.system_info.distribution.lower() in debian_os:
        f = host.file('/etc/apt/sources.list.d/powerdns-dnsdist-17.list')
    if host.system_info.distribution.lower() in rhel_os:
        f = host.file('/etc/yum.repos.d/powerdns-dnsdist-17.repo')

    assert f.exists
    assert f.contains('dnsdist-17')


def test_pdns_version(host):
    cmd = host.run('/usr/bin/dnsdist --version')

    assert 'dnsdist 1.7' in cmd.stdout
