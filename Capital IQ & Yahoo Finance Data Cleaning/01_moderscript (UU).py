import subprocess
import logging
import os

# Konfigurer logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)

dir = "c:/Users/b407939/Desktop/Speciale/Clean Start/Kode"

def run_script(script_name):
    """Funktion til at køre et script og logge status."""
    try:
        logging.info(f"Starter eksekvering af script: {script_name}")
        subprocess.run(["python", script_name], check=True)
        logging.info(f"Script kørt succesfuldt: {script_name}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Fejl under eksekvering af script: {script_name}")
        logging.error(f"Returneret kode: {e.returncode}")
        raise
    except FileNotFoundError:
        logging.error(f"Script ikke fundet: {script_name}")
        raise

def main():
    """Hovedfunktion til at køre alle scripts i rækkefølge."""
    scripts = [
        f"{dir}/3_get yf tickers.py", # Henter lejebærende arealer i kontorporteføljen på bygningsniveau.
        f"{dir}/4_get yf stock data event period.py", # Tilføjer fredningsstatus og opførelsesår.
        f"{dir}/5_get yf stock data est period.py" # Aggregerer outputtet af script 2 fra bygningsniveau til ejendomsniveau.
        f"{dir}/6_get yf stock data est period.py"
    ]

    # Tjek at alle scripts eksisterer
    for script in scripts:
        if not os.path.exists(script):
            logging.error(f"Script mangler: {script}")
            raise FileNotFoundError(f"Script mangler: {script}")

    # Eksekver scripts i rækkefølge
    for script in scripts:
        run_script(script)

    logging.info("Alle scripts blev eksekveret succesfuldt!")

if __name__ == "__main__":
    main()
