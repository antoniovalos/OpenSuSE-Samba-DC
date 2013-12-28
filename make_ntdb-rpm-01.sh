cd /srv/PROJ/samba4.1/sources/ntdb

CPPFLAGS="-Ofast -mfpu=vfp -march=armv6zk -mtune=arm1176jzf-s"
CFLAGS="-Ofast -mfpu=vfp -march=armv6zk -mtune=arm1176jzf-s"

cd /srv/GIT/samba4.1/BUILD/4.1.5

nohup rpmbuild -ba libntdb-1.0.spec &
