#!bin/bash 

cd $(dirname $0)

sudo yum install yum-utils redhat-rpm-config rpm-build make gcc spectool


mkdir -p ~/rpmbuild/{BUILD,RPMS,SOURCES,SPECS,SRPMS}
echo '%_topdir %(echo $HOME)/rpmbuild' > ~/.rpmmacros

mv collectd-5.spec ~/rpmbbuild/SPECS/
spectool -g rpmbuild/SPECS/collectd-5.spec 
mv collectd-5.1.0.tar.gz ~/rpmbuild/SOURCES/

sudo yum-builddep ~/build/SPEC/collectd-5.spec


rpmbuild -ba ~/rpmbuild/SPECS/collectd-5.spec


