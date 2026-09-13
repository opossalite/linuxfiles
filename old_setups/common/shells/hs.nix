let
    shell_name = "hs";
in { pkgs ? import <nixpkgs> {} }:
pkgs.mkShell {
    name = "${shell_name}";
    nativeBuildInputs = with pkgs.buildPackages; [
        ghc
        haskell-language-server
        haskellPackages.cabal-install
    ];
    shellHook = "
        export names=$names:${shell_name}
    ";
}

