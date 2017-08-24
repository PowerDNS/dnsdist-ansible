import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_dnsdist_configuration(host):

    f = host.file('/etc/dnsdist/dnsdist.conf')
    assert f.exists
    assert f.user == 'root'
    assert f.group == 'root'


def test_dnsdist_installed(host):

    p = host.package('dnsdist')
    assert p.is_installed


def test_dnsdist_service(host):

    # Testinfra fails on Debiand and Ubuntu to use systemd to get
    # the status of the Docker daemon
    dist = host.system_info.distribution
    if dist == 'debian' or dist == 'ubuntu':
        c = host.run("service dnsdist status")
        assert c.rc == 0
    else:
        s = host.service('dnsdist')
        assert s.is_running
        assert s.is_enabled
