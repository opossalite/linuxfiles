let
    shell_name = "py";
in { pkgs ? import <nixpkgs> {} }:
  pkgs.mkShell {
    # nativeBuildInputs is usually what you want -- tools you need to run
    #nativeBuildInputs = with pkgs.buildPackages; [ ruby_3_2 ];
    #nativeBuildInputs = with pkgs.buildPackages; [ python3 ];
    name = "${shell_name}";
    packages = [
        (pkgs.python311.withPackages (ps: [
            ps.matplotlib
            ps.numpy
            ps.pandas
            ps.pynput
            ps.qtile
            ps.scikit-learn
            ps.scipy
            #ps.torch


        ]))
    ];
    nativeBuildInputs = with pkgs.buildPackages; [
        python311
    ];
    shellHook = "
        export names=$names:${shell_name}
    ";
}
