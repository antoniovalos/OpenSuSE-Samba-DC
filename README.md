samba-dc-opensuse-RPi
=====================


Build Notices for Samba-DC    
RPMBuild on RPi 
Work License : GPL v2, see file "LICENSE"


Samba-DC 4.x BUild 

- Opensuse Compliant style Build with subpackages.
-  Heimdall  KRB enabled
-  gnutls, SSL  enabled
-  Bind9  DLZ enabled
-  Ldap, ldapsam enabled
-  AD enabled
-  cups enabled
-  syslog enabled
-  acl , attr , quotas, sys-quotas, xattr  enabled
-  fam enabled
-  xfs, ext2/3/4 vfs enabled
-  winbind enabled
-  clustering NOT  enabled - we plan an AD 
-  NDR enabled
-  selfbuild enabled : tdb ,  tevent,  talloc, ldb , libbsd, python-hashlib
   that include all develfiles  *.h / *.a to avoid Build Issues with Samba 4.1 and / or Missing feagers

- allmost selfupdated Packages based on OpenSuSE.org ´s (S)RMS 
  thus the folowing are exclude use of the      --bundled-libraries=!popt,!zlib, !ldb,!pyldb,!talloc,!pytalloc,!pytalloc-util,tdb,!pytdb,!tevent,!pytevent,ALL \


 SAMBA4-DC  BUild require a LOT of Software on the BUILD HOST to get the MOST IMPressive SAMBA featgers BUILD-IN 
 BUILD / Compile preparation will take a while.

   SAMBA4-DC  BUild as ADS works only with Bundeld heimdal - see BUGS File.


To Prerepare yourself :

 1- Install any system depend software include Compiler, devel libs - see the Samba4-DC*  Readme files.

 2- Build & Install tdb , ldb ,. ntdb , tevent , talloc, libbsd, python-hashlib

 3- build samba-dc  - see latest samba-dc-4.1.3_??.spec
 
 4- install samba-dc rpms
 
 5- setup samba-dc with dcpromo
