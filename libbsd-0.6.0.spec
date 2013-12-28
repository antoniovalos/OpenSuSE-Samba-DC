#
# spec file for package libbsd
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


Name:           libbsd
%define lname   libbsd0
Version:        0.6.0
Release:        0
Summary:        Provides useful functions commonly found on BSD systems
License:        BSD-3-Clause
Group:          System Environment/Libraries
Url:            http://libbsd.freedesktop.org/

#Git-Clone:     git://anongit.freedesktop.org/git/libbsd
#Git-Web:       http://cgit.freedesktop.org/libbsd/
Source:         http://libbsd.freedesktop.org/releases/%name-%version.tar.xz
BuildRequires:  pkgconfig
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
This library provides useful functions commonly found on BSD systems, and lacking on others like GNU systems, thus making it easier to port projects with strong BSD origins, without needing to embed the same code over and over again on each project.

%package -n %lname
Summary:        Provides useful functions commonly found on BSD systems
Group:          Development/Libraries

%description -n %lname
This library provides useful functions commonly found on BSD systems, and lacking on others like GNU systems, thus making it easier to port projects with strong BSD origins, without needing to embed the same code over and over again on each project.

%package devel
Summary:        Development headers and files for libbsd
Group:          Development/Libraries
Requires:       %lname = %{version}
Provides:       %lname-devel-static = %{version}
Requires:       glibc-devel

%description devel
This library provides useful functions commonly found on BSD systems, and lacking on others like GNU systems, thus making it easier to port projects with strong BSD origins, without needing to embed the same code over and over again on each project.

%prep
%setup -q

%build
%configure --disable-static --with-pic
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}
rm -f "%buildroot/%_libdir"/*.la

%post -n %lname -p /sbin/ldconfig

%postun -n %lname -p /sbin/ldconfig

%files -n %lname
%defattr(-, root, root)
%{_libdir}/libbsd.so.0*

%files devel
%defattr(-,root,root)
%doc ChangeLog
%{_includedir}/bsd
%{_libdir}/libbsd.so
%{_libdir}/libbsd*.a
%{_mandir}/man3/*
%{_libdir}/pkgconfig/*.pc

%changelog
