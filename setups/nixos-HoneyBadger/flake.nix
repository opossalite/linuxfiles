{
  description = "NixOS configuration";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-26.05";

    nix-flatpak.url = "github:gmodena/nix-flatpak/latest";
  };

  outputs = { nixpkgs, nix-flatpak, ... }: {
    nixosConfigurations.NixPC = nixpkgs.lib.nixosSystem {
      system = "x86_64-linux";

      modules = [
        ./configuration.nix

        nix-flatpak.nixosModules.nix-flatpak
      ];
    };
  };
}
