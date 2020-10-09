#
# spec file for package QtAV
#
# Copyright (c) 2020 UnitedRPMs
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via https://goo.gl/zqFJft
#

#define _legacy_common_support 1
%global _lto_cflags %{nil}


%global debug_package %{nil}
%global commit0 2a470d2a8d2fe22fae969bee5d594909a07b350a
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global gver .git%{shortcommit0}

%define ffmpeg_include -I%(pkg-config --variable=includedir libavutil)

Name:           qtav
Version:        1.13.0
Release:        9%{?dist}
Summary:        Qt multimedia framework
License:        LGPLv2 AND GPLv3
Group:          Applications/Multimedia
URL:            http://qtav.org/
Source0:	https://github.com/wang-bin/QtAV/archive/%{commit0}.tar.gz#/%{name}-%{shortcommit0}.tar.gz
Source1:	org.qtav.qtav.metainfo.xml	
Source2:	QtAV.svg

BuildRequires:	cmake
BuildRequires:  ImageMagick
BuildRequires:  dos2unix
BuildRequires:  hicolor-icon-theme
BuildRequires:	desktop-file-utils
BuildRequires:  kf5-filesystem
BuildRequires:  pkgconfig
BuildRequires:  portaudio-devel
BuildRequires:  libappstream-glib
BuildRequires:  pkgconfig(Qt5Core)
BuildRequires:  pkgconfig(Qt5Gui)
BuildRequires:  pkgconfig(Qt5OpenGL)
BuildRequires:  pkgconfig(Qt5Qml)
BuildRequires:  pkgconfig(Qt5Quick)
BuildRequires:  pkgconfig(Qt5Sql)
BuildRequires:  pkgconfig(Qt5Svg)
BuildRequires:  pkgconfig(Qt5Widgets)
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(libass)
BuildRequires:  pkgconfig(libavcodec)
BuildRequires:  pkgconfig(libavdevice)
BuildRequires:  pkgconfig(libavfilter)
BuildRequires:  pkgconfig(libavformat)
BuildRequires:  pkgconfig(libavresample)
BuildRequires:  pkgconfig(libavutil)
BuildRequires:  pkgconfig(libpulse) >= 1.0
BuildRequires:  pkgconfig(libswresample)
BuildRequires:  pkgconfig(libswscale)
BuildRequires:  pkgconfig(libva)
BuildRequires:  pkgconfig(openal)
BuildRequires:  pkgconfig(xv)
BuildRequires:	ffmpeg-devel >= 4.3 

%description
QtAV is a multimedia playback library based on Qt and FFmpeg. It can help
facilitate writing a player application.


%package        devel
Summary:        Development package for %{name}
Requires:       %{name} = %{version}-%{release}

%description  devel
QtAV is a multimedia playback library based on Qt and FFmpeg.

This package contains the header development files for building some QtAV
applications using QtAV headers.

%prep
%autosetup -n QtAV-%{commit0}

# We need put the path of our ffmpeg
find . -type f -name \*.pro | while read FILE; do
echo "QMAKE_CXXFLAGS_RELEASE += %{ffmpeg_include}" >> "$FILE"; done

# Fix incorrect sRGB profile
for f in $(find . -type f -name \*.png); do
convert $f -strip $f
done

sed -i 's|/lib|/lib64|g' CMakeLists.txt

%build
mkdir -p %{_target_platform}; cd %{_target_platform}
cmake -DCMAKE_INSTALL_PREFIX="/usr" -DCMAKE_INSTALL_LIBDIR=%{_libdir} -DBUILD_PLAYERS=ON -DBUILD_QT5OPENGL=ON -DHAVE_PORTAUDIO=ON -DHAVE_PULSE=ON -DHAVE_VAAPI=ON -DBUILD_TESTS=OFF -DBUILD_EXAMPLES=OFF ..
		
#pushd %{_target_platform}

%make_build

%install
pushd %{_target_platform}
%make_install INSTALL_ROOT=%{buildroot}
popd


find %{buildroot} -name \*.a -exec rm {} \;


# duplicate files
#rm -rf  %{buildroot}/%{_datadir}/doc

mkdir -p %{buildroot}/%{_datadir}/applications/ \
mkdir -p %{buildroot}/%{_datadir}/icons/hicolor/scalable/apps/


cp -f %{_builddir}/QtAV-%{commit0}/qtc_packaging/debian_generic/*.desktop %{buildroot}/%{_datadir}/applications/

cp -f %{S:2} %{buildroot}/%{_datadir}/icons/hicolor/scalable/apps/

# Appdata
install -Dm 0644 %{S:1} %{buildroot}/%{_metainfodir}/org.qtav.qtav.metainfo.xml

install -d %{buildroot}/%{_bindir}
#pushd %{buildroot}/%{_bindir}
#ln -s %{_libdir}/qt5/bin/Player Player
#ln -s %{_libdir}/qt5/bin/QMLPlayer QMLPlayer
#popd

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/Player.desktop
desktop-file-validate %{buildroot}%{_datadir}/applications/QMLPlayer.desktop
appstream-util validate-relax --nonet %{buildroot}/%{_metainfodir}/org.qtav.qtav.metainfo.xml


%files
%license gpl-3.0* lgpl-2.1*
%doc Changelog README*
%{_bindir}/Player
%{_bindir}/QMLPlayer
%{_datadir}/applications/Player.desktop
%{_datadir}/applications/QMLPlayer.desktop
%{_datadir}/icons/hicolor/scalable/apps/QtAV.svg
%{_libdir}/libQtAV.so.*
%{_libdir}/libQtAVWidgets.so.*
%{_libdir}/qml/QtAV/
%{_metainfodir}/org.qtav.qtav.metainfo.xml

%files devel
%{_includedir}/QtAV/
%{_includedir}/QtAVWidgets/
%{_libdir}/libQtAV.so
%{_libdir}/libQtAVWidgets.so
%{_libdir}/cmake/


%changelog

* Mon Oct 05 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.13.0-9
- Updated to current commit

* Sun Jul 05 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.13.0-8
- Rebuilt for ffmpeg

* Fri May 01 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.13.0-7
- Updated to current commit

* Sun Apr 05 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.13.0-2
- Fix paths

* Tue Jan 28 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.13.0-1
- Initial build
