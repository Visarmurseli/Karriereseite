# -*- coding: utf-8 -*-

def get_files_tab():
    return """
      <!-- ================= TAB 12: SSB DOKUMENTEN-EXPLORER ================= -->
      <div v-show="activeTab === 'files'" class="space-y-6">
        <div class="bg-[#141414] p-6 rounded-2xl border border-white/10 shadow-sm space-y-4">
          <div class="flex flex-col md:flex-row md:items-center justify-between gap-3">
            <div>
              <div class="flex items-center space-x-2">
                <span class="text-xl">📂</span>
                <h3 class="text-base font-bold text-white">
                  Kuratierter Dokumenten-Explorer & Artefakt-Register
                </h3>
                <span class="px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 text-[10px] font-bold">1.890 Dateien indexiert</span>
              </div>
              <p class="text-xs text-[#8f8888] mt-0.5">Dein persönlicher, lokaler Navigator durch alle Konzepte, Migrations-Sheets, Steuerungsunterlagen und Vergabe-Akten.</p>
            </div>

            <!-- Privacy Notice Badge -->
            <div class="p-2 rounded-xl bg-amber-500/10 border border-amber-500/30 flex items-center space-x-2 text-[11px] text-amber-300">
              <span>🔒</span>
              <span><strong>100% Lokal & Vertraulich:</strong> Verbleibt offline auf deiner Festplatte (kein GitHub-Upload).</span>
            </div>
          </div>

          <!-- Filter & Search Controls -->
          <div class="flex flex-col md:flex-row md:items-center justify-between gap-3 pt-2">
            <!-- Categories -->
            <div class="flex flex-wrap gap-1.5 overflow-x-auto custom-scrollbar">
              <button 
                v-for="cat in fileCategories" 
                :key="cat"
                @click="selectedFileCat = cat"
                :class="[
                  'px-2.5 py-1 rounded-lg text-xs font-semibold transition',
                  selectedFileCat === cat 
                    ? 'bg-[#bf262e] text-white shadow-sm' 
                    : 'bg-white/5 text-[#c4bebe] hover:bg-white/10 border border-white/10'
                ]"
              >
                {{ cat }}
              </button>
            </div>

            <!-- Count badge -->
            <div class="text-xs text-[#8f8888] whitespace-nowrap">
              Zeige <strong class="text-white">{{ filteredFiles.length }}</strong> kuratierte Schlüssel-Dateien
            </div>
          </div>

          <!-- Files Table -->
          <div class="overflow-x-auto">
            <table class="w-full text-left text-xs border border-white/10 rounded-xl overflow-hidden">
              <thead class="bg-white/5 text-white font-bold">
                <tr>
                  <th class="p-3 border-b border-white/10">Dateiname & Schnellzugriff</th>
                  <th class="p-3 border-b border-white/10">Kategorie</th>
                  <th class="p-3 border-b border-white/10">Inhalt & Strategische Relevanz</th>
                  <th class="p-3 border-b border-white/10">Dein Interview- & Praxis-Impact</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-white/10 text-[#c4bebe]">
                <tr v-for="(file, idx) in filteredFiles" :key="idx" class="hover:bg-white/5 transition">
                  <td class="p-3 font-semibold text-white">
                    <div class="space-y-1">
                      <div class="flex items-center space-x-2">
                        <span>📄</span>
                        <span class="text-white font-bold">{{ file.name }}</span>
                        <span class="text-[9px] bg-emerald-500/15 text-emerald-400 border border-emerald-500/30 px-1.5 py-0.5 rounded font-mono">🔒 Vertraulich verifiziert</span>
                      </div>

                      <!-- Confidentiality & Reference Note -->
                      <div class="flex items-center space-x-2 pt-0.5 text-[10px] text-[#8f8888]">
                        <span class="font-mono">Status: Internes Archiv</span>
                        <span>•</span>
                        <span>Einsichtnahme im Vorstellungsgespräch</span>
                      </div>
                    </div>
                  </td>
                  <td class="p-3">
                    <span class="tag-badge bg-white/5 text-[#c4bebe] border border-white/10 whitespace-nowrap">{{ file.cat }}</span>
                  </td>
                  <td class="p-3 leading-relaxed">{{ file.desc }}</td>
                  <td class="p-3 text-white font-medium leading-relaxed">{{ file.impact }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
"""
