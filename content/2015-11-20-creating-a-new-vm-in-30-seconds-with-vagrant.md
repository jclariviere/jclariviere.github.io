Title: Creating a new VM in 30 seconds with Vagrant
Category: DevOps
Tags: vagrant
Summary: Getting started with Vagrant
Status: draft


## What is Vagrant?
Vagrant is basically a wrapper around virtual machine providers like VirtualBox, VMware or AWS.
You simply create a config file (called `Vagrantfile`) in a folder, use `vagrant up` and you got a VM up and running in less than 30 seconds!
The only required entry in the config file is the base image to use (called "box"), but you can configure multiple properties like port forwarding, IP address, shared folders, amount of memory, script to run on first startup of the machine, etc.
This is very useful for sharing, as you only need to share a config file instead of a huge VM folder. And it can be [version controlled](https://en.wikipedia.org/wiki/Version_control)!


## Required software
For this post, I will use VirtualBox, as it's free, well supported and is the only available provider out of the box (you need to install plugins for the others).
Make sure you have [VirtualBox](https://www.virtualbox.org/) and [Vagrant](https://docs.vagrantup.com/v2/installation) installed before continuing.


## Getting started
Here is the most basic Vagrantfile you can do:
```ruby
# -*- mode: ruby -*-
# vi: set ft=ruby :

VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "ubuntu/trusty64"
end
```

As you can see, this is plain ruby, so you can use variables, loops, conditions, etc.

Put this file in a new folder and use `vagrant up` to create the virtual machine.

If this is the first time you use this box, you will notice that [I lied](https://www.youtube.com/watch?v=Q2h9L4EVIdI&t=30s), it didn't take 30 seconds!
The box first needs to be downloaded, but it will be 30 seconds for future machines, promise!

You should see the VM in the VirtualBox GUI, but **do not edit the configuration there** since Vagrant will probably override your settings. Edit the `Vagrantfile` instead.

When the VM is ready, use `vagrant ssh` to SSH in it.
Most boxes in Vagrant run in [headless mode](https://en.wikipedia.org/wiki/Headless_software), but if you need a desktop environment, [boxcutter's Ubuntu desktop box](https://atlas.hashicorp.com/boxcutter/boxes/ubuntu1404-desktop) seems to work well.

To shutdown the VM, use `vagrant halt`. To destroy it, use `vagrant destroy`. To reboot it, use `vagrant reload`.


## Configuration
You can also use `vagrant init` to create a `Vagrantfile` with a bunch of options commented out. Let's review the most interesting ones.

### Box
```ruby
# Every Vagrant development environment requires a box. You can search for
# boxes at https://atlas.hashicorp.com/search.
config.vm.box = "base"
```
In the previous section, I used the official Ubuntu 14.04 box, but you can find more at [https://atlas.hashicorp.com/search](https://atlas.hashicorp.com/search).
The value should be the name of the box (`ubuntu/trusty64` for example).

You can also use `config.vm.box_url` if the box is not in Hashicorp's Atlas. In this case you need a full URL.

### Port forwarding
```ruby
# Create a forwarded port mapping which allows access to a specific port
# within the machine from a port on the host machine. In the example below,
# accessing "localhost:8080" will access port 80 on the guest machine.
config.vm.network "forwarded_port", guest: 80, host: 8080
```

Port forwarding can be useful if you need to access a service in the VM from a machine on the network but don't want to expose the whole VM.

### Private network
```ruby
# Create a private network, which allows host-only access to the machine
# using a specific IP.
config.vm.network "private_network", ip: "192.168.56.10"
```

This will create a "host-only network", which allows other VMs and the host to communicate together.
If the interface doesn't exist on the host, it will create it.

### Public network
```ruby
# Create a public network, which generally matched to bridged network.
# Bridged networks make the machine appear as another physical device on
# your network.
config.vm.network "public_network"
```

The word `public` here is confusing. This will add an interface on the same network than the host.
Let's say your host has IP `192.168.0.100`, your VM could get `192.168.0.167` for example.
This means you will be able to ping the VM from another computer in the same network.
**Since Vagrant is [insecure by default](https://docs.vagrantup.com/v2/networking/public_network.html), this is probably a bad idea.**

### Shared folders
```ruby
# Share an additional folder to the guest VM. The first argument is
# the path on the host to the actual folder. The second argument is
# the path on the guest to mount the folder. And the optional third
# argument is a set of non-required options.
config.vm.synced_folder "../data", "/vagrant_data"
```

Share a folder with the host. By default, Vagrant shares the folder containing the `Vagrantfile` to the `/vagrant` folder in the VM.

### Provider-specific configuration
```ruby
# Provider-specific configuration so you can fine-tune various
# backing providers for Vagrant. These expose provider-specific options.
# Example for VirtualBox:
#
config.vm.provider "virtualbox" do |vb|
  # Display the VirtualBox GUI when booting the machine
  vb.gui = true

  # Customize the amount of memory on the VM:
  vb.memory = "1024"
end
#
# View the documentation for the provider you are using for more
# information on available options.
```

Note that customizing the amount of memory is done on a per-provider basis.

### Provisionning
```ruby
# Enable provisioning with a shell script. Additional provisioners such as
# Puppet, Chef, Ansible, Salt, and Docker are also available. Please see the
# documentation for more information about their specific syntax and use.
config.vm.provision "shell", inline: <<-SHELL
  sudo apt-get update
  sudo apt-get install -y apache2
SHELL
```

Provisionning is used to setup the VM once it is booted.
Of course, you can simply SSH in the machine and install what you want in it, but adding it in the `Vagrantfile` will automate the process if you need multiple VMs or want to share it.

You can add your script inline (like the example), but you can also use a script file or configuration managements systems like Chef, Puppet, Ansible or Salt.
If you use scripts, make sure they are non-interactive! (Add the `-y` flag to `apt-get install` for example).

Provisionning happens is these situations:

* On the **first** `vagrant up`
* On a running VM, `vagrant provision`
* `vagrant up --provision`
* `vagrant reload --provision`


## Defining multiple machines in a Vagrantfile
To do so, use `config.vm.define` in the `Vagrantfile`.

```ruby
# -*- mode: ruby -*-
# vi: set ft=ruby :

VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "ubuntu/trusty64"

  config.vm.define "alice" do |alice|
    alice.vm.network :private_network, ip: "192.168.56.210"
  end

  config.vm.define "bob" do |bob|
    bob.vm.network :private_network, ip: "192.168.56.211"
  end
end
```

Here, the sub-configs inherits from `config`, so alice and bob will both have the box `ubuntu/trusty64`.
You can define it per-machine, just make sure you use the per-machine variables (`bob` and `alice`).

The vagrant command lines differs when there is multiple machines defined.
Commands that only makes sense for a single machine, such as `vagrant ssh`, requires you to include the name of the machine as an argument: `vagrant ssh bob`.
Other commands, such as `vagrant up`, will operate on every machine by default, but you can also specify the target: `vagrant up alice`.


## More info
This post should cover common usage of Vagrant, but you can do more with it, such as pushing code to Heroku or sharing your VM over SSH.
The [official documentation](https://docs.vagrantup.com) is very well structured, so make sure you have a look!
