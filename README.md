samba-dc-opensuse-RPi
=====================

Build Files and Notice for Samba  AS   RPMBuild on RPi 

Work License : GPL v2


samba 4.1 AD on opensuse RPI - STEP 01


Samba 4.1 BUild 

- Opensuse Compliant style Build with subpackages.
-  Mit KRB enabled
-  gnutls, SSL enabled
-  Bind9  DLZ 
-  Ldap , ldapsam enabled
-  AD enabled
-  cups enabled
-  syslog enabled
-  acl , attr , quotas, sys-quotas, xattr  enabled
-  fam enabled
-  ssl & tls enabled
-  xfs vfs enabled
-  winbind enabled
-  clustering NOT enbabled - we plan an AD 
- NDR enabled
-  selfbuild enabaled : tdb , ntdb, tevent,  talloc, ldb 
   that include all develfiles  *.h / *.a to avoid Build Issues with Samba 4.1 and / or Missing feagers

- we use OpenSUSE selfupdated ibraries, 
  thus the folowing are exclude use of the      --bundled-libraries=!heimdal,\
  !popt,!zlib, !ldb,!pyldb,!talloc,!pytalloc,!pytalloc-util, !tdb,!pytdb,!tevent,!pytevent \




SAMBA4 BUild require a LOT of Software on the BUILD HOST to get the MOST IMPERSIVE SAMBA featgers BUILD-IN 
BUILD / Compile preparation will take a while.

see the Samba4-DC Readme files.
