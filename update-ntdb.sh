cd /srv/PROJ/samba4.1/sources/ntdb
git clone git://git.debian.org/pkg-samba/ntdb.git
cd ntdb
cd git checkout
cd /srv/PROJ/samba4.1/sources/ntdb
if [ -d ntdb-1.0 ]; then
rm -rf ntdb-1.0
fi
mv ntdb ntdb-1.0
tar cpfz ntdb-1.0.tar.gz  ntdb-1.0
cp -p ntdb-1.0.tar.gz /usr/src/packages/SOURCES

