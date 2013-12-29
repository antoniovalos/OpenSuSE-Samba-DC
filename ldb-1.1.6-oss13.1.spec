#
# spec file for package samba-dc ldb
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

#  Please submit bugfixes or comments via https://github.com/remsnet/samba-dc-opensuse-RPi
#


%{!?python_sitearch:  %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

%define talloc_version 2.0.9
%define tdb_version 1.2.11
%define tevent_version 0.9.19

Name:           ldb
%if 0%{?suse_version} > 1220
BuildRequires:  gpg-offline
%endif
BuildRequires:  libtalloc-devel >= %{talloc_version}
BuildRequires:  libtdb-devel >= %{tdb_version}
BuildRequires:  libtevent-devel >= %{tevent_version}
BuildRequires:  popt-devel
BuildRequires:  pytalloc-devel >= %{talloc_version}
BuildRequires:  python-devel
BuildRequires:  python-tdb >= %{tdb_version}
BuildRequires:  python-tevent >= %{tevent_version}
BuildRequires:  openldap2-devel
BuildRequires:  python-ldap
BuildRequires:  pam-devel
BuildRequires:  pkg-config
%if 0%{?suse_version} == 0 || 0%{?suse_version} > 1140
%define build_make_smp_mflags %{?_smp_mflags}
%else
%define build_make_smp_mflags %{?jobs:-j%jobs}
%endif
Url:            http://ldb.samba.org/
Version:        1.1.16
Release:        oss13.1
Summary:        An LDAP-like embedded database
License:        GPL-3.0+
Group:          System/Libraries
Source:         http://download.samba.org/pub/ldb/ldb-%{version}.tar.gz
Source1:        http://download.samba.org/pub/ldb/ldb-%{version}.tar.asc
Source2:        samba-library-distribution-pubkey_13084025.asc
Source4:        baselibs.conf
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
Ldb is an LDAP-like embedded database.


%define libldb_name libldb1
%package -n %{libldb_name}
Summary:        An LDAP-like embedded database
Group:          System/Libraries
%if 0%{?suse_version} > 1020
BuildRequires:  pkg-config
%else
BuildRequires:  pkgconfig
%endif
PreReq:         /sbin/ldconfig

%description -n %{libldb_name}
Ldb is an LDAP-like embedded database.

This package includes the ldb1 library.


%package -n libldb-devel
Summary:        Libraries and Header Files to Develop Programs with ldb1 Support
Group:          Development/Libraries/C and C++
Requires:       %{libldb_name} = %{version}

%description -n libldb-devel
Ldb is an LDAP-like embedded database.

Libraries and Header Files to Develop Programs with ldb1 Support


%package -n ldb-tools
Summary:        Tools to manipulate ldb files
Group:          Development/Libraries/C and C++

%description -n ldb-tools
Tools to manipulate ldb files


%package -n pyldb
Summary:        Python bindings for the LDB library
Group:          Development/Libraries/Python
Requires:       %{libldb_name} = %{version}
PreReq:         /sbin/ldconfig

%description -n pyldb
This package contains the python bindings for the LDB library.


%package -n pyldb-devel
Summary:        Development files for the Python bindings for the LDB library
Group:          Development/Libraries/Python
Requires:       pyldb = %{version}

%description -n pyldb-devel
This package contains the development files for the Python bindings for the
LDB library.


%prep
%if 0%{?suse_version} > 1220
gzip -dc %{SOURCE0} >${RPM_SOURCE_DIR}/%{name}-%{version}.tar
%{?gpg_verify: %gpg_verify --keyring %{SOURCE2} %{SOURCE1}}
rm ${RPM_SOURCE_DIR}/%{name}-%{version}.tar
%endif
%setup -n ldb-%{version} -q

%build
%if 0%{?suse_version} && 0%{?suse_version} < 911
        OPTIMIZATION="-O"
%else
        # use the default optimization
        unset OPTIMIZATION
%endif
%if 0%{?suse_version} > 1110
        export SUSE_ASNEEDED=0
%endif
export CFLAGS="${RPM_OPT_FLAGS} -D_GNU_SOURCE ${OPTIMIZATION} -D_LARGEFILE64_SOURCE -DIDMAP_RID_SUPPORT_TRUSTED_DOMAINS"
CONFIGURE_OPTIONS="\
        --prefix=%{_prefix} \
        --libdir=%{_libdir} \
        --disable-rpath \
        --with-modulesdir=%{_libdir} \
        --bundled-libraries=NONE \
        --builtin-libraries=replace \
"
./configure ${CONFIGURE_OPTIONS}
%{__make} %{build_make_smp_mflags} \
        all

%check
# make test doesn't work with --disable-rpath
#%{__make} test

%install
DESTDIR=${RPM_BUILD_ROOT} make install

%post -n %{libldb_name} -p /sbin/ldconfig

%postun -n %{libldb_name} -p /sbin/ldconfig

%post -n pyldb -p /sbin/ldconfig

%postun -n pyldb -p /sbin/ldconfig

%files -n %{libldb_name}
%defattr(-,root,root)
%{_libdir}/libldb.so.*
%dir %{_libdir}/ldb
%{_libdir}/ldb/asq.so
%{_libdir}/ldb/paged_results.so
%{_libdir}/ldb/paged_searches.so
%{_libdir}/ldb/rdn_name.so
%{_libdir}/ldb/sample.so
%{_libdir}/ldb/server_sort.so
%{_libdir}/ldb/skel.so
%{_libdir}/ldb/tdb.so
%{_mandir}/man3/*.3.gz

%files -n libldb-devel
%defattr(-,root,root)
%{_includedir}/ldb.h
%{_includedir}/ldb_errors.h
%{_includedir}/ldb_handlers.h
%{_includedir}/ldb_module.h
%{_includedir}/ldb_version.h
%{_libdir}/libldb.so
%dir %{_libdir}/ldb
%{_libdir}/ldb/libldb-cmdline.so
%{_libdir}/pkgconfig/ldb.pc

%files -n ldb-tools
%defattr(-,root,root)
%{_bindir}/ldbadd
%{_bindir}/ldbdel
%{_bindir}/ldbedit
%{_bindir}/ldbmodify
%{_bindir}/ldbrename
%{_bindir}/ldbsearch
%{_mandir}/man1/*.1.gz

%files -n pyldb
%defattr(-,root,root,-)
%{python_sitearch}/ldb.so
%{_libdir}/libpyldb-util.so.*

%files -n pyldb-devel
%defattr(-,root,root,-)
%{_includedir}/pyldb.h
%{_libdir}/libpyldb-util.so
%{_libdir}/ldb/ldap.so
%{_libdir}/pkgconfig/pyldb-util.pc


%changelog
