Summary:	Cross m68k GNU binary utility development utilities - gcc
Summary(es):	Utilitarios para desarrollo de binarios de la GNU - m68k gcc
Summary(fr):	Utilitaires de développement binaire de GNU - m68k gcc
Summary(pl):	Skro¶ne narzêdzia programistyczne GNU dla m68k - gcc
Summary(pt_BR):	Utilitários para desenvolvimento de binários da GNU - m68k gcc
Summary(tr):	GNU geliþtirme araçlarý - m68k gcc
Name:		crossm68k-gcc
Version:	2.95.3
Release:	1
Epoch:		1
License:	GPL
Group:		Development/Languages
Source0:	ftp://gcc.gnu.org/pub/gcc/releases/gcc-%{version}/gcc-%{version}.tar.bz2
# Source0-md5:	87ee083a830683e2aaa57463940a0c3c
Patch0:		%{name}-full.patch
Patch1:		%{name}-sigset.patch
Patch2:		%{name}-zext.patch
Patch3:		%{name}-build.patch
BuildRequires:	/bin/bash
BuildRequires:	autoconf
BuildRequires:	bison
BuildRequires:	crossm68k-binutils
BuildRequires:	crossm68k-uClibc
BuildRequires:	flex
Requires:	crossm68k-binutils
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		target		m68k-elf
%define		arch		%{_prefix}/%{target}
%define		gccarch		%{_libdir}/gcc-lib/%{target}
%define		gcclib		%{_libdir}/gcc-lib/%{target}/%{version}

%define		_noautostrip	.*%{gcclib}/.*libgcc\\.a

%description
This package contains a cross-gcc which allows the creation of
binaries to be run on m68k linux (architecture m68k-linux) on other
machines.

%description -l de
Dieses Paket enthält einen Cross-gcc, der es erlaubt, auf einem
anderem Rechner Code für m68k-Linux zu generieren.

%description -l pl
Ten pakiet zawiera skro¶ny gcc pozwalaj±cy na robienie na innych
maszynach binariów do uruchamiania na m68k.

%prep
%setup -q -n gcc-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
cd gcc
%{__autoconf}
cp -f /usr/share/automake/config.* .
cd ..
cp -f /usr/share/automake/config.* .

rm -rf obj-%{target}
install -d obj-%{target} && cd obj-%{target}

# Bug: CFLAGS is used to target ...
CFLAGS='-Os -Dlinux -D__linux__ -Dunix' \
../configure \
	--prefix=%{_prefix} \
	--infodir=%{_infodir} \
	--mandir=%{_mandir} \
	--bindir=%{_bindir} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libdir} \
	--disable-shared \
	--disable-threads \
	--enable-target-optspace \
	--enable-languages=c \
	--enable-multilib \
	--with-gnu-as \
	--with-gnu-ld \
	--target=%{target} \
	--host=%{_target_platform} \
	--build=%{_target_platform}

cd ..
%{__make} -C obj-%{target}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C obj-%{target} install \
        prefix=$RPM_BUILD_ROOT%{_prefix} \
	bindir=$RPM_BUILD_ROOT%{_bindir} \
        libdir=$RPM_BUILD_ROOT%{_libdir} \
	mandir=$RPM_BUILD_ROOT%{_mandir} \
	infodir=$RPM_BUILD_ROOT%{_infodir}
			
# don't want this here
rm -f $RPM_BUILD_ROOT%{_libdir}/libiberty.a
rm -rf $RPM_BUILD_ROOT%{gcclib}/include/{README,asm,linux}

%if 0%{!?debug:1}
%{target}-strip --strip-debug					\
			$RPM_BUILD_ROOT%{gcclib}/*.o		\
			$RPM_BUILD_ROOT%{gcclib}/libgcc.a	\
			$RPM_BUILD_ROOT%{gcclib}/*/libgcc.a	\
			$RPM_BUILD_ROOT%{gcclib}/*/*/libgcc.a
%endif

mv $RPM_BUILD_ROOT%{_bindir}/cpp	$RPM_BUILD_ROOT%{_bindir}/%{target}-cpp
mv $RPM_BUILD_ROOT%{_bindir}/gcov	$RPM_BUILD_ROOT%{_bindir}/%{target}-gcov

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/%{target}-*
%attr(755,root,root) %{gcclib}/cpp0
%attr(755,root,root) %{gcclib}/cc1
%attr(755,root,root) %{gcclib}/collect2
%dir %{gccarch}
%dir %{gcclib}
%{gcclib}/[imSls]*
%{gcclib}/crt*
%{_mandir}/man1/%{target}-gcc.1*
