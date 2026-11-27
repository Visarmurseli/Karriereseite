# -*- coding: utf-8 -*-

def get_dashboard(public_mode=False):
    private_quick_links = "" if public_mode else """
        <!-- Lokales Privat-Cockpit (Nur auf localhost:8085 sichtbar) -->
        <div class="bento-card p-5 space-y-3">
          <div class="flex items-center justify-between gap-2 flex-wrap">
            <h3 class="text-sm font-bold flex items-center gap-2" style="color: var(--ds-text)">
              <span>🔒</span>
              <span>Privates Karriere-Cockpit &amp; Second Brain (Lokal)</span>
            </h3>
            <span class="status-pill status-pill-amber">Nur Localhost • Live Hybrid RAG</span>
          </div>
          <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 text-xs">
            <button @click="selectTab('interview')" class="bento-card bento-interactive p-3.5 text-left transition">
              <div class="font-bold mb-0.5" style="color: var(--ds-text)">🎙️ Interview Masterclass</div>
              <div class="text-[11px]" style="color: var(--ds-text-subtlest)">Pitches, STAR &amp; Q&amp;A</div>
            </button>
            <button @click="selectTab('cv_defense')" class="bento-card bento-interactive p-3.5 text-left transition">
              <div class="font-bold mb-0.5" style="color: var(--ds-text)">📄 Optimierter CV &amp; De-Risking</div>
              <div class="text-[11px]" style="color: var(--ds-text-subtlest)">DOCX/PDF-Generator &amp; Ampelsystem</div>
            </button>
            <button @click="selectTab('files')" class="bento-card bento-interactive p-3.5 text-left transition">
              <div class="font-bold mb-0.5" style="color: var(--ds-text)">📚 Fachbibliothek &amp; Artefakte</div>
              <div class="text-[11px]" style="color: var(--ds-text-subtlest)">50+ Nachweise &amp; 454+ Bücher</div>
            </button>
            <button @click="selectTab('notebook')" class="bento-card bento-interactive p-3.5 text-left transition">
              <div class="font-bold mb-0.5" style="color: var(--ds-text)">📝 Second Brain &amp; RAG</div>
              <div class="text-[11px] bento-metric" style="color: var(--ds-text-subtlest)">{{ (ragStats.total_files || 4918).toLocaleString('de-DE') }} Notizen • {{ (ragStats.ollama_vectors || 20987).toLocaleString('de-DE') }} Vektoren</div>
            </button>
          </div>
        </div>"""

    tpl = """
      <!-- ================= TAB 1: DASHBOARD (EXECUTIVE BENTO ONE-PAGER) ================= -->
      <div v-show="activeTab === 'dashboard'" class="space-y-6">
        
        <!-- Asymmetric 12-Col Bento Hero + Live Career Telemetry Ring -->
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-4 items-stretch">
          
          <!-- Left 8 Cols: Executive Hero Mesh Card -->
          <div class="lg:col-span-8 hero-mesh rounded-2xl p-6 lg:p-7 flex flex-col justify-between space-y-5">
            <div class="space-y-3.5">
              <div class="flex flex-wrap items-center gap-2">
                <span class="status-pill status-pill-neutral">🏛️ Universität Stuttgart</span>
                <span class="status-pill status-pill-green">M.Sc. Wirtschaftsinformatik: Note 1,6 (120 ECTS)</span>
                <span class="status-pill status-pill-green">Masterarbeit: Note 1,0 (30 ECTS)</span>
                <span class="status-pill status-pill-blue">B.Sc. Note 3,0 (180 ECTS • Thesis 1,7)</span>
                <span class="status-pill status-pill-purple">TOGAF 9 ADM Zertifikat</span>
              </div>
              
              <h2 class="text-2xl sm:text-3xl font-extrabold tracking-tight leading-tight" style="color: var(--ds-text)">
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
            </div>

            <div class="pt-1 flex flex-wrap items-center gap-2.5">
              <button @click="selectTab('synergies')" class="px-4 py-2 rounded-xl text-xs font-semibold transition flex items-center gap-2 btn-primary">
                <span>⚡</span>
                <span>Persönliches Stärkenprofil &amp; Synergien</span>
                <span>➔</span>
              </button>
              <button @click="selectTab('ssb')" class="px-3.5 py-2 rounded-xl border text-xs font-semibold transition hover:opacity-85" style="background: var(--ds-surface-raised); border-color: var(--ds-border); color: var(--ds-text)">
                🚆 SSB S/4HANA Projekt
              </button>
              <button @click="selectTab('faq')" class="px-3.5 py-2 rounded-xl border text-xs font-semibold transition hover:opacity-85" style="background: var(--ds-surface-raised); border-color: var(--ds-border); color: var(--ds-text)">
                ❓ FAQ &amp; Details
              </button>
              <button @click="toggleSpotlight" class="px-3 py-2 rounded-xl border text-xs font-semibold transition hover:opacity-85" style="background: var(--ds-surface-sunken); border-color: var(--ds-border); color: var(--ds-text-subtle)">
                🔍 Ctrl K
              </button>
            </div>
          </div>

          <!-- Right 4 Cols: SVG Telemetry Ring & Tabular Metrics -->
          <div class="lg:col-span-4 bento-card p-5 flex flex-col justify-between gap-4">
            <div class="flex items-center justify-between gap-3">
              <div>
                <div class="text-[11px] font-semibold uppercase tracking-wider" style="color: var(--ds-text-subtlest)">Akademische Progression</div>
                <div class="text-lg font-extrabold bento-metric mt-0.5" style="color: var(--ds-text)">M.Sc. 1,6 • +1,4 Δ</div>
                <div class="text-[11px]" style="color: var(--ds-text-success)">Masterarbeit 1,0 (Sehr Gut)</div>
              </div>
              <!-- SVG Circular Ring -->
              <svg width="64" height="64" viewBox="0 0 64 64" class="shrink-0">
                <circle cx="32" cy="32" r="26" fill="none" stroke="var(--ds-border)" stroke-width="6" />
                <circle cx="32" cy="32" r="26" fill="none" stroke="var(--ds-brand-bold)" stroke-width="6"
                        stroke-linecap="round" stroke-dasharray="163.36" stroke-dashoffset="22"
                        transform="rotate(-90 32 32)" />
                <text x="32" y="36" text-anchor="middle" font-size="13" font-weight="800" fill="var(--ds-text)">1,6</text>
              </svg>
            </div>

            <div class="grid grid-cols-2 gap-2.5 text-xs">
              <div class="p-3 rounded-xl border" style="background: var(--ds-surface-sunken); border-color: var(--ds-border)">
                <div class="text-[10px] font-semibold uppercase" style="color: var(--ds-text-subtlest)">Hochschule</div>
                <div class="text-base font-extrabold bento-metric" style="color: var(--ds-text)">300 ECTS</div>
                <div class="text-[10px]" style="color: var(--ds-text-subtle)">180 B.Sc. + 120 M.Sc.</div>
              </div>
              <div class="p-3 rounded-xl border" style="background: var(--ds-surface-sunken); border-color: var(--ds-border)">
                <div class="text-[10px] font-semibold uppercase" style="color: var(--ds-text-subtlest)">Enterprise</div>
                <div class="text-base font-extrabold bento-metric" style="color: var(--ds-text)">36 Monate</div>
                <div class="text-[10px]" style="color: var(--ds-text-subtle)">SSB 24M + DC1 12M</div>
              </div>
              <div class="p-3 rounded-xl border" style="background: var(--ds-surface-sunken); border-color: var(--ds-border)">
                <div class="text-[10px] font-semibold uppercase" style="color: var(--ds-text-subtlest)">Empirie</div>
                <div class="text-base font-extrabold bento-metric" style="color: var(--ds-text)">12 Interv.</div>
                <div class="text-[10px]" style="color: var(--ds-text-subtle)">Mayring • 126 Seiten</div>
              </div>
              <div class="p-3 rounded-xl border" style="background: var(--ds-surface-sunken); border-color: var(--ds-border)">
                <div class="text-[10px] font-semibold uppercase" style="color: var(--ds-text-subtlest)">Unternehmen</div>
                <div class="text-base font-extrabold bento-metric" style="color: var(--ds-text)">VISMUV</div>
                <div class="text-[10px]" style="color: var(--ds-text-subtle)">Gründer ab 11/2026</div>
              </div>
            </div>
          </div>
        </div>

        <!-- 5 Kernpfeiler Bento Strip (SSB, DC1, Master, Bachelor, VISMUV & Praxisprojekte) -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5 gap-3">
          <div @click="selectTab('ssb')" class="bento-card bento-interactive cursor-pointer p-4" style="border-top: 3px solid var(--ds-brand-bold) !important;">
            <div class="flex items-center justify-between mb-1.5">
              <span class="status-pill status-pill-blue">1. SSB AG (24M)</span>
              <span class="text-xs font-semibold" style="color: var(--ds-text-brand)">➔</span>
            </div>
            <div class="font-bold text-sm" style="color: var(--ds-text)">SAP S/4HANA &amp; PMO</div>
            <div class="text-[11px] mt-1 leading-relaxed" style="color: var(--ds-text-subtle)">Explore-Abschluss, SDD-Freigabe, Cloud ALM, Signavio &amp; FI/CO.</div>
          </div>

          <div @click="selectTab('dc1')" class="bento-card bento-interactive cursor-pointer p-4" style="border-top: 3px solid var(--ds-text-success) !important;">
            <div class="flex items-center justify-between mb-1.5">
              <span class="status-pill status-pill-green">2. DC1 (12M)</span>
              <span class="text-xs font-semibold" style="color: var(--ds-text-success)">➔</span>
            </div>
            <div class="font-bold text-sm" style="color: var(--ds-text)">ITIL 4 Operations</div>
            <div class="text-[11px] mt-1 leading-relaxed" style="color: var(--ds-text-subtle)">24/7 INOC Leitstand, PRTG Monitoring, SPoC &amp; HLM (100+ Systeme).</div>
          </div>

          <div @click="selectTab('master')" class="bento-card bento-interactive cursor-pointer p-4" style="border-top: 3px solid var(--ds-text-discovery) !important;">
            <div class="flex items-center justify-between mb-1.5">
              <span class="status-pill status-pill-purple">3. Master (1,6)</span>
              <span class="text-xs font-semibold" style="color: var(--ds-text-discovery)">➔</span>
            </div>
            <div class="font-bold text-sm" style="color: var(--ds-text)">M.Sc. (120 ECTS)</div>
            <div class="text-[11px] mt-1 leading-relaxed" style="color: var(--ds-text-subtle)">Alle 16 Module • Masterarbeit 1,0 über S/4HANA Plattformisierung.</div>
          </div>

          <div @click="selectTab('bachelor')" class="bento-card bento-interactive cursor-pointer p-4" style="border-top: 3px solid var(--ds-text-warning) !important;">
            <div class="flex items-center justify-between mb-1.5">
              <span class="status-pill status-pill-amber">4. Bachelor (3,0)</span>
              <span class="text-xs font-semibold" style="color: var(--ds-text-warning)">➔</span>
            </div>
            <div class="font-bold text-sm" style="color: var(--ds-text)">B.Sc. (180 ECTS)</div>
            <div class="text-[11px] mt-1 leading-relaxed" style="color: var(--ds-text-subtle)">Alle Module • Bachelorarbeit 1,7 (Low-Code), E-Business 1,0 &amp; TOGAF 9.</div>
          </div>

          <div @click="selectTab('synergies')" class="bento-card bento-interactive cursor-pointer p-4" style="border-top: 3px solid #06B6D4 !important;">
            <div class="flex items-center justify-between mb-1.5">
              <span class="status-pill status-pill-neutral">5. Praxis &amp; Ops</span>
              <span class="text-xs font-semibold" style="color: var(--ds-text-brand)">➔</span>
            </div>
            <div class="font-bold text-sm" style="color: var(--ds-text)">VISMUV &amp; Projekte</div>
            <div class="text-[11px] mt-1 leading-relaxed" style="color: var(--ds-text-subtle)">Schmalz RPA (1,0), Klingele SaaS (2,0), PDR Ops &amp; VISMUV (11/2026).</div>
          </div>
        </div>

        <!-- Kompakte Werdegang-Timeline (2019–2026) -->
        <div class="bento-card p-5 sm:p-6 space-y-4">
          <div class="flex items-center justify-between flex-wrap gap-2">
            <h3 class="text-sm font-bold flex items-center gap-2" style="color: var(--ds-text)">
              <span>🗓️</span>
              <span>Werdegang auf einen Blick (2019 – 2026)</span>
            </h3>
            <span class="status-pill status-pill-blue">300 ECTS + 36 Monate Praxis</span>
          </div>
          <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3 text-xs">
            <div @click="selectTab('bachelor')" class="bento-card bento-interactive p-3 cursor-pointer space-y-1">
              <div class="text-[10px] font-mono font-bold" style="color: var(--ds-text-brand)">2019 – 2023</div>
              <div class="font-bold" style="color: var(--ds-text)">B.Sc. Wirtschaftsinformatik</div>
              <div class="text-[11px]" style="color: var(--ds-text-subtlest)">180 ECTS (3,0) • Thesis 1,7</div>
            </div>
            <div @click="selectTab('bachelor')" class="bento-card bento-interactive p-3 cursor-pointer space-y-1">
              <div class="text-[10px] font-mono font-bold" style="color: var(--ds-text-discovery)">01 / 2020</div>
              <div class="font-bold" style="color: var(--ds-text)">TOGAF 9 ADM</div>
              <div class="text-[11px]" style="color: var(--ds-text-subtlest)">Scape Consulting Zertifikat</div>
            </div>
            <div @click="selectTab('dc1')" class="bento-card bento-interactive p-3 cursor-pointer space-y-1">
              <div class="text-[10px] font-mono font-bold" style="color: var(--ds-text-success)">05/2023 – 04/2024</div>
              <div class="font-bold" style="color: var(--ds-text)">Datacenter One (12M)</div>
              <div class="text-[11px]" style="color: var(--ds-text-subtlest)">24/7 INOC &amp; ITIL 4 Operations</div>
            </div>
            <div @click="selectTab('ssb')" class="bento-card bento-interactive p-3 cursor-pointer space-y-1">
              <div class="text-[10px] font-mono font-bold" style="color: var(--ds-text-brand)">05/2024 – 04/2026</div>
              <div class="font-bold" style="color: var(--ds-text)">SSB AG S/4HANA (24M)</div>
              <div class="text-[11px]" style="color: var(--ds-text-subtlest)">IT-PMO (TP5) • SDD freigegeben</div>
            </div>
            <div @click="selectTab('master')" class="bento-card bento-interactive p-3 cursor-pointer space-y-1">
              <div class="text-[10px] font-mono font-bold" style="color: var(--ds-text-warning)">2023 – 09/2026</div>
              <div class="font-bold" style="color: var(--ds-text)">M.Sc. Wirtschaftsinformatik</div>
              <div class="text-[11px]" style="color: var(--ds-text-subtlest)">120 ECTS (1,6) • Thesis 1,0</div>
            </div>
            <div @click="selectTab('synergies')" class="bento-card bento-interactive p-3 cursor-pointer space-y-1">
              <div class="text-[10px] font-mono font-bold" style="color: var(--ds-text-success)">09 – 11/2026+</div>
              <div class="font-bold" style="color: var(--ds-text)">PDR Team &amp; VISMUV</div>
              <div class="text-[11px]" style="color: var(--ds-text-subtlest)">Scanning/Ops • Gründung 11/2026</div>
            </div>
          </div>
        </div>

        <!-- Zielrollen-Fokus (ATS Alignment) -->
        <div class="bento-card p-5 sm:p-6 space-y-3">
          <div class="flex items-center justify-between flex-wrap gap-2">
            <h3 class="text-sm font-bold" style="color: var(--ds-text)">🎯 Zielrollen für den Berufseinstieg (Region Stuttgart / Ludwigsburg)</h3>
            <button @click="selectTab('synergies')" class="text-xs font-semibold hover:underline" style="color: var(--ds-text-brand)">Alle Stärken ansehen ➔</button>
          </div>
          <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 text-xs">
            <div @click="selectTab('ssb')" class="bento-card bento-interactive cursor-pointer p-3.5">
              <div class="font-bold" style="color: var(--ds-text)">Junior SAP Inhouse / Transformation Consultant</div>
              <div class="text-[11px] mt-1" style="color: var(--ds-text-subtlest)">S/4HANA (FI/CO/MM), Clean Core, BTP, Cloud ALM &amp; Signavio</div>
            </div>
            <div @click="selectTab('ssb')" class="bento-card bento-interactive cursor-pointer p-3.5">
              <div class="font-bold" style="color: var(--ds-text)">Junior IT-Projektmanager / IT-PMO</div>
              <div class="text-[11px] mt-1" style="color: var(--ds-text-subtlest)">Multiprojektsteuerung (TP1–TP5), MS Project, Steering-Reporting</div>
            </div>
            <div @click="selectTab('master')" class="bento-card bento-interactive cursor-pointer p-3.5">
              <div class="font-bold" style="color: var(--ds-text)">Junior Enterprise Architect (EAM)</div>
              <div class="text-[11px] mt-1" style="color: var(--ds-text-subtlest)">TOGAF 9 ADM, Schnittstellen-Governance &amp; Bimodale IT</div>
            </div>
            <div @click="selectTab('dc1')" class="bento-card bento-interactive cursor-pointer p-3.5">
              <div class="font-bold" style="color: var(--ds-text)">IT- / Management-Trainee</div>
              <div class="text-[11px] mt-1" style="color: var(--ds-text-subtlest)">Rotation über IT-Strategie, ERP-Transformation &amp; Operations</div>
            </div>
          </div>
        </div>
%%PRIVATE_QUICK_LINKS%%
      </div>
"""
    return tpl.replace("%%PRIVATE_QUICK_LINKS%%", private_quick_links)
