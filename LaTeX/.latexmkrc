add_cus_dep('glo', 'gls', 0, 'makeglo2gls');
sub makeglo2gls {
    system("makeindex -s Thesis_AHoecherl.ist -t Thesis_AHoecherl.glg -o Thesis_AHoecherl.gls Thesis_AHoecherl.glo");
}