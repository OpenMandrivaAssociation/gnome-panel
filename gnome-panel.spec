%define api 4
%define major   0
%define	gir_major 4.0
%define libname	%mklibname panel-applet %{api} %{major}
%define girname	%mklibname panel-applet-gir %{gir_major}
%define develname %mklibname -d panel-applet %{api}

Summary:	The core programs for the GNOME GUI desktop environment
Name:		gnome-panel
Version:	3.4.1
Release:	1
License:	GPLv2+ and LGPLv2+
Group:		Graphical desktop/GNOME
URL:		http://www.gnome.org/
Source0:	ftp://ftp.gnome.org/pub/GNOME/sources/%{name}/%{name}-%{version}.tar.xz
Source1:	mandriva-panel.png

BuildRequires:	desktop-file-utils
BuildRequires:	gettext
BuildRequires:	gettext-devel
BuildRequires:	glib2.0-common
BuildRequires:	gnome-common
BuildRequires:	gnome-doc-utils
BuildRequires:	gtk-doc
BuildRequires:	intltool
BuildRequires:	pkgconfig(cairo-gobject)
BuildRequires:	pkgconfig(cairo-xlib)
BuildRequires:	pkgconfig(dconf)
BuildRequires:	pkgconfig(gconf-2.0) >= 2.6.1
BuildRequires:	pkgconfig(gdk-pixbuf-2.0) >= 2.7.1
BuildRequires:	pkgconfig(gio-2.0) >= 2.25.12
BuildRequires:	pkgconfig(gio-unix-2.0) >= 2.25.12
BuildRequires:	pkgconfig(glib-2.0) >= 2.25.12
BuildRequires:	pkgconfig(gnome-desktop-3.0) >= 2.91.0
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(gtk+-3.0) >= 3.0
BuildRequires:	pkgconfig(gweather-3.0) >= 2.91.0
BuildRequires:	pkgconfig(ice)
BuildRequires:	pkgconfig(libecal-1.2) >= 2.91.2
BuildRequires:	pkgconfig(libedataserver-1.2) >= 2.91.2
BuildRequires:	pkgconfig(libedataserverui-3.0) >= 2.91.2
BuildRequires:	pkgconfig(libgnome-menu-3.0) >= 3.1.4
BuildRequires:	pkgconfig(librsvg-2.0)
BuildRequires:	pkgconfig(libwnck-3.0) >= 2.91.0
BuildRequires:	pkgconfig(NetworkManager) >= 0.6
BuildRequires:	pkgconfig(pango) >= 1.15.4
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
Requires:	alacarte
Requires:	gnome-shell
# for screen locking and search function in panel
Requires:	gnome-utils
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
Requires:	%{libname} = %{version}-%{release}

%description -n %{girname}
GObject Introspection interface description for %{name}.

%package -n	%{develname}
Summary:	Development libraries, include files for GNOME panel
Group:		Development/GNOME and GTK+
Provides:	%{name}-devel = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}
Obsoletes:	%{_lib}panel-applet-2_0-devel
Obsoletes:	%mklibname -d panel-applet- 2 0

%description -n	%{develname}
Panel libraries and header files for creating GNOME panels.

%prep
%setup -q
%apply_patches

%build
%configure2_5x \
	--enable-eds  \
	--disable-scrollkeeper \
	--disable-static \
	--disable-schemas-install

%make LIBS='-lgmodule-2.0'

%install
%makeinstall_std
find %{buildroot} -name '*.la' -delete;

%find_lang %{name}-3.0 --with-gnome --all-name

#remove unpackaged files
rm -rf %{buildroot}%{_datadir}/gnome-panelrc

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/scalable/apps
cp -a %{SOURCE1} %{buildroot}%{_datadir}/icons/hicolor/scalable/apps

%files -f %{name}-3.0.lang
%doc AUTHORS COPYING NEWS README
%{_bindir}/*
%{_sysconfdir}/gconf/schemas/clock.schemas
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
%{_libexecdir}/gnome-panel-add
%{_libexecdir}/clock-applet
%{_libexecdir}/fish-applet
%{_libexecdir}/notification-area-applet
%{_libexecdir}/wnck-applet
%{_mandir}/man1/*
%{_datadir}/applications/*.desktop
%{_datadir}/gnome-panel
%{_datadir}/icons/hicolor/*/apps/*

%files -n %{libname}
%{_libdir}/libpanel-applet-%{api}.so.%{major}*

%files -n %{girname}
%{_libdir}/girepository-1.0/PanelApplet-%{gir_major}.typelib

%files -n %{develname}
%doc ChangeLog
%doc %{_datadir}/gtk-doc/html/*
%{_includedir}/*
%{_libdir}/libpanel*.so
%{_libdir}/pkgconfig/*
%{_datadir}/gir-1.0/PanelApplet-%{gir_major}.gir

