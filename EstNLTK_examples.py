# -*- coding: utf-8 -*-
from EstNLTK.EstNLTK import EstNLTK
enltk = EstNLTK()

### lausesta() lausestab, rohkem ei midagi
print enltk.lausesta('See on üks lause. See on juba teine lause.')

### wn_hyperonyymid() annab sõna hüpernüümid listina
print enltk.wn_hyperonyymid('auto')

### wn_synonyymid() annab sõna sünonüümid listina
print enltk.wn_hyperonyymid('jumal')

### wn_definitsioonid() annab sõna definitsioonid listina
print enltk.wn_definitsioonid('jumal')

### t3_lemmatiseeri() annab sisendi lemmatiseeritud variandi listina
print enltk.t3_lemmatiseeri('See lause on listiks lemmatiseerimiseks.', 'list')

### t3_lemmatiseeri() annab sisendi lemmatiseeritud variandi stringina
print enltk.t3_lemmatiseeri('See lause on stringiks lemmatiseerimiseks.', 'string')

### t3_yhesta() ühestab sisendi ja annab tulemuse 1d listina
print enltk.t3_yhesta('See lause läheb ühestamisele.', 'list')

### t3_yhesta() ühestab sisendi ja annab tulemuse 2d listina
print enltk.t3_yhesta('See lause läheb samuti ühestamisele, kuid tulemus on kahedimensioonilise listina.', '2dlist')

### bigrammid() leiab sisendstringist kõik bigrammid ja annab väljundi listina
print enltk.bigrammid('anna mulle selle lause bigrammid, siin on koma')

### bigrammid_kitsendustega() leiab sisendstringist kõik bigrammid, kus esimeses sõnas on argument 2 ja teises sõnas argument 3
print enltk.bigrammid_kitsendustega('anna mulle selle lause bigrammid, kusjuures siin on veel kitsendused','_P_','_S_')
