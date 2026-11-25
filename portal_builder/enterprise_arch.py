# -*- coding: utf-8 -*-

def get_enterprise_arch():
    return """
      <!-- ================= TAB 8: DATACENTER ONE (DC1) & ENTERPRISE ARCHITECTURE ================= -->
      <div v-show="activeTab === 'enterprise_arch'" class="space-y-6">
        
        <!-- Header Banner: Datacenter One (DC1) - 12 Monate Werkstudent -->
        <div class="bg-[#141414] p-6 rounded-2xl border border-white/10 shadow-sm space-y-4">
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
            <div>
              <div class="flex items-center space-x-2">
                <span class="text-xl">🖥️</span>
                <h3 class="text-lg font-bold text-white">Datacenter One GmbH (DC1) – 12 Monate ITIL 4 Service Operations</h3>
                <span class="px-2.5 py-0.5 rounded-full bg-emerald-500/15 text-emerald-300 border border-emerald-500/30 text-[10px] font-bold">05/2023 – 04/2024</span>
              </div>
              <p class="text-xs text-[#8f8888] mt-1">
                Werkstudent im Information Network Operation Center (INOC-Leitung) • Hochverfügbare Colocation-Rechenzentren (Stuttgart, Düsseldorf, Leverkusen, Hamburg).
              </p>
            </div>
            <span class="tag-badge bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 whitespace-nowrap self-start sm:self-auto">
              24/7 Mission Critical ITIL 4
            </span>
          </div>

          <!-- 4 Core Tasks at Datacenter One -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 pt-2">
            
            <div class="p-4 rounded-xl bg-white/5 border border-white/10 hover:border-[#bf262e]/30 transition space-y-2">
              <div class="flex items-center space-x-2">
                <span class="text-[#f87171] font-bold">1.</span>
                <h4 class="font-bold text-white text-xs sm:text-sm">24/7 Monitoring & Infrastructure Event Management</h4>
              </div>
              <p class="text-xs text-[#c4bebe] leading-relaxed">
                Kontinuierliche Überwachung der gesamten Rechenzentrums-Infrastruktur über PRTG Network Monitor: USV-Anlagen (Unterbrechungsfreie Stromversorgung), Diesel-Notstromgeneratoren, Klimatechnik, Kaltgangeinhausungen, Brandfrüherkennung (RAS) sowie Core-Switche und Glasfaser-Trassen.
              </p>
              <div class="text-[11px] text-[#8f8888] pt-1 border-t border-white/10">
                Fokus: Frühzeitige Erkennung von Lastspitzen, Schwellenwert-Überschreitungen und Auslösen von Vor-Ort-Bereitschaften.
              </div>
            </div>

            <div class="p-4 rounded-xl bg-white/5 border border-white/10 hover:border-[#bf262e]/30 transition space-y-2">
              <div class="flex items-center space-x-2">
                <span class="text-[#f87171] font-bold">2.</span>
                <h4 class="font-bold text-white text-xs sm:text-sm">ITIL 4 Incident- & Service-Desk-Management (SPoC)</h4>
              </div>
              <p class="text-xs text-[#c4bebe] leading-relaxed">
                Single Point of Contact (SPoC) für B2B-Kunden, Colocation-Mieter und interne Service-Techniker im Jira Service Management. Annahme, Priorisierung, Dokumentation und Zuweisung von Incidents und Service Requests unter strikter Einhaltung vertraglich garantierter SLAs (99,99% Verfügbarkeit).
              </p>
              <div class="text-[11px] text-[#8f8888] pt-1 border-t border-white/10">
                Fokus: Einhaltung von Reaktionszeiten, Major Incident Eskalation nach Eskalationsmatrix und saubere Schichtübergaben.
              </div>
            </div>

            <div class="p-4 rounded-xl bg-white/5 border border-white/10 hover:border-[#bf262e]/30 transition space-y-2">
              <div class="flex items-center space-x-2">
                <span class="text-[#f87171] font-bold">3.</span>
                <h4 class="font-bold text-white text-xs sm:text-sm">Aufbau & Standardisierung der Confluence-Wissensdatenbank</h4>
              </div>
              <p class="text-xs text-[#c4bebe] leading-relaxed">
                Konzeption und redaktioneller Aufbau eines zentralen Prozess- und Wissensportals in Atlassian Confluence. Erstellung von Standard Operating Procedures (SOPs) für Notfallszenarien, Netzausfälle, DDoS-Attacken, Zutrittskontrollen und Carrier-Eskalationspfade.
              </p>
              <div class="text-[11px] text-[#8f8888] pt-1 border-t border-white/10">
                Fokus: Beseitigung von Wissensinseln, Vereinheitlichung der Betriebsführung und strukturierte Einarbeitung neuer INOC-Mitarbeiter.
              </div>
            </div>

            <div class="p-4 rounded-xl bg-white/5 border border-white/10 hover:border-[#bf262e]/30 transition space-y-2">
              <div class="flex items-center space-x-2">
                <span class="text-[#f87171] font-bold">4.</span>
                <h4 class="font-bold text-white text-xs sm:text-sm">Hardware-Lifecycle-Management (HLM) & Carriermanagement</h4>
              </div>
              <p class="text-xs text-[#c4bebe] leading-relaxed">
                Planung und operative Durchführung eines unternehmensweiten Hardware-Rollouts: Koordination des Austauschs von über 100 Notebooks und Workstations (Dell PoC, Rollout-Fahrplan, Migration von Benutzerprofilen, datenschutzkonforme Entsorgung nach BSI-Standards). Koordination von Carriern (Telekom, Colt, Vodafone) bei Trassenstörungen.
              </p>
              <div class="text-[11px] text-[#8f8888] pt-1 border-t border-white/10">
                Fokus: Reibungsloser Austausch im laufenden 24/7 Betrieb ohne Unterbrechung kritischer Leitstand-Funktionen.
              </div>
            </div>

          </div>

          <!-- Key Learnings from Datacenter One -->
          <div class="p-4 rounded-xl bg-black/40 border border-white/10 space-y-2 mt-2">
            <h4 class="text-xs font-bold text-emerald-400 uppercase tracking-wider flex items-center space-x-1.5">
              <span>💡</span>
              <span>Zentrale Learnings für Visars Profil als IT- & ERP-Consultant:</span>
            </h4>
            <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 text-xs pt-1">
              <div class="p-3 bg-white/5 rounded-lg border border-white/10">
                <div class="font-semibold text-white mb-0.5">1. Hochverfügbarkeits-Disziplin</div>
                <p class="text-[#c4bebe] text-[11px] leading-relaxed">
                  Tiefes Verständnis für N+1 Redundanzen und SLA-Verbindlichkeiten. Übertragung auf ERP-Systeme: Warum Downtimes Millionen kosten und Cutover-Pläne sekundengenau getaktet sein müssen.
                </p>
              </div>

              <div class="p-3 bg-white/5 rounded-lg border border-white/10">
                <div class="font-semibold text-white mb-0.5">2. Standardisierte Dokumentation</div>
                <p class="text-[#c4bebe] text-[11px] leading-relaxed">
                  In kritischen Betriebslagen entscheiden standardisierte SOPs in Confluence über Minuten. Bei der SSB bildete dieses Mindset das Fundament für saubere Signavio- und ALM-Prozesse.
                </p>
              </div>

              <div class="p-3 bg-white/5 rounded-lg border border-white/10">
                <div class="font-semibold text-white mb-0.5">3. Ruhe unter Eskalationsdruck</div>
                <p class="text-[#c4bebe] text-[11px] leading-relaxed">
                  Professionelles Krisenmanagement bei Störungsmeldungen an B2B-Kunden und Führungskräfte. Fähigkeit, technische Sachverhalte schnell und sachlich auf den Punkt zu bringen.
                </p>
              </div>
            </div>
          </div>
        </div>

        <!-- Enterprise Architecture Framework: TOGAF 9 ADM -->
        <div class="bg-[#141414] p-6 rounded-2xl border border-white/10 shadow-sm space-y-4">
          <div class="flex items-center justify-between">
            <div>
              <h3 class="text-base font-bold text-white flex items-center space-x-2">
                <span>🏛️</span>
                <span>Enterprise Architecture: TOGAF 9 ADM Zyklus</span>
              </h3>
              <p class="text-xs text-[#8f8888]">Intensivkurs Scape Consulting (Dr. Daniel Simon, Universität Stuttgart, Januar 2020)</p>
            </div>
            <span class="px-2.5 py-1 rounded bg-white/10 text-white font-bold text-[11px] border border-white/10">
              📜 Zertifikat verifiziert
            </span>
          </div>

          <p class="text-xs text-[#c4bebe] leading-relaxed">
            TOGAF (The Open Group Architecture Framework) liefert den methodischen Rahmen, um Geschäftsstrategie und IT-Infrastruktur systematisch in Einklang zu bringen. Der Architecture Development Method (ADM) Zyklus wurde bei der SSB im Großprojekt SAP4SSB in der Praxis durchlaufen:
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
