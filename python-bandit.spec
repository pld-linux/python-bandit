#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_with	tests	# unit tests (python3 tests fail)
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

Summary:	Security oriented static analyser for Python code
Summary(pl.UTF-8):	Statyczny analizator kodu pythonowego zorientowany na bezpieczeństwo
Name:		python-bandit
# keep 1.6.x here for python2 support
Version:	1.6.2
Release:	2
License:	Apache v2.0
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/bandit/
Source0:	https://files.pythonhosted.org/packages/source/b/bandit/bandit-%{version}.tar.gz
# Source0-md5:	c6a6772d7afa0af8828b3384e73b7085
Patch0:		bandit-mock.patch
URL:		https://pypi.org/project/bandit/
%if %{with python2}
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-PyYAML >= 3.13
BuildRequires:	python-bs4 >= 4.6.0
BuildRequires:	python-fixtures >= 3.0.0
BuildRequires:	python-git >= 1.0.1
BuildRequires:	python-mock >= 2.0.0
BuildRequires:	python-oslotest >= 3.2.0
BuildRequires:	python-six >= 1.10.0
BuildRequires:	python-stestr >= 1.0.0
BuildRequires:	python-stevedore >= 1.20.0
BuildRequires:	python-testscenarios >= 0.4
BuildRequires:	python-testtools >= 2.2.0
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.5
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-PyYAML >= 3.13
BuildRequires:	python3-bs4 >= 4.6.0
BuildRequires:	python3-fixtures >= 3.0.0
BuildRequires:	python3-git >= 1.0.1
BuildRequires:	python3-oslotest >= 3.2.0
BuildRequires:	python3-six >= 1.10.0
BuildRequires:	python3-stestr >= 1.0.0
BuildRequires:	python3-stevedore >= 1.20.0
BuildRequires:	python3-testscenarios >= 0.4
BuildRequires:	python3-testtools >= 2.2.0
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	python-sphinx_rtd_theme >= 0.3.0
BuildRequires:	sphinx-pdg-2 >= 1.6.8
%endif
Requires:	python-modules >= 1:2.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Bandit is a tool designed to find common security issues in Python
code. To do this Bandit processes each file, builds an AST from it,
and runs appropriate plugins against the AST nodes. Once Bandit has
finished scanning all the files it generates a report.

%description -l pl.UTF-8
Bandit to narzędzie zaprojektowane do szukania najczęstszych problemów
z bezpieczeństwem w kodzie pythonowym. W tym celu Bandit przetwarza
wszystkie pliki, tworzy z nich drzewo AST i uruchamia na jego węzłach
odpowiednie wtyczki. Po zakończeniu skanowania wszystkich plików
generuje raport.

%package -n python3-bandit
Summary:	Security oriented static analyser for Python code
Summary(pl.UTF-8):	Statyczny analizator kodu pythonowego zorientowany na bezpieczeństwo
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.5

%description -n python3-bandit
Bandit is a tool designed to find common security issues in Python
code. To do this Bandit processes each file, builds an AST from it,
and runs appropriate plugins against the AST nodes. Once Bandit has
finished scanning all the files it generates a report.

%description -n python3-bandit -l pl.UTF-8
Bandit to narzędzie zaprojektowane do szukania najczęstszych problemów
z bezpieczeństwem w kodzie pythonowym. W tym celu Bandit przetwarza
wszystkie pliki, tworzy z nich drzewo AST i uruchamia na jego węzłach
odpowiednie wtyczki. Po zakończeniu skanowania wszystkich plików
generuje raport.

%package apidocs
Summary:	API documentation for Python bandit module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona bandit
Group:		Documentation

%description apidocs
API documentation for Python bandit module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona bandit.

%prep
%setup -q -n bandit-%{version}
%patch -P 0 -p1

%build
%if %{with python2}
%py_build

%if %{with tests}
install -d build-2/bin
cp -p bandit/__main__.py build-2/bin/bandit
%{__sed} -i -e '1s,/usr/bin/env python,%{__python},' build-2/bin/bandit
cat >build-2/bin/bandit-baseline <<EOF
#!%{__python}
from bandit.cli.baseline import main
main()
EOF
chmod 755 build-2/bin/bandit build-2/bin/bandit-baseline

PATH=$(pwd)/build-2/bin:$PATH \
PYTHONPATH=$(pwd) \
stestr-2 run tests
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
install -d build-3/bin
cp -p bandit/__main__.py build-3/bin/bandit
%{__sed} -i -e '1s,/usr/bin/env python,%{__python3},' build-3/bin/bandit
cat >build-3/bin/bandit-baseline <<EOF
#!%{__python3}
from bandit.cli.baseline import main
main()
EOF
chmod 755 build-3/bin/bandit build-3/bin/bandit-baseline

PATH=$(pwd)/build-3/bin:$PATH \
PYTHONPATH=$(pwd) \
stestr-3 run tests
%endif
%endif

%if %{with doc}
sphinx-build-2 -b html doc/source doc/build/html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean

for f in bandit bandit-baseline bandit-config-generator ; do
	%{__mv} $RPM_BUILD_ROOT%{_bindir}/$f $RPM_BUILD_ROOT%{_bindir}/${f}-2
done
%endif

%if %{with python3}
%py3_install

for f in bandit bandit-baseline bandit-config-generator ; do
	%{__mv} $RPM_BUILD_ROOT%{_bindir}/$f $RPM_BUILD_ROOT%{_bindir}/${f}-3
	ln -sf ${f}-3 $RPM_BUILD_ROOT%{_bindir}/$f
done
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README.rst
%attr(755,root,root) %{_bindir}/bandit-2
%attr(755,root,root) %{_bindir}/bandit-baseline-2
%attr(755,root,root) %{_bindir}/bandit-config-generator-2
%{py_sitescriptdir}/bandit
%{py_sitescriptdir}/bandit-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-bandit
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README.rst
%attr(755,root,root) %{_bindir}/bandit
%attr(755,root,root) %{_bindir}/bandit-3
%attr(755,root,root) %{_bindir}/bandit-baseline
%attr(755,root,root) %{_bindir}/bandit-baseline-3
%attr(755,root,root) %{_bindir}/bandit-config-generator
%attr(755,root,root) %{_bindir}/bandit-config-generator-3
%{py3_sitescriptdir}/bandit
%{py3_sitescriptdir}/bandit-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc doc/build/html/{_modules,_static,blacklists,formatters,man,plugins,*.html,*.js}
%endif
