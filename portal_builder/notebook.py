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

        <!-- Local Hybrid-RAG Workbench (Suche & Zitate | Job-Fit Matcher | Interview-Sparring) -->
        <div id="rag-workbench" class="bento-card p-6 space-y-4">
          <div class="flex flex-col lg:flex-row lg:items-center justify-between gap-3">
            <div>
              <div class="flex flex-wrap items-center gap-2">
                <h3 class="text-base font-bold flex items-center gap-2" style="color: var(--ds-text)">
                  <span>🔍</span>
                  <span class="bento-metric">Local Hybrid-RAG Workbench ({{ (ragStats.total_chunks || 256985).toLocaleString('de-DE') }} Chunks | RRF + Rerank)</span>
                </h3>
                <span class="status-pill status-pill-purple bento-metric">🟢 {{ ragStats.ollama_model || 'bge-m3' }} 1024d ({{ (ragStats.ollama_vectors || 20987).toLocaleString('de-DE') }} Vektoren)</span>
              </div>
              <p class="text-xs mt-1 bento-metric" style="color: var(--ds-text-subtlest)">
                FTS5 BM25 + Synonyme + {{ (ragStats.total_vectors || 560).toLocaleString('de-DE') }} Gemini- &amp; {{ (ragStats.ollama_vectors || 20987).toLocaleString('de-DE') }} Ollama-Vektoren + Cross-Signal-Reranker über {{ (ragStats.total_files || 4918).toLocaleString('de-DE') }} Obsidian-Notizen ({{ ragStats.size_mb || 1356.17 }} MB).
              </p>
            </div>
            <div class="segmented-control">
              <button @click="ragViewMode = 'search'" :class="['seg-btn', ragViewMode === 'search' ? 'active' : '']">🔍 RAG &amp; Zitate</button>
              <button @click="ragViewMode = 'matcher'" :class="['seg-btn', ragViewMode === 'matcher' ? 'active' : '']">🎯 Job-Fit Matcher</button>
              <button @click="ragViewMode === 'sparring'" :class="['seg-btn', ragViewMode === 'sparring' ? 'active' : '']">🥊 Interview-Sparring</button>
            </div>
          </div>

          <!-- ==================== MODE 1: HYBRID-RAG SUCHE & KI-SYNTHESE ==================== -->
          <div v-show="ragViewMode === 'search'" class="space-y-4">
            <div class="flex flex-wrap items-center gap-1.5 text-[11px]">
              <span class="mr-1" style="color: var(--ds-text-subtlest)">Domäne:</span>
              <button @click="ragDomain = ''" :class="ragDomain === '' ? 'btn-primary font-bold' : ''" class="px-2.5 py-1 rounded-lg border transition" :style="ragDomain === '' ? '' : 'background: var(--ds-surface-sunken); border-color: var(--ds-border); color: var(--ds-text-subtle)'">🌐 Alle ({{ (ragStats.total_files || 4918).toLocaleString('de-DE') }})</button>
              <button @click="ragDomain = 'work'" :class="ragDomain === 'work' ? 'btn-primary font-bold' : ''" class="px-2.5 py-1 rounded-lg border transition" :style="ragDomain === 'work' ? '' : 'background: var(--ds-surface-sunken); border-color: var(--ds-border); color: var(--ds-text-subtle)'">💼 Arbeit (SSB &amp; DC1)</button>
              <button @click="ragDomain = 'study'" :class="ragDomain === 'study' ? 'btn-primary font-bold' : ''" class="px-2.5 py-1 rounded-lg border transition" :style="ragDomain === 'study' ? '' : 'background: var(--ds-surface-sunken); border-color: var(--ds-border); color: var(--ds-text-subtle)'">🎓 Studium (300 ECTS)</button>
              <button @click="ragDomain = 'empirie'" :class="ragDomain === 'empirie' ? 'btn-primary font-bold' : ''" class="px-2.5 py-1 rounded-lg border transition" :style="ragDomain === 'empirie' ? '' : 'background: var(--ds-surface-sunken); border-color: var(--ds-border); color: var(--ds-text-subtle)'">🔬 Empirie (12 Interviews)</button>
              <button @click="ragDomain = 'synergies'" :class="ragDomain === 'synergies' ? 'btn-primary font-bold' : ''" class="px-2.5 py-1 rounded-lg border transition" :style="ragDomain === 'synergies' ? '' : 'background: var(--ds-surface-sunken); border-color: var(--ds-border); color: var(--ds-text-subtle)'">⚡ Synergien</button>
              <button @click="ragDomain = 'library'" :class="ragDomain === 'library' ? 'btn-primary font-bold' : ''" class="px-2.5 py-1 rounded-lg border transition" :style="ragDomain === 'library' ? '' : 'background: var(--ds-surface-sunken); border-color: var(--ds-border); color: var(--ds-text-subtle)'">📚 Fachliteratur (454)</button>
              <button @click="ragDomain = 'curated'" :class="ragDomain === 'curated' ? 'btn-primary font-bold' : ''" class="px-2.5 py-1 rounded-lg border transition" :style="ragDomain === 'curated' ? '' : 'background: var(--ds-surface-sunken); border-color: var(--ds-border); color: var(--ds-text-subtle)'">✨ Schicht 1 (Kuratiert)</button>
              <span class="ml-auto segmented-control">
                <button @click="ragStyle = 'compact'" :class="['seg-btn', ragStyle === 'compact' ? 'active' : '']">⚡ 60s-Kompakt</button>
                <button @click="ragStyle = 'deep'" :class="['seg-btn', ragStyle === 'deep' ? 'active' : '']">🔬 Tiefenanalyse</button>
              </span>
            </div>

            <div class="flex flex-wrap gap-2">
              <input 
                v-model="ragQuery"
                @keyup.enter="runRagSearch"
                type="text"
                placeholder="z.B. Wie verhindere ich technische Schulden bei S/4HANA? oder Empirie 12 Interviews Clean Core..."
                class="flex-1 min-w-[240px] px-4 py-2.5 text-xs rounded-xl border focus:outline-none"
              >
              <button @click="runRagSearch" class="px-4 py-2 text-xs font-semibold rounded-xl border transition hover:opacity-85" style="background: var(--ds-surface-sunken); border-color: var(--ds-border); color: var(--ds-text)">
                {{ ragLoading ? 'Suche...' : 'Chunks finden' }}
              </button>
              <button @click="runRagAsk" class="px-4 py-2 btn-primary text-xs font-semibold rounded-xl transition">
                {{ ragAskLoading ? 'Synthetisiere...' : (ragStyle === 'compact' ? '⚡ 60s-Synthese (Hybrid AI)' : '🔬 Tiefenanalyse (Hybrid AI)') }}
              </button>
            </div>

            <!-- Schnell-Abfragen -->
            <div class="flex flex-wrap gap-1.5 text-[11px]">
              <button @click="askSynergyRag('Fasse meine 5 Stärken und die wichtigsten Arbeit x Uni Synergien kompakt zusammen', 'synergies')" class="px-2.5 py-1 rounded-lg bg-emerald-500/10 hover:bg-emerald-500/25 text-emerald-300 border border-emerald-500/30 transition">⭐ Stärken &amp; Arbeit × Uni Synergien</button>
              <button @click="quickRagAsk('Kritische Erfolgsfaktoren Plattformisierung SAP S/4HANA Masterarbeit 1,0')" class="px-2.5 py-1 rounded-lg bg-white/5 hover:bg-[#bf262e]/20 text-[#c4bebe] hover:text-white border border-white/10 transition">💡 Plattformisierung &amp; Masterarbeit (1,0)</button>
              <button @click="quickRagAsk('KPMG IT-Transformation Audit IKS Berechtigungen Trennungsrechnung Masterarbeit')" class="px-2.5 py-1 rounded-lg bg-white/5 hover:bg-[#bf262e]/20 text-[#c4bebe] hover:text-white border border-white/10 transition">🎯 KPMG IT-Audit Prep</button>
              <button @click="quickRagAsk('Schwarz Digits IAM SAP HCM Berechtigungen UMT P_ORGIN Third Level PFCG')" class="px-2.5 py-1 rounded-lg bg-white/5 hover:bg-[#bf262e]/20 text-[#c4bebe] hover:text-white border border-white/10 transition">🔐 Schwarz IAM / UMT</button>
              <button @click="quickRagAsk('TRUMPF Trainee IT Governance EAM Signavio Clean Core')" class="px-2.5 py-1 rounded-lg bg-white/5 hover:bg-[#bf262e]/20 text-[#c4bebe] hover:text-white border border-white/10 transition">🏭 TRUMPF Governance</button>
              <button @click="askSynergyRag('Welche empirischen Aussagen liefern die 12 Masterarbeits-Interviews und das Mayring Codebuch zu Clean Core und Change Management?', 'empirie')" class="px-2.5 py-1 rounded-lg bg-cyan-500/10 hover:bg-cyan-500/25 text-cyan-300 border border-cyan-500/30 transition">🔬 Empirie &amp; 12 Interviews (Mayring)</button>
              <button @click="quickRagAsk('LTMC CVI Übernahmekonto Migration')" class="px-2.5 py-1 rounded-lg bg-white/5 hover:bg-[#bf262e]/20 text-[#c4bebe] hover:text-white border border-white/10 transition">🔄 LTMC &amp; CVI Saldo 0 €</button>
            </div>

            <!-- Hybrid AI Synthesis Answer Card (XSS-safe Markdown Rendered) -->
            <div v-if="ragAnswer" class="p-4 sm:p-5 rounded-xl ai-output-card space-y-2.5">
              <div class="flex flex-wrap items-center justify-between gap-2 text-xs border-b pb-2" style="border-color: var(--ds-border)">
                <span class="font-bold" style="color: var(--ds-text-brand)">{{ ragStyle === 'compact' ? '⚡ 60s-Kompakt-Briefing' : '🔬 Verifizierte Second-Brain-Tiefenanalyse' }}</span>
                <div class="flex flex-wrap items-center gap-2 font-mono text-[10px]">
                  <span v-if="ragGrounding.citation_count > 0" class="status-pill status-pill-green">
                    ✓ {{ ragGrounding.verified_citations }}/{{ ragGrounding.citation_count }} Zitate verifiziert
                  </span>
                  <span style="color: var(--ds-text-subtlest)">{{ ragModel }} • {{ ragRetrievalMode || 'hybrid_rrf_rerank' }} • {{ ragDomain || 'alle' }}</span>
                </div>
              </div>
              <div class="text-xs leading-relaxed space-y-1.5" style="color: var(--ds-text-subtle)" v-html="formattedRagAnswer"></div>
            </div>

            <div v-if="ragResults.length > 0" class="space-y-2.5 max-h-96 overflow-y-auto custom-scrollbar">
              <div v-for="(hit, idx) in ragResults" :key="idx" class="bento-card p-3.5 space-y-1.5">
                <div class="flex flex-wrap items-center justify-between gap-2 text-xs">
                  <span class="font-bold" style="color: var(--ds-text)">{{ hit.title }}</span>
                  <div class="flex flex-wrap items-center gap-1.5 font-mono text-[10px]">
                    <span v-if="hit.vec_sim > 0" class="status-pill status-pill-purple">Semantik: {{ hit.vec_sim }}%</span>
                    <span v-if="hit.rerank_boost && hit.rerank_boost > 1" class="status-pill status-pill-blue">Rerank ×{{ hit.rerank_boost }}</span>
                    <span class="status-pill status-pill-green">RRF: {{ hit.score }} • {{ hit.type || 'concept' }}</span>
                    <button
                      @click="openSourceDrawer(hit.file, hit.title)"
                      class="px-2 py-0.5 rounded-full border font-sans font-semibold transition hover:opacity-85"
                      style="background: var(--ds-surface-sunken); border-color: var(--ds-border); color: var(--ds-text)"
                    >📖 Quelle öffnen</button>
                  </div>
                </div>
                <div class="text-[11px] font-mono" style="color: var(--ds-text-brand)">{{ hit.file }} › {{ hit.section }}</div>
                <p class="text-xs leading-relaxed whitespace-pre-line" style="color: var(--ds-text-subtle)">{{ hit.snippet }}</p>
              </div>
            </div>
          </div>

          <!-- ==================== MODE 2: STELLENANZEIGE × VAULT MATCHER ==================== -->
          <div v-show="ragViewMode === 'matcher'" class="space-y-4">
            <div class="flex flex-wrap items-center justify-between gap-2 text-xs">
              <span style="color: var(--ds-text-subtle)">Stellenanzeige einfügen oder Interview-Preset laden → 3-Säulen-Match (SSB/DC1 × Studium × Obsidian-Primärquelle):</span>
              <div class="flex flex-wrap gap-1.5 text-[11px]">
                <button @click="loadJobPreset('kpmg')" class="px-2.5 py-1 rounded-lg bg-[#bf262e]/15 hover:bg-[#bf262e]/30 text-[#f87171] border border-[#bf262e]/30 transition">🎯 Preset: KPMG</button>
                <button @click="loadJobPreset('schwarz')" class="px-2.5 py-1 rounded-lg bg-blue-500/15 hover:bg-blue-500/30 text-blue-300 border border-blue-500/30 transition">🔐 Preset: Schwarz Digits</button>
                <button @click="loadJobPreset('trumpf')" class="px-2.5 py-1 rounded-lg bg-emerald-500/15 hover:bg-emerald-500/30 text-emerald-300 border border-emerald-500/30 transition">🏭 Preset: TRUMPF</button>
              </div>
            </div>

            <div class="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
              <input v-model="jobMatchCompany" type="text" placeholder="Unternehmen (z.B. KPMG, Schwarz Digits)" class="px-3.5 py-2 text-xs rounded-xl border focus:outline-none">
              <input v-model="jobMatchRole" type="text" placeholder="Zielrolle (z.B. Associate IT-Audit / SAP Consultant)" class="px-3.5 py-2 text-xs rounded-xl border focus:outline-none">
            </div>

            <textarea
              v-model="jobMatchText"
              rows="5"
              placeholder="Füge hier Bulletpoints der Stellenanzeige oder Aufgabenbereiche ein..."
              class="w-full p-3.5 text-xs rounded-xl border focus:outline-none custom-scrollbar"
            ></textarea>

            <div class="flex flex-wrap items-center justify-between gap-2">
              <span class="text-[11px] font-mono" style="color: var(--ds-text-subtlest)">{{ jobMatchStatus || 'Bereit für Multi-Domain RAG-Match (Arbeit × Studium × Kuratiert).' }}</span>
              <button @click="runJobMatch" :disabled="jobMatchLoading" class="px-4 py-2 btn-primary disabled:opacity-50 text-xs font-bold rounded-xl transition">
                {{ jobMatchLoading ? 'Analysiere & matche...' : '🎯 Gegen Obsidian Vault matchen' }}
              </button>
            </div>

            <div v-if="jobMatchResult" class="p-4 sm:p-5 rounded-xl ai-output-card space-y-2.5">
              <div class="flex flex-wrap items-center justify-between gap-2 text-xs border-b pb-2" style="border-color: var(--ds-border)">
                <span class="font-bold" style="color: var(--ds-text-success)">🎯 Verifizierte Job-Fit-Matrix {{ jobMatchCompany ? ('(' + jobMatchCompany + ')') : '' }}</span>
                <div class="flex items-center gap-2 font-mono text-[10px]">
                  <span v-if="jobMatchGrounding.citation_count > 0" class="status-pill status-pill-green">
                    ✓ {{ jobMatchGrounding.verified_citations }}/{{ jobMatchGrounding.citation_count }} Zitate belegt
                  </span>
                  <span style="color: var(--ds-text-subtlest)">{{ jobMatchModel }}</span>
                </div>
              </div>
              <div class="text-xs leading-relaxed space-y-1.5" style="color: var(--ds-text-subtle)" v-html="formattedJobMatch"></div>
              <div v-if="jobMatchSources.length > 0" class="pt-2 border-t flex flex-wrap gap-1.5 text-[10px] font-mono" style="border-color: var(--ds-border)">
                <span style="color: var(--ds-text-subtlest)">Verwendete Quellen:</span>
                <button
                  v-for="(s, idx) in jobMatchSources.slice(0, 8)"
                  :key="idx"
                  @click="openSourceDrawer(s.file, s.title)"
                  class="px-2 py-0.5 rounded border hover:opacity-80 transition"
                  style="background: var(--ds-surface-sunken); border-color: var(--ds-border); color: var(--ds-text)"
                >📖 {{ s.title }}</button>
              </div>
            </div>
          </div>

          <!-- ==================== MODE 3: DEVIL'S ADVOCATE INTERVIEW-SPARRING ==================== -->
          <div v-show="ragViewMode === 'sparring'" class="space-y-4">
            <div class="flex flex-wrap items-center gap-1.5 text-[11px]">
              <span class="mr-1" style="color: var(--ds-text-subtlest)">Interviewer-Persona:</span>
              <button @click="selectSparringPersona('kpmg', 'KPMG')" :class="sparringPersona === 'kpmg' ? 'btn-primary font-bold' : ''" class="px-2.5 py-1 rounded-lg border transition" :style="sparringPersona === 'kpmg' ? '' : 'background: var(--ds-surface-sunken); border-color: var(--ds-border); color: var(--ds-text-subtle)'">🎯 KPMG IT-Audit</button>
              <button @click="selectSparringPersona('schwarz', 'Schwarz Digits')" :class="sparringPersona === 'schwarz' ? 'btn-primary font-bold' : ''" class="px-2.5 py-1 rounded-lg border transition" :style="sparringPersona === 'schwarz' ? '' : 'background: var(--ds-surface-sunken); border-color: var(--ds-border); color: var(--ds-text-subtle)'">🔐 Schwarz IAM/HCM</button>
              <button @click="selectSparringPersona('trumpf', 'TRUMPF')" :class="sparringPersona === 'trumpf' ? 'btn-primary font-bold' : ''" class="px-2.5 py-1 rounded-lg border transition" :style="sparringPersona === 'trumpf' ? '' : 'background: var(--ds-surface-sunken); border-color: var(--ds-border); color: var(--ds-text-subtle)'">🏭 TRUMPF Governance</button>
              <button @click="selectSparringPersona('cto', 'CTO Stresstest')" :class="sparringPersona === 'cto' ? 'btn-primary font-bold' : ''" class="px-2.5 py-1 rounded-lg border transition" :style="sparringPersona === 'cto' ? '' : 'background: var(--ds-surface-sunken); border-color: var(--ds-border); color: var(--ds-text-subtle)'">⚡ Kritischer CTO / CV-Check</button>
            </div>

            <div class="flex flex-wrap gap-2">
              <input
                v-model="sparringTopic"
                @keyup.enter="askSparringQuestion"
                type="text"
                placeholder="Optionales Fokusthema (z.B. SoD & P_ORGIN, Trennungsrechnung, Notensprung, Clean Core vs. BTP)..."
                class="flex-1 min-w-[240px] px-3.5 py-2 text-xs rounded-xl border focus:outline-none"
              >
              <button @click="askSparringQuestion" :disabled="sparringLoading" class="px-4 py-2 btn-primary disabled:opacity-50 text-xs font-bold rounded-xl transition">
                {{ sparringLoading ? 'Generiere...' : (sparringQuestion ? '🔄 Nächste kritische Frage' : '🥊 Kritische Frage stellen') }}
              </button>
            </div>

            <div v-if="sparringQuestion" class="p-4 rounded-xl bg-amber-500/10 border border-amber-500/35 space-y-2">
              <div class="flex items-center justify-between text-xs border-b border-amber-500/20 pb-1.5">
                <span class="font-bold text-amber-300">🎙️ Frage im Stil: {{ sparringCompany || sparringPersona }}</span>
                <span class="text-[10px] font-mono" style="color: var(--ds-text-subtlest)">{{ sparringModel }}</span>
              </div>
              <div class="text-xs leading-relaxed space-y-1.5" style="color: var(--ds-text)" v-html="formattedSparringQuestion"></div>
            </div>

            <div class="space-y-2">
              <textarea
                v-model="sparringAnswer"
                rows="4"
                placeholder="Formuliere hier deine Antwort (wie im echten Gespräch) – das System prüft sie faktisch gegen deinen Obsidian Vault und gibt dir sofort Score, Blind Spots und eine geschliffene 60s-STAR-Fassung..."
                class="w-full p-3.5 text-xs rounded-xl border focus:outline-none custom-scrollbar"
              ></textarea>
              <div class="flex flex-wrap items-center justify-between gap-2">
                <span class="text-[11px] font-mono" style="color: var(--ds-text-subtlest)">{{ sparringStatus || 'Bereit für Live-Fakten-Audit deiner Antwort.' }}</span>
                <button @click="evaluateSparringAnswer" :disabled="sparringLoading || !sparringAnswer.trim()" class="px-4 py-2 btn-primary disabled:opacity-50 text-xs font-bold rounded-xl transition">
                  {{ sparringLoading ? 'Prüfe gegen Obsidian...' : '🛡️ Antwort prüfen & optimieren' }}
                </button>
              </div>
            </div>

            <div v-if="sparringFeedback" class="p-4 sm:p-5 rounded-xl ai-output-card space-y-2.5">
              <div class="flex flex-wrap items-center justify-between gap-2 text-xs border-b pb-2" style="border-color: var(--ds-border)">
                <span class="font-bold" style="color: var(--ds-text-brand)">📋 Fakten-Audit &amp; 60s-Optimierung</span>
                <div class="flex items-center gap-2 font-mono text-[10px]">
                  <span v-if="sparringGrounding.citation_count > 0" class="status-pill status-pill-green">
                    ✓ {{ sparringGrounding.verified_citations }}/{{ sparringGrounding.citation_count }} Belege verifiziert
                  </span>
                  <span style="color: var(--ds-text-subtlest)">{{ sparringModel }}</span>
                </div>
              </div>
              <div class="text-xs leading-relaxed space-y-1.5" style="color: var(--ds-text-subtle)" v-html="formattedSparringFeedback"></div>
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
              <p class="text-xs text-[#8f8888] mt-0.5">Direktabruf der laufenden Gespräche inkl. 1-Klick RAG-Prep, Job-Fit Matcher &amp; Sparring.</p>
            </div>
            <div class="flex flex-wrap items-center gap-2 text-[11px] font-mono">
              <span class="px-2.5 py-1 rounded-full bg-emerald-500/15 text-emerald-300 border border-emerald-500/30">Interviews: {{ pipelineData.interviews.length }}</span>
              <span class="px-2.5 py-1 rounded-full bg-white/10 text-[#c4bebe] border border-white/10">Offen: {{ pipelineData.open_count ?? 0 }}</span>
              <span class="px-2.5 py-1 rounded-full bg-white/5 text-[#8f8888] border border-white/10">Abgeschlossen: {{ pipelineData.closed_count ?? 65 }} / {{ pipelineData.total_rows ?? 68 }}</span>
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
              <div class="flex flex-wrap gap-1.5 pt-1">
                <button @click="prepInterview(iv.company, iv.role)" class="px-2.5 py-1 bg-[#bf262e]/20 hover:bg-[#bf262e]/40 border border-[#bf262e]/40 text-[#f87171] hover:text-white text-[11px] font-semibold rounded-lg transition">
                  ⚡ RAG Prep
                </button>
                <button @click="openCompanyWorkbench(iv.company, iv.role, 'matcher')" class="px-2.5 py-1 bg-emerald-500/15 hover:bg-emerald-500/35 border border-emerald-500/35 text-emerald-300 hover:text-white text-[11px] font-semibold rounded-lg transition">
                  🎯 Job-Fit
                </button>
                <button @click="openCompanyWorkbench(iv.company, iv.role, 'sparring')" class="px-2.5 py-1 bg-amber-500/15 hover:bg-amber-500/35 border border-amber-500/35 text-amber-300 hover:text-white text-[11px] font-semibold rounded-lg transition">
                  🥊 Sparring
                </button>
              </div>
            </div>
          </div>
          <div v-else class="text-xs text-[#8f8888]">Laufende Gespräche werden beim lokalen Start über localhost:8085 geladen.</div>
        </div>

      </div>
"""
