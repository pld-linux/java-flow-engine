#
# Conditional build:
%bcond_without	javadoc		# don't build javadoc

%define		srcname	flow-engine
%include	/usr/lib/rpm/macros.java
Summary:	Pentaho Flow Reporting Engine
Name:		java-%{srcname}
Version:	0.9.4
Release:	0.1
License:	LGPL v2+
Group:		Libraries/Java
Source0:	http://downloads.sourceforge.net/jfreereport/%{srcname}-%{version}.zip
URL:		http://reporting.pentaho.org/
BuildRequires:	ant
BuildRequires:	java-flute
BuildRequires:	java-libbase
BuildRequires:	java-libloader
BuildRequires:	java-libxml
BuildRequires:	java-sac
BuildRequires:	java-xml-commons
BuildRequires:	jdk
BuildRequires:	jpackage-utils
BuildRequires:	libfonts
BuildRequires:	libformula
BuildRequires:	liblayout
BuildRequires:	librepository
BuildRequires:	libserializer
BuildRequires:	rpmbuild(macros) >= 1.300
Requires:	java-flute
Requires:	java-libbase >= 1.1.3
Requires:	java-libxml
Requires:	java-sac
Requires:	jpackage-utils
Requires:	libfonts >= 1.1.3
Requires:	libformula >= 1.1.3
Requires:	liblayout >= 0.2.10
Requires:	librepository >= 1.1.3
Requires:	libserializer
Obsoletes:	pentaho-reporting-flow-engine
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Pentaho Reporting Flow Engine is a free Java report library, formerly
known as 'JFreeReport'

%package javadoc
Summary:	Javadoc for Flow Engine
Group:		Documentation
Requires:	jpackage-utils

%description javadoc
Javadoc for Flow Engine.

%prep
%setup -qc
install -d lib
find -name "*.jar" | xargs rm -v

%build
build-jar-repository -s -p lib commons-logging-api libbase libloader \
	libfonts libxml jaxp libformula librepository sac flute liblayout \
	libserializer

%ant jar %{?with_javadoc:javadoc}

%install
rm -rf $RPM_BUILD_ROOT

# jars
install -d $RPM_BUILD_ROOT%{_javadir}
cp -a build-lib/%{srcname}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}-%{version}.jar
ln -s %{srcname}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}.jar

# javadoc
%if %{with javadoc}
install -d $RPM_BUILD_ROOT%{_javadocdir}/%{srcname}-%{version}
cp -a build/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{srcname}-%{version}
ln -s %{srcname}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{srcname} # ghost symlink
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
ln -nfs %{srcname}-%{version} %{_javadocdir}/%{srcname}

%files
%defattr(644,root,root,755)
%doc licence-LGPL.txt README.txt ChangeLog.txt
%{_javadir}/%{srcname}.jar
%{_javadir}/%{srcname}-%{version}.jar

%if %{with javadoc}
%files javadoc
%defattr(644,root,root,755)
%{_javadocdir}/%{srcname}-%{version}
%ghost %{_javadocdir}/%{srcname}
%endif
