# ASUS C201

## Create Bootable SD Card

Original instructions adapted from
[Arch Linux ARM](http://archlinuxarm.org/platforms/armv7/rockchip/asus-chromebook-flip-c100p).

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

Original instructions adapted from
[here](https://gist.github.com/jcs/4bf59314d604538a5098).

    git clone git://git.savannah.nongnu.org/libreboot.git
    cd libreboot
    sudo ./build dependencies parabola

Note: see `resources/scripts/helpers/build/dependencies/parabola` for specific
packages. Likely you'll have to comment out the line that tests if you have the
`multilib` repository enabled, as it seems to be wrong. Afterwards execute the
following commands:

    ./download all
    ./build module all

Ensure that `/usr/bin/python` is symlinked to `/usr/bin/python2` instead of
`python3` before trying to build the ROM.

    ./build roms withdepthcharge veyron_speedy

If successful, the ROM will be in `coreboot/build/coreboot.rom`.

Now, disable SPI write protection by undoing the screw.

Backup the factory ROM.

    flashrom -r asus-c201-factory-spi.rom

You can use `fmap_decode` to view the contents of the ROM. Now, combine the
coreboot ROM with the factory ROM. We only use the first megabyte from the
coreboot ROM.

    dd if=coreboot.rom bs=1024 count=1024 of=firstmeg.rom
    dd if=asus-c201-factory-spi.rom bs=1024 skip=1024 of=latermegs.rom
    cat firstmeg.rom latermegs.rom > asus-c201-libreboot-spi.rom

Verify with `fmap_decode` that this final ROM looks like the factory ROM. Now
we're ready to flash. Ensure the write protect screw is out and run the
following commands:

    flashrom --wp-disable
    flashrom -w asus-c201-libreboot-spi.rom
    flashrom --wp-enable

Hope this works, otherwise you'll have to unbrick it yourself.
