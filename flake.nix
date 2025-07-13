{
  description = "Nix flake for khidl";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
    pyproject-nix = {
      url = "github:nix-community/pyproject.nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = { self, nixpkgs, pyproject-nix }:
    let
      project = pyproject-nix.lib.project.loadPyproject { projectRoot = ./.; };
      pkgs = nixpkgs.legacyPackages.x86_64-linux;
      python = pkgs.python3;
    in {
      packages.x86_64-linux.default =
        let attrs = project.renderers.buildPythonPackage { inherit python; };
        in python.pkgs.buildPythonApplication attrs;
    };
}
