# -*- coding: utf-8 -*-

def get_bachelor_tab():
    return """
      <!-- ================= TAB 5: BACHELOR OF SCIENCE (180 ECTS | NOTE 3,0) ================= -->
      <div v-show="activeTab === 'bachelor'" class="space-y-6">

        <!-- Bachelor Overview & Highlights -->
        <div class="bg-[#141414] p-6 rounded-2xl border border-white/10 space-y-5">
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
            <div>
              <div class="flex flex-wrap items-center gap-2 mb-1.5">
                <span class="status-pill status-pill-blue">Gesamtnote 3,0</span>
                <span class="status-pill status-pill-purple">Bachelorarbeit: Note 1,7 (12 ECTS)</span>
                <span class="status-pill status-pill-green">E-Business: Bestnote 1,0</span>
                <span class="status-pill status-pill-neutral">180 ECTS • 18.09.2023</span>
              </div>
              <h2 class="text-xl sm:text-2xl font-extrabold text-white tracking-tight">
                🏛️ B.Sc. Wirtschaftsinformatik (Universität Stuttgart)
              </h2>
              <p class="text-xs sm:text-sm text-[#8f8888] mt-1">
                Ingenieurwissenschaftlich-betriebswirtschaftliches Fundament in Informatik, Softwaretechnik, Wirtschaftsinformatik, BWL/VWL &amp; Mathematik.
              </p>
            </div>
          </div>

          <!-- Highlight Box: Bachelor Thesis 1,7 & TOGAF 9 ADM -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
            <div class="info-callout p-4 space-y-1.5">
              <div class="flex items-center justify-between gap-2">
                <span class="font-bold text-white text-sm">⭐ Bachelorarbeit (Note 1,7 | Prof. Herzwurm)</span>
                <span class="status-pill status-pill-purple">12 ECTS</span>
              </div>
              <p class="text-white font-semibold">
                „Die Bedeutung von Boundary Resources in Low-Code Entwicklungsplattformen: Eine qualitative Untersuchung am Beispiel von OutSystems und Mendix“
              </p>
              <p class="text-[#c4bebe] leading-relaxed">
                Analyse von 14 Boundary-Resource-Klassen (ABR, DBR, SBR) nach Ghazawneh &amp; Henfridsson – wissenschaftliche Grundlage für Schnittstellen- &amp; Plattform-Governance.
              </p>
            </div>

            <div class="p-4 rounded-xl bg-white/5 border border-white/10 space-y-2 flex flex-col justify-between">
              <div class="space-y-1.5">
                <div class="flex items-center justify-between gap-2">
                  <span class="font-bold text-white text-sm">🏛️ Zusätzliche Meilensteine &amp; Zertifikate</span>
                  <span class="status-pill status-pill-green">Verifiziert</span>
                </div>
                <ul class="text-[#c4bebe] space-y-1 list-disc list-inside leading-relaxed">
                  <li><strong>TOGAF 9 ADM-Intensivkurs:</strong> Scape Consulting (Dr. Daniel Simon, Uni Stuttgart, Jan 2020) – Architekturmethodik &amp; Metamodelle.</li>
                  <li><strong>E-Business (Note 1,0):</strong> B2B-Plattformen, E-Procurement, Function-Point-Analyse &amp; Design Thinking.</li>
                  <li><strong>IVP Unternehmensanalyse (Note 2,3):</strong> Mehrstufige Deckungsbeitragsrechnung &amp; BI-Controlling-Report.</li>
                </ul>
              </div>
            </div>
          </div>
        </div>

        <!-- Complete Table: All Bachelor Modules (180 ECTS) -->
        <div class="bg-[#141414] p-6 rounded-2xl border border-white/10 space-y-4">
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
            <div>
              <h3 class="text-base font-bold text-white">
                Alle Prüfungsleistungen im Bachelorstudium (180 ECTS | Gesamtnote 3,0)
              </h3>
              <p class="text-xs text-[#8f8888]">Amtlich beglaubigt in der Leistungsübersicht B.Sc. Wirtschaftsinformatik (Universität Stuttgart).</p>
            </div>
            <span class="status-pill status-pill-blue">180 ECTS Komplett</span>
          </div>

          <div class="overflow-x-auto">
            <table class="w-full text-left text-xs border border-white/10 rounded-xl overflow-hidden">
              <thead class="bg-white/10 text-white font-bold">
                <tr>
                  <th class="p-3">Modulbezeichnung</th>
                  <th class="p-3 whitespace-nowrap">Bereich nach PO</th>
                  <th class="p-3 text-center">ECTS</th>
                  <th class="p-3 text-center">Note</th>
                  <th class="p-3">Inhaltlicher Kern &amp; Fachkompetenz</th>
                </tr>
              </thead>
              <tbody class="divide-y text-[#c4bebe]">
                <tr class="font-medium">
                  <td class="p-3 font-bold text-white">⭐ Bachelorarbeit Wirtschaftsinformatik: Boundary Resources in Low-Code Entwicklungsplattformen (OutSystems &amp; Mendix)</td>
                  <td class="p-3 whitespace-nowrap text-[#8f8888]">Bereich D: Abschlussprojekt</td>
                  <td class="p-3 font-bold text-center">12</td>
                  <td class="p-3 text-center"><span class="status-pill status-pill-purple">1,7</span></td>
                  <td class="p-3">Boundary Resource Theory (Ghazawneh &amp; Henfridsson), 14 Grenzressourcen-Klassen (ABR, DBR, SBR) bei Prof. Herzwurm.</td>
                </tr>

                <tr class="font-bold">
                  <td colspan="5" class="p-2.5 uppercase tracking-wider text-[11px] text-emerald-400">
                    💻 Säule B 2: Wirtschaftsinformatik (45 ECTS)
                  </td>
                </tr>
                <tr>
                  <td class="p-3 font-bold text-white">Betriebliche Informationssysteme: Informationssysteme im E-Business</td>
                  <td class="p-3 whitespace-nowrap text-[#8f8888]">B2: WI (Teilleistung)</td>
                  <td class="p-3 text-center font-bold">4,5</td>
                  <td class="p-3 text-center"><span class="status-pill status-pill-green">1,0</span></td>
                  <td class="p-3">Elektronische Marktplätze, E-Procurement, digitale B2B-Plattformen und Web-Ökosysteme (Bestnote).</td>
                </tr>
                <tr>
                  <td class="p-3 font-semibold text-white">Betriebliche Informationssysteme: Management betrieblicher Informationssysteme</td>
                  <td class="p-3 whitespace-nowrap text-[#8f8888]">B2: WI (Teilleistung)</td>
                  <td class="p-3 text-center">4,5</td>
                  <td class="p-3 text-center"><span class="status-pill status-pill-neutral">2,7</span></td>
                  <td class="p-3">Architektur betrieblicher Standardsoftware (ERP, SCM, CRM), Integration und Geschäftsprozessmanagement.</td>
                </tr>
                <tr>
                  <td class="p-3 font-semibold text-white">Informationsverarbeitungspraktikum (IVP)</td>
                  <td class="p-3 whitespace-nowrap text-[#8f8888]">B2: WI Pflicht</td>
                  <td class="p-3 text-center font-bold">6</td>
                  <td class="p-3 text-center"><span class="status-pill status-pill-blue">2,3</span></td>
                  <td class="p-3">Hands-on Datenanalyse, Unternehmens- &amp; Deckungsbeitragsrechnung (0x539-Wear), relationale Abfragen.</td>
                </tr>
                <tr>
                  <td class="p-3 font-semibold text-white">Einführung in die Wirtschaftsinformatik</td>
                  <td class="p-3 whitespace-nowrap text-[#8f8888]">B2: WI Pflicht</td>
                  <td class="p-3 text-center">6</td>
                  <td class="p-3 text-center"><span class="status-pill status-pill-neutral">2,7</span></td>
                  <td class="p-3">Grundlagen der Wirtschaftsinformatik, Informationssystem-Architekturen, Datenmodellierung &amp; Geschäftsprozesse.</td>
                </tr>
                <tr>
                  <td class="p-3 font-semibold text-white">Informationsmanagement: Business Intelligence (BI)</td>
                  <td class="p-3 whitespace-nowrap text-[#8f8888]">B2: WI (Teilleistung)</td>
                  <td class="p-3 text-center">4,5</td>
                  <td class="p-3 text-center"><span class="status-pill status-pill-neutral">2,7</span></td>
                  <td class="p-3">Data Warehousing, ETL-Prozesse, OLAP-Cubes, multidimensionale Datenmodelle und Management-Reporting.</td>
                </tr>
                <tr>
                  <td class="p-3 font-semibold text-white">Informationsmanagement: Grundlagen des Informationsmanagements</td>
                  <td class="p-3 whitespace-nowrap text-[#8f8888]">B2: WI (Teilleistung)</td>
                  <td class="p-3 text-center">4,5</td>
                  <td class="p-3 text-center"><span class="status-pill status-pill-neutral">3,3</span></td>
                  <td class="p-3">Strategisches, administratives und operatives Informationsmanagement im Unternehmen.</td>
                </tr>
                <tr>
                  <td class="p-3 font-semibold text-white">Softwarepraktikum (SOPRA)</td>
                  <td class="p-3 whitespace-nowrap text-[#8f8888]">B2: WI Pflicht</td>
                  <td class="p-3 text-center">6</td>
                  <td class="p-3 text-center"><span class="status-pill status-pill-neutral">3,0</span></td>
                  <td class="p-3">Agiles Team-Entwicklungsprojekt, Scrum-Methodik, Git, Software-Architektur und Qualitätssicherung.</td>
                </tr>
                <tr>
                  <td class="p-3 font-semibold text-white">Wissensverarbeitung</td>
                  <td class="p-3 whitespace-nowrap text-[#8f8888]">B2: WI Pflicht</td>
                  <td class="p-3 text-center">6</td>
                  <td class="p-3 text-center"><span class="status-pill status-pill-neutral">3,7</span></td>
                  <td class="p-3">Ontologien, wissensbasierte Systeme, Logikprogrammierung und semantische Netze.</td>
                </tr>
                <tr>
                  <td class="p-3 font-semibold text-white">Informatikrecht</td>
                  <td class="p-3 whitespace-nowrap text-[#8f8888]">B2: WI Pflicht</td>
                  <td class="p-3 text-center">3</td>
                  <td class="p-3 text-center"><span class="status-pill status-pill-neutral">4,0</span></td>
                  <td class="p-3">Datenschutzrecht (DSGVO), Urheberrecht an Software, IT-Vertragsrecht und Haftung bei Cloud-Diensten.</td>
                </tr>

                <tr class="font-bold">
                  <td colspan="5" class="p-2.5 uppercase tracking-wider text-[11px] text-blue-400">
                    🖥️ Säule B 1: Informatik &amp; Softwaretechnik (48 ECTS)
                  </td>
                </tr>
                <tr>
                  <td class="p-3 font-semibold text-white">Modellierung</td>
                  <td class="p-3 whitespace-nowrap text-[#8f8888]">B1: Informatik Pflicht</td>
                  <td class="p-3 text-center font-bold">6</td>
                  <td class="p-3 text-center"><span class="status-pill status-pill-blue">2,3</span></td>
                  <td class="p-3">UML, BPMN 2.0, ER-Modelle, SQL, Petrinetze und formale Modellierungssysteme.</td>
                </tr>
                <tr>
                  <td class="p-3 font-semibold text-white">Datenstrukturen und Algorithmen (DSA)</td>
                  <td class="p-3 whitespace-nowrap text-[#8f8888]">B1: Informatik Pflicht</td>
                  <td class="p-3 text-center">9</td>
                  <td class="p-3 text-center"><span class="status-pill status-pill-neutral">3,0</span></td>
                  <td class="p-3">Bäume, Graphen, Such- und Sortieralgorithmen, Laufzeitkomplexität (O-Notation) und algorithmische Effizienz.</td>
                </tr>
                <tr>
                  <td class="p-3 font-semibold text-white">Programmentwicklung</td>
                  <td class="p-3 whitespace-nowrap text-[#8f8888]">B1: Informatik Pflicht</td>
                  <td class="p-3 text-center">6</td>
                  <td class="p-3 text-center"><span class="status-pill status-pill-neutral">3,0</span></td>
                  <td class="p-3">Fortgeschrittene Programmierung, Clean Code, Test-Driven Development (TDD) und Entwurfsmuster.</td>
                </tr>
                <tr>
                  <td class="p-3 font-semibold text-white">Mensch-Computer-Interaktion (MCI)</td>
                  <td class="p-3 whitespace-nowrap text-[#8f8888]">B1: Informatik Wahlpflicht</td>
                  <td class="p-3 text-center">6</td>
                  <td class="p-3 text-center"><span class="status-pill status-pill-neutral">3,3</span></td>
                  <td class="p-3">Usability Engineering, User Experience (UX), Interaktionsdesign, Usability-Tests und UI-Prototyping.</td>
                </tr>
                <tr>
                  <td class="p-3 font-semibold text-white">Einführung in die Softwaretechnik (EST)</td>
                  <td class="p-3 whitespace-nowrap text-[#8f8888]">B1: Informatik Pflicht</td>
                  <td class="p-3 text-center">6</td>
                  <td class="p-3 text-center"><span class="status-pill status-pill-neutral">3,7</span></td>
                  <td class="p-3">Software-Lebenszyklusmodelle, Requirements Engineering, Softwaretests und Konfigurationsmanagement.</td>
                </tr>
                <tr>
                  <td class="p-3 font-semibold text-white">Automaten und Formale Sprachen</td>
                  <td class="p-3 whitespace-nowrap text-[#8f8888]">B1: Informatik Pflicht</td>
                  <td class="p-3 text-center">6</td>
                  <td class="p-3 text-center"><span class="status-pill status-pill-neutral">3,7</span></td>
                  <td class="p-3">Reguläre Sprachen, endliche Automaten, kontextfreie Grammatiken und Berechenbarkeitstheorie.</td>
                </tr>
                <tr>
                  <td class="p-3 font-semibold text-white">Programmierung und Software-Entwicklung (PSE)</td>
                  <td class="p-3 whitespace-nowrap text-[#8f8888]">B1: Informatik Pflicht</td>
                  <td class="p-3 text-center">9</td>
                  <td class="p-3 text-center"><span class="status-pill status-pill-neutral">4,0</span></td>
                  <td class="p-3">Objektorientierte Programmierung in Java, Vererbung, Polymorphie, Datenkapselung und Collections Framework.</td>
                </tr>

                <tr class="font-bold">
                  <td colspan="5" class="p-2.5 uppercase tracking-wider text-[11px] text-purple-400">
                    📊 Säule B 3 &amp; Bereich C: Wirtschaftswissenschaften &amp; Management (45 ECTS)
                  </td>
                </tr>
                <tr>
                  <td class="p-3 font-semibold text-white">GBWL 1: Strukturen der Betriebswirtschaftslehre</td>
                  <td class="p-3 whitespace-nowrap text-[#8f8888]">B3: BWL Hohenheim</td>
                  <td class="p-3 text-center">6</td>
                  <td class="p-3 text-center"><span class="status-pill status-pill-neutral">2,7</span></td>
                  <td class="p-3">Unternehmensführung, Rechtsformen, Corporate Governance und Wertschöpfungsstrukturen.</td>
                </tr>
                <tr>
                  <td class="p-3 font-semibold text-white">GBWL 4: Finanzprozess (Finanzierung &amp; Investition)</td>
                  <td class="p-3 whitespace-nowrap text-[#8f8888]">B3: BWL Hohenheim</td>
                  <td class="p-3 text-center">6</td>
                  <td class="p-3 text-center"><span class="status-pill status-pill-neutral">2,7</span></td>
                  <td class="p-3">Investitionsrechnung (Kapitalwertmethode, IZF), Finanzierungsarten und Kapitalstruktur.</td>
                </tr>
                <tr>
                  <td class="p-3 font-semibold text-white">GVWL 1: Märkte &amp; wirtschaftliche Entscheidungen</td>
                  <td class="p-3 whitespace-nowrap text-[#8f8888]">B3: VWL Pflicht</td>
                  <td class="p-3 text-center">6</td>
                  <td class="p-3 text-center"><span class="status-pill status-pill-neutral">2,7</span></td>
                  <td class="p-3">Mikroökonomie, Marktformen, Preisbildung, Wohlfahrtstheorie, Angebot und Nachfrage.</td>
                </tr>
                <tr>
                  <td class="p-3 font-semibold text-white">Profilseminar zum Human Resource Management</td>
                  <td class="p-3 whitespace-nowrap text-[#8f8888]">Bereich C: Wahl</td>
                  <td class="p-3 text-center">6</td>
                  <td class="p-3 text-center"><span class="status-pill status-pill-neutral">3,0</span></td>
                  <td class="p-3">Personalökonomie, Mitarbeiterführung, Anreizsysteme, Talent Management und organisatorischer Wandel.</td>
                </tr>
                <tr>
                  <td class="p-3 font-semibold text-white">BWL 1: Organisation, Personalführung, Strategisches Management</td>
                  <td class="p-3 whitespace-nowrap text-[#8f8888]">B3: BWL Pflicht</td>
                  <td class="p-3 text-center">9</td>
                  <td class="p-3 text-center"><span class="status-pill status-pill-neutral">3,3</span></td>
                  <td class="p-3">Strategische Analyse (SWOT, Porter Five Forces), Organisationsstrukturen, Aufbau- und Ablauforganisation.</td>
                </tr>
                <tr>
                  <td class="p-3 font-semibold text-white">Marketing Management</td>
                  <td class="p-3 whitespace-nowrap text-[#8f8888]">Bereich C: Pflicht</td>
                  <td class="p-3 text-center">6</td>
                  <td class="p-3 text-center"><span class="status-pill status-pill-neutral">3,3</span></td>
                  <td class="p-3">Marketing-Mix (4P), Marktforschung, Kundenbindung, Produktpositionierung und Markenführung.</td>
                </tr>
                <tr>
                  <td class="p-3 font-semibold text-white">Management von Dienstleistungsunternehmen</td>
                  <td class="p-3 whitespace-nowrap text-[#8f8888]">Bereich C: Pflicht</td>
                  <td class="p-3 text-center">6</td>
                  <td class="p-3 text-center"><span class="status-pill status-pill-neutral">4,0</span></td>
                  <td class="p-3">Dienstleistungsqualität (SERVQUAL), Kapazitätssteuerung, Customer Journey und Dienstleistungsproduktivität.</td>
                </tr>

                <tr class="font-bold">
                  <td colspan="5" class="p-2.5 uppercase tracking-wider text-[11px] text-amber-400">
                    📐 Bereich A &amp; SQ: Mathematisch-Methodische Grundlagen (30 ECTS)
                  </td>
                </tr>
                <tr>
                  <td class="p-3 font-semibold text-white">Seminar interdisziplinäre Themen</td>
                  <td class="p-3 whitespace-nowrap text-[#8f8888]">Bereich A</td>
                  <td class="p-3 text-center font-bold">6</td>
                  <td class="p-3 text-center"><span class="status-pill status-pill-blue">2,3</span></td>
                  <td class="p-3">Interdisziplinäres wissenschaftliches Arbeiten, Literaturrecherche, Argumentation und Präsentation.</td>
                </tr>
                <tr>
                  <td class="p-3 font-semibold text-white">Statistik II (Induktive Statistik)</td>
                  <td class="p-3 whitespace-nowrap text-[#8f8888]">Bereich A</td>
                  <td class="p-3 text-center">6</td>
                  <td class="p-3 text-center"><span class="status-pill status-pill-neutral">2,7</span></td>
                  <td class="p-3">Wahrscheinlichkeitstheorie, Hypothesentests, Konfidenzintervalle und lineare Regression.</td>
                </tr>
                <tr>
                  <td class="p-3 font-semibold text-white">Statistik I (Deskriptive Statistik)</td>
                  <td class="p-3 whitespace-nowrap text-[#8f8888]">Bereich A</td>
                  <td class="p-3 text-center">6</td>
                  <td class="p-3 text-center"><span class="status-pill status-pill-neutral">4,0</span></td>
                  <td class="p-3">Empirische Verteilungen, Lage- und Streuungsmaße, Korrelationsrechnung und Zeitreihenanalyse.</td>
                </tr>
                <tr>
                  <td class="p-3 font-semibold text-white">Mathematik für Wirtschaftswissenschaftler</td>
                  <td class="p-3 whitespace-nowrap text-[#8f8888]">Bereich A</td>
                  <td class="p-3 text-center">9</td>
                  <td class="p-3 text-center"><span class="status-pill status-pill-neutral">4,0</span></td>
                  <td class="p-3">Lineare Algebra, Matrizenrechnung, Differentialrechnung und Optimierung unter Nebenbedingungen.</td>
                </tr>
                <tr>
                  <td class="p-3 font-semibold text-white">Schreibwerkstatt: Vom studentischen zum beruflichen Schreiben</td>
                  <td class="p-3 whitespace-nowrap text-[#8f8888]">Schlüsselqualifikationen</td>
                  <td class="p-3 text-center">3</td>
                  <td class="p-3 text-center"><span class="status-pill status-pill-green">Bestanden</span></td>
                  <td class="p-3">Strukturierte Berichtserstellung, Business Communication und adressatengerechte Dokumentation.</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

      </div>
"""
