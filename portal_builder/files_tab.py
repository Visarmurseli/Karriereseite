# -*- coding: utf-8 -*-

def get_files_tab():
    return """
      <!-- ================= TAB 12: DOKUMENTEN-EXPLORER & FACHBIBLIOTHEK ================= -->
      <div v-show="activeTab === 'files'" class="space-y-6">
        <div class="bento-card p-6 space-y-5">
          <div class="flex flex-col lg:flex-row lg:items-center justify-between gap-3">
            <div>
              <div class="flex flex-wrap items-center gap-2">
                <span class="text-xl">📂</span>
                <h3 class="text-base font-bold" style="color: var(--ds-text)">
                  Dokumenten-Explorer &amp; Fachbibliothek (RAG-Katalog)
                </h3>
                <span class="status-pill status-pill-green bento-metric">
                  {{ (ragStats.total_files || 4918).toLocaleString('de-DE') }} Obsidian-Notizen • {{ (ragStats.ollama_vectors || 20987).toLocaleString('de-DE') }} Vektoren
                </span>
              </div>
              <p class="text-xs mt-1" style="color: var(--ds-text-subtlest)">
                Dein lokaler Navigator durch kuratierte Projekt-Nachweise und alle {{ libraryTotal || 471 }} indizierten Fachbücher &amp; Synthese-Hubs.
              </p>
            </div>

            <!-- Segmented Switch: Artefakte vs Live Fachbibliothek -->
            <div class="flex flex-wrap items-center gap-2">
              <div class="segmented-control">
                <button
                  @click="filesViewMode = 'artifacts'"
                  :class="['seg-btn', filesViewMode === 'artifacts' ? 'active' : '']"
                >📂 Schlüssel-Artefakte</button>
                <button
                  @click="filesViewMode = 'library'; loadLibraryCatalog()"
                  :class="['seg-btn', filesViewMode === 'library' ? 'active' : '']"
                >📚 Fachbibliothek ({{ libraryTotal || 471 }})</button>
              </div>
              <span class="status-pill status-pill-amber">🔒 100% Lokal</span>
            </div>
          </div>

          <!-- ==================== ANSICHT A: KURATIERTE ARTEFAKTE ==================== -->
          <div v-show="filesViewMode === 'artifacts'" class="space-y-4">
            <div class="flex flex-col md:flex-row md:items-center justify-between gap-3">
              <div class="flex flex-wrap gap-1.5 overflow-x-auto custom-scrollbar">
                <button 
                  v-for="cat in fileCategories" 
                  :key="cat"
                  @click="selectedFileCat = cat"
                  :class="[
                    'px-2.5 py-1 rounded-lg text-xs font-semibold border transition',
                    selectedFileCat === cat ? 'btn-primary' : ''
                  ]"
                  :style="selectedFileCat === cat ? '' : 'background: var(--ds-surface-sunken); border-color: var(--ds-border); color: var(--ds-text-subtle)'"
                >
                  {{ cat }}
                </button>
              </div>

              <div class="text-xs whitespace-nowrap" style="color: var(--ds-text-subtlest)">
                Zeige <strong style="color: var(--ds-text)">{{ filteredFiles.length }}</strong> kuratierte Schlüssel-Dateien
              </div>
            </div>

            <div class="overflow-x-auto rounded-xl border" style="border-color: var(--ds-border)">
              <table class="w-full text-left text-xs">
                <thead>
                  <tr>
                    <th class="p-3">Dateiname &amp; Schnellzugriff</th>
                    <th class="p-3">Kategorie</th>
                    <th class="p-3">Inhalt &amp; Strategische Relevanz</th>
                    <th class="p-3">Dein Interview- &amp; Praxis-Impact</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(file, idx) in filteredFiles" :key="idx" class="transition">
                    <td class="p-3 font-semibold" style="color: var(--ds-text)">
                      <div class="space-y-1">
                        <div class="flex items-center gap-2 flex-wrap">
                          <span>📄</span>
                          <span class="font-bold">{{ file.name }}</span>
                          <span class="status-pill status-pill-green font-mono text-[9.5px]">🔒 Verifiziert</span>
                        </div>
                        <div class="flex items-center gap-2 text-[10px] font-mono" style="color: var(--ds-text-subtlest)">
                          <span>Internes Archiv</span>
                          <span>•</span>
                          <span>Nachweis im Gespräch</span>
                        </div>
                      </div>
                    </td>
                    <td class="p-3">
                      <span class="status-pill status-pill-neutral whitespace-nowrap">{{ file.cat }}</span>
                    </td>
                    <td class="p-3 leading-relaxed" style="color: var(--ds-text-subtle)">{{ file.desc }}</td>
                    <td class="p-3 font-medium leading-relaxed" style="color: var(--ds-text)">{{ file.impact }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <!-- ==================== ANSICHT B: LIVE FACHBIBLIOTHEK (RAG SQLITE KATALOG) ==================== -->
          <div v-show="filesViewMode === 'library'" class="space-y-4">
            <div class="flex flex-col sm:flex-row gap-2.5">
              <input
                v-model="libraryQuery"
                @keyup.enter="loadLibraryCatalog()"
                type="text"
                placeholder="Fachbuch, Autor oder Thema suchen (z.B. Clean Core, Audit, TOGAF, LangGraph, BTP, VISMUV)..."
                class="flex-1 px-3.5 py-2 text-xs rounded-xl border focus:outline-none"
              >
              <button @click="loadLibraryCatalog()" class="px-4 py-2 rounded-xl text-xs font-semibold btn-primary">
                {{ libraryLoading ? 'Lade...' : '🔍 Bibliothek filtern' }}
              </button>
            </div>

            <!-- Category Chips -->
            <div class="flex flex-wrap items-center gap-1.5 text-[11px]">
              <button
                @click="libraryDomain = ''; loadLibraryCatalog()"
                :class="['px-2.5 py-1 rounded-lg font-semibold border transition', libraryDomain === '' ? 'btn-primary' : '']"
                :style="libraryDomain === '' ? '' : 'background: var(--ds-surface-sunken); border-color: var(--ds-border); color: var(--ds-text-subtle)'"
              >
                🌐 Alle ({{ libraryTotal || 471 }})
              </button>
              <button
                v-for="cat in libraryCategories"
                :key="cat.id"
                @click="libraryDomain = cat.id; loadLibraryCatalog()"
                :class="['px-2.5 py-1 rounded-lg font-semibold border transition', libraryDomain === cat.id ? 'btn-primary' : '']"
                :style="libraryDomain === cat.id ? '' : 'background: var(--ds-surface-sunken); border-color: var(--ds-border); color: var(--ds-text-subtle)'"
              >
                {{ cat.label }} ({{ cat.count }})
              </button>
            </div>

            <div class="text-[11px]" style="color: var(--ds-text-subtlest)">
              Zeige <strong class="bento-metric" style="color: var(--ds-text)">{{ libraryBooks.length }}</strong> von <strong class="bento-metric" style="color: var(--ds-text)">{{ libraryFiltered }}</strong> passenden Werken/Synthese-Hubs (Klick auf „Chunks lesen“ öffnet den lokalen Reader-Drawer).
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-3 max-h-[34rem] overflow-y-auto custom-scrollbar pr-1">
              <div v-for="(book, idx) in libraryBooks" :key="idx" class="bento-card p-3.5 flex flex-col justify-between gap-2.5">
                <div class="space-y-1">
                  <div class="flex items-center justify-between gap-2">
                    <span :class="book.doc_type === 'moc' || book.doc_type === 'concept' ? 'status-pill status-pill-purple' : 'status-pill status-pill-blue'">
                      {{ book.category_label }}
                    </span>
                    <span class="font-mono text-[10px] bento-metric" style="color: var(--ds-text-subtlest)">{{ book.chunks }} Chunks</span>
                  </div>
                  <div class="font-bold text-xs leading-snug" style="color: var(--ds-text)">{{ book.title }}</div>
                  <div class="font-mono text-[10px] truncate" style="color: var(--ds-text-subtlest)">{{ book.filename }}</div>
                </div>
                <div class="flex items-center gap-2 pt-1 border-t" style="border-color: var(--ds-border)">
                  <button
                    @click="openSourceDrawer(book.file, book.title)"
                    class="px-2.5 py-1 rounded-lg border text-[11px] font-semibold transition hover:opacity-85"
                    style="background: var(--ds-surface-sunken); border-color: var(--ds-border); color: var(--ds-text)"
                  >📖 Chunks lesen</button>
                  <button
                    @click="askAboutSource(book.file, book.title)"
                    class="px-2.5 py-1 rounded-lg text-[11px] font-semibold btn-primary transition"
                  >🤖 Mit RAG fragen</button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
"""
