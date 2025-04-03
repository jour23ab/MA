1.	Hent bond yield data fra ECB.
2.	Hent europæiske fama french factors fra Kenneth French's data library.
3.	Brug "0_get_eu_market_data.py" til at hente STOXX 600 indexen som markedsportefølje.

4.	Hent data fra Capital IQ.
5.	Brug "0_clean_raw_data.py" til at rengøre filen.
6.	Tilføj VBA koden til excel filen og kør den for at tilføje start og slut datoer for event og estimations perioderne.

7.	Brug "2_remove_overlapping_events.py" til at fjerne events der overlapper.
a.	Alternativt kan "1_moderscript" anvendes der kører alle de resterende scripts med et klik.
8.	Brug "3_yf_tickers.py" for at få yahoo finance tickers på baggrund af navnene fået i Bloomberg.
9.	Brug "4_yf_stock_data_event_period.py" for at få stock priserne i eventperioden gennem Yahoo finance.
10.	Brug "5_yf_stock_data_est_period.py" for at få stock priserne i estimeringsperioden gennem Yahoo finance.
11.	Brug "6_calc_event_returns_merge_fama_french_factors.py" for at omregne stock priserne i eventperioden til simple returns og merge STOXX 600 daglige returns, risk free rate, SMB og HML på.
12.	Brug "7_calc_est_returns_merge_fama_french_regression.py".
