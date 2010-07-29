%define name dconf
%define version 0.4.2
%define release %mkrel 1
%define major 0
%define libname %mklibname %name %major
%define develname %mklibname -d %name

Summary: Configuration backend for Glib
Name: %{name}
Version: %{version}
Release: %{release}
Source0: http://ftp.gnome.org/pub/GNOME/sources/%name/%{name}-%{version}.tar.bz2
License: LGPLv2+
Group: System/Libraries
Url: http://www.gnome.org/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: glib2-devel >= 2.25.10
BuildRequires: gtk+2-devel
BuildRequires: libgee-devel
BuildRequires: gobject-introspection-devel

%description
This is a configuration backend for Glib's GSettings and part of GNOME 3.0.

%package editor
Summary: An editor for the Dconf configuration system
Group: Graphical desktop/GNOME
Requires: %name = %version-%release

%description editor
This is a graphical editor for the Dconf configuration system.

%package -n %libname
Group: System/Libraries
Summary: Configuration backend library for Glib

%description -n %libname
This is a configuration backend for Glib's GSettings and part of GNOME 3.0.

%package -n %develname
Group: Development/C
Summary: Configuration backend library for Glib - development files
Provides: lib%name-devel = %version-%release
Requires: %libname = %version-%release

%description -n %develname
This is a configuration backend for Glib's GSettings and part of GNOME 3.0.

%prep
%setup -q

%build
%configure2_5x
%make

%install
rm -rf %{buildroot}
%makeinstall_std

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc NEWS
%_bindir/dconf
%_libexecdir/dconf-service
%_libdir/gio/modules/libdconfsettings.*
%_datadir/dbus-1/services/ca.desrt.dconf.service
%_datadir/dbus-1/system-services/ca.desrt.dconf.service

%files editor
%defattr(-,root,root)
%_bindir/dconf-editor

%files -n %libname
%defattr(-,root,root)
%_libdir/libdconf.so.%{major}*
%_libdir/girepository-1.0/dconf-0.3.typelib

%files -n %develname
%defattr(-,root,root)
%_libdir/libdconf.so
%_libdir/libdconf.*a
%_libdir/pkgconfig/dconf.pc
%_includedir/dconf
%_datadir/gir-1.0/dconf-0.3.gir
%_datadir/gtk-doc/html/dconf
