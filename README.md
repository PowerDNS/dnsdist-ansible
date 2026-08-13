# Ansible Role: dnsdist

[![Build Status](https://github.com/PowerDNS/dnsdist-ansible/actions/workflows/main.yml/badge.svg)](https://github.com/PowerDNS/dnsdist-ansible)
[![License](https://img.shields.io/badge/license-MIT%20License-brightgreen.svg)](https://opensource.org/licenses/MIT)
[![Ansible Role](https://img.shields.io/badge/ansible%20role-PowerDNS.dnsdist-blue.svg)](https://galaxy.ansible.com/PowerDNS/dnsdist)
[![GitHub tag](https://img.shields.io/github/tag/PowerDNS/dnsdist-ansible.svg)](https://github.com/PowerDNS/dnsdist-ansible/tags)

An Ansible role create by the folks behind PowerDNS to set up [dnsdist](https://dnsdist.org/).

## Requirements

An ansible-core 2.16 or newer installation. Enterprise Linux 8 targets must be
managed with ansible-core 2.16: their system Python is 3.6, which the modules of
ansible-core 2.20 cannot run.

## Dependencies

None.

## Role Variables

Available variables are listed below, along with default values (see `defaults/main.yml`):

```yaml
dnsdist_install_repo: ""
```

By default, dnsdist is installed from the software repositories configured on the target hosts.

```yaml
# Install dnsdist from the master branch
- hosts: dnsdist
  roles:
  - { role: PowerDNS.dnsdist,
      dnsdist_install_repo: "{{ dnsdist_powerdns_repo_master }}"

# Install dnsdist 1.3.x
- hosts: dnsdist
  roles:
  - { role: PowerDNS.dnsdist,
      dnsdist_install_repo: "{{ dnsdist_powerdns_repo_13 }}"
```

The examples above, show how to install DNSdist from the official PowerDNS repositories
(see the complete list of pre-defined repos in `vars/main.yml`).

```yaml
- hosts: all
  vars:
    dnsdist_install_repo:
      name: "dnsdist" # the repository name
      apt_repo_origin: "example.com"  # used to pin dnsdist to the provided repository
      apt_version: "dnsdist-19"  # deb822 suites suffix (appended to release codename)
      gpg_key_url: "http://example.com/MYREPOGPGPUBKEY.asc" # repository public GPG key
      yum_repo_baseurl: "http://example.com/centos/$basearch/$releasever/dnsdist"
      yum_debug_symbols_repo_baseurl: "http://example.com/centos/$basearch/$releasever/dnsdist/debug"
  roles:
  - { role: PowerDNS.dnsdist }
```

It is also possible to install dnsdist from custom repositories as demonstrated in the example above.

```yaml
dnsdist_install_epel: true
```

By default, install EPEL to satisfy some DNSdist dependencies like `lidsodium`.
To skip the installation of EPEL set the `dnsdist_install_epel` variable to `false`.

```yaml
dnsdist_package_name: "{{ default_dnsdist_package_name }}"
```

The name of the dnsdist package: "dnsdist" on both RHEL and Debian derivates distributions.

```yaml
dnsdist_package_version: ""
```

Optionally, allow to set a specific version of the dnsdist package to be installed.

```yaml
dnsdist_package_state: "present"
```

The desired state of the dnsdist packages. Use `"present"` (default) to install, `"latest"` to upgrade, or `"absent"` to uninstall.

```yaml
dnsdist_install_debug_symbols_package: false
```

Install dnsdist debug symbols package.

```yaml
dnsdist_debug_symbols_package_name: "{{ default_dnsdist_debug_symbols_package_name }}"
```

The name of the dnsdist debug symbols package to be installed when `dnsdist_install_debug_symbols_package` is `true`.


```yaml
dnsdist_additional_packages: []
```

List of additional packages to install, list support version pining for each of the packages.

```yaml
dnsdist_acls: []
```

Configures the dnsdist ACLS (netmasks).

```yaml
dnsdist_locals: ['127.0.0.1:5300']
```

Configure dnsdist's listen addresses.

```yaml
dnsdist_servers:
  - '127.0.0.1'
  - "{ address='127.0.0.1:5300', source='127.0.0.1@lo', order=1 }"
```

The list of IP addresses of the downstream DNS servers dnsdist should be send traffic to
OR of Lua tables that the newServer function ( https://dnsdist.org/reference/config.html#newServer ) can parse.

```yaml
dnsdist_carbonserver: ""
```

The IP address of the Carbon server that should receive dnsdist metrics.

```yaml
dnsdist_setkey: ""
```

Encryption key for the dnsdist's TCP control socket. If it is empty, a random key will be generated. If a key is already present in the configuration file, it will be kept.

```yaml
dnsdist_generatekey: "{{ (dnsdist_setkey | length == 0) | bool }}"
```

Whether to auto-generate a control socket encryption key. Defaults to `true` when `dnsdist_setkey` is empty.

```yaml
dnsdist_controlsocket: "127.0.0.1"
```

The listen IP address of the dnsdist's TCP control socket.

```yaml
dnsdist_webserver_address: ""
```

The listen IP address of the built-in webserver, empty thus disable by default.

```yaml
dnsdist_webserver_password: ""
```

The authentication credentials for the built-in webserver. Must be set when `dnsdist_webserver_address` is set.

```yaml
dnsdist_webserver_apikey: ""
```

The authentication credentials for the built-in API.

```yaml
dnsdist_webserver_acl: ""
```

Since 1.5.0, only connections from 127.0.0.1 and ::1 are allowed by default. See https://dnsdist.org/guides/webserver.html for more information.

```yaml
dnsdist_config: ""
```

Additional dnsdist configuration to be injected verbatim in the configuration file.

```yaml
dnsdist_config_files: {}
```

Additional dnsdist configuration files to be placed in the configuration directory.

```yaml
dnsdist_config_owner: ""
dnsdist_config_group: ""
```

User and Group that own the configuration file. When empty, version-specific defaults are used.

```yaml
dnsdist_service_overrides: {}
```

Dict with overrides for the service (systemd only).
This can be used to change any systemd settings in the `[Service]` category.

```yaml
dnsdist_unit_overrides: {}
```

Dict with overrides for the service unit (systemd only).
This can be used to change any systemd settings in the `[Unit]` category.

```yaml
dnsdist_environment_overrides: {}
```

Dict with overrides for the service environments (systemd only).
This can be used to change any environment variables in systemd settings in the `[Service]` category.

The three dicts are written to `override.conf`, `override-unit.conf` and
`override-environment.conf` in `/etc/systemd/system/<service name>.service.d/`. Emptying one of
them removes its own file again and restarts the service; the other two files and any drop-in an
operator added next to them are left alone.

```yaml
dnsdist_service_name: "dnsdist"
```

Name of the managed service. Set it to `dnsdist@<instance>` to manage an instance of the templated
systemd unit shipped by the dnsdist packages, and set `dnsdist_config_location` to the matching
`/etc/dnsdist/dnsdist-<instance>.conf`. See [Handlers](#handlers).

```yaml
dnsdist_config_location: "{{ default_dnsdist_config_location }}"
```

Location of the configuration file, `/etc/dnsdist/dnsdist.conf` on Linux and
`/usr/local/etc/dnsdist.conf` on FreeBSD. The additional files from `dnsdist_config_files` are
written next to it.

```yaml
dnsdist_service_state: "started"
dnsdist_service_enabled: true
dnsdist_service_masked: false
```

Allow to specify the desired state of the DNSdist service.
E.g. This allows to install and configure DNSdist without automatically starting the service.
Masking is a systemd concept and is ignored on hosts without systemd.

```yaml
dnsdist_disable_handlers: false
```

Disable automated service restart on configuration changes.

```yaml
dnsdist_flush_handlers: false
```

Run the notified handlers at the end of the role instead of at the end of the play. See
[Handlers](#handlers).

```yaml
dnsdist_tlslocals: []
```
Configures DNS over TLS listeners. The entries are copied verbatim entry-by-entry.

```yaml
dnsdist_force_reinstall: false
```

Force reinstall of dnsdist packages by performing a removal prior to the package installation steps. Intended for usage where a downgrade of dnsdist needs to be performed.

## Role Tags

Tags for `--tags` / `--skip-tags`:

- `repository`: repo and GPG key setup, APT pinning, removal of stale versioned repo files.
- `install`: package installation and removal.
- `config` (alias `configure`): config files, systemd overrides, control socket key.
- `service`: service state.
- `always`: OS variable import.

Repository tasks are also tagged `install`. The control socket key tasks are tagged `install`,
`configure` and `config`, so the key exists before the config is rendered.

Contributors: tags belong on the tasks inside `install.yml`, `configure.yml` and `repo-*.yml`, not
only on the `include_tasks` in `tasks/main.yml`. A dynamic `include_tasks` does not pass its tags
to included tasks, so a narrow `--tags` run would execute the include and skip its body, silently,
with `rc=0`.

## Check Mode

Supported only on a host where this role already ran successfully.

Converged host: `--check` reports real drift only. Read-only probes such as the key lookup carry
`check_mode: false` so they still run and register results; they change nothing. Without that,
every run reports the config as changed with the existing `setKey(...)` removed.

Fresh host: `--check` is expected to fail. It installs neither the repository, `python3-debian`
nor the package, so `deb822_repository` fails and the config cannot be validated without the
`dnsdist` binary.

## Package and Service State

- `dnsdist_package_state`: `present`, `latest`, `absent`, ...
- `dnsdist_force_reinstall`: remove before install, for downgrades.
- `dnsdist_service_state` (`started`, `stopped`, `restarted`, `reloaded`),
  `dnsdist_service_enabled`, `dnsdist_service_masked` (systemd hosts only).

`dnsdist_package_state: absent` removes the packages, but the config and service tasks still run,
so a full run fails on the service task (`Could not find the requested service dnsdist`). Remove
via the install path only:

```bash
ansible-playbook site.yml -e dnsdist_package_state=absent --tags install
```

Works with or without the config file present.

## Handlers

Handlers run at the end of the play, and Ansible shares them between invocations of the same role.
A role parameter read inside a handler resolves to the value of the *last* invocation, so with more
than one invocation in a play the restart targets the wrong service or is collapsed into a single
run. Set `dnsdist_flush_handlers: true` to run `meta: flush_handlers` as the last task of the role,
which restarts the `dnsdist_service_name` of that invocation.

Every instance needs its own service name and configuration file; the templated systemd unit reads
`/etc/dnsdist/dnsdist-<instance>.conf`:

```yaml
- hosts: dnsdist
  tasks:
    - name: Instance a
      ansible.builtin.include_role:
        name: PowerDNS.dnsdist
      vars:
        dnsdist_service_name: dnsdist@a
        dnsdist_config_location: /etc/dnsdist/dnsdist-a.conf
        dnsdist_locals: ['127.0.0.1:5301']
        dnsdist_controlsocket: '127.0.0.1:5401'
        dnsdist_flush_handlers: true

    - name: Instance b
      ansible.builtin.include_role:
        name: PowerDNS.dnsdist
      vars:
        dnsdist_service_name: dnsdist@b
        dnsdist_config_location: /etc/dnsdist/dnsdist-b.conf
        dnsdist_locals: ['127.0.0.1:5302']
        dnsdist_controlsocket: '127.0.0.1:5402'
        dnsdist_flush_handlers: true
```

The `dnsdist_locals` and `dnsdist_controlsocket` of every instance have to differ, otherwise the
second instance cannot bind its addresses.

The systemd overrides of an instance are written to `/etc/systemd/system/<service name>.service.d/`.

`meta: flush_handlers` is play-wide: it also runs handlers that earlier roles in the same play
notified. `dnsdist_disable_handlers: true` skips the restart handlers entirely.

`dnsdist_flush_handlers` defaults to `false`, which is correct for a single invocation and wrong
for more than one: without it the pending restarts of every instance run once, at the end of the
play, against the service name of the last invocation.

On systemd hosts the restart handler reloads the units in the same task, so a restart never runs
against a unit systemd has not read. The reload happens even when `dnsdist_service_state: stopped`
keeps the service down, so the next manual start uses the drop-ins this run wrote.

Tag selection filters tasks, not handlers: under `--skip-tags service` the service task is skipped,
but a configuration change still notifies the restart handler, and restarting an inactive unit
starts it. Use `dnsdist_disable_handlers: true` to apply configuration without touching the running
service.

## Example Playbook

Deploy dnsdist in front of Quad9 and enable the web monitoring interface

```yaml
- hosts: dnsdist
  roles:
    - { role: PowerDNS.dnsdist,
        dnsdist_servers: ['9.9.9.9'],
        dnsdist_webserver_address: "{{ ansible_default_ipv4['address'] }}:8083",
        dnsdist_webserver_password: 'geheim' }
```

## Changelog

A detailed changelog of all the changes applied to the role is available [here](./CHANGELOG.md).

## Testing

Tests are performed by [Molecule](http://molecule.readthedocs.org/en/latest/).

```bash
$ pip install tox
$ tox
```

See [molecule/README.md](./molecule/README.md) for the test layout, how to run a
single leg, and what to change when a new release or operating system has to be
covered.

## License

MIT
