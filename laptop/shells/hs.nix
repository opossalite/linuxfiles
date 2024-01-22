let
    shell_name = "hs";
in { pkgs ? import <nixpkgs> {} }:
  pkgs.mkShell {
    # nativeBuildInputs is usually what you want -- tools you need to run
    #nativeBuildInputs = with pkgs.buildPackages; [ ruby_3_2 ];
    nativeBuildInputs = with pkgs.buildPackages; [
      ghc
      haskell-language-server
      haskellPackages.split
      haskellPackages.Cabal
    ];
    name = "${shell_name}";
    shellHook = "
        export names=$names:${shell_name}
    ";
}

