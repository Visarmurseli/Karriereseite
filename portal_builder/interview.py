# -*- coding: utf-8 -*-

def get_interview():
    return """
      <!-- ================= TAB 11: INTERVIEW-MASTERCLASS ================= -->
      <div v-show="activeTab === 'interview'" class="space-y-6">
        
        <!-- Pitch Box -->
        <div class="bg-white dark:bg-slate-900 p-6 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm space-y-4">
          <div class="flex items-center justify-between">
            <div>
              <h3 class="text-base font-bold text-slate-900 dark:text-white flex items-center space-x-2">
                <span>🎙️</span>
                <span>Deine perfekte Selbstpräsentation ("Erzählen Sie etwas über sich")</span>
              </h3>
              <p class="text-xs text-slate-500">Wähle zwischen der 60-Sekunden-Executive-Version und dem 3-Minuten-Deep-Dive</p>
            </div>
            <div class="flex space-x-1 bg-slate-100 dark:bg-slate-800 p-1 rounded-lg text-xs">
              <button 
                @click="pitchMode = 'short'" 
                :class="['px-3 py-1 rounded font-medium transition', pitchMode === 'short' ? 'bg-white dark:bg-slate-700 shadow text-blue-600' : 'text-slate-500']"
              >
                60 Sek. Elevator Pitch
              </button>
              <button 
                @click="pitchMode = 'deep'" 
                :class="['px-3 py-1 rounded font-medium transition', pitchMode === 'deep' ? 'bg-white dark:bg-slate-700 shadow text-blue-600' : 'text-slate-500']"
              >
                3 Min. Deep Dive Pitch
              </button>
            </div>
          </div>

          <div class="p-4 rounded-xl bg-slate-50 dark:bg-slate-800/50 border border-slate-200 dark:border-slate-700 text-xs sm:text-sm text-slate-800 dark:text-slate-200 leading-relaxed font-sans relative">
            <p v-if="pitchMode === 'short'" class="whitespace-pre-line">{{ pitch60 }}</p>
            <p v-else class="whitespace-pre-line">{{ pitchDeep }}</p>
            
            <div class="mt-4 pt-3 border-t border-slate-200 dark:border-slate-700 flex justify-between items-center text-xs">
              <span class="text-slate-500">Präzise formuliert für maximale Überzeugungskraft</span>
              <button @click="copyText(pitchMode === 'short' ? pitch60 : pitchDeep)" class="text-blue-600 hover:text-blue-700 font-bold flex items-center space-x-1">
                <span>Text kopieren</span>
                <span>📋</span>
              </button>
            </div>
          </div>
        </div>

        <!-- 5 STAR Stories -->
        <div class="bg-white dark:bg-slate-900 p-6 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm space-y-4">
          <div class="flex items-center justify-between">
            <div>
              <h3 class="text-base font-bold text-slate-900 dark:text-white flex items-center space-x-2">
                <span>🌟</span>
                <span>Deine 5 unschlagbaren STAR-Stories aus der SSB-Praxis</span>
              </h3>
              <p class="text-xs text-slate-500">Situation ➔ Task ➔ Action ➔ Result (Klicke zum Ausklappen)</p>
            </div>
          </div>

          <div class="space-y-3">
            <div 
              v-for="(story, idx) in starStories" 
              :key="idx" 
              class="border border-slate-200 dark:border-slate-700 rounded-xl overflow-hidden bg-slate-50/50 dark:bg-slate-800/30"
            >
              <div 
                @click="story.expanded = !story.expanded" 
                class="p-4 cursor-pointer flex items-center justify-between hover:bg-slate-100 dark:hover:bg-slate-800 transition"
              >
                <div class="flex items-center space-x-3">
                  <span class="tag-badge bg-blue-100 text-blue-800 dark:bg-blue-900/60 dark:text-blue-300">{{ story.tag }}</span>
                  <h4 class="text-sm font-semibold text-slate-900 dark:text-white">{{ story.title }}</h4>
                </div>
                <span class="text-xs text-slate-400">{{ story.expanded ? '▲ Einklappen' : '▼ Ausklappen' }}</span>
              </div>

              <div v-show="story.expanded" class="p-4 border-t border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 space-y-3 text-xs">
                <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
                  <div class="p-3 bg-slate-50 dark:bg-slate-800/40 rounded-lg">
                    <span class="font-bold text-slate-900 dark:text-white block mb-1">Situation:</span>
                    <p class="text-slate-600 dark:text-slate-300">{{ story.s }}</p>
                  </div>
                  <div class="p-3 bg-slate-50 dark:bg-slate-800/40 rounded-lg">
                    <span class="font-bold text-slate-900 dark:text-white block mb-1">Task:</span>
                    <p class="text-slate-600 dark:text-slate-300">{{ story.t }}</p>
                  </div>
                  <div class="p-3 bg-blue-50/50 dark:bg-blue-950/20 rounded-lg border border-blue-100 dark:border-blue-900/40">
                    <span class="font-bold text-blue-700 dark:text-blue-300 block mb-1">Action:</span>
                    <p class="text-slate-600 dark:text-slate-300">{{ story.a }}</p>
                  </div>
                  <div class="p-3 bg-emerald-50/50 dark:bg-emerald-950/20 rounded-lg border border-emerald-100 dark:border-emerald-900/40">
                    <span class="font-bold text-emerald-700 dark:text-emerald-300 block mb-1">Result:</span>
                    <p class="text-slate-600 dark:text-slate-300">{{ story.r }}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 15+ Q&A Simulator -->
        <div class="bg-white dark:bg-slate-900 p-6 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm space-y-4">
          <div class="flex flex-col md:flex-row md:items-center justify-between gap-3">
            <div>
              <h3 class="text-base font-bold text-slate-900 dark:text-white flex items-center space-x-2">
                <span>💬</span>
                <span>Interaktiver Interview-Simulator (15+ Fach- und Verhaltensfragen)</span>
              </h3>
              <p class="text-xs text-slate-500">Filtern nach Themengebieten</p>
            </div>
            
            <div class="flex flex-wrap gap-1">
              <button 
                v-for="cat in qaCategories" 
                :key="cat"
                @click="selectedQACat = cat"
                :class="[
                  'px-2.5 py-1 rounded-md text-xs font-medium transition',
                  selectedQACat === cat 
                    ? 'bg-blue-600 text-white' 
                    : 'bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300 hover:bg-slate-200'
                ]"
              >
                {{ cat }}
              </button>
            </div>
          </div>

          <div class="space-y-3">
            <div 
              v-for="(item, idx) in filteredQA" 
              :key="idx" 
              class="border border-slate-200 dark:border-slate-700 rounded-xl overflow-hidden bg-slate-50/50 dark:bg-slate-800/30"
            >
              <div 
                @click="item.open = !item.open" 
                class="p-4 cursor-pointer flex items-center justify-between hover:bg-slate-100 dark:hover:bg-slate-800 transition"
              >
                <div class="flex items-center space-x-3">
                  <span class="tag-badge bg-slate-200 dark:bg-slate-700 text-slate-800 dark:text-slate-200">{{ item.cat }}</span>
                  <h4 class="text-sm font-semibold text-slate-900 dark:text-white">{{ item.q }}</h4>
                </div>
                <span class="text-xs text-slate-400">{{ item.open ? '▲ Einklappen' : '▼ Antwort zeigen' }}</span>
              </div>

              <div v-show="item.open" class="p-4 border-t border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 space-y-3 text-xs">
                <p class="text-slate-700 dark:text-slate-200 leading-relaxed whitespace-pre-line">{{ item.a }}</p>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-2 pt-2 border-t border-slate-100 dark:border-slate-800">
                  <div class="text-[11px] text-emerald-700 dark:text-emerald-400">
                    <strong>Do:</strong> {{ item.do }}
                  </div>
                  <div class="text-[11px] text-red-600 dark:text-red-400">
                    <strong>Don't:</strong> {{ item.dont }}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

      </div>
"""
