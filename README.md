# Registro precios Mercadona

Intento de crear un histórico de los precios de Mercadona.
La idea es que estos datos sirvan para calcular métricas reales de variación de precios en España, basándonos directamente en uno de los supermercados más populares.

No se si los datos de la API son fiables o se actualizan a menudo.
El archivo data.json se irá actualizando por medio de github actions, a priori semanalmente, viendo la historia de git se podrán ver las diferencias, si no se actualiza es porque no a habido cambios.

Mas adelante si los datos resultan de utilidad se actualizará con alguna herramienta de análisis. Suponemos que los datos que nos da el INE son correctos, dentro de la parte subjetiva que tiene el IPC claro, pero nunca está de más revisar los datos oficiales.

En el archivo [.excalidraw](https://excalidraw.com/) esta recogido mas o menos como se estructura la api. Este script intenta hacer un uso responsable de esta, ya que es una gran herramienta para estadísticos de andar por casa.
