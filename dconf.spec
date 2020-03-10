%define url_ver %(echo %{version} | cut -d. -f1,2)

%define major 1
%define libname %mklibname %{name} %{major}
%define devname %mklibname %{name} -d

%define giolibname %mklibname gio2.0_ 0

# From 0.24.x -- just to be obsoleted
%define dbusapi 1
%define dbusmaj 0
%define libdbus %mklibname %{name}-dbus- %{dbusapi} %{dbusmaj}
%define devdbus %mklibname %{name}-dbus -d

Summary:	Configuration backend for Glib
Name:		dconf
Version:	0.36.0
Release:	1
License:	LGPLv2+
Group:		System/Libraries
Url:		http://www.gnome.org/
Source0:	http://ftp.gnome.org/pub/GNOME/sources/dconf/%{url_ver}/%{name}-%{version}.tar.xz
BuildRequires:	meson
BuildRequires:	vala-devel
BuildRequires:	vala
BuildRequires:	bash-completion-devel
BuildRequires:	pkgconfig(dbus-1)
BuildRequires:	pkgconfig(gio-2.0)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(gmodule-2.0)
BuildRequires:	pkgconfig(bash-completion)
BuildRequires:	gtk-doc
BuildRequires:	intltool
Requires:	dbus
Requires(post,postun):	gio2.0
Requires(post,postun):	%{giolibname} >= 2.23.4-2

%description
This is a configuration backend for Glib's GSettings and part of GNOME 3.0.

%package -n	%{libname}
Summary:	Configuration backend library for Glib
Group:		System/Libraries

# this is b/c of the gio modules
Obsoletes:	%{_lib}dconf0 < %{version}
Obsoletes:	%{libdbus} < %{EVRD}


%description -n	%{libname}
This is a configuration backend for Glib's GSettings and part of GNOME 3.0.

%package -n	%{devname}
Summary:	Configuration backend library for Glib - development files
Group:		Development/C
Provides:	%{name}-devel = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}
Obsoletes:	%{devdbus} < %{EVRD}

%description -n	%{devname}
This is a configuration backend for Glib's GSettings and part of GNOME 3.0.

%prep
%setup -q
%autopatch -p1

%build
%meson -Dgtk_doc=true
%meson_build

%install
%meson_install
#we need this beacuse ibus and gdm installs file there
install -d %{buildroot}%{_sysconfdir}/dconf/db
install -d %{buildroot}%{_sysconfdir}/dconf/profile

%post
%{_bindir}/gio-querymodules-%{__isa_bits} %{_libdir}/gio/modules

%postun
if [ "$1" = "0" ]; then
 %{_bindir}/gio-querymodules-%{__isa_bits} %{_libdir}/gio/modules
fi

%check
#meson_test

%files
%doc NEWS
%dir %{_sysconfdir}/dconf
%dir %{_sysconfdir}/dconf/db
%dir %{_sysconfdir}/dconf/profile
%{_bindir}/dconf
%{_mandir}/man?/dconf.*
%{_mandir}/man1/dconf-service.*
%{_libexecdir}/dconf-service
%{_datadir}/bash-completion/completions/dconf
%{_datadir}/dbus-1/services/ca.desrt.dconf.service
%{_libdir}/gio/modules/libdconfsettings.*

%files -n %{libname}
%{_libdir}/libdconf.so.%{major}{,.*}

%files -n %{devname}
%doc %{_datadir}/gtk-doc/html/dconf
%{_libdir}/libdconf.so
%{_libdir}/pkgconfig/dconf.pc
%{_includedir}/dconf
%{_datadir}/vala/vapi/dconf*
