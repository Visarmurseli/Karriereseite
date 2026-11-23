# -*- coding: utf-8 -*-

def get_thesis():
    return """
      <!-- ================= TAB 7: 300 ECTS ACADEMIC KNOWLEDGE HUB (BACHELOR & MASTER) ================= -->
      <div v-show="activeTab === 'thesis'" class="space-y-6">
        
        <!-- Header Hero -->
        <div class="bg-[#141414] p-6 rounded-2xl border border-white/10 shadow-sm space-y-4">
          <div class="flex flex-col md:flex-row md:items-center justify-between gap-3">
            <div>
              <span class="text-xs font-bold text-[#f87171] uppercase tracking-wider">
                Universität Stuttgart | Fakultät für Wirtschafts- und Sozialwissenschaften
              </span>
              <h3 class="text-xl font-extrabold text-white mt-1">
                300 ECTS Academic Knowledge Hub: Bachelor & Master Single Source of Truth
              </h3>
              <p class="text-xs text-[#8f8888] mt-1">
                Visar Murseli, M.Sc. Wirtschaftsinformatik (M.Sc. Note 1,6 „gut“ | Masterarbeit 1,0 „sehr gut“ | B.Sc. 180 ECTS Note 3,0 | Bachelorarbeit 1,7 „gut“)
              </p>
            </div>
            <div class="flex flex-wrap items-center gap-2">
              <span class="tag-badge bg-emerald-600 text-white font-bold text-xs whitespace-nowrap">Masterarbeit: Note 1,0 (30 ECTS)</span>
              <span class="tag-badge bg-[#bf262e] text-white font-bold text-xs whitespace-nowrap">M.Sc. Gesamtnote: 1,6 (120 ECTS)</span>
              <span class="tag-badge bg-indigo-100 text-indigo-800 dark:bg-indigo-900/60 dark:text-indigo-300 font-bold text-xs whitespace-nowrap">Bachelorarbeit: Note 1,7 (12 ECTS)</span>
              <span class="tag-badge bg-purple-100 text-purple-800 dark:bg-purple-900/60 dark:text-purple-300 font-bold text-xs whitespace-nowrap">B.Sc. Gesamtnote: 3,0 (180 ECTS)</span>
            </div>
          </div>

          <!-- 2 Official Degree Certificates Grid -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 pt-1">
            
            <!-- Master Certificate Callout -->
            <div class="p-4 rounded-xl bg-gradient-to-r from-emerald-950/30 to-[#141414] border border-emerald-500/30 text-xs text-[#c4bebe] space-y-2 flex flex-col justify-between">
              <div class="space-y-1.5">
                <div class="flex items-center justify-between">
                  <span class="font-bold text-emerald-900 dark:text-emerald-300 text-sm flex items-center space-x-1.5">
                    <span>📜</span>
                    <span>Master of Science (M.Sc.)</span>
                  </span>
                  <span class="tag-badge bg-emerald-600 text-white font-bold text-[10px]">1,6 (Gut) | 120 ECTS</span>
                </div>
                <p class="text-[11px] text-[#c4bebe] leading-relaxed">
                  Ausgestellt am <strong>17. September 2026</strong> durch Prüfungsausschussvorsitzenden Prof. Dr. Christian Becker. 
                  Masterarbeit bei Prof. Dr. Georg Herzwurm mit der <strong>Spitzennote 1,0 (sehr gut)</strong>.
                </p>
              </div>
              <div class="pt-2 border-t border-emerald-200 dark:border-emerald-800 flex flex-wrap items-center justify-between gap-1">
                <span class="text-[10px] text-slate-500 font-mono">Masterzeugnis & Masterarbeit</span>
                <div class="flex items-center space-x-1.5">
                  <span class="inline-flex items-center space-x-1 px-2.5 py-1 rounded bg-emerald-600/30 text-emerald-300 border border-emerald-500/40 font-bold text-[11px]">
                    <span>📄</span>
                    <span>Zeugnis verifiziert</span>
                  </span>
                  <span class="inline-flex items-center space-x-1 px-2.5 py-1 rounded bg-white/10 text-white font-bold text-[11px] border border-white/15">
                    <span>⭐</span>
                    <span>Masterarbeit (1,0)</span>
                  </span>
                </div>
              </div>
            </div>

            <!-- Bachelor Certificate Callout -->
            <div class="p-4 rounded-xl bg-gradient-to-r from-[#1c080a] to-[#141414] border border-[#bf262e]/30 text-xs text-[#c4bebe] space-y-2 flex flex-col justify-between">
              <div class="space-y-1.5">
                <div class="flex items-center justify-between">
                  <span class="font-bold text-blue-900 dark:text-blue-300 text-sm flex items-center space-x-1.5">
                    <span>📜</span>
                    <span>Bachelor of Science (B.Sc.)</span>
                  </span>
                  <span class="tag-badge bg-[#bf262e] text-white font-bold text-[10px]">3,0 | 180 ECTS</span>
                </div>
                <p class="text-[11px] text-[#c4bebe] leading-relaxed">
                  Amtliche Leistungsübersicht (Dezernat 3 - Studium, Universität Stuttgart).
                  Bachelorarbeit: <strong>Note 1,7 (gut)</strong> bei Prof. Herzwurm. 
                  Bestnote <strong>1,0 in Informationssysteme im E-Business</strong>.
                </p>
              </div>
              <div class="pt-2 border-t border-white/10 flex items-center justify-between">
                <span class="text-[10px] text-[#8f8888] font-mono">Amtliche Leistungsübersicht</span>
                <span class="inline-flex items-center space-x-1 px-2.5 py-1 rounded bg-[#bf262e]/30 text-white font-bold text-[11px] border border-[#bf262e]/40">
                  <span>📄</span>
                  <span>Bachelorzeugnis verifiziert</span>
                </span>
              </div>
            </div>

          </div>

          <!-- Academic Growth Story (Der Rote Faden) -->
          <div class="p-4 rounded-xl bg-gradient-to-r from-slate-50 to-indigo-50/40 dark:from-slate-800/60 dark:to-indigo-950/30 border border-white/10 text-xs text-[#c4bebe] leading-relaxed space-y-2">
            <div class="font-bold text-white flex items-center space-x-2">
              <span>🚀</span>
              <span>Die akademische Entwicklung: Von den Bachelor-Grundlagen zur Master-Spitzenleistung (+1,4 Notenpunkte)</span>
            </div>
            <p class="text-[11px] text-[#c4bebe]">
              Im Bachelorstudium (180 ECTS) hast du das breite und fordernde ingenieurwissenschaftliche Fundament erworben: Höhere Mathematik, Theoretische Informatik, Algorithmen, Datenstrukturen, Java-Programmierung und Rechnungslegung. Im Masterstudium (120 ECTS) hast du deine Spezialisierung voll entfaltet: Software-Architektur (1,7), Advanced Software Engineering (1,6), Cloud Computing (2,0) und die mit der <strong>Traumnote 1,0</strong> bewertete Masterarbeit. Deine Notensteigerung von <strong>3,0 auf 1,6</strong> belegt deine außerordentliche Lernkurve, Zielstrebigkeit und architektonische Reife!
            </p>
          </div>

          <!-- Interactive Degree View Selector -->
          <div class="flex flex-wrap items-center gap-2 pt-1 border-t border-slate-100 dark:border-slate-800">
            <span class="text-xs font-semibold text-slate-500 mr-1">Ansicht filtern:</span>
            <button @click="degreeTab = 'all'" :class="degreeTab === 'all' ? 'bg-[#bf262e] text-white shadow-sm' : 'bg-white/10 text-[#c4bebe] hover:bg-slate-200'" class="px-3 py-1.5 rounded-lg text-xs font-bold transition">
              🌐 Alle 300 ECTS (Gesamtübersicht)
            </button>
            <button @click="degreeTab = 'master'" :class="degreeTab === 'master' ? 'bg-emerald-600 text-white shadow-sm' : 'bg-white/10 text-[#c4bebe] hover:bg-slate-200'" class="px-3 py-1.5 rounded-lg text-xs font-bold transition">
              🎓 Master of Science (120 ECTS | Note 1,6)
            </button>
            <button @click="degreeTab = 'bachelor'" :class="degreeTab === 'bachelor' ? 'bg-indigo-600 text-white shadow-sm' : 'bg-white/10 text-[#c4bebe] hover:bg-slate-200'" class="px-3 py-1.5 rounded-lg text-xs font-bold transition">
              🏛️ Bachelor of Science (180 ECTS | Note 3,0)
            </button>
            <button @click="degreeTab = 'synergies'" :class="degreeTab === 'synergies' ? 'bg-purple-600 text-white shadow-sm' : 'bg-white/10 text-[#c4bebe] hover:bg-slate-200'" class="px-3 py-1.5 rounded-lg text-xs font-bold transition">
              ⚡ 300 ECTS Synergie-Cluster (Knowledge Graph)
            </button>
          </div>
        </div>

        <!-- ================= SECTION: 300 ECTS KNOWLEDGE GRAPH & SYNERGIES ================= -->
        <div v-show="degreeTab === 'all' || degreeTab === 'synergies'" class="bg-[#141414] p-6 rounded-2xl border border-white/10 shadow-sm space-y-4">
          <div class="flex items-center justify-between">
            <h3 class="text-base font-bold text-white flex items-center space-x-2">
              <span>⚡</span>
              <span>Das 300 ECTS Synergie-Netzwerk: Bachelor ➔ Master ➔ Enterprise-Praxis</span>
            </h3>
            <span class="tag-badge bg-purple-100 text-purple-800 dark:bg-purple-900/60 dark:text-purple-300">Single Source of Truth</span>
          </div>
          <p class="text-xs text-slate-500">
            Wie sich deine universitären Grundlagen über 6 Jahre hinweg zu einer unschlagbaren Enterprise-Architektur- und Transformationskompetenz verdichtet haben:
          </p>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
            
            <!-- Cluster 1: Architecture & Platforms -->
            <div class="p-4 rounded-xl border border-blue-200 dark:border-blue-800/80 bg-blue-50/20 dark:bg-blue-950/20 space-y-2">
              <div class="font-bold text-blue-700 dark:text-blue-400 text-sm flex items-center justify-between">
                <span>1. Enterprise Architecture, Plattformen & Boundary Resources</span>
                <span class="tag-badge bg-[#bf262e] text-white text-[10px]">Kern-Kompetenz</span>
              </div>
              <div class="text-[11px] text-[#c4bebe] space-y-1">
                <p><strong>Bachelor:</strong> PSE (Java/OOP), Datenstrukturen & Algorithmen (3,0), Softwaretechnik, <strong>Bachelorarbeit: Boundary Resources (1,7)</strong> bei OutSystems & Mendix.</p>
                <p><strong>Master:</strong> <strong>Software-Architektur (1,7)</strong>, <strong>Advanced Software Engineering (1,6)</strong>, <strong>Cloud Computing (2,0)</strong>, <strong>Masterarbeit: S/4HANA Plattformisierung (1,0)</strong>.</p>
                <p><strong>Praxis (SSB):</strong> BTP-Zielarchitektur, API-Management (xSuite, PATRIS), ES4-Mandantenlandschaft mit Axians, TOGAF ADM.</p>
                <div class="text-blue-800 dark:text-blue-300 font-semibold pt-1">
                  ➔ Synergie-Wert: Du beherrschst die Entkopplung von Kern- und Cloud-Systemen von der theoretischen Modellierung bis zum realen SAP-Großprojekt.
                </div>
              </div>
            </div>

            <!-- Cluster 2: Kaufmännische Prozesse & ERP -->
            <div class="p-4 rounded-xl border border-emerald-200 dark:border-emerald-800/80 bg-emerald-50/20 dark:bg-emerald-950/20 space-y-2">
              <div class="font-bold text-emerald-700 dark:text-emerald-400 text-sm flex items-center justify-between">
                <span>2. Kaufmännische Prozesse, ERP & Finance</span>
                <span class="tag-badge bg-emerald-600 text-white text-[10px]">Business & IT</span>
              </div>
              <div class="text-[11px] text-[#c4bebe] space-y-1">
                <p><strong>Bachelor:</strong> Einführung BWL, Einführung Rechnungswesen, Finanzprozesse (2,7), Modellierung (2,3), <strong>Informationssysteme im E-Business (1,0 - Bestnote)</strong>.</p>
                <p><strong>Master:</strong> <strong>Digitale Nachhaltigkeit (1,0 - Fallstudie Schmalz)</strong>, Innovationsmanagement (1,7), INUT (1,7), Service Operations Management (3,0).</p>
                <p><strong>Praxis (SSB):</strong> TP2 Lösungsdesign (FI/CO/MM/RE-FX), Trennungsrechnung kaufmännisch/steuerlich, Eröffnungsbilanz-Abgleich auf 0,00 € Übernahmekonto.</p>
                <div class="text-emerald-800 dark:text-emerald-300 font-semibold pt-1">
                  ➔ Synergie-Wert: Du sprichst die Sprache der Buchhaltung und des Controllings genauso fließend wie die der IT-Entwickler.
                </div>
              </div>
            </div>

            <!-- Cluster 3: Data, Analytics & AI -->
            <div class="p-4 rounded-xl border border-purple-200 dark:border-purple-800/80 bg-purple-50/20 dark:bg-purple-950/20 space-y-2">
              <div class="font-bold text-purple-700 dark:text-purple-400 text-sm flex items-center justify-between">
                <span>3. Data Architecture, Analytics & Artificial Intelligence</span>
                <span class="tag-badge bg-purple-600 text-white text-[10px]">Data & Intelligence</span>
              </div>
              <div class="text-[11px] text-[#c4bebe] space-y-1">
                <p><strong>Bachelor:</strong> Statistik 1 (4,0) & Statistik 2 (2,7), Wissensverarbeitung (3,7), Business Intelligence (2,7).</p>
                <p><strong>Master:</strong> Datenbanken & Informationssysteme (2,7), <strong>AI4IoT (2,0)</strong>, <strong>Applied AI (1,7)</strong>, <strong>FPWI: Smart Service Blueprinting (1,3 - SUS-Score 85/100)</strong>.</p>
                <p><strong>Praxis (SSB):</strong> Datenmigrations-Cockpit (LTMC Staging-Tabellen, CVI Business Partner Konsolidierung), Signavio Process Insights.</p>
                <div class="text-purple-800 dark:text-purple-300 font-semibold pt-1">
                  ➔ Synergie-Wert: Fundiertes Datenverständnis von relationalen SQL/HANA-Modellen bis hin zu modernen generativen KI- und IoT-Architekturen.
                </div>
              </div>
            </div>

            <!-- Cluster 4: Governance, PMO & Leadership -->
            <div class="p-4 rounded-xl border border-amber-200 dark:border-amber-800/80 bg-amber-50/20 dark:bg-amber-950/20 space-y-2">
              <div class="font-bold text-amber-700 dark:text-amber-400 text-sm flex items-center justify-between">
                <span>4. Transformations-Governance, PMO & Leadership</span>
                <span class="tag-badge bg-amber-600 text-white text-[10px]">PMO & Governance</span>
              </div>
              <div class="text-[11px] text-[#c4bebe] space-y-1">
                <p><strong>Bachelor:</strong> Management von Dienstleistungsunternehmen (4,0), Human Resource Management (3,0), Informatikrecht (4,0), SQ Schreibwerkstatt.</p>
                <p><strong>Master:</strong> <strong>Seminar Wirtschaftsinformatik 2 (1,7 - SLR PRISMA 2020)</strong>, Forschungsmethoden (1,7), Management von IT-Unternehmen (3,0).</p>
                <p><strong>Praxis (SSB):</strong> 24 Monate IT-PMO (TP5), Steuerung von Partnern (Nagarro, Axians, Evora), SAP Cloud ALM Quality Gates, Betriebsvereinbarung mit Betriebsrat.</p>
                <div class="text-amber-800 dark:text-amber-300 font-semibold pt-1">
                  ➔ Synergie-Wert: Lückenlose Methodenkompetenz für C-Level Steering Committees, Stakeholder-Alignment und agile Fit-to-Standard Governance.
                </div>
              </div>
            </div>

          </div>
        </div>

        <!-- ================= SECTION: MASTER-CURRICULUM (120 ECTS | NOTE 1,6) ================= -->
        <div v-show="degreeTab === 'all' || degreeTab === 'master'" class="bg-[#141414] p-6 rounded-2xl border border-white/10 shadow-sm space-y-4">
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
            <div>
              <div class="flex items-center space-x-2">
                <span class="text-lg">🎓</span>
                <h3 class="text-base font-bold text-white">
                  Master-Curriculum: Alle 16 Prüfungsleistungen (120 ECTS | Gesamtnote 1,6)
                </h3>
              </div>
              <p class="text-xs text-slate-500">
                Offiziell verbürgt im Zeugnis über die Masterprüfung (Universität Stuttgart, 17.09.2026, Prof. Becker)
              </p>
            </div>
            <span class="tag-badge bg-emerald-600 text-white font-bold text-xs whitespace-nowrap">
              Masterarbeit: Note 1,0 (30 ECTS)
            </span>
          </div>

          <div class="overflow-x-auto">
            <table class="w-full text-left text-xs border border-white/10 rounded-xl overflow-hidden">
              <thead class="bg-white/10 text-white font-bold">
                <tr>
                  <th class="p-3 border-b dark:border-slate-700">Katalog / Modulbezeichnung</th>
                  <th class="p-3 border-b dark:border-slate-700 whitespace-nowrap">Bereich</th>
                  <th class="p-3 border-b dark:border-slate-700 text-center">ECTS</th>
                  <th class="p-3 border-b dark:border-slate-700 text-center">Note</th>
                  <th class="p-3 border-b dark:border-slate-700">Akademischer Inhalt & Praxisrelevanz</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-slate-200 dark:divide-slate-700 text-[#c4bebe]">
                
                <!-- MASTERARBEIT -->
                <tr class="bg-emerald-50/40 dark:bg-emerald-950/20 font-medium">
                  <td class="p-3 font-bold text-white">
                    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                      <span>⭐ Masterarbeit: Kritische Erfolgsfaktoren in der Transformation großer ERP-Systeme: Eine Untersuchung am Beispiel der Plattformisierung von SAP S/4HANA</span>
                      <span class="inline-flex items-center space-x-1 px-2 py-0.5 rounded bg-emerald-600/30 text-emerald-300 border border-emerald-500/40 font-bold text-[10px] whitespace-nowrap self-start sm:self-auto">
                        <span>📄</span>
                        <span>126 Seiten • 12 Interviews</span>
                      </span>
                    </div>
                  </td>
                  <td class="p-3 whitespace-nowrap text-slate-500">Masterarbeit</td>
                  <td class="p-3 font-bold text-center">30</td>
                  <td class="p-3 text-center"><span class="tag-badge bg-emerald-600 text-white font-bold">1,0</span></td>
                  <td class="p-3">Kritische Erfolgsfaktoren (CSF) und Plattformisierung großer ERP-Systeme, Plattform-Governance, 12 leitfadengestützte Experteninterviews im Großprojekt SSB AG. Qualitative Inhaltsanalyse nach Mayring. Höchste universitäre Auszeichnung (Note 1,0).</td>
                </tr>

                <!-- VERTIEFUNGSMODULE (66 ECTS) -->
                <tr>
                  <td class="p-3 font-semibold text-white">Forschungsmethoden in der Wirtschaftsinformatik</td>
                  <td class="p-3 whitespace-nowrap text-slate-500">Pflichtmodul</td>
                  <td class="p-3 text-center">6</td>
                  <td class="p-3 text-center"><span class="tag-badge bg-blue-100 text-blue-800 dark:bg-blue-900/60 dark:text-blue-300 font-bold">1,7</span></td>
                  <td class="p-3">Design Science Research Methodology (DSRM nach Peffers), qualitative Inhaltsanalyse nach Mayring, quantitative Hypothesenprüfung. Wissenschaftliches Fundament.</td>
                </tr>

                <tr class="bg-blue-50/20 dark:bg-blue-950/10">
                  <td class="p-3 font-semibold text-white">Forschungsprojekte in der Wirtschaftsinformatik (FPWI)</td>
                  <td class="p-3 whitespace-nowrap text-slate-500">Katalog WI</td>
                  <td class="p-3 text-center font-bold">6</td>
                  <td class="p-3 text-center"><span class="tag-badge bg-[#bf262e] text-white font-bold">1,3</span></td>
                  <td class="p-3">Smart Service Blueprinting Framework für cyber-physische Systeme & IoT. DSRM, Thinking-Aloud Tests, empirischer SUS-Score 85/100 (Grade A / Excellent).</td>
                </tr>

                <tr>
                  <td class="p-3 font-semibold text-white">AI4IoT – Artificial Intelligence for the Internet of Things</td>
                  <td class="p-3 whitespace-nowrap text-slate-500">Katalog WI</td>
                  <td class="p-3 text-center">6</td>
                  <td class="p-3 text-center"><span class="tag-badge bg-slate-200 dark:bg-slate-700 text-slate-800 dark:text-slate-200 font-semibold">2,0</span></td>
                  <td class="p-3">Sensorik-Datenströme, Edge Computing, Predictive Maintenance im industriellen Maschinenbau, Time-Series Forecasting für verteilte Anlagen.</td>
                </tr>

                <tr>
                  <td class="p-3 font-semibold text-white">Management von IT-Unternehmen</td>
                  <td class="p-3 whitespace-nowrap text-slate-500">Katalog WI</td>
                  <td class="p-3 text-center">6</td>
                  <td class="p-3 text-center"><span class="tag-badge bg-slate-200 dark:bg-slate-700 text-slate-800 dark:text-slate-200 font-semibold">3,0</span></td>
                  <td class="p-3">IT-Governance, COBIT, ITIL Service Lifecycle, Sourcing-Modelle, IT-Kostenrechnung und Budgetierung für Enterprise-IT.</td>
                </tr>

                <tr class="bg-purple-50/20 dark:bg-purple-950/10">
                  <td class="p-3 font-semibold text-white">Seminar Wirtschaftsinformatik 2</td>
                  <td class="p-3 whitespace-nowrap text-slate-500">Katalog Seminar WI</td>
                  <td class="p-3 text-center">6</td>
                  <td class="p-3 text-center"><span class="tag-badge bg-purple-600 text-white font-bold">1,7</span></td>
                  <td class="p-3">Systematische Literaturanalyse (SLR nach PRISMA 2020) über 5 Fachdatenbanken (570 gefundene Studien): KI-gestützte Mensch-Roboter-Kollaboration in der Produktion (Industrie 5.0).</td>
                </tr>

                <tr class="bg-indigo-50/20 dark:bg-indigo-950/10">
                  <td class="p-3 font-semibold text-white">Advanced Software Engineering (ASE)</td>
                  <td class="p-3 whitespace-nowrap text-slate-500">Katalog Software Eng.</td>
                  <td class="p-3 text-center font-bold">6</td>
                  <td class="p-3 text-center"><span class="tag-badge bg-indigo-600 text-white font-bold">1,6</span></td>
                  <td class="p-3">Fortgeschrittene Software-Architekturen, Domain-Driven Design (DDD), CI/CD-Pipelines, automatisiertes Testing, Clean Code und Refactoring im Enterprise-Maßstab.</td>
                </tr>

                <tr class="bg-indigo-50/20 dark:bg-indigo-950/10">
                  <td class="p-3 font-semibold text-white">Software-Architektur</td>
                  <td class="p-3 whitespace-nowrap text-slate-500">Katalog MINF Informatik</td>
                  <td class="p-3 text-center font-bold">6</td>
                  <td class="p-3 text-center"><span class="tag-badge bg-indigo-600 text-white font-bold">1,7</span></td>
                  <td class="p-3">Architekturmuster (Microservices, Event-Driven, SOA), Schnittstellendesign (REST, gRPC, Event Mesh), Bounded Contexts und Entkopplungsstrategien für Cloud-Plattformen.</td>
                </tr>

                <tr>
                  <td class="p-3 font-semibold text-white">Service Management and Cloud Computing, and Evaluation</td>
                  <td class="p-3 whitespace-nowrap text-slate-500">Katalog MINF Informatik</td>
                  <td class="p-3 text-center">6</td>
                  <td class="p-3 text-center"><span class="tag-badge bg-slate-200 dark:bg-slate-700 text-slate-800 dark:text-slate-200 font-semibold">2,0</span></td>
                  <td class="p-3">AWS Well-Architected Framework, Microservices & Serverless (DynamoDB, EventBridge, Step Functions), Cloud Service Level Agreements (SLAs) und quantitative Evaluation.</td>
                </tr>

                <tr>
                  <td class="p-3 font-semibold text-white">Datenbanken und Informationssysteme</td>
                  <td class="p-3 whitespace-nowrap text-slate-500">Katalog MINF Informatik</td>
                  <td class="p-3 text-center">6</td>
                  <td class="p-3 text-center"><span class="tag-badge bg-slate-200 dark:bg-slate-700 text-slate-800 dark:text-slate-200 font-semibold">2,7</span></td>
                  <td class="p-3">Relationale Datenmodelle, SQL-Anfragen, ACID-Transaktionsprinzipien, Indizierungsstrategien, NoSQL- und In-Memory-Konzepte (Fundament für SAP HANA).</td>
                </tr>

                <tr>
                  <td class="p-3 font-semibold text-white">Innovationsmanagement</td>
                  <td class="p-3 whitespace-nowrap text-slate-500">Katalog BWL</td>
                  <td class="p-3 text-center">6</td>
                  <td class="p-3 text-center"><span class="tag-badge bg-slate-200 dark:bg-slate-700 text-slate-800 dark:text-slate-200 font-semibold">1,7</span></td>
                  <td class="p-3">Disruptive Innovationen, Plattform-Ökosysteme, Technologie-Lebenszyklen und strategische Go-to-Market-Planung für digitale Produkte.</td>
                </tr>

                <tr>
                  <td class="p-3 font-semibold text-white">Theorie und Empirie internationaler Unternehmenstätigkeit (INUT)</td>
                  <td class="p-3 whitespace-nowrap text-slate-500">Katalog BWL</td>
                  <td class="p-3 text-center">6</td>
                  <td class="p-3 text-center"><span class="tag-badge bg-slate-200 dark:bg-slate-700 text-slate-800 dark:text-slate-200 font-semibold">1,7</span></td>
                  <td class="p-3">Globale Wertschöpfungsketten, internationale Standortentscheidungen, Multinationale Konzerne (MNE), globales IT-Sourcing und Außenhandelstheorie.</td>
                </tr>

                <!-- ERGÄNZENDE MODULE (24 ECTS) -->
                <tr class="bg-emerald-50/20 dark:bg-emerald-950/10">
                  <td class="p-3 font-semibold text-white">Digitale Nachhaltigkeit (Green IT & CSRD)</td>
                  <td class="p-3 whitespace-nowrap text-slate-500">Ergänzung WI</td>
                  <td class="p-3 text-center font-bold">6</td>
                  <td class="p-3 text-center"><span class="tag-badge bg-emerald-600 text-white font-bold">1,0</span></td>
                  <td class="p-3">Praxis-Fallstudie J. Schmalz GmbH: BPMN-Prozessmodellierung, Schnittstellenintegration und Software-Prototyp zur automatisierten CSRD-Abfallbilanz.</td>
                </tr>

                <tr>
                  <td class="p-3 font-semibold text-white">Applied AI and Upcoming Technologies in Industries</td>
                  <td class="p-3 whitespace-nowrap text-slate-500">Ergänzung WI</td>
                  <td class="p-3 text-center">6</td>
                  <td class="p-3 text-center"><span class="tag-badge bg-slate-200 dark:bg-slate-700 text-slate-800 dark:text-slate-200 font-semibold">1,7</span></td>
                  <td class="p-3">Machine Learning im industriellen Einsatz, NLP, LLM-Architekturen, generative KI und Integration intelligenter Algorithmen in ERP-Geschäftsprozesse.</td>
                </tr>

                <tr>
                  <td class="p-3 font-semibold text-white">Innovationsmethoden für software- und datenintensive Geschäftsmodelle (ISG)</td>
                  <td class="p-3 whitespace-nowrap text-slate-500">Ergänzung WI</td>
                  <td class="p-3 text-center">6</td>
                  <td class="p-3 text-center"><span class="tag-badge bg-slate-200 dark:bg-slate-700 text-slate-800 dark:text-slate-200 font-semibold">2,0</span></td>
                  <td class="p-3">Data-driven Business Models, Plattformökonomie, Venture-Pitch „PatentRadar“ für Klingele Paper & Packaging (KI-gestützte Patentrecherche und RPA-Kernprozesse).</td>
                </tr>

                <tr>
                  <td class="p-3 font-semibold text-white">Service Operations Management (SOM)</td>
                  <td class="p-3 whitespace-nowrap text-slate-500">Ergänzung BWL</td>
                  <td class="p-3 text-center">6</td>
                  <td class="p-3 text-center"><span class="tag-badge bg-slate-200 dark:bg-slate-700 text-slate-800 dark:text-slate-200 font-semibold">3,0</span></td>
                  <td class="p-3">Operations Management, Warteschlangentheorie, Kapazitäts- und Durchsatzoptimierung operativer Dienstleistungsprozesse im Dienstleistungssektor.</td>
                </tr>

              </tbody>
            </table>
          </div>
        </div>

        <!-- ================= SECTION: BACHELOR-CURRICULUM (180 ECTS | NOTE 3,0) ================= -->
        <div v-show="degreeTab === 'all' || degreeTab === 'bachelor'" class="bg-[#141414] p-6 rounded-2xl border border-white/10 shadow-sm space-y-4">
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
            <div>
              <div class="flex items-center space-x-2">
                <span class="text-lg">🏛️</span>
                <h3 class="text-base font-bold text-white">
                  Bachelor-Curriculum: Alle 25+ Prüfungsleistungen (180 ECTS | Gesamtnote 3,0)
                </h3>
              </div>
              <p class="text-xs text-slate-500">
                Amtlich beglaubigt in der Leistungsübersicht B.Sc. Wirtschaftsinformatik (Universität Stuttgart, Abschluss 18.09.2023)
              </p>
            </div>
            <div class="flex items-center gap-2">
              <span class="tag-badge bg-indigo-600 text-white font-bold text-xs whitespace-nowrap">
                Bachelorarbeit: Note 1,7 (12 ECTS)
              </span>
              <span class="tag-badge bg-emerald-600 text-white font-bold text-xs whitespace-nowrap">
                E-Business: Note 1,0 (Bestnote)
              </span>
            </div>
          </div>

          <!-- Bachelor Scorecard Grid -->
          <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs">
            <div class="p-3 bg-white/5 rounded-xl border border-white/10">
              <div class="text-[11px] text-slate-500 font-medium">Bereich B1: Informatik</div>
              <div class="text-lg font-bold text-[#f87171] mt-0.5">48 ECTS</div>
              <div class="text-[10px] text-slate-500">Modellierung 2,3 | DSA 3,0</div>
            </div>
            <div class="p-3 bg-white/5 rounded-xl border border-white/10">
              <div class="text-[11px] text-slate-500 font-medium">Bereich B2: Wirtschaftsinformatik</div>
              <div class="text-lg font-bold text-emerald-600 mt-0.5">45 ECTS</div>
              <div class="text-[10px] text-emerald-600 font-bold">E-Business: 1,0 | IVP: 2,3</div>
            </div>
            <div class="p-3 bg-white/5 rounded-xl border border-white/10">
              <div class="text-[11px] text-slate-500 font-medium">Bereich B3 & C: BWL / VWL</div>
              <div class="text-lg font-bold text-purple-600 mt-0.5">45 ECTS</div>
              <div class="text-[10px] text-slate-500">Finanzprozess 2,7 | Märkte 2,7</div>
            </div>
            <div class="p-3 bg-white/5 rounded-xl border border-white/10">
              <div class="text-[11px] text-slate-500 font-medium">Bachelorarbeit (Prof. Herzwurm)</div>
              <div class="text-lg font-bold text-indigo-600 mt-0.5">1,7 (Gut)</div>
              <div class="text-[10px] text-slate-500">12 ECTS | Boundary Resources</div>
            </div>
          </div>

          <!-- 8-Semester Meilenstein-Chronik & Original-Artefakte Grid -->
          <div class="p-4 rounded-xl border border-indigo-200 dark:border-indigo-800/80 bg-gradient-to-r from-indigo-50/50 to-blue-50/40 dark:from-indigo-950/30 dark:to-blue-950/20 space-y-3">
            <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
              <div class="font-bold text-white text-xs flex items-center space-x-2">
                <span>📁</span>
                <span>Praxisprojekte, Seminararbeiten & Original-Artefakte aus den 8 Bachelor-Semestern</span>
              </div>
              <span class="text-[11px] text-indigo-700 dark:text-indigo-300 font-semibold">100% verifiziert auf NAS & Vault</span>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3 text-xs">
              
              <!-- Card 1: Bachelorarbeit & Verteidigung -->
              <div class="p-3 bg-[#141414] rounded-xl border border-indigo-200 dark:border-indigo-800 space-y-2 flex flex-col justify-between">
                <div>
                  <div class="flex items-center justify-between">
                    <span class="font-bold text-indigo-700 dark:text-indigo-400 text-xs">Bachelorarbeit & Kolloquium</span>
                    <span class="tag-badge bg-indigo-600 text-white text-[10px]">Note 1,7 | 12 ECTS</span>
                  </div>
                  <div class="text-[11px] font-semibold text-white mt-1">Boundary Resources in Low-Code Plattformen</div>
                  <p class="text-[10px] text-slate-500 mt-0.5">Lehrstuhl Prof. Dr. Georg Herzwurm. Analyse von 14 Boundary-Resource-Klassen (ABR, DBR, SBR) bei OutSystems & Mendix.</p>
                </div>
                <div class="pt-2 border-t border-white/10 flex flex-wrap gap-1">
                  <span class="px-2 py-0.5 rounded bg-indigo-500/20 text-indigo-300 border border-indigo-500/30 text-[10px] font-bold">📄 Volltext archiviert</span>
                  <span class="px-2 py-0.5 rounded bg-white/10 text-[#c4bebe] text-[10px] font-bold">📋 14 Boundary Classes</span>
                  <span class="px-2 py-0.5 rounded bg-amber-500/20 text-amber-300 border border-amber-500/30 text-[10px] font-bold">📊 Kolloquium 1,7</span>
                </div>
              </div>

              <!-- Card 2: 5. Semester E-Business 1,0 -->
              <div class="p-3 bg-[#141414] rounded-xl border border-emerald-200 dark:border-emerald-800 space-y-2 flex flex-col justify-between">
                <div>
                  <div class="flex items-center justify-between">
                    <span class="font-bold text-emerald-700 dark:text-emerald-400 text-xs">5. Semester: E-Business</span>
                    <span class="tag-badge bg-emerald-600 text-white text-[10px]">Bestnote 1,0</span>
                  </div>
                  <div class="text-[11px] font-semibold text-white mt-1">Informationssysteme im E-Business</div>
                  <p class="text-[10px] text-slate-500 mt-0.5">B2B-Marktplätze, E-Procurement, Function-Point-Analyse, Aufwandsschätzung, Testmanagement und Design Thinking.</p>
                </div>
                <div class="pt-2 border-t border-slate-100 dark:border-slate-800">
                  <span class="text-[10px] text-emerald-700 dark:text-emerald-300 font-medium">➔ Direkte Brücke zu S/4HANA B2B & Cloud ALM</span>
                </div>
              </div>

              <!-- Card 3: 4. Semester IVP Unternehmensanalyse -->
              <div class="p-3 bg-[#141414] rounded-xl border border-blue-200 dark:border-blue-800 space-y-2 flex flex-col justify-between">
                <div>
                  <div class="flex items-center justify-between">
                    <span class="font-bold text-blue-700 dark:text-blue-400 text-xs">4. Semester: IVP Datenanalyse</span>
                    <span class="tag-badge bg-[#bf262e] text-white text-[10px]">Note 2,3 | 6 ECTS</span>
                  </div>
                  <div class="text-[11px] font-semibold text-white mt-1">Unternehmensanalyse 0x539-Wear GmbH</div>
                  <p class="text-[10px] text-slate-500 mt-0.5">Lehrstuhl Abteilung VII (WI). Detaillierte Bestellungs-, Plan-Ist-, Kosten-, Kunden-, Artikel- und Lieferanten-Deckungsbeitragsrechnung.</p>
                </div>
                <div class="pt-2 border-t border-white/10 flex items-center justify-between">
                  <span class="text-[10px] text-[#8f8888] font-mono">Deckungsbeitragsrechnung</span>
                  <span class="px-2 py-0.5 rounded bg-blue-500/20 text-blue-300 border border-blue-500/30 text-[10px] font-bold">📄 Analyse verifiziert</span>
                </div>
              </div>

              <!-- Card 4: 6. Semester Bachelorseminar Büttgen -->
              <div class="p-3 bg-[#141414] rounded-xl border border-purple-200 dark:border-purple-800 space-y-2 flex flex-col justify-between">
                <div>
                  <div class="flex items-center justify-between">
                    <span class="font-bold text-purple-700 dark:text-purple-400 text-xs">6. Semester: Bachelorseminar</span>
                    <span class="tag-badge bg-purple-600 text-white text-[10px]">6 ECTS | Büttgen</span>
                  </div>
                  <div class="text-[11px] font-semibold text-white mt-1">Mensch-Roboter-Interaktion & Servicequalität</div>
                  <p class="text-[10px] text-slate-500 mt-0.5">Universität Hohenheim (Prof. Dr. Marion Büttgen). Messung von Kundenzufriedenheit und Servicequalität über Expectation-Confirmation.</p>
                </div>
                <div class="pt-2 border-t border-white/10 flex items-center justify-between">
                  <span class="text-[10px] text-[#8f8888] font-mono">Büttgen Seminararbeit</span>
                  <span class="px-2 py-0.5 rounded bg-purple-500/20 text-purple-300 border border-purple-500/30 text-[10px] font-bold">📄 Paper verifiziert</span>
                </div>
              </div>

              <!-- Card 5: 6. Semester Modellierung (BPMN / SQL) -->
              <div class="p-3 bg-[#141414] rounded-xl border border-white/10 space-y-2 flex flex-col justify-between">
                <div>
                  <div class="flex items-center justify-between">
                    <span class="font-bold text-[#c4bebe] text-xs">6. Semester: Modellierung</span>
                    <span class="tag-badge bg-slate-200 dark:bg-slate-700 text-slate-800 dark:text-slate-200 text-[10px]">Note 2,3 | 6 ECTS</span>
                  </div>
                  <div class="text-[11px] font-semibold text-white mt-1">BPMN 2.0, ER-Modelle, Petrinetze & SQL</div>
                  <p class="text-[10px] text-slate-500 mt-0.5">Formale Geschäftsprozessmodellierung in BPMN 2.0, Relationale Algebra, Normalformen, SQL DDL/DML und Metamodellierung.</p>
                </div>
                <div class="pt-2 border-t border-slate-100 dark:border-slate-800">
                  <span class="text-[10px] text-blue-700 dark:text-blue-300 font-medium">➔ Fundament für SAP Signavio & Green IT Fallstudie</span>
                </div>
              </div>

              <!-- Card 6: TOGAF & Enterprise Architecture -->
              <div class="p-3 bg-[#141414] rounded-xl border border-teal-200 dark:border-teal-800 space-y-2 flex flex-col justify-between">
                <div>
                  <div class="flex items-center justify-between">
                    <span class="font-bold text-teal-700 dark:text-teal-400 text-xs">EAM-Zertifizierung</span>
                    <span class="tag-badge bg-teal-600 text-white text-[10px]">Scape Consulting</span>
                  </div>
                  <div class="text-[11px] font-semibold text-white mt-1">TOGAF 9 ADM-Intensivkurs</div>
                  <p class="text-[10px] text-slate-500 mt-0.5">Dozent: Dr. Daniel Simon (Scape Consulting GmbH, Uni Stuttgart). Architecture Development Method, Metamodell, Gap-Analyse & Sichten.</p>
                </div>
                <div class="pt-2 border-t border-white/10 flex items-center justify-between">
                  <span class="text-[10px] text-[#8f8888] font-mono">Scape Consulting</span>
                  <span class="px-2 py-0.5 rounded bg-teal-500/20 text-teal-300 border border-teal-500/30 text-[10px] font-bold">📜 Zertifikat verifiziert</span>
                </div>
              </div>

            </div>
          </div>

          <div class="overflow-x-auto">
            <table class="w-full text-left text-xs border border-white/10 rounded-xl overflow-hidden">
              <thead class="bg-white/10 text-white font-bold">
                <tr>
                  <th class="p-3 border-b dark:border-slate-700">Modulbezeichnung</th>
                  <th class="p-3 border-b dark:border-slate-700 whitespace-nowrap">Bereich nach PO</th>
                  <th class="p-3 border-b dark:border-slate-700 text-center">ECTS</th>
                  <th class="p-3 border-b dark:border-slate-700 text-center">Note</th>
                  <th class="p-3 border-b dark:border-slate-700">Inhaltlicher Kern & Fachkompetenz</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-slate-200 dark:divide-slate-700 text-[#c4bebe]">
                
                <!-- BEREICH D: ABSCHLUSSPROJEKT -->
                <tr class="bg-indigo-50/40 dark:bg-indigo-950/20 font-medium">
                  <td class="p-3 font-bold text-white">
                    ⭐ Bachelorarbeit Wirtschaftsinformatik: Die Bedeutung von Boundary Resources in Low-Code Entwicklungsplattformen (OutSystems & Mendix)
                  </td>
                  <td class="p-3 whitespace-nowrap text-slate-500">Bereich D: Abschlussprojekt</td>
                  <td class="p-3 font-bold text-center">12</td>
                  <td class="p-3 text-center"><span class="tag-badge bg-indigo-600 text-white font-bold">1,7</span></td>
                  <td class="p-3">Boundary Resource Theory (Ghazawneh & Henfridsson). Identifikation von 14 Grenzressourcen-Klassen (ABR, DBR, SBR). Fundament für Schnittstellen- und Plattform-Governance bei Prof. Herzwurm.</td>
                </tr>

                <!-- BEREICH B2: WIRTSCHAFTSINFORMATIK -->
                <tr class="bg-slate-100/80 dark:bg-slate-800/80 font-bold text-white">
                  <td colspan="5" class="p-2.5 uppercase tracking-wider text-[11px] text-emerald-700 dark:text-emerald-400">
                    💻 Säule B 2: Wirtschaftsinformatik (45 ECTS | Note: 2,8)
                  </td>
                </tr>
                <tr class="bg-emerald-50/30 dark:bg-emerald-950/15">
                  <td class="p-3 font-bold text-white">Betriebliche Informationssysteme: Informationssysteme im E-Business</td>
                  <td class="p-3 whitespace-nowrap text-slate-500">B2: WI (Teilleistung)</td>
                  <td class="p-3 text-center font-bold">4,5</td>
                  <td class="p-3 text-center"><span class="tag-badge bg-emerald-600 text-white font-bold">1,0</span></td>
                  <td class="p-3">Elektronische Marktplätze, E-Procurement, digitale B2B-Plattformen und Web-Ökosysteme. Absolute Bestnote!</td>
                </tr>
                <tr>
                  <td class="p-3 font-semibold text-white">Betriebliche Informationssysteme: Management betrieblicher Informationssysteme</td>
                  <td class="p-3 whitespace-nowrap text-slate-500">B2: WI (Teilleistung)</td>
                  <td class="p-3 text-center">4,5</td>
                  <td class="p-3 text-center"><span class="tag-badge bg-slate-200 dark:bg-slate-700 text-slate-800 dark:text-slate-200 font-semibold">2,7</span></td>
                  <td class="p-3">Architektur betrieblicher Standardsoftware (ERP, SCM, CRM), Integration und Geschäftsprozessmanagement.</td>
                </tr>
                <tr class="bg-blue-50/20 dark:bg-blue-950/10">
                  <td class="p-3 font-semibold text-white">Informationsverarbeitungspraktikum (IVP)</td>
                  <td class="p-3 whitespace-nowrap text-slate-500">B2: WI Pflicht</td>
                  <td class="p-3 text-center font-bold">6</td>
                  <td class="p-3 text-center"><span class="tag-badge bg-[#bf262e] text-white font-bold">2,3</span></td>
                  <td class="p-3">Hands-on Softwareentwicklung, Datenanalyse, relationale Abfragen und Implementierung betrieblicher Datenstrecken.</td>
                </tr>
                <tr>
                  <td class="p-3 font-semibold text-white">Einführung in die Wirtschaftsinformatik</td>
                  <td class="p-3 whitespace-nowrap text-slate-500">B2: WI Pflicht</td>
                  <td class="p-3 text-center">6</td>
                  <td class="p-3 text-center"><span class="tag-badge bg-slate-200 dark:bg-slate-700 text-slate-800 dark:text-slate-200 font-semibold">2,7</span></td>
                  <td class="p-3">Grundlagen der Wirtschaftsinformatik, Informationssystem-Architekturen, Datenmodellierung und Geschäftsprozesse.</td>
                </tr>
                <tr>
                  <td class="p-3 font-semibold text-white">Informationsmanagement: Business Intelligence (BI)</td>
                  <td class="p-3 whitespace-nowrap text-slate-500">B2: WI (Teilleistung)</td>
                  <td class="p-3 text-center">4,5</td>
                  <td class="p-3 text-center"><span class="tag-badge bg-slate-200 dark:bg-slate-700 text-slate-800 dark:text-slate-200 font-semibold">2,7</span></td>
                  <td class="p-3">Data Warehousing, ETL-Prozesse, OLAP-Cubes, multidimensionale Datenmodelle und Management-Reporting.</td>
                </tr>
                <tr>
                  <td class="p-3 font-semibold text-white">Informationsmanagement: Grundlagen des Informationsmanagements</td>
                  <td class="p-3 whitespace-nowrap text-slate-500">B2: WI (Teilleistung)</td>
                  <td class="p-3 text-center">4,5</td>
                  <td class="p-3 text-center"><span class="tag-badge bg-slate-200 dark:bg-slate-700 text-slate-800 dark:text-slate-200 font-semibold">3,3</span></td>
                  <td class="p-3">Strategisches, administratives und operatives Informationsmanagement im Unternehmen.</td>
                </tr>
                <tr>
                  <td class="p-3 font-semibold text-white">Softwarepraktikum (SOPRA)</td>
                  <td class="p-3 whitespace-nowrap text-slate-500">B2: WI Pflicht</td>
                  <td class="p-3 text-center">6</td>
                  <td class="p-3 text-center"><span class="tag-badge bg-slate-200 dark:bg-slate-700 text-slate-800 dark:text-slate-200 font-semibold">3,0</span></td>
                  <td class="p-3">Agiles Team-Entwicklungsprojekt, Scrum-Methodik, Versionskontrolle (Git), Software-Architektur und Qualitätssicherung.</td>
                </tr>
                <tr>
                  <td class="p-3 font-semibold text-white">Wissensverarbeitung</td>
                  <td class="p-3 whitespace-nowrap text-slate-500">B2: WI Pflicht</td>
                  <td class="p-3 text-center">6</td>
                  <td class="p-3 text-center"><span class="tag-badge bg-slate-200 dark:bg-slate-700 text-slate-800 dark:text-slate-200 font-semibold">3,7</span></td>
                  <td class="p-3">Ontologien, Wissensbasierte Systeme, Logikprogrammierung, Inferenzmechanismen und semantische Netze.</td>
                </tr>
                <tr>
                  <td class="p-3 font-semibold text-white">Informatikrecht</td>
                  <td class="p-3 whitespace-nowrap text-slate-500">B2: WI Pflicht</td>
                  <td class="p-3 text-center">3</td>
                  <td class="p-3 text-center"><span class="tag-badge bg-slate-200 dark:bg-slate-700 text-slate-800 dark:text-slate-200 font-semibold">4,0</span></td>
                  <td class="p-3">Datenschutzrecht (DSGVO), Urheberrecht an Software, IT-Vertragsrecht und Haftung bei Cloud-Diensten.</td>
                </tr>

                <!-- BEREICH B1: INFORMATIK -->
                <tr class="bg-slate-100/80 dark:bg-slate-800/80 font-bold text-white">
                  <td colspan="5" class="p-2.5 uppercase tracking-wider text-[11px] text-blue-700 dark:text-blue-400">
                    🖥️ Säule B 1: Informatik & Softwaretechnik (48 ECTS | Note: 3,3)
                  </td>
                </tr>
                <tr class="bg-blue-50/20 dark:bg-blue-950/10">
                  <td class="p-3 font-semibold text-white">Modellierung</td>
                  <td class="p-3 whitespace-nowrap text-slate-500">B1: Informatik Pflicht</td>
                  <td class="p-3 text-center font-bold">6</td>
                  <td class="p-3 text-center"><span class="tag-badge bg-[#bf262e] text-white font-bold">2,3</span></td>
                  <td class="p-3">UML-Klassendiagramme, Sequenzdiagramme, Zustandsautomaten, Petrinetze und formale Modellierungssysteme.</td>
                </tr>
                <tr>
                  <td class="p-3 font-semibold text-white">Datenstrukturen und Algorithmen (DSA)</td>
                  <td class="p-3 whitespace-nowrap text-slate-500">B1: Informatik Pflicht</td>
                  <td class="p-3 text-center">9</td>
                  <td class="p-3 text-center"><span class="tag-badge bg-slate-200 dark:bg-slate-700 text-slate-800 dark:text-slate-200 font-semibold">3,0</span></td>
                  <td class="p-3">Bäume, Graphen, Such- und Sortieralgorithmen, Laufzeitkomplexität (O-Notation) und algorithmische Effizienz.</td>
                </tr>
                <tr>
                  <td class="p-3 font-semibold text-white">Programmentwicklung</td>
                  <td class="p-3 whitespace-nowrap text-slate-500">B1: Informatik Pflicht</td>
                  <td class="p-3 text-center">6</td>
                  <td class="p-3 text-center"><span class="tag-badge bg-slate-200 dark:bg-slate-700 text-slate-800 dark:text-slate-200 font-semibold">3,0</span></td>
                  <td class="p-3">Fortgeschrittene Programmierung, Clean Code, Test-Driven Development (TDD), Entwurfsmuster und Modularisierung.</td>
                </tr>
                <tr>
                  <td class="p-3 font-semibold text-white">Mensch-Computer-Interaktion (MCI)</td>
                  <td class="p-3 whitespace-nowrap text-slate-500">B1: Informatik Wahlpflicht</td>
                  <td class="p-3 text-center">6</td>
                  <td class="p-3 text-center"><span class="tag-badge bg-slate-200 dark:bg-slate-700 text-slate-800 dark:text-slate-200 font-semibold">3,3</span></td>
                  <td class="p-3">Usability Engineering, User Experience (UX), Interaktionsdesign, Usability-Tests und UI-Prototyping.</td>
                </tr>
                <tr>
                  <td class="p-3 font-semibold text-white">Einführung in die Softwaretechnik (EST)</td>
                  <td class="p-3 whitespace-nowrap text-slate-500">B1: Informatik Pflicht</td>
                  <td class="p-3 text-center">6</td>
                  <td class="p-3 text-center"><span class="tag-badge bg-slate-200 dark:bg-slate-700 text-slate-800 dark:text-slate-200 font-semibold">3,7</span></td>
                  <td class="p-3">Software-Lebenszyklusmodelle, Anforderungsanalyse (Requirements Engineering), Softwaretests und Konfigurationsmanagement.</td>
                </tr>
                <tr>
                  <td class="p-3 font-semibold text-white">Automaten und Formale Sprachen</td>
                  <td class="p-3 whitespace-nowrap text-slate-500">B1: Informatik Pflicht</td>
                  <td class="p-3 text-center">6</td>
                  <td class="p-3 text-center"><span class="tag-badge bg-slate-200 dark:bg-slate-700 text-slate-800 dark:text-slate-200 font-semibold">3,7</span></td>
                  <td class="p-3">Reguläre Sprachen, endliche Automaten, kontextfreie Grammatiken, Turing-Maschinen und Berechenbarkeitstheorie.</td>
                </tr>
                <tr>
                  <td class="p-3 font-semibold text-white">Programmierung und Software-Entwicklung (PSE)</td>
                  <td class="p-3 whitespace-nowrap text-slate-500">B1: Informatik Pflicht</td>
                  <td class="p-3 text-center">9</td>
                  <td class="p-3 text-center"><span class="tag-badge bg-slate-200 dark:bg-slate-700 text-slate-800 dark:text-slate-200 font-semibold">4,0</span></td>
                  <td class="p-3">Objektorientierte Programmierung in Java, Vererbung, Polymorphie, Datenkapselung, Collections Framework.</td>
                </tr>

                <!-- BEREICH B3 & C: BWL / VWL / MANAGEMENT -->
                <tr class="bg-slate-100/80 dark:bg-slate-800/80 font-bold text-white">
                  <td colspan="5" class="p-2.5 uppercase tracking-wider text-[11px] text-purple-700 dark:text-purple-400">
                    📊 Säule B 3 & Bereich C: Wirtschaftswissenschaften & Management (45 ECTS)
                  </td>
                </tr>
                <tr>
                  <td class="p-3 font-semibold text-white">GBWL 1: Strukturen der Betriebswirtschaftslehre</td>
                  <td class="p-3 whitespace-nowrap text-slate-500">B3: BWL Hohenheim</td>
                  <td class="p-3 text-center">6</td>
                  <td class="p-3 text-center"><span class="tag-badge bg-slate-200 dark:bg-slate-700 text-slate-800 dark:text-slate-200 font-semibold">2,7</span></td>
                  <td class="p-3">Unternehmensführung, Rechtsformen, Corporate Governance, Standortfaktoren und Wertschöpfungsstrukturen.</td>
                </tr>
                <tr>
                  <td class="p-3 font-semibold text-white">GBWL 4: Finanzprozess (Finanzierung & Investition)</td>
                  <td class="p-3 whitespace-nowrap text-slate-500">B3: BWL Hohenheim</td>
                  <td class="p-3 text-center">6</td>
                  <td class="p-3 text-center"><span class="tag-badge bg-slate-200 dark:bg-slate-700 text-slate-800 dark:text-slate-200 font-semibold">2,7</span></td>
                  <td class="p-3">Investitionsrechnung (Kapitalwertmethode, IZF), Finanzierungsarten, Liquiditätsmanagement und Kapitalstruktur.</td>
                </tr>
                <tr>
                  <td class="p-3 font-semibold text-white">GVWL 1: Märkte & wirtschaftliche Entscheidungen</td>
                  <td class="p-3 whitespace-nowrap text-slate-500">B3: VWL Pflicht</td>
                  <td class="p-3 text-center">6</td>
                  <td class="p-3 text-center"><span class="tag-badge bg-slate-200 dark:bg-slate-700 text-slate-800 dark:text-slate-200 font-semibold">2,7</span></td>
                  <td class="p-3">Mikroökonomie, Marktformen, Preisbildung, Wohlfahrtstheorie, Angebot und Nachfrage.</td>
                </tr>
                <tr>
                  <td class="p-3 font-semibold text-white">Profilseminar zum Human Resource Management</td>
                  <td class="p-3 whitespace-nowrap text-slate-500">Bereich C: Wahl</td>
                  <td class="p-3 text-center">6</td>
                  <td class="p-3 text-center"><span class="tag-badge bg-slate-200 dark:bg-slate-700 text-slate-800 dark:text-slate-200 font-semibold">3,0</span></td>
                  <td class="p-3">Personalökonomie, Mitarbeiterführung, Anreizsysteme, Talent Management und organisatorischer Wandel.</td>
                </tr>
                <tr>
                  <td class="p-3 font-semibold text-white">BWL 1: Organisation, Personalführung, Strategisches Management</td>
                  <td class="p-3 whitespace-nowrap text-slate-500">B3: BWL Pflicht</td>
                  <td class="p-3 text-center">9</td>
                  <td class="p-3 text-center"><span class="tag-badge bg-slate-200 dark:bg-slate-700 text-slate-800 dark:text-slate-200 font-semibold">3,3</span></td>
                  <td class="p-3">Strategische Analyse (SWOT, Porter Five Forces), Organisationsstrukturen, Aufbau- und Ablauforganisation.</td>
                </tr>
                <tr>
                  <td class="p-3 font-semibold text-white">Marketing Management</td>
                  <td class="p-3 whitespace-nowrap text-slate-500">Bereich C: Pflicht</td>
                  <td class="p-3 text-center">6</td>
                  <td class="p-3 text-center"><span class="tag-badge bg-slate-200 dark:bg-slate-700 text-slate-800 dark:text-slate-200 font-semibold">3,3</span></td>
                  <td class="p-3">Marketing-Mix (4P), Marktforschung, Kundenbindung, Produktpositionierung und Markenführung.</td>
                </tr>
                <tr>
                  <td class="p-3 font-semibold text-white">Management von Dienstleistungsunternehmen</td>
                  <td class="p-3 whitespace-nowrap text-slate-500">Bereich C: Pflicht</td>
                  <td class="p-3 text-center">6</td>
                  <td class="p-3 text-center"><span class="tag-badge bg-slate-200 dark:bg-slate-700 text-slate-800 dark:text-slate-200 font-semibold">4,0</span></td>
                  <td class="p-3">Dienstleistungsqualität (SERVQUAL), Kapazitätssteuerung, Customer Journey und Dienstleistungsproduktivität.</td>
                </tr>

                <!-- BEREICH A & SQ: ALLGEMEINE LEISTUNGEN & MATHEMATIK -->
                <tr class="bg-slate-100/80 dark:bg-slate-800/80 font-bold text-white">
                  <td colspan="5" class="p-2.5 uppercase tracking-wider text-[11px] text-slate-700 dark:text-slate-400">
                    📐 Bereich A & SQ: Mathematisch-Methodische Grundlagen (30 ECTS)
                  </td>
                </tr>
                <tr class="bg-blue-50/20 dark:bg-blue-950/10">
                  <td class="p-3 font-semibold text-white">Seminar interdisziplinäre Themen</td>
                  <td class="p-3 whitespace-nowrap text-slate-500">Bereich A</td>
                  <td class="p-3 text-center font-bold">6</td>
                  <td class="p-3 text-center"><span class="tag-badge bg-[#bf262e] text-white font-bold">2,3</span></td>
                  <td class="p-3">Interdisziplinäres wissenschaftliches Arbeiten, Literaturrecherche, Argumentation und Präsentation.</td>
                </tr>
                <tr>
                  <td class="p-3 font-semibold text-white">Statistik II (Induktive Statistik)</td>
                  <td class="p-3 whitespace-nowrap text-slate-500">Bereich A</td>
                  <td class="p-3 text-center">6</td>
                  <td class="p-3 text-center"><span class="tag-badge bg-slate-200 dark:bg-slate-700 text-slate-800 dark:text-slate-200 font-semibold">2,7</span></td>
                  <td class="p-3">Wahrscheinlichkeitstheorie, Hypothesentests, Konfidenzintervalle, lineare Regression und multivariate Analyseverfahren.</td>
                </tr>
                <tr>
                  <td class="p-3 font-semibold text-white">Statistik I (Deskriptive Statistik)</td>
                  <td class="p-3 whitespace-nowrap text-slate-500">Bereich A</td>
                  <td class="p-3 text-center">6</td>
                  <td class="p-3 text-center"><span class="tag-badge bg-slate-200 dark:bg-slate-700 text-slate-800 dark:text-slate-200 font-semibold">4,0</span></td>
                  <td class="p-3">Empirische Verteilungen, Lage- und Streuungsmaße, Korrelationsrechnung und Zeitreihenanalyse.</td>
                </tr>
                <tr>
                  <td class="p-3 font-semibold text-white">Mathematik für Wirtschaftswissenschaftler</td>
                  <td class="p-3 whitespace-nowrap text-slate-500">Bereich A</td>
                  <td class="p-3 text-center">9</td>
                  <td class="p-3 text-center"><span class="tag-badge bg-slate-200 dark:bg-slate-700 text-slate-800 dark:text-slate-200 font-semibold">4,0</span></td>
                  <td class="p-3">Lineare Algebra, Matrizenrechnung, Differentialrechnung mehrerer Variablen und Optimierung unter Nebenbedingungen.</td>
                </tr>
                <tr>
                  <td class="p-3 font-semibold text-white">Schreibwerkstatt: Vom studentischen zum beruflichen Schreiben</td>
                  <td class="p-3 whitespace-nowrap text-slate-500">Schlüsselqualifikationen</td>
                  <td class="p-3 text-center">3</td>
                  <td class="p-3 text-center"><span class="tag-badge bg-emerald-100 text-emerald-800 dark:bg-emerald-900/60 dark:text-emerald-300 font-bold">Bestanden</span></td>
                  <td class="p-3">Strukturierte Berichtserstellung, Business Communication, Zielgruppenansprache und professionelles Storytelling.</td>
                </tr>

              </tbody>
            </table>
          </div>
        </div>

        <!-- ================= SECTION: 12 EMPIRICAL INTERVIEWS & THEORETICAL CONSTRUCTS ================= -->
        <div v-show="degreeTab === 'all' || degreeTab === 'master'" class="bg-[#141414] p-6 rounded-2xl border border-white/10 shadow-sm space-y-4">
          <div class="flex items-center justify-between">
            <h3 class="text-base font-bold text-white flex items-center space-x-2">
              <span>🎙️</span>
              <span>Die 12 empirischen Experteninterviews deiner Masterarbeit (IP1–IP12)</span>
            </h3>
            <span class="tag-badge bg-white/10 text-[#c4bebe]">Mayring Inhaltsanalyse & Codebuch</span>
          </div>
          <p class="text-xs text-slate-500">
            Alle Transkripte und das Auswertungs-Codebuch liegen lokal im Workspace unter <code>Studium_Dokumente/Interviews_Masterarbeit</code>:
          </p>

          <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-3 text-xs">
            <div class="p-3.5 bg-white/5 rounded-xl border border-white/10 space-y-1.5">
              <div class="flex justify-between items-center">
                <span class="font-bold text-white">Roland Nowak</span>
                <span class="text-[9px] bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300 px-1.5 py-0.5 rounded font-bold">IP1</span>
              </div>
              <div class="text-[11px] text-[#f87171] font-semibold">Gesamtprojektleiter SAP4SSB</div>
              <p class="text-[#c4bebe] text-[10px] leading-relaxed">
                Fokus: Multiprojektsteuerung (TP1–TP5), ERP-Plattform-Governance, C-Level Alignment und formelle Betriebsvereinbarung mit BR.
              </p>
              <div class="text-[9px] text-slate-400 font-mono">Interview_Roland_Nowak_Gesamt_PL.docx</div>
            </div>

            <div class="p-3.5 bg-white/5 rounded-xl border border-white/10 space-y-1.5">
              <div class="flex justify-between items-center">
                <span class="font-bold text-white">Thomas Wimpff</span>
                <span class="text-[9px] bg-emerald-100 text-emerald-800 dark:bg-emerald-900 dark:text-emerald-300 px-1.5 py-0.5 rounded font-bold">IP2</span>
              </div>
              <div class="text-[11px] text-emerald-600 dark:text-emerald-400 font-semibold">Teilprojektleiter TP2 (Finance & Controlling)</div>
              <p class="text-[#c4bebe] text-[10px] leading-relaxed">
                Fokus: Trennungsrechnung (Kaufmännisch/Steuerlich), Universelles Journal (ACDOCA), Ablösung von Innenaufträgen durch PSP-Elemente und Übernahmekonto 0,00 €.
              </p>
              <div class="text-[9px] text-slate-400 font-mono">Interview_Thomas_Wimpff_TP2_Leitung.docx</div>
            </div>

            <div class="p-3.5 bg-white/5 rounded-xl border border-white/10 space-y-1.5">
              <div class="flex justify-between items-center">
                <span class="font-bold text-white">Armin Heinrich</span>
                <span class="text-[9px] bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-300 px-1.5 py-0.5 rounded font-bold">IP3</span>
              </div>
              <div class="text-[11px] text-purple-600 dark:text-purple-400 font-semibold">Enterprise Basisarchitekt SSB AG</div>
              <p class="text-[#c4bebe] text-[10px] leading-relaxed">
                Fokus: BTP-Zielarchitektur, SSO-Integration mit Microsoft Entra ID, ES4 Mandantenlandschaft und Schnittstellenabsicherung.
              </p>
              <div class="text-[9px] text-slate-400 font-mono">Interview_Armin_Heinrich_Basis_Architektur.docx</div>
            </div>

            <div class="p-3.5 bg-white/5 rounded-xl border border-white/10 space-y-1.5">
              <div class="flex justify-between items-center">
                <span class="font-bold text-white">Henning Gerdes</span>
                <span class="text-[9px] bg-amber-100 text-amber-800 dark:bg-amber-900 dark:text-amber-300 px-1.5 py-0.5 rounded font-bold">IP4</span>
              </div>
              <div class="text-[11px] text-amber-600 dark:text-amber-400 font-semibold">Lead Architect Axians ES4</div>
              <p class="text-[#c4bebe] text-[10px] leading-relaxed">
                Fokus: Bereitstellung der Private-Cloud-Infrastruktur, Adobe Document Services (ADS) Formulare und Transportkonsolidierung.
              </p>
              <div class="text-[9px] text-slate-400 font-mono">Interview_Henning_Gerdes_Axians_Lead.docx</div>
            </div>
          </div>
        </div>

      </div>
"""
