
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm

def _table(data, col_widths, header_rows=None):
    t = Table(data, colWidths=col_widths)
    style = [("GRID",(0,0),(-1,-1),0.5,colors.black)]
    if header_rows:
        for r in header_rows:
            style.append(("BACKGROUND",(0,r),(-1,r),colors.lightgrey))
    t.setStyle(TableStyle(style))
    return t

def build_mypas_icc_pdf(path, record):
    doc = SimpleDocTemplate(path, pagesize=A4)
    styles = getSampleStyleSheet()
    elems = []
    elems.append(Paragraph("<b>Scheda m-YPAS & ICC (Baseline)</b>", styles["Title"]))
    elems.append(Spacer(1,8))

    info = [
        ["ID:", record.get("ID Paziente",""), "Età:", record.get("Età",""), "Sesso:", record.get("Sesso",""), "ASA:", record.get("ASA","")],
        ["Tipo chir. (min/mag):", record.get("Tipo chirurgia (minore/maggiore)",""),
         "Genitore (S/N):", record.get("Presenza genitore (Sì/No)",""),
         "Midazolam (Y/N, dose):", record.get("Midazolam pre-op (Y/N, dose)","")],
    ]
    elems.append(_table(info, [30*mm, 25*mm, 20*mm, 25*mm, 20*mm, 20*mm, 15*mm, 25*mm]))

    elems.append(Spacer(1,8))
    mypas = [
        ["m-YPAS T1 (Holding)", "Score"],
        ["Activity", record.get("m-YPAS T1 Activity","")],
        ["Emotional expressivity", record.get("m-YPAS T1 Emotional","")],
        ["State of arousal", record.get("m-YPAS T1 Arousal","")],
        ["Vocalization", record.get("m-YPAS T1 Vocalization","")],
        ["Use of parents", record.get("m-YPAS T1 Parents","")],
        ["Totale T1", record.get("m-YPAS T1 Totale","")],
        ["",""],
        ["m-YPAS T2 (Induzione)", "Score"],
        ["Activity", record.get("m-YPAS T2 Activity","")],
        ["Emotional expressivity", record.get("m-YPAS T2 Emotional","")],
        ["State of arousal", record.get("m-YPAS T2 Arousal","")],
        ["Vocalization", record.get("m-YPAS T2 Vocalization","")],
        ["Use of parents", record.get("m-YPAS T2 Parents","")],
        ["Totale T2", record.get("m-YPAS T2 Totale","")],
    ]
    elems.append(_table(mypas, [90*mm, 40*mm], header_rows=[0,8]))

    elems.append(Spacer(1,8))
    icc = [
        ["ICC - Induction Compliance Checklist", ""],
        ["Punteggio totale:", record.get("ICC (Induzione)","")],
        ["Note comportamento:", record.get("Note","")],
    ]
    elems.append(_table(icc, [90*mm, 90*mm], header_rows=[0]))

    doc.build(elems)

def build_medicazione_pdf(path, record):
    doc = SimpleDocTemplate(path, pagesize=A4)
    styles = getSampleStyleSheet()
    elems = []
    elems.append(Paragraph("<b>Scheda Medicazione – Dolore/Ansia</b>", styles["Title"]))
    elems.append(Spacer(1,8))

    info = [
        ["ID:", record.get("ID Paziente",""), "Data:", record.get("Data",""), "Giorno post-op:", record.get("Giorno post-op","")],
        ["N° medicazione:", record.get("N° medicazione",""), "Operatore:", record.get("Operatore presente (sigla/ruolo)",""), "Uso VR (S/N):", record.get("Uso VR durante medicazione (Sì/No)","")],
    ]
    elems.append(_table(info, [30*mm, 25*mm, 25*mm, 25*mm, 40*mm, 25*mm]))

    elems.append(Spacer(1,6))
    wb = [["Wong-Baker (0-10):", record.get("Wong-Baker (0-10)","")]]
    elems.append(_table(wb, [50*mm, 100*mm], header_rows=[0]))

    elems.append(Spacer(1,6))
    flacc = [
        ["FLACC", "Face", "Legs", "Activity", "Cry", "Consolability", "Totale"],
        ["Punteggi", record.get("FLACC - Face (0-2)",""), record.get("FLACC - Legs (0-2)",""),
         record.get("FLACC - Activity (0-2)",""), record.get("FLACC - Cry (0-2)",""),
         record.get("FLACC - Consolability (0-2)",""), record.get("FLACC Totale (0-10)","")],
    ]
    elems.append(_table(flacc, [25*mm, 20*mm, 20*mm, 25*mm, 20*mm, 35*mm, 25*mm], header_rows=[0]))

    elems.append(Spacer(1,6))
    vit = [["HR (bpm):",record.get("HR (bpm)",""), "SpO2 (%):",record.get("SpO2 (%)",""), "Durata (min):",record.get("Durata procedura (min)","")]]
    elems.append(_table(vit, [30*mm, 20*mm, 30*mm, 20*mm, 40*mm, 20*mm]))

    elems.append(Spacer(1,6))
    rows = [
        ["Analgesici rescue:", record.get("Analgesici rescue (farmaco/dose/orario)","")],
        ["Interruzioni:", record.get("Interruzioni (Sì/No, motivi)","")],
        ["Eventi avversi:", record.get("Eventi avversi (nausea/cefalea/altro)","")],
        ["Soddisf. bambino (1-5):", record.get("Soddisfazione bambino (1-5)",""),
         "Soddisf. genitore (1-5):", record.get("Soddisfazione genitore (1-5)","")],
        ["Note:", record.get("Note","")],
    ]
    for r in rows:
        if len(r)==2:
            elems.append(_table([r], [50*mm, 120*mm]))
        else:
            elems.append(_table([r], [50*mm, 20*mm, 50*mm, 20*mm]))
    doc.build(elems)
