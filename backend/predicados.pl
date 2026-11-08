:- consult('hechos.pl').

% Predicados

% ===================================================
% Auxiliares

/*
* Objetivo: Determina si un elemento pertenece a una lista (reemplazo propio de member/2, que viene de una librería)
* Entradas: Elemento y Lista
* Salidas: Verdadero si Elemento está en Lista; con Elemento sin instanciar devuelve cada elemento por backtracking
* Restricciones: Lista debe ser una lista; no se permiten librerías adicionales de Prolog
*/
miembro(Elemento, [Elemento|_]).
miembro(Elemento, [_|Resto]) :-
  miembro(Elemento, Resto).

% ===================================================
% Consultas básicas

/*
* Objetivo: Determina si una persona estuvo registrada en un lugar determinado durante una hora específica.
* Entradas: Persona, Lugar, Hora
* Salidas: Verdadero si la persona estuvo en el lugar a la hora indicada según los registros.
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
  current_predicate(accesoPorObjeto/2), % Puede que no exista un acceso condicionado por un objeto en el caso
  current_predicate(ubicado/2), % Puede que no se establezca donde se encuentra un objeto en el caso
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
  current_predicate(corresponde/2),  % el caso puede no relacionar evidencias con personas
  current_predicate(evidencia/3),    % el caso puede no traer evidencias
  !,
  findall(Evidencia, (corresponde(Evidencia, Persona), evidencia(Evidencia, _, _)), Evidencias).
evidencias_de(_, []).


% ===================================================
% Sospechosos

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
  current_predicate(accesoPorObjeto/2), % Puede que no exista un acceso condicionado por un objeto en el caso
  current_predicate(ubicado/2), % Puede que no se establezca donde se encuentra un objeto en el caso
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
  ;  forall(miembro(H-L, Movs), format("  - ~w a las ~w~n", [L, H]))
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
  ;  forall(miembro(L, Lugares),
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
  ;  forall(miembro(E, Evs),
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
    forall(miembro(LD-HD-LR-HR, Cs),
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
  E = 'ESCENA:\nEl registro de movimientos ubica a la persona en el lugar del evento durante el intervalo analizado (la hora del evento mas/menos el margen permitido).\nEsto significa que estuvo en la escena mientras ocurria el hecho, lo cual le da oportunidad directa de participar.'.

% Acceso al lugar del evento
explicacion_(Persona, E) :-
  evento(_, Lugar, _),
  motivo_acceso(Persona, Lugar, _),
  E = 'ACCESO:\nLa persona tenia autorizacion para ingresar al lugar del evento, ya sea porque tiene acceso directo a el o porque tiene acceso al lugar donde esta el objeto que abre esa puerta.\nEsto significa que contaba con los medios para entrar a la escena, aunque no haya quedado registrada alli.'.

% Evidencia hallada en la escena
explicacion_(Persona, E) :-
  evidencia_en_escena(Persona, Evidencia),
  evidencia(Evidencia, _, _),
  E = 'EVIDENCIA:\nUna evidencia hallada en el lugar del evento esta relacionada con la persona.\nEsto significa que existe una prueba material que la vincula directamente con la escena, lo cual cuenta como indicio en su contra.'.

% Contradiccion durante el evento (es un indicio)
explicacion_(Persona, E) :-
  contradiccion(Persona, _, HD, _, _),
  en_intervalo_evento(HD),
  E = 'CONTRADICCION EN EL EVENTO:\nEl testimonio de la persona dice que estaba en un lugar, pero el registro de movimientos la ubica en otro a la misma hora (dentro del margen permitido), y esa hora cae dentro del intervalo del evento.\nEsto significa que su version es incompatible con los registros justo en el momento clave, por lo que cuenta como indicio en su contra.'.

% Contradiccion fuera del evento (relevante, pero no es indicio)
explicacion_(Persona, E) :-
  contradiccion(Persona, _, HD, _, _),
  \+ en_intervalo_evento(HD),
  E = 'CONTRADICCION FUERA DEL EVENTO:\nEl testimonio de la persona no coincide con el registro de movimientos, pero la hora de la contradiccion queda fuera del intervalo del evento.\nEsto significa que es un dato relevante para la investigacion (su testimonio no es del todo confiable), pero no cuenta como indicio porque no la ubica en la escena durante el hecho.'.

% Coartada
explicacion_(Persona, E) :-
  coartada(Persona, _, _),
  E = 'COARTADA:\nLa persona declaro estar en un lugar distinto al del evento a la hora en que ocurrio, el registro de movimientos respalda ese testimonio y ningun registro la ubica en la escena durante el evento.\nEsto significa que existe una version coherente que la deja fuera del lugar del hecho.'.

% Conclusion: responsable
explicacion_(Persona, E) :-
  responsable_valido(Persona),
  E = 'CONCLUSION:\nPOSIBLE RESPONSABLE: La persona es sospechosa porque cumple tres condiciones:\n(1) tuvo oportunidad, pues estuvo en la escena durante el evento o tiene acceso a ella;\n(2) existe al menos un indicio, ya sea una evidencia hallada en la escena o una contradiccion durante el evento;\n(3) no puede descartarse, pues no cumple las condiciones de descarte (coartada respaldada por los registros, sin presencia ni evidencia en la escena).'.

% Conclusion: descartada
explicacion_(Persona, E) :-
  descartar(Persona),
  E = 'CONCLUSION:\nDESCARTADA: La persona se descarta porque cumple tres condiciones:\n(1) tiene coartada, su testimonio la ubica en otro lugar a la hora del evento y el registro de movimientos lo respalda;\n(2) ningun registro la ubica en la escena durante el intervalo del evento;\n(3) ninguna evidencia hallada en la escena le corresponde.\nPor lo tanto, la informacion disponible es incompatible con que haya participado.'.

% Conclusion: ni responsable ni descartada
explicacion_(Persona, E) :-
  \+ responsable_valido(Persona),
  \+ descartar(Persona),
  E = 'CONCLUSION:\nEN INVESTIGACION: La persona no es una responsable probable porque le falta oportunidad (no estuvo en la escena ni tiene acceso a ella) o un indicio (ninguna evidencia en la escena ni contradiccion durante el evento).\nAun asi no se descarta, pues no cumple todas las condiciones de descarte (coartada respaldada, sin presencia ni evidencia en la escena).\nLa informacion disponible no alcanza para cerrar su caso.'.


% ===================================================
% Resolver caso

/*
* Objetivo: Imprime el informe completo de una persona considerada responsable
* Entradas: Persona
* Salidas: Evidencias, ubicación relevante, accesos, coartada, contradicciones, justificación y validación
* Restricciones: Solo debe llamarse con personas que están en posibles_responsables/1
*/
informe_responsable(Persona) :-
  format("~n========================================~n"),
  format("POSIBLE RESPONSABLE: ~w~n", [Persona]),
  format("========================================~n~n"),
  % 1. Evidencias relacionadas
  mostrar_evidencias(Persona),
  % 2. Ubicación y movimientos relevantes (en la escena o dentro del intervalo del evento)
  format("~nUbicacion y movimientos relevantes:~n"),
  evento(_, LugarEvento, _),
  intervalo_evento(Ini, Fin),
  movimientos_de(Persona, Movs),
  forall(( miembro(H-L, Movs),
          once((L == LugarEvento ; (H >= Ini, H =< Fin))) ),
        format("  - ~w a las ~w~n", [L, H])),
  % 3. Accesos relevantes (al lugar del evento)
  format("~nAccesos relevantes:~n"),
  (  setof(M, motivo_acceso(Persona, LugarEvento, M), Ms)
  -> forall(miembro(M, Ms), format("  - ~w~n", [M]))
  ;  format("  (sin acceso al lugar del evento)~n")
  ),
  % 4. Coartadas y contradicciones
  nl,
  mostrar_coartada(Persona),
  mostrar_contradicciones(Persona),
  % 5. Justificación lógica
  format("~nJustificacion logica:~n~n"),
  forall(explicaciones(Persona, E), format("~w~n~n", [E])),
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
  format("~n========================================~n"),
  format("         RESOLUCION DEL CASO~n"),
  format("========================================~n~n"),
  format("  Evento:    ~w~n  Lugar:     ~w~n  Hora:      ~w~n  Intervalo: ~w - ~w~n",
        [Nombre, Lugar, Hora, Ini, Fin]),
  posibles_responsables(Responsables),
  length(Responsables, N),
  format("~n----------------------------------------~n"),
  format("  POSIBLES RESPONSABLES: ~w~n", [N]),
  format("----------------------------------------~n~n"),
  (  Responsables == []
  -> format("  No se encontraron responsables con la informacion disponible.~n")
  ;  forall(miembro(P, Responsables), format("  - ~w~n", [P])),
    forall(miembro(P, Responsables), informe_responsable(P))
  ),
  findall(D, (persona(D), descartar(D)), Descartados),
  format("~n----------------------------------------~n"),
  format("  PERSONAS DESCARTADAS~n"),
  format("----------------------------------------~n~n"),
  (  Descartados == []
  -> format("  No hay personas descartadas con la informacion disponible.~n")
  ;  forall(miembro(D, Descartados), format("  - ~w~n", [D]))
  ).

  
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