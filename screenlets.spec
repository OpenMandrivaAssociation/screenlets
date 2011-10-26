Name: screenlets
Version: 0.1.5
Release: 1
License: GPLv2
URL: http://www.screenlets.org/
Summary: Widget mini-apps (like OSX Dashboard or Vista Gadgets)
Group: System/X11
# https://code.launchpad.net/screenlets/trunk
Source0: %name-%version.tar.bz2
Patch0: fix-dotdesktop.patch
Source1: logo24.png
BuildRequires: python-devel
BuildRequires: desktop-file-utils
Buildarch: noarch
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
%setup -q
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

echo "Icon=%{_datadir}/%{name}/logo24.png" >>desktop-menu/%{name}-daemon.desktop
desktop-file-install \
  --vendor="" \
  --add-category="Settings" \
  --add-category="DesktopSettings" \
  --add-category="X-MandrivaLinux-CrossDesktop" \
  --dir %{buildroot}%{_datadir}/applications \
  desktop-menu/%{name}-daemon.desktop

%find_lang %name %name %name-manager

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

%files -f %name.lang
%defattr(-, root, root, 0755)
%doc CHANGELOG README TODO
%{_bindir}/*
%{_datadir}/applications/%{name}-*.desktop
%{_datadir}/%{name}
%{_datadir}/%{name}-manager
%{_iconsdir}/%{name}.svg
%{_iconsdir}/hicolor/scalable/apps/*svg
%{_iconsdir}/ubuntu-mono-*/apps/24/*svg
%{py_puresitedir}/screenlets/*
