#
# spec file for package bind
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


Name:           bind
%define pkg_name bind
%define pkg_vers 9.9.4-P1
BuildRequires:  krb5-devel
BuildRequires:  libcap
BuildRequires:  libcap-devel
BuildRequires:  libmysqlclient-devel
BuildRequires:  libtool
BuildRequires:  libxml2-devel
BuildRequires:  openldap2-devel
BuildRequires:  openssl
BuildRequires:  openssl-devel
BuildRequires:  python-base
BuildRequires:  update-desktop-files
Summary:        Domain Name System (DNS) Server (named)
License:        ISC
Group:          Productivity/Networking/DNS/Servers
Version:        9.9.4P1
Release:        oss13.1
Provides:       named
Provides:       bind9
Provides:       dns_daemon
Obsoletes:      bind8
Obsoletes:      bind9
Requires:       %{name}-chrootenv
Requires:       %{name}-utils
PreReq:         %fillup_prereq %insserv_prereq bind-utils /bin/grep /bin/sed /bin/mkdir /usr/bin/tee /bin/chmod /bin/chown /bin/mv /bin/cat /usr/bin/dirname /usr/bin/diff /usr/bin/old /usr/sbin/groupadd /usr/sbin/useradd /usr/sbin/usermod
Url:            http://isc.org/sw/bind/
Source:         ftp://ftp.isc.org/isc/bind9/%{pkg_vers}/bind-%{pkg_vers}.tar.gz
Source3:        ftp://ftp.isc.org/isc/bind9/%{pkg_vers}/bind-%{pkg_vers}.tar.gz.asc
# from http://www.isc.org/about/openpgp/ ... changes yearly apparently.
Source4:        %name.keyring
Source1:        vendor-files.tar.bz2
Source2:        baselibs.conf
Source9:        ftp://ftp.internic.net/domain/named.root
Source40:       http://www.venaas.no/ldap/bind-sdb/dnszone-schema.txt
Patch:          configure.in.diff
Patch1:         Makefile.in.diff
Patch2:         pid-path.diff
Patch4:         perl-path.diff
Patch51:        pie_compile.diff
Patch52:        named-bootconf.diff
Patch100:       configure.in.diff2
%if 0%{?suse_version} > 1220
BuildRequires:  gpg-offline
%endif

# Rate limiting patch by Paul Vixie et.al. for reflection DoS protection
# see http://www.redbarn.org/dns/ratelimits
#Patch200:       http://ss.vix.su/~vjs/rpz2+rl-9.9.3-P1.patch
#Patch200:       rpz2+rl-9.9.3-P1.patch

Source60:       dlz-schema.txt
%if %ul_version >= 1
%define VENDOR UL
%else
%if "%{_vendor}" == "suse"
%define VENDOR SUSE
%else
%define VENDOR %_vendor
%endif
%endif
# Defines for user and group add
%define NAMED_UID 44
%define NAMED_UID_NAME named
%define NAMED_GID 44
%define NAMED_GID_NAME named
%define NAMED_COMMENT Name server daemon
%define NAMED_HOMEDIR /var/lib/named
%define NAMED_SHELL /bin/false
%define GROUPADD_NAMED /usr/sbin/groupadd -g %{NAMED_GID} -o -r %{NAMED_GID_NAME} 2> /dev/null || :
%define USERADD_NAMED /usr/sbin/useradd -r -o -g %{NAMED_GID_NAME} -u %{NAMED_UID} -s %{NAMED_SHELL} -c "%{NAMED_COMMENT}" -d %{NAMED_HOMEDIR} %{NAMED_UID_NAME} 2> /dev/null || :
%define USERMOD_NAMED /usr/sbin/usermod -s %{NAMED_SHELL} -d  %{NAMED_HOMEDIR} %{NAMED_UID_NAME} 2>/dev/null || :
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
Berkeley Internet Name Domain (BIND) is an implementation of the Domain
Name System (DNS) protocols and provides an openly redistributable
reference implementation of the major components of the Domain Name
System.  This package includes the components to operate a DNS server.

%package chrootenv
Summary:        Chroot environment for BIND named and lwresd
Group:          Productivity/Networking/DNS/Servers
PreReq:         /usr/sbin/groupadd /usr/sbin/useradd

%description chrootenv
This package contains all directories and files which are common to the
chroot environment of BIND named and lwresd.  Most is part of the
structure below /var/lib/named.

%package devel
Summary:        Development Libraries and Header Files of BIND
Group:          Development/Libraries/C and C++
Requires:       %{name}-libs = %{version}
Provides:       bind8-devel
Provides:       bind9-devel
Obsoletes:      bind8-devel
Obsoletes:      bind9-devel
# bug437293
%ifarch ppc64
Obsoletes:      bind-devel-64bit
%endif
#

%description devel
This package contains the header files, libraries, and documentation
for building programs using the libraries of the Berkeley Internet Name
Domain (BIND) Domain Name System implementation of the Domain Name
System (DNS) protocols.

%package doc
Summary:        BIND documentation
Group:          Documentation/Other
%if 0%{?suse_version} >= 1120
BuildArch:      noarch
%endif

%description doc
Documentation of the Berkeley Internet Name Domain (BIND) Domain Name
System implementation of the Domain Name System (DNS) protocols.  This
includes also the BIND Administrator Reference Manual (ARM).

%package libs
Summary:        Shared libraries of BIND
Group:          Development/Libraries/C and C++
# bug437293
%ifarch ppc64
Obsoletes:      bind-libs-64bit
%endif
#

%description libs
This package contains the shared libraries of the Berkeley Internet
Name Domain (BIND) Domain Name System implementation of the Domain Name
System (DNS) protocols.

%package lwresd
Summary:        Lightweight Resolver Daemon
Group:          Productivity/Networking/DNS/Utilities
Requires:       %{name}-chrootenv
Provides:       dns_daemon
PreReq:         /usr/sbin/groupadd /usr/sbin/useradd
%if %suse_version > 1131
PreReq:         sysvinit(network) sysvinit(syslog)
%endif

%description lwresd
Bind-lwresd provides resolution services to local clients using a
combination of the lightweight resolver library liblwres and the
resolver daemon process lwresd running on the local host.  These
communicate using a simple UDP-based protocol, the "lightweight
resolver protocol" that is distinct from and simpler than the full DNS
protocol.

%package utils
Summary:        Utilities to query and test DNS
Group:          Productivity/Networking/DNS/Utilities
Provides:       bind9-utils
Provides:       bindutil
Provides:       dns_utils
Obsoletes:      bind9-utils
Obsoletes:      bindutil
# bug437293
%ifarch ppc64
Obsoletes:      bind-utils-64bit
%endif
#

%description utils
This package includes the utilities host, dig, and nslookup used to
test and query the Domain Name System (DNS).  The Berkeley Internet
Name Domain (BIND) DNS server is found in the package named bind.

%prep
%if 0%{?suse_version} > 1220
%gpg_verify %{S:3}
%endif
%setup -q -n %{pkg_name}-%{pkg_vers}
#%setup -n %{pkg_name}-%{version} -T -D -a1 -a50
%setup -q -n %{pkg_name}-%{pkg_vers} -T -D -a1
%patch -p1
%patch1 -p1
%patch2 -p0
%patch4 -p0
#%patch50
%if 0%{?suse_version} >= 1000
%patch51
%endif
%patch52
%if 0%{?suse_version} <= 1010
%patch100 -p1
%endif
#%patch110 -p0
#%patch200 -p0
# modify settings of some files regarding to OS version and vendor
function replaceStrings()
{
        file="$1"
        sed -e "s@__NSD__@/lib@g" \
                -e "s@__BIND_PACKAGE_NAME__@%{pkg_name}@g" \
                -e "s@__VENDOR__@%{VENDOR}@g" \
                "${file}" >"${file}.new" && \
                        mv "${file}.new" "${file}"
}
pushd vendor-files
for file in docu/README tools/createNamedConfInclude config/{README,named.conf} init/{named,lwresd} sysconfig/{named-common,named-named,syslog-named}; do
        replaceStrings ${file}
done
popd
#cp bind-sdb-ldap-%{SDB_LDAP_VERSION}/ldapdb.c bin/named/
#cp bind-sdb-ldap-%{SDB_LDAP_VERSION}/ldapdb.h bin/named/include/
# ---------------------------------------------------------------------------

%build
%{?suse_update_config:%{suse_update_config -f}}
cat /usr/share/aclocal/libtool.m4 >> aclocal.m4
%{__libtoolize} -f
%{__aclocal}
%{__autoconf}
#pushd lib/bind
#%{?suse_update_config:%{suse_update_config -f}}
#cat /usr/share/aclocal/libtool.m4 >> aclocal.m4
#%{__libtoolize} -f
#%{__aclocal}
#%{__autoconf}
#popd
#pushd contrib/idn/idnkit-1.0-src
#%{?suse_update_config:%{suse_update_config -f}}
#cat /usr/share/aclocal/libtool.m4 >> aclocal.m4
#%{__libtoolize} -f
#%{__aclocal}
#%{__autoconf}
#popd
export CFLAGS="$RPM_OPT_FLAGS -DNO_VERSION_DATE -fno-strict-aliasing" LDFLAGS="-L%{_libdir}"
#export CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing -DLDAP_DEPRECATED" LDFLAGS="-L%{_libdir}"
#export CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing -fpie" LDFLAGS="-L%{_libdir} -pie"
CONFIGURE_OPTIONS="\
        --prefix=%{_prefix} \
        --bindir=%{_bindir} \
        --sbindir=%{_sbindir} \
        --sysconfdir=%{_sysconfdir} \
        --localstatedir=%{_var} \
        --libdir=%{_libdir} \
        --includedir=%{_includedir}/bind \
        --mandir=%{_mandir} \
        --infodir=%{_infodir} \
        --disable-static \
        --with-openssl \
        --enable-threads \
        --with-gssapi=/usr/include/gssapi \
        --with-libtool \
        --enable-runidn \
        --with-libxml2 \
        --with-dlopen=yes \
        --with-dlz-mysql \
        --with-dlz-bdb \
        --with-dlz-ldap  \
        --enable-filter-aaaa \
        --enable-rrl \
        --with-ecdsa \
        --disable-isc-spnego

"
cp -f -p config.guess config.sub contrib/idn/idnkit-1.0-src/
./configure ${CONFIGURE_OPTIONS}
# disable rpath
sed -i '
  s|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g
  s|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g
' libtool
%{__make} %{?_smp_mflags}
pushd contrib/idn/idnkit-1.0-src
./configure ${CONFIGURE_OPTIONS}
# disable rpath
sed -i '
  s|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g
  s|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g
' libtool
%{__make} %{?_smp_mflags}
popd
# running BIND system tests
# FIXME: enable make test if every test checks for a free port first; fixed port
# 5300 might lead to test failures if port is already in use.
#pushd bin/tests/system/
#./ifconfig.sh up
#%{__make} test
#./ifconfig.sh down
#popd
# replace __NSD__ in some files by a sub directory to set the full path to
# named's root directory
# ---------------------------------------------------------------------------

%install
%{GROUPADD_NAMED}
%{USERADD_NAMED}
mkdir -p \
        ${RPM_BUILD_ROOT}/%{_sysconfdir}/init.d \
        ${RPM_BUILD_ROOT}/%{_sysconfdir}/named.d \
        ${RPM_BUILD_ROOT}/%{_sysconfdir}/openldap/schema \
    ${RPM_BUILD_ROOT}/%{_sysconfdir}/slp.reg.d \
        ${RPM_BUILD_ROOT}/usr/{bin,%{_lib},sbin,include} \
        ${RPM_BUILD_ROOT}/%{_datadir}/bind \
        ${RPM_BUILD_ROOT}/%{_datadir}/susehelp/meta/Administration/System \
        ${RPM_BUILD_ROOT}/%{_defaultdocdir}/bind \
        ${RPM_BUILD_ROOT}/var/lib/named/{etc/named.d,dev,dyn,log,master,slave,var/{lib,run/named}} \
        ${RPM_BUILD_ROOT}%{_mandir}/{man1,man3,man5,man8} \
        ${RPM_BUILD_ROOT}/var/adm/fillup-templates \
        ${RPM_BUILD_ROOT}/var/run \
    ${RPM_BUILD_ROOT}/%{_sysconfdir}/sysconfig/SuSEfirewall2.d/services
%{__make} DESTDIR=${RPM_BUILD_ROOT} install
pushd contrib/idn/idnkit-1.0-src
%{__make} DESTDIR=${RPM_BUILD_ROOT} install
popd
# remove useless .la files
rm -f ${RPM_BUILD_ROOT}/%{_lib}/libidnkit.la
rm -f ${RPM_BUILD_ROOT}/%{_lib}/libidnkitlite.la
rm -f ${RPM_BUILD_ROOT}/%{_libdir}/lib*.{la,a}
mv vendor-files/config/named.conf ${RPM_BUILD_ROOT}/%{_sysconfdir}
mv vendor-files/config/bind.reg ${RPM_BUILD_ROOT}/%{_sysconfdir}/slp.reg.d
mv vendor-files/config/rndc-access.conf ${RPM_BUILD_ROOT}/%{_sysconfdir}/named.d
for file in named.conf.include rndc.key; do
        touch ${RPM_BUILD_ROOT}/%{_sysconfdir}/${file}
done
for file in lwresd named; do
        install -m 0754 vendor-files/init/${file} ${RPM_BUILD_ROOT}/etc/init.d/${file}
        ln -sf /etc/init.d/${file} ${RPM_BUILD_ROOT}/usr/sbin/rc${file}
done
install -m 0644 ${RPM_SOURCE_DIR}/named.root ${RPM_BUILD_ROOT}/var/lib/named/root.hint
mv vendor-files/config/{127.0.0,localhost}.zone ${RPM_BUILD_ROOT}/var/lib/named
install -m 0754 vendor-files/tools/createNamedConfInclude ${RPM_BUILD_ROOT}/%{_datadir}/bind
install -m 0755 vendor-files/tools/bind.genDDNSkey ${RPM_BUILD_ROOT}/%{_bindir}/genDDNSkey
cp -a vendor-files/docu/BIND.desktop ${RPM_BUILD_ROOT}/%{_datadir}/susehelp/meta/Administration/System
cp -p ${RPM_SOURCE_DIR}/dnszone-schema.txt ${RPM_BUILD_ROOT}/%{_sysconfdir}/openldap/schema/dnszone.schema
cp -p "%{S:60}" "${RPM_BUILD_ROOT}/%{_sysconfdir}/openldap/schema/dlz.schema"
install -m 0754 vendor-files/tools/ldapdump ${RPM_BUILD_ROOT}/%{_datadir}/bind
find ${RPM_BUILD_ROOT}/%{_libdir} -type f -name '*.so*' -print0 | xargs -0 chmod 0755
touch ${RPM_BUILD_ROOT}/var/lib/named/etc/{localtime,named.conf.include,named.d/rndc.access.conf}
touch ${RPM_BUILD_ROOT}/var/lib/named/dev/log
ln -s ../.. ${RPM_BUILD_ROOT}/var/lib/named/var/lib/named
ln -s ../log ${RPM_BUILD_ROOT}/var/lib/named/var
ln -s ../lib/named/var/run/named ${RPM_BUILD_ROOT}/var/run
for file in named-common named-named syslog-named; do
        install -m 0644 vendor-files/sysconfig/${file} ${RPM_BUILD_ROOT}/var/adm/fillup-templates/sysconfig.${file}
done
install -m 644 vendor-files/sysconfig/SuSEFirewall.named %{buildroot}/%{_sysconfdir}/sysconfig/SuSEfirewall2.d/services/bind
# Cleanup doc
rm doc/misc/Makefile*
# Remove samples
rm ${RPM_BUILD_ROOT}/etc/*.sample
find doc/arm -type f ! -name '*.html' -print0 | xargs -0 rm -f
# Create doc as we want it in bind and not bind-doc
cp -a vendor-files/docu/README ${RPM_BUILD_ROOT}/%{_defaultdocdir}/bind/README.%{VENDOR}
cp -a vendor-files/docu/dnszonehowto.html contrib/sdb/ldap/
mkdir -p vendor-files/config/ISC-examples
cp -a bin/tests/*.conf* vendor-files/config/ISC-examples
for file in CHANGES COPYRIGHT README FAQ version contrib doc/{arm,misc} vendor-files/config; do
        basename=$( basename ${file})
        cp -a ${file} ${RPM_BUILD_ROOT}/%{_defaultdocdir}/bind/${basename}
        echo "%doc %{_defaultdocdir}/bind/${basename}" >>filelist-bind-doc
done
pushd ${RPM_BUILD_ROOT}%{_defaultdocdir}/bind/contrib/idn/idnkit-1.0-src
%{__make} distclean
rm -rf include lib man map patch tools win wsock Makefile.in acconfig.h aclocal.m4 config.* configure* install-sh ltconfig make.wnt mkinstalldirs
popd
# ---------------------------------------------------------------------------

%pre
# Are we updating from a package named bind9?
if test -d usr/share/doc/packages/bind9 && sbin/chkconfig -c named; then
        NAMED_ACTIVE_FILE="var/adm/named.was.active"
        test -f ${NAMED_ACTIVE_FILE} && old ${NAMED_ACTIVE_FILE}
        ACTIVE_DIR=$( dirname ${NAMED_ACTIVE_FILE})
        test -d ${ACTIVE_DIR} || mkdir -p ${ACTIVE_DIR}
        touch ${NAMED_ACTIVE_FILE}
fi
%{GROUPADD_NAMED}
%{USERADD_NAMED}
# Might be an update.
%{USERMOD_NAMED}
# var/run/named is now a sym link pointing to the chroot jail
test -L var/run/named || rm -rf var/run/named
test -f etc/sysconfig/named && \
        . etc/sysconfig/named
# Store NAMED_RUN_CHROOTED setting to a temp file.
TEMP_SYSCONFIG_FILE="var/adm/named-chroot"
TEMP_DIR=$( dirname ${TEMP_SYSCONFIG_FILE})
test -d ${TEMP_DIR} || \
        mkdir -p ${TEMP_DIR}
test -e ${TEMP_SYSCONFIG_FILE} && \
        old ${TEMP_SYSCONFIG_FILE}
echo "NAMED_RUN_CHROOTED=\"${NAMED_RUN_CHROOTED}\"" >${TEMP_SYSCONFIG_FILE}

%preun
%stop_on_removal named

%post
%{fillup_and_insserv -nf named}
%{fillup_only -nsa named named}
if [ ! -f etc/rndc.key ]; then
        usr/sbin/rndc-confgen -a -b 512 -r dev/urandom
        chmod 0640 etc/rndc.key
        chown root:named etc/rndc.key
fi
TEMP_SYSCONFIG_FILE="var/adm/named-chroot"
# Are we in update mode?
if [ ${FIRST_ARG:-0} -gt 1 ]; then
# Is named.conf an old, /var/named configuration?
if [ -f etc/named.conf ] && grep -qi '^[[:space:]]*directory[[:space:]]*"/var/named"[[:space:]]*;' etc/named.conf; then
        test -d var/log || \
                mkdir -p var/log
        CONVLOG="/var/log/named-move-to-var-lib"
        # move zone files to new location
        echo "Moving zone files to new location /var/lib/named" | tee ${CONVLOG}
        IFS="
"
        for dir in var/named var/named/slave; do
                for source in $( find ${dir} -maxdepth 1 ); do
                        case "${source#var/named/}" in
                                localhost.zone|127.0.0.zone|root.hint|slave|var/named) continue ;;
                        esac
                        sourcedir=$( echo "${source%/*}")
                        destdir=$( echo "${sourcedir#var/named}")
                        if [ -e "var/lib/named/${destdir}/${source##*/}" ]; then
                                echo "Warning: /var/lib/named${destdir}/${source##*/} already exists; skipped." | tee -a ${CONVLOG}
                        else
                                echo "${source#var/named/}" | tee -a ${CONVLOG}
                                mv "${source}" "var/lib/named/${destdir}"
                        fi
                done
        done
        # updating named.conf
        echo -n "Backup old /etc/named.conf to " | tee -a ${CONVLOG}
        oldconfig=$( old etc/named.conf) 2>/dev/null
        oldconfig=${oldconfig##*/}
        echo -en "/etc/${oldconfig}. Conversion " | tee -a ${CONVLOG}
        sed -e "s@\"/var/named\"@\"/var/lib/named\"@" "etc/${oldconfig}" > etc/named.conf 2>/dev/null
        conv_rc=$?
        if [ ${conv_rc} -eq 0 ]; then
                echo "succeded." | tee -a ${CONVLOG}
                chmod --reference="etc/${oldconfig}" etc/named.conf
                chown --reference="etc/${oldconfig}" etc/named.conf
        else
                echo "failed." | tee -a ${CONVLOG}
        fi
        if [ ${conv_rc} -eq 0 ]; then
                cat << EOF >>${CONVLOG}
Result: named.conf conversion succeded.  For details check the following
diff of the the old and new configuration.
Ergebnis: Die named.conf-Konvertierung war erfolgreich. Details finden
Sie in der nachfolgenden Differenz der alten und neuen Konfiguration.
EOF
                diff -u etc/${oldconfig} etc/named.conf >>${CONVLOG}
        else
                cat << EOF >>${CONVLOG}
Result: Conversion failed. You must check your /etc/named.conf
Ergebnis: Die Konvertierung ist fehlgeschlagen. Sie müssen Ihre
/etc/named.conf überprüfen.
EOF
        fi
else
        rm -f var/lib/update-messages/bind.1
fi # End of 'Is named.conf an old, /var/named configuration?'.
# Add include files to NAMED_CONF_INCLUDE_FILES if we have already a include
# file (SL Standard Server 8) and NAMED_RUN_CHROOTED from the
# TEMP_SYSCONFIG_FILE is empty.
if [ -f ${TEMP_SYSCONFIG_FILE} ]; then
        . ${TEMP_SYSCONFIG_FILE}
fi
if [ -s etc/named.conf.include -a -z "${NAMED_RUN_CHROOTED}" ]; then
        test -f etc/sysconfig/named && . etc/sysconfig/named
        if [ "${NAMED_INITIALIZE_SCRIPTS}" = "createNamedConfInclude" -a \
                -z "${NAMED_CONF_INCLUDE_FILES}" ]; then
                # Get the included files from an existing meta include file.
                INCLUDE_LINES=$( grep -e '^[[:space:]]*include' etc/named.conf.include | cut -f 2 -d '"')
                if [ "${INCLUDE_LINES}" -a -z "${NAMED_CONF_INCLUDE_FILES}" ]; then
                        for file in ${INCLUDE_LINES}; do
                                # don't add a file a second time
                                echo "${INCLUDE_FILES}" | grep -qe "\<${file#/etc/named.d/}\>" && continue
                                # don't add the meta include file as the init script copy it anyway
                                # to the chroot jail
                                test "${file}" = "/etc/named.conf.include" && continue
                                test "${INCLUDE_FILES}" && INCLUDE_FILES="${INCLUDE_FILES} "
                                # strip off any leading /etc/named.d/ as the init script takes care
                                # of relative file names
                                INCLUDE_FILES="${INCLUDE_FILES}${file#/etc/named.d/}"
                        done
                        TMPFILE=$( mktemp /var/tmp/named.sysconfig.XXXXXX)
                        if [ $? -ne 0 ]; then
                                echo -e "Can't create temp file. Please add your included files from /etc/named.conf to\nNAMED_CONF_INCLUDE_FILES of /etc/sysconfig/named manually."
                                return
                        fi
                        chmod --reference=etc/sysconfig/named ${TMPFILE}
                        if sed "s+^NAMED_CONF_INCLUDE_FILES.*$+NAMED_CONF_INCLUDE_FILES=\"${INCLUDE_FILES}\"+" etc/sysconfig/named > "${TMPFILE}"; then
                                mv "${TMPFILE}" etc/sysconfig/named
                        else
                                echo "Can't set NAMED_CONF_INCLUDE_FILES of /etc/sysconfig/named to \"${INCLUDE_FILES}\"."
                        fi
                fi
        fi
else
        rm -f touch var/lib/update-messages/bind.3
fi # End of 'Add include files to NAMED_CONF_INCLUDE_FILES'
fi # End of 'Are we in update mode?'
# Remove TEMP_SYSCONFIG_FILE in any case.
rm -f ${TEMP_SYSCONFIG_FILE}
NAMED_ACTIVE_FILE="var/adm/named.was.active"
if [ -f ${NAMED_ACTIVE_FILE} ]; then
        sbin/insserv named
        test ! -s ${NAMED_ACTIVE_FILE} && rm -f ${NAMED_ACTIVE_FILE}
fi

%postun
%restart_on_update named
%insserv_cleanup

%pre chrootenv
%{GROUPADD_NAMED}
%{USERADD_NAMED}

%post chrootenv
%{fillup_only -nsa named common}
%{fillup_only -nsa syslog named}

%pre lwresd
%{GROUPADD_NAMED}
%{USERADD_NAMED}

%post lwresd
# Create a key if usr/sbin/rndc-confgen is installed.
if [ -x usr/sbin/rndc-confgen -a ! -f etc/rndc.key ]; then
        usr/sbin/rndc-confgen -a -b 512 -r dev/urandom
        chmod 0640 etc/rndc.key
        chown root:named etc/rndc.key
fi
# delete an emtpy lwresd.conf file
if [ ! -s etc/lwresd.conf ]; then
    rm -f etc/lwresd.conf
fi
if [ $1 -le 1 ]; then
    %{fillup_and_insserv -fy lwresd}
fi;

%preun lwresd
%stop_on_removal lwresd

%postun lwresd
%restart_on_update lwresd
%insserv_cleanup

%post utils
/sbin/ldconfig
# Create a key if lwresd is installed.
if [ -x usr/sbin/lwresd -a ! -f etc/rndc.key ]; then
        usr/sbin/rndc-confgen -a -b 512 -r dev/urandom
        chmod 0640 etc/rndc.key
        chown root:named etc/rndc.key
fi
# ---------------------------------------------------------------------------

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%files
%defattr(-,root,root)
%attr(0644,root,named) %config(noreplace) /%{_sysconfdir}/named.conf
%dir %{_sysconfdir}/slp.reg.d
%attr(0644,root,root) /%{_sysconfdir}/slp.reg.d/bind.reg
%attr(0644,root,named) %ghost /%{_sysconfdir}/named.conf.include
%attr(0640,root,named) %ghost %config(noreplace) /%{_sysconfdir}/rndc.key
%config /%{_sysconfdir}/init.d/named
%{_sbindir}/rcnamed
%{_sbindir}/named
%{_sbindir}/named-checkconf
%{_sbindir}/named-checkzone
%{_sbindir}/named-compilezone
%doc %{_mandir}/man5/named.conf.5.gz
%doc %{_mandir}/man8/named-checkconf.8.gz
%doc %{_mandir}/man8/named-checkzone.8.gz
%doc %{_mandir}/man8/named.8.gz
%doc %{_mandir}/man8/named-compilezone.8.gz
%dir %{_datadir}/bind
%{_datadir}/bind/createNamedConfInclude
%{_datadir}/bind/ldapdump
%{_var}/adm/fillup-templates/sysconfig.named-named
%dir %{_var}/lib/named/master
%attr(-,named,named) %dir %{_var}/lib/named/dyn
%attr(-,named,named) %dir %{_var}/lib/named/slave
%config %{_var}/lib/named/root.hint
%config %{_var}/lib/named/127.0.0.zone
%config %{_var}/lib/named/localhost.zone
%ghost %{_var}/lib/named/etc/localtime
%attr(0644,root,named) %ghost %{_var}/lib/named/etc/named.conf.include
%{_sysconfdir}/sysconfig/SuSEfirewall2.d/services/bind

%files chrootenv
%defattr(-,root,root)
%dir %{_var}/lib/named
%dir %{_var}/lib/named/etc
%dir %{_var}/lib/named/etc/named.d
%dir %{_var}/lib/named/dev
%dir %{_var}/lib/named/var
%dir %{_var}/lib/named/var/lib
%dir %{_var}/lib/named/var/run
%attr(-,named,named) %dir %{_var}/lib/named/log
%attr(-,named,named) %dir %{_var}/lib/named/var/run/named
%ghost %{_var}/lib/named/etc/named.d/rndc.access.conf
%ghost %{_var}/lib/named/dev/log
%attr(0666, root, root) %dev(c, 1, 3) %{_var}/lib/named/dev/null
%attr(0666, root, root) %dev(c, 1, 8) %{_var}/lib/named/dev/random
%{_var}/lib/named/var/lib/named
%{_var}/lib/named/var/log
%ghost %{_var}/run/named
%{_var}/adm/fillup-templates/sysconfig.named-common
%{_var}/adm/fillup-templates/sysconfig.syslog-named

%files devel
%defattr(-,root,root)
%{_bindir}/isc-config.sh
#%{_libdir}/*.a
%{_libdir}/*.so
#%{_libdir}/libbind.la
#%{_libdir}/libbind9.la
#%{_libdir}/libdns.la
#%{_libdir}/libidnkit.la
#%{_libdir}/libidnkitlite.la
#%{_libdir}/libisc.la
#%{_libdir}/libisccc.la
#%{_libdir}/libisccfg.la
#%{_libdir}/liblwres.la
%{_includedir}/bind
%doc %{_mandir}/man3/*

%files doc -f filelist-bind-doc
%defattr(-,root,root)
%dir %doc %{_defaultdocdir}/bind
%doc %{_datadir}/susehelp

%files libs
%defattr(-,root,root)
%{_libdir}/*.so.*
#%{_libdir}/libidnkitres.la

%files lwresd
%defattr(-,root,root)
%config /etc/init.d/lwresd
%{_sbindir}/rclwresd
%{_sbindir}/lwresd
%doc %{_mandir}/man8/lwresd.8.gz

%files utils
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/idn.conf
%config(noreplace) %{_sysconfdir}/idnalias.conf
%dir /etc/named.d
%config(noreplace) /etc/named.d/rndc-access.conf
%config(noreplace) /etc/bind.keys
%dir %{_sysconfdir}/openldap
%dir %{_sysconfdir}/openldap/schema
%attr(0444,root,root) %config %{_sysconfdir}/openldap/schema/dnszone.schema
%attr(0444,root,root) %config %{_sysconfdir}/openldap/schema/dlz.schema
%{_bindir}/dig
%{_bindir}/host
%{_bindir}/idnconv
%{_bindir}/nslookup
%{_bindir}/nsupdate
%{_bindir}/genDDNSkey
%{_bindir}/runidn
%{_sbindir}/arpaname
%{_sbindir}/ddns-confgen
%{_sbindir}/dnssec-checkds
%{_sbindir}/dnssec-coverage
%{_sbindir}/dnssec-dsfromkey
%{_sbindir}/dnssec-keyfromlabel
%{_sbindir}/dnssec-keygen
%{_sbindir}/dnssec-revoke
%{_sbindir}/dnssec-settime
%{_sbindir}/dnssec-signzone
%{_sbindir}/dnssec-verify
%{_sbindir}/genrandom
%{_sbindir}/isc-hmac-fixup
%{_sbindir}/named-journalprint
%{_sbindir}/nsec3hash
%{_sbindir}/rndc
%{_sbindir}/rndc-confgen
%dir %{_datadir}/idnkit
%{_datadir}/idnkit/jp.map
%dir %doc %{_defaultdocdir}/bind
%{_defaultdocdir}/bind/README.%{VENDOR}
%doc %{_mandir}/man1/arpaname.1.gz
%doc %{_mandir}/man1/dig.1.gz
%doc %{_mandir}/man1/host.1.gz
%doc %{_mandir}/man1/isc-config.sh.1.gz
%doc %{_mandir}/man1/nslookup.1.gz
%doc %{_mandir}/man1/nsupdate.1.gz
%doc %{_mandir}/man5/rndc.conf.5.gz
%doc %{_mandir}/man8/ddns-confgen.8.gz
%doc %{_mandir}/man8/dnssec-checkds.8.gz
%doc %{_mandir}/man8/dnssec-coverage.8.gz
%doc %{_mandir}/man8/dnssec-dsfromkey.8.gz
%doc %{_mandir}/man8/dnssec-keyfromlabel.8.gz
%doc %{_mandir}/man8/dnssec-keygen.8.gz
%doc %{_mandir}/man8/dnssec-revoke.8.gz
%doc %{_mandir}/man8/dnssec-settime.8.gz
%doc %{_mandir}/man8/dnssec-signzone.8.gz
%doc %{_mandir}/man8/dnssec-verify.8.gz
%doc %{_mandir}/man8/genrandom.8.gz
%doc %{_mandir}/man8/isc-hmac-fixup.8.gz
%doc %{_mandir}/man8/named-journalprint.8.gz
%doc %{_mandir}/man8/nsec3hash.8.gz
%doc %{_mandir}/man8/rndc.8.gz
%doc %{_mandir}/man8/rndc-confgen.8.gz
# idn kit
%doc %{_mandir}/man1/idnconv.1.gz
%doc %{_mandir}/man1/runidn.1.gz
%doc %{_mandir}/man5/idn.conf.5.gz
%doc %{_mandir}/man5/idnalias.conf.5.gz
%doc %{_mandir}/man5/idnrc.5.gz

%changelog

