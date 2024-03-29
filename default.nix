with import <nixpkgs> {};
with pkgs.python36Packages;

stdenv.mkDerivation {
  name = "impurePythonEnv";



  buildInputs = [
    # these packages are required for virtualenv and pip to work:
    #
    python36Full
    python36Packages.virtualenv
    python36Packages.pycurl
    python36Packages.lxml
   # python36Packages.pandas
 #   libffi
  #  openssl
#    python36Packages.dev
    #thonny
#    mysql-workbench
#    mysql
#    gcc

    # the following packages are related to the dependencies of your python
    # project.
    # In this particular example the python modules listed in the
    # requirements.tx require the following packages to be installed locally
    # in order to compile any binary extensions they may require.
    #
    tkinter
    ];
  src = null;
  shellHook = ''
  # set SOURCE_DATE_EPOCH so that we can use python wheels
  SOURCE_DATE_EPOCH=$(date +%s)
  virtualenv --no-setuptools venv
  export PATH=$PWD/venv/bin:$PATH
  pip install -r requirements.txt
#  mysql-workbench statbot.mwb &
 # emacs fl_bot.py &
  '';
}
