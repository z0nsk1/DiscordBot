Kaveriporukan Discord-serverille tehty botti. Botti on toteutettu Python:lla. Bottia kutsutaan Discord-viestinä annettavana komentona, esim. $members. Ennen komentosanaa pitää käyttää merkkiä '$', jotta botti ymmärtää sen komennoksi.  

Botille toteutetut komennot:  
- <strong>temp <kaupunki>:</strong> tulostaa argumenttina annettavan kaupungin ajankohtaisen sään sekä säätä kuvaavan kuvan. Jos kaupunkia ei annetta, tulostetaan oletusarvoisesti Jyväskylän sää. Säätiedot haetaan OpenWeather-API:n kautta. Sää-API:n kutsuminen tapahtuu koordinaateilla, joten ensin kutsutaan toista API:a kaupungin nimellä, jotta saadaan sen koordinaatit. Tämän jälkeen voidaan koordinaateilla kutsua Sää-API:a.
- <strong>shtpost:</strong> tulostaa koneella sijaitsevasta kuvakansiosta satunnaisesti valitun kuvan
- <strong>apua:</strong> tulostaa koneella sijaitsevan tekstitiedoston sisällön, jossa on ohjeet botin käyttöön sekä lista sen ymmärtämistä komennoista
- <strong>lenny:</strong> tulostaa chattiin lenny-facen ( ͡° ͜ʖ ͡°) (tätä on aina ärsyttävä kaivaa Googlesta, joten nyt se on helpompaa)
- <strong>bingobangobongo:</strong> botti vastaa "Bish Bash Bosh!". Legendaarinen lausahdus, joka on ainakin Counter Striken pelaajille tuttu.
- <strong>luikaus:</strong> tulostaa koneella sijaitsevasta tiedostosta satunnaisen, hassun hauskan lausahduksen, joka on  jonkun meidän kaveriporukan suusta joskus päässyt lipsahtamaan. Näitä olemme keränneet vuosia.
- <strong>pvm:</strong> tulostaa nykyisen päivämäärän muodossa "viikonpäivä dd.mm.yyyy klo hh:mm viikko: <vknro>
- <strong>dice <luku>: </strong> nopanheitto! Botti arpoo ja tulostaa satunnaisen luvun lukujen 1 ja argumenttina annetun luvun väliltä. Jos argumenttia ei anneta, arvotaan luku väliltä [1, 6], kuten tavallisessa nopassa
- <strong>info:</strong> tulostaa botin version, tekijän (minä) sekä millä ohjelmointikielellä botti on tehty
- <strong>yee:</strong> tulostaa legendaarisen yee-kuvan

Komennoissa, jotka voivat ottaa argumentin, on myös virheenkäsittely, jos argumentti ei ole oikeaa muotoa. Jos komentoa ei ole olemassa, käsitellään se virhetilanteena ja botti vastaa että "Komentoa ei ole olemassa". 
  
Esimerkki temp-komennon käytöstä:  
  
![Esimerkkikuva temp-komennon käytöstä](/esimerkki.png)
