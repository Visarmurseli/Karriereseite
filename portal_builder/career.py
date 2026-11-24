# -*- coding: utf-8 -*-

def get_career(public_mode=False):
    salary_badge = "Junior & Trainee Einstieg" if public_mode else "Gehaltsziel: 55.000 € – 75.000 € (Konzern/IGM bis 75k €)"
    s_role1 = "Markt- & tarifgerechte Junior-Vergütung (IGM / TVöD)" if public_mode else "58.000 € – 75.000 € (IGM EG 12/13 / Konzern)"
    s_role2 = "Strukturiertes Trainee-Vergütungspaket (+ Weiterbildung)" if public_mode else "55.000 € – 68.000 € (+ Weiterbildungsbudget)"
    s_role3 = "Marktübliches Consulting-Einstiegspaket" if public_mode else "55.000 € – 68.000 € (Fixum + Bonus)"
    s_role4 = "Tarifliche / konzernübliche Einstiegsvergütung" if public_mode else "55.000 € – 65.000 €"
    return f"""
      <!-- ================= TAB 10: KARRIERE- & EINSTIEGSSTRATEGIE ================= -->
      <div v-show="activeTab === 'career'" class="space-y-6">
        
        <!-- Header Banner: Junior & Trainee Positioning -->
        <div class="bg-[#141414] p-6 rounded-2xl border border-white/10 shadow-sm space-y-4">
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
            <div>
              <div class="flex items-center space-x-2">
                <span class="text-xl">🎯</span>
                <h3 class="text-lg font-bold text-white">Karriere- & Einstiegsstrategie: Junior & Trainee</h3>
                <span class="px-2.5 py-0.5 rounded-full bg-[#bf262e]/20 text-[#f87171] border border-[#bf262e]/40 text-[10px] font-bold">Region Stuttgart / Ludwigsburg</span>
              </div>
              <p class="text-xs text-[#8f8888] mt-1">
                Fokussierte Zielrollen für den Berufseinstieg nach dem Masterstudium (M.Sc. 1,6 / Masterarbeit 1,0) mit 24 Monaten SSB-Großprojekterfahrung.
              </p>
            </div>
            <div class="px-3 py-1.5 rounded-xl bg-emerald-500/15 border border-emerald-500/30 text-emerald-400 text-xs font-bold whitespace-nowrap self-start sm:self-auto">
              {salary_badge}
            </div>
          </div>

          <!-- 4 Junior & Trainee Target Roles -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 pt-2">
            
            <!-- Role 1: Junior SAP Inhouse Consultant -->
            <div class="p-4 rounded-xl border border-white/10 bg-white/5 space-y-2.5 hover:border-[#bf262e]/40 transition group">
              <div class="flex justify-between items-center">
                <h4 class="font-bold text-sm text-white group-hover:text-[#bf262e] transition">1. Junior SAP Inhouse Consultant (S/4HANA & BTP)</h4>
                <span class="tag-badge bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 text-[10px]">Top Industrie Match</span>
              </div>
              <p class="text-xs text-[#c4bebe]">
                <strong class="text-white">Zielunternehmen:</strong> Industrie- und Großunternehmen (z.B. Porsche, Mercedes-Benz, Trumpf, Mahle, Festo, STIHL, EnBW).
              </p>
              <p class="text-xs text-[#c4bebe]">
                <strong class="text-white">Aufgabenbereich:</strong> Strukturierte Einarbeitung und operative Betreuung von S/4-Kernmodulen (FI/CO, MM, PM) oder Unterstützung im Bereich SAP BTP Integration und Fiori Extensions.
              </p>
              <div class="pt-2 border-t border-white/10 flex items-center justify-between text-xs">
                <span class="text-[#8f8888]">Vergütungsrahmen:</span>
                <span class="font-bold text-emerald-400">{s_role1}</span>
              </div>
            </div>

            <!-- Role 2: IT- / Management-Trainee -->
            <div class="p-4 rounded-xl border border-white/10 bg-white/5 space-y-2.5 hover:border-[#bf262e]/40 transition group">
              <div class="flex justify-between items-center">
                <h4 class="font-bold text-sm text-white group-hover:text-[#bf262e] transition">2. IT- / Management-Trainee (Enterprise ERP)</h4>
                <span class="tag-badge bg-blue-500/20 text-blue-300 border border-blue-500/30 text-[10px]">Strukturiertes Programm</span>
              </div>
              <p class="text-xs text-[#c4bebe]">
                <strong class="text-white">Zielunternehmen:</strong> Großkonzerne, Infrastruktur- und Verkehrsunternehmen mit Traineeprogrammen.
              </p>
              <p class="text-xs text-[#c4bebe]">
                <strong class="text-white">Aufgabenbereich:</strong> 12–24 Monate Rotation durch IT-Strategie, SAP-Transformation, Enterprise Architecture (EAM) und PMO zur Ausbildung künftiger Führungs- und Fachkräfte.
              </p>
              <div class="pt-2 border-t border-white/10 flex items-center justify-between text-xs">
                <span class="text-[#8f8888]">Vergütungsrahmen:</span>
                <span class="font-bold text-blue-400">{s_role2}</span>
              </div>
            </div>

            <!-- Role 3: Junior ERP / Transformation Consultant -->
            <div class="p-4 rounded-xl border border-white/10 bg-white/5 space-y-2.5 hover:border-[#bf262e]/40 transition group">
              <div class="flex justify-between items-center">
                <h4 class="font-bold text-sm text-white group-hover:text-[#bf262e] transition">3. Junior ERP Transformation Consultant (Consulting)</h4>
                <span class="tag-badge bg-[#bf262e]/20 text-[#f87171] border border-[#bf262e]/30 text-[10px]">Steile Lernkurve</span>
              </div>
              <p class="text-xs text-[#c4bebe]">
                <strong class="text-white">Zielunternehmen:</strong> MHP (Ludwigsburg!), All for One Group, msg systems, cbs, Nagarro, PwC, EY, Deloitte.
              </p>
              <p class="text-xs text-[#c4bebe]">
                <strong class="text-white">Aufgabenbereich:</strong> Unterstützung bei S/4HANA Transformationsprojekten, Prozessaufnahme in SAP Signavio, Fit-to-Standard Vorbereitung und Begleitung von Datenmigrationen.
              </p>
              <div class="pt-2 border-t border-white/10 flex items-center justify-between text-xs">
                <span class="text-[#8f8888]">Vergütungsrahmen:</span>
                <span class="font-bold text-[#f87171]">{s_role3}</span>
              </div>
            </div>

            <!-- Role 4: Junior IT-Projektmanager / IT-PMO -->
            <div class="p-4 rounded-xl border border-white/10 bg-white/5 space-y-2.5 hover:border-[#bf262e]/40 transition group">
              <div class="flex justify-between items-center">
                <h4 class="font-bold text-sm text-white group-hover:text-[#bf262e] transition">4. Junior IT-Projektmanager / IT-PMO Specialist</h4>
                <span class="tag-badge bg-amber-500/20 text-amber-300 border border-amber-500/30 text-[10px]">Projekt-Governance</span>
              </div>
              <p class="text-xs text-[#c4bebe]">
                <strong class="text-white">Zielunternehmen:</strong> Große Mittelständler und Konzerne mit Multiprojektlandschaften.
              </p>
              <p class="text-xs text-[#c4bebe]">
                <strong class="text-white">Aufgabenbereich:</strong> Unterstützung des Projektleiters bei Meilenstein-Controlling (MS Project), Status-Reporting, Risikomanagement und Tool-Governance (SAP Cloud ALM).
              </p>
              <div class="pt-2 border-t border-white/10 flex items-center justify-between text-xs">
                <span class="text-[#8f8888]">Vergütungsrahmen:</span>
                <span class="font-bold text-amber-400">{s_role4}</span>
              </div>
            </div>

          </div>
        </div>

        <!-- Warum Visar Murseli als Junior / Trainee? (Recruiter Argumentationsmatrix) -->
        <div class="bg-[#141414] p-6 rounded-2xl border border-white/10 shadow-sm space-y-4">
          <h3 class="text-base font-bold text-white flex items-center space-x-2">
            <span>💡</span>
            <span>Warum Visar Murseli? Der ideale Junior / Trainee für Ihr ERP-Team</span>
          </h3>
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
            <div class="p-4 bg-white/5 rounded-xl border border-white/10 hover:border-[#bf262e]/30 transition space-y-1.5">
              <div class="font-bold text-white flex items-center space-x-1.5">
                <span>⚡</span>
                <span>Zero Basic Ramp-up</span>
              </div>
              <p class="text-[#c4bebe] leading-relaxed">
                Während normale Absolventen oft 6 Monate Grundschulung benötigen, bringt Visar bereits 24 Monate operative Großprojekterfahrung mit (SAP Activate, Signavio, Cloud ALM, WBS-Steuerung).
              </p>
            </div>

            <div class="p-4 bg-white/5 rounded-xl border border-white/10 hover:border-[#bf262e]/30 transition space-y-1.5">
              <div class="font-bold text-white flex items-center space-x-1.5">
                <span>🎓</span>
                <span>Wissenschaftliche Tiefe (Master 1,6 / Thesis 1,0)</span>
              </div>
              <p class="text-[#c4bebe] leading-relaxed">
                Fundierte Methodenkompetenz der Uni Stuttgart: 12 Experteninterviews im Großprojekt empirisch ausgewertet. Versteht ERP-Transformationen und Plattform-Governance von Grund auf.
              </p>
            </div>

            <div class="p-4 bg-white/5 rounded-xl border border-white/10 hover:border-[#bf262e]/30 transition space-y-1.5">
              <div class="font-bold text-white flex items-center space-x-1.5">
                <span>🌱</span>
                <span>Hohe Lernbereitschaft & Teamgeist</span>
              </div>
              <p class="text-[#c4bebe] leading-relaxed">
                Visar sucht bewusst einen Junior- oder Trainee-Einstieg, um unter erfahrenen Mentoren schnell zu wachsen, Verantwortung zu übernehmen und sich langfristig zum Leistungsträger zu entwickeln.
              </p>
            </div>
          </div>
        </div>

        <!-- 30-60-90 Tage Onboarding Plan für den Berufseinstieg -->
        <div class="bg-[#141414] p-6 rounded-2xl border border-white/10 shadow-sm space-y-4">
          <div class="flex items-center justify-between">
            <h3 class="text-base font-bold text-white flex items-center space-x-2">
              <span>📅</span>
              <span>30-60-90 Tage Onboarding-Fahrplan (Junior & Trainee)</span>
            </h3>
            <span class="text-xs text-[#8f8888]">Strukturierter Start ab Tag 1</span>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
            <div class="p-4 rounded-xl bg-white/5 border border-white/10 hover:border-[#bf262e]/30 transition space-y-2">
              <div class="font-bold text-[#f87171] text-sm flex items-center justify-between">
                <span>Tag 1 bis 30</span>
                <span class="text-[10px] bg-white/10 px-2 py-0.5 rounded text-white font-normal">Orientierung</span>
              </div>
              <ul class="text-[#c4bebe] space-y-1.5 list-disc list-inside leading-relaxed">
                <li>Einarbeitung in Unternehmensabläufe, IT-Governance und Systemzugänge.</li>
                <li>Stakeholder-Kennenlernen und Vernetzung mit Mentoren und Teamkollegen.</li>
                <li>Erste Zuarbeit bei Dokumentationen, Testfällen und Bestandsaufnahmen in CALM/Signavio.</li>
              </ul>
            </div>

            <div class="p-4 rounded-xl bg-white/5 border border-white/10 hover:border-[#bf262e]/30 transition space-y-2">
              <div class="font-bold text-[#f87171] text-sm flex items-center justify-between">
                <span>Tag 31 bis 60</span>
                <span class="text-[10px] bg-white/10 px-2 py-0.5 rounded text-white font-normal">Eigenverantwortung</span>
              </div>
              <ul class="text-[#c4bebe] space-y-1.5 list-disc list-inside leading-relaxed">
                <li>Eigenständige Bearbeitung konkreter Sub-Arbeitspakete im Modulbereich.</li>
                <li>Unterstützung bei Datenbereinigungen und Feld-Mappings für die Migration.</li>
                <li>Begleitung und Protokollierung von Fit-to-Standard- und Anwender-Workshops.</li>
              </ul>
            </div>

            <div class="p-4 rounded-xl bg-white/5 border border-white/10 hover:border-[#bf262e]/30 transition space-y-2">
              <div class="font-bold text-[#f87171] text-sm flex items-center justify-between">
                <span>Tag 61 bis 90</span>
                <span class="text-[10px] bg-white/10 px-2 py-0.5 rounded text-white font-normal">Volle Produktivität</span>
              </div>
              <ul class="text-[#c4bebe] space-y-1.5 list-disc list-inside leading-relaxed">
                <li>Vollwertige Übernahme eigener Teilaufgaben im Rollout oder Projekt-PMO.</li>
                <li>Begleitung von Anwendertests (UAT) und Schulungen mit SAP Enable Now.</li>
                <li>Erstes Zwischenfazit mit Führungskraft & Vereinbarung mittelfristiger Entwicklungsziele.</li>
              </ul>
            </div>
          </div>
        </div>

      </div>
"""
