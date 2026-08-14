## v1.7.3 (Unreleased)

NEW FEATURES:
- Add `dnsdist_config_format` to write the configuration in YAML instead of Lua, and `dnsdist_config_yaml` to hold it. The default stays `lua`, so an existing playbook is unaffected. The dict is submitted as given, without the role interpreting or renaming anything, and a value that arrives as a string is converted to a real number or boolean, because the YAML parser of dnsdist rejects a quoted number where it wants a real one. The two formats are separate inputs: in `yaml` the Lua-shaped variables are ignored, with the console key the one exception, since it is generated once and read back from `console.key` on later runs ([\#199](https://github.com/PowerDNS/dnsdist-ansible/pull/199))
- Add `dnsdist_config_yaml_string_keys` for the settings whose value must stay a string even when it looks like a number or a boolean. Type conversion follows the shape of the value, since a template cannot know the type a setting declares, so without this a password of `12345678` would be written as an integer and a backend named `no` as `false`. The rule matches by key name at any depth and reaches inside lists ([\#199](https://github.com/PowerDNS/dnsdist-ansible/pull/199))
- Fail the run when `dnsdist_config_format` and the extension of `dnsdist_config_location` disagree. dnsdist picks its parser from the file name, so a YAML document written to a `.conf` file is read as Lua - and silently: the configuration check passes, because it runs against a name the role chooses, and the daemon then fails at start ([\#199](https://github.com/PowerDNS/dnsdist-ansible/pull/199))
- Add `dnsdist_config_remove_stale_yaml`, which removes the YAML configuration file an earlier `yaml` run wrote when the format goes back to `lua`. Given both files, a dnsdist started without an explicit `--config` reads the `.yml` one, so the leftover would otherwise stay in charge and the Lua configuration be ignored ([\#199](https://github.com/PowerDNS/dnsdist-ansible/pull/199))
- Add `dnsdist_service_masked` to mask or unmask the service unit. Masking is a systemd concept and is ignored on hosts without systemd ([\#198](https://github.com/PowerDNS/dnsdist-ansible/pull/198))
- Add Arch Linux support. The package is `dnsdist`, the configuration lives in `/etc/dnsdist.conf` (`/etc/dnsdist-<instance>.conf` for the templated unit) and the process runs as `dnsdist` ([\#197](https://github.com/PowerDNS/dnsdist-ansible/pull/197))
- Add `dnsdist_service_name` and `dnsdist_config_location` so the role can manage an instance of the templated `dnsdist@.service` unit. The systemd drop-in directory follows the service name ([\#195](https://github.com/PowerDNS/dnsdist-ansible/pull/195))
- Add `dnsdist_flush_handlers` to run the notified handlers at the end of the role instead of at the end of the play, which is required when the role runs more than once in a play ([\#195](https://github.com/PowerDNS/dnsdist-ansible/pull/195))
- Add the `multi-instance` Molecule scenario, which configures two instances in a single play ([\#195](https://github.com/PowerDNS/dnsdist-ansible/pull/195))

BREAKING CHANGES:
- Require ansible-core 2.16 or newer. Support for 2.15 is dropped, and Enterprise Linux 8 targets must be managed with 2.16 because their system Python is 3.6 ([\#197](https://github.com/PowerDNS/dnsdist-ansible/pull/197))

IMPROVEMENTS:
- Read facts through `ansible_facts` instead of the injected top-level `ansible_*` variables. ansible-core deprecated that injection and removes it in 2.24, after which a role reading `ansible_distribution` would break. The Molecule configuration sets `inject_facts_as_vars: false`, so a missed reference fails a test run instead of surfacing on a future ansible-core ([\#197](https://github.com/PowerDNS/dnsdist-ansible/pull/197))
- Cap every collection in `requirements.yml`. A collection that raises its `requires_ansible` in a new major would otherwise break the ansible-core 2.16 leg on the day it is published, without a change in this repository ([\#197](https://github.com/PowerDNS/dnsdist-ansible/pull/197))
- Manage the service with `ansible.builtin.systemd_service` on systemd hosts and with `ansible.builtin.service` on hosts without systemd, instead of mixing the two modules across the service task and the handlers ([\#197](https://github.com/PowerDNS/dnsdist-ansible/pull/197))
- Declare Ubuntu 26.04, Arch Linux and FreeBSD in the Galaxy metadata ([\#197](https://github.com/PowerDNS/dnsdist-ansible/pull/197))
- Rework apt and dnf repo file creation to stop using version suffixed file names which are not cleaned up on version changes ([\#183](https://github.com/PowerDNS/dnsdist-ansible/pull/183), @l00d3r)
- Remove version suffixed apt and dnf repo files ([\#183](https://github.com/PowerDNS/dnsdist-ansible/pull/183), @l00d3r)
- Document the role tags, check mode support (converged hosts only) and the package/service state variables in the README ([\#194](https://github.com/PowerDNS/dnsdist-ansible/pull/194))
- Document the handler behaviour and the multi-instance usage in the README ([\#195](https://github.com/PowerDNS/dnsdist-ansible/pull/195))

REMOVED FEATURES:
- Stop testing the `dnsdist-master` repository and test the three most recent release series instead. The `dnsdist_powerdns_repo_master` preset is unchanged and still usable ([\#197](https://github.com/PowerDNS/dnsdist-ansible/pull/197))

BUG FIXES:
- Skip the restart under `--skip-tags service`. Ansible filters tasks by tag but not handlers, so a run that deliberately left the service alone still restarted it on a configuration change - and restarting an inactive unit starts it. The handlers read `ansible_skip_tags` and still reload the units, so a `--tags config` run is unaffected ([\#198](https://github.com/PowerDNS/dnsdist-ansible/pull/198))
- Reload the systemd units in the same task that restarts the service. A restart can no longer run against a unit systemd has not read, and a host left with a drop-in systemd never loaded is repaired by the next change instead of restarting onto the stale unit ([\#198](https://github.com/PowerDNS/dnsdist-ansible/pull/198))
- Reload the systemd units in the service task when this run changed a drop-in. Handlers flush at the end of the play, so a service that was not running yet was started from the unit systemd had loaded before the run and kept the previous settings until the handler restarted it ([\#198](https://github.com/PowerDNS/dnsdist-ansible/pull/198))
- Remove the drop-in override directory when `dnsdist_package_state: absent`, so a later reinstall does not inherit the overrides of the previous installation. The task is tagged `install`, because removal runs through the install path ([\#198](https://github.com/PowerDNS/dnsdist-ansible/pull/198))
- Remove the drop-in of an override dict that is emptied. `override.conf`, `override-unit.conf` and `override-environment.conf` used to stay on disk, so clearing `dnsdist_service_overrides`, `dnsdist_unit_overrides` or `dnsdist_environment_overrides` kept the previous settings applied forever. Only the file of the emptied dict is removed ([\#198](https://github.com/PowerDNS/dnsdist-ansible/pull/198))
- Correct the FreeBSD paths and ownership. The configuration lives in `/usr/local/etc/dnsdist/dnsdist.conf` and the process runs as `_dnsdist`, following the `dns/dnsdist` port ([\#197](https://github.com/PowerDNS/dnsdist-ansible/pull/197))
- Restart the service after a systemd drop-in changes. The reload handler notified the restart handler, but a daemon reload alone never reports `changed`, so the notification was dropped and a modified `dnsdist_service_overrides`, `dnsdist_unit_overrides` or `dnsdist_environment_overrides` never took effect ([\#197](https://github.com/PowerDNS/dnsdist-ansible/pull/197))
- Restart the service on hosts without systemd. The restart handler and the `daemon_reload` handler used the systemd module unconditionally, so a FreeBSD run failed as soon as a configuration change notified them ([\#197](https://github.com/PowerDNS/dnsdist-ansible/pull/197))
- Skip the debug symbols package on platforms that ship none. `dnsdist_debug_symbols_package_name` was referenced unconditionally by the `dnsdist_force_reinstall` path, where it is undefined on FreeBSD ([\#197](https://github.com/PowerDNS/dnsdist-ansible/pull/197))
- Tag the tasks inside `install.yml`, `configure.yml` and `repo-*.yml` so that `--tags install`, `--tags config` and `--tags repository` no longer run the include and skip its body. A dynamic `include_tasks` does not pass its tags to the tasks it includes, so filtered runs silently did nothing and still exited 0 ([\#194](https://github.com/PowerDNS/dnsdist-ansible/pull/194))
- Add `check_mode: false` to the control socket key probe so `--check` against a converged host no longer reports the configuration file as changed with the existing `setKey(...)` line removed ([\#194](https://github.com/PowerDNS/dnsdist-ansible/pull/194))
- Read the service name and state from facts published per role invocation in the restart handlers. Ansible shares handlers between invocations of the same role and resolves role parameters to the last invocation, so a play with more than one instance restarted the wrong service. Correct restarts need `dnsdist_flush_handlers: true` as well ([\#195](https://github.com/PowerDNS/dnsdist-ansible/pull/195))

## v1.7.2 (2026-02-23)

BUG FIXES:
- Fix the `namespace` in meta/main.yml must match the registered Galaxy namespace exactly as `powerdns`.

## v1.7.1 (2026-02-23)

BUG FIXES:
- Fix the `namespace` in meta/main.yml must match the registered Galaxy namespace exactly as `PowerDNS`.

## v1.7.0 (2026-02-23)

NEW FEATURES:
- Add dnsdist 2.1 repository preset (`dnsdist_powerdns_repo_21`) and a Molecule scenario/test suite for `dnsdist-21` (https://github.com/PowerDNS/dnsdist-ansible/pull/166).
- Add package lifecycle control via `dnsdist_package_state` (`present`, `latest`, `absent`) (https://github.com/PowerDNS/dnsdist-ansible/pull/166).
- Add Debian architecture mapping for Deb822 repository setup (`x86_64/amd64 -> amd64`, `aarch64/arm64/armv8l -> arm64`) (https://github.com/PowerDNS/dnsdist-ansible/pull/166).

IMPROVEMENTS:
- Switch Debian repository management to `ansible.builtin.deb822_repository` (https://github.com/PowerDNS/dnsdist-ansible/pull/166).
- Refresh supported platforms and metadata: EL 10, Debian trixie, Ubuntu noble; set `min_ansible_version` to 2.15 (https://github.com/PowerDNS/dnsdist-ansible/pull/166).
- Expand and modernize Molecule targets/images (new `el-systemd` and `debian-systemd` templates, updated distro matrix, and multi-architecture Docker build support) (https://github.com/PowerDNS/dnsdist-ansible/pull/166).
- Improve role defaults and documentation consistency (booleans, repository examples, default config ownership) (https://github.com/PowerDNS/dnsdist-ansible/pull/166).

REMOVED / EOL:
- Remove dnsdist-18 repository preset and Molecule scenario (https://github.com/PowerDNS/dnsdist-ansible/pull/166).
- Remove legacy APT source template (`templates/dnsdist.sources.j2`) in favor of Deb822 repository management (https://github.com/PowerDNS/dnsdist-ansible/pull/166).
- Remove legacy prepare-task flow (`tasks/prepare.yml`) from role execution (https://github.com/PowerDNS/dnsdist-ansible/pull/166).

BUG FIXES:
- Fix package list rendering in install tasks (remove undefined `item` usage; support both dict and string additional package inputs) (https://github.com/PowerDNS/dnsdist-ansible/pull/166).
- Fix systemd environment override template to use `dnsdist_environment_overrides` (https://github.com/PowerDNS/dnsdist-ansible/pull/166).
- Fix Molecule Docker image discovery/build conditions and image naming to avoid cache/cross-architecture mismatches (https://github.com/PowerDNS/dnsdist-ansible/pull/166).
- Fix test coverage gaps for repository pinning checks and Debian architecture assertions (https://github.com/PowerDNS/dnsdist-ansible/pull/166).
- Fix Debian/Ubuntu Molecule images by installing required system packages (including `python3-apt` and `adduser`) to avoid package post-install failures (https://github.com/PowerDNS/dnsdist-ansible/pull/166).
- Fix test assertions for `setKey("...")` to ensure active (non-commented) configuration lines are validated (https://github.com/PowerDNS/dnsdist-ansible/pull/166).

## v1.6.0 (2025-10-29)

NEW FEATURES:
- Add dnsdist 1.8 ([\#78](https://github.com/PowerDNS/dnsdist-ansible/pull/78))
- Added ol9 ([\#82](https://github.com/PowerDNS/dnsdist-ansible/pull/82))
- Add variable `dnsdist_config_files` for add additional configuration files ([\#145](https://github.com/PowerDNS/dnsdist-ansible/pull/145))
- Add variable `dnsdist_additional_packages` for add additional dependency packages. Set `no_log: true` for "Get installed packages facts" task.  ([\#146](https://github.com/PowerDNS/dnsdist-ansible/pull/146))
- Update for DNSdist 19 and 20, and apt fixes   ([\#152](https://github.com/PowerDNS/dnsdist-ansible/pull/152))

IMPROVEMENTS:
- GH Actions: test weekly and new CI targets ([\#118](https://github.com/PowerDNS/dnsdist-ansible/pull/118))
- CI tests: upgraded version of molecule and ansible-core packages ([\#136](https://github.com/PowerDNS/dnsdist-ansible/pull/136))
- Change the order of tasks for additional files and configration file  ([\#150](https://github.com/PowerDNS/dnsdist-ansible/pull/150))

REMOVED / EOL:
- Removed EOL dnsdist15 ([\#84](https://github.com/PowerDNS/dnsdist-ansible/pull/84))
- Remove sleep Option from handler ([\#86](https://github.com/PowerDNS/dnsdist-ansible/pull/86))
- Removed EOL targets RHEL-7 and Debian-10 ([\#127](https://github.com/PowerDNS/dnsdist-ansible/pull/127))

BUG FIXES:
- unbreak CI, bump a few things ([\#97](https://github.com/PowerDNS/dnsdist-ansible/pull/97))
- ansible-lint should no longer complain ([\#99](https://github.com/PowerDNS/dnsdist-ansible/pull/99))
- Unbreak CI again ([\#100](https://github.com/PowerDNS/dnsdist-ansible/pull/100))
- GH Actions: fix issues with CI  ([\#125](https://github.com/PowerDNS/dnsdist-ansible/pull/125))
- Change the order of tasks for additional files  ([\#150](https://github.com/PowerDNS/dnsdist-ansible/pull/150))

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
