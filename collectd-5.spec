Summary:	Statistics collection daemon for filling RRD files.
Name:		collectd
Version:	5.1.0
Release:	1%{?dist}
Source:		http://collectd.org/files/%{name}-%{version}.tar.gz
License:	GPL
Group:		System Environment/Daemons
BuildRoot:	%{_tmppath}/%{name}-%{version}-root
BuildRequires:  perl(ExtUtils::MakeMaker), perl(ExtUtils::Embed)
BuildRequires:	lm_sensors-devel, rrdtool-devel, libpcap-devel
BuildRequires:	net-snmp-devel, libstatgrab-devel, libxml2-devel
BuildRequires:	yajl-devel, libiptcdata-devel, java-1.6.0-openjdk-devel
BuildRequires:	curl-devel, libidn-devel, openssl-devel, iptables-devel
BuildRequires:	python-devel, ipvsadm, kernel-headers, bison, pkgconfig, flex, autoconf, libtool, libgcrypt-devel
BuildRequires:  libdbi-devel, libesmtp-devel, libmemcache-devel, libmemcached-devel, libnfnetlink-devel
BuildRequires:  libnotify-devel, OpenIPMI-devel, liboping-devel, varnish-libs-devel, libvirt-devel, protobuf-devel
Packager:	Gianluca Varisco <gianluca.varisco@gmail.com>
Vendor:		collectd development team <collectd@verplant.org>

%description
collectd is a small daemon which collects system information periodically and
provides mechanisms to monitor and store the values in a variety of ways. It
is written in C for performance. Since the daemon doesn't need to startup
every time it wants to update the values it's very fast and easy on the
system. Also, the statistics are very fine grained since the files are updated
every 10 seconds.

%package apache
Summary:	apache-plugin for collectd.
Group:		System Environment/Daemons
Requires:	collectd = %{version}, libcurl
%description apache
This plugin collects data provided by Apache's `mod_status'.

%package dbi
Summary:        dbi-plugin for collectd.
Group:          System Environment/Daemons
Requires:       collectd = %{version}, libdbi
%description dbi
This plugin executes SQL statements on a database and read back the result.

%package ipmi
Summary:        ipmi-plugin for collectd.
Group:          System Environment/Daemons
Requires:       collectd = %{version}, OpenIPMI
%description ipmi
This plugin reads hardware sensors from servers using the Intelligent Platform Management Interface (IPMI).

%package libvirt
Summary:        libvirt-plugin for collectd.
Group:          System Environment/Daemons
Requires:       collectd = %{version}, libvirt
%description libvirt
This plugin gathers statistics about virtualized guests on a system.

%package memcachec
Summary:        memcachec-plugin for collectd.
Group:          System Environment/Daemons
Requires:       collectd = %{version}, libmemcache
%description memcachec
This plugin connects to a memcached server, queries one or more given pages and parses the returned data.

%package notify_desktop
Summary:        notify_desktop-plugin for collectd.
Group:          System Environment/Daemons
Requires:       collectd = %{version}, libnotify
%description notify_desktop
This plugin displays notifications to the user via the desktop notification specification.

%package notify_email
Summary:        notify_email-plugin for collectd.
Group:          System Environment/Daemons
Requires:       collectd = %{version}, libnotify
%description notify_email
This plugin sends notifications to a configured email address.

%package ping
Summary:        ping-plugin for collectd.
Group:          System Environment/Daemons
Requires:       collectd = %{version}, liboping
%description ping
This plugin measures network latency using ICMP “echo requests".

%package varnish
Summary:        varnish-plugin for collectd.
Group:          System Environment/Daemons
Requires:       collectd = %{version}, varnish-libs
%description varnish
This plugin collects information about Varnish, an HTTP accelerator.

%package email
Summary:	email-plugin for collectd.
Group:		System Environment/Daemons
Requires:	collectd = %{version}, spamassassin
%description email
This plugin collects data provided by spamassassin.

%package mysql
Summary:	mysql-module for collectd.
Group:		System Environment/Daemons
Requires:	collectd = %{version}, mysql
BuildRequires:	mysql-devel
%description mysql
MySQL querying plugin. This plugins provides data of issued commands, called
handlers and database traffic.

%package memcache
Summary:    memcached-module for collectd
Group:      System-Environment/Daemons
Requires:   collectd = %{version}, memcached
BuildRequires:  memcached-devel
%description memcache
The memcached plugin connects to a memcached daemon and collects the
number of connections and requests handled by the daemon, the CPU
resources consumed, number of items cached, number of threads, and bytes
sent and received. This package only includes the memcached plugin.

%package nginx
Summary:	nginx-plugin for collectd.
Group:		System Environment/Daemons
Requires:	collectd = %{version}, libcurl
%description nginx
This plugin gets data provided by nginx.

%package sensors
Summary:	libsensors-module for collectd.
Group:		System Environment/Daemons
Requires:	collectd = %{version}, lm_sensors
%description sensors
This plugin for collectd provides querying of sensors supported by lm_sensors.

%package snmp
Summary:	snmp-module for collectd.
Group:		System Environment/Daemons
Requires:	collectd = %{version}, net-snmp
%description snmp
This plugin for collectd allows querying of network equipment using SNMP.

%package java
Summary:	java-module for collectd.
Group:		System Environment/Daemons
Requires:	collectd = %{version}, java-1.6.0-openjdk-devel >= 1.6
BuildRequires:	java-1.6.0-openjdk-devel >= 1.6
%description java
This plugin for collectd allows plugins to be written in Java and executed
in an embedded JVM.

%prep
rm -rf $RPM_BUILD_ROOT
%setup

%build
export JAVA_HOME=/usr/lib/jvm/java-1.6.0-openjdk-1.6.0.0.%{_arch}
export PATH=$PATH:$JAVA_HOME/bin
./configure --prefix=%{_prefix} --sbindir=%{_sbindir} --mandir=%{_mandir} --libdir=%{_libdir} --sysconfdir=%{_sysconfdir} --with-java=$JAVA_HOME --enable-java --disable-battery
make

%install
make install DESTDIR=$RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/etc/rc.d/init.d
mkdir -p $RPM_BUILD_ROOT/var/www/cgi-bin
cp contrib/redhat/init.d-collectd $RPM_BUILD_ROOT/etc/rc.d/init.d/collectd
cp contrib/collection.cgi $RPM_BUILD_ROOT/var/www/cgi-bin
cp contrib/collection.conf $RPM_BUILD_ROOT/etc/
mkdir -p $RPM_BUILD_ROOT/etc/collectd.d
mkdir -p $RPM_BUILD_ROOT/var/lib/collectd
### Clean up docs
find contrib/ -type f -exec %{__chmod} a-x {} \;

###Modify Config for Redhat Based Distros
sed -i 's:#BaseDir     "/usr/var/lib/collectd":BaseDir     "/var/lib/collectd":' $RPM_BUILD_ROOT/etc/collectd.conf
sed -i 's:#PIDFile     "/usr/var/run/collectd.pid":PIDFile     "/var/run/collectd.pid":' $RPM_BUILD_ROOT/etc/collectd.conf
sed -i 's:#PluginDir   "/usr/lib/collectd":PluginDir   "%{_libdir}/collectd":' $RPM_BUILD_ROOT/etc/collectd.conf
sed -i 's:#TypesDB     "/usr/share/collectd/types.db":TypesDB     "/usr/share/collectd/types.db":' $RPM_BUILD_ROOT/etc/collectd.conf
sed -i 's:#Interval     10:Interval     30:' $RPM_BUILD_ROOT/etc/collectd.conf
sed -i 's:#ReadThreads  5:ReadThreads  5:' $RPM_BUILD_ROOT/etc/collectd.conf
sed -i 's:^datadir.*:datadir\: "/var/lib/collectd/rrd":' $RPM_BUILD_ROOT/etc/collection.conf
sed -i 's:^libdir.*:libdir\: "/usr/lib64/collectd":' $RPM_BUILD_ROOT/etc/collection.conf

###Include broken out config directory
echo -e '\nInclude "/etc/collectd.d"' >> $RPM_BUILD_ROOT/etc/collectd.conf

##Move config contribs
cp contrib/redhat/apache.conf $RPM_BUILD_ROOT/etc/collectd.d/apache.conf
cp contrib/redhat/email.conf $RPM_BUILD_ROOT/etc/collectd.d/email.conf
cp contrib/redhat/sensors.conf $RPM_BUILD_ROOT/etc/collectd.d/sensors.conf
cp contrib/redhat/mysql.conf $RPM_BUILD_ROOT/etc/collectd.d/mysql.conf
cp contrib/redhat/nginx.conf $RPM_BUILD_ROOT/etc/collectd.d/nginx.conf
cp contrib/redhat/snmp.conf $RPM_BUILD_ROOT/etc/collectd.d/snmp.conf

%clean
#rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add collectd
/sbin/chkconfig collectd on

%preun
if [ "$1" = 0 ]; then
   /sbin/chkconfig collectd off
   /etc/init.d/collectd stop
   /sbin/chkconfig --del collectd
fi
exit 0

%postun
if [ "$1" -ge 1 ]; then
    /etc/init.d/collectd restart
fi
exit 0

%files
%defattr(-,root,root)
%doc AUTHORS COPYING ChangeLog INSTALL NEWS README contrib/
%config %attr(0644,root,root) /etc/collectd.conf
%config %attr(0644,root,root) /etc/collection.conf
%attr(0755,root,root) /etc/rc.d/init.d/collectd
%attr(0755,root,root) /var/www/cgi-bin/collection.cgi
%attr(0755,root,root) %{_sbindir}/collectd
%attr(0755,root,root) %{_bindir}/collectdctl
%attr(0755,root,root) %{_bindir}/collectd-nagios
%attr(0755,root,root) %{_sbindir}/collectdmon
%attr(0644,root,root) %{_mandir}/man1/*
%attr(0644,root,root) %{_mandir}/man5/*
%dir /etc/collectd.d

# client
%attr(0644,root,root) /usr/include/collectd/client.h
%attr(0644,root,root) /usr/include/collectd/lcc_features.h

%attr(0644,root,root) %{_libdir}/libcollectdclient.*
%attr(0644,root,root) %{_libdir}/pkgconfig/libcollectdclient.pc

# macro to grab binaries for a plugin, given a name
%define plugin_macro() \
%attr(0644,root,root) %{_libdir}/%{name}/%1.so* \
%attr(0644,root,root) %{_libdir}/%{name}/%1.a \
%attr(0644,root,root) %{_libdir}/%{name}/%1.la 

%plugin_macro apcups
%plugin_macro ascent
%plugin_macro bind
%plugin_macro conntrack
%plugin_macro contextswitch
%plugin_macro cpufreq
%plugin_macro cpu
%plugin_macro csv
%plugin_macro curl
%plugin_macro curl_json
%plugin_macro curl_xml
%plugin_macro dbi
%plugin_macro df
%plugin_macro disk
%plugin_macro dns
%plugin_macro entropy
%plugin_macro email
%plugin_macro ethstat
%plugin_macro exec
%plugin_macro filecount
%plugin_macro fscache
%plugin_macro hddtemp
%plugin_macro interface
%plugin_macro ipmi
%plugin_macro iptables
%plugin_macro ipvs
%plugin_macro irq
%plugin_macro libvirt
%plugin_macro load
%plugin_macro logfile
%plugin_macro madwifi
%plugin_macro match_empty_counter
%plugin_macro match_hashed
%plugin_macro match_regex
%plugin_macro match_timediff
%plugin_macro match_value
%plugin_macro mbmon
%plugin_macro md
%plugin_macro memcachec
%plugin_macro memory
%plugin_macro multimeter
%plugin_macro network
%plugin_macro nfs
%plugin_macro notify_desktop
%plugin_macro notify_email
%plugin_macro ntpd
%plugin_macro numa
%plugin_macro openvpn
%plugin_macro olsrd
%plugin_macro perl
%plugin_macro ping
%plugin_macro powerdns
%plugin_macro processes
%plugin_macro protocols
%plugin_macro python
%plugin_macro rrdtool
%plugin_macro serial
%plugin_macro sensors
%plugin_macro swap
%plugin_macro syslog
%plugin_macro table
%plugin_macro tail
%plugin_macro target_notification
%plugin_macro target_replace
%plugin_macro target_scale
%plugin_macro target_set
%plugin_macro target_v5upgrade
%plugin_macro tcpconns
%plugin_macro teamspeak2
%plugin_macro ted
%plugin_macro thermal
%plugin_macro threshold
%plugin_macro unixsock
%plugin_macro uptime
%plugin_macro users
%plugin_macro uuid
%plugin_macro varnish
%plugin_macro vmem
%plugin_macro vserver
%plugin_macro wireless
%plugin_macro write_graphite
%plugin_macro write_http

%attr(0644,root,root) %{_datadir}/%{name}/types.db

%exclude %{_libdir}/perl5/perllocal.pod
%attr(0755,root,root) %{_libdir}/perl5/auto/Collectd
%attr(0644,root,root) %{_libdir}/perl5/auto/Collectd/.packlist
%attr(0644,root,root) /usr/share/perl5/Collectd.pm
%attr(0644,root,root) /usr/share/perl5/Collectd/Unixsock.pm
%attr(0644,root,root) /usr/share/perl5/Collectd/Plugins/OpenVZ.pm
%attr(0644,root,root) /usr/share/perl5/Collectd/Plugins/Monitorus.pm
%attr(0644,root,root) /usr/share/man/man3/Collectd::Unixsock.3pm.gz

%exclude /usr/share/collectd/postgresql_default.conf

%dir /var/lib/collectd

#%if %with_java
%files java
%attr(0644,root,root) /usr/share/%{name}/java/*.jar
%plugin_macro java
#%endif

%files apache
%config %attr(0644,root,root) /etc/collectd.d/apache.conf
%plugin_macro apache

%files email
%attr(0644,root,root) %{_libdir}/%{name}/email.so*
%attr(0644,root,root) %{_libdir}/%{name}/email.la
%config %attr(0644,root,root) /etc/collectd.d/email.conf

%files memcache
%plugin_macro memcached

%files mysql
%config %attr(0644,root,root) /etc/collectd.d/mysql.conf
%plugin_macro mysql

%files nginx
%config %attr(0644,root,root) /etc/collectd.d/nginx.conf
%plugin_macro nginx

%files sensors
%attr(0644,root,root) %{_libdir}/%{name}/sensors.so*
%attr(0644,root,root) %{_libdir}/%{name}/sensors.la
%config %attr(0644,root,root) /etc/collectd.d/sensors.conf

%files snmp
%attr(0644,root,root) /etc/collectd.d/snmp.conf
%plugin_macro snmp

%changelog
* Tue Sep 4 2012 Gianluca Varisco <gianluca.varisco@gmail.com>
- New upstream version 5.1.0
- Cleaning up build dependencies
- Added dbi, ipmi, libvirt, memcachec, notify_desktop plug-ins
- Added notify_email, ping, varnish plug-ins
* Sun Jan 22 2012 Ulrich Habel <rhaen@cpan.org>
- New upstream version 5.0.2
- Cleaning up build dependencies bison, kernel-headers
- Enabled java plugin against openjdk by default
- Added memcache package
- removed CFLAGS
- added patch for build ipvs plugin
  (http://mailman.verplant.org/pipermail/collectd/2012-January/004899.html)

* Thu Jul 28 2011 Ulrich Habel <rhaen@cpan.org>
- Added BuildRequires python-devel, yajl-devel
- Added curl_json to files section

* Wed Jul 13 2011 Ulrich Habel <rhaen@cpan.org>
- configuration changes to collection.conf for RHEL

* Wed Jul 06 2011 Ulrich Habel <rhaen@cpan.org>
- New upstream version
- Changed BuildRequires
- Corrections to files section

* Tue Jan 04 2010 Rackspace <stu.hood@rackspace.com> 4.9.0
- New upstream version
- Changes to support 4.9.0
- Added support for Java/GenericJMX plugin

* Mon Mar 17 2008 RightScale <support@rightscale.com> 4.3.1
- New upstream version
- Changes to support 4.3.1
- Added More Prereqs to support more plugins
- Added support for perl plugin

* Mon Aug 06 2007 Kjell Randa <Kjell.Randa@broadpark.no> 4.0.6
- New upstream version

* Wed Jul 25 2007 Kjell Randa <Kjell.Randa@broadpark.no> 4.0.5
- New major releas
- Changes to support 4.0.5 

* Wed Jan 11 2007 Iain Lea <iain@bricbrac.de> 3.11.0-0
- fixed spec file to build correctly on fedora core
- added improved init.d script to work with chkconfig
- added %post and %postun to call chkconfig automatically

* Sun Jul 09 2006 Florian octo Forster <octo@verplant.org> 3.10.0-1
- New upstream version

* Tue Jun 25 2006 Florian octo Forster <octo@verplant.org> 3.9.4-1
- New upstream version

* Tue Jun 01 2006 Florian octo Forster <octo@verplant.org> 3.9.3-1
- New upstream version

* Tue May 09 2006 Florian octo Forster <octo@verplant.org> 3.9.2-1
- New upstream version

* Tue May 09 2006 Florian octo Forster <octo@verplant.org> 3.8.5-1
- New upstream version

* Fri Apr 21 2006 Florian octo Forster <octo@verplant.org> 3.9.1-1
- New upstream version

* Fri Apr 14 2006 Florian octo Forster <octo@verplant.org> 3.9.0-1
- New upstream version
- Added the `apache' package.

* Thu Mar 14 2006 Florian octo Forster <octo@verplant.org> 3.8.2-1
- New upstream version

* Thu Mar 13 2006 Florian octo Forster <octo@verplant.org> 3.8.1-1
- New upstream version

* Thu Mar 09 2006 Florian octo Forster <octo@verplant.org> 3.8.0-1
- New upstream version

* Sat Feb 18 2006 Florian octo Forster <octo@verplant.org> 3.7.2-1
- Include `tape.so' so the build doesn't terminate because of missing files..
- New upstream version

* Sat Feb 04 2006 Florian octo Forster <octo@verplant.org> 3.7.1-1
- New upstream version

* Mon Jan 30 2006 Florian octo Forster <octo@verplant.org> 3.7.0-1
- New upstream version
- Removed the extra `hddtemp' package

* Tue Jan 24 2006 Florian octo Forster <octo@verplant.org> 3.6.2-1
- New upstream version

* Fri Jan 20 2006 Florian octo Forster <octo@verplant.org> 3.6.1-1
- New upstream version

* Fri Jan 20 2006 Florian octo Forster <octo@verplant.org> 3.6.0-1
- New upstream version
- Added config file, `collectd.conf(5)', `df.so'
- Added package `collectd-mysql', dependency on `mysqlclient10 | mysql'

* Wed Dec 07 2005 Florian octo Forster <octo@verplant.org> 3.5.0-1
- New upstream version

* Sat Nov 26 2005 Florian octo Forster <octo@verplant.org> 3.4.0-1
- New upstream version

* Sat Nov 05 2005 Florian octo Forster <octo@verplant.org> 3.3.0-1
- New upstream version

* Tue Oct 26 2005 Florian octo Forster <octo@verplant.org> 3.2.0-1
- New upstream version
- Added statement to remove the `*.la' files. This fixes a problem when
  `Unpackaged files terminate build' is in effect.
- Added `processes.so*' to the main package

* Fri Oct 14 2005 Florian octo Forster <octo@verplant.org> 3.1.0-1
- New upstream version
- Added package `collectd-hddtemp'

* Fri Sep 30 2005 Florian octo Forster <octo@verplant.org> 3.0.0-1
- New upstream version
- Split the package into `collectd' and `collectd-sensors'

* Fri Sep 16 2005 Florian octo Forster <octo@verplant.org> 2.1.0-1
- New upstream version

* Mon Sep 10 2005 Florian octo Forster <octo@verplant.org> 2.0.0-1
- New upstream version

* Mon Aug 29 2005 Florian octo Forster <octo@verplant.org> 1.8.0-1
- New upstream version

* Sun Aug 25 2005 Florian octo Forster <octo@verplant.org> 1.7.0-1
- New upstream version

* Sun Aug 21 2005 Florian octo Forster <octo@verplant.org> 1.6.0-1
- New upstream version

* Sun Jul 17 2005 Florian octo Forster <octo@verplant.org> 1.5.1-1
- New upstream version

* Sun Jul 17 2005 Florian octo Forster <octo@verplant.org> 1.5-1
- New upstream version

* Mon Jul 11 2005 Florian octo Forster <octo@verplant.org> 1.4.2-1
- New upstream version

* Sat Jul 09 2005 Florian octo Forster <octo@verplant.org> 1.4-1
- Built on RedHat 7.3
