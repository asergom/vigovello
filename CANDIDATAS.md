# Fotos candidatas para revisar

Fotos encontradas que **todavía no están en el mapa**. Ábrelas una a una y decide si se incluyen.

Antes de pasar una foto al mapa, comprueba en su ficha de Commons:
1. **Licencia:** dominio público o Creative Commons que permita publicarla (CC0, CC BY, CC BY-SA). No valen las licencias «NC» (no comercial) ni «ND» (sin obras derivadas) ni «todos los derechos reservados».
2. **Autor y fecha:** que coincidan con lo que dice la ficha.
3. **Lugar:** que se pueda situar en el mapa con cierta seguridad.

Para incluir una, usa `editor.html` → **+ Añadir foto por URL**, o pídeselo a Claude.

## Ya incorporadas al mapa

Las fotos de Wikimedia Commons de los apartados anteriores se han añadido al mapa. Commons solo admite archivos de dominio público o con licencia libre, y cada foto enlaza a su ficha, donde figuran autor y licencia. Las que no tienen un lugar conocido llevan la etiqueta «Ubicación sin confirmar», y los visitantes pueden proponer dónde se tomaron.

**Cine Royalty (Archivo Pacheco):** licencia CC BY-SA 4.0 confirmada en su ficha.

Las nuevas fotos de Wikimedia Commons se incorporan con el importador, que se ejecuta a mano (ver README). Este listado queda para lo que no se puede importar así.

## Lista de tareas pendientes

Todo lo que queda por hacer fuera del importador, para resolverlo al terminar la búsqueda de fuentes.

### 1. Subir a Wikimedia Commons (licencia libre confirmada)

Para que la web pueda mostrarlas hace falta una dirección de imagen permanente. Al subirlas, pon como fuente el enlace permanente y la licencia indicada; después, pasa a Claude los enlaces de Commons para añadirlas al mapa.

| Foto | Fecha | Lugar | Licencia según la fuente | Enlace permanente |
|---|---|---|---|---|
| Mundial 1982: Italia–Polonia (0-0). Cabrini (n.º 4), Boniek y el portero Zoff. Spaarnestad Photo, fotógrafo desconocido. Nationaal Archief, inventario 7.000SPABB / 36572 | 14/06/1982 | Estadio de Balaídos | «Rechtenvrij» (libre de derechos) | http://hdl.handle.net/10648/35429da6-2819-a382-e063-6df0900a6686 |

### 2. Comprobar la licencia y, si es libre, subir a Commons

| Qué | Dónde | Qué hacer |
|---|---|---|
| ETH Zúrich, Dia 298-05341 | Buscar el número en [E-Pics](https://e-pics3.ethz.ch/en/home_en/) | Mirar título, fecha y licencia. Las diapositivas de la ETH suelen ser CC BY-SA 4.0. |
| ETH Zúrich, Fel 045353 y Fel 045354 | Ídem | Miniaturas con marca de agua: probablemente con derechos. Confirmar; si no son libres, descartar o pedir permiso a la ETH. |
| Fotos estereoscópicas de Vigo hacia 1900, de Aurelio Paz dos Reis (Príncipe, Porta do Sol, Praza da Constitución, Campo de Granada, el Castro, A Laxe) | [Centro Português de Fotografia](https://cpf.pt/), referencias «PT-CPF-APR». Descritas en [este artículo de VigoÉ](https://www.vigoe.es/vigo/mas-vigo/las-increibles-fotos-estereoscopicas-del-vigo-de-1900/) | El autor murió en 1931, así que deberían ser de dominio público. Revisar las condiciones de uso del CPF. |
| Fotos de Vigo del Nationaal Archief no publicadas en Commons | [Buscador de fotos libres](https://nationaalarchief.nl/onderzoeken/zoeken?activeTab=photos&qf_nao_download=Direct%20beschikbaar&rm=gallery), buscar «Vigo» | Valen las que tengan botón de descarga y digan «CC0», «Public Domain» o «Rechtenvrij». |
| Revistas ilustradas antiguas no publicadas en Commons | [Hemeroteca Digital](https://hemerotecadigital.bne.es/) y [Biblioteca Digital Hispánica](https://bdh.bne.es/) de la BNE | Buscar «Vigo» en *La Ilustración Española y Americana*, *Blanco y Negro*, *Nuevo Mundo*… Valen las obras en dominio público. |

### 3. Pedir permiso (fuentes con derechos)

| Fuente | Contacto | Notas |
|---|---|---|
| Archivo Pacheco y [Postais históricas municipais](https://postaishistoricasmunicipais.vigo.org/es/) | Concello de Vigo | El gran archivo visual de la ciudad. Claude puede redactar el correo de solicitud. Algunas fotos del Archivo Pacheco ya están en Commons con CC BY-SA 4.0. |
| [Postales de la Deputación de Pontevedra](https://arquivos.depo.gal/es/fondos-graficos) (unas 6.600) | Servizo de Patrimonio Documental e Bibliográfico | La web solo indica «Copyright © Deputación de Pontevedra». |
| Fondo de la Asociación de la Prensa de Vigo (509 fotos, más de 300 de Ángel Llanos) | Deputación de Pontevedra ([Atopo](https://atopo.depo.gal/)) | Fotos de la segunda mitad del siglo XX con autores conocidos. |

### 4. Situar fotos que ya están en el mapa

| Foto | Qué falta |
|---|---|
| Emilia Pardo Bazán en el Pazo da Pastora (3 fotos, 1909) | Ubicación del Pazo da Pastora. |
| Teatro Rosalía (1908) y teatro Tamberlik (1936) | Ubicación exacta de los teatros. |
| Casa de Caridad y Escuela Obrera (h. 1900) | Ubicación de los edificios. |
| Resto de fotos con la etiqueta «Ubicación sin confirmar» | Se pueden ir corrigiendo con `editor.html` o con las propuestas de los visitantes. |

### 5. Revisar: otras imágenes encontradas en Europeana

Licencia libre según Europeana. Hay que comprobar fecha, lugar y si encajan en el mapa.

| Imagen | Institución | Licencia | Ficha en Europeana |
|---|---|---|---|
| Vista de la parte oriental de la ciudad y puerto de Vigo [Material gráfico no proyectable] | Digital Library Real Academia de la Historia | PDM | https://www.europeana.eu/item/344/https___hispana_mcu_es_lod_oai_bibliotecadigital_rah_es_62777_ent0 |
| Fotografía de Carmen Martín Gaite en la playa de Canido (Vigo) | Digital Library of Castilla y León | CC0 | https://www.europeana.eu/item/545/https___hispana_mcu_es_lod_oai_bibliotecadigital_jcyl_es_28923_ent0 |
| Camilo José Cela en Vigo, 1982 | Virtual Library of Bibliographical Heritage | CC BY 4.0 | https://www.europeana.eu/item/109/https___hispana_mcu_es_lod_oai_bvpb_mcu_es_572011_ent0 |
| Camilo José Cela en Vigo, 1957 | Virtual Library of Bibliographical Heritage | CC BY 4.0 | https://www.europeana.eu/item/109/https___hispana_mcu_es_lod_oai_bvpb_mcu_es_573989_ent0 |
| Camilo José Cela en Vigo : recepción en el Ayuntamiento | Virtual Library of Bibliographical Heritage | CC BY 4.0 | https://www.europeana.eu/item/109/https___hispana_mcu_es_lod_oai_bvpb_mcu_es_574354_ent0 |
| Camilo José Cela en Vigo : ágape en el Centro de Hijos de Vigo | Virtual Library of Bibliographical Heritage | CC BY 4.0 | https://www.europeana.eu/item/109/https___hispana_mcu_es_lod_oai_bvpb_mcu_es_574356_ent0 |
| Camilo José Cela en Vigo : con Celso Emilio Ferreiro | Virtual Library of Bibliographical Heritage | CC BY 4.0 | https://www.europeana.eu/item/109/https___hispana_mcu_es_lod_oai_bvpb_mcu_es_574357_ent0 |
| Camilo José Cela en Vigo : ágape en el Centro de Hijos de Vigo | Virtual Library of Bibliographical Heritage | CC BY 4.0 | https://www.europeana.eu/item/109/https___hispana_mcu_es_lod_oai_bvpb_mcu_es_574358_ent0 |
| Camilo José Cela en Vigo : primera conferencia en el Círculo Recreativo Mercantil e Indust | Virtual Library of Bibliographical Heritage | CC BY 4.0 | https://www.europeana.eu/item/109/https___hispana_mcu_es_lod_oai_bvpb_mcu_es_574359_ent0 |
| Camilo José Cela en Vigo : cena homenaje en el Monte del Castro | Virtual Library of Bibliographical Heritage | CC BY 4.0 | https://www.europeana.eu/item/109/https___hispana_mcu_es_lod_oai_bvpb_mcu_es_574362_ent0 |
| Camilo José Cela en Vigo : segunda conferencia en el Círculo Recreativo Mercantil e Indust | Virtual Library of Bibliographical Heritage | CC BY 4.0 | https://www.europeana.eu/item/109/https___hispana_mcu_es_lod_oai_bvpb_mcu_es_574367_ent0 |
| Camilo José Cela en Vigo, 1957 | Virtual Library of Bibliographical Heritage | CC BY 4.0 | https://www.europeana.eu/item/109/https___hispana_mcu_es_lod_oai_bvpb_mcu_es_574376_ent0 |
| Camilo José Cela en Vigo : cena-homenaje en el Monte del Castro, tocando la gaita | Virtual Library of Bibliographical Heritage | CC BY 4.0 | https://www.europeana.eu/item/109/https___hispana_mcu_es_lod_oai_bvpb_mcu_es_574378_ent0 |
| Bilden föreställer en stadsvy från Vigo, Spanien, från havet | Naval Museum | PDM | https://www.europeana.eu/item/916108/smm_mm_photo_D13816_3A47 |
| Fotografía de Carmen Martín Gaite en la playa de Canido (Vigo) | Digital Library of Castilla y León | CC0 | https://www.europeana.eu/item/545/https___hispana_mcu_es_lod_oai_bibliotecadigital_jcyl_es_28908_ent0 |
| Fotografía de Carmen Martín Gaite en la playa de Canido (Vigo) | Digital Library of Castilla y León | CC0 | https://www.europeana.eu/item/545/https___hispana_mcu_es_lod_oai_bibliotecadigital_jcyl_es_28913_ent0 |
| S[an]t[ísi]mo Cristo de la Victoria de Vigo [Material gráfico no proyectable | Digital Library Real Academia de la Historia | PDM | https://www.europeana.eu/item/344/https___hispana_mcu_es_lod_oai_bibliotecadigital_rah_es_62424_ent0 |
| Fotografía de Carmen Martín Gaite en la playa de Canido (Vigo) | Digital Library of Castilla y León | CC0 | https://www.europeana.eu/item/545/https___hispana_mcu_es_lod_oai_bibliotecadigital_jcyl_es_28911_ent0 |
| Fotografía de Carmen Martín Gaite en la playa de Canido (Vigo) | Digital Library of Castilla y León | CC0 | https://www.europeana.eu/item/545/https___hispana_mcu_es_lod_oai_bibliotecadigital_jcyl_es_28912_ent0 |

## C · Otras fotos sueltas encontradas en Commons (sin revisar)

| Foto | Notas para revisar |
|---|---|
| [Concello de Vigo - Puerto](https://commons.wikimedia.org/wiki/File:Concello_de_Vigo_-_Puerto.jpg) | Comprobar si es antigua, su fecha y su licencia. |
| [Plaza Puerta del Sol. Vigo](https://commons.wikimedia.org/wiki/File:Plaza_Puerta_del_Sol._Vigo.jpg) | Comprobar si es antigua o actual. |

## D · Colecciones donde buscar más

Ordenadas de más a menos fácil de usar sin problemas de derechos.

### Probablemente utilizables (licencia abierta o dominio público por antigüedad)

| Colección | Qué hay | Derechos | Cómo seguir |
|---|---|---|---|
| [ETH-Bibliothek Zürich, E-Pics Bildarchiv](https://e-pics3.ethz.ch/en/home_en/) | De aquí salen las fotos de 1896, 1898 y 1934 que ya están en el mapa. Su serie de diapositivas «Dia 247» tiene más fotos de Vigo. | CC BY-SA 4.0 en las fichas comprobadas. | Buscar «Vigo» en E-Pics y comprobar la licencia de cada ficha. |
| [Postales de Eugenio Krapf en Commons](https://commons.wikimedia.org/wiki/Category:Postcards_published_by_Eugenio_Krapf) | Postales del editor y fotógrafo vigués Eugenio Krapf, hacia 1900. | Muy probablemente dominio público: tienen más de 100 años y el autor murió hace más de 80. | Revisar la ficha de cada postal. |
| Colección Seoane Prado (en Commons) | De aquí sale la vista desde el Castro (fotógrafo Thoman, 1920–1940). | La foto comprobada está marcada como dominio público (Public Domain Mark). | Buscar en Commons «Colección Seoane Prado» o «Thoman» para ver si hay más fotos de Vigo. |
| [Biblioteca Digital Hispánica (BNE)](https://bdh.bne.es/) | Postales y fotografías antiguas. | La BNE [permite el uso comercial gratuito](https://www.bne.es/es/noticias/0430-bne-permitira-uso-comercial-gratuito-imagenes-digitalizadas-obras-dominio-publico) de sus imágenes digitalizadas de obras en dominio público. | Buscar «Vigo» y quedarse con las que la ficha marque como dominio público. |
| Álbum «Recuerdo de Vigo», Hauser y Menet (Biblioteca de Galicia) | 20 postales de principios del siglo XX: Príncipe, Urzáiz, Berbés, Bouzas, Castro, Paseo de Alfonso, una conservera… Lo describe [este artículo de VigoÉ](https://www.vigoe.es/vigo/mas-vigo/un-album-de-vistas-de-vigo-de-hace-un-siglo/). | Por su antigüedad, probablemente dominio público. Hay que confirmarlo en la ficha de Galiciana. | Buscarlo en [Galiciana](https://biblioteca.galiciana.gal/) y comprobar sus condiciones de uso. |

### Con derechos o sin licencia clara: pedir permiso antes de usar

| Colección | Qué hay | Problema |
|---|---|---|
| [Fondo da Asociación da Prensa de Vigo](https://atopo.depo.gal/) (Deputación de Pontevedra, buscador Atopo) | 509 fotos, diapositivas y postales de la segunda mitad del siglo XX, más de 300 de Ángel Llanos. | Algunos medios dicen que son «de dominio público», pero se refieren a que se pueden consultar gratis. Son fotos recientes con autor conocido, así que casi seguro tienen derechos. Habría que pedir permiso a la Deputación. |
| [Fondos gráficos de la Deputación de Pontevedra](https://arquivos.depo.gal/es/fondos-graficos) | Unas 6.600 postales digitalizadas. | La web solo indica «Copyright © Deputación de Pontevedra», sin licencia abierta. Las postales muy antiguas pueden ser de dominio público, pero hay que confirmarlo. |
| [Postais históricas municipais (Concello de Vigo)](https://postaishistoricasmunicipais.vigo.org/es/) | Colección municipal de postales históricas. | No he podido leer sus condiciones de uso. Revisar su aviso legal o preguntar al Concello. |
| Archivo Pacheco (Concello de Vigo) | El gran archivo fotográfico de Vigo. | Derechos del Concello. Solo con permiso o con una licencia libre explícita. |
| [Oldpik](https://oldpik.com/es/lugar/europa-espana-galicia-pontevedra-vigo) | 34 fotos antiguas de Vigo (1870–1972). | Es un agregador sin licencia ni fuente original. No usar salvo que se localice el original con licencia libre. |

## Descartadas

| Foto | Motivo |
|---|---|
| [Centro e porto de Vigo](https://commons.wikimedia.org/wiki/File:Centro_e_porto_de_Vigo_cropped.jpg) | Foto actual (2007), no histórica. |
| [Juan Martínez Abades recogiendo algas en el Berbés](https://commons.wikimedia.org/wiki/File:Juan_Mart%C3%ADnez_Abades_Gathering_Seaweed_on_the_Banks_of_the_Berb%C3%A9s_1892.jpg) | Es una pintura, no una fotografía. |

## Otras fuentes para buscar más

- [Category:History of Vigo](https://commons.wikimedia.org/wiki/Category:History_of_Vigo) y sus subcategorías en Wikimedia Commons.
- [ETH-Bibliothek, E-Pics Bildarchiv](https://ba.e-pics.ethz.ch/): fotos de Vigo de 1896–1934 con licencia CC BY-SA 4.0.
- [Biblioteca Digital Hispánica](https://bdh.bne.es/) y [Europeana](https://www.europeana.eu/): postales antiguas. Revisar la licencia de cada una.
