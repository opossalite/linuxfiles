{ config, pkgs, ... }:

let
  unstable = import <nixos-unstable> { config = { allowUnfree = true;}; };
in {
  imports =
    [
      ./hardware-configuration.nix
      <home-manager/nixos>
    ];



  ### Fix for NixOS 23.05

  #nixpkgs.overlays = with pkgs; [
  #  (self: super: {
  #    fcitx-engines = fcitx5;
  #  })
  #];

  #nixpkgs.overlays = [(self: super: { discord = super.discord.overrideAttrs (_: { src = builtins.fetchTarball "/home/terrior/Downloads/discord-0.0.46.tar.gz"; });})];

  ### Keep shell packages
  nix.extraOptions = ''
    keep-outputs = true
    keep-derivations = true
  '';


  ### Try to fix audio cutting off problem
  boot.extraModprobeConfig = ''
      options snd_hda_intel power_save=0
  '';


  ### Bootloader

  boot.loader.grub.enable = true;
  boot.loader.grub.device = "/dev/sda";
  boot.loader.grub.useOSProber = true;

  boot.loader.grub.efiSupport = true;
  boot.loader.efi.canTouchEfiVariables = true;



  ### System Settings, including auto update and optimize

  system.stateVersion = "22.11";
  system.autoUpgrade = {
    enable = true;
  };
  nix.optimise.automatic = true;
  nix.settings.auto-optimise-store = true;
  networking.hostName = "VulpesKrovPC";
  users.users.terrior = {
    isNormalUser = true;
    description = "terrior";
    extraGroups = [ "networkmanager" "wheel" "storage" "docker" "dialout"];
    shell = pkgs.zsh;
    packages = with pkgs; [  #ensure some packages are installed for the user, even if home-manager isn't working correctly
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
  '';
  security.polkit.enable = true;



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
  services.blueman.enable = true;



  ### Mounting
  
  services.devmon.enable = true;
  services.gvfs.enable = true;
  services.udisks2.enable = true;
  boot.supportedFilesystems = [ "ntfs" ];



  ### Environment
  environment.sessionVariables = {
    #GDK_SCALE = "0.5";
    #GDK_DPI_SCALE = "0.5";
    #_JAVA_OPTIONS = "-Dsun.java2d.uiScale=0.5";
    QT_QPA_PLATFORMTHEME = "qt5ct";
  };
  programs.zsh = {
    enable = true;
    ohMyZsh.enable = true;
    autosuggestions.enable = true;
    histSize = 10000;
    #histFile = "${config.xdg.dataHome}/zsh/history";
  };



  ### Display Server

  services.xserver = {
    enable = true;
    layout = "us";
    xkbVariant = "";
    videoDrivers = [ "nvidia" ];
    displayManager.lightdm.enable = true;
    desktopManager.gnome.enable = true;
    #desktopManager.plasma5.enable = true;
    windowManager.qtile.enable = true;
    windowManager.awesome = {
      enable = true;
      luaModules = with pkgs.luaPackages; [
        luarocks  #package manager for Lua modules
	luadbi-mysql  #database abstraction layer
      ];
    };
    libinput = {
      mouse.accelProfile = "flat";
      touchpad.accelProfile = "flat";
    };
    #dpi = 96; #too big
    #dpi = 60; #way too small
    #dpi = 80; #maybe too small?
    dpi = 90;
  };
  hardware.opengl.enable = true;
  hardware.opengl.driSupport32Bit = true;
  #hardware.video.hidpi.enable = false;



  ### Audio

  #sound.enable = true;
  hardware.pulseaudio.enable = false;  #don't use pulseaudio
  security.rtkit.enable = true;
  services.pipewire = {
    enable = true;
    wireplumber.enable = true;
    alsa.enable = true;
    alsa.support32Bit = true;
    pulse.enable = true;
    jack.enable = true;
    #config.pipewire = {
    #  "properties" = {
    #    default.clock.allowed-rates = [ 44100 48000 88200 96000 ];
    #  };
    #};
    #extraConfig.pipewire = {
    #  "stream.properties" = {
    #    "default.clock.allowed-rates" = "[ 44100 48000 88200 96000 ]";
    #    #"channelmix.upmix" = true;
    #    #"default.clock.rate" = 192000;
    #    #"default.clock.quantum" = 128;
    #  };
    #};
    extraConfig.pipewire."92-low-latency" = {
      context.properties = {
        default.clock.allowed-rates = [ 44100 48000 88200 96000 ];
        default.clock.rate = 44100;
      };
    };
  };
  #environment.etc = {
  #  #"pipewire/pipewire.conf.d/clock-rate.conf".text = ''
  #  #/usr/share/pipewire/pipewire.conf
  #  #quantum is all 32 by default here
  #  #"pipewire/pipewire.conf.d/92-low-latency.conf".text = ''
  #  #  context.properties = {
  #  #    default.clock.rate = 48000
  #  #    default.clock.quantum = 32
  #  #    default.clock.min-quantum = 32
  #  #    default.clock.max-quantum = 32
  #  #  }
  #  #'';
  #  "pipewire/pipewire.conf.d/01-clock-rate.conf".text = ''
  #    context.properties = {
  #      default.clock.allowed-rates = [ 44100 48000 88200 96000 ]
  #      default.clock.rate = 44100
  #    }
  #  '';
  #};



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
    #cudaSupport = true;

    permittedInsecurePackages = [
      "electron-12.2.3"
      "openssl-1.1.1u"
    ];
  };



  ### System Packages

  environment.systemPackages = with pkgs; [
    home-manager

    git
    neovim
    pciutils
    python3Full
    qtile
    udevil
    wget
    xorg.libxcb.dev

    clang_multi
    clang-tools
    gcc_multi
    glibc
    gnumake
    libclang
  ];



  ### Fonts

  fonts.packages = with pkgs; [
    (nerdfonts.override { fonts = ["SourceCodePro"]; })

  ];

}

