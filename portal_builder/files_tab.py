# -*- coding: utf-8 -*-

def get_files_tab():
    return """
      <!-- ================= TAB 12: SSB DOKUMENTEN-EXPLORER ================= -->
      <div v-show="activeTab === 'files'" class="space-y-6">
        <div class="bg-white dark:bg-slate-900 p-6 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm space-y-4">
          <div class="flex flex-col md:flex-row md:items-center justify-between gap-3">
            <div>
              <h3 class="text-base font-bold text-slate-900 dark:text-white flex items-center space-x-2">
                <span>📂</span>
                <span>Kuratierter SSB Dokumenten-Explorer (50+ Dateien analysiert)</span>
              </h3>
              <p class="text-xs text-slate-500">Alle relevanten Konzeptpapiere, Migrations-Sheets und PMO-Artefakte mit Interview-Impact</p>
            </div>

            <!-- Categories -->
            <div class="flex flex-wrap gap-1">
              <button 
                v-for="cat in fileCategories" 
                :key="cat"
                @click="selectedFileCat = cat"
                :class="[
                  'px-2.5 py-1 rounded-md text-xs font-medium transition',
                  selectedFileCat === cat 
                    ? 'bg-blue-600 text-white' 
                    : 'bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300 hover:bg-slate-200'
                ]"
              >
                {{ cat }}
              </button>
            </div>
          </div>

          <!-- Files Table -->
          <div class="overflow-x-auto">
            <table class="w-full text-left text-xs border border-slate-200 dark:border-slate-700 rounded-xl overflow-hidden">
              <thead class="bg-slate-100 dark:bg-slate-800 text-slate-900 dark:text-white font-bold">
                <tr>
                  <th class="p-3 border-b dark:border-slate-700">Dateiname</th>
                  <th class="p-3 border-b dark:border-slate-700">Kategorie</th>
                  <th class="p-3 border-b dark:border-slate-700">Inhalt & Relevanz</th>
                  <th class="p-3 border-b dark:border-slate-700">Dein Interview-Impact</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-slate-200 dark:divide-slate-700 text-slate-600 dark:text-slate-300">
                <tr v-for="(file, idx) in filteredFiles" :key="idx" class="hover:bg-slate-50 dark:hover:bg-slate-800/50">
                  <td class="p-3 font-semibold text-slate-900 dark:text-white">
                    <div class="flex items-center space-x-2">
                      <span>📄</span>
                      <a v-if="file.path && file.path.startsWith('Studium_Dokumente')" :href="file.path + '/' + file.name" target="_blank" class="text-blue-600 dark:text-blue-400 hover:underline font-bold inline-flex items-center space-x-1.5">
                        <span>{{ file.name }}</span>
                        <span class="text-[10px] bg-blue-100 dark:bg-blue-900/60 text-blue-700 dark:text-blue-300 px-1.5 py-0.5 rounded font-mono">Öffnen ↗</span>
                      </a>
                      <span v-else>{{ file.name }}</span>
                    </div>
                  </td>
                  <td class="p-3"><span class="tag-badge bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300">{{ file.cat }}</span></td>
                  <td class="p-3 leading-relaxed">{{ file.desc }}</td>
                  <td class="p-3 text-slate-700 dark:text-slate-200 font-medium leading-relaxed">{{ file.impact }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
"""
