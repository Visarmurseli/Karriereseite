# -*- coding: utf-8 -*-

def get_tools():
    return """
      <!-- ================= TAB 6: TOOL-STACK & METHODEN-HANDBUCH ================= -->
      <div v-show="activeTab === 'tools'" class="space-y-6">
        
        <div class="bg-white dark:bg-slate-900 p-6 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm space-y-4">
          <div class="flex items-center justify-between">
            <div>
              <h3 class="text-lg font-bold text-slate-900 dark:text-white">Die Cloud-Toolchain bei SAP4SSB</h3>
              <p class="text-xs text-slate-500">Governance, Traceability und Enablement in der Praxis</p>
            </div>
            <span class="tag-badge bg-blue-100 text-blue-800 dark:bg-blue-900/60 dark:text-blue-300">Modern ALM Architecture</span>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-3 gap-4 pt-2">
            <!-- SAP Cloud ALM -->
            <div class="p-4 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/40 space-y-3">
              <div class="flex items-center space-x-2 text-blue-600 font-bold text-sm">
                <span>⚡</span>
                <span>SAP Cloud ALM</span>
              </div>
              <p class="text-xs text-slate-600 dark:text-slate-300 leading-relaxed">
                Das zentrale Rückgrat für Projektsteuerung, Aufgabenverteilung und Testmanagement. 
              </p>
              <div class="text-xs space-y-1.5 text-slate-700 dark:text-slate-300">
                <div><strong>Deine Rolle:</strong> Verfasser des offiziellen <em>"SAP_CALM_How2handle_quickguide"</em> für die SSB.</div>
                <div><strong>Funktionen:</strong> Projekt-Scope, User Stories, funktionale Anforderungen, Quality Gates (Q-Gates), Testausführung.</div>
                <div><strong>Vorteil:</strong> Kein schwerfälliger Solution Manager mehr; Cloud-native SaaS-Lösung.</div>
              </div>
            </div>

            <!-- SAP Signavio -->
            <div class="p-4 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/40 space-y-3">
              <div class="flex items-center space-x-2 text-purple-600 font-bold text-sm">
                <span>🔄</span>
                <span>SAP Signavio</span>
              </div>
              <p class="text-xs text-slate-600 dark:text-slate-300 leading-relaxed">
                Die Plattform für Geschäftsprozessanalyse, Modellierung und Process Mining.
              </p>
              <div class="text-xs space-y-1.5 text-slate-700 dark:text-slate-300">
                <div><strong>Zusammenspiel:</strong> Modellierung der Soll-Prozesse in Signavio (BPMN 2.0).</div>
                <div><strong>Synchronisation:</strong> Nahtloser Export der Prozessmodelle nach Cloud ALM zur Verknüpfung mit Testfällen.</div>
                <div><strong>Process Insights:</strong> Schnelle Analyse des ECC 6.0 Altsystems (Plug and Gain Ansatz) zur Identifikation von Reibungsverlusten.</div>
              </div>
            </div>

            <!-- SAP Enable Now -->
            <div class="p-4 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/40 space-y-3">
              <div class="flex items-center space-x-2 text-amber-600 font-bold text-sm">
                <span>🎓</span>
                <span>SAP Enable Now</span>
              </div>
              <p class="text-xs text-slate-600 dark:text-slate-300 leading-relaxed">
                Die unternehmensweite Lösung für digitales Lernen, Benutzerführung und Content-Erstellung.
              </p>
              <div class="text-xs space-y-1.5 text-slate-700 dark:text-slate-300">
                <div><strong>Deine Leistung:</strong> Erstellung des strategischen Übergabekonzepts von der IT (UB I) an die Personalentwicklung (UB AC).</div>
                <div><strong>Single-Source-Prinzip:</strong> Aus einer einzigen Bildschirmaufnahme entstehen Schulungsunterlagen, interaktive Tutorials, Tests und die Fiori In-App-Hilfe (Web Assistant).</div>
              </div>
            </div>
          </div>
        </div>

        <!-- How CALM and Signavio interact -->
        <div class="bg-white dark:bg-slate-900 p-6 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm space-y-4">
          <h3 class="text-base font-bold text-slate-900 dark:text-white">Die geschlossene Traceability-Kette (Signavio ➔ CALM ➔ Testing ➔ Enable Now)</h3>
          <div class="p-4 rounded-xl bg-slate-50 dark:bg-slate-800/40 border border-slate-200 dark:border-slate-700 flex flex-col md:flex-row items-center justify-between gap-3 text-center text-xs">
            <div class="p-3 bg-white dark:bg-slate-900 rounded-lg shadow-sm border border-slate-200 dark:border-slate-800 w-full md:w-1/4">
              <div class="font-bold text-purple-600">1. Signavio</div>
              <div class="text-[11px] text-slate-500 mt-1">Prozessanalyse & BPMN 2.0 Modellierung (Soll-Prozess)</div>
            </div>
            <div class="text-slate-400 font-bold">➔</div>
            <div class="p-3 bg-white dark:bg-slate-900 rounded-lg shadow-sm border border-slate-200 dark:border-slate-800 w-full md:w-1/4">
              <div class="font-bold text-blue-600">2. Cloud ALM</div>
              <div class="text-[11px] text-slate-500 mt-1">Synchronisation, User Story, Anforderung & Testfall</div>
            </div>
            <div class="text-slate-400 font-bold">➔</div>
            <div class="p-3 bg-white dark:bg-slate-900 rounded-lg shadow-sm border border-slate-200 dark:border-slate-800 w-full md:w-1/4">
              <div class="font-bold text-emerald-600">3. Test Execution</div>
              <div class="text-[11px] text-slate-500 mt-1">Ausführung im ES4 System, Defect-Tracking & Q-Gates</div>
            </div>
            <div class="text-slate-400 font-bold">➔</div>
            <div class="p-3 bg-white dark:bg-slate-900 rounded-lg shadow-sm border border-slate-200 dark:border-slate-800 w-full md:w-1/4">
              <div class="font-bold text-amber-600">4. Enable Now</div>
              <div class="text-[11px] text-slate-500 mt-1">In-App Kontext-Hilfe für Endanwender im Produktivbetrieb</div>
            </div>
          </div>
        </div>

        <!-- Detail: SAP Cloud ALM How2Handle Leitfaden -->
        <div class="bg-white dark:bg-slate-900 p-6 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm space-y-4">
          <h3 class="text-base font-bold text-slate-900 dark:text-white flex items-center space-x-2">
            <span>📘</span>
            <span>Auszug aus deinem "SAP Cloud ALM How2Handle" Leitfaden</span>
          </h3>
          <p class="text-xs text-slate-500">Von Visar verfasster Standard für alle Teilprojektleiter und externen Berater</p>

          <div class="grid grid-cols-1 md:grid-cols-3 gap-3 text-xs">
            <div class="p-3.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/40 space-y-1">
              <div class="font-bold text-slate-900 dark:text-white">1. Projekt-Setup & Quality Gates</div>
              <p class="text-slate-600 dark:text-slate-300 text-[11px] leading-relaxed">
                Definition von Quality Gates (Q-Gate Explore, Q-Gate Realize, Q-Gate Deploy). Erst wenn 100% aller geschäftskritischen Anforderungen abgenommen und alle Blocker-Defects geschlossen sind, wird das Q-Gate im Lenkungsausschuss freigegeben.
              </p>
            </div>

            <div class="p-3.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/40 space-y-1">
              <div class="font-bold text-slate-900 dark:text-white">2. Task- & User-Story Tracking</div>
              <p class="text-slate-600 dark:text-slate-300 text-[11px] leading-relaxed">
                Jede Lücke (GAP) aus den Fit-to-Standard Workshops erhält eine eindeutige CalmID. Zuordnung nach T-Shirt-Sizes (S, M, L) und verbindliche Zuweisung an Teilprojektleiter (z.B. Wimpff für TP2, Neifer für TP3).
              </p>
            </div>

            <div class="p-3.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/40 space-y-1">
              <div class="font-bold text-slate-900 dark:text-white">3. Testfall-Management & Defect Clearing</div>
              <p class="text-slate-600 dark:text-slate-300 text-[11px] leading-relaxed">
                Manuelle und automatisierte Testfälle werden direkt an BPMN-Prozessdiagrammen aufgehängt. Tritt ein Fehler auf, wird ein Defect erzeugt, der direkt dem verantwortlichen Implementierungspartner (Nagarro, Evora) zugewiesen wird.
              </p>
            </div>
          </div>
        </div>

      </div>
"""
