%define		module	cssutils
%define		encutils_ver 0.9
Summary:	A CSS Cascading Style Sheets library for Python
Summary(pl.UTF-8):	Biblioteka CSS (Cascading Style Sheets) dla Pythona
Name:		python-%{module}
Version:	0.9.7b3
Release:	0.beta.1
License:	LGPL v3+
Group:		Libraries/Python
Source0:	http://cheeseshop.python.org/packages/source/c/cssutils/%{module}-%{version}.zip
# Source0-md5:	4539c061bb03612cc3a0e278c44e8f96
URL:		http://cthedot.de/cssutils/
BuildRequires:	python-devel >= 1:2.5
BuildRequires:	python-setuptools
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.174
BuildRequires:	unzip
%pyrequires_eq	python-modules
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

%prep
%setup -q -n %{module}-%{version}
eval $(PYTHONPATH=src python -c "from encutils import VERSION;print 'VERSION=%%s' %% VERSION")
if [ $VERSION != %{encutils_ver} ]; then
	echo "Please set encutils_ver to $VERSION"
	exit 1
fi

%build
python setup.py build

%install
rm -rf $RPM_BUILD_ROOT

python setup.py install \
        --single-version-externally-managed \
	--optimize=2 \
	--root $RPM_BUILD_ROOT

%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.txt
%attr(755,root,root) %{_bindir}/csscapture
%attr(755,root,root) %{_bindir}/csscombine
%attr(755,root,root) %{_bindir}/cssparse
%dir %{py_sitescriptdir}/cssutils
%dir %{py_sitescriptdir}/cssutils/css
%dir %{py_sitescriptdir}/cssutils/scripts
%dir %{py_sitescriptdir}/cssutils/stylesheets
%dir %{py_sitescriptdir}/encutils
#%%dir %{py_sitescriptdir}/tests
#%%dir %{py_sitescriptdir}/tests/test_encutils
%attr(755,root,root) %{py_sitescriptdir}/cssutils/*.py[co]
%attr(755,root,root) %{py_sitescriptdir}/cssutils/css/*.py[co]
%attr(755,root,root) %{py_sitescriptdir}/cssutils/scripts/*.py[co]
%attr(755,root,root) %{py_sitescriptdir}/cssutils/stylesheets/*.py[co]
%attr(755,root,root) %{py_sitescriptdir}/encutils/*.py[co]
#%%attr(755,root,root) %{py_sitescriptdir}/tests/*.py[co]
#%%attr(755,root,root) %{py_sitescriptdir}/tests/test_encutils/*.py[co]
%{py_sitescriptdir}/*.egg-info
