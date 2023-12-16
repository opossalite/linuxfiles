let
    shell_name = "pypy";
in { pkgs ? import <nixpkgs> {} }:
  pkgs.mkShell {
    # nativeBuildInputs is usually what you want -- tools you need to run
    #nativeBuildInputs = with pkgs.buildPackages; [ ruby_3_2 ];
    #nativeBuildInputs = with pkgs.buildPackages; [ python3 ];
    name = "${shell_name}";
    packages = [
        (pkgs.python310.withPackages (ps: [
            #ps.jupyterlab
            ps.matplotlib
            ps.numpy
            ps.pandas
            #ps.progress
            ps.pynput
            ps.qtile
            ps.scikit-learn
            #ps.scipy
            ps.torch
            #ps.torchvision
            #ps.tqdm

            ps.pypytools
        ]))
    ];
    nativeBuildInputs = with pkgs.buildPackages; [
        #python311
        python310
        pypy310
    ];
    shellHook = "
        export names=$names:${shell_name}
    ";
}

