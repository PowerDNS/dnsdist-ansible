debian_os = ['debian', 'ubuntu']
rhel_os = ['redhat', 'centos', 'ol', 'rocky', 'almalinux']

instances = {'a': '5311', 'b': '5312'}


def test_instance_configuration(host):
    for name, port in instances.items():
        f = host.file('/etc/dnsdist/dnsdist-{}.conf'.format(name))
        assert f.exists
        assert f.contains('-- instance {}'.format(name))
        assert f.contains('127.0.0.1:{}'.format(port))


def test_instance_service(host):
    for name in instances:
        s = host.service('dnsdist@{}'.format(name))
        assert s.is_running
        assert s.is_enabled


def test_instance_systemd_override(host):
    for name in instances:
        f = host.file(
            '/etc/systemd/system/dnsdist@{}.service.d/override.conf'.format(name)
        )
        assert f.exists
        assert f.contains('LimitCORE=infinity')


def test_instance_listens(host):
    for port in instances.values():
        assert host.socket('tcp://127.0.0.1:{}'.format(port)).is_listening
