# -*- coding: utf-8 -*-

def get_dashboard(public_mode=False):
    private_quick_links = "" if public_mode else """
        <!-- Lokales Privat-Cockpit (Nur auf localhost:8085 sichtbar) -->
        <div class="bg-[#141414] p-5 rounded-2xl border border-white/10 space-y-3">
          <div class="flex items-center justify-between">
            <h3 class="text-sm font-bold text-white flex items-center gap-2">
              <span>🔒</span>
              <span>Privates Karriere-Cockpit &amp; Second Brain (Lokal)</span>
            </h3>
            <span class="status-pill status-pill-amber">Nur Localhost</span>
          </div>
          <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs">
            <button @click="selectTab('interview')" class="p-3 text-left rounded-xl border border-white/10 bg-white/5 transition">
              <div class="font-bold text-white mb-0.5">🎙️ Interview Masterclass</div>
              <div class="text-[11px] text-[#8f8888]">Pitches, STAR &amp; Q&amp;A</div>
            </button>
            <button @click="selectTab('cv_defense')" class="p-3 text-left rounded-xl border border-white/10 bg-white/5 transition">
              <div class="font-bold text-white mb-0.5">🛡️ CV De-Risking</div>
              <div class="text-[11px] text-[#8f8888]">Ampelsystem &amp; Pivot-Brücken</div>
            </button>
            <button @click="selectTab('files')" class="p-3 text-left rounded-xl border border-white/10 bg-white/5 transition">
              <div class="font-bold text-white mb-0.5">📂 Deliverables-Register</div>
              <div class="text-[11px] text-[#8f8888]">50+ Nachweis-Artefakte</div>
            </button>
            <button @click="selectTab('notebook')" class="p-3 text-left rounded-xl border border-white/10 bg-white/5 transition">
              <div class="font-bold text-white mb-0.5">📝 Second Brain &amp; RAG</div>
              <div class="text-[11px] text-[#8f8888]">Obsidian Sync &amp; FTS5</div>
            </button>
          </div>
        </div>"""

    tpl = """
      <!-- ================= TAB 1: DASHBOARD (EXECUTIVE ONE-PAGER) ================= -->
      <div v-show="activeTab === 'dashboard'" class="space-y-6">
        
        <!-- Executive Hero Section -->
        <div class="bg-[#141414] rounded-2xl p-6 lg:p-8 border border-white/10 space-y-5">
          <div class="space-y-3">
            <div class="flex flex-wrap items-center gap-2">
              <span class="status-pill status-pill-neutral">🏛️ Universität Stuttgart</span>
              <span class="status-pill status-pill-green">M.Sc. Wirtschaftsinformatik: Note 1,6 (120 ECTS)</span>
              <span class="status-pill status-pill-green">Masterarbeit: Note 1,0 (30 ECTS)</span>
              <span class="status-pill status-pill-blue">B.Sc. Note 3,0 (180 ECTS • Thesis 1,7)</span>
              <span class="status-pill status-pill-purple">TOGAF 9 ADM Zertifikat</span>
            </div>
            
            <h2 class="text-2xl sm:text-3xl font-extrabold tracking-tight text-white">
              Enterprise ERP Transformation, IT-PMO &amp; Service Operations
            </h2>

            <div class="info-callout p-4 flex items-start gap-3 text-xs sm:text-sm leading-relaxed">
              <span class="text-base shrink-0 mt-0.5">⚡</span>
              <div>
                <div class="font-bold mb-0.5" style="color: var(--ds-text)">Executive Profil</div>
                <p style="color: var(--ds-text-subtle)">
                  Wirtschaftsinformatiker (<strong>300 ECTS</strong>, M.Sc. Note <strong>1,6</strong>, Masterarbeit <strong>1,0</strong>) mit <strong>36 Monaten Enterprise-Praxiserfahrung</strong>: 24 Monate IT-PMO &amp; Lösungsdesign in der <strong>SAP S/4HANA Transformation</strong> (SSB AG bis Explore-Abschluss &amp; SDD-Freigabe) sowie 12 Monate <strong>24/7 ITIL 4 Service Operations</strong> im Rechenzentrumsbetrieb (Datacenter One).
                </p>
              </div>
            </div>

            <div class="pt-1 flex flex-wrap items-center gap-2.5">
              <button @click="selectTab('synergies')" class="px-4 py-2 rounded-lg bg-[#bf262e] hover:bg-[#cf3840] text-white text-xs font-semibold transition flex items-center space-x-2">
                <span>⚡</span>
                <span>Persönliches Stärkenprofil &amp; Synergien</span>
                <span>➔</span>
              </button>
              <button @click="selectTab('ssb')" class="px-3.5 py-2 rounded-lg bg-white/5 text-[#f0eded] text-xs font-semibold border border-white/15 transition">
                🚆 SSB S/4HANA Projekt
              </button>
              <button @click="selectTab('faq')" class="px-3.5 py-2 rounded-lg bg-white/5 text-[#f0eded] text-xs font-semibold border border-white/15 transition">
                ❓ FAQ &amp; Details
              </button>
            </div>
          </div>

          <!-- 4 Kernpfeiler (Direktzugriff auf die 4 Hauptstationen) -->
          <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 pt-1">
            <div @click="selectTab('ssb')" class="bg-white/5 transition cursor-pointer rounded-xl p-4 border border-white/10 group" style="border-top: 3px solid var(--ds-brand-bold);">
              <div class="flex items-center justify-between mb-1.5">
                <span class="status-pill status-pill-blue">1. SSB AG (24M)</span>
                <span class="text-xs font-semibold" style="color: var(--ds-text-brand)">➔</span>
              </div>
              <div class="font-bold text-sm text-white">SAP S/4HANA &amp; PMO</div>
              <div class="text-[11px] text-[#c4bebe] mt-1">Explore-Abschluss, SDD-Freigabe, Cloud ALM, Signavio &amp; FI/CO.</div>
            </div>

            <div @click="selectTab('dc1')" class="bg-white/5 transition cursor-pointer rounded-xl p-4 border border-white/10 group" style="border-top: 3px solid var(--ds-text-success);">
              <div class="flex items-center justify-between mb-1.5">
                <span class="status-pill status-pill-green">2. DC1 (12M)</span>
                <span class="text-xs font-semibold" style="color: var(--ds-text-success)">➔</span>
              </div>
              <div class="font-bold text-sm text-white">ITIL 4 Operations</div>
              <div class="text-[11px] text-[#c4bebe] mt-1">24/7 INOC Leitstand, PRTG Monitoring, SPoC &amp; HLM (100+ Systeme).</div>
            </div>

            <div @click="selectTab('master')" class="bg-white/5 transition cursor-pointer rounded-xl p-4 border border-white/10 group" style="border-top: 3px solid var(--ds-text-discovery);">
              <div class="flex items-center justify-between mb-1.5">
                <span class="status-pill status-pill-purple">3. Master (1,6)</span>
                <span class="text-xs font-semibold" style="color: var(--ds-text-discovery)">➔</span>
              </div>
              <div class="font-bold text-sm text-white">M.Sc. (120 ECTS)</div>
              <div class="text-[11px] text-[#c4bebe] mt-1">Alle 16 Module • Masterarbeit 1,0 über S/4HANA Plattformisierung.</div>
            </div>

            <div @click="selectTab('bachelor')" class="bg-white/5 transition cursor-pointer rounded-xl p-4 border border-white/10 group" style="border-top: 3px solid var(--ds-text-warning);">
              <div class="flex items-center justify-between mb-1.5">
                <span class="status-pill status-pill-amber">4. Bachelor (3,0)</span>
                <span class="text-xs font-semibold" style="color: var(--ds-text-warning)">➔</span>
              </div>
              <div class="font-bold text-sm text-white">B.Sc. (180 ECTS)</div>
              <div class="text-[11px] text-[#c4bebe] mt-1">Alle Module • Bachelorarbeit 1,7 (Low-Code), E-Business 1,0 &amp; TOGAF 9.</div>
            </div>
          </div>
        </div>

        <!-- Kompakte Werdegang-Timeline (2019–2026) -->
        <div class="bg-[#141414] p-5 sm:p-6 rounded-2xl border border-white/10 space-y-4">
          <div class="flex items-center justify-between">
            <h3 class="text-sm font-bold text-white flex items-center space-x-2">
              <span>🗓️</span>
              <span>Werdegang auf einen Blick (2019 – 2026)</span>
            </h3>
            <span class="text-[11px] text-[#8f8888]">300 ECTS + 36 Monate Praxis</span>
          </div>
          <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-3 text-xs">
            <div @click="selectTab('bachelor')" class="p-3 rounded-xl bg-white/5 border border-white/10 cursor-pointer space-y-1">
              <div class="text-[10px] font-mono font-bold text-blue-400">2019 – 2023</div>
              <div class="font-bold text-white">B.Sc. Wirtschaftsinformatik</div>
              <div class="text-[11px] text-[#8f8888]">180 ECTS (3,0) • Thesis 1,7</div>
            </div>
            <div @click="selectTab('bachelor')" class="p-3 rounded-xl bg-white/5 border border-white/10 cursor-pointer space-y-1">
              <div class="text-[10px] font-mono font-bold text-purple-400">01 / 2020</div>
              <div class="font-bold text-white">TOGAF 9 ADM</div>
              <div class="text-[11px] text-[#8f8888]">Scape Consulting Zertifikat</div>
            </div>
            <div @click="selectTab('dc1')" class="p-3 rounded-xl bg-white/5 border border-white/10 cursor-pointer space-y-1">
              <div class="text-[10px] font-mono font-bold text-emerald-400">05/2023 – 04/2024</div>
              <div class="font-bold text-white">Datacenter One (12M)</div>
              <div class="text-[11px] text-[#8f8888]">24/7 INOC &amp; ITIL 4 Operations</div>
            </div>
            <div @click="selectTab('ssb')" class="p-3 rounded-xl bg-white/5 border border-white/10 cursor-pointer space-y-1">
              <div class="text-[10px] font-mono font-bold text-[#f87171]">05/2024 – 04/2026</div>
              <div class="font-bold text-white">SSB AG S/4HANA (24M)</div>
              <div class="text-[11px] text-[#8f8888]">IT-PMO (TP5) • SDD freigegeben</div>
            </div>
            <div @click="selectTab('master')" class="p-3 rounded-xl bg-white/5 border border-white/10 cursor-pointer space-y-1">
              <div class="text-[10px] font-mono font-bold text-amber-400">2023 – 09/2026</div>
              <div class="font-bold text-white">M.Sc. Wirtschaftsinformatik</div>
              <div class="text-[11px] text-[#8f8888]">120 ECTS (1,6) • Thesis 1,0</div>
            </div>
          </div>
        </div>

        <!-- Zielrollen-Fokus (ATS Alignment) -->
        <div class="bg-[#141414] p-5 sm:p-6 rounded-2xl border border-white/10 space-y-3">
          <div class="flex items-center justify-between">
            <h3 class="text-sm font-bold text-white">🎯 Zielrollen für den Berufseinstieg (Region Stuttgart / Ludwigsburg)</h3>
            <button @click="selectTab('synergies')" class="text-xs font-semibold hover:underline" style="color: var(--ds-text-brand)">Alle Stärken ansehen ➔</button>
          </div>
          <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 text-xs">
            <div class="p-3.5 rounded-xl bg-white/5 border border-white/10">
              <div class="font-bold text-white">Junior SAP Inhouse / Transformation Consultant</div>
              <div class="text-[11px] text-[#8f8888] mt-1">S/4HANA (FI/CO/MM), Clean Core, BTP, Cloud ALM &amp; Signavio</div>
            </div>
            <div class="p-3.5 rounded-xl bg-white/5 border border-white/10">
              <div class="font-bold text-white">Junior IT-Projektmanager / IT-PMO</div>
              <div class="text-[11px] text-[#8f8888] mt-1">Multiprojektsteuerung (TP1–TP5), MS Project, Steering-Reporting</div>
            </div>
            <div class="p-3.5 rounded-xl bg-white/5 border border-white/10">
              <div class="font-bold text-white">Junior Enterprise Architect (EAM)</div>
              <div class="text-[11px] text-[#8f8888] mt-1">TOGAF 9 ADM, Schnittstellen-Governance &amp; Bimodale IT</div>
            </div>
            <div class="p-3.5 rounded-xl bg-white/5 border border-white/10">
              <div class="font-bold text-white">IT- / Management-Trainee</div>
              <div class="text-[11px] text-[#8f8888] mt-1">Rotation über IT-Strategie, ERP-Transformation &amp; Operations</div>
            </div>
          </div>
        </div>
%%PRIVATE_QUICK_LINKS%%
      </div>
"""
    return tpl.replace("%%PRIVATE_QUICK_LINKS%%", private_quick_links)
