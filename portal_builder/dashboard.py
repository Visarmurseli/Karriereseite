# -*- coding: utf-8 -*-

def get_dashboard():
    return """
      <!-- ================= TAB 1: EXECUTIVE BRIEFING ================= -->
      <div v-show="activeTab === 'dashboard'" class="space-y-6">
        
        <!-- Hero Banner: The Strategic Triangle -->
        <div class="bg-gradient-to-br from-[#181818] via-[#141414] to-[#1c080a] text-white rounded-2xl p-6 lg:p-8 shadow-2xl border border-[#bf262e]/30 relative overflow-hidden">
          <div class="relative z-10 max-w-4xl space-y-4">
            <div class="flex flex-wrap items-center gap-2">
              <span class="bg-[#bf262e] text-white px-2.5 py-0.5 rounded-md text-xs font-bold uppercase tracking-wider shadow-md shadow-[#bf262e]/30">🎯 Junior Einstieg & Trainee</span>
              <span class="bg-white/5 text-[#fecdd3] border border-[#bf262e]/30 px-2.5 py-0.5 rounded-md text-xs font-medium">Stuttgarter Straßenbahnen AG (3.700 MA)</span>
              <span class="bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 px-2.5 py-0.5 rounded-md text-xs font-medium">24 Monate Greenfield S/4HANA</span>
              <span class="bg-purple-500/20 text-purple-300 border border-purple-500/30 px-2.5 py-0.5 rounded-md text-xs font-medium">Masterarbeit Note 1,0 (30 ECTS)</span>
            </div>
            
            <h2 class="text-2xl sm:text-3xl font-extrabold tracking-tight text-[#f5f3f3]">
              Das Enterprise Knowledge & Career Operating System
            </h2>
            <p class="text-[#c4bebe] text-xs sm:text-sm leading-relaxed">
              Dieses Wissensportal bündelt dein gesamtes Know-how für den <strong>zielgerichteten Direkteinstieg als Junior SAP Consultant oder in ein IT-/Management-Traineeprogramm</strong>: <strong>Zwei Jahre operative IT-PMO Praxis bei der SSB AG (3.700 MA)</strong>, deine <strong>mit 1,0 bewertete Masterarbeit (Prof. Herzwurm)</strong>, deine <strong>TOGAF-Zertifizierung</strong> und <strong>12 Monate ITIL 4 Service Operations bei Datacenter One</strong>.
            </p>

            <!-- 3 Pillars -->
            <div class="grid grid-cols-1 md:grid-cols-3 gap-3 pt-2">
              <div @click="activeTab = 'project'" class="bg-white/5 hover:bg-[#bf262e]/15 transition cursor-pointer backdrop-blur rounded-xl p-3.5 border border-white/10 hover:border-[#bf262e]/50 group">
                <div class="text-[#f87171] font-bold text-xs uppercase flex items-center justify-between">
                  <span>1. Enterprise Praxis</span>
                  <span class="group-hover:translate-x-1 transition">➔</span>
                </div>
                <div class="font-semibold text-sm mt-1 text-white">24 Mo. IT-PMO (TP5)</div>
                <div class="text-[11px] text-[#c4bebe] mt-1">TP1–TP5 Koordination, Lenkungsausschuss, Meilensteine, Tool-Governance (CALM, Signavio, SEN).</div>
              </div>

              <div @click="activeTab = 'thesis'" class="bg-white/5 hover:bg-[#bf262e]/15 transition cursor-pointer backdrop-blur rounded-xl p-3.5 border border-white/10 hover:border-[#bf262e]/50 group">
                <div class="text-[#f87171] font-bold text-xs uppercase flex items-center justify-between">
                  <span>2. Akademische Spitze</span>
                  <span class="group-hover:translate-x-1 transition">➔</span>
                </div>
                <div class="font-semibold text-sm mt-1 text-white">Masterarbeit Note 1,0</div>
                <div class="text-[11px] text-[#c4bebe] mt-1">126 Seiten, 12 Experteninterviews, empirische ERP-Transformation & Plattform-Governance.</div>
              </div>

              <div @click="activeTab = 'solution_design'" class="bg-white/5 hover:bg-[#bf262e]/15 transition cursor-pointer backdrop-blur rounded-xl p-3.5 border border-white/10 hover:border-[#bf262e]/50 group">
                <div class="text-[#f87171] font-bold text-xs uppercase flex items-center justify-between">
                  <span>3. Architektur & Daten</span>
                  <span class="group-hover:translate-x-1 transition">➔</span>
                </div>
                <div class="font-semibold text-sm mt-1 text-white">Solution Design & Migration</div>
                <div class="text-[11px] text-[#c4bebe] mt-1">Trennungsrechnung, Staging-Tabellen, SuSa-Abgleich (0,00 € Übernahmekonto), CVI & Drittsysteme.</div>
              </div>
            </div>
          </div>
          <div class="absolute right-0 top-0 bottom-0 w-1/3 bg-gradient-to-l from-[#bf262e]/10 to-transparent pointer-events-none"></div>
        </div>

        <!-- KPI Grid -->
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div class="bg-[#141414] p-4 rounded-xl border border-white/10 hover:border-[#bf262e]/40 transition shadow-sm">
            <div class="text-xs text-[#8f8888] font-medium">Praxiserfahrung SSB AG</div>
            <div class="text-xl font-bold text-white mt-1">24 Monate</div>
            <div class="text-xs text-emerald-400 mt-1 font-medium">01.05.2024 – 30.04.2026</div>
          </div>

          <div class="bg-[#141414] p-4 rounded-xl border border-white/10 hover:border-[#bf262e]/40 transition shadow-sm">
            <div class="text-xs text-[#8f8888] font-medium">Konzern-Scope SSB</div>
            <div class="text-xl font-bold text-white mt-1">3.700 MA</div>
            <div class="text-xs text-[#f87171] mt-1 font-medium">5 Teilprojekte (TP1–TP5)</div>
          </div>

          <div class="bg-[#141414] p-4 rounded-xl border border-white/10 hover:border-[#bf262e]/40 transition shadow-sm">
            <div class="text-xs text-[#8f8888] font-medium">Masterabschluss (Uni Stuttgart)</div>
            <div class="text-xl font-bold text-white mt-1">M.Sc. 1,6</div>
            <div class="text-xs text-purple-400 mt-1 font-medium">Masterarbeit Note 1,0 (30 ECTS)</div>
          </div>

          <div class="bg-[#141414] p-4 rounded-xl border border-white/10 hover:border-[#bf262e]/40 transition shadow-sm">
            <div class="text-xs text-[#8f8888] font-medium">Empirische Expertenbasis</div>
            <div class="text-xl font-bold text-white mt-1">12 Interviews</div>
            <div class="text-xs text-amber-400 mt-1 font-medium">Nowak, Nagarro Architekten, TPLs</div>
          </div>
        </div>

        <!-- Knowledge Graph & Ecosystem Telemetry Bar -->
        <div class="bg-gradient-to-r from-[#141414] via-[#1a0e10] to-[#141414] p-5 rounded-2xl border border-[#bf262e]/30 text-white shadow-lg space-y-3">
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
            <div class="flex items-center space-x-2">
              <span class="text-lg">🧠</span>
              <div>
                <h4 class="text-sm font-bold tracking-tight text-[#f5f3f3] flex items-center gap-2">
                  <span>Neuronales Second Brain & Enterprise Wissensgraph</span>
                  <span class="px-2 py-0.5 rounded-full bg-[#bf262e]/20 text-[#f87171] border border-[#bf262e]/40 text-[10px] font-mono">Obsidian & Notion Bridge</span>
                </h4>
                <p class="text-[11px] text-[#c4bebe]">Vollständig vernetztes Wissenssystem: Von empirischen Interviewtranskripten bis zu SDD-Architekturmodellen.</p>
              </div>
            </div>
            <button @click="openCommandPalette" class="self-start sm:self-auto px-3 py-1.5 rounded-lg bg-[#bf262e] hover:bg-[#cf3840] text-white text-xs font-semibold flex items-center space-x-1.5 transition shadow-md shadow-[#bf262e]/30">
              <span>⚡ Schnellsuche starten</span>
              <kbd class="px-1 py-0.5 bg-black/40 rounded text-[9px] font-mono">Ctrl K</kbd>
            </button>
          </div>

          <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 pt-1">
            <div @click="activeTab = 'notebook'" class="p-3 rounded-xl bg-white/5 hover:bg-[#bf262e]/10 transition border border-white/10 hover:border-[#bf262e]/40 cursor-pointer">
              <div class="text-[11px] text-[#fecdd3] font-medium">Obsidian Deep-Dive Dossiers</div>
              <div class="text-xl font-extrabold text-white mt-0.5">53 Dossiers</div>
              <div class="text-[10px] text-emerald-400 mt-0.5">266 bidirektionale Links (0 Broken)</div>
            </div>

            <div @click="activeTab = 'files'" class="p-3 rounded-xl bg-white/5 hover:bg-[#bf262e]/10 transition border border-white/10 hover:border-[#bf262e]/40 cursor-pointer">
              <div class="text-[11px] text-[#fecdd3] font-medium">Notion Transformation Hub</div>
              <div class="text-xl font-extrabold text-white mt-0.5">21 Deliverables</div>
              <div class="text-[10px] text-blue-400 mt-0.5">SSB Großprojekt-Wissensdatenbank</div>
            </div>

            <div @click="activeTab = 'project'" class="p-3 rounded-xl bg-white/5 hover:bg-[#bf262e]/10 transition border border-white/10 hover:border-[#bf262e]/40 cursor-pointer">
              <div class="text-[11px] text-[#fecdd3] font-medium">Authentische WBS-Steuerung</div>
              <div class="text-xl font-extrabold text-white mt-0.5">TP1 – TP5</div>
              <div class="text-[10px] text-amber-400 mt-0.5">Vorgang 1–297 (Explore ➔ Go-Live)</div>
            </div>

            <div @click="activeTab = 'thesis'" class="p-3 rounded-xl bg-white/5 hover:bg-[#bf262e]/10 transition border border-white/10 hover:border-[#bf262e]/40 cursor-pointer">
              <div class="text-[11px] text-[#fecdd3] font-medium">Akademisches Fundament</div>
              <div class="text-xl font-extrabold text-white mt-0.5">300 ECTS</div>
              <div class="text-[10px] text-purple-400 mt-0.5">M.Sc. (1,6) + B.Sc. (3,0) Uni Stuttgart</div>
            </div>
          </div>
        </div>

        <!-- Quick Jump Navigation Grid -->
        <div class="bg-[#141414] p-6 rounded-2xl border border-white/10 shadow-sm space-y-4">
          <div class="flex items-center justify-between">
            <h3 class="text-sm font-bold text-white flex items-center space-x-2">
              <span>🧭</span>
              <span>Wissens-Module: Direktzugriff auf alle Bereiche</span>
            </h3>
            <span class="text-xs text-[#8f8888]">12 strukturierte Fachbereiche</span>
          </div>

          <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-3 text-xs">
            <button @click="activeTab = 'cv_defense'" class="p-3 text-left rounded-xl border border-red-500/30 bg-red-500/10 hover:border-red-500 transition">
              <div class="text-red-400 font-bold mb-0.5">🛡️ CV De-Risking</div>
              <div class="text-[11px] text-[#8f8888]">Ampelsystem, Pivot-Brücken & Fangfragen</div>
            </button>

            <button @click="activeTab = 'project'" class="p-3 text-left rounded-xl border border-white/10 bg-white/5 hover:border-[#bf262e] transition">
              <div class="font-bold text-white mb-0.5">🏛️ Großprojekt SSB</div>
              <div class="text-[11px] text-[#8f8888]">Greenfield, Clean Core & TP1–TP5</div>
            </button>

            <button @click="activeTab = 'solution_design'" class="p-3 text-left rounded-xl border border-white/10 bg-white/5 hover:border-[#bf262e] transition">
              <div class="font-bold text-white mb-0.5">📐 Solution Design</div>
              <div class="text-[11px] text-[#8f8888]">Trennungsrechnung, FI/CO & ACDOCA</div>
            </button>

            <button @click="activeTab = 'migration'" class="p-3 text-left rounded-xl border border-white/10 bg-white/5 hover:border-[#bf262e] transition">
              <div class="font-bold text-white mb-0.5">🔄 Datenmigration</div>
              <div class="text-[11px] text-[#8f8888]">Staging, SuSa-Abgleich & 0,00 € Konto</div>
            </button>

            <button @click="activeTab = 'tools'" class="p-3 text-left rounded-xl border border-white/10 bg-white/5 hover:border-[#bf262e] transition">
              <div class="font-bold text-white mb-0.5">🛠️ Toolchain Hub</div>
              <div class="text-[11px] text-[#8f8888]">Cloud ALM, Signavio & Enable Now</div>
            </button>

            <button @click="activeTab = 'thesis'" class="p-3 text-left rounded-xl border border-white/10 bg-white/5 hover:border-[#bf262e] transition">
              <div class="font-bold text-white mb-0.5">🎓 Masterarbeit 1,0</div>
              <div class="text-[11px] text-[#8f8888]">12 Interviews, Theorien & CSF-Matrix</div>
            </button>

            <button @click="activeTab = 'enterprise_arch'" class="p-3 text-left rounded-xl border border-white/10 bg-white/5 hover:border-[#bf262e] transition">
              <div class="font-bold text-white mb-0.5">🏛️ EAM & ITIL 4</div>
              <div class="text-[11px] text-[#8f8888]">TOGAF ADM & Datacenter One INOC</div>
            </button>

            <button @click="activeTab = 'cheatsheet'" class="p-3 text-left rounded-xl border border-white/10 bg-white/5 hover:border-[#bf262e] transition">
              <div class="font-bold text-white mb-0.5">⚡ Tech Cheatsheet</div>
              <div class="text-[11px] text-[#8f8888]">Fiori Apps, BTP Services & SQL Spickzettel</div>
            </button>

            <button @click="activeTab = 'career'" class="p-3 text-left rounded-xl border border-white/10 bg-white/5 hover:border-[#bf262e] transition">
              <div class="font-bold text-white mb-0.5">🚀 Karriere & Gehalt</div>
              <div class="text-[11px] text-[#8f8888]">Zielrollen Stuttgart & 90-Tage-Plan</div>
            </button>

            <button @click="activeTab = 'interview'" class="p-3 text-left rounded-xl border border-white/10 bg-white/5 hover:border-[#bf262e] transition">
              <div class="font-bold text-white mb-0.5">🎙️ Interview Masterclass</div>
              <div class="text-[11px] text-[#8f8888]">Pitches, STAR-Stories & 15+ Q&A</div>
            </button>

            <button @click="activeTab = 'files'" class="p-3 text-left rounded-xl border border-white/10 bg-white/5 hover:border-[#bf262e] transition">
              <div class="font-bold text-white mb-0.5">📂 Dokumenten-Vault</div>
              <div class="text-[11px] text-[#8f8888]">50+ kuratierte SSB-Originaldateien</div>
            </button>

            <button @click="activeTab = 'notebook'" class="p-3 text-left rounded-xl border border-white/10 bg-white/5 hover:border-[#bf262e] transition">
              <div class="font-bold text-white mb-0.5">📝 Mein Second Brain</div>
              <div class="text-[11px] text-[#8f8888]">Interaktives Notizbuch mit Autosave</div>
            </button>
          </div>
        </div>

      </div>
"""
