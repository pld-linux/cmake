%define name cmake
%define version 1.4.7
%define release 1

Summary:	Cross-platform, open-source make system
Name:		%name
Version:	%version
Release:	%release
License:	BSD
Group:		Development/Other
######		Unknown group!
Url:		http://www.cmake.org/HTML/Index.html
Source0:	CMake%{version}-src-unix.tar.bz2
Patch0:		cmake-ncurses.patch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
CMake is used to control the software compilation process using simple
platform and compiler independent configuration files. CMake generates
native makefiles and workspaces that can be used in the compiler
environment of your choice. CMake is quite sophisticated: it is
possible to support complex environments requiring system
configuration, pre-processor generation, code generation, and template
instantiation.

%prep
%setup -q -n CMake-%version
%patch0 -p1

%build
CXXFLAGS="%{rpmcflags} -I%{_includedir}/ncurses"
%configure2_13
%{__make} \
	CXXFLAGS="%{rpmcflags} -I%{_includedir}/ncurses"

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install DESTDIR=$RPM_BUILD_ROOT
mv $RPM_BUILD_ROOT%{_prefix}/man $RPM_BUILD_ROOT/%_datadir/
bzip2 $RPM_BUILD_ROOT/%_datadir/man/man1/*

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc ChangeLog.txt *.pdf *.rtf Copyright.txt *.gif
%_bindir/ccmake
%_bindir/cmake
%_bindir/cmaketest
%_bindir/ctest
%_mandir/man1/*.1.*
%_datadir/CMake/Modules
%_datadir/CMake/Templates
