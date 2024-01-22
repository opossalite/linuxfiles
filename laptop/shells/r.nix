let
    shell_name = "r";
in { pkgs ? import <nixpkgs> {} }:
  pkgs.mkShell {
    # nativeBuildInputs is usually what you want -- tools you need to run
    #nativeBuildInputs = with pkgs.buildPackages; [ ruby_3_2 ];
    nativeBuildInputs = with pkgs.buildPackages; [
      R
      rstudio
      rPackages.tidyverse
      rPackages.maps
    ];
    name = "${shell_name}";
    shellHook = "
        export names=$names:${shell_name}
    ";
}

