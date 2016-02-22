dnsdist
=======
This sets up dnsdist. Note: this role is in development and cannot be considered stable at the moment.

Requirements
------------
Ansible 2.0+.

Role Variables
--------------
## dnsdist_acls
A list of dnsdist ACLS (netmasks) to add to the configuration.

## dnsdist_carbonserver
The IP address of the Carbon server that shoudl receive metrics.

## dnsdist_config
A string containing the full config for dnsdist. This is copied verbatim to the dnsdist.conf file.

## dnsdist_controlsocket
The IP address to listen on for the control socket.

## dnsdist_locals
A list of IP addresses dnsdist should listen on.

## dnsdist_repo_branch
When `dnsdist_repo_provider` is set to 'powerdns', use packages from this branch. By default this is 'master', but can be set to '10' for 1.0.X releases.

## dnsdist_repo_provider
When this is set to 'powerdns' (the default), the PowerDNS [dnsdist repositories](http://repo.powerdns.com) are added and dnsdist is installed from there. Set this to 'os' to use the distribution provided packages.

## dnsdist_servers
A list of IP addresses denoting the downstream DNS servers in the default pool.

## dnsdist_setkey
A string that has the key for the dnsdist client.

## dnsdist_version
Set to 'latest', set this to a specific version (or wildcard like '1.0*') to install a specific dnsdist version.

## dnsdist_webserver_address
The IP address where the built-in webserver should listen, empty (and thus disabled) by default.

## dnsdist_webserver_password
The password for the webserver. Must be set when dnsdist_webserver_address is set.


Example Playbook
----------------

```
- hosts: localhost
  remote_user: root
  roles:
    - {role: dnsdist,
       dnsdist_servers: ['8.8.8.8', '8.8.4.4'],
       dnsdist_webserver_password: 'geheim'}
```

```
- hosts: localhost
  remote_user: root
  roles:
    - { role: dnsdist,
        dnsdist_config: |
          setACL("127.0.0.1/8")
          newServer("192.0.2.53")
      }
```

License
-------

GPLv2

Author Information
------------------
Pieter Lexis (PowerDNS) <pieter.lexis@powerdns.com>
