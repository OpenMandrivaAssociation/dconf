# TODO: split library package on libdconf, libdconf-dbus-1 and modules


%define major 1
%define libname %mklibname %{name} %{major}
%define develname %mklibname -d %{name}
%define giolibname %mklibname gio2.0_ 0

Summary:	Configuration backend for Glib
Name:		dconf
Version:	0.14.1
Release:	1
Source0:	http://ftp.gnome.org/pub/GNOME/sources/%name/0.14/%{name}-%{version}.tar.xz
License:	LGPLv2+
Group:		System/Libraries
Url:		http://www.gnome.org/

BuildRequires:	pkgconfig(dbus-1)
BuildRequires:	pkgconfig(gio-2.0)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	vala-devel intltool xsltproc gtk-doc

%description
This is a configuration backend for Glib's GSettings and part of GNOME 3.0.

%package editor
Summary:	An editor for the Dconf configuration system
Group:		Graphical desktop/GNOME
Requires:	%{name} = %{version}-%{release}

%description editor
This is a graphical editor for the Dconf configuration system.

%package -n %{libname}
Group:		System/Libraries
Summary:	Configuration backend library for Glib
Obsoletes:	%{mklibname dconf 0} < 0.14
Requires(post): %{giolibname} >= 2.23.4
Requires(postun): %{giolibname} >= 2.23.4

%description -n %{libname}
This is a configuration backend for Glib's GSettings and part of GNOME 3.0.

%package -n %{develname}
Group:		Development/C
Summary:	Configuration backend library for Glib - development files
Provides:	lib%{name}-devel = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}

%description -n %{develname}
This is a configuration backend for Glib's GSettings and part of GNOME 3.0.

%prep
%setup -q

%build
%configure2_5x
%make

%install
%makeinstall_std

%find_lang %{name}

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

%files -f %{name}.lang
%doc NEWS
%{_bindir}/dconf
%{_libexecdir}/dconf-service
%{_datadir}/dbus-1/services/ca.desrt.dconf.service
%{_datadir}/applications/dconf-editor.desktop
%{_datadir}/bash-completion/completions/dconf
%{_mandir}/man?/*
#%_datadir/dbus-1/system-services/ca.desrt.dconf.service

%files editor
%{_bindir}/dconf-editor
%{_datadir}/glib-2.0/schemas/ca.desrt.dconf-editor.gschema.xml
%{_datadir}/dconf-editor/dconf-editor-menu.ui
%{_datadir}/dconf-editor/dconf-editor.ui
%{_datadir}/icons/*/*/*/dconf-editor.png

%files -n %{libname}
%{_libdir}/libdconf.so.%{major}*
%{_libdir}/libdconf-dbus-1.so*
%{_libdir}/gio/modules/libdconfsettings.*
#%_libdir/girepository-1.0/dconf-1.0.typelib

%files -n %{develname}
%{_libdir}/libdconf.so
%{_libdir}/pkgconfig/dconf.pc
%{_libdir}/pkgconfig/dconf-dbus-1.pc
%{_includedir}/dconf
%{_includedir}/dconf-dbus-1/dconf-dbus-1.h
#%_datadir/gir-1.0/dconf-1.0.gir
%{_datadir}/gtk-doc/html/dconf
%{_datadir}/vala/vapi/dconf*

%changelog
* Tue Nov 13 2012 Arkady L. Shane <ashejn@rosalab.ru> 0.14.1-1
- update to 0.14.1

* Mon Oct  1 2012 Arkady L. Shane <ashejn@rosalab.ru> 0.14-1
- update to 0.14.0

* Sat Sep 18 2010 Götz Waschk <waschk@mandriva.org> 0.5.1-1mdv2011.0
+ Revision: 579737
- new version
- bump deps
- rename introspection data files

* Tue Aug 31 2010 Götz Waschk <waschk@mandriva.org> 0.5-2mdv2011.0
+ Revision: 574668
- add introspection support
- fix postun script
- move gio module to the library package
- add postinstallation scripts for gio module

* Wed Aug 04 2010 Götz Waschk <waschk@mandriva.org> 0.5-1mdv2011.0
+ Revision: 565646
- new version
- remove static libs
- remove gobject-introspection support
- add vala support
- new version
- add editor package
- import dconf


