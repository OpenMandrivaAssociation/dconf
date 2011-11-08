%define major 0
%define dbusapi	1
%define libname %mklibname %name %major
%define develname %mklibname %name -d
%define libdbus %mklibname %{name}-dbus- %dbusapi %major
%define develdbus %mklibname %{name}-dbus -d

%define giolibname %mklibname gio2.0_ 0

Summary: Configuration backend for Glib
Name: dconf
Version: 0.11.0
Release: 1
Source0: http://ftp.gnome.org/pub/GNOME/sources/%name/%{name}-%{version}.tar.xz
License: LGPLv2+
Group: System/Libraries
Url: http://www.gnome.org/

BuildRequires: pkgconfig(dbus-1)
BuildRequires: pkgconfig(gio-2.0)
BuildRequires: pkgconfig(glib-2.0) >= 2.29.90
BuildRequires: pkgconfig(gobject-introspection-1.0)
BuildRequires: pkgconfig(gtk+-3.0)
BuildRequires: pkgconfig(libxml-2.0)
BuildRequires: vala-devel >= 0.9.5

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
Requires(post): %giolibname >= 2.23.4-2
Requires(postun): %giolibname >= 2.23.4-2

%description -n %libname
This is a configuration backend for Glib's GSettings and part of GNOME 3.0.

%package -n %develname
Group: Development/C
Summary: Configuration backend library for Glib - development files
Provides: lib%name-devel = %version-%release
Requires: %libname = %version-%release

%description -n %develname
This is a configuration backend for Glib's GSettings and part of GNOME 3.0.

%package -n %libdbus
Group: System/Libraries
Summary: Configuration backend library for Dbus

%description -n %libdbus
This is a configuration backend for Dbus' GSettings and part of GNOME 3.0.

%package -n %develdbus
Group: Development/C
Summary: Configuration backend library for Dbus - development files
Provides: libdconf-dbus-devel = %version-%release
Requires: %libdbus = %version-%release

%description -n %develdbus
This is a configuration backend for Dbus' GSettings and part of GNOME 3.0.

%prep
%setup -q

%build
%configure2_5x
%make libdconfsettings_so_LDFLAGS="-shared"

%install
rm -rf %{buildroot}
%makeinstall_std

%post -n %{libname}
%if %_lib != lib
 %{_bindir}/gio-querymodules-64 %{_libdir}/gio/modules 
%else
 %{_bindir}/gio-querymodules-32 %{_libdir}/gio/modules
%endif

%postun -n %{libname}
if [ "$1" = "0" ]; then
%if %_lib != lib
 %{_bindir}/gio-querymodules-64 %{_libdir}/gio/modules 
%else
 %{_bindir}/gio-querymodules-32 %{_libdir}/gio/modules
%endif
fi

%files
%doc NEWS
%{_sysconfdir}/bash_completion.d/dconf-bash-completion.sh
%_bindir/dconf
%_libexecdir/dconf-service
%_datadir/dbus-1/services/ca.desrt.dconf.service

%files editor
%_bindir/dconf-editor
%{_datadir}/applications/dconf-editor.desktop
%{_datadir}/dconf-editor/
%{_datadir}/glib-2.0/schemas/ca.desrt.dconf-editor.gschema.xml

%files -n %libname
%_libdir/libdconf.so.%{major}*
%_libdir/gio/modules/libdconfsettings.*

%files -n %develname
%_libdir/libdconf.so
%_libdir/pkgconfig/dconf.pc
%_includedir/dconf/
%_datadir/gtk-doc/html/dconf
%_datadir/vala/vapi/dconf*

%files -n %libdbus
%_libdir/libdconf-dbus-%{dbusapi}.so.%{major}*

%files -n %develdbus
%_includedir/dconf-dbus*/
%_libdir/pkgconfig/dconf-dbus*.pc
%_libdir/libdconf-dbus*.so
