#
# spec file for package krb5
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

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#


%define build_mini 0
%define srcRoot krb5-1.11.4
%define vendorFiles %{_builddir}/%{srcRoot}/vendor-files/
%define krb5docdir  %{_defaultdocdir}/krb5

Name:           krb5
Url:            http://web.mit.edu/kerberos/www/
BuildRequires:  autoconf
BuildRequires:  bison
BuildRequires:  doxygen
BuildRequires:  keyutils
BuildRequires:  keyutils-devel
BuildRequires:  libcom_err-devel
BuildRequires:  libselinux-devel
BuildRequires:  ncurses-devel
Version:        1.11.4
Release:        0
Summary:        MIT Kerberos5 Implementation--Libraries
License:        MIT
Group:          Productivity/Networking/Security
%if ! 0%{?build_mini}
BuildRequires:  libopenssl-devel
BuildRequires:  openldap2-devel
BuildRequires:  pam-devel
BuildRequires:  python-Cheetah
BuildRequires:  python-Sphinx
BuildRequires:  python-libxml2
BuildRequires:  python-lxml
%if 0%{?suse_version} >= 1210
BuildRequires:  pkgconfig(systemd)
%endif
# bug437293
%ifarch ppc64
Obsoletes:      krb5-64bit
%endif
Conflicts:      krb5-mini
%else # -mini
Conflicts:      krb5
Conflicts:      krb5-client
Conflicts:      krb5-server
Conflicts:      krb5-plugin-kdb-ldap
Conflicts:      krb5-plugin-preauth-pkinit
%endif
Source:         krb5-%{version}.tar.bz2
Source1:        vendor-files.tar.bz2
Source2:        baselibs.conf
Source5:        krb5-rpmlintrc
Patch1:         krb5-1.11-pam.patch
Patch2:         krb5-1.9-manpaths.dif
Patch3:         krb5-1.10-buildconf.patch
Patch4:         krb5-1.6.3-gssapi_improve_errormessages.dif
Patch5:         krb5-1.10-kpasswd_tcp.patch
Patch6:         krb5-1.6.3-ktutil-manpage.dif
Patch7:         krb5-1.7-doublelog.patch
Patch8:         krb5-1.8-api.patch
Patch9:         krb5-1.9-kprop-mktemp.patch
Patch10:        krb5-1.10-ksu-access.patch
Patch11:        krb5-1.9-ksu-path.patch
Patch12:        krb5-1.11-selinux-label.patch
Patch13:        krb5-1.9-debuginfo.patch
Patch14:        krb5-kvno-230379.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
PreReq:         mktemp, grep, /bin/touch, coreutils
PreReq:         %insserv_prereq %fillup_prereq

%description
Kerberos V5 is a trusted-third-party network authentication system,
which can improve your network's security by eliminating the insecure
practice of clear text passwords.

%if ! %{build_mini}

%package client
Conflicts:      krb5-mini
Summary:        MIT Kerberos5 implementation - client programs
Group:          Productivity/Networking/Security

%description client
Kerberos V5 is a trusted-third-party network authentication system,
which can improve your network's security by eliminating the insecure
practice of cleartext passwords. This package includes some required
client programs, like kinit, kadmin, ...

%package server
Summary:        MIT Kerberos5 implementation - server
Group:          Productivity/Networking/Security
Requires:       cron
Requires:       logrotate
Requires:       perl-Date-Calc
%{?systemd_requires}
PreReq:         %insserv_prereq %fillup_prereq

%description server
Kerberos V5 is a trusted-third-party network authentication system,
which can improve your network's security by eliminating the insecure
practice of cleartext passwords. This package includes the kdc, kadmind
and more.

%package plugin-kdb-ldap
Summary:        MIT Kerberos5 Implementation--LDAP Database Plugin
Group:          Productivity/Networking/Security
Requires:       krb5-server = %{version}

%description plugin-kdb-ldap
Kerberos V5 is a trusted-third-party network authentication system,
which can improve your network's security by eliminating the insecure
practice of clear text passwords. This package contains the LDAP
database plugin.

%package plugin-preauth-pkinit
Summary:        MIT Kerberos5 Implementation--PKINIT preauth Plugin
Group:          Productivity/Networking/Security

%description plugin-preauth-pkinit
Kerberos V5 is a trusted-third-party network authentication system,
which can improve your network's security by eliminating the insecure
practice of cleartext passwords. This package includes a PKINIT plugin.

%package doc
Summary:        MIT Kerberos5 Implementation--Documentation
Group:          Documentation/Other

%description doc
Kerberos V5 is a trusted-third-party network authentication
system,which can improve your network's security by eliminating the
insecurepractice of clear text passwords. This package includes
extended documentation for MIT Kerberos.

%endif #! build_mini

%package devel
Summary:        MIT Kerberos5 - Include Files and Libraries
Group:          Development/Libraries/C and C++
PreReq:         %{name} = %{version}
Requires:       keyutils-devel
Requires:       libcom_err-devel
# bug437293
%ifarch ppc64
Obsoletes:      krb5-devel-64bit
%endif
%if %{build_mini}
Provides:       krb5-devel = %{version}
Conflicts:      krb5-devel
%else
Conflicts:      krb5-mini-devel
%endif
#

%description devel
Kerberos V5 is a trusted-third-party network authentication system,
which can improve your network's security by eliminating the insecure
practice of cleartext passwords. This package includes Libraries and
Include Files for Development

%prep
%setup -q -n %{srcRoot}
%setup -a 1 -T -D -n %{srcRoot}
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p0
%patch14 -p1

%build
# needs to be re-generated
rm -f src/lib/krb5/krb/deltat.c
cd src
./util/reconf
DEFCCNAME=DIR:/run/user/%%{uid}/krb5cc; export DEFCCNAME
./configure \
        CC="%{__cc}" \
        CFLAGS="$RPM_OPT_FLAGS -I%{_includedir}/et -fno-strict-aliasing -D_GNU_SOURCE -fPIC $(getconf LFS_CFLAGS)" \
        CPPFLAGS="-I%{_includedir}/et " \
        SS_LIB="-lss" \
        --prefix=/usr/lib/mit \
        --sysconfdir=%{_sysconfdir} \
        --mandir=%{_mandir} \
        --infodir=%{_infodir} \
        --libexecdir=/usr/lib/mit/sbin \
        --libdir=%{_libdir} \
        --includedir=%{_includedir} \
        --localstatedir=%{_localstatedir}/lib/kerberos \
        --localedir=%{_datadir}/locale \
        --enable-shared \
        --disable-static \
        --enable-dns-for-realm \
        --disable-rpath \
%if ! %{build_mini}
        --with-ldap \
        --with-pam \
        --enable-pkinit \
        --with-pkinit-crypto-impl=openssl \
%else
        --disable-pkinit \
        --without-pam \
%endif
        --with-selinux \
        --with-system-et \
        --with-system-ss
%{__make} %{?_smp_mflags}
%if ! 0%{?build_mini}
cd doc
make %{?jobs:-j%jobs} substhtml
cp -a html_subst ../../html
cd ..
%endif

%install

# Where per-user keytabs live by default.
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/lib/kerberos/krb5/user
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/log/krb5

cd src
make DESTDIR=%{buildroot} install
cd ..
# Munge krb5-config yet again.  This is totally wrong for 64-bit, but chunks
# of the buildconf patch already conspire to strip out /usr/<anything> from the
# list of link flags, and it helps prevent file conflicts on multilib systems.
sed -r -i -e 's|^libdir=/usr/lib(64)?$|libdir=/usr/lib|g' $RPM_BUILD_ROOT/usr/lib/mit/bin/krb5-config

# install autoconf macro
mkdir -p %{buildroot}/%{_datadir}/aclocal
install -m 644 src/util/ac_check_krb5.m4 %{buildroot}%{_datadir}/aclocal/
# install sample config files
# I'll probably do something about this later on
mkdir -p %{buildroot}%{_sysconfdir} %{buildroot}%{_localstatedir}/lib/kerberos/krb5kdc
mkdir -p %{buildroot}%{_sysconfdir}
mkdir -p %{buildroot}/etc/profile.d/
mkdir -p %{buildroot}/var/log/krb5
mkdir -p %{buildroot}/etc/sysconfig/SuSEfirewall2.d/services/
# create plugin directories
mkdir -p %{buildroot}/%{_libdir}/krb5/plugins/kdb
mkdir -p %{buildroot}/%{_libdir}/krb5/plugins/preauth
mkdir -p %{buildroot}/%{_libdir}/krb5/plugins/libkrb5
install -m 644 %{vendorFiles}/krb5.conf %{buildroot}%{_sysconfdir}
install -m 600 %{vendorFiles}/kdc.conf %{buildroot}%{_localstatedir}/lib/kerberos/krb5kdc/
install -m 600 %{vendorFiles}/kadm5.acl %{buildroot}%{_localstatedir}/lib/kerberos/krb5kdc/
install -m 600 %{vendorFiles}/kadm5.dict %{buildroot}%{_localstatedir}/lib/kerberos/krb5kdc/
install -m 644 %{vendorFiles}/krb5.csh.profile %{buildroot}/etc/profile.d/krb5.csh
install -m 644 %{vendorFiles}/krb5.sh.profile %{buildroot}/etc/profile.d/krb5.sh
install -m 644 %{vendorFiles}/SuSEFirewall.kdc %{buildroot}/etc/sysconfig/SuSEfirewall2.d/services/kdc
install -m 644 %{vendorFiles}/SuSEFirewall.kadmind %{buildroot}/etc/sysconfig/SuSEfirewall2.d/services/kadmind
# all libs must have permissions 0755
for lib in `find %{buildroot}/%{_libdir}/ -type f -name "*.so*"`
do
  chmod 0755 ${lib}
done
# and binaries too
chmod 0755 %{buildroot}/usr/lib/mit/bin/ksu
# install init scripts
mkdir -p %{buildroot}%{_sysconfdir}/init.d
install -m 755 %{vendorFiles}/kadmind.init %{buildroot}%{_sysconfdir}/init.d/kadmind
install -m 755 %{vendorFiles}/krb5kdc.init %{buildroot}%{_sysconfdir}/init.d/krb5kdc
install -m 755 %{vendorFiles}/kpropd.init  %{buildroot}%{_sysconfdir}/init.d/kpropd
# install systemd files
%if 0%{?suse_version} >= 1210
mkdir -p %{buildroot}%{_unitdir}
install -m 644 %{vendorFiles}/kadmind.service %{buildroot}%{_unitdir}
install -m 644 %{vendorFiles}/krb5kdc.service %{buildroot}%{_unitdir}
install -m 644 %{vendorFiles}/kpropd.service %{buildroot}%{_unitdir}
%endif
# install sysconfig templates
mkdir -p $RPM_BUILD_ROOT/%{_var}/adm/fillup-templates
install -m 644 %{vendorFiles}/sysconfig.kadmind $RPM_BUILD_ROOT/%{_var}/adm/fillup-templates/
install -m 644 %{vendorFiles}/sysconfig.krb5kdc $RPM_BUILD_ROOT/%{_var}/adm/fillup-templates/
# install logrotate files
mkdir -p %{buildroot}%{_sysconfdir}/logrotate.d
install -m 644 %{vendorFiles}/krb5-server.logrotate %{buildroot}%{_sysconfdir}/logrotate.d/krb5-server
find . -type f -name '*.ps' -exec gzip -9 {} \;
# create rc* links
mkdir -p %{buildroot}/usr/bin/
mkdir -p %{buildroot}/usr/sbin/
ln -sf ../../etc/init.d/kadmind %{buildroot}/usr/sbin/rckadmind
ln -sf ../../etc/init.d/krb5kdc %{buildroot}/usr/sbin/rckrb5kdc
ln -sf ../../etc/init.d/kpropd %{buildroot}/usr/sbin/rckpropd
# create links for kinit and klist, because of the java ones
ln -sf ../../usr/lib/mit/bin/kinit   %{buildroot}/usr/bin/kinit
ln -sf ../../usr/lib/mit/bin/klist   %{buildroot}/usr/bin/klist
# install doc
install -d -m 755 %{buildroot}/%{krb5docdir}
install -m 644 %{_builddir}/%{srcRoot}/README %{buildroot}/%{krb5docdir}/README
%if ! %{build_mini}
install -m 644 %{_builddir}/%{srcRoot}/src/plugins/kdb/ldap/libkdb_ldap/kerberos.schema %{buildroot}/%{krb5docdir}/kerberos.schema
install -m 644 %{_builddir}/%{srcRoot}/src/plugins/kdb/ldap/libkdb_ldap/kerberos.ldif %{buildroot}/%{krb5docdir}/kerberos.ldif
%endif
# cleanup
rm -f  %{buildroot}/usr/share/man/man1/tmac.doc*
rm -f  /usr/share/man/man1/tmac.doc*
rm -rf %{buildroot}/usr/lib/mit/share/examples

%find_lang mit-krb5

#####################################################
# krb5(-mini) pre/post/postun
#####################################################

%if %{build_mini}

%preun
%if 0%{?suse_version} >= 1210
%service_del_preun krb5kdc.service kadmind.service kpropd.service
%else
%stop_on_removal krb5kdc kadmind kpropd
%endif

%postun
/sbin/ldconfig
%if 0%{?suse_version} >= 1210
%service_del_postun krb5kdc.service kadmind.service kpropd.service
%else
%restart_on_update krb5kdc kadmind kpropd
%{insserv_cleanup}
%endif

%post
/sbin/ldconfig
%if 0%{?suse_version} >= 1210
%service_add_post krb5kdc.service kadmind.service kpropd.service
%endif
%{fillup_only -n kadmind}
%{fillup_only -n krb5kdc}
%{fillup_only -n kpropd}

%pre
%if 0%{?suse_version} >= 1210
%service_add_pre krb5kdc.service kadmind.service kpropd.service
%endif

%else

%post -p /sbin/ldconfig

%postun
/sbin/ldconfig

#####################################################
# krb5-server preun/postun/pre/post
#####################################################

%preun server
%if 0%{?suse_version} >= 1210
%service_del_preun krb5kdc.service kadmind.service kpropd.service
%else
%stop_on_removal krb5kdc kadmind kpropd
%endif

%postun server
%if 0%{?suse_version} >= 1210
%service_del_postun krb5kdc.service kadmind.service kpropd.service
%else
%restart_on_update krb5kdc kadmind kpropd
%{insserv_cleanup}
%endif

%post server
%if 0%{?suse_version} >= 1210
%service_add_post krb5kdc.service kadmind.service kpropd.service
%endif
%{fillup_only -n kadmind}
%{fillup_only -n krb5kdc}
%{fillup_only -n kpropd}

%pre server
%if 0%{?suse_version} >= 1210
%service_add_pre krb5kdc.service kadmind.service kpropd.service
%endif

#####################################################
# krb5-plugin-kdb-ldap post/postun
#####################################################

%post plugin-kdb-ldap -p /sbin/ldconfig

%postun plugin-kdb-ldap
/sbin/ldconfig

%endif

########################################################
# files sections
########################################################

%files devel
%defattr(-,root,root)
%dir /usr/lib/mit
%dir /usr/lib/mit/bin
%dir /usr/lib/mit/sbin
%dir /usr/lib/mit/share
%dir %{_datadir}/aclocal
%{_libdir}/libgssrpc.so
%{_libdir}/libk5crypto.so
%{_libdir}/libkadm5clnt_mit.so
%{_libdir}/libkadm5clnt.so
%{_libdir}/libkadm5srv_mit.so
%{_libdir}/libkadm5srv.so
%{_libdir}/libkdb5.so
%{_libdir}/libkrb5.so
%{_libdir}/libkrb5support.so
%{_libdir}/libverto.so
%{_includedir}/*
/usr/lib/mit/bin/krb5-config
/usr/lib/mit/sbin/krb5-send-pr
/usr/lib/mit/share/gnats
%{_mandir}/man1/krb5-send-pr.1*
%{_mandir}/man1/krb5-config.1*
%{_datadir}/aclocal/ac_check_krb5.m4

%if %{build_mini}

%files -f mit-krb5.lang
%defattr(-,root,root)
%dir %{krb5docdir}
# add directories
%dir %{_libdir}/krb5
%dir %{_libdir}/krb5/plugins
%dir %{_libdir}/krb5/plugins/kdb
%dir %{_libdir}/krb5/plugins/preauth
%dir %{_libdir}/krb5/plugins/libkrb5
%dir %{_localstatedir}/lib/kerberos/
%dir %{_localstatedir}/lib/kerberos/krb5kdc
%dir %{_localstatedir}/lib/kerberos/krb5
%dir %{_localstatedir}/lib/kerberos/krb5/user
%attr(0700,root,root) %dir /var/log/krb5
%dir /usr/lib/mit
%dir /usr/lib/mit/sbin
%dir /usr/lib/mit/bin
%doc %{krb5docdir}/README
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/krb5.conf
%attr(0644,root,root) %config /etc/profile.d/krb5*
%config(noreplace) %{_sysconfdir}/logrotate.d/krb5-server
%attr(0600,root,root) %config(noreplace) %{_localstatedir}/lib/kerberos/krb5kdc/kdc.conf
%attr(0600,root,root) %config(noreplace) %{_localstatedir}/lib/kerberos/krb5kdc/kadm5.acl
%attr(0600,root,root) %config(noreplace) %{_localstatedir}/lib/kerberos/krb5kdc/kadm5.dict
%config %{_sysconfdir}/sysconfig/SuSEfirewall2.d/services/k*
%{_var}/adm/fillup-templates/sysconfig.*
%{_sysconfdir}/init.d/*
%if 0%{?suse_version} >= 1210
%{_unitdir}/kadmind.service
%{_unitdir}/krb5kdc.service
%{_unitdir}/kpropd.service
%endif
%{_libdir}/libgssapi_krb5.*
%{_libdir}/libgssrpc.so.*
%{_libdir}/libk5crypto.so.*
%{_libdir}/libkadm5clnt_mit.so.*
%{_libdir}/libkadm5srv_mit.so.*
%{_libdir}/libkdb5.so.*
%{_libdir}/libkrb5.so.*
%{_libdir}/libkrb5support.so.*
%{_libdir}/libverto.so.*
%{_libdir}/krb5/plugins/kdb/*
#/usr/lib/mit/sbin/*
/usr/lib/mit/sbin/kadmin.local
/usr/lib/mit/sbin/kadmind
/usr/lib/mit/sbin/kpropd
/usr/lib/mit/sbin/kproplog
/usr/lib/mit/sbin/kprop
/usr/lib/mit/sbin/kdb5_util
/usr/lib/mit/sbin/krb5kdc
/usr/lib/mit/sbin/uuserver
/usr/lib/mit/sbin/sserver
/usr/lib/mit/sbin/gss-server
/usr/lib/mit/sbin/sim_server
/usr/lib/mit/bin/k5srvutil
/usr/lib/mit/bin/kvno
/usr/lib/mit/bin/kinit
/usr/lib/mit/bin/kdestroy
/usr/lib/mit/bin/kpasswd
/usr/lib/mit/bin/klist
/usr/lib/mit/bin/kadmin
/usr/lib/mit/bin/ktutil
/usr/lib/mit/bin/kswitch
%attr(0755,root,root) /usr/lib/mit/bin/ksu
/usr/lib/mit/bin/uuclient
/usr/lib/mit/bin/sclient
/usr/lib/mit/bin/gss-client
/usr/lib/mit/bin/sim_client
/usr/bin/kinit
/usr/bin/klist
/usr/sbin/rc*
#%{_mandir}/man1/*
%{_mandir}/man1/kvno.1*
%{_mandir}/man1/kinit.1*
%{_mandir}/man1/kdestroy.1*
%{_mandir}/man1/kpasswd.1*
%{_mandir}/man1/klist.1*
%{_mandir}/man1/ksu.1*
%{_mandir}/man1/sclient.1*
%{_mandir}/man1/kadmin.1*
%{_mandir}/man1/ktutil.1*
%{_mandir}/man1/k5srvutil.1*
%{_mandir}/man1/kswitch.1*
%{_mandir}/man5/*
%{_mandir}/man5/.k5login.5.gz
%{_mandir}/man5/.k5identity.5*
%{_mandir}/man8/*
%else

%files -f mit-krb5.lang
%defattr(-,root,root)
%dir %{krb5docdir}
# add plugin directories
%dir %{_libdir}/krb5
%dir %{_libdir}/krb5/plugins
%dir %{_libdir}/krb5/plugins/kdb
%dir %{_libdir}/krb5/plugins/preauth
%dir %{_libdir}/krb5/plugins/libkrb5
# add log directory
%attr(0700,root,root) %dir /var/log/krb5
%doc %{krb5docdir}/README
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/krb5.conf
%attr(0644,root,root) %config /etc/profile.d/krb5*
%{_libdir}/libgssapi_krb5.*
%{_libdir}/libgssrpc.so.*
%{_libdir}/libk5crypto.so.*
%{_libdir}/libkadm5clnt_mit.so.*
%{_libdir}/libkadm5srv_mit.so.*
%{_libdir}/libkdb5.so.*
%{_libdir}/libkrb5.so.*
%{_libdir}/libkrb5support.so.*
%{_libdir}/libverto.so.*

%files server
%defattr(-,root,root)
%attr(0700,root,root) %dir /var/log/krb5
%config(noreplace) %{_sysconfdir}/logrotate.d/krb5-server
%{_sysconfdir}/init.d/kadmind
%{_sysconfdir}/init.d/krb5kdc
%{_sysconfdir}/init.d/kpropd
%if 0%{?suse_version} >= 1210
%{_unitdir}/kadmind.service
%{_unitdir}/krb5kdc.service
%{_unitdir}/kpropd.service
%endif
%dir %{krb5docdir}
%dir /usr/lib/mit
%dir /usr/lib/mit/sbin
%dir %{_localstatedir}/lib/kerberos/
%dir %{_localstatedir}/lib/kerberos/krb5kdc
%dir %{_localstatedir}/lib/kerberos/krb5
%dir %{_localstatedir}/lib/kerberos/krb5/user
%dir %{_libdir}/krb5
%dir %{_libdir}/krb5/plugins
%dir %{_libdir}/krb5/plugins/kdb
%attr(0600,root,root) %config(noreplace) %{_localstatedir}/lib/kerberos/krb5kdc/kdc.conf
%attr(0600,root,root) %config(noreplace) %{_localstatedir}/lib/kerberos/krb5kdc/kadm5.acl
%attr(0600,root,root) %config(noreplace) %{_localstatedir}/lib/kerberos/krb5kdc/kadm5.dict
%config %{_sysconfdir}/sysconfig/SuSEfirewall2.d/services/k*
%{_var}/adm/fillup-templates/sysconfig.*
/usr/sbin/rc*
/usr/lib/mit/sbin/kadmin.local
/usr/lib/mit/sbin/kadmind
/usr/lib/mit/sbin/kpropd
/usr/lib/mit/sbin/kproplog
/usr/lib/mit/sbin/kprop
/usr/lib/mit/sbin/kdb5_util
/usr/lib/mit/sbin/krb5kdc
/usr/lib/mit/sbin/gss-server
/usr/lib/mit/sbin/sim_server
/usr/lib/mit/sbin/sserver
/usr/lib/mit/sbin/uuserver
%{_libdir}/krb5/plugins/kdb/db2.so
%{_mandir}/man5/kdc.conf.5*
%{_mandir}/man5/kadm5.acl.5*
%{_mandir}/man8/kadmind.8*
%{_mandir}/man8/kadmin.local.8*
%{_mandir}/man8/kpropd.8*
%{_mandir}/man8/kprop.8*
%{_mandir}/man8/kproplog.8.gz
%{_mandir}/man8/kdb5_util.8*
%{_mandir}/man8/krb5kdc.8*
%{_mandir}/man8/sserver.8*

%files client
%defattr(-,root,root)
%dir /usr/lib/mit
%dir /usr/lib/mit/bin
%dir /usr/lib/mit/sbin
/usr/lib/mit/bin/kvno
/usr/lib/mit/bin/kinit
/usr/lib/mit/bin/kdestroy
/usr/lib/mit/bin/kpasswd
/usr/lib/mit/bin/klist
/usr/lib/mit/bin/kadmin
/usr/lib/mit/bin/ktutil
/usr/lib/mit/bin/k5srvutil
/usr/lib/mit/bin/gss-client
/usr/lib/mit/bin/ksu
/usr/lib/mit/bin/sclient
/usr/lib/mit/bin/sim_client
/usr/lib/mit/bin/uuclient
/usr/lib/mit/bin/kswitch
/usr/bin/kinit
/usr/bin/klist
%{_mandir}/man1/kvno.1*
%{_mandir}/man1/kinit.1*
%{_mandir}/man1/kdestroy.1*
%{_mandir}/man1/kpasswd.1*
%{_mandir}/man1/klist.1*
%{_mandir}/man1/kadmin.1*
%{_mandir}/man1/ktutil.1*
%{_mandir}/man1/k5srvutil.1*
%{_mandir}/man1/kswitch.1*
%{_mandir}/man5/krb5.conf.5*
%{_mandir}/man5/.k5login.5*
%{_mandir}/man5/.k5identity.5*
%{_mandir}/man5/k5identity.5*
%{_mandir}/man5/k5login.5*
%{_mandir}/man1/ksu.1.gz
%{_mandir}/man1/sclient.1.gz

%files plugin-kdb-ldap
%defattr(-,root,root)
%dir %{_libdir}/krb5
%dir %{_libdir}/krb5/plugins
%dir %{_libdir}/krb5/plugins/kdb
%dir /usr/lib/mit/sbin/
%dir %{krb5docdir}
%doc %{krb5docdir}/kerberos.schema
%doc %{krb5docdir}/kerberos.ldif
%{_libdir}/krb5/plugins/kdb/kldap.so
/usr/lib/mit/sbin/kdb5_ldap_util
%{_libdir}/libkdb_ldap*
%{_mandir}/man8/kdb5_ldap_util.8*

%files plugin-preauth-pkinit
%defattr(-,root,root)
%dir %{_libdir}/krb5
%dir %{_libdir}/krb5/plugins
%dir %{_libdir}/krb5/plugins/preauth
%{_libdir}/krb5/plugins/preauth/pkinit.so

%files doc
%defattr(-,root,root)
%doc html doc/CHANGES doc/README

%endif #build_mini

%changelog

