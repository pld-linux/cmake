# TODO:
# - any valid CMAKE_BUILD_TYPE causes overriding of our optflags
#   (and default non-verbose makefiles are hiding it!)
# - rpmldflags/rpmcppflags are not passed through %%cmake macro at all
#   (is there any standard way???)
#
# Conditional build:
%bcond_with	bootstrap	# use internal versions of some libraries
%bcond_without	gui		# don't build gui package
#
Summary:	Cross-platform, open-source make system
Summary(pl.UTF-8):	Wieloplatformowy system make o otwartych źródłach
Name:		cmake
Version:	2.6.3
Release:	1
License:	BSD
Group:		Development/Building
Source0:	http://www.cmake.org/files/v2.6/%{name}-%{version}.tar.gz
# Source0-md5:	5ba47a94ce276f326abca1fd72a7e7c6
Patch0:		%{name}-lib64.patch
URL:		http://www.cmake.org/
%{?with_gui:BuildRequires:	QtGui-devel}
BuildRequires:	libstdc++-devel
BuildRequires:	ncurses-devel
%{?with_gui:BuildRequires:	qt4-build}
%{?with_gui:BuildRequires:	qt4-qmake}
BuildRequires:	rpmbuild(macros) >= 1.167
%{!?with_bootstrap:BuildRequires:	xmlrpc-c-devel >= 1.4.12-2}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
CMake is used to control the software compilation process using simple
platform and compiler independent configuration files. CMake generates
native makefiles and workspaces that can be used in the compiler
environment of your choice. CMake is quite sophisticated: it is
possible to support complex environments requiring system
configuration, pre-processor generation, code generation, and template
instantiation.

%description -l pl.UTF-8
CMake służy do sterowania procesem kompilacji oprogramowania przy
użyciu prostych plików konfiguracyjnych niezależnych od platformy
i kompilatora. CMake generuje natywne pliki makefile i workspace,
których można używać w wybranym środowisku kompilatora. CMake jest
dość przemyślany: może obsłużyć złożone środowiska wymagające
konfiguracji systemu, generowanie preprocesora, generowanie kodu
i dziedziczenie szablonów.

%package gui
Summary:	Qt GUI for CMake
Summary(pl.UTF-8):	Graficzny interfejs użytkownika Qt dla CMake
Group:		Development/Tools
Requires:	%{name} = %{version}-%{release}

%description gui
This package contains the Qt based GUI for CMake.

%description gui -l pl.UTF-8
Ten pakiet zawiera oparty na Qt graficzny interfejs użytkownika dla
CMake.

%prep
%setup -q
%if "%{_lib}" == "lib64"
%patch0 -p1
%endif

cat > "init.cmake" <<EOF
SET (CURSES_INCLUDE_PATH "/usr/include/ncurses" CACHE PATH " " FORCE)
EOF

%build
export CC="%{__cc}"
export CXX="%{__cxx}"
export CFLAGS="%{rpmcflags}"
export CXXFLAGS="%{rpmcxxflags}"
export LDFLAGS="%{rpmldflags}"
./bootstrap \
	--prefix=%{_prefix} \
	--mandir=/share/man \
	--datadir=/share/cmake \
	--init=init.cmake \
	%{!?with_bootstrap:--system-libs} \
	%{?with_gui:--qt-gui} \
	--verbose

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

rm -rf $RPM_BUILD_ROOT%{_prefix}/doc

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc ChangeLog.* Copyright.txt *.gif Docs/{cmake,ctest}.{txt,html}
%attr(755,root,root) %{_bindir}/ccmake
%attr(755,root,root) %{_bindir}/cmake
%attr(755,root,root) %{_bindir}/cpack
%attr(755,root,root) %{_bindir}/ctest
%{_mandir}/man1/*.1*
%{_datadir}/cmake

%files gui
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/cmake-gui
%{_datadir}/mime/packages/cmakecache.xml
%{_desktopdir}/CMake.desktop
%{_pixmapsdir}/CMakeSetup.png
