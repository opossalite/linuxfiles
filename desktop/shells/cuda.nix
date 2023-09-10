# Run with `nix-shell cuda-shell.nix`
{ pkgs ? import <nixpkgs> {} }:
pkgs.mkShell {
    name = "cuda";
    buildInputs = with pkgs; [
        git gitRepo gnupg autoconf curl
        procps gnumake util-linux m4 gperf unzip
        cudatoolkit linuxPackages.nvidia_x11
        libGLU libGL
        xorg.libXi xorg.libXmu freeglut
        xorg.libXext xorg.libX11 xorg.libXv xorg.libXrandr zlib 
        ncurses5 stdenv.cc binutils
    ];
    shellHook = "
        export names=$names:cuda
        arrIN=(\${names//:/ })
        arrSTR=\${arrIN[@]}
        export PS1=\"$(tput sgr0)$(tput bold)$(tput setaf 15)\\u$(tput setaf 6) in \\
$(tput setaf 15)($arrSTR) $(tput setaf 4)\\w$(tput setaf 15)$(tput sgr0)\\n$(tput setaf 15)$ \"

    " + ''
        export CUDA_PATH=${pkgs.cudatoolkit}
        # export LD_LIBRARY_PATH=${pkgs.linuxPackages.nvidia_x11}/lib:${pkgs.ncurses5}/lib
        export EXTRA_LDFLAGS="-L/lib -L${pkgs.linuxPackages.nvidia_x11}/lib"
        export EXTRA_CCFLAGS="-I/usr/include"
   '';          
}
