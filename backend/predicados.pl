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

% ===================================================
% Investigar

/*
* Objetivo: Obtiene los movimientos de una persona ordenados por hora
* Entradas: Persona
* Salidas: Lista de pares Hora-Lugar
* Restricciones: Usa estuvo/3
*/
movimientos_de(Persona, Movimientos) :-
  findall(Hora-Lugar, estuvo(Persona, Lugar, Hora), SinOrden),
  sort(SinOrden, Movimientos).

/*
* Objetivo: Obtiene los lugares a los que una persona tiene acceso (directo o por objeto)
* Entradas: Persona
* Salidas: Lista de lugares sin repetidos
* Restricciones: Usa tiene_acceso/2
*/
accesos_de(Persona, Lugares) :-
  findall(Lugar, tiene_acceso(Persona, Lugar), SinOrden),
  sort(SinOrden, Lugares).

/*
* Objetivo: Explica por qué una persona tiene acceso a un lugar
* Entradas: Persona, Lugar
* Salidas: Motivo (texto) del acceso
* Restricciones: Puede dar un motivo directo y otro por objeto (backtracking)
*/
motivo_acceso(Persona, Lugar, Motivo) :-
  acceso(Persona, Lugar),
  format(atom(Motivo), 'acceso directo a ~w', [Lugar]).
motivo_acceso(Persona, Lugar, Motivo) :-
  accesoPorObjeto(Lugar, Objeto),
  ubicado(Objeto, LugarObjeto),
  acceso(Persona, LugarObjeto),
  format(atom(Motivo), 'acceso a ~w mediante ~w (que esta en ~w, donde tiene acceso)',
         [Lugar, Objeto, LugarObjeto]).

/*
* Objetivo: Imprime los lugares donde estuvo una persona
* Entradas: Persona
* Salidas: Texto en pantalla
* Restricciones: Usa movimientos_de/2
*/
mostrar_lugares(Persona) :-
  movimientos_de(Persona, Movs),
  format("Lugares donde estuvo:~n"),
  (  Movs == []
  -> format("  (sin registros)~n")
  ;  forall(member(H-L, Movs), format("  - ~w a las ~w~n", [L, H]))
  ).

/*
* Objetivo: Imprime los accesos de una persona y su motivo
* Entradas: Persona
* Salidas: Texto en pantalla
* Restricciones: Muestra un solo motivo por lugar (once/1)
*/
mostrar_accesos(Persona) :-
  accesos_de(Persona, Lugares),
  format("Acceso a lugares:~n"),
  (  Lugares == []
  -> format("  (ninguno)~n")
  ;  forall(member(L, Lugares),
            ( once(motivo_acceso(Persona, L, M)),
              format("  - ~w~n", [M]) ))
  ).

/*
* Objetivo: Imprime las evidencias relacionadas con una persona
* Entradas: Persona
* Salidas: Texto en pantalla
* Restricciones: Usa evidencias_de/2 y evidencia/3
*/
mostrar_evidencias(Persona) :-
  evidencias_de(Persona, Evs),
  format("Evidencias relacionadas:~n"),
  (  Evs == []
  -> format("  (ninguna)~n")
  ;  forall(member(E, Evs),
            ( evidencia(E, L, H),
              format("  - ~w (hallada en ~w a las ~w)~n", [E, L, H]) ))
  ).

/*
* Objetivo: Imprime si la persona tiene una posible coartada
* Entradas: Persona
* Salidas: Texto en pantalla
* Restricciones: Usa coartada/3
*/
mostrar_coartada(Persona) :-
  (  coartada(Persona, L, H)
  -> format("Posible coartada: SI, declara estar en ~w a las ~w y el registro lo respalda~n", [L, H])
  ;  format("Posible coartada: NO~n")
  ).

/*
* Objetivo: Imprime las contradicciones de una persona
* Entradas: Persona
* Salidas: Texto en pantalla
* Restricciones: Usa contradiccion/5
*/
mostrar_contradicciones(Persona) :-
  findall(LD-HD-LR-HR, contradiccion(Persona, LD, HD, LR, HR), Cs),
  (  Cs == []
  -> format("Contradicciones: NO~n")
  ;  format("Contradicciones: SI~n"),
     forall(member(LD-HD-LR-HR, Cs),
            format("  - Dijo estar en ~w a las ~w, pero el registro lo ubica en ~w a las ~w~n",
                   [LD, HD, LR, HR]))
  ).

/*
* Objetivo: Realiza una consulta de investigación sobre una persona
* Entradas: Persona
* Salidas: Imprime lugares, accesos, evidencias, coartada y contradicciones
* Restricciones: La persona debe estar definida con persona/1
*/
investigar(Persona) :-
  persona(Persona),
  format("~n=== Investigacion de ~w ===~n", [Persona]),
  mostrar_lugares(Persona),
  mostrar_accesos(Persona),
  mostrar_evidencias(Persona),
  mostrar_coartada(Persona),
  mostrar_contradicciones(Persona).

% ===================================================
% Posibles responsables

/*
* Objetivo: Determina si una persona es responsable válida: es posible sospechosa y no puede ser descartada
* Entradas: Persona
* Salidas: Verdadero si posible_sospechoso/1 se cumple y descartar/1 no
* Restricciones: Comprueba que la conclusión sea consistente, es decir, que no exista un descarte para la persona
*/
responsable_valido(Persona) :-
  posible_sospechoso(Persona),
  \+ descartar(Persona).

/*
* Objetivo: Construye la lista de personas que pueden ser responsables del caso
* Entradas: Ninguna
* Salidas: Lista de personas que cumplen responsable_valido/1
* Restricciones: Recorre las personas definidas con persona/1 y evalúa las reglas de investigación en cada una
*/
posibles_responsables(Lista) :-
  findall(Persona, (persona(Persona), responsable_valido(Persona)), Lista).

% ===================================================
% Explicaciones

/*
* Objetivo: Genera, por backtracking, explicaciones logicas sobre una persona
* Entradas: Persona
* Salidas: Explicacion construida a partir de los hechos y reglas
* Restricciones: Cada explicación se infiere, no se almacena; al pedir más soluciones (;) devuelve una por una
*/
explicaciones(Persona, Explicacion) :-
  persona(Persona),
  explicacion_(Persona, Explicacion).

% Estuvo en la escena durante el intervalo del evento
explicacion_(Persona, E) :-
  evento(_, Lugar, _),
  intervalo_evento(Ini, Fin),
  estuvo_en_intervalo(Persona, Lugar, Ini, Fin),
  estuvo(Persona, Lugar, Hora),
  Hora >= Ini, Hora =< Fin,
  format(atom(E), 'Estuvo en ~w a las ~w, dentro del intervalo del evento (~w-~w).',
         [Lugar, Hora, Ini, Fin]).

% Acceso al lugar del evento
explicacion_(Persona, E) :-
  evento(_, Lugar, _),
  motivo_acceso(Persona, Lugar, Motivo),
  format(atom(E), 'Tenia ~w, lugar del evento.', [Motivo]).

% Evidencia hallada en la escena
explicacion_(Persona, E) :-
  evidencia_en_escena(Persona, Evidencia),
  evidencia(Evidencia, Lugar, Hora),
  format(atom(E), 'La evidencia ~w, hallada en ~w a las ~w, le corresponde.',
         [Evidencia, Lugar, Hora]).

% Contradiccion durante el evento (es un indicio)
explicacion_(Persona, E) :-
  contradiccion(Persona, LD, HD, LR, HR),
  en_intervalo_evento(HD),
  format(atom(E), 'Se contradice durante el evento: dijo estar en ~w a las ~w, pero el registro dice ~w a las ~w.',
         [LD, HD, LR, HR]).

% Contradiccion fuera del evento (relevante, pero no es indicio)
explicacion_(Persona, E) :-
  contradiccion(Persona, LD, HD, LR, HR),
  \+ en_intervalo_evento(HD),
  format(atom(E), 'Tiene una contradiccion fuera del evento (dijo ~w a las ~w, registro ~w a las ~w); es relevante pero no lo ubica en la escena.',
         [LD, HD, LR, HR]).

% Coartada
explicacion_(Persona, E) :-
  coartada(Persona, Lugar, Hora),
  format(atom(E), 'Tiene coartada: declara estar en ~w a las ~w y el registro lo respalda.',
         [Lugar, Hora]).

% Conclusion: responsable
explicacion_(Persona, E) :-
  responsable_valido(Persona),
  E = 'CONCLUSION: es posible responsable (tiene oportunidad e indicio y no puede ser descartada).'.

% Conclusion: descartada
explicacion_(Persona, E) :-
  descartar(Persona),
  E = 'CONCLUSION: se descarta (tiene coartada, no estuvo en la escena y no tiene evidencia en ella).'.

% Conclusion: ni responsable ni descartada
explicacion_(Persona, E) :-
  \+ responsable_valido(Persona),
  \+ descartar(Persona),
  E = 'CONCLUSION: no es responsable probable, pero no hay informacion suficiente para descartarla.'.


% ===================================================
% Resolver caso

/*
* Objetivo: Imprime el informe completo de una persona considerada responsable
* Entradas: Persona
* Salidas: Evidencias, ubicación relevante, accesos, coartada, contradicciones, justificación y validación
* Restricciones: Solo debe llamarse con personas que están en posibles_responsables/1
*/
informe_responsable(Persona) :-
  format("~n--- Responsable: ~w ---~n", [Persona]),
  % 1. Evidencias relacionadas
  mostrar_evidencias(Persona),
  % 2. Ubicación y movimientos relevantes (en la escena o dentro del intervalo del evento)
  format("Ubicacion y movimientos relevantes:~n"),
  evento(_, LugarEvento, _),
  intervalo_evento(Ini, Fin),
  movimientos_de(Persona, Movs),
  forall(( member(H-L, Movs),
           once((L == LugarEvento ; (H >= Ini, H =< Fin))) ),
         format("  - ~w a las ~w~n", [L, H])),
  % 3. Accesos relevantes (al lugar del evento)
  format("Accesos relevantes:~n"),
  (  setof(M, motivo_acceso(Persona, LugarEvento, M), Ms)
  -> forall(member(M, Ms), format("  - ~w~n", [M]))
  ;  format("  (sin acceso al lugar del evento)~n")
  ),
  % 4. Coartadas y contradicciones
  mostrar_coartada(Persona),
  mostrar_contradicciones(Persona),
  % 5. Justificación lógica
  format("Justificacion logica:~n"),
  forall(explicaciones(Persona, E), format("  * ~w~n", [E])),
  % 6. Validación de la solución
  (  responsable_valido(Persona)
  -> format("Validacion: OK (oportunidad + indicio, sin descarte)~n")
  ;  format("Validacion: FALLIDA~n")
  ).

/*
* Objetivo: Ejecuta el proceso general de resolución del caso
* Entradas: Ninguna
* Salidas: Imprime el evento, los responsables con su informe y las personas descartadas
* Restricciones: El caso debe tener un único evento; la conclusión se infiere con las reglas, no se almacena
*/
resolver_caso :-
  evento(Nombre, Lugar, Hora),
  intervalo_evento(Ini, Fin),
  format("~n====== RESOLUCION DEL CASO ======~n"),
  format("Evento: ~w en ~w a las ~w (intervalo analizado: ~w-~w)~n",
         [Nombre, Lugar, Hora, Ini, Fin]),
  posibles_responsables(Responsables),
  (  Responsables == []
  -> format("~nNo se encontraron responsables con la informacion disponible.~n")
  ;  length(Responsables, N),
     format("Posibles responsables (~w): ~w~n", [N, Responsables]),
     forall(member(P, Responsables), informe_responsable(P))
  ),
  findall(D, (persona(D), descartar(D)), Descartados),
  format("~nPersonas descartadas: ~w~n", [Descartados]).

  
% ===================================================
% Expediente de investigacion

/*
* Objetivo: Obtiene los datos de una evidencia relacionada con una persona.
* Entradas: Persona.
* Salidas: Evidencia, Lugar y Hora donde se encontró.
* Restricciones: El caso puede no relacionar evidencias con personas.
*/
detalle_evidencia(Persona, Evidencia, Lugar, Hora) :-
  current_predicate(corresponde/2),
  corresponde(Evidencia, Persona),
  evidencia(Evidencia, Lugar, Hora).

/*
* Objetivo: Obtiene lo que una persona declaró en su testimonio.
* Entradas: Persona.
* Salidas: Lugar y Hora declarados.
* Restricciones: El caso puede no traer testimonios.
*/
declaracion(Persona, Lugar, Hora) :-
  current_predicate(testimonio/3),
  testimonio(Persona, Lugar, Hora).

/*
* Objetivo: Clasifica a una persona según las reglas de investigación.
* Entradas: Persona.
* Salidas: Resultado (responsable, descartada o en_investigacion).
* Restricciones: La clasificación se infiere; no existe como hecho.
*/
clasificacion(Persona, responsable) :-
  responsable_valido(Persona).
clasificacion(Persona, descartada) :-
  descartar(Persona).
clasificacion(Persona, en_investigacion) :-
  persona(Persona),
  \+ responsable_valido(Persona),
  \+ descartar(Persona).

/*
* Objetivo: Determina si la decisión del jugador coincide con la inferencia del sistema.
* Entradas: Persona y Decision
* Salidas: Verdadero si la decisión coincide con clasificacion/2.
* Restricciones: Decision debe ser responsable, descartada o en_investigacion
*/
decision_correcta(Persona, Decision) :-
  clasificacion(Persona, Decision).