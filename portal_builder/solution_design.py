# -*- coding: utf-8 -*-

def get_solution_design():
    return """
      <!-- ================= TAB 4: SOLUTION DESIGN DEEP-DIVE ================= -->
      <div v-show="activeTab === 'solution_design'" class="space-y-6">
        
        <div class="bg-white dark:bg-slate-900 p-6 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm space-y-4">
          <div class="flex items-center justify-between">
            <div>
              <h3 class="text-lg font-bold text-slate-900 dark:text-white">Solution Design Deep-Dive: Kaufmännische Prozesse (TP2)</h3>
              <p class="text-xs text-slate-500">Detaillierte Analyse des 82.000 Zeichen starken Lösungsdesign-Dokuments (Nagarro & SSB)</p>
            </div>
            <span class="tag-badge bg-emerald-100 text-emerald-800 dark:bg-emerald-900/60 dark:text-emerald-300">Finance & Controlling Blueprint</span>
          </div>

          <!-- Enterprise Structure & Core Principles -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 pt-2">
            
            <!-- Buchungskreise & Controllingbereich -->
            <div class="p-4 rounded-xl bg-slate-50 dark:bg-slate-800/50 border border-slate-200 dark:border-slate-700 space-y-2">
              <h4 class="text-sm font-bold text-slate-900 dark:text-white flex items-center space-x-2">
                <span>🏢</span>
                <span>Organisationsstruktur (Bukrs & Kokrs)</span>
              </h4>
              <ul class="text-xs text-slate-600 dark:text-slate-300 space-y-2">
                <li>
                  <strong>Buchungskreise (Bukrs):</strong>
                  <ul class="pl-4 list-disc mt-1 space-y-0.5">
                    <li><code>Bukrs 1000</code>: Stuttgarter Straßenbahnen AG (ÖPNV, Muttergesellschaft).</li>
                    <li><code>Bukrs 3000</code>: SSB Reisen GmbH (Tourismus & gewerbliche Verkehre).</li>
                  </ul>
                </li>
                <li>
                  <strong>Controllingbereiche (Kokrs):</strong>
                  <div class="mt-0.5">Zuordnung 1:1 zu Buchungskreisen (Kokrs 1000 und Kokrs 3000), um eine strikte gesellschaftsrechtliche Trennung der Deckungsbeiträge zu garantieren.</div>
                </li>
                <li>
                  <strong>Währung & Geschäftsjahr:</strong>
                  <div class="mt-0.5">Buchungskreiswährung EUR, Geschäftsjahr entspricht dem Kalenderjahr (K4: 12 Perioden + 4 Sonderperioden).</div>
                </li>
              </ul>
            </div>

            <!-- Trennungsrechnung & PSP-Dogma -->
            <div class="p-4 rounded-xl bg-slate-50 dark:bg-slate-800/50 border border-slate-200 dark:border-slate-700 space-y-2">
              <h4 class="text-sm font-bold text-slate-900 dark:text-white flex items-center space-x-2">
                <span>⚖️</span>
                <span>Trennungsrechnung & Das PSP-Dogma</span>
              </h4>
              <ul class="text-xs text-slate-600 dark:text-slate-300 space-y-2">
                <li>
                  <strong>Gesetzliche Trennungsrechnung (EU-VO 1370/2007):</strong>
                  <div class="mt-0.5">Als subventioniertes Verkehrsunternehmen muss die SSB gemeinwirtschaftliche Verkehrsleistungen (PBV) strikt von gewerblichen Tätigkeiten trennen. Quersubventionierungen sind beihilferechtlich verboten!</div>
                </li>
                <li>
                  <strong>Profit Center als Schattenobjekte:</strong>
                  <div class="mt-0.5">Profit Center werden im Zielsystem primär als <em>Schattenobjekte</em> geführt, um die Segmentberichterstattung und Trennungsrechnung zu sichern – nicht zur operativen Kostenstellensteuerung.</div>
                </li>
                <li>
                  <strong>Abschaffung der Innenaufträge:</strong>
                  <div class="mt-0.5 font-medium text-blue-600 dark:text-blue-400">Strategische Vereinheitlichung: Klassische Innenaufträge (CO-OM-OPA) werden komplett abgeschafft! Sämtliche Investitionen, Projekte und Kostensammler werden über PSP-Elemente (Projektsystem / PS) gesteuert.</div>
                </li>
              </ul>
            </div>

          </div>
        </div>

        <!-- Universal Journal & Ledger Architecture -->
        <div class="bg-white dark:bg-slate-900 p-6 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm space-y-4">
          <h3 class="text-base font-bold text-slate-900 dark:text-white flex items-center space-x-2">
            <span>📊</span>
            <span>Universal Journal (ACDOCA) & Multi-Ledger Architektur</span>
          </h3>

          <div class="grid grid-cols-1 md:grid-cols-3 gap-3 text-xs">
            <div class="p-3.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/40 space-y-1.5">
              <div class="font-bold text-blue-600">1. Single Source of Truth (ACDOCA)</div>
              <p class="text-slate-600 dark:text-slate-300 leading-relaxed">
                In SAP ECC 6.0 gab es getrennte Tabellen für Hauptbuch (BKPF/BSEG), Anlagen (ANEP), Controlling (COEP) und Material (MLIT). In S/4HANA fließen alle Finanz- und Controllingbuchungen in eine einzige Tabelle: <strong>ACDOCA</strong>. Sekundärkostenarten sind nun vollwertige Sachkonten.
              </p>
            </div>

            <div class="p-3.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/40 space-y-1.5">
              <div class="font-bold text-purple-600">2. Ledger-Ansatz (Multi-GAAP)</div>
              <p class="text-slate-600 dark:text-slate-300 leading-relaxed">
                <strong>Leading Ledger (0L):</strong> Führt den handelsrechtlichen Abschluss nach HGB und Steuerrecht.<br>
                <strong>Non-Leading Ledger (2L):</strong> Parallelführung für IFRS-Konzernberichterstattung und kalkulatorische Abschreibungen, besonders relevant für Schienenfahrzeuge und Gleisinfrastruktur.
              </p>
            </div>

            <div class="p-3.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/40 space-y-1.5">
              <div class="font-bold text-emerald-600">3. New Asset Accounting (FI-AA)</div>
              <p class="text-slate-600 dark:text-slate-300 leading-relaxed">
                Anlagenbuchhaltung bucht in Echtzeit in alle relevanten Ledger. Delta-Buchungsläufe gehören der Vergangenheit an. Statistische Anlagen im Bau (AiB) werden direkt mit PSP-Elementen gekoppelt und bei Fertigstellung per Endabrechnung aktiviert.
              </p>
            </div>
          </div>
        </div>

        <!-- Business Partner & Customer Vendor Integration (CVI) -->
        <div class="bg-white dark:bg-slate-900 p-6 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm space-y-4">
          <h3 class="text-base font-bold text-slate-900 dark:text-white flex items-center space-x-2">
            <span>👥</span>
            <span>Business Partner (CVI) & Stammdaten-Harmonisierung</span>
          </h3>
          <p class="text-xs text-slate-500">Zusammenführung historischer Stammdaten im Rahmen des Greenfield Scopes</p>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
            <div class="p-4 rounded-xl bg-slate-50 dark:bg-slate-800/40 border border-slate-200 dark:border-slate-700 space-y-2">
              <div class="font-bold text-slate-900 dark:text-white text-xs uppercase tracking-wider text-amber-600">Das CVI-Prinzip</div>
              <p class="text-slate-600 dark:text-slate-300 leading-relaxed">
                In SAP ECC 6.0 existierten Debitoren (Tabelle <code>KNA1</code>) und Kreditoren (Tabelle <code>LFA1</code>) getrennt nebeneinander. War ein Zulieferer (z.B. Siemens Mobility) gleichzeitig Kunde für Werkstattleistungen, gab es zwei Stammsätze ohne automatische Verknüpfung.
              </p>
              <p class="text-slate-600 dark:text-slate-300 leading-relaxed">
                In S/4HANA ist der <strong>Business Partner (BP)</strong> das zentrale führende Objekt (Tabelle <code>BUT000</code>). Ein BP erhält Rollen:
                <br>• <code>FLCU00 / FLCU01</code>: Debitor (FI & Vertrieb)
                <br>• <code>FLVN00 / FLVN01</code>: Kreditor (FI & Einkauf)
              </p>
            </div>

            <div class="p-4 rounded-xl bg-slate-50 dark:bg-slate-800/40 border border-slate-200 dark:border-slate-700 space-y-2">
              <div class="font-bold text-slate-900 dark:text-white text-xs uppercase tracking-wider text-blue-600">Konsolidierungshebel bei der SSB</div>
              <ul class="text-slate-600 dark:text-slate-300 space-y-1.5 list-disc list-inside">
                <li><strong>Dublettenbereinigung:</strong> Hunderte historisch doppelt angelegte Handwerker und Lieferanten wurden vor der Migration zusammengeführt.</li>
                <li><strong>Nummernkreis-Harmonisierung:</strong> Festlegung gleicher Nummern für Business Partner, Debitor und Kreditor zur Vermeidung von Verwirrung in den Fachabteilungen.</li>
                <li><strong>Bankdaten-Validierung:</strong> IBAN- und BIC-Prüfung über SEPA-Regeln direkt in den Staging-Tabellen vor dem S/4HANA Import.</li>
              </ul>
            </div>
          </div>
        </div>

      </div>
"""
