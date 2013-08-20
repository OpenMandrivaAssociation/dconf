%define url_ver %(echo %{version} | cut -d. -f1,2)

%define major 1
%define dbusapi 1
%define dbusmaj 0
%define libname %mklibname %{name} %{major}
%define devname %mklibname %{name} -d
%define libdbus %mklibname %{name}-dbus- %{dbusapi} %{dbusmaj}
%define devdbus %mklibname %{name}-dbus -d

%define giolibname %mklibname gio2.0_ 0

Summary:	Configuration backend for Glib
Name:		dconf
Version:	0.14.1
Release:	3
License:	LGPLv2+
Group:		System/Libraries
Url:		http://www.gnome.org/
Source0:	http://ftp.gnome.org/pub/GNOME/sources/dconf/%{url_ver}/%{name}-%{version}.tar.xz

BuildRequires:	gtk-doc
BuildRequires:	intltool
BuildRequires:	xsltproc
BuildRequires:	vala-devel
BuildRequires:	pkgconfig(dbus-1)
BuildRequires:	pkgconfig(gio-2.0)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(libxml-2.0)
Requires(post,postun):	gio2.0
Requires(post,postun):	%{giolibname} >= 2.23.4-2

%description
This is a configuration backend for Glib's GSettings and part of GNOME 3.0.

%package	editor
Summary:	An editor for the Dconf configuration system
Group:		Graphical desktop/GNOME
Requires:	%{name} = %{version}-%{release}

%description	editor
This is a graphical editor for the Dconf configuration system.

%package -n	%{libname}
Summary:	Configuration backend library for Glib
Group:		System/Libraries

# this is b/c of the gio modules
Obsoletes:	%{_lib}dconf0 < %{version}


%description -n	%{libname}
This is a configuration backend for Glib's GSettings and part of GNOME 3.0.

%package -n	%{devname}
Summary:	Configuration backend library for Glib - development files
Group:		Development/C
Provides:	%{name}-devel = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}

%description -n	%{devname}
This is a configuration backend for Glib's GSettings and part of GNOME 3.0.

%package -n	%{libdbus}
Summary:	Configuration backend library for Dbus
Group:		System/Libraries

%description -n	%{libdbus}
This is a configuration backend for Dbus' GSettings and part of GNOME 3.0.

%package -n	%{devdbus}
Summary:	Configuration backend library for Dbus - development files
Group:		Development/C
Provides:	dconf-dbus-devel = %{version}-%{release}
Requires:	%{libdbus} = %{version}-%{release}

%description -n	%{devdbus}
This is a configuration backend for Dbus' GSettings and part of GNOME 3.0.

%prep
%setup -q

%build
%configure2_5x
%make libdconfsettings_so_LDFLAGS="-shared"

%install
%makeinstall_std

%find_lang %{name}

%post
%if %{_lib} != lib
 %{_bindir}/gio-querymodules-64 %{_libdir}/gio/modules 
%else
 %{_bindir}/gio-querymodules-32 %{_libdir}/gio/modules
%endif

%postun
if [ "$1" = "0" ]; then
%if %{_lib} != lib
 %{_bindir}/gio-querymodules-64 %{_libdir}/gio/modules 
%else
 %{_bindir}/gio-querymodules-32 %{_libdir}/gio/modules
%endif
fi

%files -f %{name}.lang
%doc NEWS
%{_bindir}/dconf
%{_libexecdir}/dconf-service
%{_datadir}/dbus-1/services/ca.desrt.dconf.service
%{_datadir}/bash-completion/completions/dconf
%{_mandir}/man1/dconf.1*
%{_mandir}/man1/dconf-service.1*

%files editor
%{_bindir}/dconf-editor
%{_datadir}/applications/dconf-editor.desktop
%{_datadir}/dconf-editor/
%{_datadir}/glib-2.0/schemas/ca.desrt.dconf-editor.gschema.xml
%{_iconsdir}/hicolor/*/apps/dconf-editor.png
%{_mandir}/man1/dconf-editor.1*

%files -n %{libname}
%{_libdir}/libdconf.so.%{major}*
%{_libdir}/gio/modules/libdconfsettings.*

%files -n %{devname}
%{_libdir}/libdconf.so
%{_libdir}/pkgconfig/dconf.pc
%{_includedir}/dconf/
%{_datadir}/gtk-doc/html/dconf
%{_datadir}/vala/vapi/dconf*
%{_mandir}/man7/dconf.7*

%files -n %{libdbus}
%{_libdir}/libdconf-dbus-%{dbusapi}.so.%{dbusmaj}*

%files -n %{devdbus}
%{_includedir}/dconf-dbus*/
%{_libdir}/pkgconfig/dconf-dbus*.pc
%{_libdir}/libdconf-dbus*.so

