Summary:	Cross-platform, open-source make system
Summary(pl):	Wieloplatformowy system make o otwartych ¼ród³ach
Name:		cmake
Version:	2.4.6
Release:	1
License:	BSD
Group:		Development/Building
Source0:	http://www.cmake.org/files/v2.4/%{name}-%{version}.tar.gz
# Source0-md5:	c99c747ad8e9bfb3bef9cca875a52129
Patch0:		%{name}-ncurses.patch
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

%description -l pl
CMake s³u¿y do sterowania procesem kompilacji oprogramowania przy
u¿yciu prostych plików konfiguracyjnych niezale¿nych od platformy i
kompilatora. CMake generuje natywne pliki makefile i workspace,
których mo¿na u¿ywaæ w wybranym ¶rodowisku kompilatora. CMake jest
do¶æ przemy¶lany: mo¿e obs³u¿yæ z³o¿one ¶rodowiska wymagaj±ce
konfiguracji systemu, generowanie preprocesora, generowanie kodu i
dziedziczenie szablonów.

%prep
%setup -q
%patch0 -p1

cat > "init.cmake" <<EOF
SET (CURSES_INCLUDE_PATH "%{_includedir}/ncurses" CACHE PATH " " FORCE)
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
