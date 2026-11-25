# -*- coding: utf-8 -*-

def get_master_tab():
    return """
      <!-- ================= TAB 4: MASTER OF SCIENCE (120 ECTS | NOTE 1,6) ================= -->
      <div v-show="activeTab === 'master'" class="space-y-6">

        <!-- Master Overview & Thesis Highlight -->
        <div class="bg-[#141414] p-6 rounded-2xl border border-white/10 space-y-5">
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
            <div>
              <div class="flex flex-wrap items-center gap-2 mb-1.5">
                <span class="status-pill status-pill-green">Gesamtnote 1,6 („gut“)</span>
                <span class="status-pill status-pill-green">Masterarbeit: Note 1,0 („sehr gut“)</span>
                <span class="status-pill status-pill-purple">120 ECTS • 100 % abgeschlossen</span>
              </div>
              <h2 class="text-xl sm:text-2xl font-extrabold text-white tracking-tight">
                🎓 M.Sc. Wirtschaftsinformatik (Universität Stuttgart)
              </h2>
              <p class="text-xs sm:text-sm text-[#8f8888] mt-1">
                Amtliches Masterzeugnis vom 17.09.2026 • Schwerpunkt: ERP-Transformation, Plattformisierung, Software-Architektur &amp; Applied AI.
              </p>
            </div>
          </div>

          <!-- Highlight Box: Master Thesis 1,0 -->
          <div class="info-callout p-4 space-y-2 text-xs">
            <div class="flex flex-wrap items-center justify-between gap-2">
              <span class="font-bold text-sm text-white">⭐ Masterarbeit (Note 1,0 | 30 ECTS | Lehrstuhl Prof. Dr. Georg Herzwurm)</span>
              <span class="status-pill status-pill-green">126 Seiten • 12 Experteninterviews • Mayring</span>
            </div>
            <p class="text-white font-semibold">
              „Kritische Erfolgsfaktoren in der Transformation großer ERP-Systeme: Eine Untersuchung am Beispiel der Plattformisierung von SAP S/4HANA“
            </p>
            <p class="text-[#c4bebe] leading-relaxed">
              Empirische Untersuchung im Großprojekt SAP4SSB anhand von 12 leitfadengestützten Experteninterviews (Gesamtprojektleitung, Teilprojektleiter, Lead-Architekten), ausgewertet mittels strukturierender qualitativer Inhaltsanalyse nach Mayring. Kernfokus: Plattform-Governance, Boundary Resources, bimodale IT-Entkopplung, Absorptive Capacity &amp; Change Management.
            </p>
          </div>

          <!-- Key Applied Master Projects (3 Compact Cards) -->
          <div class="grid grid-cols-1 md:grid-cols-3 gap-3 text-xs">
            <div class="p-4 rounded-xl bg-white/5 border border-white/10 space-y-1.5">
              <div class="flex items-center justify-between">
                <span class="font-bold text-white">Automatisierte CSRD-Abfallbilanz</span>
                <span class="status-pill status-pill-green">1,0</span>
              </div>
              <p class="text-[#c4bebe] text-[11px] leading-relaxed">Fallstudie J. Schmalz GmbH: BPMN-Prozessanalyse und PowerShell-Datenstrecke für automatisierte, fehlerfreie Nachhaltigkeitsberichte.</p>
            </div>
            <div class="p-4 rounded-xl bg-white/5 border border-white/10 space-y-1.5">
              <div class="flex items-center justify-between">
                <span class="font-bold text-white">Smart Service Blueprinting (FPWI)</span>
                <span class="status-pill status-pill-blue">1,3</span>
              </div>
              <p class="text-[#c4bebe] text-[11px] leading-relaxed">Design Science Research (DSRM) Framework für IoT-/CPS-Ökosysteme, empirisch evaluiert mit Usability-SUS-Score 85/100 (Excellent).</p>
            </div>
            <div class="p-4 rounded-xl bg-white/5 border border-white/10 space-y-1.5">
              <div class="flex items-center justify-between">
                <span class="font-bold text-white">PatentRadar SaaS/RPA-Konzept</span>
                <span class="status-pill status-pill-purple">2,0</span>
              </div>
              <p class="text-[#c4bebe] text-[11px] leading-relaxed">Hybrides SaaS- &amp; Beratungs-Geschäftsmodell für die Verpackungsindustrie (Klingele/ISG) inkl. KI-Patent-Volltextsuche &amp; BPMN-RPA.</p>
            </div>
          </div>
        </div>

        <!-- Complete Table: All 16 Master Modules (120 ECTS) -->
        <div class="bg-[#141414] p-6 rounded-2xl border border-white/10 space-y-4">
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
            <div>
              <h3 class="text-base font-bold text-white">
                Alle 16 Prüfungsleistungen im Masterstudium (120 ECTS | Gesamtnote 1,6)
              </h3>
              <p class="text-xs text-[#8f8888]">Vollständiger Leistungsnachweis gemäß amtlichem Masterzeugnis der Universität Stuttgart.</p>
            </div>
            <span class="status-pill status-pill-green">100 % Verifiziert</span>
          </div>

          <div class="overflow-x-auto">
            <table class="w-full text-left text-xs border border-white/10 rounded-xl overflow-hidden">
              <thead class="bg-white/10 text-white font-bold">
                <tr>
                  <th class="p-3">Katalog / Modulbezeichnung</th>
                  <th class="p-3 whitespace-nowrap">Bereich</th>
                  <th class="p-3 text-center">ECTS</th>
                  <th class="p-3 text-center">Note</th>
                  <th class="p-3">Akademischer Inhalt &amp; Praxisrelevanz</th>
                </tr>
              </thead>
              <tbody class="divide-y text-[#c4bebe]">
                <tr class="font-medium">
                  <td class="p-3 font-bold text-white">⭐ Masterarbeit: Kritische Erfolgsfaktoren in der Transformation großer ERP-Systeme (Plattformisierung von SAP S/4HANA)</td>
                  <td class="p-3 whitespace-nowrap text-[#8f8888]">Masterarbeit</td>
                  <td class="p-3 font-bold text-center">30</td>
                  <td class="p-3 text-center"><span class="status-pill status-pill-green">1,0</span></td>
                  <td class="p-3">126 Seiten, 12 leitfadengestützte Experteninterviews (SSB AG), qualitative Inhaltsanalyse nach Mayring, Plattform-Governance &amp; CSF.</td>
                </tr>
                <tr>
                  <td class="p-3 font-semibold text-white">Forschungsmethoden in der Wirtschaftsinformatik</td>
                  <td class="p-3 whitespace-nowrap text-[#8f8888]">Pflichtmodul</td>
                  <td class="p-3 text-center">6</td>
                  <td class="p-3 text-center"><span class="status-pill status-pill-blue">1,7</span></td>
                  <td class="p-3">Design Science Research Methodology (DSRM nach Peffers), qualitative Inhaltsanalyse nach Mayring, quantitative Hypothesenprüfung.</td>
                </tr>
                <tr>
                  <td class="p-3 font-semibold text-white">Forschungsprojekte in der Wirtschaftsinformatik (FPWI)</td>
                  <td class="p-3 whitespace-nowrap text-[#8f8888]">Katalog WI</td>
                  <td class="p-3 text-center font-bold">6</td>
                  <td class="p-3 text-center"><span class="status-pill status-pill-green">1,3</span></td>
                  <td class="p-3">Smart Service Blueprinting Framework für cyber-physische Systeme &amp; IoT. Empirischer SUS-Score 85/100 (Excellent).</td>
                </tr>
                <tr>
                  <td class="p-3 font-semibold text-white">AI4IoT – Artificial Intelligence for the Internet of Things</td>
                  <td class="p-3 whitespace-nowrap text-[#8f8888]">Katalog WI</td>
                  <td class="p-3 text-center">6</td>
                  <td class="p-3 text-center"><span class="status-pill status-pill-neutral">2,0</span></td>
                  <td class="p-3">Sensorik-Datenströme, Edge Computing, Predictive Maintenance und Time-Series Forecasting für verteilte Anlagen.</td>
                </tr>
                <tr>
                  <td class="p-3 font-semibold text-white">Management von IT-Unternehmen</td>
                  <td class="p-3 whitespace-nowrap text-[#8f8888]">Katalog WI</td>
                  <td class="p-3 text-center">6</td>
                  <td class="p-3 text-center"><span class="status-pill status-pill-neutral">3,0</span></td>
                  <td class="p-3">IT-Governance, COBIT, ITIL Service Lifecycle, Sourcing-Modelle, IT-Kostenrechnung und Budgetierung für Enterprise-IT.</td>
                </tr>
                <tr>
                  <td class="p-3 font-semibold text-white">Seminar Wirtschaftsinformatik 2</td>
                  <td class="p-3 whitespace-nowrap text-[#8f8888]">Seminar WI</td>
                  <td class="p-3 text-center">6</td>
                  <td class="p-3 text-center"><span class="status-pill status-pill-purple">1,7</span></td>
                  <td class="p-3">Systematische Literaturanalyse (PRISMA 2020) über KI-gestützte Mensch-Roboter-Kollaboration (Industrie 5.0).</td>
                </tr>
                <tr>
                  <td class="p-3 font-semibold text-white">Advanced Software Engineering (ASE)</td>
                  <td class="p-3 whitespace-nowrap text-[#8f8888]">Software Eng.</td>
                  <td class="p-3 text-center font-bold">6</td>
                  <td class="p-3 text-center"><span class="status-pill status-pill-blue">1,6</span></td>
                  <td class="p-3">Enterprise-Softwarearchitekturen, Domain-Driven Design (DDD), CI/CD-Pipelines, automatisiertes Testing &amp; Clean Code.</td>
                </tr>
                <tr>
                  <td class="p-3 font-semibold text-white">Software-Architektur</td>
                  <td class="p-3 whitespace-nowrap text-[#8f8888]">MINF Informatik</td>
                  <td class="p-3 text-center font-bold">6</td>
                  <td class="p-3 text-center"><span class="status-pill status-pill-blue">1,7</span></td>
                  <td class="p-3">Microservices, Event-Driven Architecture, SOA, API-Design (REST, gRPC, Event Mesh) und Entkopplungsstrategien.</td>
                </tr>
                <tr>
                  <td class="p-3 font-semibold text-white">Service Management and Cloud Computing, and Evaluation</td>
                  <td class="p-3 whitespace-nowrap text-[#8f8888]">MINF Informatik</td>
                  <td class="p-3 text-center">6</td>
                  <td class="p-3 text-center"><span class="status-pill status-pill-neutral">2,0</span></td>
                  <td class="p-3">AWS Well-Architected Framework, Serverless-Architekturen (DynamoDB, EventBridge, Step Functions) &amp; Cloud SLAs.</td>
                </tr>
                <tr>
                  <td class="p-3 font-semibold text-white">Datenbanken und Informationssysteme</td>
                  <td class="p-3 whitespace-nowrap text-[#8f8888]">MINF Informatik</td>
                  <td class="p-3 text-center">6</td>
                  <td class="p-3 text-center"><span class="status-pill status-pill-neutral">2,7</span></td>
                  <td class="p-3">Relationale Datenmodelle, SQL, ACID-Transaktionen, Indizierungsstrategien, NoSQL- und In-Memory-Konzepte.</td>
                </tr>
                <tr>
                  <td class="p-3 font-semibold text-white">Innovationsmanagement</td>
                  <td class="p-3 whitespace-nowrap text-[#8f8888]">Katalog BWL</td>
                  <td class="p-3 text-center">6</td>
                  <td class="p-3 text-center"><span class="status-pill status-pill-blue">1,7</span></td>
                  <td class="p-3">Disruptive Innovationen, Plattform-Ökosysteme, Technologie-Lebenszyklen und Go-to-Market-Planung.</td>
                </tr>
                <tr>
                  <td class="p-3 font-semibold text-white">Theorie und Empirie internationaler Unternehmenstätigkeit (INUT)</td>
                  <td class="p-3 whitespace-nowrap text-[#8f8888]">Katalog BWL</td>
                  <td class="p-3 text-center">6</td>
                  <td class="p-3 text-center"><span class="status-pill status-pill-blue">1,7</span></td>
                  <td class="p-3">Globale Wertschöpfungsketten, multinationale Konzerne, internationales IT-Sourcing &amp; Standortentscheidungen.</td>
                </tr>
                <tr>
                  <td class="p-3 font-semibold text-white">Digitale Nachhaltigkeit (Green IT &amp; CSRD)</td>
                  <td class="p-3 whitespace-nowrap text-[#8f8888]">Ergänzung WI</td>
                  <td class="p-3 text-center font-bold">6</td>
                  <td class="p-3 text-center"><span class="status-pill status-pill-green">1,0</span></td>
                  <td class="p-3">Praxis-Fallstudie J. Schmalz GmbH: BPMN-Prozessmodellierung &amp; PowerShell-Automatisierung für CSRD-Abfallbilanz.</td>
                </tr>
                <tr>
                  <td class="p-3 font-semibold text-white">Applied AI and Upcoming Technologies in Industries</td>
                  <td class="p-3 whitespace-nowrap text-[#8f8888]">Ergänzung WI</td>
                  <td class="p-3 text-center">6</td>
                  <td class="p-3 text-center"><span class="status-pill status-pill-blue">1,7</span></td>
                  <td class="p-3">Machine Learning im industriellen Einsatz, NLP, LLM-Architekturen und Integration intelligenter Agenten in ERP-Prozesse.</td>
                </tr>
                <tr>
                  <td class="p-3 font-semibold text-white">Innovationsmethoden für software- und datenintensive Geschäftsmodelle (ISG)</td>
                  <td class="p-3 whitespace-nowrap text-[#8f8888]">Ergänzung WI</td>
                  <td class="p-3 text-center">6</td>
                  <td class="p-3 text-center"><span class="status-pill status-pill-neutral">2,0</span></td>
                  <td class="p-3">Data-driven Business Models, Plattformökonomie &amp; Venture „PatentRadar“ für Klingele Paper &amp; Packaging.</td>
                </tr>
                <tr>
                  <td class="p-3 font-semibold text-white">Service Operations Management (SOM)</td>
                  <td class="p-3 whitespace-nowrap text-[#8f8888]">Ergänzung BWL</td>
                  <td class="p-3 text-center">6</td>
                  <td class="p-3 text-center"><span class="status-pill status-pill-neutral">3,0</span></td>
                  <td class="p-3">Operations Management, Warteschlangentheorie, Kapazitäts- und Durchsatzoptimierung im Dienstleistungssektor.</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

      </div>
"""
