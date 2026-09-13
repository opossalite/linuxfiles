let
    shell_name = "pytest";
in { pkgs ? import <nixpkgs> {} }:
(pkgs.buildFHSUserEnv {
    name = "${shell_name}";
    targetPkgs = pkgs: (with pkgs; [
        python311
        python311Packages.pip
        python39Packages.virtualenv
        cudaPackages.cudatoolkit
    ]);
    #runScript = "export names=$names:${shell_name}";
    runScript = "bash; echo hi";
}).env

