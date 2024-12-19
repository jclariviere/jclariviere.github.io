Title: Virtual machines with Vagrant
Category: DevOps
Tags: vagrant
Modified: 2024-12-19


**2024 update: Updated links and use `kalilinux/rolling` instead of the outdated `ubuntu/trusty64`. The rest is still relevant today.**

---

One of the biggest pain points of using a VM is bootstrapping it.
Even if you have a pre-packaged VM, you still have to use the UI to import it and customize its settings, and then you have to log in to install the packages you need.
It's possible to use the command line, but the commands are specific to each provider and they're not very user friendly.

Vagrant solves this problem. It is basically a wrapper around virtual machine providers like VirtualBox, VMware or AWS.
You simply need to create a config file (called `Vagrantfile`) in a folder, use `vagrant up` and you've got a VM up and running in less than 30 seconds!
The only required entry in the config file is the base image to use, but you can configure multiple properties like port forwarding, IP address, shared folders, amount of memory, script to run on first startup of the machine, etc.
This is very useful for sharing, as you only need to share a config file instead of a huge VM folder, which can then be version controlled with `git`.

## Getting started

### Required software

For this post, I will use the VirtualBox provider, as it's free and available out of the box.
If you wish to use VMware, you will need to [install a plugin](https://developer.hashicorp.com/vagrant/docs/providers/vmware/installation).

Make sure you have [VirtualBox](https://www.virtualbox.org/) and [Vagrant](https://developer.hashicorp.com/vagrant/docs/installation) installed before continuing.
Vagrant also uses ruby, but you don't need to install it since it's embedded in Vagrant.

### Basics

Here is the most basic `Vagrantfile` you can do.

``` { .ruby filename="Vagrantfile" }
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "kalilinux/rolling"
end
```

As you might have noticed, this is plain ruby, so you could use variables, loops, conditions, etc.
Don't panic if you don't know ruby, the `Vagrantfile` is simple enough that it can be read like a regular config file.

The base image (called "box") I used is Kali Linux [rolling](https://www.kali.org/docs/general-use/kali-branches/).

Put this file in a new folder and use `vagrant up` to create the virtual machine.
Remember when I told you it'd take 30 seconds?

![I lied!]({static}/images/i-lied.png)

The box needs to be downloaded locally when it's first used.
But! The next machine created from it will be set up much faster.

You should see the VM in the VirtualBox GUI, but **do not edit the configuration there** since Vagrant will probably override your settings. Edit the `Vagrantfile` instead.

When the VM is ready, use `vagrant ssh` to SSH into it.
Most boxes in Vagrant run in "headless mode" (no GUI), but some, like Kali Linux, do start a desktop environment that you can use in a different window.

You can use these commands to manage the VM:

- `vagrant halt` to shut it down
- `vagrant reload` to reboot it
- `vagrant destroy` to destroy it

## Configuration

You can use `vagrant init` to create a `Vagrantfile` with a bunch of options commented out. Let's review the most interesting ones.

### Box

```ruby
# Every Vagrant development environment requires a box. You can search for
# boxes at https://vagrantcloud.com/search.
config.vm.box = "base"
```

In the previous section, I used the `kalilinux/rolling` box, but you can find more at [https://vagrantcloud.com/search](https://vagrantcloud.com/search).

You can also use `config.vm.box_url` if the box is not in Hashicorp's Cloud.

### Port forwarding

```ruby
# Create a forwarded port mapping which allows access to a specific port
# within the machine from a port on the host machine. In the example below,
# accessing "localhost:8080" will access port 80 on the guest machine.
# NOTE: This will enable public access to the opened port
config.vm.network "forwarded_port", guest: 80, host: 8080
```

Port forwarding can be useful if you need to access a service in the VM from a machine on the network but don't want to expose the whole VM.

### Private network

```ruby
# Create a private network, which allows host-only access to the machine
# using a specific IP.
config.vm.network "private_network", ip: "192.168.33.10"
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

The word `public` here is confusing. This will add an interface on the same network as the host.
Let's say your host has IP `192.168.0.100`, your VM could get `192.168.0.167`, for example.
This means you will be able to ping the VM from another computer in the same network.
**Since Vagrant is [insecure by default](https://developer.hashicorp.com/vagrant/docs/networking/public_network), this is probably a bad idea.**

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
# Ansible, Chef, Docker, Puppet and Salt are also available. Please see the
# documentation for more information about their specific syntax and use.
config.vm.provision "shell", inline: <<-SHELL
  apt-get update
  apt-get install -y apache2
SHELL
```

Provisionning is used to setup the VM once it is booted.
Of course, you can simply SSH into the machine and install what you want in it, but adding it in the `Vagrantfile` will automate the process if you need multiple VMs or want to share it.

You can add your script inline (like the example), but you can also use a script file or configuration managements systems like Ansible, Chef, Puppet or Salt.
If you use scripts, make sure they are non-interactive (add the `-y` flag to `apt-get install` for example).

Provisionning happens in these situations:

- On the **first** `vagrant up`
- On a running VM, `vagrant provision`
- `vagrant up --provision`
- `vagrant reload --provision`

## Defining multiple machines in a Vagrantfile

To do so, use `config.vm.define` in the `Vagrantfile`.

``` { .ruby filename="Vagrantfile" }
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "kalilinux/rolling"

  config.vm.define "alice" do |alice|
    alice.vm.hostname = "alice"
    alice.vm.network :private_network, ip: "192.168.33.210"
    alice.vm.provision "shell", inline: "echo 192.168.33.211 bob >> /etc/hosts"
  end

  config.vm.define "bob" do |bob|
    bob.vm.hostname = "bob"
    bob.vm.network :private_network, ip: "192.168.33.211"
    bob.vm.provision "shell", inline: "echo 192.168.33.210 alice >> /etc/hosts"
  end
end
```

Here, we defined 2 VMs, `alice` and `bob`, that both have a sub-config block configuring their hostname and a private network IP, as well as adding the other machine in their `/etc/hosts` file.
They also inherit from the top level config, so they will both use the box `kalilinux/rolling`.
To define it per-machine, simply use their per-machine variable: `alice.vm.box = "box/name"`.

The Vagrant command line differs when there is multiple machines defined.
Commands that only make sense for a single machine, such as `vagrant ssh`, require you to include the name of the machine as an argument: `vagrant ssh bob`.
Other commands, such as `vagrant up`, will operate on every machine by default, but you can also specify the target: `vagrant up alice`.

## More info

This post covered common usage of Vagrant, but you can do more with it, such as pushing code to Heroku or sharing your VM over SSH.
The [official documentation](https://developer.hashicorp.com/vagrant/docs) is very well structured, so make sure you have a look!
