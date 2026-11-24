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

            <div class="flex flex-wrap items-center gap-2">
              <button 
                @click="saveNotesToObsidian" 
                class="px-3 py-1.5 bg-emerald-600 hover:bg-emerald-500 text-white rounded-xl text-xs font-semibold transition flex items-center space-x-1 shadow-md shadow-emerald-600/30"
              >
                <span>In Obsidian Vault speichern 🧠</span>
              </button>
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
          <div v-if="ragStatusMsg" class="text-xs px-3 py-2 rounded-lg bg-emerald-500/10 border border-emerald-500/30 text-emerald-300">
            {{ ragStatusMsg }}
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
                <span class="text-emerald-400 font-medium">● Browser-Autosave + Obsidian Sync</span>
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

        <!-- Local Hybrid-RAG Wissenssuche & KI-Synthese (SQLite FTS5 + Gemini 3) -->
        <div class="bg-[#141414] p-6 rounded-2xl border border-white/10 shadow-sm space-y-4">
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
            <div>
              <h3 class="text-base font-bold text-white flex items-center space-x-2">
                <span>🔍</span>
                <span>Local Hybrid-RAG & KI-Synthese (Obsidian Knowledge Lake | 137.000+ Chunks)</span>
              </h3>
              <p class="text-xs text-[#8f8888] mt-0.5">Hybrid-Suche (AND/OR + Zettel-Ranking) über 4.980 Originaldokumente + optionale Gemini-Synthese mit Quellenangaben.</p>
            </div>
            <span class="text-[10px] font-mono px-2.5 py-1 rounded-full bg-purple-500/15 text-purple-300 border border-purple-500/30">Hybrid FTS5 BM25</span>
          </div>

          <div class="flex flex-wrap gap-2">
            <input 
              v-model="ragQuery"
              @keyup.enter="runRagSearch"
              type="text"
              placeholder="z.B. KPMG IT-Transformation IKS, Trennungsrechnung ACDOCA, UMT Schwarz, LTMC CVI..."
              class="flex-1 min-w-[240px] px-4 py-2.5 text-xs bg-black/50 border border-white/15 rounded-xl text-white placeholder-[#8f8888] focus:outline-none focus:border-[#bf262e]"
            >
            <button @click="runRagSearch" class="px-4 py-2 bg-white/10 hover:bg-white/20 text-white text-xs font-semibold rounded-xl transition border border-white/10">
              {{ ragLoading ? 'Suche...' : 'Chunks finden' }}
            </button>
            <button @click="runRagAsk" class="px-4 py-2 bg-[#bf262e] hover:bg-[#cf3840] text-white text-xs font-semibold rounded-xl transition shadow-md shadow-[#bf262e]/30">
              {{ ragAskLoading ? 'Synthetisiere...' : '🤖 KI-Synthese (Gemini)' }}
            </button>
          </div>

          <!-- Gemini Synthesis Answer Card -->
          <div v-if="ragAnswer" class="p-4 rounded-xl bg-gradient-to-br from-[#bf262e]/15 to-black/60 border border-[#bf262e]/40 space-y-2">
            <div class="flex items-center justify-between text-xs">
              <span class="font-bold text-[#f87171]">🤖 Verifizierte Second-Brain-Antwort</span>
              <span class="font-mono text-[10px] text-[#8f8888]">{{ ragModel }}</span>
            </div>
            <div class="text-xs text-[#f0eded] leading-relaxed whitespace-pre-line">{{ ragAnswer }}</div>
          </div>

          <div v-if="ragResults.length > 0" class="space-y-2.5 max-h-96 overflow-y-auto custom-scrollbar">
            <div v-for="(hit, idx) in ragResults" :key="idx" class="p-3.5 rounded-xl bg-white/5 border border-white/10 space-y-1">
              <div class="flex items-center justify-between text-xs">
                <span class="font-bold text-white">{{ hit.title }}</span>
                <span class="font-mono text-[10px] text-emerald-400">Score: {{ hit.score }} • {{ hit.type || 'concept' }} • {{ hit.domain }}</span>
              </div>
              <div class="text-[11px] text-[#f87171] font-mono">{{ hit.file }} › {{ hit.section }}</div>
              <p class="text-xs text-[#c4bebe] leading-relaxed whitespace-pre-line">{{ hit.snippet }}</p>
            </div>
          </div>
        </div>

        <!-- Live Bewerbungspipeline & 1-Klick Interview-Prep (localhost:8085 only) -->
        <div class="bg-[#141414] p-6 rounded-2xl border border-white/10 shadow-sm space-y-4">
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
            <div>
              <h3 class="text-base font-bold text-white flex items-center space-x-2">
                <span>🎯</span>
                <span>Live-Bewerbungspipeline & Interview-Radar (Bewerbungsverlauf.xlsx)</span>
              </h3>
              <p class="text-xs text-[#8f8888] mt-0.5">Direktabruf der laufenden Gespräche inkl. 1-Klick-Wissensabruf aus deinem Obsidian Second Brain.</p>
            </div>
            <div class="flex items-center gap-2 text-[11px] font-mono">
              <span class="px-2.5 py-1 rounded-full bg-emerald-500/15 text-emerald-300 border border-emerald-500/30">Interviews: {{ pipelineData.interviews.length }}</span>
              <span class="px-2.5 py-1 rounded-full bg-white/10 text-[#c4bebe] border border-white/10">Offen: {{ pipelineData.open_count }}</span>
            </div>
          </div>

          <div v-if="pipelineData.interviews.length > 0" class="grid grid-cols-1 md:grid-cols-2 gap-3">
            <div v-for="(iv, idx) in pipelineData.interviews" :key="idx" class="p-3.5 rounded-xl bg-white/5 border border-white/10 flex flex-col justify-between gap-2">
              <div>
                <div class="flex items-center justify-between gap-2">
                  <span class="font-bold text-white text-xs">{{ iv.company }}</span>
                  <span class="text-[10px] font-mono text-amber-300">G1: {{ iv.g1 }} | G2: {{ iv.g2 }}</span>
                </div>
                <div class="text-[11px] text-[#f87171] mt-0.5">{{ iv.role }}</div>
                <div class="text-[11px] text-[#8f8888] mt-1">{{ iv.status }}</div>
              </div>
              <button @click="prepInterview(iv.company, iv.role)" class="self-start px-3 py-1 bg-[#bf262e]/20 hover:bg-[#bf262e]/40 border border-[#bf262e]/40 text-[#f87171] hover:text-white text-[11px] font-semibold rounded-lg transition">
                ⚡ Prep via RAG + KI laden
              </button>
            </div>
          </div>
          <div v-else class="text-xs text-[#8f8888]">Laufende Gespräche werden beim lokalen Start über localhost:8085 geladen.</div>
        </div>

      </div>
"""
