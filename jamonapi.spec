%{?_javapackages_macros:%_javapackages_macros}
%global oname jamon

Name:          jamonapi
Version:       2.74
Release:       4.3
Summary:       A Java monitoring API
Group:		Development/Java
License:       BSD
URL:           https://jamonapi.sourceforge.net/
# cvs -d:pserver:anonymous@jamonapi.cvs.sourceforge.net:/cvsroot/jamonapi login
# cvs -z3 -d:pserver:anonymous@jamonapi.cvs.sourceforge.net:/cvsroot/jamonapi co -P -r v2_74 jamonapi/src
# Remove pregenerated javadoc files in the source tree
# rm -rf jamonapi/src/JAMonUsersGuide/javadoc/*
# Remove zip file which contains a proprietary binary
# rm -rf jamonapi/src/JAMonUsersGuide/JAMon_PB.zip
# rm -rf $(find -name "CVS")
# tar cJf jamonapi-2.74.tar.xz jamonapi
Source0:       %{name}-%{version}.tar.xz
# This POM is completely Fedora-specific
Source1:       %{name}-%{version}.pom
Patch0:        %{name}-buildxml.patch
Patch1:        %{name}-jetty8.patch
Patch2:		%{name}-log4j12.patch

BuildRequires: java-devel
BuildRequires: javapackages-tools
BuildRequires: ant
BuildRequires: tomcat-lib
BuildRequires: tomcat-servlet-3.0-api
BuildRequires: tomcat-el-2.2-api
BuildRequires: jetty
BuildRequires: geronimo-interceptor
BuildRequires: log4j12
BuildRequires: dos2unix
Requires:      java
Requires:      javapackages-tools
Requires:      tomcat-lib
Requires:      tomcat-servlet-3.0-api
Requires:      tomcat-el-2.2-api
Requires:      jetty
Requires:      geronimo-interceptor
Requires:      log4j12
BuildArch:     noarch

%description
JAMon API is a free, simple, high performance, thread safe,
Java API that allows developers to easily monitor the
performance and scalability of production applications. JAMon
tracks hits, execution times (total, avg, min, max, std dev),
and more.

%package javadoc
Summary:         API documentation for %{name}

%description javadoc
This package contains API documentation for Java monitoring API.

%prep
%setup -q -n %{name}
%patch0 -p0
%patch1 -p1
%patch2 -p1
mkdir dist
mkdir lib

# jetty 9 build fix
sed -i "s|BlockingHttpConnection|HttpChannel|" \
 src/java/com/jamonapi/http/JAMonJettyHandler.java
sed -i "s|getCurrentConnection()|getCurrentHttpChannel()|" \
 src/java/com/jamonapi/http/JAMonJettyHandler.java
 
%build
pushd src/ant
ant JAR
ant javadoc
popd

# Remove spurious executable permissions
find src/JAMonUsersGuide -type f | xargs chmod -x
find src/JAMonUsersGuide -regex '.*\(xml\|css\|js\)' -o -name package-list | xargs dos2unix

# There should be a shorter way to do an iconv task, but I do not know of one
pushd src/JAMonUsersGuide/presentation/jamon_files/
mv master04_stylesheet.css master04_stylesheet.css.iso8859-1
iconv -f ISO-8859-1 -t UTF-8 master04_stylesheet.css.iso8859-1 > master04_stylesheet.css
rm master04_stylesheet.css.iso8859-1
popd

%install

mkdir -p %{buildroot}%{_javadir}
install -m 644 dist/%{oname}-%{version}.jar %{buildroot}%{_javadir}/%{name}.jar
ln -s %{name}.jar %{buildroot}%{_javadir}/%{oname}.jar

mkdir -p %{buildroot}%{_mavenpomdir}
install -pm 644 %{SOURCE1} %{buildroot}%{_mavenpomdir}/JPP-%{oname}.pom
%add_maven_depmap JPP-%{oname}.pom %{oname}.jar

mkdir -p %{buildroot}%{_javadocdir}
cp -rp src/doc/javadoc %{buildroot}%{_javadocdir}/%{name}

%files -f .mfiles
%doc src/JAMonUsersGuide
%{_javadir}/%{name}.jar

%files javadoc
%doc src/JAMonUsersGuide/JAMonLicense.html
%{_javadocdir}/%{name}

%changelog
* Sun Oct 13 2013 gil cattaneo <puntogil@libero.it> 2.74-2
- fix project url

* Sun Oct 13 2013 gil cattaneo <puntogil@libero.it> 2.74-1
- update to 2.74

* Sat Aug 17 2013 gil cattaneo <puntogil@libero.it> 2.73-9
- fix rhbz#992588
- build fix for jetty 9.x
- minor changes to adapt to current guideline

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.73-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.73-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.73-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Mar 14 2012 Andy Grimm <agrimm@gmail.com> 2.73-5
- Update POM to reflect current jetty and tomcat deps

* Sun Feb 26 2012 Andy Grimm <agrimm@gmail.com> 2.73-4
- remove duplicate javadoc directory
- Remove PowerBuilder example zipfile

* Thu Feb 16 2012 Andy Grimm <agrimm@gmail.com> 2.73-3
- add javadoc subpackage

* Tue Feb 14 2012 Andy Grimm <agrimm@gmail.com> 2.73-2
- Update for Jetty 8

* Tue Dec 20 2011 Andy Grimm <agrimm@gmail.com> 2.73-1
- Initial Package
