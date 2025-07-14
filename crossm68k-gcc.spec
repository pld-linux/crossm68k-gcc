Summary:	Cross m68k GNU binary utility development utilities - gcc
Summary(es.UTF-8):	Utilitarios para desarrollo de binarios de la GNU - m68k gcc
Summary(fr.UTF-8):	Utilitaires de développement binaire de GNU - m68k gcc
Summary(pl.UTF-8):	Skrośne narzędzia programistyczne GNU dla m68k - gcc
Summary(pt_BR.UTF-8):	Utilitários para desenvolvimento de binários da GNU - m68k gcc
Summary(tr.UTF-8):	GNU geliţtirme araçlarý - m68k gcc
Name:		crossm68k-gcc
Version:	3.3.6
Release:	1
Epoch:		1
License:	GPL
Group:		Development/Languages
Source0:	ftp://gcc.gnu.org/pub/gcc/releases/gcc-%{version}/gcc-%{version}.tar.bz2
# Source0-md5:	6936616a967da5a0b46f1e7424a06414
Patch0:		%{name}-coldfire-targets.patch
Patch1:		%{name}-coldfire-frame.patch
Patch2:		%{name}-idshlib.patch
Patch3:		%{name}-coldfire-omitfp.patch
Patch4:		%{name}-specs.patch
Patch5:		%{name}-thunk.patch
Patch6:		%{name}-nowchar.patch
BuildRequires:	/bin/bash
BuildRequires:	autoconf
BuildRequires:	bison
BuildRequires:	crossm68k-binutils
BuildRequires:	crossm68k-uClibc
BuildRequires:	flex
BuildRequires:	sed >= 4.0
Requires:	crossm68k-binutils
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		target		m68k-elf
%define		arch		%{_prefix}/%{target}
%define		gccarch		%{_libdir}/gcc-lib/%{target}
%define		gcclib		%{_libdir}/gcc-lib/%{target}/%{version}

%define		_noautostrip	.*lib.*\\.a

%description
This package contains a cross-gcc which allows the creation of
binaries to be run on m68k linux (architecture m68k-linux) on other
machines.

%description -l de.UTF-8
Dieses Paket enthält einen Cross-gcc, der es erlaubt, auf einem
anderem Rechner Code für m68k-Linux zu generieren.

%description -l pl.UTF-8
Ten pakiet zawiera skrośny gcc pozwalający na robienie na innych
maszynach binariów do uruchamiania na m68k.

%prep
%setup -q -n gcc-%{version}
%patch -P0 -p1
%patch -P1 -p1
%patch -P2 -p1
%patch -P3 -p1
%patch -P4 -p1
%patch -P5 -p1
%patch -P6 -p1

sed -i 's#unsigned signo;#int signo;#'		 \
	libiberty/strsignal.c

sed -i 's#char \*message;#const char *message;#' \
	libiberty/strsignal.c

rm -rf	libstdc++-v3/config/os/newlib
ln -s	generic libstdc++-v3/config/os/newlib

%build
rm -rf %{target}-obj && install -d %{target}-obj && cd %{target}-obj

CFLAGS="%{rpmcflags}" \
CXXFLAGS="%{rpmcflags}" \
TEXCONFIG=false \
../configure \
	--prefix=%{_prefix} \
	--infodir=%{_infodir} \
	--mandir=%{_mandir} \
	--bindir=%{_bindir} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libdir} \
	--disable-nls \
	--disable-shared \
	--disable-wchar_t \
	--enable-languages="c" \
	--enable-target-optspace \
	--enable-threads=posix \
	--with-headers=%{arch}/include \
	--with-multilib \
	--with-newlib \
	--with-system-zlib \
	--without-x \
	--target=%{target} \
	--host=%{_target_platform} \
	--build=%{_target_platform}
cd ..
%{__make} -C %{target}-obj

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C %{target}-obj install \
	DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name 'libiberty.a' | \
	xargs rm

%if 0%{!?debug:1}
find $RPM_BUILD_ROOT -type f -name '*.[ao]' | \
	xargs %{target}-strip --strip-debug
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/%{target}-cpp
%attr(755,root,root) %{_bindir}/%{target}-gc*
%attr(755,root,root) %{gcclib}/cc1
%attr(755,root,root) %{gcclib}/collect2
%dir %{gccarch}
%dir %{gcclib}
%dir %{gcclib}/include
%{gcclib}/include/*.h
%{gcclib}/m*
%{gcclib}/specs
%{_mandir}/man1/%{target}-gcc.1*
