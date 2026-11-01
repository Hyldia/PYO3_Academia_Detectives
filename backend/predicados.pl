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

/*
* Objetivo: Determina si una persona estuvo en un lugar en un intervalo de tiempo.
*/
estuvo_en_intervalo(Persona, Lugar, Inicio, Fin) :-
  estuvo(Persona, Lugar, Hora),
  Hora >= Inicio, % Verifica que la hora esté dentro del intervalo
  Hora =< Fin.

/*
* Objetivo: Determina cuáles evidencias del caso han sido relacionadas con una persona.
*/
evidencias_de(Persona, Evidencias) :-
  findall(Evidencia,(corresponde(Evidencia, Persona), evidencia(Evidencia, _, _)), Evidencias).