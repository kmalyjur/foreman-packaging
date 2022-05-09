# Generated from foreman_wreckingball-3.3.0.gem by gem2rpm -*- rpm-spec -*-
# template: foreman_plugin
%{?scl:%scl_package rubygem-%{gem_name}}
%{!?scl:%global pkg_name %{name}}

%global gem_name foreman_wreckingball
%global plugin_name wreckingball
%global foreman_min_version 2.3

Name: %{?scl_prefix}rubygem-%{gem_name}
Version: 4.0.0
Release: 2%{?foremandist}%{?dist}
Summary: Adds status checks of the VMWare VMs to Foreman
Group: Applications/Systems
License: GPLv3+
URL: https://github.com/dm-drogeriemarkt/foreman_wreckingball
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem

# start specfile generated dependencies
Requires: foreman >= %{foreman_min_version}
Requires: %{?scl_prefix_ruby}ruby(release)
Requires: %{?scl_prefix_ruby}ruby
Requires: %{?scl_prefix_ruby}ruby(rubygems)
Requires: %{?scl_prefix}rubygem(foreman-tasks) >= 0.13.1
BuildRequires: foreman-assets >= %{foreman_min_version}
BuildRequires: foreman-plugin >= %{foreman_min_version}
BuildRequires: %{?scl_prefix}rubygem(foreman-tasks) >= 0.13.1
BuildRequires: %{?scl_prefix_ruby}ruby(release)
BuildRequires: %{?scl_prefix_ruby}ruby
BuildRequires: %{?scl_prefix_ruby}rubygems-devel
BuildArch: noarch
Provides: %{?scl_prefix}rubygem(%{gem_name}) = %{version}
Provides: foreman-plugin-%{plugin_name} = %{version}
# end specfile generated dependencies

%description
Adds status checks of the VMWare VMs to Foreman.


%package doc
Summary: Documentation for %{pkg_name}
Group: Documentation
Requires: %{?scl_prefix}%{pkg_name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{pkg_name}.

%prep
%{?scl:scl enable %{scl} - << \EOF}
gem unpack %{SOURCE0}
%{?scl:EOF}

%setup -q -D -T -n  %{gem_name}-%{version}

%{?scl:scl enable %{scl} - << \EOF}
gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec
%{?scl:EOF}

%build
# Create the gem as gem install only works on a gem file
%{?scl:scl enable %{scl} - << \EOF}
gem build %{gem_name}.gemspec
%{?scl:EOF}

# %%gem_install compiles any C extensions and installs the gem into ./%%gem_dir
# by default, so that we can move it into the buildroot in %%install
%{?scl:scl enable %{scl} - << \EOF}
%gem_install
%{?scl:EOF}

%install
mkdir -p %{buildroot}%{gem_dir}
cp -pa .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%foreman_bundlerd_file
%foreman_precompile_plugin -s

%files
%dir %{gem_instdir}
%license %{gem_instdir}/LICENSE
%{gem_instdir}/app
%{gem_instdir}/config
%{gem_instdir}/db
%{gem_libdir}
%{gem_instdir}/locale
%exclude %{gem_cache}
%{gem_spec}
%{foreman_bundlerd_plugin}
%{foreman_assets_plugin}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/README.md
%{gem_instdir}/Rakefile
%{gem_instdir}/test

%posttrans
%{foreman_plugin_log}

%changelog
* Mon May 09 2022 Evgeni Golov - 4.0.0-2
- log plugin installation in posttrans

* Fri Oct 22 2021 Manuel Laug <laugmanuel@gmail.com> - 4.0.0-1
- Update foreman_wreckingball to 4.0.0

* Tue Apr 06 2021 Eric D. Helms <ericdhelms@gmail.com> - 3.4.1-2
- Rebuild plugins for Ruby 2.7

* Thu Jan 28 2021 Manuel Laug <laugmanuel@gmail.com> - 3.4.1-1
- Update foreman_wreckingball to 3.4.1

* Tue Jan 07 2020 Eric D. Helms <ericdhelms@gmail.com> - 3.4.0-2
- Drop migrate, seed and restart posttans

* Wed Apr 17 2019 Timo Goebel <mail@timogoebel.name> - 3.4.0-1
- Update foreman_wreckingball to 3.4.0

* Tue Mar 19 2019 Timo Goebel <mail@timogoebel.name> - 3.3.0-2
- Add asset precompilation

* Fri Mar 01 2019 Timo Goebel <mail@timogoebel.name> - 3.3.0-1
- Update foreman_wreckingball to 3.3.0

* Thu Jan 24 2019 Timo Goebel <mail@timogoebel.name> - 3.2.0-1
- Update foreman_wreckingball to 3.2.0

* Wed Sep 12 2018 Bryan Kearney <bryan.kearney@gmail.com> - 3.0.1-3
- Move licenes which are GPL-* to GPLv3

* Mon Sep 10 2018 Eric D. Helms <ericdhelms@gmail.com> - 3.0.1-2
- Rebuild for Rails 5.2 and Ruby 2.5

* Mon Aug 27 2018 Timo Goebel <mail@timogoebel.name> - 3.0.1-1
- Update foreman_wreckingball to 3.0.1

* Wed Jun 13 2018 Ondrej Prazak <oprazak@redhat.com> 3.0.0-1
- Update to 3.0.0

* Thu Jun 07 2018 Dirk Goetz <dirk.goetz@netways.de> 2.0.0-2
- Changed to foreman_plugin template

* Tue Jun 05 2018 Dirk Goetz <dirk.goetz@netways.de> 2.0.0-1
- Add rubygem-foreman_wreckingball generated by gem2rpm using the scl template

