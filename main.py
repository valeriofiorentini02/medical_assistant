from embedchain import App
import fitz  # PyMuPDF
from io import BytesIO
import json
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph
import streamlit as st
from streamlit_lottie import st_lottie


versione = "0.0.7"

# Configurazione Pagina
st.set_page_config(
  page_title="Medical Assistant",
  page_icon="🏥",
  layout="centered",
  initial_sidebar_state="expanded",
  menu_items={
    'Get Help': None,
    'Report a bug': 'mailto:r.moscato@ilivetech.it',
    'About': f'MedAssistant v{versione} - ROSARIOSoft - Un software MIRACOLOSO!'
      }
  )

# Nascondo Hamburger Menu e Footer
hide_st_style = """
              <style>
              MainMenu {visibility: hidden;}
              footer {visibility: hidden;}
              header {visibility: hidden;}
              </style>
              """

st.markdown(hide_st_style, unsafe_allow_html=True)   

# Loading Lottie Files
def load_lottiefile(filepath: str):
  with open(filepath, "r") as f:
    return json.load(f)

def prescrizione_final_answer(bot, initial_answer):
  follow_up_query = ("Considerando che" + initial_answer + " e che sei un medico con anni di esperienza: "
                     "tieni conto della patologia sospetta e applica le buone pratiche. "
                     "Se presente rispondi con il nome del paziente. Indica la patologia sospetta e gli esami prescritti. Dimmi se gli esami prescritti sono corretti. "
                     "Per essere assolutamente sicuri circa la patologia consiglia ulteriori indagini da fare indicandole chiaramente. "
                     "Nella risposta non includere che sei un medico e non includere mai frasi del tipo 'Non riesco a leggere il file per ulteriori indagini specifiche'. Rispondi sempre in italiano. Inizia sempre con 'La prescrizione sottoposta indica che:'")
  return bot.query(follow_up_query)


def diagnosi_final_answer(bot, initial_answer):
  follow_up_query = ("Considerando che" + initial_answer + " e che sei un medico con anni di esperienza: "
                     "tieni conto della patologia sospetta e applica le buone pratiche. "
                     "Interpreta il referto e spiegamelo dettagliatamente come se fossi una persona di 14 anni. "
                     "Considerando tre livelli di urgenza pari a 'alta', 'media' e 'bassa' "
                     "indica quanto è urgente contattare un medico. Indica anche in maniera precisa che tipo di medico specialista va contattato. "
                     "Infine suggerisci ulteriori indagini da fare indicandole chiaramente. "
                     "Nella risposta non includere che sei un medico e non includere mai frasi del tipo 'Non riesco a leggere il file per ulteriori indagini specifiche'. "
                     "Rispondi sempre in italiano. Inizia sempre con 'La diagnosi sottoposta indica che:'")
  return bot.query(follow_up_query)
  

def analisi_final_answer(bot, initial_answer):
  follow_up_query = ("Considerando che" + initial_answer + " e che sei un medico con anni di esperienza: "
                     "tieni conto dei risultati acquisiti e applica le buone pratiche. "
                     "Interpreta le analisi e spiegamele sinteticamente come se fossi una persona di 14 anni. "
                     "Per ogni esame dimmi sinteticamente cosa significa il suo valore e se è corretto. "
                     "In caso di valori non corretti indica quali potrebbero essere le loro cause. "
                     "In caso di valori non corretti, suggerisci ulteriori indagini da fare indicandole chiaramente."
                     "Concludi riassumendo le ulteriori indagini da fate. "
                     "Prima di chiudere dai delle indicazioni sintetiche su un coretto stile di vita. "
                     "Nella risposta non includere che sei un medico e non includere mai frasi del tipo 'Non riesco a leggere il file per ulteriori indagini specifiche'. "
                     "Rispondi sempre in italiano. Inizia sempre con 'Le analisi sottoposte indicano che:'")
  return bot.query(follow_up_query)

def pulisci_sessione():
  st.session_state.clear()

def pulisci_db(bot):
  bot.reset()

# Creazione Sidebar
st.sidebar.image("items/dw_logo.png", width=200)
st.sidebar.write("")
st.sidebar.write("")
st.sidebar.write("")

# Creazione Menu
menu = st.sidebar.selectbox("Menu", ("Home", "Analisi", "Diagnosi", "Prescrizioni", "Info"))

# Sezione HOME
if menu == "Home":
  st.title(":rainbow[AI Medical Assistant] by :blue[Datawizard]")
  st.write("---")
  
  lottie_hr = load_lottiefile("items/doctor.json")
  st_lottie(
    lottie_hr,
    reverse=False,
    loop=True,
    quality="medium",
    height=640,
    width=800,
    key="hello")

elif menu == "Analisi":
  st.title(":rainbow[Lettura] :blue[Analisi]")
  st.write("---")

  analisi_pdf = st.sidebar.file_uploader("Carica il file delle analisi in formato PDF", type="pdf")
  
  if analisi_pdf is not None and not st.session_state.get('file_processed', False):
    st.sidebar.success("File caricato con successo")
  
    # Converto la prima pagina del PDF in un'immagine di anteprima
    with fitz.open(stream=analisi_pdf.getvalue(), filetype="pdf") as pdf_file:
      page = pdf_file[0]  # recupero la prima pagina
      pix = page.get_pixmap()  # converto la pagina in immagine
      pix.save("analisi_image.png")  # salvo l'immagine come PNG
      st.sidebar.image("analisi_image.png", caption="Anteprima file analisi")    

    # Salvo il file PDF in un buffer
    with open("analisi.pdf", "wb") as temp_file:
      temp_file.write(analisi_pdf.getbuffer())
  
    with st.spinner("Elaborazione in corso..."):
      analisi_bot = App()
      try:
        analisi_bot.add("analisi.pdf", data_type='pdf_file')
      except Exception as e:
        pass
      input_query = "Sei un operatore sanitario. Leggi il file e per ogni voce memorizza il valore rilevato e l'intervallo di riferimento."
      #input_query = "Di cosa parla il documento?"
      answer = analisi_bot.query(input_query)  
      
      try:
        final_answer = analisi_final_answer(analisi_bot, answer)
        st.subheader("Risposta:")
        st.write(f"{final_answer}\n\n")
        #st.write(f"{answer}\n\n")
        pulisci_sessione()
        pulisci_db(analisi_bot)
      except Exception as e:
        st.error(f"Errore durante le analisi: {e}")
        pulisci_sessione()
        pulisci_db(analisi_bot)
      
      # Creo un BytesIO buffer per il file PDF
      pdf_buffer = BytesIO()
      # Creo una SimpleDocTemplate instance
      pdf_doc = SimpleDocTemplate(pdf_buffer, pagesize=letter)
      # Creo uno StyleSheet
      styles = getSampleStyleSheet()
      normal_style = styles['Normal']
      # Create un Paragraph object con la final_answer, e aggiungo alcuni breaks
      final_answer_paragraph = Paragraph("<img src='items/dw_logo.png' width='90' height='12' /><br/><br/><br/>Risposta Diagnosi<br/><br/>"+final_answer.replace('\n', '<br/>'), normal_style)

      # Creo il PDF
      pdf_elements = [final_answer_paragraph]
      pdf_doc.build(pdf_elements)
  
      # Recupero il contenuto del PDF dal BytesIO buffer
      pdf_buffer.seek(0)
      risposta_analisi = pdf_buffer.getvalue()
  
      st.session_state['file_processed'] = True
  
      # Download Button
      st.download_button(label="Download Risposta",
         data=risposta_analisi,
         file_name="risposta_analisi.pdf",
         mime="application/pdf")


  elif analisi_pdf is None and st.session_state.get('file_processed', False):
    st.session_state.pop('file_processed')

  else:
    st.sidebar.error("Caricare un file PDF per procedere")



elif menu == "Diagnosi":
  st.title(":rainbow[Lettura] :blue[Diagnosi]")
  st.write("---")

  diagnosi_pdf = st.sidebar.file_uploader("Carica il file della diagnosi in formato PDF", type="pdf")
  
  if diagnosi_pdf is not None and not st.session_state.get('file_processed', False):
    st.sidebar.success("File caricato con successo")
  
    # Converto la prima pagina del PDF in un'immagine di anteprima
    with fitz.open(stream=diagnosi_pdf.getvalue(), filetype="pdf") as pdf_file:
      page = pdf_file[0]  # recupero la prima pagina
      pix = page.get_pixmap()  # converto la pagina in immagine
      pix.save("diagnosi_image.png")  # salvo l'immagine come PNG
      st.sidebar.image("diagnosi_image.png", caption="Anteprima file diagnosi")    
  
    # Salvo il file PDF in un buffer
    with open("diagnosi.pdf", "wb") as temp_file:
      temp_file.write(diagnosi_pdf.getbuffer())
  
    with st.spinner("Elaborazione in corso..."):
      diagnosi_bot = App()
      try:
        diagnosi_bot.add("diagnosi.pdf", data_type='pdf_file')
      except Exception as e:
        pass
      #input_query = "Di cosa parla il file?"
      input_query = "Riassumi dettagliatamente il contenuto del file includendo tutte le informazioni rilevanti."
      answer = diagnosi_bot.query(input_query)  
      try:
        final_answer = diagnosi_final_answer(diagnosi_bot, answer)
        st.subheader("Risposta:")
        st.write(f"{final_answer}\n\n")
        pulisci_sessione()
        pulisci_db(diagnosi_bot)
      except Exception as e:
          st.error(f"Errore durante la diagnosi: {e}")
          pulisci_sessione()
          pulisci_db(diagnosi_bot)
  
      # Creo un BytesIO buffer per il file PDF
      pdf_buffer = BytesIO()
      # Creo una SimpleDocTemplate instance
      pdf_doc = SimpleDocTemplate(pdf_buffer, pagesize=letter)
      # Creo uno StyleSheet
      styles = getSampleStyleSheet()
      normal_style = styles['Normal']
      # Create un Paragraph object con la final_answer, e aggiungo alcuni breaks
      final_answer_paragraph = Paragraph("<img src='items/dw_logo.png' width='90' height='12' /><br/><br/><br/>Risposta Diagnosi<br/><br/>"+final_answer.replace('\n', '<br/>'), normal_style)
  
      # Creo il PDF
      pdf_elements = [final_answer_paragraph]
      pdf_doc.build(pdf_elements)
  
      # Recupero il contenuto del PDF dal BytesIO buffer
      pdf_buffer.seek(0)
      risposta_diagnosi = pdf_buffer.getvalue()
  
      st.session_state['file_processed'] = True
  
      # Download Button
      st.download_button(label="Download Risposta",
         data=risposta_diagnosi,
         file_name="risposta_diagnosi.pdf",
         mime="application/pdf")
  
  
  elif diagnosi_pdf is None and st.session_state.get('file_processed', False):
    st.session_state.pop('file_processed')
  
  else:
    st.sidebar.error("Caricare un file PDF per procedere")
  

# Sezione PRESCRIZIONI
elif menu == "Prescrizioni":
  st.title(":rainbow[Lettura] :blue[Prescrizioni]")
  st.write("---")
  
  prescrizione_pdf = st.sidebar.file_uploader("Carica il file delle prescrizioni in formato PDF", type="pdf")
  
  if prescrizione_pdf is not None and not st.session_state.get('file_processed', False):
    st.sidebar.success("File caricato con successo")

    # Converto la prima pagina del PDF in un'immagine di anteprima
    with fitz.open(stream=prescrizione_pdf.getvalue(), filetype="pdf") as pdf_file:
      page = pdf_file[0]  # recupero la prima pagina
      pix = page.get_pixmap()  # converto la pagina in immagine
      pix.save("prescrizione_image.png")  # salvo l'immagine come PNG
      st.sidebar.image("prescrizione_image.png", caption="Anteprima file prescrizione")    
      
    # Salvo il file PDF in un buffer
    with open("prescrizioni.pdf", "wb") as temp_file:
      temp_file.write(prescrizione_pdf.getbuffer())
    
    with st.spinner("Elaborazione in corso..."):
      prescrizioni_bot = App()
      try:
        prescrizioni_bot.add("prescrizioni.pdf", data_type='pdf_file')
      except Exception as e:
        pass
      #input_query = "Di cosa parla il file?"
      input_query = "Riassumi il contenuto del file includendo se esiste il nome del paziente, la patologia sospetta e gli esami prescritti."
      answer = prescrizioni_bot.query(input_query)  
      try:
        final_answer = prescrizione_final_answer(prescrizioni_bot, answer)
        st.subheader("Risposta:")
        st.write(f"{final_answer}\n\n")
        pulisci_sessione()
        pulisci_db(prescrizioni_bot)
      
      except Exception as e:
        st.error(f"Errore durante la prescrizione: {e}")
        pulisci_sessione()
        pulisci_db(prescrizioni_bot)

      # Creo un BytesIO buffer per il file PDF
      pdf_buffer = BytesIO()
      # Creo una SimpleDocTemplate instance
      pdf_doc = SimpleDocTemplate(pdf_buffer, pagesize=letter)
      # Creo uno StyleSheet
      styles = getSampleStyleSheet()
      normal_style = styles['Normal']
      # Create un Paragraph object con la final_answer, e aggiungo alcuni breaks
      final_answer_paragraph = Paragraph("<img src='items/dw_logo.png' width='90' height='12' /><br/><br/><br/>Risposta Prescrizione<br/><br/>"+final_answer.replace('\n', '<br/>'), normal_style)
      
      # Creo il PDF
      pdf_elements = [final_answer_paragraph]
      pdf_doc.build(pdf_elements)
      
      # Recupero il contenuto del PDF dal BytesIO buffer
      pdf_buffer.seek(0)
      risposta_prescrizione = pdf_buffer.getvalue()

      st.session_state['file_processed'] = True

      # Download Button
      st.download_button(label="Download Risposta",
         data=risposta_prescrizione,
         file_name="risposta_prescrizione.pdf",
         mime="application/pdf")
      

  elif prescrizione_pdf is None and st.session_state.get('file_processed', False):
    st.session_state.pop('file_processed')
     
  else:
    st.sidebar.error("Caricare un file PDF per procedere")
    

else:
  st.title(":rainbow[Informazioni]")
  st.write("---")
  st.sidebar.markdown("""
      ### AI Medical Assistant
      **Developed by**: ROSARIOSoft

      [📧 Contattaci](mailto:r.moscato@ilivetech.it)

      © 2023 All rights reserved.

      ---

      Powered by OpenAI and Embedchain.  
      *Prompting is the Key!*
  """, unsafe_allow_html=True)

  st.markdown("""
      ## Come utilizzare l'AI Medical Assistant
      ### Passi da seguire:
      1. Seleziona dal **menu a tendina** nella barra laterale il tipo di operazione che desideri compiere:
          - **Home**: per tornare alla schermata principale dell'applicazione.
          - **Analisi**: per caricare e analizzare i risultati di analisi cliniche.
          - **Diagnosi**: per consultare e valutare le diagnosi.
          - **Prescrizioni**: per gestire le prescrizioni mediche.
      2. A seconda della scelta effettuata, ti saranno fornite le istruzioni specifiche su come procedere nella **schermata principale**.
      3. Per alcune funzionalità potrebbe essere necessario **caricare dei file** (come per esempio le prescrizioni mediche in formato PDF).
      4. Attendi che l'elaborazione sia completata e leggi o scarica i risultati proposti.
      ### Note aggiuntive:
      - Questa applicazione è sostenuta da tecnologie di intelligenza artificiale per l'elaborazione del linguaggio naturale.
      - Sarà possibile scaricare i risultati delle analisi, delle diagnosi o delle prescrizioni in formato PDF se necessario.
      - Per qualsiasi domanda o chiarimento, utilizza il link per contattare il supporto presente nella barra laterale sotto "Contattaci".
      ### Buon lavoro e benvenuti nell'era dell'assistenza medica supportata dall'AI!
  """, unsafe_allow_html=True)



 