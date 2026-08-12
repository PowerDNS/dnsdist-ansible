# Molecule test layout

```
molecule/config.yml        shared driver, provisioner and verifier configuration
molecule/platforms/*.yml   platform sets, one per group of operating systems
molecule/default/         install from a PowerDNS repository and configure
molecule/multi-instance/  two instances of dnsdist@.service in a single play
molecule/os-repos/        install from the packages of the distribution
molecule/resources/       playbooks, task files, variables and tests shared by all
```

Three things vary independently and none of them is a scenario:

- the **release** under test, taken from `DNSDIST_VERSION` (`19`, `20`, `21`),
- the **platforms**, taken from the platform set passed with `--base-config`,
- the **ansible-core version**, which follows the platforms and is never chosen
  separately. Enterprise Linux 8 has Python 3.6, which only ansible-core 2.16 can
  manage, and Ubuntu 20.04 has 3.8; everything else runs 2.20, plus one 2.18 leg
  to keep the templating engine from before the 2.19 rewrite covered. See
  [Ansible legs](#ansible-legs).

Run one leg like this:

```bash
DNSDIST_VERSION=21 tox -e ansible220 -- molecule \
  -c molecule/config.yml \
  -c molecule/platforms/dnsdist-21.yml \
  test -s default
```

A bare `molecule` command does not pick this configuration up - Molecule only
auto-discovers a base config at `.config/molecule/config.yml`. Always pass
`-c molecule/config.yml`, which `tox` does for you.

## Ansible legs

Three ansible-core versions are tested. Which one applies follows from the
platform set, never from the scenario:

| leg | tox env | target Python floor | what it is for |
|---|---|---|---|
| 2.16 | `ansible216` | 3.6 | Enterprise Linux 8, and Ubuntu 20.04 where the release has focal packages. 2.16 is the last ansible-core whose modules run on Python 3.6 and those hosts cannot move to a newer one, so the role has to keep working with it. These platforms never run under another leg. |
| 2.18 | `ansible218` | 3.8 | The last release before the 2.19 templating rewrite, run on the newest release's own set. Enterprise Linux 8 cannot serve this purpose because its Python 3.6 is below the 3.8 floor of 2.18. |
| 2.20 | `ansible220` | 3.9 | Current. Every platform except Enterprise Linux 8 and Ubuntu 20.04. |

## Platform sets

Every release has its own pair of sets, so a set lists exactly the operating
systems upstream publishes packages for. Nothing has to be inferred from a
generic name:

| set | contents | leg |
|---|---|---|
| `dnsdist-<release>` | the operating systems that release has packages for, from Enterprise Linux 9 upwards | `ansible220`, plus one `ansible218` row |
| `dnsdist-<release>-ansible216` | Enterprise Linux 8 always, and Ubuntu 20.04 where that release has focal packages | `ansible216` only |

The split exists because of the target Python, not preference: Enterprise Linux 8
has 3.6 and Ubuntu 20.04 has 3.8. Those platforms are **never** run with
`ansible218` or `ansible220`.

Availability is sparse, which is exactly why the sets are per release. Upstream
publishes Enterprise Linux 10 and Debian 13 only from the second-newest release
onwards, Ubuntu 26.04 only for the newest, and focal only for `dnsdist-19`.
AlmaLinux is not tested because it tracks Rocky; Oracle is kept because it
diverges.

## Adding a new release, for example dnsdist 2.2

Upstream names its repositories `dnsdist-22`, so `22` is the value used
everywhere below. Availability is sparse and a missing repository fails a whole
leg, so step 3 checks every operating system before the sets are written.

1. **`vars/main.yml`** - add a `dnsdist_powerdns_repo_22` block. Copy the newest
   existing one and change every occurrence of the release number. Confirm the
   signing key is still the same as the previous release; PowerDNS has used more
   than one.
2. **`defaults/main.yml`** - add the commented usage example for the new preset,
   next to the others.
3. **Two new platform sets.** Check availability first, then list exactly what
   exists:

   ```bash
   for os in 8 9 10; do curl -sI https://repo.powerdns.com/el/x86_64/$os/dnsdist-22/repodata/repomd.xml | head -1; done
   for s in bullseye bookworm trixie focal jammy noble resolute; do
     curl -sI https://repo.powerdns.com/{debian,ubuntu}/dists/$s-dnsdist-22/Release 2>/dev/null | head -1
   done
   ```

   - `molecule/platforms/dnsdist-22.yml` - Enterprise Linux 9 upwards, Debian and
     Ubuntu 22.04 upwards. Copy the newest existing set and delete what has no
     packages.
   - `molecule/platforms/dnsdist-22-ansible216.yml` - Enterprise Linux 8, plus
     Ubuntu 20.04 only if `focal-dnsdist-22` exists.

4. **`.github/workflows/main.yml`** - add one row per set:

   ```yaml
   - {scenario: default, version: "22", platforms: dnsdist-22-ansible216, toxenv: ansible216}
   - {scenario: default, version: "22", platforms: dnsdist-22, toxenv: ansible220}
   ```

   Move the single `ansible218` row to the new release as well.

5. **Move `multi-instance` to the new release** by changing `version: "21"` to
   `version: "22"` in its two matrix rows. That scenario only ever runs against
   the newest release.
6. **Retire the oldest release** in the same change: delete both of its platform sets
   and its matrix rows, and remove its `dnsdist_powerdns_repo_19` block only if the
   series is really end of life. Three releases are tested at a time.
7. **Default for local runs** - `molecule/resources/vars/dnsdist-version.yml`
   defaults `DNSDIST_VERSION` to the newest tested release. Bump it there.

No test module needs editing. `molecule/resources/tests/repo/test_repo.py` reads
the release from the environment through the `component_version` fixture in
`molecule/resources/tests/conftest.py` and derives both the repository tag
(`dnsdist-22`) and the version string the binary reports (`2.2`).

## Adding a new operating system

Because the sets are per release, an image goes into every set whose release has
packages for it - and nowhere else.

1. Check which releases have it:

   ```bash
   for v in 19 .. 21; do
     curl -sI https://repo.powerdns.com/ubuntu/dists/<suite>-dnsdist-$v/Release | head -1
   done
   ```

   For Enterprise Linux use
   `https://repo.powerdns.com/el/x86_64/<major>/dnsdist-$v/repodata/repomd.xml`.

2. Add the image to `molecule/platforms/dnsdist-<release>.yml` for each release
   that has packages. No matrix row and no test change is needed: the rows already
   reference those sets.

3. If its Python is below the floor of `ansible220` (3.9), it belongs in
   `molecule/platforms/dnsdist-<release>-ansible216.yml` instead, next to
   Enterprise Linux 8 and Ubuntu 20.04. Never put such a platform in the plain
   set - it would then run under `ansible218` and `ansible220` and fail.

4. Retire an operating system by deleting it from the sets. Keep each family to
   roughly its two newest versions, plus whatever older ones upstream still
   publishes for.

5. A new distribution *family* additionally needs a `vars/<family>.yml` in the
   role and a `molecule/resources/Dockerfile.<name>-systemd.j2` image template.

AlmaLinux is not tested because it tracks Rocky; Oracle is kept because it
diverges.
