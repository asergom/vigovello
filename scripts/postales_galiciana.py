#!/usr/bin/env python3
"""
Incorpora las postales de Vigo de Galiciana (Biblioteca Dixital de Galicia),
localizadas a través de Europeana, a data/fotos.json con sus textos en los
cinco idiomas de la web.

    python3 scripts/postales_galiciana.py RESULTADO_EUROPEANA.json

Galiciana las publica con la marca de dominio público (Public Domain Mark).
"""
import json
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
FOTOS = RAIZ / "data" / "fotos.json"

# --- Lugares: nombre, lat, lng, estado de la ubicación ---
SU = "sin_confirmar"
AP = "aproximada"
L = {
    "centro": ("Vigo (sin ubicar)", 42.23700, -8.72150, SU),
    "ria": ("Ría de Vigo", 42.24900, -8.74300, SU),
    "puerto": ("Puerto de Vigo", 42.24250, -8.72400, AP),
    "puerto?": ("Puerto de Vigo", 42.24250, -8.72400, SU),
    "comercio": ("Muelle del Comercio", 42.24120, -8.72320, AP),
    "maritima": ("Muelle de Trasatlánticos", 42.24100, -8.72350, AP),
    "berbes": ("O Berbés", 42.23880, -8.72640, AP),
    "berbes?": ("O Berbés", 42.23880, -8.72640, SU),
    "castro": ("Monte do Castro", 42.23350, -8.72450, AP),
    "desdecastro": ("Vista general desde el Castro", 42.23360, -8.72330, AP),
    "alameda": ("Alameda (Praza de Compostela)", 42.23955, -8.72230, AP),
    "elduayen_x": ("Xardíns de Elduayen", 42.24000, -8.72200, AP),
    "sol": ("Porta do Sol", 42.23700, -8.72300, AP),
    "principe": ("Rúa do Príncipe", 42.23690, -8.72080, AP),
    "policarpo": ("Rúa de Policarpo Sanz", 42.23810, -8.72030, AP),
    "policarpo?": ("Rúa de Policarpo Sanz", 42.23810, -8.72030, SU),
    "colon": ("Rúa de Colón", 42.23620, -8.71780, AP),
    "elduayen": ("Rúa de Elduayen", 42.23720, -8.72420, AP),
    "velazquez": ("Rúa Velázquez Moreno", 42.23650, -8.71950, AP),
    "carral": ("Rúa de Carral", 42.23850, -8.72150, AP),
    "areal": ("O Areal", 42.24080, -8.71600, AP),
    "barbon": ("Teatro García Barbón", 42.23740, -8.71810, AP),
    "montero": ("Avenida de Montero Ríos", 42.24050, -8.72150, AP),
    "alfonso": ("Paseo de Alfonso XII", 42.23820, -8.72750, AP),
    "canovas": ("Rúa de Cánovas del Castillo", 42.23960, -8.72150, AP),
    "constitucion": ("Praza da Constitución", 42.23890, -8.72480, AP),
    "princesa": ("Praza da Princesa", 42.23930, -8.72580, AP),
    "colegiata": ("Concatedral de Santa María", 42.23930, -8.72530, AP),
    "espana": ("Praza de España", 42.22900, -8.71800, AP),
    "espana?": ("Praza de España", 42.22900, -8.71800, SU),
    "granvia": ("Gran Vía", 42.22950, -8.71700, AP),
    "samil": ("Praia de Samil", 42.21050, -8.77450, AP),
    "coia": ("Coia", 42.22700, -8.74200, AP),
    "bouzas": ("Bouzas", 42.23450, -8.75200, AP),
    "guixar": ("O Guixar", 42.24450, -8.70600, AP),
    "teis": ("Teis", 42.25100, -8.69500, AP),
    "guia": ("Monte da Guía", 42.25300, -8.69200, AP),
    "cies": ("Illas Cíes", 42.21800, -8.90500, AP),
    "toralla": ("Illa de Toralla", 42.20090, -8.79830, AP),
    "sansimon": ("Illa de San Simón", 42.30300, -8.63200, AP),
    "castrelos": ("Castrelos", 42.21400, -8.72300, AP),
    "nautico": ("Real Club Náutico", 42.24050, -8.72300, AP),
    "laxe": ("A Laxe", 42.23980, -8.72320, AP),
    "rosalia": ("Teatro Rosalía", 42.23660, -8.72120, SU),
    "moderno": ("Rúa de Policarpo Sanz", 42.23810, -8.72030, AP),
    "barcena": ("Casa Bárcena", 42.23770, -8.71880, AP),
    "caridad": ("Casa de Caridad", 42.23300, -8.71800, SU),
    "falperra": ("Praza da Falperra", 42.23400, -8.72150, AP),
    "deportes": ("Pavillón de As Travesas", 42.22450, -8.72900, AP),
}

# --- Textos: título limpio → (es, gl, en, pt, fr, lugar) ---
T = {
 "(Nocturna) Plaza de España, fuente luminosa": ("Plaza de España de noche, fuente luminosa", "Praza de España de noite, fonte luminosa", "Plaza de España at night, illuminated fountain", "Praça de Espanha à noite, fonte luminosa", "Place d'Espagne de nuit, fontaine lumineuse", "espana"),
 "(Nocturna) fuente y Restaurante El Castro": ("Fuente y restaurante El Castro de noche", "Fonte e restaurante O Castro de noite", "Fountain and El Castro restaurant at night", "Fonte e restaurante El Castro à noite", "Fontaine et restaurant El Castro de nuit", "castro"),
 "Al fondo las Islas Cíes": ("Atardecer con las islas Cíes al fondo", "Solpor coas illas Cíes ao fondo", "Sunset with the Cíes Islands in the distance", "Pôr do sol com as ilhas Cíes ao fundo", "Coucher de soleil avec les îles Cíes au fond", "ria"),
 "Alameda": ("La Alameda", "A Alameda", "The Alameda", "A Alameda", "L'Alameda", "alameda"),
 "Alameda, Estatua de Méndez Núñez": ("La Alameda y la estatua de Méndez Núñez", "A Alameda e a estatua de Méndez Núñez", "The Alameda and the statue of Méndez Núñez", "A Alameda e a estátua de Méndez Núñez", "L'Alameda et la statue de Méndez Núñez", "alameda"),
 "Alba en la Ría": ("Amanecer en la ría", "Alba na ría", "Dawn over the estuary", "Alvorada na ria", "Aube sur la ria", "ria"),
 "Aldeana": ("Aldeana", "Aldeá", "Village woman", "Aldeã", "Paysanne", "centro"),
 "Almanzora": ("El trasatlántico Almanzora", "O transatlántico Almanzora", "The ocean liner Almanzora", "O transatlântico Almanzora", "Le paquebot Almanzora", "puerto?"),
 "Alrededores de Vigo": ("Alrededores de Vigo", "Arredores de Vigo", "Outskirts of Vigo", "Arredores de Vigo", "Environs de Vigo", "centro"),
 "Alrrededores (sic)": ("Alrededores de Vigo", "Arredores de Vigo", "Outskirts of Vigo", "Arredores de Vigo", "Environs de Vigo", "centro"),
 "Avd. Samil, Polígono de Goya [Coia": ("Avenida de Samil y polígono de Coia", "Avenida de Samil e polígono de Coia", "Samil Avenue and the Coia estate", "Avenida de Samil e bairro de Coia", "Avenue de Samil et quartier de Coia", "coia"),
 "Avda. de la GranVía [sic": ("Avenida de la Gran Vía", "Avenida da Gran Vía", "Gran Vía Avenue", "Avenida da Gran Vía", "Avenue de la Gran Vía", "granvia"),
 "Avenida \"Policarpo Sanz\"": ("Avenida de Policarpo Sanz", "Avenida de Policarpo Sanz", "Policarpo Sanz Avenue", "Avenida de Policarpo Sanz", "Avenue Policarpo Sanz", "policarpo"),
 "Avenida Montero Ríos": ("Avenida de Montero Ríos", "Avenida de Montero Ríos", "Montero Ríos Avenue", "Avenida de Montero Ríos", "Avenue Montero Ríos", "montero"),
 "Avenida de Alfonso XII": ("Avenida de Alfonso XII", "Avenida de Afonso XII", "Alfonso XII Avenue", "Avenida de Afonso XII", "Avenue Alphonse XII", "alfonso"),
 "Avenida de Cánovas": ("Avenida de Cánovas del Castillo", "Avenida de Cánovas del Castillo", "Cánovas del Castillo Avenue", "Avenida de Cánovas del Castillo", "Avenue Cánovas del Castillo", "canovas"),
 "Avenida de García Barbón": ("Avenida de García Barbón", "Avenida de García Barbón", "García Barbón Avenue", "Avenida de García Barbón", "Avenue García Barbón", "barbon"),
 "Avenida de Montero Ríos": ("Avenida de Montero Ríos", "Avenida de Montero Ríos", "Montero Ríos Avenue", "Avenida de Montero Ríos", "Avenue Montero Ríos", "montero"),
 "Avenida de Policarpo Sanz": ("Avenida de Policarpo Sanz", "Avenida de Policarpo Sanz", "Policarpo Sanz Avenue", "Avenida de Policarpo Sanz", "Avenue Policarpo Sanz", "policarpo"),
 "Avenidas": ("Las avenidas", "As avenidas", "The avenues", "As avenidas", "Les avenues", "montero"),
 "Bahía de Guixar": ("Bahía del Guixar", "Baía do Guixar", "O Guixar bay", "Baía do Guixar", "Baie du Guixar", "guixar"),
 "Bahía y Muelle del Comercio": ("La bahía y el muelle del Comercio", "A baía e o peirao do Comercio", "The bay and the Comercio pier", "A baía e o cais do Comércio", "La baie et le quai du Commerce", "comercio"),
 "Baile del país": ("Baile popular", "Baile do país", "Traditional dance", "Baile popular", "Danse traditionnelle", "centro"),
 "Banco Pastor": ("Banco Pastor", "Banco Pastor", "Banco Pastor building", "Banco Pastor", "Banque Pastor", "policarpo?"),
 "Banco de España": ("Banco de España", "Banco de España", "Bank of Spain building", "Banco de Espanha", "Banque d'Espagne", "centro"),
 "Banco de España y pozo del puerto": ("Banco de España y dársena del puerto", "Banco de España e dársena do porto", "Bank of Spain and the harbour basin", "Banco de Espanha e doca do porto", "Banque d'Espagne et bassin du port", "puerto?"),
 "Banco de Vigo": ("Banco de Vigo", "Banco de Vigo", "Banco de Vigo building", "Banco de Vigo", "Banque de Vigo", "centro"),
 "Banco de Vigo-Escuela de Artes e Industrias": ("Banco de Vigo y Escuela de Artes e Industrias", "Banco de Vigo e Escola de Artes e Industrias", "Banco de Vigo and the School of Arts and Industries", "Banco de Vigo e Escola de Artes e Indústrias", "Banque de Vigo et École des arts et industries", "centro"),
 "Barrio del Regueiro": ("Barrio del Regueiro", "Barrio do Regueiro", "O Regueiro neighbourhood", "Bairro do Regueiro", "Quartier du Regueiro", "centro"),
 "Base naval": ("La base naval", "A base naval", "The naval base", "A base naval", "La base navale", "teis"),
 "Bouzas-Vigo. Vista general del Puerto": ("Bouzas, vista general del puerto", "Bouzas, vista xeral do porto", "Bouzas, general view of the harbour", "Bouzas, vista geral do porto", "Bouzas, vue générale du port", "bouzas"),
 "Café Méndez Núñez": ("Café Méndez Núñez", "Café Méndez Núñez", "Café Méndez Núñez", "Café Méndez Núñez", "Café Méndez Núñez", "centro"),
 "Calle Colón": ("Calle de Colón", "Rúa de Colón", "Colón Street", "Rua de Colón", "Rue Colón", "colon"),
 "Calle José Antonio": ("Calle José Antonio (hoy Urzaiz)", "Rúa José Antonio (hoxe Urzaiz)", "José Antonio Street (now Urzaiz)", "Rua José Antonio (hoje Urzaiz)", "Rue José Antonio (aujourd'hui Urzaiz)", "centro"),
 "Calle Policarpo Sanz": ("Calle de Policarpo Sanz", "Rúa de Policarpo Sanz", "Policarpo Sanz Street", "Rua de Policarpo Sanz", "Rue Policarpo Sanz", "policarpo"),
 "Calle Policarpo Sanz y Teatro Barbón": ("Calle de Policarpo Sanz y teatro García Barbón", "Rúa de Policarpo Sanz e teatro García Barbón", "Policarpo Sanz Street and García Barbón Theatre", "Rua de Policarpo Sanz e teatro García Barbón", "Rue Policarpo Sanz et théâtre García Barbón", "barbon"),
 "Calle de Carral": ("Calle de Carral", "Rúa de Carral", "Carral Street", "Rua de Carral", "Rue Carral", "carral"),
 "Calle de Colón": ("Calle de Colón", "Rúa de Colón", "Colón Street", "Rua de Colón", "Rue Colón", "colon"),
 "Calle de Elduayen": ("Calle de Elduayen", "Rúa de Elduayen", "Elduayen Street", "Rua de Elduayen", "Rue Elduayen", "elduayen"),
 "Calle de José Antonio": ("Calle José Antonio (hoy Urzaiz)", "Rúa José Antonio (hoxe Urzaiz)", "José Antonio Street (now Urzaiz)", "Rua José Antonio (hoje Urzaiz)", "Rue José Antonio (aujourd'hui Urzaiz)", "centro"),
 "Calle de Policarpo Sanz": ("Calle de Policarpo Sanz", "Rúa de Policarpo Sanz", "Policarpo Sanz Street", "Rua de Policarpo Sanz", "Rue Policarpo Sanz", "policarpo"),
 "Calle de Policarpo Sanz y Puerta del Sol": ("Calle de Policarpo Sanz y Porta do Sol", "Rúa de Policarpo Sanz e Porta do Sol", "Policarpo Sanz Street and Porta do Sol", "Rua de Policarpo Sanz e Porta do Sol", "Rue Policarpo Sanz et Porta do Sol", "sol"),
 "Calle de Velázquez Moreno": ("Calle de Velázquez Moreno", "Rúa de Velázquez Moreno", "Velázquez Moreno Street", "Rua de Velázquez Moreno", "Rue Velázquez Moreno", "velazquez"),
 "Calle del Arenal": ("Calle del Areal", "Rúa do Areal", "Areal Street", "Rua do Areal", "Rue de l'Areal", "areal"),
 "Calle del Príncipe": ("Calle del Príncipe", "Rúa do Príncipe", "Príncipe Street", "Rua do Príncipe", "Rue du Príncipe", "principe"),
 "Calle del Príncipe, lado del Gimnasio": ("Calle del Príncipe, junto al Gimnasio", "Rúa do Príncipe, xunto ao Ximnasio", "Príncipe Street by the Gymnasium", "Rua do Príncipe, junto ao Ginásio", "Rue du Príncipe, côté du Gymnase", "principe"),
 "Camping Islas Cíes": ("Camping de las islas Cíes", "Cámping das illas Cíes", "Campsite on the Cíes Islands", "Parque de campismo das ilhas Cíes", "Camping des îles Cíes", "cies"),
 "Canido (Vigo) : Isla de Toralla": ("Isla de Toralla, Canido", "Illa de Toralla, Canido", "Toralla Island, Canido", "Ilha de Toralla, Canido", "Île de Toralla, Canido", "toralla"),
 "Carro del Pais": ("Carro del país", "Carro do país", "Traditional ox cart", "Carro de bois tradicional", "Char à bœufs traditionnel", "centro"),
 "Casa Blanca": ("Casa Blanca", "Casa Branca", "Casa Blanca", "Casa Branca", "Casa Blanca", "centro"),
 "Casa Caridad": ("La Casa de Caridad", "A Casa de Caridade", "The Charity House", "A Casa de Caridade", "La Maison de charité", "caridad"),
 "Casa de Bárcena": ("Casa Bárcena", "Casa Bárcena", "Casa Bárcena", "Casa Bárcena", "Casa Bárcena", "barcena"),
 "Casa de viajeros": ("Casa de viajeros", "Casa de viaxeiros", "Travellers' inn", "Casa de hóspedes", "Maison de voyageurs", "centro"),
 "Casino de Vigo": ("Casino de Vigo", "Casino de Vigo", "Vigo Casino", "Casino de Vigo", "Casino de Vigo", "centro"),
 "Castillo del Castro": ("El castillo del Castro", "O castelo do Castro", "O Castro castle", "O castelo do Castro", "Le château du Castro", "castro"),
 "Catedral": ("Concatedral de Santa María: interior", "Concatedral de Santa María: interior", "Co-cathedral of Santa María: interior", "Concatedral de Santa María: interior", "Cocathédrale Santa María : intérieur", "colegiata"),
 "Club Náutico y piscina cubierta": ("Club Náutico y piscina cubierta", "Club Náutico e piscina cuberta", "Yacht club and indoor pool", "Clube Náutico e piscina coberta", "Club nautique et piscine couverte", "nautico"),
 "Continental Hôtel, Mercado de la Laje": ("Hotel Continental y mercado de A Laxe", "Hotel Continental e mercado da Laxe", "Hotel Continental and A Laxe market", "Hotel Continental e mercado da Laxe", "Hôtel Continental et marché d'A Laxe", "laxe"),
 "Crucero \"Navarra\" en el puerto": ("El crucero Navarra en el puerto", "O cruceiro Navarra no porto", "The cruiser Navarra in the port", "O cruzador Navarra no porto", "Le croiseur Navarra dans le port", "puerto?"),
 "Detalle del Castro": ("Detalle del Castro", "Detalle do Castro", "Detail of O Castro", "Pormenor do Castro", "Détail du Castro", "castro"),
 "Detalle del puerto": ("Detalle del puerto", "Detalle do porto", "Detail of the port", "Pormenor do porto", "Détail du port", "puerto?"),
 "Dársena del Real Club Náutico": ("Dársena del Real Club Náutico", "Dársena do Real Club Náutico", "Royal Yacht Club basin", "Doca do Real Clube Náutico", "Bassin du Real Club Náutico", "nautico"),
 "El Arenal": ("El Areal", "O Areal", "O Areal", "O Areal", "L'Areal", "areal"),
 "El Berbés": ("El Berbés", "O Berbés", "O Berbés", "O Berbés", "Le Berbés", "berbes"),
 "El Castro (Monumento a los Galeones de Rande)": ("El Castro y el monumento a los Galeones de Rande", "O Castro e o monumento aos Galeóns de Rande", "O Castro and the monument to the Rande galleons", "O Castro e o monumento aos Galeões de Rande", "Le Castro et le monument aux galions de Rande", "castro"),
 "El Espiñeiro": ("El Espiñeiro", "O Espiñeiro", "O Espiñeiro", "O Espiñeiro", "L'Espiñeiro", "centro"),
 "El Muelle": ("El muelle", "O peirao", "The pier", "O cais", "Le quai", "puerto"),
 "El mercado": ("El mercado", "O mercado", "The market", "O mercado", "Le marché", "centro"),
 "El puerto, fuente en la Alameda, monumento a los Caídos y plaza de España": ("El puerto, la Alameda, el monumento a los Caídos y la plaza de España", "O porto, a Alameda, o monumento aos Caídos e a praza de España", "The port, the Alameda, the war memorial and Plaza de España", "O porto, a Alameda, o monumento aos Caídos e a praça de Espanha", "Le port, l'Alameda, le monument aux morts et la place d'Espagne", "centro"),
 "Embarque en la Mala Real": ("Embarque en la Mala Real", "Embarque na Mala Real", "Boarding a Royal Mail liner", "Embarque na Mala Real", "Embarquement sur la Malle royale", "maritima"),
 "Escuadra Inglesa": ("La escuadra inglesa", "A escuadra inglesa", "The British squadron", "A esquadra inglesa", "L'escadre anglaise", "ria"),
 "Escuadras inglesas en el día del Santo de la Reina Victoria. Panorama parcial tráfico del Puerto. Panorama tomada desde el Castillo": ("Escuadras inglesas en el santo de la reina Victoria, vistas desde el castillo", "Escuadras inglesas no santo da raíña Vitoria, vistas dende o castelo", "British squadrons on Queen Victoria's name day, seen from the castle", "Esquadras inglesas no dia da rainha Vitória, vistas do castelo", "Escadres anglaises le jour de la fête de la reine Victoria, vues du château", "desdecastro"),
 "Escuela de Artes e Industrias de Vigo": ("Escuela de Artes e Industrias", "Escola de Artes e Industrias", "School of Arts and Industries", "Escola de Artes e Indústrias", "École des arts et industries", "centro"),
 "Escuela de Artes é Industrias": ("Escuela de Artes e Industrias", "Escola de Artes e Industrias", "School of Arts and Industries", "Escola de Artes e Indústrias", "École des arts et industries", "centro"),
 "Estación Marítima": ("La estación marítima", "A estación marítima", "The maritime station", "A estação marítima", "La gare maritime", "maritima"),
 "Estación marítima": ("La estación marítima", "A estación marítima", "The maritime station", "A estação marítima", "La gare maritime", "maritima"),
 "Estatua de Elduayen": ("Estatua de Elduayen", "Estatua de Elduayen", "Statue of Elduayen", "Estátua de Elduayen", "Statue d'Elduayen", "elduayen_x"),
 "Estatua de Méndez Núñez": ("Estatua de Méndez Núñez", "Estatua de Méndez Núñez", "Statue of Méndez Núñez", "Estátua de Méndez Núñez", "Statue de Méndez Núñez", "alameda"),
 "Faenas típicas de Galicia": ("Faenas típicas gallegas", "Faenas típicas galegas", "Traditional Galician work", "Trabalhos típicos galegos", "Travaux typiques de Galice", "centro"),
 "Fuente de la Falpena [sic": ("Fuente de la Falperra", "Fonte da Falperra", "Falperra fountain", "Fonte da Falperra", "Fontaine de la Falperra", "falperra"),
 "Grand Hotel Continental": ("Gran Hotel Continental", "Gran Hotel Continental", "Grand Hotel Continental", "Grande Hotel Continental", "Grand Hôtel Continental", "laxe"),
 "Grandes Hoteles Mogin. Vigo, Continental Hotel": ("Hotel Continental", "Hotel Continental", "Hotel Continental", "Hotel Continental", "Hôtel Continental", "laxe"),
 "Grupo de aldeanos": ("Grupo de aldeanos", "Grupo de aldeáns", "Group of villagers", "Grupo de aldeãos", "Groupe de paysans", "centro"),
 "Hotel Continental": ("Hotel Continental", "Hotel Continental", "Hotel Continental", "Hotel Continental", "Hôtel Continental", "laxe"),
 "Hotel Moderno, Bar Restaurant": ("Hotel Moderno, bar y restaurante", "Hotel Moderno, bar e restaurante", "Hotel Moderno, bar and restaurant", "Hotel Moderno, bar e restaurante", "Hôtel Moderno, bar et restaurant", "moderno"),
 "Hotel Universe, Vigo. Gran Hotel R. Universal": ("Gran Hotel Universal", "Gran Hotel Universal", "Grand Hotel Universal", "Grande Hotel Universal", "Grand Hôtel Universal", "laxe"),
 "Hoteles Universal y Continental": ("Hoteles Universal y Continental", "Hoteis Universal e Continental", "Hotels Universal and Continental", "Hotéis Universal e Continental", "Hôtels Universal et Continental", "laxe"),
 "Iglesia de San Pedro de Sardón": ("Iglesia de San Pedro de Sárdoma", "Igrexa de San Pedro de Sárdoma", "Church of San Pedro de Sárdoma", "Igreja de San Pedro de Sárdoma", "Église San Pedro de Sárdoma", "centro"),
 "Iglesia de Teis y Muelle de la Base Naval": ("Iglesia de Teis y muelle de la base naval", "Igrexa de Teis e peirao da base naval", "Teis church and the naval base pier", "Igreja de Teis e cais da base naval", "Église de Teis et quai de la base navale", "teis"),
 "Iglesia de Teis y muelle de la Base Naval": ("Iglesia de Teis y muelle de la base naval", "Igrexa de Teis e peirao da base naval", "Teis church and the naval base pier", "Igreja de Teis e cais da base naval", "Église de Teis et quai de la base navale", "teis"),
 "Isla de San Simón": ("Isla de San Simón", "Illa de San Simón", "San Simón Island", "Ilha de San Simón", "Île de San Simón", "sansimon"),
 "Islas Cíes": ("Islas Cíes", "Illas Cíes", "Cíes Islands", "Ilhas Cíes", "Îles Cíes", "cies"),
 "Islas Cíes, vista panorámica": ("Islas Cíes, vista panorámica", "Illas Cíes, vista panorámica", "Cíes Islands, panoramic view", "Ilhas Cíes, vista panorâmica", "Îles Cíes, vue panoramique", "cies"),
 "Islas Cíes. Ría de Vigo. Vista aérea": ("Islas Cíes, vista aérea", "Illas Cíes, vista aérea", "Cíes Islands, aerial view", "Ilhas Cíes, vista aérea", "Îles Cíes, vue aérienne", "cies"),
 "Jardines de Elduayen": ("Jardines de Elduayen", "Xardíns de Elduayen", "Elduayen Gardens", "Jardins de Elduayen", "Jardins d'Elduayen", "elduayen_x"),
 "Jardines de la Alameda": ("Jardines de la Alameda", "Xardíns da Alameda", "Alameda gardens", "Jardins da Alameda", "Jardins de l'Alameda", "alameda"),
 "Jardines de la Pza. de Compostela": ("Jardines de la plaza de Compostela", "Xardíns da praza de Compostela", "Plaza de Compostela gardens", "Jardins da praça de Compostela", "Jardins de la place de Compostela", "alameda"),
 "La Bahía con la Escuadra Inglesa": ("La bahía con la escuadra inglesa", "A baía coa escuadra inglesa", "The bay with the British squadron", "A baía com a esquadra inglesa", "La baie avec l'escadre anglaise", "ria"),
 "La Campiña desde el Castillo del Castro": ("El campo desde el castillo del Castro", "O campo dende o castelo do Castro", "The countryside from O Castro castle", "O campo visto do castelo do Castro", "La campagne depuis le château du Castro", "desdecastro"),
 "La Guía": ("Monte de la Guía", "Monte da Guía", "A Guía hill", "Monte da Guía", "Mont de la Guía", "guia"),
 "La Ribera": ("La Ribera", "A Ribeira", "The waterfront", "A Ribeira", "La Ribera", "berbes"),
 "La bahía": ("La bahía", "A baía", "The bay", "A baía", "La baie", "ria"),
 "La playa": ("La playa", "A praia", "The beach", "A praia", "La plage", "centro"),
 "Lavanderas en el Río de San Pedro": ("Lavanderas en el río de San Pedro", "Lavandeiras no río de San Pedro", "Washerwomen in the San Pedro river", "Lavadeiras no rio de San Pedro", "Lavandières dans la rivière San Pedro", "centro"),
 "Lazareto de San Simón": ("Lazareto de San Simón", "Lazareto de San Simón", "San Simón lazaretto", "Lazareto de San Simón", "Lazaret de San Simón", "sansimon"),
 "Llegada del pescado": ("Llegada del pescado", "Chegada do peixe", "The fish arrives", "Chegada do peixe", "Arrivée du poisson", "berbes?"),
 "Monte El Castro (vista aérea)": ("Monte del Castro, vista aérea", "Monte do Castro, vista aérea", "O Castro hill, aerial view", "Monte do Castro, vista aérea", "Mont du Castro, vue aérienne", "castro"),
 "Monte La Guía, en Teis": ("Monte de la Guía, en Teis", "Monte da Guía, en Teis", "A Guía hill, Teis", "Monte da Guía, em Teis", "Mont de la Guía, à Teis", "guia"),
 "Monumento a los Caídos (nocturna)": ("Monumento a los Caídos de noche", "Monumento aos Caídos de noite", "War memorial at night", "Monumento aos Caídos à noite", "Monument aux morts de nuit", "espana?"),
 "Monumento a los Galeones de Rande": ("Monumento a los Galeones de Rande", "Monumento aos Galeóns de Rande", "Monument to the Rande galleons", "Monumento aos Galeões de Rande", "Monument aux galions de Rande", "castro"),
 "Muelle Del Comercio": ("Muelle del Comercio", "Peirao do Comercio", "Comercio pier", "Cais do Comércio", "Quai du Commerce", "comercio"),
 "Muelle de Piedra": ("Muelle de Piedra", "Peirao de Pedra", "Stone pier", "Cais de Pedra", "Quai de pierre", "comercio"),
 "Muelle de piedra": ("Muelle de Piedra", "Peirao de Pedra", "Stone pier", "Cais de Pedra", "Quai de pierre", "comercio"),
 "Muelle del Comercio": ("Muelle del Comercio", "Peirao do Comercio", "Comercio pier", "Cais do Comércio", "Quai du Commerce", "comercio"),
 "Muelle y estatua de Elduayen": ("Muelle y estatua de Elduayen", "Peirao e estatua de Elduayen", "Pier and statue of Elduayen", "Cais e estátua de Elduayen", "Quai et statue d'Elduayen", "elduayen_x"),
 "Museo y Palacio Municipal de Castrelos": ("Museo y pazo municipal de Castrelos", "Museo e pazo municipal de Castrelos", "Castrelos manor house and museum", "Museu e paço municipal de Castrelos", "Musée et manoir municipal de Castrelos", "castrelos"),
 "Palacio Castrelos (jardines)": ("Jardines del pazo de Castrelos", "Xardíns do pazo de Castrelos", "Castrelos manor gardens", "Jardins do paço de Castrelos", "Jardins du manoir de Castrelos", "castrelos"),
 "Palacio Municipal de Deportes": ("Palacio Municipal de Deportes", "Pazo Municipal dos Deportes", "Municipal Sports Hall", "Pavilhão Municipal de Desportos", "Palais municipal des sports", "deportes"),
 "Palacio de Castrelos": ("Pazo de Castrelos", "Pazo de Castrelos", "Castrelos manor house", "Paço de Castrelos", "Manoir de Castrelos", "castrelos"),
 "Palacio de Santhomé. Jardín del Conde": ("Pazo de Santhomé: jardín del conde", "Pazo de Santhomé: xardín do conde", "Santhomé manor: the count's garden", "Paço de Santhomé: jardim do conde", "Manoir de Santhomé : jardin du comte", "centro"),
 "Palacio de Santhomé. Salón central": ("Pazo de Santhomé: salón central", "Pazo de Santhomé: salón central", "Santhomé manor: main hall", "Paço de Santhomé: salão central", "Manoir de Santhomé : salon central", "centro"),
 "Panorama desde la Guía": ("Panorama desde el monte de la Guía", "Panorama dende o monte da Guía", "Panorama from A Guía hill", "Panorama do monte da Guía", "Panorama depuis le mont de la Guía", "guia"),
 "Paseo del Arenal": ("Paseo del Areal", "Paseo do Areal", "Areal promenade", "Passeio do Areal", "Promenade de l'Areal", "areal"),
 "Paseo, Estatua de Méndez-Núñez": ("Paseo y estatua de Méndez Núñez", "Paseo e estatua de Méndez Núñez", "Promenade and statue of Méndez Núñez", "Passeio e estátua de Méndez Núñez", "Promenade et statue de Méndez Núñez", "alameda"),
 "Pazo de Santhomé": ("Pazo de Santhomé", "Pazo de Santhomé", "Santhomé manor", "Paço de Santhomé", "Manoir de Santhomé", "centro"),
 "Playa": ("La playa", "A praia", "The beach", "A praia", "La plage", "centro"),
 "Playa \"La Foz\"": ("Playa de La Foz", "Praia da Foz", "La Foz beach", "Praia da Foz", "Plage de La Foz", "centro"),
 "Playa Samil": ("Playa de Samil", "Praia de Samil", "Samil beach", "Praia de Samil", "Plage de Samil", "samil"),
 "Playa de Bouzas": ("Playa de Bouzas", "Praia de Bouzas", "Bouzas beach", "Praia de Bouzas", "Plage de Bouzas", "bouzas"),
 "Playa de Guixar": ("Playa del Guixar", "Praia do Guixar", "O Guixar beach", "Praia do Guixar", "Plage du Guixar", "guixar"),
 "Playa de Samil": ("Playa de Samil", "Praia de Samil", "Samil beach", "Praia de Samil", "Plage de Samil", "samil"),
 "Plaza Puerta del Sol (nocturna)": ("Porta do Sol de noche", "Porta do Sol de noite", "Porta do Sol at night", "Porta do Sol à noite", "Porta do Sol de nuit", "sol"),
 "Plaza de Abastos y Paseo del berbés": ("Plaza de abastos y paseo del Berbés", "Praza de abastos e paseo do Berbés", "Food market and Berbés promenade", "Mercado e passeio do Berbés", "Marché et promenade du Berbés", "berbes"),
 "Plaza de Compostela": ("Plaza de Compostela", "Praza de Compostela", "Plaza de Compostela", "Praça de Compostela", "Place de Compostela", "alameda"),
 "Plaza de España y vista parcial": ("Plaza de España y vista parcial", "Praza de España e vista parcial", "Plaza de España and partial view", "Praça de Espanha e vista parcial", "Place d'Espagne et vue partielle", "espana"),
 "Plaza de la Constitución": ("Plaza de la Constitución", "Praza da Constitución", "Constitution Square", "Praça da Constituição", "Place de la Constitution", "constitucion"),
 "Plaza de la Princesa": ("Plaza de la Princesa", "Praza da Princesa", "Princesa Square", "Praça da Princesa", "Place de la Princesa", "princesa"),
 "Puerta del Sol": ("La Porta do Sol", "A Porta do Sol", "Porta do Sol", "A Porta do Sol", "La Porta do Sol", "sol"),
 "Puerto de pescadores": ("Puerto pesquero", "Porto pesqueiro", "Fishing harbour", "Porto de pesca", "Port de pêche", "berbes?"),
 "Puerto del Sol": ("La Porta do Sol", "A Porta do Sol", "Porta do Sol", "A Porta do Sol", "La Porta do Sol", "sol"),
 "Puerto pesquero desde El Castro": ("El puerto pesquero desde el Castro", "O porto pesqueiro dende o Castro", "The fishing harbour from O Castro", "O porto de pesca visto do Castro", "Le port de pêche depuis le Castro", "desdecastro"),
 "Puesta de sol": ("Puesta de sol", "Solpor", "Sunset", "Pôr do sol", "Coucher de soleil", "ria"),
 "Puesta de sol en Samil": ("Puesta de sol en Samil", "Solpor en Samil", "Sunset at Samil", "Pôr do sol em Samil", "Coucher de soleil à Samil", "samil"),
 "Punta del Murallón": ("Punta del Murallón", "Punta do Murallón", "Murallón point", "Ponta do Murallón", "Pointe du Murallón", "centro"),
 "Real Club Náutico": ("Real Club Náutico", "Real Club Náutico", "Royal Yacht Club", "Real Clube Náutico", "Real Club Náutico", "nautico"),
 "Regatas marítimas en el Puerto": ("Regatas en el puerto", "Regatas no porto", "Regattas in the harbour", "Regatas no porto", "Régates dans le port", "puerto?"),
 "Regreso de la pesca": ("Regreso de la pesca", "Volta da pesca", "Return from fishing", "Regresso da pesca", "Retour de la pêche", "berbes?"),
 "Residencia \"Almirante Vierna\"": ("Residencia Almirante Vierna", "Residencia Almirante Vierna", "Almirante Vierna residence", "Residência Almirante Vierna", "Résidence Almirante Vierna", "centro"),
 "Ribera de Berbés": ("Ribera del Berbés", "Ribeira do Berbés", "Ribeira do Berbés", "Ribeira do Berbés", "Ribeira do Berbés", "berbes"),
 "Ribera del Berbés": ("Ribera del Berbés", "Ribeira do Berbés", "Ribeira do Berbés", "Ribeira do Berbés", "Ribeira do Berbés", "berbes"),
 "Samil": ("Samil", "Samil", "Samil", "Samil", "Samil", "samil"),
 "Teatro Rosalía de Castro": ("Teatro Rosalía de Castro", "Teatro Rosalía de Castro", "Rosalía de Castro Theatre", "Teatro Rosalía de Castro", "Théâtre Rosalía de Castro", "rosalia"),
 "Tipo del país": ("Tipo popular", "Tipo do país", "Local character", "Tipo popular", "Personnage typique", "centro"),
 "Tipos del país": ("Tipos populares", "Tipos do país", "Local characters", "Tipos populares", "Personnages typiques", "centro"),
 "Un desembarco de pasajeros": ("Desembarco de pasajeros", "Desembarco de pasaxeiros", "Passengers disembarking", "Desembarque de passageiros", "Débarquement de passagers", "maritima"),
 "Un detalle de la Alameda": ("Detalle de la Alameda", "Detalle da Alameda", "Detail of the Alameda", "Pormenor da Alameda", "Détail de l'Alameda", "alameda"),
 "Una carreta de tojo": ("Una carreta de tojo", "Un carro de toxo", "A cart of gorse", "Um carro de tojo", "Une charrette d'ajoncs", "centro"),
 "Vigo": ("Vigo", "Vigo", "Vigo", "Vigo", "Vigo", "centro"),
 "Vigo (España). A la fuente": ("A la fuente", "Á fonte", "At the fountain", "À fonte", "À la fontaine", "centro"),
 "Vista General": ("Vista general", "Vista xeral", "General view", "Vista geral", "Vue générale", "centro"),
 "Vista General y Bouzas": ("Vista general y Bouzas", "Vista xeral e Bouzas", "General view and Bouzas", "Vista geral e Bouzas", "Vue générale et Bouzas", "bouzas"),
 "Vista Parcial": ("Vista parcial", "Vista parcial", "Partial view", "Vista parcial", "Vue partielle", "centro"),
 "Vista aérea": ("Vista aérea", "Vista aérea", "Aerial view", "Vista aérea", "Vue aérienne", "centro"),
 "Vista aérea y calle del Príncipe": ("Vista aérea y calle del Príncipe", "Vista aérea e rúa do Príncipe", "Aerial view and Príncipe Street", "Vista aérea e rua do Príncipe", "Vue aérienne et rue du Príncipe", "principe"),
 "Vista aérea. Playa de Samil": ("Playa de Samil, vista aérea", "Praia de Samil, vista aérea", "Samil beach, aerial view", "Praia de Samil, vista aérea", "Plage de Samil, vue aérienne", "samil"),
 "Vista desde el Banco de España": ("Vista desde el Banco de España", "Vista dende o Banco de España", "View from the Bank of Spain", "Vista do Banco de Espanha", "Vue depuis la Banque d'Espagne", "centro"),
 "Vista desde el camino de la estación": ("Vista desde el camino de la estación", "Vista dende o camiño da estación", "View from the station road", "Vista do caminho da estação", "Vue depuis le chemin de la gare", "centro"),
 "Vista desde el mar": ("Vista desde el mar", "Vista dende o mar", "View from the sea", "Vista do mar", "Vue depuis la mer", "ria"),
 "Vista desde la calle de Policarpo Sanz": ("Vista desde la calle de Policarpo Sanz", "Vista dende a rúa de Policarpo Sanz", "View from Policarpo Sanz Street", "Vista da rua de Policarpo Sanz", "Vue depuis la rue Policarpo Sanz", "policarpo"),
 "Vista general": ("Vista general", "Vista xeral", "General view", "Vista geral", "Vue générale", "centro"),
 "Vista general de la Bahía desde la Ribera": ("La bahía desde la Ribera", "A baía dende a Ribeira", "The bay from the waterfront", "A baía vista da Ribeira", "La baie depuis la Ribera", "berbes"),
 "Vista general desde el Castillo del Castro": ("Vista general desde el castillo del Castro", "Vista xeral dende o castelo do Castro", "General view from O Castro castle", "Vista geral do castelo do Castro", "Vue générale depuis le château du Castro", "desdecastro"),
 "Vista general desde la Guía": ("Vista general desde el monte de la Guía", "Vista xeral dende o monte da Guía", "General view from A Guía hill", "Vista geral do monte da Guía", "Vue générale depuis le mont de la Guía", "guia"),
 "Vista general panorámica": ("Vista panorámica", "Vista panorámica", "Panoramic view", "Vista panorâmica", "Vue panoramique", "centro"),
 "Vista panorámica": ("Vista panorámica", "Vista panorámica", "Panoramic view", "Vista panorâmica", "Vue panoramique", "centro"),
 "Vista panorámica de la Ribera de Berbés": ("Vista panorámica de la Ribera del Berbés", "Vista panorámica da Ribeira do Berbés", "Panoramic view of the Ribeira do Berbés", "Vista panorâmica da Ribeira do Berbés", "Vue panoramique de la Ribeira do Berbés", "berbes"),
 "Vista panorámica y Ría": ("Vista panorámica y la ría", "Vista panorámica e a ría", "Panoramic view and the estuary", "Vista panorâmica e a ria", "Vue panoramique et la ria", "ria"),
 "Vista parcial": ("Vista parcial", "Vista parcial", "Partial view", "Vista parcial", "Vue partielle", "centro"),
 "Vista parcial con la escuadra inglesa": ("Vista parcial con la escuadra inglesa", "Vista parcial coa escuadra inglesa", "Partial view with the British squadron", "Vista parcial com a esquadra inglesa", "Vue partielle avec l'escadre anglaise", "ria"),
 "Vista parcial de la Ría": ("Vista parcial de la ría", "Vista parcial da ría", "Partial view of the estuary", "Vista parcial da ria", "Vue partielle de la ria", "ria"),
 "Vista parcial desde El Castro": ("Vista parcial desde el Castro", "Vista parcial dende o Castro", "Partial view from O Castro", "Vista parcial do Castro", "Vue partielle depuis le Castro", "desdecastro"),
 "Vista parcial desde el Monte El Casto": ("Vista parcial desde el monte del Castro", "Vista parcial dende o monte do Castro", "Partial view from O Castro hill", "Vista parcial do monte do Castro", "Vue partielle depuis le mont du Castro", "desdecastro"),
 "Vista tomada desde \"El Castro\"": ("Vista desde el Castro", "Vista dende o Castro", "View from O Castro", "Vista do Castro", "Vue depuis le Castro", "desdecastro"),
 "Vista tomada desde la calzada": ("Vista desde la calzada", "Vista dende a calzada", "View from the road", "Vista da estrada", "Vue depuis la chaussée", "centro"),
}

DESC = {
    "es": "Tarjeta postal.", "gl": "Tarxeta postal.", "en": "Postcard.",
    "pt": "Bilhete-postal.", "fr": "Carte postale.",
}

FUERA = (r"fiestas|festejos|festival|aficionados|teatro artello|plaza de toros|la flor|oxitiol|perla coruñesa|houlder|"
         r"draught|carte de|plano|royaume|principales puertos|ria de vigo : spain|álbum de cromos|acto cultural|"
         r"el castillo, restaurante|bayona|santiago de compostela|coruña|mugía|pontevedra\.|arbo,|berducido|vincios|"
         r"nigrán|panjón|playa américa|playa america|samil \(pontevedra\)|la ría\. bayona|redondela|recuerdo de vigo|"
         r"la chapela")


def limpiar(t):
    t = re.sub(r"^\[?Vigo\]?\s*[\.\]]\s*", "", t.strip())
    t = re.sub(r"\s*=.*$", "", t)
    t = re.sub(r",\s*Vigo$", "", t).strip(" .[]")
    return t or "Vigo"


def main():
    origen = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))["fotos"]
    datos = json.loads(FOTOS.read_text(encoding="utf-8"))
    existentes = {f.get("url_fuente") for f in datos["fotos"]}
    añadidas, sin_texto = 0, []
    for f in origen:
        if not f["fuente"].startswith("Galiciana") or re.search(FUERA, f["titulo"], re.I):
            continue
        if f["url_fuente"] in existentes:
            continue
        clave = limpiar(f["titulo"])
        if clave not in T:
            sin_texto.append(clave)
            continue
        es, gl, en, pt, fr, lugar = T[clave]
        nombre, lat, lng, ub = L[lugar]
        anio = f["anio"] if f["anio"] not in (1800, 1900) else None  # 1800/1900: fechas genéricas del catálogo
        datos["fotos"].append({
            "id": f["id"],
            "titulo": es,
            "lugar": nombre,
            "anio": anio,
            "aproximada": bool(f["aproximada"]) and anio is not None,
            "descripcion": DESC["es"],
            "lat": lat, "lng": lng, "ubicacion": ub,
            "imagen": f["imagen"],
            "miniatura": f["miniatura"],
            "original": f["miniatura"],
            "autor": "",
            "fuente": "Galiciana",
            "url_fuente": f["url_fuente"],
            "licencia": "PDM",
            "importada": True,
            "textos": {l: {"titulo": t, "descripcion": DESC[l]}
                       for l, t in zip(["es", "gl", "en", "pt", "fr"], [es, gl, en, pt, fr])},
        })
        existentes.add(f["url_fuente"])
        añadidas += 1
    FOTOS.write_text(json.dumps(datos, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"Añadidas {añadidas} postales. Total: {len(datos['fotos'])} fotos.")
    if sin_texto:
        print("Sin texto (no añadidas):", sorted(set(sin_texto)))


if __name__ == "__main__":
    main()
