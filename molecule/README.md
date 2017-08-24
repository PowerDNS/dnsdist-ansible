# Testing with Molecule

This role uses [molecule](https://molecule.readthedocs.io/en/latest/) 
to implement automated testing of its functionalities. 

## Requirements

* Ansible >= 2.2 
* molecule v2
* Docker

## Create a Docker virtual machine (optional on most Linux distros) 

On some systems, e.g. OS X, is not possible to run successfully the docker-based molecule test-suite
because of the lack of systemd support (the services in the docker containers will fail to start).

To overcome this issue, make sure to have

* Vagrant
* Virtualbox
* docker-machine

installed on your system and follow these instructions to create a docker virtual machine
to use for your tests

```bash
# Create the virtual machine
vagrant up

# Install docker inside the virtual machine
docker-machine create -d generic \
--generic-ssh-user vagrant \
--generic-ssh-key .vagrant/machines/molecule-dnsdist/virtualbox/private_key \
--generic-ip-address "$(vagrant ssh -- hostname -I | cut -d ' ' -f 2)" \
--engine-install-url "https://get.docker.com" \
molecule-dnsdist

# Connect your local docker client to the docker deamon running in the virtual machine
eval $(docker-machine env molecule-dnsdist)
```

To clean-up the environment just execute

```bash
# Destroy the virtual machine
vagrant rm

# Remove the docker virtual machine from the docker-machines list
docker-machine rm molecule-dnsdist
```

# Execute the tests

```bash
# if using the docker virtual machine
eval $(docker-machine env molecule-dnsdist)

# test all the scenarios
molecule test --all

# execute only a specific scenario
# e.g.
molecule test --scenario-name dnsdist-1.2.x
```
