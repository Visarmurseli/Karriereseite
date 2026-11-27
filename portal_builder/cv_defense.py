# -*- coding: utf-8 -*-

def get_cv_defense():
    return """
      <!-- ================= TAB 2: CV STUDIO (GENERATOR) & DE-RISKING PLAYBOOK ================= -->
      <div v-show="activeTab === 'cv_defense'" class="space-y-6">
        
        <!-- Top Segmented Studio Header Bar -->
        <div class="bento-card p-5 sm:p-6 no-cv-print flex flex-col lg:flex-row lg:items-center justify-between gap-4">
          <div class="space-y-1">
            <div class="flex flex-wrap items-center gap-2">
              <span class="status-pill status-pill-blue">📄 CV Studio &amp; De-Risking</span>
              <span class="status-pill status-pill-green">ATS-Optimiert • 0 Coding-Fallen</span>
            </div>
            <h2 class="text-lg sm:text-xl font-extrabold tracking-tight" style="color: var(--ds-text)">
              Optimierter Lebenslauf-Generator &amp; Kugelsicheres Profil
            </h2>
            <p class="text-xs" style="color: var(--ds-text-subtlest)">
              Alle CV-De-Risking-Empfehlungen direkt als editierbarer A4-Lebenslauf mit echtem Word (.docx), Vektor-PDF &amp; KI-Stellen-Tailoring.
            </p>
          </div>
          <div class="segmented-control shrink-0">
            <button
              @click="cvStudioView = 'generator'"
              :class="['seg-btn', cvStudioView === 'generator' ? 'active' : '']"
            >📄 Optimierter CV-Generator</button>
            <button
              @click="cvStudioView = 'playbook'"
              :class="['seg-btn', cvStudioView === 'playbook' ? 'active' : '']"
            >🛡️ De-Risking &amp; Ampel-Playbook</button>
          </div>
        </div>

        <!-- ==================== ANSICHT 1: INTERAKTIVER CV-GENERATOR STUDIO ==================== -->
        <div v-show="cvStudioView === 'generator'" class="space-y-5">

          <!-- Preset & Export Action Toolbar -->
          <div class="bento-card p-4 sm:p-5 no-cv-print space-y-3">
            <div class="flex flex-wrap items-center justify-between gap-3">
              <div class="flex flex-wrap items-center gap-1.5 text-xs">
                <span class="font-semibold mr-1" style="color: var(--ds-text-subtlest)">Zielrollen-Profil:</span>
                <button
                  @click="applyCvPreset('universal')"
                  :class="['px-3 py-1.5 rounded-lg font-semibold border transition', cvDraft.preset === 'universal' ? 'btn-primary' : '']"
                  :style="cvDraft.preset === 'universal' ? '' : 'background: var(--ds-surface-sunken); border-color: var(--ds-border); color: var(--ds-text)'"
                >✨ Kugelsicher Universal</button>
                <button
                  @click="applyCvPreset('consulting')"
                  :class="['px-3 py-1.5 rounded-lg font-semibold border transition', cvDraft.preset === 'consulting' ? 'btn-primary' : '']"
                  :style="cvDraft.preset === 'consulting' ? '' : 'background: var(--ds-surface-sunken); border-color: var(--ds-border); color: var(--ds-text)'"
                >💼 S/4HANA Consulting</button>
                <button
                  @click="applyCvPreset('audit_iam')"
                  :class="['px-3 py-1.5 rounded-lg font-semibold border transition', cvDraft.preset === 'audit_iam' ? 'btn-primary' : '']"
                  :style="cvDraft.preset === 'audit_iam' ? '' : 'background: var(--ds-surface-sunken); border-color: var(--ds-border); color: var(--ds-text)'"
                >🛡️ IT-Audit, IKS &amp; IAM</button>
                <button
                  @click="applyCvPreset('trainee_eam')"
                  :class="['px-3 py-1.5 rounded-lg font-semibold border transition', cvDraft.preset === 'trainee_eam' ? 'btn-primary' : '']"
                  :style="cvDraft.preset === 'trainee_eam' ? '' : 'background: var(--ds-surface-sunken); border-color: var(--ds-border); color: var(--ds-text)'"
                >🏛️ IT-Trainee &amp; EAM</button>
              </div>

              <div class="flex flex-wrap items-center gap-2 text-xs">
                <button
                  @click="exportCvFile('docx')"
                  :disabled="cvExportLoading"
                  class="px-3.5 py-2 rounded-xl font-bold btn-primary disabled:opacity-50 transition flex items-center gap-1.5"
                >📥 Word (.docx)</button>
                <button
                  @click="exportCvFile('pdf')"
                  :disabled="cvExportLoading"
                  class="px-3.5 py-2 rounded-xl font-bold border transition flex items-center gap-1.5 hover:opacity-85"
                  style="background: var(--ds-bg-success); border-color: var(--ds-border-success); color: var(--ds-text-success)"
                >📕 PDF (.pdf)</button>
                <button
                  @click="printGeneratedCv"
                  class="px-3 py-2 rounded-xl font-semibold border transition hover:opacity-85"
                  style="background: var(--ds-surface-sunken); border-color: var(--ds-border); color: var(--ds-text)"
                >🖨️ Druckansicht</button>
                <button
                  @click="copyCvMarkdown"
                  class="px-3 py-2 rounded-xl font-semibold border transition hover:opacity-85"
                  style="background: var(--ds-surface-sunken); border-color: var(--ds-border); color: var(--ds-text)"
                >📋 Markdown</button>
                <button
                  @click="saveCvToWorkspace('pdf')"
                  :disabled="cvExportLoading"
                  class="px-3 py-2 rounded-xl font-semibold border transition hover:opacity-85"
                  style="background: var(--ds-bg-discovery); border-color: var(--ds-border-discovery); color: var(--ds-text-discovery)"
                  title="Speichert PDF & DOCX direkt in 00_Aktuelle_Bewerbungsunterlagen/"
                >💾 In Bewerbungsordner</button>
              </div>
            </div>
          </div>

          <!-- Split-Pane: Left Editor & AI Tailoring (5 cols) | Right Live A4 Preview (7 cols) -->
          <div class="grid grid-cols-1 xl:grid-cols-12 gap-5 items-start">

            <!-- LEFT EDITOR & CONTROLS -->
            <div class="xl:col-span-5 space-y-4 no-cv-print">

              <!-- AI Tailoring on Job Posting -->
              <div class="bento-card p-4 space-y-3">
                <div class="flex items-center justify-between gap-2">
                  <div class="font-bold text-xs flex items-center gap-1.5" style="color: var(--ds-text)">
                    <span>🤖</span>
                    <span>KI-Stellen-Tailoring (Obsidian RAG + De-Risking)</span>
                  </div>
                  <div class="flex gap-1 text-[10px]">
                    <button @click="fillCvJobSample('kpmg')" class="px-2 py-0.5 rounded border hover:opacity-80" style="background: var(--ds-surface-sunken); border-color: var(--ds-border); color: var(--ds-text-brand)">KPMG</button>
                    <button @click="fillCvJobSample('schwarz')" class="px-2 py-0.5 rounded border hover:opacity-80" style="background: var(--ds-surface-sunken); border-color: var(--ds-border); color: var(--ds-text-brand)">Schwarz</button>
                    <button @click="fillCvJobSample('trumpf')" class="px-2 py-0.5 rounded border hover:opacity-80" style="background: var(--ds-surface-sunken); border-color: var(--ds-border); color: var(--ds-text-brand)">TRUMPF</button>
                  </div>
                </div>
                <div class="grid grid-cols-2 gap-2">
                  <input v-model="cvTailorCompany" type="text" placeholder="Unternehmen (optional)" class="px-2.5 py-1.5 text-xs rounded-lg border focus:outline-none">
                  <input v-model="cvTailorRole" type="text" placeholder="Zielrolle (optional)" class="px-2.5 py-1.5 text-xs rounded-lg border focus:outline-none">
                </div>
                <textarea
                  v-model="cvTailorJobText"
                  rows="3"
                  placeholder="Stellenanzeige oder Anforderungen einfügen – KI passt Kurzprofil, SSB-Schwerpunkte und ATS-Keywords kugelsicher an..."
                  class="w-full p-2.5 text-xs rounded-lg border focus:outline-none custom-scrollbar"
                ></textarea>
                <div class="flex items-center justify-between gap-2">
                  <span class="text-[11px] font-mono truncate" style="color: var(--ds-text-subtlest)">{{ cvTailorStatus || 'Wendet alle 4 De-Risking-Regeln automatisch an.' }}</span>
                  <button
                    @click="runCvTailoring"
                    :disabled="cvTailorLoading"
                    class="px-3 py-1.5 rounded-lg text-xs font-bold btn-primary disabled:opacity-50 shrink-0"
                  >{{ cvTailorLoading ? 'Optimiere...' : '✨ Auf Stelle optimieren' }}</button>
                </div>
                <div v-if="cvTailorHighlights.length > 0" class="p-2.5 rounded-lg border space-y-1 text-[11px]" style="background: var(--ds-bg-success); border-color: var(--ds-border-success); color: var(--ds-text-success)">
                  <div class="font-bold">Optimierungs-Protokoll:</div>
                  <ul class="list-disc pl-4 space-y-0.5">
                    <li v-for="(hl, i) in cvTailorHighlights" :key="i">{{ hl }}</li>
                  </ul>
                </div>
              </div>

              <!-- Layout, Theme & Modular Toggles -->
              <div class="bento-card p-4 space-y-3">
                <div class="flex items-center justify-between">
                  <span class="font-bold text-xs" style="color: var(--ds-text)">🎛️ Layout &amp; Sichtbare Bausteine</span>
                  <button @click="resetCvDraft" class="text-[11px] font-semibold hover:underline" style="color: var(--ds-text-brand)">↺ Reset</button>
                </div>

                <div class="grid grid-cols-2 gap-2 text-[11px]">
                  <div class="segmented-control w-full justify-center">
                    <button @click="cvDraft.theme = 'modern-cobalt'" :class="['seg-btn flex-1 text-center', cvDraft.theme === 'modern-cobalt' ? 'active' : '']">Cobalt Navy</button>
                    <button @click="cvDraft.theme = 'classic-mono'" :class="['seg-btn flex-1 text-center', cvDraft.theme === 'classic-mono' ? 'active' : '']">Monochrom</button>
                  </div>
                  <div class="segmented-control w-full justify-center">
                    <button @click="cvDraft.compact = true" :class="['seg-btn flex-1 text-center', cvDraft.compact ? 'active' : '']">1 Seite Fit</button>
                    <button @click="cvDraft.compact = false" :class="['seg-btn flex-1 text-center', !cvDraft.compact ? 'active' : '']">Ausführlich</button>
                  </div>
                </div>

                <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs pt-1">
                  <label class="flex items-center gap-2 cursor-pointer p-2 rounded-lg border" style="background: var(--ds-surface-sunken); border-color: var(--ds-border); color: var(--ds-text-subtle)">
                    <input type="checkbox" v-model="cvDraft.showSummary" class="accent-blue-600">
                    <span>Executive Kurzprofil</span>
                  </label>
                  <label class="flex items-center gap-2 cursor-pointer p-2 rounded-lg border" style="background: var(--ds-surface-sunken); border-color: var(--ds-border); color: var(--ds-text-subtle)">
                    <input type="checkbox" v-model="cvDraft.showMasterDetails" class="accent-blue-600">
                    <span>Masterarbeit 1,0 &amp; Module</span>
                  </label>
                  <label class="flex items-center gap-2 cursor-pointer p-2 rounded-lg border" style="background: var(--ds-surface-sunken); border-color: var(--ds-border); color: var(--ds-text-subtle)">
                    <input type="checkbox" v-model="cvDraft.showBachelor" class="accent-blue-600">
                    <span>B.Sc. (180 ECTS • 1,7)</span>
                  </label>
                  <label class="flex items-center gap-2 cursor-pointer p-2 rounded-lg border" style="background: var(--ds-surface-sunken); border-color: var(--ds-border); color: var(--ds-text-subtle)">
                    <input type="checkbox" v-model="cvDraft.showVismuv" class="accent-blue-600">
                    <span>VISMUV (ab 11/2026)</span>
                  </label>
                  <label class="flex items-center gap-2 cursor-pointer p-2 rounded-lg border" style="background: var(--ds-surface-sunken); border-color: var(--ds-border); color: var(--ds-text-subtle)">
                    <input type="checkbox" v-model="cvDraft.showPdr" class="accent-blue-600">
                    <span>PDR Team (09–11/2026)</span>
                  </label>
                  <label class="flex items-center gap-2 cursor-pointer p-2 rounded-lg border" style="background: var(--ds-surface-sunken); border-color: var(--ds-border); color: var(--ds-text-subtle)">
                    <input type="checkbox" v-model="cvDraft.showExtra" class="accent-blue-600">
                    <span>TOGAF 9 &amp; Ehrenamt</span>
                  </label>
                </div>
              </div>

              <!-- Before/After De-Risking Audit Checklist -->
              <div class="bento-card p-4 space-y-2 text-[11px]">
                <div class="font-bold text-xs flex items-center justify-between" style="color: var(--ds-text)">
                  <span>✅ Aktive Verbesserungen vs. Alt-CV</span>
                  <span class="status-pill status-pill-green">5 / 5 Gelöst</span>
                </div>
                <ul class="space-y-1.5" style="color: var(--ds-text-subtle)">
                  <li><strong style="color: var(--ds-text-success)">✓ Coding-Fallen entfernt:</strong> Java/Python/UiPath als Architektur-, Daten- &amp; Process-Automation-Analyse geframt.</li>
                  <li><strong style="color: var(--ds-text-success)">✓ Masterarbeit 1,0 sichtbar:</strong> Note 1,0, 120 ECTS &amp; 12 Experteninterviews prominent ergänzt.</li>
                  <li><strong style="color: var(--ds-text-success)">✓ SSB auf PMO-Niveau:</strong> TP1–TP5, SDD, Cloud ALM How2Handle, Signavio, Enable Now &amp; LTMC/CVI statt „Teams-Kanäle“.</li>
                  <li><strong style="color: var(--ds-text-success)">✓ B.Sc. &amp; TOGAF ergänzt:</strong> B.Sc. (180 ECTS, Thesis 1,7) + TOGAF 9 ADM Zertifikat integriert.</li>
                  <li><strong style="color: var(--ds-text-success)">✓ Form &amp; Typo bereinigt:</strong> „O2/2024“ → „02/2024“, S/4HANA &amp; Sprachen (DE/AL/EN C1) vervollständigt.</li>
                </ul>
              </div>

              <!-- Live Text Editor -->
              <div class="bento-card p-4 space-y-3 text-xs">
                <div class="font-bold" style="color: var(--ds-text)">✏️ Feinschliff (synchronisiert Live-Vorschau)</div>
                <div class="grid grid-cols-1 sm:grid-cols-3 gap-2">
                  <div class="space-y-1">
                    <label class="text-[10.5px] font-semibold" style="color: var(--ds-text-subtlest)">E-Mail</label>
                    <input v-model="cvDraft.header.email" type="text" placeholder="lokal aus CV geladen" class="w-full px-2 py-1 text-[11px] rounded-lg border">
                  </div>
                  <div class="space-y-1">
                    <label class="text-[10.5px] font-semibold" style="color: var(--ds-text-subtlest)">Telefon</label>
                    <input v-model="cvDraft.header.phone" type="text" placeholder="lokal aus CV geladen" class="w-full px-2 py-1 text-[11px] rounded-lg border">
                  </div>
                  <div class="space-y-1">
                    <label class="text-[10.5px] font-semibold" style="color: var(--ds-text-subtlest)">Adresse</label>
                    <input v-model="cvDraft.header.address" type="text" class="w-full px-2 py-1 text-[11px] rounded-lg border">
                  </div>
                </div>
                <div class="space-y-1">
                  <label class="text-[11px] font-semibold" style="color: var(--ds-text-subtlest)">Ziel-Headline / Untertitel</label>
                  <input v-model="cvDraft.header.subtitle" type="text" class="w-full px-2.5 py-1.5 text-xs rounded-lg border">
                </div>
                <div v-if="cvDraft.showSummary" class="space-y-1">
                  <label class="text-[11px] font-semibold" style="color: var(--ds-text-subtlest)">Kurzprofil</label>
                  <textarea v-model="cvDraft.summary" rows="3" class="w-full p-2 text-xs rounded-lg border custom-scrollbar"></textarea>
                </div>
                <div class="space-y-1">
                  <label class="text-[11px] font-semibold" style="color: var(--ds-text-subtlest)">SSB AG Bullets (1 Zeile = 1 Bullet)</label>
                  <textarea
                    :value="cvExpBulletsText(0)"
                    @input="updateCvExpBullets(0, $event.target.value)"
                    rows="4"
                    class="w-full p-2 text-[11px] rounded-lg border custom-scrollbar"
                  ></textarea>
                </div>
                <div class="space-y-1">
                  <label class="text-[11px] font-semibold" style="color: var(--ds-text-subtlest)">Datacenter One Bullets (1 Zeile = 1 Bullet)</label>
                  <textarea
                    :value="cvExpBulletsText(1)"
                    @input="updateCvExpBullets(1, $event.target.value)"
                    rows="3"
                    class="w-full p-2 text-[11px] rounded-lg border custom-scrollbar"
                  ></textarea>
                </div>
                <div class="space-y-1">
                  <label class="text-[11px] font-semibold" style="color: var(--ds-text-subtlest)">ERP &amp; Architektur-Governance Skills</label>
                  <textarea v-model="cvDraft.skills.erp_governance" rows="2" class="w-full p-2 text-[11px] rounded-lg border custom-scrollbar"></textarea>
                </div>
                <div class="space-y-1">
                  <label class="text-[11px] font-semibold" style="color: var(--ds-text-subtlest)">Daten &amp; Prozessautomatisierung (De-risked)</label>
                  <textarea v-model="cvDraft.skills.data_analysis" rows="2" class="w-full p-2 text-[11px] rounded-lg border custom-scrollbar"></textarea>
                </div>
              </div>
            </div>

            <!-- RIGHT LIVE A4 PAPER PREVIEW -->
            <div class="xl:col-span-7">
              <div
                id="cv-print-sheet"
                class="cv-a4-paper rounded-xl p-6 sm:p-8 space-y-3"
                :class="cvDraft.compact ? 'text-[11.2px] leading-snug' : 'text-[12px] leading-normal'"
              >
                <!-- CV Header -->
                <div class="space-y-0.5 pb-1">
                  <h1 class="text-2xl font-extrabold tracking-tight" style="color: #0F172A">{{ cvDraft.header.name }}</h1>
                  <div
                    v-if="cvDraft.header.subtitle"
                    class="text-xs font-bold"
                    :style="{ color: cvDraft.theme === 'modern-cobalt' ? '#1E40AF' : '#334155' }"
                  >{{ cvDraft.header.subtitle }}</div>
                  <div class="text-[10.5px] pt-0.5" style="color: #475569">
                    {{ [cvDraft.header.email, cvDraft.header.phone, cvDraft.header.address, cvDraft.header.links].filter(Boolean).join(' • ') }}
                  </div>
                </div>

                <!-- Kurzprofil -->
                <div v-if="cvDraft.showSummary && cvDraft.summary" class="space-y-1 pt-1">
                  <div
                    class="text-[10.5px] font-extrabold uppercase tracking-wider pb-0.5 border-b"
                    :style="{ color: cvDraft.theme === 'modern-cobalt' ? '#1E40AF' : '#1E293B', borderColor: cvDraft.theme === 'modern-cobalt' ? '#1E40AF' : '#1E293B' }"
                  >Kurzprofil</div>
                  <p style="color: #1E293B">{{ cvDraft.summary }}</p>
                </div>

                <!-- Berufserfahrung -->
                <div class="space-y-2 pt-1">
                  <div
                    class="text-[10.5px] font-extrabold uppercase tracking-wider pb-0.5 border-b"
                    :style="{ color: cvDraft.theme === 'modern-cobalt' ? '#1E40AF' : '#1E293B', borderColor: cvDraft.theme === 'modern-cobalt' ? '#1E40AF' : '#1E293B' }"
                  >Berufserfahrung</div>
                  <div v-for="ex in activeCvExperience" :key="ex.id" class="space-y-0.5">
                    <div class="flex items-baseline justify-between gap-2">
                      <span class="font-bold text-[12px]" style="color: #0F172A">{{ ex.company }}</span>
                      <span class="font-bold text-[10.5px] whitespace-nowrap" style="color: #475569">{{ ex.period }}</span>
                    </div>
                    <div class="italic text-[11px] font-medium" :style="{ color: cvDraft.theme === 'modern-cobalt' ? '#2563EB' : '#334155' }">{{ ex.role }}</div>
                    <ul class="list-disc pl-4 space-y-0.5" style="color: #1E293B">
                      <li v-for="(b, bi) in ex.bullets" :key="bi">{{ b }}</li>
                    </ul>
                  </div>
                </div>

                <!-- Studium -->
                <div class="space-y-2 pt-1">
                  <div
                    class="text-[10.5px] font-extrabold uppercase tracking-wider pb-0.5 border-b"
                    :style="{ color: cvDraft.theme === 'modern-cobalt' ? '#1E40AF' : '#1E293B', borderColor: cvDraft.theme === 'modern-cobalt' ? '#1E40AF' : '#1E293B' }"
                  >Studium</div>
                  <div v-for="ed in activeCvEducation" :key="ed.id" class="space-y-0.5">
                    <div class="flex items-baseline justify-between gap-2">
                      <span class="font-bold text-[12px]" style="color: #0F172A">{{ ed.institution }}</span>
                      <span class="font-bold text-[10.5px] whitespace-nowrap" style="color: #475569">{{ ed.period }}</span>
                    </div>
                    <div class="italic text-[11px] font-medium" :style="{ color: cvDraft.theme === 'modern-cobalt' ? '#2563EB' : '#334155' }">{{ ed.degree }}</div>
                    <ul class="list-disc pl-4 space-y-0.5" style="color: #1E293B">
                      <li v-for="(d, di) in ed.details" :key="di">{{ d }}</li>
                    </ul>
                  </div>
                </div>

                <!-- Projekte & Unternehmertum -->
                <div v-if="activeCvProjects.length > 0" class="space-y-2 pt-1">
                  <div
                    class="text-[10.5px] font-extrabold uppercase tracking-wider pb-0.5 border-b"
                    :style="{ color: cvDraft.theme === 'modern-cobalt' ? '#1E40AF' : '#1E293B', borderColor: cvDraft.theme === 'modern-cobalt' ? '#1E40AF' : '#1E293B' }"
                  >Projekte &amp; Unternehmertum</div>
                  <div v-for="pr in activeCvProjects" :key="pr.id" class="space-y-0.5">
                    <div class="flex items-baseline justify-between gap-2">
                      <span class="font-bold text-[11.5px]" style="color: #0F172A">{{ pr.title }}</span>
                      <span class="font-bold text-[10.5px] whitespace-nowrap" style="color: #475569">{{ pr.period }}</span>
                    </div>
                    <ul class="list-disc pl-4 space-y-0.5" style="color: #1E293B">
                      <li v-for="(b, bi) in pr.bullets" :key="bi">{{ b }}</li>
                    </ul>
                  </div>
                </div>

                <!-- Qualifikationen & Kompetenzen -->
                <div class="space-y-1 pt-1">
                  <div
                    class="text-[10.5px] font-extrabold uppercase tracking-wider pb-0.5 border-b"
                    :style="{ color: cvDraft.theme === 'modern-cobalt' ? '#1E40AF' : '#1E293B', borderColor: cvDraft.theme === 'modern-cobalt' ? '#1E40AF' : '#1E293B' }"
                  >Qualifikationen &amp; Kompetenzen</div>
                  <div v-if="cvDraft.skills.erp_governance" style="color: #1E293B">
                    <strong style="color: #0F172A">ERP &amp; Architektur-Governance:</strong> {{ cvDraft.skills.erp_governance }}
                  </div>
                  <div v-if="cvDraft.skills.data_analysis" style="color: #1E293B">
                    <strong style="color: #0F172A">Daten &amp; Prozessautomatisierung:</strong> {{ cvDraft.skills.data_analysis }}
                  </div>
                  <div v-if="cvDraft.skills.pmo_tools" style="color: #1E293B">
                    <strong style="color: #0F172A">PMO, Steuerung &amp; Tools:</strong> {{ cvDraft.skills.pmo_tools }}
                  </div>
                  <div v-if="cvDraft.skills.languages" style="color: #1E293B">
                    <strong style="color: #0F172A">Sprachen:</strong> {{ cvDraft.skills.languages }}
                  </div>
                </div>

                <!-- Zertifizierung & Engagement -->
                <div v-if="cvDraft.showExtra && cvDraft.extra.length" class="space-y-1 pt-1">
                  <div
                    class="text-[10.5px] font-extrabold uppercase tracking-wider pb-0.5 border-b"
                    :style="{ color: cvDraft.theme === 'modern-cobalt' ? '#1E40AF' : '#1E293B', borderColor: cvDraft.theme === 'modern-cobalt' ? '#1E40AF' : '#1E293B' }"
                  >Zertifizierung &amp; Engagement</div>
                  <ul class="list-disc pl-4 space-y-0.5" style="color: #1E293B">
                    <li v-for="(exItem, ei) in cvDraft.extra" :key="ei">{{ exItem }}</li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- ==================== ANSICHT 2: BESTEHENDES DE-RISKING PLAYBOOK ==================== -->
        <div v-show="cvStudioView === 'playbook'" class="space-y-6 no-cv-print">

        <!-- Header Alert Banner -->
        <div class="bg-gradient-to-r from-[#1c080a] via-[#141414] to-[#141414] text-white rounded-2xl p-6 lg:p-8 shadow-xl border border-[#bf262e]/40 relative overflow-hidden">
          <div class="relative z-10 max-w-4xl space-y-3">
            <div class="flex flex-wrap items-center gap-2">
              <span class="bg-[#bf262e] text-white px-2.5 py-0.5 rounded-md text-xs font-bold uppercase tracking-wider shadow-md shadow-[#bf262e]/30">Kritische Gefahrenabwehr</span>
              <span class="bg-white/10 text-white px-2.5 py-0.5 rounded-md text-xs font-medium">Headhunter- & Architekten-Perspektive</span>
            </div>
            <h2 class="text-2xl font-black tracking-tight text-white">
              Das De-Risking Playbook: Wie du deinen Lebenslauf kugelsicher machst
            </h2>
            <p class="text-[#c4bebe] text-xs sm:text-sm leading-relaxed">
              <strong>Die schonungslose Wahrheit:</strong> Du hast im Lebenslauf Skills wie Java, UiPath oder SQL angegeben, die teilweise theoretisch oder übertrieben sind. In technischen Interviews mit Senior-Entwicklern drohen Fangfragen (z.B. Spring Boot, OOP-Patterns, UiPath REFramework).<br>
              <strong>Die beruhigende Entwarnung:</strong> Du wirst <strong>NICHT</strong> als Software-Entwickler oder RPA-Scripter eingestellt! Dein echter Marktwert liegt in der <strong>ERP-Architektur, Transformations-Governance und Clean-Core-Methodik</strong>. Wenn du versuchst, Coding vorzutäuschen, fliegst du auf. Wenn du stattdessen die nachfolgenden Pivot-Brücken nutzt, wirkst du wie ein erfahrener Stratege!
            </p>
          </div>
        </div>

        <!-- Das 3-Stufen Ampelsystem -->
        <div class="bg-[#141414] p-6 rounded-2xl border border-white/10 shadow-sm space-y-4">
          <div class="flex items-center justify-between">
            <div>
              <h3 class="text-base font-bold text-white flex items-center space-x-2">
                <span>🚦</span>
                <span>Das Ampelsystem deines Profils: Wo du angreifst, framest oder abwehrst</span>
              </h3>
              <p class="text-xs text-[#8f8888]">Kategorisiere jedes Thema in deinem Lebenslauf vor dem Gespräch</p>
            </div>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            
            <!-- GRÜN: Echte Superkräfte -->
            <div class="p-4 rounded-xl bg-emerald-500/10 border border-emerald-500/30 space-y-3">
              <div class="flex items-center space-x-2 text-emerald-400 font-bold text-xs uppercase tracking-wider">
                <span class="w-2.5 h-2.5 rounded-full bg-emerald-500"></span>
                <span>🟢 GRÜN: Echte Superkräfte (Offensive)</span>
              </div>
              <div class="text-xs text-[#c4bebe] space-y-2">
                <p class="text-white font-medium">Hier führst du das Gespräch! Sprich aktiv darüber, bringe Beispiele, zeige Tiefe:</p>
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
            <div class="p-4 rounded-xl bg-amber-500/10 border border-amber-500/30 space-y-3">
              <div class="flex items-center space-x-2 text-amber-400 font-bold text-xs uppercase tracking-wider">
                <span class="w-2.5 h-2.5 rounded-full bg-amber-500"></span>
                <span>🟡 GELB: Defensiv framen (Brücke schlagen)</span>
              </div>
              <div class="text-xs text-[#c4bebe] space-y-2">
                <p class="text-white font-medium">Niemals als Programmierer auftreten! Immer als Prozess- & Architekturkompetenz framen:</p>
                <ul class="space-y-1.5 list-disc list-inside text-[11px]">
                  <li><strong>SQL / Relationale Datenbanken:</strong> "Genutzt für Datenbereinigung und Migrations-Checks (MARA, KNA1, BSEG). Ich verstehe Datenmodelle, bin aber kein DBA."</li>
                  <li><strong>Python:</strong> "Im Master für statistische Auswertungen und Prototypen eingesetzt. Meine Stärke ist die Übersetzung in fachliche Anforderungen."</li>
                  <li><strong>TOGAF:</strong> "Zertifizierter Intensivkurs (Scape Consulting 2020) als methodischer Kompass für Schnittstellen- und Bebauungsplanung."</li>
                  <li><strong>SAP ECC 6.0:</strong> "Tiefe Analyse des Altsystems zur Scoping-Vorbereitung für das Greenfield-Target."</li>
                </ul>
              </div>
            </div>

            <!-- ROT: Gefahrenzone -->
            <div class="p-4 rounded-xl bg-red-500/10 border border-red-500/30 space-y-3">
              <div class="flex items-center space-x-2 text-red-400 font-bold text-xs uppercase tracking-wider">
                <span class="w-2.5 h-2.5 rounded-full bg-red-500"></span>
                <span>🔴 ROT: Gefahrenzone (Sofort deflecten)</span>
              </div>
              <div class="text-xs text-[#c4bebe] space-y-2">
                <p class="text-white font-medium">Absolute Fangfragen-Falle! Bei Nachfrage sofort die Pivot-Formel anwenden:</p>
                <ul class="space-y-1.5 list-disc list-inside text-[11px]">
                  <li><strong>Java / OOP / Spring Boot:</strong> "Teil des Grundlagenstudiums. In der Praxis konzentriere ich mich zu 100% auf ERP-Architektur und Clean-Core-Governance."</li>
                  <li><strong>UiPath / RPA Scripting:</strong> "Im Innovationsprojekt für die Verpackungsindustrie lag mein Fokus auf BPMN-Prozessmodellierung, Machbarkeitsanalyse und dem Business Case für KI/RPA-Workflows – nicht auf manuellem Scripting."</li>
                  <li><strong>SPRO Customizing / ABAP Coding:</strong> "Unser Dogma war Clean Core – ich habe Z-Entwicklungen im PMO verhindert, nicht selbst gecodet!"</li>
                </ul>
              </div>
            </div>

          </div>
        </div>

        <!-- Das Pivot-Playbook: 4 Meister-Dialoge -->
        <div class="bg-[#141414] p-6 rounded-2xl border border-white/10 shadow-sm space-y-4">
          <div class="flex items-center justify-between">
            <div>
              <h3 class="text-base font-bold text-white flex items-center space-x-2">
                <span>🔄</span>
                <span>Das Pivot-Playbook: Wortwörtliche Abwehr- und Umlenksätze</span>
              </h3>
              <p class="text-xs text-[#8f8888]">Klicke auf die Szenarien, um die genauen Antworten zu studieren</p>
            </div>
          </div>

          <div class="space-y-3">
            <div 
              v-for="(scenario, idx) in defenseScenarios" 
              :key="idx"
              class="border border-white/10 rounded-xl overflow-hidden bg-white/5 transition-all"
            >
              <div 
                @click="scenario.open = !scenario.open" 
                class="p-4 cursor-pointer flex items-center justify-between hover:bg-white/10 transition"
              >
                <div class="flex items-center space-x-3">
                  <span class="text-base">{{ scenario.icon }}</span>
                  <div>
                    <span class="text-xs font-bold text-red-400 uppercase tracking-wider">{{ scenario.danger }}</span>
                    <h4 class="text-sm font-semibold text-white">{{ scenario.question }}</h4>
                  </div>
                </div>
                <div class="flex items-center space-x-2">
                  <span class="text-xs text-[#bf262e] font-medium">{{ scenario.open ? 'Einklappen' : 'Antwort zeigen' }}</span>
                  <span class="text-xs text-[#8f8888]">{{ scenario.open ? '▲' : '▼' }}</span>
                </div>
              </div>

              <div v-show="scenario.open" class="p-4 border-t border-white/10 bg-black/40 space-y-3 text-xs">
                
                <div class="p-3 bg-red-500/10 border border-red-500/30 rounded-lg text-red-300">
                  <div class="font-bold flex items-center space-x-1.5 mb-1">
                    <span>❌</span>
                    <span>Tödliche Falle (Was du NIEMALS sagen darfst):</span>
                  </div>
                  <p class="leading-relaxed">{{ scenario.badAnswer }}</p>
                </div>

                <div class="p-3 bg-emerald-500/10 border border-emerald-500/30 rounded-lg text-emerald-200">
                  <div class="font-bold flex items-center space-x-1.5 mb-1">
                    <span>✅</span>
                    <span>Deine kugelsichere Meister-Antwort (Wortlaut einprägen!):</span>
                  </div>
                  <p class="leading-relaxed whitespace-pre-line font-medium">{{ scenario.goodAnswer }}</p>
                  <button 
                    @click="copyText(scenario.goodAnswer)" 
                    class="mt-2 px-2.5 py-1 bg-emerald-600 hover:bg-emerald-500 text-white rounded text-[11px] font-semibold transition"
                  >
                    Antwort in Zwischenablage kopieren 📋
                  </button>
                </div>

                <div class="p-2.5 bg-white/5 border border-white/10 rounded-lg text-[#c4bebe] text-[11px]">
                  <strong class="text-white">Warum dieser Pivot gewinnt:</strong> {{ scenario.whyItWorks }}
                </div>

              </div>
            </div>
          </div>
        </div>

        <!-- Zeugnis- & Fakten-Check: Deine belegten Noten -->
        <div class="bg-[#141414] p-6 rounded-2xl border border-white/10 shadow-sm space-y-4">
          <h3 class="text-base font-bold text-white flex items-center space-x-2">
            <span>📜</span>
            <span>Zeugnis- & Fakten-Check: Deine schwarz auf weiß belegten Erfolge</span>
          </h3>
          <p class="text-xs text-[#8f8888]">Diese Fakten sind wasserdicht belegt und bilden dein unangreifbares Fundament</p>

          <div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
            <div class="p-4 rounded-xl border border-white/10 bg-white/5 space-y-2 hover:border-[#bf262e]/40 transition">
              <div class="font-bold text-[#f87171] text-sm">Universität Stuttgart (Master M.Sc.)</div>
              <div class="text-white font-semibold">Gesamtnote: 1,6 „gut“ (120 ECTS) | Masterarbeit: 1,0</div>
              <p class="text-[#c4bebe] text-[11px] leading-relaxed">
                Amtliches Zeugnis über die Masterprüfung (17.09.2026, Prof. Dr. Becker): Masterarbeit (1,0, Prof. Herzwurm), Digitale Nachhaltigkeit (1,0), FPWI (1,3), Advanced Software Engineering (1,6), Software-Architektur (1,7), Applied AI (1,7), Seminar WI (1,7).
              </p>
              <div class="text-[10px] text-emerald-400 font-bold">Amtlich beglaubigte universitäre Spitzenleistung</div>
            </div>

            <div class="p-4 rounded-xl border border-white/10 bg-white/5 space-y-2 hover:border-[#bf262e]/40 transition">
              <div class="font-bold text-[#f87171] text-sm">SSB AG Zwischenzeugnis</div>
              <div class="text-white font-semibold">24 Monate IT-PMO (01.05.2024 – 30.04.2026)</div>
              <p class="text-[#c4bebe] text-[11px] leading-relaxed">
                Ausgestellt von IT-Leitung & Gesamtprojektleitung. Bestbewertung: "stets zu unserer vollen Zufriedenheit", "vorbildliche Einsatzbereitschaft und Arbeitsweise".
              </p>
              <div class="text-[10px] text-emerald-400 font-bold">Vorstandsnah gezeichnetes Top-Zeugnis</div>
            </div>

            <div class="p-4 rounded-xl border border-white/10 bg-white/5 space-y-2 hover:border-[#bf262e]/40 transition">
              <div class="font-bold text-[#f87171] text-sm">Datacenter One & Zertifikate</div>
              <div class="text-white font-semibold">12 Monate INOC + TOGAF Intensive</div>
              <p class="text-[#c4bebe] text-[11px] leading-relaxed">
                Datacenter One: 1st/2nd Level Incident Management, Monitoring, ITSM Service Desk &amp; Wissensdatenbank. TOGAF-Intensivkurs bei Scape Consulting (Dr. Daniel Simon, Jan 2020).
              </p>
              <div class="text-[10px] text-emerald-400 font-bold">Operatives ITIL- & Architektur-Fundament</div>
            </div>
          </div>
        </div>

        <!-- CV Optimierungs-Matrix (Vorher vs. Nachher Wording) -->
        <div class="bg-[#141414] p-6 rounded-2xl border border-white/10 shadow-sm space-y-4">
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
            <div>
              <h3 class="text-base font-bold text-white flex items-center space-x-2">
                <span>📝</span>
                <span>CV-Optimierungs-Empfehlungen: Vom Minenfeld zum kugelsicheren Profil</span>
              </h3>
              <p class="text-xs text-[#8f8888]">So solltest du deine Skills im Lebenslauf formulieren, um Einladungen zu maximieren und Fangfragen auszuschließen</p>
            </div>
            <button
              @click="cvStudioView = 'generator'; scrollToTop()"
              class="px-4 py-2 rounded-xl text-xs font-bold btn-primary shrink-0 transition"
            >✨ Optimierten Lebenslauf daraus erstellen ➔</button>
          </div>

          <div class="overflow-x-auto">
            <table class="w-full text-left text-xs border border-white/10 rounded-xl overflow-hidden">
              <thead class="bg-white/5 text-white font-bold">
                <tr>
                  <th class="p-3 border-b border-white/10">Bereich im CV</th>
                  <th class="p-3 border-b border-white/10 text-red-400">Bisherige Formulierung (Gefahr)</th>
                  <th class="p-3 border-b border-white/10 text-emerald-400">Optimierte Formulierung (Kugelsicher)</th>
                  <th class="p-3 border-b border-white/10">Strategischer Effekt</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-white/10 text-[#c4bebe]">
                <tr v-for="(item, idx) in cvImprovements" :key="idx" class="hover:bg-white/5 transition">
                  <td class="p-3 font-semibold text-white">{{ item.area }}</td>
                  <td class="p-3 bg-red-500/10 text-red-300 font-mono text-[11px]">{{ item.oldText }}</td>
                  <td class="p-3 bg-emerald-500/10 text-emerald-200 font-medium">{{ item.newText }}</td>
                  <td class="p-3 text-[11px]">{{ item.effect }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        </div> <!-- End playbook view -->
      </div>
"""
