import streamlit as st
from streamlit_lottie import st_lottie
import json
from embedchain import App
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph
from io import BytesIO

versione = "0.0.1"

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
                     "Rispondi con il nome del paziente e della patologia sospetta e dimmi se gli esami prescritti sono corretti. "
                     "Per essere assolutamente sicuri circa la patologia consiglia ulteriori indagini da fare indicandole chiaramente. "
                     "Nella risposta non includere che sei un medico. Rispondi sempre in italiano. "
                     "Se non puoi rispondere a domande, rispondi con 'Non riesco a leggere il file'.")
  return bot.query(follow_up_query)

def pulisci_sessione():
  st.session_state.clear()

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


elif menu == "Diagnosi":
  st.title(":rainbow[Lettura] :blue[Diagnosi]")
  st.write("---")

# Sezione PRESCRIZIONI
elif menu == "Prescrizioni":
  st.title(":rainbow[Lettura] :blue[Prescrizioni]")
  st.write("---")

  # Inizializzazioni
  #final_answer = ""
  #prescrizione_pdf_old_name = ""
  
  prescrizione_pdf = st.sidebar.file_uploader("Carica il file delle prescrizioni in formato PDF", type="pdf")
  
  if prescrizione_pdf is not None:
    st.sidebar.success("File caricato con successo")

    with open("prescrizioni.pdf", "wb") as temp_file:
      temp_file.write(prescrizione_pdf.getbuffer())
    
    with st.spinner("Elaborazione in corso..."):
      prescrizioni_bot = App()
      prescrizioni_bot.add("prescrizioni.pdf", data_type='pdf_file')
    
      input_query = "Di cosa parla il file?"
      answer = prescrizioni_bot.query(input_query)      
      final_answer = prescrizione_final_answer(prescrizioni_bot, answer)
      st.subheader("Risposta:")
      st.write(f"{final_answer}\n\n")

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
    
      st.download_button(label="Download Risposta",
         data=risposta_prescrizione,
         file_name="risposta_prescrizione.pdf",
         mime="application/pdf")
     
  else:
    st.sidebar.error("Caricare un file PDF per procedere")
    

else:
  st.title(":rainbow[Informazioni]")
  st.write("---")



 