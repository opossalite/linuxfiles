{ config, pkgs, ... }:

{
  imports =
    [
      ./hardware-configuration.nix
      <home-manager/nixos>
    ];


  ### Things I don't understand
  nixpkgs.overlays = with pkgs; [
    (self: super: {
      fcitx-engines = fcitx5;
    })
  ];


  ### Bootloader

  boot.loader.grub.enable = true;
  boot.loader.grub.device = "/dev/sda";
  boot.loader.grub.useOSProber = true;
  #boot.kernelPackages = pkgs.linuxPackages_4_19;



  ### System Settings

  system.stateVersion = "22.11";
  system.autoUpgrade = {
    enable = true;
  };
  networking.hostName = "MonoWolfPC";
  users.users.terrior = {  #define a user account, don't forget to set a password with 'passwd'
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
    #displayManager.gdm.enable = true;  #use GDM as the login manager
    displayManager.lightdm.enable = true;  #use LightDM as the login manager
    desktopManager.gnome.enable = true;  #enable GNOME desktop environment
    windowManager.qtile.enable = true;  #enable Qtile window manager
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

  #"context.properties": [
  #    "module.x11.bell": "false")
  #];



  ### Virtualization
  virtualisation = {
    docker = {
      enable = true;
    };
    podman = {
      enable = true;

      # Create a `docker` alias for podman, to use it as a drop-in replacement
      #dockerCompat = true;

      # Required for containers under podman-compose to be able to talk to each other.
      defaultNetwork.settings.dns_enabled = true;
      # For Nixos version > 22.11
      #defaultNetwork.settings = {
      #  dns_enabled = true;
      #};
    };
  };



  ### Flatpak
  services.flatpak.enable = true;




  ################
  ### Packages ###
  ################


  nixpkgs.config = {
    # Allow unfree packages
    allowUnfree = true;

    # Allow insecure packages
    permittedInsecurePackages = [
      "electron-12.2.3"
    ];
  };



  # List packages installed in system profile. To search, run:
  # $ nix search wget
  environment.systemPackages = with pkgs; [
    vim
    wget
    neovim
    git
    qtile
    python3
    xorg.libxcb.dev
    udevil
  ];


  # Fonts
  fonts.fonts = with pkgs; [
    (nerdfonts.override { fonts = ["SourceCodePro"]; })
  ];


  home-manager.useGlobalPkgs = true;
  home-manager.users.terrior = { pkgs, ... }: {
    home.stateVersion = "22.11";
    home.packages = with pkgs; [

      # command-line programs (programs that run in the terminal)
      lf
      neofetch
      htop
      btop
      nvtop
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


      # system utilities (makes the system run smoothly internally)
      ntfs3g
      exfat
      xclip
      cifs-utils
      samba


      # desktop utilities (programs to make the system usable from the user's perspective)
      kitty
      rofi
      pavucontrol
      pasystray
      easyeffects
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
      gcc_multi
      glibc
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


      # desktop programs (user gui programs with few system dependencies)
      librewolf
      brave
      tor-browser-bundle-bin
      discord
      spotify
      #vscodium-fhs
      vscode
      audacity
      amberol
      #libsForQt5.elisa
      strawberry
      audacious
      #lollypop
      

      # games
      minecraft
      #prismlauncher


      # fonts
      #source-code-pro
      #nerdfonts

    ];
  };
}

