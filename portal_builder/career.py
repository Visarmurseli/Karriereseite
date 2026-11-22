# -*- coding: utf-8 -*-

def get_career():
    return """
      <!-- ================= TAB 10: KARRIERE- & ZUKUNFTSSTRATEGIE ================= -->
      <div v-show="activeTab === 'career'" class="space-y-6">
        <div class="bg-white dark:bg-slate-900 p-6 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm space-y-4">
          <h3 class="text-lg font-bold text-slate-900 dark:text-white">Karriere- & Positionierungsstrategie Region Stuttgart / Ludwigsburg</h3>
          <p class="text-xs text-slate-500">Optimale Zielrollen, Gehaltsbandbreiten und strategischer 90-Tage-Fahrplan</p>

          <!-- 4 Target Roles -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 pt-2">
            <div class="p-4 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/40 space-y-2">
              <div class="flex justify-between items-center">
                <h4 class="font-bold text-sm text-slate-900 dark:text-white">1. SAP Inhouse Consultant (S/4HANA & BTP)</h4>
                <span class="tag-badge bg-emerald-100 text-emerald-800 text-[10px]">Top Match Industrie</span>
              </div>
              <p class="text-xs text-slate-600 dark:text-slate-300">
                <strong>Unternehmen:</strong> Porsche, Bosch, Mercedes-Benz, Trumpf, Mahle, Festo, EnBW.
              </p>
              <p class="text-xs text-slate-600 dark:text-slate-300">
                <strong>Rolle:</strong> Betreuung und Weiterentwicklung der S/4-Kernmodule (FI/CO, MM, PM) oder als BTP Solution Architect.
              </p>
              <div class="text-xs font-semibold text-emerald-600 dark:text-emerald-400">Gehaltsspanne: 68.000 € – 80.000 € (EG 12 / IGM EG 14-15)</div>
            </div>

            <div class="p-4 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/40 space-y-2">
              <div class="flex justify-between items-center">
                <h4 class="font-bold text-sm text-slate-900 dark:text-white">2. ERP Management Consultant (Big 4 / IT-Boutique)</h4>
                <span class="tag-badge bg-blue-100 text-blue-800 text-[10px]">Steile Lernkurve</span>
              </div>
              <p class="text-xs text-slate-600 dark:text-slate-300">
                <strong>Unternehmen:</strong> MHP (Ludwigsburg!), All for One Group, msg systems, cbs, Nagarro, PwC, EY, Deloitte.
              </p>
              <p class="text-xs text-slate-600 dark:text-slate-300">
                <strong>Rolle:</strong> Berater für S/4HANA Transformationen, Fit-to-Standard Moderation, Process Mining mit Signavio.
              </p>
              <div class="text-xs font-semibold text-blue-600 dark:text-blue-400">Gehaltsspanne: 68.000 € – 82.000 € (Fixum + variabler Bonus)</div>
            </div>

            <div class="p-4 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/40 space-y-2">
              <div class="flex justify-between items-center">
                <h4 class="font-bold text-sm text-slate-900 dark:text-white">3. Enterprise Data & Migration Lead</h4>
                <span class="tag-badge bg-purple-100 text-purple-800 text-[10px]">Spezialisten-Rolle</span>
              </div>
              <p class="text-xs text-slate-600 dark:text-slate-300">
                <strong>Unternehmen:</strong> Großunternehmen in der S/4-Planung oder Beratungsfirmen mit Migration-Practice.
              </p>
              <p class="text-xs text-slate-600 dark:text-slate-300">
                <strong>Rolle:</strong> Leitung von Migrationsprojekten, Konzeption von Staging-Pipelines, CVI-Harmonisierung.
              </p>
              <div class="text-xs font-semibold text-purple-600 dark:text-purple-400">Gehaltsspanne: 70.000 € – 85.000 €</div>
            </div>

            <div class="p-4 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/40 space-y-2">
              <div class="flex justify-between items-center">
                <h4 class="font-bold text-sm text-slate-900 dark:text-white">4. Transformation PMO Lead / Project Manager</h4>
                <span class="tag-badge bg-amber-100 text-amber-800 text-[10px]">Management Track</span>
              </div>
              <p class="text-xs text-slate-600 dark:text-slate-300">
                <strong>Unternehmen:</strong> Konzerne und große Mittelständler mit Multiprojektlandschaften.
              </p>
              <p class="text-xs text-slate-600 dark:text-slate-300">
                <strong>Rolle:</strong> Steuerung von Großprojekten, Budget-, Termin- und Risikocontrolling, C-Level Reporting.
              </p>
              <div class="text-xs font-semibold text-amber-600 dark:text-amber-400">Gehaltsspanne: 66.000 € – 78.000 €</div>
            </div>
          </div>
        </div>

        <!-- Gehaltsverhandlung & Argumentationsmatrix -->
        <div class="bg-white dark:bg-slate-900 p-6 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm space-y-4">
          <h3 class="text-base font-bold text-slate-900 dark:text-white flex items-center space-x-2">
            <span>💰</span>
            <span>Deine Argumentationsmatrix für die Gehaltsverhandlung</span>
          </h3>
          <div class="grid grid-cols-1 md:grid-cols-3 gap-3 text-xs">
            <div class="p-3 bg-slate-50 dark:bg-slate-800/40 rounded-xl border border-slate-200 dark:border-slate-700">
              <div class="font-bold text-slate-900 dark:text-white mb-1">1. Qualifikation (M.Sc. 1,6 / Thesis 1,0)</div>
              <p class="text-slate-600 dark:text-slate-300">
                Abgeschlossener Master in Wirtschaftsinformatik an einer forschungsstarken Universität (Stuttgart). Formal sauber eingestuft in EG 12 (TV-N/TVöD) bzw. gehobener IT-Tarif.
              </p>
            </div>
            <div class="p-3 bg-slate-50 dark:bg-slate-800/40 rounded-xl border border-slate-200 dark:border-slate-700">
              <div class="font-bold text-slate-900 dark:text-white mb-1">2. Zero Ramp-up Time</div>
              <p class="text-slate-600 dark:text-slate-300">
                Ein normaler Absolvent kostet 6 Monate Einarbeitung. Du beherrschst SAP Activate, CALM, Signavio und Migrations-Mechaniken ab dem ersten Tag und generierst sofort produktiven ROI.
              </p>
            </div>
            <div class="p-3 bg-slate-50 dark:bg-slate-800/40 rounded-xl border border-slate-200 dark:border-slate-700">
              <div class="font-bold text-slate-900 dark:text-white mb-1">3. Mangel an S/4-Spezialisten</div>
              <p class="text-slate-600 dark:text-slate-300">
                Bis 2027/2030 müssen tausende Unternehmen auf S/4HANA migrieren. Kandidaten, die Clean Core und Plattformisierung wissenschaftlich und operativ verstehen, sind extrem rar gesät.
              </p>
            </div>
          </div>
        </div>

        <!-- 30-60-90 Tage Onboarding Plan -->
        <div class="bg-white dark:bg-slate-900 p-6 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm space-y-4">
          <h3 class="text-base font-bold text-slate-900 dark:text-white">Dein 30-60-90 Tage Plan für den neuen Arbeitgeber</h3>
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
            <div class="p-4 rounded-xl bg-slate-50 dark:bg-slate-800/40 border border-slate-200 dark:border-slate-700">
              <div class="font-bold text-blue-600 text-sm mb-1">Tag 1 bis 30: Orientierung & Quick Wins</div>
              <ul class="text-slate-600 dark:text-slate-300 space-y-1.5 list-disc list-inside">
                <li>Systemlandschaft und Schnittstellen spiegeln.</li>
                <li>Stakeholder-Interviews führen und operative Schmerzpunkte identifizieren.</li>
                <li>Erste Prozessdokumentationen und Testfälle in CALM/Signavio aufsetzen.</li>
              </ul>
            </div>
            <div class="p-4 rounded-xl bg-slate-50 dark:bg-slate-800/40 border border-slate-200 dark:border-slate-700">
              <div class="font-bold text-blue-600 text-sm mb-1">Tag 31 bis 60: Eigenverantwortung</div>
              <ul class="text-slate-600 dark:text-slate-300 space-y-1.5 list-disc list-inside">
                <li>Eigenständige Betreuung eines Modulbereichs oder Teilprojekts.</li>
                <li>Konzeption von Datenmigrations-Staging-Tabellen und Validierungsregeln.</li>
                <li>Moderation von Fit-to-Standard Workshops mit Fachbereichen.</li>
              </ul>
            </div>
            <div class="p-4 rounded-xl bg-slate-50 dark:bg-slate-800/40 border border-slate-200 dark:border-slate-700">
              <div class="font-bold text-blue-600 text-sm mb-1">Tag 61 bis 90: Strategischer Hebel</div>
              <ul class="text-slate-600 dark:text-slate-300 space-y-1.5 list-disc list-inside">
                <li>Etablierung von Clean-Core-Richtlinien und Extension-Reviews.</li>
                <li>Rollout von Enable-Now-Schulungskonzepten zur Anwenderbefähigung.</li>
                <li>Reporting an Management und Vorbereitung von Quality Gates.</li>
              </ul>
            </div>
          </div>
        </div>

        <!-- 5-Year Leadership Trajectory -->
        <div class="bg-white dark:bg-slate-900 p-6 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm space-y-4">
          <h3 class="text-base font-bold text-slate-900 dark:text-white">Dein 5-Jahres-Fahrplan zur Führungskraft im ERP-Bereich</h3>
          <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 text-xs">
            <div class="p-3.5 bg-slate-50 dark:bg-slate-800/40 rounded-xl border border-slate-200 dark:border-slate-700">
              <div class="font-bold text-blue-600 mb-1">Jahr 1–2: Senior Solution Consultant</div>
              <p class="text-slate-600 dark:text-slate-300 text-[11px] leading-relaxed">
                Fundierte Etablierung in Großprojekten. Fachliche Führung von Modulbereichen (FI/CO, MM oder BTP Integrationsarchitektur). Erste Projektleitungsverantwortung für Teilprojekte.
              </p>
            </div>
            <div class="p-3.5 bg-slate-50 dark:bg-slate-800/40 rounded-xl border border-slate-200 dark:border-slate-700">
              <div class="font-bold text-purple-600 mb-1">Jahr 3–4: Enterprise ERP Architect</div>
              <p class="text-slate-600 dark:text-slate-300 text-[11px] leading-relaxed">
                Gesamtarchitektonische Verantwortung über heterogene Systemlandschaften. Leitung von Architecture Review Boards (ARB), Schnittstellen-Governance und Cloud-Roadmaps.
              </p>
            </div>
            <div class="p-3.5 bg-slate-50 dark:bg-slate-800/40 rounded-xl border border-slate-200 dark:border-slate-700">
              <div class="font-bold text-emerald-600 mb-1">Jahr 5+: Head of ERP / Transformation Director</div>
              <p class="text-slate-600 dark:text-slate-300 text-[11px] leading-relaxed">
                Budget- und Personalverantwortung für die ERP-Plattform. Strategische Ausrichtung des Plattform-Ökosystems und direktes C-Level Reporting (CIO/CFO).
              </p>
            </div>
          </div>
        </div>

      </div>
"""
