%global pkg_name geronimo-jaxrpc
%{?scl:%scl_package %{pkg_name}}
%{?maven_find_provides_and_requires}

%global spec_ver 1.1
%global spec_name geronimo-jaxrpc_%{spec_ver}_spec

Name:             %{?scl_prefix}%{pkg_name}
Version:          2.1
Release:          14.10%{?dist}
Summary:          Java EE: Java API for XML Remote Procedure Call v1.1
License:          ASL 2.0 and W3C

URL:              http://geronimo.apache.org/
Source0:          http://repo2.maven.org/maven2/org/apache/geronimo/specs/%{spec_name}/%{version}/%{spec_name}-%{version}-source-release.tar.gz
# Use parent pom files instead of unavailable 'genesis-java5-flava'
Patch1:           use_parent_pom.patch
BuildArch:        noarch

BuildRequires:    %{?scl_prefix_java_common}javapackages-tools
BuildRequires:    %{?scl_prefix_java_common}maven-local
BuildRequires:    maven30-geronimo-parent-poms
BuildRequires:    maven30-maven-resources-plugin
BuildRequires:    maven30-geronimo-saaj
BuildRequires:    maven30-geronimo-osgi-support
BuildRequires:    %{?scl_prefix_java_common}tomcat-servlet-3.0-api
BuildRequires:    maven30-maven-surefire-provider-junit


%description
This package contains the core JAX-RPC APIs for the client programming model. 

%package javadoc
Summary:          Javadoc for %{pkg_name}

%description javadoc
This package contains the API documentation for %{pkg_name}.


%prep
%setup -q -n %{spec_name}-%{version}
%{?scl:scl enable maven30 %{scl} - <<"EOF"}
set -e -x
iconv -f iso8859-1 -t utf-8 LICENSE > LICENSE.conv && mv -f LICENSE.conv LICENSE
sed -i 's/\r//' LICENSE NOTICE
%patch1 -p0

%pom_xpath_replace "pom:dependency[pom:artifactId[text()='geronimo-servlet_3.0_spec']]" \
  "<dependency>
     <groupId>org.apache.tomcat</groupId>
     <artifactId>tomcat-servlet-api</artifactId>
     <scope>provided</scope>
  </dependency>"

%mvn_file : %{pkg_name} jaxrpc
%mvn_alias : javax.xml:jaxrpc-api
%{?scl:EOF}

%build
%{?scl:scl enable maven30 %{scl} - <<"EOF"}
set -e -x
%mvn_build
%{?scl:EOF}

%install
%{?scl:scl enable maven30 %{scl} - <<"EOF"}
set -e -x
%mvn_install
%{?scl:EOF}

%files -f .mfiles
%doc LICENSE NOTICE

%files javadoc -f .mfiles-javadoc
%doc LICENSE NOTICE

%changelog
* Sat Jan 09 2016 Michal Srb <msrb@redhat.com> - 2.1-14.10
- maven33 rebuild

* Tue Jan 13 2015 Michael Simacek <msimacek@redhat.com> - 2.1-14.9
- Mass rebuild 2015-01-13

* Tue Jan 06 2015 Michael Simacek <msimacek@redhat.com> - 2.1-14.8
- Mass rebuild 2015-01-06

* Mon May 26 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.1-14.7
- Mass rebuild 2014-05-26

* Wed Feb 19 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.1-14.6
- Mass rebuild 2014-02-19

* Tue Feb 18 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.1-14.5
- Mass rebuild 2014-02-18

* Tue Feb 18 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.1-14.4
- Remove requires on java

* Mon Feb 17 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.1-14.3
- SCL-ize build-requires

* Thu Feb 13 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.1-14.2
- Rebuild to regenerate auto-requires

* Tue Feb 11 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.1-14.1
- First maven30 software collection build

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 2.1-14
- Mass rebuild 2013-12-27

* Mon Aug 26 2013 Michal Srb <msrb@redhat.com> - 2.1-13
- Migrate away from mvn-rpmbuild (Resolves: #997503)

* Fri Jun 28 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.1-12
- Rebuild to regenerate API documentation
- Resolves: CVE-2013-1571

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 2.1-10
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Thu Aug 23 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.1-9
- Fix license tag
- Install NOTICE file
- Update to current packaging guidelines

* Fri Aug 10 2012 Andy Grimm <agrimm@gmail.com> - 2.1-8
- Update tomcat requirement to fix FTBFS

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Dec 1 2011 Alexander Kurtakov <akurtako@redhat.com> 2.1-5
- Fix the jaxrpc.jar symlink.

* Wed Nov 30 2011 Alexander Kurtakov <akurtako@redhat.com> 2.1-4
- Build with maven 3.
- Adapt to current guidelines.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Aug 2 2010 Chris Spike <chris.spike@arcor.de> 2.1-2
- Changed BR from 'servlet' to 'servlet >= 2.5'

* Thu Jul 22 2010 Chris Spike <chris.spike@arcor.de> 2.1-1
- Initial version of the package
