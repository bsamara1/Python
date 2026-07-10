% regras.pl - Regras de elegibilidade para bolsas de estudo

% Bolsa de Merito: exige media >= 15.0
elegivel("Merito", Media, _) :-
    Media >= 15.0.

% Bolsa Social: exige media >= 10.0 E rendimento <= 35000
elegivel("Social", Media, Rendimento) :-
    Media >= 10.0,
    Rendimento =< 35000.

% Bolsa de Estudo Integral: exige media >= 16.0 E rendimento <= 45000
elegivel("Estudo Integral", Media, Rendimento) :-
    Media >= 16.0,
    Rendimento =< 45000.

% Aliases com nomes completos (para compatibilidade)
elegivel("Bolsa de Merito", Media, _) :- elegivel("Merito", Media, _).
elegivel("Bolsa Social", Media, Rendimento) :- elegivel("Social", Media, Rendimento).
elegivel("Bolsa de Estudo Integral", Media, Rendimento) :- elegivel("Estudo Integral", Media, Rendimento).