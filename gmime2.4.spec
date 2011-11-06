%define oname gmime
%define	major 2
%define apiver 2.4
%define libname %mklibname %{oname} %{apiver} %{major}
%define develname %mklibname %{oname} %{apiver} -d

%define build_mono 1

%ifarch %mips %arm
%define build_mono 0
%endif

%define _gtkdocdir	%{_datadir}/gtk-doc/html
%{expand:%%define _aclocaldir %(aclocal --print-ac-dir 2>/dev/null)}

%define _requires_exceptions libgmime
Summary:		The libGMIME library
Name:			gmime2.4
Version:		2.4.27
Release:		%mkrel 1
License:		LGPLv2+
Group:			System/Libraries
URL:			http://spruce.sourceforge.net/gmime
Source0:		http://ftp.gnome.org/pub/GNOME/sources/%oname/%{oname}-%{version}.tar.xz
BuildRequires:		glib2-devel
BuildRequires:		gtk-doc
BuildRequires:		libz-devel
%if %{build_mono}
BuildRequires:		mono-devel
BuildRequires:		gtk-sharp2-devel
BuildRequires:		gtk-sharp2
%endif
Buildroot:		%{_tmppath}/%{name}-%{version}-buildroot

%description
This library allows you to manipulate MIME messages.

%package -n %{name}-utils
Summary:	Utilities using the libGMIME library
Group:		File tools
Requires:	%{libname} = %{version}-%{release}
Conflicts: %{oname}-utils

%description -n %{name}-utils
This package contains gmime-uudecode and gmime-uuencode and will 
allow you to manipulate MIME messages. These utilities can also be
used instead of uudecode and uuencode from the sharutils package. 

%package -n %{libname}
Summary:	The libGMIME library
Group:		System/Libraries
Obsoletes:	%mklibname %{oname} 2.0
Provides:	%mklibname %{oname} 2.0
Provides:	lib%{oname} = %{version}-%{release}

%description -n %{libname}
This library allows you to manipulate MIME messages.

%package -n %{develname}
Summary:	Development library and header files for the lib%{name} library
Group:		Development/C
Provides:	lib%{name}-devel
Provides:	%{name}-devel
Requires:	%{libname} = %{version}-%{release}
Obsoletes:	%mklibname %{oname} 2.0 -d
Provides:	%mklibname %{oname} 2.0 -d

%description -n %{develname}
This package contains the lib%{name} development library and its header files.

%if %{build_mono}
%package sharp
Summary:	GMIME# bindings for mono
Group:		System/Libraries
Requires:	%{libname} = %{version}-%{release}

%description sharp
This library allows you to manipulate MIME messages.
%endif

%prep

%setup -q -n %oname-%version

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
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%makeinstall_std

# these are provided by sharutils, gotta rename them...
mv %{buildroot}%{_bindir}/uudecode %{buildroot}%{_bindir}/gmime-uudecode
mv %{buildroot}%{_bindir}/uuencode %{buildroot}%{_bindir}/gmime-uuencode

# cleanup
rm -f %{buildroot}%{_libdir}/gmimeConf.sh

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%files -n %{name}-utils
%defattr(-,root,root)
%{_bindir}/gmime-uudecode
%{_bindir}/gmime-uuencode

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/lib*%{apiver}.so.%{major}*

%files -n %{develname}
%defattr(-,root,root)
%doc AUTHORS ChangeLog PORTING README TODO
%{_libdir}/lib*.a
%{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_libdir}/pkgconfig/gmime-%{apiver}.pc
%{_includedir}/*
%doc %{_gtkdocdir}/*

%if %{build_mono}
%files sharp
%defattr(-,root,root)
%{_prefix}/lib/mono/gac/%{oname}-sharp
%{_prefix}/lib/mono/%{oname}-sharp-%{apiver}
%{_libdir}/pkgconfig/%{oname}-sharp-%{apiver}.pc
%endif
