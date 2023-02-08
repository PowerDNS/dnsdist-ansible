## v1.5.0 (2023-02-08)

NEW FEATURES:
- Include DNSdist 17 ([\#44](https://github.com/PowerDNS/dnsdist-ansible/pull/44))

IMPROVEMENTS:
- Add varibles to change unit and env vars for dnsdist service ([\#60](https://github.com/PowerDNS/dnsdist-ansible/pull/60))
- Handlers: change the order, order matters when config and service unit were modified ([\#47](https://github.com/PowerDNS/dnsdist-ansible/pull/47))
- Allow for newServer Lua table syntax in dnsdist_servers list ([\#42](https://github.com/PowerDNS/dnsdist-ansible/pull/42))
- Improved Linter coverage ([\#39](https://github.com/PowerDNS/dnsdist-ansible/pull/39))

BUG FIXES:
- Version fix in yum_debug_symbols_repo_baseurl  ([\#69](https://github.com/PowerDNS/dnsdist-ansible/pull/69))
- Fix dependabot spacing and dashes ([\#68](https://github.com/PowerDNS/dnsdist-ansible/pull/68))
- Bump yamllint from 1.26.1 to 1.29.0 ([\#62](https://github.com/PowerDNS/dnsdist-ansible/pull/62))
- Bump actions/checkout from 2 to 3 ([\#48](https://github.com/PowerDNS/dnsdist-ansible/pull/48))
- Webserver needs config in setWebserverConfig (introduced in dnsdist 15) ([\#57](https://github.com/PowerDNS/dnsdist-ansible/pull/57))
- Fix for dnsdist_setkey is ignored ([\#45](https://github.com/PowerDNS/dnsdist-ansible/pull/45))
- Fix CI ([\#39](https://github.com/PowerDNS/dnsdist-ansible/pull/39))

REMOVED FEATURES:
- EOL version repositories (1.4) have been removed ([\#66](https://github.com/PowerDNS/dnsdist-ansible/pull/66))
- Travis integration have been removed ([\#65](https://github.com/PowerDNS/dnsdist-ansible/pull/65))

## v1.4.0 (2021-07-02)

NEW FEATURES:
- Add 1.6 repositories ([\#32](https://github.com/PowerDNS/dnsdist-ansible/pull/32))

IMPROVEMENTS:
- The `dnsdist_setkey` variable is now Ansible Vault-safe ([\#31](https://github.com/PowerDNS/dnsdist-ansible/pull/31))

REMOVED FEATURES:
- EOL version repositories (1.0, 1.1, 1.2, 1.3) have been removed ([\#35](https://github.com/PowerDNS/dnsdist-ansible/pull/35))

## v1.3.0 (2020-09-17)

NEW FEATURES:
- `dnsdist_force_reinstall` flag added to allow a forced downgrade/reinstall ([\#26](https://github.com/PowerDNS/dnsdist-ansible/pull/26))

IMPROVEMENTS:
- Repositories for PowerDNS dnsdist 1.5 added by @xgin ([\#25](https://github.com/PowerDNS/dnsdist-ansible/pull/25))
- Backwards compatibility introduced for dnsdist PR [\#7820](https://github.com/PowerDNS/pdns/pull/7820) ([\#27](https://github.com/PowerDNS/dnsdist-ansible/pull/27))
- Updated Ansible dependency to 2.5 ([\#28](https://github.com/PowerDNS/dnsdist-ansible/pull/28))

## v1.2.1 (2019-02-19)

NEW FEATURES:
- Add some options (`dnsdist_service_state` and `dnsdist_service_enabled`) to configure the status of the dnsdist service ([\#15](https://github.com/PowerDNS/dnsdist-ansible/pull/15))

## v1.2.0 (2018-12-02)

NEW FEATURES:
- Allow to manage systemd overrides ([\#13](https://github.com/PowerDNS/pdns-ansible/pull/13))
- Add an option (`dnsdist_disable_handlers`) to disable the automated restart of the service on configuration changes ([\#14](https://github.com/PowerDNS/dnsdist-ansible/pull/14))

## v1.1.0 (2018-06-25)

IMPROVEMENTS:
- Upgrade molecule to 2.14.0 ([\#10](https://github.com/PowerDNS/dnsdist-ansible/pull/10))
- Improved README file ([\#12](https://github.com/PowerDNS/dnsdist-ansible/pull/12))

BUG FIXES:
- Make sure the `dnsdist_package_version` variable is set correctly ([\#11](https://github.com/PowerDNS/dnsdist-ansible/pull/11))

## v1.0.0 (2018-04-18)

IMPROVEMENTS:
- Improved tests-suite ([\#9](https://github.com/PowerDNS/dnsdist-ansible/pull/9))

NEW FEATURES:
- Dnsdist 1.3 support ([\#9](https://github.com/PowerDNS/dnsdist-ansible/pull/9))
- Debug packages installation ([\#9](https://github.com/PowerDNS/dnsdist-ansible/pull/9))

## v0.2.0 (2017-08-25)

NEW FEATURES:
- Molecule tests ([\#7](https://github.com/PowerDNS/dnsdist-ansible/pull/7))
- Dnsdist 1.2.x support ([\#6](https://github.com/PowerDNS/dnsdist-ansible/pull/6))

## v0.1.1 (2017-07-10)

IMPROVEMENTS:
- Configure correctly the dnsdist.conf file permissions ([\#5](https://github.com/PowerDNS/dnsdist-ansible/pull/5))

## v0.1.0 (2017-06-12)

Initial release.

IMPROVEMENTS:
- Switch to the MIT License ([\#4](https://github.com/PowerDNS/dnsdist-ansible/pull/4))
- Improved installation procedure ([\#3](https://github.com/PowerDNS/dnsdist-ansible/pull/3))
- Improved target distribution detection ([\#1](https://github.com/PowerDNS/dnsdist-ansible/pull/1))
