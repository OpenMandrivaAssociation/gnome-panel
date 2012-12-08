%define api	4
%define major	0
%define girmajor 4.0
%define libname	%mklibname panel-applet %{api} %{major}
%define girname	%mklibname panel-applet-gir %{girmajor}
%define develname %mklibname -d panel-applet %{api}

Summary:	The core programs for the GNOME GUI desktop environment
Name:		gnome-panel
Version:	3.6.2
Release:	1
License:	GPLv2+ and LGPLv2+
Group:		Graphical desktop/GNOME
URL:		http://www.gnome.org/
Source0:	ftp://ftp.gnome.org/pub/GNOME/sources/gnome-panel/3.6/%{name}-%{version}.tar.xz
Source1:	mandriva-panel.png

BuildRequires:	desktop-file-utils
BuildRequires:	gettext itstool
BuildRequires:	gettext-devel
BuildRequires:	glib2.0-common
BuildRequires:	gnome-common
BuildRequires:	gtk-doc
BuildRequires:	intltool
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
BuildRequires:	pkgconfig(libedataserverui-3.0) >= 2.91.2
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
BuildConflicts:	libevolution-data-server2-devel

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
Obsoletes:	gnome-panel2 < 3.4

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

%package -n	%{develname}
Summary:	Development libraries, include files for GNOME panel
Group:		Development/GNOME and GTK+
Provides:	%{name}-devel = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}
Requires:	%{girname} = %{version}-%{release}
Obsoletes:	%{_lib}panel-applet-2_0-devel < 3.4
Obsoletes:	%{mklibname -d panel-applet- 2 0} < 3.4

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
%{_libdir}/girepository-1.0/PanelApplet-%{girmajor}.typelib

%files -n %{develname}
%doc ChangeLog
%doc %{_datadir}/gtk-doc/html/*
%{_includedir}/*
%{_libdir}/libpanel*.so
%{_libdir}/pkgconfig/*
%{_datadir}/gir-1.0/PanelApplet-%{girmajor}.gir



%changelog
* Mon Oct  1 2012 Arkady L. Shane <ashejn@rosalab.ru> 3.6.0-1
- update to 3.6.0

* Wed May 16 2012 Matthew Dawkins <mattydaw@mandriva.org> 3.4.2.1-1
+ Revision: 799261
- update to new version 3.4.2.1

* Thu May 10 2012 Matthew Dawkins <mattydaw@mandriva.org> 3.4.1-3
+ Revision: 798121
- rebuild
- dropped alacarte (pakagekit-gtk2-modules is obsolete)
- obsoleted gnome-panel2

* Sat May 05 2012 Matthew Dawkins <mattydaw@mandriva.org> 3.4.1-2
+ Revision: 796854
- rebuild to switch dep on gnome-utils to gnome-search-tool

* Tue May 01 2012 Alexander Khrukin <akhrukin@mandriva.org> 3.4.1-1
+ Revision: 794677
- version update 3.4.1

* Thu Mar 08 2012 Matthew Dawkins <mattydaw@mandriva.org> 3.2.1-2
+ Revision: 783416
- rebuild
- fixed requires for gnome-search-tool to gnome-utils
- removed omf find files and files list (handled by find_lang)

* Thu Dec 08 2011 Matthew Dawkins <mattydaw@mandriva.org> 3.2.1-1
+ Revision: 739076
- fixed configure
- fixed api
- fixed files and dirs lists
- added obsoletes for old style devel pkg
- dropped hyphen in lib & devel pkg names
- new version 3.2.1
- dropped unused patches
- cleaned up spec
- converted BRs to pkgconfig provides
- removed .la files
- removed defattr, clean section, mkrel, BuildRoot
- removed old scriptlets
- split out gir pkg
- libname2 is gone

* Mon Oct 24 2011 Götz Waschk <waschk@mandriva.org> 2.32.1-4
+ Revision: 705849
- fix linking
- rebuild for libpng

* Tue May 03 2011 Oden Eriksson <oeriksson@mandriva.com> 2.32.1-3
+ Revision: 664877
- mass rebuild

* Tue Dec 14 2010 Funda Wang <fwang@mandriva.org> 2.32.1-2mdv2011.0
+ Revision: 621686
- rebuild for new popt

* Wed Nov 17 2010 Götz Waschk <waschk@mandriva.org> 2.32.1-1mdv2011.0
+ Revision: 598370
- new version

  + John Balcaen <mikala@mandriva.org>
    - Fix BR for libcanberra-gtk-devel

* Tue Sep 28 2010 Götz Waschk <waschk@mandriva.org> 2.32.0.2-1mdv2011.0
+ Revision: 581612
- update to new version 2.32.0.2

  + Funda Wang <fwang@mandriva.org>
    - we are using oxygen rather than crystalsvg for kde4

* Mon Sep 27 2010 Götz Waschk <waschk@mandriva.org> 2.32.0.1-1mdv2011.0
+ Revision: 581368
- new version
- drop patch 2

* Mon Sep 27 2010 Götz Waschk <waschk@mandriva.org> 2.32.0-1mdv2011.0
+ Revision: 581306
- new version
- patch to fix linking

* Tue Sep 14 2010 Götz Waschk <waschk@mandriva.org> 2.31.92-1mdv2011.0
+ Revision: 578314
- new version
- rediff patch 1

* Thu Sep 02 2010 Götz Waschk <waschk@mandriva.org> 2.31.91-1mdv2011.0
+ Revision: 575213
- update to new version 2.31.91

* Mon Aug 30 2010 Götz Waschk <waschk@mandriva.org> 2.31.90-2mdv2011.0
+ Revision: 574326
- rebuild for new e-d-s

* Wed Aug 18 2010 Götz Waschk <waschk@mandriva.org> 2.31.90-1mdv2011.0
+ Revision: 571271
- new version
- update file list

* Sun Aug 08 2010 Götz Waschk <waschk@mandriva.org> 2.31.6-2mdv2011.0
+ Revision: 567711
- disable in-process applet support (bug #60542)
- update file list

* Wed Aug 04 2010 Götz Waschk <waschk@mandriva.org> 2.31.6-1mdv2011.0
+ Revision: 565853
- update build deps
- new version
- drop patch 17
- rediff patch 23
- add libgnome-panel-3
- update file list
- add introspection support

* Wed Jun 23 2010 Frederic Crozat <fcrozat@mandriva.com> 2.30.2-1mdv2010.1
+ Revision: 548681
- Release 2.30.2
- Remove patch24 (merged upstream)
- regenerate patch23

* Mon Jun 21 2010 Frederic Crozat <fcrozat@mandriva.com> 2.30.0-4mdv2010.1
+ Revision: 548456
- Patch24 (GIT): fix hidden panel regression

* Wed Apr 28 2010 Christophe Fergeau <cfergeau@mandriva.com> 2.30.0-3mdv2010.1
+ Revision: 540343
- rebuild so that shared libraries are properly stripped again

* Mon Apr 26 2010 Frederic Crozat <fcrozat@mandriva.com> 2.30.0-2mdv2010.1
+ Revision: 539090
- Patch22 (Fedora): add padding for icons on panel (GNOME bug #343346)
- Patch23 (Fedora): add padding for notification area (GNOME bug #583273)
- Update patch1 to add default padding
- Update patch16 to correctly detect beagle and tracker for some case. Ensure tracker is now favored over beagle.

* Tue Mar 30 2010 Götz Waschk <waschk@mandriva.org> 2.30.0-1mdv2010.1
+ Revision: 528967
- update to new version 2.30.0

* Wed Mar 10 2010 Götz Waschk <waschk@mandriva.org> 2.29.92.1-1mdv2010.1
+ Revision: 517276
- update to new version 2.29.92.1

* Tue Mar 09 2010 Götz Waschk <waschk@mandriva.org> 2.29.92-1mdv2010.1
+ Revision: 517237
- new version
- bump gtk dep
- drop patch 18
- rediff patch 19

* Mon Feb 22 2010 Götz Waschk <waschk@mandriva.org> 2.29.91-1mdv2010.1
+ Revision: 509780
- update to new version 2.29.91

* Wed Feb 17 2010 Funda Wang <fwang@mandriva.org> 2.29.6-2mdv2010.1
+ Revision: 506919
- rebuild for new popt

* Wed Jan 27 2010 Götz Waschk <waschk@mandriva.org> 2.29.6-1mdv2010.1
+ Revision: 497404
- update to new version 2.29.6

* Thu Jan 14 2010 Götz Waschk <waschk@mandriva.org> 2.29.5.1-1mdv2010.1
+ Revision: 491242
- update to new version 2.29.5.1

* Wed Jan 13 2010 Götz Waschk <waschk@mandriva.org> 2.29.5-1mdv2010.1
+ Revision: 490563
- update build deps
- new version
- rediff patches 1,20
- drop patch 22

* Mon Oct 26 2009 Frederic Crozat <fcrozat@mandriva.com> 2.28.0-4mdv2010.0
+ Revision: 459402
- Patch20: increase minimal entries to push bookmarks as submenu
- Patch21: add about-mandriva menu entry
- Patch22 (GIT): xrandr fixes (GNOME bug #597101)

* Tue Oct 20 2009 Frederic Crozat <fcrozat@mandriva.com> 2.28.0-3mdv2010.0
+ Revision: 458419
- Patch18 (Fedora): add default order for some icons in tray (GNOME bug #583115)
- Patch19: define net_applet as a network applet

* Wed Sep 23 2009 Frederic Crozat <fcrozat@mandriva.com> 2.28.0-2mdv2010.0
+ Revision: 447785
- Remove patch2, obsolete
- Regenerate patch0

* Mon Sep 21 2009 Götz Waschk <waschk@mandriva.org> 2.28.0-1mdv2010.0
+ Revision: 446952
- update to new version 2.28.0

* Fri Sep 11 2009 Götz Waschk <waschk@mandriva.org> 2.27.92-1mdv2010.0
+ Revision: 437896
- new version
- update gnome-menus dep

* Tue Aug 25 2009 Götz Waschk <waschk@mandriva.org> 2.27.91-1mdv2010.0
+ Revision: 421183
- update file list
- depend on polkit-agent
- new version
- upate patch 16
- new polkit
- depend on new libgweather

  + Frederic Crozat <fcrozat@mandriva.com>
    - Update patch0 to fix warnings
    - Update patch16 to correctly detect beagle/tracker on mandriva
    - Replace BR scrollkeeper with rarian

* Wed Jul 15 2009 Götz Waschk <waschk@mandriva.org> 2.27.4-1mdv2010.0
+ Revision: 396382
- new version
- rediff patch 0

* Wed Jul 01 2009 Götz Waschk <waschk@mandriva.org> 2.26.3-1mdv2010.0
+ Revision: 391240
- new version
- rediff patch 1

* Wed May 20 2009 Götz Waschk <waschk@mandriva.org> 2.26.2-1mdv2010.0
+ Revision: 378020
- new version
- drop patch 18

* Fri Apr 17 2009 Frederic Crozat <fcrozat@mandriva.com> 2.26.1-2mdv2009.1
+ Revision: 367881
- Patch17 (Fedora): don't complain about missing applets if they are from default install
- Patch18: fix libglade warning

* Tue Apr 14 2009 Götz Waschk <waschk@mandriva.org> 2.26.1-1mdv2009.1
+ Revision: 367233
- update to new version 2.26.1

* Tue Mar 17 2009 Götz Waschk <waschk@mandriva.org> 2.26.0-1mdv2009.1
+ Revision: 356309
- update to new version 2.26.0

* Tue Mar 03 2009 Götz Waschk <waschk@mandriva.org> 2.25.92-1mdv2009.1
+ Revision: 348020
- update to new version 2.25.92

* Tue Mar 03 2009 Frederic Crozat <fcrozat@mandriva.com> 2.25.91-2mdv2009.1
+ Revision: 347770
- Fix patch1, MCC launcher was incorrectly added to panel schema

* Tue Feb 17 2009 Götz Waschk <waschk@mandriva.org> 2.25.91-1mdv2009.1
+ Revision: 341386
- new version
- rediff patch 1

* Tue Feb 03 2009 Götz Waschk <waschk@mandriva.org> 2.25.90-1mdv2009.1
+ Revision: 336942
- new version
- drop patch 17

* Wed Jan 21 2009 Funda Wang <fwang@mandriva.org> 2.25.5.1-1mdv2009.1
+ Revision: 332072
- 2.25.5.1

* Tue Jan 20 2009 Götz Waschk <waschk@mandriva.org> 2.25.5-1mdv2009.1
+ Revision: 331934
- new version

* Fri Dec 19 2008 Frederic Crozat <fcrozat@mandriva.com> 2.25.3-2mdv2009.1
+ Revision: 316129
- Update patch1 to no longer add volume applet, it is provided by gnome-media now
- don't requires drakxtools, time configuration is using policykit

* Fri Dec 19 2008 Götz Waschk <waschk@mandriva.org> 2.25.3-1mdv2009.1
+ Revision: 316101
- new version
- update patch 1
- get new version of patch 16 from Fedora
- patch 17: fix format strings

* Tue Nov 25 2008 Götz Waschk <waschk@mandriva.org> 2.24.2-1mdv2009.1
+ Revision: 306620
- fix build deps
- update to new version 2.24.2

* Sun Nov 09 2008 Oden Eriksson <oeriksson@mandriva.com> 2.24.1-3mdv2009.1
+ Revision: 301393
- rebuilt against new libxcb

* Thu Nov 06 2008 Götz Waschk <waschk@mandriva.org> 2.24.1-2mdv2009.1
+ Revision: 300205
- rebuild for new gnome-desktop

* Wed Oct 22 2008 Götz Waschk <waschk@mandriva.org> 2.24.1-1mdv2009.1
+ Revision: 296500
- new version
- bump libgweather dep

* Tue Sep 23 2008 Götz Waschk <waschk@mandriva.org> 2.24.0-1mdv2009.0
+ Revision: 287292
- new epiphany

* Tue Sep 09 2008 Götz Waschk <waschk@mandriva.org> 2.23.92-1mdv2009.0
+ Revision: 282920
- new version

* Tue Sep 02 2008 Götz Waschk <waschk@mandriva.org> 2.23.91-1mdv2009.0
+ Revision: 278813
- new version

* Thu Aug 21 2008 Götz Waschk <waschk@mandriva.org> 2.23.90.1-1mdv2009.0
+ Revision: 274634
- new version

* Tue Aug 19 2008 Frederic Crozat <fcrozat@mandriva.com> 2.23.90-2mdv2009.0
+ Revision: 273969
- Use new name for firefox .desktop file

* Tue Aug 19 2008 Götz Waschk <waschk@mandriva.org> 2.23.90-1mdv2009.0
+ Revision: 273623
- new version

* Tue Aug 05 2008 Götz Waschk <waschk@mandriva.org> 2.23.6-1mdv2009.0
+ Revision: 263794
- fix build deps
- new version
- bump libgweather dep
- update patch 2

* Wed Jul 23 2008 Götz Waschk <waschk@mandriva.org> 2.23.5-1mdv2009.0
+ Revision: 241910
- new version

* Thu Jul 03 2008 Götz Waschk <waschk@mandriva.org> 2.23.4-1mdv2009.0
+ Revision: 231289
- new version

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers
    - adapt to %%_localstatedir now being /var instead of /var/lib (#22312)

  + Frederic Crozat <fcrozat@mandriva.com>
    - remove unneeded cpp define

* Tue May 27 2008 Götz Waschk <waschk@mandriva.org> 2.22.2-1mdv2009.0
+ Revision: 211636
- new version
- drop patch 17
- update file list

* Wed May 07 2008 Frederic Crozat <fcrozat@mandriva.com> 2.22.1.3-2mdv2009.0
+ Revision: 202957
- Patch17 (SVN): fix application to use for recent files (Mdv bug #40632) (SVN)

* Tue Apr 15 2008 Götz Waschk <waschk@mandriva.org> 2.22.1.3-1mdv2009.0
+ Revision: 194357
- new version

* Tue Apr 15 2008 Götz Waschk <waschk@mandriva.org> 2.22.1.2-1mdv2009.0
+ Revision: 193611
- new version
- bump libgweather dep
- drop patches 3,17,18

* Wed Apr 02 2008 Frederic Crozat <fcrozat@mandriva.com> 2.22.0-4mdv2008.1
+ Revision: 191563
- Update patch18 with more clock fixes

* Wed Mar 26 2008 Emmanuel Andry <eandry@mandriva.org> 2.22.0-3mdv2008.1
+ Revision: 190547
- Fix lib group

* Tue Mar 18 2008 Frederic Crozat <fcrozat@mandriva.com> 2.22.0-2mdv2008.1
+ Revision: 188563
- Patch17: fix invalid username when locale is not UTF-8
- Patch28 (SVN): various fixes from SVN for clock applet

* Mon Mar 10 2008 Götz Waschk <waschk@mandriva.org> 2.22.0-1mdv2008.1
+ Revision: 183880
- new version

* Tue Feb 26 2008 Götz Waschk <waschk@mandriva.org> 2.21.92-1mdv2008.1
+ Revision: 175410
- add build dep on policykit
- update file list

* Tue Feb 12 2008 Götz Waschk <waschk@mandriva.org> 2.21.91-1mdv2008.1
+ Revision: 165848
- new version
- update deps

* Tue Jan 29 2008 Götz Waschk <waschk@mandriva.org> 2.21.90-1mdv2008.1
+ Revision: 159906
- new version

* Tue Jan 15 2008 Götz Waschk <waschk@mandriva.org> 2.21.5-1mdv2008.1
+ Revision: 152141
- new version
- update buildrequires
- fix build with libgweather

* Tue Jan 08 2008 Götz Waschk <waschk@mandriva.org> 2.20.3-1mdv2008.1
+ Revision: 146431
- new version

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Tue Nov 27 2007 Götz Waschk <waschk@mandriva.org> 2.20.2-1mdv2008.1
+ Revision: 113349
- new version

* Mon Oct 15 2007 Götz Waschk <waschk@mandriva.org> 2.20.1-1mdv2008.1
+ Revision: 98709
- new version

  + Frederic Crozat <fcrozat@mandriva.com>
    - Update patch1 to fix Mdv bug #34392 and no longer add help launcher on panel
    - Remove patch17, no longer needed

* Wed Oct 03 2007 Emmanuel Andry <eandry@mandriva.org> 2.20.0.1-2mdv2008.0
+ Revision: 95259
- diff patch17 to fix a pixmaps path (bug #34392)

* Tue Sep 18 2007 Götz Waschk <waschk@mandriva.org> 2.20.0.1-1mdv2008.0
+ Revision: 89679
- new version
- new version
- drop patch 15

  + Frederic Crozat <fcrozat@mandriva.com>
    - Update patch 2 : fix launcher order, fix mandriva-panel.png location (Mdv bug #33604)
    - Patch16 (Fedora): call beagle or tracker (if installed) for file search instead of gnome-search

* Wed Sep 05 2007 Götz Waschk <waschk@mandriva.org> 2.19.92-1mdv2008.0
+ Revision: 79736
- new version

* Thu Aug 30 2007 Frederic Crozat <fcrozat@mandriva.com> 2.19.6-2mdv2008.0
+ Revision: 75214
- Update patch1 to no longer change default directory to ~/Desktop, don't change clock schemas for drakclock (use configure flag instead)

* Tue Aug 14 2007 Götz Waschk <waschk@mandriva.org> 2.19.6-1mdv2008.0
+ Revision: 63293
- new version
- drop patch 16

* Tue Aug 07 2007 Frederic Crozat <fcrozat@mandriva.com> 2.19.5-4mdv2008.0
+ Revision: 59968
- Remove patch14, not needed anymore with XDG user dirs

* Wed Aug 01 2007 Götz Waschk <waschk@mandriva.org> 2.19.5-3mdv2008.0
+ Revision: 57569
- new devel name

* Wed Jul 18 2007 Pascal Terjan <pterjan@mandriva.org> 2.19.5-2mdv2008.0
+ Revision: 53296
- Fix another crash when editing timezone (not the last one unfortunately)
- Fix the patch
- Better fix for the crash
- Fix a crash when selecting timezones of the clock applet

* Mon Jul 09 2007 Götz Waschk <waschk@mandriva.org> 2.19.5-1mdv2008.0
+ Revision: 50464
- fix build
- new version
- bump deps

* Sun Jun 17 2007 Götz Waschk <waschk@mandriva.org> 2.19.4-1mdv2008.0
+ Revision: 40619
- new version
- bump deps

* Thu Jun 07 2007 Götz Waschk <waschk@mandriva.org> 2.19.3-2mdv2008.0
+ Revision: 36460
- new version
- drop patch 13
- rediff patch 14
- update file list

* Mon May 28 2007 Götz Waschk <waschk@mandriva.org> 2.18.2-1mdv2008.0
+ Revision: 32131
- new version

* Wed Apr 18 2007 Götz Waschk <waschk@mandriva.org> 2.18.1-1mdv2008.0
+ Revision: 14401
- new version
- update patch 0
- drop patch 15


* Tue Mar 20 2007 Frederic Crozat <fcrozat@mandriva.com> 2.18.0-5mdv2007.1
+ Revision: 147037
- Patch15: lock screen when using switch user (Mdv bug #29717)

* Sat Mar 17 2007 Frederic Crozat <fcrozat@mandriva.com> 2.18.0-4mdv2007.1
+ Revision: 145371
- Update patch14 to no longer warn when some .desktop bookmark are no longer valid

* Thu Mar 15 2007 Frederic Crozat <fcrozat@mandriva.com> 2.18.0-2mdv2007.1
+ Revision: 144403
- Fix gnome-panel showing incorrectly in menu

* Mon Mar 12 2007 Götz Waschk <waschk@mandriva.org> 2.18.0-1mdv2007.1
+ Revision: 142088
- new version
- update file list

  + Thierry Vignaud <tvignaud@mandriva.com>
    - no need to package big ChangeLog when NEWS is already there

* Mon Feb 26 2007 Götz Waschk <waschk@mandriva.org> 2.17.92-1mdv2007.1
+ Revision: 126157
- new version

* Tue Feb 20 2007 Frederic Crozat <fcrozat@mandriva.com> 2.17.91-2mdv2007.1
+ Revision: 122972
- Update patch1 / add source1 : add default texture to panels

* Tue Feb 13 2007 Götz Waschk <waschk@mandriva.org> 2.17.91-1mdv2007.1
+ Revision: 120274
- new version

* Mon Jan 22 2007 Götz Waschk <waschk@mandriva.org> 2.17.90-1mdv2007.1
+ Revision: 111678
- new version

* Thu Nov 30 2006 Götz Waschk <waschk@mandriva.org> 2.16.2-5mdv2007.1
+ Revision: 89239
- bot rebuild
- rebuild

* Wed Nov 29 2006 Götz Waschk <waschk@mandriva.org> 2.16.2-3mdv2007.1
+ Revision: 88538
- rebuild
- list all schema files

* Wed Nov 22 2006 Götz Waschk <waschk@mandriva.org> 2.16.2-1mdv2007.1
+ Revision: 86291
- new version

* Fri Oct 13 2006 Götz Waschk <waschk@mandriva.org> 2.16.1-3mdv2007.1
+ Revision: 63833
- rebuild
- unpack patches
- Import gnome-panel

* Fri Oct 06 2006 G�tz Waschk <waschk@mandriva.org> 2.16.1-1mdv2007.0
- drop patch 15
- New version 2.16.1

* Fri Sep 15 2006 Frederic Crozat <fcrozat@mandriva.com> 2.16.0-3mdv2007.0
- Update patch14 to no query non local file (Mdv bug #25631)

* Thu Sep 07 2006 Frederic Crozat <fcrozat@mandriva.com> 2.16.0-2mdv2007.0
- Patch15: fix crash when alacarte isn't installed (GNOME bug #354637)
- Requires alacarte

* Tue Sep 05 2006 Götz Waschk <waschk@mandriva.org> 2.16.0-1mdv2007.0
- New release 2.16.0

* Thu Aug 24 2006 Frederic Crozat <fcrozat@mandriva.com> 2.15.92-2mdv2007.0
- Switch to in-process applets for most used applets

* Wed Aug 23 2006 G�tz Waschk <waschk@mandriva.org> 2.15.92-1mdv2007.0
- drop patch 16
- New release 2.15.92

* Sat Aug 19 2006 Frederic Crozat <fcrozat@mandriva.com> 2.15.91-5mdv2007.0
- Update patch1, correctly detect menu style and merge patch15 in it

* Fri Aug 18 2006 Frederic Crozat <fcrozat@mandriva.com> 2.15.91-4mdv2007.0
- use the correct version of patch1, not an old one
- Regenerate patch15

* Thu Aug 10 2006 G�tz Waschk <waschk@mandriva.org> 2.15.91-3mdv2007.0
- rediff patch 14

* Wed Aug 09 2006 Götz Waschk <waschk@mandriva.org> 2.15.91-1mdv2007.0
- rebuild for new e-d-s

* Wed Aug 09 2006 Frederic Crozat <fcrozat@mandriva.com> 2.15.91-1mdv2007.0
- Release 2.15.91
- Regenerate patch15
- Update patch1, use MDV_MENU_STYLE env variable to disable customisations,
  use new mcc .desktop file for default panel launcher
- Remove patch 17 (merged upstream)
- Disable patch14 temporary

* Wed Aug 02 2006 Frederic Crozat <fcrozat@mandriva.com> 2.15.90-4mdv2007.0
- Rebuild with latest dbus

* Sat Jul 29 2006 Frederic Crozat <fcrozat@mandriva.com> 2.15.90-3mdv2007.0
- Patch17: fix panel going crazy when X11 is killed (GNOME bug #348803)

* Wed Jul 26 2006 G�tz Waschk <waschk@mandriva.org> 2.15.90-2mdv2007.0
- rebuild for new e-d-s

* Wed Jul 26 2006 G�tz Waschk <waschk@mandriva.org> 2.15.90-1mdv2007.0
- drop patch 17
- New release 2.15.90

* Tue Jul 18 2006 Frederic Crozat <fcrozat@mandriva.com> 2.14.2-6mdv2007.0
- Update patch1 for final XDG menu switch
- Patch17 : try to use alacarte as menu editor
- Regenerate patch15

* Sat Jun 24 2006 Frederic Crozat <fcrozat@mandriva.com> 2.14.2-5mdv2007.0
- Update patch1 with xdg menu for firefox

* Sat Jun 24 2006 Frederic Crozat <fcrozat@mandriva.com> 2.14.2-4mdv2007.0
- Switch to gnome-screensaver
- use new macros
- drop laptop hack in post, we use gnome-power-manager instead

* Sat Jun 03 2006 G�tz Waschk <waschk@mandriva.org> 2.14.2-3mdv2007.0
- rebuild for e-d-s 1.7.2

* Thu Jun 01 2006 G�tz Waschk <waschk@mandriva.org> 2.14.2-2mdv2007.0
- fix buildrequires for xorg 7
- rebuild for new e-d-s

* Wed May 31 2006 G�tz Waschk <waschk@mandriva.org> 2.14.2-1mdv2007.0
- bump deps
- New release 2.14.2

* Fri Apr 14 2006 Frederic Crozat <fcrozat@mandriva.com> 2.14.1-1mdk
- Release 2.14.1
- Regenerate patches 0, 1, 2, 14, 16
- Remove patches 6 (fixed upstream), 7 (merged upstream)

* Mon Mar 06 2006 Frederic Crozat <fcrozat@mandriva.com> 2.12.3-3mdk
- Patch16: fix transparency for tray icons (GNOME bug #100600)

* Thu Mar 02 2006 Götz Waschk <waschk@mandriva.org> 2.12.3-2mdk
- Rebuild to remove howl dep

* Tue Feb 07 2006 Götz Waschk <waschk@mandriva.org> 2.12.3-1mdk
- New release 2.12.3
- use mkrel

* Tue Dec 06 2005 Frederic Crozat <fcrozat@mandriva.com> 2.12.2-2mdk
- Update patch1, don't add two notification areas

* Wed Nov 30 2005 Frederic Crozat <fcrozat@mandriva.com> 2.12.2-1mdk
- Release 2.12.2
- Regenerate patch14

* Fri Oct 07 2005 G�tz Waschk <waschk@mandriva.org> 2.12.1-2mdk
- fix buildrequires

* Fri Oct 07 2005 Frederic Crozat <fcrozat@mandriva.com> 2.12.1-1mdk
- Release 2.12.1
- Remove patches 9, 11, 12 (merged upstream)
- Regenerate patches 0, 1, 2, 14

* Tue Sep 27 2005 Frederic Crozat <fcrozat@mandriva.com> 2.10.2-10mdk 
- Update patch14, fix for UTF8 encoded url in .desktop file

* Tue Sep 06 2005 Frederic Crozat <fcrozat@mandriva.com> 2.10.2-9mdk 
- Update patch14, display directory in shortcuts correctly

* Sat Sep 03 2005 Götz Waschk <waschk@mandriva.org> 2.10.2-8mdk
- rebuild to remove glitz dep

* Thu Sep 01 2005 Frederic Crozat <fcrozat@mandriva.com> 2.10.2-7mdk 
- Update patch15, file to check is really ~/.mdk-no-desktop-launch (Mdk bug #18070)

* Sat Aug 27 2005 Frederic Crozat <fcrozat@mandriva.com> 2.10.2-6mdk 
- Update patch14 to detect if .desktop points to existing directory
- Update patch 15, allow disabling the feature when ~/.mdk-no-desktop-launch
  file exists.

* Fri Aug 26 2005 Frederic Crozat <fcrozat@mandriva.com> 2.10.2-5mdk 
- Patch14: support .desktop as bookmarks
- Patch15: start applications in Desktop dir by default

* Fri Aug 05 2005 Frederic Crozat <fcrozat@mandriva.com> 2.10.2-4mdk 
- Patch13: fix KDE icons search (Mdk bug #17279)

* Fri Aug 05 2005 Frederic Crozat <fcrozat@mandriva.com> 2.10.2-3mdk 
- Really add patch12 this time

* Fri Aug 05 2005 Frederic Crozat <fcrozat@mandriva.com> 2.10.2-2mdk 
- Patch12 (CVS): fix executable name in .server file
- Update patch11 with crash fix (CVS)

* Wed Jun 29 2005 G�tz Waschk <waschk@mandriva.org> 2.10.2-1mdk
- drop patch 10
- New release 2.10.2

* Wed Jun 08 2005 Frederic Crozat <fcrozat@mandriva.com> 2.10.1-8mdk 
- Patch11: initially load menu in idle loop

* Thu May 26 2005 Frederic Crozat <fcrozat@mandriva.com> 2.10.1-7mdk 
- Update patch1 : use Mdk path for evolution,fix typo in default settings

* Sat May 14 2005 Frederic Crozat <fcrozat@mandriva.com> 2.10.1-6mdk 
- Patch10 (CVS): fixes various crashes 
- replace Prereq with new syntax

* Thu Apr 28 2005 Guillaume Rousse <guillomovitch@mandriva.org> 2.10.1-5mdk 
- buildrequires libglade >= 2.5.0

* Thu Apr 28 2005 Frederic Crozat <fcrozat@mandriva.com> 2.10.1-4mdk 
- Remove patch10, it is causing crashes

* Wed Apr 27 2005 Frederic Crozat <fcrozat@mandriva.com> 2.10.1-3mdk 
- Patch10 : don't keep reference on recent view

* Sun Apr 24 2005 Christiaan Welvaart <cjw@daneel.dyndns.org> 2.10.1-2mdk
- add BuildRequires: gtk-doc gnome-common intltool

* Sat Apr 23 2005 Frederic Crozat <fcrozat@mandriva.com> 2.10.1-1mdk 
- Release 2.10.1 (based on G�tz Waschk package)
- Remove source 2 (now in gnome-menus)
- Update patches 0, 2, 6
- Remove patches 3, 4, 5 (merged upstream), 7 (not applicable)
- Patch8 (CVS): update to new menu API

* Wed Mar 16 2005 Frederic Crozat <fcrozat@mandrakesoft.com> 2.8.3-6mdk 
- Patch8: fix hidden tray icons at startup (GNOME bug #108864)

* Thu Mar 10 2005 Frederic Crozat <fcrozat@mandrakesoft.com> 2.8.3-5mdk 
- Update patch3 and source4 to fix Mdk bug #12971

* Wed Mar 09 2005 Frederic Crozat <fcrozat@mandrakesoft.com> 2.8.3-4mdk 
- Update patch3 with better legacy support and fix for Mdk bug 14379
- Update source2 with more translations

* Wed Mar 02 2005 Frederic Crozat <fcrozat@mandrakesoft.com> 2.8.3-3mdk 
- Update patch1 with fixed path for MCC

* Wed Feb 16 2005 Frederic Crozat <fcrozat@mandrakesoft.com> 2.8.3-2mdk 
- Update patch1 with modified default launchers
- Update patch3 to really fix default layout order

* Tue Feb 15 2005 Frederic Crozat <fcrozat@mandrakesoft.com> 2.8.3-1mdk 
- Release 2.8.3

* Mon Feb 14 2005 Frederic Crozat <fcrozat@mandrakesoft.com> 2.8.2-9mdk 
- Update patch1 for modified location of MCC menu entry
- Update source2 to display "Core" entries
- Update patch3 with default layout fixed (menus then entries)

* Fri Feb 11 2005 Frederic Crozat <fcrozat@mandrakesoft.com> 2.8.2-8mdk 
- Add source2: ship XDG menu files for original menus

* Mon Feb 07 2005 Frederic Crozat <fcrozat@mandrakesoft.com> 2.8.2-7mdk 
- Update patch3 with new version of layout patch
- Regenerate patch1

* Fri Jan 28 2005 Frederic Crozat <fcrozat@mandrakesoft.com> 2.8.2-6mdk 
- Update patch3 to support optional part of menu spec (layout)

* Wed Jan 05 2005 Frederic Crozat <fcrozat@mandrakesoft.com> 2.8.2-5mdk 
- Rebuild with latest howl

* Tue Dec 21 2004 Frederic Crozat <fcrozat@mandrakesoft.com> 2.8.2-4mdk 
- Update patch 3 to refresh correctly menus after running update-menus

* Fri Dec 17 2004 Frederic Crozat <fcrozat@mandrakesoft.com> 2.8.2-3mdk 
- Update patch 3 with support for version 0.9 of spec and using glib 2.6.x
- Update patch 1 (mdk menu only if mdk customizations are set, 
  applications are back in the main menu)
- Add battstat applet when installing on a laptop (Fedora)
- Change default layout, back to two panels (I swear, it won't change... :)
- Patch4: fix clock format in or po file
- Patch5 (Fedora): use new configuration location (in sync with future GNOME 2.10)
- Patch6 (Novell): ignore launcher double click
- Patch7 (Novell): fix screenshot hang when destination hasn't enough perms

* Tue Dec 14 2004 Frederic Crozat <fcrozat@mandrakesoft.com> 2.8.2-2mdk 
- Patch3 (CVS): XDG menu support
- Regenerate patches 1 & 3
- Remove menu methods

* Mon Dec 06 2004 G�tz Waschk <waschk@linux-mandrake.com> 2.8.2-1mdk
- drop merged patch 3
- New release 2.8.2

* Thu Nov 11 2004 G�tz Waschk <waschk@linux-mandrake.com> 2.8.1-2mdk
- remove menu entry
- add desktop-file-utils dependancy

* Wed Nov 10 2004 G�tz Waschk <waschk@linux-mandrake.com> 2.8.1-1mdk
- add some mime support to the menu method
- fix gconf schema uninstallation
- fix omf file listing
- New release 2.8.1
- Regenerate patches 1, 2
- Remove patches 3, 4, 5, 6 (merged upstream)
- Patch3 (Fedora): fix dropping non-ASCII uris

* Tue Oct 05 2004 Frederic Crozat <fcrozat@mandrakesoft.com> 2.6.2-8mdk
- Patch6 (CVS): fix save to webpage translation (Mdk bug #11905)

* Thu Sep 30 2004 Frederic Crozat <fcrozat@mandrakesoft.com> 2.6.2-7mdk 
- Update patch2 to display Mdk logo instead of Foot (was forgotten)

* Thu Sep 23 2004 Frederic Crozat <fcrozat@mandrakesoft.com> 2.6.2-6mdk
- Patch5 (CVS): many bug fixes for clock/calendar applet (Mdk bug #11599)

* Wed Sep 01 2004 Frederic Crozat <fcrozat@mandrakesoft.com> 2.6.2-5mdk
- Patch4 (CVS): fix evolution command line parameter

* Tue Aug 24 2004 Frederic Crozat <fcrozat@mandrakesoft.com> 2.6.2-4mdk
- Patch3 (CVS): fix moving applets with middle button (Mdk bug #10921)

* Wed Aug 18 2004 Frederic Crozat <fcrozat@mandrakesoft.com> 2.6.2-3mdk 
- Update patch1 for menu changes

* Tue Aug 10 2004 Frederic Crozat <fcrozat@mandrakesoft.com> 2.6.2-2mdk
- Update patch2 to call pmsuspend (therefore it is disabled)
- Update patch1 (partially merged)
- Enable dropped requirements
- Update sources 1 & 2 to no longer use menu-link.sh

* Wed Jun 16 2004 G�tz Waschk <waschk@linux-mandrake.com> 2.6.2-1mdk
- drop merged patch 3
- New release 2.6.2

* Wed Jun 09 2004 Per �yvind Karlsen <peroyvind@linux-mandrake.com> 2.6.1-6mdk
- fix buildrequires
- cosmetics

* Mon May 24 2004 Abel Cheung <deaddog@deaddog.org> 2.6.1-5mdk
- Update patch2 (call pmsuspend2 instead of pmsuspend)
- Leave some requirements for review later
- Fix buildrequires and devel requires
- Patch3: Fix brainless translation, thus fixing schemas install

* Sun May 23 2004 G�tz Waschk <waschk@linux-mandrake.com> 2.6.1-4mdk
- reenable libtoolize
- new eds

* Sat May 01 2004 G�tz Waschk <waschk@linux-mandrake.com> 2.6.1-3mdk
- fix buildrequires

* Wed Apr 21 2004 Frederic Crozat <fcrozat@mandrakesoft.com> 2.6.1-2mdk
- Enable evolution-data-server support

* Wed Apr 21 2004 G�tz Waschk <waschk@linux-mandrake.com> 2.6.1-1mdk
- requires new GConf2
- drop merged patch 3
- rediff patch 1
- new version

* Wed Apr 07 2004 Frederic Crozat <fcrozat@mandrakesoft.com> 2.6.0-2mdk
- Fix patch 1 : still use Applications for main menu name

* Wed Apr 07 2004 Frederic Crozat <fcrozat@mandrakesoft.com> 2.6.0-1mdk
- Release 2.6.0 (with G�tz help)
- Regenerate patches 0, 1, 2
- remove patch3 (merged upstream)
- Patch3 : fix parallel build

