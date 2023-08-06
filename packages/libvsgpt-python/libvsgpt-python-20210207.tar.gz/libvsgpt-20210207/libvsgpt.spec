Name: libvsgpt
Version: 20210207
Release: 1
Summary: Library to access the GUID Partition Table (GPT) volume system format
Group: System Environment/Libraries
License: LGPLv3+
Source: %{name}-%{version}.tar.gz
URL: https://github.com/libyal/libvsgpt
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
             
BuildRequires: gcc             

%description -n libvsgpt
Library to access the GUID Partition Table (GPT) volume system format

%package -n libvsgpt-static
Summary: Library to access the GUID Partition Table (GPT) volume system format
Group: Development/Libraries
Requires: libvsgpt = %{version}-%{release}

%description -n libvsgpt-static
Static library version of libvsgpt.

%package -n libvsgpt-devel
Summary: Header files and libraries for developing applications for libvsgpt
Group: Development/Libraries
Requires: libvsgpt = %{version}-%{release}

%description -n libvsgpt-devel
Header files and libraries for developing applications for libvsgpt.

%package -n libvsgpt-python2
Obsoletes: libvsgpt-python < %{version}
Provides: libvsgpt-python = %{version}
Summary: Python 2 bindings for libvsgpt
Group: System Environment/Libraries
Requires: libvsgpt = %{version}-%{release} python2
BuildRequires: python2-devel

%description -n libvsgpt-python2
Python 2 bindings for libvsgpt

%package -n libvsgpt-python3
Summary: Python 3 bindings for libvsgpt
Group: System Environment/Libraries
Requires: libvsgpt = %{version}-%{release} python3
BuildRequires: python3-devel

%description -n libvsgpt-python3
Python 3 bindings for libvsgpt

%package -n libvsgpt-tools
Summary: Several tools for Several tools for reading GUID Partition Table (GPT) volume systems
Group: Applications/System
Requires: libvsgpt = %{version}-%{release}

%description -n libvsgpt-tools
Several tools for Several tools for reading GUID Partition Table (GPT) volume systems

%prep
%setup -q

%build
%configure --prefix=/usr --libdir=%{_libdir} --mandir=%{_mandir} --enable-python2 --enable-python3
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
%make_install

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -n libvsgpt
%defattr(644,root,root,755)
%license COPYING COPYING.LESSER
%doc AUTHORS README
%attr(755,root,root) %{_libdir}/*.so.*

%files -n libvsgpt-static
%defattr(644,root,root,755)
%license COPYING COPYING.LESSER
%doc AUTHORS README
%attr(755,root,root) %{_libdir}/*.a

%files -n libvsgpt-devel
%defattr(644,root,root,755)
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/*.la
%{_libdir}/*.so
%{_libdir}/pkgconfig/libvsgpt.pc
%{_includedir}/*
%{_mandir}/man3/*

%files -n libvsgpt-python2
%defattr(644,root,root,755)
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/python2*/site-packages/*.a
%{_libdir}/python2*/site-packages/*.la
%{_libdir}/python2*/site-packages/*.so

%files -n libvsgpt-python3
%defattr(644,root,root,755)
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/python3*/site-packages/*.a
%{_libdir}/python3*/site-packages/*.la
%{_libdir}/python3*/site-packages/*.so

%files -n libvsgpt-tools
%defattr(644,root,root,755)
%license COPYING COPYING.LESSER
%doc AUTHORS README
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man1/*

%changelog
* Sun Feb  7 2021 Joachim Metz <joachim.metz@gmail.com> 20210207-1
- Auto-generated

