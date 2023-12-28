{ config, pkgs, ... }:

let
  unstable = import <nixos-unstable> { config = { allowUnfree = true;}; };
in {
  imports =
    [ # Include the results of the hardware scan.
      ./hardware-configuration.nix
      <home-manager/nixos>
    ];



  ### Fix for NixOS 23.05

  nixpkgs.overlays = with pkgs; [
    (self: super: {
      fcitx-engines = fcitx5;
    })
  ];



  ### Keep shell packages
  nix.extraOptions = ''
    keep-outputs = true
    keep-derivations = true
  '';


  ### Auto Optimize
  nix.settings.auto-optimise-store = true;


  ### Bootloader

  boot.loader.systemd-boot.enable = true;
  boot.loader.efi.canTouchEfiVariables = true;
  boot.loader.efi.efiSysMountPoint = "/boot/efi";
  boot.loader.systemd-boot.configurationLimit = 1;
  


  ### System Settings

  system.stateVersion = "22.11";
  system.autoUpgrade = {
    enable = true;
  };
  networking.hostName = "CobaltCanidPC";
  users.users.terrior = {
    isNormalUser = true;
    description = "terrior";
    extraGroups = [ "networkmanager" "wheel" "storage" "docker" "input"];
    shell = pkgs.zsh;
    packages = with pkgs; [ #ensure some packages are installed for the user, even if home-manager isn't working correctly
      firefox
    ];
  };
  programs.zsh = {
    enable = true;
    autosuggestions.enable = true;
    enableCompletion = true;
    histSize = 10000;
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
  # services.openssh.enable = true;
  hardware.bluetooth.enable = true;
  services.blueman.enable = true;
  #hardware.enableAllFirmware = true;



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
    desktopManager.gnome.enable = true;
    windowManager.qtile.enable = true;
    windowManager.awesome = {
      enable = true;
      luaModules = with pkgs.luaPackages; [
        luarocks #package manager for Lua modules
	luadbi-mysql #database abstraction layer
      ];
    };
    libinput = {
      enable = true; #enable touchpad support
      mouse.accelProfile = "flat";
      touchpad.accelProfile = "flat";
    };
  };
  hardware.opengl.enable = true;
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



  ### Enabling Extras

  services.flatpak.enable = true;
  nixpkgs.config = {
    allowUnfree = true;

    permittedInsecurePackages = [
      "electron-12.2.3"
      "openssl-1.1.1v"
    ];
  };



  ### System Packages
  environment.systemPackages = with pkgs; [
    home-manager 

    git
    neovim
    python310Full
    qtile
    udevil
    wget
    xorg.libxcb.dev

    clang-tools
    clang_multi
    libclang
    gcc_multi
    glibc_multi
    gnumake
    libstdcxx5
  ];


  #environment.sessionVariables = rec {
  #  XDG_DATA_DIRS="$HOME/desktop:$XDG_DATA_DIRS";
  #};


  ### Fonts

  fonts.packages = with pkgs; [
    (nerdfonts.override { fonts = ["SourceCodePro"]; })
  ];


  # Some programs need SUID wrappers, can be configured further or are
  # started in user sessions.
  # programs.mtr.enable = true;
  # programs.gnupg.agent = {
  #   enable = true;
  #   enableSSHSupport = true;
  # };
}

