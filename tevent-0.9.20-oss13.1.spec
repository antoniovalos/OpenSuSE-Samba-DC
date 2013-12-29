#
# spec file for package samba-dc tevent (Version 2.1.0)
#
# Copyright (c) 2012 SUSE LINUX Products GmbH, Nuernberg, Germany.
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

# norootforbuild

%{!?python_sitelib:  %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch:  %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

%define talloc_version 2.1.0


Name:           tevent
BuildRequires:  doxygen
#!BuildIgnore: libtalloc
BuildRequires:  libtalloc-devel >= %{talloc_version}
%if 0%{?suse_version} > 1020
BuildRequires:  pkg-config
%else
BuildRequires:  pkgconfig
%endif
BuildRequires:  python-devel
BuildRequires:  pytalloc-devel >= %{talloc_version}
%if 0%{?suse_version} == 0 || 0%{?suse_version} > 1140
%define build_make_smp_mflags %{?_smp_mflags}
%else
%define build_make_smp_mflags %{?jobs:-j%jobs}
%endif
License:        LGPL-3.0+
Group:          System/Libraries
Url:            http://tevent.samba.org/
Version:        0.9.20
Release:        oss13.1
Summary:        An event system based on the talloc memory management library
Source:         http://download.samba.org/pub/tevent/tevent-%{version}.tar.gz
Source4:        baselibs.conf
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
Tevent is an event system based on the talloc memory management library. It
is the core event system used in Samba.

The low level tevent has support for many event types, including timers,
signals, and the classic file descriptor events.

Tevent also provide helpers to deal with asynchronous code providing the
tevent_req (tevent request) functions.


%define libtevent_name libtevent0
%package -n %{libtevent_name}
License:        LGPL-3.0+
Group:          System/Libraries
PreReq:         /sbin/ldconfig
Summary:        Samba tevent Library

%description -n %{libtevent_name}
Tevent is an event system based on the talloc memory management library. It
is the core event system used in Samba.

The low level tevent has support for many event types, including timers,
signals, and the classic file descriptor events.

This package contains the tevent0 library.


%package -n libtevent-devel
License:        LGPL-3.0+
Summary:        Libraries and Header Files to Develop Programs with tevent0 Support
Group:          Development/Libraries/C and C++
Requires:       %{libtevent_name} = %{version}
Requires:       libtalloc-devel >= %{talloc_version}
%if 0%{?suse_version} > 1020
Requires:       pkg-config
%else
Requires:       pkgconfig
%endif

%description -n libtevent-devel
Tevent is an event system based on the talloc memory management library. It
is the core event system used in Samba.

The low level tevent has support for many event types, including timers,
signals, and the classic file descriptor events.

Tevent also provide helpers to deal with asynchronous code providing the
tevent_req (tevent request) functions.

This package contains libraries and header files need for development.


%package -n python-tevent
License:        LGPL-3.0+
Summary:        Python bindings for the Tevent library
Group:          Development/Libraries/Python
Requires:       %{libtevent_name} = %{version}

%description -n python-tevent
This package contains the python bindings for the Tevent library.

%prep
%setup -n tevent-%{version} -q

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
        --bundled-libraries=NONE \
        --builtin-libraries=replace \
"
./configure ${CONFIGURE_OPTIONS}
%{__make} %{build_make_smp_mflags} \
        all

%check
%{__make} test

%install
DESTDIR=${RPM_BUILD_ROOT} make install
# Shared libraries need to be marked executable for rpmbuild to strip them and
# include them in debuginfo
find ${RPM_BUILD_ROOT} -name "*.so*" -exec chmod -c +x {} \;

%post -n %{libtevent_name} -p /sbin/ldconfig

%postun -n %{libtevent_name} -p /sbin/ldconfig

%post -n python-tevent -p /sbin/ldconfig

%postun -n python-tevent -p /sbin/ldconfig

%files -n %{libtevent_name}
%defattr(-,root,root)
%{_libdir}/libtevent.so.*

%files -n libtevent-devel
%defattr(-,root,root)
%{_includedir}/tevent.h
%{_libdir}/libtevent.so
%{_libdir}/pkgconfig/tevent.pc

%files -n python-tevent
%defattr(-,root,root)
%attr(0755,root,root) %{python_sitelib}/tevent.py*
%{python_sitearch}/_tevent.so

%changelog
