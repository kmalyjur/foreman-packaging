%{?scl:%scl_package nodejs-%{npm_name}}
%{!?scl:%global pkg_name %{name}}

%global npm_name graphql

Name: %{?scl_prefix}nodejs-graphql
Version: 15.8.0
Release: 1%{?dist}
Summary: A Query Language and Runtime which can target any service
License: MIT
Group: Development/Libraries
URL: https://github.com/graphql/graphql-js
Source0: https://registry.npmjs.org/graphql/-/graphql-%{version}.tgz
%if 0%{?!scl:1}
BuildRequires: nodejs-packaging
%endif
BuildArch: noarch
ExclusiveArch: %{nodejs_arches} noarch
Provides: %{?scl_prefix}npm(%{npm_name}) = %{version}

%description
%{summary}

%prep
%setup -q -n package

%install
mkdir -p %{buildroot}%{nodejs_sitelib}/%{npm_name}
cp -pfr error %{buildroot}%{nodejs_sitelib}/%{npm_name}
cp -pfr execution %{buildroot}%{nodejs_sitelib}/%{npm_name}
cp -pfr graphql.d.ts %{buildroot}%{nodejs_sitelib}/%{npm_name}
cp -pfr graphql.js %{buildroot}%{nodejs_sitelib}/%{npm_name}
cp -pfr graphql.js.flow %{buildroot}%{nodejs_sitelib}/%{npm_name}
cp -pfr graphql.mjs %{buildroot}%{nodejs_sitelib}/%{npm_name}
cp -pfr index.d.ts %{buildroot}%{nodejs_sitelib}/%{npm_name}
cp -pfr index.js %{buildroot}%{nodejs_sitelib}/%{npm_name}
cp -pfr index.js.flow %{buildroot}%{nodejs_sitelib}/%{npm_name}
cp -pfr index.mjs %{buildroot}%{nodejs_sitelib}/%{npm_name}
cp -pfr jsutils %{buildroot}%{nodejs_sitelib}/%{npm_name}
cp -pfr language %{buildroot}%{nodejs_sitelib}/%{npm_name}
cp -pfr package.json %{buildroot}%{nodejs_sitelib}/%{npm_name}
cp -pfr polyfills %{buildroot}%{nodejs_sitelib}/%{npm_name}
cp -pfr subscription %{buildroot}%{nodejs_sitelib}/%{npm_name}
cp -pfr type %{buildroot}%{nodejs_sitelib}/%{npm_name}
cp -pfr utilities %{buildroot}%{nodejs_sitelib}/%{npm_name}
cp -pfr validation %{buildroot}%{nodejs_sitelib}/%{npm_name}
cp -pfr version.d.ts %{buildroot}%{nodejs_sitelib}/%{npm_name}
cp -pfr version.js %{buildroot}%{nodejs_sitelib}/%{npm_name}
cp -pfr version.js.flow %{buildroot}%{nodejs_sitelib}/%{npm_name}
cp -pfr version.mjs %{buildroot}%{nodejs_sitelib}/%{npm_name}

%nodejs_symlink_deps

%check
%{nodejs_symlink_deps} --check

%files
%{nodejs_sitelib}/%{npm_name}
%license LICENSE
%doc README.md

%changelog
* Fri Aug 11 2023 Foreman Packaging Automation <packaging@theforeman.org> 15.8.0-1
- Update to 15.8.0

* Wed Jun 09 2021 Ondrej Prazak <oprazak@redhat.com> 15.5.0-1
- Add nodejs-graphql generated by npm2rpm using the single strategy

