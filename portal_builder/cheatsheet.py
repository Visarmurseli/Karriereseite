# -*- coding: utf-8 -*-

def get_cheatsheet():
    return """
      <!-- ================= TAB 9: UNIVERSAL TECH & ARCHITECTURE CHEATSHEET ================= -->
      <div v-show="activeTab === 'cheatsheet'" class="space-y-6">
        
        <div class="bg-white dark:bg-slate-900 p-6 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm space-y-4">
          <div class="flex items-center justify-between">
            <div>
              <h3 class="text-lg font-bold text-slate-900 dark:text-white">Universal Architecture & Technology Cheatsheet</h3>
              <p class="text-xs text-slate-500">Dein lebenslanger Spickzettel für moderne ERP-, Cloud- und Datenarchitekturen</p>
            </div>
            <span class="tag-badge bg-blue-100 text-blue-800 dark:bg-blue-900/60 dark:text-blue-300">Quick Reference Guide</span>
          </div>

          <!-- Section 1: SAP S/4HANA Modern Tech Stack -->
          <div class="space-y-3 pt-2">
            <h4 class="text-sm font-bold text-slate-900 dark:text-white flex items-center space-x-2">
              <span>⚡</span>
              <span>1. Modern SAP S/4HANA Architecture (Fiori, CDS & RAP)</span>
            </h4>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-3 text-xs">
              <div class="p-3.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/40 space-y-1">
                <div class="font-bold text-blue-600">Core Data Services (CDS Views)</div>
                <p class="text-slate-600 dark:text-slate-300 text-[11px] leading-relaxed">
                  Semantische Datenschicht direkt auf der SAP HANA Datenbank. Verschiebt Berechnungen und Verknüpfungen von der Anwendungsschicht in die In-Memory-Datenbank (<strong>Code-to-Data Paradigma</strong>). Ersetzt klassische Datenbank-Views und bereitet Daten direkt für UI5/Fiori oder Analytics auf.
                </p>
              </div>

              <div class="p-3.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/40 space-y-1">
                <div class="font-bold text-purple-600">ABAP Cloud & RAP Model</div>
                <p class="text-slate-600 dark:text-slate-300 text-[11px] leading-relaxed">
                  <strong>RESTful Application Programming (RAP):</strong> Der offizielle, cloud-fähige Entwicklungsstandard für S/4HANA. Trennt strikt zwischen Datenmodellierung (CDS), Business Logic (Behavior Definitions) und Service Binding (OData V4 Exposure). Volle Clean-Core-Konformität!
                </p>
              </div>

              <div class="p-3.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/40 space-y-1">
                <div class="font-bold text-emerald-600">SAP Fiori & OData Protocols</div>
                <p class="text-slate-600 dark:text-slate-300 text-[11px] leading-relaxed">
                  <strong>OData V2 vs. V4:</strong> V4 bietet Batch-Optimierung, geringeren Overhead und asynchrone Verarbeitung.<br>
                  <strong>Fiori Elements:</strong> Metadaten-gesteuerte UI-Generierung aus CDS Annotations (List Reports, Object Pages). Standardisiert, barrierefrei und wartungsarm.
                </p>
              </div>
            </div>
          </div>

          <!-- Section 2: SAP Business Technology Platform (BTP) -->
          <div class="space-y-3 pt-3">
            <h4 class="text-sm font-bold text-slate-900 dark:text-white flex items-center space-x-2">
              <span>☁️</span>
              <span>2. SAP BTP Service-Kompass (Side-by-Side Extensibility)</span>
            </h4>

            <div class="grid grid-cols-1 md:grid-cols-4 gap-3 text-xs">
              <div class="p-3 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/40">
                <div class="font-bold text-slate-900 dark:text-white mb-1">Integration Suite</div>
                <div class="text-[11px] text-blue-600 font-semibold mb-1">Cloud Integration (CPI) & API Mgmt</div>
                <p class="text-slate-600 dark:text-slate-300 text-[11px]">
                  Orchestrierung aller Drittsysteme (xSuite, d.velop, PATRIS). Vorgefertigte Integrationspakete (iFlows), Protokolltransformation (REST, SOAP, IDoc, OData).
                </p>
              </div>

              <div class="p-3 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/40">
                <div class="font-bold text-slate-900 dark:text-white mb-1">SAP Build</div>
                <div class="text-[11px] text-purple-600 font-semibold mb-1">Low-Code / No-Code Suite</div>
                <p class="text-slate-600 dark:text-slate-300 text-[11px]">
                  Schnelle Erstellung von Genehmigungsworkflows (Build Process Automation) und mobilen Apps für Werkstätten und Fahrer ohne Eingriff in den Kern.
                </p>
              </div>

              <div class="p-3 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/40">
                <div class="font-bold text-slate-900 dark:text-white mb-1">SAP Event Mesh</div>
                <div class="text-[11px] text-emerald-600 font-semibold mb-1">Event-Driven Architecture (EDA)</div>
                <p class="text-slate-600 dark:text-slate-300 text-[11px]">
                  Asynchrone Ereignissteuerung: Wenn im S/4HANA ein Business Partner oder eine Störung angelegt wird, publiziert das System ein Event, das externe Systeme entkoppelt konsumieren.
                </p>
              </div>

              <div class="p-3 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/40">
                <div class="font-bold text-slate-900 dark:text-white mb-1">SAP HANA Cloud</div>
                <div class="text-[11px] text-amber-600 font-semibold mb-1">Data Fabric & Analytics</div>
                <p class="text-slate-600 dark:text-slate-300 text-[11px]">
                  Skalierbare In-Memory-Datenbank in der Cloud. Anbindung an SAP Datasphere zur konzernweiten Datenharmonisierung ohne Replikationsredundanz.
                </p>
              </div>
            </div>
          </div>

          <!-- Section 3: Relational Data Engineering & SQL -->
          <div class="space-y-3 pt-3">
            <h4 class="text-sm font-bold text-slate-900 dark:text-white flex items-center space-x-2">
              <span>🗄️</span>
              <span>3. Relationale Datenbanken & Daten-Architektur (Architekten-Perspektive)</span>
            </h4>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-3 text-xs">
              <div class="p-3 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/40 space-y-1">
                <div class="font-bold text-slate-900 dark:text-white">Normalisierung & Konsistenz</div>
                <ul class="text-slate-600 dark:text-slate-300 space-y-1 list-disc list-inside text-[11px]">
                  <li><strong>1NF:</strong> Atomare Wertebereiche (keine Listen im Feld).</li>
                  <li><strong>2NF:</strong> 1NF + voll funktional abhängig vom Primärschlüssel.</li>
                  <li><strong>3NF:</strong> 2NF + keine transitiven Abhängigkeiten (keine Nicht-Schlüsselattribute bestimmen andere Nicht-Schlüsselattribute).</li>
                </ul>
              </div>

              <div class="p-3 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/40 space-y-1">
                <div class="font-bold text-slate-900 dark:text-white">ACID-Prinzipien im ERP</div>
                <ul class="text-slate-600 dark:text-slate-300 space-y-1 list-disc list-inside text-[11px]">
                  <li><strong>Atomarität (A):</strong> Ganz oder gar nicht (Rollback bei Fehler).</li>
                  <li><strong>Konsistenz (C):</strong> Gültige Zustände und Fremdschlüsselintegrität.</li>
                  <li><strong>Isolation (I):</strong> Gleichzeitige Transaktionen beeinflussen sich nicht.</li>
                  <li><strong>Dauerhaftigkeit (D):</strong> Festgeschriebene Daten überstehen Abstürze.</li>
                </ul>
              </div>

              <div class="p-3 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/40 space-y-1">
                <div class="font-bold text-slate-900 dark:text-white">JOIN-Mechanismen & Performance</div>
                <ul class="text-slate-600 dark:text-slate-300 space-y-1 list-disc list-inside text-[11px]">
                  <li><strong>INNER JOIN:</strong> Nur Treffer auf beiden Seiten.</li>
                  <li><strong>LEFT OUTER JOIN:</strong> Alle Datensätze links + passende rechts (Standard bei optionalen Attributen).</li>
                  <li><strong>Indexierung:</strong> B-Tree für Bereichsabfragen, Hash-Index für Punktabfragen. In SAP HANA: Column-Store mit automatischer Komprimierung.</li>
                </ul>
              </div>
            </div>
          </div>

        </div>

      </div>
"""
