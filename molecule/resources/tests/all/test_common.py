import re


def test_distribution(distro_family):
    assert distro_family in ('debian', 'rhel', 'arch')


def test_repo_pinning_file(host, distro_family):
    if distro_family == 'debian':
        f = host.file('/etc/apt/preferences.d/dnsdist')
        assert f.exists
        assert f.user == 'root'
        assert f.group == 'root'
        assert f.contains('Package: dnsdist*')
        assert f.contains('Pin: origin repo.powerdns.com')
        assert f.contains('Pin-Priority: 600')


def test_package(host, distro_family):
    if distro_family == 'arch':
        assert host.run('pacman -Q dnsdist').rc == 0
        return

    assert host.package('dnsdist').is_installed


def test_configuration(host, config_location, config_owner):
    f = host.file(config_location)
    owner, group = config_owner
    assert f.exists
    assert f.user == owner
    assert f.group == group


def test_default_controlsocket_config(host, config_location):
    f = host.file(config_location)
    assert f.contains('controlSocket("127.0.0.1")')


def test_default_setkey_generated(host, config_location):
    f = host.file(config_location)
    for raw_line in f.content.decode().splitlines():
        line = raw_line.strip()
        if 'setKey("' not in line:
            continue
        assert not line.startswith('--')
        assert '--' not in line
        assert re.match(r'^setKey\("[^"]+"\)$', line) is not None
        return
    assert False, 'No active setKey("...") line found in the dnsdist configuration'


def test_distribution_package_is_the_running_one(host, distro_family):
    """On the distribution packages there is no repository to attribute, so
    check that the installed package is what answers."""
    if distro_family != 'arch':
        return

    package_version = host.check_output("pacman -Q dnsdist | awk '{print $2}'")
    cmd = host.run('/usr/bin/dnsdist --version')
    output = '{}\n{}'.format(cmd.stdout, cmd.stderr)

    # pacman reports 2.1.1-2 where dnsdist reports 2.1.1
    assert package_version.split('-')[0] in output


def test_service(host):
    # Use the service module to avoid backend-specific service inspection differences.
    s = host.ansible('service', 'name=dnsdist state=started enabled=yes')

    assert s["changed"] is False


def test_tcp(host):
    tcp = host.socket('tcp://127.0.0.1:5300')
    assert tcp.is_listening


def test_udp(host):
    udp = host.socket('udp://127.0.0.1:5300')
    assert udp.is_listening


def test_additional_package(host, distro_family, additional_package):
    if distro_family == 'arch':
        # testinfra does not map every Arch flavour to ArchPackage, so query
        # pacman directly.
        assert host.run('pacman -Q {}'.format(additional_package)).rc == 0
        return

    assert host.package(additional_package).is_installed


def test_additional_config_file(host, config_location, config_owner):
    f = host.file('{}/extra.conf'.format(config_location.rsplit('/', 1)[0]))
    owner, group = config_owner
    assert f.exists
    assert f.contains('-- extra file with configration')
    assert f.user == owner
    assert f.group == group


def test_service_overrides(host):
    smgr = host.ansible("setup")["ansible_facts"]["ansible_service_mgr"]
    if smgr == 'systemd':
        fname = '/etc/systemd/system/dnsdist.service.d/override.conf'
        f = host.file(fname)

        assert f.exists

        f_string = f.content.decode()

        assert re.search(r'^LimitCORE=infinity$', f_string, re.MULTILINE) is not None

        # Ensure a ExecStart override is preceeded by a 'ExecStart=' reset instruction
        if re.search(r'^ExecStart=.+$', f_string, re.MULTILINE) is not None:
            assert re.search(r'^ExecStart=$(\r?\n)^ExecStart=.+$', f_string, re.MULTILINE) is not None

        # Ensure a ExecStartPre override is preceeded by a 'ExecStartPre=' reset instruction
        if re.search(r'^ExecStartPre=.+$', f_string, re.MULTILINE) is not None:
            assert re.search(r'^ExecStartPre=$(\r?\n)^ExecStartPre=.+$', f_string, re.MULTILINE) is not None


def test_unit_overrides(host):
    smgr = host.ansible("setup")["ansible_facts"]["ansible_service_mgr"]
    if smgr == 'systemd':
        fname = '/etc/systemd/system/dnsdist.service.d/override-unit.conf'
        f = host.file(fname)

        assert f.exists
        assert re.search(r'^PartOf=network.service$', f.content.decode(), re.MULTILINE) is not None


def test_environment_overrides(host):
    smgr = host.ansible("setup")["ansible_facts"]["ansible_service_mgr"]
    if smgr == 'systemd':
        fname = '/etc/systemd/system/dnsdist.service.d/override-environment.conf'
        f = host.file(fname)

        assert f.exists
        assert re.search(r'^Environment=TZ=UTC$', f.content.decode(), re.MULTILINE) is not None
