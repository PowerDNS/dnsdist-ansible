# Ansible Role: dnsdist

[![Build Status](https://travis-ci.org/PowerDNS/dnsdist-ansible.svg?branch=master)](https://travis-ci.org/PowerDNS/dnsdist-ansible)
[![License](https://img.shields.io/badge/license-MIT%20License-brightgreen.svg)](https://opensource.org/licenses/MIT)
[![Ansible Role](https://img.shields.io/badge/ansible%20role-PowerDNS.dnsdist-blue.svg)](https://galaxy.ansible.com/PowerDNS/dnsdist)
[![GitHub tag](https://img.shields.io/github/tag/PowerDNS/dnsdist-ansible.svg)](https://github.com/PowerDNS/dnsdist-ansible/tags)

An Ansible role create by the folks behind PowerDNS to set up [dnsdist](https://dnsdist.org/).

## Requirements

An Ansible 2.3 or higher installation.

## Dependencies

None.

## Role Variables

Available variables are listed below, along with default values (see `defaults/main.yml`):

```yaml
dnsdist_install_repo: ""
```

By default dnsdist is installed from the software repositories availableavailable  on the target hosts.

To install dnsdist from the official PowerDNS repositories,
override the `dnsdist_install_repo` variable value as follow
(see the complete list of pre-defined repos in `vars/main.yml`):

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

The install dnsdist from a custom repository set the `dnsdist_install_repo` variable as shown below:

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

Note that when targeting only a specific platform (e.g. Debian) it's not needed to provide other platform (e.g. yum) repositories information.

```yaml
dnsdist_install_epel: True
```

By defaul, install EPEL to satisfy some dnsdist dependencies like `lidsodium`.
To skip the installtion of EPEL set the `dnsdist_install_epel` variable to `False`.

```yaml
dnsdist_package_name: "{{ default_dnsdist_package_name }}"
```

The name of the dnsdist package: "dnsdist" on both RHEL and Debian derivates distributions.

```yaml
dnsdist_package_version: ""
```

Install a specific version of dnsdist

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

A list of dnsdist ACLS (netmasks) to add to the configuration.

```yaml
dnsdist_locals: ['127.0.0.1:5300']
```

A list of IP addresses dnsdist should listen on.

```yaml
dnsdist_servers: []
```

A list of IP addresses of the downstream DNS servers in the default pool.

```yaml
dnsdist_carbonserver: ""
```

The IP address of the Carbon server that should receive dnsdist metrics.

```yaml
dnsdist_controlsocket: "127.0.0.1"
```

The IP address to listen on for the control socket connections.

```yaml
dnsdist_setkey: ""
```

A string that has the key for the dnsdist client.

```yaml
dnsdist_webserver_address: ""
```

The IP address where the built-in webserver should listen, empty thus disabled by default.

```yaml
dnsdist_webserver_password: ""
```

The password for the webserver. Must be set when `dnsdist_webserver_address` is set.

```
dnsdist_config: ""
```

A string containing additional configuration for dnsdist to be copied verbatim to the `dnsdist.conf` file.

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

## License

MIT
