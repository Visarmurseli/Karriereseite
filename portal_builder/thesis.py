# -*- coding: utf-8 -*-

def get_thesis():
    return """
      <!-- ================= TAB 7: MASTERARBEIT, FORSCHUNG & ACADEMIC KNOWLEDGE HUB ================= -->
      <div v-show="activeTab === 'thesis'" class="space-y-6">
        
        <!-- Header Hero -->
        <div class="bg-white dark:bg-slate-900 p-6 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm space-y-4">
          <div class="flex flex-col md:flex-row md:items-center justify-between gap-3">
            <div>
              <span class="text-xs font-bold text-blue-600 dark:text-blue-400 uppercase tracking-wider">
                Universität Stuttgart | Fakultät für Wirtschafts- und Sozialwissenschaften
              </span>
              <h3 class="text-xl font-extrabold text-slate-900 dark:text-white mt-1">
                Akademischer Knowledge Hub: Forschung, Veröffentlichungen & Master-Curriculum
              </h3>
              <p class="text-xs text-slate-500 dark:text-slate-400 mt-1">
                Visar Murseli, M.Sc. Wirtschaftsinformatik (Amtliches Zeugnis: Gesamtnote 1,6 „gut“ | Masterarbeit 1,0 „sehr gut“ | 120 ECTS)
              </p>
            </div>
            <div class="flex flex-wrap items-center gap-2">
              <span class="tag-badge bg-emerald-600 text-white font-bold text-xs whitespace-nowrap">Masterarbeit: Note 1,0 (30 ECTS)</span>
              <span class="tag-badge bg-blue-600 text-white font-bold text-xs whitespace-nowrap">M.Sc. Gesamtnote: 1,6 (120 ECTS)</span>
              <span class="tag-badge bg-purple-100 text-purple-800 dark:bg-purple-900/60 dark:text-purple-300 font-bold text-xs whitespace-nowrap">B.Sc. Note: 2,3 (180 ECTS)</span>
            </div>
          </div>

          <!-- Official Master Degree Certificate Callout -->
          <div class="p-4 rounded-xl bg-gradient-to-r from-emerald-50 via-teal-50 to-blue-50 dark:from-emerald-950/40 dark:via-teal-950/30 dark:to-blue-950/30 border border-emerald-300 dark:border-emerald-700 text-xs text-slate-700 dark:text-slate-300 space-y-2.5">
            <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
              <div class="flex items-center space-x-2 font-bold text-emerald-900 dark:text-emerald-300 text-sm">
                <span>📜</span>
                <span>Offizielles Zeugnis über die Masterprüfung (Universität Stuttgart)</span>
              </div>
              <span class="text-[11px] font-semibold bg-emerald-100 dark:bg-emerald-900/80 text-emerald-800 dark:text-emerald-200 px-2.5 py-1 rounded-full border border-emerald-300 dark:border-emerald-700">
                Stuttgart, den 17. September 2026 | Prof. Dr. Christian Becker (Prüfungsausschussvorsitzender)
              </span>
            </div>
            <p class="text-xs leading-relaxed text-slate-600 dark:text-slate-300">
              Mit Beschluss des Prüfungsausschusses der Universität Stuttgart wurde Visar Murseli nach Erbringung aller 120 ECTS Leistungspunkte der akademische Grad <strong>Master of Science (M.Sc.) Wirtschaftsinformatik</strong> mit dem Gesamturteil <strong>„gut“ (1,6)</strong> verliehen. Die Masterarbeit am Lehrstuhl von Prof. Dr. Georg Herzwurm wurde mit der <strong>Spitzennote 1,0 (sehr gut)</strong> bewertet.
            </p>
            <div class="pt-2 flex flex-wrap items-center justify-between gap-2 border-t border-emerald-200 dark:border-emerald-800 text-[11px]">
              <span class="text-slate-500 dark:text-slate-400">
                Verifizierte Originaldatei: <code>Studium_Dokumente/Masterzeugnis_Murseli_Visar.pdf</code> (3 Seiten, 120 ECTS)
              </span>
              <a href="Studium_Dokumente/Masterzeugnis_Murseli_Visar.pdf" target="_blank" class="inline-flex items-center space-x-1.5 px-3 py-1.5 rounded-lg bg-emerald-600 hover:bg-emerald-700 text-white font-bold transition shadow-sm">
                <span>📄</span>
                <span>Offizielles Masterzeugnis (PDF) öffnen</span>
              </a>
            </div>
          </div>

          <!-- Academic Impact Explanation -->
          <div class="p-4 rounded-xl bg-gradient-to-r from-blue-50 to-indigo-50 dark:from-blue-950/40 dark:to-indigo-950/30 border border-blue-200 dark:border-blue-800 text-xs text-slate-700 dark:text-slate-300 leading-relaxed space-y-2">
            <div>
              <strong>Dein wissenschaftlicher USP im Bewerbungsgespräch:</strong>
              Du bist kein reiner Theoretiker und kein reiner Konfigurations-Klicker. Dein 6-jähriges Studium an der Exzellenzuniversität Stuttgart zeichnet sich durch einen stringenten <strong>Roten Faden</strong> aus: 
              <em>Von Software-Ökosystemen und Low-Code Boundary Resources im Bachelor über Software-Architektur (1,7), Advanced Software Engineering (1,6), Cloud Computing (2,0) und Smart Services bis hin zur empirisch fundierten ERP-Transformation, Plattformisierung und Plattform-Governance im Master (Note 1,0).</em>
            </div>
            <div class="text-[11px] text-slate-600 dark:text-slate-400">
              Alle hier dokumentierten Arbeiten sind durch amtliche Notenbescheide, Original-PDFs und empirische Transkripte im Ordner <code>Studium_Dokumente</code> lokal im System verifiziert.
            </div>
          </div>
        </div>

        <!-- Die 6 Meilensteine deiner wissenschaftlichen Forschung -->
        <div class="bg-white dark:bg-slate-900 p-6 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm space-y-4">
          <div class="flex items-center justify-between">
            <h3 class="text-base font-bold text-slate-900 dark:text-white flex items-center space-x-2">
              <span>📚</span>
              <span>Die 6 Meilensteine & Industrieprojekte deiner akademischen Forschung (Originalarbeiten)</span>
            </h3>
            <span class="tag-badge bg-blue-100 text-blue-800 dark:bg-blue-900/50 dark:text-blue-300">Empirie & Design Science</span>
          </div>

          <div class="grid grid-cols-1 lg:grid-cols-2 gap-4 text-xs">
            
            <!-- Paper 1: Masterarbeit (1,0) -->
            <div class="p-5 rounded-xl border-2 border-emerald-500 bg-emerald-50/20 dark:bg-emerald-950/20 space-y-3 shadow-sm flex flex-col justify-between">
              <div class="space-y-2">
                <div class="flex justify-between items-start gap-2">
                  <span class="text-[10px] font-extrabold uppercase tracking-wider text-emerald-700 dark:text-emerald-400">
                    Masterarbeit | Lehrstuhl Prof. Dr. Georg Herzwurm (30 ECTS)
                  </span>
                  <span class="tag-badge bg-emerald-600 text-white font-extrabold text-[11px]">Note: 1,0 (Sehr Gut)</span>
                </div>
                <h4 class="font-bold text-slate-900 dark:text-white text-sm leading-snug">
                  „Kritische Erfolgsfaktoren in der Transformation großer ERP-Systeme: Eine Untersuchung am Beispiel der Plattformisierung von SAP S/4HANA“
                </h4>
                <div class="text-slate-600 dark:text-slate-300 text-[11px] leading-relaxed space-y-1.5">
                  <p>
                    <strong>Wissenschaftliche Fragestellung:</strong> Wie verändert die Plattformisierung von ERP-Systemen (Schnittstellen zwischen S/4HANA Core und Cloud-Erweiterungen wie SAP BTP) die traditionellen Kritischen Erfolgsfaktoren (CSF)?
                  </p>
                  <p>
                    <strong>Methodik & Empirie:</strong> 12 leitfadengestützte Experteninterviews im Großprojekt SAP4SSB (Gesamtprojektleiter Roland Nowak, Teilprojektleiter Thomas Wimpff, Enterprise Architekten Axians & Nagarro). Qualitative Inhaltsanalyse nach Mayring mit dediziertem Kategoriensystem.
                  </p>
                  <p>
                    <strong>Zentrales Artefakt:</strong> Phase-based Platform Excellence Framework (4 Phasen × 4 Dimensionen: Organisation, Technik, Mensch, PMO).
                  </p>
                </div>
              </div>
              <div class="pt-3 border-t border-emerald-200 dark:border-emerald-800/60 flex items-center justify-between">
                <span class="text-[10px] text-slate-500">126 Seiten | 12 Transkripte | Codebuch</span>
                <span class="text-[11px] font-bold text-emerald-700 dark:text-emerald-400">PDF: Masterarbeit_Visar_Murseli.pdf</span>
              </div>
            </div>

            <!-- Paper 2: FPWI Forschungsprojekt (1,3) -->
            <div class="p-5 rounded-xl border-2 border-blue-500 bg-blue-50/20 dark:bg-blue-950/20 space-y-3 shadow-sm flex flex-col justify-between">
              <div class="space-y-2">
                <div class="flex justify-between items-start gap-2">
                  <span class="text-[10px] font-extrabold uppercase tracking-wider text-blue-700 dark:text-blue-400">
                    Forschungsprojekt Wirtschaftsinformatik (FPWI) | D. Anders, V. Murseli, U.E. Tumar (6 ECTS)
                  </span>
                  <span class="tag-badge bg-blue-600 text-white font-extrabold text-[11px]">Note: 1,3 (Sehr Gut)</span>
                </div>
                <h4 class="font-bold text-slate-900 dark:text-white text-sm leading-snug">
                  „Integration physischer und digitaler Welten: Ein Framework für Smart Service Blueprinting“
                </h4>
                <div class="text-slate-600 dark:text-slate-300 text-[11px] leading-relaxed space-y-1.5">
                  <p>
                    <strong>Wissenschaftliche Fragestellung:</strong> Klassisches Service Blueprinting (Bitner et al., 2008) versagt bei vernetzten Smart Services und cyber-physischen Systemen (CPS). Wie muss ein Modellierungsframework gestaltet sein, um Omnichannel-Interaktionen, IoT-Sensoren und automatisierte Entscheidungsknoten abzubilden?
                  </p>
                  <p>
                    <strong>Methodik:</strong> Design Science Research Methodology (DSRM nach Peffers et al., 2007). Konzeptionelle Iterationen, Artefakterstellung und empirische Evaluation.
                  </p>
                  <p>
                    <strong>Praxis-Use-Cases:</strong> Connected Cars (Predictive Maintenance & Smart Charging) sowie Smart Home (Smarte Rolladensteuerung basierend auf Sonneneinstrahlungsdaten und Wetterprognosen).
                  </p>
                  <p>
                    <strong>Evaluation & Usability:</strong> Thinking-Aloud Usability-Tests mit anschließender System Usability Scale (SUS) Messung. <strong>Ergebnis: Überragender SUS-Score von 85 / 100 Punkten („Grade A / Excellent“)!</strong>
                  </p>
                </div>
              </div>
              <div class="pt-3 border-t border-blue-200 dark:border-blue-800/60 flex items-center justify-between">
                <span class="text-[10px] text-slate-500">DSRM Framework | SUS-Score 85/100</span>
                <span class="text-[11px] font-bold text-blue-700 dark:text-blue-400">PDF: FPWI_Forschungsprojekt_Paper.pdf</span>
              </div>
            </div>

            <!-- Paper 3: Seminararbeit (SLR nach PRISMA 2020) -->
            <div class="p-5 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/40 space-y-3 flex flex-col justify-between">
              <div class="space-y-2">
                <div class="flex justify-between items-start gap-2">
                  <span class="text-[10px] font-extrabold uppercase tracking-wider text-purple-700 dark:text-purple-400">
                    Seminar Wirtschaftsinformatik 2 | Visar Murseli (6 ECTS)
                  </span>
                  <span class="tag-badge bg-purple-600 text-white font-extrabold text-[11px]">Note: 1,7 (Gut)</span>
                </div>
                <h4 class="font-bold text-slate-900 dark:text-white text-sm leading-snug">
                  „Die Transformation menschlicher Arbeitsrollen durch KI-gestützte Mensch-Roboter-Kollaboration in der Produktion“
                </h4>
                <div class="text-slate-600 dark:text-slate-300 text-[11px] leading-relaxed space-y-1.5">
                  <p>
                    <strong>Wissenschaftliche Fragestellung:</strong> Wie verändern kognitive Cobots und KI-Systeme die menschliche Rolle im Übergang von Industrie 4.0 (reine Automatisierung) zu <strong>Industrie 5.0 (Human-Centricity)</strong>?
                  </p>
                  <p>
                    <strong>Methodik:</strong> Strenge Systematische Literaturanalyse (SLR) nach dem <strong>PRISMA 2020 Protokoll</strong>. Systematische Recherche über 5 wissenschaftliche Datenbanken (ACM Digital Library, AIS eLibrary, EBSCOhost, IEEE Xplore, Web of Science). 
                  </p>
                  <p>
                    <strong>Recherche-Trichter:</strong> 570 gefundene Datensätze → Deduplizierung → Title/Abstract-Screening → Volltextprüfung → <strong>26 identifizierte und synthesefähige Kernstudien</strong>.
                  </p>
                  <p>
                    <strong>Kernergebnisse:</strong> Analyse von Learning from Demonstration (LfD), Messung kognitiver Ermüdung über Heart Rate Variability (HRV), Status Threat (Angst vor Kontrollverlust) und die Rolle der Metakognition (Human-in-the-Loop).
                  </p>
                </div>
              </div>
              <div class="pt-3 border-t border-slate-200 dark:border-slate-700 flex items-center justify-between">
                <span class="text-[10px] text-slate-500">PRISMA 2020 | 570 screened | 26 Studien</span>
                <span class="text-[11px] font-bold text-purple-700 dark:text-purple-400">PDF: Seminararbeit_Murseli.pdf</span>
              </div>
            </div>

            <!-- Paper 4: Bachelorarbeit (1,7) -->
            <div class="p-5 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/40 space-y-3 flex flex-col justify-between">
              <div class="space-y-2">
                <div class="flex justify-between items-start gap-2">
                  <span class="text-[10px] font-extrabold uppercase tracking-wider text-slate-700 dark:text-slate-400">
                    Bachelorarbeit (B.Sc. WI) | Lehrstuhl Prof. Dr. Georg Herzwurm (12 ECTS)
                  </span>
                  <span class="tag-badge bg-blue-100 text-blue-800 dark:bg-blue-900/60 dark:text-blue-300 font-extrabold text-[11px]">Note: 1,7 (Gut)</span>
                </div>
                <h4 class="font-bold text-slate-900 dark:text-white text-sm leading-snug">
                  „Die Bedeutung von Boundary Resources in Low-Code Entwicklungsplattformen: Eine qualitative Untersuchung am Beispiel von OutSystems und Mendix“
                </h4>
                <div class="text-slate-600 dark:text-slate-300 text-[11px] leading-relaxed space-y-1.5">
                  <p>
                    <strong>Wissenschaftliche Fragestellung:</strong> Welche Grenzressourcen (Boundary Resources) stellen Low-Code-Plattformbetreiber bereit, um Entwickler an ihre Plattform zu binden und Ökosystem-Wachstum zu steuern?
                  </p>
                  <p>
                    <strong>Theoretische Fundierung:</strong> Boundary Resource Theory (Ghazawneh & Henfridsson, 2013).
                  </p>
                  <p>
                    <strong>Ergebnis & Taxonomie:</strong> Identifikation und Klassifizierung von 14 aggregierten Boundary-Resource-Gruppen aufgeteilt in:
                    <br>• Application Boundary Resources (ABR: APIs, REST Services, Cloud Connectors)
                    <br>• Development Boundary Resources (DBR: Visual Modeler, AI-Assistants, CI/CD Pipelines)
                    <br>• Social Boundary Resources (SBR: Community Foren, Marktplätze wie OutSystems Forge & Mendix Marketplace).
                  </p>
                  <p>
                    <strong>Strategischer Transfer:</strong> Bereits 2023 das Fundament gelegt für Schnittstellen-Governance – direkt transferiert auf die SAP BTP im Master!
                  </p>
                </div>
              </div>
              <div class="pt-3 border-t border-slate-200 dark:border-slate-700 flex items-center justify-between">
                <span class="text-[10px] text-slate-500">14 Resource-Gruppen | OutSystems & Mendix</span>
                <span class="text-[11px] font-bold text-slate-700 dark:text-slate-300">PDF: Bachelorarbeit_Murseli.pdf</span>
              </div>
            </div>

            <!-- Paper 5: Fallstudie J. Schmalz GmbH (Digitale Nachhaltigkeit 1,0) -->
            <div class="p-5 rounded-xl border-2 border-emerald-500/80 bg-emerald-50/20 dark:bg-emerald-950/20 space-y-3 flex flex-col justify-between">
              <div class="space-y-2">
                <div class="flex justify-between items-start gap-2">
                  <span class="text-[10px] font-extrabold uppercase tracking-wider text-emerald-700 dark:text-emerald-400">
                    Praxis-Fallstudie | Dr. Dimitri Petrik (6 ECTS)
                  </span>
                  <span class="tag-badge bg-emerald-600 text-white font-extrabold text-[11px]">Note: 1,0 (Sehr Gut)</span>
                </div>
                <h4 class="font-bold text-slate-900 dark:text-white text-sm leading-snug">
                  „Nachhaltigkeit durch Automatisierung: Eine Fallstudie zur Optimierung der Abfallbilanz bei der Schmalz GmbH“
                </h4>
                <div class="text-slate-600 dark:text-slate-300 text-[11px] leading-relaxed space-y-1.5">
                  <p>
                    <strong>Praxispartner:</strong> J. Schmalz GmbH (Weltmarktführer für Vakuum-Automation).
                  </p>
                  <p>
                    <strong>Problemstellung:</strong> Manuelle, fehleranfällige Erfassung von Abfall- und Wertstoffbilanzen per Excel verhinderte präzises ESG-Reporting und verursachte hohe Personalkosten.
                  </p>
                  <p>
                    <strong>Lösungsansatz:</strong> Detaillierte BPMN-Modellierung des Ist- und Soll-Zustands, Konzeption einer automatisierten Datenintegrationsstrecke und Entwicklung eines funktionalen Softwareprototypen für automatisierte CSRD-Kennzahlen.
                  </p>
                  <p>
                    <strong>Beratungs-Transfer:</strong> Du beherrschst Prozessmodellierung (BPMN), Schnittstellenautomatisierung und ESG-Reporting im industriellen Mittelstand aus erster Hand!
                  </p>
                </div>
              </div>
              <div class="pt-3 border-t border-emerald-200 dark:border-emerald-800 flex items-center justify-between">
                <span class="text-[10px] text-slate-500">J. Schmalz GmbH | BPMN & ESG Prototyp</span>
                <span class="text-[11px] font-bold text-emerald-700 dark:text-emerald-400">DOCX: DigitaleNachhaltigkeit_Ausarbeitung_Schmalz.docx</span>
              </div>
            </div>

            <!-- Paper 6: Cloud Computing Kurzpaper (AWS Well-Architected) -->
            <div class="p-5 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/40 space-y-3 flex flex-col justify-between">
              <div class="space-y-2">
                <div class="flex justify-between items-start gap-2">
                  <span class="text-[10px] font-extrabold uppercase tracking-wider text-blue-700 dark:text-blue-400">
                    Wissenschaftliches Kurzpaper | Service Management & Cloud Computing (6 ECTS)
                  </span>
                  <span class="tag-badge bg-blue-600 text-white font-extrabold text-[11px]">Note: 2,0 (Gut) | 12 Seiten</span>
                </div>
                <h4 class="font-bold text-slate-900 dark:text-white text-sm leading-snug">
                  „Entwicklung einer Cloud-basierten Plattformarchitektur für einen wachsenden Onlineshop“
                </h4>
                <div class="text-slate-600 dark:text-slate-300 text-[11px] leading-relaxed space-y-1.5">
                  <p>
                    <strong>Architektur-Framework:</strong> AWS Well-Architected Framework (Operational Excellence, Security, Reliability, Performance Efficiency, Cost Optimization).
                  </p>
                  <p>
                    <strong>Komponenten:</strong> Entwurf einer Microservices- und Serverless-Architektur: React Frontend via AWS Amplify, DynamoDB & ElastiCache, Amazon RDS Multi-AZ, AWS IoT Core für Lagerbestands-Sensorik, AWS Step Functions Workflow-Orchestrierung, Amazon EventBridge für CRM & Event-Driven-Streaming, Amazon Kinesis & QuickSight für Real-Time Clickstream-Analytics.
                  </p>
                  <p>
                    <strong>DevOps & Governance:</strong> CI/CD-Pipelines mit AWS CodePipeline, CodeBuild und CodeDeploy.
                  </p>
                </div>
              </div>
              <div class="pt-3 border-t border-slate-200 dark:border-slate-700 flex items-center justify-between">
                <span class="text-[10px] text-slate-500">12 Seiten | AWS Microservices & Serverless</span>
                <span class="text-[11px] font-bold text-blue-700 dark:text-blue-400">PDF: CloudComputing_Kurzpaper_Murseli.pdf</span>
              </div>
            </div>

          </div>
        </div>

        <!-- Master-Curriculum & Leistungsübersicht (Alle 16 Module offiziell nach Zeugnis) -->
        <div class="bg-white dark:bg-slate-900 p-6 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm space-y-5">
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
            <div>
              <div class="flex items-center space-x-2">
                <span class="text-lg">🎓</span>
                <h3 class="text-base font-bold text-slate-900 dark:text-white">
                  Vollständiges Master-Curriculum: Alle 16 Prüfungsleistungen (120 ECTS)
                </h3>
              </div>
              <p class="text-xs text-slate-500 dark:text-slate-400 mt-0.5">
                Amtlich beglaubigt im Zeugnis über die Masterprüfung (Universität Stuttgart, PO 2020) | Gesamtnote: 1,6 „gut“
              </p>
            </div>
            <div class="flex items-center gap-2">
              <span class="tag-badge bg-emerald-100 text-emerald-800 dark:bg-emerald-900/60 dark:text-emerald-300 font-bold text-xs whitespace-nowrap">
                Masterarbeit: 1,0 (30 ECTS)
              </span>
              <span class="tag-badge bg-blue-100 text-blue-800 dark:bg-blue-900/60 dark:text-blue-300 font-bold text-xs whitespace-nowrap">
                Gesamtnote M.Sc.: 1,6
              </span>
            </div>
          </div>

          <!-- Academic Scorecard Grid -->
          <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs">
            <div class="p-3 bg-slate-50 dark:bg-slate-800/50 rounded-xl border border-slate-200 dark:border-slate-700">
              <div class="text-[11px] text-slate-500 font-medium">Gesamt-ECTS</div>
              <div class="text-lg font-bold text-slate-900 dark:text-white mt-0.5">120 ECTS</div>
              <div class="text-[10px] text-emerald-600 font-semibold">100% abgeschlossen</div>
            </div>
            <div class="p-3 bg-slate-50 dark:bg-slate-800/50 rounded-xl border border-slate-200 dark:border-slate-700">
              <div class="text-[11px] text-slate-500 font-medium">Masterarbeit (Herzwurm)</div>
              <div class="text-lg font-bold text-emerald-600 mt-0.5">1,0 (Sehr Gut)</div>
              <div class="text-[10px] text-slate-500">30 ECTS | 126 Seiten</div>
            </div>
            <div class="p-3 bg-slate-50 dark:bg-slate-800/50 rounded-xl border border-slate-200 dark:border-slate-700">
              <div class="text-[11px] text-slate-500 font-medium">Vertiefungsmodule</div>
              <div class="text-lg font-bold text-blue-600 mt-0.5">66 ECTS</div>
              <div class="text-[10px] text-slate-500">11 Module à 6 ECTS</div>
            </div>
            <div class="p-3 bg-slate-50 dark:bg-slate-800/50 rounded-xl border border-slate-200 dark:border-slate-700">
              <div class="text-[11px] text-slate-500 font-medium">Ergänzende Module</div>
              <div class="text-lg font-bold text-purple-600 mt-0.5">24 ECTS</div>
              <div class="text-[10px] text-slate-500">4 Module à 6 ECTS</div>
            </div>
          </div>

          <!-- Detailed Curriculum Table -->
          <div class="overflow-x-auto">
            <table class="w-full text-left text-xs border border-slate-200 dark:border-slate-700 rounded-xl overflow-hidden">
              <thead class="bg-slate-100 dark:bg-slate-800 text-slate-900 dark:text-white font-bold">
                <tr>
                  <th class="p-3 border-b dark:border-slate-700">Katalog / Modulbezeichnung</th>
                  <th class="p-3 border-b dark:border-slate-700 whitespace-nowrap">Bereich</th>
                  <th class="p-3 border-b dark:border-slate-700 text-center">ECTS</th>
                  <th class="p-3 border-b dark:border-slate-700 text-center">Note</th>
                  <th class="p-3 border-b dark:border-slate-700">Akademischer Inhalt & Relevanz für Vorstellungsgespräche</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-slate-200 dark:divide-slate-700 text-slate-600 dark:text-slate-300">
                
                <!-- SECTION 1: MASTERARBEIT -->
                <tr class="bg-slate-100/80 dark:bg-slate-800/80 font-bold text-slate-900 dark:text-white">
                  <td colspan="5" class="p-2.5 uppercase tracking-wider text-[11px] text-emerald-700 dark:text-emerald-400">
                    ⭐ Bereich 1: Masterarbeit (30 ECTS) – Höchste Auszeichnung
                  </td>
                </tr>
                <tr class="bg-emerald-50/40 dark:bg-emerald-950/20 font-medium">
                  <td class="p-3 font-bold text-slate-900 dark:text-white">
                    Kritische Erfolgsfaktoren in der Transformation großer ERP-Systeme: Eine Untersuchung am Beispiel der Plattformisierung von SAP S/4HANA
                  </td>
                  <td class="p-3 whitespace-nowrap text-slate-500">Masterarbeit</td>
                  <td class="p-3 font-bold text-center">30</td>
                  <td class="p-3 text-center"><span class="tag-badge bg-emerald-600 text-white font-bold">1,0</span></td>
                  <td class="p-3">Kritische Erfolgsfaktoren (CSF) und Plattformisierung großer ERP-Systeme, Plattform-Governance, 12 leitfadengestützte Experteninterviews im Großprojekt SSB AG. Qualitative Inhaltsanalyse nach Mayring. Höchste universitäre Auszeichnung (Note 1,0).</td>
                </tr>

                <!-- SECTION 2: VERTIEFUNGSMODULE (66 ECTS) -->
                <tr class="bg-slate-100/80 dark:bg-slate-800/80 font-bold text-slate-900 dark:text-white">
                  <td colspan="5" class="p-2.5 uppercase tracking-wider text-[11px] text-blue-700 dark:text-blue-400">
                    📘 Bereich 2: Vertiefungsmodule (66 ECTS)
                  </td>
                </tr>

                <!-- 1. Forschungsmethoden -->
                <tr>
                  <td class="p-3 font-semibold text-slate-900 dark:text-white">Forschungsmethoden in der Wirtschaftsinformatik</td>
                  <td class="p-3 whitespace-nowrap text-slate-500">Pflichtmodul</td>
                  <td class="p-3 text-center">6</td>
                  <td class="p-3 text-center"><span class="tag-badge bg-blue-100 text-blue-800 dark:bg-blue-900/60 dark:text-blue-300 font-bold">1,7</span></td>
                  <td class="p-3">Design Science Research Methodology (DSRM nach Peffers), qualitative Inhaltsanalyse nach Mayring, quantitative Hypothesenprüfung. Wissenschaftliches Fundament.</td>
                </tr>

                <!-- 2. Forschungsprojekte WI -->
                <tr class="bg-blue-50/20 dark:bg-blue-950/10">
                  <td class="p-3 font-semibold text-slate-900 dark:text-white">Forschungsprojekte in der Wirtschaftsinformatik (FPWI)</td>
                  <td class="p-3 whitespace-nowrap text-slate-500">Katalog Wirtschaftsinformatik</td>
                  <td class="p-3 text-center font-bold">6</td>
                  <td class="p-3 text-center"><span class="tag-badge bg-blue-600 text-white font-bold">1,3</span></td>
                  <td class="p-3">Smart Service Blueprinting Framework für cyber-physische Systeme & IoT. DSRM, Thinking-Aloud Tests, empirischer SUS-Score 85/100 (Grade A / Excellent).</td>
                </tr>

                <!-- 3. AI4IoT -->
                <tr>
                  <td class="p-3 font-semibold text-slate-900 dark:text-white">AI4IoT – Artificial Intelligence for the Internet of Things</td>
                  <td class="p-3 whitespace-nowrap text-slate-500">Katalog Wirtschaftsinformatik</td>
                  <td class="p-3 text-center">6</td>
                  <td class="p-3 text-center"><span class="tag-badge bg-slate-200 dark:bg-slate-700 text-slate-800 dark:text-slate-200 font-semibold">2,0</span></td>
                  <td class="p-3">Sensorik-Datenströme, Edge Computing, Predictive Maintenance im industriellen Maschinenbau, Time-Series Forecasting für verteilte Anlagen.</td>
                </tr>

                <!-- 4. Management von IT-Unternehmen -->
                <tr>
                  <td class="p-3 font-semibold text-slate-900 dark:text-white">Management von IT-Unternehmen</td>
                  <td class="p-3 whitespace-nowrap text-slate-500">Katalog Wirtschaftsinformatik</td>
                  <td class="p-3 text-center">6</td>
                  <td class="p-3 text-center"><span class="tag-badge bg-slate-200 dark:bg-slate-700 text-slate-800 dark:text-slate-200 font-semibold">3,0</span></td>
                  <td class="p-3">IT-Governance, COBIT, ITIL Service Lifecycle, Sourcing-Modelle, IT-Kostenrechnung und Budgetierung für Enterprise-IT.</td>
                </tr>

                <!-- 5. Seminar WI 2 -->
                <tr class="bg-purple-50/20 dark:bg-purple-950/10">
                  <td class="p-3 font-semibold text-slate-900 dark:text-white">Seminar Wirtschaftsinformatik 2</td>
                  <td class="p-3 whitespace-nowrap text-slate-500">Katalog Seminar WI</td>
                  <td class="p-3 text-center">6</td>
                  <td class="p-3 text-center"><span class="tag-badge bg-purple-600 text-white font-bold">1,7</span></td>
                  <td class="p-3">Systematische Literaturanalyse (SLR nach PRISMA 2020) über 5 Fachdatenbanken (570 gefundene Studien): KI-gestützte Mensch-Roboter-Kollaboration in der Produktion (Industrie 5.0).</td>
                </tr>

                <!-- 6. Advanced Software Engineering -->
                <tr class="bg-indigo-50/20 dark:bg-indigo-950/10">
                  <td class="p-3 font-semibold text-slate-900 dark:text-white">Advanced Software Engineering (ASE)</td>
                  <td class="p-3 whitespace-nowrap text-slate-500">Katalog Software Engineering</td>
                  <td class="p-3 text-center font-bold">6</td>
                  <td class="p-3 text-center"><span class="tag-badge bg-indigo-600 text-white font-bold">1,6</span></td>
                  <td class="p-3">Fortgeschrittene Software-Architekturen, Domain-Driven Design (DDD), CI/CD-Pipelines, automatisiertes Testing, Clean Code und Refactoring im Enterprise-Maßstab.</td>
                </tr>

                <!-- 7. Software-Architektur -->
                <tr class="bg-indigo-50/20 dark:bg-indigo-950/10">
                  <td class="p-3 font-semibold text-slate-900 dark:text-white">Software-Architektur</td>
                  <td class="p-3 whitespace-nowrap text-slate-500">Katalog MINF Informatik</td>
                  <td class="p-3 text-center font-bold">6</td>
                  <td class="p-3 text-center"><span class="tag-badge bg-indigo-600 text-white font-bold">1,7</span></td>
                  <td class="p-3">Architekturmuster (Microservices, Event-Driven, SOA), Schnittstellendesign (REST, gRPC, Event Mesh), Bounded Contexts und Entkopplungsstrategien für Cloud-Plattformen.</td>
                </tr>

                <!-- 8. Service Management & Cloud Computing -->
                <tr>
                  <td class="p-3 font-semibold text-slate-900 dark:text-white">Service Management and Cloud Computing, and Evaluation</td>
                  <td class="p-3 whitespace-nowrap text-slate-500">Katalog MINF Informatik</td>
                  <td class="p-3 text-center">6</td>
                  <td class="p-3 text-center"><span class="tag-badge bg-slate-200 dark:bg-slate-700 text-slate-800 dark:text-slate-200 font-semibold">2,0</span></td>
                  <td class="p-3">AWS Well-Architected Framework, Microservices & Serverless (DynamoDB, EventBridge, Step Functions), Cloud Service Level Agreements (SLAs) und quantitative Evaluation.</td>
                </tr>

                <!-- 9. Datenbanken und Informationssysteme -->
                <tr>
                  <td class="p-3 font-semibold text-slate-900 dark:text-white">Datenbanken und Informationssysteme</td>
                  <td class="p-3 whitespace-nowrap text-slate-500">Katalog MINF Informatik</td>
                  <td class="p-3 text-center">6</td>
                  <td class="p-3 text-center"><span class="tag-badge bg-slate-200 dark:bg-slate-700 text-slate-800 dark:text-slate-200 font-semibold">2,7</span></td>
                  <td class="p-3">Relationale Datenmodelle, SQL-Anfragen, ACID-Transaktionsprinzipien, Indizierungsstrategien, NoSQL- und In-Memory-Konzepte (Fundament für SAP HANA).</td>
                </tr>

                <!-- 10. Innovationsmanagement -->
                <tr>
                  <td class="p-3 font-semibold text-slate-900 dark:text-white">Innovationsmanagement</td>
                  <td class="p-3 whitespace-nowrap text-slate-500">Katalog Betriebswirtschaftslehre</td>
                  <td class="p-3 text-center">6</td>
                  <td class="p-3 text-center"><span class="tag-badge bg-slate-200 dark:bg-slate-700 text-slate-800 dark:text-slate-200 font-semibold">1,7</span></td>
                  <td class="p-3">Disruptive Innovationen, Plattform-Ökosysteme, Technologie-Lebenszyklen und strategische Go-to-Market-Planung für digitale Produkte.</td>
                </tr>

                <!-- 11. Theorie & Empirie int. Unternehmenstätigkeit (INUT) -->
                <tr>
                  <td class="p-3 font-semibold text-slate-900 dark:text-white">Theorie und Empirie internationaler Unternehmenstätigkeit (INUT)</td>
                  <td class="p-3 whitespace-nowrap text-slate-500">Katalog Betriebswirtschaftslehre</td>
                  <td class="p-3 text-center">6</td>
                  <td class="p-3 text-center"><span class="tag-badge bg-slate-200 dark:bg-slate-700 text-slate-800 dark:text-slate-200 font-semibold">1,7</span></td>
                  <td class="p-3">Globale Wertschöpfungsketten, internationale Standortentscheidungen, Multinationale Konzerne (MNE), globales IT-Sourcing und Außenhandelstheorie.</td>
                </tr>

                <!-- SECTION 3: ERGÄNZENDE SPEZIALISIERUNGSMODULE (24 ECTS) -->
                <tr class="bg-slate-100/80 dark:bg-slate-800/80 font-bold text-slate-900 dark:text-white">
                  <td colspan="5" class="p-2.5 uppercase tracking-wider text-[11px] text-purple-700 dark:text-purple-400">
                    🚀 Bereich 3: Ergänzende Spezialisierungsmodule (24 ECTS)
                  </td>
                </tr>

                <!-- 1. Digitale Nachhaltigkeit -->
                <tr class="bg-emerald-50/20 dark:bg-emerald-950/10">
                  <td class="p-3 font-semibold text-slate-900 dark:text-white">Digitale Nachhaltigkeit (Green IT & CSRD)</td>
                  <td class="p-3 whitespace-nowrap text-slate-500">Katalog Wirtschaftsinformatik</td>
                  <td class="p-3 text-center font-bold">6</td>
                  <td class="p-3 text-center"><span class="tag-badge bg-emerald-600 text-white font-bold">1,0</span></td>
                  <td class="p-3">Praxis-Fallstudie J. Schmalz GmbH: BPMN-Prozessmodellierung, Schnittstellenintegration und Software-Prototyp zur automatisierten CSRD-Abfallbilanz.</td>
                </tr>

                <!-- 2. Applied AI -->
                <tr>
                  <td class="p-3 font-semibold text-slate-900 dark:text-white">Applied AI and Upcoming Technologies in Industries</td>
                  <td class="p-3 whitespace-nowrap text-slate-500">Katalog Wirtschaftsinformatik</td>
                  <td class="p-3 text-center">6</td>
                  <td class="p-3 text-center"><span class="tag-badge bg-slate-200 dark:bg-slate-700 text-slate-800 dark:text-slate-200 font-semibold">1,7</span></td>
                  <td class="p-3">Machine Learning im industriellen Einsatz, NLP, LLM-Architekturen, generative KI und Integration intelligenter Algorithmen in ERP-Geschäftsprozesse.</td>
                </tr>

                <!-- 3. ISG Innovationsmethoden -->
                <tr>
                  <td class="p-3 font-semibold text-slate-900 dark:text-white">Innovationsmethoden für software- und datenintensive Geschäftsmodelle (ISG)</td>
                  <td class="p-3 whitespace-nowrap text-slate-500">Katalog Wirtschaftsinformatik</td>
                  <td class="p-3 text-center">6</td>
                  <td class="p-3 text-center"><span class="tag-badge bg-slate-200 dark:bg-slate-700 text-slate-800 dark:text-slate-200 font-semibold">2,0</span></td>
                  <td class="p-3">Data-driven Business Models, Plattformökonomie, Venture-Pitch „PatentRadar“ für Klingele Paper & Packaging (Verknüpfung mit Bosch-Erfahrung).</td>
                </tr>

                <!-- 4. Service Operations Management -->
                <tr>
                  <td class="p-3 font-semibold text-slate-900 dark:text-white">Service Operations Management (SOM)</td>
                  <td class="p-3 whitespace-nowrap text-slate-500">Katalog Betriebswirtschaftslehre</td>
                  <td class="p-3 text-center">6</td>
                  <td class="p-3 text-center"><span class="tag-badge bg-slate-200 dark:bg-slate-700 text-slate-800 dark:text-slate-200 font-semibold">3,0</span></td>
                  <td class="p-3">Operations Management, Warteschlangentheorie, Kapazitäts- und Durchsatzoptimierung operativer Dienstleistungsprozesse im Dienstleistungssektor.</td>
                </tr>

              </tbody>
            </table>
          </div>
        </div>

        <!-- The 12 Empirical Expert Interviews -->
        <div class="bg-white dark:bg-slate-900 p-6 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm space-y-4">
          <div class="flex items-center justify-between">
            <h3 class="text-base font-bold text-slate-900 dark:text-white flex items-center space-x-2">
              <span>🎙️</span>
              <span>Die 12 empirischen Experteninterviews deiner Masterarbeit (IP1–IP12)</span>
            </h3>
            <span class="tag-badge bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300">Mayring Inhaltsanalyse & Codebuch</span>
          </div>
          <p class="text-xs text-slate-500">
            Alle Transkripte und das Auswertungs-Codebuch liegen nun lokal im Workspace unter <code>Studium_Dokumente/Interviews_Masterarbeit</code>:
          </p>

          <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-3 text-xs">
            <div class="p-3.5 bg-slate-50 dark:bg-slate-800/40 rounded-xl border border-slate-200 dark:border-slate-700 space-y-1.5">
              <div class="flex justify-between items-center">
                <span class="font-bold text-slate-900 dark:text-white">Roland Nowak</span>
                <span class="text-[9px] bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300 px-1.5 py-0.5 rounded font-bold">IP1</span>
              </div>
              <div class="text-[11px] text-blue-600 dark:text-blue-400 font-semibold">Gesamtprojektleiter SAP4SSB</div>
              <p class="text-slate-600 dark:text-slate-300 text-[10px] leading-relaxed">
                Fokus: Multiprojektsteuerung (TP1–TP5), ERP-Plattform-Governance, C-Level Alignment und formelle Betriebsvereinbarung mit BR.
              </p>
              <div class="text-[9px] text-slate-400 font-mono">Interview_Roland_Nowak_Gesamt_PL.docx</div>
            </div>

            <div class="p-3.5 bg-slate-50 dark:bg-slate-800/40 rounded-xl border border-slate-200 dark:border-slate-700 space-y-1.5">
              <div class="flex justify-between items-center">
                <span class="font-bold text-slate-900 dark:text-white">Thomas Wimpff</span>
                <span class="text-[9px] bg-emerald-100 text-emerald-800 dark:bg-emerald-900 dark:text-emerald-300 px-1.5 py-0.5 rounded font-bold">IP2</span>
              </div>
              <div class="text-[11px] text-emerald-600 dark:text-emerald-400 font-semibold">Teilprojektleiter TP2 (Finance & Controlling)</div>
              <p class="text-slate-600 dark:text-slate-300 text-[10px] leading-relaxed">
                Fokus: Trennungsrechnung (Kaufmännisch/Steuerlich), Universelles Journal (ACDOCA), Ablösung von Innenaufträgen durch PSP-Elemente und Übernahmekonto 0,00 €.
              </p>
              <div class="text-[9px] text-slate-400 font-mono">Interview_Thomas_Wimpff_TP2_Leitung.docx</div>
            </div>

            <div class="p-3.5 bg-slate-50 dark:bg-slate-800/40 rounded-xl border border-slate-200 dark:border-slate-700 space-y-1.5">
              <div class="flex justify-between items-center">
                <span class="font-bold text-slate-900 dark:text-white">Armin Heinrich</span>
                <span class="text-[9px] bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-300 px-1.5 py-0.5 rounded font-bold">IP3</span>
              </div>
              <div class="text-[11px] text-purple-600 dark:text-purple-400 font-semibold">Enterprise Basisarchitekt SSB AG</div>
              <p class="text-slate-600 dark:text-slate-300 text-[10px] leading-relaxed">
                Fokus: BTP-Zielarchitektur, SSO-Integration mit Microsoft Entra ID, ES4 Mandantenlandschaft und Schnittstellenabsicherung.
              </p>
              <div class="text-[9px] text-slate-400 font-mono">Interview_Armin_Heinrich_Basis_Architektur.docx</div>
            </div>

            <div class="p-3.5 bg-slate-50 dark:bg-slate-800/40 rounded-xl border border-slate-200 dark:border-slate-700 space-y-1.5">
              <div class="flex justify-between items-center">
                <span class="font-bold text-slate-900 dark:text-white">Henning Gerdes</span>
                <span class="text-[9px] bg-amber-100 text-amber-800 dark:bg-amber-900 dark:text-amber-300 px-1.5 py-0.5 rounded font-bold">IP4</span>
              </div>
              <div class="text-[11px] text-amber-600 dark:text-amber-400 font-semibold">Lead Architect Axians ES4</div>
              <p class="text-slate-600 dark:text-slate-300 text-[10px] leading-relaxed">
                Fokus: Bereitstellung der Private-Cloud-Infrastruktur, Adobe Document Services (ADS) Formulare und Transportkonsolidierung.
              </p>
              <div class="text-[9px] text-slate-400 font-mono">Interview_Henning_Gerdes_Axians_Lead.docx</div>
            </div>
          </div>
        </div>

        <!-- The 4 Core Theoretical Constructs -->
        <div class="bg-white dark:bg-slate-900 p-6 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm space-y-4">
          <h3 class="text-base font-bold text-slate-900 dark:text-white flex items-center space-x-2">
            <span>🔬</span>
            <span>Die 4 theoretischen Säulen deiner wissenschaftlichen Arbeit</span>
          </h3>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
            <div class="p-4 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/40 space-y-1.5">
              <div class="font-bold text-blue-600 dark:text-blue-400">1. Boundary Resources Theory (Wareham et al., 2014)</div>
              <p class="text-slate-600 dark:text-slate-300 text-[11px] leading-relaxed">
                Schnittstellen, APIs, CDS Views und Entwicklungsrichtlinien sind nicht bloß technischer Code, sondern strategische „Grenzressourcen“. Sie bestimmen, wie Drittpartner (Nagarro, Axians) an die Plattform andocken können, ohne die Kernstabilität zu gefährden.
              </p>
            </div>

            <div class="p-4 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/40 space-y-1.5">
              <div class="font-bold text-purple-600 dark:text-purple-400">2. Decoupling / Entkopplungstheorie (Benlian et al., 2015)</div>
              <p class="text-slate-600 dark:text-slate-300 text-[11px] leading-relaxed">
                Bimodale IT in der Praxis: Der ERP-Kern (System of Record) muss hochgradig stabil und standardisiert bleiben, während kundenindividuelle Innovationszyklen (Systems of Innovation) auf der SAP BTP entkoppelt und agil entwickelt werden.
              </p>
            </div>

            <div class="p-4 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/40 space-y-1.5">
              <div class="font-bold text-emerald-600 dark:text-emerald-400">3. Absorptive Capacity Theory (Min et al., 2016)</div>
              <p class="text-slate-600 dark:text-slate-300 text-[11px] leading-relaxed">
                Die Fähigkeit einer Organisation (wie der SSB), externes Wissen der Implementierungspartner aufzunehmen und in eigenes Know-how zu transformieren. Ohne gezieltes Enablement (Enable Now) entsteht gefährliche Beraterabhängigkeit.
              </p>
            </div>

            <div class="p-4 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/40 space-y-1.5">
              <div class="font-bold text-amber-600 dark:text-amber-400">4. Das Integrations-Paradoxon & Technical Debt</div>
              <p class="text-slate-600 dark:text-slate-300 text-[11px] leading-relaxed">
                Jede Sonderlocke und jedes proprietäre Z-Programm erhöht kurzfristig die Zufriedenheit einzelner Key User, erzeugt aber langfristig exponentiell steigende Upgrade- und Wartungskosten (Technische Schuld). Eine strategische Plattform- und Schnittstellen-Governance löst dieses Paradoxon auf.
              </p>
            </div>
          </div>
        </div>

        <!-- The 4x4 Phase-based Platform Excellence Framework -->
        <div class="bg-white dark:bg-slate-900 p-6 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm space-y-4">
          <h3 class="text-base font-bold text-slate-900 dark:text-white flex items-center space-x-2">
            <span>📊</span>
            <span>Das Phase-based Platform Excellence Framework (Phasen × Dimensionen)</span>
          </h3>
          <div class="overflow-x-auto">
            <table class="w-full text-left text-xs border border-slate-200 dark:border-slate-700 rounded-xl overflow-hidden">
              <thead class="bg-slate-100 dark:bg-slate-800 text-slate-900 dark:text-white font-bold">
                <tr>
                  <th class="p-3 border-b dark:border-slate-700">Kategorie</th>
                  <th class="p-3 border-b dark:border-slate-700">Pre-Implementation (Discover / Prepare)</th>
                  <th class="p-3 border-b dark:border-slate-700">Implementation (Explore / Realize)</th>
                  <th class="p-3 border-b dark:border-slate-700">Post-Implementation (Deploy / Run)</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-slate-200 dark:divide-slate-700 text-slate-600 dark:text-slate-300">
                <tr>
                  <td class="p-3 font-semibold text-slate-900 dark:text-white bg-slate-50 dark:bg-slate-800/40">Organisation & Strategie</td>
                  <td class="p-3">Strategische Plattform-Vision, C-Level Commitment, Betriebsvereinbarung mit Betriebsrat.</td>
                  <td class="p-3">Strikte Standard-Governance (Abweichung vom Standard bedarf Freigabe), Rollenmodell.</td>
                  <td class="p-3">Kontinuierliche BTP-Roadmap, Anpassung an halbjährliche Cloud-Release-Zyklen.</td>
                </tr>
                <tr>
                  <td class="p-3 font-semibold text-slate-900 dark:text-white bg-slate-50 dark:bg-slate-800/40">Technik & Architektur</td>
                  <td class="p-3">Clean-Core-Strategie, Ziel-Architektur (BTP vs Core), Systemlandkarte (EAM/LeanIX).</td>
                  <td class="p-3">API-First Management, Side-by-Side Extensions, Staging-Datenmigration, Testautomatisierung.</td>
                  <td class="p-3">Upgrade-Stabilität, Monitoring über SAP Cloud ALM Operations, Schnittstellen-Performance.</td>
                </tr>
                <tr>
                  <td class="p-3 font-semibold text-slate-900 dark:text-white bg-slate-50 dark:bg-slate-800/40">Mensch & Befähigung</td>
                  <td class="p-3">Transparente Change-Kommunikation, Abbau von Zukunftsängsten bei Fachbereichen.</td>
                  <td class="p-3">Key-User-Befähigung, In-App-Lernen mit SAP Enable Now, abteilungsübergreifende Co-Creation.</td>
                  <td class="p-3">Kultureller Wandel zum agilen Plattform-Mindset, kontinuierliches Feedback.</td>
                </tr>
                <tr>
                  <td class="p-3 font-semibold text-slate-900 dark:text-white bg-slate-50 dark:bg-slate-800/40">Projektmanagement</td>
                  <td class="p-3">Partner-Auswahl (Tier-1 Kompetenz), Meilenstein- und Budgetplanung, Scope-Definition.</td>
                  <td class="p-3">Agiles Fit-to-Standard Tracking in CALM, Multi-Projekt-Synchronisation (TP1–TP5).</td>
                  <td class="p-3">Hyper-Care-Management, Lesson-Learned-Synthese, Übergang in Regelbetrieb.</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

      </div>
"""
