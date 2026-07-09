% regras.pl

elegivel("Bolsa de Mérito", Media, _) :- 
    Media >= 15.0.

elegivel("Bolsa Social", Media, Rendimento) :- 
    Media >= 10.0, 
    Rendimento =< 35000.

elegivel("Bolsa de Estudo Integral", Media, Rendimento) :- 
    Media >= 16.0, 
    Rendimento =< 45000.