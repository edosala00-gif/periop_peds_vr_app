
import streamlit as st
import pandas as pd
import os
from utils.pdf_templates import build_mypas_icc_pdf, build_medicazione_pdf

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

st.set_page_config(page_title="Periop Peds VR – Data App", layout="wide")
st.title("Periop Peds VR – Data Entry & Forms")
st.caption("m-YPAS / ICC / FLACC – Screening, Baseline e Medicazioni")

def init_table(path, columns):
    if os.path.exists(path):
        try:
            return pd.read_excel(path)
        except Exception:
            pass
    df = pd.DataFrame(columns=columns)
    df.to_excel(path, index=False)
    return df

def append_row(path, row_dict, columns):
    df = init_table(path, columns)
    df = pd.concat([df, pd.DataFrame([row_dict], columns=columns)], ignore_index=True)
    df.to_excel(path, index=False)
    return df

def download_df(df):
    return df.to_csv(index=False).encode("utf-8")

page = st.sidebar.radio("Sezioni", ["Screening Log", "Baseline m-YPAS/ICC", "Medicazioni", "Randomization"])

# ---------- Screening Log ----------
if page == "Screening Log":
    st.header("Screening Log")
    SCREEN_PATH = os.path.join(DATA_DIR, "Screening_Log.xlsx")
    columns = [
        "Data", "Giorno (Mar/Gio)", "N° Lista/Sala", "Tipo procedura (minore/maggiore)",
        "Età", "ASA", "Genitore presente (Sì/No)",
        "Eleggibile (Sì/No)", "Motivo NON eleggibilità",
        "Consenso ottenuto (Sì/No)", "Motivo mancato consenso",
        "Randomizzato (A=VR / B=Controllo)", "m-YPAS T1 registrato (Sì/No)",
        "m-YPAS T2 registrato (Sì/No)", "ICC registrato (Sì/No)",
        "Programmate medicazioni post-op (Sì/No)", "Note"
    ]
    with st.form("screen_form"):
        c1,c2,c3 = st.columns(3)
        data = c1.date_input("Data")
        day = c2.selectbox("Giorno", ["Martedì","Giovedì"])
        sala = c3.text_input("N° Lista/Sala")
        tipo = st.selectbox("Tipo procedura", ["Minore","Maggiore"])
        c4,c5,c6 = st.columns(3)
        eta = c4.number_input("Età (anni)", min_value=0, max_value=18, step=1)
        asa = c5.selectbox("ASA", ["I","II","III","IV"])
        gen = c6.selectbox("Genitore presente", ["Sì","No"])
        c7,c8 = st.columns(2)
        elig = c7.selectbox("Eleggibile", ["Sì","No"])
        motivon = c8.text_input("Motivo NON eleggibilità")
        c9,c10 = st.columns(2)
        cons = c9.selectbox("Consenso ottenuto", ["Sì","No"])
        motivoc = c10.text_input("Motivo mancato consenso")
        c11,c12,c13 = st.columns(3)
        rand = c11.selectbox("Randomizzato", ["","A","B"])
        m1 = c12.selectbox("m-YPAS T1 registrato", ["","Sì","No"])
        m2 = c13.selectbox("m-YPAS T2 registrato", ["","Sì","No"])
        c14,c15 = st.columns(2)
        icc = c14.selectbox("ICC registrato", ["","Sì","No"])
        medp = c15.selectbox("Programmate medicazioni post-op", ["","Sì","No"])
        note = st.text_area("Note")
        submitted = st.form_submit_button("Salva nel registro")
    if submitted:
        row = {
            "Data": pd.to_datetime(data),
            "Giorno (Mar/Gio)": day,
            "N° Lista/Sala": sala,
            "Tipo procedura (minore/maggiore)": tipo,
            "Età": eta, "ASA": asa, "Genitore presente (Sì/No)": gen,
            "Eleggibile (Sì/No)": elig, "Motivo NON eleggibilità": motivon,
            "Consenso ottenuto (Sì/No)": cons, "Motivo mancato consenso": motivoc,
            "Randomizzato (A=VR / B=Controllo)": rand,
            "m-YPAS T1 registrato (Sì/No)": m1,
            "m-YPAS T2 registrato (Sì/No)": m2,
            "ICC registrato (Sì/No)": icc,
            "Programmate medicazioni post-op (Sì/No)": medp,
            "Note": note
        }
        df = append_row(SCREEN_PATH, row, columns)
        st.success("Registrato nello Screening Log.")
    df = init_table(SCREEN_PATH, columns)
    st.dataframe(df, use_container_width=True)
    st.download_button("Scarica CSV", data=download_df(df), file_name="Screening_Log.csv", mime="text/csv")

# ---------- Baseline m-YPAS/ICC ----------
elif page == "Baseline m-YPAS/ICC":
    st.header("Baseline m-YPAS / ICC")
    BASE_PATH = os.path.join(DATA_DIR, "CRF_Baseline_mYPAS_ICC.xlsx")
    columns = [
        "ID Paziente","Età","Sesso","ASA","Tipo chirurgia (minore/maggiore)",
        "Precedenti esperienze chirurgiche (Sì/No)","Presenza genitore (Sì/No)",
        "Midazolam pre-op (Y/N, dose)",
        "m-YPAS T1 Activity","m-YPAS T1 Emotional","m-YPAS T1 Arousal","m-YPAS T1 Vocalization","m-YPAS T1 Parents","m-YPAS T1 Totale",
        "m-YPAS T2 Activity","m-YPAS T2 Emotional","m-YPAS T2 Arousal","m-YPAS T2 Vocalization","m-YPAS T2 Parents","m-YPAS T2 Totale",
        "ICC (Induzione)","Note"
    ]
    with st.form("baseline_form"):
        c1,c2,c3,c4 = st.columns(4)
        pid = c1.text_input("ID Paziente")
        eta = c2.number_input("Età", min_value=0, max_value=18, step=1)
        sesso = c3.selectbox("Sesso", ["M","F","Altro"])
        asa = c4.selectbox("ASA", ["I","II","III","IV"])
        c5,c6 = st.columns(2)
        tipo = c5.selectbox("Tipo chirurgia", ["Minore","Maggiore"])
        prev = c6.selectbox("Precedenti esperienze chirurgiche", ["Sì","No"])
        c7,c8 = st.columns(2)
        gen = c7.selectbox("Presenza genitore", ["Sì","No"])
        mid = c8.text_input("Midazolam pre-op (Y/N, dose)")

        st.subheader("m-YPAS T1 (Holding)")
        t1c1,t1c2 = st.columns(2)
        a1 = t1c1.number_input("Activity (T1)", 0, 100, step=1)
        e1 = t1c2.number_input("Emotional expressivity (T1)", 0, 100, step=1)
        t1c3,t1c4 = st.columns(2)
        ar1 = t1c3.number_input("State of arousal (T1)", 0, 100, step=1)
        v1 = t1c4.number_input("Vocalization (T1)", 0, 100, step=1)
        p1 = st.number_input("Use of parents (T1)", 0, 100, step=1)
        tot1 = st.number_input("Totale T1", 0, 100, step=1)

        st.subheader("m-YPAS T2 (Induzione)")
        t2c1,t2c2 = st.columns(2)
        a2 = t2c1.number_input("Activity (T2)", 0, 100, step=1)
        e2 = t2c2.number_input("Emotional expressivity (T2)", 0, 100, step=1)
        t2c3,t2c4 = st.columns(2)
        ar2 = t2c3.number_input("State of arousal (T2)", 0, 100, step=1)
        v2 = t2c4.number_input("Vocalization (T2)", 0, 100, step=1)
        p2 = st.number_input("Use of parents (T2)", 0, 100, step=1)
        tot2 = st.number_input("Totale T2", 0, 100, step=1)

        icc = st.number_input("ICC (Induzione)", 0, 100, step=1)
        note = st.text_area("Note")
        submitted = st.form_submit_button("Salva CRF + Genera PDF")
    if submitted:
        row = {
            "ID Paziente": pid, "Età": eta, "Sesso": sesso, "ASA": asa,
            "Tipo chirurgia (minore/maggiore)": tipo,
            "Precedenti esperienze chirurgiche (Sì/No)": prev,
            "Presenza genitore (Sì/No)": gen,
            "Midazolam pre-op (Y/N, dose)": mid,
            "m-YPAS T1 Activity": a1, "m-YPAS T1 Emotional": e1, "m-YPAS T1 Arousal": ar1, "m-YPAS T1 Vocalization": v1, "m-YPAS T1 Parents": p1, "m-YPAS T1 Totale": tot1,
            "m-YPAS T2 Activity": a2, "m-YPAS T2 Emotional": e2, "m-YPAS T2 Arousal": ar2, "m-YPAS T2 Vocalization": v2, "m-YPAS T2 Parents": p2, "m-YPAS T2 Totale": tot2,
            "ICC (Induzione)": icc, "Note": note
        }
        df = append_row(BASE_PATH, row, columns)
        pdf_out = os.path.join(DATA_DIR, f"PDF_mYPAS_ICC_{pid or 'anonimo'}.pdf")
        build_mypas_icc_pdf(pdf_out, row)
        st.success("CRF salvata. PDF generato.")
        with open(pdf_out, "rb") as f:
            st.download_button("Scarica PDF m-YPAS/ICC", data=f, file_name=os.path.basename(pdf_out), mime="application/pdf")

    df = init_table(BASE_PATH, columns)
    st.dataframe(df, use_container_width=True)
    st.download_button("Scarica CSV", data=download_df(df), file_name="CRF_Baseline.csv", mime="text/csv")

# ---------- Medicazioni ----------
elif page == "Medicazioni":
    st.header("Medicazioni Post-Operatorie")
    MED_PATH = os.path.join(DATA_DIR, "CRF_Medicazioni_Dolore.xlsx")
    columns = [
        "ID Paziente", "Data", "Giorno post-op", "N° medicazione",
        "Tipo scala dolore (Wong-Baker/FLACC)",
        "Wong-Baker (0-10)",
        "FLACC - Face (0-2)", "FLACC - Legs (0-2)", "FLACC - Activity (0-2)",
        "FLACC - Cry (0-2)", "FLACC - Consolability (0-2)", "FLACC Totale (0-10)",
        "HR (bpm)", "SpO2 (%)", "Durata procedura (min)",
        "Analgesici rescue (farmaco/dose/orario)",
        "Interruzioni (Sì/No, motivi)",
        "Uso VR durante medicazione (Sì/No)",
        "Eventi avversi (nausea/cefalea/altro)",
        "Soddisfazione bambino (1-5)", "Soddisfazione genitore (1-5)",
        "Operatore presente (sigla/ruolo)", "Note"
    ]
    with st.form("med_form"):
        c1,c2,c3,c4 = st.columns(4)
        pid = c1.text_input("ID Paziente")
        data = c2.date_input("Data")
        gpo = c3.text_input("Giorno post-op")
        nmed = c4.number_input("N° medicazione", 1, 10, 1)
        scala = st.selectbox("Tipo scala dolore", ["Wong-Baker","FLACC","Entrambe"])
        c5,c6 = st.columns(2)
        wb = c5.number_input("Wong-Baker (0-10)", 0, 10, step=1)
        fl_face = c6.number_input("FLACC - Face (0-2)", 0, 2, step=1)
        c7,c8,c9 = st.columns(3)
        fl_legs = c7.number_input("FLACC - Legs (0-2)", 0, 2, step=1)
        fl_act = c8.number_input("FLACC - Activity (0-2)", 0, 2, step=1)
        fl_cry = c9.number_input("FLACC - Cry (0-2)", 0, 2, step=1)
        fl_con = st.number_input("FLACC - Consolability (0-2)", 0, 2, step=1)
        fl_tot = fl_face + fl_legs + fl_act + fl_cry + fl_con
        st.info(f"FLACC Totale (automatico): {fl_tot}")
        c10,c11,c12 = st.columns(3)
        hr = c10.number_input("HR (bpm)", 0, 220, step=1)
        spo2 = c11.number_input("SpO2 (%)", 0, 100, step=1)
        dur = c12.number_input("Durata procedura (min)", 0, 300, step=1)
        analg = st.text_input("Analgesici rescue (farmaco/dose/orario)")
        interr = st.text_input("Interruzioni (Sì/No, motivi)")
        uso_vr = st.selectbox("Uso VR durante medicazione", ["Sì","No"])
        ea = st.text_input("Eventi avversi (nausea/cefalea/altro)")
        c13,c14 = st.columns(2)
        s_bimbo = c13.slider("Soddisfazione bambino (1-5)", 1, 5, 3)
        s_gen = c14.slider("Soddisfazione genitore (1-5)", 1, 5, 3)
        oper = st.text_input("Operatore presente (sigla/ruolo)")
        note = st.text_area("Note")
        submitted = st.form_submit_button("Salva CRF + Genera PDF")
    if submitted:
        row = {
            "ID Paziente": pid, "Data": pd.to_datetime(data), "Giorno post-op": gpo, "N° medicazione": nmed,
            "Tipo scala dolore (Wong-Baker/FLACC)": scala, "Wong-Baker (0-10)": wb,
            "FLACC - Face (0-2)": fl_face, "FLACC - Legs (0-2)": fl_legs, "FLACC - Activity (0-2)": fl_act,
            "FLACC - Cry (0-2)": fl_cry, "FLACC - Consolability (0-2)": fl_con, "FLACC Totale (0-10)": fl_tot,
            "HR (bpm)": hr, "SpO2 (%)": spo2, "Durata procedura (min)": dur,
            "Analgesici rescue (farmaco/dose/orario)": analg,
            "Interruzioni (Sì/No, motivi)": interr, "Uso VR durante medicazione (Sì/No)": uso_vr,
            "Eventi avversi (nausea/cefalea/altro)": ea,
            "Soddisfazione bambino (1-5)": s_bimbo, "Soddisfazione genitore (1-5)": s_gen,
            "Operatore presente (sigla/ruolo)": oper, "Note": note
        }
        df = append_row(MED_PATH, row, columns)
        pdf_out = os.path.join(DATA_DIR, f"PDF_Medicazione_{pid or 'anonimo'}_{nmed}.pdf")
        build_medicazione_pdf(pdf_out, row)
        st.success("CRF salvata. PDF generato.")
        with open(pdf_out, "rb") as f:
            st.download_button("Scarica PDF Medicazione", data=f, file_name=os.path.basename(pdf_out), mime="application/pdf")

    df = init_table(MED_PATH, columns)
    st.dataframe(df, use_container_width=True)
    st.download_button("Scarica CSV", data=download_df(df), file_name="CRF_Medicazioni.csv", mime="text/csv")

# ---------- Randomization (placeholder semplice) ----------
else:
    st.header("Randomization (semplice)")
    st.info("Per la Cloud demo: gestisci la randomizzazione con il foglio Excel locale e caricalo come allegato nella pagina Screening.")
    st.write("In alternativa possiamo collegare Google Sheets per avere un registro condiviso sempre online.")
