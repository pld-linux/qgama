Summary:	Qt based GUI for GNU Gama project
Summary(pl.UTF-8):	Oparty na Qt graficzny interfejs do projektu GNU Gama
Name:		qgama
Version:	2.08
%define	gama_ver	2.32
Release:	1
License:	GPL v3+
Group:		Applications/Science
Source0:	https://ftp.gnu.org/gnu/gama/qgama/%{name}-%{version}.tar.gz
# Source0-md5:	79048fab55bcfabd6e55ff8a7266f253
Source1:	https://ftp.gnu.org/gnu/gama/gama-%{gama_ver}.tar.gz
# Source1-md5:	93c0b0b13ad802a71a40958f812b0e97
Patch0:		%{name}-system-expat.patch
Patch1:		gama-cmake.patch
URL:		http://www.gnu.org/software/gama/
BuildRequires:	Qt6Core-devel >= 6
BuildRequires:	Qt6Gui-devel >= 6
BuildRequires:	Qt6PrintSupport-devel >= 6
BuildRequires:	Qt6Sql-devel >= 6
BuildRequires:	Qt6Widgets-devel >= 6
BuildRequires:	cmake >= 3.18
BuildRequires:	expat-devel
BuildRequires:	libstdc++-devel >= 6:7
BuildRequires:	qt6-build >= 6
BuildRequires:	sqlite3-devel >= 3
# vendored in gama 2.32
#BuildRequires:	yaml-cpp-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
GNU Gama package is dedicated to adjustment of geodetic networks. It
is intended for use with traditional geodetic surveyings which are
still used and needed in special measurements (e.g., underground or
high precision engineering measurements) where the Global Positioning
System (GPS) cannot be used.

%description -l pl.UTF-8
Pakiet GNU Gama służy do wyrównywania sieci geodezyjnych. Jest
przeznaczony do użycia w tradycyjnych badaniach geodezyjnych, które są
nadal używane w specjalnych pomiarach (np. podziemnych lub
precyzyjnych pomiarach inżynierskich), gdzie nie można użyć GPS-a
(Global Positioning System).

%prep
%setup -q -n qt-qgama-%{version} -a1
ln -s gama-%{gama_ver} gama
%patch -P0 -p1
%patch -P1 -p0

%build
%cmake -B build \
	-DENABLE_EXPAT_1_1=OFF

%{__make} -C build

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

# already in gama
%{__rm} $RPM_BUILD_ROOT%{_bindir}/{compare-xyz,krumm2gama-local}
%{__rm} $RPM_BUILD_ROOT%{_bindir}/gama-{g3,local,local-gkf2yaml}

# make install is broken
install build/qgama $RPM_BUILD_ROOT%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc ChangeLog.md QuickStart.md README.md
%attr(755,root,root) %{_bindir}/qgama
