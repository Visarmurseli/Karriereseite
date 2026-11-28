# -*- coding: utf-8 -*-
"""
Generate and inject the comprehensive 40+ Q&A catalog into portal_builder/vue_app.py
"""
import re

qa_data = [
    # --- KATEGORIE 1: SSB S/4HANA & EXPLORE-PHASE (10 Fragen) ---
    {
        "q": "Was genau war Ihre Rolle bei der SSB AG und wie war das Transformationsprogramm SAP4SSB strukturiert?",
        "cat": "SSB S/4HANA & Explore-Phase",
        "open": True,
        "a": "Ich war 24 Monate lang als Werkstudent im IT-PMO (Teilprojekt 5: Gesamtsteuerung & Architektur) unter Gesamtprojektleiter Roland Nowak und IT-Leiter Dietmar Fillinger tätig.\n\nDas Programm SAP4SSB gliederte sich in 5 disjunkte Teilprojekte:\n- TP1: Change Management & Enablement (Rollout SAP Enable Now, Coffee Corners, Key-User-Befähigung)\n- TP2: Kaufmännische Prozesse & Solution Design (FI/CO/MM/RE-FX mit Nagarro ES)\n- TP3: Technische Prozesse & Asset Management (Instandhaltung Stadtbahn/Busse/Fahrleitung mit Evora & Nagarro)\n- TP4: IT-Unterstützung & Systemlandschaft (4-System-Landschaft ES4/QS4/PS4 mit Axians)\n- TP5: Gesamtsteuerung, PMO, Vergabe & Mitbestimmung mit Betriebsrat\n\nMeine Aufgabe war die operative Klammer: Tool-Governance (Quickguide für SAP Cloud ALM, Enable Now Übergabekonzept), Analyse der Migrationsobjekte und Statusreporting für den Lenkungsausschuss.",
        "do": "Betone die 24 Monate Laufzeit, die 5 Teilprojekte (TP1-TP5) und konkrete Artefakte (CALM How2Handle, Enable Now Konzept).",
        "dont": "Stelle dich nicht als reiner Zuarbeiter dar – du hast Governance-Vorgaben aktiv erarbeitet und bereichsübergreifend abgestimmt!"
    },
    {
        "q": "Welcher Meilenstein markierte Ihren Projektaustritt bei der SSB und wie ging es danach weiter?",
        "cat": "SSB S/4HANA & Explore-Phase",
        "open": False,
        "a": "Mein Austritt erfolgte zum formalen und erfolgreichen Abschluss der Explore-Phase:\nDas umfassende Solution Design Document (SDD) für die kaufmännischen und technischen Prozesse (inklusive aller Prozessmodelle in Signavio, Schnittstellenmatrizen und WRICEFA-Entwicklungsobjekte) war zu 100% finalisiert und vom Lenkungsausschuss (Steering Board) abgenommen.\n\nDer unmittelbar anschließende nächste Projektschritt war der Eintritt in die Realize-Phase (WBS 197-202): Das Customizing im System, die Bereitstellung des Integrations-Testsystems QS4.100 durch Axians, die iterative Datenmigration via LTMC-Staging-Tabellen und die Vorbereitung der Pilot-Betriebsvereinbarung zum 01.04.2026 für die End-to-End-Tests.",
        "do": "Nenne den exakten Meilenstein: SDD vollständig finalisiert & genehmigt, formaler Explore-Abschluss, direkter Übergang in die Realize-Phase.",
        "dont": "Verwechsle die Phasen nicht – du hast die Konzeption bis zur vollständigen Genehmigung begleitet, nicht erst mittendrin aufgehört."
    },
    {
        "q": "Was bedeutet 'Clean Core' im S/4HANA Private Cloud Kontext und wie verhindert man Wildwuchs?",
        "cat": "SSB S/4HANA & Explore-Phase",
        "open": False,
        "a": "Clean Core bedeutet, dass der ERP-Kern modifikationsfrei bleibt und ausschließlich über stabile, von SAP freigegebene Schnittstellen (APIs und CDS Views) angesprochen wird. Dadurch bleibt das System upgradefähig, was in Cloud-Releases essenziell ist.\n\nIn der Praxis teilt sich das auf:\n1. On-Stack Extensibility: Erweiterungen im Kern erfolgen nur über ABAP Cloud und das RESTful Application Programming Model (RAP).\n2. Side-by-Side Extensibility: Komplexe Eigenentwicklungen, Fiori-Frontends und Drittsystem-Integrationen laufen auf der SAP BTP.\n\nUm Wildwuchs zu verhindern, braucht es eine strikte Governance: Jede Z-Anforderung muss durch ein Architecture Review Board (ARB), in dem geprüft wird: Geht es im Best-Practice-Standard? Wenn nein, warum nicht BTP?",
        "do": "Erwähne die Unterscheidung On-Stack vs. Side-by-Side und das ARB (Architecture Review Board).",
        "dont": "Behaupte nicht, dass man bei Clean Core gar nichts mehr programmieren darf – es geht um das 'Wo' und 'Wie'!"
    },
    {
        "q": "Warum hat sich die SSB für Greenfield und nicht für eine Systemkonvertierung (Brownfield) entschieden?",
        "cat": "SSB S/4HANA & Explore-Phase",
        "open": False,
        "a": "Das bestehende SAP ECC 6.0 der SSB war über 20 Jahre historisch gewachsen und wies hunderte Z-Modifikationen, ungenutzte Altdaten und veraltete Berechtigungsstrukturen auf. Ein Brownfield-Ansatz hätte diese technische Schuld 1:1 in die neue Welt mitgeschleift und zukünftige Cloud-Upgrades massiv erschwert.\n\nMit dem Greenfield-Ansatz in einer RISE with SAP Private Cloud Edition konnte die SSB tabula rasa machen: Rückkehr zum Best-Practice-Standard durch Fit-to-Standard Workshops, Bereinigung der Stammdaten (CVI) und strikte Einhaltung des Clean-Core-Paradigmas.",
        "do": "Verwende Fachbegriffe: Technische Schuld, Modifikationsfreier Kern, Fit-to-Standard, Best-Practice-Standard.",
        "dont": "Sage nicht einfach: 'Brownfield war zu alt.' Begründe es mit Upgrade-Sicherheit und Wartungskosten."
    },
    {
        "q": "Was versteht man unter der Trennungsrechnung nach EU-Verordnung 1370/2007 im ÖPNV?",
        "cat": "SSB S/4HANA & Explore-Phase",
        "open": False,
        "a": "Die Trennungsrechnung nach EU-VO 1370/2007 und § 45a PBefG verpflichtet Verkehrsunternehmen wie die SSB, die Buchführung strikt zwischen eigenwirtschaftlichen Verkehren (z.B. kommerzieller Gelegenheitsverkehr) und gemeinwirtschaftlichen, durch die öffentliche Hand bezuschussten Verkehren (ÖPNV-Linienverkehr) zu trennen.\n\nDadurch wird europarechtlich sichergestellt, dass keine verbotenen Quersubventionierungen öffentlicher Ausgleichsleistungen in den freien Wettbewerb fließen. Im S/4HANA-Lösungsdesign (TP2) wurde dies durch eine saubere Kostenstellen-, Profit-Center- und Buchungskreis-Segmentierung sowie parallele Ledger im Hauptbuch realisiert.",
        "do": "Nenne die EU-Verordnung 1370/2007, § 45a PBefG und die Vermeidung von Quersubventionierungen.",
        "dont": "Tue nicht so, als sei Trennungsrechnung eine rein technische SAP-Einstellung – es ist eine rechtlich zwingende Compliance-Vorgabe."
    },
    {
        "q": "Was sind die architektonischen Vorteile des Universal Journal (ACDOCA) gegenüber der klassischen Tabellenwelt?",
        "cat": "SSB S/4HANA & Explore-Phase",
        "open": False,
        "a": "Im alten ECC 6.0 waren Finanzdaten auf unzählige Tabellen verteilt: BSEG und BKPF für Hauptbuch, BSIS/BSAS für offene Posten, KNC1/LFC1 für Debitoren/Kreditoren und COEP für das Controlling. Das erforderte komplexe Abstimmungsarbeiten (Reconciliation) zwischen FI und CO am Monatsende.\n\nDas Universal Journal (Tabelle ACDOCA) vereint Hauptbuch, Kostenrechnung, Anlagenbuchhaltung (FI-AA) und Material-Ledger in einer einzigen, spaltenbasierten 'Single Source of Truth' auf der SAP HANA In-Memory-Datenbank. FI und CO sind von vornherein abgestimmt; Berichte aggregieren Millionen Zeilen in Millisekunden on-the-fly.",
        "do": "Nenne konkrete Tabellen (BSEG, COEP, ACDOCA) und das Prinzip 'Single Source of Truth'.",
        "dont": "Vergiss nicht die betriebswirtschaftliche Konsequenz: Wegfall von zeitaufwändigen Abstimmungsarbeiten zum Periodenabschluss."
    },
    {
        "q": "Wie unterscheiden sich PSP-Elemente und Innenaufträge in der SSB-Kostenrechnung?",
        "cat": "SSB S/4HANA & Explore-Phase",
        "open": False,
        "a": "In der alten ECC-Welt wurden häufig Innenaufträge für alles Mögliche genutzt, was zu unübersichtlichen Auftragsfriedhöfen führte.\n\nIm S/4HANA-Lösungsdesign wurde eine klare Trennung definiert:\n- PSP-Elemente (Projektstrukturplan im Projektsystem PS): Werden für mehrjährige, investive Großprojekte genutzt (z.B. Neubau von Stadtbahntrassen, Anschaffung neuer Fahrzeugflotten). Sie erlauben hierarchische Budgetierung, Fördermittelzuordnung (Grants Management) und Abrechnung auf Anlagen im Bau (AiB).\n- Innenaufträge: Werden ausschließlich für operative, kurzfristige Gemeinkosten- oder Instandhaltungsmaßnahmen mit begrenzter Laufzeit eingesetzt.",
        "do": "Erkläre die strategische Trennung: PSP = mehrjährige Investitionen mit Budgetierung; Innenaufträge = operative Kostenverrechnung.",
        "dont": "Verwechsle nicht PS (Projektsystem) mit PM (Plant Maintenance / Instandhaltung)."
    },
    {
        "q": "Wie funktionierte die Customer Vendor Integration (CVI) bei der SSB?",
        "cat": "SSB S/4HANA & Explore-Phase",
        "open": False,
        "a": "Unter ECC gab es getrennte Stammdatensätze für Kunden (Debitoren, Tabelle KNA1) und Lieferanten (Kreditoren, Tabelle LFA1). War ein Partner beides, gab es redundante Datensätze.\n\nIn S/4HANA ist der Business Partner (Geschäftspartner) das führende Objekt. Im Rahmen der CVI haben wir die Nummernkreise und Kontengruppen harmonisiert. Ein einzelner Geschäftspartner erhält verschiedene Rollen (z.B. FLCU00 für Debitor, FLVN00 für Kreditor) unter derselben ID. Das war eine zentrale Vorbedingung für die Datenmigration mit LTMC.",
        "do": "Nenne das Führende-Objekt-Prinzip, Rollen (FLCU00, FLVN00) und die Konsolidierung redundanter Altdaten.",
        "dont": "Bezeichne CVI nicht als einfache Datenkopie – es ist eine zwingende Datenharmonisierung."
    },
    {
        "q": "Wie lief die Datenmigration mit dem SAP Migration Cockpit (LTMC) ab und warum ist das 0,00 € Saldo entscheidend?",
        "cat": "SSB S/4HANA & Explore-Phase",
        "open": False,
        "a": "Die Migration erfolgte über das SAP Migration Cockpit (LTMC) primär nach dem Staging-Tabellen-Prinzip: Altdaten aus ECC wurden in Staging-Tabellen auf der HANA-DB geladen, dort über Mapping-Regeln transformiert und validiert.\n\nIm Finanzbereich (FI) ist der Eröffnungsbilanz-Abgleich die kritischste Revisionsprüfung: Sachkontensalden, offene Posten (OP) und Anlagenbuchwerte (FI-AA) werden gegen ein zentrales Datenübernahmekonto gebucht. Nach erfolgreichem Cutover muss dieses Übernahmekonto centgenau einen Saldo von 0,00 € aufweisen. Jeder Cent Abweichung bedeutet eine unvollständige oder asynchrone Buchung, die das Testat der Wirtschaftsprüfer gefährdet.",
        "do": "Erkläre den Cutover-Ablauf: Staging -> Mappings -> Simulation -> Import -> Abstimmung des Datenübernahmekontos auf 0,00 €.",
        "dont": "Tue nicht so, als ob Datenmigration per 'Excel-Upload' erledigt wäre – es ist ein hochgradig revisionssicherer Prozess."
    },
    {
        "q": "Welche Rolle spielten die Mitbestimmungs-Meilensteine mit dem Betriebsrat?",
        "cat": "SSB S/4HANA & Explore-Phase",
        "open": False,
        "a": "In einem öffentlichen Verkehrsunternehmen unterliegt die Einführung eines ERP-Systems, das potenziell Leistungs- und Verhaltensdaten von Mitarbeitern verarbeiten kann, der zwingenden Mitbestimmung nach § 87 Abs. 1 Nr. 6 BetrVG.\n\nIm Programm SAP4SSB haben Gesamtprojektleiter Roland Nowak und IT-Leiter Dietmar Fillinger den Betriebsrat (Vorsitzende Schmidt & Kraus) von Beginn an eingebunden. Wir hatten zwei verbindliche Meilensteine im Masterplan:\n1. Pilot-Betriebsvereinbarung (01.04.2026): Regelung für den Testbetrieb mit anonymisierten/pseudonymisierten Echtdaten im UAT auf QS4.210.\n2. Finale Betriebsvereinbarung (01.01.2027): Regelung für den Produktivbetrieb zum Go-Live mit klarem Rollen- und Berechtigungskonzept.",
        "do": "Erwähne § 87 BetrVG, die Pilot-BV (01.04.2026) und die Finale BV (01.01.2027) sowie das Rollen-/Berechtigungskonzept.",
        "dont": "Unterschätze niemals die Mitbestimmung – in deutschen Konzernen ist das ein zentraler Erfolgsfaktor!"
    },

    # --- KATEGORIE 2: DATACENTER ONE & ITIL 4 (7 Fragen) ---
    {
        "q": "Welche Aufgaben hatten Sie 12 Monate lang bei Datacenter One im INOC?",
        "cat": "Datacenter One & ITIL 4",
        "open": False,
        "a": "Ich war 12 Monate lang als Werkstudent im Information Network Operation Center (INOC) unter Helmut Schmidpeter tätig.\n\nMeine Hauptaufgaben umfassten:\n- 24/7 Monitoring von Core-Netzwerken, Serverfarmen, USV-Anlagen (Unterbrechungsfreie Stromversorgung) und RZ-Klimatechnik.\n- Single Point of Contact (SPoC) für Enterprise-Kunden und Tier-1 Carrier bei Störungen nach ITIL 4 Service Operations.\n- Konzeption und Aufbau einer zentralen Wissensdatenbank in Confluence zur Prozessstandardisierung.\n- Hands-on Incident- und Problem-Management via Jira Service Management.",
        "do": "Betone die 24/7 Leitstands-Verantwortung, ITIL 4 Prinzipien und den Single Point of Contact (SPoC).",
        "dont": "Reduziere den Leitstand nicht auf 'Kabel stecken' – es ging um unternehmenskritisches SLA-Management."
    },
    {
        "q": "Wie sind Sie bei Netzwerk- und Verbindungsausfällen konkret vorgegangen?",
        "cat": "Datacenter One & ITIL 4",
        "open": False,
        "a": "Trat im PRTG-Monitoring ein Alarm auf (z.B. Packet Loss oder Leitungsunterbrechung auf einer Glasfaserstrecke), folgte das Vorgehen einer strikten Standard Operating Procedure (SOP):\n1. Verifikation & Triage: Prüfen, ob es sich um einen lokalen Port, einen Switch oder eine externe Carrier-Leitung handelt.\n2. Ticket-Erstellung: Sofortige Erfassung im Jira Service Management mit Severity-Einstufung und Zuweisung an die zuständige Carrier-Eskalationsstufe.\n3. Stakeholder-Kommunikation: Proaktive Kundeninformation innerhalb der vertraglichen Reaktionszeit (SLA).\n4. Entstörung & Dokumentation: Koordination mit Field Service Technikern vor Ort und Revisionssichere Abschlussdokumentation im Ticket.",
        "do": "Beschreibe die Schritte strukturiert: Alarm -> Triage -> Ticket -> Carrier-Eskalation -> SLA-Einhaltung.",
        "dont": "Antworte nicht unstrukturiert – im Leitstand zählt methodische Ruhe und standardisierte Vorgehensweise."
    },
    {
        "q": "Wie haben Sie die Prozessstandardisierung im INOC vorangetrieben?",
        "cat": "Datacenter One & ITIL 4",
        "open": False,
        "a": "Vor meiner Initiative lag viel Erfahrungswissen isoliert bei einzelnen Schichtleitern. Ich habe die Initiative ergriffen, dieses Wissen in Confluence zu systematisieren.\n\nIch habe Standard Operating Procedures (SOPs) für wiederkehrende Störungsbilder erstellt – darunter Leitfäden für Carrier-Ausfälle, USV-Alarme, Notfall-Paging und das Onboarding neuer Rechenzentrums-Kunden. Dadurch sank die Einarbeitungszeit neuer Mitarbeiter deutlich und die Erstlösungsquote (First Contact Resolution) stieg messbar.",
        "do": "Erwähne die Confluence-Wissensdatenbank, SOPs und die Steigerung der First Contact Resolution.",
        "dont": "Behaupte nicht, du hättest das Rechenzentrum alleine betrieben – stelle deinen Beitrag zur Standardisierung heraus."
    },
    {
        "q": "Was war das Projekt Hardware Lifecycle Management (HLM) bei Datacenter One?",
        "cat": "Datacenter One & ITIL 4",
        "open": False,
        "a": "Im Rahmen des Projekts Hardware Lifecycle Management (HLM) habe ich den gesamten Lebenszyklus der Client- und Leitstands-Hardware (über 100 Systeme) analysiert und optimiert.\n\nIch habe den Soll-Prozess in Microsoft Visio modelliert: Von der Bedarfsanforderung über die Beschaffung, Staging/Betankung, Rollout im laufenden Betrieb bis hin zum datenschutzkonformen Decommissioning (Zertifizierte Datenlöschung). Zudem habe ich eine Excel-basierte PoC-Rollout-Matrix erstellt, um Ausfallzeiten im 24/7 Betrieb zu verhindern.",
        "do": "Nenne die Phasen: Beschaffung -> Staging -> Rollout -> Decommissioning und die Modellierung in MS Visio.",
        "dont": "Stelle es nicht als reines Schrauben an PCs dar – es war ein strukturiertes IT-Asset-Management-Projekt."
    },
    {
        "q": "Wie funktionierte das Carriermanagement und die Netzanbindung im Leitstand?",
        "cat": "Datacenter One & ITIL 4",
        "open": False,
        "a": "Datacenter One betreibt Colocation- und Rechenzentrumsflächen, in denen Kunden Leitungen unterschiedlichster Carrier (Telekom, Vodafone, Colt, GasLINE etc.) nutzen.\n\nIm Carriermanagement ging es um die Überwachung der Meet-Me-Rooms (MMR), das Patching von Cross-Connects und die Sicherstellung vereinbarter Service Level Agreements (SLAs). Kam es zu Baggerunfällen oder Faserrissen, musste die Umschaltung auf redundante Strecken überwacht und der Ticket-Lifecycle mit dem jeweiligen Carrier koordiniert werden.",
        "do": "Nenne Meet-Me-Room (MMR), Cross-Connects, Carrier-SLAs und Redundanzschaltungen.",
        "dont": "Verwechsle Carriermanagement nicht mit reinem Telemarketing – es ist kritische Glasfaser-Infrastruktur."
    },
    {
        "q": "Was waren Ihre drei wichtigsten Learnings aus der Zeit bei Datacenter One?",
        "cat": "Datacenter One & ITIL 4",
        "open": False,
        "a": "Erstens: Absolute SLA-Disziplin. Bei einer vertraglichen Verfügbarkeit von 99,99% kosten wenige Minuten ungeplante Ausfallzeit tausende Euro Vertragsstrafen. Man lernt, unter Druck extrem präzise zu arbeiten.\n\nZweitens: Dokumentationsqualität ist die Lebensversicherung. Im 24/7 Schichtbetrieb muss die nachfolgende Schicht ein Ticket in 30 Sekunden vollständig verstehen, ohne nachfragen zu müssen.\n\nDrittens: Deeskalierende Krisenkommunikation. Wenn ein Kunde anruft, dessen Kernsysteme stehen, braucht er keine Ausreden, sondern einen ruhigen Ansprechpartner, der klare Zeithorizonte und Maßnahmen kommuniziert.",
        "do": "Nenne die 3 Punkte: 1. SLA-Disziplin, 2. Dokumentation im Schichtbetrieb, 3. Deeskalierende Kundenkommunikation.",
        "dont": "Wähle keine rein technischen Schlagworte – zeige deine persönliche Reife und Verlässlichkeit."
    },
    {
        "q": "Wie schlägt Ihre Erfahrung bei DC1 die Brücke zu Ihrer späteren SAP-Tätigkeit?",
        "cat": "Datacenter One & ITIL 4",
        "open": False,
        "a": "Viele Wirtschaftsinformatiker betrachten Cloud-Systeme wie S/4HANA nur als abstrakte Software im Browser. Durch meine 12 Monate im Rechenzentrum kenne ich das physische Fundament: Ich weiß, was Latenzen, redundante Netzanbindungen, USV-Pufferung und Tier-3/Tier-4 Klassifizierungen in der Praxis bedeuten.\n\nAls wir bei der SSB mit Axians über die Bereitstellung der Private-Cloud-Infrastruktur (ES4) und mit Nagarro über Schnittstellen diskutierten, konnte ich ITIL 4 Incident- und Change-Prozesse nahtlos mit den SAP Cloud ALM Quality Gates verbinden.",
        "do": "Stelle die Brücke her: Physische RZ-Infrastruktur + ITIL 4 Prozessdisziplin ➔ Verständnis für Enterprise-Cloud-Architekturen.",
        "dont": "Spiele die Station bei DC1 nicht herunter – sie zeigt dein tiefes technisches Fundament vor der SAP-Spezialisierung!"
    },

    # --- KATEGORIE 3: MASTER & PLATTFORMISIERUNG (9 Fragen) ---
    {
        "q": "Wie lautet der offizielle Titel Ihrer Masterarbeit und worum ging es im Kern?",
        "cat": "Master & Plattformisierung",
        "open": False,
        "a": "Der offizielle Titel lautet:\n'Kritische Erfolgsfaktoren in der Transformation großer ERP-Systeme: Eine Untersuchung am Beispiel der Plattformisierung von SAP S/4HANA'\n(126 Seiten, Note 1,0 'sehr gut', Erstprüfer Prof. Dr. Georg Herzwurm, Lehrstuhl für Wirtschaftsinformatik II, Universität Stuttgart).\n\nIm Kern untersucht die Arbeit auf Basis von 12 leitfadengestützten Experteninterviews im Großprojekt SAP4SSB und einer qualitativen Inhaltsanalyse nach Mayring, welche organisatorischen, technischen, personellen und projektsteuernden Faktoren über den Erfolg einer ERP-Plattformisierung entscheiden.",
        "do": "Zitiere den Titel exakt und nenne Umfang (126 Seiten), Note (1,0) und Lehrstuhl (Prof. Herzwurm).",
        "dont": "Verkürze die Arbeit niemals auf ein einzelnes Modul oder Schlagwort – es ist eine ganzheitliche Transformationsuntersuchung!"
    },
    {
        "q": "Warum darf die Masterarbeit niemals auf das Schlagwort 'Clean Core' reduziert werden?",
        "cat": "Master & Plattformisierung",
        "open": False,
        "a": "Weil 'Clean Core' nur eine technische Facette einer viel größeren architektonischen und organisatorischen Herausforderung ist!\n\nEine moderne ERP-Transformation zur digitalen Plattform umfasst:\n1. Plattform-Governance: Wie werden Schnittstellen (APIs) als Boundary Resources gesteuert?\n2. Bimodale IT: Wie entkoppelt man stabile Core-Systeme (Mode 1) von agilen Innovationsschichten (Mode 2 / BTP)?\n3. Soziotechnischer Wandel & Absorptive Capacity: Wie nimmt die Belegschaft neue Prozesse an (Betriebsrat, Change Management, Key User)?\n4. Multiprojekt-Steuerung (PMO): Wie orchestriert man komplexe Partner-Ökosysteme (Nagarro, Evora, Axians)?\n\nMeine Masterarbeit liefert ein ganzheitliches 4x3-Erfolgsfaktorenmodell, das all diese Dimensionen empirisch fundiert integriert.",
        "do": "Betone die 4 Dimensionen: Organisation, Technik, Mensch und PMO.",
        "dont": "Lass dich nicht in die rein technische 'Clean-Core-Schublade' stecken – deine Arbeit ist ganzheitlich strategisch."
    },
    {
        "q": "Wie haben Sie die qualitative Inhaltsanalyse nach Mayring methodisch umgesetzt?",
        "cat": "Master & Plattformisierung",
        "open": False,
        "a": "Ich habe 12 leitfadengestützte Experteninterviews transkribiert und nach Mayring strukturiert analysiert:\n1. Deduktive Kategorienbildung: Ableitung vorläufiger Hauptkategorien aus der theoretischen Literatur (CSF-Forschung, Boundary Resources, EAM).\n2. Induktive Kategorienanpassung: Während der Codierung wurden neue, praxisgetriebene Subkategorien direkt aus den Transkripten entwickelt.\n3. Erstellung eines standardisierten Codebuchs: Jede Kategorie erhielt eine präzise Definition, Ankerbeispiele aus den Interviews und explizite Abgrenzungsregeln.\n4. Paraphrasierung und Generalisierung: Verdichtung der Aussagen zu Kern-Erfolgsfaktoren und Validierung durch Methoden-Triangulation.",
        "do": "Erkläre den methodischen Dreischritt: Deduktiv-induktive Kategorien, Codebuch mit Ankerbeispielen, Triangulation.",
        "dont": "Beschreibe Mayring nicht als bloßes 'Texte markieren' – es ist ein streng wissenschaftliches, reliables Verfahren."
    },
    {
        "q": "Welche Kern-Erkenntnisse lieferten die Interviews mit Roland Nowak, Thomas Wimpff und Armin Heinrich?",
        "cat": "Master & Plattformisierung",
        "open": False,
        "a": "Die Interviews mit den Schlüsselakteuren der SSB zeigten komplementäre Perspektiven:\n- Roland Nowak (Gesamtprojektleiter): Unterstrich, dass ERP-Transformationen zu 80% ein Führungs- und Kommunikationsproblem sind. Die formelle Mitbestimmung mit dem Betriebsrat und ein rigoroses Scope-Management in den Fit-to-Standard Workshops sind der Schlüssel.\n- Thomas Wimpff (TPL TP2 Finance): Betonte die Notwendigkeit, das Universal Journal (ACDOCA) und die Trennungsrechnung frühzeitig architektonisch abzusichern, um spätere Steuer- und Bilanzierungsrisiken auszuschließen.\n- Armin Heinrich (Basisarchitekt): Verwies auf die zwingende Trennung zwischen Core und BTP sowie die Notwendigkeit stabiler SSO- und Authentifizierungs-Infrastrukturen.",
        "do": "Nenne die Namen der Experten und ihre spezifischen strategischen Schwerpunkte.",
        "dont": "Behandle die Interviews nicht abstrakt – zeige, dass du mit echten C-Level- und Architektur-Verantwortlichen auf Augenhöhe gesprochen hast."
    },
    {
        "q": "Wie hängen Boundary Resources Theory und ERP-Plattformisierung zusammen?",
        "cat": "Master & Plattformisierung",
        "open": False,
        "a": "Die Boundary Resources Theory (Ghazawneh & Henfridsson) erklärt, wie Plattformbetreiber externe Akteure befähigen, Innovationen auf der Plattform zu bauen, ohne die Stabilität der Plattform zu gefährden.\n\nIm ERP-Kontext ist die SAP BTP die 'Boundary Resource':\n- Application Boundary Resources (ABR): Freigegebene OData- und REST-APIs, Business Accelerators.\n- Development Boundary Resources (DBR): Cloud SDKs, Business Application Studio, CAP/RAP Frameworks.\n- Social Boundary Resources (SBR): Architektur-Richtlinien, Clean-Core-Governance und Community-Standards.\n\nDurch diese Grenzressourcen können Fachbereiche und Partner wie Nagarro maßgeschneiderte Apps bauen, während der S/4HANA-Kern modifikationsfrei und upgrade-sicher bleibt.",
        "do": "Erkläre die 3 Klassen: ABR, DBR, SBR und wende sie direkt auf SAP BTP und APIs an.",
        "dont": "Vergiss nicht die theoretische Quelle: Ghazawneh & Henfridsson."
    },
    {
        "q": "Was haben Sie im Masterprojekt 'Digitale Nachhaltigkeit' (Note 1,0) bei Schmalz GmbH erarbeitet?",
        "cat": "Master & Plattformisierung",
        "open": False,
        "a": "In der wissenschaftlichen Fallstudie (betreut durch Dr. Dimitri Petrik) ging es um die Optimierung der betrieblichen Abfallbilanz und CSRD-Nachhaltigkeitsberichterstattung beim Weltmarktführer J. Schmalz GmbH.\n\nIch habe die bestehenden, manuellen Erfassungsprozesse in BPMN 2.0 modelliert, Medienbrüche identifiziert und eine automatisierte Datenextraktionsstrecke mittels PowerShell konzipiert und implementiert. Dadurch wurden Entsorgungsnachweise automatisiert extrahiert, typisiert und fehlerfrei aggregiert – eine direkte Einsparung manueller Aufwände und revisionssichere Datenbasis für den CSRD-Nachhaltigkeitsbericht.",
        "do": "Nenne Schmalz GmbH, CSRD-Berichterstattung, BPMN 2.0 Modellierung und PowerShell-Automatisierung.",
        "dont": "Wichtig: Dies war eine Fallstudie bei der J. Schmalz GmbH – ordne das Projekt präzise diesem Unternehmen zu!"
    },
    {
        "q": "Was war das Ergebnis Ihres Forschungsprojekts FPWI (Note 1,3)?",
        "cat": "Master & Plattformisierung",
        "open": False,
        "a": "Im Forschungsprojekt Wirtschaftsinformatik (FPWI) habe ich ein Framework für 'Smart Service Blueprinting' zur Modellierung vernetzter cyber-physischer Systeme (CPS) und IoT-Dienstleistungen entwickelt.\n\nMethodisch basierte die Arbeit auf der Design Science Research Methodology (DSRM nach Peffers). Das konstruierte Artefakt integriert Sensorebenen, Datenflüsse und Service-Touchpoints. In Thinking-Aloud-Tests mit Fachexperten erzielte das Framework einen empirischen System Usability Scale (SUS) Score von 85/100, was der Bestbewertung 'Grade A / Excellent' entspricht.",
        "do": "Nenne DSRM nach Peffers, Smart Service Blueprinting, Thinking-Aloud Usability Tests und den SUS-Score 85/100.",
        "dont": "Bleibe präzise bei den Methodenbegriffen – das belegt dein universitäres Spitzenforschungs-Niveau."
    },
    {
        "q": "Was haben Sie im Projekt 'PatentRadar' für Klingele Paper & Packaging konzipiert?",
        "cat": "Master & Plattformisierung",
        "open": False,
        "a": "Im Rahmen der Innovationsmethoden für software- und datenintensive Geschäftsmodelle (ISG) entwickelten wir das Venture-Konzept 'PatentRadar' für die Verpackungsindustrie (Klingele Paper & Packaging).\n\nWir konzipierten ein hybrides Geschäftsmodell (SaaS & Beratungsdienstleistung), das manuelle Patentrecherchen und Fristenüberwachungen durch eine automatisierte RPA-Strecke (UiPath) in Verbindung mit KI-gestützter Relevanzfilterung (DEPATISnet) ablöst. Ich verantwortete die BPMN 2.0 Prozessanalyse, die Schnittstellendefinition und die wirtschaftliche Business-Case-Kalkulation für das finale Pitchdeck vor C-Level.",
        "do": "Betone Klingele Paper & Packaging, das hybride Geschäftsmodell, RPA/UiPath-Prozessmodellierung und Wirtschaftlichkeitskalkulation.",
        "dont": "Verwechsle dieses Industrieprojekt nicht mit einem Praktikum – es war ein hochkarätiges universitäres Praxis-Innovationsprojekt."
    },
    {
        "q": "Wie beurteilen Sie den Notensprung von 3,0 im Bachelor auf 1,6 im Master?",
        "cat": "Master & Plattformisierung",
        "open": False,
        "a": "Der Notensprung von 3,0 auf 1,6 (+1,4 Notenpunkte) belegt meine außerordentliche Lernkurve und Zielstrebigkeit!\n\nIm Bachelorstudium (180 ECTS) habe ich das breite, harte Fundament erworben: Höhere Mathematik, Theoretische Informatik, Algorithmen, Datenstrukturen und Buchführung. Im Masterstudium (120 ECTS) konnte ich meine Spezialisierung voll entfalten: Software-Architektur (1,7), Advanced Software Engineering (1,6), Digitale Nachhaltigkeit (1,0) und die Masterarbeit mit der Traumnote 1,0.\n\nIch habe bewiesen, dass ich mich in hochkomplexe Themen verbeiße, mich kontinuierlich steigere und in meiner Fachdomäne zu absoluten Spitzenleistungen fähig bin.",
        "do": "Framing: Bachelor = breites forderndes Fundament; Master = fokussierte Exzellenz (+1,4 Notenpunkte Leistungssteigerung).",
        "dont": "Entschuldige dich nicht für die 3,0 im Bachelor – die Universität Stuttgart ist bekannt für ihr anspruchsvolles ingenieurwissenschaftliches Niveau!"
    },

    # --- KATEGORIE 4: BACHELOR & METHODENKOMPETENZ (7 Fragen) ---
    {
        "q": "Was war der Gegenstand Ihrer Bachelorarbeit bei Prof. Herzwurm?",
        "cat": "Bachelor & Methodenkompetenz",
        "open": False,
        "a": "Meine Bachelorarbeit trug den Titel:\n'Die Bedeutung von Boundary Resources in Low-Code Entwicklungsplattformen: Eine qualitative Untersuchung am Beispiel von OutSystems und Mendix'\n(Note 1,7 'gut', Lehrstuhl für ABWL und Wirtschaftsinformatik II, Prof. Dr. Georg Herzwurm).\n\nIch untersuchte, wie führende Low-Code-Plattformen Grenzressourcen bereitstellen, um Citizen Developers und professionelle Software-Ingenieure in die Lage zu versetzen, Anwendungen schnell und architektonisch sauber zu erstellen.",
        "do": "Nenne den vollen Titel, Note 1,7, die Plattformen OutSystems & Mendix sowie den Lehrstuhl Herzwurm.",
        "dont": "Vergiss nicht die Verbindung zur Masterarbeit: Die Bachelorarbeit legte das theoretische Fundament für Plattform-Architekturen!"
    },
    {
        "q": "Was sind die 14 Klassen von Boundary Resources nach Ghazawneh & Henfridsson?",
        "cat": "Bachelor & Methodenkompetenz",
        "open": False,
        "a": "In meiner Bachelorarbeit habe ich 14 distinkte Grenzressourcen-Klassen identifiziert und den drei Dimensionen zugeordnet:\n1. Application Boundary Resources (ABR): REST/SOAP APIs, Webhooks, Datenkonnektoren und Integrationskomponenten.\n2. Development Boundary Resources (DBR): Visuelle Entwicklungsumgebungen (IDE), SDKs, Komponenten-Bibliotheken, Debugging-Tools und Test-Harnesses.\n3. Social Boundary Resources (SBR): Marktplätze (z.B. OutSystems Forge), Entwickler-Foren, Dokumentationen, Styleguides und Zertifizierungsprogramme.\n\nDiese Taxonomie belegt, wie Plattform-Ökosysteme technisch und sozial gesteuert werden.",
        "do": "Strukturiere klar nach ABR, DBR und SBR und nenne konkrete Beispiele wie Marktplätze, SDKs und APIs.",
        "dont": "Bleibe nicht bei der reinen Aufzählung stehen – erkläre den Nutzen für die Plattform-Governance."
    },
    {
        "q": "Wie haben Sie im Bachelor die Bestnote 1,0 in 'Informationssysteme im E-Business' erreicht?",
        "cat": "Bachelor & Methodenkompetenz",
        "open": False,
        "a": "Informationssysteme im E-Business (Teil von WI 1) war eines der Kernmodule meines Bachelorstudiums. Ich habe mich intensiv mit den Architekturen digitaler B2B- und B2C-Marktplätze, EDI-Standards (EDIFACT), E-Procurement-Katalogen und Plattformökonomie befasst.\n\nZudem gehörten formale Methoden des Software-Projektmanagements zum Prüfungsstoff: Function-Point-Analyse zur Aufwandsschätzung, Testmanagement-Strategien und agile Entwicklung. Mit der Traumnote 1,0 habe ich bewiesen, dass ich betriebliche Informationssysteme von Grund auf durchdrungen habe.",
        "do": "Erwähne B2B-Marktplätze, EDIFACT, E-Procurement und die Function-Point-Analyse.",
        "dont": "Reduziere E-Business nicht auf einfachen 'Online-Handel' – es geht um komplexe elektronische Wertschöpfungsketten."
    },
    {
        "q": "Was haben Sie im Informationsverarbeitungspraktikum (IVP) bei der 0x539-Wear GmbH analysiert?",
        "cat": "Bachelor & Methodenkompetenz",
        "open": False,
        "a": "Im Informationsverarbeitungspraktikum (Note 2,3, Lehrstuhl Abteilung VII) führten wir eine tiefgehende datengestützte Unternehmensanalyse der fiktiven 0x539-Wear GmbH durch.\n\nIch analysierte umfangreiche relationale Bestelldaten und erstellte mehrstufige Deckungsbeitragsrechnungen (DB I bis DB IV). Wir führten Plan-Ist-Vergleiche, ABC-Kunden- und Artikelanalysen sowie Lieferantenbewertungen durch, um margenschwache Produkte und Engpässe im Beschaffungsprozess aufzudecken. Das war mein praktischer Einstieg in Business Intelligence und operatives Controlling.",
        "do": "Nenne mehrstufige Deckungsbeitragsrechnung, Plan-Ist-Vergleiche und relationale Datenanalysen.",
        "dont": "Tue nicht so, als sei das nur Theorie gewesen – es war ein handfestes BI- und Controlling-Projekt."
    },
    {
        "q": "Welche Modellierungsmethoden beherrschen Sie aus dem Bachelorstudium?",
        "cat": "Bachelor & Methodenkompetenz",
        "open": False,
        "a": "Im Modul 'Modellierung' (Note 2,3 bei Prof. Dr. Bernhard Mitschang) und in nachfolgenden Praxisprojekten habe ich ein breites Repertoire formaler Modellierungsmethoden erlernt:\n- Geschäftsprozesse: BPMN 2.0 (Gateways, Pools, Lanes, Zwischenereignisse, Nachrichtenflüsse) und erweiterte Ereignisgesteuerte Prozessketten (eEPK).\n- Software- und Systemarchitektur: UML 2.0 (Klassendiagramme, Sequenzdiagramme, Zustandsautomaten, Aktivitätsdiagramme).\n- Formale Systeme: Petrinetze (Erreichbarkeitsgraphen, Lebendigkeit, Verklemmungsfreiheit).\n- Datenmodellierung: Entity-Relationship-Modelle (ERM), Relationale Algebra, Normalisierung (1NF bis BCNF) und SQL.",
        "do": "Nenne BPMN 2.0, UML, Petrinetze, ERM und Normalformen.",
        "dont": "Stelle Modellierung nicht als 'bunte Kästchen malen' dar – es ist die formale Semantik für fehlerfreie IT-Architekturen."
    },
    {
        "q": "Worum ging es in Ihrer Seminararbeit bei Prof. Dr. Marion Büttgen (Hohenheim)?",
        "cat": "Bachelor & Methodenkompetenz",
        "open": False,
        "a": "Am Lehrstuhl für Unternehmensführung der Universität Hohenheim (Prof. Dr. Marion Büttgen) verfasste ich meine Seminararbeit zum Thema Mensch-Roboter-Interaktion und Servicequalität bei digitalen Service Encountern.\n\nIch untersuchte auf Basis des Expectation-Confirmation-Modells (ECM) und der Servqual-Dimensionen, wie Kunden die Interaktion mit Servicerobotern und KI-Assistenten wahrnehmen und welche Faktoren die Akzeptanz und Zufriedenheit im Dienstleistungssektor determinieren. Diese Arbeit schärfte meinen Blick für User Acceptance und Human-Computer-Interaction.",
        "do": "Nenne Prof. Büttgen, Expectation-Confirmation-Modell (ECM) und Service Encounters.",
        "dont": "Vergiss nicht den Nutzen: Akzeptanzforschung ist direkt relevant für die Einführung neuer SAP Fiori Apps bei Anwendern."
    },
    {
        "q": "Welche mathematisch-statistischen Methoden beherrschen Sie?",
        "cat": "Bachelor & Methodenkompetenz",
        "open": False,
        "a": "Mein Studium umfasste 30 ECTS mathematisch-methodische Grundlagen:\n- Höhere Mathematik: Lineare Algebra, Matrizenrechnung, Vektorräume, Differential- und Integralrechnung mehrerer Variablen und Optimierung unter Nebenbedingungen (Lagrange-Multiplikatoren).\n- Deskriptive & Induktive Statistik: Wahrscheinlichkeitsverteilungen (Normal-, t-, Chi-Quadrat-Verteilung), Konfidenzintervalle, parametrische und nicht-parametrische Hypothesentests, lineare und multivariate Regression sowie Zeitreihenanalysen.\n- Algorithmik: Analyse der asymptotischen Laufzeit- und Speicherkomplexität (O-Notation) in Datenstrukturen und Algorithmen.",
        "do": "Betone die quantitative Denkdisziplin und das Durchhaltevermögen bei anspruchsvollen mathematischen Methoden.",
        "dont": "Lass dich nicht als 'reiner BWLer' abstempeln – du hast das volle informationstechnische Mathe-Programm absolviert!"
    },

    # --- KATEGORIE 5: ENTERPRISE ARCHITECTURE & TOGAF (5 Fragen) ---
    {
        "q": "Was beinhaltet Ihre TOGAF 9 ADM Zertifizierung bei Scape Consulting?",
        "cat": "Enterprise Architecture & TOGAF",
        "open": False,
        "a": "Ich habe den TOGAF 9 ADM-Intensivkurs an der Universität Stuttgart bei Dr. Daniel Simon (Scape Consulting GmbH, 16.01.2020) erfolgreich absolviert.\n\nDer Kurs vermittelte den vollständigen Architektur-Entwicklungszyklus (Architecture Development Method ADM):\n- Vorphase: Architecture Principles & Governance Framework\n- Phase A: Architecture Vision & Stakeholder Management\n- Phase B: Business Architecture (Geschäftsprozesse, Fähigkeiten)\n- Phase C: Information Systems Architecture (Data & Application Architecture)\n- Phase D: Technology Architecture (Infrastruktur, Plattformen)\n- Phase E & F: Opportunities & Solutions, Migration Planning\n- Phase G & H: Implementation Governance & Architecture Change Management",
        "do": "Nenne Scape Consulting, Dr. Daniel Simon, die ADM-Phasen A-H und die 4 Kernarchitekturen.",
        "dont": "Beschreibe TOGAF nicht nur theoretisch – erkläre, wie du diese Struktur im Solution Design bei der SSB genutzt hast."
    },
    {
        "q": "Was versteht man unter dem TOGAF Architecture Metamodel?",
        "cat": "Enterprise Architecture & TOGAF",
        "open": False,
        "a": "Das TOGAF Architecture Metamodel definiert die formalen Objekttypen und deren Beziehungen innerhalb einer Unternehmensarchitektur.\n\nEs verknüpft strukturiert:\n- Business Architecture: Business Capabilities, Business Actors, Rollen und Geschäftsprozesse.\n- Information Systems Architecture: Data Entities, Logical Data Models und Application Components.\n- Technology Architecture: Technology Services, Nodes und Netzwerke.\n\nDieses Metamodell verhindert Insellösungen, weil jede Software-Komponente und jedes Datenobjekt exakt einem Geschäftsziel und Geschäftsprozess zugeordnet ist.",
        "do": "Erkläre die vertikale Durchgängigkeit: Business Goal -> Capability -> Process -> Application -> Data -> Technology Node.",
        "dont": "Verliere dich nicht in Fachchinesisch – der Kern ist die lückenlose Verknüpfung von Business und IT."
    },
    {
        "q": "Was ist der Unterschied zwischen Baseline Architecture und Target Architecture?",
        "cat": "Enterprise Architecture & TOGAF",
        "open": False,
        "a": "Die Baseline Architecture beschreibt den aktuellen Ist-Zustand der Anwendungs-, Daten- und Technologie-Landschaft (inklusive historischer Z-Modifikationen, redundanter Systeme und technischer Schulden).\n\nDie Target Architecture definiert den strategischen Soll-Zustand (z.B. Greenfield S/4HANA Private Cloud, Clean Core, BTP-Integration).\n\nDer Wert entsteht durch die Gap-Analyse: Was fällt weg? Was wird neu aufgebaut? Wie sehen die Transition Architectures (Übergangszustände) aus, um das Geschäft während der mehrjährigen Transformation ohne Unterbrechung am Laufen zu halten?",
        "do": "Nenne Gap-Analyse, Transition Architectures und die Risikominimierung im laufenden Geschäftsbetrieb.",
        "dont": "Vergiss nicht die Transition Architectures – Großunternehmen können nicht über Nacht den Schalter umlegen."
    },
    {
        "q": "Wie funktioniert Architecture Governance in der Praxis?",
        "cat": "Enterprise Architecture & TOGAF",
        "open": False,
        "a": "Architecture Governance stellt sicher, dass laufende Projekte nicht an den Unternehmensrichtlinien vorbeientwickeln.\n\nIn der Praxis wird dazu ein Architecture Review Board (ARB) etabliert. Wenn ein Projektteam oder Fachbereich eine neue Anforderung hat, die vom Standard abweicht, muss ein Architecture Compliance Review durchlaufen werden. Es wird geprüft: Entspricht die Lösung den Clean-Core-Richtlinien? Gibt es Sicherheits- oder Datenrisiken? Werden bestehende BTP-Dienste genutzt? Erst mit ARB-Freigabe darf die Implementierung beginnen.",
        "do": "Nenne das Architecture Review Board (ARB), Architecture Compliance Reviews und Clean-Core-Gates.",
        "dont": "Stelle Governance nicht als bürokratische Bremse dar – sie schützt das Unternehmen vor Millionenverlusten durch Fehlinvestitionen."
    },
    {
        "q": "Wie grenzt sich Enterprise Architecture von reiner Softwareentwicklung ab?",
        "cat": "Enterprise Architecture & TOGAF",
        "open": False,
        "a": "Klassische Softwareentwicklung fokussiert auf die Implementierung eines konkreten Systems: Code-Qualität, Frameworks, Klassen, Algorithmen und Sprint-Deliverables im Zeithorizont von Wochen bis Monaten.\n\nEnterprise Architecture Management (EAM) blickt aus der Vogelperspektive auf das gesamte Ökosystem im Zeithorizont von 3 bis 7 Jahren: Wie spielen 50 verschiedene Systeme, ERP-Kerne, Cloud-Plattformen, Schnittstellen, regulatorische Vorgaben und Business-Fähigkeiten zusammen? EAM fragt nicht 'Wie schreibe ich den Code?', sondern 'Sollte diese Funktion überhaupt im Kern gebaut werden oder gehört sie auf die BTP?'",
        "do": "Klarer Kontrast: Softwareentwicklung = lokale Systemimplementierung; EAM = strategische Gesamtsystem- und Portfolio-Steuerung.",
        "dont": "Werte die Softwareentwicklung nicht ab – betone, dass EAM das Dach bildet, unter dem Entwickler sauber arbeiten können."
    },

    # --- KATEGORIE 6: PERSÖNLICH & TRAINEE-EINSTIEG (5 Fragen) ---
    {
        "q": "Warum bewerben Sie sich bewusst auf eine Junior-Position oder ein Traineeprogramm?",
        "cat": "Persönlich & Trainee-Einstieg",
        "open": False,
        "a": "Weil ich realistische Selbsteinschätzung mit hoher Leistungsbereitschaft verbinde!\n\nIch bringe zwar durch 24 Monate S/4HANA Großprojekt im IT-PMO, 12 Monate Rechenzentrumsbetrieb bei DC1 und meine mit 1,0 bewertete Masterarbeit ein außergewöhnlich starkes Fundament mit. Aber: Jedes Unternehmen hat eigene Prozesse, eigene Unternehmenskulturen und spezifische Systemlandschaften.\n\nIch suche den Einstieg als Junior Consultant oder in einem anspruchsvollen Traineeprogramm, um mit einer gesunden Mischung aus Demut, Neugier und Engagement Ihr Unternehmen von Grund auf kennenzulernen. Ich möchte nicht mit vorgefertigten Meinungen auftreten, sondern zuhören, schnell lernen und mit hoher Verlässlichkeit binnen kürzester Zeit zur tragenden Säule in Ihrem Team heranwachsen.",
        "do": "Betone die Haltung: Fundiertes Vorwissen vorhanden, aber bewusste Offenheit, Lernbegierde und Respekt vor der Firmenkultur.",
        "dont": "Trete nicht arrogant auf ('Ich weiß schon alles wegen meiner 1,0'). Reife Absolventen zeigen Lernbereitschaft!"
    },
    {
        "q": "Wie reagieren Sie, wenn Sie in einem Projekt auf eine völlig unbekannte SAP- oder IT-Frage stoßen?",
        "cat": "Persönlich & Trainee-Einstieg",
        "open": False,
        "a": "Ich verfalle weder in Aktionismus noch sitze ich das Problem aus, sondern gehe in einem 4-Stufen-Modell vor:\n1. Problem strukturieren: Exakte Definition des Gaps – handelt es sich um ein Prozess-, Konfigurations- oder Schnittstellenthema?\n2. Eigenrecherche im Standard: Analyse der SAP Best Practice Explorer Scope-IDs, SAP Learning Hub und offizieller SAP Press Referenzen.\n3. Lösungsoptionen erarbeiten: Ich erarbeite mindestens 2 fundierte Handlungsoptionen inklusive Vor- und Nachteilen.\n4. Gezielte Abstimmung: Mit diesen vorstrukturierten Optionen gehe ich auf Seniorkollegen oder Fachexperten zu. So stehle ich niemandem Zeit, sondern ermögliche eine fundierte Entscheidung.",
        "do": "Beschreibe die 4 Stufen: Strukturieren -> Eigenrecherche -> Optionen formulieren -> Gezieltes Sparring.",
        "dont": "Sage niemals 'Ich frage sofort meinen Chef' (unselbstständig) oder 'Ich probiere einfach rum' (gefährlich im Produktivsystem)."
    },
    {
        "q": "Wie vermitteln Sie zwischen rein technischen Beratern und konservativen Fachbereichen?",
        "cat": "Persönlich & Trainee-Einstieg",
        "open": False,
        "a": "Das war genau meine tägliche Rolle im IT-PMO bei der SSB!\n\nFachbereiche denken in ihren gewohnten Buchungsabläufen, Belegen und Arbeitszeitplänen; technische Berater von Partnern wie Nagarro denken in CDS Views, OData-Services und RAP-Objekten. Meine Stärke ist die 'bilinguale' Vermittlung:\nIch übersetze die Anforderungen des Fachbereichs in präzise User Stories und Akzeptanzkriterien für die Entwickler. Umgekehrt erkläre ich dem Fachbereich technische Einschränkungen nicht mit IT-Jargon, sondern anhand der konkreten Auswirkungen auf ihren täglichen Arbeitsablauf in SAP Fiori.",
        "do": "Framing: Du bist der 'Bilinguale Übersetzer' zwischen Fachbereichs-Sprache und IT-Architektur.",
        "dont": "Wähle keine Partei – weder Fachbereich noch IT sind 'schuld', wenn Kommunikation hakt; es braucht Empathie für beide Seiten."
    },
    {
        "q": "Welche Gehaltserwartung bringen Sie für den Berufseinstieg mit?",
        "cat": "Persönlich & Trainee-Einstieg",
        "open": False,
        "a": "Auf Basis meiner soliden Qualifikation – Master of Science Wirtschaftsinformatik an der Universität Stuttgart (Note 1,6), Masterarbeit mit Note 1,0 sowie insgesamt 36 Monaten relevanter Praxiserfahrung in Großprojekt (SSB) und Rechenzentrum (DC1) – sehe ich ein Einstiegsgehalt im Bereich von 55.000 € bis 65.000 € brutto pro Jahr als fair und marktüblich an.\n\nFür mich steht jedoch der inhaltliche Fit, die Qualität des Teams, anspruchsvolle Projekte und gezielte Weiterentwicklungsmöglichkeiten klar an erster Stelle. Wenn das Gesamtpaket stimmt, finden wir mit Sicherheit eine gemeinsame Basis.",
        "do": "Nenne die Spanne 55.000 € - 65.000 € ruhig, begründe sie sachlich mit 300 ECTS + 36 Mo. Praxis und betone die Priorität der Lernperspektive.",
        "dont": "Nenne keine überzogenen 75k-80k Senior-Forderungen und sei nicht unverschämt flexibel nach unten (unter Wert verkaufen)."
    },
    {
        "q": "Wo sehen Sie sich in 3 bis 5 Jahren in unserer Organisation?",
        "cat": "Persönlich & Trainee-Einstieg",
        "open": False,
        "a": "In 3 bis 5 Jahren sehe ich mich als fachlich etablierte und geschätzte Stütze in Ihrem Beratungsteam oder Enterprise-Architecture-Bereich.\n\nIch möchte nach meiner Junior-/Traineephase schnell eigenverantwortlich anspruchsvolle Teilprojekte und Workstreams führen, die Schnittstelle zwischen Business und IT gestalten und mein Wissen über moderne Cloud-Architekturen und Clean Core kontinuierlich vertiefen. Zudem liegt es mir am Herzen, neue Trainees und Werkstudenten an Bord zu holen und als Mentor die nächste Generation mit der gleichen Begeisterung zu unterstützen, die ich heute mitbringe.",
        "do": "Skizziere einen klaren Entwicklungspfad: Verantwortung übernehmen -> Fachthemen prägen -> Mentoring für Nachwuchs.",
        "dont": "Sage nicht 'Ich will Partner / Geschäftsführer werden' – zeige Loyalität, Teamorientierung und fachliche Reife."
    }
]

print(f"Total Q&A items defined: {len(qa_data)}")

# Convert to valid JavaScript literal
js_lines = ["        const allQA = ["]
for idx, item in enumerate(qa_data):
    comma = "," if idx < len(qa_data) - 1 else ""
    js_lines.append("          {")
    js_lines.append(f"            q: {repr(item['q'])},")
    js_lines.append(f"            cat: {repr(item['cat'])},")
    js_lines.append(f"            open: {'true' if item['open'] else 'false'},")
    # use backtick string for multi-line 'a'
    escaped_a = item['a'].replace('`', '\\`').replace('${', '\\${')
    js_lines.append(f"            a: `{escaped_a}`,")
    js_lines.append(f"            do: {repr(item['do'])},")
    js_lines.append(f"            dont: {repr(item['dont'])}")
    js_lines.append(f"          }}{comma}")
js_lines.append("        ];")

js_all_qa = "\n".join(js_lines)

# Read vue_app.py
with open("portal_builder/vue_app.py", "r", encoding="utf-8") as f:
    content = f.read()

# Replace qaCategories
old_qa_cat = "const qaCategories = ['Alle', 'Architektur & Clean Core', 'Datenmigration', 'Projektmanagement & Governance', 'Persönlich & Verhalten'];"
new_qa_cat = "const qaCategories = ['Alle', 'SSB S/4HANA & Explore-Phase', 'Datacenter One & ITIL 4', 'Master & Plattformisierung', 'Bachelor & Methodenkompetenz', 'Enterprise Architecture & TOGAF', 'Persönlich & Trainee-Einstieg'];"

if old_qa_cat in content:
    content = content.replace(old_qa_cat, new_qa_cat)
    print("Replaced qaCategories successfully.")
else:
    print("Warning: old_qa_cat not found, trying regex.")
    content = re.sub(r"const qaCategories = \[.*?\];", new_qa_cat, content)

# Add qaSearch if missing
if "const qaSearch = ref('');" not in content:
    content = content.replace("const personalNotes = ref('');", "const personalNotes = ref('');\n        const qaSearch = ref('');")
    print("Added qaSearch ref.")

# Update filteredQA
old_filtered_qa = """        const filteredQA = computed(() => {
          let list = allQA;
          if (selectedQACat.value !== 'Alle') {
            list = list.filter(item => item.cat === selectedQACat.value);
          }
          if (searchQuery.value) {
            const q = searchQuery.value.toLowerCase();
            list = list.filter(item => item.q.toLowerCase().includes(q) || item.a.toLowerCase().includes(q));
          }
          return list;
        });"""

new_filtered_qa = """        const filteredQA = computed(() => {
          let list = allQA;
          if (selectedQACat.value !== 'Alle') {
            list = list.filter(item => item.cat === selectedQACat.value);
          }
          const term = (qaSearch.value || searchQuery.value || '').trim().toLowerCase();
          if (term) {
            list = list.filter(item => 
              item.q.toLowerCase().includes(term) || 
              item.a.toLowerCase().includes(term) ||
              (item.cat && item.cat.toLowerCase().includes(term))
            );
          }
          return list;
        });"""

if old_filtered_qa in content:
    content = content.replace(old_filtered_qa, new_filtered_qa)
    print("Replaced filteredQA successfully.")
else:
    print("Warning: old_filtered_qa not found exactly, updating with regex.")
    content = re.sub(
        r"const filteredQA = computed\(\(\) => \{[\s\S]*?return list;\s*\}\);",
        new_filtered_qa.strip(),
        content
    )

# Replace allQA block
qa_pattern = re.compile(r"const allQA = \[[\s\S]*?\n        \];", re.MULTILINE)
if qa_pattern.search(content):
    content = qa_pattern.sub(js_all_qa, content)
    print("Replaced allQA block with 43 questions successfully.")
else:
    print("Error: Could not find allQA block in vue_app.py!")

with open("portal_builder/vue_app.py", "w", encoding="utf-8") as f:
    f.write(content)

print("vue_app.py successfully written.")
