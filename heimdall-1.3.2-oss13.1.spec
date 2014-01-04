#
# spec file for package heimdall
#
# Copyright (c) 2011 Pascal Bleser <pascal.bleser@opensuse.org>
# Copyright (c) 2011 Malcolm J Lewis <malcolmlewis@opensuse.org>
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

Name:           heimdall
Version:        1.3.2
Release:        0
License:        MIT
Summary:        Samsung Galaxy S Device Firmware Flasher
Url:            https://github.com/Benjamin-Dobell/Heimdall/tree/master/Linux
Group:          Hardware/Mobile
# https://github.com/downloads/Benjamin-Dobell/Heimdall/heimdall-%%{version}.tar.gz
# tar xf Benjamin-Dobell-Heimdall-v1.3.0-0-ged9b08e.tar.gz
# mv Benjamin-Dobell-Heimdall-ed9b08e heimdall-1.3.0
# tar cjf heimdall-1.3.0.tar.bz2 heimdall-1.3.0
Source:         heimdall-%{version}-0-66f1e84.tar.bz2
Source1:        heimdall.desktop
# PATCH-FIX-OPENSUSE heimdall-remove-udev-service-restart.patch malcolmlewis@opensuse.org -- Drop udev service restart from install.
Patch0:         heimdall-remove-udev-service-restart.patch
# PATCH-FIX-OPENSUSE heimdall-totime_t-for-older-qt.patch malcolmlewis@opensuse.org -- Allow building with build with QT < 4.7
Patch1:         heimdall-totime_t-for-older-qt.patch
Source99:       heimdall-rpmlintrc
BuildRequires:  gcc-c++
BuildRequires:  glibc-devel
BuildRequires:  libqt4-devel
BuildRequires:  libtool
BuildRequires:  libusb-1_0-devel >= 1.0.8
BuildRequires:  pkgconfig
BuildRequires:  udev
BuildRequires:  update-desktop-files
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
Heimdall is a cross-platform open-source tool suite used to flash
firmware (aka ROMs) onto Samsung Galaxy S devices.

%package frontend
Summary:        Samsung Galaxy S Device Firmware Flasher
Group:          Hardware/Mobile
Requires:       %{name} = %{version}

%description frontend
Heimdall is a cross-platform open-source tool suite used to flash
firmware (aka ROMs) onto Samsung Galaxy S devices.

This package contains a graphical user interface for %{name}.

%debug_package
%prep
%setup -q -n heimdall-1.3.2-0-66f1e84
%patch0
%if 0%{?suse_version} <= 1130
%patch1
%endif

sed -i -e 's/\r$//' Linux/README

%build
pushd libpit
%configure
make %{?_smp_flags}
popd #libpit

pushd heimdall
%configure
make %{?_smp_flags}
popd #heimdall

pushd heimdall-frontend
qmake OUTPUTDIR="%{_bindir}" QMAKE_CXXFLAGS="%{optflags}"
make %{?_smp_flags}
popd #heimdall-frontend

%install
pushd heimdall
%makeinstall
popd #heimdall

pushd heimdall-frontend
make INSTALL_ROOT=%{buildroot} install
popd #heimdall

install -D -m0644 "%{SOURCE1}" "%{buildroot}%{_datadir}/applications/%{name}.desktop"
%suse_update_desktop_file -r "%{name}" HardwareSettings Settings

%clean
%{?buildroot:rm -rf %{buildroot}}

%files
%defattr(-,root,root)
%doc Linux/README
%config /lib/udev/rules.d/60-heimdall-galaxy-s.rules
%{_bindir}/heimdall

%files frontend
%defattr(-,root,root)
%doc Linux/README
%{_bindir}/heimdall-frontend
%{_datadir}/applications/%{name}.desktop

%changelog

