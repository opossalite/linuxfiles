{ config, pkgs, ... }:

let
  unstable = import <nixos-unstable> { config = { allowUnfree = true;}; };
in {
  home.username = "terrior";
  home.homeDirectory = "/home/terrior";
  home.stateVersion = "22.11"; #keep this as is


  # Let Home Manager install and manage itself.
  programs.home-manager.enable = true;


  #xdg.mimeApps.defaultApplications = {
  #    "text/plain" = [ "neovide.desktop" ];
  #};


  nixpkgs.config.allowUnfree = true;
  nixpkgs.config.permittedInsecurePackages = [
    "electron-19.1.9" #for something
    #"electron-24.8.6" #for obsidian
    "electron-25.9.0" #for inkscape
  ];
  home.packages = with pkgs; [
    ed

    # command-line tools
    hello

    btop
    distrobox
    dmidecode
    htop
    killall
    lf
    lolcat
    lshw
    neofetch
    nms
    redshift
    sshfs
    texlive.combined.scheme-basic
    trash-cli
    tty-clock
    unzip
    xdotool
    xorg.xkbcomp
    xorg.xkill
    xorg.xmodmap
    yad
    zip

    brightnessctl


    # system utilities (makes the system run smoothly internally)
    cifs-utils
    dunst
    exfat
    libinput-gestures
    ntfs3g
    pandoc
    samba
    wmctrl
    xclip
    xorg.xev


    # desktop utilities (programs to make the system usable from the user's perspective)
    alacritty
    arandr
    baobab
    cbatticon
    cinnamon.nemo
    conky
    copyq
    #unstable.easyeffects
    easyeffects
    easytag
    etcher
    gsimplecal
    feh
    flameshot
    kitty
    libsForQt5.dolphin
    lxappearance
    mlterm
    networkmanagerapplet
    nitrogen
    pasystray
    pavucontrol
    pcmanfm
    picom-jonaburg
    rofi
    rxvt-unicode-emoji
    st
    xfce.thunar


    # development utilities (packages that help compile or develop code other than c)
    cargo
    cudaPackages.cudatoolkit
    cudaPackages.cudnn
    ghc
    go
    gopls
    haskell-language-server
    julia-bin
    lua-language-server
    maturin
    mypy
    nodePackages.pyright
    rust-analyzer
    rustc
    zig
    zls
    zulu

    arduino


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
    #obsidian
    tor-browser-bundle-bin
    spotify
    vscode

    superTuxKart
  ];


  # The home.packages option allows you to install Nix packages into your
  # environment.
  #home.packages = [
    # # Adds the 'hello' command to your environment. It prints a friendly
    # # "Hello, world!" when run.
    #pkgs.hello

    # # It is sometimes useful to fine-tune packages, for example, by applying
    # # overrides. You can do that directly here, just don't forget the
    # # parentheses. Maybe you want to install Nerd Fonts with a limited number of
    # # fonts?
    # (pkgs.nerdfonts.override { fonts = [ "FantasqueSansMono" ]; })

    # # You can also create simple shell scripts directly inside your
    # # configuration. For example, this adds a command 'my-hello' to your
    # # environment:
    # (pkgs.writeShellScriptBin "my-hello" ''
    #   echo "Hello, ${config.home.username}!"
    # '')
  #];


  # Home Manager is pretty good at managing dotfiles. The primary way to manage
  # plain files is through 'home.file'.
  home.file = {
    # # Building this configuration will create a copy of 'dotfiles/screenrc' in
    # # the Nix store. Activating the configuration will then make '~/.screenrc' a
    # # symlink to the Nix store copy.
    # ".screenrc".source = dotfiles/screenrc;

    # # You can also set the file content immediately.
    # ".gradle/gradle.properties".text = ''
    #   org.gradle.console=verbose
    #   org.gradle.daemon.idletimeout=3600000
    # '';
  };
}

