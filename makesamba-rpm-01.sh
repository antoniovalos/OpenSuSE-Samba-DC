#  every full  rpmbuild run take more then 8h  on an RPi model B
#  so we run that at background .
#
#  this script was written to check the samba BUILD that we preveniosly
#  prepared with Hint helps from  makesamba.sh and checksamba4-dependencyiesa.sh logs

# After that we do check the nohup.out log
#
# you can run this script with :  nohup makesamba-rpm-01.sh &
#



CPPFLAGS="-Ofast -mfpu=vfp -march=armv6zk -mtune=arm1176jzf-s"
CFLAGS="-Ofast -mfpu=vfp -march=armv6zk -mtune=arm1176jzf-s"

cd /srv/PROJ/samba4.1/BUILD/4.1.3

nohup rpmbuild -ba samba-4.1.3_01.spec &
