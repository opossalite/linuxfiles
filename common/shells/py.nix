let
    shell_name = "py";
in { pkgs ? import <nixpkgs> {} }:
pkgs.mkShell {
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
            ps.torch
            ps.torchvision
        ]))
    ];
    nativeBuildInputs = with pkgs.buildPackages; [
        python311
    ];
    shellHook = "
        export names=$names:${shell_name}
    ";
}

