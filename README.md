# Libreria Generatore Tipografico di Libertà

Una libreria per la generazione di caratteri a partire da una grammatica di simboli.

Lo scopo della libreria è quello di fornire uno strumento per la generazione di caratteri tipografici composti da elementi discreti.
La descrizione dei singoli glifi è fatta con puro testo, il numero di simboli usato è arbitrario e possono essere trasformati in elementi grafici attraverso ogni sintassi che descriva tutti quegli elementi. In questo modo la stessa descrizione può essere tradotta in elementi grafici in un numero teoricamente illimitato di modi.

La libreria può essere quindi usata come un interprete minimo di “linguaggi” arbitrari per la scrittura di font basate su elementi discreti: in questo senso è utile anche per riflettere, a un livello di complessità basso ma sufficiente, su alcuni problemi legati alla parametrizzazione del carattere tipografico e alla scrittura di linguaggi specifici per la creazione di “meta” font.

Il **Generatore Tipografico di Libertà** è scritto in Python e può essere usato con uno stile di programmazione funzionale.



Indice

1. Struttura del progetto
2. Rappresentazione della font come testo
3. Interprete
4. Utility per la descrizione di contorni
5. Composizione di funzioni per disegnare
6. Prospettive, suggerimenti e commenti dei partecipanti
7. Il nome del progetto
8. Partecipanti


## Struttura del progetto




## Rappresentazione della font come testo

Ogni glifo del carattere è rappresentato in un file di testo. la prima linea contiene il nome del glifo, la seconda linea è vuota, le linee successive rappresentano il glifo con una serie di simboli.

Esempio:

```
A

.#####.
.#...#.
.#...#.
.#####.
.#...#.
.#...#.
.#...#.
.......
.......

```
I file dei glifi sono contenuti in una cartella e organizzati in sottocartelle come questo esempio:
  
```
font_liberta
      |
      |
      +--- lettere
      |       |
      |       |
      |       +--- minuscole
      |       |        |
      |       |        +--- a.txt
      |       |        +--- b.txt
      |       |        +--- ...
      |       |
      |       +--- maiuscole

```

I nomi dei file dei glifi non hanno uno scopo al fine della generazione della font ma solo come mezzo per tenere organizzati i glifi.




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


make_clockwise(c, cw) -> RContour
c: RContour
cw: Boolean

La funzione accetta un contorno e un Boolean (True se il contorno deve essere in senso orario, False altrimenti) e cambia il senso del contorno secondo il valore di cw. Produce il contorno.


do_nothing(gly, position, size, properties) -> None

gly: RGlyph
position: Vect
size: Vect
properties: DrawingProps

**do_nothing** è una funzione di tipo **DrawingFunc** utile per attribuire a un comando della sintassi il significato di un elemento vuoto.


rectangle(gly, position, size, properties) -> None

gly: RGlyph
position: Vect
size: Vect
properties: DrawingProps

**rectangle** è una funzione di tipo **DrawingFunc**; crea un rettangolo nel glifo alla posizione data (centro), con le dimensioni date e applicando le proprietà passate alla funzione.
Le proprietà da passare sono "scale" (Vect), "rotation" (Float) e "clockwise" (Boolean).


ellipse(gly, position, size, properties) -> None

gly: RGlyph
position: Vect
size: Vect
properties: DrawingProps

**ellipse** è una funzione di tipo **DrawingFunc**; crea un'ellisse nel glifo alla posizione data (centro), con le dimensioni date e applicando le proprietà passate alla funzione.
Le proprietà da passare sono "scale" (Vect), "rotation" (Float), "squaring" (Float) e "clockwise" (Boolean).


ellipse_quarter(gly, position, size, properties) -> None

gly: RGlyph
position: Vect
size: Vect
properties: DrawingProps

**ellipse_quarter** è una funzione di tipo **DrawingFunc**; crea un quarto di ellisse nel glifo alla posizione data (centro), con le dimensioni date e applicando le proprietà passate alla funzione.
Le proprietà da passare sono "scale" (Vect), "rotation" (Float), "squaring" (Float), "orientation" (OneOf "NW" "NE" "SE" "SW") e "clockwise" (Boolean).


ellipse_half(gly, position, size, properties) -> None

gly: RGlyph
position: Vect
size: Vect
properties: DrawingProps

**ellipse_half** è una funzione di tipo **DrawingFunc**; crea un semiellisse nel glifo alla posizione data (centro), con le dimensioni date e applicando le proprietà passate alla funzione.
Le proprietà da passare sono "scale" (Vect), "rotation" (Float), "squaring" (Float), "orientation" (OneOf "N" "E" "S" "W") e "clockwise" (Boolean).


random_function (gly, position, size, properties) -> None

gly: RGlyph
position: Vect
size: Vect
properties: ListOf (Tuple (DrawingFunc, DrawingProps))

La funzione **random_function** accetta come argomenti un RGlyph e ci disegna con una delle funzioni passate tra le proprietà (properties) scelta in modo casuale nella posizione data, con le dimensioni date. Ogni funzione è passata in una lista insieme alle proprietà che le devono essere applicate.


ellipse_quarter_ro(gly, position, size, properties) -> None

gly: RGlyph
position: Vect
size: Vect
properties: ListOf (Tuple (DrawingFunc, DrawingProps))

Come ellipse_quarter ma scelglie l'orientamento in modo casuale.


ellipse_half_ro(gly, position, size, properties) -> None

gly: RGlyph
position: Vect
size: Vect
properties: ListOf (Tuple (DrawingFunc, DrawingProps))

Come ellipse_half ma sceglie l'orientamento in modo casuale.


## Composizione di funzioni per disegnare

import composition

Il modulo **composition** consente di comporre un numero arbitrario di funzioni di disegno in altre funzioni di disegno suddividendo il box in senso orizzontale o verticale.


### Funzioni

### split_hor

split_hor (fn, fn, ...) -> (RGlyph, Number, Number, Dictionary -> None)

fn: (RGlyph, Number, Number, Dictionary -> None)

Prende un numero arbitrario di funzioni di disegno e ritorna una funzione che disegna con le funzioni argomento una accanto all'altra.

Esempio

```

fn = split_hor (rectangle, rectangle)

+----+----+
|    |    |
|    |    |
|    |    |
|    |    |
+----+----+

```


### split_ver

split_ver (fn, fn, ...) -> (RGlyph, Number, Number, Dictionary -> None)

fn: (RGlyph, Number, Number, Dictionary -> None)

Prende un numero arbitrario di funzioni di disegno e ritorna una funzione che disegna con le funzioni argomento una sotto l'altra.

Esempio

```

fn = split_ver (rectangle, rectangle)

+---------+
|         |
|         |
+---------+
|         |
|         |
+---------+

```


Esempio
Composizione annidata

```

fn = split_ver (rectangle, split_hor (rectangle, rectangle))

+---------+
|         |
|         |
+----+----+
|    |    |
|    |    |
+----+----+

```


## Prospettive, suggerimenti e commenti dei partecipanti

### Daniele
Il codice è scritto in parte in uno stile funzionale (nel senso della *functional programming*) in parte no. Questo rispecchia le diverse inclinazioni di chi lo ha scritto ma soprattutto il fatto che la libreria sottostante, Robofab, opera quasi sempre con dati mutabili e attraverso mutazioni. 
Credo che si potrebbe, come esercizio, tentare comunque di mantenere uno stile funzionale, pur scontando il fatto che le procedure determineranno mutazioni e "effetti collaterali", imponendo che tutte le funzioni ritornino qualcosa. Una riscrittura più radicale in termini di programmazione funzionale potrebbe costruire un livello che isoli le mutazioni di robofab attraverso copie: in questo modo si eliminerebbero tutte le mutaziuoni e tutto il codice potrebbe essere libero da effetti collaterali.
Senza arrivare a questo, una riscrittura in termini funzionali potrebbe cercare di cambiare determinati meccanismi di passaggio delle proprietà per le funzioni.

Da un punto di vista dell'usabilità sarebbe forse il caso di aggiungere dei controlli che "assicurino" che il corretto tipo di dati è passato alle funzioni, in questo modo sarebbe più facile tracciare e individuare gli errori.

Se interpretiamo questo lavoro come la realizzazione di un linguaggio incompleto per la definizione arbitraria di simboli di descrizione e progettazione di caratteri quasi parametrici, allora sarebbe bello ipotizzare un modo per definire i significati dei simboli senza usare python in modo diretto.


## Il nome del progetto

Il nome Libertà è un gioco tra il significato comune del termine e il nome del quartiere di Bari in cui si trova l'Officina degli Esordi. Il nome è stato scelto dai partecipanti al gruppo di X Type (forse non tutti all'unanimità, ma i più decisi).

## I partecipanti

Giovanni
Giulio
Greta 
Laura
Micol
Roberto
Daniele

La libreria è stata scritta in massima parte da Giovanni sulla base di alcune funzioni scritte da Daniele per il corso di Type and Code.
I glifi contenuti nella cartella assets/letters sono il lavoro collettivo del gruppo di X Type, in modo particolare di Giulio, Greta, Laura, Micol e Roberto).
I glifi nella cartella assets/italic sono il frutto del lavoro di Giulio.
Le forme che compongono le lettere sono state proposte dal gruppo di X Identità coordinato da Andrea Bergamini.

Ringrazio tutti per avere avuto la pazienza di sopportare le mie stranezze comunicative,
Daniele.



Non è il caos ma
l'ordine, invece.
È la semplicità
che è difficile a farsi.

B.B.
