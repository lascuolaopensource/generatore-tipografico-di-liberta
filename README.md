# Libreria Libertà

Una libreria per la generazione di caratteri a partire da una grammatica di simboli.

Lo scopo della libreria è quello di fornire uno strumento per la generazione di caratteri tipografici composti da elementi discreti.
La descrizione dei singoli glifi è fatta con puro testo, il numero di simboli usato è arbitrario e possono essere trasformati in elementi grafici attraverso ogni sintassi che descriva tutti quegli elementi. In questo modo la stessa descrizione può essere tradotta in elementi grafici in un numero teoricamente illimitato di modi.

La libreria può essere quindi usata come un interprete minimo di “linguaggi” arbitrari per la scrittura di font basate su elementi discreti: in questo senso è utile anche per riflettere, a un livello di complessità basso ma sufficiente, su alcuni problemi legati alla parametrizzazione del carattere tipografico e alla scrittura di linguaggi specifici per la creazione di “meta” font.

**Libertà** è scritta in Python e può essere usata con uno stile di programmazione funzionale.

Indice

1. Rappresentazione della font come testo
1. Interprete
2. Utility per la descrizione di contorni
3. Composizione di funzioni per disegnare


## Interprete

*import txt_reader*

Il modulo **txt_reader** è usato per estrarre una rappresentazione della struttura della font da una directory che contiene file di testo che descrivono il glifo (vedi paragrafo precedente).


### Tipi di dati

GlyphName: String

Il nome del glifo come stringa.


TextGlyph: ListOf String

Una rappresentazione del glifo come lista di stringhe, si assume che tutte le stringhe abbiano la stessa lunghezza.


FontDict: Dictionary (GlyphName, TextGlyph)

Una rappresentazione della font come un Dictionary di python. Le chiavi sono stringhe che rappresentano il nome del glifo, il valore la descrizione del glifo come testo.


### Funzioni

get_font_from_folder (folder_path) -> FontDict

folder_path: String

La funzione accetta come argomento l'indirizzo della directory dove sono i file che descrivono i glifi e produce una rappresentazione della font come FontDict. I file dei glifi devono avere estensione txt.


get_glyph_from_txt(txt_file) -> FontDict

txt_file: String

La funzione accetta come argomento l'indirizzo del file di testo che contiene la descrizione del glifo e produce un FontDict che contiene unicamente quel glifo.


*import draw_bits*

Il modulo **draw_bits** è usato per trasformare la descrizione astratta dei TextGlyph in glifi "grafici".


### Tipi di dati

Command: String
Una stringa di uno e un solo carattere da creare 

Vect: Tuple (Float, Float)
Un vettore bidimensionale rappresentato da una tupla composto da due numeri

DrawingProps: Dictionary (String, Any)
Le proprietà da passare alla funzione disegno; le chiavi sono stringhe e i valori possono essere qualsiasi tipo 

DrawingFunc: RGlyph Vect Vect DrawingProps -> None
Una procedura che disegna su un dato glifo a una data posizione secondo certe dimensioni e usando le proprietà passate come argomento

Syntax: Dictionary (Command, Tuple (DrawingFunc, DrawingProps))


### Funzioni

draw_bit_fnt (fnt, fnt_dict, suffix, dsc_hgt, box_size, box_layout, syntax) -> RFont

fnt: RFont
fnt_dict: FontDict
suffix: String
dsc_hgt: Integer
box_size: Vect
box_layout: Tuple (Integer, Integer)
syntax: Syntax

La funzione accetta come argomenti una RFont, un FontDict, l'eventuale suffisso da aggiungere ai glifi, la dimensione in celle delle discendenti, la dimensione della cella, l'eventuale suddivisione della cella in sottocelle e la sintassi. Produce una RFont.


draw_bit_gly(gly, gly_desc, dsc_hgt, box_size, box_layout, syntax) -> RGlyph

gly: RGlyph
gly_desc: TextGlyph
dsc_height: Integer
box_size: Vect
box_layout: Tuple (Integer, Integer)
syntax: Syntax

La funzione accetta come argomenti un RGlyph, un TextGlyph (vedi sopra), la dimensione in celle delle discendenti, la dimensione della cella, l'eventuale suddivisione della cella in sottocelle e la sintassi. Produce un RGlyph.



def draw_bit_lin(gly, char_line, box_position, box_size, box_layout, syntax) -> None

gly: RGlyph
char_line: String
box_position: Vect
box_size: Vect
box_layout: Tuple (Integer, Integer)
syntax: Syntax

La funzione accetta come argomenti un RGlyph, una stringa di comandi che rappresenta una "linea" di elementi, la posizione in cui cominciare a disegnare, la dimensione della cella, la suddivisione della cella, la sintassi. Non produce nulla.


draw_bit_chr(gly, char, box_position, box_size, box_layout, syntax) -> None

gly: RGlyph
char: Command
box_position: Vect
box_size: Vect
box_layout: Tuple (Integer, Integer)
syntax: Syntax

La funzione accetta come argomenti un RGlyph, una Command, la posizione in cui iniziare a disegnare, la dimensione della cella, la sufddivisione eventuale della cela e la sintassi. Non produce nulla.


## Utility per la descrizione di contorni

import shape_functions

Il modulo **shape_functions** fornisce delle funzione di utilità per la scrittura di contorni e di primitive.


### Tipi di dati

Point: Vect
Un punto è un Vect (tupla costituita da due numeri)

CurveElement: OneOf (Point, Tuple (Point, Point, Float))
Un elemento di curva può essere un punto o una tupla costituita da tre elementi: due punti e un valore numerico che indica la squadratura. Il primo e l'ultimo punto devono coincidere.

Curve: ListOf (Point, CurveElement, ...)
Una curva è rappresentata da una lista che inzia obbligatoriamente con un punto e continua con una sequenza di CurveElement.
Le regole sono le seguenti:
1. [..., pt1, pt2, ...] rappresenta una linea da pt1 a pt2
2. [..., pt1, (pt2, pt3, sq), ...] rappresenta una curva che inizia in pt1 e finisce in pt3. I segmenti pt1-pt2 e pt2-pt3 rappresentano, rispettivamente, le tangenti alla curva in pt1 e pt3, sq è un paramentro che controlla la tensione dei punti di controllo della curva di Bézier rappresentata così, ad esempio, se sq=1 i due punti di controllo coincidono con pt2, se sq=0 i due punti di controllo coincidono rispettivamente con pt1 e pt3 e la curva degenera in una linea da pt1 a pt3.
3. [..., (pt1, pt2, sq), (pt3, pt4, sq), ... ] rappresenta una curva che parte da pt2 e finisce a pt4 secondo le stesse regole descritte sopra.


### Funzioni

interpolate_points(pA, pB, f) -> Point

pA: Point
pB: Point
f: Float

Interpola tra i punti pA e pB usando come fattore di interpolazione il numero f. Produce un punto.


drawer(gly, pts) -> RGlyph

gly: RGlyph
pts: Curve

**drawer** accetta come argomenti un RGlyph su cui disegnare e una Curve. La funzione crea un contorno corrispondente alla curva nel glifo. Produce il Glifo.



## Composizione di funzioni per disegnare

import composition

Il modulo **composition** consente di comporre un numero arbitrario di funzioni di disegno in altre funzioni di disegno suddividendo il box in senso orizzontale o verticale.


### Funzioni

### split_hor

split_hor (fn, fn, ...) -> (RGlyph, Number, Number, Dictionary -> None)

fn: (RGlyph, Number, Number, Dictionary -> None)

Prende un numero arbitrario di funzioni di disegno e ritorna una funzione che disegna con le funzioni argomento una accanto all'altra.

Esempio

fn = split_hor (rectangle, rectangle)

+----+----+
|    |    |
|    |    |
|    |    |
|    |    |
+----+----+

### split_ver

split_ver (fn, fn, ...) -> (RGlyph, Number, Number, Dictionary -> None)

fn: (RGlyph, Number, Number, Dictionary -> None)

Prende un numero arbitrario di funzioni di disegno e ritorna una funzione che disegna con le funzioni argomento una sotto l'altra.

Esempio

fn = split_ver (rectangle, rectangle)

+---------+
|         |
|         |
+---------+
|         |
|         |
+---------+


Esempio
Composizione annidata

fn = split_ver (rectangle, split_hor (rectangle, rectangle))

+---------+
|         |
|         |
+----+----+
|    |    |
|    |    |
+----+----+
