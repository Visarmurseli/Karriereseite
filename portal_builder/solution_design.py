# -*- coding: utf-8 -*-

def get_solution_design():
    return """
      <!-- ================= TAB 4: SOLUTION DESIGN DEEP-DIVE ================= -->
      <div v-show="activeTab === 'solution_design'" class="space-y-6">
        
        <div class="bg-[#141414] p-6 rounded-2xl border border-white/10 shadow-sm space-y-4">
          <div class="flex items-center justify-between">
            <div>
              <h3 class="text-lg font-bold text-white">Solution Design Deep-Dive: Kaufmännische Prozesse (TP2)</h3>
              <p class="text-xs text-[#8f8888]">Detaillierte Analyse des 82.000 Zeichen starken Lösungsdesign-Dokuments (Nagarro & SSB)</p>
            </div>
            <span class="tag-badge bg-emerald-500/20 text-emerald-300 border border-emerald-500/40">Finance & Controlling Blueprint</span>
          </div>

          <!-- Enterprise Structure & Core Principles -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 pt-2">
            
            <!-- Buchungskreise & Controllingbereich -->
            <div class="p-4 rounded-xl bg-white/5 border border-white/10 space-y-2 hover:border-[#bf262e]/30 transition">
              <h4 class="text-sm font-bold text-white flex items-center space-x-2">
                <span>🏢</span>
                <span>Organisationsstruktur (Bukrs & Kokrs)</span>
              </h4>
              <ul class="text-xs text-[#c4bebe] space-y-2">
                <li>
                  <strong class="text-white">Buchungskreise (Bukrs):</strong>
                  <ul class="pl-4 list-disc mt-1 space-y-0.5">
                    <li><code class="text-[#fecdd3]">Bukrs 1000</code>: Stuttgarter Straßenbahnen AG (ÖPNV, Muttergesellschaft).</li>
                    <li><code class="text-[#fecdd3]">Bukrs 3000</code>: SSB Reisen GmbH (Tourismus & gewerbliche Verkehre).</li>
                  </ul>
                </li>
                <li>
                  <strong class="text-white">Controllingbereiche (Kokrs):</strong>
                  <div class="mt-0.5">Zuordnung 1:1 zu Buchungskreisen (Kokrs 1000 und Kokrs 3000), um eine strikte gesellschaftsrechtliche Trennung der Deckungsbeiträge zu garantieren.</div>
                </li>
                <li>
                  <strong class="text-white">Währung & Geschäftsjahr:</strong>
                  <div class="mt-0.5">Buchungskreiswährung EUR, Geschäftsjahr entspricht dem Kalenderjahr (K4: 12 Perioden + 4 Sonderperioden).</div>
                </li>
              </ul>
            </div>

            <!-- Trennungsrechnung & PSP-Dogma -->
            <div class="p-4 rounded-xl bg-white/5 border border-white/10 space-y-2 hover:border-[#bf262e]/30 transition">
              <h4 class="text-sm font-bold text-white flex items-center space-x-2">
                <span>⚖️</span>
                <span>Trennungsrechnung & Das PSP-Dogma</span>
              </h4>
              <ul class="text-xs text-[#c4bebe] space-y-2">
                <li>
                  <strong class="text-white">Gesetzliche Trennungsrechnung (EU-VO 1370/2007):</strong>
                  <div class="mt-0.5">Als subventioniertes Verkehrsunternehmen muss die SSB gemeinwirtschaftliche Verkehrsleistungen (PBV) strikt von gewerblichen Tätigkeiten trennen. Quersubventionierungen sind beihilferechtlich verboten!</div>
                </li>
                <li>
                  <strong class="text-white">Profit Center als Schattenobjekte:</strong>
                  <div class="mt-0.5">Profit Center werden im Zielsystem primär als <em>Schattenobjekte</em> geführt, um die Segmentberichterstattung und Trennungsrechnung zu sichern – nicht zur operativen Kostenstellensteuerung.</div>
                </li>
                <li>
                  <strong class="text-white">Abschaffung der Innenaufträge:</strong>
                  <div class="mt-0.5 font-medium text-[#f87171]">Strategische Vereinheitlichung: Klassische Innenaufträge (CO-OM-OPA) werden komplett abgeschafft! Sämtliche Investitionen, Projekte und Kostensammler werden über PSP-Elemente (Projektsystem / PS) gesteuert.</div>
                </li>
              </ul>
            </div>

          </div>
        </div>

        <!-- Universal Journal & Ledger Architecture -->
        <div class="bg-[#141414] p-6 rounded-2xl border border-white/10 shadow-sm space-y-4">
          <h3 class="text-base font-bold text-white flex items-center space-x-2">
            <span>📊</span>
            <span>Universal Journal (ACDOCA) & Multi-Ledger Architektur</span>
          </h3>

          <div class="grid grid-cols-1 md:grid-cols-3 gap-3 text-xs">
            <div class="p-3.5 rounded-xl border border-white/10 bg-white/5 space-y-1.5 hover:border-[#bf262e]/30 transition">
              <div class="font-bold text-[#f87171]">1. Single Source of Truth (ACDOCA)</div>
              <p class="text-[#c4bebe] leading-relaxed">
                In SAP ECC 6.0 gab es getrennte Tabellen für Hauptbuch (BKPF/BSEG), Anlagen (ANEP), Controlling (COEP) und Material (MLIT). In S/4HANA fließen alle Finanz- und Controllingbuchungen in eine einzige Tabelle: <strong>ACDOCA</strong>. Sekundärkostenarten sind nun vollwertige Sachkonten.
              </p>
            </div>

            <div class="p-3.5 rounded-xl border border-white/10 bg-white/5 space-y-1.5 hover:border-[#bf262e]/30 transition">
              <div class="font-bold text-purple-400">2. Ledger-Ansatz (Multi-GAAP)</div>
              <p class="text-[#c4bebe] leading-relaxed">
                <strong>Leading Ledger (0L):</strong> Führt den handelsrechtlichen Abschluss nach HGB und Steuerrecht.<br>
                <strong>Non-Leading Ledger (2L):</strong> Parallelführung für IFRS-Konzernberichterstattung und kalkulatorische Abschreibungen, besonders relevant für Schienenfahrzeuge und Gleisinfrastruktur.
              </p>
            </div>

            <div class="p-3.5 rounded-xl border border-white/10 bg-white/5 space-y-1.5 hover:border-[#bf262e]/30 transition">
              <div class="font-bold text-emerald-400">3. New Asset Accounting (FI-AA)</div>
              <p class="text-[#c4bebe] leading-relaxed">
                Anlagenbuchhaltung bucht in Echtzeit in alle relevanten Ledger. Delta-Buchungsläufe gehören der Vergangenheit an. Statistische Anlagen im Bau (AiB) werden direkt mit PSP-Elementen gekoppelt und bei Fertigstellung per Endabrechnung aktiviert.
              </p>
            </div>
          </div>
        </div>

        <!-- Business Partner & Customer Vendor Integration (CVI) -->
        <div class="bg-[#141414] p-6 rounded-2xl border border-white/10 shadow-sm space-y-4">
          <h3 class="text-base font-bold text-white flex items-center space-x-2">
            <span>👥</span>
            <span>Business Partner (CVI) & Stammdaten-Harmonisierung</span>
          </h3>
          <p class="text-xs text-[#8f8888]">Zusammenführung historischer Stammdaten im Rahmen des Greenfield Scopes</p>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
            <div class="p-4 rounded-xl bg-white/5 border border-white/10 space-y-2 hover:border-[#bf262e]/30 transition">
              <div class="font-bold text-amber-400 text-xs uppercase tracking-wider">Das CVI-Prinzip</div>
              <p class="text-[#c4bebe] leading-relaxed">
                In SAP ECC 6.0 existierten Debitoren (Tabelle <code>KNA1</code>) und Kreditoren (Tabelle <code>LFA1</code>) getrennt nebeneinander. War ein Zulieferer (z.B. Siemens Mobility) gleichzeitig Kunde für Werkstattleistungen, gab es zwei Stammsätze ohne automatische Verknüpfung.
              </p>
              <p class="text-[#c4bebe] leading-relaxed">
                In S/4HANA ist der <strong>Business Partner (BP)</strong> das zentrale führende Objekt (Tabelle <code>BUT000</code>). Ein BP erhält Rollen:
                <br>• <code>FLCU00 / FLCU01</code>: Debitor (FI & Vertrieb)
                <br>• <code>FLVN00 / FLVN01</code>: Kreditor (FI & Einkauf)
              </p>
            </div>

            <div class="p-4 rounded-xl bg-white/5 border border-white/10 space-y-2 hover:border-[#bf262e]/30 transition">
              <div class="font-bold text-[#f87171] text-xs uppercase tracking-wider">Konsolidierungshebel bei der SSB</div>
              <ul class="text-[#c4bebe] space-y-1.5 list-disc list-inside">
                <li><strong class="text-white">Dublettenbereinigung:</strong> Hunderte historisch doppelt angelegte Handwerker und Lieferanten wurden vor der Migration zusammengeführt.</li>
                <li><strong class="text-white">Nummernkreis-Harmonisierung:</strong> Festlegung gleicher Nummern für Business Partner, Debitor und Kreditor zur Vermeidung von Verwirrung in den Fachabteilungen.</li>
                <li><strong class="text-white">Bankdaten-Validierung:</strong> IBAN- und BIC-Prüfung über SEPA-Regeln direkt in den Staging-Tabellen vor dem S/4HANA Import.</li>
              </ul>
            </div>
          </div>
        </div>

        <!-- Materialwirtschaft (MM) & Bestandsführung (MATDOC) -->
        <div class="bg-[#141414] p-6 rounded-2xl border border-white/10 shadow-sm space-y-4">
          <div class="flex items-center justify-between">
            <h3 class="text-base font-bold text-white flex items-center space-x-2">
              <span>📦</span>
              <span>Materialwirtschaft (MM): Operative Beschaffung & Bestandsführung (MATDOC)</span>
            </h3>
            <span class="tag-badge bg-amber-500/20 text-amber-300 border border-amber-500/40">Fit-to-Standard Scope</span>
          </div>
          <p class="text-xs text-[#8f8888]">Ergebnisse der BPD-Workshops 1–3 mit Nagarro: Ablösung historischer Transaktionen und SektVO-Vergabekonformität.</p>

          <div class="grid grid-cols-1 md:grid-cols-3 gap-3 text-xs">
            <div class="p-3.5 rounded-xl border border-white/10 bg-white/5 space-y-1.5 hover:border-[#bf262e]/30 transition">
              <div class="font-bold text-amber-400">1. Bestellmanagement & Preisanfragen</div>
              <ul class="text-[#c4bebe] space-y-1 list-disc list-inside">
                <li><strong class="text-white">1XF (Request for Price):</strong> Preisanfragen & strukturierter Angebotsvergleich.</li>
                <li><strong class="text-white">BMD (Purchase Contract):</strong> Rahmen- und Mengenkontrakte für DT8-Ersatzteile.</li>
                <li><strong class="text-white">2TW (Complementary Functions):</strong> Chargenverwaltung & Herstellerteilenummern (HTN).</li>
              </ul>
            </div>

            <div class="p-3.5 rounded-xl border border-white/10 bg-white/5 space-y-1.5 hover:border-[#bf262e]/30 transition">
              <div class="font-bold text-[#f87171]">2. Lieferpläne & Dienstleistungen</div>
              <ul class="text-[#c4bebe] space-y-1 list-disc list-inside">
                <li><strong class="text-white">BMR (Scheduling Agreements):</strong> Just-in-Time-Lieferpläne für die Hauptwerkstatt Möhringen.</li>
                <li><strong class="text-white">BMY (Subcontracting):</strong> Lohnbearbeitung & Fremdaufarbeitung von Fahrgestellen.</li>
                <li><strong class="text-white">22Z (Procurement of Services):</strong> Dienstleistungsbestellungen mit elektronischen SES.</li>
              </ul>
            </div>

            <div class="p-3.5 rounded-xl border border-white/10 bg-white/5 space-y-1.5 hover:border-[#bf262e]/30 transition">
              <div class="font-bold text-emerald-400">3. S/4HANA Simplifications (MATDOC)</div>
              <ul class="text-[#c4bebe] space-y-1 list-disc list-inside">
                <li><strong class="text-white">MATDOC ersetzt MKPF/MSEG:</strong> Echtzeit-Bestandsführung ohne Lichtsperren (Note 2206980).</li>
                <li><strong class="text-white">MIGO-Standardisierung:</strong> Decommissioning historischer MB-Transaktionen (Note 1804812).</li>
                <li><strong class="text-white">ME21N / ME51N:</strong> Ablösung alter ME21/ME51 Pflegedialoge (Note 1803189).</li>
              </ul>
            </div>
          </div>
        </div>

        <!-- Real Estate Management (RE-FX) & Liegenschaften -->
        <div class="bg-[#141414] p-6 rounded-2xl border border-white/10 shadow-sm space-y-4">
          <div class="flex items-center justify-between">
            <h3 class="text-base font-bold text-white flex items-center space-x-2">
              <span>🏢</span>
              <span>Real Estate Management (RE-FX): Liegenschaften, Mietobjekte & Erbbaurechte</span>
            </h3>
            <span class="tag-badge bg-purple-500/20 text-purple-300 border border-purple-500/40">Solution Design WorXX</span>
          </div>
          <p class="text-xs text-[#8f8888]">Konzeption von Lösungsarchitekt Michael Gehrung: Betreuung von Betriebshöfen, Haltestellen und gewerblichen Mietflächen.</p>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
            <div class="p-4 rounded-xl bg-white/5 border border-white/10 space-y-2 hover:border-[#bf262e]/30 transition">
              <div class="font-bold text-purple-400 uppercase tracking-wider">Zweistufige Objekthierarchie</div>
              <ul class="text-[#c4bebe] space-y-1.5 list-disc list-inside">
                <li><strong class="text-white">Wirtschaftseinheit (<code>VIBDCO</code>):</strong> Oberste Klammer für Liegenschaftskomplexe (z.B. Betriebshof Möhringen mit allen Hallen).</li>
                <li><strong class="text-white">Grundstücke (<code>VIBDPR</code>) & Gebäude (<code>VIBDBU</code>):</strong> Katasteramtliche Flurstücke und physische Baukörper.</li>
                <li><strong class="text-white">Mietobjekte (<code>VIBDPO</code>):</strong> Räume und Gewerbeflächen in Stadtbahnstationen (Kioske, Bäckereien).</li>
                <li><strong class="text-white">Immobilienverträge (<code>VICNCN</code>):</strong> Pachten, Erbbaurechte und gewerbliche Mietverträge mit Wertsicherungsklauseln (VPI).</li>
              </ul>
            </div>

            <div class="p-4 rounded-xl bg-white/5 border border-white/10 space-y-2 hover:border-[#bf262e]/30 transition">
              <div class="font-bold text-emerald-400 uppercase tracking-wider">Integration & Trennungsrechnung (EU 1370/2007)</div>
              <ul class="text-[#c4bebe] space-y-1.5 list-disc list-inside">
                <li><strong class="text-white">Regulatorische Trennung:</strong> Erlöse aus Kioskvermietungen werden über separate Segmente im Universal Journal (<code>ACDOCA</code>) streng von subventionierten Verkehrsflächen getrennt.</li>
                <li><strong class="text-white">Anlagenbuchhaltung (FI-AA):</strong> Gebäude und Grundstücke sind 1:1 mit den Anlagennummern (<code>ANLA</code>) zur parallelen HGB/Steuer-Abschreibung verknüpft.</li>
                <li><strong class="text-white">Instandhaltung (PM):</strong> Aufzüge und Fahrtreppen sind als Technische Plätze (<code>IFLOT</code>) geführt, Reparaturkosten fließen direkt in die Liegenschaftskalkulation.</li>
              </ul>
            </div>
          </div>
        </div>

        <!-- WRICEF & Non-SAP Subsysteme Schnittstellenmatrix -->
        <div class="bg-[#141414] p-6 rounded-2xl border border-white/10 shadow-sm space-y-4">
          <div class="flex items-center justify-between">
            <h3 class="text-base font-bold text-white flex items-center space-x-2">
              <span>🔌</span>
              <span>WRICEF & Non-SAP Schnittstellenmatrix (Entkopplung via BTP)</span>
            </h3>
            <span class="tag-badge bg-[#bf262e]/20 text-[#f87171] border border-[#bf262e]/40">Integration Suite</span>
          </div>
          <p class="text-xs text-[#8f8888]">Architektur zur Entkopplung operativer Massendaten von den Kern-Finanztabellen.</p>

          <div class="grid grid-cols-1 md:grid-cols-3 gap-3 text-xs">
            <div class="p-3.5 rounded-xl border border-white/10 bg-white/5 space-y-1.5 hover:border-[#bf262e]/30 transition">
              <div class="font-bold text-[#f87171]">PATRIS (Vertrieb & Ticketing)</div>
              <p class="text-[#c4bebe] leading-relaxed">
                Über 500.000 monatliche Fahrkartenverkäufe werden im Non-SAP System PATRIS aggregiert und als verdichtete Buchungsläufe nach S/4HANA SD/FI übertragen.
              </p>
            </div>

            <div class="p-3.5 rounded-xl border border-white/10 bg-white/5 space-y-1.5 hover:border-[#bf262e]/30 transition">
              <div class="font-bold text-purple-400">xSuite & d.velop (ECM)</div>
              <p class="text-[#c4bebe] leading-relaxed">
                Automatisierte OCR-Rechnungsverarbeitung mit 3-Wege-Match gegen Bestelldaten (<code>EKKO</code>) und Wareneingänge (<code>MATDOC</code>) zur revisionssicheren Ablage.
              </p>
            </div>

            <div class="p-3.5 rounded-xl border border-white/10 bg-white/5 space-y-1.5 hover:border-[#bf262e]/30 transition">
              <div class="font-bold text-emerald-400">Multi-Bank-Connectivity (MBC)</div>
              <p class="text-[#c4bebe] leading-relaxed">
                Vollautomatischer Zahlungsverkehr via EBICS/SWIFT (<code>pain.001</code> / <code>pain.008</code>) und Einlesen elektronischer CAMT.053-Kontoauszüge.
              </p>
            </div>
          </div>
        </div>

      </div>
"""
