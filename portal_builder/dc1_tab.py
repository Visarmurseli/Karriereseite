# -*- coding: utf-8 -*-

def get_dc1_tab():
    return """
      <!-- ================= TAB 3: DATACENTER ONE (DC1) – 12 MONATE ITIL 4 OPERATIONS ================= -->
      <div v-show="activeTab === 'dc1'" class="space-y-6">

        <div class="bg-[#141414] p-6 rounded-2xl border border-white/10 space-y-5">
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
            <div>
              <div class="flex flex-wrap items-center gap-2 mb-1.5">
                <span class="status-pill status-pill-green">12 Monate (05/2023 – 04/2024)</span>
                <span class="status-pill status-pill-blue">24/7 INOC Leitstand • ITIL 4</span>
              </div>
              <h2 class="text-xl sm:text-2xl font-extrabold text-white tracking-tight">
                🖥️ Datacenter One GmbH: ITIL 4 Service Operations
              </h2>
              <p class="text-xs sm:text-sm text-[#8f8888] mt-1">
                Werkstudent im 24/7 Information Network Operation Center (INOC) – Hochverfügbarkeits-Betrieb, Service Desk &amp; Prozessstandardisierung.
              </p>
            </div>
          </div>

          <!-- 2x2 ATS Core Grid -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
            <div class="p-4 rounded-xl bg-white/5 border border-white/10 space-y-2">
              <div class="flex items-center justify-between">
                <h3 class="font-bold text-white text-sm">1. 24/7 Monitoring &amp; Infrastruktur</h3>
                <span class="status-pill status-pill-green">PRTG &amp; SLA</span>
              </div>
              <p class="text-[#c4bebe] leading-relaxed">
                Kontinuierliche Überwachung von Core-Netzwerken, Dark-Fiber-Strecken, USV-Anlagen und Rechenzentrums-Klimatechnik über PRTG. Früherkennung kritischer Anomalien im 24/7-Leitstand zur Sicherung von 99,99 % SLA-Verfügbarkeit.
              </p>
            </div>

            <div class="p-4 rounded-xl bg-white/5 border border-white/10 space-y-2">
              <div class="flex items-center justify-between">
                <h3 class="font-bold text-white text-sm">2. ITIL 4 Incident &amp; Service Desk (SPoC)</h3>
                <span class="status-pill status-pill-blue">ITSM</span>
              </div>
              <p class="text-[#c4bebe] leading-relaxed">
                Single Point of Contact (SPoC) für B2B-Kunden, Colocation-Mieter und Servicetechniker. Strukturierte Triage, Priorisierung, SLA-konforme Dokumentation und Major-Incident-Eskalation nach ITIL 4.
              </p>
            </div>

            <div class="p-4 rounded-xl bg-white/5 border border-white/10 space-y-2">
              <div class="flex items-center justify-between">
                <h3 class="font-bold text-white text-sm">3. Wissensmanagement &amp; SOP-Standardisierung</h3>
                <span class="status-pill status-pill-purple">Knowledge Base</span>
              </div>
              <p class="text-[#c4bebe] leading-relaxed">
                Konzeption und Aufbau einer zentralen Wissensdatenbank (Standard Operating Procedures) für Netzausfälle, Notfall-Paging, Zutrittskontrollen und Carrier-Eskalationen zur Beschleunigung von Einarbeitung und Entstörung.
              </p>
            </div>

            <div class="p-4 rounded-xl bg-white/5 border border-white/10 space-y-2">
              <div class="flex items-center justify-between">
                <h3 class="font-bold text-white text-sm">4. Hardware-Lifecycle &amp; Carriermanagement</h3>
                <span class="status-pill status-pill-amber">100+ Systeme</span>
              </div>
              <p class="text-[#c4bebe] leading-relaxed">
                Steuerung des unternehmensweiten Hardware-Rollouts für über 100 Leitstands- &amp; Client-Systeme (Dell PoC, Visio-Sollprozess, BSI-konformes Decommissioning) sowie Koordination von Carriern (Telekom, Colt, Vodafone) bei Trassenstörungen.
              </p>
            </div>
          </div>

          <!-- Strategic Transfer to S/4HANA & Enterprise IT -->
          <div class="info-callout p-4 flex flex-col sm:flex-row sm:items-center justify-between gap-3 text-xs">
            <div class="space-y-1">
              <div class="font-bold text-white">💡 Transferwert für SAP S/4HANA &amp; Enterprise Architecture</div>
              <p class="text-[#c4bebe] leading-relaxed">
                Aus 12 Monaten 24/7-Leitstand übertrage ich kompromisslose <strong>Hochverfügbarkeits-Disziplin</strong>, präzises <strong>Incident- &amp; Eskalationsmanagement</strong> sowie gelebte <strong>SOP-Dokumentationsqualität</strong> direkt in SAP Activate Run-Readiness, Cutover-Steuerung und Hypercare.
              </p>
            </div>
            <button @click="selectTab('faq')" class="px-3 py-1.5 rounded-lg bg-[#bf262e] text-white font-semibold whitespace-nowrap self-start sm:self-center">
              FAQ: Operations &amp; TOGAF ➔
            </button>
          </div>
        </div>

      </div>
"""
