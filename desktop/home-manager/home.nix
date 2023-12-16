{ config, pkgs, ... }:

let unstable = import <nixos-unstable> { config = { allowUnfree = true; }; };
in {
  home.username = "terrior";
  home.homeDirectory = "/home/terrior";
  home.stateVersion = "22.11";

  # Let Home Manager install and manage itself.
  programs.home-manager.enable = true;

  nixpkgs.overlays = [
    (self: super: {
      fcitx-engines = pkgs.fcitx5;
    })
  ];

  nixpkgs.config.allowUnfree = true;
  nixpkgs.config.permittedInsecurePackages = [
    "electron-12.2.3"
    "electron-19.1.9"
  ];
  home.packages = with pkgs; [

    hello
    jupyter

    # command-line programs (programs that run in the terminal)
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
    pandoc
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
    zip
    zlib

    nvtop


    # system utilities (makes the system run smoothly internally)
    cifs-utils
    curl
    dunst
    exfat
    ntfs3g
    samba
    webp-pixbuf-loader
    xclip
    xorg.xev


    # desktop utilities (programs to make the system usable from the user's perspective)
    arandr
    cinnamon.nemo
    conky
    copyq
    easytag
    etcher
    flameshot
    #gnome.gnome-calendar
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
    unstable.easyeffects
    xfce.thunar


    # development utilities (packages that help compile or develop code)
    arduino
    arduino-cli
    arduino-language-server
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
    R
    rstudio
    rust-analyzer
    rustc
    zig
    zulu


    # desktop programs (user gui programs with few system dependencies)
    audacious
    audacity
    brave
    discord
    krita
    libreoffice
    librewolf
    libsForQt5.falkon
    spotify
    tor-browser-bundle-bin
    vlc
    vscode
    #zoom-us


    # games
    #minecraft

  ];

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

  # You can also manage environment variables but you will have to manually
  # source
  #
  #  ~/.nix-profile/etc/profile.d/hm-session-vars.sh
  #
  # or
  #
  #  /etc/profiles/per-user/terrior/etc/profile.d/hm-session-vars.sh
  #
  # if you don't want to manage your shell through Home Manager.
  home.sessionVariables = {
    # EDITOR = "emacs";
  };

}

