{ stdenv
, mkRosPackage
, robonomics_comm
}:

mkRosPackage rec {
  name = "${pname}-${version}";
  pname = "zenit_printer_agent";
  version = "0.1.0";

  src = ./.;

  propagatedBuildInputs = [
    robonomics_comm
  ];

  meta = with stdenv.lib; {
    description = "";
    homepage = http://github.com/vourhey/;
    license = licenses.bsd3;
    maintainers = with maintainers; [ vourhey ];
  };
}
