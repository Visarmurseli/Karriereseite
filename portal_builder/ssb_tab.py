# -*- coding: utf-8 -*-

def get_ssb_tab():
    return """
      <!-- ================= TAB 2: SSB AG – S/4HANA TRANSFORMATION (ATS KERNTHEMEN) ================= -->
      <div v-show="activeTab === 'ssb'" class="space-y-6">

        <!-- Header & Milestone Summary -->
        <div class="bg-[#141414] p-6 rounded-2xl border border-white/10 space-y-5">
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
            <div>
              <div class="flex flex-wrap items-center gap-2 mb-1.5">
                <span class="status-pill status-pill-blue">24 Monate (05/2024 – 04/2026)</span>
                <span class="status-pill status-pill-green">Explore-Phase abgeschlossen • SDD genehmigt</span>
              </div>
              <h2 class="text-xl sm:text-2xl font-extrabold text-white tracking-tight">
                🚆 Stuttgarter Straßenbahnen AG: SAP S/4HANA Transformation
              </h2>
              <p class="text-xs sm:text-sm text-[#8f8888] mt-1">
                Werkstudent IT-PMO &amp; Gesamtsteuerung (Teilprojekt 5) im Greenfield-Programm <strong>SAP4SSB</strong> (3.700+ Mitarbeitende, RISE with SAP Private Cloud).
              </p>
            </div>
          </div>

          <!-- 3 ATS Core Domains -->
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
            <div class="p-4 rounded-xl bg-white/5 border border-white/10 space-y-2">
              <div class="flex items-center justify-between">
                <span class="font-bold text-white text-sm">1. IT-PMO &amp; Governance (TP5)</span>
                <span class="status-pill status-pill-blue">Steuerung</span>
              </div>
              <ul class="text-[#c4bebe] space-y-1.5 list-disc list-inside leading-relaxed">
                <li><strong>Multiprojekt-Steuerung:</strong> Koordination über TP1 bis TP5 inklusive Meilenstein- &amp; Ressourcenplanung in MS Project.</li>
                <li><strong>C-Level Reporting:</strong> Vorbereitung von Steering-Board-Entscheidungen und Quality-Gate-Abnahmen bis Explore-Ende.</li>
                <li><strong>Vergabe &amp; Mitbestimmung:</strong> Begleitung von SektVO-Ausschreibungen und Betriebsvereinbarungs-Fahrplänen (UAT).</li>
              </ul>
            </div>

            <div class="p-4 rounded-xl bg-white/5 border border-white/10 space-y-2">
              <div class="flex items-center justify-between">
                <span class="font-bold text-white text-sm">2. Solution Design (FI/CO/MM)</span>
                <span class="status-pill status-pill-green">Blueprint</span>
              </div>
              <ul class="text-[#c4bebe] space-y-1.5 list-disc list-inside leading-relaxed">
                <li><strong>Greenfield &amp; Clean Core:</strong> Fit-to-Standard Moderation sowie Side-by-Side-Entkopplung über SAP BTP.</li>
                <li><strong>Finance Kernarchitektur:</strong> Universal Journal (ACDOCA), Trennungsrechnung (EU-VO 1370/2007), PSP-Steuerung &amp; Grants Management.</li>
                <li><strong>Prozessbreite:</strong> Beschaffung (MM), Mobile Instandhaltung (SAP SSAM) &amp; Schnittstellensteuerung.</li>
              </ul>
            </div>

            <div class="p-4 rounded-xl bg-white/5 border border-white/10 space-y-2">
              <div class="flex items-center justify-between">
                <span class="font-bold text-white text-sm">3. Toolchain &amp; Migration</span>
                <span class="status-pill status-pill-purple">Execution</span>
              </div>
              <ul class="text-[#c4bebe] space-y-1.5 list-disc list-inside leading-relaxed">
                <li><strong>SAP Cloud ALM:</strong> Etablierung für Anforderungs-, Test- &amp; Aufgabenmanagement inkl. eigenem „How2Handle“-Leitfaden.</li>
                <li><strong>SAP Signavio &amp; Enable Now:</strong> BPMN 2.0 Sollprozess-Governance und Übergabekonzept für Key-User-Enablement.</li>
                <li><strong>Datenmigration:</strong> Vorbereitung über SAP Migration Cockpit (LTMC), CVI (Business Partner) &amp; Eröffnungsbilanz-Abgleich.</li>
              </ul>
            </div>
          </div>

          <!-- Compact TP1-TP5 Strip -->
          <div class="p-4 rounded-xl bg-black/40 border border-white/10 space-y-2.5">
            <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
              <span class="text-xs font-bold text-white">Programmstruktur SAP4SSB (5 Teilprojekte unter zentraler PMO-Klammer)</span>
              <span class="text-[11px] text-[#8f8888]">Partner-Ökosystem: Nagarro, Axians, Evora, apsolut</span>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-5 gap-2 text-[11px]">
              <div class="p-2.5 rounded-lg bg-white/5 border border-white/10">
                <div class="font-bold text-white">TP1 • Change</div>
                <div class="text-[#8f8888] mt-0.5">Enable Now, Key-User &amp; Betriebsrat</div>
              </div>
              <div class="p-2.5 rounded-lg bg-white/5 border border-white/10">
                <div class="font-bold text-white">TP2 • Finanzen</div>
                <div class="text-[#8f8888] mt-0.5">FI/CO, ACDOCA, Trennungsrechnung</div>
              </div>
              <div class="p-2.5 rounded-lg bg-white/5 border border-white/10">
                <div class="font-bold text-white">TP3 • Technik</div>
                <div class="text-[#8f8888] mt-0.5">Instandhaltung (SAP SSAM) &amp; MM</div>
              </div>
              <div class="p-2.5 rounded-lg bg-white/5 border border-white/10">
                <div class="font-bold text-white">TP4 • HR &amp; IT</div>
                <div class="text-[#8f8888] mt-0.5">Systemlandschaft, BTP &amp; HR-Systeme</div>
              </div>
              <div class="p-2.5 rounded-lg border-2 border-[#bf262e] bg-[#bf262e]/10">
                <div class="font-bold text-[#f87171]">TP5 • PMO (Fokus)</div>
                <div class="text-[#c4bebe] mt-0.5">Gesamtsteuerung, Governance &amp; CALM</div>
              </div>
            </div>
          </div>
        </div>

        <!-- Interaktives SAP Activate Phasen-Cockpit -->
        <div class="bg-[#141414] p-6 rounded-2xl border border-white/10 space-y-4">
          <div class="flex flex-col md:flex-row md:items-center justify-between gap-3">
            <div>
              <h3 class="text-base font-bold text-white flex items-center gap-2">
                <span>🎯</span>
                <span>Interaktives SAP Activate Phasen-Cockpit</span>
              </h3>
              <p class="text-xs text-[#8f8888]">Methodische Einordnung meiner 24-monatigen Praxisleistung bis zum Explore-Abschluss (Solution Design Document genehmigt).</p>
            </div>
            
            <div class="flex items-center space-x-1 bg-white/5 p-1 rounded-xl text-xs overflow-x-auto no-scrollbar border border-white/10">
              <button 
                @click="wbsFilter = 'all'" 
                :class="['px-2.5 py-1 rounded-lg font-medium transition', wbsFilter === 'all' ? 'bg-[#bf262e] text-white' : 'text-[#8f8888] hover:text-white']"
              >Alle (6 Phasen)</button>
              <button 
                @click="wbsFilter = 'explore'" 
                :class="['px-2.5 py-1 rounded-lg font-medium transition', wbsFilter === 'explore' ? 'bg-[#bf262e] text-white' : 'text-[#8f8888] hover:text-white']"
              >Visars Fokus (Discover–Explore)</button>
              <button 
                @click="wbsFilter = 'realize'" 
                :class="['px-2.5 py-1 rounded-lg font-medium transition', wbsFilter === 'realize' ? 'bg-[#bf262e] text-white' : 'text-[#8f8888] hover:text-white']"
              >Ausblick (Realize–Run)</button>
            </div>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3 pt-1">
            <div 
              v-for="p in filteredWbsProjects" 
              :key="p.id"
              class="p-4 rounded-xl border border-white/10 bg-white/5 space-y-2"
            >
              <div class="flex items-center justify-between">
                <span class="font-bold text-xs text-[#f87171]">{{ p.id }}</span>
                <span class="status-pill status-pill-blue">{{ p.tag }}</span>
              </div>
              <div>
                <h4 class="text-xs font-bold text-white">{{ p.title }}</h4>
                <div class="text-[11px] text-[#8f8888] mt-0.5">{{ p.wbs }}</div>
              </div>
              <div class="w-full bg-white/10 h-1.5 rounded-full overflow-hidden">
                <div class="bg-[#bf262e] h-1.5 rounded-full transition-all duration-500" :style="{ width: p.progress + '%' }"></div>
              </div>
              <p class="text-[11px] text-[#c4bebe] leading-snug">{{ p.details }}</p>
            </div>
          </div>

          <div class="pt-2 border-t border-white/10 flex flex-wrap items-center justify-between gap-2 text-xs">
            <span class="text-[#8f8888]">Tiefe Details zu Greenfield, LTMC/0,00 € Abgleich &amp; Schnittstellen (PATRIS, xSuite, d.velop):</span>
            <button @click="selectTab('faq')" class="px-3 py-1.5 rounded-lg bg-[#bf262e]/15 text-[#f87171] border border-[#bf262e]/30 font-semibold hover:bg-[#bf262e] hover:text-white transition">
              ❓ Technische Details in den FAQ öffnen ➔
            </button>
          </div>
        </div>

      </div>
"""
