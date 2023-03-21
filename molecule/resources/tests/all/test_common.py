import re

debian_os = ['debian', 'ubuntu']
rhel_os = ['redhat', 'centos', 'oracleserver']


def test_distribution(host):
    assert host.system_info.distribution.lower() in debian_os + rhel_os


def test_repo_pinning_file(host):
    if host.system_info.distribution.lower() in debian_os:
        f = host.file('/etc/apt/preferences.d/dnsdist')
        assert f.exists
        assert f.user == 'root'
        assert f.group == 'root'
        f.contains('Package: dnsdist*')
        f.contains('Pin: origin repo.powerdns.com')
        f.contains('Pin-Priority: 600')


def test_package(host):
    p = host.package('dnsdist')
    assert p.is_installed


def test_configuration(host):
    f = host.file('/etc/dnsdist/dnsdist.conf')
    assert f.exists


def test_service(host):
    # Using Ansible to mitigate some issues with the service test on debian-8
    s = host.ansible('service', 'name=dnsdist state=started enabled=yes')

    assert s["changed"] is False


def test_tcp(host):
    tcp = host.socket('tcp://127.0.0.1:5300')
    assert tcp.is_listening


def test_udp(host):
    udp = host.socket('udp://127.0.0.1:5300')
    assert udp.is_listening


def test_service_overrides(host):
    smgr = host.ansible("setup")["ansible_facts"]["ansible_service_mgr"]
    if smgr == 'systemd':
        fname = '/etc/systemd/system/dnsdist.service.d/override.conf'
        f = host.file(fname)

        assert f.exists

        f_string = f.content.decode()

        assert re.search(r'^LimitCORE=infinity$', f_string, re.MULTILINE) is not None

        # # Ensure a ExecStart override is preceeded by a 'ExecStart=' reset instruction
        if re.search(r'^ExecStart=.+$', f_string, re.MULTILINE) is not None:
            assert re.search(r'^ExecStart=$(\r?\n)^ExecStart=.+$', f_string, re.MULTILINE) is not None
        
        # # Ensure a ExecStartPre override is preceeded by a 'ExecStartPre=' reset instruction
        if re.search(r'^ExecStartPre=.+$', f_string, re.MULTILINE) is not None:
            assert re.search(r'^ExecStartPre=$(\r?\n)^ExecStartPre=.+$', f_string, re.MULTILINE) is not None