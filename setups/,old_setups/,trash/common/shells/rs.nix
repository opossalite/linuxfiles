let
    shell_name = "rs";
in { pkgs ? import <nixpkgs> {} }:
pkgs.mkShell {
    name = "${shell_name}";
    nativeBuildInputs = with pkgs.buildPackages; [
        rustc
        cargo
        maturin
    ];
    shellHook = "
        export names=$names:${shell_name}
    ";
}

