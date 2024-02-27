let
    shell_name = "c";
in { pkgs ? import <nixpkgs> {} }:
pkgs.mkShell {
    name = "${shell_name}";
    nativeBuildInputs = with pkgs.buildPackages; [
        deadbeef
        fftw
        gtk2
        #gtk2-x11
        #gtkmm2
        gtk3
        #gtk3-x11
        #gtkmm3
        #gtk4
        #gtkmm4
        pkg-config
        sqlite

        bison
        flex
        ncurses
        #_9base
        bc
        libelf
        #libelfin
        elfutils
        bmake
        eflio
        #gnused
        coreutils-full
        kmod
        cpio
        gettext
        graphviz
        imagemagick
        pahole
        perl
        python3
        sphinx
        xz
    ];
    shellHook = "
        export names=$names:${shell_name}
    ";
}

