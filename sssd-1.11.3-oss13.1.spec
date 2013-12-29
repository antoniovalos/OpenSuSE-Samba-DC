#
# spec file for samba-dc package sssd
#
# Copyright (c) 2013 SUSE LINUX Products GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via https://github.com/remsnet/samba-dc-opensuse-RPi

#

%{!?python_sitearch:  %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}



Name:           sssd
Version:        1.11.3
Release:        115.1
Summary:        System Security Services Daemon
License:        GPL-3.0+ and LGPL-3.0+
Group:          System/Daemons
Url:            https://fedorahosted.org/sssd/

#Git-Clone:     git://git.fedorahosted.org/sssd
Source:         https://fedorahosted.org/released/sssd/sssd-%version.tar.gz
Source2:        https://fedorahosted.org/released/sssd/sssd-%version.tar.gz.asc
Source3:        baselibs.conf
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%define servicename     sssd
%define sssdstatedir    %_localstatedir/lib/sss
%define dbpath          %sssdstatedir/db
%define pipepath        %sssdstatedir/pipes
%define pubconfpath     %sssdstatedir/pubconf
%define initscript      systemd


%if 0%{?suse_version} == 0 || 0%{?suse_version} > 1140
%define build_make_smp_mflags %{?_smp_mflags}
%else
%define build_make_smp_mflags %{?jobs:-j%jobs}
%endif


%if %suse_version <= 1110
# SLES11 doesn't know the python_* macros
%define python_sitelib  %py_sitedir
%define python_sitearch %py_sitedir
%endif

BuildRequires:  autoconf >= 2.59
BuildRequires:  automake
BuildRequires:  bind-utils
BuildRequires:  cyrus-sasl-devel
BuildRequires:  docbook-xsl-stylesheets
BuildRequires:  krb5-devel
BuildRequires:  libtool
BuildRequires:  pkgconfig >= 0.21
BuildRequires:  systemd-devel
%if 0%{?suse_version} >= 1210
BuildRequires:  pkgconfig(collection) >= 0.5.1
BuildRequires:  pkgconfig(dbus-1) >= 1.0.0
BuildRequires:  pkgconfig(dhash) >= 0.4.2
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(ini_config) >= 0.6.1
BuildRequires:  pkgconfig(ldb) >= 0.9.2
BuildRequires:  pkgconfig(libcares)
BuildRequires:  pkgconfig(libnl-1) >= 1.1
BuildRequires:  pkgconfig(libpcre) >= 7
BuildRequires:  pkgconfig(ndr_nbt)
BuildRequires:  pkgconfig(openssl)
BuildRequires:  pkgconfig(popt)
BuildRequires:  pkgconfig(python)
BuildRequires:  pkgconfig(talloc)
BuildRequires:  pkgconfig(tdb) >= 1.1.3
BuildRequires:  pkgconfig(tevent)
%else
BuildRequires:  dbus-1-devel >= 1.0.0
BuildRequires:  glib2-devel
BuildRequires:  libcares-devel
BuildRequires:  libcollection-devel >= 0.5.1
BuildRequires:  libdhash-devel >= 0.4.2
BuildRequires:  libini_config-devel >= 0.6.1
BuildRequires:  libldb-devel >= 0.9.2
BuildRequires:  libnl-devel >= 1.1
BuildRequires:  libopenssl-devel
BuildRequires:  libtalloc-devel
BuildRequires:  libtdb-devel >= 1.1.3
BuildRequires:  libtevent-devel
BuildRequires:  pcre-devel >= 7
BuildRequires:  popt-devel
BuildRequires:  python-devel
BuildRequires:  samba-devel >= 4
%endif
BuildRequires:  samba-libs >= 4
%if 0%{?suse_version} >= 1220
BuildRequires:  libxml2-tools
BuildRequires:  libxslt-tools
%else
BuildRequires:  libxml2
BuildRequires:  libxslt
%endif
BuildRequires:  nscd
BuildRequires:  openldap2-devel
BuildRequires:  pam-devel
BuildRequires:  pkg-config
%if %suse_version >= 1210
BuildRequires:  systemd
%{?systemd_requires}
%endif
%if %suse_version >= 1230
BuildRequires:  gpg-offline
%endif
Requires:       sssd-ldap = %version-%release
Requires(postun): pam-config

%description
Provides a set of daemons to manage access to remote directories and
authentication mechanisms. It provides an NSS and PAM interface toward
the system and a pluggable backend system to connect to multiple different
account sources. It is also the basis to provide client auditing and policy
services for projects like FreeIPA.

%package ad
Summary:        The ActiveDirectory backend plugin for sssd
License:        GPL-3.0+
Group:          System/Daemons
Requires:       %name-krb5-common = %version

%description ad
Provides the Active Directory back end that the SSSD can utilize to
fetch identity data from and authenticate against an Active Directory
server.

%package ipa
Summary:        FreeIPA backend plugin for sssd
License:        GPL-3.0+
Group:          System/Daemons
Requires:       %name = %version
Requires:       %name-krb5-common = %version-%release
Obsoletes:      %name-ipa-provider < %version-%release
Provides:       %name-ipa-provider = %version-%release

%description ipa
Provides the IPA back end that the SSSD can utilize to fetch identity
data from and authenticate against an IPA server.

%package krb5
Summary:        The Kerberos authentication backend plugin for sssd
License:        GPL-3.0+
Group:          System/Daemons
Requires:       %name-krb5-common = %version-%release

%description krb5
Provides the Kerberos back end that the SSSD can utilize authenticate
against a Kerberos server.

%package krb5-common
Summary:        SSSD helpers needed for Kerberos and GSSAPI authentication
License:        GPL-3.0+
Group:          System/Daemons

%description krb5-common
Provides helper processes that the LDAP and Kerberos back ends can
use for Kerberos user or host authentication.

%package ldap
Summary:        The LDAP backend plugin for sssd
License:        GPL-3.0+
Group:          System/Daemons
Requires:       %name-krb5-common = %version-%release

%description ldap
Provides the LDAP back end that the SSSD can utilize to fetch
identity data from and authenticate against an LDAP server.

%package proxy
Summary:        The proxy backend plugin for sssd
License:        GPL-3.0+
Group:          System/Daemons

%description proxy
Provides the proxy back end which can be used to wrap an existing NSS
and/or PAM modules to leverage SSSD caching.

%package tools
Summary:        Commandline tools for sssd
License:        GPL-3.0+ and LGPL-3.0+
Group:          System/Management
Requires:       sssd = %version

%description tools
The packages contains commandline tools for managing users and groups using
the "local" id provider of the System Security Services Daemon (sssd).

%package -n libipa_hbac0
Summary:        FreeIPA HBAC Evaluator library
License:        LGPL-3.0+
Group:          System/Libraries

%description -n libipa_hbac0
Utility library to validate FreeIPA HBAC rules for authorization
requests.

%package -n libipa_hbac-devel
Summary:        Development files for the FreeIPA HBAC Evaluator library
License:        LGPL-3.0+
Group:          Development/Libraries/C and C++
Requires:       libipa_hbac0 = %version

%description -n libipa_hbac-devel
Utility library to validate FreeIPA HBAC rules for authorization
requests.

%package -n libsss_idmap0
Summary:        FreeIPA ID mapping library
License:        LGPL-3.0+
Group:          System/Libraries

%description -n libsss_idmap0
A utility library for FreeIPA to map Windows SIDs to Unix user/group IDs.

%package -n libsss_idmap-devel
Summary:        Development files for the FreeIPA idmap library
License:        LGPL-3.0+
Group:          Development/Libraries/C and C++
Requires:       libsss_idmap0 = %version

%description -n libsss_idmap-devel
A utility library for FreeIPA to map Windows SIDs to Unix user/group IDs.

%package -n libsss_nss_idmap0
Summary:        FreeIPA ID mapping library
License:        LGPL-3.0+
Group:          System/Libraries

%description -n libsss_nss_idmap0
A utility library for FreeIPA to map Windows SIDs to Unix user/group IDs.

%package -n libsss_nss_idmap-devel
Summary:        Development files for the FreeIPA idmap library
License:        LGPL-3.0+
Group:          Development/Libraries/C and C++
Requires:       libsss_nss_idmap0 = %version

%description -n libsss_nss_idmap-devel
A utility library for FreeIPA to map Windows SIDs to Unix user/group IDs.

%package -n libsss_sudo
Summary:        A library to allow communication between sudo and SSSD
License:        LGPL-3.0+
Group:          System/Libraries
Provides:       libsss_sudo-devel = %version-%release
Obsoletes:      libsss_sudo-devel < %version-%release
# No provides: true obsolete.
Obsoletes:      libsss_sudo1

%description -n libsss_sudo
A utility library to allow communication between sudo and SSSD.

%package -n python-ipa_hbac
Summary:        Python bindings for the FreeIPA HBAC Evaluator library
License:        LGPL-3.0+
Group:          Development/Libraries/Python
%py_requires

%description -n python-ipa_hbac
The python-ipa_hbac package contains the bindings so that libipa_hbac
can be used by Python applications.

%package -n python-sss_nss_idmap
Summary:        Python bindings for libsss_nss_idmap
License:        LGPL-3.0+
Group:          Development/Libraries/Python
%py_requires

%description -n python-sss_nss_idmap
The libsss_nss_idmap-python contains the bindings so that
libsss_nss_idmap can be used by Python applications.

%package -n python-sssd-config
Summary:        Python API for configuring sssd
License:        GPL-3.0+ and LGPL-3.0+
Group:          Development/Libraries/Python
%py_requires

%description -n python-sssd-config
Provide python module to access and manage configuration of the System
Security Services Daemon (sssd).

%prep

%if 0%{?suse_version} < 1230

# let configure know that we have an systemd.pc - just Opensuse renamed that .. damn.
if [ -f /usr/lib/pkgconfig/libsystemd-daemon.pc ] && [  ; then
        ln -s /usr/lib/pkgconfig/libsystemd-daemon.pc /usr/lib/pkgconfig/systemd.pc
fi
else
        echo "Samba4 DC  package require at least Opensuse 12.3 with systemd - exiting Pkg Build"
        exit 1
%endif

%setup -q

%build
%if 0%{?suse_version} < 1210
# pkgconfig file not present
export LDB_LIBS="-lldb"
export LDB_CFLAGS=" "
export LDB_DIR="%_libdir/ldb"
%else
export LDB_DIR="$(pkg-config ldb --variable=modulesdir)"
%endif

# help configure find nscd
export PATH="$PATH:/usr/sbin"


%if 0%{?suse_version} && 0%{?suse_version} < 911
        OPTIMIZATION="-O"
%else
        # use the default optimization
        unset OPTIMIZATION
%endif

autoreconf -fi;
export CFLAGS="${RPM_OPT_FLAGS} -D_GNU_SOURCE ${OPTIMIZATION} -D_LARGEFILE64_SOURCE -DIDMAP_RID_SUPPORT_TRUSTED_DOMAINS"
CONFIGURE_OPTIONS="\
-with-crypto=libcrypto \
    --with-db-path="%dbpath" \
    --with-pipe-path="%pipepath" \
    --with-pubconf-path="%pubconfpath" \
    --with-init-dir="%_initrddir" \
    --enable-nsslibdir="/%_lib" \
    --enable-pammoddir="/%_lib/security" \
    --with-libnl \
    --enable-pac-responder \
    --enable-all-experimental-features \
    --with-ldb-lib-dir="$LDB_DIR" \
    --with-selinux=no \
    --with-os=suse \
    --with-semanage=no \
    --with-initscript="%initscript" \
"

%configure ${CONFIGURE_OPTIONS}

%{__make} %{build_make_smp_mflags} \
        all

%install
b="%buildroot";
make install DESTDIR="$b"

# Copy default sssd.conf file
install -d "$b/%_mandir"/{cs,cs/man8,nl,nl/man8,pt,pt/man8,uk,uk/man1} \
           "$b/%_mandir"/{uk/man5,uk/man8};
install -d "$b/%_sysconfdir/sssd";
install -m600 src/examples/sssd-example.conf "$b/%_sysconfdir/sssd/sssd.conf";
%if 0%{?_unitdir:1}
install -d "$b/%_unitdir";
install src/sysv/systemd/sssd.service "$b/%_unitdir/sssd.service";
rm -Rf "$b/%_initddir"
%else
install src/sysv/SUSE/sssd "$b/%_sysconfdir/init.d/sssd";
ln -sf ../../etc/init.d/sssd "$b/usr/sbin/rcsssd"
%endif

find "$b" -type f -name "*.la" -delete;

%if %suse_version <= 1110
# remove some unsupported languages, sssd does not contain
# translations for these anyway
rm -Rf "$b/usr/share/locale"/{fa_IR,ja_JP,lt_LT,ta_IN,vi_VN}
%endif

%find_lang %name --all-name

%if 0%{?_unitdir:1}
%pre
%service_add_pre sssd.service
%endif

%post
# migrate config variable krb5_kdcip to krb5_server (bnc#851048)
/bin/sed -i -e 's,^krb5_kdcip =,krb5_server =,g' %_sysconfdir/sssd/sssd.conf

/sbin/ldconfig
%if 0%{?_unitdir:1}
%service_add_post sssd.service
%endif

%if 0%{?_unitdir:1}
%preun
%service_del_preun sssd.service
%endif

%postun
/sbin/ldconfig
%if 0%{?_unitdir:1}
%service_del_postun sssd.service
%endif
if [ "$1" == "0" ]; then
        "%_sbindir/pam-config" -d --sss || :;
fi;

%post   -n libipa_hbac0 -p /sbin/ldconfig
%postun -n libipa_hbac0 -p /sbin/ldconfig
%post   -n libsss_idmap0 -p /sbin/ldconfig
%postun -n libsss_idmap0 -p /sbin/ldconfig
%post   -n libsss_nss_idmap0 -p /sbin/ldconfig
%postun -n libsss_nss_idmap0 -p /sbin/ldconfig

%files -f sssd.lang
%defattr(-,root,root)
%doc COPYING
%if 0%{?_unitdir:1}
%_unitdir
%else
%_initrddir/%name
%_sbindir/rcsssd
%endif
%_bindir/sss_ssh_*
%_sbindir/sssd
%dir %_mandir/??/
%dir %_mandir/??/man?/
%_mandir/??/man1/sss_ssh_*
%_mandir/??/man5/sssd-simple.5*
%_mandir/??/man5/sssd-sudo.5*
%_mandir/??/man5/sssd.conf.5*
%_mandir/??/man8/sssd.8*
%_mandir/man1/sss_ssh_*
%_mandir/man5/sssd-simple.5*
%_mandir/man5/sssd-sudo.5*
%_mandir/man5/sssd.conf.5*
%_mandir/man8/sssd.8*
%dir %_libdir/%name/
%_libdir/%name/libsss_child*
%_libdir/%name/libsss_crypt*
%_libdir/%name/libsss_debug*
%_libdir/%name/libsss_simple*
%_libdir/%name/libsss_util*
%_libdir/%name/modules/
%dir %_libdir/ldb/
%_libdir/ldb/memberof.so
%dir %_libexecdir/%name/
%_libexecdir/%name/sssd_*
%dir %sssdstatedir
%attr(700,root,root) %dir %dbpath/
%attr(755,root,root) %dir %pipepath/
%attr(700,root,root) %dir %pipepath/private/
%attr(755,root,root) %dir %pubconfpath/
%attr(750,root,root) %dir %_localstatedir/log/%name/
%dir %_sysconfdir/sssd/
%config(noreplace) %_sysconfdir/sssd/sssd.conf
%dir %_datadir/%name/
%_datadir/%name/sssd.api.conf
%dir %_datadir/%name/sssd.api.d/
%_datadir/%name/sssd.api.d/sssd-local.conf
%_datadir/%name/sssd.api.d/sssd-simple.conf
#
# sssd-client
#
/%_lib/libnss_sss.so.2
/%_lib/security/pam_sss.so
%_libdir/krb5/plugins/libkrb5/*
%_mandir/??/man8/pam_sss.8*
%_mandir/??/man8/sssd_krb5_locator_plugin.8*
%_mandir/man8/pam_sss.8*
%_mandir/man8/sssd_krb5_locator_plugin.8*

%files ad
%defattr(-,root,root)
%dir %_libdir/%name/
%_libdir/%name/libsss_ad.so
%dir %_datadir/%name/
%dir %_datadir/%name/sssd.api.d/
%_datadir/%name/sssd.api.d/sssd-ad.conf
%dir %_mandir/??/man5/
%_mandir/man5/sssd-ad.5*
%_mandir/??/man5/sssd-ad.5*

%files ipa
%defattr(-,root,root)
%dir %_libdir/%name/
%_libdir/%name/libsss_ipa*
%dir %_datadir/%name/
%dir %_datadir/%name/sssd.api.d
%_datadir/%name/sssd.api.d/sssd-ipa.conf
%dir %_mandir/??/man5/
%_mandir/man5/sssd-ipa.5*
%_mandir/??/man5/sssd-ipa.5*

%files krb5
%defattr(-,root,root)
%dir %_libdir/%name/
%_libdir/%name/libsss_krb5.so
%dir %_datadir/%name/
%dir %_datadir/%name/sssd.api.d/
%_datadir/%name/sssd.api.d/sssd-krb5.conf
%dir %_mandir/??/man5/
%_mandir/man5/sssd-krb5.5*
%_mandir/??/man5/sssd-krb5.5*

%files krb5-common
%defattr(-,root,root)
%dir %_libdir/%name/
%_libdir/%name/libsss_krb5_common.so
%dir %_libexecdir/%name/
%_libexecdir/%name/krb5_child
%_libexecdir/%name/ldap_child

%files ldap
%defattr(-,root,root)
%dir %_libdir/%name/
%_libdir/%name/libsss_ldap*
%dir %_datadir/%name/
%dir %_datadir/%name/sssd.api.d/
%_datadir/%name/sssd.api.d/sssd-ldap.conf
%dir %_mandir/??/man5/
%_mandir/??/man5/sssd-ldap.5*
%_mandir/man5/sssd-ldap.5*

%files proxy
%defattr(-,root,root)
%dir %_libdir/%name/
%_libdir/%name/libsss_proxy.so
%dir %_libexecdir/%name/
%_libexecdir/%name/proxy_child
%dir %_datadir/%name/
%dir %_datadir/%name/sssd.api.d/
%_datadir/%name/sssd.api.d/sssd-proxy.conf

%files tools
%defattr(-,root,root)
%_sbindir/sss_cache
%_sbindir/sss_debuglevel
%_sbindir/sss_groupadd
%_sbindir/sss_groupdel
%_sbindir/sss_groupmod
%_sbindir/sss_groupshow
%_sbindir/sss_seed
%_sbindir/sss_obfuscate
%_sbindir/sss_useradd
%_sbindir/sss_userdel
%_sbindir/sss_usermod
%dir %_mandir/??/man8/
%_mandir/??/man8/sss_*.8*
%_mandir/man8/sss_*.8*

%files -n libipa_hbac0
%defattr(-,root,root)
%_libdir/libipa_hbac.so.0*

%files -n libipa_hbac-devel
%defattr(-,root,root)
%_includedir/ipa_hbac.h
%_libdir/libipa_hbac.so
%_libdir/pkgconfig/ipa_hbac.pc

%files -n libsss_idmap0
%defattr(-,root,root)
%_libdir/libsss_idmap.so.0*

%files -n libsss_idmap-devel
%defattr(-,root,root)
%_includedir/sss_idmap.h
%_libdir/libsss_idmap.so
%_libdir/pkgconfig/sss_idmap.pc

%files -n libsss_nss_idmap0
%defattr(-,root,root)
%_libdir/libsss_nss_idmap.so.0*

%files -n libsss_nss_idmap-devel
%defattr(-,root,root)
%_includedir/sss_nss_idmap.h
%_libdir/libsss_nss_idmap.so
%_libdir/pkgconfig/sss_nss_idmap.pc

%files -n libsss_sudo
%defattr(-,root,root)
%_libdir/libsss_sudo.so

%files -n python-ipa_hbac
%defattr(-,root,root)
%dir %python_sitearch
%python_sitearch/pyhbac.so

%files -n python-sss_nss_idmap
%defattr(-,root,root)
%dir %python_sitearch
%python_sitearch/pysss_nss_idmap.so

%files -n python-sssd-config
%defattr(-,root,root)
%python_sitearch/pysss.so
%python_sitearch/pysss_murmur.so
%python_sitelib/SSSDConfig*

%changelog
* Fri Dec 20 2013 jengelh@inai.de
- Update to new upstream release 1.11.3
  * The AD provider is able to resolve group memberships for groups
  with Global and Universal scope
  * The initgroups (get groups for user) operation for users from
  trusted AD domains was made more reliable by reading the required
  tokenGroups attribute from LDAP instead of Global Catalog
  * A new option ad_enable_gc was added to the AD provider. This
  option allows the administrator to force SSSD to talk to LDAP
  port only and never try the Global Catalog
  * The AD provider is now able to leverage the tokenGroups attribute
  even when POSIX attributes are used, providing better performance
  during logins.
  * A memory leak in the NSS responder that affected long-lived
  clients that requested netgroup data was fixed
- Remove sssd-ldflags.diff (merged upstream)
* Thu Nov 28 2013 ckornacker@suse.com
- Migrate deprecated krb5_kdcip variable to krb5_server (bnc#851048)
* Fri Nov  1 2013 jengelh@inai.de
- Update to new upstream release 1.11.2
  * A new option ad_access_filter was added. This option allows the
  administrator to easily configure LDAP search filter that the users
  logging in must match in order to be granted access.
  * The Kerberos provider will no longer try to create public
  directories when evaluating the krb5_ccachedir option.
- Remove 0005-implicit-decl.diff (merged upstream)
* Tue Sep  3 2013 jengelh@inai.de
- Update to new upstream release 1.11.0
  * The sudo integration was made more robust. SSSD is now able to
  gracefully handle situations where it is not able to resolve the
  client host name or sudo rules have multiple name attributes.
  * Several nested group membership bugs were fixed
  * The PAC responder was made more robust and efficient, modifying
  existing cache entries instead of always recreating them.
  * The Kerberos provider now supports the new KEYRING ccache type.
- Remove sssd-no-ldb-check.diff, now implemented through a
  configure argument --disable-ldb-version-check
* Sun Jun 16 2013 jengelh@inai.de
- Explicitly formulate SASL BuildRequires
* Thu May  2 2013 jengelh@inai.de
- Update to new upstream release 1.9.5
  * Includes a fix for CVE-2013-0287: A simple access provider flaw
  prevents intended ACL use when SSSD is configured as an Active
  Directory client.
  * Fixed spurious password expiration warning that was printed on
  login with the Kerberos back end.
  * A new option ldap_rfc2307_fallback_to_local_users was added. If
  this option is set to true, SSSD is be able to resolve local
  group members of LDAP groups.
  * Fixed an indexing bug that prevented the contents of autofs maps
  from being returned to the automounter deamon in case the map
  contained a large number of entries.
  * Several fixes for safer handling of Kerberos credential caches
  for cases where the ccache is set to be stored in a DIR: type.
- Remove Provide-a-be_get_account_info_send-function.patch,
  Add-unit-tests-for-simple-access-test-by-groups.patch,
  Do-not-compile-main-in-DP-if-UNIT_TESTING-is-defined.patch,
  Resolve-GIDs-in-the-simple-access-provider.patch
  (CVE-2013-0287 material is in upstream),
  sssd-sysdb-binary-attrs.diff (merged upstream)
* Fri Apr  5 2013 jengelh@inai.de
- Implement signature verification
* Wed Mar 20 2013 rhafer@suse.com
- Fixed security issue: CVE-2013-0287 (bnc#809153):
  When SSSD is configured as an Active Directory client by using
  the new Active Directory provider or equivalent configuration
  of the LDAP provider, the Simple Access Provider does not
  handle access control correctly.  If any groups are specified
  with the simple_deny_groups option, the group members are
  permitted access. New patches:
  * Provide-a-be_get_account_info_send-function.patch
  * Add-unit-tests-for-simple-access-test-by-groups.patch
  * Do-not-compile-main-in-DP-if-UNIT_TESTING-is-defined.patch
  * Resolve-GIDs-in-the-simple-access-provider.patch
* Tue Feb 26 2013 jengelh@inai.de
- Resolve user retrieval problems when encountering binary data
  in LDAP attributes (bnc#806078),
  added sssd-sysdb-binary-attrs.diff
- Added sssd-no-ldb-check.diff so that SSSD continues to start
  even after an LDB update.
* Fri Feb  8 2013 rhafer@suse.com
- fix package name in baselibs.conf (bnc#796423)
* Thu Jan 31 2013 rhafer@suse.com
- update to 1.9.4 (bnc#801036):
  * A security bug assigned CVE-2013-0219 was fixed - TOCTOU race
    conditions when creating or removing home directories for users
    in local domain
  * A security bug assigned CVE-2013-0220 was fixed - out-of-bounds
    reads in autofs and ssh responder
  * The sssd_pam responder processes pending requests after
    reconnect
  * A serious memory leak in the NSS responder was fixed
  * Requests that were processing group entries with DNs pointing
    out of any configured search bases were not terminated
    correctly, causing long timeouts
  * Kerberos tickets are correctly renewed even after SSSD daemon
    restart
  * Multiple fixes related to SUDO integration, in particular
    fixing functionality when the sssd back end process was
    changing its online/offline status
  * The pwd_exp_warning option was fixed to function as documented
    in the manual page
- refreshed sssd-ldflags.diff to apply cleanly
* Mon Dec 10 2012 rhafer@suse.com
- Removed left-over "Requires" for no longer existing sssd-client
  subpackage.
- New patch: sssd-ldflags.diff to fix link failures due to erroneous
  LDFLAGS usage
* Thu Dec  6 2012 rhafer@suse.com
- Switch back to using libcrypto instead of mozilla-nss as it seems
  to be supported upstream again, cf.
  https://lists.fedorahosted.org/pipermail/sssd-devel/2012-June/010202.html
- Cleanup PAM configuration after uninstalling sssd (bnc#788328)
* Thu Dec  6 2012 jengelh@inai.de
- Update to new upstream release 1.9.3
  * Many fixes related to deployments where the SSSD is running as
  a client of IPA server with trust relation established with an
  Active Directory server
  * Multiple fixes related to correct reporting of group
  memberships, especially in setups that use nested groups
  * Fixed a bug that prevented upgrade from the 1.8 series if the
  cache contained nested groups before the upgrade
  * Restarting the responders is more robust for cases where the
  machine is under heavy load during back end restart
  * The default_shell option can now be also set per-domain in
  addition to global setting.
* Sat Nov 10 2012 jengelh@inai.de
- Update to new upstream release 1.9.2
  * Users or groups from trusted domains can be retrieved by UID or
  GID as well
  * Several fixes that mitigate file descriptor leak during logins
  * SSH host keys are also removed from the cache after being
  removed from the server
  * Fix intermittent crash in responders if the responder was
  shutting down while requests were still pending
  * Catch an error condition that might have caused a tight loop in
  the sssd_nss process while refreshing expired enumeration request
  * Fixed memory hierarchy of subdomains discovery requests that
  caused use-after-free access bugs
  * The krb5_child and ldap_child processes can print libkrb5 tracing
  information in the debug logs
* Wed Jun 27 2012 jengelh@inai.de
- Update to new upstream release 1.8.93 (1.9.0~beta3)
  * Add native support for autofs to the IPA provider
  * Support for id mapping when connecting to Active Directory
  * Support for handling very large (> 1500 users) groups in
  Active Directory
  * Add a new fast in-memory cache to speed up lookups of cached data
  on repeated requests
  * Add support for the Kerberos DIR cache for storing multiple TGTs
  automatically
  * Add a new PAC responder for dealing with cross-realm Kerberos
  trusts
  * Terminate idle connections to the NSS and PAM responders
* Thu May 10 2012 jengelh@inai.de
- Update to new upstream release 1.8.3
  * LDAP: Handle situations where the RootDSE is not available
  anonymously
  * LDAP: Fix regression for users using non-standard LDAP attributes
  for user information
- Switch from openssl to mozilla-nss, as this is the officially
  supported crypto integration
* Fri Apr 13 2012 ben.kevan@gmail.com
- Fix build error on SLES 11 builds
* Tue Apr 10 2012 ben.kevan@gmail.com
- Add suse_version condition for glib over libunistring for
  SLES 11 SP2.
- Update to new upstream release 1.8.2
  * Fix for GSSAPI binds when the keytab contains unrelated
  principals
  * Workarounds added for LDAP servers with unreadable RootDSE
* Wed Apr  4 2012 ben.kevan@gmail.com
- Update to new upstream release 1.8.1
  * Resolve issue where we could enter an infinite loop trying to
  connect to an auth server
* Sun Mar 11 2012 jengelh@medozas.de
- Update to new upstream release 1.8.0
  * Support for the service map in NSS
  * Support for setting default SELinux user context from FreeIPA
  * Support for retrieving SSH user and host keys from LDAP
  * Support for caching autofs LDAP requests
  * Support for caching SUDO rules
  * Include the IPA AutoFS provider
  * Fixed several memory-corruption bugs
  * Fixed a regression in the proxy provider
* Wed Oct 19 2011 rhafer@suse.de
- Fixed systemd related packaging issues (bnc#724157)
- fixed build on older openSUSE releases
* Mon Sep 19 2011 jengelh@medozas.de
- Resolve "have choice for libnl-devel:
  libnl-1_1-devel libnl3-devel"
* Tue Aug  2 2011 rhafer@suse.de
- Fixed typos in configure args
- Cherry-picked password policy fixes from 1.5 branch (bnc#705768)
- switched to fd-leak fix cherry-picked from 1.5 branch
- Add /usr/sbin to the search path to make configure find nscd
  (bnc#709747)
* Fri Jul 29 2011 jengelh@medozas.de
- Add patches to fix an fd leak in sssd_pam
* Thu Jul 28 2011 jengelh@medozas.de
- Update to new upstream release 1.5.11
  * Support for overriding home directory, shell and primary GID
  locally
  * Properly honor TTL values from SRV record lookups
  * Support non-POSIX groups in nested group chains (for RFC2307bis
  LDAP servers)
  * Properly escape IPv6 addresses in the failover code
  * Do not crash if inotify fails (e.g. resource exhaustion)
- Remove redundant %%clean section; delete .la files more
  efficiently
* Tue Jun  7 2011 rhafer@suse.de
- Update to 1.5.8:
  * Support for the LDAP paging control
  * Support for multiple DNS servers for name resolution
  * Fixes for several group membership bugs
  * Fixes for rare crash bugs
* Wed May  4 2011 rhafer@suse.de
- Update to 1.5.7
  * A flaw was found in the handling of cached passwords when
    kerberos renewal tickets is enabled.  Due to a bug, the cached
    password was overwritten with a (moderately) predictable
    filename, which could allow a user to authenticate as someone
    else if they knew the name of the cache file (bnc#691135,
    CVE-2011-1758)
- Changes in 1.5.6:
  * Fixed a serious memory leak in the memberOf plugin
  * Fixed a regression with the negative cache that caused it to be
    essentially nonfunctional
  * Fixed an issue where the user's full name would sometimes be
    removed from the cache
  * Fixed an issue with password changes in the kerberos provider
    not working with kpasswd
* Thu Apr 14 2011 rhafer@suse.de
- Update to 1.5.5
  * Fixes for several crash bugs
  * LDAP group lookups will no longer abort if there is a
  zero-length member attribute
  * Add automatic fallback to 'cn' if the 'gecos' attribute does not
  exist
* Wed Mar 30 2011 rhafer@suse.de
- Should build in SLE-11-SP1 now
* Tue Mar 29 2011 rhafer@suse.de
- Updated to 1.5.4
  * Fixes for Active Directory when not all users and groups have
    POSIX attributes
  * Fixes for handling users and groups that have name aliases
    (aliases are ignored)
  * Fix group memberships after initgroups in the IPA provider
* Thu Mar 24 2011 rhafer@suse.de
- Updated to 1.5.3
  * Support for libldb >= 1.0.0
  * Proper detection of manpage translations
  * Changes between 1.5.1 and 1.5.2
  * Fixes for support of FreeIPA v2
  * Fixes for failover if DNS entries change
  * Improved sss_obfuscate tool with better interactive mode
  * Fix several crash bugs
  * Don't attempt to use START_TLS over SSL. Some LDAP servers
    can't handle this
  * Delete users from the local cache if initgroups calls return
    'no such user' (previously only worked for getpwnam/getpwuid)
  * Use new Transifex.net translations
  * Better support for automatic TGT renewal (now survives
    restart)
  * Netgroup fixes
* Tue Mar  8 2011 rhafer@suse.de
- Updated to 1.5.1
  * Vast performance improvements when enumerate = true
  * All PAM actions will now perform a forced initgroups lookup
    instead of just a user information lookup This guarantees that
    all group information is available to other providers, such as
    the simple provider.
  * For backwards-compatibility, DNS lookups will also fall back to
    trying the SSSD domain name as a DNS discovery domain.
  * Support for more password expiration policies in LDAP
  - 389 Directory Server
  - FreeIPA
  - ActiveDirectory
  * Support for ldap_tls_{cert,key,cipher_suite} config options
  * Assorted bugfixes
* Wed Jan 19 2011 rhafer@suse.de
- /var/lib/sss/pubconf was missing (bnc#665442)
* Tue Jan 18 2011 rhafer@suse.de
- It was possible to make sssd hang forever inside a loop in the
  PAM responder by sending a carefully crafted packet to sssd.
  This could be exploited by a local attacker to crash sssd and
  prevent other legitimate users from logging into the system.
  (bnc#660481, CVE-2010-4341)
* Sun Dec 19 2010 aj@suse.de
- Own /etc/systemd directories to fix build.
* Thu Nov 25 2010 rhafer@novell.com
- install systemd service file
* Tue Nov 16 2010 rhafer@novell.com
- Updated to 1.4.1
  * Add support for netgroups to the LDAP and proxy providers
  * Fixes a minor bug with UIDs/GIDs >= 2^31
  * Fixes a segfault in the kerberos provider
  * Fixes a segfault in the NSS responder if a data provider crashes
  * Correctly use sdap_netgroup_search_base
  * the utility libraries libpath_utils1, libpath_utils-devel,
    libref_array1 and libref_array-devel moved to their own
    separate upstream project (ding-libs)
  * Performance improvements made to group processing of RFC2307
    LDAP servers
  * Fixed nested group issues with RFC2307bis LDAP servers without
    a memberOf plugin
  * Manpage reviewed and updated
* Mon Sep 13 2010 coolo@novell.com
- remove hard coded python version
* Fri Sep  3 2010 rhafer@novell.com
- No dependencies on %%{release}
* Mon Aug 30 2010 rhafer@novell.com
- Updated to 1.3.1
  * Fixes to the HBAC backend for obsolete or removed HBAC entries
  * Improvements to log messages around TLS and GSSAPI for LDAP
  * Support for building in environments using --as-needed LDFLAGS
  * Vast performance improvement for initgroups on RFC2307 LDAP servers
  * Long-running SSSD clients (e.g. GDM) will now reconnect properly to the
  daemon if SSSD is restarted
  * Rewrote the internal LDB cache API. As a synchronous API it is now faster
  to access and easier to work with
  * Eugene Indenbom contributed a sizeable amount of code to the LDAP provider
  - We now handle failover situations much more reliably than we did
    previously
  - We also will now monitor the GSSAPI kerberos ticket and automatically
    renew it when appropriate, instead of waiting for a connection to fail
  * Support for netlink now allows us to more quickly detect situations
  where we may have come online
  * New option "dns_discovery_domain" allows better configuration for
  using SRV records for failover
- New subpackages: libpath_utils1, libpath_utils-devel, libref_array1
  and libref_array-devel
* Wed Mar 31 2010 rhafer@novell.com
- Package pam- and nss-Modules as baselibs
- cleaned up file list and dependencies
- fixed init script dependencies
* Wed Mar 31 2010 rhafer@novell.com
- Updated to 1.1.0
  * Support for IPv6
  * Support for LDAP referrals
  * Offline failed login counter
  * Fix for the long-standing cache cleanup performance issues
  * libini_config, libcollection, libdhash, libref_array and
    libpath_utils are now built as shared libraries for general
    consumption (libref_array and libpath_utils are currently not
    packaged, as no component in sssd links against them)
  * Users get feedback from PAM if they authenticated offline
  * Native local backend now has a utility to show nested memberships
    (sss_groupshow)
  * New "simple" access provider for easy restriction of users
- Backported libcrypto support from master to avoid Mozilla NSS
  dependency
- Backported password policy improvments for LDAP provider from
  master
* Mon Mar  8 2010 rhafer@novell.com
- use logfiles for debug messages by default
* Fri Mar  5 2010 rhafer@novell.com
- subpackages for commandline tools, ipa-provider plugin and
  python API
* Fri Feb 26 2010 rhafer@novell.com
- Updated to 1.0.5. Highlights:
  * Removed some dead code (libreplace
  * Clarify licenses throughout the code
* Thu Feb  4 2010 rhafer@novell.com
- Updated to 1.0.4
* Thu Oct  8 2009 rhafer@novell.com
- Update to 0.6.0
* Fri Sep  4 2009 rhafer@novell.com
- fix LDAP filter for initgroups() with  rfc2307bis setups
* Tue Sep  1 2009 rhafer@novell.com
- initial package submission
