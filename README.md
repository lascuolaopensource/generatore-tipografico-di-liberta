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
