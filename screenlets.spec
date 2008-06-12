%define name screenlets
%define version 0.0.12
%define release %mkrel 2

Name: %name
Version: %version
Release: %release
License: GPL
URL: http://www.screenlets.org/
Summary: Widget mini-apps (like OSX Dashboard or Vista Gadgets)
Group: System/X11
BuildRoot: %{_tmppath}/%{name}-%{version}-root
Source: %name-%version.tar.gz
Patch0: fix-dotdesktop.patch
Source1: logo24.png
BuildRequires: python-devel
BuildRequires: desktop-file-utils
Requires(post): desktop-file-utils
Requires(postun): desktop-file-utils
Requires: pyxdg
Requires: dbus-python
Requires: gnome-python-desktop

%description
Screenlets are small owner-drawn applications (written in Python) 
that can be described as "the virtual representation of things 
lying/standing around on your desk". Sticknotes, clocks, rulers, ... 
the possibilities are endless

Screenlets work best with the Widget plugin for Compiz Fusion.

%prep
%setup -n %{name}
%patch0 -p0 -b .desktop
# Fix paths
grep -rl '/usr/local' * | xargs sed -i 's,/usr/local,%{_prefix},g'
# Fix dodgy desktop files
find -name *.desktop -exec sed -i 's/^\(Exec=.*\) >.*$/\1/' {} \;

%build
%{__python} setup.py build

%install
rm -rf %{buildroot}
%{__python} setup.py install --root %{buildroot}
# Remove useless egg-info file
rm -f %{buildroot}%{py_puresitedir}/*.egg-info

install -d %{buildroot}%{_datadir}/%{name}
install -m0644 %{SOURCE1} %{buildroot}%{_datadir}/%{name}/logo24.png

install -d %{buildroot}%{_datadir}/icons
install -m0644 desktop-menu/screenlets.svg %{buildroot}%{_datadir}/icons/screenlets.svg

desktop-file-install \
  --vendor="" \
  --add-category="Settings" \
  --add-category="DesktopSettings" \
  --add-category="X-MandrivaLinux-CrossDesktop" \
  --dir %{buildroot}%{_datadir}/applications \
  desktop-menu/%{name}-manager.desktop

echo "Type=Application" >>desktop-menu/%{name}-daemon.desktop
echo "Icon=%{_datadir}/%{name}/logo24.png" >>desktop-menu/%{name}-daemon.desktop
desktop-file-install \
  --vendor="" \
  --add-category="Settings" \
  --add-category="DesktopSettings" \
  --add-category="X-MandrivaLinux-CrossDesktop" \
  --dir %{buildroot}%{_datadir}/applications \
  desktop-menu/%{name}-daemon.desktop


%if %mdkversion < 200900
%post
%update_menus
%{update_desktop_database}
%endif

%if %mdkversion < 200900
%postun
%clean_menus
%{clean_desktop_database}
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%doc CHANGELOG README TODO
%{_bindir}/screenletsd
%{_bindir}/%{name}-manager
%{_bindir}/%{name}-packager
%{_datadir}/applications/%{name}-*.desktop
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/logo24.png
%dir %{_datadir}/%{name}-manager
%{_datadir}/%{name}-manager/noimage.svg
%{_datadir}/%{name}-manager/%{name}-*.py
%{_datadir}/icons/%{name}.svg

%{py_puresitedir}/screenlets/*
%{_datadir}/screenlets/*



