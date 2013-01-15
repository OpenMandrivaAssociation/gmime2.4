%define url_ver %(echo %{version}|cut -d. -f1,2)

%define oname	gmime
%define major	2
%define apiver	2.4
%define libname %mklibname %{oname} %{apiver} %{major}
%define devname %mklibname %{oname} %{apiver} -d

%define build_mono 1

%ifarch %mips %arm
%define build_mono 0
%endif

%define _gtkdocdir	%{_datadir}/gtk-doc/html
%{expand:%%define _aclocaldir %(aclocal --print-ac-dir 2>/dev/null)}

%if %{_use_internal_dependency_generator}
%define __noautoreq 'libgmime'
%else
%define _requires_exceptions libgmime
%endif

Summary:	The libGMIME library
Name:		%{oname}%{apiver}
Version:	2.4.33
Release:	1
License:	LGPLv2+
Group:		System/Libraries
URL:		http://spruce.sourceforge.net/gmime
Source0:	http://ftp.gnome.org/pub/GNOME/sources/%{oname}/%{url_ver}/%{oname}-%{version}.tar.xz
Patch0:		gmime-2.4.28-glib-deprecation.patch
Patch1:		gmime2.4-automake-1.13.patch

BuildRequires:	gtk-doc
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(zlib)
%if %{build_mono}
BuildRequires:	mono-devel
BuildRequires:	gtk-sharp2-devel
BuildRequires:	gtk-sharp2
%endif
#gw: autoconf:
BuildRequires:	gettext-devel

%description
This library allows you to manipulate MIME messages.

%package -n %{name}-utils
Summary:	Utilities using the libGMIME library
Group:		File tools
Conflicts:	%{oname}-utils

%description -n %{name}-utils
This package contains gmime-uudecode and gmime-uuencode and will 
allow you to manipulate MIME messages. These utilities can also be
used instead of uudecode and uuencode from the sharutils package. 

%package -n %{libname}
Summary:	The libGMIME library
Group:		System/Libraries

%description -n %{libname}
This library allows you to manipulate MIME messages.

%package -n %{devname}
Summary:	Development library and header files for the lib%{name} library
Group:		Development/C
Provides:	%{name}-devel = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}

%description -n %{devname}
This package contains the lib%{name} development library and its header files.

%if %{build_mono}
%package sharp
Summary:	GMIME bindings for mono
Group:		System/Libraries
Requires:	%{libname} = %{version}-%{release}

%description sharp
This library allows you to manipulate MIME messages.
%endif

%prep
%setup -qn %{oname}-%{version}
%apply_patches

autoreconf -fi

%build
%configure2_5x \
	--with-html-dir=%{_gtkdocdir} \
	--enable-gtk-doc

#gw parallel build broken in 2.1.15
# (tpg) mono stuff doesn't like parallel build, this solves it
%(echo %make|perl -pe 's/-j\d+/-j1/g')

%check
make check

%install
%makeinstall_std

# cleanup
rm -f %{buildroot}%{_libdir}/gmimeConf.sh

%files -n %{libname}
%{_libdir}/lib*%{apiver}.so.%{major}*

%files -n %{devname}
%doc AUTHORS ChangeLog PORTING README TODO
%{_libdir}/lib*.a
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/gmime-%{apiver}.pc
%{_includedir}/*
%doc %{_gtkdocdir}/*

%if %{build_mono}
%files sharp
%{_prefix}/lib/mono/gac/%{oname}-sharp
%{_prefix}/lib/mono/%{oname}-sharp-%{apiver}
%{_libdir}/pkgconfig/%{oname}-sharp-%{apiver}.pc
%endif

