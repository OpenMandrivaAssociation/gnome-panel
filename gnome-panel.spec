%define req_libwnck_version 2.19.5
%define req_libglade_version 2.5.0
%define req_gconf2_version 2.6.1
%define req_gnomeui_version 2.5.4
%define req_gtk_version 2.11.3
%define req_vfs_version 2.14.2
%define req_gnomedesktop_version 2.11.1

%define api_version 2
%define lib_major   0
%define libname	%mklibname panel-applet- %{api_version} %{lib_major}
%define libnamedev %mklibname -d panel-applet- %{api_version}

%define in_process_applets 1


Summary:	The core programs for the GNOME GUI desktop environment
Name:		gnome-panel
Version: 2.19.6
Release: %mkrel 1
License:	GPL/LGPL
Group:		Graphical desktop/GNOME
Source0:	ftp://ftp.gnome.org/pub/GNOME/sources/%{name}/%{name}-%{version}.tar.bz2
Source1:	mandriva-panel.png

# (fc) 2.0.1-2mdk  use xlock instead of xscreensaver to lock root desktop
Patch0:		gnome-panel-2.18.1-rootlock.patch
# (fc) 2.0.1-2mdk  Mandriva customization
Patch1:		gnome-panel-mdvcustomizations.patch
# (fc) 2.3.6.2-2mdk add "Suspend to disk" support
Patch2:		gnome-panel-2.14.1-suspend.patch
Patch3: gnome-panel-2.19.5-fpic.patch
Patch15:	gnome-panel_clock_tz_fix_crash.patch

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
URL:		http://www.gnome.org/
BuildRequires:	gnome-desktop-devel >= %{req_gnomedesktop_version}
BuildRequires:	libglade2.0-devel >= %{req_libglade_version}
BuildRequires:	libwnck-devel >= %{req_libwnck_version}
BuildRequires:	perl-XML-Parser
BuildRequires:	libxres-devel
BuildRequires:	libpng-devel
BuildRequires:	scrollkeeper
BuildRequires:	gnome-doc-utils
BuildRequires:	libxslt-proc
BuildRequires:	glib2-devel >= 2.6.0
BuildRequires:	gtk+2-devel >= %{req_gtk_version}
BuildRequires:	libgnomeui2-devel >= %{req_gnomeui_version}
BuildRequires:	libGConf2-devel >= %{req_gconf2_version}
BuildRequires:	evolution-data-server-devel >= 1.5.3
BuildRequires:  gnome-menus-devel >= 2.11.1
BuildRequires:  gnome-vfs2-devel >= %{req_vfs_version}
BuildRequires:  automake1.8
BuildRequires:	gtk-doc
BuildRequires:	gnome-common
BuildRequires:	intltool
Requires(post):	scrollkeeper
Requires(postun): scrollkeeper
Requires:	gnome-session
Requires:	gnome-desktop
Requires:	GConf2 >= %{req_gconf2_version}
Requires:	gnome-applets
Requires:	glib2 >= 2.6.0
Requires:	gnome-menus
Requires:	alacarte

# for screen locking and search function in panel
Requires:	gnome-utils
Requires:	gnome-screensaver
Requires:	desktop-common-data
#(patch0)
Requires:	xlockmore
#(patch1) (needed for time setting)
Requires:	drakxtools

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
Group:		%{group}

Provides:	libpanel-applet = %{version}-%{release}
Provides:	libpanel-applet-%{api_version} = %{version}-%{release}

%description -n	%{libname}
Panel libraries for running GNOME panels.

%package -n	%{libnamedev}
Summary:	Static libraries, include files for GNOME panel
Group:		Development/GNOME and GTK+
Provides:	%{name}-devel = %{version}-%{release}
Provides:	libpanel-applet-devel = %{version}-%{release}
Provides:	libpanel-applet-%{api_version}-devel = %{version}-%{release}
Requires:	%{libname} = %{version}
Obsoletes: %mklibname -d panel-applet- 2 0

%description -n	%{libnamedev}
Panel libraries and header files for creating GNOME panels.

%prep
%setup -q
%patch0 -p1 -b .rootlock
%patch2 -p1 -b .suspend
%patch1 -p1 -b .mdvcustomizations
%patch3 -p1 -b .pic
%patch15 -p0 -b .clockcrash
aclocal -I m4
autoconf
automake -a -c

%build

%configure2_5x --enable-eds --disable-scrollkeeper \
%if %{in_process_applets}
--with-in-process-applets=all
%endif

make

%install
rm -rf $RPM_BUILD_ROOT %name-2.0.lang

GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1 %makeinstall_std

install -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/gnome-panel/pixmaps

#remove old files
rm -rf %buildroot%_datadir/omf/gnome-panel

%find_lang %name-2.0 --with-gnome --all-name
for omf in %buildroot%_datadir/omf/*/{*-??.omf,*-??_??.omf};do
echo "%lang($(basename $omf|sed -e s/.*-// -e s/.omf//)) $(echo $omf|sed s!%buildroot!!)" >> %name-2.0.lang
done

#remove unpackaged files
rm -rf $RPM_BUILD_ROOT%{_datadir}/gnome-panelrc $RPM_BUILD_ROOT%{_localstatedir}/scrollkeeper $RPM_BUILD_ROOT%{_libexecdir}/gnome-panel/*.{a,la}


%clean
[ -n "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != / ] && rm -rf $RPM_BUILD_ROOT

%define schemas clock fish panel-compatibility panel-general panel-global panel-object panel-toplevel window-list workspace-switcher

%post -p /sbin/ldconfig -n %{libname}

%post
%update_scrollkeeper 
export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
gconftool-2 --direct --config-source=$GCONF_CONFIG_SOURCE --recursive-unset /apps/panel > /dev/null 2> /dev/null
gconftool-2 --direct --config-source=$GCONF_CONFIG_SOURCE --recursive-unset /schemas/apps/panel > /dev/null 2> /dev/null

%post_install_gconf_schemas %{schemas}
gconftool-2 --direct --config-source=$GCONF_CONFIG_SOURCE --load %{_sysconfdir}/gconf/schemas/panel-default-setup.entries > /dev/null
gconftool-2 --direct --config-source=$GCONF_CONFIG_SOURCE --load %{_sysconfdir}/gconf/schemas/panel-default-setup.entries /apps/panel > /dev/null

%update_icon_cache hicolor

%preun
%preun_uninstall_gconf_schemas %{schemas}

%postun -p /sbin/ldconfig -n %{libname}

%postun
%clean_scrollkeeper
%clean_icon_cache hicolor

%files -f %name-2.0.lang
%defattr (-, root, root)
%doc AUTHORS COPYING NEWS README
%{_sysconfdir}/gconf/schemas/clock.schemas
%{_sysconfdir}/gconf/schemas/fish.schemas
%{_sysconfdir}/gconf/schemas/panel-compatibility.schemas
%{_sysconfdir}/gconf/schemas/panel-general.schemas
%{_sysconfdir}/gconf/schemas/panel-global.schemas
%{_sysconfdir}/gconf/schemas/panel-object.schemas
%{_sysconfdir}/gconf/schemas/panel-toplevel.schemas
%{_sysconfdir}/gconf/schemas/window-list.schemas
%{_sysconfdir}/gconf/schemas/workspace-switcher.schemas

%{_sysconfdir}/gconf/schemas/panel-default-setup.entries

%{_bindir}/*
%if %{in_process_applets}
%dir %{_libexecdir}/gnome-panel
%dir %{_libexecdir}/gnome-panel/*.so
%else
%{_libexecdir}/clock-applet
%{_libexecdir}/fish-applet-2
%{_libexecdir}/notification-area-applet
%{_libexecdir}/wnck-applet
%endif
%{_mandir}/man1/*
%{_libdir}/bonobo/servers/*
%{_datadir}/applications/*.desktop
%dir %{_datadir}/gnome
%dir %{_datadir}/gnome/help
%_datadir/gnome-panel
%{_datadir}/gnome-2.0/ui/*
%{_datadir}/idl/*
%dir %{_datadir}/omf/*
%{_datadir}/omf/*/*-C.omf
%{_datadir}/icons/hicolor/*/apps/*

%files -n %{libname}
%defattr (-, root, root)
%{_libdir}/libpanel-applet-%{api_version}.so.%{lib_major}*

%files -n %{libnamedev}
%defattr (-, root, root)
%doc ChangeLog
%doc %{_datadir}/gtk-doc/html/*
%{_includedir}/*
%attr(644,root,root) %{_libdir}/*.la
%{_libdir}/*.a
%{_libdir}/libpanel*.so
%{_libdir}/pkgconfig/*
