# -*- coding: utf-8 -*-

def get_dashboard(public_mode=False):
    dossier_target = "thesis" if public_mode else "notebook"
    files_target = "tools" if public_mode else "files"
    career_sub = "Junior & Trainee Einstieg" if public_mode else "Junior & Trainee (55k–75k €)"
    private_cards = "" if public_mode else """
            <button @click="activeTab = 'interview'" class="p-3 text-left rounded-xl border border-white/10 bg-white/5 hover:border-[#bf262e] transition">
              <div class="font-bold text-white mb-0.5">🎙️ Interview Masterclass</div>
              <div class="text-[11px] text-[#8f8888]">Pitches, STAR-Stories & 40+ Q&A</div>
            </button>

            <button @click="activeTab = 'cv_defense'" class="p-3 text-left rounded-xl border border-white/10 bg-white/5 hover:border-[#bf262e] transition">
              <div class="font-bold text-white mb-0.5">🛡️ CV De-Risking</div>
              <div class="text-[11px] text-[#8f8888]">Ampelsystem & Pivot-Brücken</div>
            </button>"""
    private_tail_cards = "" if public_mode else """
            <button @click="activeTab = 'files'" class="p-3 text-left rounded-xl border border-white/10 bg-white/5 hover:border-[#bf262e] transition">
              <div class="font-bold text-white mb-0.5">📂 Deliverables-Register</div>
              <div class="text-[11px] text-[#8f8888]">50+ kuratierte Nachweis-Akten</div>
            </button>

            <button @click="activeTab = 'notebook'" class="p-3 text-left rounded-xl border border-white/10 bg-white/5 hover:border-[#bf262e] transition">
              <div class="font-bold text-white mb-0.5">📝 Second Brain & RAG</div>
              <div class="text-[11px] text-[#8f8888]">Local RAG Suche & Obsidian Sync</div>
            </button>"""
    return f"""
      <!-- ================= TAB 1: WISSENSDATENBANK ÜBERSICHT ================= -->
      <div v-show="activeTab === 'dashboard'" class="space-y-6">
        
        <!-- Hero Banner: Objektive Wissensdatenbank-Übersicht -->
        <div class="bg-gradient-to-br from-[#181818] via-[#141414] to-[#1a1213] text-white rounded-2xl p-6 lg:p-8 shadow-xl border border-white/10 relative overflow-hidden">
          <div class="relative z-10 max-w-5xl space-y-4">
            
            <!-- Objective Credentials Badges -->
            <div class="flex flex-wrap items-center gap-2 text-xs">
              <span class="bg-white/10 text-white px-2.5 py-1 rounded-lg font-medium border border-white/15">
                🏛️ Universität Stuttgart
              </span>
              <span class="bg-emerald-500/15 text-emerald-300 border border-emerald-500/30 px-2.5 py-1 rounded-lg font-medium">
                M.Sc. Wirtschaftsinformatik: Note 1,6 (120 ECTS)
              </span>
              <span class="bg-emerald-500/25 text-emerald-200 border border-emerald-500/40 px-2.5 py-1 rounded-lg font-bold">
                Masterarbeit: Note 1,0 (30 ECTS)
              </span>
              <span class="bg-blue-500/15 text-blue-300 border border-blue-500/30 px-2.5 py-1 rounded-lg font-medium">
                B.Sc. Wirtschaftsinformatik: Note 3,0 (180 ECTS)
              </span>
              <span class="bg-blue-500/25 text-blue-200 border border-blue-500/40 px-2.5 py-1 rounded-lg font-bold">
                Bachelorarbeit: Note 1,7 (12 ECTS)
              </span>
            </div>
            
            <h2 class="text-2xl sm:text-3xl font-extrabold tracking-tight text-white">
              Persönliche Wissensdatenbank: Akademisches & Berufliches Fundament
            </h2>
            <p class="text-[#c4bebe] text-xs sm:text-sm leading-relaxed">
              Dieses Wissensportal bündelt alle Unterlagen, Projekt-Deliverables und theoretischen Grundlagen aus meinem Werdegang als Wirtschaftsinformatiker: <strong>300 ECTS universitäre Ausbildung an der Universität Stuttgart</strong> (Master & Bachelor), <strong>24 Monate Großprojekterfahrung bei der Stuttgarter Straßenbahnen AG</strong> (S/4HANA Transformation bis zum Abschluss der Explore-Phase), <strong>12 Monate ITIL 4 Service Operations bei Datacenter One</strong> sowie die <strong>TOGAF 9 ADM-Zertifizierung</strong>.
            </p>
            <div class="pt-1 flex flex-wrap items-center gap-2.5">
              <button @click="activeTab = 'synergies'" class="px-4 py-2 rounded-xl bg-[#bf262e] hover:bg-[#cf3840] text-white text-xs font-bold shadow-lg shadow-[#bf262e]/30 border border-white/15 transition flex items-center space-x-2">
                <span>⚡</span>
                <span>Persönliches Stärkenprofil & 6 Arbeit × Uni Synergien entdecken</span>
                <span>➔</span>
              </button>
              <button @click="activeTab = 'career'" class="px-3.5 py-2 rounded-xl bg-white/5 hover:bg-white/10 text-[#f0eded] text-xs font-semibold border border-white/15 transition">
                🎯 Zielrollen & Roadmap
              </button>
            </div>

            <!-- 4 Equal Pillars of Knowledge -->
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 pt-2">
              
              <!-- Pillar 1: SSB S/4HANA Transformation -->
              <div @click="activeTab = 'project'" class="bg-white/5 hover:bg-[#bf262e]/15 transition cursor-pointer rounded-xl p-3.5 border border-white/10 hover:border-[#bf262e]/50 group">
                <div class="text-[#f87171] font-bold text-xs uppercase flex items-center justify-between">
                  <span>1. S/4HANA Transformation</span>
                  <span class="group-hover:translate-x-1 transition">➔</span>
                </div>
                <div class="font-semibold text-sm mt-1 text-white">SSB AG (24 Monate)</div>
                <div class="text-[11px] text-[#c4bebe] mt-1">Stand bei Austritt: Explore-Phase abgeschlossen, Solution Design Document (SDD) vollständig genehmigt.</div>
              </div>

              <!-- Pillar 2: Datacenter One ITIL Operations -->
              <div @click="activeTab = 'enterprise_arch'" class="bg-white/5 hover:bg-[#bf262e]/15 transition cursor-pointer rounded-xl p-3.5 border border-white/10 hover:border-[#bf262e]/50 group">
                <div class="text-[#f87171] font-bold text-xs uppercase flex items-center justify-between">
                  <span>2. IT-Operations & RZ</span>
                  <span class="group-hover:translate-x-1 transition">➔</span>
                </div>
                <div class="font-semibold text-sm mt-1 text-white">Datacenter One (12 Monate)</div>
                <div class="text-[11px] text-[#c4bebe] mt-1">24/7 INOC Leitstand, ITIL 4 Incident Management, Confluence SOPs, PRTG Monitoring & HLM.</div>
              </div>

              <!-- Pillar 3: Masterstudium & Forschung -->
              <div @click="activeTab = 'thesis'" class="bg-white/5 hover:bg-[#bf262e]/15 transition cursor-pointer rounded-xl p-3.5 border border-white/10 hover:border-[#bf262e]/50 group">
                <div class="text-[#f87171] font-bold text-xs uppercase flex items-center justify-between">
                  <span>3. Masterstudium (1,6)</span>
                  <span class="group-hover:translate-x-1 transition">➔</span>
                </div>
                <div class="font-semibold text-sm mt-1 text-white">M.Sc. Uni Stuttgart</div>
                <div class="text-[11px] text-[#c4bebe] mt-1">Masterarbeit Note 1,0 (12 Interviews, Mayring), Digitale Nachhaltigkeit (1,0), Advanced SE (1,6).</div>
              </div>

              <!-- Pillar 4: Bachelorstudium & Methoden -->
              <div @click="activeTab = 'thesis'" class="bg-white/5 hover:bg-[#bf262e]/15 transition cursor-pointer rounded-xl p-3.5 border border-white/10 hover:border-[#bf262e]/50 group">
                <div class="text-[#f87171] font-bold text-xs uppercase flex items-center justify-between">
                  <span>4. Bachelorstudium (3,0)</span>
                  <span class="group-hover:translate-x-1 transition">➔</span>
                </div>
                <div class="font-semibold text-sm mt-1 text-white">B.Sc. Uni Stuttgart</div>
                <div class="text-[11px] text-[#c4bebe] mt-1">Bachelorarbeit Note 1,7 (Low-Code), E-Business (1,0), Unternehmensanalyse (2,3), BPMN 2.0 & SQL.</div>
              </div>

            </div>
          </div>
        </div>

        <!-- Objective Key Metrics Grid -->
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div class="bg-[#141414] p-4 rounded-xl border border-white/10 hover:border-[#bf262e]/40 transition shadow-sm">
            <div class="text-xs text-[#8f8888] font-medium">Akademisches Gesamtvolumen</div>
            <div class="text-xl font-bold text-white mt-1">300 ECTS</div>
            <div class="text-xs text-purple-400 mt-1 font-medium">M.Sc. (120) + B.Sc. (180)</div>
          </div>

          <div class="bg-[#141414] p-4 rounded-xl border border-white/10 hover:border-[#bf262e]/40 transition shadow-sm">
            <div class="text-xs text-[#8f8888] font-medium">Berufliche Praxiserfahrung</div>
            <div class="text-xl font-bold text-white mt-1">36 Monate</div>
            <div class="text-xs text-emerald-400 mt-1 font-medium">24M SSB AG + 12M DC1</div>
          </div>

          <div class="bg-[#141414] p-4 rounded-xl border border-white/10 hover:border-[#bf262e]/40 transition shadow-sm">
            <div class="text-xs text-[#8f8888] font-medium">Empirische Expertenbasis</div>
            <div class="text-xl font-bold text-white mt-1">12 Interviews</div>
            <div class="text-xs text-amber-400 mt-1 font-medium">Gesamt-PL, TPLs, Lead Architects</div>
          </div>

          <div class="bg-[#141414] p-4 rounded-xl border border-white/10 hover:border-[#bf262e]/40 transition shadow-sm">
            <div class="text-xs text-[#8f8888] font-medium">Enterprise Architektur</div>
            <div class="text-xl font-bold text-white mt-1">TOGAF 9 ADM</div>
            <div class="text-xs text-blue-400 mt-1 font-medium">Zertifiziert bei Scape Consulting</div>
          </div>
        </div>

        <!-- Knowledge Graph & Ecosystem Telemetry Bar -->
        <div class="bg-[#141414] p-5 rounded-2xl border border-white/10 text-white shadow-lg space-y-3">
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
            <div class="flex items-center space-x-2">
              <span class="text-lg">🧠</span>
              <div>
                <h4 class="text-sm font-bold tracking-tight text-white flex items-center gap-2">
                  <span>Wissensgraph & Second Brain Index</span>
                  <span class="px-2 py-0.5 rounded-full bg-white/10 text-[#c4bebe] text-[10px] font-mono">Obsidian & Notizdatenbank</span>
                </h4>
                <p class="text-[11px] text-[#8f8888]">Strukturierte Text-Dossiers und Querverbindungen über alle beruflichen und akademischen Unterlagen.</p>
              </div>
            </div>
            <button @click="openCommandPalette" class="self-start sm:self-auto px-3 py-1.5 rounded-lg bg-[#bf262e] hover:bg-[#cf3840] text-white text-xs font-semibold flex items-center space-x-1.5 transition shadow-md shadow-[#bf262e]/30">
              <span>⚡ Schnellsuche öffnen</span>
              <kbd class="px-1 py-0.5 bg-black/40 rounded text-[9px] font-mono">Ctrl K</kbd>
            </button>
          </div>

          <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 pt-1">
            <div @click="activeTab = '{dossier_target}'" class="p-3 rounded-xl bg-white/5 hover:bg-[#bf262e]/10 transition border border-white/10 hover:border-[#bf262e]/40 cursor-pointer">
              <div class="text-[11px] text-[#8f8888] font-medium">Obsidian Text-Dossiers</div>
              <div class="text-xl font-extrabold text-white mt-0.5">53 Dossiers</div>
              <div class="text-[10px] text-emerald-400 mt-0.5">266 bidirektionale Links</div>
            </div>

            <div @click="activeTab = '{files_target}'" class="p-3 rounded-xl bg-white/5 hover:bg-[#bf262e]/10 transition border border-white/10 hover:border-[#bf262e]/40 cursor-pointer">
              <div class="text-[11px] text-[#8f8888] font-medium">Kuratierte Dokumente</div>
              <div class="text-xl font-extrabold text-white mt-0.5">21 Deliverables</div>
              <div class="text-[10px] text-blue-400 mt-0.5">SSB Großprojekt-Artefakte</div>
            </div>

            <div @click="activeTab = 'project'" class="p-3 rounded-xl bg-white/5 hover:bg-[#bf262e]/10 transition border border-white/10 hover:border-[#bf262e]/40 cursor-pointer">
              <div class="text-[11px] text-[#8f8888] font-medium">SSB S/4HANA Steuerung</div>
              <div class="text-xl font-extrabold text-white mt-0.5">TP1 – TP5</div>
              <div class="text-[10px] text-amber-400 mt-0.5">Ende Explore / SDD vollständig</div>
            </div>

            <div @click="activeTab = 'thesis'" class="p-3 rounded-xl bg-white/5 hover:bg-[#bf262e]/10 transition border border-white/10 hover:border-[#bf262e]/40 cursor-pointer">
              <div class="text-[11px] text-[#8f8888] font-medium">Akademisches Curriculum</div>
              <div class="text-xl font-extrabold text-white mt-0.5">300 ECTS</div>
              <div class="text-[10px] text-purple-400 mt-0.5">M.Sc. (1,6) + B.Sc. (3,0)</div>
            </div>
          </div>
        </div>

        <!-- Schnellzugriff auf alle Wissensbereiche (11 Module) -->
        <div class="bg-[#141414] p-6 rounded-2xl border border-white/10 shadow-sm space-y-4">
          <div class="flex items-center justify-between">
            <h3 class="text-sm font-bold text-white flex items-center space-x-2">
              <span>🧭</span>
              <span>Direktzugriff auf alle Fach- und Wissensmodule</span>
            </h3>
            <span class="text-xs text-[#8f8888]">11 Themenbereiche</span>
          </div>

          <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-3 text-xs">
            <button @click="activeTab = 'project'" class="p-3 text-left rounded-xl border border-white/10 bg-white/5 hover:border-[#bf262e] transition">
              <div class="font-bold text-white mb-0.5">🚆 SSB S/4HANA</div>
              <div class="text-[11px] text-[#8f8888]">Ende Explore, SDD & TP1–TP5</div>
            </button>

            <button @click="activeTab = 'enterprise_arch'" class="p-3 text-left rounded-xl border border-white/10 bg-white/5 hover:border-[#bf262e] transition">
              <div class="font-bold text-white mb-0.5">🖥️ Datacenter One (DC1)</div>
              <div class="text-[11px] text-[#8f8888]">ITIL 4, 24/7 Monitoring & Confluence</div>
            </button>

            <button @click="activeTab = 'solution_design'" class="p-3 text-left rounded-xl border border-white/10 bg-white/5 hover:border-[#bf262e] transition">
              <div class="font-bold text-white mb-0.5">📐 Solution Design</div>
              <div class="text-[11px] text-[#8f8888]">Trennungsrechnung, FI/CO & ACDOCA</div>
            </button>

            <button @click="activeTab = 'migration'" class="p-3 text-left rounded-xl border border-white/10 bg-white/5 hover:border-[#bf262e] transition">
              <div class="font-bold text-white mb-0.5">🔄 Datenmigration</div>
              <div class="text-[11px] text-[#8f8888]">LTMC Staging & 0,00 € Konto</div>
            </button>

            <button @click="activeTab = 'tools'" class="p-3 text-left rounded-xl border border-white/10 bg-white/5 hover:border-[#bf262e] transition">
              <div class="font-bold text-white mb-0.5">🛠️ Toolchain Hub</div>
              <div class="text-[11px] text-[#8f8888]">Cloud ALM, Signavio & Enable Now</div>
            </button>

            <button @click="activeTab = 'thesis'" class="p-3 text-left rounded-xl border border-white/10 bg-white/5 hover:border-[#bf262e] transition">
              <div class="font-bold text-white mb-0.5">🎓 Master & Bachelor</div>
              <div class="text-[11px] text-[#8f8888]">300 ECTS, Arbeiten & Projekte</div>
            </button>
{private_cards}
            <button @click="activeTab = 'career'" class="p-3 text-left rounded-xl border border-white/10 bg-white/5 hover:border-[#bf262e] transition">
              <div class="font-bold text-white mb-0.5">🎯 Einstiegsstrategie</div>
              <div class="text-[11px] text-[#8f8888]">{career_sub}</div>
            </button>
{private_tail_cards}
          </div>
        </div>

      </div>
"""
