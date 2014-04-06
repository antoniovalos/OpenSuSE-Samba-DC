 OpenSuSE-Samba-DC

=====================


Build Notices for Samba-DC    
RPMBuild on RPi 
Work License : GPL v2, see file "LICENSE"<br>
<br>

Samba-DC 4.x BUild 

- Opensuse Compliant style Build with subpackages.<br>
-  Heimdall embeded enabled due requirement for ADS DC Build <br>
-  gnutls, SSL  enabled<br>
-  Bind9  DLZ enabled<br>
-  Ldap, ldapsam enabled<br>
-  AD enabled<br>
-  cups enabled
-  syslog enabled
-  acl , attr , quotas, sys-quotas, xattr  enabled
-  fam enabled
-  xfs, ext2/3/4 vfs enabled
-  winbind enabled
-  clustering NOT  enabled - we plan an AD 
-  NDR enabled
-  selfbuild enabled : tdb ,  tevent,  talloc, ldb , libbsd, python-hashlib
   that include all develfiles  *.h / *.a to avoid Build Issues with Samba 4.1 and / or Missing feagers<br>

- allmost selfupdated Packages based on OpenSuSE.org ´s (S)RMS <br>
  thus the folowing are exclude use of the      --bundled-libraries=!popt,!zlib, <br> !ldb,!pyldb,!talloc,!pytalloc,!pytalloc-util,tdb,!pytdb,!tevent,!pytevent,ALL \ <br>


 SAMBA4-DC  BUild require a LOT of Software on the BUILD HOST to get the MOST IMPressive SAMBA featgers BUILD-IN  <br>
 BUILD / Compile preparation will take a while. <br>

   SAMBA4-DC  BUild as ADS works only with Bundeld heimdal - see BUGS File. <br>


To Prerepare yourself : <br>

 1- Install any system depend software include Compiler, devel libs - see the Samba4-DC*  Readme files.
 2- Build & Install tdb , ldb ,. ntdb , tevent , talloc, libbsd, python-hashlib
 3- build samba-dc  - see latest samba-dc-4.1.3_??.spec
 4- install samba-dc rpms
 5- setup samba-dc with dcpromo
 
 
 
 RPM Build changelog 05-03-2014 <br>
 samba 4.2-betta ( 4.1.6-23 rpmbuild from GIT )    : Completed <br>
 
 depend Samba4  AD Software <br>
 bind9  with dlz                                   : Completed <br>
 talloc 2.1                                        : completed <br>
 tdb 1.2.12                                        : Completed <br>
 tevent 0.9.20                                     : completed <br>
 ldb 1.1.6                                         : completed <br>
 ntdb 1.0                                          : samba4.2 build-in <br>
 libbds 0.6                                        : completed <br>
 cifs-utils                                        : completed <br>
 python-hashlib                                   : completed <br>
 heimdall 1.3.2                                    : completed <br>
 krb51.11.4                                        : completed <br>
 
 RPMS , SRPM Files   of this Samba4-DC Build  are stored on Our Drop box url :  <br>
 
Current of this Samba4-DC Build  are stored on Our Drop box url : https://www.dropbox.com/sh/p4ijdacy90xebqk/4moyZY9Ne8
Currently RPMS are created for : 
 -  OSS 13.1 arm 
 
 
 <pre>
 samba4-4.1.6-DC_master_r22.src.rpm
 samba4-4.1.6-DC_master_r22.armv6hl.rpm
 samba4-client-4.1.6-DC_master_r22.armv6hl.rpm
 samba4-man-4.1.6-DC_master_r22.armv6hl.rpm
 samba4-common-4.1.6-DC_master_r22.armv6hl.rpm
 samba4-dc-4.1.6-DC_master_r22.armv6hl.rpm
 samba4-dc-libs-4.1.6-DC_master_r22.armv6hl.rpm
 samba4-dc-doc-4.1.6-DC_master_r22.armv6hl.rpm
 samba4-dc-config-4.1.6-DC_master_r22.armv6hl.rpm
 samba4-devel-4.1.6-DC_master_r22.armv6hl.rpm
 samba4-libs-4.1.6-DC_master_r22.armv6hl.rpm
 libsmbclient0-4.1.6-DC_master_r22.armv6hl.rpm
 libsmbclient-devel-4.1.6-DC_master_r22.armv6hl.rpm
 libsmbclient-raw0-4.1.6-DC_master_r22.armv6hl.rpm
 libsmbclient-raw-devel-4.1.6-DC_master_r22.armv6hl.rpm
 libwbclient0-4.1.6-DC_master_r22.armv6hl.rpm
 libwbclient-devel-4.1.6-DC_master_r22.armv6hl.rpm
 libsmbsharemodes0-4.1.6-DC_master_r22.armv6hl.rpm
 libsmbsharemodes-devel-4.1.6-DC_master_r22.armv6hl.rpm
 samba4-python-4.1.6-DC_master_r22.armv6hl.rpm
 samba4-pidl-4.1.6-DC_master_r22.armv6hl.rpm
 samba4-test-4.1.6-DC_master_r22.armv6hl.rpm
 samba4-test-devel-4.1.6-DC_master_r22.armv6hl.rpm
 winbind-4.1.6-DC_master_r22.armv6hl.rpm
 winbind-clients-4.1.6-DC_master_r22.armv6hl.rpm
 winbind-krb5-locator-4.1.6-DC_master_r22.armv6hl.rpm
 winbind-modules-4.1.6-DC_master_r22.armv6hl.rpm
</pre>
 
 



 
 For Build issues raise an issue - please.
 
