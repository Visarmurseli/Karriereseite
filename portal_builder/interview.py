# -*- coding: utf-8 -*-

def get_interview():
    return """
      <!-- ================= TAB 11: INTERVIEW-MASTERCLASS ================= -->
      <div v-show="activeTab === 'interview'" class="space-y-6">
        
        <!-- Pitch Box -->
        <div class="bg-[#141414] p-6 rounded-2xl border border-white/10 shadow-sm space-y-4">
          <div class="flex items-center justify-between">
            <div>
              <h3 class="text-base font-bold text-white flex items-center space-x-2">
                <span>🎙️</span>
                <span>Deine perfekte Selbstpräsentation ("Erzählen Sie etwas über sich")</span>
              </h3>
              <p class="text-xs text-[#8f8888]">Wähle zwischen der 60-Sekunden-Executive-Version und dem 3-Minuten-Deep-Dive</p>
            </div>
            <div class="flex space-x-1 bg-white/5 border border-white/10 p-1 rounded-xl text-xs">
              <button 
                @click="pitchMode = 'short'" 
                :class="['px-3 py-1 rounded-lg font-medium transition', pitchMode === 'short' ? 'bg-[#bf262e] text-white shadow' : 'text-[#8f8888] hover:text-white']"
              >
                60 Sek. Elevator Pitch
              </button>
              <button 
                @click="pitchMode = 'deep'" 
                :class="['px-3 py-1 rounded-lg font-medium transition', pitchMode === 'deep' ? 'bg-[#bf262e] text-white shadow' : 'text-[#8f8888] hover:text-white']"
              >
                3 Min. Deep Dive Pitch
              </button>
            </div>
          </div>

          <div class="p-4 rounded-xl bg-white/5 border border-white/10 text-xs sm:text-sm text-[#c4bebe] leading-relaxed font-sans relative">
            <p v-if="pitchMode === 'short'" class="whitespace-pre-line text-white/90">{{ pitch60 }}</p>
            <p v-else class="whitespace-pre-line text-white/90">{{ pitchDeep }}</p>
            
            <div class="mt-4 pt-3 border-t border-white/10 flex justify-between items-center text-xs">
              <span class="text-[#8f8888]">Präzise formuliert für maximale Überzeugungskraft</span>
              <button @click="copyText(pitchMode === 'short' ? pitch60 : pitchDeep)" class="text-[#f87171] hover:text-white font-bold flex items-center space-x-1 transition">
                <span>Text kopieren</span>
                <span>📋</span>
              </button>
            </div>
          </div>
        </div>

        <!-- 5 STAR Stories -->
        <div class="bg-[#141414] p-6 rounded-2xl border border-white/10 shadow-sm space-y-4">
          <div class="flex items-center justify-between">
            <div>
              <h3 class="text-base font-bold text-white flex items-center space-x-2">
                <span>🌟</span>
                <span>Deine 5 unschlagbaren STAR-Stories aus der SSB-Praxis</span>
              </h3>
              <p class="text-xs text-[#8f8888]">Situation ➔ Task ➔ Action ➔ Result (Klicke zum Ausklappen)</p>
            </div>
          </div>

          <div class="space-y-3">
            <div 
              v-for="(story, idx) in starStories" 
              :key="idx" 
              class="border border-white/10 rounded-xl overflow-hidden bg-white/5 transition"
            >
              <div 
                @click="story.expanded = !story.expanded" 
                class="p-4 cursor-pointer flex items-center justify-between hover:bg-white/10 transition"
              >
                <div class="flex items-center space-x-3">
                  <span class="tag-badge bg-[#bf262e]/20 text-[#f87171] border border-[#bf262e]/30">{{ story.tag }}</span>
                  <h4 class="text-sm font-semibold text-white">{{ story.title }}</h4>
                </div>
                <span class="text-xs text-[#8f8888]">{{ story.expanded ? '▲ Einklappen' : '▼ Ausklappen' }}</span>
              </div>

              <div v-show="story.expanded" class="p-4 border-t border-white/10 bg-black/40 space-y-3 text-xs">
                <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
                  <div class="p-3 bg-white/5 border border-white/10 rounded-lg">
                    <span class="font-bold text-white block mb-1">Situation:</span>
                    <p class="text-[#c4bebe]">{{ story.s }}</p>
                  </div>
                  <div class="p-3 bg-white/5 border border-white/10 rounded-lg">
                    <span class="font-bold text-white block mb-1">Task:</span>
                    <p class="text-[#c4bebe]">{{ story.t }}</p>
                  </div>
                  <div class="p-3 bg-[#bf262e]/10 border border-[#bf262e]/30 rounded-lg">
                    <span class="font-bold text-[#f87171] block mb-1">Action:</span>
                    <p class="text-[#c4bebe]">{{ story.a }}</p>
                  </div>
                  <div class="p-3 bg-emerald-500/10 border border-emerald-500/30 rounded-lg">
                    <span class="font-bold text-emerald-400 block mb-1">Result:</span>
                    <p class="text-[#c4bebe]">{{ story.r }}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 40+ Q&A Simulator -->
        <div class="bg-[#141414] p-6 rounded-2xl border border-white/10 shadow-sm space-y-4">
          <div class="flex flex-col md:flex-row md:items-center justify-between gap-3">
            <div>
              <h3 class="text-base font-bold text-white flex items-center space-x-2">
                <span>💬</span>
                <span>Interaktiver Interview- & Wissens-Simulator (40+ fundierte Fach- & Verhaltensfragen)</span>
              </h3>
              <p class="text-xs text-[#8f8888]">Strukturierter Wissenskatalog: SSB S/4HANA, DC1 ITIL 4, Master, Bachelor, EAM & Verhalten</p>
            </div>
            
            <div class="flex items-center gap-2">
              <span class="text-xs text-[#8f8888] font-mono whitespace-nowrap">{{ filteredQA.length }} Fragen gefunden</span>
            </div>
          </div>

          <!-- Category Filter Bar & Live Search -->
          <div class="space-y-3 pt-1">
            <div class="flex flex-wrap gap-1.5">
              <button 
                v-for="cat in qaCategories" 
                :key="cat"
                @click="selectedQACat = cat"
                :class="[
                  'px-3 py-1.5 rounded-lg text-xs font-semibold transition',
                  selectedQACat === cat 
                    ? 'bg-[#bf262e] text-white shadow' 
                    : 'bg-white/5 text-[#c4bebe] hover:bg-white/10 border border-white/10'
                ]"
              >
                {{ cat }}
              </button>
            </div>

            <!-- Instant Search Input inside QA tab -->
            <div class="relative">
              <input 
                type="text" 
                v-model="qaSearch" 
                placeholder="Fragen oder Antworten durchsuchen (z.B. Trennungsrechnung, PRTG, Clean Core, Mayring, BTP, CVI, 0,00 €)..." 
                class="w-full bg-[#181818] border border-white/10 rounded-xl px-4 py-2.5 text-xs text-white placeholder-[#8f8888] focus:outline-none focus:border-[#bf262e]"
              >
              <button 
                v-if="qaSearch" 
                @click="qaSearch = ''" 
                class="absolute right-3 top-2.5 text-xs text-slate-400 hover:text-white"
              >
                ✕ Löschen
              </button>
            </div>
          </div>

          <div class="space-y-3">
            <div 
              v-for="(item, idx) in filteredQA" 
              :key="idx" 
              class="border border-white/10 rounded-xl overflow-hidden bg-white/5 transition"
            >
              <div 
                @click="item.open = !item.open" 
                class="p-4 cursor-pointer flex items-center justify-between hover:bg-white/10 transition"
              >
                <div class="flex items-center space-x-3">
                  <span class="tag-badge bg-white/10 text-white">{{ item.cat }}</span>
                  <h4 class="text-sm font-semibold text-white">{{ item.q }}</h4>
                </div>
                <span class="text-xs text-[#8f8888]">{{ item.open ? '▲ Einklappen' : '▼ Antwort zeigen' }}</span>
              </div>

              <div v-show="item.open" class="p-4 border-t border-white/10 bg-black/40 space-y-3 text-xs">
                <p class="text-[#c4bebe] leading-relaxed whitespace-pre-line">{{ item.a }}</p>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-2 pt-2 border-t border-white/10">
                  <div class="text-[11px] text-emerald-400">
                    <strong class="text-emerald-300">Do:</strong> {{ item.do }}
                  </div>
                  <div class="text-[11px] text-red-400">
                    <strong class="text-red-300">Don't:</strong> {{ item.dont }}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

      </div>
"""
