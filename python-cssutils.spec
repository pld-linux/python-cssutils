#
# Conditional build:
%bcond_without	tests		# unit tests
%bcond_with	tests_net	# unit tests using network

%define		module	cssutils
%define		encutils_ver 0.9.8
Summary:	A CSS Cascading Style Sheets library for Python 2
Summary(pl.UTF-8):	Biblioteka CSS (Cascading Style Sheets) dla Pythona 2
Name:		python-%{module}
# keep 1.x here for python2 support
Version:	1.0.2
Release:	12
Epoch:		1
License:	LGPL v3+
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/cssutils/
Source0:	https://files.pythonhosted.org/packages/source/c/cssutils/%{module}-%{version}.tar.gz
# Source0-md5:	dc66d96c2d78f1687f59ac412fe9d318
Patch0:		%{name}-tests.patch
Patch1:		%{name}-mock.patch
URL:		http://cthedot.de/cssutils/
BuildRequires:	python-devel >= 1:2.5
%{?with_tests:BuildRequires:	python-mock}
BuildRequires:	python-setuptools
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
Requires:	python-modules >= 1:2.5
Provides:	python-encutils = %{encutils_ver}
Obsoletes:	python-encutils < %{encutils_ver}
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A Python package to parse and build CSS Cascading Style Sheets. Partly
implements the DOM Level 2 Stylesheets and DOM Level 2 CSS interfaces.

%description -l pl.UTF-8
Pakiet Pythona do analizy i tworzenia CSS (Cascading Style Sheets).
Częściowo implementuje interfejsy DOM Level 2 Stylesheets oraz DOM
Level 2 CSS.

%prep
%setup -q -n %{module}-%{version}
%patch -P 0 -p1
%patch -P 1 -p1

eval $(PYTHONPATH=src python -c "from encutils import VERSION;print 'VERSION=%%s' %% VERSION")
if [ $VERSION != %{encutils_ver} ]; then
	echo "Please set encutils_ver to $VERSION"
	exit 1
fi

%if %{without tests_net}
%{__sed} -i -e 's/def test_parseUrl/def skip_parseUrl/' src/cssutils/tests/test_parse.py
%{__sed} -i -e 's/def test_handlers/def skip_handlers/' src/cssutils/tests/test_errorhandler.py
%endif

%build
%py_build

%if %{with tests}
%{__python} -m unittest discover -t build-2/lib -s build-2/lib/cssutils/tests
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py_install

for f in csscapture csscombine cssparse ; do
	%{__mv} $RPM_BUILD_ROOT%{_bindir}/$f $RPM_BUILD_ROOT%{_bindir}/${f}-2
done

%py_postclean
%{__rm} -r $RPM_BUILD_ROOT%{py_sitescriptdir}/cssutils/tests

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.txt
%attr(755,root,root) %{_bindir}/csscapture-2
%attr(755,root,root) %{_bindir}/csscombine-2
%attr(755,root,root) %{_bindir}/cssparse-2
%{py_sitescriptdir}/cssutils
%{py_sitescriptdir}/encutils
%{py_sitescriptdir}/cssutils-%{version}-py*.egg-info
