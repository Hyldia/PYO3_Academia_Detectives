
% HEHCOS
/*
Contexto del caso: El Robo del Expediente Secreto
Historia:
En una exposición especial en la Academia de Detectives desapareció un expediente secreto 
tenía información confidencial sobre una investigaciones en curso.

El robo ocurrió a las 15:00 horas en la Sala de Evidencias.

Cinco personas estuvieron presentes en el edificio ese día. A través de evidencias,
testimonios y registros de acceso, se deberá determinar quién pudo haber cometido el robo.
*/

% Personas
persona(karina). 
persona(carlos). 
persona(nicole). 
persona(diego).
persona(andrey). 

% Lugares
lugar(laboratorio).
lugar(biblioteca).
lugar(oficina).
lugar(sala_evidencias).

% Objetos
objeto(tarjeta_maestra).
objeto(llave_laboratorio).
objeto(expediente_secreto).

% Ubicación de los objetos
ubicado(tarjeta_acceso, biblioteca).
ubicado(llave_maestra, laboratorio).
ubicado(expediente_secreto, sala_evidencias).

% Accesos a lugares (Persona, Lugar)
acceso(karina, laboratorio).
acceso(diego, laboratorio).
acceso(karina, biblioteca).
acceso(carlos, biblioteca).
acceso(nicole, oficina).
acceso(nicole, sala_evidencias).
acceso(andrey, sala_evidencias).

% Accesos por objetos (Lugar, objeto)
accesoPorObjeto(sala_evidencias, tarjeta_maestra).
accesoPorObjeto(laboratorio, llave_laboratorio).

% Registro de movimientos (Persona, Lugar, Hora)
estuvo(karina, entrada, 1800).
estuvo(karina, biblioteca, 1900).
estuvo(karina, laboratorio, 2000).

estuvo(carlos, entrada, 1815).
estuvo(carlos, biblioteca, 1915).
estuvo(carlos, sala_evidencias, 2000).

estuvo(nicole, entrada, 1830).
estuvo(nicole, laboratorio, 1930).
estuvo(nicole, sala_evidencias, 2000).

estuvo(diego, entrada, 1845).
estuvo(diego, laboratorio, 1945).
estuvo(diego, biblioteca, 2000).

estuvo(andrey, sala_evidencias, 1800).
estuvo(andrey, biblioteca, 1900).
estuvo(andrey, sala_evidecnias, 2000).

% Evento (Nombre, Lugar, Hora)
evento(robo_expediente, sala_evidencia, 2000).

% Evidencias (Evidencia, Lugar, Hora)
evidencia(huella_digital, sala_evidencias, 2005).
evidencia(registro_acceso, sala_evidencias, 2002).
evidencia(video_seguridad, biblioteca, 1955).
evidencia(llave_encontrada, laboratorio, 2010).
evidencia(documento_anonimo, biblioteca, 2015).

% Correponde evidencia (Evidencia, Persona)
corresponde(huella_digital, karina).
corresponde(registro_acceso, carlos).
corresponde(video_seguridad, nicole).
corresponde(llave_encontrada, diego).
corresponde(documento_anonimo, andrey).

% Testimonios (Persona, Lugar, Hora)
testimonio(karina, biblioteca, 2000).
testimonio(carlos, biblioteca, 2000).
testimonio(nicole, oficina, 2000).
testimonio(diego, laboratorio, 2000).
testimonio(andrey, sala_evidencias, 1900).

