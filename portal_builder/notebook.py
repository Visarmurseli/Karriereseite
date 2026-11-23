# -*- coding: utf-8 -*-

def get_notebook():
    return """
      <!-- ================= TAB 13: PERSÖNLICHES SECOND BRAIN NOTIZBUCH ================= -->
      <div v-show="activeTab === 'notebook'" class="space-y-6">
        
        <div class="bg-[#141414] p-6 rounded-2xl border border-white/10 shadow-sm space-y-4">
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
            <div>
              <h3 class="text-lg font-bold text-white flex items-center space-x-2">
                <span>📝</span>
                <span>Mein Second Brain: Persönliches Karriere- & Wissens-Notizbuch</span>
              </h3>
              <p class="text-xs text-[#8f8888]">
                Speichere hier deine persönlichen Gedanken, Interview-Notizen, Kontakte und Ziele. Daten werden automatisch im lokalen Speicher deines Browsers gespeichert (Autosave).
              </p>
            </div>

            <div class="flex items-center space-x-2">
              <button 
                @click="copyNotesToClipboard" 
                class="px-3 py-1.5 bg-[#bf262e] hover:bg-[#cf3840] text-white rounded-xl text-xs font-semibold transition flex items-center space-x-1 shadow-md shadow-[#bf262e]/30"
              >
                <span>In Zwischenablage kopieren 📋</span>
              </button>
              <button 
                @click="clearNotes" 
                class="px-3 py-1.5 bg-white/5 hover:bg-red-500/20 text-[#c4bebe] hover:text-red-400 border border-white/10 rounded-xl text-xs font-semibold transition"
              >
                <span>Leeren 🗑️</span>
              </button>
            </div>
          </div>

          <!-- Note Editor & Quick Templates -->
          <div class="grid grid-cols-1 lg:grid-cols-4 gap-4 pt-2">
            
            <!-- Sidebar: Quick Templates -->
            <div class="space-y-2 text-xs">
              <div class="font-bold text-white text-xs uppercase tracking-wider mb-1">
                Vorlagen & Schnellbausteine
              </div>
              
              <button 
                @click="insertTemplate('interview_log')" 
                class="w-full text-left p-2.5 rounded-xl border border-white/10 bg-white/5 hover:bg-[#bf262e]/10 hover:border-[#bf262e]/40 transition"
              >
                <div class="font-bold text-[#f87171]">📋 Interview-Protokoll</div>
                <div class="text-[10px] text-[#8f8888] mt-0.5">Unternehmen, Ansprechpartner, Fragen, Feedback</div>
              </button>

              <button 
                @click="insertTemplate('salary_target')" 
                class="w-full text-left p-2.5 rounded-xl border border-white/10 bg-white/5 hover:bg-[#bf262e]/10 hover:border-[#bf262e]/40 transition"
              >
                <div class="font-bold text-emerald-400">💰 Gehaltskalkulation</div>
                <div class="text-[10px] text-[#8f8888] mt-0.5">Fixum, Bonus, IGM EG-Stufen, Verhandlungsziel</div>
              </button>

              <button 
                @click="insertTemplate('daily_focus')" 
                class="w-full text-left p-2.5 rounded-xl border border-white/10 bg-white/5 hover:bg-[#bf262e]/10 hover:border-[#bf262e]/40 transition"
              >
                <div class="font-bold text-purple-400">🎯 VISMUV & Tagesfokus</div>
                <div class="text-[10px] text-[#8f8888] mt-0.5">Tagesprioritäten, Sport/Gesundheit, Meilensteine</div>
              </button>

              <button 
                @click="insertTemplate('learning_cheat')" 
                class="w-full text-left p-2.5 rounded-xl border border-white/10 bg-white/5 hover:bg-[#bf262e]/10 hover:border-[#bf262e]/40 transition"
              >
                <div class="font-bold text-amber-400">💡 Neues SAP/IT Learning</div>
                <div class="text-[10px] text-[#8f8888] mt-0.5">BTP Service, CDS View, Architektur-Notiz</div>
              </button>
            </div>

            <!-- Main Editor Textarea -->
            <div class="lg:col-span-3 space-y-2">
              <div class="flex items-center justify-between text-xs text-[#8f8888]">
                <span>Markdown-kompatibler Texteditor</span>
                <span class="text-emerald-400 font-medium">● Automatisch gespeichert</span>
              </div>
              <textarea 
                v-model="personalNotes" 
                @input="saveNotes" 
                placeholder="Schreibe hier deine Gedanken, Interviewvorbereitungen, SAP-Erkenntnisse und Ziele auf..." 
                class="w-full h-96 p-4 text-xs font-mono bg-black/50 border border-white/10 rounded-xl focus:outline-none focus:border-[#bf262e] focus:ring-1 focus:ring-[#bf262e] transition-all text-white leading-relaxed custom-scrollbar"
              ></textarea>
            </div>

          </div>
        </div>

      </div>
"""
