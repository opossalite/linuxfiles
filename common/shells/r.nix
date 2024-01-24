let
    shell_name = "r";
in { pkgs ? import <nixpkgs> {} }:
pkgs.mkShell {
    name = "${shell_name}";
    nativeBuildInputs = with pkgs.buildPackages; [
        R
        rstudio
        rPackages.ISLR
        rPackages.maps
        rPackages.SnowballC
        rPackages.tidyverse
        rPackages.tm
        rPackages.tokenizers
    ];
    shellHook = "
        export names=$names:${shell_name}
    ";
}

