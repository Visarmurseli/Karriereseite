# -*- coding: utf-8 -*-

def get_enterprise_arch():
    return """
      <!-- ================= TAB 8: ENTERPRISE ARCHITECTURE & ITIL ================= -->
      <div v-show="activeTab === 'enterprise_arch'" class="space-y-6">
        
        <div class="bg-[#141414] p-6 rounded-2xl border border-white/10 shadow-sm space-y-4">
          <div class="flex items-center justify-between">
            <div>
              <h3 class="text-lg font-bold text-white">Enterprise Architecture (TOGAF) & IT-Operations (ITIL 4)</h3>
              <p class="text-xs text-[#8f8888]">Methodisches Fundament aus TOGAF-Zertifizierung und 12 Monaten Rechenzentrumserfahrung (Datacenter One)</p>
            </div>
            <span class="tag-badge bg-[#bf262e]/20 text-[#f87171] border border-[#bf262e]/40">Scape Consulting & Datacenter One</span>
          </div>

          <!-- TOGAF ADM Cycle -->
          <div class="p-4 rounded-xl bg-white/5 border border-white/10 space-y-3 hover:border-[#bf262e]/30 transition">
            <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
              <h4 class="text-sm font-bold text-white flex items-center space-x-2">
                <span>🏛️</span>
                <span>Der TOGAF Architecture Development Method (ADM) Zyklus</span>
              </h4>
              <div class="flex items-center space-x-2">
                <span class="text-[11px] text-[#8f8888]">Intensivkurs Scape Consulting (Dr. Daniel Simon, Jan 2020)</span>
                <span class="px-2.5 py-1 rounded bg-white/10 text-white font-bold text-[11px] inline-flex items-center space-x-1 border border-white/10 shadow-sm">
                  <span>📜</span>
                  <span>Zertifikat verifiziert</span>
                </span>
              </div>
            </div>
            <p class="text-xs text-[#c4bebe] leading-relaxed">
              TOGAF ist dein strategischer Kompass, um komplexe IT-Landschaften ganzheitlich zu strukturieren. Bei der SSB hast du diesen Zyklus im Programm SAP4SSB in der Praxis erlebt:
            </p>

            <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-2.5 text-xs pt-1">
              <div class="p-3 bg-black/40 rounded-lg border border-white/10">
                <div class="font-bold text-[#f87171]">Phase A: Architecture Vision</div>
                <div class="text-[11px] text-[#8f8888] mt-0.5">Greenfield S/4HANA Private Cloud, Clean Core Leitbild und Business Case mit Nagarro.</div>
              </div>

              <div class="p-3 bg-black/40 rounded-lg border border-white/10">
                <div class="font-bold text-[#f87171]">Phase B: Business Architecture</div>
                <div class="text-[11px] text-[#8f8888] mt-0.5">Fit-to-Standard Workshops, Soll-Prozessmodellierung in SAP Signavio (BPMN 2.0).</div>
              </div>

              <div class="p-3 bg-black/40 rounded-lg border border-white/10">
                <div class="font-bold text-[#f87171]">Phase C: Information Systems</div>
                <div class="text-[11px] text-[#8f8888] mt-0.5">Datenarchitektur (CVI Business Partner, ACDOCA) und Applikationslandschaft (xSuite, d.velop).</div>
              </div>

              <div class="p-3 bg-black/40 rounded-lg border border-white/10">
                <div class="font-bold text-[#f87171]">Phase D: Technology Architecture</div>
                <div class="text-[11px] text-[#8f8888] mt-0.5">SAP BTP, Axians ES4 Systeme, Cloud-Infrastruktur, Single Sign-On und ADS-Druckdienste.</div>
              </div>

              <div class="p-3 bg-black/40 rounded-lg border border-white/10">
                <div class="font-bold text-purple-400">Phase E: Opportunities & Solutions</div>
                <div class="text-[11px] text-[#8f8888] mt-0.5">Bewertung von Standard vs. Side-by-Side BTP Erweiterungen und Partnersichtung.</div>
              </div>

              <div class="p-3 bg-black/40 rounded-lg border border-white/10">
                <div class="font-bold text-purple-400">Phase F: Migration Planning</div>
                <div class="text-[11px] text-[#8f8888] mt-0.5">Cutover-Drehbuch, Staging-Datenmigration, Freeze-Perioden und SuSa-Bilanzabgleich.</div>
              </div>

              <div class="p-3 bg-black/40 rounded-lg border border-white/10">
                <div class="font-bold text-purple-400">Phase G: Implementation Governance</div>
                <div class="text-[11px] text-[#8f8888] mt-0.5">Dein IT-PMO Kerngeschäft: Quality Gates in SAP Cloud ALM, Meilenstein-Tracking.</div>
              </div>

              <div class="p-3 bg-black/40 rounded-lg border border-white/10">
                <div class="font-bold text-purple-400">Phase H: Change Management</div>
                <div class="text-[11px] text-[#8f8888] mt-0.5">TP1 Enablement, SAP Enable Now Übergabe an HR (UB AC) und Anwenderbefähigung.</div>
              </div>
            </div>
          </div>
        </div>

        <!-- Datacenter One & ITIL Service Management -->
        <div class="bg-[#141414] p-6 rounded-2xl border border-white/10 shadow-sm space-y-4">
          <div class="flex items-center justify-between">
            <h3 class="text-base font-bold text-white flex items-center space-x-2">
              <span>🖥️</span>
              <span>ITIL 4 Service Operations (Datacenter One - 12 Monate INOC)</span>
            </h3>
            <span class="tag-badge bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">24/7 Mission Critical Operations</span>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-3 gap-3 text-xs">
            <div class="p-3.5 rounded-xl border border-white/10 bg-white/5 space-y-1.5 hover:border-[#bf262e]/30 transition">
              <div class="font-bold text-white">1. Incident & Problem Management</div>
              <p class="text-[#c4bebe] leading-relaxed text-[11px]">
                Erfassung, Klassifizierung und Behebung von Störungen im Integrated Network Operation Center (INOC). Einhaltung strikter SLAs (Service Level Agreements) für Colocation- und Cloud-Kunden. Unterscheidung zwischen Sofort-Workaround (Incident) und Ursachenanalyse (Root Cause Analysis / Problem Management).
              </p>
            </div>

            <div class="p-3.5 rounded-xl border border-white/10 bg-white/5 space-y-1.5 hover:border-[#bf262e]/30 transition">
              <div class="font-bold text-white">2. Monitoring & Event Management</div>
              <p class="text-[#c4bebe] leading-relaxed text-[11px]">
                Proaktive Überwachung von Rechenzentrums-Infrastruktur: USV-Anlagen, Klimatechnik, Glasfaser-Trassen und Core-Switche. Alarmierungsketten, Eskalationsmanagement nach Matrix und Kommunikation an Notfall-Bereitschaften.
              </p>
            </div>

            <div class="p-3.5 rounded-xl border border-white/10 bg-white/5 space-y-1.5 hover:border-[#bf262e]/30 transition">
              <div class="font-bold text-white">3. Tool-Stack: Jira & Confluence</div>
              <p class="text-[#c4bebe] leading-relaxed text-[11px]">
                Lückenlose Dokumentation von Störungsberichten und Notfallhandbüchern (Standard Operating Procedures / SOPs). Revisionssichere Übergabeprotokolle bei Schichtwechseln unter Leitung von Helmut Schmidpeter.
              </p>
            </div>
          </div>
        </div>

        <!-- BPMN 2.0 Process Modeling Standard -->
        <div class="bg-[#141414] p-6 rounded-2xl border border-white/10 shadow-sm space-y-4">
          <h3 class="text-base font-bold text-white flex items-center space-x-2">
            <span>🔄</span>
            <span>BPMN 2.0 Modellierungs-Standard (SAP Signavio Referenz)</span>
          </h3>

          <div class="grid grid-cols-1 md:grid-cols-3 gap-3 text-xs">
            <div class="p-3 rounded-xl bg-white/5 border border-white/10 hover:border-[#bf262e]/30 transition">
              <div class="font-bold text-[#f87171] mb-1">Gateways & Verzweigungen</div>
              <ul class="text-[#c4bebe] space-y-1 list-disc list-inside text-[11px]">
                <li><strong class="text-white">Exklusiv (XOR):</strong> Genau ein Pfad wird gewählt (z.B. Rechnungsbetrag > 10.000 € ? Ja/Nein).</li>
                <li><strong class="text-white">Parallel (AND):</strong> Alle ausgehenden Pfade werden gleichzeitig gestartet (z.B. Bonitätsprüfung und Lagerprüfung parallel).</li>
                <li><strong class="text-white">Inklusiv (OR):</strong> Ein oder mehrere Pfade können gewählt werden.</li>
              </ul>
            </div>

            <div class="p-3 rounded-xl bg-white/5 border border-white/10 hover:border-[#bf262e]/30 transition">
              <div class="font-bold text-purple-400 mb-1">Ereignisse (Events)</div>
              <ul class="text-[#c4bebe] space-y-1 list-disc list-inside text-[11px]">
                <li><strong class="text-white">Start-Event:</strong> Anstoß des Prozesses (z.B. Eingang BANF).</li>
                <li><strong class="text-white">Zwischen-Event:</strong> Timer (z.B. Warte 5 Tage auf Freigabe) oder Nachrichtenempfang.</li>
                <li><strong class="text-white">End-Event:</strong> Erfolgreicher Abschluss oder Fehlerabbruch (Terminating Event).</li>
              </ul>
            </div>

            <div class="p-3 rounded-xl bg-white/5 border border-white/10 hover:border-[#bf262e]/30 transition">
              <div class="font-bold text-emerald-400 mb-1">Pools & Lanes (Zuständigkeiten)</div>
              <ul class="text-[#c4bebe] space-y-1 list-disc list-inside text-[11px]">
                <li><strong class="text-white">Pool:</strong> Repräsentiert eine eigenständige Organisationseinheit (z.B. SSB AG vs. Lieferant).</li>
                <li><strong class="text-white">Lane:</strong> Teilbereich innerhalb des Pools (z.B. Einkauf, Finanzbuchhaltung, Werkstattleiter).</li>
                <li><strong class="text-white">Message Flow:</strong> Nachrichtenfluss nur zwischen verschiedenen Pools erlaubt!</li>
              </ul>
            </div>
          </div>
        </div>

      </div>
"""
