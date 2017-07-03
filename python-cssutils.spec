#
# Conditional build:
%bcond_without	python2	# CPython 2.x module
%bcond_without	python3 # CPython 3.x module
%bcond_without	tests	# unit tests

%define		module	cssutils
%define		encutils_ver 0.9.8
Summary:	A CSS Cascading Style Sheets library for Python 2
Summary(pl.UTF-8):	Biblioteka CSS (Cascading Style Sheets) dla Pythona 2
Name:		python-%{module}
Version:	1.0.2
Release:	1
Epoch:		1
License:	LGPL v3+
Group:		Libraries/Python
Source0:	http://files.pythonhosted.org/packages/source/c/cssutils/%{module}-%{version}.tar.gz
# Source0-md5:	dc66d96c2d78f1687f59ac412fe9d318
Patch0:		%{name}-tests.patch
Patch1:		%{name}-mock.patch
URL:		http://cthedot.de/cssutils/
%if %{with python2}
BuildRequires:	python-devel >= 1:2.5
%{?with_tests:BuildRequires:	python-mock}
BuildRequires:	python-setuptools
%endif
%if %{with python3}
BuildRequires:	python3-2to3 >= 1:3.2
BuildRequires:	python3-devel >= 1:3.2
BuildRequires:	python3-setuptools
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
Requires:	python-modules >= 1:2.5
Provides:	python-encutils = %{encutils_ver}
Obsoletes:	python-encutils < %{encutils_ver}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A Python package to parse and build CSS Cascading Style Sheets. Partly
implements the DOM Level 2 Stylesheets and DOM Level 2 CSS interfaces.

%description -l pl.UTF-8
Pakiet Pythona do analizy i tworzenia CSS (Cascading Style Sheets).
Częściowo implementuje interfejsy DOM Level 2 Stylesheets oraz DOM
Level 2 CSS.

%package -n python3-%{module}
Summary:	A CSS Cascading Style Sheets library for Python 3
Summary(pl.UTF-8):	Biblioteka CSS (Cascading Style Sheets) dla Pythona 3
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.2

%description -n python3-%{module}
A Python package to parse and build CSS Cascading Style Sheets. Partly
implements the DOM Level 2 Stylesheets and DOM Level 2 CSS interfaces.

%description -n python3-%{module} -l pl.UTF-8
Pakiet Pythona do analizy i tworzenia CSS (Cascading Style Sheets).
Częściowo implementuje interfejsy DOM Level 2 Stylesheets oraz DOM
Level 2 CSS.

%prep
%setup -q -n %{module}-%{version}
%patch0 -p1
%patch1 -p1

eval $(PYTHONPATH=src python -c "from encutils import VERSION;print 'VERSION=%%s' %% VERSION")
if [ $VERSION != %{encutils_ver} ]; then
	echo "Please set encutils_ver to $VERSION"
	exit 1
fi

%build
%if %{with python2}
%py_build

%if %{with tests}
%{__python} -m unittest discover -t build-2/lib -s build-2/lib/cssutils/tests
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
%{__python3} -m unittest discover -t build-3/lib -s build-3/lib/cssutils/tests
%endif
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python3}
%py3_install

for f in csscapture csscombine cssparse ; do
	%{__mv} $RPM_BUILD_ROOT%{_bindir}/$f $RPM_BUILD_ROOT%{_bindir}/${f}-3
done

%{__rm} -r $RPM_BUILD_ROOT%{py3_sitescriptdir}/cssutils/tests
%endif

%if %{with python2}
%py_install

for f in csscapture csscombine cssparse ; do
	%{__mv} $RPM_BUILD_ROOT%{_bindir}/$f $RPM_BUILD_ROOT%{_bindir}/${f}-2
	ln -sf ${f}-2 $RPM_BUILD_ROOT%{_bindir}/$f
done

%py_postclean
%{__rm} -r $RPM_BUILD_ROOT%{py_sitescriptdir}/cssutils/tests
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc README.txt
%attr(755,root,root) %{_bindir}/csscapture
%attr(755,root,root) %{_bindir}/csscombine
%attr(755,root,root) %{_bindir}/cssparse
%attr(755,root,root) %{_bindir}/csscapture-2
%attr(755,root,root) %{_bindir}/csscombine-2
%attr(755,root,root) %{_bindir}/cssparse-2
%{py_sitescriptdir}/cssutils
%{py_sitescriptdir}/encutils
%{py_sitescriptdir}/cssutils-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/csscapture-3
%attr(755,root,root) %{_bindir}/csscombine-3
%attr(755,root,root) %{_bindir}/cssparse-3
%{py3_sitescriptdir}/cssutils
%{py3_sitescriptdir}/encutils
%{py3_sitescriptdir}/cssutils-%{version}-py*.egg-info
%endif
