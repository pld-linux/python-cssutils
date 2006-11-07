%define		module	cssutils
%define		alpha	a6
Summary:	A CSS Cascading Style Sheets library for Python
Summary(pl):	Biblioteka CSS (Cascading Style Sheets) dla Pythona
Name:		python-%{module}
Version:	0.9
Release:	0.%{alpha}.1
License:	LGPL v2.1
Group:		Libraries/Python
Source0:	http://cheeseshop.python.org/packages/source/c/cssutils/%{module}-%{version}%{alpha}.zip
# Source0-md5:	fadcfa5370481f4692fb42fd0c96166b
Patch0:		%{name}-ez.patch
URL:		http://cthedot.de/cssutils/
BuildRequires:	python-devel >= 1:2.5
BuildRequires:	python-setuptools
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.174
%pyrequires_eq	python-modules
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A Python package to parse and build CSS Cascading Style Sheets. Partly
implements the DOM Level 2 Stylesheets and DOM Level 2 CSS interfaces.

%description -l pl
Pakiet Pythona do analizy i tworzenia CSS (Cascading Style Sheets).
Czê¶ciowo implementuje interfejsy DOM Level 2 Stylesheets oraz DOM
Level 2 CSS.

%prep
%setup -q -n %{module}-%{version}%{alpha}
%patch -p1

%build
python setup.py build

%install
rm -rf $RPM_BUILD_ROOT

python setup.py install \
        --single-version-externally-managed \
	--optimize=2 \
	--root $RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.txt
%attr(755,root,root) %{_bindir}/cssparse
%dir %{py_sitescriptdir}/cssutils
%dir %{py_sitescriptdir}/cssutils/css
%dir %{py_sitescriptdir}/cssutils/stylesheets
%dir %{py_sitescriptdir}/cssutils/tests
%attr(755,root,root) %{py_sitescriptdir}/cssutils/*.py[co]
%attr(755,root,root) %{py_sitescriptdir}/cssutils/css/*.py[co]
%attr(755,root,root) %{py_sitescriptdir}/cssutils/stylesheets/*.py[co]
%attr(755,root,root) %{py_sitescriptdir}/cssutils/tests/*.py[co]
%{py_sitescriptdir}/*.egg-info
