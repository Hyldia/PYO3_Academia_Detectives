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


% ===================================================
% Sospechosos

% Objetivo: Define cuántos minutos de diferencia se aceptan para considerar que dos horas son el mismo momento
margen_minutos(10).

/*
* Objetivo: Convierte una hora en formato HHMM a minutos desde las 00:00
* Entradas: Hora en formato HHMM
* Salidas: Minutos equivalentes 
* Restricciones: Hora debe ser un entero HHMM válido
*/
a_minutos(Hora, Minutos) :-
  Minutos is (Hora // 100) * 60 + Hora mod 100.

/*
* Objetivo: Convierte minutos desde las 00:00 a una hora en formato HHMM
* Entradas: Minutos
* Salidas: Hora en formato HHMM
* Restricciones: Minutos debe ser un entero mayor o igual a 0
*/
a_hhmm(Minutos, Hora) :-
  Hora is (Minutos // 60) * 100 + Minutos mod 60.

/*
* Objetivo: Determina si dos horas están dentro del margen permitido
* Entradas: Hora1 y Hora2 en formato HHMM
* Salidas: Verdadero si la diferencia real en minutos no supera margen_minutos
* Restricciones: Se convierte a minutos porque restar en HHMM da resultados incorrectos
*/
cerca(Hora1, Hora2) :-
  margen_minutos(Margen),
  a_minutos(Hora1, Minutos1),
  a_minutos(Hora2, Minutos2),
  abs(Minutos1 - Minutos2) =< Margen.

/*
* Objetivo: Calcula el intervalo de tiempo que se analiza alrededor del evento central
* Entradas: Ninguna
* Salidas: Inicio y Fin del intervalo en formato HHMM
* Restricciones: El caso debe tener un único evento
*/
intervalo_evento(Inicio, Fin) :-
  evento(_, _, HoraEvento),
  margen_minutos(Margen),
  a_minutos(HoraEvento, MinutosEvento),
  MinutosInicio is max(0, MinutosEvento - Margen),  % evita horas negativas si el evento es cerca de las 0000
  MinutosFin is MinutosEvento + Margen,
  a_hhmm(MinutosInicio, Inicio),
  a_hhmm(MinutosFin, Fin).

/*
* Objetivo: Determina si una hora cae dentro del intervalo del evento
* Entradas: Hora en formato HHMM
* Salidas: Verdadero si Inicio =< Hora =< Fin
* Restricciones: Comparar en HHMM es válido; solo restar requiere convertir a minutos
*/
en_intervalo_evento(Hora) :-
  intervalo_evento(Inicio, Fin),
  Hora >= Inicio,
  Hora =< Fin.

/*
* Objetivo: Encuentra cada contradicción entre un testimonio de una persona y su registro de movimientos
* Entradas: Persona
* Salidas: LugarDicho y HoraDicha (testimonio/3), LugarRegistro y HoraRegistro (estuvo/3)
* Restricciones: Hay contradicción si los lugares son distintos y las horas están dentro del margen
*/
contradiccion(Persona, LugarDicho, HoraDicha, LugarRegistro, HoraRegistro) :-
  current_predicate(testimonio/3),  % el caso puede no traer testimonios
  testimonio(Persona, LugarDicho, HoraDicha),
  estuvo(Persona, LugarRegistro, HoraRegistro),
  LugarDicho \= LugarRegistro,
  cerca(HoraDicha, HoraRegistro).

/*
* Objetivo: Determina si una persona tiene al menos una contradicción
* Entradas: Persona
* Salidas: Verdadero si existe al menos una contradicción
* Restricciones: Se infiere de testimonio/3 y estuvo/3; no hay un hecho que diga que alguien miente
*/
tiene_contradiccion(Persona) :-
  persona(Persona),
  once(contradiccion(Persona, _, _, _, _)).