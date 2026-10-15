#!/usr/bin/env python3
"""
Títulos y descripciones de cada foto en los cinco idiomas de la web
(es, gl, en, pt, fr), para que el visitante lo lea todo en un solo idioma.

Ejecutar tras editar: python3 scripts/textos_fotos.py
Escribe el campo "textos" de cada foto en data/fotos.json.
Formato: id: (título_es, desc_es, título_gl, desc_gl, título_en, desc_en,
              título_pt, desc_pt, título_fr, desc_fr)
"""
import json
from pathlib import Path

T = {
"commons-castro-thoman": (
 "Vigo desde el Castro", "La ciudad y la ría vistas desde el monte del Castro.",
 "Vigo dende o Castro", "A cidade e a ría vistas dende o monte do Castro.",
 "Vigo from O Castro", "The city and the estuary seen from O Castro hill.",
 "Vigo visto do Castro", "A cidade e a ria vistas do monte do Castro.",
 "Vigo depuis le Castro", "La ville et la ria vues depuis la colline du Castro."),
"commons-eth-lotse-1896": (
 "Barca de prácticos junto a un barco", "Una pequeña barca de prácticos se acerca al costado de un barco en la ría.",
 "Barca de prácticos xunto a un barco", "Unha pequena barca de prácticos achégase ao costado dun barco na ría.",
 "Pilot boat beside a ship", "A small pilot boat comes alongside a ship in the estuary.",
 "Barco de pilotos junto a um navio", "Um pequeno barco de pilotos aproxima-se do costado de um navio na ria.",
 "Bateau-pilote le long d'un navire", "Un petit bateau-pilote accoste un navire dans la ria."),
"commons-eth-lotse-1898": (
 "Barca de prácticos en la ría", "Pequeña embarcación al costado de un barco.",
 "Barca de prácticos na ría", "Pequena embarcación ao costado dun barco.",
 "Pilot boat in the estuary", "A small boat alongside a ship.",
 "Barco de pilotos na ria", "Pequena embarcação ao costado de um navio.",
 "Bateau-pilote dans la ria", "Petite embarcation le long d'un navire."),
"commons-vigo-1877": (
 "Vista general de la ciudad y del puerto (grabado)", "Grabado de La Ilustración Española y Americana (1877), hecho a partir de una fotografía con motivo de la visita del rey.",
 "Vista xeral da cidade e do porto (gravado)", "Gravado de La Ilustración Española y Americana (1877), feito a partir dunha fotografía con motivo da visita do rei.",
 "General view of the city and port (engraving)", "Engraving from La Ilustración Española y Americana (1877), made from a photograph on the occasion of the king's visit.",
 "Vista geral da cidade e do porto (gravura)", "Gravura de La Ilustración Española y Americana (1877), feita a partir de uma fotografia por ocasião da visita do rei.",
 "Vue générale de la ville et du port (gravure)", "Gravure de La Ilustración Española y Americana (1877), réalisée d'après une photographie lors de la visite du roi."),
"commons-krapf-chocolatero": (
 "Chocolatero y churrero", "Retrato de dos vendedores ambulantes de chocolate y churros.",
 "Chocolateiro e churreiro", "Retrato de dous vendedores ambulantes de chocolate e churros.",
 "Chocolate and churro sellers", "Portrait of two street vendors selling chocolate and churros.",
 "Vendedores de chocolate e churros", "Retrato de dois vendedores ambulantes de chocolate e churros.",
 "Marchands de chocolat et de churros", "Portrait de deux marchands ambulants de chocolat et de churros."),
"commons-krapf-playa-1901": (
 "En la playa de Vigo", "Escena en una playa de Vigo, con texto de Luis Taboada.",
 "Na praia de Vigo", "Escena nunha praia de Vigo, con texto de Luis Taboada.",
 "On the beach in Vigo", "A scene on a beach in Vigo, with text by Luis Taboada.",
 "Na praia de Vigo", "Cena numa praia de Vigo, com texto de Luis Taboada.",
 "Sur la plage de Vigo", "Scène sur une plage de Vigo, avec un texte de Luis Taboada."),
"commons-krapf-casa-caridad": (
 "La Casa de Caridad", "Edificio de la Casa de Caridad de Vigo.",
 "A Casa de Caridade", "Edificio da Casa de Caridade de Vigo.",
 "The Charity House", "The building of Vigo's Casa de Caridad (charity house).",
 "A Casa de Caridade", "Edifício da Casa de Caridade de Vigo.",
 "La Maison de charité", "Le bâtiment de la Casa de Caridad (maison de charité) de Vigo."),
"commons-hauser-berbes-1925": (
 "Fuente de la Ribera del Berbés", "La fuente de la Ribera del Berbés, en el antiguo barrio marinero.",
 "Fonte da Ribeira do Berbés", "A fonte da Ribeira do Berbés, no antigo barrio mariñeiro.",
 "Fountain on the Ribeira do Berbés", "The fountain on the Ribeira do Berbés, in the old fishermen's quarter.",
 "Fonte da Ribeira do Berbés", "A fonte da Ribeira do Berbés, no antigo bairro piscatório.",
 "Fontaine de la Ribeira do Berbés", "La fontaine de la Ribeira do Berbés, dans l'ancien quartier des pêcheurs."),
"commons-pacheco-royalty": (
 "Cine Royalty", "El cine Royalty, en la calle Velázquez Moreno.",
 "Cine Royalty", "O cine Royalty, na rúa Velázquez Moreno.",
 "Royalty Cinema", "The Royalty cinema on Velázquez Moreno street.",
 "Cinema Royalty", "O cinema Royalty, na rua Velázquez Moreno.",
 "Cinéma Royalty", "Le cinéma Royalty, rue Velázquez Moreno."),
"commons-escuela-obrera": (
 "Entrega de diplomas de la Escuela Obrera", "Mercedes de la Escalera entrega diplomas de la Escuela Obrera de Vigo.",
 "Entrega de diplomas da Escola Obreira", "Mercedes de la Escalera entrega diplomas da Escola Obreira de Vigo.",
 "Workers' School diploma ceremony", "Mercedes de la Escalera hands out diplomas at Vigo's Workers' School.",
 "Entrega de diplomas da Escola Operária", "Mercedes de la Escalera entrega diplomas da Escola Operária de Vigo.",
 "Remise des diplômes de l'École ouvrière", "Mercedes de la Escalera remet les diplômes de l'École ouvrière de Vigo."),
"commons-iln-atalanta-1880": (
 "Búsqueda del HMS Atalanta (grabado)", "Grabado de The Illustrated London News (1880) sobre la búsqueda de la fragata británica HMS Atalanta, desaparecida ese año.",
 "Busca do HMS Atalanta (gravado)", "Gravado de The Illustrated London News (1880) sobre a busca da fragata británica HMS Atalanta, desaparecida ese ano.",
 "Search for HMS Atalanta (engraving)", "Engraving from The Illustrated London News (1880) on the search for the British frigate HMS Atalanta, lost that year.",
 "Busca do HMS Atalanta (gravura)", "Gravura de The Illustrated London News (1880) sobre a busca da fragata britânica HMS Atalanta, desaparecida nesse ano.",
 "Recherche du HMS Atalanta (gravure)", "Gravure de The Illustrated London News (1880) sur la recherche de la frégate britannique HMS Atalanta, disparue cette année-là."),
"commons-batalla-1832": (
 "Batalla de Vigo, 1832 (ilustración coloreada)", "Ilustración coloreada de un combate naval en Vigo en octubre de 1832.",
 "Batalla de Vigo, 1832 (ilustración coloreada)", "Ilustración coloreada dun combate naval en Vigo en outubro de 1832.",
 "Battle of Vigo, 1832 (coloured illustration)", "Coloured illustration of a naval engagement at Vigo in October 1832.",
 "Batalha de Vigo, 1832 (ilustração colorida)", "Ilustração colorida de um combate naval em Vigo em outubro de 1832.",
 "Bataille de Vigo, 1832 (illustration colorisée)", "Illustration colorisée d'un combat naval à Vigo en octobre 1832."),
"commons-eth-panorama-1934": (
 "Panorama de Vigo hacia el este", "Panorámica de la ciudad mirando al este.",
 "Panorama de Vigo cara ao leste", "Panorámica da cidade mirando ao leste.",
 "Panorama of Vigo looking east", "Panoramic view of the city looking east.",
 "Panorama de Vigo para leste", "Panorâmica da cidade olhando para leste.",
 "Panorama de Vigo vers l'est", "Vue panoramique de la ville vers l'est."),
"commons-21170705": (
 "Recogiendo algas en la ribera del Berbés (pintura)", "Pintura de Juan Martínez Abades, 1892.",
 "Recollendo algas na ribeira do Berbés (pintura)", "Pintura de Juan Martínez Abades, 1892.",
 "Gathering seaweed on the Berbés shore (painting)", "Painting by Juan Martínez Abades, 1892.",
 "Apanhando algas na ribeira do Berbés (pintura)", "Pintura de Juan Martínez Abades, 1892.",
 "Ramassage d'algues sur la rive du Berbés (peinture)", "Peinture de Juan Martínez Abades, 1892."),
"commons-57430185": (
 "La estación marítima", "La antigua estación marítima de Vigo, entre 1920 y 1940.",
 "A estación marítima", "A antiga estación marítima de Vigo, entre 1920 e 1940.",
 "The maritime station", "Vigo's old maritime station, between 1920 and 1940.",
 "A estação marítima", "A antiga estação marítima de Vigo, entre 1920 e 1940.",
 "La gare maritime", "L'ancienne gare maritime de Vigo, entre 1920 et 1940."),
"commons-57430186": (
 "El Berbés y Bouzas", "Vista de la zona del Berbés y Bouzas, entre 1920 y 1940.",
 "O Berbés e Bouzas", "Vista da zona do Berbés e Bouzas, entre 1920 e 1940.",
 "O Berbés and Bouzas", "View of the Berbés and Bouzas area, between 1920 and 1940.",
 "O Berbés e Bouzas", "Vista da zona do Berbés e Bouzas, entre 1920 e 1940.",
 "Le Berbés et Bouzas", "Vue du secteur du Berbés et de Bouzas, entre 1920 et 1940."),
"commons-66462326": (
 "Vigo saluda a los héroes de El Callao", "Recibimiento en Vigo a los marinos del combate de El Callao (1866).",
 "Vigo saúda os heroes do Callao", "Recibimento en Vigo aos mariños do combate do Callao (1866).",
 "Vigo welcomes the heroes of Callao", "Vigo's welcome for the sailors of the Battle of Callao (1866).",
 "Vigo saúda os heróis de Callao", "Receção em Vigo aos marinheiros do combate de Callao (1866).",
 "Vigo salue les héros de Callao", "Accueil à Vigo des marins du combat de Callao (1866)."),
"commons-68547623": (
 "Panorama de Vigo hacia el oeste", "Panorámica de la ciudad mirando al oeste.",
 "Panorama de Vigo cara ao oeste", "Panorámica da cidade mirando ao oeste.",
 "Panorama of Vigo looking west", "Panoramic view of the city looking west.",
 "Panorama de Vigo para oeste", "Panorâmica da cidade olhando para oeste.",
 "Panorama de Vigo vers l'ouest", "Vue panoramique de la ville vers l'ouest."),
"commons-68547635": (
 "La bahía vista desde el oeste", "Vista de la ría desde el oeste. Diapositiva coloreada por Margrit Wehrli-Frey.",
 "A baía vista dende o oeste", "Vista da ría dende o oeste. Diapositiva coloreada por Margrit Wehrli-Frey.",
 "The bay seen from the west", "View of the estuary from the west. Slide hand-coloured by Margrit Wehrli-Frey.",
 "A baía vista de oeste", "Vista da ria a partir de oeste. Diapositivo colorido por Margrit Wehrli-Frey.",
 "La baie vue de l'ouest", "Vue de la ria depuis l'ouest. Diapositive colorisée par Margrit Wehrli-Frey."),
"commons-146177243": (
 "Batalla de Vigo, octubre de 1832", "Grabado a partir de una pintura de W. J. Huggins, pintor de marina del rey de Inglaterra (1833).",
 "Batalla de Vigo, outubro de 1832", "Gravado a partir dunha pintura de W. J. Huggins, pintor de mariña do rei de Inglaterra (1833).",
 "Battle of Vigo, October 1832", "Print after a painting by W. J. Huggins, marine painter to the King of England (1833).",
 "Batalha de Vigo, outubro de 1832", "Gravura a partir de uma pintura de W. J. Huggins, pintor de marinha do rei de Inglaterra (1833).",
 "Bataille de Vigo, octobre 1832", "Gravure d'après une peinture de W. J. Huggins, peintre de marine du roi d'Angleterre (1833)."),
"commons-161860392": (
 "Francisco Llanos Mas ante un expositor de fotografías", "El fotógrafo Francisco Llanos Mas en la época en que se estableció en Vigo, hacia 1901.",
 "Francisco Llanos Mas diante dun expositor de fotografías", "O fotógrafo Francisco Llanos Mas na época en que se estableceu en Vigo, cara a 1901.",
 "Francisco Llanos Mas beside a photo display", "Photographer Francisco Llanos Mas around the time he set up in Vigo, c. 1901.",
 "Francisco Llanos Mas diante de um expositor de fotografias", "O fotógrafo Francisco Llanos Mas na época em que se estabeleceu em Vigo, c. 1901.",
 "Francisco Llanos Mas devant une vitrine de photographies", "Le photographe Francisco Llanos Mas à l'époque de son installation à Vigo, vers 1901."),
"commons-194672206": (
 "Tranvía en la Porta do Sol", "Un tranvía de Vigo circula por la Porta do Sol.",
 "Tranvía na Porta do Sol", "Un tranvía de Vigo circula pola Porta do Sol.",
 "Tram at Porta do Sol", "A Vigo tram running through Porta do Sol.",
 "Elétrico na Porta do Sol", "Um elétrico de Vigo circula pela Porta do Sol.",
 "Tramway à la Porta do Sol", "Un tramway de Vigo traverse la Porta do Sol."),
"commons-195936153": (
 "Avenida de García Barbón", "La avenida de García Barbón en una postal de los años 20 o 30.",
 "Avenida de García Barbón", "A avenida de García Barbón nunha postal dos anos 20 ou 30.",
 "García Barbón Avenue", "García Barbón Avenue on a postcard from the 1920s or 1930s.",
 "Avenida de García Barbón", "A avenida de García Barbón num postal dos anos 20 ou 30.",
 "Avenue García Barbón", "L'avenue García Barbón sur une carte postale des années 1920 ou 1930."),
"commons-195947702": (
 "Porta do Sol a principios del siglo XX", "La Porta do Sol en una postal de comienzos del siglo XX.",
 "Porta do Sol a comezos do século XX", "A Porta do Sol nunha postal de comezos do século XX.",
 "Porta do Sol in the early 20th century", "Porta do Sol on an early 20th-century postcard.",
 "Porta do Sol no início do século XX", "A Porta do Sol num postal do início do século XX.",
 "La Porta do Sol au début du XXe siècle", "La Porta do Sol sur une carte postale du début du XXe siècle."),
"commons-196084836": (
 "Barricadas en el Calvario, 1936", "Barricadas en el barrio del Calvario, entonces en el municipio de Lavadores, al comienzo de la Guerra Civil.",
 "Barricadas no Calvario, 1936", "Barricadas no barrio do Calvario, daquela no concello de Lavadores, ao comezo da Guerra Civil.",
 "Barricades in O Calvario, 1936", "Barricades in the Calvario neighbourhood, then in the municipality of Lavadores, at the start of the Spanish Civil War.",
 "Barricadas no Calvario, 1936", "Barricadas no bairro do Calvario, então no município de Lavadores, no início da Guerra Civil.",
 "Barricades au Calvario, 1936", "Barricades dans le quartier du Calvario, alors sur la commune de Lavadores, au début de la guerre civile."),
"commons-197160994": (
 "Avenida de Cánovas del Castillo", "La avenida en una postal anterior a 1907.",
 "Avenida de Cánovas del Castillo", "A avenida nunha postal anterior a 1907.",
 "Cánovas del Castillo Avenue", "The avenue on a postcard from before 1907.",
 "Avenida de Cánovas del Castillo", "A avenida num postal anterior a 1907.",
 "Avenue Cánovas del Castillo", "L'avenue sur une carte postale antérieure à 1907."),
"commons-36401743": (
 "La antigua pescadería de la Ribera (grabado)", "Grabado de La Ilustración Española y Americana.",
 "A antiga pescadería da Ribeira (gravado)", "Gravado de La Ilustración Española y Americana.",
 "The old Ribera fish market (engraving)", "Engraving from La Ilustración Española y Americana.",
 "A antiga peixaria da Ribeira (gravura)", "Gravura de La Ilustración Española y Americana.",
 "L'ancienne poissonnerie de la Ribera (gravure)", "Gravure de La Ilustración Española y Americana."),
"commons-40079622": (
 "Vigo hacia 1895", "Fotografía de Filippo Prosperi.",
 "Vigo cara a 1895", "Fotografía de Filippo Prosperi.",
 "Vigo around 1895", "Photograph by Filippo Prosperi.",
 "Vigo por volta de 1895", "Fotografia de Filippo Prosperi.",
 "Vigo vers 1895", "Photographie de Filippo Prosperi."),
"commons-86795309": (
 "Fortaleza junto a Vigo, 1867", "",
 "Fortaleza xunto a Vigo, 1867", "",
 "Fort near Vigo, 1867", "",
 "Fortaleza junto a Vigo, 1867", "",
 "Fort près de Vigo, 1867", ""),
"commons-87776921": (
 "Inauguración de la estatua de Méndez Núñez (grabado)", "Inauguración de la estatua en los jardines de la Alameda, 1890. Grabado a partir de fotografías de Felipe Prosperi.",
 "Inauguración da estatua de Méndez Núñez (gravado)", "Inauguración da estatua nos xardíns da Alameda, 1890. Gravado a partir de fotografías de Felipe Prosperi.",
 "Unveiling of the Méndez Núñez statue (engraving)", "Unveiling of the statue in the Alameda gardens, 1890. Engraving after photographs by Felipe Prosperi.",
 "Inauguração da estátua de Méndez Núñez (gravura)", "Inauguração da estátua nos jardins da Alameda, 1890. Gravura a partir de fotografias de Felipe Prosperi.",
 "Inauguration de la statue de Méndez Núñez (gravure)", "Inauguration de la statue dans les jardins de l'Alameda, 1890. Gravure d'après des photographies de Felipe Prosperi."),
"commons-95680035": (
 "Juegos florales en el teatro (grabado)", "Juegos florales celebrados en el teatro de Vigo, presididos por Emilio Castelar.",
 "Xogos florais no teatro (gravado)", "Xogos florais celebrados no teatro de Vigo, presididos por Emilio Castelar.",
 "Floral games at the theatre (engraving)", "Floral games (poetry contest) held at Vigo's theatre, presided over by Emilio Castelar.",
 "Jogos florais no teatro (gravura)", "Jogos florais celebrados no teatro de Vigo, presididos por Emilio Castelar.",
 "Jeux floraux au théâtre (gravure)", "Jeux floraux célébrés au théâtre de Vigo, sous la présidence d'Emilio Castelar."),
"commons-105835583": (
 "Viaje del rey a las provincias del noroeste (grabado)", "Grabado de La Ilustración Española y Americana, 1877.",
 "Viaxe do rei ás provincias do noroeste (gravado)", "Gravado de La Ilustración Española y Americana, 1877.",
 "The king's journey to the north-western provinces (engraving)", "Engraving from La Ilustración Española y Americana, 1877.",
 "Viagem do rei às províncias do noroeste (gravura)", "Gravura de La Ilustración Española y Americana, 1877.",
 "Voyage du roi dans les provinces du nord-ouest (gravure)", "Gravure de La Ilustración Española y Americana, 1877."),
"commons-105853363": (
 "Vista general de la ciudad y del puerto, 1877 (grabado)", "Vista de Vigo durante la visita del rey, a partir de una fotografía enviada por Bocconi.",
 "Vista xeral da cidade e do porto, 1877 (gravado)", "Vista de Vigo durante a visita do rei, a partir dunha fotografía enviada por Bocconi.",
 "General view of the city and port, 1877 (engraving)", "View of Vigo during the king's visit, after a photograph sent by Bocconi.",
 "Vista geral da cidade e do porto, 1877 (gravura)", "Vista de Vigo durante a visita do rei, a partir de uma fotografia enviada por Bocconi.",
 "Vue générale de la ville et du port, 1877 (gravure)", "Vue de Vigo lors de la visite du roi, d'après une photographie envoyée par Bocconi."),
"commons-105857456": (
 "Últimos apuntes del viaje del rey (grabado)", "Grabado de La Ilustración Española y Americana, 1877.",
 "Últimos apuntamentos da viaxe do rei (gravado)", "Gravado de La Ilustración Española y Americana, 1877.",
 "Last sketches of the king's journey (engraving)", "Engraving from La Ilustración Española y Americana, 1877.",
 "Últimos apontamentos da viagem do rei (gravura)", "Gravura de La Ilustración Española y Americana, 1877.",
 "Derniers croquis du voyage du roi (gravure)", "Gravure de La Ilustración Española y Americana, 1877."),
"commons-117869650": (
 "La ribera de Vigo (pintura)", "Óleo de Aureliano de Beruete, hacia 1880.",
 "A ribeira de Vigo (pintura)", "Óleo de Aureliano de Beruete, cara a 1880.",
 "The Vigo waterfront (painting)", "Oil painting by Aureliano de Beruete, c. 1880.",
 "A ribeira de Vigo (pintura)", "Óleo de Aureliano de Beruete, c. 1880.",
 "La rive de Vigo (peinture)", "Huile d'Aureliano de Beruete, vers 1880."),
"commons-140454870": (
 "Ribera del Berbés (ilustración)", "Ilustración de Avendaño en la revista Blanco y Negro, 1896.",
 "Ribeira do Berbés (ilustración)", "Ilustración de Avendaño na revista Blanco y Negro, 1896.",
 "Ribeira do Berbés (illustration)", "Illustration by Avendaño in Blanco y Negro magazine, 1896.",
 "Ribeira do Berbés (ilustração)", "Ilustração de Avendaño na revista Blanco y Negro, 1896.",
 "Ribeira do Berbés (illustration)", "Illustration d'Avendaño dans la revue Blanco y Negro, 1896."),
"commons-140531962": (
 "Escabecheras de Vigo (ilustración)", "Tipos populares, ilustración de J. Araujo en Blanco y Negro, 1893.",
 "Escabecheiras de Vigo (ilustración)", "Tipos populares, ilustración de J. Araujo en Blanco y Negro, 1893.",
 "Fish-pickling women of Vigo (illustration)", "Local characters, illustration by J. Araujo in Blanco y Negro, 1893.",
 "Escabecheiras de Vigo (ilustração)", "Tipos populares, ilustração de J. Araujo em Blanco y Negro, 1893.",
 "Escabecheuses de Vigo (illustration)", "Types populaires, illustration de J. Araujo dans Blanco y Negro, 1893."),
"commons-16191166": (
 "Café Moderno", "Edificio El Moderno (1897), del arquitecto Michel Pacewicz, en Policarpo Sanz, 1. Postal de Hauser y Menet.",
 "Café Moderno", "Edificio El Moderno (1897), do arquitecto Michel Pacewicz, en Policarpo Sanz, 1. Postal de Hauser y Menet.",
 "Café Moderno", "El Moderno building (1897) by architect Michel Pacewicz, at Policarpo Sanz 1. Postcard by Hauser y Menet.",
 "Café Moderno", "Edifício El Moderno (1897), do arquiteto Michel Pacewicz, em Policarpo Sanz, 1. Postal de Hauser y Menet.",
 "Café Moderno", "Immeuble El Moderno (1897), de l'architecte Michel Pacewicz, au 1 rue Policarpo Sanz. Carte postale de Hauser y Menet."),
"commons-51926111": (
 "Pablo Iglesias y Heraclio Botana en Vigo", "Visita a Vigo del fundador del PSOE y la UGT, junto a Enrique Heraclio Botana.",
 "Pablo Iglesias e Heraclio Botana en Vigo", "Visita a Vigo do fundador do PSOE e a UGT, xunto a Enrique Heraclio Botana.",
 "Pablo Iglesias and Heraclio Botana in Vigo", "Visit to Vigo by the founder of the PSOE and UGT, with Enrique Heraclio Botana.",
 "Pablo Iglesias e Heraclio Botana em Vigo", "Visita a Vigo do fundador do PSOE e da UGT, com Enrique Heraclio Botana.",
 "Pablo Iglesias et Heraclio Botana à Vigo", "Visite à Vigo du fondateur du PSOE et de l'UGT, avec Enrique Heraclio Botana."),
"commons-51930364": (
 "Heraclio Botana en su despacho de la Casa del Pueblo", "Enrique Heraclio Botana trabajando en la Casa del Pueblo de Vigo.",
 "Heraclio Botana no seu despacho da Casa do Pobo", "Enrique Heraclio Botana traballando na Casa do Pobo de Vigo.",
 "Heraclio Botana in his office at the Casa del Pueblo", "Enrique Heraclio Botana at work in Vigo's Casa del Pueblo (workers' centre).",
 "Heraclio Botana no seu gabinete da Casa do Povo", "Enrique Heraclio Botana a trabalhar na Casa do Povo de Vigo.",
 "Heraclio Botana dans son bureau de la Maison du peuple", "Enrique Heraclio Botana au travail à la Maison du peuple de Vigo."),
"commons-51953169": (
 "Heraclio Botana y Emilio Martínez Garrido", "Con la Juventud Socialista de Vigo.",
 "Heraclio Botana e Emilio Martínez Garrido", "Coa Xuventude Socialista de Vigo.",
 "Heraclio Botana and Emilio Martínez Garrido", "With Vigo's Socialist Youth.",
 "Heraclio Botana e Emilio Martínez Garrido", "Com a Juventude Socialista de Vigo.",
 "Heraclio Botana et Emilio Martínez Garrido", "Avec la Jeunesse socialiste de Vigo."),
"commons-98309922": (
 "Encuentro del emperador de Alemania y el rey de España (grabado)", "Ilustración de Mariano Pedrero en La Ilustración Española y Americana, 1904.",
 "Encontro do emperador de Alemaña e o rei de España (gravado)", "Ilustración de Mariano Pedrero en La Ilustración Española y Americana, 1904.",
 "Meeting of the German Emperor and the King of Spain (engraving)", "Illustration by Mariano Pedrero in La Ilustración Española y Americana, 1904.",
 "Encontro do imperador da Alemanha e do rei de Espanha (gravura)", "Ilustração de Mariano Pedrero em La Ilustración Española y Americana, 1904.",
 "Rencontre de l'empereur d'Allemagne et du roi d'Espagne (gravure)", "Illustration de Mariano Pedrero dans La Ilustración Española y Americana, 1904."),
"commons-158231624": (
 "Naufragio del Southern Cross, 1909", "El buque Southern Cross naufragado en Punta Borneira, en la ría de Vigo.",
 "Naufraxio do Southern Cross, 1909", "O buque Southern Cross naufragado en Punta Borneira, na ría de Vigo.",
 "Wreck of the Southern Cross, 1909", "The Southern Cross wrecked at Punta Borneira, in the Vigo estuary.",
 "Naufrágio do Southern Cross, 1909", "O navio Southern Cross naufragado em Punta Borneira, na ria de Vigo.",
 "Naufrage du Southern Cross, 1909", "Le Southern Cross échoué à Punta Borneira, dans la ria de Vigo."),
"commons-159813099": (
 "Placa en homenaje a Nicolás Taboada Leal, 1910", "",
 "Placa en homenaxe a Nicolás Taboada Leal, 1910", "",
 "Plaque honouring Nicolás Taboada Leal, 1910", "",
 "Placa em homenagem a Nicolás Taboada Leal, 1910", "",
 "Plaque en hommage à Nicolás Taboada Leal, 1910", ""),
"commons-170563804": (
 "El castillo de San Sebastián en la Primera Guerra Mundial", "",
 "O castelo de San Sebastián na Primeira Guerra Mundial", "",
 "San Sebastián castle during the First World War", "",
 "O castelo de San Sebastián na Primeira Guerra Mundial", "",
 "Le château de San Sebastián pendant la Première Guerre mondiale", ""),
"commons-182420771": (
 "Panificadora de Vigo, 1927", "Fachada sur de la fábrica de pan. Archivo Pacheco.",
 "Panificadora de Vigo, 1927", "Fachada sur da fábrica de pan. Arquivo Pacheco.",
 "Vigo bread factory, 1927", "South façade of the bread factory. Pacheco Archive.",
 "Panificadora de Vigo, 1927", "Fachada sul da fábrica de pão. Arquivo Pacheco.",
 "Boulangerie industrielle de Vigo, 1927", "Façade sud de la fabrique de pain. Archives Pacheco."),
"commons-187041329": (
 "Mercado de A Laxe, 1927", "El antiguo mercado, derribado en los años 60 para construir el hotel Bahía.",
 "Mercado da Laxe, 1927", "O antigo mercado, derrubado nos anos 60 para construír o hotel Bahía.",
 "A Laxe market, 1927", "The old market, demolished in the 1960s to build the Hotel Bahía.",
 "Mercado da Laxe, 1927", "O antigo mercado, demolido nos anos 60 para construir o hotel Bahía.",
 "Marché d'A Laxe, 1927", "L'ancien marché, démoli dans les années 1960 pour construire l'hôtel Bahía."),
"commons-195628024": (
 "Caja de Ahorros Municipal en la Casa Bárcena", "Sede de la Caja de Ahorros y Monte de Piedad Municipal de Vigo.",
 "Caixa de Aforros Municipal na Casa Bárcena", "Sede da Caixa de Aforros e Monte de Piedade Municipal de Vigo.",
 "Municipal Savings Bank in the Casa Bárcena", "Headquarters of Vigo's Municipal Savings Bank and pawnshop.",
 "Caixa Económica Municipal na Casa Bárcena", "Sede da Caixa Económica e Monte de Piedade Municipal de Vigo.",
 "Caisse d'épargne municipale, Casa Bárcena", "Siège de la Caisse d'épargne et mont-de-piété municipal de Vigo."),
"commons-195630584": (
 "Casa Bárcena", "Sede de la Caja de Ahorros y Monte de Piedad Municipal de Vigo.",
 "Casa Bárcena", "Sede da Caixa de Aforros e Monte de Piedade Municipal de Vigo.",
 "Casa Bárcena", "Headquarters of Vigo's Municipal Savings Bank and pawnshop.",
 "Casa Bárcena", "Sede da Caixa Económica e Monte de Piedade Municipal de Vigo.",
 "Casa Bárcena", "Siège de la Caisse d'épargne et mont-de-piété municipal de Vigo."),
"commons-201611775": (
 "Delegación en Vigo del Lar Gallego de Caracas, 1954", "",
 "Delegación en Vigo do Lar Gallego de Caracas, 1954", "",
 "Vigo branch of the Lar Gallego of Caracas, 1954", "",
 "Delegação em Vigo do Lar Gallego de Caracas, 1954", "",
 "Délégation à Vigo du Lar Gallego de Caracas, 1954", ""),
"commons-67820290": (
 "Joaquín Tenreiro Montenegro", "Retrato del primer conde de Vigo.",
 "Joaquín Tenreiro Montenegro", "Retrato do primeiro conde de Vigo.",
 "Joaquín Tenreiro Montenegro", "Portrait of the first Count of Vigo.",
 "Joaquín Tenreiro Montenegro", "Retrato do primeiro conde de Vigo.",
 "Joaquín Tenreiro Montenegro", "Portrait du premier comte de Vigo."),
"commons-67903692": (
 "Toma de Vigo por los españoles (grabado)", "La reconquista de Vigo frente a las tropas francesas en 1809.",
 "Toma de Vigo polos españois (gravado)", "A reconquista de Vigo fronte ás tropas francesas en 1809.",
 "Capture of Vigo by the Spanish (engraving)", "The recapture of Vigo from French troops in 1809.",
 "Tomada de Vigo pelos espanhóis (gravura)", "A reconquista de Vigo às tropas francesas em 1809.",
 "Prise de Vigo par les Espagnols (gravure)", "La reprise de Vigo aux troupes françaises en 1809."),
"commons-67904984": (
 "Los abades de Couto y Valladares (grabado)", "Protagonistas de la reconquista de Vigo en 1809.",
 "Os abades de Couto e Valadares (gravado)", "Protagonistas da reconquista de Vigo en 1809.",
 "The abbots of Couto and Valladares (engraving)", "Leading figures in the recapture of Vigo in 1809.",
 "Os abades de Couto e Valadares (gravura)", "Protagonistas da reconquista de Vigo em 1809.",
 "Les abbés de Couto et Valladares (gravure)", "Figures de la reprise de Vigo en 1809."),
"commons-68214906": (
 "Los guerrilleros gallegos entran por la Puerta de la Gamboa", "Episodio de la reconquista de Vigo en 1809.",
 "Os guerrilleiros galegos entran pola porta da Gamboa", "Episodio da reconquista de Vigo en 1809.",
 "Galician guerrillas enter through the Gamboa gate", "An episode in the recapture of Vigo in 1809.",
 "Os guerrilheiros galegos entram pela porta da Gamboa", "Episódio da reconquista de Vigo em 1809.",
 "Les guérilleros galiciens entrent par la porte de la Gamboa", "Épisode de la reprise de Vigo en 1809."),
"commons-61257788": (
 "Vista del Areal, 1892 (pintura)", "Pintura de Juan Martínez Abades.",
 "Vista do Areal, 1892 (pintura)", "Pintura de Juan Martínez Abades.",
 "View of O Areal, 1892 (painting)", "Painting by Juan Martínez Abades.",
 "Vista do Areal, 1892 (pintura)", "Pintura de Juan Martínez Abades.",
 "Vue de l'Areal, 1892 (peinture)", "Peinture de Juan Martínez Abades."),
"commons-52039467": (
 "Detención de uno de los autores del atentado contra Paz Andrade", "",
 "Detención dun dos autores do atentado contra Paz Andrade", "",
 "Arrest of one of the attackers of Paz Andrade", "",
 "Detenção de um dos autores do atentado contra Paz Andrade", "",
 "Arrestation de l'un des auteurs de l'attentat contre Paz Andrade", ""),
"commons-72018904": (
 "Colegio Apóstol Santiago de Teis, 1932", "Colegio jesuita de Teis, con Xosé Manuel Cábada Vázquez y Xesús Ferro Couselo, entre otros.",
 "Colexio Apóstolo Santiago de Teis, 1932", "Colexio xesuíta de Teis, con Xosé Manuel Cábada Vázquez e Xesús Ferro Couselo, entre outros.",
 "Apóstolo Santiago School, Teis, 1932", "Jesuit school in Teis, with Xosé Manuel Cábada Vázquez and Xesús Ferro Couselo, among others.",
 "Colégio Apóstolo Santiago de Teis, 1932", "Colégio jesuíta de Teis, com Xosé Manuel Cábada Vázquez e Xesús Ferro Couselo, entre outros.",
 "Collège Apóstolo Santiago de Teis, 1932", "Collège jésuite de Teis, avec Xosé Manuel Cábada Vázquez et Xesús Ferro Couselo, entre autres."),
"commons-76814215": (
 "Lorca y Ugarte, creadores de La Barraca", "Con el uniforme de la compañía teatral. Vigo, agosto de 1932.",
 "Lorca e Ugarte, creadores de La Barraca", "Co uniforme da compañía teatral. Vigo, agosto de 1932.",
 "Lorca and Ugarte, founders of La Barraca", "Wearing the theatre company's uniform. Vigo, August 1932.",
 "Lorca e Ugarte, criadores de La Barraca", "Com o uniforme da companhia de teatro. Vigo, agosto de 1932.",
 "Lorca et Ugarte, créateurs de La Barraca", "En uniforme de la compagnie théâtrale. Vigo, août 1932."),
"commons-76823516": (
 "Lorca y La Barraca en la calle del Príncipe", "Gonzalo Menéndez Pidal filma a Federico García Lorca y la compañía en la calle del Príncipe (entonces Capitán Galán), agosto de 1932.",
 "Lorca e La Barraca na rúa do Príncipe", "Gonzalo Menéndez Pidal filma a Federico García Lorca e a compañía na rúa do Príncipe (daquela Capitán Galán), agosto de 1932.",
 "Lorca and La Barraca on Rúa do Príncipe", "Gonzalo Menéndez Pidal films Federico García Lorca and the company on Rúa do Príncipe (then Capitán Galán), August 1932.",
 "Lorca e La Barraca na rua do Príncipe", "Gonzalo Menéndez Pidal filma Federico García Lorca e a companhia na rua do Príncipe (então Capitán Galán), agosto de 1932.",
 "Lorca et La Barraca rue du Príncipe", "Gonzalo Menéndez Pidal filme Federico García Lorca et la compagnie rue du Príncipe (alors Capitán Galán), août 1932."),
"commons-76835209": (
 "Lorca en Vigo, mayo de 1932", "Federico García Lorca tras una conferencia, con Manuel Gómez Román y otros vigueses.",
 "Lorca en Vigo, maio de 1932", "Federico García Lorca tras unha conferencia, con Manuel Gómez Román e outros vigueses.",
 "Lorca in Vigo, May 1932", "Federico García Lorca after a lecture, with Manuel Gómez Román and others from Vigo.",
 "Lorca em Vigo, maio de 1932", "Federico García Lorca depois de uma conferência, com Manuel Gómez Román e outros vigueses.",
 "Lorca à Vigo, mai 1932", "Federico García Lorca après une conférence, avec Manuel Gómez Román et d'autres Vigolais."),
"commons-76844617": (
 "La Barraca en el parque de Cabanas, 1932", "Federico García Lorca y la compañía en el desaparecido parque de Cabanas, agosto de 1932.",
 "La Barraca no parque de Cabanas, 1932", "Federico García Lorca e a compañía no desaparecido parque de Cabanas, agosto de 1932.",
 "La Barraca in Cabanas park, 1932", "Federico García Lorca and the company in the now-vanished Cabanas park, August 1932.",
 "La Barraca no parque de Cabanas, 1932", "Federico García Lorca e a companhia no desaparecido parque de Cabanas, agosto de 1932.",
 "La Barraca au parc de Cabanas, 1932", "Federico García Lorca et la compagnie dans l'ancien parc de Cabanas, août 1932."),
"commons-50480620": (
 "Alexandre Bóveda, 1935", "Conferencia sobre el Estatuto de Autonomía en la Asociación Gallega de Contables.",
 "Alexandre Bóveda, 1935", "Conferencia sobre o Estatuto de Autonomía na Asociación Galega de Contables.",
 "Alexandre Bóveda, 1935", "Lecture on the Statute of Autonomy at the Galician Accountants' Association.",
 "Alexandre Bóveda, 1935", "Conferência sobre o Estatuto de Autonomia na Associação Galega de Contabilistas.",
 "Alexandre Bóveda, 1935", "Conférence sur le statut d'autonomie à l'Association galicienne des comptables."),
"commons-17539169": (
 "El puerto, 1967", "Vista del puerto desde el monumento a los Galeones de Rande.",
 "O porto, 1967", "Vista do porto dende o monumento aos Galeóns de Rande.",
 "The port, 1967", "View of the port from the monument to the Rande galleons.",
 "O porto, 1967", "Vista do porto a partir do monumento aos Galeões de Rande.",
 "Le port, 1967", "Vue du port depuis le monument aux galions de Rande."),
"commons-17539191": (
 "Monumento a los Galeones de Rande, 1967", "",
 "Monumento aos Galeóns de Rande, 1967", "",
 "Monument to the Rande galleons, 1967", "",
 "Monumento aos Galeões de Rande, 1967", "",
 "Monument aux galions de Rande, 1967", ""),
"commons-17539204": (
 "Bateas de mejillón, 1967", "Cultivo de mejillón en la ría de Vigo.",
 "Bateas de mexillón, 1967", "Cultivo de mexillón na ría de Vigo.",
 "Mussel rafts, 1967", "Mussel farming in the Vigo estuary.",
 "Jangadas de mexilhão, 1967", "Cultivo de mexilhão na ria de Vigo.",
 "Radeaux à moules, 1967", "Élevage de moules dans la ria de Vigo."),
"commons-40248": (
 "La bahía de Vigo (ilustración)", "Ilustración de «Veinte mil leguas de viaje submarino», de Julio Verne.",
 "A baía de Vigo (ilustración)", "Ilustración de «Vinte mil leguas de viaxe submarina», de Xulio Verne.",
 "Vigo Bay (illustration)", "Illustration from Jules Verne's \"Twenty Thousand Leagues Under the Seas\".",
 "A baía de Vigo (ilustração)", "Ilustração de «Vinte Mil Léguas Submarinas», de Júlio Verne.",
 "La baie de Vigo (illustration)", "Illustration de « Vingt mille lieues sous les mers », de Jules Verne."),
"commons-66509844": (
 "1702: destrucción de la flota francesa en la bahía de Vigo (grabado)", "La batalla de Rande.",
 "1702: destrución da frota francesa na baía de Vigo (gravado)", "A batalla de Rande.",
 "1702: destruction of the French fleet in Vigo Bay (engraving)", "The Battle of Vigo Bay (Rande).",
 "1702: destruição da frota francesa na baía de Vigo (gravura)", "A batalha de Rande.",
 "1702 : destruction de la flotte française dans la baie de Vigo (gravure)", "La bataille de Rande."),
"commons-116818265": (
 "Ramón Arbones Carballido", "",
 "Ramón Arbones Carballido", "",
 "Ramón Arbones Carballido", "",
 "Ramón Arbones Carballido", "",
 "Ramón Arbones Carballido", ""),
"commons-117086024": (
 "Francisco López Carballo", "Pintor y político gallego.",
 "Francisco López Carballo", "Pintor e político galego.",
 "Francisco López Carballo", "Galician painter and politician.",
 "Francisco López Carballo", "Pintor e político galego.",
 "Francisco López Carballo", "Peintre et homme politique galicien."),
"commons-166474514": (
 "Pedro Guimarey Filgueiras", "",
 "Pedro Guimarey Filgueiras", "",
 "Pedro Guimarey Filgueiras", "",
 "Pedro Guimarey Filgueiras", "",
 "Pedro Guimarey Filgueiras", ""),
"commons-57430182": (
 "El Real Club Náutico", "La zona del Real Club Náutico de Vigo, entre 1920 y 1940.",
 "O Real Club Náutico", "A zona do Real Club Náutico de Vigo, entre 1920 e 1940.",
 "The Royal Yacht Club", "The area of Vigo's Real Club Náutico, between 1920 and 1940.",
 "O Real Clube Náutico", "A zona do Real Club Náutico de Vigo, entre 1920 e 1940.",
 "Le Real Club Náutico", "Le secteur du Real Club Náutico de Vigo, entre 1920 et 1940."),
"commons-139106233": (
 "Embarque de tropas para África, 1921", "Soldados embarcando hacia Melilla en el puerto de Vigo. Archivo Llanos.",
 "Embarque de tropas para África, 1921", "Soldados embarcando cara a Melilla no porto de Vigo. Arquivo Llanos.",
 "Troops embarking for Africa, 1921", "Soldiers boarding for Melilla in the port of Vigo. Llanos Archive.",
 "Embarque de tropas para África, 1921", "Soldados a embarcar para Melilla no porto de Vigo. Arquivo Llanos.",
 "Embarquement de troupes pour l'Afrique, 1921", "Soldats embarquant pour Melilla dans le port de Vigo. Archives Llanos."),
"commons-156997264": (
 "Entierro de un marino ruso, 1908", "Entierro de un tripulante del acorazado ruso Tsesarevich en el puerto de Vigo.",
 "Enterro dun mariño ruso, 1908", "Enterro dun tripulante do acoirazado ruso Tsesarevich no porto de Vigo.",
 "Funeral of a Russian sailor, 1908", "Funeral of a crew member of the Russian battleship Tsesarevich in the port of Vigo.",
 "Funeral de um marinheiro russo, 1908", "Funeral de um tripulante do couraçado russo Tsesarevich no porto de Vigo.",
 "Obsèques d'un marin russe, 1908", "Obsèques d'un membre d'équipage du cuirassé russe Tsesarevich dans le port de Vigo."),
"commons-157556434": (
 "El crucero Carlos V, 1909", "El crucero Carlos V en el puerto de Vigo.",
 "O cruceiro Carlos V, 1909", "O cruceiro Carlos V no porto de Vigo.",
 "The cruiser Carlos V, 1909", "The cruiser Carlos V in the port of Vigo.",
 "O cruzador Carlos V, 1909", "O cruzador Carlos V no porto de Vigo.",
 "Le croiseur Carlos V, 1909", "Le croiseur Carlos V dans le port de Vigo."),
"commons-77842583": (
 "La ría con un edificio y un paseo arbolado", "",
 "A ría cun edificio e un paseo arborado", "",
 "The estuary with a building and a tree-lined promenade", "",
 "A ria com um edifício e um passeio arborizado", "",
 "La ria avec un bâtiment et une promenade arborée", ""),
"commons-77843295": (
 "Costa de la ría con árboles en primer plano", "",
 "Costa da ría con árbores en primeiro plano", "",
 "The estuary shore with trees in the foreground", "",
 "Costa da ria com árvores em primeiro plano", "",
 "Côte de la ria avec des arbres au premier plan", ""),
"commons-77843657": (
 "Embarcaciones y puerto en la ría", "",
 "Embarcacións e porto na ría", "",
 "Boats and harbour in the estuary", "",
 "Embarcações e porto na ria", "",
 "Embarcations et port dans la ria", ""),
"commons-77844158": (
 "Casa rodeada de árboles con vista a la ría", "",
 "Casa rodeada de árbores con vista á ría", "",
 "House among trees overlooking the estuary", "",
 "Casa rodeada de árvores com vista para a ria", "",
 "Maison entourée d'arbres avec vue sur la ria", ""),
"commons-74912150": (
 "Galicia (ría de Vigo)", "",
 "Galicia (ría de Vigo)", "",
 "Galicia (Vigo estuary)", "",
 "Galiza (ria de Vigo)", "",
 "Galice (ria de Vigo)", ""),
"commons-146489738": (
 "Ría de Vigo, 1923 (pintura)", "Óleo sobre lienzo de Arturo Fernández Cersa.",
 "Ría de Vigo, 1923 (pintura)", "Óleo sobre lenzo de Arturo Fernández Cersa.",
 "Vigo estuary, 1923 (painting)", "Oil on canvas by Arturo Fernández Cersa.",
 "Ria de Vigo, 1923 (pintura)", "Óleo sobre tela de Arturo Fernández Cersa.",
 "Ria de Vigo, 1923 (peinture)", "Huile sur toile d'Arturo Fernández Cersa."),
"commons-77841555": (
 "Una embarcación en la ría y árboles en la costa", "",
 "Unha embarcación na ría e árbores na costa", "",
 "A boat in the estuary and trees on the shore", "",
 "Uma embarcação na ria e árvores na costa", "",
 "Une embarcation dans la ria et des arbres sur la côte", ""),
"commons-77843474": (
 "Barco en la ría", "",
 "Barco na ría", "",
 "Ship in the estuary", "",
 "Navio na ria", "",
 "Navire dans la ria", ""),
"commons-158104472": (
 "El SMS Hansa y el RMS Dunottar Castle, 1909", "Los dos buques en la ría de Vigo.",
 "O SMS Hansa e o RMS Dunottar Castle, 1909", "Os dous buques na ría de Vigo.",
 "SMS Hansa and RMS Dunottar Castle, 1909", "The two ships in the Vigo estuary.",
 "O SMS Hansa e o RMS Dunottar Castle, 1909", "Os dois navios na ria de Vigo.",
 "Le SMS Hansa et le RMS Dunottar Castle, 1909", "Les deux navires dans la ria de Vigo."),
"commons-68547626": (
 "El vapor De Lasalle visto desde el Highland Chieftain", "",
 "O vapor De Lasalle visto dende o Highland Chieftain", "",
 "The steamer De Lasalle seen from the Highland Chieftain", "",
 "O vapor De Lasalle visto do Highland Chieftain", "",
 "Le vapeur De Lasalle vu depuis le Highland Chieftain", ""),
"commons-65407623": (
 "Recogiendo algas (ilustración)", "Ilustración de Serafín Avendaño en Blanco y Negro, 1906.",
 "Recollendo algas (ilustración)", "Ilustración de Serafín Avendaño en Blanco y Negro, 1906.",
 "Gathering seaweed (illustration)", "Illustration by Serafín Avendaño in Blanco y Negro, 1906.",
 "Apanhando algas (ilustração)", "Ilustração de Serafín Avendaño em Blanco y Negro, 1906.",
 "Ramassage d'algues (illustration)", "Illustration de Serafín Avendaño dans Blanco y Negro, 1906."),
"commons-70045502": (
 "Escollera de Bouzas (ilustración)", "Ilustración de Serafín Avendaño en Blanco y Negro, 1907.",
 "Escolleira de Bouzas (ilustración)", "Ilustración de Serafín Avendaño en Blanco y Negro, 1907.",
 "Bouzas breakwater (illustration)", "Illustration by Serafín Avendaño in Blanco y Negro, 1907.",
 "Molhe de Bouzas (ilustração)", "Ilustração de Serafín Avendaño em Blanco y Negro, 1907.",
 "Digue de Bouzas (illustration)", "Illustration de Serafín Avendaño dans Blanco y Negro, 1907."),
"commons-141855010": (
 "El equipo de fútbol de Vigo, 1909", "Fotografía de Cifuentes publicada en Blanco y Negro.",
 "O equipo de fútbol de Vigo, 1909", "Fotografía de Cifuentes publicada en Blanco y Negro.",
 "Vigo football team, 1909", "Photograph by Cifuentes published in Blanco y Negro.",
 "A equipa de futebol de Vigo, 1909", "Fotografia de Cifuentes publicada em Blanco y Negro.",
 "L'équipe de football de Vigo, 1909", "Photographie de Cifuentes publiée dans Blanco y Negro."),
"commons-57829083": (
 "Mitin de Falange en el teatro Tamberlik, 1936", "Intervención de Manuel Castro Prena el 27 de diciembre de 1936. Publicada en Vida Gallega.",
 "Mitin de Falange no teatro Tamberlik, 1936", "Intervención de Manuel Castro Prena o 27 de decembro de 1936. Publicada en Vida Gallega.",
 "Falange rally at the Tamberlik theatre, 1936", "Speech by Manuel Castro Prena on 27 December 1936. Published in Vida Gallega.",
 "Comício da Falange no teatro Tamberlik, 1936", "Intervenção de Manuel Castro Prena em 27 de dezembro de 1936. Publicada em Vida Gallega.",
 "Meeting de la Phalange au théâtre Tamberlik, 1936", "Discours de Manuel Castro Prena le 27 décembre 1936. Publié dans Vida Gallega."),
"commons-57829339": (
 "Jesús Suevos en el teatro Tamberlik, 1936", "Mitin de Falange del 27 de diciembre de 1936. Publicada en Vida Gallega.",
 "Jesús Suevos no teatro Tamberlik, 1936", "Mitin de Falange do 27 de decembro de 1936. Publicada en Vida Gallega.",
 "Jesús Suevos at the Tamberlik theatre, 1936", "Falange rally on 27 December 1936. Published in Vida Gallega.",
 "Jesús Suevos no teatro Tamberlik, 1936", "Comício da Falange de 27 de dezembro de 1936. Publicada em Vida Gallega.",
 "Jesús Suevos au théâtre Tamberlik, 1936", "Meeting de la Phalange du 27 décembre 1936. Publié dans Vida Gallega."),
"commons-112220461": (
 "Recibimiento a Gumersindo Busto, 1909", "Gumersindo Busto con los directores de El Noticiero de Vigo y La Voz de Vigo al desembarcar de América.",
 "Recibimento a Gumersindo Busto, 1909", "Gumersindo Busto cos directores de El Noticiero de Vigo e La Voz de Vigo ao desembarcar de América.",
 "Welcome for Gumersindo Busto, 1909", "Gumersindo Busto with the editors of El Noticiero de Vigo and La Voz de Vigo on landing from America.",
 "Receção a Gumersindo Busto, 1909", "Gumersindo Busto com os diretores de El Noticiero de Vigo e La Voz de Vigo ao desembarcar da América.",
 "Accueil de Gumersindo Busto, 1909", "Gumersindo Busto avec les directeurs d'El Noticiero de Vigo et de La Voz de Vigo à son retour d'Amérique."),
"commons-157226212": (
 "Entrada del teatro Rosalía, 1908", "Mitin del Partido Liberal el 8 de diciembre de 1908. Publicada en Vida Gallega.",
 "Entrada do teatro Rosalía, 1908", "Mitin do Partido Liberal o 8 de decembro de 1908. Publicada en Vida Gallega.",
 "Entrance to the Rosalía theatre, 1908", "Liberal Party rally on 8 December 1908. Published in Vida Gallega.",
 "Entrada do teatro Rosalía, 1908", "Comício do Partido Liberal em 8 de dezembro de 1908. Publicada em Vida Gallega.",
 "Entrée du théâtre Rosalía, 1908", "Meeting du Parti libéral le 8 décembre 1908. Publié dans Vida Gallega."),
"commons-157227895": (
 "El Vigo Foot-ball Club, 1909", "Publicada en Vida Gallega.",
 "O Vigo Foot-ball Club, 1909", "Publicada en Vida Gallega.",
 "Vigo Foot-ball Club, 1909", "Published in Vida Gallega.",
 "O Vigo Foot-ball Club, 1909", "Publicada em Vida Gallega.",
 "Le Vigo Foot-ball Club, 1909", "Publiée dans Vida Gallega."),
"commons-157536293": (
 "El Real Club Fortuna, 1908", "El equipo de fútbol en agosto de 1908. Publicada en Vida Gallega.",
 "O Real Club Fortuna, 1908", "O equipo de fútbol en agosto de 1908. Publicada en Vida Gallega.",
 "Real Club Fortuna, 1908", "The football team in August 1908. Published in Vida Gallega.",
 "O Real Club Fortuna, 1908", "A equipa de futebol em agosto de 1908. Publicada em Vida Gallega.",
 "Le Real Club Fortuna, 1908", "L'équipe de football en août 1908. Publiée dans Vida Gallega."),
"commons-157537288": (
 "Comida en el Hotel Universal, 1909", "Jugadores del Real Club Fortuna y del FC Porto comen juntos en Vigo. Publicada en Vida Gallega.",
 "Xantar no Hotel Universal, 1909", "Xogadores do Real Club Fortuna e do FC Porto comen xuntos en Vigo. Publicada en Vida Gallega.",
 "Lunch at the Hotel Universal, 1909", "Players from Real Club Fortuna and FC Porto eat together in Vigo. Published in Vida Gallega.",
 "Almoço no Hotel Universal, 1909", "Jogadores do Real Club Fortuna e do FC Porto almoçam juntos em Vigo. Publicada em Vida Gallega.",
 "Repas à l'Hôtel Universal, 1909", "Des joueurs du Real Club Fortuna et du FC Porto déjeunent ensemble à Vigo. Publiée dans Vida Gallega."),
"commons-157554943": (
 "Partido en el campo de Bouzas, 1909", "Encuentro amistoso entre el Real Club Fortuna y el Galicia FC. Publicada en Vida Gallega.",
 "Partido no campo de Bouzas, 1909", "Encontro amigable entre o Real Club Fortuna e o Galicia FC. Publicada en Vida Gallega.",
 "Match at the Bouzas ground, 1909", "Friendly between Real Club Fortuna and Galicia FC. Published in Vida Gallega.",
 "Jogo no campo de Bouzas, 1909", "Encontro amigável entre o Real Club Fortuna e o Galicia FC. Publicada em Vida Gallega.",
 "Match au terrain de Bouzas, 1909", "Rencontre amicale entre le Real Club Fortuna et le Galicia FC. Publiée dans Vida Gallega."),
"commons-157805155": (
 "El primer tobogán de Galicia, 1909", "Publicada en Vida Gallega.",
 "O primeiro tobogán de Galicia, 1909", "Publicada en Vida Gallega.",
 "Galicia's first toboggan slide, 1909", "Published in Vida Gallega.",
 "O primeiro tobogã da Galiza, 1909", "Publicada em Vida Gallega.",
 "Le premier toboggan de Galice, 1909", "Publiée dans Vida Gallega."),
"commons-158008149": (
 "Homenaje fúnebre a José García Barbón, 1909", "Acto en la Porta do Sol en marzo de 1909. Publicada en Vida Gallega.",
 "Homenaxe fúnebre a Xosé García Barbón, 1909", "Acto na Porta do Sol en marzo de 1909. Publicada en Vida Gallega.",
 "Funeral tribute to José García Barbón, 1909", "Ceremony at Porta do Sol in March 1909. Published in Vida Gallega.",
 "Homenagem fúnebre a José García Barbón, 1909", "Ato na Porta do Sol em março de 1909. Publicada em Vida Gallega.",
 "Hommage funèbre à José García Barbón, 1909", "Cérémonie à la Porta do Sol en mars 1909. Publiée dans Vida Gallega."),
"commons-158008650": (
 "Emilia Pardo Bazán en el Pazo da Pastora, 1909", "La escritora durante su visita a Vigo. Publicada en Vida Gallega.",
 "Emilia Pardo Bazán no Pazo da Pastora, 1909", "A escritora durante a súa visita a Vigo. Publicada en Vida Gallega.",
 "Emilia Pardo Bazán at the Pazo da Pastora, 1909", "The writer during her visit to Vigo. Published in Vida Gallega.",
 "Emilia Pardo Bazán no Pazo da Pastora, 1909", "A escritora durante a sua visita a Vigo. Publicada em Vida Gallega.",
 "Emilia Pardo Bazán au Pazo da Pastora, 1909", "L'écrivaine lors de sa visite à Vigo. Publiée dans Vida Gallega."),
"commons-158008651": (
 "Emilia Pardo Bazán en el Pazo da Pastora, 1909 (II)", "La escritora durante su visita a Vigo. Publicada en Vida Gallega.",
 "Emilia Pardo Bazán no Pazo da Pastora, 1909 (II)", "A escritora durante a súa visita a Vigo. Publicada en Vida Gallega.",
 "Emilia Pardo Bazán at the Pazo da Pastora, 1909 (II)", "The writer during her visit to Vigo. Published in Vida Gallega.",
 "Emilia Pardo Bazán no Pazo da Pastora, 1909 (II)", "A escritora durante a sua visita a Vigo. Publicada em Vida Gallega.",
 "Emilia Pardo Bazán au Pazo da Pastora, 1909 (II)", "L'écrivaine lors de sa visite à Vigo. Publiée dans Vida Gallega."),
"commons-158008652": (
 "Emilia Pardo Bazán en el Pazo da Pastora, 1909 (III)", "La escritora durante su visita a Vigo. Publicada en Vida Gallega.",
 "Emilia Pardo Bazán no Pazo da Pastora, 1909 (III)", "A escritora durante a súa visita a Vigo. Publicada en Vida Gallega.",
 "Emilia Pardo Bazán at the Pazo da Pastora, 1909 (III)", "The writer during her visit to Vigo. Published in Vida Gallega.",
 "Emilia Pardo Bazán no Pazo da Pastora, 1909 (III)", "A escritora durante a sua visita a Vigo. Publicada em Vida Gallega.",
 "Emilia Pardo Bazán au Pazo da Pastora, 1909 (III)", "L'écrivaine lors de sa visite à Vigo. Publiée dans Vida Gallega."),
"commons-31867629": (
 "El Vigo Foot Ball Club, 1912", "Primer equipo del club en septiembre de 1912, antecedente lejano del Celta de Vigo.",
 "O Vigo Foot Ball Club, 1912", "Primeiro equipo do club en setembro de 1912, antecedente afastado do Celta de Vigo.",
 "Vigo Foot Ball Club, 1912", "The club's first team in September 1912, a distant forerunner of Celta de Vigo.",
 "O Vigo Foot Ball Club, 1912", "Primeira equipa do clube em setembro de 1912, antecessora longínqua do Celta de Vigo.",
 "Le Vigo Foot Ball Club, 1912", "Première équipe du club en septembre 1912, lointain ancêtre du Celta de Vigo."),
"commons-151618980": (
 "Monumento a los repatriados (escultura)", "Obra de Julio González Pola, publicada en la revista La Esfera, 1929.",
 "Monumento aos repatriados (escultura)", "Obra de Julio González Pola, publicada na revista La Esfera, 1929.",
 "Monument to the repatriated (sculpture)", "Work by Julio González Pola, published in La Esfera magazine, 1929.",
 "Monumento aos repatriados (escultura)", "Obra de Julio González Pola, publicada na revista La Esfera, 1929.",
 "Monument aux rapatriés (sculpture)", "Œuvre de Julio González Pola, publiée dans la revue La Esfera, 1929."),
"commons-bakhuizen-rande": (
 "La batalla de Rande, 1702 (pintura)", "Óleo de Ludolf Bakhuizen sobre la batalla naval en el estrecho de Rande. Rijksmuseum, Ámsterdam.",
 "A batalla de Rande, 1702 (pintura)", "Óleo de Ludolf Bakhuizen sobre a batalla naval no estreito de Rande. Rijksmuseum, Ámsterdam.",
 "The Battle of Vigo Bay, 1702 (painting)", "Oil painting by Ludolf Bakhuizen of the naval battle in the Rande strait. Rijksmuseum, Amsterdam.",
 "A batalha de Rande, 1702 (pintura)", "Óleo de Ludolf Bakhuizen sobre a batalha naval no estreito de Rande. Rijksmuseum, Amesterdão.",
 "La bataille de Rande, 1702 (peinture)", "Huile de Ludolf Bakhuizen sur la bataille navale dans le détroit de Rande. Rijksmuseum, Amsterdam."),
"commons-7163837": (
 "Vendimia en Vigo (pintura)", "Óleo de Aureliano de Beruete, 1912.",
 "Vendima en Vigo (pintura)", "Óleo de Aureliano de Beruete, 1912.",
 "Grape harvest in Vigo (painting)", "Oil painting by Aureliano de Beruete, 1912.",
 "Vindima em Vigo (pintura)", "Óleo de Aureliano de Beruete, 1912.",
 "Vendanges à Vigo (peinture)", "Huile d'Aureliano de Beruete, 1912."),
"commons-47599451": (
 "El Exiles English Club de Vigo, 1903", "Equipo de fútbol de la colonia británica en Vigo.",
 "O Exiles English Club de Vigo, 1903", "Equipo de fútbol da colonia británica en Vigo.",
 "Exiles English Club of Vigo, 1903", "Football team of the British community in Vigo.",
 "O Exiles English Club de Vigo, 1903", "Equipa de futebol da colónia britânica em Vigo.",
 "L'Exiles English Club de Vigo, 1903", "Équipe de football de la colonie britannique de Vigo."),
"commons-47738432": (
 "Vista de Vigo, 1843 (grabado)", "Grabado de John Harrison Allan para «A Pictorial Tour in the Mediterranean».",
 "Vista de Vigo, 1843 (gravado)", "Gravado de John Harrison Allan para «A Pictorial Tour in the Mediterranean».",
 "View of Vigo, 1843 (engraving)", "Engraving by John Harrison Allan for \"A Pictorial Tour in the Mediterranean\".",
 "Vista de Vigo, 1843 (gravura)", "Gravura de John Harrison Allan para «A Pictorial Tour in the Mediterranean».",
 "Vue de Vigo, 1843 (gravure)", "Gravure de John Harrison Allan pour « A Pictorial Tour in the Mediterranean »."),
"commons-57430181": (
 "La playa de Samil", "Fotografía entre 1920 y 1940. Colección Seoane Prado.",
 "A praia de Samil", "Fotografía entre 1920 e 1940. Colección Seoane Prado.",
 "Samil beach", "Photograph from between 1920 and 1940. Seoane Prado Collection.",
 "A praia de Samil", "Fotografia entre 1920 e 1940. Coleção Seoane Prado.",
 "La plage de Samil", "Photographie prise entre 1920 et 1940. Collection Seoane Prado."),
"commons-89507795": (
 "La selección española antes del partido contra Hungría, 1926", "Partido amistoso jugado en Vigo el 19 de diciembre de 1926.",
 "A selección española antes do partido contra Hungría, 1926", "Partido amigable xogado en Vigo o 19 de decembro de 1926.",
 "Spain's national team before the match against Hungary, 1926", "Friendly played in Vigo on 19 December 1926.",
 "A seleção espanhola antes do jogo contra a Hungria, 1926", "Jogo amigável disputado em Vigo a 19 de dezembro de 1926.",
 "L'équipe d'Espagne avant le match contre la Hongrie, 1926", "Match amical joué à Vigo le 19 décembre 1926."),
"commons-127469766": (
 "Primer partido del Celta de Vigo, 1923", "Alineación del Celta en su debut, el 23 de septiembre de 1923, contra el Boavista de Oporto (1-8).",
 "Primeiro partido do Celta de Vigo, 1923", "Aliñación do Celta no seu debut, o 23 de setembro de 1923, fronte ao Boavista do Porto (1-8).",
 "Celta de Vigo's first match, 1923", "Celta's line-up for its debut on 23 September 1923 against Boavista of Porto (1-8).",
 "Primeiro jogo do Celta de Vigo, 1923", "Onze do Celta na estreia, a 23 de setembro de 1923, contra o Boavista do Porto (1-8).",
 "Premier match du Celta de Vigo, 1923", "Composition du Celta lors de ses débuts, le 23 septembre 1923, contre le Boavista de Porto (1-8)."),
"commons-35955954": (
 "El campo de Coia", "Primer estadio del Celta de Vigo, en uso entre 1908 y 1923, conocido como «La Catedral».",
 "O campo de Coia", "Primeiro estadio do Celta de Vigo, en uso entre 1908 e 1923, coñecido como «A Catedral».",
 "The Coia ground", "Celta de Vigo's first stadium, in use from 1908 to 1923, known as \"The Cathedral\".",
 "O campo de Coia", "Primeiro estádio do Celta de Vigo, usado entre 1908 e 1923, conhecido como «A Catedral».",
 "Le terrain de Coia", "Premier stade du Celta de Vigo, utilisé de 1908 à 1923, surnommé « la Cathédrale »."),
"commons-7901789": (
 "Venta del pescado en la playa de Vigo (pintura)", "Óleo de Francisco Pradilla, 1916.",
 "Venda do peixe na praia de Vigo (pintura)", "Óleo de Francisco Pradilla, 1916.",
 "Selling fish on the beach in Vigo (painting)", "Oil painting by Francisco Pradilla, 1916.",
 "Venda do peixe na praia de Vigo (pintura)", "Óleo de Francisco Pradilla, 1916.",
 "Vente du poisson sur la plage de Vigo (peinture)", "Huile de Francisco Pradilla, 1916."),
"commons-78260812": (
 "Vigo visto desde el mar", "Fotografía de Lluís Marià Vidal i Carreras, hacia 1880.",
 "Vigo visto dende o mar", "Fotografía de Lluís Marià Vidal i Carreras, cara a 1880.",
 "Vigo seen from the sea", "Photograph by Lluís Marià Vidal i Carreras, c. 1880.",
 "Vigo visto do mar", "Fotografia de Lluís Marià Vidal i Carreras, c. 1880.",
 "Vigo vu de la mer", "Photographie de Lluís Marià Vidal i Carreras, vers 1880."),
"commons-127871363": (
 "Barcos en la costa de la bahía de Vigo (pintura)", "Obra de Benjamin Olsen, 1923.",
 "Barcos na costa da baía de Vigo (pintura)", "Obra de Benjamin Olsen, 1923.",
 "Boats along the coast of Vigo Bay (painting)", "Work by Benjamin Olsen, 1923.",
 "Barcos na costa da baía de Vigo (pintura)", "Obra de Benjamin Olsen, 1923.",
 "Bateaux sur la côte de la baie de Vigo (peinture)", "Œuvre de Benjamin Olsen, 1923."),
"commons-141825088": (
 "La Ribeira de San Francisco, 1867 (grabado)", "Grabado de la «Crónica de la provincia de Pontevedra», de Fernando Fulgosio.",
 "A Ribeira de San Francisco, 1867 (gravado)", "Gravado da «Crónica de la provincia de Pontevedra», de Fernando Fulgosio.",
 "Ribeira de San Francisco, 1867 (engraving)", "Engraving from Fernando Fulgosio's \"Crónica de la provincia de Pontevedra\".",
 "A Ribeira de San Francisco, 1867 (gravura)", "Gravura da «Crónica de la provincia de Pontevedra», de Fernando Fulgosio.",
 "La Ribeira de San Francisco, 1867 (gravure)", "Gravure de la « Crónica de la provincia de Pontevedra » de Fernando Fulgosio."),
"commons-139108220": (
 "Derrota de la escuadra de Don Miguel frente a Vigo, 1833 (grabado)", "Grabado inglés sobre la batalla naval de la guerra civil portuguesa.",
 "Derrota da escuadra de Don Miguel fronte a Vigo, 1833 (gravado)", "Gravado inglés sobre a batalla naval da guerra civil portuguesa.",
 "Defeat of Dom Miguel's squadron off Vigo, 1833 (engraving)", "English engraving of the naval battle in the Portuguese Civil War.",
 "Derrota da esquadra de D. Miguel ao largo de Vigo, 1833 (gravura)", "Gravura inglesa sobre a batalha naval da guerra civil portuguesa.",
 "Défaite de l'escadre de Dom Miguel au large de Vigo, 1833 (gravure)", "Gravure anglaise de la bataille navale de la guerre civile portugaise."),
"commons-176352021": (
 "Mercado del Berbés (pintura)", "Obra de Enrique Simonet, hacia 1905.",
 "Mercado do Berbés (pintura)", "Obra de Enrique Simonet, cara a 1905.",
 "Berbés market (painting)", "Work by Enrique Simonet, c. 1905.",
 "Mercado do Berbés (pintura)", "Obra de Enrique Simonet, c. 1905.",
 "Marché du Berbés (peinture)", "Œuvre d'Enrique Simonet, vers 1905."),
"commons-51087895": (
 "Naufragio del Highland Pride, 1929", "El vapor de pasajeros y carga de la Nelson Line, encallado cerca de Vigo.",
 "Naufraxio do Highland Pride, 1929", "O vapor de pasaxeiros e carga da Nelson Line, encallado preto de Vigo.",
 "Wreck of the Highland Pride, 1929", "The Nelson Line passenger and cargo steamer, aground near Vigo.",
 "Naufrágio do Highland Pride, 1929", "O vapor de passageiros e carga da Nelson Line, encalhado perto de Vigo.",
 "Naufrage du Highland Pride, 1929", "Le vapeur de passagers et de fret de la Nelson Line, échoué près de Vigo."),
}

# Ubicaciones corregidas a mano (el importador las había asignado por palabras sueltas)
CENTRO = (42.23700, -8.72150)
UBICACIONES = {
    "commons-67820290": ("Vigo (sin ubicar)", *CENTRO, "sin_confirmar"),      # retrato: "Castro" era un apellido
    "commons-76835209": ("Vigo (sin ubicar)", *CENTRO, "sin_confirmar"),      # Lorca tras una conferencia: lugar no consta
    "commons-170563804": ("Castelo de San Sebastián", 42.23800, -8.72330, "aproximada"),
    "commons-195628024": ("Casa Bárcena", 42.23770, -8.71880, "aproximada"),
    "commons-195630584": ("Casa Bárcena", 42.23770, -8.71880, "aproximada"),
    "commons-57430182": ("Real Club Náutico", 42.24050, -8.72300, "aproximada"),
    "commons-196084836": ("O Calvario", 42.22700, -8.70500, "aproximada"),
    "commons-76844617": ("Vigo (sin ubicar)", *CENTRO, "sin_confirmar"),
    # Flickr Commons y dominio público (importación de octubre de 2026)
    "commons-7163837": ("Vigo (sin ubicar)", *CENTRO, "sin_confirmar"),
    "commons-47599451": ("Vigo (sin ubicar)", *CENTRO, "sin_confirmar"),
    "commons-47738432": ("Ría de Vigo", 42.24900, -8.74300, "sin_confirmar"),
    "commons-57430181": ("Praia de Samil", 42.21050, -8.77450, "aproximada"),
    "commons-89507795": ("Campo de Coia", 42.22500, -8.74000, "aproximada"),
    "commons-127469766": ("Campo de Coia", 42.22500, -8.74000, "aproximada"),
    "commons-35955954": ("Campo de Coia", 42.22500, -8.74000, "aproximada"),
    "commons-7901789": ("O Berbés", 42.23880, -8.72640, "sin_confirmar"),
    "commons-78260812": ("Ría de Vigo", 42.24900, -8.74300, "sin_confirmar"),
    "commons-127871363": ("Ría de Vigo", 42.24900, -8.74300, "sin_confirmar"),
    "commons-141825088": ("Ribeira de San Francisco", 42.23930, -8.72700, "aproximada"),
    "commons-139108220": ("Ría de Vigo", 42.24900, -8.74300, "sin_confirmar"),
    "commons-176352021": ("O Berbés", 42.23880, -8.72640, "aproximada"),
    "commons-51087895": ("Ría de Vigo", 42.24900, -8.74300, "sin_confirmar"),
    # Revistas ilustradas (importación de octubre de 2026)
    "commons-65407623": ("Ría de Vigo", 42.24900, -8.74300, "sin_confirmar"),
    "commons-57829083": ("Teatro Tamberlik", 42.23720, -8.72050, "sin_confirmar"),  # "Castro" era un apellido
    "commons-57829339": ("Teatro Tamberlik", 42.23720, -8.72050, "sin_confirmar"),
    "commons-112220461": ("Puerto de Vigo", 42.24250, -8.72400, "sin_confirmar"),
    "commons-157226212": ("Teatro Rosalía", 42.23660, -8.72120, "sin_confirmar"),
    "commons-158008650": ("Vigo (sin ubicar)", *CENTRO, "sin_confirmar"),
    "commons-158008651": ("Vigo (sin ubicar)", *CENTRO, "sin_confirmar"),
    "commons-158008652": ("Vigo (sin ubicar)", *CENTRO, "sin_confirmar"),
}

LENGUAS = ["es", "gl", "en", "pt", "fr"]


def main():
    ruta = Path(__file__).resolve().parent.parent / "data" / "fotos.json"
    datos = json.loads(ruta.read_text(encoding="utf-8"))
    sin = []
    for f in datos["fotos"]:
        if f["id"] in UBICACIONES:
            lugar, lat, lng, ub = UBICACIONES[f["id"]]
            f.update(lugar=lugar, lat=lat, lng=lng, ubicacion=ub)
        t = T.get(f["id"])
        if not t:
            if not f.get("textos"):  # las postales de Galiciana traen sus textos de scripts/postales_galiciana.py
                sin.append(f["id"])
            continue
        f["textos"] = {l: {"titulo": t[2 * i], "descripcion": t[2 * i + 1]} for i, l in enumerate(LENGUAS)}
        # Los textos en español sustituyen a los originales mezclados
        f["titulo"], f["descripcion"] = t[0], t[1]
        f.pop("fecha", None)
    ruta.write_text(json.dumps(datos, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"Textos aplicados a {len(datos['fotos']) - len(sin)} fotos.")
    if sin:
        print("Sin traducir:", ", ".join(sin))


if __name__ == "__main__":
    main()
