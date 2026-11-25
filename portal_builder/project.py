# -*- coding: utf-8 -*-

def get_project():
    return """
      <!-- ================= TAB 3: DAS PROJEKT SAP4SSB 360° ================= -->
      <div v-show="activeTab === 'project'" class="space-y-6">
        <div class="bg-[#141414] p-6 rounded-2xl border border-white/10 shadow-sm space-y-4">
          <div class="flex items-center justify-between">
            <div>
              <h3 class="text-lg font-bold text-white">Das Großprojekt: SAP4SSB Greenfield Implementation</h3>
              <p class="text-xs text-[#8f8888]">Das Herzstück deiner Praxiserfahrung bei der Stuttgarter Straßenbahnen AG</p>
            </div>
            <span class="tag-badge bg-[#bf262e]/20 text-[#f87171] border border-[#bf262e]/40">RISE with SAP Private Cloud</span>
          </div>

          <!-- Stand bei Austritt: Meilenstein Ende Explore-Phase & SDD-Abnahme -->
          <div class="p-5 rounded-xl bg-gradient-to-r from-[#1e1516] via-[#161616] to-[#121c15] border border-emerald-500/30 space-y-3">
            <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-white/10 pb-3">
              <div class="flex items-center space-x-2.5">
                <span class="text-xl">🏁</span>
                <div>
                  <h4 class="text-sm font-bold text-white flex items-center gap-2">
                    <span>Projektstand bei Austritt: Explore-Phase erfolgreich abgeschlossen</span>
                    <span class="px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 text-[10px] font-bold">Meilenstein erreicht</span>
                  </h4>
                  <p class="text-[11px] text-[#8f8888]">Stuttgarter Straßenbahnen AG (SSB AG) • Programm SAP4SSB • Werkstudententätigkeit bis April 2026</p>
                </div>
              </div>
              <div class="text-xs text-right">
                <span class="text-[#8f8888]">Status:</span>
                <span class="text-emerald-400 font-bold ml-1">SDD vollständig genehmigt</span>
              </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs pt-1">
              <div class="space-y-1.5">
                <div class="font-bold text-white flex items-center space-x-1.5">
                  <span class="text-emerald-400">✓</span>
                  <span>Erreichte Ergebnisse (Ende Explore-Phase):</span>
                </div>
                <ul class="text-[#c4bebe] space-y-1 list-disc list-inside text-[11px] leading-relaxed">
                  <li><strong>Fit-to-Standard abgeschlossen:</strong> Sämtliche Fachworkshops in TP1 bis TP5 erfolgreich moderiert und dokumentiert.</li>
                  <li><strong>Solution Design Document (SDD):</strong> Kaufmännische Kernprozesse (FI/CO, MM, PM, Trennungsrechnung, ACDOCA) vollständig finalisiert und durch den Lenkungsausschuss freigegeben.</li>
                  <li><strong>Prozessmodellierung:</strong> Solldokumentation in SAP Signavio (BPMN 2.0) als verbindliche Implementierungsgrundlage eingefroren.</li>
                  <li><strong>Tool-Governance:</strong> SAP Cloud ALM für Anforderungs-, Test- und Aufgabenmanagement über alle Teilprojekte hinweg etabliert.</li>
                  <li><strong>Enable Now Übergabe:</strong> Autoren- und Schulungskonzept erfolgreich an die Personalentwicklung (UB AC) übergeben.</li>
                  <li><strong>Mitbestimmungs-Fahrplan:</strong> Pilot-Betriebsvereinbarung für den Testbetrieb mit Echtdaten (UAT) vorbereitet.</li>
                </ul>
              </div>

              <div class="space-y-1.5">
                <div class="font-bold text-white flex items-center space-x-1.5">
                  <span class="text-blue-400">➔</span>
                  <span>Nächster Projektschritt im Masterplan: Realize-Phase</span>
                </div>
                <ul class="text-[#c4bebe] space-y-1 list-disc list-inside text-[11px] leading-relaxed">
                  <li><strong>System-Customizing:</strong> Konfiguration und Aufbau des Entwicklungssystems im modifikationsfreien Clean-Core-Standard.</li>
                  <li><strong>Realisierung von Erweiterungen:</strong> On-Stack ABAP Cloud / RAP Entwicklung und Side-by-Side Entkopplung auf der SAP BTP.</li>
                  <li><strong>Migrations-Staging:</strong> Vorbereitung der Extraktions-Pipelines und Befüllung der Staging-Tabellen im SAP Migration Cockpit (LTMC).</li>
                  <li><strong>Test-Zyklen (SIT & UAT):</strong> Durchführung der Systemintegrationstests (SIT 1–3) in Cloud ALM und Vorbereitung des Produktiv-Cutovers.</li>
                </ul>
              </div>
            </div>
          </div>

          <!-- Why Greenfield & Clean Core -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 pt-2">
            <div class="p-4 rounded-xl bg-white/5 border border-white/10 hover:border-[#bf262e]/30 transition">
              <h4 class="text-sm font-bold text-white flex items-center space-x-2">
                <span>🌱</span>
                <span>Warum Greenfield und kein Brownfield?</span>
              </h4>
              <ul class="text-xs text-[#c4bebe] mt-2 space-y-1.5 list-disc list-inside">
                <li><strong>Historischer Monolith:</strong> Das bestehende SAP ECC 6.0 war über 20 Jahre durch unzählige Z-Modifikationen, User-Exits und proprietäre Tabellen verbaut.</li>
                <li><strong>Mangelnde Update-Fähigkeit:</strong> Ein direktes System-Upgrade (Brownfield) hätte Altlasten, veraltete Datenstrukturen und fehlerhafte Berechtigungen mitgeschleift.</li>
                <li><strong>Neustart nach Best Practice:</strong> Greenfield ermöglichte die strikte Rückkehr zum SAP-Standard via Fit-to-Standard Workshops mit Nagarro und Evora.</li>
              </ul>
            </div>

            <div class="p-4 rounded-xl bg-white/5 border border-white/10 hover:border-[#bf262e]/30 transition">
              <h4 class="text-sm font-bold text-white flex items-center space-x-2">
                <span>💎</span>
                <span>Das Clean Core Paradigma</span>
              </h4>
              <ul class="text-xs text-[#c4bebe] mt-2 space-y-1.5 list-disc list-inside">
                <li><strong>Keine Core-Modifikationen:</strong> Der S/4HANA Kern bleibt upgrade-sicher und cloud-kompatibel.</li>
                <li><strong>On-Stack Extensibility:</strong> Kundeneigene Logik im Kern erfolgt ausschließlich über freigegebene Schnittstellen (ABAP Cloud, RESTful Application Programming / RAP).</li>
                <li><strong>Side-by-Side auf der SAP BTP:</strong> Komplexe Individual-Applikationen und Schnittstellen-Orchestrierungen werden auf die SAP Business Technology Platform ausgelagert.</li>
              </ul>
            </div>
          </div>
        </div>

        <!-- Interaktives SAP Activate Phasen-Cockpit -->
        <div class="bg-[#141414] p-6 rounded-2xl border border-white/10 shadow-sm space-y-4">
          <div class="flex flex-col md:flex-row md:items-center justify-between gap-3">
            <div>
              <h3 class="text-base font-bold text-white flex items-center gap-2">
                <span>🎯</span>
                <span>Interaktives SAP Activate Phasen-Cockpit (End-to-End Methodik)</span>
              </h3>
              <p class="text-xs text-[#8f8888]">Strukturierte Umsetzung nach der offiziellen SAP Activate Methodik: Phasen-Deliverables, Q-Gates und Governance.</p>
            </div>
            
            <!-- Filter Tabs -->
            <div class="flex items-center space-x-1 bg-white/5 p-1 rounded-xl text-xs overflow-x-auto custom-scrollbar border border-white/10">
              <button 
                @click="wbsFilter = 'all'" 
                :class="['px-2.5 py-1 rounded-lg font-medium transition', wbsFilter === 'all' ? 'bg-[#bf262e] text-white shadow-sm' : 'text-[#8f8888] hover:text-white']"
              >Alle (6 Phasen)</button>
              <button 
                @click="wbsFilter = 'explore'" 
                :class="['px-2.5 py-1 rounded-lg font-medium transition', wbsFilter === 'explore' ? 'bg-[#bf262e] text-white shadow-sm' : 'text-[#8f8888] hover:text-white']"
              >Explore (Visars Fokus ⭐)</button>
              <button 
                @click="wbsFilter = 'realize'" 
                :class="['px-2.5 py-1 rounded-lg font-medium transition', wbsFilter === 'realize' ? 'bg-[#bf262e] text-white shadow-sm' : 'text-[#8f8888] hover:text-white']"
              >Ausblick (Realize / Deploy / Run)</button>
            </div>
          </div>

          <!-- Highlight Banner: Meilenstein-Governance nach SAP Activate Q-Gates -->
          <div class="p-4 rounded-xl bg-gradient-to-r from-red-950/30 via-[#181818] to-emerald-950/20 border border-[#bf262e]/30 flex flex-col md:flex-row items-start md:items-center justify-between gap-3">
            <div class="flex items-start space-x-3">
              <span class="text-2xl pt-0.5">🤝</span>
              <div class="space-y-0.5">
                <div class="text-xs font-bold text-white flex items-center gap-2">
                  <span>Meilenstein-Governance nach SAP Activate Q-Gates & Mitbestimmung</span>
                  <span class="px-2 py-0.2 rounded-full bg-[#bf262e]/20 text-[#f87171] text-[10px] font-bold">End-to-End Governance</span>
                </div>
                <p class="text-[11px] text-[#c4bebe]">
                  <strong>Q-Gate Explore formal freigegeben:</strong> Kaufmännisches Solution Design Document (SDD: FI/CO/MM/Trennungsrechnung/ACDOCA) vollständig finalisiert und durch den Lenkungsausschuss genehmigt. ➔ 
                  <strong>Institutionelle Mitbestimmung:</strong> Frühzeitige Einbindung der Arbeitnehmervertretung (Pilot-Betriebsvereinbarung für UAT-Tests und finale Betriebsvereinbarung für Produktivbetrieb).
                </p>
              </div>
            </div>
            <div class="text-right whitespace-nowrap">
              <span class="text-[10px] uppercase font-bold text-[#8f8888] tracking-wider">Explore Abschluss</span>
              <div class="text-xs font-extrabold text-[#f87171]">Meilenstein erreicht</div>
            </div>
          </div>

          <!-- WBS Cards Grid -->
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3 pt-2">
            <div 
              v-for="p in filteredWbsProjects" 
              :key="p.id"
              class="p-4 rounded-xl border border-white/10 bg-white/5 space-y-2.5 hover:border-[#bf262e]/40 transition"
            >
              <div class="flex items-center justify-between">
                <div class="flex items-center space-x-2">
                  <span class="font-extrabold text-xs text-[#f87171]">{{ p.id }}</span>
                  <span class="text-[10px] font-mono px-2 py-0.5 rounded bg-white/10 text-white">{{ p.wbs }}</span>
                </div>
                <span class="text-[10px] font-bold px-2 py-0.5 rounded-full bg-[#bf262e]/20 text-[#f87171] border border-[#bf262e]/30">{{ p.tag }}</span>
              </div>

              <div>
                <h4 class="text-xs font-bold text-white">{{ p.title }}</h4>
                <div class="text-[11px] text-[#8f8888] mt-0.5">Leitung: {{ p.lead }}</div>
              </div>

              <!-- Progress bar -->
              <div class="space-y-1">
                <div class="flex justify-between text-[10px] font-medium text-[#8f8888]">
                  <span>Reifegrad / Fortschritt</span>
                  <span class="font-bold text-white">{{ p.progress }}%</span>
                </div>
                <div class="w-full bg-white/10 h-1.5 rounded-full overflow-hidden">
                  <div class="bg-gradient-to-r from-[#bf262e] to-[#cf3840] h-1.5 rounded-full transition-all duration-500" :style="{ width: p.progress + '%' }"></div>
                </div>
              </div>

              <p class="text-[11px] text-[#c4bebe] leading-snug">{{ p.details }}</p>

              <div class="p-2 rounded-lg bg-black/40 border border-white/10 text-[10px] flex items-center space-x-1.5">
                <span class="text-amber-400 font-bold">🏁 Meilenstein:</span>
                <span class="font-medium text-[#c4bebe]">{{ p.milestone }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Die 5 Teilprojekte (TP1 bis TP5) -->
        <div class="bg-[#141414] p-6 rounded-2xl border border-white/10 shadow-sm space-y-4">
          <h3 class="text-base font-bold text-white">Die 5 Teilprojekte (TP1 bis TP5) & Stakeholder-Matrix</h3>
          <div class="grid grid-cols-1 md:grid-cols-5 gap-3">
            
            <!-- TP1 -->
            <div class="p-3.5 rounded-xl border border-white/10 bg-white/5 space-y-2 hover:border-[#bf262e]/30 transition">
              <div class="flex items-center justify-between">
                <span class="font-bold text-xs text-[#f87171]">TP1</span>
                <span class="text-[10px] bg-white/10 text-[#c4bebe] px-1.5 py-0.5 rounded">Change & Enablement</span>
              </div>
              <div class="text-xs font-semibold text-white">Change Management & Academy</div>
              <div class="text-[11px] text-[#8f8888]">Leitung: Teilprojektleitung Change Management & Academy</div>
              <p class="text-[11px] text-[#c4bebe]">
                Kultureller Wandel, Betriebsrat-Einbindung, Kommunikation an 3.700 MA, SAP Enable Now Rollout mit UB AC (Personalentwicklung).
              </p>
            </div>

            <!-- TP2 -->
            <div class="p-3.5 rounded-xl border border-white/10 bg-white/5 space-y-2 hover:border-[#bf262e]/30 transition">
              <div class="flex items-center justify-between">
                <span class="font-bold text-xs text-[#f87171]">TP2</span>
                <span class="text-[10px] bg-emerald-500/20 text-emerald-300 px-1.5 py-0.5 rounded">Kaufmännisch</span>
              </div>
              <div class="text-xs font-semibold text-white">Finance & Controlling</div>
              <div class="text-[11px] text-[#8f8888]">Leitung: Teilprojektleitung Finanzen & Controlling</div>
              <p class="text-[11px] text-[#c4bebe]">
                S/4HANA FI/CO, Trennungsrechnung (PBV/ÖPNV), Universal Journal (ACDOCA), New Asset Accounting (FI-AA), xSuite Rechnungswesen.
              </p>
            </div>

            <!-- TP3 -->
            <div class="p-3.5 rounded-xl border border-white/10 bg-white/5 space-y-2 hover:border-[#bf262e]/30 transition">
              <div class="flex items-center justify-between">
                <span class="font-bold text-xs text-[#f87171]">TP3</span>
                <span class="text-[10px] bg-amber-500/20 text-amber-300 px-1.5 py-0.5 rounded">Technik</span>
              </div>
              <div class="text-xs font-semibold text-white">Instandhaltung & Logistik</div>
              <div class="text-[11px] text-[#8f8888]">Leitung: Teilprojektleitung Instandhaltung & Logistik</div>
              <p class="text-[11px] text-[#c4bebe]">
                Instandhaltung der Stadtbahnen, Busse und Schieneninfrastruktur (SAP PM / EAM), mobile Instandhaltung mit Evora, Materialwirtschaft (MM).
              </p>
            </div>

            <!-- TP4 -->
            <div class="p-3.5 rounded-xl border border-white/10 bg-white/5 space-y-2 hover:border-[#bf262e]/30 transition">
              <div class="flex items-center justify-between">
                <span class="font-bold text-xs text-[#f87171]">TP4</span>
                <span class="text-[10px] bg-purple-500/20 text-purple-300 px-1.5 py-0.5 rounded">Personal</span>
              </div>
              <div class="text-xs font-semibold text-white">HR & Nachfolgesystem</div>
              <div class="text-[11px] text-[#8f8888]">Leitung: Teilprojektleitung Personal & HR</div>
              <p class="text-[11px] text-[#c4bebe]">
                Evaluation von SAP SuccessFactors vs. Best-of-Breed HR-Lösungen, Digitale Personalakte (d.velop), Entgeltabrechnung.
              </p>
            </div>

            <!-- TP5 -->
            <div class="p-3.5 rounded-xl border-2 border-[#bf262e] bg-[#bf262e]/10 space-y-2 shadow-lg shadow-[#bf262e]/10">
              <div class="flex items-center justify-between">
                <span class="font-bold text-xs text-white">TP5 (DEIN HOME)</span>
                <span class="text-[10px] bg-[#bf262e] text-white font-bold px-1.5 py-0.5 rounded">IT-PMO & Architektur</span>
              </div>
              <div class="text-xs font-bold text-white">Gesamtsteuerung & Basis</div>
              <div class="text-[11px] text-[#fecdd3]">Leitung: Gesamtprojektleitung ERP & IT-Leitung</div>
              <p class="text-[11px] text-white/90 font-medium">
                Multiprojekt-Governance, Tool-Stack (CALM, Signavio), Schnittstellenarchitektur, Basisbetreuung mit Axians, Lenkungsausschuss-Vorbereitung.
              </p>
            </div>

          </div>
        </div>

        <!-- Scope & Third-Party System Landscape -->
        <div class="bg-[#141414] p-6 rounded-2xl border border-white/10 shadow-sm space-y-4">
          <h3 class="text-base font-bold text-white">Die komplexe Drittsystem-Landschaft der SSB</h3>
          <p class="text-xs text-[#8f8888]">Schnittstellen und Integrationsmuster, die du aus dem Lösungsdesign kennst</p>
          <div class="grid grid-cols-2 md:grid-cols-4 gap-3 text-xs">
            <div class="p-3 rounded-lg border border-white/10 bg-white/5 hover:border-[#bf262e]/30 transition">
              <div class="font-bold text-white">xSuite</div>
              <div class="text-[#8f8888] text-[11px]">Rechnungseingang & OCR</div>
              <div class="text-[#c4bebe] mt-1 text-[11px]">Automatisierte Rechnungsverarbeitung, Freigabeworkflows, Anbindung an S/4-FI.</div>
            </div>
            <div class="p-3 rounded-lg border border-white/10 bg-white/5 hover:border-[#bf262e]/30 transition">
              <div class="font-bold text-white">d.velop</div>
              <div class="text-[#8f8888] text-[11px]">DMS & Digitale Akten</div>
              <div class="text-[#c4bebe] mt-1 text-[11px]">Archivierung von Belegen, Anbindung über ArchiveLink und CMIS-Schnittstellen.</div>
            </div>
            <div class="p-3 rounded-lg border border-white/10 bg-white/5 hover:border-[#bf262e]/30 transition">
              <div class="font-bold text-white">PATRIS / iTWO / EDM</div>
              <div class="text-[#8f8888] text-[11px]">Branchenspezifisch ÖPNV</div>
              <div class="text-[#c4bebe] mt-1 text-[11px]">Abrechnung Fahrgeldeinnahmen, Bauprojektmanagement und Energiedatenmanagement.</div>
            </div>
            <div class="p-3 rounded-lg border border-white/10 bg-white/5 hover:border-[#bf262e]/30 transition">
              <div class="font-bold text-white">Axians ES4 / ADS</div>
              <div class="text-[#8f8888] text-[11px]">Infrastruktur & Cloud Basis</div>
              <div class="text-[#c4bebe] mt-1 text-[11px]">ES4 Testmandanten (M300/M100), Adobe Document Services, Single Sign-On (SSO).</div>
            </div>
          </div>
        </div>
      </div>
"""
