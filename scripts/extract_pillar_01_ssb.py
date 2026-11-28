# -*- coding: utf-8 -*-
"""
Full-Text Extractor for Pillar 01: Stuttgarter Straßenbahnen AG (SSB)
Target: C:\\Users\\SHQIPTAR634\\Documents\\Obsidian Vault\\03_SAP_EnterpriseArchitecture
"""
import os
import docx
import datetime

WS_DIR = r"c:\Users\SHQIPTAR634\Desktop\SSB Dateien"
VAULT_DIR = r"C:\Users\SHQIPTAR634\Documents\Obsidian Vault"

def write_vault_note(relative_path, content):
    full_path = os.path.join(VAULT_DIR, relative_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"[OK] Wrote note: {relative_path} ({len(content)} chars)")

def extract_docx_paras(filepath):
    if not os.path.exists(filepath):
        return []
    doc = docx.Document(filepath)
    return [p.text.strip() for p in doc.paragraphs if p.text.strip()]

def run_ssb_extraction():
    print("\n=== STARTING PILLAR 01 (SSB) FULL-TEXT EXTRACTION ===")
    
    # 1. Solution Design Document (SDD)
    sdd_path = os.path.join(WS_DIR, "01_SSB", "02_Teilprojekte_TP1_bis_TP5", "TP2_Kaufmaennische_Prozesse", "Explore_Phase", "SSB Lösungsdesign", "SSB Lösungsdesign Dokument.docx")
    sdd_paras = extract_docx_paras(sdd_path)
    
    # Format SDD content with markdown headings where detected
    formatted_sdd_lines = []
    for p in sdd_paras:
        if p.startswith("Lösungs-Design") or p.startswith("Architektur-Design"):
            formatted_sdd_lines.append(f"\n# {p}\n")
        elif p.startswith("Aspekte zu") or p.startswith("Geschäftsfähigkeiten") or p.startswith("Die SAP") or p.startswith("SAP Systemlandschaft") or p.startswith("Angebundene Systeme") or p.startswith("Übersicht über die WRICEF"):
            formatted_sdd_lines.append(f"\n## {p}\n")
        elif any(p.startswith(prefix) for prefix in ["Kostenrechnungskreis", "Buchungskreise", "Ergebnisbereich", "Werke", "Lagerorte", "Verkaufsorganisation", "Einkaufsorganisation", "Instandhaltung", "Kontenplan", "Kostenstellen", "Profit Center", "PSP-Elemente"]):
            formatted_sdd_lines.append(f"\n### {p}\n")
        else:
            formatted_sdd_lines.append(p)
            
    sdd_fulltext = "\n\n".join(formatted_sdd_lines)
    
    note_sdd = f"""---
title: "SSB Solution Design Document (SDD) – Volltext-Dossier"
program: "SAP4SSB"
phase: "Explore-Phase (100% finalisiert & genehmigt)"
source_file: "file:///{sdd_path.replace('\\', '/')}"
partner: "Nagarro Enterprise Services & Axians"
tags:
  - ssb
  - s4hana
  - solution_design
  - clean_core
  - architecture
  - wricef
---

# 📐 SSB Solution Design Document (SDD) – Volltext & Architektur-Referenz

> [!IMPORTANT] **Meilenstein-Status bei Austritt von Visar Murseli**
> Dieses Dokument repräsentiert den **vollständig abgeschlossenen und vom Lenkungsausschuss (Steering Board) freigegebenen Stand der Explore-Phase**.
> Es definiert verbindlich alle Organisationsstrukturen, Stammdaten-Harmonisierungen (CVI), Finanzstrukturen (Trennungsrechnung EU 1370/2007), BTP-Schnittstellen und WRICEF-Objekte für den Übergang in die Realize-Phase (WBS 197–202).

---

## 🏛️ Executive Summary der Lösungsarchitektur
1. **ERP-Zielsystem:** SAP S/4HANA Private Cloud Edition im RISE-Betriebsmodell mit modularen Side-by-Side-Erweiterungen auf der SAP BTP.
2. **Kaufmännische Kernarchitektur:**
   - **Trennungsrechnung nach EU-VO 1370/2007 & § 45a PBefG:** Strikte buchhalterische und kostenrechnerische Trennung eigenwirtschaftlicher Verkehre von gemeinwirtschaftlichen, öffentlich bezuschussten Verkehren zur Vermeidung unzulässiger Quersubventionierungen.
   - **Parallel-Ledger im Universal Journal (ACDOCA):** Führendes Hauptbuch `0L` (Handelsrecht nach HGB) und paralleles Ledger `2L` (Steuerrecht).
   - **Projekt- und Kostenrechnung:** Hierarchische Mehrjahres-Investitionssteuerung über **PSP-Elemente** im Projektsystem (PS) in Kombination mit Grants Management (GM for Grantee); operative Werkstatt- und Reparaturaufträge über **Innenaufträge**.
3. **Clean Core & Integrationsarchitektur:**
   - Striktes Verbot von Modifikationen im Kern.
   - Entkopplung proprietärer Subsysteme (Vertriebssystem PATRIS, Rechnungsworkflow xSuite, Dokumentenarchiv d.velop) über REST/OData APIs und die SAP BTP Integration Suite.

---

## 📜 Volltext-Extraktion aus dem Original-Lösungsdesign (794 Absätze)

{sdd_fulltext}

---

## 🔗 Verknüpfungen im Wissensnetz
- [[03_SAP_EnterpriseArchitecture/SSB_Migration_Volltext]]
- [[03_SAP_EnterpriseArchitecture/01_Architektur_Technik/Clean_Core_Paradigma]]
- [[03_SAP_EnterpriseArchitecture/02_Kaufmaennische_Prozesse/Trennungsrechnung_OEPNV_EU1370]]
- [[03_SAP_EnterpriseArchitecture/02_Kaufmaennische_Prozesse/Universal_Journal_ACDOCA]]
- [[03_SAP_EnterpriseArchitecture/SSB_Interviews_Experten_Transkripte]]
"""
    write_vault_note("03_SAP_EnterpriseArchitecture/SSB_Solution_Design_Volltext.md", note_sdd)

    # 2. Migrationskonzept Volltext
    mig_path = os.path.join(WS_DIR, "01_SSB", "04_Architektur_Methoden_Tools", "Datenmigration_LTMC", "Migrationskonzept v0 1 2025_04_28.docx")
    mig_paras = extract_docx_paras(mig_path)
    mig_fulltext = "\n\n".join(mig_paras)
    
    note_mig = f"""---
title: "SSB Datenmigrationskonzept (LTMC & CVI) – Volltext-Dossier"
program: "SAP4SSB"
method: "SAP Migration Cockpit (Staging-Tabellen-Architektur)"
source_file: "file:///{mig_path.replace('\\', '/')}"
partner: "Nagarro Enterprise Services"
tags:
  - ssb
  - datenmigration
  - ltmc
  - cvi
  - saldo_null
---

# 🔄 SSB Datenmigrationskonzept – Volltext & Cutover-Architektur

> [!IMPORTANT] **Revisionssicherer Eröffnungsbilanz-Abgleich**
> Das fundamentale Prüfkriterium für Wirtschaftsprüfer im Finanzbereich (FI) ist das **Datenübernahmekonto**:
> Nach Übernahme aller Sachkontensalden, offenen Posten (OP) und Anlagenbuchwerte (FI-AA) muss das zentrale Übernahmekonto centgenau den **Saldo von 0,00 €** aufweisen.

---

## 📋 Kernaspekte der Datenmigration bei der SSB AG
1. **Migrationswerkzeug:** SAP S/4HANA Migration Cockpit (LTMC / Migrate Your Data Fiori App) mit dedizierten **Staging-Tabellen** auf der HANA-Datenbank.
2. **Migrationspfad:** Selektive Extraktion aus dem 20 Jahre gewachsenen SAP ECC 6.0, automatisierte Bereinigung historischer Z-Strukturen, Transformation über Mapping-Tabellen und iteratives Laden in die Ziel-Sandbox ES4.400 bzw. QS4.100.
3. **Customer Vendor Integration (CVI):**
   - Historisch getrennte Debitoren (KNA1) und Kreditoren (LFA1) werden zum zentralen **SAP Business Partner** harmonisiert.
   - Zuordnung standardisierter Rollen (`FLCU00` für Debitor FI, `FLVN00` für Kreditor FI).
4. **Cutover-Vorgehensmodell:**
   - Iteration 1: Stammdaten (Kostenstellen, Profit Center, Sachkonten, Business Partner, Anlagenstammsätze).
   - Iteration 2: Historische Bewegungsdaten & offene Posten zum Stichtag.
   - Iteration 3: Delta-Load und SuSa-Bilanzabgleich (Summen- und Saldenliste) gegen 0,00 € Übernahmekonto.

---

## 📜 Extrahierter Volltext aus dem Migrationskonzept (296 Absätze)

{mig_fulltext}

---

## 🔗 Verknüpfungen im Wissensnetz
- [[03_SAP_EnterpriseArchitecture/01_Architektur_Technik/SAP_Migration_Cockpit_LTMC]]
- [[03_SAP_EnterpriseArchitecture/01_Architektur_Technik/Customer_Vendor_Integration_CVI]]
- [[03_SAP_EnterpriseArchitecture/SSB_Solution_Design_Volltext]]
"""
    write_vault_note("03_SAP_EnterpriseArchitecture/SSB_Migration_Volltext.md", note_mig)

    # 3. Tool-Governance: CALM & Enable Now
    calm_path = os.path.join(WS_DIR, "01_SSB", "04_Architektur_Methoden_Tools", "SAP_Cloud_ALM", "20251107_SAP_CALM_How2handle_quickguide.docx")
    calm_paras = extract_docx_paras(calm_path)
    
    sr_path = os.path.join(WS_DIR, "01_SSB", "01_Gesamtprojekt_SAP4SSB_Governance", "01_Projektleitung_PMO_Masterplan", "PMO_Arbeitsordner", "Spielregeln CALM.docx")
    sr_paras = extract_docx_paras(sr_path)
    
    en_path = os.path.join(WS_DIR, "01_SSB", "04_Architektur_Methoden_Tools", "SAP_Enable_Now", "SAP Enable Now Übergabe.docx")
    en_paras = extract_docx_paras(en_path)
    
    note_tools = f"""---
title: "SSB Tool-Governance & Enablement: CALM, Signavio & Enable Now"
author: "Visar Murseli (IT-PMO)"
program: "SAP4SSB"
tags:
  - ssb
  - tool_governance
  - cloud_alm
  - signavio
  - enable_now
---

# 🛠️ SSB Tool-Governance – Handbücher & Richtlinien von Visar Murseli

> [!SUMMARY] **Operative Verantwortung im IT-PMO**
> Visar Murseli verantwortete die toolgestützte Prozess- und Test-Governance im Programm SAP4SSB.
> Dies umfasste das Verfassen des verbindlichen Onboarding-Quickguides für **SAP Cloud ALM**, die Definition der **Spielregeln für Anforderungen und Testfälle** sowie das strategische **Übergabekonzept von SAP Enable Now** von der IT an die Personalentwicklung.

---

## 1. SAP Cloud ALM How2Handle & Spielregeln (Volltext)

### Handlungsleitfaden für Berater & Teilprojektleiter
{chr(10).join(calm_paras)}

### Verbindliche Spielregeln für CALM (Aufgaben, Testfälle, Stories)
{chr(10).join(sr_paras)}

---

## 2. Strategisches Übergabekonzept SAP Enable Now (Volltext)

### Kontext & Single-Source-Content-Strategie
{chr(10).join(en_paras)}

---

## 🔗 Verknüpfungen im Wissensnetz
- [[03_SAP_EnterpriseArchitecture/SSB_Grossprojekt_SAP4SSB]]
- [[03_SAP_EnterpriseArchitecture/04_Change_Enablement/Key_User_Enablement_EnableNow]]
- [[03_SAP_EnterpriseArchitecture/03_Governance_Vergabe/Toolkette_Signavio_CALM_EnableNow]]
"""
    write_vault_note("03_SAP_EnterpriseArchitecture/SSB_Tool_Governance_CALM_EnableNow_Volltext.md", note_tools)

    # 4. Experten-Interviews Transkripte Dossier
    trans_dir = os.path.join(WS_DIR, "02_Master", "Masterarbeit Wirtschaftsinformatik", "3-Transkripte")
    
    tw_text = "\n\n".join(extract_docx_paras(os.path.join(trans_dir, "Interviewpartner 1 - TW.docx")))
    rn_text = "\n\n".join(extract_docx_paras(os.path.join(trans_dir, "Interviewpartner 2 - RN.docx")))
    hg_text = "\n\n".join(extract_docx_paras(os.path.join(trans_dir, "Interviewpartner 5 - HG.docx")))
    ah_text = "\n\n".join(extract_docx_paras(os.path.join(trans_dir, "Interviewpartner 9 - AH.docx")))
    
    note_transcripts = f"""---
title: "Experten-Interviews Transkripte (Großprojekt SAP4SSB)"
author: "Visar Murseli (Masterarbeit Note 1,0)"
interviewees:
  - "Roland Nowak (Gesamtprojektleiter SAP4SSB)"
  - "Thomas Wimpff (TPL TP2 Finance & Controlling)"
  - "Armin Heinrich (Enterprise Basisarchitekt SSB)"
  - "Henning Gerdes (Lead Architect Axians ES4)"
methodology: "Qualitative Inhaltsanalyse nach Mayring"
tags:
  - interviews
  - empirie
  - ssb
  - nowak
  - wimpff
  - heinrich
  - gerdes
  - mayring
---

# 🎙️ Experten-Interviews Transkripte – Großprojekt SAP4SSB

> [!INFO] **Wissenschaftliche Primärquelle der Masterarbeit (Note 1,0)**
> Diese Transkripte dokumentieren die empirische Feldarbeit von Visar Murseli im Rahmen seiner Masterarbeit am Lehrstuhl von Prof. Herzwurm.
> Sie liefern unschätzbare Primäreinblicke in die tatsächlichen Reibungspunkte, Governance-Strukturen und Architektur-Entscheidungen der S/4HANA Transformation.

---

# 1. Interviewpartner 2 (IP2 / RN): Roland Nowak – Gesamtprojektleiter SAP4SSB
- **Datum:** 28.11.2025 | **Dauer:** ca. 50 Min.
- **Rolle:** Gesamtprojektleiter S/4HANA Transformation (Leiter Projektleitungspool)
- **Schwerpunkte:** Multiprojekt-Steuerung (TP1–TP5), C-Level Steering Board, Betriebsrat-Mitbestimmung (§ 87 BetrVG), Scope Governance im Fit-to-Standard.

### Vollständiges Interviewtranskript:
{rn_text}

---

# 2. Interviewpartner 1 (IP1 / TW): Thomas Wimpff – TPL TP2 Finance & Controlling
- **Datum:** 28.11.2025 | **Dauer:** ca. 28 Min.
- **Rolle:** Teilprojektleiter kaufmännische Prozesse (Unternehmensbereichsleiter Steuerung)
- **Schwerpunkte:** Trennungsrechnung (EU 1370/2007), Universal Journal (ACDOCA), Ablösung von Innenaufträgen durch PSP-Elemente, Eröffnungsbilanz-Abgleich.

### Vollständiges Interviewtranskript:
{tw_text}

---

# 3. Interviewpartner 9 (IP9 / AH): Armin Heinrich – Enterprise Basisarchitekt SSB
- **Datum:** 02.12.2025 | **Dauer:** ca. 57 Min.
- **Rolle:** Enterprise- und Basisarchitekt der SSB AG
- **Schwerpunkte:** BTP-Zielarchitektur, SSO-Integration mit Microsoft Entra ID, Schnittstellenabsicherung, Mandantenlandschaft ES4/QS4/PS4.

### Vollständiges Interviewtranskript:
{ah_text}

---

# 4. Interviewpartner 5 (IP5 / HG): Henning Gerdes – Lead Architect Axians ES4
- **Datum:** 08.12.2025 | **Dauer:** ca. 35 Min.
- **Rolle:** Lead Solution Architect (Infrastruktur- und Basispartner Axians)
- **Schwerpunkte:** Bereitstellung Private Cloud Infrastruktur, Adobe Document Services (ADS) Formulare, Transportkonsolidierung.

### Vollständiges Interviewtranskript:
{hg_text}

---

## 🔗 Verknüpfungen im Wissensnetz
- [[02_Wirtschaftsinformatik_300ECTS/Modul_Masterarbeit]]
- [[03_SAP_EnterpriseArchitecture/SSB_Solution_Design_Volltext]]
- [[03_SAP_EnterpriseArchitecture/03_Governance_Vergabe/Betriebsvereinbarungen_Mitbestimmung_Detail]]
"""
    write_vault_note("03_SAP_EnterpriseArchitecture/SSB_Interviews_Experten_Transkripte.md", note_transcripts)

    # 5. Betriebsrat & Mitbestimmung Volltext
    br_path = os.path.join(WS_DIR, "01_SSB", "01_Gesamtprojekt_SAP4SSB_Governance", "01_Projektleitung_PMO_Masterplan", "Projektleiter_Ordner", "Entwurf_Modulbeschreibung_SAP_S4HANA.docx")
    br_paras = extract_docx_paras(br_path)
    br_fulltext = "\n\n".join(br_paras)
    
    note_br = f"""---
title: "SSB Mitbestimmung & Betriebsrat-Governance – Volltext-Dossier"
program: "SAP4SSB"
law: "§ 87 Abs. 1 Nr. 6 BetrVG"
stakeholders: "Betriebsrat SSB (Schmidt & Kraus), Gesamt-PL Nowak, IT-Leiter Fillinger"
source_file: "file:///{br_path.replace('\\', '/')}"
tags:
  - ssb
  - betriebsrat
  - mitbestimmung
  - datenschutz
  - pilot_bv
  - finale_bv
---

# 🏛️ SSB Betriebsrat-Governance – Modulbeschreibungen & Mitbestimmung

> [!IMPORTANT] **Historische Meilensteine im Masterplan**
> 1. **Vorgang 294 (01.04.2026):** **Pilot-Betriebsvereinbarung** in Kraft für den Testbetrieb mit Echtdaten (UAT auf System QS4.210).
> 2. **Vorgang 297 (01.01.2027):** **Finale Betriebsvereinbarung** in Kraft exakt zum produktiven Go-Live Neujahr 2027.

---

## 📜 Volltext der offiziellen Modulbeschreibung für den Betriebsrat (215 Absätze)
Dieses Dokument definiert detailliert, welche Daten in den einzelnen S/4HANA-Modulen (FI, CO, SD, MM, PM, EHS, Treasury, Fiori) verarbeitet werden und welche Schutzmaßnahmen gegen missbräuchliche Verhaltens- und Leistungskontrollen greifen:

{br_fulltext}

---

## 🔗 Verknüpfungen im Wissensnetz
- [[03_SAP_EnterpriseArchitecture/03_Governance_Vergabe/Betriebsvereinbarungen_Mitbestimmung_Detail]]
- [[03_SAP_EnterpriseArchitecture/03_Governance_Vergabe/TP5_Gesamtsteuerung_PMO_Betriebsvereinbarung_Plan]]
- [[03_SAP_EnterpriseArchitecture/SSB_Interviews_Experten_Transkripte]]
"""
    write_vault_note("03_SAP_EnterpriseArchitecture/SSB_Mitbestimmung_Betriebsrat_Dossier.md", note_br)

if __name__ == "__main__":
    run_ssb_extraction()
