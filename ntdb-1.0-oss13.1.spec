#
# Remsnet  Spec file for package ntdb  (Version 1.00)
#
# Copyright (c) 1995-2008 Remsnet Netzwerk Service OhG , D-73630 Remshalden
# Copyright (c) 2008-2014 Remsnet Consullting & Internet Services LTD , D-40476 Duesseldorf

# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Please submit bugfixes or comments via https://github.com/remsnet/samba-dc-opensuse-RPi


%{!?python_sitearch:  %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

#
Name: ntdb

%if 0%{?suse_version} == 0 || 0%{?suse_version} > 1140
%define build_make_smp_mflags %{?_smp_mflags}
%else
%define build_make_smp_mflags %{?jobs:-j%jobs}
%endif

Version: 1.0
Release: oss13.1
Summary: A not-so trivial database
License: LGPLv3+
Group: System/Libraries
Url: http://ntdb.samba.org/
BuildRequires: autoconf
BuildRequires: docbook-xsl-stylesheets
BuildRequires: libxslt
BuildRequires: pkgconfig
BuildRequires: xsltproc docbook-xsl-stylesheets docbook-dtds

Source: http://samba.org/ftp/%{name}/%{name}-%{version}.tar.gz


%description -n ntdb
This is a simple database API.
If you have previously used the tdb library from Samba, much of
this will seem familiar, but there are some API changes which a
compiler will warn you about if you simply replace 'tdb' with
'ntdb' in your code!  The on-disk format for ntdb is
incompatible with tdb.

%package -n ntdb-devel
Group: Development/C
Summary: Developer tools for the NTDB library
Requires: %name

%description -n ntdb-devel
This is a simple database API.
If you have previously used the tdb library from Samba, much of
this will seem familiar, but there are some API changes which a
compiler will warn you about if you simply replace 'tdb' with
'ntdb' in your code!  The on-disk format for ntdb is
incompatible with tdb.

These are the development files.

%package -n ntdb-utils
Group: Development/Tools
Summary: A not-so trivial database utils
Requires: %name

%description -n ntdb-utils
This is a simple database API.
If you have previously used the tdb library from Samba, much of
this will seem familiar, but there are some API changes which a
compiler will warn you about if you simply replace 'tdb' with
'ntdb' in your code!  The on-disk format for ntdb is
incompatible with tdb.

This package contains some utils for managing ntdb databases

%package -n pyntdb
Group: Development/Python
Summary: Python bindings for the NTDB library
Requires: %name

%description -n pyntdb
Python bindings for the NTDB library


#%package -n pyntdb-devel
#Summary:        Development files for the Python bindings for the NTDB library
#Group:          Development/Libraries/Python
#Requires:       pyntdb = %{version}

#%description -n pyntdb-devel
#This package contains the development files for the Python bindings for the
#NTDB library.



%prep
%setup -q

%build
%if 0%{?suse_version} && 0%{?suse_version} < 911
        OPTIMIZATION="-O"
%else
        # use the default optimization
        unset OPTIMIZATION
%endif
export CFLAGS="${RPM_OPT_FLAGS} -D_GNU_SOURCE ${OPTIMIZATION} -D_LARGEFILE64_SOURCE -DIDMAP_RID_SUPPORT_TRUSTED_DOMAINS"
CONFIGURE_OPTIONS="\
        --prefix=%{_prefix} \
        --libdir=%{_libdir} \
        --bundled-libraries=ALL \
"
%configure ${CONFIGURE_OPTIONS}

%{__make} %{build_make_smp_mflags}  all


%install
DESTDIR=${RPM_BUILD_ROOT} make install


%post -n ntdb -p /sbin/ldconfig

%postun -n ntdb -p /sbin/ldconfig


%post -n pyntdb -p /sbin/ldconfig

%postun -n pyntdb -p /sbin/ldconfig


%files -n ntdb
%defattr(-,root,root,-)
%{_libdir}/libntdb.so
%{_libdir}/libntdb.so.1
%{_libdir}/libntdb.so.1.0

%files -n ntdb-devel
%defattr(-,root,root,-)
%_includedir/ntdb.h
%{_libdir}/pkgconfig/ntdb.pc

%files -n ntdb-utils
%defattr(-,root,root)
%_bindir/ntdbtool
%_bindir/ntdbdump
%_bindir/ntdbrestore
%_bindir/ntdbbackup
%{_mandir}/man3/ntdb*
%{_mandir}/man8/ntdbtool*
%{_mandir}/man8/ntdbdump*
%{_mandir}/man8/ntdbrestore*
%{_mandir}/man8/ntdbbackup*

%files -n pyntdb
%{python_sitearch}/ntdb.so

#%files -n pyntdb-deveL
#%{_includedir}/py*.h
#%{_libdir}/libpyntdb-util.so
##%{_libdir}/pkgconfig/pyntdb-util.pc

%doc LICENSE %doc doc/*.txt

%changelog
* Sat Dec 28 2013 - Horst venzke - info@remsnet.de - 1.0 _b
- replaced makebuild with __make macro
- replaced makeinstall_std with DESTDIR=${RPM_BUILD_ROOT} make install
- read-added %_libdir/*.a for devel files - samba build requirement
- fiddel OpenSuSE style configure in from tdb-1.2.12.spec
* Sat Dec 28 2013 - Horst venzke - info@remsnet.de - 1.0 _a
- initial samba NTDB 1.0 build for  OpenSuSE 13.1 RPi
