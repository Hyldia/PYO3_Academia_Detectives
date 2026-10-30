:- consult('hechos.pl').

% Predicados

/*
* Objetivo: Determina si una persona estuvo registrada en un lugar determinado durante una hora específica.
* CONSULTAR *
*/
estuvo_en(Persona, Lugar, Hora) :-
  estuvo(Persona, Lugar, Hora).

/*
* Objetivo: Determina si una persona tiene autorización para ingresar a un lugar.
*/
% Acceso directo
tiene_acceso(Persona, Lugar) :-
  acceso(Persona, Lugar).
% Acceso indirecto por medio de un objeto que se posee
tiene_acceso(Persona, Lugar) :-
  accesoPorObjeto(Lugar, Objeto),
  ubicado(Objeto, LugarObjeto),
  acceso(Persona, LugarObjeto).

