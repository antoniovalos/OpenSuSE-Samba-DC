#  every full  make run take more then 6h  on an RPi model B
#  so we run that at background .
#
#  this script was written to check the samba BUILD that we preveniosly
#  prepared with Hint helps from checksamba4-dependencyiesa.sh logs

# After that we do check the log
#
# you can run this script with :  nohup ./makesamba.sh
#

CPPFLAGS="-Ofast -mfpu=vfp -march=armv6zk -mtune=arm1176jzf-s"
CFLAGS="-Ofast -mfpu=vfp -march=armv6zk -mtune=arm1176jzf-s"

cd /srv/PROJ/samba4.1/BUILD/4.1.3/samba-master
./configure --prefix=/usr \
        --sysconfdir=/etc \
        --localstatedir=/var/run \
        --enable-fhs \
        --enable-socket-wrapper \
        --with-ads \
        --with-winbind \
        --enable-gnutls \
        --with-ldap \
        --with-pam \
        --with-regedit \
        --with-dmapi

make -j2
