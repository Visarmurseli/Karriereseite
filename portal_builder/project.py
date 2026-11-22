# -*- coding: utf-8 -*-

def get_project():
    return """
      <!-- ================= TAB 3: DAS PROJEKT SAP4SSB 360° ================= -->
      <div v-show="activeTab === 'project'" class="space-y-6">
        <div class="bg-white dark:bg-slate-900 p-6 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm space-y-4">
          <div class="flex items-center justify-between">
            <div>
              <h3 class="text-lg font-bold text-slate-900 dark:text-white">Das Großprojekt: SAP4SSB Greenfield Implementation</h3>
              <p class="text-xs text-slate-500">Das Herzstück deiner Praxiserfahrung bei der Stuttgarter Straßenbahnen AG</p>
            </div>
            <span class="tag-badge bg-blue-100 text-blue-800 dark:bg-blue-900/60 dark:text-blue-300">RISE with SAP Private Cloud</span>
          </div>

          <!-- Why Greenfield & Clean Core -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 pt-2">
            <div class="p-4 rounded-xl bg-slate-50 dark:bg-slate-800/50 border border-slate-200 dark:border-slate-700">
              <h4 class="text-sm font-bold text-slate-900 dark:text-white flex items-center space-x-2">
                <span>🌱</span>
                <span>Warum Greenfield und kein Brownfield?</span>
              </h4>
              <ul class="text-xs text-slate-600 dark:text-slate-300 mt-2 space-y-1.5 list-disc list-inside">
                <li><strong>Historischer Monolith:</strong> Das bestehende SAP ECC 6.0 war über 20 Jahre durch unzählige Z-Modifikationen, User-Exits und proprietäre Tabellen verbaut.</li>
                <li><strong>Mangelnde Update-Fähigkeit:</strong> Ein direktes System-Upgrade (Brownfield) hätte Altlasten, veraltete Datenstrukturen und fehlerhafte Berechtigungen mitgeschleift.</li>
                <li><strong>Neustart nach Best Practice:</strong> Greenfield ermöglichte die strikte Rückkehr zum SAP-Standard via Fit-to-Standard Workshops mit Nagarro und Evora.</li>
              </ul>
            </div>

            <div class="p-4 rounded-xl bg-slate-50 dark:bg-slate-800/50 border border-slate-200 dark:border-slate-700">
              <h4 class="text-sm font-bold text-slate-900 dark:text-white flex items-center space-x-2">
                <span>💎</span>
                <span>Das Clean Core Paradigma</span>
              </h4>
              <ul class="text-xs text-slate-600 dark:text-slate-300 mt-2 space-y-1.5 list-disc list-inside">
                <li><strong>Keine Core-Modifikationen:</strong> Der S/4HANA Kern bleibt upgrade-sicher und cloud-kompatibel.</li>
                <li><strong>On-Stack Extensibility:</strong> Kundeneigene Logik im Kern erfolgt ausschließlich über freigegebene Schnittstellen (ABAP Cloud, RESTful Application Programming / RAP).</li>
                <li><strong>Side-by-Side auf der SAP BTP:</strong> Komplexe Individual-Applikationen und Schnittstellen-Orchestrierungen werden auf die SAP Business Technology Platform ausgelagert.</li>
              </ul>
            </div>
          </div>
        </div>

        <!-- Die 5 Teilprojekte (TP1 bis TP5) -->
        <div class="bg-white dark:bg-slate-900 p-6 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm space-y-4">
          <h3 class="text-base font-bold text-slate-900 dark:text-white">Die 5 Teilprojekte (TP1 bis TP5) & Stakeholder-Matrix</h3>
          <div class="grid grid-cols-1 md:grid-cols-5 gap-3">
            
            <!-- TP1 -->
            <div class="p-3.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/40 space-y-2">
              <div class="flex items-center justify-between">
                <span class="font-bold text-xs text-blue-600">TP1</span>
                <span class="text-[10px] bg-blue-100 text-blue-800 dark:bg-blue-900/60 dark:text-blue-300 px-1.5 py-0.5 rounded">Change & Enablement</span>
              </div>
              <div class="text-xs font-semibold text-slate-900 dark:text-white">Change Management & Academy</div>
              <div class="text-[11px] text-slate-500">Leitung: Cichon / Göhring / Sarah Lozano</div>
              <p class="text-[11px] text-slate-600 dark:text-slate-300">
                Kultureller Wandel, Betriebsrat-Einbindung, Kommunikation an 3.700 MA, SAP Enable Now Rollout mit UB AC (Personalentwicklung).
              </p>
            </div>

            <!-- TP2 -->
            <div class="p-3.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/40 space-y-2">
              <div class="flex items-center justify-between">
                <span class="font-bold text-xs text-blue-600">TP2</span>
                <span class="text-[10px] bg-emerald-100 text-emerald-800 dark:bg-emerald-900/60 dark:text-emerald-300 px-1.5 py-0.5 rounded">Kaufmännisch</span>
              </div>
              <div class="text-xs font-semibold text-slate-900 dark:text-white">Finance & Controlling</div>
              <div class="text-[11px] text-slate-500">Leitung: Wimpff / Partner: Nagarro ES</div>
              <p class="text-[11px] text-slate-600 dark:text-slate-300">
                S/4HANA FI/CO, Trennungsrechnung (PBV/ÖPNV), Universal Journal (ACDOCA), New Asset Accounting (FI-AA), xSuite Rechnungswesen.
              </p>
            </div>

            <!-- TP3 -->
            <div class="p-3.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/40 space-y-2">
              <div class="flex items-center justify-between">
                <span class="font-bold text-xs text-blue-600">TP3</span>
                <span class="text-[10px] bg-amber-100 text-amber-800 dark:bg-amber-900/60 dark:text-amber-300 px-1.5 py-0.5 rounded">Technik</span>
              </div>
              <div class="text-xs font-semibold text-slate-900 dark:text-white">Instandhaltung & Logistik</div>
              <div class="text-[11px] text-slate-500">Leitung: Neifer / Partner: Evora IT</div>
              <p class="text-[11px] text-slate-600 dark:text-slate-300">
                Instandhaltung der Stadtbahnen, Busse und Schieneninfrastruktur (SAP PM / EAM), mobile Instandhaltung mit Evora, Materialwirtschaft (MM).
              </p>
            </div>

            <!-- TP4 -->
            <div class="p-3.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/40 space-y-2">
              <div class="flex items-center justify-between">
                <span class="font-bold text-xs text-blue-600">TP4</span>
                <span class="text-[10px] bg-purple-100 text-purple-800 dark:bg-purple-900/60 dark:text-purple-300 px-1.5 py-0.5 rounded">Personal</span>
              </div>
              <div class="text-xs font-semibold text-slate-900 dark:text-white">HR & Nachfolgesystem</div>
              <div class="text-[11px] text-slate-500">Leitung: Tielesch / UB P</div>
              <p class="text-[11px] text-slate-600 dark:text-slate-300">
                Evaluation von SAP SuccessFactors vs. Best-of-Breed HR-Lösungen, Digitale Personalakte (d.velop), Entgeltabrechnung.
              </p>
            </div>

            <!-- TP5 -->
            <div class="p-3.5 rounded-xl border-2 border-yellow-400 dark:border-yellow-500 bg-yellow-50/50 dark:bg-yellow-950/20 space-y-2 shadow-sm">
              <div class="flex items-center justify-between">
                <span class="font-bold text-xs text-slate-900 dark:text-yellow-400">TP5 (DEIN HOME)</span>
                <span class="text-[10px] bg-yellow-400 text-slate-950 font-bold px-1.5 py-0.5 rounded">IT-PMO & Architektur</span>
              </div>
              <div class="text-xs font-bold text-slate-900 dark:text-white">Gesamtsteuerung & Basis</div>
              <div class="text-[11px] text-slate-600 dark:text-slate-400">Gesamt-PL: Roland Nowak / IT-Leitung: Dietmar Fillinger</div>
              <p class="text-[11px] text-slate-700 dark:text-slate-200 font-medium">
                Multiprojekt-Governance, Tool-Stack (CALM, Signavio), Schnittstellenarchitektur, Basisbetreuung mit Axians, Lenkungsausschuss-Vorbereitung.
              </p>
            </div>

          </div>
        </div>

        <!-- Scope & Third-Party System Landscape -->
        <div class="bg-white dark:bg-slate-900 p-6 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm space-y-4">
          <h3 class="text-base font-bold text-slate-900 dark:text-white">Die komplexe Drittsystem-Landschaft der SSB</h3>
          <p class="text-xs text-slate-500">Schnittstellen und Integrationsmuster, die du aus dem Lösungsdesign kennst</p>
          <div class="grid grid-cols-2 md:grid-cols-4 gap-3 text-xs">
            <div class="p-3 rounded-lg border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/30">
              <div class="font-bold text-slate-900 dark:text-white">xSuite</div>
              <div class="text-slate-500 text-[11px]">Rechnungseingang & OCR</div>
              <div class="text-slate-600 dark:text-slate-300 mt-1 text-[11px]">Automatisierte Rechnungsverarbeitung, Freigabeworkflows, Anbindung an S/4-FI.</div>
            </div>
            <div class="p-3 rounded-lg border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/30">
              <div class="font-bold text-slate-900 dark:text-white">d.velop</div>
              <div class="text-slate-500 text-[11px]">DMS & Digitale Akten</div>
              <div class="text-slate-600 dark:text-slate-300 mt-1 text-[11px]">Archivierung von Belegen, Anbindung über ArchiveLink und CMIS-Schnittstellen.</div>
            </div>
            <div class="p-3 rounded-lg border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/30">
              <div class="font-bold text-slate-900 dark:text-white">PATRIS / iTWO / EDM</div>
              <div class="text-slate-500 text-[11px]">Branchenspezifisch ÖPNV</div>
              <div class="text-slate-600 dark:text-slate-300 mt-1 text-[11px]">Abrechnung Fahrgeldeinnahmen, Bauprojektmanagement und Energiedatenmanagement.</div>
            </div>
            <div class="p-3 rounded-lg border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/30">
              <div class="font-bold text-slate-900 dark:text-white">Axians ES4 / ADS</div>
              <div class="text-slate-500 text-[11px]">Infrastruktur & Cloud Basis</div>
              <div class="text-slate-600 dark:text-slate-300 mt-1 text-[11px]">ES4 Testmandanten (M300/M100), Adobe Document Services, Single Sign-On (SSO).</div>
            </div>
          </div>
        </div>
      </div>
"""
