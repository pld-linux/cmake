Summary:	Cross-platform, open-source make system
Summary(pl):	Wieloplatformowy system make o otwartych ¼ród³ach
Name:		cmake
Version:	1.8.3
Release:	1
License:	BSD
Group:		Development/Building
# current: http://www.cmake.org/files/v2.0/cmake-2.0.2.tar.gz
Source0:	http://www.cmake.org/files/v1.8/%{name}-%{version}.tar.gz	
# Source0-md5:	781afe6ed9000e303bf6ac3e4e384dce
Patch0:		%{name}-ncurses.patch
URL:		http://www.cmake.org/
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

%build
./bootstrap \
	--prefix=%{_prefix} \
	--mandir=/share/man \
	--datadir=/share/cmake \
	--verbose

./Bootstrap.cmk/cmake \
	-DCURSES_INCLUDE_PATH=%{_includedir}/ncurses

%{__make}
	

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

rm -rf $RPM_BUILD_ROOT/usr/doc

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc ChangeLog.txt *.pdf *.rtf Copyright.txt *.gif Docs/{cmake,ccmake,ctest}.*
%attr(755,root,root) %{_bindir}/ccmake
%attr(755,root,root) %{_bindir}/cmake
%attr(755,root,root) %{_bindir}/ctest
%{_mandir}/man1/*.1*
%{_datadir}/cmake
