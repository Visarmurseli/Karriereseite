# -*- coding: utf-8 -*-

def get_dashboard():
    return """
      <!-- ================= TAB 1: EXECUTIVE BRIEFING ================= -->
      <div v-show="activeTab === 'dashboard'" class="space-y-6">
        
        <!-- Hero Banner: The Strategic Triangle -->
        <div class="bg-gradient-to-r from-slate-900 via-blue-950 to-slate-900 text-white rounded-2xl p-6 lg:p-8 shadow-xl border border-blue-900/40 relative overflow-hidden">
          <div class="relative z-10 max-w-4xl space-y-4">
            <div class="flex flex-wrap items-center gap-2">
              <span class="bg-yellow-400 text-slate-950 px-2.5 py-0.5 rounded-md text-xs font-bold uppercase tracking-wider">Dein Unschlagbarer Marktwert</span>
              <span class="bg-blue-500/30 text-blue-200 border border-blue-400/30 px-2.5 py-0.5 rounded-md text-xs font-medium">Stuttgarter Straßenbahnen AG (3.700 MA)</span>
              <span class="bg-emerald-500/30 text-emerald-200 border border-emerald-400/30 px-2.5 py-0.5 rounded-md text-xs font-medium">24 Monate Greenfield S/4HANA</span>
              <span class="bg-purple-500/30 text-purple-200 border border-purple-400/30 px-2.5 py-0.5 rounded-md text-xs font-medium">Masterarbeit Note 1,0 (30 ECTS)</span>
            </div>
            
            <h2 class="text-2xl sm:text-3xl font-extrabold tracking-tight">
              Das Enterprise Knowledge & Career Operating System
            </h2>
            <p class="text-slate-300 text-xs sm:text-sm leading-relaxed">
              Dieses Wissensportal bündelt dein gesamtes universitäres und berufliches Know-how aus <strong>zwei Jahren IT-PMO Großprojekterfahrung bei der SSB</strong>, deiner <strong>mit 1,0 bewerteten Masterarbeit am Lehrstuhl von Prof. Herzwurm</strong>, deiner <strong>TOGAF-Zertifizierung</strong> und deiner <strong>Netzwerk-/Rechenzentrumspraxis bei Datacenter One</strong>. Es dient dir ab sofort als persönliche Wissensdatenbank und Navigator für deine gesamte berufliche Laufbahn.
            </p>

            <!-- 3 Pillars -->
            <div class="grid grid-cols-1 md:grid-cols-3 gap-3 pt-2">
              <div @click="activeTab = 'project'" class="bg-white/10 hover:bg-white/15 transition cursor-pointer backdrop-blur rounded-xl p-3 border border-white/10">
                <div class="text-yellow-400 font-bold text-xs uppercase flex items-center justify-between">
                  <span>1. Enterprise Praxis</span>
                  <span>➔</span>
                </div>
                <div class="font-semibold text-sm mt-1">24 Mo. IT-PMO (TP5)</div>
                <div class="text-[11px] text-slate-300 mt-1">TP1–TP5 Koordination, Lenkungsausschuss, Meilensteine, Tool-Governance (CALM, Signavio, SEN).</div>
              </div>

              <div @click="activeTab = 'thesis'" class="bg-white/10 hover:bg-white/15 transition cursor-pointer backdrop-blur rounded-xl p-3 border border-white/10">
                <div class="text-yellow-400 font-bold text-xs uppercase flex items-center justify-between">
                  <span>2. Akademische Spitze</span>
                  <span>➔</span>
                </div>
                <div class="font-semibold text-sm mt-1">Masterarbeit Note 1,0</div>
                <div class="text-[11px] text-slate-300 mt-1">126 Seiten, 12 Experteninterviews, empirisches Clean Core & Plattform-Framework.</div>
              </div>

              <div @click="activeTab = 'solution_design'" class="bg-white/10 hover:bg-white/15 transition cursor-pointer backdrop-blur rounded-xl p-3 border border-white/10">
                <div class="text-yellow-400 font-bold text-xs uppercase flex items-center justify-between">
                  <span>3. Architektur & Daten</span>
                  <span>➔</span>
                </div>
                <div class="font-semibold text-sm mt-1">Solution Design & Migration</div>
                <div class="text-[11px] text-slate-300 mt-1">Trennungsrechnung, Staging-Tabellen, SuSa-Abgleich (0,00 € Übernahmekonto), CVI & Drittsysteme.</div>
              </div>
            </div>
          </div>
          <div class="absolute right-0 top-0 bottom-0 w-1/3 bg-gradient-to-l from-blue-500/10 to-transparent pointer-events-none"></div>
        </div>

        <!-- KPI Grid -->
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div class="bg-white dark:bg-slate-900 p-4 rounded-xl border border-slate-200 dark:border-slate-800 shadow-sm">
            <div class="text-xs text-slate-500 font-medium">Praxiserfahrung SSB AG</div>
            <div class="text-xl font-bold text-slate-900 dark:text-white mt-1">24 Monate</div>
            <div class="text-xs text-emerald-600 mt-1 font-medium">01.05.2024 – 30.04.2026</div>
          </div>

          <div class="bg-white dark:bg-slate-900 p-4 rounded-xl border border-slate-200 dark:border-slate-800 shadow-sm">
            <div class="text-xs text-slate-500 font-medium">Konzern-Scope SSB</div>
            <div class="text-xl font-bold text-slate-900 dark:text-white mt-1">3.700 MA</div>
            <div class="text-xs text-blue-600 mt-1 font-medium">5 Teilprojekte (TP1–TP5)</div>
          </div>

          <div class="bg-white dark:bg-slate-900 p-4 rounded-xl border border-slate-200 dark:border-slate-800 shadow-sm">
            <div class="text-xs text-slate-500 font-medium">Masterabschluss (Uni Stuttgart)</div>
            <div class="text-xl font-bold text-slate-900 dark:text-white mt-1">M.Sc. 1,6</div>
            <div class="text-xs text-purple-600 mt-1 font-medium">Masterarbeit Note 1,0 (30 ECTS)</div>
          </div>

          <div class="bg-white dark:bg-slate-900 p-4 rounded-xl border border-slate-200 dark:border-slate-800 shadow-sm">
            <div class="text-xs text-slate-500 font-medium">Empirische Expertenbasis</div>
            <div class="text-xl font-bold text-slate-900 dark:text-white mt-1">12 Interviews</div>
            <div class="text-xs text-amber-600 mt-1 font-medium">Nowak, Nagarro Architekten, TPLs</div>
          </div>
        </div>

        <!-- Quick Jump Navigation Grid -->
        <div class="bg-white dark:bg-slate-900 p-6 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm space-y-4">
          <div class="flex items-center justify-between">
            <h3 class="text-sm font-bold text-slate-900 dark:text-white flex items-center space-x-2">
              <span>🧭</span>
              <span>Wissens-Module: Direktzugriff auf alle Bereiche</span>
            </h3>
            <span class="text-xs text-slate-400">12 strukturierte Fachbereiche</span>
          </div>

          <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-3 text-xs">
            <button @click="activeTab = 'cv_defense'" class="p-3 text-left rounded-xl border border-red-200 dark:border-red-900/60 bg-red-50/50 dark:bg-red-950/20 hover:border-red-400 transition">
              <div class="text-red-600 dark:text-red-400 font-bold mb-0.5">🛡️ CV De-Risking</div>
              <div class="text-[11px] text-slate-500">Ampelsystem, Pivot-Brücken & Fangfragen</div>
            </button>

            <button @click="activeTab = 'project'" class="p-3 text-left rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/40 hover:border-blue-500 transition">
              <div class="font-bold text-slate-900 dark:text-white mb-0.5">🏛️ Großprojekt SSB</div>
              <div class="text-[11px] text-slate-500">Greenfield, Clean Core & TP1–TP5</div>
            </button>

            <button @click="activeTab = 'solution_design'" class="p-3 text-left rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/40 hover:border-blue-500 transition">
              <div class="font-bold text-slate-900 dark:text-white mb-0.5">📐 Solution Design</div>
              <div class="text-[11px] text-slate-500">Trennungsrechnung, FI/CO & ACDOCA</div>
            </button>

            <button @click="activeTab = 'migration'" class="p-3 text-left rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/40 hover:border-blue-500 transition">
              <div class="font-bold text-slate-900 dark:text-white mb-0.5">🔄 Datenmigration</div>
              <div class="text-[11px] text-slate-500">Staging, SuSa-Abgleich & 0,00 € Konto</div>
            </button>

            <button @click="activeTab = 'tools'" class="p-3 text-left rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/40 hover:border-blue-500 transition">
              <div class="font-bold text-slate-900 dark:text-white mb-0.5">🛠️ Toolchain Hub</div>
              <div class="text-[11px] text-slate-500">Cloud ALM, Signavio & Enable Now</div>
            </button>

            <button @click="activeTab = 'thesis'" class="p-3 text-left rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/40 hover:border-blue-500 transition">
              <div class="font-bold text-slate-900 dark:text-white mb-0.5">🎓 Masterarbeit 1,0</div>
              <div class="text-[11px] text-slate-500">12 Interviews, Theorien & CSF-Matrix</div>
            </button>

            <button @click="activeTab = 'enterprise_arch'" class="p-3 text-left rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/40 hover:border-blue-500 transition">
              <div class="font-bold text-slate-900 dark:text-white mb-0.5">🏛️ EAM & ITIL 4</div>
              <div class="text-[11px] text-slate-500">TOGAF ADM & Datacenter One INOC</div>
            </button>

            <button @click="activeTab = 'cheatsheet'" class="p-3 text-left rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/40 hover:border-blue-500 transition">
              <div class="font-bold text-slate-900 dark:text-white mb-0.5">⚡ Tech Cheatsheet</div>
              <div class="text-[11px] text-slate-500">Fiori Apps, BTP Services & SQL Spickzettel</div>
            </button>

            <button @click="activeTab = 'career'" class="p-3 text-left rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/40 hover:border-blue-500 transition">
              <div class="font-bold text-slate-900 dark:text-white mb-0.5">🚀 Karriere & Gehalt</div>
              <div class="text-[11px] text-slate-500">Zielrollen Stuttgart & 90-Tage-Plan</div>
            </button>

            <button @click="activeTab = 'interview'" class="p-3 text-left rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/40 hover:border-blue-500 transition">
              <div class="font-bold text-slate-900 dark:text-white mb-0.5">🎙️ Interview Masterclass</div>
              <div class="text-[11px] text-slate-500">Pitches, STAR-Stories & 15+ Q&A</div>
            </button>

            <button @click="activeTab = 'files'" class="p-3 text-left rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/40 hover:border-blue-500 transition">
              <div class="font-bold text-slate-900 dark:text-white mb-0.5">📂 Dokumenten-Vault</div>
              <div class="text-[11px] text-slate-500">50+ kuratierte SSB-Originaldateien</div>
            </button>

            <button @click="activeTab = 'notebook'" class="p-3 text-left rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/40 hover:border-blue-500 transition">
              <div class="font-bold text-slate-900 dark:text-white mb-0.5">📝 Mein Second Brain</div>
              <div class="text-[11px] text-slate-500">Interaktives Notizbuch mit Autosave</div>
            </button>
          </div>
        </div>

      </div>
"""
