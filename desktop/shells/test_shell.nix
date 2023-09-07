{ pkgs ? import <nixpkgs> {} }:
  pkgs.mkShell {
      name = "hello";
    # nativeBuildInputs is usually what you want -- tools you need to run
    #nativeBuildInputs = with pkgs.buildPackages; [ ruby_3_2 ];
    nativeBuildInputs = with pkgs.buildPackages; [
        python311
    ];
}
