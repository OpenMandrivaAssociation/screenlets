Name:		screenlets
Version:	0.1.6
Release:	1
License:	GPLv2
Url:		https://www.screenlets.org/
Summary:	Widget mini-apps (like OSX Dashboard or Vista Gadgets)
Group:		System/X11
# https://code.launchpad.net/screenlets/trunk
Source0:	%{name}-%{version}.tar.bz2
Patch0:		fix-dotdesktop.patch
Source1:	logo24.png
BuildRequires:	python-devel
BuildRequires:	desktop-file-utils
Buildarch:	noarch
Requires(post,postun):	desktop-file-utils
Requires:	pyxdg
Requires:	dbus-python
Requires:	gnome-python-desktop
Requires:	python-beautifulsoup
Requires:	gnome-python-wnck

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
python setup.py build

%install
python setup.py install --root %{buildroot}

# Remove useless egg-info file
rm -f %{buildroot}%{py_puresitedir}/*.egg-info

# Define prefix
mkdir -p %{buildroot}%{_sysconfdir}/%{name}

echo %{_prefix} > %{buildroot}%{_sysconfdir}/%{name}/prefix

# Icons
install -Dm0644 %{SOURCE1} %{buildroot}%{_datadir}/icons/%{name}.png
install -Dm0644 desktop-menu/screenlets.svg %{buildroot}%{_datadir}/icons/screenlets.svg

desktop-file-install \
  --vendor="" \
  --add-category="Settings" \
  --add-category="DesktopSettings" \
  --add-category="X-MandrivaLinux-CrossDesktop" \
  --dir %{buildroot}%{_datadir}/applications \
  desktop-menu/%{name}-manager.desktop

echo "Icon=%{name}" >> desktop-menu/%{name}-daemon.desktop

desktop-file-install \
  --vendor="" \
  --add-category="Settings" \
  --add-category="DesktopSettings" \
  --add-category="X-MandrivaLinux-CrossDesktop" \
  --dir %{buildroot}%{_datadir}/applications \
  desktop-menu/%{name}-daemon.desktop

%find_lang %{name}

%find_lang %{name}-manager

# Clean Ubuntu icons
rm -rf %{buildroot}%{_datadir}/icons/ubuntu*

%files -f %{name}.lang
%defattr(-, root, root, 0755)
%doc CHANGELOG README TODO
%{_bindir}/*
%{_datadir}/applications/%{name}-*.desktop
%{_datadir}/%{name}
%{_datadir}/%{name}-manager
%{_iconsdir}/%{name}.*
%{_iconsdir}/hicolor/scalable/apps/*svg
%{py_puresitedir}/screenlets/*
%{_sysconfdir}/%{name}/prefix
%{_datadir}/locale/*/LC_MESSAGES/%{name}-manager.mo

