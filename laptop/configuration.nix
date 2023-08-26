# Edit this configuration file to define what should be installed on
# your system.  Help is available in the configuration.nix(5) man page
# and in the NixOS manual (accessible by running ‘nixos-help’).

{ config, pkgs, ... }:

{
  imports =
    [ # Include the results of the hardware scan.
      ./hardware-configuration.nix
      <home-manager/nixos>
    ];



  ### Random fix for NixOS 23.05

  nixpkgs.overlays = with pkgs; [
    (self: super: {
      fcitx-engines = fcitx5;
    })
  ];



  ### Bootloader

  boot.loader.systemd-boot.enable = true;
  boot.loader.efi.canTouchEfiVariables = true;
  boot.loader.efi.efiSysMountPoint = "/boot/efi";
  boot.loader.systemd-boot.configurationLimit = 1;
  


  #boot.initrd.kernelModules = [ "wl" ];
  #boot.kernelModules = [ "kvm-intel" "wl" ];
  #boot.extraModulePackages = [ config.boot.kernelPackages.broadcom_sta ];



  ### System Settings

  system.stateVersion = "22.11";
  system.autoUpgrade = {
    enable = true;
  };
  networking.hostName = "CobaltCanidPC";
  users.users.terrior = {
    isNormalUser = true;
    description = "terrior";
    extraGroups = [ "networkmanager" "wheel" "storage" "docker"];
    packages = with pkgs; [ #ensure some packages are installed for the user, even if home-manager isn't working correctly
      firefox
    ];
  };



  systemd.services.wpa_supplicant.environment.OPENSSL_CONF = pkgs.writeText"openssl.cnf"''
  openssl_conf = openssl_init
  [openssl_init]
  ssl_conf = ssl_sect
  [ssl_sect]
  system_default = system_default_sect
  [system_default_sect]
  Options = UnsafeLegacyRenegotiation
  [system_default_sect]
  CipherString = Default:@SECLEVEL=0
  ''
  ;



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
  #networking.wireless.enable = false;
  #networking.wireless.networks.wlp0s20f3.psk = "<psk>";
  #networking.wireless.wifi.backend = "iwd";
  #networking.useDHCP = false;
  #networking.interfaces.eno1.useDHCP = true;
  # networking.firewall.allowedTCPPorts = [ ... ]; #open ports in the firewall
  # networking.firewall.allowedUDPPorts = [ ... ];
  # networking.firewall.enable = false;
  services.printing.enable = true; #printing via CUPS
  services.xserver.libinput.enable = true; #enable touchpad support
  # services.openssh.enable = true;



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
    #displayManager.gdm.enable = true;
    displayManager.lightdm.enable = true;
    displayManager.defaultSession = "none+qtile";
    desktopManager.gnome.enable = true;
    windowManager.qtile.enable = true;
    windowManager.awesome = {
      enable = true;
      luaModules = with pkgs.luaPackages; [
        luarocks #package manager for Lua modules
	luadbi-mysql #database abstraction layer
      ];
    };
  };
  hardware.opengl.driSupport32Bit = true;



  ### Audio

  sound.enable = true;
  hardware.pulseaudio.enable = false; #don't use pulseaudio
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

  services.flatpak.enable = true;
  nixpkgs.config = {
    allowUnfree = true;

    permittedInsecurePackages = [
      "electron-12.2.3"
      "openssl-1.1.1v"
    ];
  };
  #buildInputs = [ stdenv.cc.cc.lib ];



  # List packages installed in system profile. To search, run:
  # $ nix search wget
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



  ### Home Manager Packages

  home-manager.useGlobalPkgs = true;
  home-manager.users.terrior = { pkgs, ...}: {
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
      brightnessctl
      xorg.xmodmap
      trash-cli
      xorg.xkbcomp


      # system utilities (makes the system run smoothly internally)
      ntfs3g
      exfat
      xclip
      cifs-utils
      samba
      dunst


      # desktop utilities (programs to make the system usable from the user's perspective)
      kitty
      alacritty
      rxvt-unicode-emoji
      mlterm
      st
      rofi
      pavucontrol
      pasystray
      easyeffects
      flameshot
      nitrogen
      picom-jonaburg
      networkmanagerapplet
      copyq
      lxappearance
      etcher
      cinnamon.nemo
      xfce.thunar
      pcmanfm
      libsForQt5.dolphin
      easytag
      baobab
      cbatticon


      # development utilities (packages that help compile or develop code other than c)
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
      arduino


      # desktop programs (user gui programs with few system dependencies)
      librewolf
      brave
      tor-browser-bundle-bin
      spotify
      vscode
      audacity
      element-desktop
      cinny-desktop
      libreoffice
      krita
      libsForQt5.falkon
      
    ];
  };







  # Some programs need SUID wrappers, can be configured further or are
  # started in user sessions.
  # programs.mtr.enable = true;
  # programs.gnupg.agent = {
  #   enable = true;
  #   enableSSHSupport = true;
  # };
}

