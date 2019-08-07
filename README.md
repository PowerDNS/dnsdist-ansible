# Ansible Role: dnsdist

[![Build Status](https://travis-ci.org/PowerDNS/dnsdist-ansible.svg?branch=master)](https://travis-ci.org/PowerDNS/dnsdist-ansible)
[![License](https://img.shields.io/badge/license-MIT%20License-brightgreen.svg)](https://opensource.org/licenses/MIT)
[![Ansible Role](https://img.shields.io/badge/ansible%20role-PowerDNS.dnsdist-blue.svg)](https://galaxy.ansible.com/PowerDNS/dnsdist)
[![GitHub tag](https://img.shields.io/github/tag/PowerDNS/dnsdist-ansible.svg)](https://github.com/PowerDNS/dnsdist-ansible/tags)

An Ansible role create by the folks behind PowerDNS to set up [dnsdist](https://dnsdist.org/).

## Requirements

An Ansible 2.2 or higher installation.

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

The examples above, show how to install dnsdist from the official PowerDNS repositories
(see the complete list of pre-defined repos in `vars/main.yml`).

```yaml
- hosts: all
  vars:
    dnsdist_install_repo:
      name: "dnsdist" # the repository name
      apt_repo_origin: "example.com"  # used to pin dnsdist to the provided repository
      apt_repo: "deb http://example.com/{{ ansible_distribution | lower }} {{ ansible_distribution_release | lower }}/dnsdist main"
      gpg_key: "http://example.com/MYREPOGPGPUBKEY.asc" # repository public GPG key
      gpg_key_id: "MYREPOGPGPUBKEYID" # to avoid to reimport the key each time the role is executed
      yum_repo_baseurl: "http://example.com/centos/$basearch/$releasever/dnsdist"
      yum_debug_symbols_repo_baseurl: "http://example.com/centos/$basearch/$releasever/dnsdist/debug"
  roles:
  - { role: PowerDNS.dnsdist }
```

It is also possible to install dnsdist from custom repositories as demonstrated in the example above.

```yaml
dnsdist_install_epel: True
```

By default, install EPEL to satisfy some dnsdist dependencies like `lidsodium`.
To skip the installtion of EPEL set the `dnsdist_install_epel` variable to `False`.

```yaml
dnsdist_package_name: "{{ default_dnsdist_package_name }}"
```

The name of the dnsdist package: "dnsdist" on both RHEL and Debian derivates distributions.

```yaml
dnsdist_package_version: ""
```

Optionally, allow to set a specific version of the dnsdist package to be installed.

```yaml
dnsdist_install_debug_symbols_package: False
```

Install dnsdist debug symbols package.

```yaml
dnsdist_debug_symbols_package_name: "{{ default_dnsdist_debug_symbols_package_name }}"
```

The name of the dnsdist debug symbols package to be installed when `dnsdist_install_debug_symbols_package` is `True`.

```yaml
dnsdist_acls: []
```

Configures the dnsdist ACLS (netmasks).

```yaml
dnsdist_locals: ['127.0.0.1:5300']
```

Configure dnsdist's listen addresses.

```yaml
dnsdist_servers: []
```

The list of IP addresses of the downstream DNS servers dnsdist should be send traffic to.

```yaml
dnsdist_carbonserver: ""
```

The IP address of the Carbon server that should receive dnsdist metrics.

```yaml
dnsdist_controlsocket: "127.0.0.1"
```

The listen IP address of the dnsdist's TCP control socket.

```yaml
dnsdist_setkey: ""
```

Encryption key for the dnsdist's TCP control socket.

```yaml
dnsdist_webserver_address: ""
```

The listen IP address of the built-in webserver, empty thus disable by default.

```yaml
dnsdist_webserver_password: ""
```

The authentication credentials fro the build-in webserver. Must be set when `dnsdist_webserver_address` is set.

```yaml
dnsdist_config: ""
```

Additional dnsdist configuration to be injected verbatim in the `dnsdist.conf` file.

```yaml
dnsdist_service_overrides: {}
```

Dict with overrides for the service (systemd only).
This can be used to change any systemd settings in the `[Service]` category.

```yaml
dnsdist_service_state: "started"
dnsdist_service_enabled: "yes"
```

Allow to specify the desired state of the DNSdist service.
E.g. This allows to install and configure DNSdist without automatically starting the service.

```yaml
dnsdist_disable_handlers: False
```

Disable automated service restart on configuration changes.

```yaml
dnsdist_tlslocals: []
```
Configures DNS over TLS listeners. The entries are copied verbatim entry-by-entry.

## Example Playbook

Deploy dnsdist in front of Quad9 and enable the web monitoring interface

```yaml
- hosts: dnsdist
  roles:
    - { role: PowerDNS.dnsdist,
        dnsdist_servers: ['9.9.9.9'],
        dnsdist_webserver_address: "{{ ansible_default_ipv4['address']:8083 }}",
        dnsdist_webserver_password: 'geheim' }
```

## Changelog

A detailed changelog of all the changes applied to the role is available [here](./CHANGELOG.md).

## Testing

Tests are performed by [Molecule](http://molecule.readthedocs.org/en/latest/).

    $ pip install tox

To test all the scenarios run

    $ tox

To run a custom molecule command

    $ tox -e py27-ansible22 -- molecule test -s dnsdist-13

## License

MIT
