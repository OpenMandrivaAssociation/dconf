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
Version:	0.27.1
Release:	1
License:	LGPLv2+
Group:		System/Libraries
Url:		http://www.gnome.org/
Source0:	http://ftp.gnome.org/pub/GNOME/sources/dconf/%{url_ver}/%{name}-%{version}.tar.xz
BuildRequires:	meson
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

%build
%meson
%meson_build

%install
%meson_install

%post
%if "%{_lib}" != "lib"
 %{_bindir}/gio-querymodules-64 %{_libdir}/gio/modules
%else
 %{_bindir}/gio-querymodules-32 %{_libdir}/gio/modules
%endif

%postun
if [ "$1" = "0" ]; then
%if "%{_lib}" != "lib"
 %{_bindir}/gio-querymodules-64 %{_libdir}/gio/modules 
%else
 %{_bindir}/gio-querymodules-32 %{_libdir}/gio/modules
%endif
fi

%files
%doc NEWS
%{_bindir}/dconf
%{_libexecdir}/dconf-service
%{_datadir}/dbus-1/services/ca.desrt.dconf.service
%{_datadir}/bash-completion/completions/dconf

%files -n %{libname}
%{_libdir}/libdconf.so.%{major}*
%{_libdir}/gio/modules/libdconfsettings.*

%files -n %{devname}
%{_libdir}/libdconf.so
%{_libdir}/pkgconfig/dconf.pc
%{_includedir}/dconf/
%{_datadir}/vala/vapi/dconf*
