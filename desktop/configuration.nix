{ config, pkgs, ... }:

let
  unstable = import <nixos-unstable> { config = { allowUnfree = true; }; };
in {
  imports =
    [
      ./hardware-configuration.nix
      <home-manager/nixos>
    ];



  ### Fix for NixOS 23.05

  nixpkgs.overlays = with pkgs; [
    (self: super: {
      fcitx-engines = fcitx5;
    })
  ];



  ### Bootloader

  boot.loader.grub.enable = true;
  boot.loader.grub.device = "/dev/sda";
  boot.loader.grub.useOSProber = true;



  ### System Settings

  system.stateVersion = "22.11";
  system.autoUpgrade = {
    enable = true;
  };
  networking.hostName = "MonoWolfPC";
  users.users.terrior = {
    isNormalUser = true;
    description = "terrior";
    extraGroups = [ "networkmanager" "wheel" "storage" "docker" ];
    packages = with pkgs; [  #ensure some packages are installed for the user, even if home-manager isn't working correctly
      firefox
    ];
  };



  ### System Configuration

  time.timeZone = "America/Los_Angeles";
  i18n.defaultLocale = "en_US.UTF-8";
  i18n.extraLocaleSettings = {
    LC_ADDRESS = "en_US.UTF-8";
    LC_IDENTIFICATION = "en_US.UTF-8";
    LC_MEASUREMENT = "en_US.UTF-8";
    LC_MONETARY = "en_US.UTF-8";
    LC_NAME = "en_US.UTF-8";
    LC_NUMERIC = "en_US.UTF-8";
    LC_PAPER = "en_US.UTF-8";
    LC_TELEPHONE = "en_US.UTF-8";
    LC_TIME = "en_US.UTF-8";
  };



  ### System Services

  networking.networkmanager.enable = true;
  # networking.wireless.enable = true;  # Enables wireless support via wpa_supplicant.
  # networking.firewall.allowedTCPPorts = [ ... ];  #open ports in the firewall
  # networking.firewall.allowedUDPPorts = [ ... ];
  # networking.firewall.enable = false;  #disable the firewall
  services.printing.enable = true;  #printing via CUPS
  # services.xserver.libinput.enable = true;  #enable touchpad support
  # services.openssh.enable = true;  #OpenSSH daemon



  ### Mounting
  
  services.devmon.enable = true;
  services.gvfs.enable = true;
  services.udisks2.enable = true;
  boot.supportedFilesystems = [ "ntfs" ];



  ### Display Server

  services.xserver = {
    enable = true;
    layout = "us";
    xkbVariant = "";
    videoDrivers = [ "nvidia" ];
    displayManager.lightdm.enable = true;
    desktopManager.gnome.enable = true;
    windowManager.qtile.enable = true;
    windowManager.awesome = {
      enable = true;
      luaModules = with pkgs.luaPackages; [
        luarocks  #package manager for Lua modules
	luadbi-mysql  #database abstraction layer
      ];
    };
  };
  hardware.opengl.driSupport32Bit = true;



  ### Audio

  sound.enable = true;
  hardware.pulseaudio.enable = false;  #don't use pulseaudio
  security.rtkit.enable = true;
  services.pipewire = {
    enable = true;
    alsa.enable = true;
    alsa.support32Bit = true;
    pulse.enable = true;
    jack.enable = true;
  };



  ### Virtualization

  virtualisation = {
    podman = {
      enable = true;
      defaultNetwork.settings.dns_enabled = true;
    };
  };




  ################
  ### Packages ###
  ################



  ### Enabling Extras

  services.flatpak.enable = true;
  nixpkgs.config = {
    allowUnfree = true;

    permittedInsecurePackages = [
      "electron-12.2.3"
      "openssl-1.1.1u"
    ];
  };



  ### System Packages

  environment.systemPackages = with pkgs; [
    wget
    neovim
    git
    qtile
    python3
    xorg.libxcb.dev
    udevil

    gcc_multi
    clang_multi
    clang-tools
    libclang
    glibc
    gnumake
  ];



  ### Fonts

  fonts.fonts = with pkgs; [
    (nerdfonts.override { fonts = ["SourceCodePro"]; })
  ];



  ### User Packages (with Home Manager)

  home-manager.useGlobalPkgs = true;
  home-manager.users.terrior = { pkgs, ... }: {
    home.stateVersion = "22.11";
    home.packages = with pkgs; [

      # command-line programs (programs that run in the terminal)
      lf
      neofetch
      htop
      btop
      lolcat
      nms
      xdotool
      xorg.xkill
      yad
      redshift
      distrobox
      zip
      unzip
      sshfs
      xorg.xmodmap

      nvtop



      # system utilities (makes the system run smoothly internally)
      ntfs3g
      exfat
      xclip
      cifs-utils
      samba
      dunst


      # desktop utilities (programs to make the system usable from the user's perspective)
      kitty
      rofi
      pavucontrol
      pasystray
      unstable.easyeffects
      flameshot
      cinnamon.nemo
      nitrogen
      picom-jonaburg
      networkmanagerapplet
      copyq
      lxappearance
      etcher
      xfce.thunar
      pcmanfm
      libsForQt5.dolphin
      easytag


      # development utilities (packages that help compile or develop code)
      rustc
      cargo
      rust-analyzer
      maturin
      ghc
      haskell-language-server
      mypy
      nodePackages.pyright
      go
      gopls
      lua-language-server
      julia-bin


      # desktop programs (user gui programs with few system dependencies)
      librewolf
      brave
      tor-browser-bundle-bin
      spotify
      vscode
      audacity
      libreoffice

      amberol
      strawberry
      audacious

      discord
      

      # games
      minecraft

    ];
  };
}

