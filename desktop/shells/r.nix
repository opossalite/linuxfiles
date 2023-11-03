let
    shell_name = "r";
in { pkgs ? import <nixpkgs> {} }:
  pkgs.mkShell {
    # nativeBuildInputs is usually what you want -- tools you need to run
    #nativeBuildInputs = with pkgs.buildPackages; [ ruby_3_2 ];
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
    name = "${shell_name}";
    shellHook = "
        export names=$names:${shell_name}
    ";
}

