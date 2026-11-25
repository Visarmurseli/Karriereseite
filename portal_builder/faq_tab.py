# -*- coding: utf-8 -*-

def get_faq_tab():
    return """
      <!-- ================= TAB 7: FAQ & TECHNISCHE VERTIEFUNG (AKKORDEON) ================= -->
      <div v-show="activeTab === 'faq'" class="space-y-6">

        <div class="bg-[#141414] p-6 rounded-2xl border border-white/10 space-y-5">
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
            <div>
              <h2 class="text-xl sm:text-2xl font-extrabold text-white tracking-tight flex items-center gap-2">
                <span>❓</span>
                <span>FAQ &amp; Fachliche Vertiefung</span>
              </h2>
              <p class="text-xs sm:text-sm text-[#8f8888] mt-1">
                Architekturdetails, SAP S/4HANA Fachkonzepte, Migrationsmethodik &amp; Antworten auf vertiefende Fachfragen auf einen Klick.
              </p>
            </div>
            <div class="flex flex-wrap gap-1.5 text-[11px]">
              <button
                v-for="cat in ['Alle', 'SSB & S/4HANA', 'Migration & Schnittstellen', 'Studium & DC1', 'Einstieg & Arbeitsweise']"
                :key="cat"
                @click="selectedFaqCat = cat"
                :class="selectedFaqCat === cat ? 'bg-[#bf262e] text-white font-semibold' : 'bg-white/5 text-[#c4bebe] hover:bg-white/10'"
                class="px-2.5 py-1 rounded-lg border border-white/10 transition"
              >
                {{ cat }}
              </button>
            </div>
          </div>

          <div class="space-y-3">
            <div
              v-for="(item, idx) in filteredFaqItems"
              :key="idx"
              class="rounded-xl border border-white/10 bg-white/5 overflow-hidden transition"
            >
              <button
                @click="item.open = !item.open"
                class="w-full p-4 text-left flex items-center justify-between gap-3 hover:bg-white/5 transition"
              >
                <div class="flex items-center gap-2.5 min-w-0">
                  <span class="status-pill status-pill-blue shrink-0">{{ item.cat }}</span>
                  <span class="font-bold text-xs sm:text-sm text-white">{{ item.q }}</span>
                </div>
                <span class="text-xs font-mono shrink-0" style="color: var(--ds-text-subtlest)">{{ item.open ? '−' : '+' }}</span>
              </button>
              <div v-show="item.open" class="px-4 pb-4 pt-2 border-t border-white/10 text-xs text-[#c4bebe] leading-relaxed space-y-2">
                <p v-for="(para, pIdx) in item.a" :key="pIdx">{{ para }}</p>
              </div>
            </div>
          </div>
        </div>

      </div>
"""
