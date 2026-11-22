# -*- coding: utf-8 -*-

def get_enterprise_arch():
    return """
      <!-- ================= TAB 8: ENTERPRISE ARCHITECTURE & ITIL ================= -->
      <div v-show="activeTab === 'enterprise_arch'" class="space-y-6">
        
        <div class="bg-white dark:bg-slate-900 p-6 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm space-y-4">
          <div class="flex items-center justify-between">
            <div>
              <h3 class="text-lg font-bold text-slate-900 dark:text-white">Enterprise Architecture (TOGAF) & IT-Operations (ITIL 4)</h3>
              <p class="text-xs text-slate-500">Methodisches Fundament aus TOGAF-Zertifizierung und 12 Monaten Rechenzentrumserfahrung (Datacenter One)</p>
            </div>
            <span class="tag-badge bg-blue-100 text-blue-800 dark:bg-blue-900/60 dark:text-blue-300">Scape Consulting & Datacenter One</span>
          </div>

          <!-- TOGAF ADM Cycle -->
          <div class="p-4 rounded-xl bg-slate-50 dark:bg-slate-800/50 border border-slate-200 dark:border-slate-700 space-y-3">
            <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
              <h4 class="text-sm font-bold text-slate-900 dark:text-white flex items-center space-x-2">
                <span>🏛️</span>
                <span>Der TOGAF Architecture Development Method (ADM) Zyklus</span>
              </h4>
              <div class="flex items-center space-x-2">
                <span class="text-[11px] text-slate-500">Intensivkurs Scape Consulting (Dr. Daniel Simon)</span>
                <a href="Studium_Dokumente/Togaf_Zertifikat.pdf" target="_blank" class="px-2.5 py-1 rounded bg-blue-600 hover:bg-blue-700 text-white font-bold text-[11px] transition inline-flex items-center space-x-1">
                  <span>📜</span>
                  <span>Zertifikat (PDF)</span>
                </a>
              </div>
            </div>
            <p class="text-xs text-slate-600 dark:text-slate-300 leading-relaxed">
              TOGAF ist dein strategischer Kompass, um komplexe IT-Landschaften ganzheitlich zu strukturieren. Bei der SSB hast du diesen Zyklus im Programm SAP4SSB in der Praxis erlebt:
            </p>

            <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-2.5 text-xs pt-1">
              <div class="p-3 bg-white dark:bg-slate-900 rounded-lg border border-slate-200 dark:border-slate-800">
                <div class="font-bold text-blue-600">Phase A: Architecture Vision</div>
                <div class="text-[11px] text-slate-500 mt-0.5">Greenfield S/4HANA Private Cloud, Clean Core Leitbild und Business Case mit Nagarro.</div>
              </div>

              <div class="p-3 bg-white dark:bg-slate-900 rounded-lg border border-slate-200 dark:border-slate-800">
                <div class="font-bold text-blue-600">Phase B: Business Architecture</div>
                <div class="text-[11px] text-slate-500 mt-0.5">Fit-to-Standard Workshops, Soll-Prozessmodellierung in SAP Signavio (BPMN 2.0).</div>
              </div>

              <div class="p-3 bg-white dark:bg-slate-900 rounded-lg border border-slate-200 dark:border-slate-800">
                <div class="font-bold text-blue-600">Phase C: Information Systems</div>
                <div class="text-[11px] text-slate-500 mt-0.5">Datenarchitektur (CVI Business Partner, ACDOCA) und Applikationslandschaft (xSuite, d.velop).</div>
              </div>

              <div class="p-3 bg-white dark:bg-slate-900 rounded-lg border border-slate-200 dark:border-slate-800">
                <div class="font-bold text-blue-600">Phase D: Technology Architecture</div>
                <div class="text-[11px] text-slate-500 mt-0.5">SAP BTP, Axians ES4 Systeme, Cloud-Infrastruktur, Single Sign-On und ADS-Druckdienste.</div>
              </div>

              <div class="p-3 bg-white dark:bg-slate-900 rounded-lg border border-slate-200 dark:border-slate-800">
                <div class="font-bold text-purple-600">Phase E: Opportunities & Solutions</div>
                <div class="text-[11px] text-slate-500 mt-0.5">Bewertung von Standard vs. Side-by-Side BTP Erweiterungen und Partnersichtung.</div>
              </div>

              <div class="p-3 bg-white dark:bg-slate-900 rounded-lg border border-slate-200 dark:border-slate-800">
                <div class="font-bold text-purple-600">Phase F: Migration Planning</div>
                <div class="text-[11px] text-slate-500 mt-0.5">Cutover-Drehbuch, Staging-Datenmigration, Freeze-Perioden und SuSa-Bilanzabgleich.</div>
              </div>

              <div class="p-3 bg-white dark:bg-slate-900 rounded-lg border border-slate-200 dark:border-slate-800">
                <div class="font-bold text-purple-600">Phase G: Implementation Governance</div>
                <div class="text-[11px] text-slate-500 mt-0.5">Dein IT-PMO Kerngeschäft: Quality Gates in SAP Cloud ALM, Meilenstein-Tracking.</div>
              </div>

              <div class="p-3 bg-white dark:bg-slate-900 rounded-lg border border-slate-200 dark:border-slate-800">
                <div class="font-bold text-purple-600">Phase H: Change Management</div>
                <div class="text-[11px] text-slate-500 mt-0.5">TP1 Enablement, SAP Enable Now Übergabe an HR (UB AC) und Anwenderbefähigung.</div>
              </div>
            </div>
          </div>
        </div>

        <!-- Datacenter One & ITIL Service Management -->
        <div class="bg-white dark:bg-slate-900 p-6 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm space-y-4">
          <div class="flex items-center justify-between">
            <h3 class="text-base font-bold text-slate-900 dark:text-white flex items-center space-x-2">
              <span>🖥️</span>
              <span>ITIL 4 Service Operations (Datacenter One - 12 Monate INOC)</span>
            </h3>
            <span class="tag-badge bg-emerald-100 text-emerald-800">24/7 Mission Critical Operations</span>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-3 gap-3 text-xs">
            <div class="p-3.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/40 space-y-1.5">
              <div class="font-bold text-slate-900 dark:text-white">1. Incident & Problem Management</div>
              <p class="text-slate-600 dark:text-slate-300 leading-relaxed text-[11px]">
                Erfassung, Klassifizierung und Behebung von Störungen im Integrated Network Operation Center (INOC). Einhaltung strikter SLAs (Service Level Agreements) für Colocation- und Cloud-Kunden. Unterscheidung zwischen Sofort-Workaround (Incident) und Ursachenanalyse (Root Cause Analysis / Problem Management).
              </p>
            </div>

            <div class="p-3.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/40 space-y-1.5">
              <div class="font-bold text-slate-900 dark:text-white">2. Monitoring & Event Management</div>
              <p class="text-slate-600 dark:text-slate-300 leading-relaxed text-[11px]">
                Proaktive Überwachung von Rechenzentrums-Infrastruktur: USV-Anlagen, Klimatechnik, Glasfaser-Trassen und Core-Switche. Alarmierungsketten, Eskalationsmanagement nach Matrix und Kommunikation an Notfall-Bereitschaften.
              </p>
            </div>

            <div class="p-3.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/40 space-y-1.5">
              <div class="font-bold text-slate-900 dark:text-white">3. Tool-Stack: Jira & Confluence</div>
              <p class="text-slate-600 dark:text-slate-300 leading-relaxed text-[11px]">
                Lückenlose Dokumentation von Störungsberichten und Notfallhandbüchern (Standard Operating Procedures / SOPs). Revisionssichere Übergabeprotokolle bei Schichtwechseln unter Leitung von Helmut Schmidpeter.
              </p>
            </div>
          </div>
        </div>

        <!-- BPMN 2.0 Process Modeling Standard -->
        <div class="bg-white dark:bg-slate-900 p-6 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm space-y-4">
          <h3 class="text-base font-bold text-slate-900 dark:text-white flex items-center space-x-2">
            <span>🔄</span>
            <span>BPMN 2.0 Modellierungs-Standard (SAP Signavio Referenz)</span>
          </h3>

          <div class="grid grid-cols-1 md:grid-cols-3 gap-3 text-xs">
            <div class="p-3 rounded-lg bg-slate-50 dark:bg-slate-800/40 border border-slate-200 dark:border-slate-700">
              <div class="font-bold text-blue-600 mb-1">Gateways & Verzweigungen</div>
              <ul class="text-slate-600 dark:text-slate-300 space-y-1 list-disc list-inside text-[11px]">
                <li><strong>Exklusiv (XOR):</strong> Genau ein Pfad wird gewählt (z.B. Rechnungsbetrag > 10.000 € ? Ja/Nein).</li>
                <li><strong>Parallel (AND):</strong> Alle ausgehenden Pfade werden gleichzeitig gestartet (z.B. Bonitätsprüfung und Lagerprüfung parallel).</li>
                <li><strong>Inklusiv (OR):</strong> Ein oder mehrere Pfade können gewählt werden.</li>
              </ul>
            </div>

            <div class="p-3 rounded-lg bg-slate-50 dark:bg-slate-800/40 border border-slate-200 dark:border-slate-700">
              <div class="font-bold text-purple-600 mb-1">Ereignisse (Events)</div>
              <ul class="text-slate-600 dark:text-slate-300 space-y-1 list-disc list-inside text-[11px]">
                <li><strong>Start-Event:</strong> Anstoß des Prozesses (z.B. Eingang BANF).</li>
                <li><strong>Zwischen-Event:</strong> Timer (z.B. Warte 5 Tage auf Freigabe) oder Nachrichtenempfang.</li>
                <li><strong>End-Event:</strong> Erfolgreicher Abschluss oder Fehlerabbruch (Terminating Event).</li>
              </ul>
            </div>

            <div class="p-3 rounded-lg bg-slate-50 dark:bg-slate-800/40 border border-slate-200 dark:border-slate-700">
              <div class="font-bold text-emerald-600 mb-1">Pools & Lanes (Zuständigkeiten)</div>
              <ul class="text-slate-600 dark:text-slate-300 space-y-1 list-disc list-inside text-[11px]">
                <li><strong>Pool:</strong> Repräsentiert eine eigenständige Organisationseinheit (z.B. SSB AG vs. Lieferant).</li>
                <li><strong>Lane:</strong> Teilbereich innerhalb des Pools (z.B. Einkauf, Finanzbuchhaltung, Werkstattleiter).</li>
                <li><strong>Message Flow:</strong> Nachrichtenfluss nur zwischen verschiedenen Pools erlaubt!</li>
              </ul>
            </div>
          </div>
        </div>

      </div>
"""
