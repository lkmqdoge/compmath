{
  description = "I hate nixos";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
  };

  outputs = { self, nixpkgs }:
    let
      inherit (nixpkgs) lib;
      forAllSystems = lib.genAttrs lib.systems.flakeExposed;
    in
    {
      devShells = forAllSystems (
        system:
        let
          pkgs = nixpkgs.legacyPackages.${system};
          python = (pkgs.python313.withPackages(ps: [
            ps.pyqtgraph
            ps.numpy
            ps.matplotlib
            ps.pyqt6
            ps.scipy
          ]));
        in
        {
          default = pkgs.mkShell {
            packages = [
              python 
            ];

            env.LD_LIBRARY_PATH = lib.makeLibraryPath (with pkgs;[
              dbus # libdbus-1.so.3
              fontconfig # libfontconfig.so.1
              freetype # libfreetype.so.6
              glib # libglib-2.0.so.0
              libGL # libGL.so.1
              libxkbcommon # libxkbcommon.so.0
              wayland             

              xorg.libX11 # libX11.so.6
              xorg.libxcb
              xorg.xcbutilwm
              xorg.xcbutilimage
              xorg.xcbutilkeysyms
              xorg.xcbutilrenderutil
              xcb-util-cursor
            ]);
          };
        });
    };
}
