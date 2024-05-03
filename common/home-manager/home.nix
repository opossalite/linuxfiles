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


    home.sessionVariables = {
        QT_QPA_PLATFORMTHEME = "qt5ct";
        EDITOR = "nvim";
    };


    # Theming
    
    #qogir, ultimate-maia, juno, ant themes, equilux

    gtk = {
        enable = true; #verify these names in lxappearance but don't use it
        theme.name = "Materia-dark";
        iconTheme.name = "Vimix-Black-dark";
    };
    qt = { #use qt5ct to configure icons, kvantum to configure theme!
        enable = true;
        platformTheme = "qtct";
    };


    nixpkgs.config.allowUnfree = true;
    nixpkgs.config.permittedInsecurePackages = [
        "electron-12.2.3"
        "electron-19.1.9"
    ];
    home.packages = with pkgs; [

        # themes
        materia-theme
        materia-kde-theme
        maia-icon-theme
        vimix-icon-theme


        # system utilities (makes the system run smoothly internally)
        cifs-utils
        curl
        dunst
        exfat
        libinput-gestures
        libvirt
        nfs-utils
        ntfs3g
        oh-my-zsh
        qemu
        samba
        virt-manager
        webp-pixbuf-loader
        wmctrl
        xclip


        # command-line programs (programs that run in the terminal)
        ark
        brightnessctl
        btop
        cli-visualizer
        colordiff
        distrobox
        dmidecode
        ffmpegthumbnailer
        fzf
        fzf-zsh
        htop
        imagemagick
        jupyter
        killall
        lf
        lolcat
        lshw
        most
        neofetch
        nms
        #nvidia-podman
        unstable.nvidia-container-toolkit
        nvtop
        redshift
        sshfs
        #texlive.combined.scheme-basic
        texliveMedium
        trash-cli
        tty-clock
        unrar
        unzip
        vim
        xdotool
        xorg.xcbproto
        xorg.xev
        xorg.xhost
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
        #contour
        cool-retro-term
        copyq
        deadbeef_
        easyeffects
        easytag
        etcher
        feh
        filelight
        flameshot
        gsimplecal
        helvum
        kitty
        libsForQt5.dolphin
        libsForQt5.dolphin-plugins
        libsForQt5.ffmpegthumbs
        #libsForQt5.kglobalaccel
        libsForQt5.gwenview
        libsForQt5.kdegraphics-thumbnailers
        libsForQt5.kio-extras
        libsForQt5.phonon-backend-vlc
        #libsForQt5.plasma-workspace
        libsForQt5.qt5ct
        libsForQt5.qtstyleplugin-kvantum
        #libsForQt5.spectacle
        lxappearance
        networkmanagerapplet
        nitrogen
        pasystray
        pavucontrol
        pcmanfm
        picom-jonaburg
        rofi
        xfce.thunar


        # development utilities (packages that help compile or develop code)
        #arduino
        #arduino-cli
        #arduino-language-server
        cudaPackages.cudatoolkit
        cudaPackages.cudnn
        ##go
        ##gopls
        ##julia-bin
        ##lua-language-server
        ##mypy
        ##nodePackages.pyright
        ##R
        ##rstudio
        ##rust-analyzer
        ##rustc
        ##zig
        ##zls
        zulu


        # desktop programs (user gui programs with few system dependencies)
        audacious
        audacity
        brave
        #unstable.discord
        discord
        gimp
        inkscape
        krita
        libreoffice
        librewolf
        libsForQt5.falkon
        obs-studio
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

