%global git_commit 0a1b50503bdf202fb6fa7ca62124b0242a004e69
%global commit_short_form %(c=%{git_commit}; echo ${c:0:7})
%define _applicationsdir %{_datadir}/applications
%define _iconsdir %{_datadir}/icons/hicolor

Name:		xephem
Version:	4.1.0+git%{commit_short_form}
Release:	1%{?dist}
Summary:	Scientific-grade interactive astronomical ephemeris software

License:	MIT-advertising and LGPL-2.1-or-later
URL:		https://github.com/XEphem/XEphem

# The source for this package was pulled from upstream's vcs. Use the
# script xephem-get-orig-source.sh to generate the tarball.
Source0:	%{name}-%{version}.tar.xz
Source1:	xephem-get-orig-source.sh
Source2:	version.sh
Patch1:		001-xephem-adjustment-in-manpage.patch
Patch2:		002-xephem-adjust-path-for-awk.patch
Patch3:		003-xephem-fix-spelling-error-in-binary.patch
Patch4:		004-xephem-fix-gsc23.patch
Patch5:		005-fifos-reubication.patch
Patch6:		006-xephem-declaration-strptime.patch
Patch7:		007-xephem-manage-desktopfiles.patch
Patch8:		008-xephem-add-build-installation-with-support-multiarch_rpm.patch
Patch9:		009-xephem-safe-build-parallel.patch
Patch10:	010-xephem-update-address-lgpl2.1.patch

BuildRequires:	make
BuildRequires:	gcc
BuildRequires:	libjpeg-turbo-devel
BuildRequires:	libpng-devel
BuildRequires:	libXext-devel
BuildRequires:	libXmu-devel
BuildRequires:	libXt-devel
BuildRequires:	motif-devel
BuildRequires:	openssl-devel
BuildRequires:	zlib-devel
BuildRequires:	ImageMagick
BuildRequires:	desktop-file-utils
BuildRequires:	libappstream-glib

Requires:	curl

%description
XEphem is an interactive astronomy program for all UNIX platforms,
written and maintained by Elwood Downey over more than thirty years
1990–2021 and now generously released under the MIT License.

XEphem can compute information on demand or time can be set to
increment automatically. In this way a series of computations and
movies can be generated.

%package data
Summary:	XEphem data files
Requires:	%{name} = %{version}-%{release}
BuildArch:	noarch

%description data
This package contains data-files which are used by xephem.

%prep
%setup -q
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1

%build
%make_build -C GUI/xephem RPM_HOST_MULTIARCH="%{_libdir}" RPM_CFLAGS="%{build_cflags}" RPM_LDFLAGS="%{build_ldflags}"

# Copy licenses in the code
cp LICENSE LICENSE_%{name}
cp liblilxml/LICENSE LICENSE_liblilxml

%install
rm -rf %{buildroot}
%make_install -C GUI/xephem prefix=%{_prefix}

# Create/install file configuration
mkdir -p %{buildroot}%{_sysconfdir}
cat > %{buildroot}%{_sysconfdir}/XEphem <<EOF
XEphem.ShareDir: %{_datadir}/%{name}
EOF

%check
desktop-file-validate %{buildroot}%{_applicationsdir}/%{name}.desktop
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/%{name}.metainfo.xml

%files
%license LICENSE_%{name} LICENSE_liblilxml
%doc README.md
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*
%{_applicationsdir}/%{name}.desktop
%{_metainfodir}/%{name}.metainfo.xml
%{_iconsdir}/*/apps/%{name}.png
%config(noreplace) %{_sysconfdir}/XEphem

%files data
%{_datadir}/%{name}

%changelog
* Sat Feb 18 2023 Miguel Molina <mmolina.unphysics@gmail.com> - 4.1.0+git0a1b505-1%{?dist}
- Initial packaging for test purpose.
- Fixed spelling errors in binary file.
- Added support multiarch for package build in the Makefile upstream
  in according to owned packaging guidelines of this distribution.
- Added manage for desktop files and metadata files.
- Bugs fixed from patches proposed by various authors. Credits for
  Richard J. Mathar, Lukasz Sanocki, Mattia Verga and Florian Weimer.
* Fri Mar 05 2021 Douglas Needham <cinnion+github@gmail.com> - 4.0.1-1
- New RPM package built with tito
