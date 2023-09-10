{ pkgs ? import <nixpkgs> {} }:
  pkgs.mkShell {
    # nativeBuildInputs is usually what you want -- tools you need to run
    #nativeBuildInputs = with pkgs.buildPackages; [ ruby_3_2 ];
    name = "dev";
    packages = [
        (pkgs.python3.withPackages (ps: [
            ps.numpy
        ]))
    ];
    #nativeBuildInputs = with pkgs.buildPackages; [
    #    python311
    #    python311Packages.pip
    #];
    shellHook = "
        export names=$names:dev
        arrIN=(\${names//:/ })
        arrSTR=\${arrIN[@]}
        export PS1=\"$(tput sgr0)$(tput bold)$(tput setaf 15)\\u$(tput setaf 6) in \\
$(tput setaf 15)($arrSTR) $(tput setaf 4)\\w$(tput setaf 15)$(tput sgr0)\\n$(tput setaf 15)$ \"

    ";
}
