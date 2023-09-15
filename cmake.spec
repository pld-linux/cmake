# TODO:
# - system kwiml >= 1.0?
# - make lib64/libx32 patch changes applicable everywhere
# - any valid CMAKE_BUILD_TYPE causes overriding of our optflags
#   (and default non-verbose makefiles are hiding it!)
# - rpmldflags/rpmcppflags are not passed through %%cmake macro at all
#   (is there any standard way???)
# - FindJNI.cmake module is a PoS full of random incorrect paths,
#   needs lib64/libx32 awareness
#
# Conditional build:
%bcond_with	bootstrap	# use internal versions of some libraries
%bcond_without	gui		# gui package
%bcond_with	tests		# perform "make test"
%bcond_without	doc		# documentation

Summary:	Cross-platform, open-source make system
Summary(pl.UTF-8):	Wieloplatformowy system make o otwartych źródłach
Name:		cmake
Version:	3.27.5
Release:	1
License:	BSD
Group:		Development/Building
Source0:	https://cmake.org/files/v3.27/%{name}-%{version}.tar.gz
# Source0-md5:	fbda83fa70276f6971cab8cdb1407191
Patch0:		%{name}-lib64.patch
Patch1:		%{name}-libx32.patch
Patch2:		%{name}-jni.patch
Patch3:		%{name}-findruby.patch
Patch4:		%{name}-findruby2.patch
Patch5:		disable-completness-check.patch
URL:		https://cmake.org/
# system zlib,bzip2,xz,zstd used only when without system libarchive
%if %{with gui}
BuildRequires:	Qt5Core-devel >= 5.0
BuildRequires:	Qt5Gui-devel >= 5.0
BuildRequires:	Qt5Widgets-devel >= 5.0
%endif
BuildRequires:	automake
BuildRequires:	cppdap-devel
BuildRequires:	curl-devel
BuildRequires:	expat-devel
BuildRequires:	jsoncpp-devel >= 1.6.2-2
BuildRequires:	libarchive-devel >= 3.3.3
%ifnarch %arch_with_atomics64
BuildRequires:	libatomic-devel
%endif
BuildRequires:	libstdc++-devel >= 6:4.7
BuildRequires:	libuv-devel >= 1.28.0
BuildRequires:	ncurses-devel > 5.9-3
BuildRequires:	ncurses-ext-devel > 5.9-3
BuildRequires:	nghttp2-devel
%{?with_gui:BuildRequires:	qt5-build >= 5.0}
%{?with_gui:BuildRequires:	qt5-qmake >= 5.0}
BuildRequires:	rhash-devel
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 2.025
%{?with_doc:BuildRequires:	sphinx-pdg}
BuildRequires:	xz-devel
BuildRequires:	zlib-devel
BuildRequires:	zstd-devel
Requires:	filesystem >= 3.0-52
Requires:	libarchive >= 3.3.3
Requires:	libuv >= 1.28.0
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
Requires(post,postun):	desktop-file-utils
Requires(post,postun):	gtk-update-icon-cache
Requires:	%{name} = %{version}-%{release}
Requires:	hicolor-icon-theme

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
Requires:	bash-completion >= 1:2.0
BuildArch:	noarch

%description -n bash-completion-%{name}
bash-completion for cmake.

%description -n bash-completion-%{name} -l pl.UTF-8
Bashowe dopełnianie parametrów dla cmake'a.

%prep
%setup -q
%if "%{_lib}" == "lib64"
%patch0 -p1
%endif
%if "%{_lib}" == "libx32"
%patch1 -p1
%endif
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

%{__sed} -i -e '1s,/usr/bin/env bash,/bin/bash,' \
	Modules/Compiler/XL-Fortran/cpp

cat > "init.cmake" <<EOF
SET (CURSES_INCLUDE_PATH "/usr/include/ncurses" CACHE PATH " " FORCE)
SET (CMAKE_INSTALL_SYSCONFDIR "%{_sysconfdir}" CACHE PATH " " FORCE)
SET (CMAKE_INSTALL_DATADIR "%{_datadir}" CACHE PATH " " FORCE)
SET (CMAKE_SYSTEM_NAME "Linux" CACHE STRING " " FORCE)
SET (CMAKE_SYSTEM_VERSION "%(uname -r)" CACHE STRING " " FORCE)
SET (CMAKE_CROSSCOMPILING FALSE CACHE BOOL " " FORCE)
%ifarch x32
SET (CMAKE_SYSTEM_PROCESSOR "x86_64" CACHE STRING " " FORCE)
%else
SET (CMAKE_SYSTEM_PROCESSOR "%{_target_cpu}" CACHE STRING " " FORCE)
%endif
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
	--qt-qmake=%{_bindir}/qmake-qt5 \
	%{?with_doc:--sphinx-html} \
	%{?with_doc:--sphinx-man} \
	%{?__jobs:--parallel=%{__jobs}} \
	--verbose

%{__make} \
	VERBOSE=1

%{?with_tests:%{__make} test}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# just a bit more recent than packaged in vim.spec
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/vim
# packaged as %doc
%{__rm} -r $RPM_BUILD_ROOT%{_prefix}/doc

%clean
rm -rf $RPM_BUILD_ROOT

%post gui
%update_desktop_database_post
%update_icon_cache hicolor

%postun gui
%update_desktop_database_postun
%update_icon_cache hicolor

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
%{_mandir}/man7/cpack-generators.7*
%{_mandir}/man7/cmake-buildsystem.7*
%{_mandir}/man7/cmake-commands.7*
%{_mandir}/man7/cmake-compile-features.7*
%{_mandir}/man7/cmake-configure-log.7*
%{_mandir}/man7/cmake-developer.7*
%{_mandir}/man7/cmake-env-variables.7*
%{_mandir}/man7/cmake-file-api.7*
%{_mandir}/man7/cmake-generator-expressions.7*
%{_mandir}/man7/cmake-generators.7*
%{_mandir}/man7/cmake-language.7*
%{_mandir}/man7/cmake-modules.7*
%{_mandir}/man7/cmake-packages.7*
%{_mandir}/man7/cmake-policies.7*
%{_mandir}/man7/cmake-presets.7*
%{_mandir}/man7/cmake-properties.7*
%{_mandir}/man7/cmake-qt.7*
%{_mandir}/man7/cmake-server.7*
%{_mandir}/man7/cmake-toolchains.7*
%{_mandir}/man7/cmake-variables.7*
%{_datadir}/cmake/Help
%endif
# top cmake/Modules dirs belong to filesystem
%{_datadir}/cmake/Modules/.NoDartCoverage
%{_datadir}/cmake/Modules/*
%{_datadir}/cmake/Templates
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
%{_desktopdir}/cmake-gui.desktop
%{_iconsdir}/hicolor/128x128/apps/CMakeSetup.png
%{_iconsdir}/hicolor/32x32/apps/CMakeSetup.png
%if %{with doc}
%{_mandir}/man1/cmake-gui.1*
%endif
%endif

%files emacs
%defattr(644,root,root,755)
%{_datadir}/emacs/site-lisp/cmake-mode.el

%files -n bash-completion-%{name}
%defattr(644,root,root,755)
%{bash_compdir}/cmake
%{bash_compdir}/cpack
%{bash_compdir}/ctest
