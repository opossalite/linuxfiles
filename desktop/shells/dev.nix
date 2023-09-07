{ pkgs ? import <nixpkgs> {} }:
  pkgs.mkShell {
    # nativeBuildInputs is usually what you want -- tools you need to run
    #nativeBuildInputs = with pkgs.buildPackages; [ ruby_3_2 ];
    name = "dev";
    packages = [
        (pkgs.python3.withPackages (ps: [
            ps.numpy
        ]))
        pkgs.jq
        pkgs.curl
    ];
    #nativeBuildInputs = with pkgs.buildPackages; [
    #    python311
    #    python311Packages.pip
    #];
}
