:- consult('hechos.pl').

% Predicados

/*
* Objetivo: Determina si una persona estuvo registrada en un lugar determinado durante una hora específica.
* Entradas: Persona, Lugar, Hora
* Salidas: Verdadero si la persona estuvo en el lugar a la hora indicada según los registros.
* CONSULTAR *
*/
estuvo_en(Persona, Lugar, Hora) :-
  estuvo(Persona, Lugar, Hora).

/*
* Objetivo: Determina si una persona tiene autorización para ingresar a un lugar.
* Entradas: Persona, Lugar
* Salidas: Verdadero si la persona tiene acceso directo o indirecto al lugar.
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
* Entradas: Persona, Lugar, Inicio, Fin
* Salidas: Verdadero si la persona estuvo en el lugar entre las horas Inicio y Fin
*/
estuvo_en_intervalo(Persona, Lugar, Inicio, Fin) :-
  estuvo(Persona, Lugar, Hora),
  Hora >= Inicio, % Verifica que la hora esté dentro del intervalo
  Hora =< Fin.

/*
* Objetivo: Determina cuáles evidencias del caso han sido relacionadas con una persona.
* Entradas: Persona
* Salidas: Lista de evidencias relacionadas con la persona
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


/*
* Objetivo: Determina si una persona estuvo en el lugar del evento durante el intervalo del evento
* Entradas: Persona
* Salidas: Verdadero si estuvo_en_intervalo/4 la ubica en la escena
* Restricciones: Usa el intervalo calculado por intervalo_evento/2
*/
estuvo_en_escena(Persona) :-
  evento(_, LugarEvento, _),
  intervalo_evento(Inicio, Fin),
  estuvo_en_intervalo(Persona, LugarEvento, Inicio, Fin).

/*
* Objetivo: Encuentra la coartada de una persona, un testimonio que la ubica fuera de la escena a la hora del evento y que su registro de movimientos respalda
* Entradas: Persona
* Salidas: Lugar y Hora declarados en el testimonio
* Restricciones: No es válida si algún registro ubica a la persona en la escena durante el evento
*/
coartada(Persona, Lugar, Hora) :-
  current_predicate(testimonio/3), % el caso puede no traer testimonios
  evento(_, LugarEvento, _),
  testimonio(Persona, Lugar, Hora),
  Lugar \= LugarEvento, % declara estar en otro lugar
  en_intervalo_evento(Hora), % a la hora del evento
  estuvo(Persona, Lugar, HoraRegistro), % el registro de movimientos lo respalda
  cerca(Hora, HoraRegistro),
  \+ estuvo_en_escena(Persona). % y ningún registro la ubica en la escena

/*
* Objetivo: Determina si una persona tiene una coartada válida
* Entradas: Persona
* Salidas: Verdadero si coartada/3 encuentra al menos una
* Restricciones: La coartada se infiere; no existe como hecho
*/
tiene_coartada(Persona) :-
  persona(Persona),
  once(coartada(Persona, _, _)).


/*
* Objetivo: Determina si una persona tiene acceso al lugar donde ocurrió el evento
* Entradas: Persona
* Salidas: Verdadero si tiene_acceso/2 lo permite
* Restricciones: Incluye acceso directo y acceso por objeto
*/
acceso_a_escena(Persona) :-
  evento(_, LugarEvento, _),
  tiene_acceso(Persona, LugarEvento).

/*
* Objetivo: Determina si una persona tuvo oportunidad de participar en el evento
* Entradas: Persona
* Salidas: Verdadero si estuvo en la escena o tiene acceso a ella
* Restricciones: Basta con una de las dos condiciones
*/
oportunidad(Persona) :-
  estuvo_en_escena(Persona).
oportunidad(Persona) :-
  acceso_a_escena(Persona).

/*
* Objetivo: Encuentra las evidencias relacionadas con una persona que se hallaron en el lugar del evento
* Entradas: Persona
* Salidas: Evidencia.
* Restricciones: Usa evidencia/3 y corresponde/2.
*/
evidencia_en_escena(Persona, Evidencia) :-
  current_predicate(corresponde/2),      % el caso puede no relacionar evidencias con personas
  evento(_, LugarEvento, _),
  evidencia(Evidencia, LugarEvento, _),
  corresponde(Evidencia, Persona).

/*
* Objetivo: Determina si una persona se contradice sobre dónde estaba a la hora del evento
* Entradas: Persona
* Salidas: Verdadero si alguna contradicción cae dentro del intervalo del evento
* Restricciones: Una contradicción en otra hora no cuenta como indicio
*/
contradiccion_en_evento(Persona) :-
  contradiccion(Persona, _, HoraDicha, _, _),
  en_intervalo_evento(HoraDicha).

/*
* Objetivo: Determina si existe algún indicio que vincule a la persona con el evento.
* Entradas: Persona
* Salidas: Verdadero si tiene evidencia en la escena o contradicción durante el evento.
* Restricciones: Basta con uno de los dos
*/
indicio(Persona) :-
  evidencia_en_escena(Persona, _).
indicio(Persona) :-
  contradiccion_en_evento(Persona).

/*
* Objetivo: Determina si una persona puede considerarse posible sospechosa
* Entradas: Persona (sin instanciar devuelve cada persona una sola vez).
* Salidas: Verdadero si cumple oportunidad e indicio
* Restricciones: Requiere oportunidad (escena o acceso) y al menos un indicio (evidencia en la escena o contradicción durante el evento)
*/
posible_sospechoso(Persona) :-
  persona(Persona),
  once(oportunidad(Persona)),
  once(indicio(Persona)).

/*
* Objetivo: Determina si una persona puede ser descartada como posible responsable, una peronsa se descarta si tiene coartada y no estuvo en la escena y no tiene evidencia en la escena.
* Entradas: Persona (sin instanciar devuelve cada persona una sola vez).
* Salidas: Verdadero si no estuvo en la escena y no tiene evidencia en la escena
*/
descartar(Persona):-
  persona(Persona),
  tiene_coartada(Persona),
  \+ estuvo_en_escena(Persona), % +/ = no estuvo en la escena
  \+ evidencia_en_escena(Persona, _). % +/ = no tiene evidencia en la escena. _ = no importa cuál evidencia, basta con que no tenga ninguna