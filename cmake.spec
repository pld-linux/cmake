Summary:	Cross-platform, open-source make system
Summary(pl.UTF-8):	Wieloplatformowy system make o otwartych źródłach
Name:		cmake
Version:	2.4.8
Release:	1
License:	BSD
Group:		Development/Building
Source0:	http://www.cmake.org/files/v2.4/%{name}-%{version}.tar.gz
# Source0-md5:	f5dd061c31765a49dc17ae8bdc986779
Patch0:		%{name}-ncurses.patch
Patch1:		%{name}-lib64.patch
URL:		http://www.cmake.org/HTML/Index.html
BuildRequires:	libstdc++-devel
BuildRequires:	ncurses-devel
BuildRequires:	rpmbuild(macros) >= 1.167
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
dość przemyślany: może obsłużyć złożone środowiska wymagające
konfiguracji systemu, generowanie preprocesora, generowanie kodu i
dziedziczenie szablonów.

%prep
%setup -q
%patch0 -p1
%if "%{_lib}" == "lib64"
%patch1 -p1
%endif

cat > "init.cmake" <<EOF
SET (CURSES_INCLUDE_PATH "/usr/include/ncurses" CACHE PATH " " FORCE)
EOF

%build
export CC="%{__cc}"
export CXX="%{__cxx}"
export CFLAGS="%{rpmcflags}"
export CXXFLAGS="%{rpmcxxflags}"
./bootstrap \
	--prefix=%{_prefix} \
	--mandir=/share/man \
	--datadir=/share/cmake \
	--init=init.cmake \
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
