yum localinstall -y --nogpgcheck https://download1.rpmfusion.org/free/el/rpmfusion-free-release-7.noarch.rpm

yum install -y https://vault.centos.org/7.9.2009/os/x86_64/Packages/libva-1.8.3-1.el7.x86_64.rpm
yum install -y https://vault.centos.org/7.9.2009/os/x86_64/Packages/libva-devel-1.8.3-1.el7.x86_64.rpm

yum install -y ffmpeg ffmpeg-devel