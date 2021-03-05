Summary:	Qt based GUI for GNU Gama project
Summary(pl.UTF-8):	Oparty na Qt graficzny interfejs do projektu GNU Gama
Name:		gama-qt
Version:	1.03
%define	fver	%(echo %{version} | tr . -)
%define	gama_ver	2.13
Release:	1
License:	GPL v3+
Group:		Applications/Science
Source0:	https://ftp.gnu.org/gnu/gama/gama-qt/qt-gama-qt-%{fver}.tar.gz
# Source0-md5:	0bc18d72824037717582a75863965f66
Source1:	https://ftp.gnu.org/gnu/gama/gama-%{gama_ver}.tar.gz
# Source1-md5:	bc0f6c70c10bd14663c7033d0a10085b
Patch0:		%{name}-system-expat.patch
URL:		http://www.gnu.org/software/gama/
BuildRequires:	Qt5Core-devel >= 5
BuildRequires:	Qt5Gui-devel >= 5
BuildRequires:	Qt5PrintSupport-devel >= 5
BuildRequires:	Qt5Sql-devel >= 5
BuildRequires:	Qt5Svg-devel >= 5
BuildRequires:	Qt5Widgets-devel >= 5
BuildRequires:	cmake >= 3.5
BuildRequires:	expat-devel
BuildRequires:	libstdc++-devel >= 6:5
BuildRequires:	qt5-build >= 5
BuildRequires:	sed >= 4.0
BuildRequires:	sqlite3-devel >= 3
BuildRequires:	yaml-cpp-devel
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
%setup -q -n qt-gama-qt-%{fver} -a1
ln -s gama-%{gama_ver} gama
%patch0 -p1

%define qt5_ver	%(rpm -q Qt5Core-devel)
%if "%{_ver_lt '%{qt5_ver}' '5.15'}" == "1"
%{__sed} -i -e 's/Qt::SkipEmptyParts/QString::SkipEmptyParts/' gama-q2/{gamaq2controlpanel,networkadjustmentpanel}.cpp
%endif

%build
install -d build
cd build
%cmake ..

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

# already in gama
%{__rm} $RPM_BUILD_ROOT%{_bindir}/gama-{g3,local}

# missing in make install
install build/gama-q2 $RPM_BUILD_ROOT%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc QuickStart.txt
%attr(755,root,root) %{_bindir}/gama-q2
