let
    shell_name = "py10";
in { pkgs ? import <nixpkgs> {} }:
  pkgs.mkShell {
    # nativeBuildInputs is usually what you want -- tools you need to run
    #nativeBuildInputs = with pkgs.buildPackages; [ ruby_3_2 ];
    #nativeBuildInputs = with pkgs.buildPackages; [ python3 ];
    name = "${shell_name}";
    packages = [
        (pkgs.python310.withPackages (ps: [
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
        python310
    ];
    shellHook = "
        export names=$names:${shell_name}
    ";
}
