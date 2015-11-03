# Asus C201

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
