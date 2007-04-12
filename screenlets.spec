%define name screenlets
%define version 0.0.7
%define release %mkrel 1

Name: %name
Version: %version
Release: %release
License: GPL
URL: http://forum.go-compiz.org/viewtopic.php?t=358
Summary: OsX Like Dashboard
Group: System/X11
BuildRoot: %{_tmppath}/%{name}-%{version}-root
Source: %name-%version.tar.bz2
Source1: %name-tray
Source2: logo24.png
Patch0: screenlets-init.patch 
Patch1: setup.py.patch
Patch2: add-screenlet.patch
BuildRequires: python-devel
Requires: python-gnome
Requires: python-gtk
Requires: pyxdg

%description
Screenlets are small owner-drawn applications (written in Python) 
that can be described as "the virtual representation of things 
lying/standing around on your desk". Sticknotes, clocks, rulers, ... 
the possibilities are endless

You need Compiz or Beryl to use screenlets

%prep
%setup -n %{name}-%{version}
%patch0 -p1 -b .usr
%patch1 -p1 -b .patch
%patch2 -p1 -b .patch
%build
%{__python} setup.py build

%install
rm -rf %{buildroot}
%{__python} setup.py install --root %{buildroot}

# Fix a path issue
sed -i "s,/usr/local,%{_prefix}," %{buildroot}%{_bindir}/screenletsd

install -d %{buildroot}%{_bindir}
install -m0755 %{SOURCE1} %{buildroot}%{_bindir}/%{name}-tray

install -d %{buildroot}%{_datadir}/%{name}
install -m0644 %{SOURCE2} %{buildroot}%{_datadir}/%{name}/logo24.png


%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%doc CHANGELOG README TODO
%{_bindir}/screenletsd
%{_bindir}/%{name}-tray
%{_datadir}/%{name}/logo24.png
%py_puresitedir/screenlets-0.0.7-py2.5.egg-info
%py_puresitedir/screenlets/*
%_datadir/screenlets/*



