# TODO:
# - extend libx32 patch to work also on 64-bit arch
# - any valid CMAKE_BUILD_TYPE causes overriding of our optflags
#   (and default non-verbose makefiles are hiding it!)
# - rpmldflags/rpmcppflags are not passed through %%cmake macro at all
#   (is there any standard way???)
#
# Conditional build:
%bcond_with	bootstrap	# use internal versions of some libraries
%bcond_without	gui		# don't build gui package
%bcond_with	tests		# perform "make test"
%bcond_without	doc		# don't build documentation

Summary:	Cross-platform, open-source make system
Summary(pl.UTF-8):	Wieloplatformowy system make o otwartych źródłach
Name:		cmake
Version:	3.2.2
Release:	1
License:	BSD
Group:		Development/Building
Source0:	http://www.cmake.org/files/v3.2/%{name}-%{version}.tar.gz
# Source0-md5:	2da57308071ea98b10253a87d2419281
Patch0:		%{name}-lib64.patch
Patch1:		%{name}-helpers.patch
Patch2:		%{name}-findruby.patch
Patch3:		%{name}-tests.patch

Patch5:		%{name}-findruby2.patch
Patch6:		%{name}-findpython.patch
Patch7:		%{name}-libx32.patch
URL:		http://www.cmake.org/
%{?with_gui:BuildRequires:	QtGui-devel}
BuildRequires:	jsoncpp-devel >= 1.6.2-2
BuildRequires:	libarchive-devel
BuildRequires:	libstdc++-devel
BuildRequires:	ncurses-devel > 5.9-3
%{?with_gui:BuildRequires:	qt5-build}
%{?with_gui:BuildRequires:	qt5-qmake}
BuildRequires:	rpmbuild(macros) >= 1.167
%{?with_doc:BuildRequires:	sphinx-pdg}
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

%package doc-html
Summary:	CMake documentation in HTML format
Summary(pl.UTF-8):	Dokumentacja do pakietu CMake w formacie HTML
Group:		Documentation

%description doc-html
CMake documentation in HTML format.

%description doc-html -l pl.UTF-8
Dokumentacja do pakietu CMake w formacie HTML.

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
Requires:	bash-completion >= 2.0
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

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

%patch5 -p1
%patch6 -p1
%if "%{_lib}" == "libx32"
%patch7 -p1
%endif

cat > "init.cmake" <<EOF
SET (CURSES_INCLUDE_PATH "/usr/include/ncurses" CACHE PATH " " FORCE)
SET (CMAKE_INSTALL_SYSCONFDIR "%{_sysconfdir}" CACHE PATH " " FORCE)
SET (CMAKE_INSTALL_DATADIR "%{_datadir}" CACHE PATH " " FORCE)
EOF

# cleanup backups after patching, modules are copied as-is
find '(' -name '*~' -o -name '*.orig' ')' -print0 | xargs -0 -r -l512 rm -f

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
	--qt-qmake=%{_bindir}/qmake-qt4 \
	%{?with_doc:--sphinx-html} \
	%{?with_doc:--sphinx-man} \
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
%doc Copyright.txt README.rst *.gif
%attr(755,root,root) %{_bindir}/ccmake
%attr(755,root,root) %{_bindir}/cmake
%attr(755,root,root) %{_bindir}/cpack
%attr(755,root,root) %{_bindir}/ctest
%if %{with doc}
%{_mandir}/man1/ccmake.1*
%{_mandir}/man1/cmake.1*
%{_mandir}/man1/cpack.1*
%{_mandir}/man1/ctest.1*
%{_mandir}/man7/cmake-buildsystem.7*
%{_mandir}/man7/cmake-commands.7*
%{_mandir}/man7/cmake-compile-features.7*
%{_mandir}/man7/cmake-developer.7*
%{_mandir}/man7/cmake-generator-expressions.7*
%{_mandir}/man7/cmake-generators.7*
%{_mandir}/man7/cmake-language.7*
%{_mandir}/man7/cmake-modules.7*
%{_mandir}/man7/cmake-packages.7*
%{_mandir}/man7/cmake-policies.7*
%{_mandir}/man7/cmake-properties.7*
%{_mandir}/man7/cmake-qt.7*
%{_mandir}/man7/cmake-toolchains.7*
%{_mandir}/man7/cmake-variables.7*
%{_datadir}/cmake/Help
%endif
# top cmake/Modules dirs belong to filesystem
%{_datadir}/cmake/Modules/.NoDartCoverage
%{_datadir}/cmake/Modules/*
%{_datadir}/cmake/Templates
%{_datadir}/cmake/editors
%{_datadir}/cmake/include
%{_aclocaldir}/cmake.m4

%if %{with doc}
%files doc-html
%defattr(644,root,root,755)
%doc Utilities/Sphinx/html/*
%endif

%if %{with gui}
%files gui
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/cmake-gui
%{_datadir}/mime/packages/cmakecache.xml
%{_desktopdir}/CMake.desktop
%{_iconsdir}/hicolor/128x128/apps/CMakeSetup.png
%{_iconsdir}/hicolor/32x32/apps/CMakeSetup.png
%{_mandir}/man1/cmake-gui.1*
%endif

%files emacs
%defattr(644,root,root,755)
%{_datadir}/emacs/site-lisp/cmake-mode.el

%files -n bash-completion-%{name}
%defattr(644,root,root,755)
%{bash_compdir}/cmake
%{bash_compdir}/cpack
%{bash_compdir}/ctest
