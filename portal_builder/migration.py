# -*- coding: utf-8 -*-

def get_migration():
    return """
      <!-- ================= TAB 5: DATENMIGRATION DEEP-DIVE ================= -->
      <div v-show="activeTab === 'migration'" class="space-y-6">
        
        <div class="bg-white dark:bg-slate-900 p-6 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm space-y-4">
          <div class="flex items-center justify-between">
            <div>
              <h3 class="text-lg font-bold text-slate-900 dark:text-white">Datenmigrations-Methodik & Cutover-Architektur</h3>
              <p class="text-xs text-slate-500">Basiert auf dem Nagarro Migrationskonzept v0.1 und dem Migrationsobjekte-Vorschlag</p>
            </div>
            <span class="tag-badge bg-emerald-100 text-emerald-800 dark:bg-emerald-900/60 dark:text-emerald-300">SAP Migration Cockpit (LTMC)</span>
          </div>

          <!-- Migration Approaches Comparison -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 pt-2">
            <div class="p-4 rounded-xl bg-slate-50 dark:bg-slate-800/50 border border-slate-200 dark:border-slate-700 space-y-2">
              <h4 class="text-sm font-bold text-slate-900 dark:text-white flex items-center space-x-2">
                <span>📥</span>
                <span>Staging-Tabellen vs. Direkte Übertragung</span>
              </h4>
              <p class="text-xs text-slate-600 dark:text-slate-300 leading-relaxed">
                Bei der SSB wurde für die meisten Objekte der Ansatz über <strong>Staging-Tabellen</strong> gewählt. Warum?
              </p>
              <ul class="text-xs text-slate-600 dark:text-slate-300 space-y-1 list-disc list-inside">
                <li><strong>Entkopplung:</strong> Die Altdaten aus ECC 6.0 werden zunächst in dedizierte Staging-Tabellen auf einer separaten Datenbank extrahiert.</li>
                <li><strong>Bereinigung vor dem Import:</strong> Datenqualität und Dubletten können vor der Übernahme bereinigt werden (z.B. inaktive Kreditoren/Debitoren aussortieren).</li>
                <li><strong>Revisionssicherheit:</strong> Jede Transformation und jedes Mapping ist vor dem Einspielen in den S/4HANA Kern dokumentiert und nachvollziehbar.</li>
              </ul>
            </div>

            <div class="p-4 rounded-xl bg-slate-50 dark:bg-slate-800/50 border border-slate-200 dark:border-slate-700 space-y-2">
              <h4 class="text-sm font-bold text-slate-900 dark:text-white flex items-center space-x-2">
                <span>⚖️</span>
                <span>Bilanzabgleich & Das Übernahmekonto (0,00 €)</span>
              </h4>
              <p class="text-xs text-slate-600 dark:text-slate-300 leading-relaxed">
                Der absolute Lackmustest für das Finanzwesen (FI) bei jedem Cutover:
              </p>
              <ul class="text-xs text-slate-600 dark:text-slate-300 space-y-1 list-disc list-inside">
                <li><strong>Eröffnungsbilanz:</strong> Sachkontensalden, Offene Posten (OPs) von Debitoren/Kreditoren und Anlagenwerte (FI-AA) werden migriert.</li>
                <li><strong>Gegenbuchung:</strong> Jede Migrationsbuchung erfolgt gegen ein zentrales <em>Datenübernahmekonto</em>.</li>
                <li><strong>Goldene Regel:</strong> Nach vollständiger Migration der Summen- und Saldenliste (SuSa) muss das Übernahmekonto exakt <strong>0,00 €</strong> aufweisen. Weicht es um 1 Cent ab, scheitert das Quality Gate für den Produktivstart!</li>
              </ul>
            </div>
          </div>
        </div>

        <!-- Migration Workflow Steps -->
        <div class="bg-white dark:bg-slate-900 p-6 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm space-y-4">
          <h3 class="text-base font-bold text-slate-900 dark:text-white">Der 5-stufige Migrations-Workflow im Cockpit</h3>
          <div class="grid grid-cols-1 md:grid-cols-5 gap-3 text-xs">
            <div class="p-3 rounded-xl bg-slate-50 dark:bg-slate-800/40 border border-slate-200 dark:border-slate-700">
              <div class="font-bold text-blue-600 mb-1">Schritt 1: Extraktion</div>
              <p class="text-slate-600 dark:text-slate-300">
                Altdaten-Export aus ECC Tabellen (KNA1, LFA1, SKA1, ANLC) in Staging-Dateien oder DB-Tabellen.
              </p>
            </div>
            <div class="p-3 rounded-xl bg-slate-50 dark:bg-slate-800/40 border border-slate-200 dark:border-slate-700">
              <div class="font-bold text-blue-600 mb-1">Schritt 2: Mapping</div>
              <p class="text-slate-600 dark:text-slate-300">
                Feld-Mapping (Struktur) und Werte-Mapping (z.B. alte Buchungskreise 0100 & 0200 zu Bukrs 1000).
              </p>
            </div>
            <div class="p-3 rounded-xl bg-slate-50 dark:bg-slate-800/40 border border-slate-200 dark:border-slate-700">
              <div class="font-bold text-blue-600 mb-1">Schritt 3: Simulation</div>
              <p class="text-slate-600 dark:text-slate-300">
                Validierung aller Datensätze gegen die Standard-Prüfungen der S/4HANA APIs ohne Festschreibung.
              </p>
            </div>
            <div class="p-3 rounded-xl bg-slate-50 dark:bg-slate-800/40 border border-slate-200 dark:border-slate-700">
              <div class="font-bold text-blue-600 mb-1">Schritt 4: Import</div>
              <p class="text-slate-600 dark:text-slate-300">
                Revisionssichere Verbuchung im Produktiv- oder Testmandanten über das SAP Migration Cockpit.
              </p>
            </div>
            <div class="p-3 rounded-xl bg-slate-50 dark:bg-slate-800/40 border border-slate-200 dark:border-slate-700">
              <div class="font-bold text-blue-600 mb-1">Schritt 5: Abstimmung</div>
              <p class="text-slate-600 dark:text-slate-300">
                SuSa-Abgleich, Saldenvortrag und formelles Freigabeprotokoll durch Wirtschaftsprüfer und TP-Leiter.
              </p>
            </div>
          </div>
        </div>

        <!-- Key Migration Objects Table -->
        <div class="bg-white dark:bg-slate-900 p-6 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm space-y-4">
          <h3 class="text-base font-bold text-slate-900 dark:text-white">Die wichtigsten Migrationsobjekte bei der SSB</h3>
          <div class="overflow-x-auto">
            <table class="w-full text-left text-xs border border-slate-200 dark:border-slate-700 rounded-xl overflow-hidden">
              <thead class="bg-slate-100 dark:bg-slate-800 text-slate-900 dark:text-white font-bold">
                <tr>
                  <th class="p-3 border-b dark:border-slate-700">Migrationsobjekt</th>
                  <th class="p-3 border-b dark:border-slate-700">Teilprojekt</th>
                  <th class="p-3 border-b dark:border-slate-700">Typ</th>
                  <th class="p-3 border-b dark:border-slate-700">Besonderheiten & Mapping-Herausforderungen</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-slate-200 dark:divide-slate-700 text-slate-600 dark:text-slate-300">
                <tr>
                  <td class="p-3 font-semibold text-slate-900 dark:text-white">Geschäftspartner (CVI)</td>
                  <td class="p-3">TP2 / TP3</td>
                  <td class="p-3"><span class="tag-badge bg-blue-100 text-blue-800">Stammdaten</span></td>
                  <td class="p-3">Zusammenführung von Kreditor (LFA1) und Debitor (KNA1) zum zentralen Business Partner. Bereinigung von Dubletten und IBAN-Validierung.</td>
                </tr>
                <tr>
                  <td class="p-3 font-semibold text-slate-900 dark:text-white">Sachkonten & Salden</td>
                  <td class="p-3">TP2 (Finance)</td>
                  <td class="p-3"><span class="tag-badge bg-purple-100 text-purple-800">Finanzen</span></td>
                  <td class="p-3">Neuer Kontenplan nach IFRS / HGB (Trennungsrechnung). Saldenübernahme zum Stichtag gegen Übernahmekonto 0,00 €.</td>
                </tr>
                <tr>
                  <td class="p-3 font-semibold text-slate-900 dark:text-white">Anlagenbuchhaltung (FI-AA)</td>
                  <td class="p-3">TP2 (Finance)</td>
                  <td class="p-3"><span class="tag-badge bg-purple-100 text-purple-800">Finanzen</span></td>
                  <td class="p-3">Historische Anschaffungskosten (AHK) und kumulierte Abschreibungen für Schienenfahrzeuge und Haltestelleninfrastruktur.</td>
                </tr>
                <tr>
                  <td class="p-3 font-semibold text-slate-900 dark:text-white">Offene Posten (OPs)</td>
                  <td class="p-3">TP2 (Finance)</td>
                  <td class="p-3"><span class="tag-badge bg-amber-100 text-amber-800">Bewegungsdaten</span></td>
                  <td class="p-3">Stichtagsbezogene Übernahme aller offenen Rechnungen von Lieferanten und Kunden zum Cutover-Wochenende.</td>
                </tr>
                <tr>
                  <td class="p-3 font-semibold text-slate-900 dark:text-white">Equipments & Techn. Plätze</td>
                  <td class="p-3">TP3 (Instandhaltung)</td>
                  <td class="p-3"><span class="tag-badge bg-emerald-100 text-emerald-800">Logistik/EAM</span></td>
                  <td class="p-3">Übernahme tausender Weichen, Schienenstränge, Signalanlagen und Stadtbahn-Wagen aus Altsystemen.</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Cutover-Phasen & Freeze-Strategie -->
        <div class="bg-white dark:bg-slate-900 p-6 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm space-y-4">
          <h3 class="text-base font-bold text-slate-900 dark:text-white flex items-center space-x-2">
            <span>⏱️</span>
            <span>Das Cutover-Drehbuch: Vom Freeze zum Go-Live</span>
          </h3>

          <div class="grid grid-cols-1 md:grid-cols-4 gap-3 text-xs">
            <div class="p-3.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/40">
              <div class="font-bold text-slate-900 dark:text-white mb-1">1. Pre-Cutover (T-4 Wochen)</div>
              <p class="text-slate-600 dark:text-slate-300">
                Generalprobe der Migration im Testsystem (Dress Rehearsal), Fixierung der Buchungs- und Berechtigungsstop-Termine (Freeze-Plan).
              </p>
            </div>
            <div class="p-3.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/40">
              <div class="font-bold text-slate-900 dark:text-white mb-1">2. Altsystem-Freeze (Freitag)</div>
              <p class="text-slate-600 dark:text-slate-300">
                Sperrung aller ECC 6.0 Buchungsperioden um 18:00 Uhr. Finale Delta-Extrakte für Finanzsalden, OPs und Instandhaltungsaufträge.
              </p>
            </div>
            <div class="p-3.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/40">
              <div class="font-bold text-slate-900 dark:text-white mb-1">3. Cutover Weekend (Sa/So)</div>
              <p class="text-slate-600 dark:text-slate-300">
                Batch-Lauf des Migration Cockpits. Centgenauer SuSa-Abgleich. Freigabe durch Wirtschaftsprüfer, Gesamt-PL Roland Nowak und IT-Leitung.
              </p>
            </div>
            <div class="p-3.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/40">
              <div class="font-bold text-slate-900 dark:text-white mb-1">4. Hypercare & Ramp-up (Montag)</div>
              <p class="text-slate-600 dark:text-slate-300">
                Produktivstart um 06:00 Uhr. Fiori-Launchpad Freigabe, Enable Now Web Assistant aktiv, tägliche Standups für Incident-Clearing in CALM.
              </p>
            </div>
          </div>
        </div>

      </div>
"""
