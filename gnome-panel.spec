%define url_ver %(echo %{version}|cut -d. -f1,2)
# modules/action-button and friends are dlopened and may call
# into stuff they're not linked to directly
%define _disable_ld_no_undefined 1

%define api	0
%define major	3
%define gimajor	5.0
%define libname	%mklibname panel-applet %{major}
%define girname	%mklibname panel-applet-gir %{gimajor}
%define devname	%mklibname -d panel-applet

Summary:	The core programs for the GNOME GUI desktop environment
Name:		gnome-panel
Version:	3.49.1
Release:	1
License:	GPLv2+ and LGPLv2+
Group:		Graphical desktop/GNOME
Url:		http://www.gnome.org/
Source0:	http://ftp.gnome.org/pub/GNOME/sources/gnome-panel/%{url_ver}/%{name}-%{version}.tar.xz
Source1:	mandriva-panel.png

BuildRequires:	desktop-file-utils
BuildRequires:	glib2.0-common
BuildRequires:	gnome-common
BuildRequires:	gtk-doc
BuildRequires:	intltool
BuildRequires:	itstool
BuildRequires:	gettext-devel
BuildRequires:	pkgconfig(cairo-gobject)
BuildRequires:	pkgconfig(cairo-xlib)
BuildRequires:	pkgconfig(dconf)
BuildRequires:  pkgconfig(evolution-data-server-1.2)
BuildRequires:	pkgconfig(gdk-pixbuf-2.0) >= 2.7.1
BuildRequires:	pkgconfig(gdm)
BuildRequires:	pkgconfig(glib-2.0) >= 2.25.12
BuildRequires:	pkgconfig(gnome-desktop-3.0) >= 2.91.0
BuildRequires:	pkgconfig(gnome-doc-utils)
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(gtk+-3.0) >= 3.0
BuildRequires:	pkgconfig(gweather4)
BuildRequires:	pkgconfig(ice)
BuildRequires:	pkgconfig(libecal-2.0)
BuildRequires:	pkgconfig(libgnome-menu-3.0) >= 3.1.4
BuildRequires:	pkgconfig(librsvg-2.0)
BuildRequires:	pkgconfig(libwnck-3.0) >= 2.91.0
BuildRequires:	pkgconfig(pango) >= 1.15.4
BuildRequires:	pkgconfig(polkit-gobject-1)
BuildRequires:	pkgconfig(sm)
BuildRequires:	pkgconfig(systemd)
BuildRequires:	pkgconfig(telepathy-glib) >= 0.14.0
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xau)
BuildRequires:	pkgconfig(xrandr) >= 1.2.0
BuildRequires:	yelp-tools

Requires:	gsettings-desktop-schemas
Requires:	gnome-session
Requires:	gnome-desktop3
Requires:	polkit-agent
Requires:	gnome-menus
Requires:	gnome-shell
# for search function in panel
Requires:	gnome-search-tool
Requires:	gnome-screensaver
Requires:	desktop-common-data

Suggests:	gnome-applets

%description
GNOME (GNU Network Object Model Environment) is a user-friendly
set of applications and desktop tools to be used in conjunction with a
window manager for the X Window System.  GNOME is similar in purpose and
scope to CDE and KDE, but GNOME is based completely on free
software.

The GNOME panel packages provides the gnome panel, menus and some
basic applets for the panel.

%package -n	%{libname}
Summary:	%{summary}
Group:		System/Libraries
Provides:	libpanel-applet = %{version}-%{release}
Provides:	libpanel-applet-%{api} = %{version}-%{release}

%description -n	%{libname}
Panel libraries for running GNOME panels.

#%package -n %{girname}
#Summary:	GObject Introspection interface description for %{name}
#Group:		System/Libraries
#
#%description -n %{girname}
#GObject Introspection interface description for %{name}.

%package -n	%{devname}
Summary:	Development libraries, include files for GNOME panel
Group:		Development/GNOME and GTK+
Provides:	%{name}-devel = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}
#Requires:	%{girname} = %{version}-%{release}
Obsoletes:	%{_lib}panel-applet4-devel

%description -n	%{devname}
Panel libraries and header files for creating GNOME panels.

%prep
%setup -q
%autopatch -p1

%build
%configure \
	--enable-eds  \
	--disable-schemas-install \
	--enable-compile-warnings=no

%make_build LIBS='-lgmodule-2.0'

%install
%make_install

%find_lang %{name}-3.0 --with-gnome --all-name

#remove unpackaged files
rm -rf %{buildroot}%{_datadir}/gnome-panelrc

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/scalable/apps
cp -a %{SOURCE1} %{buildroot}%{_datadir}/icons/hicolor/scalable/apps

%files -f %{name}-3.0.lang
%doc AUTHORS COPYING NEWS
%{_bindir}/*
#{_libdir}/gnome-panel/%{gimajor}/libclock-applet.so
#{_libdir}/gnome-panel/%{gimajor}/libfish-applet.so
#{_libdir}/gnome-panel/%{gimajor}/libnotification-area-applet.so
#{_libdir}/gnome-panel/%{gimajor}/libwnck-applet.so
%{_libdir}/gnome-panel/modules/*
%{_datadir}/glib-2.0/schemas/org.gnome.gnome-panel.applet.clock.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.gnome-panel.applet.fish.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.gnome-panel.applet.launcher.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.gnome-panel.applet.window-list.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.gnome-panel.applet.workspace-switcher.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.gnome-panel.enums.xml
%{_datadir}/glib-2.0/schemas/org.gnome.gnome-panel.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.gnome-panel.applet.menu-button.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.gnome-panel.applet.initial-settings.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.gnome-panel.object.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.gnome-panel.toplevel.gschema.xml
%{_datadir}/applications/*.desktop
%{_datadir}/gnome-panel
%{_iconsdir}/hicolor/*/apps/*
%{_mandir}/man1/*

%files -n %{libname}
%{_libdir}/libgnome-panel.so.%{api}*

#%files -n %{girname}
#{_libdir}/girepository-1.0/PanelApplet-%{gimajor}.typelib

%files -n %{devname}
%doc ChangeLog
%{_includedir}/*
%{_libdir}/libgnome-panel.so
%{_libdir}/pkgconfig/*
#{_datadir}/gir-1.0/PanelApplet-%{gimajor}.gir

