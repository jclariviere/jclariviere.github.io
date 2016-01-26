Title: Netcat basics
Category: Infosec
Tags: netcat, vagrant
Summary: Netcat basics
Status: draft


## What is netcat?
From the manpage:
> The nc (or netcat) utility is used for just about anything under the sun involving TCP, UDP, or UNIX-domain sockets. It can open TCP connections, send UDP packets, listen on arbitrary TCP and UDP ports, do port scanning and deal with both IPv4 and IPv6.

It is referred as the TCP/IP swiss army knife, and is most commonly used to either connect to an open TCP port (client-mode), or to listen on a port (server-mode).

## Setup
To test the connection between 2 machines, I will use Vagrant to create 2 virtual machines. Vagrant is very simple to use, see [this post]({filename}/posts/2015-11-23-virtual-machines-with-vagrant.md) for the basics.

{% include_code vagrantfile-netcat/Vagrantfile lang:ruby %}

Put this `Vagrantfile` in a new folder, use `vagrant up` to create the VMs then in 2 separate command prompts, use `vagrant ssh alice` and `vagrant ssh bob` to SSH into them.

## Basic chat
To see what netcat does, we will do a very basic chat.
We'll simply connect the two machines, send hello messages from both sides then kill the connection (with `<Ctrl-C>`).

`alice` will act as the server and `bob` as the client.
Note that the "client" and "server" terms are only used for the connection setup.
Once the connection is established, both sides can send and receive data.

### Server
To listen on a port: `nc -l port`.
```
vagrant@alice:~$ nc -l 4444
```

### Client
To connect to a TCP port: `nc destination port`. Destination can be an IP address or a DNS name. In our case, `alice` is in the `hosts` file.
```
vagrant@bob:~$ nc alice 4444
```

### Output
Here is the output from both machines.
The `-v` option is for `verbose`, which shows the "connection accepted/succeeded" message.

```
:::text hl_lines="4"

vagrant@alice:~$ nc -vl 4444
Listening on [0.0.0.0] (family 0, port 4444)
Connection from [192.168.33.211] port 4444 [tcp/*] accepted (family 2, sport 41025)
Hello from alice!
Hello from bob!
```

```
:::text hl_lines="4 5"

vagrant@bob:~$ nc -v alice 4444
Connection to alice 4444 port [tcp/*] succeeded!
Hello from alice!
Hello from bob!
<Ctrl-C>
```

The highlighted lines are input sent from the prompt. As you can see, both sides can send and receive.

### Packets
Here is the full conversation as captured by tcpdump (I grouped the packets so it's easier to follow).
```
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

* First 3 packets: standard tcp 3-way handshake (SYN, SYN-ACK, ACK).
* Next 2: alice sending its hello message and bob's ack.
* Next 2: bob sending its hello message and alice's ack.
* Final 3: connection getting killed.

## Example usages
Here are some interesting usages of netcat.

### Connecting to a web server
Simply connect to the web server on port 80. You can then do a manual HTTP request.
```
:::text hl_lines="3 4"

$ nc -Cv perdu.com 80
Connection to perdu.com 80 port [tcp/http] succeeded!
GET / HTTP/1.1
Host: perdu.com

HTTP/1.1 200 OK
Date: Thu, 17 Dec 2015 04:48:05 GMT
Server: Apache
Last-Modified: Tue, 02 Mar 2010 18:52:21 GMT
ETag: "cc-480d5dd98a340"
Accept-Ranges: bytes
Content-Length: 204
Vary: Accept-Encoding
Content-Type: text/html

<html><head><title>Vous Etes Perdu ?</title></head><body><h1>Perdu sur l'Internet ?</h1><h2>Pas de panique, on va vous aider</h2><strong><pre>    * <----- vous &ecirc;tes ici</pre></strong></body></html>
```

The `-C` option is to send CRLF instead of LF, [following the HTTP standard](http://stackoverflow.com/a/5757349/3672769).

### Transferring files
You can transfer files (it works for binaries too) using shell redirections.
```
:::text hl_lines="1 4"

vagrant@alice:~$ nc -vl 4444 > received-file
Listening on [0.0.0.0] (family 0, port 4444)
Connection from [192.168.33.211] port 4444 [tcp/*] accepted (family 2, sport 41034)
vagrant@alice:~$ cat received-file
This is text written by bob
```

```
:::text hl_lines="2"

vagrant@bob:~$ echo This is text written by bob > file-to-transfer.txt
vagrant@bob:~$ nc -v alice 4444 < file-to-transfer.txt
Connection to alice 4444 port [tcp/*] succeeded!
vagrant@bob:~$ # Connection closes after the transfer
```

You can also pipe the result of a command.
```
:::text hl_lines="1 4"

vagrant@alice:~$ nc -vl 4444 > received-input
Listening on [0.0.0.0] (family 0, port 4444)
Connection from [192.168.33.211] port 4444 [tcp/*] accepted (family 2, sport 41038)
vagrant@alice:~$ cat received-input
bob
```

```
:::text hl_lines="1"

vagrant@bob:~$ hostname | nc -v alice 4444
Connection to alice 4444 port [tcp/*] succeeded!
vagrant@bob:~$ # Connection closes after the transfer
```

### Port scanning
If you don't want to interact with the port and just want to verify if it's open, you can use the `-z` option.
```text
vagrant@bob:~$ nc -vz alice 4444
Connection to alice 4444 port [tcp/*] succeeded!
```

For a range:
```text
vagrant@bob:~$ nc -vz alice 4443-4445
nc: connect to alice port 4443 (tcp) failed: Connection refused
Connection to alice 4444 port [tcp/*] succeeded!
nc: connect to alice port 4445 (tcp) failed: Connection refused
```

*For more advanced port scanning, you should use a real port scanner, such as [nmap](https://nmap.org).*

## Differences between netcat versions
There are 2 main versions of netcat: traditional and OpenBSD.
So far, we used the OpenBSD version.
Here are the package descriptions (credits to [this askubuntu question](http://askubuntu.com/a/426320)):
```text
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
They both use the `-l` option, but the traditional version requires you to set the port with the `-p` option.
So it looks like this: `nc -lp 4444` instead of `nc -l 4444`.
Using the traditional syntax with the OpenBSD version seems to work, but the manpage specifies not to use it (`-l [...] It is an error to use this option in conjunction with the -p, -s, or -z options.`), so your mileage may vary.

The OpenBSD version also doesn't contain the `-e` or `-c` options, which lets you execute a program or a shell command after connect.
This is mostly used to execute a remote shell (more on that in a future post) and was called `GAPING_SECURITY_HOLE` at some point in traditionnal netcat's [source code](http://sourceforge.net/p/netcat/code/HEAD/tree/tags/netcat-0.2.2/src/netcat.c#l271).
There is a way to simulate these options in OpenBSD's version by using named pipes, which is explained in the manpage.

## Going encrypted
Neither traditional nor OpenBSD netcat have support for SSL.
You will have to use `ncat` for that, which is an improved reimplementation of netcat by the [nmap](https://nmap.org) team.
It's bundled with nmap since [version 5](https://nmap.org/5/).

> Ncat [...] is the culmination of the currently splintered family of Netcat incarnations.
>
> -- ncat manpage

It supports all the options from both versions of netcat (including `-e`/`-c`) and adds some really interesting ones, like a list of allowed and denied IPs and, of course... SSL!
It's as simple as adding `--ssl` to both sides.
```
:::text hl_lines="9"

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

```
:::text hl_lines="6"

vagrant@bob:~$ ncat --ssl -v alice 4444
Ncat: Version 6.40 ( http://nmap.org/ncat )
Ncat: SSL connection to 192.168.33.210:4444.
Ncat: SHA-1 fingerprint: 7A3A 0A5F 35BA DCB4 A4F0 72B6 C1E0 2647 218F 29CB
Hello from alice!
Hello from bob!
```

## Conclusion
As the TCP/IP swiss army knife, netcat is a very useful tool with multiple usages.
The command execution options (`-e`/`-c`) were not covered, but it will be the subject of a future post.
Stay tuned!
