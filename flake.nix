{
  description = "Nix flake for khidl";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
    pyproject-nix = {
      url = "github:nix-community/pyproject.nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = { self, nixpkgs, pyproject-nix, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        project =
          pyproject-nix.lib.project.loadPyproject { projectRoot = ./.; };
        pkgs = import nixpkgs { inherit system; };
        python = pkgs.python3;
        attrs = project.renderers.buildPythonPackage { inherit python; };
      in {
        packages = { default = python.pkgs.buildPythonApplication attrs; };
      });
}
