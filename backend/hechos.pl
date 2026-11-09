/*
Caso 3: Robo de un Archivo
Historia
Desapareció un archivo de una biblioteca a las 16:00.

Personas
Gabriel
Helen
Ivan

Lo que ocurrió
Gabriel dijo que estaba en la biblioteca y efectivamente estaba allí.
Helen dijo que estaba en la oficina y efectivamente estaba allí.
Ivan dijo que estaba en la oficina.
Los registros muestran que Ivan estaba realmente en la biblioteca.
Una cámara de seguridad encontrada en la biblioteca está asociada a Ivan.

Resultados esperados
Evidencias
Ivan -> video

Contradicciones
Solo Ivan debe tener contradicción.

Ubicaciones
Ivan -> biblioteca
aunque declarara otra cosa.

Sospechosos
Ivan

Descartados
Helen

Posibles responsables
Ivan
*/

% Hechos
persona(gabriel).
persona(helen).
persona(ivan).

lugar(biblioteca).
lugar(oficina).
lugar(bodega).

acceso(gabriel, biblioteca).
acceso(helen, oficina).
acceso(ivan, biblioteca).

estuvo(gabriel, biblioteca, 1600).
estuvo(helen, oficina, 1600).
estuvo(ivan, biblioteca, 1600).

evento(robo_archivo, biblioteca, 1600).

evidencia(video_seguridad, biblioteca, 1601).
corresponde(video_seguridad, ivan).

testimonio(gabriel, biblioteca, 1600).
testimonio(helen, oficina, 1600).

testimonio(ivan, oficina, 1600).
