{ config, pkgs, ... }:

let
    unstable = import <nixos-unstable> { config = { allowUnfree = true; }; };
    deadbeef_ = pkgs.deadbeef.override {
        wavpackSupport = true;
    };
in {
    home.username = "terrior";
    home.homeDirectory = "/home/terrior";
    home.stateVersion = "22.11"; #don't touch


    # Let Home Manager install and manage itself.
    programs.home-manager.enable = true;


    nixpkgs.config.allowUnfree = true;
    nixpkgs.config.permittedInsecurePackages = [
        "electron-12.2.3"
        "electron-19.1.9"
    ];
    home.packages = with pkgs; [

        # system utilities (makes the system run smoothly internally)
        cifs-utils
        curl
        dunst
        exfat
        libinput-gestures
        ntfs3g
        samba
        webp-pixbuf-loader
        wmctrl
        xclip


        # command-line programs (programs that run in the terminal)
        brightnessctl
        btop
        cli-visualizer
        colordiff
        distrobox
        dmidecode
        htop
        jupyter
        killall
        lf
        lolcat
        lshw
        most
        neofetch
        nms
        nvtop
        redshift
        sshfs
        texlive.combined.scheme-basic
        trash-cli
        tty-clock
        unzip
        vim
        xdotool
        xorg.xcbproto
        xorg.xev
        xorg.xkbcomp
        xorg.xkill
        xorg.xmodmap
        zip
        zlib


        # desktop utilities (programs to make the system usable from the user's perspective)
        alacritty
        arandr
        baobab
        cbatticon
        cinnamon.nemo
        conky
        contour
        cool-retro-term
        copyq
        deadbeef_
        easyeffects
        easytag
        etcher
        feh
        flameshot
        gsimplecal
        kitty
        libsForQt5.dolphin
        lxappearance
        networkmanagerapplet
        nitrogen
        pasystray
        pavucontrol
        pcmanfm
        picom-jonaburg
        rofi
        wezterm
        xfce.thunar


        # development utilities (packages that help compile or develop code)
        #arduino
        #arduino-cli
        #arduino-language-server
        cudaPackages.cudatoolkit
        cudaPackages.cudnn
        go
        gopls
        julia-bin
        lua-language-server
        mypy
        nodePackages.pyright
        R
        rstudio
        rust-analyzer
        rustc
        zig
        zls
        zulu


        # desktop programs (user gui programs with few system dependencies)
        audacious
        audacity
        brave
        discord
        inkscape
        krita
        libreoffice
        librewolf
        libsForQt5.falkon
        spotify
        steam
        tor-browser-bundle-bin
        vlc
        vscode
        #zoom-us


        # games
        #minecraft
        superTuxKart
    ];
}

