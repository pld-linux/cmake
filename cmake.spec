# TODO:
# - any valid CMAKE_BUILD_TYPE causes overriding of our optflags
#   (and default non-verbose makefiles are hiding it!)
# - rpmldflags/rpmcppflags are not passed through %%cmake macro at all
#   (is there any standard way???)
#
# Conditional build:
%bcond_with	bootstrap	# use internal versions of some libraries
%bcond_without	gui		# don't build gui package
%bcond_without	tests

Summary:	Cross-platform, open-source make system
Summary(pl.UTF-8):	Wieloplatformowy system make o otwartych źródłach
Name:		cmake
Version:	2.8.11.1
Release:	2
License:	BSD
Group:		Development/Building
Source0:	http://www.cmake.org/files/v2.8/%{name}-%{version}.tar.gz
# Source0-md5:	df5324a3b203373a9e0a04b924281a43
Patch0:		%{name}-lib64.patch
Patch1:		%{name}-helpers.patch
Patch2:		cmake-findruby.patch
Patch3:		cmake-git.patch
URL:		http://www.cmake.org/
%{?with_gui:BuildRequires:	QtGui-devel}
BuildRequires:	libarchive-devel
BuildRequires:	libstdc++-devel
BuildRequires:	ncurses-devel > 5.9-3
%{?with_gui:BuildRequires:	qt4-build}
%{?with_gui:BuildRequires:	qt4-qmake}
BuildRequires:	rpmbuild(macros) >= 1.167
%{!?with_bootstrap:BuildRequires:	xmlrpc-c-devel >= 1.4.12-2}
Requires:	filesystem >= 3.0-52
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
użyciu prostych plików konfiguracyjnych niezależnych od platformy i
kompilatora. CMake generuje natywne pliki makefile i workspace,
których można używać w wybranym środowisku kompilatora. CMake jest
dość wyrafinowany: może obsłużyć złożone środowiska wymagające
konfiguracji systemu, generowanie preprocesora, generowanie kodu i
dziedziczenie szablonów.

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

%package emacs
Summary:	Emacs mode for cmake files
Summary(pl.UTF-8):	Tryb Emacsa dla plików cmake'a
Group:		Development/Tools

%description emacs
Emacs mode for cmake files.

%description emacs -l pl.UTF-8
Tryb Emacsa dla plików cmake'a.

%package -n bash-completion-%{name}
Summary:	bash-completion for cmake
Summary(pl.UTF-8):	Bashowe dopełnianie parametrów dla cmake'a
Group:		Applications/Shells
Requires:	%{name} = %{version}-%{release}

%description -n bash-completion-%{name}
bash-completion for cmake.

%description -n bash-completion-%{name} -l pl.UTF-8
Bashowe dopełnianie parametrów dla cmake'a.

%prep
%setup -q
%if "%{_lib}" == "lib64"
%patch0 -p1
%endif
%patch1 -p1
%patch2 -p1
%patch3 -p1

cat > "init.cmake" <<EOF
SET (CURSES_INCLUDE_PATH "/usr/include/ncurses" CACHE PATH " " FORCE)
SET (CMAKE_INSTALL_SYSCONFDIR "%{_sysconfdir}" CACHE PATH " " FORCE)
SET (CMAKE_INSTALL_DATADIR "%{_datadir}" CACHE PATH " " FORCE)
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
	--qt-qmake=/usr/bin/qmake-qt4 \
	--verbose

%{__make} VERBOSE=1

%{?with_tests:%{__make} test}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} -r $RPM_BUILD_ROOT%{_prefix}/doc

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc ChangeLog.* Copyright.txt *.gif Docs/{cmake,ctest}.{txt,html}
%attr(755,root,root) %{_bindir}/ccmake
%attr(755,root,root) %{_bindir}/cmake
%attr(755,root,root) %{_bindir}/cpack
%attr(755,root,root) %{_bindir}/ctest
%{_mandir}/man1/ccmake.1*
%{_mandir}/man1/cmake.1*
%{_mandir}/man1/cmakecommands.1*
%{_mandir}/man1/cmakecompat.1*
%{_mandir}/man1/cmakemodules.1*
%{_mandir}/man1/cmakepolicies.1*
%{_mandir}/man1/cmakeprops.1*
%{_mandir}/man1/cmakevars.1*
%{_mandir}/man1/cpack.1*
%{_mandir}/man1/ctest.1*
# top cmake/Modules dirs belong to filesystem
%{_datadir}/cmake/Modules/.NoDartCoverage
%{_datadir}/cmake/Modules/*
%{_datadir}/cmake/Templates
%{_datadir}/cmake/editors
%{_datadir}/cmake/include
%{_aclocaldir}/cmake.m4

%if %{with gui}
%files gui
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/cmake-gui
%{_datadir}/mime/packages/cmakecache.xml
%{_desktopdir}/CMake.desktop
%{_pixmapsdir}/CMakeSetup32.png
%{_mandir}/man1/cmake-gui.1*
%endif

%files emacs
%defattr(644,root,root,755)
%{_datadir}/emacs/site-lisp/cmake-mode.el

%files -n bash-completion-%{name}
%defattr(644,root,root,755)
/etc/bash_completion.d/cmake
/etc/bash_completion.d/cpack
/etc/bash_completion.d/ctest
