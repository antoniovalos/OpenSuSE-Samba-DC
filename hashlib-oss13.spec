#
# Remsnet  Spec file for package Python-hashlib  (Version 1.00)
#
# Copyright (c) 1995-2008 Remsnet Netzwerk Service OhG , D-73630 Remshalden
# Copyright (c) 2008-2014 Remsnet Consullting & Internet Services LTD , D-40476 Duesseldorf

# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Please submit bugfixes or comments via https://github.com/remsnet/samba-dc-opensuse-RPi


%define python_sitearch %(%{__python} -c 'from distutils import sysconfig; print sysconfig.get_python_lib(1)')

%define real_name hashlib

Summary: Secure hash and message digest algorithm library
Name: python-hashlib
Version: 20081119
Release: oss13.1
License: Python
Group: Development/Libraries
URL: http://code.krypto.org/python/hashlib/

Source: http://code.krypto.org/python/hashlib/hashlib-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires: openssl-devel
BuildRequires: python-devel
BuildRequires: dos2unix
BuildRequires: docbook-xsl-stylesheets
BuildRequires: libxslt
BuildRequires: pkgconfig
BuildRequires: xsltproc docbook-xsl-stylesheets docbook-dtds


%description
This is a stand alone packaging of the hashlib library introduced in
Python 2.5 so that it can be used on older versions of Python.

%prep
%setup -n %{real_name}-%{version}

dos2unix ChangeLog README.txt

%build
CFLAGS="%{optflags}" %{__python} setup.py build

%install
%{__rm} -rf %{buildroot}
%{__python} setup.py install -O1 --root="%{buildroot}" --prefix="%{_prefix}"

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%doc ChangeLog README.txt
%{python_sitearch}/_*.so
%{python_sitearch}/%{real_name}.py
%{python_sitearch}/%{real_name}.pyc
%{python_sitearch}/%{real_name}.pyc
%{python_sitearch}/%{real_name}-%{version}-*.egg-info
%ghost %{python_sitearch}/%{real_name}.pyo

%changelog
* Sat Dec 28 2013 - Horst venzke - info@remsnet.de - 1.0 _a
- initial python-hashlib 20081119  build for  OpenSuSE 13.1 RPi
