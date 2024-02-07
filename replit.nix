{pkgs}: {
  deps = [
    pkgs.glibcLocales
    pkgs.freetype
  ];
  env = {
    PYTHON_LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath [
      pkgs.glibcLocales
      pkgs.freetype
    ];
  };
}
