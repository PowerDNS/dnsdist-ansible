
debian_os = ['debian', 'ubuntu']
rhel_os = ['redhat', 'centos', 'oracleserver', 'oraclelinux']


def test_repo_file(host):
    f = None
    if host.system_info.distribution.lower() in debian_os:
        f = host.file('/etc/apt/sources.list.d/powerdns-dnsdist-18.list')
    if host.system_info.distribution.lower() in rhel_os:
        f = host.file('/etc/yum.repos.d/powerdns-dnsdist-18.repo')

    assert f.exists
    assert f.user == 'root'
    assert f.group == 'root'


def test_pdns_repo(host):
    f = None
    if host.system_info.distribution.lower() in debian_os:
        f = host.file('/etc/apt/sources.list.d/powerdns-dnsdist-18.list')
    if host.system_info.distribution.lower() in rhel_os:
        f = host.file('/etc/yum.repos.d/powerdns-dnsdist-18.repo')

    assert f.exists
    assert f.contains('dnsdist-18')


def test_pdns_version(host):
    cmd = host.run('/usr/bin/dnsdist --version')

    assert 'dnsdist 1.8' in cmd.stdout
