{
  description = "NixOS configuration";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-26.05";
    nixpkgs-unstable.url = "github:NixOS/nixpkgs/nixos-unstable";
    #nix-flatpak.url = "github:gmodena/nix-flatpak/latest";
    #nix-flatpak.url = "github:gmodena/nix-flatpak/0.6.0";
    nix-flatpak.url = "github:gmodena/nix-flatpak/?ref=v0.6.0";
  };

  outputs = { nixpkgs, nixpkgs-unstable, nix-flatpak, ... }: 
  let
    system = "x86_64-linux";
    pkgs-unstable = import nixpkgs-unstable { inherit system; };
  in
  {
    nixosConfigurations.NixPC = nixpkgs.lib.nixosSystem {
      inherit system;
      specialArgs = { inherit pkgs-unstable; };
      modules = [
        ./configuration.nix
        nix-flatpak.nixosModules.nix-flatpak
      ];
    };
  };
}
