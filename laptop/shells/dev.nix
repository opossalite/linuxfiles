{ pkgs ? import <nixpkgs> {} }:
  pkgs.mkShell {
    # nativeBuildInputs is usually what you want -- tools you need to run
    #nativeBuildInputs = with pkgs.buildPackages; [ ruby_3_2 ];
    name = "dev";
    #shellHook = "export PS1='\n\[\033[1;34m\][${name}:\w]\$\[\033[0m\]' ";
    #shellHook = "export PS1='\n\[\033[1;34m\][test:\w]\$\[\033[0m\]' ";

    #RESET_="\[$(tput sgr0)\]"
    #BOLD_="\[$(tput bold)\]"
    #WHITE_="\[$(tput setaf 15)\]"
    #BRACKET_="\[$(tput setaf 21)\]"
    #USER_="\[$(tput setaf 240)\]"
    #HOST_="\[$(tput setaf 2)\]"
    #DIR_="\[$(tput setaf 4)\]"

    #PS1="${BOLD_}${WHITE_}\u${HOST_}@\h${WHITE_}:${DIR_}\w${WHITE_}$ ${RESET_}${WHITE_}"

    shellHook = "export PS1=\"\${HOSTNAME}> \"";
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
