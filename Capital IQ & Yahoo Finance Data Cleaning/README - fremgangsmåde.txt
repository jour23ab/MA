Hej. Velkommen til fremgangsmåden for koden. Koden kan desværre ikke køres med et enkelt klik, hvorfor denne lange beskrivelse er nødvendig.
Desværre er moderscriptet stadig under udvikling (UU) og vil tage for lang tid at udbedre.

1.	Hent bond yield data fra ECB.
2.	Hent europæiske fama french factors fra Kenneth French's data library.
3.	Brug "0_get_eu_market_data.py" til at hente STOXX 600 indexen som markedsportefølje.

4.	Hent data fra Capital IQ.
        (dernæst preprocess capital iq dataen fra en xls til xlsx fil.)
5.	Brug "0_clean_raw_data.py" til at rengøre filen.
6.	Tilføj VBA koden til excel filen og kør den for at tilføje start og slut datoer for event og estimations perioderne.

7.	Brug "2_remove_overlapping_events.py" til at fjerne events der overlapper.
8.	Brug "3_yf_tickers.py" for at få yahoo finance tickers på baggrund af navnene fået i Bloomberg.
9.	Brug "4_yf_stock_data_event_period.py" for at få stock priserne i eventperioden gennem Yahoo finance.
10.	Brug "5_yf_stock_data_est_period.py" for at få stock priserne i estimeringsperioden gennem Yahoo finance.
11.	Brug "6_calc_event_returns_merge_fama_french_factors.py" for at omregne stock priserne i eventperioden til simple returns og merge STOXX 600 daglige returns, risk free rate, SMB og HML på.
12.	Brug "7_calc_est_returns_merge_fama_french_regression.py".
13. Brug de resterende numerede filer i deres naturlige rækkefølge.
