# Asus C201

## Create Bootable SD Card

From http://archlinuxarm.org/platforms/armv7/rockchip/asus-chromebook-flip-c100p

    umount /dev/mmcblk1*
    fdisk /dev/mmcblk1

Type `g`, then type `w`.

    cgpt create /dev/mmcblk1
    cgpt add -i 1 -t kernel -b 8192 -s 32768 -l Kernel -S 1 -T 5 -P 10 /dev/mmcblk1

To create the rootfs partition, we first need to calculate how big to make the
partition using information from cgpt show. Look for the number under the start
column for Sec GPT table which is 15633375 in this example:

    cgpt add -i 2 -t data -b 40960 -s `expr 30949343 - 40960` -l Root /dev/mmcblk1
    sfdisk -R /dev/mmcblk1
    mkfs.ext4 /dev/mmcblk1p2
    cd /mnt/stateful_partition
    mkdir tmp
    cd tmp
    wget http://archlinuxarm.org/os/ArchLinuxARM-veyron-latest.tar.gz
    mkdir root
    mount /dev/mmcblk1p2 root
    tar -xf ArchLinuxARM-veyron-latest.tar.gz -C root
    dd if=root/boot/vmlinux.kpart of=/dev/mmcblk1p1
    umount root
    sync

## Libreboot

    git clone git://git.savannah.nongnu.org/libreboot.git
    cd libreboot
    sudo ./build dependencies parabola

Note: see `resources/scripts/helpers/build/dependencies/parabola` for specific
packages.

    ./download all
    cd coreboot
    make crossgcc-arm
    cd ..
    ./build module flashrom static
    ./build roms withdepthcharge veyron_speedy
