# -*- coding: utf-8 -*-
"""
Portal Builder Module: Stärkenprofil, Synergie-Atlas (Arbeit × Uni × Projekte) & Kompakte Erfahrungs-Synthese.
Renders safely in BOTH Local Cockpit (index.html) and Public Showcase (public_index.html).
"""


def get_synergies(public_mode=False):
    rag_hint = (
        ""
        if public_mode
        else """
              <button
                @click="askSynergyRag('Fasse meine stärksten Arbeit x Uni Synergien inkl. konkreter Projektnachweise kompakt zusammen', 'synergies')"
                class="px-3 py-1.5 rounded-xl bg-[#bf262e] hover:bg-[#cf3840] text-white text-xs font-semibold shadow-md shadow-[#bf262e]/30 transition flex items-center space-x-1.5"
              >
                <span>🤖</span>
                <span>Kompakt-Briefing im Local RAG öffnen</span>
              </button>"""
    )

    deep_rag_btn = (
        ""
        if public_mode
        else """
                <button
                  @click="askSynergyRag(syn.ragQuery, 'synergies')"
                  class="mt-2 inline-flex items-center space-x-1.5 px-2.5 py-1 rounded-lg bg-[#bf262e]/15 hover:bg-[#bf262e]/30 border border-[#bf262e]/40 text-[#f87171] hover:text-white text-[11px] font-semibold transition"
                >
                  <span>🤖</span>
                  <span>60s-Synthese via RAG laden</span>
                </button>"""
    )

    return f"""
      <!-- ================= TAB: STÄRKENPROFIL, SYNERGIEN & KOMPAKTE ERFAHRUNGEN ================= -->
      <div v-show="activeTab === 'synergies'" class="space-y-6">

        <!-- Hero Banner: Profil & Kernnutzen -->
        <div class="bg-gradient-to-br from-[#181818] via-[#141414] to-[#1d1112] p-6 rounded-2xl border border-white/10 shadow-xl space-y-4">
          <div class="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
            <div class="space-y-1.5 max-w-4xl">
              <div class="flex flex-wrap items-center gap-2">
                <span class="px-2.5 py-0.5 rounded-full bg-[#bf262e]/20 text-[#f87171] border border-[#bf262e]/40 text-[10px] font-bold uppercase tracking-wider">
                  Knowledge & Profile OS 2.0
                </span>
                <span class="px-2.5 py-0.5 rounded-full bg-emerald-500/15 text-emerald-300 border border-emerald-500/30 text-[10px] font-semibold">
                  M.Sc. 1,6 | Masterarbeit 1,0 | +1,4 Notenpunkte Entwicklung
                </span>
                <span class="px-2.5 py-0.5 rounded-full bg-blue-500/15 text-blue-300 border border-blue-500/30 text-[10px] font-semibold">
                  36 Monate Enterprise-Praxis (24M SSB + 12M DC1)
                </span>
              </div>
              <h3 class="text-xl sm:text-2xl font-extrabold text-white tracking-tight">
                Persönliches Stärkenprofil & Arbeit × Studium Synergie-Atlas
              </h3>
              <p class="text-xs sm:text-sm text-[#c4bebe] leading-relaxed">
                Wie aus <strong>300 ECTS Wirtschaftsinformatik (Universität Stuttgart)</strong>, <strong>24 Monaten S/4HANA Großprojekt (SSB AG)</strong>, <strong>12 Monaten 24/7 Rechenzentrumsbetrieb (Datacenter One)</strong> und angewandten <strong>Industrie- & Eigenprojekten</strong> fünf scharfe Kompetenz-Cluster entstehen.
              </p>
            </div>
            <div class="flex flex-wrap items-center gap-2 self-start lg:self-center">{rag_hint}
              <div class="inline-flex rounded-xl bg-black/50 border border-white/10 p-1 text-xs">
                <button
                  @click="synergyViewMode = 'compact'"
                  :class="synergyViewMode === 'compact' ? 'bg-[#bf262e] text-white font-bold shadow-sm' : 'text-[#c4bebe] hover:text-white'"
                  class="px-3 py-1 rounded-lg transition"
                >
                  ⚡ 60s-Kompakt
                </button>
                <button
                  @click="synergyViewMode = 'deep'"
                  :class="synergyViewMode === 'deep' ? 'bg-white/15 text-white font-bold shadow-sm' : 'text-[#c4bebe] hover:text-white'"
                  class="px-3 py-1 rounded-lg transition"
                >
                  🔬 Tiefenprofil
                </button>
              </div>
            </div>
          </div>

          <!-- Roter Faden Timeline (2019 -> 2026+) -->
          <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 pt-2 text-xs">
            <div class="p-3.5 rounded-xl bg-white/5 border border-white/10">
              <div class="text-[10px] font-mono text-indigo-300 uppercase">2019–2023 • Fundament</div>
              <div class="font-bold text-white mt-0.5">B.Sc. (180 ECTS) & TOGAF 9</div>
              <p class="text-[11px] text-[#c4bebe] mt-1">Breite Informatik & BWL, <strong>E-Business (1,0)</strong>, TOGAF 9 ADM (2020), Bachelorarbeit <strong>1,7</strong> über Boundary Resources (OutSystems/Mendix).</p>
            </div>
            <div class="p-3.5 rounded-xl bg-white/5 border border-white/10">
              <div class="text-[10px] font-mono text-blue-300 uppercase">05/2023–04/2024 • Betrieb</div>
              <div class="font-bold text-white mt-0.5">Datacenter One (12M INOC)</div>
              <p class="text-[11px] text-[#c4bebe] mt-1"><strong>24/7 Leitstand</strong>, ITIL 4 SPoC (Jira), PRTG-Monitoring, Aufbau Confluence-SOPs & Hardware-Lifecycle-Prozess in Visio (100+ Systeme).</p>
            </div>
            <div class="p-3.5 rounded-xl bg-white/5 border border-white/10">
              <div class="text-[10px] font-mono text-emerald-300 uppercase">05/2024–04/2026 • Großprojekt</div>
              <div class="font-bold text-white mt-0.5">SSB AG SAP4SSB & M.Sc. (1,6)</div>
              <p class="text-[11px] text-[#c4bebe] mt-1"><strong>24M IT-PMO (TP5)</strong> bis Explore-Abschluss (SDD, Signavio, Cloud ALM, Enable Now) & <strong>Masterarbeit 1,0</strong> (12 Interviews, Mayring).</p>
            </div>
            <div class="p-3.5 rounded-xl bg-[#bf262e]/15 border border-[#bf262e]/40">
              <div class="text-[10px] font-mono text-[#f87171] uppercase">2026+ • Zielwirkung</div>
              <div class="font-bold text-white mt-0.5">Enterprise Transformation</div>
              <p class="text-[11px] text-[#f0eded] mt-1">Junior SAP / ERP-Consultant, Enterprise Architecture & Governance oder IT-Trainee mit sofortiger Anschlussfähigkeit an Business & IT.</p>
            </div>
          </div>
        </div>

        <!-- Die 5 Evidenzbasierten Stärken-Cluster -->
        <div class="bg-[#141414] p-6 rounded-2xl border border-white/10 shadow-sm space-y-4">
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
            <div>
              <h4 class="text-base font-bold text-white flex items-center space-x-2">
                <span>💪</span>
                <span>Die 5 Stärken-Cluster (jeder Anspruch durch harte Belege gedeckt)</span>
              </h4>
              <p class="text-xs text-[#8f8888]">Abgeleitet aus amtlichen Zeugnissen, 36 Monaten Arbeitszeugnis-/Projektdaten und verwertbaren Artefakten.</p>
            </div>
            <span class="text-[11px] font-mono text-emerald-400">100% Fakten-verifiziert</span>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 text-xs">
            <div class="p-4 rounded-xl bg-white/5 border border-white/10 hover:border-[#bf262e]/40 transition space-y-2">
              <div class="flex items-center justify-between">
                <span class="font-bold text-white">1. Ganzheitliche Plattform-Architektur</span>
                <span class="tag-badge bg-[#bf262e]/20 text-[#f87171] border border-[#bf262e]/40">Kernstärke</span>
              </div>
              <p class="text-[#c4bebe] leading-relaxed">Verbindet Geschäftsprozesse mit sauberer System-Entkopplung: <strong>TOGAF 9 ADM</strong>, <strong>Boundary Resource Theory</strong> (B.Sc. 1,7) und ganzheitliche <strong>S/4HANA-Plattformisierung</strong> (Masterarbeit 1,0, 126 S., 12 Interviews).</p>
              <div v-show="synergyViewMode === 'deep'" class="pt-2 border-t border-white/10 text-[11px] text-[#8f8888]">
                Belege: WRICEFA-Entkopplung (PATRIS/xSuite/d.velop), ASE (1,6), Software-Architektur (1,7), AWS Cloud (2,0).
              </div>
            </div>

            <div class="p-4 rounded-xl bg-white/5 border border-white/10 hover:border-emerald-500/40 transition space-y-2">
              <div class="flex items-center justify-between">
                <span class="font-bold text-white">2. „Bilingualer Übersetzer“ Business × IT</span>
                <span class="tag-badge bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">Stakeholder</span>
              </div>
              <p class="text-[#c4bebe] leading-relaxed">Spricht sowohl HGB-/Controlling-Sprache (<strong>E-Business 1,0</strong>, <strong>IVP 2,3</strong>, Trennungsrechnung EU-1370) als auch Entwickler-/Architekturlogik — erprobt als Klammer über <strong>TP1–TP5</strong> bei der SSB AG.</p>
              <div v-show="synergyViewMode === 'deep'" class="pt-2 border-t border-white/10 text-[11px] text-[#8f8888]">
                Belege: Partner-Abstimmung (Nagarro, Axians, Evora, apsolut), C-Level Steering Board & Betriebsrat § 87 BetrVG.
              </div>
            </div>

            <div class="p-4 rounded-xl bg-white/5 border border-white/10 hover:border-purple-500/40 transition space-y-2">
              <div class="flex items-center justify-between">
                <span class="font-bold text-white">3. Methodische Tiefe & Lernkurve (+1,4)</span>
                <span class="tag-badge bg-purple-500/20 text-purple-300 border border-purple-500/30">Empirie</span>
              </div>
              <p class="text-[#c4bebe] leading-relaxed">Kontinuierliche Steigerung vom <strong>B.Sc. (3,0)</strong> zum <strong>M.Sc. (1,6)</strong> — gekrönt durch Masterarbeit <strong>1,0</strong> (Mayring Codebuch), <strong>FPWI (1,3 | SUS 85/100)</strong> und <strong>PRISMA SLR (1,7)</strong>.</p>
              <div v-show="synergyViewMode === 'deep'" class="pt-2 border-t border-white/10 text-[11px] text-[#8f8888]">
                Belege: Forschungsmethoden (1,7, Algorithm Aversion), 439 analysierte MRK-Studien, strukturierte Entscheidungsreife.
              </div>
            </div>

            <div class="p-4 rounded-xl bg-white/5 border border-white/10 hover:border-amber-500/40 transition space-y-2">
              <div class="flex items-center justify-between">
                <span class="font-bold text-white">4. Tool-Governance & Automatisierung</span>
                <span class="tag-badge bg-amber-500/20 text-amber-300 border border-amber-500/30">Execution</span>
              </div>
              <p class="text-[#c4bebe] leading-relaxed">Schafft einheitliche Standards in komplexen Teams: offizieller <strong>SAP Cloud ALM How2Handle</strong>-Leitfaden, <strong>Enable Now Übergabekonzept</strong> und fehlerfreie <strong>PowerShell-/BPMN-Automatisierung</strong> (Schmalz 1,0).</p>
              <div v-show="synergyViewMode === 'deep'" class="pt-2 border-t border-white/10 text-[11px] text-[#8f8888]">
                Belege: Signavio BPMN 2.0 (SSB), Visio HLM_v2.vsdx (DC1), Klingele PatentRadar SaaS/RPA-Konzept (ISG 2,0).
              </div>
            </div>

            <div class="p-4 rounded-xl bg-white/5 border border-white/10 hover:border-blue-500/40 transition space-y-2">
              <div class="flex items-center justify-between">
                <span class="font-bold text-white">5. Operative Resilienz & Service Ops</span>
                <span class="tag-badge bg-blue-500/20 text-blue-300 border border-blue-500/30">ITIL 4 / 24-7</span>
              </div>
              <p class="text-[#c4bebe] leading-relaxed">Bewahrt im Live-Betrieb analytische Ruhe: <strong>12 Monate 24/7 INOC</strong> bei Datacenter One (PRTG, Jira SPoC, USV/Klima/Dark Fiber, Confluence SOPs) plus Basis-GAP-Tracking bei SSB.</p>
              <div v-show="synergyViewMode === 'deep'" class="pt-2 border-t border-white/10 text-[11px] text-[#8f8888]">
                Belege: Strukturierte 3rd-Level Root-Cause-Methodik (Job-Monitoring, Berechtigungsobjekte, Schnittstellen-Checks).
              </div>
            </div>

            <div class="p-4 rounded-xl bg-black/40 border border-white/15 space-y-2">
              <div class="flex items-center justify-between">
                <span class="font-bold text-amber-300">🎯 Bewusster Wachstums-Radar (Jahr 1)</span>
                <span class="tag-badge bg-white/10 text-[#c4bebe] border border-white/15">Transparenz</span>
              </div>
              <p class="text-[#c4bebe] leading-relaxed">Kein klassischer SPRO-/ABAP-Altsystem-Developer — bewusstes Clean-Core-PMO-Profil (Austritt SSB zum <strong>Explore-Abschluss 04/2026</strong>). Fokus ab Tag 1: volle <strong>Realize-/Go-Live-Begleitung</strong> & <strong>RAP/BTP/ITIL 4</strong>-Vertiefung.</p>
            </div>
          </div>
        </div>

        <!-- Interaktiver Arbeit × Studium × Projekte Synergie-Atlas (6 Matrizen) -->
        <div class="bg-[#141414] p-6 rounded-2xl border border-white/10 shadow-sm space-y-4">
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-white/10 pb-4">
            <div>
              <h4 class="text-base font-bold text-white flex items-center space-x-2">
                <span>🔗</span>
                <span>Synergie-Atlas: Wie Arbeit, Universität & Eigenprojekte ineinandergreifen</span>
              </h4>
              <p class="text-xs text-[#8f8888]">6 kuratierte Querverbindungen — jeweils direkt aus deinem Obsidian Second Brain abgeleitet.</p>
            </div>
            <div class="flex flex-wrap gap-1.5 text-[11px]">
              <button
                v-for="cat in ['Alle', 'Architektur & Cloud', 'Governance & Daten', 'Automatisierung & KI']"
                :key="cat"
                @click="synergyFilter = cat"
                :class="synergyFilter === cat ? 'bg-[#bf262e] text-white font-bold' : 'bg-white/5 text-[#c4bebe] hover:bg-white/10'"
                class="px-2.5 py-1 rounded-lg border border-white/10 transition"
              >
                {{ cat }}
              </button>
            </div>
          </div>

          <div class="grid grid-cols-1 lg:grid-cols-2 gap-4 text-xs">
            <div
              v-for="syn in filteredSynergies"
              :key="syn.id"
              class="p-4 rounded-xl bg-white/5 border border-white/10 hover:border-[#bf262e]/45 transition flex flex-col justify-between space-y-3"
            >
              <div class="space-y-2.5">
                <div class="flex items-start justify-between gap-2">
                  <div>
                    <span class="text-[10px] font-mono uppercase text-[#f87171]">{{{{ syn.cluster }}}}</span>
                    <h5 class="text-sm font-bold text-white mt-0.5">{{{{ syn.title }}}}</h5>
                  </div>
                  <span class="px-2 py-0.5 rounded-full bg-white/10 text-[10px] font-mono text-[#c4bebe] whitespace-nowrap">{{{{ syn.badge }}}}</span>
                </div>

                <div class="grid grid-cols-1 sm:grid-cols-3 gap-2 text-[11px]">
                  <div class="p-2.5 rounded-lg bg-purple-500/10 border border-purple-500/20">
                    <div class="font-bold text-purple-300 mb-0.5">🎓 Studium</div>
                    <div class="text-[#d6d0d0] leading-snug">{{{{ syn.uni }}}}</div>
                  </div>
                  <div class="p-2.5 rounded-lg bg-blue-500/10 border border-blue-500/20">
                    <div class="font-bold text-blue-300 mb-0.5">🏢/🚆 Praxis</div>
                    <div class="text-[#d6d0d0] leading-snug">{{{{ syn.work }}}}</div>
                  </div>
                  <div class="p-2.5 rounded-lg bg-emerald-500/10 border border-emerald-500/20">
                    <div class="font-bold text-emerald-300 mb-0.5">🚀 Projekt / Proof</div>
                    <div class="text-[#d6d0d0] leading-snug">{{{{ syn.project }}}}</div>
                  </div>
                </div>

                <div class="p-2.5 rounded-lg bg-black/40 border border-white/10 text-[#f0eded] leading-relaxed">
                  <strong class="text-[#f87171]">⚡ Synergie-Effekt:</strong> {{{{ syn.synergy }}}}
                </div>
                <p v-show="synergyViewMode === 'deep'" class="text-[11px] text-[#c4bebe] leading-relaxed">
                  {{{{ syn.deepNote }}}}
                </p>
              </div>
              <div class="flex flex-wrap items-center justify-between gap-2 pt-1 border-t border-white/10">
                <button @click="activeTab = syn.targetTab" class="text-[11px] text-[#c4bebe] hover:text-white underline">
                  Fachbereich im Portal ansehen ➔
                </button>{deep_rag_btn}
              </div>
            </div>
          </div>
        </div>

        <!-- Kompakte 60s-Erfahrungs-Essenzen (Alle Stationen auf einen Blick) -->
        <div class="bg-[#141414] p-6 rounded-2xl border border-white/10 shadow-sm space-y-4">
          <h4 class="text-base font-bold text-white flex items-center space-x-2">
            <span>⚡</span>
            <span>Erfahrungs-Essenzen (Alle Stationen in je 60 Sekunden)</span>
          </h4>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
            <div class="p-4 rounded-xl bg-white/5 border border-white/10 space-y-1.5">
              <div class="flex items-center justify-between font-bold text-white">
                <span>🚆 Stuttgarter Straßenbahnen AG (SSB AG)</span>
                <span class="text-[11px] text-emerald-400">24 Monate (05/2024–04/2026)</span>
              </div>
              <p class="text-[#c4bebe] leading-relaxed">Werkstudent IT-PMO & Gesamtsteuerung (`TP5`) unter Gesamtprojektleitung & IT-Leitung. Pflege MS-Project-Masterplan (`TP1–TP5`), SDD-Prozessdokumentation (`FI/CO/MM`), Governance über Signavio, Cloud ALM (`How2Handle`) & Enable Now sowie Datenmigrations-Vorbereitung (`LTMC`/`CVI`) bis zum erfolgreichen Explore-Abschluss.</p>
            </div>
            <div class="p-4 rounded-xl bg-white/5 border border-white/10 space-y-1.5">
              <div class="flex items-center justify-between font-bold text-white">
                <span>🏢 Datacenter One GmbH (INOC)</span>
                <span class="text-[11px] text-blue-400">12 Monate (05/2023–04/2024)</span>
              </div>
              <p class="text-[#c4bebe] leading-relaxed">Werkstudent 24/7 Information Network Operation Center unter INOC-Leitung. Single Point of Contact (Jira), PRTG-Echtzeitüberwachung (Core-Netze, USV, Klima, Dark Fiber), Aufbau der Confluence-Prozessdatenbank nach ITIL 4 und Visio-BPMN-Design für den Hardware-Lifecycle (100+ Arbeitsplätze).</p>
            </div>
            <div class="p-4 rounded-xl bg-white/5 border border-white/10 space-y-1.5">
              <div class="flex items-center justify-between font-bold text-white">
                <span>🎓 M.Sc. & B.Sc. Wirtschaftsinformatik (Uni Stuttgart)</span>
                <span class="text-[11px] text-purple-300">300 ECTS (M.Sc. 1,6 | Thesis 1,0)</span>
              </div>
              <p class="text-[#c4bebe] leading-relaxed">Bachelor (180 ECTS, Note 3,0, E-Business Bestnote 1,0, Bachelorarbeit Boundary Resources 1,7) gefolgt von exzellentem Master (120 ECTS, Gesamtnote 1,6, Zeugnis 17.09.2026, Masterarbeit S/4HANA-Plattformisierung 1,0 mit 12 Experteninterviews nach Mayring) + TOGAF 9 ADM.</p>
            </div>
            <div class="p-4 rounded-xl bg-white/5 border border-white/10 space-y-1.5">
              <div class="flex items-center justify-between font-bold text-white">
                <span>🚀 Industrie- & Eigenprojekte (Automation, SaaS, RAG)</span>
                <span class="text-[11px] text-amber-300">Hands-on Belege</span>
              </div>
              <p class="text-[#c4bebe] leading-relaxed"><strong>J. Schmalz GmbH (1,0):</strong> PowerShell-Automatisierung & BPMN für CSRD-Abfallbilanz • <strong>Klingele/ISG PatentRadar (2,0):</strong> Hybrides SaaS-/RPA-Geschäftsmodell • <strong>Knowledge & Profile OS:</strong> Modulares Vue 3 Portal + lokales 3-Signal Hybrid RAG V3 über 4.980 Quelldateien.</p>
            </div>
          </div>
        </div>

      </div>
"""
