# -*- coding: utf-8 -*-

def get_cv_defense():
    return """
      <!-- ================= TAB 2: CV DE-RISKING & DEFENSE ================= -->
      <div v-show="activeTab === 'cv_defense'" class="space-y-6">
        
        <!-- Header Alert Banner -->
        <div class="bg-gradient-to-r from-red-950 via-slate-900 to-slate-900 text-white rounded-2xl p-6 lg:p-8 shadow-xl border border-red-900/40 relative overflow-hidden">
          <div class="relative z-10 max-w-4xl space-y-3">
            <div class="flex flex-wrap items-center gap-2">
              <span class="bg-red-500 text-white px-2.5 py-0.5 rounded-md text-xs font-bold uppercase tracking-wider">Kritische Gefahrenabwehr</span>
              <span class="bg-white/10 text-slate-200 px-2.5 py-0.5 rounded-md text-xs font-medium">Headhunter- & Architekten-Perspektive</span>
            </div>
            <h2 class="text-2xl font-black tracking-tight text-white">
              Das De-Risking Playbook: Wie du deinen Lebenslauf kugelsicher machst
            </h2>
            <p class="text-slate-300 text-xs sm:text-sm leading-relaxed">
              <strong>Die schonungslose Wahrheit:</strong> Du hast im Lebenslauf Skills wie Java, UiPath oder SQL angegeben, die teilweise theoretisch oder übertrieben sind. In technischen Interviews mit Senior-Entwicklern drohen Fangfragen (z.B. Spring Boot, OOP-Patterns, UiPath REFramework).<br>
              <strong>Die beruhigende Entwarnung:</strong> Du wirst <strong>NICHT</strong> als Software-Entwickler oder RPA-Scripter eingestellt! Dein echter Marktwert liegt in der <strong>ERP-Architektur, Transformations-Governance und Clean-Core-Methodik</strong>. Wenn du versuchst, Coding vorzutäuschen, fliegst du auf. Wenn du stattdessen die nachfolgenden Pivot-Brücken nutzt, wirkst du wie ein erfahrener Stratege!
            </p>
          </div>
        </div>

        <!-- Das 3-Stufen Ampelsystem -->
        <div class="bg-white dark:bg-slate-900 p-6 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm space-y-4">
          <div class="flex items-center justify-between">
            <div>
              <h3 class="text-base font-bold text-slate-900 dark:text-white flex items-center space-x-2">
                <span>🚦</span>
                <span>Das Ampelsystem deines Profils: Wo du angreifst, framest oder abwehrst</span>
              </h3>
              <p class="text-xs text-slate-500">Kategorisiere jedes Thema in deinem Lebenslauf vor dem Gespräch</p>
            </div>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            
            <!-- GRÜN: Echte Superkräfte -->
            <div class="p-4 rounded-xl bg-emerald-50/60 dark:bg-emerald-950/20 border border-emerald-200 dark:border-emerald-800/50 space-y-3">
              <div class="flex items-center space-x-2 text-emerald-700 dark:text-emerald-300 font-bold text-xs uppercase tracking-wider">
                <span class="w-2.5 h-2.5 rounded-full bg-emerald-500"></span>
                <span>🟢 GRÜN: Echte Superkräfte (Offensive)</span>
              </div>
              <div class="text-xs text-slate-700 dark:text-slate-300 space-y-2">
                <p><strong>Hier führst du das Gespräch!</strong> Sprich aktiv darüber, bringe Beispiele, zeige Tiefe:</p>
                <ul class="space-y-1.5 list-disc list-inside text-[11px]">
                  <li><strong>24 Mo. IT-PMO SSB:</strong> TP1-TP5 Governance, Lenkungsausschuss, Meilenstein-Tracking.</li>
                  <li><strong>Masterarbeit 1,0 (30 ECTS):</strong> 126 Seiten, 12 Experteninterviews, empirische Forschung zu ERP-Transformation, Plattformisierung & Kritischen Erfolgsfaktoren.</li>
                  <li><strong>SAP Cloud ALM & Signavio:</strong> Offizieller Quickguide-Autor; End-to-End Traceability.</li>
                  <li><strong>SAP Enable Now:</strong> Strategisches Übergabekonzept an HR/Personalentwicklung (UB AC).</li>
                  <li><strong>Datenmigrations-Methodik:</strong> Staging vs. Direct, SuSa/Bilanzabgleich (0,00 € Übernahmekonto).</li>
                  <li><strong>Stakeholder & Schnittstellen:</strong> Nagarro, Evora, Axians, xSuite, d.velop, PATRIS.</li>
                </ul>
              </div>
            </div>

            <!-- GELB: Defensiv framen -->
            <div class="p-4 rounded-xl bg-amber-50/60 dark:bg-amber-950/20 border border-amber-200 dark:border-amber-800/50 space-y-3">
              <div class="flex items-center space-x-2 text-amber-700 dark:text-amber-300 font-bold text-xs uppercase tracking-wider">
                <span class="w-2.5 h-2.5 rounded-full bg-amber-500"></span>
                <span>🟡 GELB: Defensiv framen (Brücke schlagen)</span>
              </div>
              <div class="text-xs text-slate-700 dark:text-slate-300 space-y-2">
                <p><strong>Niemals als Programmierer auftreten!</strong> Immer als Prozess- & Architekturkompetenz framen:</p>
                <ul class="space-y-1.5 list-disc list-inside text-[11px]">
                  <li><strong>SQL / Relationale Datenbanken:</strong> "Genutzt für Datenbereinigung und Migrations-Checks (MARA, KNA1, BSEG). Ich verstehe Datenmodelle, bin aber kein DBA."</li>
                  <li><strong>Python:</strong> "Im Master für statistische Auswertungen und Prototypen eingesetzt. Meine Stärke ist die Übersetzung in fachliche Anforderungen."</li>
                  <li><strong>TOGAF:</strong> "Zertifizierter Intensivkurs (Scape Consulting 2020) als methodischer Kompass für Schnittstellen- und Bebauungsplanung."</li>
                  <li><strong>SAP ECC 6.0:</strong> "Tiefe Analyse des Altsystems zur Scoping-Vorbereitung für das Greenfield-Target."</li>
                </ul>
              </div>
            </div>

            <!-- ROT: Gefahrenzone -->
            <div class="p-4 rounded-xl bg-red-50/60 dark:bg-red-950/20 border border-red-200 dark:border-red-800/50 space-y-3">
              <div class="flex items-center space-x-2 text-red-700 dark:text-red-300 font-bold text-xs uppercase tracking-wider">
                <span class="w-2.5 h-2.5 rounded-full bg-red-500"></span>
                <span>🔴 ROT: Gefahrenzone (Sofort deflecten)</span>
              </div>
              <div class="text-xs text-slate-700 dark:text-slate-300 space-y-2">
                <p><strong>Absolute Fangfragen-Falle!</strong> Bei Nachfrage sofort die Pivot-Formel anwenden:</p>
                <ul class="space-y-1.5 list-disc list-inside text-[11px]">
                  <li><strong>Java / OOP / Spring Boot:</strong> "Teil des Grundlagenstudiums. In der Praxis konzentriere ich mich zu 100% auf ERP-Architektur und Clean-Core-Governance."</li>
                  <li><strong>UiPath / RPA Scripting:</strong> "Bei Bosch lag der Fokus auf Prozessanalyse und Business Case – die Implementierung machten dedizierte Scripter."</li>
                  <li><strong>SPRO Customizing / ABAP Coding:</strong> "Unser Dogma war Clean Core – ich habe Z-Entwicklungen im PMO verhindert, nicht selbst gecodet!"</li>
                </ul>
              </div>
            </div>

          </div>
        </div>

        <!-- Das Pivot-Playbook: 4 Meister-Dialoge -->
        <div class="bg-white dark:bg-slate-900 p-6 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm space-y-4">
          <div class="flex items-center justify-between">
            <div>
              <h3 class="text-base font-bold text-slate-900 dark:text-white flex items-center space-x-2">
                <span>🔄</span>
                <span>Das Pivot-Playbook: Wortwörtliche Abwehr- und Umlenksätze</span>
              </h3>
              <p class="text-xs text-slate-500">Klicke auf die Szenarien, um die genauen Antworten zu studieren</p>
            </div>
          </div>

          <div class="space-y-3">
            <div 
              v-for="(scenario, idx) in defenseScenarios" 
              :key="idx"
              class="border border-slate-200 dark:border-slate-700/80 rounded-xl overflow-hidden bg-slate-50/50 dark:bg-slate-800/30 transition-all"
            >
              <div 
                @click="scenario.open = !scenario.open" 
                class="p-4 cursor-pointer flex items-center justify-between hover:bg-slate-100 dark:hover:bg-slate-800/60 transition"
              >
                <div class="flex items-center space-x-3">
                  <span class="text-base">{{ scenario.icon }}</span>
                  <div>
                    <span class="text-xs font-bold text-red-600 dark:text-red-400 uppercase tracking-wider">{{ scenario.danger }}</span>
                    <h4 class="text-sm font-semibold text-slate-900 dark:text-white">{{ scenario.question }}</h4>
                  </div>
                </div>
                <div class="flex items-center space-x-2">
                  <span class="text-xs text-blue-600 font-medium">{{ scenario.open ? 'Einklappen' : 'Antwort zeigen' }}</span>
                  <span class="text-xs text-slate-400">{{ scenario.open ? '▲' : '▼' }}</span>
                </div>
              </div>

              <div v-show="scenario.open" class="p-4 border-t border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 space-y-3 text-xs">
                
                <div class="p-3 bg-red-50 dark:bg-red-950/30 border border-red-200 dark:border-red-900/40 rounded-lg text-red-800 dark:text-red-300">
                  <div class="font-bold flex items-center space-x-1.5 mb-1">
                    <span>❌</span>
                    <span>Tödliche Falle (Was du NIEMALS sagen darfst):</span>
                  </div>
                  <p class="leading-relaxed">{{ scenario.badAnswer }}</p>
                </div>

                <div class="p-3 bg-emerald-50 dark:bg-emerald-950/30 border border-emerald-200 dark:border-emerald-900/40 rounded-lg text-emerald-900 dark:text-emerald-200">
                  <div class="font-bold flex items-center space-x-1.5 mb-1">
                    <span>✅</span>
                    <span>Deine kugelsichere Meister-Antwort (Wortlaut einprägen!):</span>
                  </div>
                  <p class="leading-relaxed whitespace-pre-line font-medium">{{ scenario.goodAnswer }}</p>
                  <button 
                    @click="copyText(scenario.goodAnswer)" 
                    class="mt-2 px-2.5 py-1 bg-emerald-600 text-white rounded text-[11px] font-semibold hover:bg-emerald-700 transition"
                  >
                    Antwort in Zwischenablage kopieren 📋
                  </button>
                </div>

                <div class="p-2.5 bg-blue-50/60 dark:bg-blue-950/20 border border-blue-200 dark:border-blue-900/40 rounded-lg text-blue-900 dark:text-blue-300 text-[11px]">
                  <strong>Warum dieser Pivot gewinnt:</strong> {{ scenario.whyItWorks }}
                </div>

              </div>
            </div>
          </div>
        </div>

        <!-- Zeugnis- & Fakten-Check: Deine belegten Noten -->
        <div class="bg-white dark:bg-slate-900 p-6 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm space-y-4">
          <h3 class="text-base font-bold text-slate-900 dark:text-white flex items-center space-x-2">
            <span>📜</span>
            <span>Zeugnis- & Fakten-Check: Deine schwarz auf weiß belegten Erfolge</span>
          </h3>
          <p class="text-xs text-slate-500">Diese Fakten sind wasserdicht belegt und bilden dein unangreifbares Fundament</p>

          <div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
            <div class="p-4 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/40 space-y-2">
              <div class="font-bold text-blue-600 text-sm">Universität Stuttgart (Master M.Sc.)</div>
              <div class="text-slate-900 dark:text-white font-semibold">Gesamtnote: 1,6 „gut“ (120 ECTS) | Masterarbeit: 1,0</div>
              <p class="text-slate-600 dark:text-slate-300 text-[11px] leading-relaxed">
                Amtliches Zeugnis über die Masterprüfung (17.09.2026, Prof. Dr. Becker): Masterarbeit (1,0, Prof. Herzwurm), Digitale Nachhaltigkeit (1,0), FPWI (1,3), Advanced Software Engineering (1,6), Software-Architektur (1,7), Applied AI (1,7), Seminar WI (1,7).
              </p>
              <div class="text-[10px] text-emerald-600 font-bold">Amtlich beglaubigte universitäre Spitzenleistung</div>
            </div>

            <div class="p-4 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/40 space-y-2">
              <div class="font-bold text-blue-600 text-sm">SSB AG Zwischenzeugnis</div>
              <div class="text-slate-900 dark:text-white font-semibold">24 Monate IT-PMO (01.05.2024 – 30.04.2026)</div>
              <p class="text-slate-600 dark:text-slate-300 text-[11px] leading-relaxed">
                Ausgestellt von IT-Leiter ppa. Dietmar Fillinger & Roland Nowak. Bestbewertung: "stets zu unserer vollen Zufriedenheit", "vorbildliche Einsatzbereitschaft und Arbeitsweise".
              </p>
              <div class="text-[10px] text-emerald-600 font-bold">Vorstandsnah gezeichnetes Top-Zeugnis</div>
            </div>

            <div class="p-4 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/40 space-y-2">
              <div class="font-bold text-blue-600 text-sm">Datacenter One & Zertifikate</div>
              <div class="text-slate-900 dark:text-white font-semibold">12 Monate INOC + TOGAF Intensive</div>
              <p class="text-slate-600 dark:text-slate-300 text-[11px] leading-relaxed">
                Datacenter One: 1st/2nd Level Incident Management, Monitoring, Jira/Confluence. TOGAF-Intensivkurs bei Scape Consulting (Dr. Daniel Simon, Jan 2020).
              </p>
              <div class="text-[10px] text-emerald-600 font-bold">Operatives ITIL- & Architektur-Fundament</div>
            </div>
          </div>
        </div>

        <!-- CV Optimierungs-Matrix (Vorher vs. Nachher Wording) -->
        <div class="bg-white dark:bg-slate-900 p-6 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm space-y-4">
          <h3 class="text-base font-bold text-slate-900 dark:text-white flex items-center space-x-2">
            <span>📝</span>
            <span>CV-Optimierungs-Empfehlungen: Vom Minenfeld zum kugelsicheren Profil</span>
          </h3>
          <p class="text-xs text-slate-500">So solltest du deine Skills im Lebenslauf formulieren, um Einladungen zu maximieren und Fangfragen auszuschließen</p>

          <div class="overflow-x-auto">
            <table class="w-full text-left text-xs border border-slate-200 dark:border-slate-700 rounded-xl overflow-hidden">
              <thead class="bg-slate-100 dark:bg-slate-800 text-slate-900 dark:text-white font-bold">
                <tr>
                  <th class="p-3 border-b dark:border-slate-700">Bereich im CV</th>
                  <th class="p-3 border-b dark:border-slate-700 text-red-600 dark:text-red-400">Bisherige Formulierung (Gefahr)</th>
                  <th class="p-3 border-b dark:border-slate-700 text-emerald-600 dark:text-emerald-400">Optimierte Formulierung (Kugelsicher)</th>
                  <th class="p-3 border-b dark:border-slate-700">Strategischer Effekt</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-slate-200 dark:divide-slate-700 text-slate-600 dark:text-slate-300">
                <tr v-for="(item, idx) in cvImprovements" :key="idx">
                  <td class="p-3 font-semibold text-slate-900 dark:text-white">{{ item.area }}</td>
                  <td class="p-3 bg-red-50/50 dark:bg-red-950/20 text-red-900 dark:text-red-300 font-mono text-[11px]">{{ item.oldText }}</td>
                  <td class="p-3 bg-emerald-50/50 dark:bg-emerald-950/20 text-emerald-900 dark:text-emerald-200 font-medium">{{ item.newText }}</td>
                  <td class="p-3 text-[11px]">{{ item.effect }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

      </div>
"""
