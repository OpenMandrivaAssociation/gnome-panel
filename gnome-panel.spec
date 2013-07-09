%define url_ver %(echo %{version}|cut -d. -f1,2)

%define api	4
%define major	0
%define gimajor	4.0
%define libname	%mklibname panel-applet %{api} %{major}
%define girname	%mklibname panel-applet-gir %{gimajor}
%define devname	%mklibname -d panel-applet %{api}

Summary:	The core programs for the GNOME GUI desktop environment
Name:		gnome-panel
Version:	3.6.2
Release:	4
License:	GPLv2+ and LGPLv2+
Group:		Graphical desktop/GNOME
Url:		http://www.gnome.org/
Source0:	http://ftp.gnome.org/pub/GNOME/sources/gnome-panel/%{url_ver}/%{name}-%{version}.tar.xz
Source1:	mandriva-panel.png
Patch0:		gnome-panel.remove-unused-gweatherxml-include.patch

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
BuildRequires:	pkgconfig(gconf-2.0) >= 2.6.1
BuildRequires:	pkgconfig(gdk-pixbuf-2.0) >= 2.7.1
BuildRequires:	pkgconfig(glib-2.0) >= 2.25.12
BuildRequires:	pkgconfig(gnome-desktop-3.0) >= 2.91.0
BuildRequires:	pkgconfig(gnome-doc-utils)
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(gtk+-3.0) >= 3.0
BuildRequires:	pkgconfig(gweather-3.0) >= 2.91.0
BuildRequires:	pkgconfig(ice)
BuildRequires:	pkgconfig(libgnome-menu-3.0) >= 3.1.4
BuildRequires:	pkgconfig(librsvg-2.0)
BuildRequires:	pkgconfig(libwnck-3.0) >= 2.91.0
BuildRequires:	pkgconfig(NetworkManager) >= 0.6
BuildRequires:	pkgconfig(pango) >= 1.15.4
BuildRequires:	pkgconfig(polkit-gobject-1)
BuildRequires:	pkgconfig(sm)
BuildRequires:	pkgconfig(telepathy-glib) >= 0.14.0
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xau)
BuildRequires:	pkgconfig(xrandr) >= 1.2.0

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

%package -n %{girname}
Summary:	GObject Introspection interface description for %{name}
Group:		System/Libraries

%description -n %{girname}
GObject Introspection interface description for %{name}.

%package -n	%{devname}
Summary:	Development libraries, include files for GNOME panel
Group:		Development/GNOME and GTK+
Provides:	%{name}-devel = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}
Requires:	%{girname} = %{version}-%{release}

%description -n	%{devname}
Panel libraries and header files for creating GNOME panels.

%prep
%setup -q
%apply_patches

%build
%configure2_5x \
	--enable-eds  \
	--disable-scrollkeeper \
	--disable-static \
	--disable-schemas-install \

%make LIBS='-lgmodule-2.0'

%install
%makeinstall_std

%find_lang %{name}-3.0 --with-gnome --all-name

#remove unpackaged files
rm -rf %{buildroot}%{_datadir}/gnome-panelrc

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/scalable/apps
cp -a %{SOURCE1} %{buildroot}%{_datadir}/icons/hicolor/scalable/apps

%files -f %{name}-3.0.lang
%doc AUTHORS COPYING NEWS README
%{_bindir}/*
%{_libexecdir}/gnome-panel-add
%{_libexecdir}/clock-applet
%{_libexecdir}/fish-applet
%{_libexecdir}/notification-area-applet
%{_libexecdir}/wnck-applet
%{_datadir}/glib-2.0/schemas/org.gnome.gnome-panel.applet.clock.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.gnome-panel.applet.fish.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.gnome-panel.applet.window-list.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.gnome-panel.applet.workspace-switcher.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.gnome-panel.enums.xml
%{_datadir}/glib-2.0/schemas/org.gnome.gnome-panel.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.gnome-panel.launcher.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.gnome-panel.menu-button.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.gnome-panel.object.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.gnome-panel.toplevel.gschema.xml
%{_datadir}/dbus-1/services/org.gnome.panel.applet.ClockAppletFactory.service
%{_datadir}/dbus-1/services/org.gnome.panel.applet.FishAppletFactory.service
%{_datadir}/dbus-1/services/org.gnome.panel.applet.NotificationAreaAppletFactory.service
%{_datadir}/dbus-1/services/org.gnome.panel.applet.WnckletFactory.service
%{_datadir}/applications/*.desktop
%{_datadir}/gnome-panel
%{_iconsdir}/hicolor/*/apps/*
%{_mandir}/man1/*

%files -n %{libname}
%{_libdir}/libpanel-applet-%{api}.so.%{major}*

%files -n %{girname}
%{_libdir}/girepository-1.0/PanelApplet-%{gimajor}.typelib

%files -n %{devname}
%doc ChangeLog
%doc %{_datadir}/gtk-doc/html/*
%{_includedir}/*
%{_libdir}/libpanel*.so
%{_libdir}/pkgconfig/*
%{_datadir}/gir-1.0/PanelApplet-%{gimajor}.gir

