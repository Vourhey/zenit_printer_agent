{ stdenv
, mkRosPackage
, robonomics_comm
, python3Packages
}:

mkRosPackage rec {
  name = "${pname}-${version}";
  pname = "zenit_printer_agent";
  version = "0.1.0";

  src = ./.;

  propagatedBuildInputs = [
    robonomics_comm
    python3Packages.requests
  ];

  meta = with stdenv.lib; {
    description = "";
    homepage = http://github.com/vourhey/zenit_printer_agent;
    license = licenses.bsd3;
    maintainers = with maintainers; [ vourhey ];
  };
}
