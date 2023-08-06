# GF Parser 
> Pulls useful information from the web, helping you make flashcards for learning the German language.


This file will become your README and also the index of your documentation.

## Install

##### Still not working!

`pip install gfparser`

## How to use

First, import the `WikiParser`

```python
from gfparser import WikiParser
```

Create the parser object

```python
parser = WikiParser()
```

```python
parser.parse(["Hund", "arbeiten", "schön"])
```

    Downloading words
    0% [███] 100% | ETA: 00:00:00 | Item ID: schön               
    Total time elapsed: 00:00:01
    Downloading words
    0% [█] 100% | ETA: 00:00:00 | Item ID: schönen            
    Total time elapsed: 00:00:00


Iterate over `parser.words` and print the words:

```python
for w in parser.words:
    print (w)
```

    =======================================================
    =                         Hund                        =
    =======================================================
                                                           
                           Substantiv                      
                                                           
    [hʊnt]
    
    der Hund
    die Hunde
    
    1: Die mustergültige Definition, dass ein Hund ein von Flöhen bewohnter Organismus ist, der bellt, hat Kurt Tucholsky in seinem Traktat über den Hund dem Philosophen Gottfried Wilhelm Leibniz zugeschrieben.
    2: „Schatz, hab ich heute nacht das ganze Rindfleisch gefressen oder der Hund?…Gott! Ich hab'n Kopf wie'n Sieb!! Wir haben ja gar kein' Hund.“
    3: Bei neueren Umfragen bestätigen immerhin ein Viertel der Hundehalter, den Hund ins Bett zu lassen bzw. ihn dorthin auch des Nachts mitzunehmen.
    4: „In Gemeinschaft mit Eseln, Pferden und Hunden sitzen die Handwerker bei ihrer Arbeit auf der Straße.“
    5: „Der Hund gehorcht aufs Wort und geht links neben Elsa.“
    6: Er ist ein krummer Hund.
    7: „…; wenn die Beine müde werden, legst du dich in einem engen, schrägen Schacht, der wie ein zur Hälfte aufgestellter Abzugskanal wirkt, in einen der »Hunde« und läßt dich an das Tageslicht ziehen,…“
    8: „Erst mußte er die schweren Hunde schieben und Obacht geben, daß er sich nicht den Schädel einrammte in dem niedrigen Gang oder überfahren wurde.“
    9: Ich heb' an, und du schiebst den Hund drunter.
    10: Zur Familie der Hunde gehören Arten wie der Rotfuchs und der Wolf (mit der Unterart Haushund).
    
                                                           
                      Substantiv/Eigenname                 
                                                           
    [hʊnt]
    
    
    1: {{Beispiele fehlen|spr=de}}
    
                                                           
                      Substantiv/Nachname                  
                                                           
    [hʊnt]
    
    
    1: Frau Hund ist ein Genie im Verkauf.
    2: Herr Hund wollte uns kein Interview geben.
    3: Die Hunds fliegen heute nach Sri Lanka.
    4: Der Hund trägt nie die Pullover, die die Hund ihm strickt.
    5: Das kann ich dir aber sagen: „Wenn die Frau Hund kommt, geht der Herr Hund.“
    6: Hund kommt und geht.
    7: Hunds kamen, sahen und siegten.
    
    
    =======================================================
    =                       arbeiten                      =
    =======================================================
                                                           
                              Verb                         
                                                           
    [ˈaʁbaɪ̯tn̩]
    
    arbeite
    arbeitete
    haben gearbeitet
    
    1: Wir arbeiten gemeinsam an einem Wörterbuch.
    2: „Der Vater arbeitete in einer Kleiderfabrik und betrieb zu Hause mit seiner Frau in der Wohnung eine Schneiderei.“
    3: Er arbeitet als Lektor in einem bekannten Verlag.
    4: Was macht das Studium? Ich arbeite daran.
    5: Was macht die Reparatur? Wir arbeiten mit Hochdruck an der Hauptleitung.
    6: Seit der Reparatur arbeitet die Maschine ohne Unterbrechung.
    7: Die Anlage arbeitet wieder vorschriftsmäßig und im Takt.
    8: Viele Schmähungen musste er ertragen, fortan arbeitete es in seinem Herzen.
    9: Die Erlebnisse von gestern Abend arbeiten noch immer in mir, ich kann mich gar nicht auf die Arbeit konzentrieren.
    10: „Was ist der Unterschied zwischen einem Beamten und einem Stück Holz?“ – „Holz arbeitet!“
    11: Vergiss nicht die Fuge am Rand zu lassen, mindestens 2 cm, damit das Holz arbeiten kann!
    12: Ab Montag arbeite ich Teilzeit.
    
    
    =======================================================
    =                        schön                        =
    =======================================================
                                                           
                            Adjektiv                       
                                                           
    [ʃøːn]
    
    schön
    schöner
    am schönsten
    
    1: Sie hat schönes Haar. Das Musikstück ist schön.
    2: Sie sang schön, schöner als gewöhnlich, weil die Instrumentalisten ihr so vertraut waren. Am schönsten sang sie, als Viktor am Klavier saß.
    3: „Nik Wallenda, Urenkel eines deutschen Zirkusakrobaten, hat als erster Mensch die Niagarafälle an ihrer schönsten und gefährlichsten Stelle überquert.“
    4: Das hat er aber schön gemacht. Wir hatten schöne Ferientage. Es wäre schön, wenn wir uns wieder treffen. Es war schön von ihm, seiner Frau Blumen zu schenken.
    5: Das ist ja eine schöne Geschichte! Oder anders gesagt: Das ist aber wirklich schlimm!
    6: Du bist mir ja ein schöner Freund! Oder anders gesagt: Du bist wahrlich ein schlechter Freund!
    7: Da wird sie ganz schön staunen. Also, da wird sie aber überrascht sein.
    8: Das wird eine schöne Stange Geld kosten. Also, das wird wohl ziemlich teuer werden.
    9: Lass uns doch mal wieder im Kino einen Film ansehen! – Schön, dann komm!
    10: So, jetzt gehen wir schön ins Bett.
    11: Schön aufpassen, wenn du über die Straße gehst!
    
    
    =======================================================
    =                       schönen                       =
    =======================================================
                                                           
                              Verb                         
                                                           
    [ˈʃøːnən]
    
    schöne
    schönte
    haben geschönt
    
    1: Das Ergebnis: Angestellte der Politiker hatten in Hunderten Fällen die Biografien ihrer Arbeitgeber geschönt, Kritik entfernt oder den politischen Gegner verleumdet.
    2: Zudem wurden statistische Angaben in der UdSSR regelmäßig geschönt.
    3: Dieser Wein wurde mit Bentonit geschönt.
    
    

