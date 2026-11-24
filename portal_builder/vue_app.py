# -*- coding: utf-8 -*-

def get_vue_app(public_mode=False):
    tpl = """
    </main>

    <!-- Footer -->
    <footer class="bg-[#121212] border-t border-white/10 py-4 px-6 text-center text-xs text-[#8f8888]">
      <div class="max-w-7xl mx-auto flex flex-col md:flex-row justify-between items-center gap-2">
        <span class="text-[#c4bebe]">Visar Murseli, M.Sc. | Enterprise Knowledge Hub & S/4HANA Career OS</span>
        <span class="text-[#bf262e] font-medium">Design System: Portfolioseite (Crimson Hue 358) | 100% lokal & persistent</span>
      </div>
    </footer>
  </div>
</div>

  <!-- Application Logic & Data Injection -->
  <script>
    const { createApp, ref, computed, onMounted } = Vue;

    createApp({
      setup() {
        const activeTab = ref('dashboard');
        const isMobileMenuOpen = ref(false);
        const degreeTab = ref('all');
        const searchQuery = ref('');
        const isDark = ref(true);
        const isCommandPaletteOpen = ref(false);
        const commandSearch = ref('');
        const wbsFilter = ref('all');
        const pitchMode = ref('short');
        const selectedQACat = ref('Alle');
        const selectedFileCat = ref('Alle');
        const personalNotes = ref('');
        const qaSearch = ref('');

        const ragQuery = ref('');
        const ragResults = ref([]);
        const ragLoading = ref(false);
        const ragAskLoading = ref(false);
        const ragAnswer = ref('');
        const ragModel = ref('');
        const ragStatusMsg = ref('');
        const pipelineData = ref({ interviews: [], open_tier1: [], open_count: 0 });

        const currentTabName = computed(() => {
          const found = tabs.find(t => t.id === activeTab.value);
          return found ? found.label : 'Dashboard';
        });

        const currentHubName = computed(() => {
          const tabId = activeTab.value;
          if (tabId === 'dashboard') return 'Profil & Einstieg';
          if (['project', 'solution_design', 'migration', 'tools'].includes(tabId)) return 'S/4HANA Transformation';
          if (['thesis', 'enterprise_arch'].includes(tabId)) return 'Akademische Exzellenz';
          if (['career', 'cheatsheet'].includes(tabId)) return 'Junior & Trainee Karriere';
          %%PRIVATE_HUB_LINE%%
          return 'Wissensportal';
        });

        const tabs = [
          { id: 'dashboard', label: 'Profil & Einstieg', icon: '📊', badge: 'Junior & Trainee' },
          { id: 'project', label: 'TP1–TP5 Steuerung & WBS', icon: '🚆', badge: 'SSB AG' },
          { id: 'solution_design', label: 'Solution Design (FI/CO)', icon: '📐', badge: 'Trennungsrechnung' },
          { id: 'migration', label: 'Datenmigration & CVI', icon: '🔄', badge: '0,00 € Saldo' },
          { id: 'tools', label: 'Toolchain Hub', icon: '🛠️', badge: 'CALM / Signavio' },
          { id: 'thesis', label: 'Masterarbeit (Note 1,0)', icon: '🎓', badge: '12 Interviews' },
          { id: 'enterprise_arch', label: 'TOGAF ADM & ITIL 4', icon: '🏛️', badge: 'EAM' },
          { id: 'career', label: 'Junior & Trainee Karriere', icon: '🎯', badge: '%%CAREER_BADGE%%' },
          { id: 'cheatsheet', label: 'Tech & BTP Cheatsheet', icon: '⚡', badge: 'Architektur' },
          // PRIVATE_TABS_START
          { id: 'interview', label: 'Interview Masterclass', icon: '🎙️', badge: 'Pitches & STAR' },
          { id: 'cv_defense', label: 'CV De-Risking', icon: '🛡️', badge: 'Gefahrenabwehr' },
          { id: 'files', label: 'Deliverables-Register', icon: '📂', badge: 'Katalog' },
          { id: 'notebook', label: 'Second Brain & RAG', icon: '📝', badge: 'Obsidian Sync' }
          // PRIVATE_TABS_END
        ];

        const qaCategories = ['Alle', 'SSB S/4HANA & Explore-Phase', 'Datacenter One & ITIL 4', 'Master & Plattformisierung', 'Bachelor & Methodenkompetenz', 'Enterprise Architecture & TOGAF', 'Persönlich & Trainee-Einstieg'];

        const fileCategories = ['Alle', 'Aktuelle Bewerbungsunterlagen', 'PMO & Steuerung', 'Explore & Lösungsdesign', 'Finance & Controlling', 'Grants Management', 'Sustainability & EHS', 'Vertrieb & PATRIS', 'Datenmigration', 'Basis & Infrastruktur', 'Vergabe & SektVO', 'Tools & Enablement', 'SAP Fachliteratur (Rheinwerk)', 'Datacenter One (DC1 / ITIL 4)', 'Wissenschaft & Uni', 'Master-Module (120 ECTS)', 'Bachelor-Module (180 ECTS)'];

        // PRIVATE_DEFENSE_START
        const defenseScenarios = ref([
          {
            icon: '☕',
            danger: 'Gefahrenstufe Rot: Java & Software-Engineering Fangfrage',
            question: '"Sie haben Java und Softwareentwicklung im CV stehen. Wie würden Sie ein Microservice-Backend mit Spring Boot aufsetzen?"',
            badAnswer: 'Versuchen zu improvisieren ("Äh, ja, mit Annotationen wie @SpringBootApplication und JPA Repositories..."). Der Interviewer merkt sofort, dass du kein Fullstack-Developer bist, und hakt gnadenlos nach!',
            goodAnswer: `Im Grundlagenstudium an der Universität Stuttgart habe ich die Softwaretechnik- und OOP-Grundlagen in Java erlernt – dadurch verstehe ich exakt, wie Entwickler denken, welche Schnittstellenverträge benötigt werden und was saubere Modularisierung bedeutet.

In meiner zweijährigen Praxis bei der SSB habe ich mich jedoch ganz bewusst gegen das eigene Hands-on-Codieren und für die Enterprise-Architektur und Transformations-Governance entschieden. Warum? Weil im Kontext moderner ERP-Systeme wie S/4HANA und dem Clean-Core-Paradigma der eigentliche Engpass nicht das Tippen von Java-Code ist, sondern die architektonische Entkopplung: Wie binden wir Drittsysteme wie xSuite oder PATRIS über standardisierte APIs an und wie orchestrieren wir Side-by-Side Erweiterungen auf der SAP BTP?

Meine Stärke liegt darin, die Brücke zwischen Fachbereich und den Entwicklerteams von Partnern wie Nagarro zu schlagen und sicherzustellen, dass Entwickler die Architekturvorgaben exakt einhalten.`,
            whyItWorks: 'Du gibst offen zu, dass Java akademisches Grundlagenwissen ist, framest es sofort als "Entwickler-Verständnis" und pivotierst auf deine unschlagbare Stärke: BTP-Architektur und Schnittstellen-Governance nach Clean Core!',
            open: true
          },
          {
            icon: '⚙️',
            danger: 'Gefahrenstufe Rot: SPRO Customizing & ABAP Fangfrage',
            question: '"Haben Sie bei der SSB schon selbst im SPRO gecustomized oder BAdIs in ABAP implementiert?"',
            badAnswer: '"Ja, ein bisschen in den Buchungskreisen rumgeklickt..." – TÖDLICH! Wenn er nach der genauen Transaktion oder Tabellenstrukturen fragt, bist du geliefert.',
            goodAnswer: `Ganz im Gegenteil – und das war eine ganz bewusste strategische Entscheidung in unserem Transformationsprogramm SAP4SSB!

Wir haben bei der SSB eine Greenfield-Einführung nach der RISE with SAP-Methodik durchgeführt. Das oberste Dogma von Gesamtprojektleiter Roland Nowak und IT-Leiter Dietmar Fillinger war: Striktes Clean Core! Klassisches Customizing im SPRO, das Systemmodifikationen erzeugt, und proprietäre Z-Tabellen im Kern waren für uns tabu, weil genau das das Altsystem über 20 Jahre verbaut hatte.

Meine Rolle im IT-PMO war es, die Einhaltung dieses Standards in den Fit-to-Standard Workshops zu steuern und abweichende Wünsche der Fachbereiche zu hinterfragen. Wenn eine Anforderung nicht im SAP-Standard abgebildet werden konnte, haben wir gemeinsam mit Nagarro geprüft, ob sie als On-Stack-Extension (ABAP Cloud / RAP) oder als Side-by-Side-Extension auf der SAP BTP realisiert wird.

Ich bin also ganz bewusst kein klassischer ABAP-Customizer alter Schule, sondern ein moderner Cloud-ERP-Architekt, der dafür sorgt, dass das System upgrade-sicher und wartbar bleibt.`,
            whyItWorks: 'Du machst aus einer vermeintlichen Schwäche ("nicht gecustomized") die modernste aller SAP-Kompetenzen: Strikte Clean-Core-Governance!',
            open: false
          },
          {
            icon: '🤖',
            danger: 'Gefahrenstufe Rot: UiPath & RPA Fangfrage',
            question: '"Erzählen Sie uns von Ihrer RPA- und Prozessanalyse im Innovationsprojekt. Wie haben Sie Machbarkeit und Business Case bewertet?"',
            badAnswer: '"Ich habe da Bots gebaut mit Activities..." – Der Interviewer fragt nach REFramework, Try-Catch-Blöcken oder Orchestrator-Triggern.',
            goodAnswer: `Im Innovationsprojekt für ein führendes Unternehmen der Verpackungsindustrie lag mein Schwerpunkt an der Schnittstelle von Business Model und Prozessautomatisierung: 

Die Patentrecherche und Fristenüberwachung war stark manuell geprägt. Ich habe die Kernprozesse mit BPMN 2.0 detailliert modelliert, Prozesskosten quantifiziert und analysiert, welche Recherche- und Monitoring-Schritte sich wirtschaftlich für eine robotergestützte Automatisierung (UiPath) in Verbindung mit KI-gestützter Volltextsuche eignen.

Meine Kernkompetenz lag in der Konzeption des hybriden Geschäftsmodells, der Business-Case-Kalkulation und der Definition der Prozessschnittstellen.

Genau diese Fähigkeit – komplexe Geschäftsprozesse strukturiert zu zerlegen, Wirtschaftlichkeit zu prüfen und Soll-Architekturen zu entwerfen – war anschließend auch bei der SSB der Schlüssel für meine Arbeit mit SAP Signavio und Cloud ALM im Solution Design.`,
            whyItWorks: 'Du positionierst dich als Business Analyst, Solution Designer und Innovationsstratege, nicht als Bot-Scripter. Das erhöht dein Ansehen sofort.',
            open: false
          },
          {
            icon: '🥊',
            danger: 'Gefahrenstufe Gelb: Die "Sie sind ja nur Absolvent"-Provokation',
            question: '"Wir suchen jemanden mit 5 bis 10 Jahren Senior-Beratungserfahrung. Warum sollten wir Sie nehmen?"',
            badAnswer: 'Defensiv werden oder dich entschuldigen ("Ich lerne aber schnell...").',
            goodAnswer: `Weil viele Berater mit 10 Jahren Erfahrung genau das Mindset mitbringen, das moderne S/4HANA-Projekte heute scheitern lässt: Sie denken immer noch in der alten ECC 6.0-Welt – mit tiefem Customizing im SPRO, ABAP-Z-Transaktionen und Modifikationen im Kern.

Ich bringe zwei unschlagbare Vorteile mit:
Erstens: Ich bin unbelastet von Legacy-Denkmustern und habe mein Verständnis von Grund auf im modernen S/4HANA Private Cloud Paradigma mit Clean Core, SAP BTP, Cloud ALM und Signavio aufgebaut.
Zweitens: Ich kenne nicht nur die Theorie. Ich habe zwei volle Jahre im IT-PMO der SSB die realen Reibungspunkte eines 3.700-Mitarbeiter-Konzerns miterlebt – von den Einwänden des Betriebsrats über die Abstimmung der Eröffnungsbilanz bis hin zur Steuerung von Implementierungspartnern wie Nagarro und Evora.

Zusätzlich habe ich in meiner Masterarbeit am Lehrstuhl von Prof. Herzwurm – die mit 1,0 bewertet wurde – 12 hochkarätige Experteninterviews geführt und genau untersucht, warum Plattform-Transformationen gelingen oder scheitern. Sie bekommen bei mir also die Dynamik eines Universitätsabsolventen, gepaart mit dem Reifegrad und Architekturverständnis eines Mid-Level Transformation Managers.`,
            whyItWorks: 'Du greifst das traditionelle "Senior-Consultant"-Stereotyp an und zeigst, dass deine 2 Jahre moderne Greenfield-Praxis + 1,0 Masterarbeit wertvoller sind als 10 Jahre veraltetes ECC-Customizing!',
            open: false
          }
        ]);

        const cvImprovements = [
          {
            area: 'Programmiersprachen',
            oldText: 'Java, Python, SQL, HTML/CSS (aktiv als Skills gelistet)',
            newText: 'Architektur- & Datenverständnis: Relationale Datenmodelle (SQL-Verständnis), Software-Engineering-Prinzipien (OOP / Clean Code), Datenanalyse',
            effect: 'Nimmt dir das Risiko von Live-Coding-Tests und stellt deine Architekturkompetenz heraus.'
          },
          {
            area: 'RPA / Automatisierung',
            oldText: 'Automatisierung & UiPath (Innovationsprojekt Verpackungsindustrie)',
            newText: 'Business Process Automation & Analyse (UiPath-Machbarkeitsprüfung, Prozesskosten-Kalkulation, PDD-Erstellung)',
            effect: 'Positioniert dich als strategischen Business Analysten statt als Script-Entwickler.'
          },
          {
            area: 'SAP-Kenntnisse',
            oldText: 'SAP ERP, SAP S/4HANA (allgemein gelistet)',
            newText: 'SAP S/4HANA Transformation Governance, Clean Core & BTP-Architektur, SAP Cloud ALM, SAP Signavio, SAP Enable Now, SAP Migration Cockpit (LTMC)',
            effect: 'Signalisiert sofort Expertenwissen in den neuesten und teuersten SAP-Technologien.'
          },
          {
            area: 'Projektmanagement',
            oldText: 'Projektunterstützung Werkstudent',
            newText: 'IT-PMO & Multiprojekt-Steuerung (24 Monate S/4HANA Großprojekt, TP1–TP5 Koordination, Lenkungsausschuss-Reporting, Partnersteuerung Nagarro/Evora)',
            effect: 'Macht aus einer "Aushilfsstelle" eine vollwertige zweijährige Projektmanagement-Erfahrung.'
          }
        ];

        const pitch60 = `Mein Name ist Visar Murseli, ich habe meinen Master in Wirtschaftsinformatik an der Universität Stuttgart mit der Note 1,6 abgeschlossen – meine Masterarbeit über S/4HANA-Plattformisierung wurde mit 1,0 bewertet. In den vergangenen zwei Jahren war ich als Werkstudent im IT-PMO beim Transformationsprogramm SAP4SSB der Stuttgarter Straßenbahnen AG tätig.

Bei der SSB habe ich die Transformation nicht vom Spielfeldrand beobachtet, sondern die Fäden zwischen den fünf Teilprojekten, der IT-Leitung und unseren Partnern Nagarro, Evora und Axians operativ zusammengehalten. Mein Fokus lag dabei auf der Tool- und Prozess-Governance mit SAP Cloud ALM und Signavio sowie auf der strategischen Übergabe von SAP Enable Now.

Genau diese Schnittstelle aus 24 Monaten Greenfield-Großprojekterfahrung und modernem Architekturwissen nach dem Clean-Core-Prinzip bringe ich mit. Heute suche ich den gezielten Einstieg als Junior SAP Consultant oder in ein anspruchsvolles IT-/Management-Traineeprogramm, um mein Praxiswissen ab Tag 1 wertschöpfend einzubringen und mit hoher Lernbereitschaft schnell zur tragenden Säule in Ihrem Team heranzuwachsen.`;

        const pitchDeep = `Wenn Sie mich nach meinem fachlichen Profil fragen, lässt sich das in drei Bausteinen zusammenfassen:

Erstens: Operative ERP-Großprojekterfahrung in einem kritischen Infrastrukturunternehmen. Die SSB AG mit 3.700 Mitarbeitern migriert von einem hochgradig modifizierten ECC 6.0 auf S/4HANA in einer RISE Private Cloud. Ich war im TP5 unter Gesamtprojektleiter Roland Nowak dafür zuständig, die Projektorganisation, das Meilenstein-Controlling und die Tool-Etablierung zu steuern. Ich kenne die realen Reibungspunkte – von der Schnittstellenintegration mit Drittsystemen wie xSuite, d.velop oder PATRIS bis hin zu den Vorbehalten des Betriebsrats bei Fiori-Rollen.

Zweitens: Fundierte Daten- und Migrationskompetenz. Ich habe mich intensiv mit den Mechanismen des SAP Migration Cockpits befasst – von der Validierung der Staging-Tabellen über Feld- und Werte-Mappings bis hin zum revisionssicheren Cutover und Bilanzabgleich im FI. Ich weiß genau, warum die Eröffnungsbilanz und das Übernahmekonto centgenau auf 0,00 € abgestimmt sein müssen und wie man Stammdaten im Rahmen von CVI sauber konsolidiert.

Drittens: Strategische Architektur- und Plattformkompetenz. Viele reden über 'Clean Core', verstehen aber die Konsequenzen nicht. In meiner Masterarbeit am Lehrstuhl von Prof. Herzwurm – die mit der Note 1,0 bewertet wurde – habe ich auf Basis von 12 Experteninterviews empirisch untersucht, welche Erfolgsfaktoren die Plattformisierung erfordert. Wer den Kern reinhalten will, muss Side-by-Side-Erweiterungen auf der SAP BTP beherrschen und APIs wie ein Produkt managen.

Ich bringe die seltene Kombination aus methodischem Weitblick, wissenschaftlicher Spitzenleistung und 24 Monaten echter Hands-on-ERP-Erfahrung mit. Für meinen Einstieg suche ich eine Junior-Rolle oder ein anspruchsvolles Traineeprogramm, in dem ich dieses Fundament sofort einbringen und mich mit hoher Motivation und Teamgeist weiterentwickeln kann.`;

        const starStories = ref([
          {
            title: 'Strategische Übergabe von SAP Enable Now an die Personalentwicklung',
            tag: 'Change & Enablement',
            expanded: true,
            s: 'Nachdem die IT die technische Aktivierung von SAP Enable Now abgeschlossen hatte, drohte das Tool als reine IT-Insellösung zu versanden, ohne dass die Fachbereiche und Key User aktiv Lerninhalte erstellten.',
            t: 'Als Werkstudent im IT-PMO sollte ich ein Übergabekonzept entwickeln, das dem Unternehmensbereich Personalentwicklung (UB AC) den strategischen Mehrwert aufzeigt und die Autoren-Befähigung anstößt.',
            a: 'Ich habe ein ganzheitliches Übergabekonzept verfasst, das das Single-Source-Prinzip (aus 1 Aufnahme entstehen Handbuch, interaktives Tutorial, Quiz und Fiori In-App-Hilfe) herausstellt, die Rollen der Key User als Subject Matter Experts definiert und die direkte Verknüpfung mit Signavio-Prozessmodellen konzipiert.',
            r: 'Das Management akzeptierte das Konzept vollständig. Die Personalentwicklung übernahm die Content-Governance und die Autoren-Schulung über den SAP Learning Hub wurde strukturiert ausgerollt.'
          },
          {
            title: 'Erstellung des offiziellen Leitfadens "SAP Cloud ALM How2Handle"',
            tag: 'Tool-Governance & PMO',
            expanded: false,
            s: 'Im Programm SAP4SSB trafen unterschiedliche Arbeitsweisen der Partner Nagarro (TP2), Evora (TP3) und SSB-interner Berater aufeinander. Es fehlte ein einheitlicher Standard, wie Anforderungen, User Stories und Testfälle in SAP Cloud ALM gepflegt werden.',
            t: 'Meine Aufgabe war es, eine praxisnahe Handlungsanleitung zu erstellen, damit alle Teilprojektleiter und Berater CALM homogen und revisionssicher nutzen.',
            a: 'Ich verfasste den umfassenden "SAP_CALM_How2handle_quickguide", der Schritt für Schritt die Verknüpfung von Signavio-Prozessen, die Definition von Quality Gates, das Task-Tracking und das Testfallmanagement dokumentierte.',
            r: 'Der Quickguide wurde zum verbindlichen Onboarding-Dokument für interne Mitarbeiter und externe Berater, wodurch Datensilos vermieden und der Projektfortschritt in Echtzeit transparent wurde.'
          },
          {
            title: 'Konzeption der Datenmigration & Migrationsobjekte-Vorschlag',
            tag: 'Data Architecture & Migration',
            expanded: false,
            s: 'Im Greenfield-Projekt stand die SSB vor der Herausforderung, hunderte Stamm- und Bewegungsdatenobjekte aus dem Altsystem zu identifizieren, zu bereinigen und ins SAP S/4HANA Zielschema zu überführen.',
            t: 'Zusammen mit Nagarro musste ein transparenter Vorschlag aller benötigten Migrationsobjekte erarbeitet und die Migrationsmethode (Staging vs. Direkte Übertragung) bewertet werden.',
            a: 'Ich analysierte den Migrationsobjekte-Katalog (u.a. Business Partner, FI-AA Anlagen, Kostenstellen, PM-Equipments) in Excel und CALM, differenzierte zwischen reinen Stammdaten und offenen Posten und dokumentierte die Notwendigkeit von Feld- und Werte-Mappings.',
            r: 'Der erstellte Migrationsobjekte-Vorschlag diente als verbindliche Arbeitsgrundlage für die Teilprojekte TP2 und TP3 zur Vorbereitung der Staging-Tabellen und Cutover-Simulationen.'
          },
          {
            title: 'Harmonisierung der Schnittstellen & GAP-Tracking mit Basispartner Axians',
            tag: 'IT-Plattform & Basis',
            expanded: false,
            s: 'In der Explore-Phase identifizierte das Team kritische GAPs in der Bereitstellung des ES4-Testsystems (Mandanten M300/M100), bei ADS-Formularen, SSO und der Fiori BANF-App.',
            t: 'Im IT-PMO musste eine lückenlose Erfassung und Priorisierung der offenen IT-ToDos erfolgen, um die Testfähigkeit der kaufmännischen Prozesse nicht zu gefährden.',
            a: 'Ich strukturierte die Themensammlung und Priorisierung in enger Abstimmung mit Axians (Gerdes) und Armin Heinrich, ordnete CalmIDs zu und klassifizierte Aufgaben nach T-Shirt-Sizes (S, M, L).',
            r: 'Die Engpässe wurden im wöchentlichen PL-Meeting transparent priorisiert, wodurch kritische Basis-Komponenten (SSO, Druck/ADS, Transportkonsolidierung) rechtzeitig vor den End-to-End-Tests bereitstanden.'
          },
          {
            title: 'Empirische Triangulation für die Masterarbeit im laufenden Projekt (Note 1,0)',
            tag: 'Wissenschaftliche Exzellenz',
            expanded: false,
            s: 'In der akademischen ERP-Forschung gab es bislang kaum empirisch fundierte Modelle darüber, wie sich klassische Erfolgsfaktoren bei der Plattformisierung von S/4HANA mit BTP verändern.',
            t: 'Im Rahmen meiner Masterarbeit an der Uni Stuttgart wollte ich ein wissenschaftlich fundiertes und zugleich praxiserprobtes Framework entwickeln.',
            a: 'Ich führte 12 leitfadengestützte Experteninterviews mit Gesamtprojektleiter Roland Nowak, Teilprojektleitern (Wimpff, Neifer) und Architekten durch, analysierte diese qualitativ nach Mayring und triangulierte sie mit der internationalen Literatur.',
            r: 'Ich entwickelte ein 4x3 CSF-Framework, das belegt, dass API-Governance, Event-Driven Architecture und Clean-Core-Richtlinien heute genauso erfolgskritisch sind wie klassischer Top-Management-Support. Die Arbeit wurde am 20.04.2026 mit der Traumnote 1,0 bewertet.'
          }
        ]);
        // PRIVATE_DEFENSE_END


        const wbsProjects = ref([
          {
            id: 'TP1',
            wbs: 'WBS 16–63',
            phase: 'Explore',
            title: 'TP1: Change Management, People & Enablement',
            lead: 'Sarah Lozano / Göhring / Cichon (UB AC)',
            progress: 75,
            tag: 'People & Change',
            tagColor: 'bg-blue-100 text-blue-800 dark:bg-blue-900/60 dark:text-blue-300',
            details: 'Multiplikatoren-Schulungskonzept, Rollout SAP Enable Now (März 2026), Coffee Corners in allen Unternehmensbereichen (UB Z, K, T, W), Berg & Tal Mitarbeiterevents.',
            milestone: 'Schulungskonzept & Enable Now live (März 2026)'
          },
          {
            id: 'TP2',
            wbs: 'WBS 64–112',
            phase: 'Explore',
            title: 'TP2: Kaufmännische Prozesse & Solution Design',
            lead: 'Sebastian Neifer / Tim Lopez / Tim Waldberg (Nagarro ES)',
            progress: 80,
            tag: 'Fit-to-Standard',
            tagColor: 'bg-emerald-100 text-emerald-800 dark:bg-emerald-900/60 dark:text-emerald-300',
            details: 'Fit-to-Standard Reifegrade: CO 90%, MM 91%, RE-FX 86%, FI 76%, SD 76%, EHS 71%, Cross Topics 58%. BPMN 2.0 Modellierung in Signavio & CALM-Sync auf ES4.400.',
            milestone: 'Explore-Phase formal abgeschlossen (29.08.2025, Vorgang 110)'
          },
          {
            id: 'TP3',
            wbs: 'WBS 173–196',
            phase: 'Explore',
            title: 'TP3: Technische Prozesse & Asset Management',
            lead: 'UB W, UB K, UB T / Partner Evora & Nagarro',
            progress: 100,
            tag: 'Instandhaltung',
            tagColor: 'bg-amber-100 text-amber-800 dark:bg-amber-900/60 dark:text-amber-300',
            details: '100% Freigabe der Kernprozesse für Stadtbahn (SSAM Mobile Instandhaltung auf Tablets), Kraftverkehr (Busse) und Fahrleitung/Gleise. Gebäudewirtschaft (VH) erst nach Go-Live 01.01.2027.',
            milestone: 'Kernprozesse UB W, K, T 100% freigegeben (30.09.2025)'
          },
          {
            id: 'TP4',
            wbs: 'WBS 197–202',
            phase: 'Realize',
            title: 'TP4: IT-Unterstützung, RISE & Systemlandschaft',
            lead: 'Dietmar Fillinger / Axians & Nagarro Basis-Architekten',
            progress: 70,
            tag: 'Cloud & BTP',
            tagColor: 'bg-purple-100 text-purple-800 dark:bg-purple-900/60 dark:text-purple-300',
            details: '4-System-Landschaft (ES4.400 Sandbox, QS4.100 Int-Test 1, QS4.210 Int-Test 2/UAT, PS4 Produktiv), SAP Cloud Connector, BTP Integration Suite und SSO via Azure AD.',
            milestone: 'Staging ES4 -> QS4 -> PS4 bereitgestellt (01.04.2026)'
          },
          {
            id: 'TP5',
            wbs: 'WBS 203–297',
            phase: 'Explore',
            title: 'TP5: Gesamtsteuerung, PMO & Betriebsvereinbarungen',
            lead: 'Roland Nowak / Dietmar Fillinger / Betriebsrat (Schmidt, Kraus)',
            progress: 85,
            tag: 'PMO & Governance',
            tagColor: 'bg-rose-100 text-rose-800 dark:bg-rose-900/60 dark:text-rose-300',
            details: 'Gesamtprojektsteuerung in MS Project, C-Level Reporting Steering Board, Meilenstein-Controlling und die beiden historischen Mitbestimmungs-Meilensteine mit dem Betriebsrat.',
            milestone: 'Pilot-BV in Kraft (01.04.2026) | Finale BV in Kraft (01.01.2027)'
          }
        ]);

        const searchCatalog = [
          // Kaufmännisch & Solution Design
          { title: 'Trennungsrechnung EU 1370/2007', cat: 'Kaufmännisch & FI/CO', tab: 'solution_design', desc: 'Verkehrsvertragliche Trennung eigenwirtschaftlicher vs. gemeinwirtschaftlicher Verkehre (§ 45a PBefG).' },
          { title: 'Grants Management (GM) & Fördermittel', cat: 'Kaufmännisch & FI/CO', tab: 'solution_design', desc: 'Fonds, Förderungsarten (LGVFG/GVFG) und Derivationsregeln für Investitionszuschüsse im ÖPNV.' },
          { title: 'Universal Journal (ACDOCA)', cat: 'Kaufmännisch & FI/CO', tab: 'solution_design', desc: 'Single Source of Truth im Hauptbuch, Ledger 0L (HGB) und 2L (Steuerrecht), Echtzeit-Kostenarten.' },
          { title: 'Kostenrechnung: PSP-Element vs. Innenauftrag', cat: 'Kaufmännisch & FI/CO', tab: 'solution_design', desc: 'Hierarchische Mehrjahres-Großprojekte via PSP versus operative Instandhaltungs-Innenaufträge.' },
          { title: 'Anlagenbuchhaltung (FI-AA) & Eröffnungsbilanz', cat: 'Kaufmännisch & FI/CO', tab: 'migration', desc: 'SuSa-Bilanzabgleich: 0,00 € Saldo auf dem Datenübernahmekonto nach Altdatenmigration.' },
          { title: 'Customer Vendor Integration (CVI)', cat: 'Kaufmännisch & FI/CO', tab: 'migration', desc: 'Zentraler SAP Business Partner (Geschäftspartner) für Debitoren, Kreditoren und Personal.' },
          { title: 'Sustainability & CSRD (EHS)', cat: 'Kaufmännisch & FI/CO', tab: 'solution_design', desc: 'Gefahrstoffmanagement, Abfallbilanzierung und ESG-Kennzahlen im S/4HANA Standard.' },

          // Technik & Architektur
          { title: 'Clean Core Paradigma', cat: 'Technik & Architektur', tab: 'project', desc: 'Modifikationsfreier ERP-Kern, Upgrade-Sicherheit, On-Stack RAP vs. Side-by-Side BTP.' },
          { title: 'SAP BTP Integration Suite', cat: 'Technik & Architektur', tab: 'cheatsheet', desc: 'Event-driven Architecture, Cloud Integration, OData/REST APIs und Entkopplung von Subsystemen.' },
          { title: 'Mobile Instandhaltung (SAP SSAM)', cat: 'Technik & Architektur', tab: 'project', desc: 'SAP Service and Asset Management auf robusten Tablets für Stadtbahnwerkstätten und Busdepots.' },
          { title: 'SAP Migration Cockpit (LTMC)', cat: 'Technik & Architektur', tab: 'migration', desc: 'Staging-Tabellen-Architektur, Delta-Loads, Validierungsregeln und Cutover-Management.' },
          { title: 'Non-SAP Schnittstellenmatrix', cat: 'Technik & Architektur', tab: 'cheatsheet', desc: 'Subsysteme PATRIS (Vertrieb), xSuite (Rechnungsworkflow), d.velop (DMS), Oracle DWH, EFD4.' },
          { title: 'Core Data Services (CDS) & ABAP Cloud', cat: 'Technik & Architektur', tab: 'cheatsheet', desc: 'Virtuelle Datenmodelle (VDM), analytische Views und RESTful Application Programming (RAP).' },
          { title: 'TOGAF 9 ADM Enterprise Architecture', cat: 'Technik & Architektur', tab: 'enterprise_arch', desc: 'Architecture Development Method, Baseline vs. Target Architecture und Architecture Governance.' },
          { title: 'ITIL 4 Service Operations (Datacenter One)', cat: 'Technik & Architektur', tab: 'enterprise_arch', desc: 'Incident-, Problem- und Change-Management, SLA-Steuerung und 24/7 Rechenzentrums-Monitoring.' },

          // Großprojekt & PMO
          { title: 'Gesamtprojektplan SAP4SSB (MS Project)', cat: 'Großprojekt & PMO', tab: 'project', desc: 'WBS 1–297: Discover bis Run, Phasenplanung, Critical Path und Meilenstein-Tracking.' },
          { title: 'TP1 Change Management & Enable Now', cat: 'Großprojekt & PMO', tab: 'project', desc: 'WBS 16–63: Change Champions, Coffee Corners in allen 4 Unternehmensbereichen (UB Z/K/T/W).' },
          { title: 'TP2 Kaufmännische Prozesse WBS Plan', cat: 'Großprojekt & PMO', tab: 'project', desc: 'WBS 64–112: Fit2Standard Reifegrade (CO 90%, MM 91%, RE-FX 86%, FI 76%), Abschluss 29.08.2025.' },
          { title: 'TP3 Technische Prozesse & Instandhaltung', cat: 'Großprojekt & PMO', tab: 'project', desc: 'WBS 173–196: 100% Freigabe für Stadtbahn, Busse und Netz; Gebäudewirtschaft erst Post-Go-Live.' },
          { title: 'TP4 IT-Unterstützung & 4-System-Landschaft', cat: 'Großprojekt & PMO', tab: 'project', desc: 'WBS 197–202: ES4.400 Sandbox, QS4.100 Integrationstest 1, QS4.210 UAT, PS4 Produktivsystem.' },
          { title: 'TP5 Gesamtsteuerung & PMO', cat: 'Großprojekt & PMO', tab: 'project', desc: 'WBS 203–297: Lenkungsausschuss-Reporting, Budgetcontrolling und Meilenstein-Freigaben.' },
          { title: 'Pilot-Betriebsvereinbarung (01.04.2026)', cat: 'Großprojekt & PMO', tab: 'project', desc: 'Vorgang 294: Meilenstein Pilot-BV für Test mit Echtdaten (UAT auf QS4.210) mit Betriebsrat Schmidt & Kraus.' },
          { title: 'Finale Betriebsvereinbarung (01.01.2027)', cat: 'Großprojekt & PMO', tab: 'project', desc: 'Vorgang 297: Finale BV inkraftgetreten exakt zum produktiven Go-Live Neujahr 2027.' },
          { title: 'Tool-Governance: CALM vs. Signavio', cat: 'Großprojekt & PMO', tab: 'tools', desc: 'BPMN 2.0 Prozessmodellierung in Signavio synchronisiert mit Testskripten in SAP Cloud ALM.' },

          // Masterarbeit & Wissenschaft
          { title: 'Masterarbeit Note 1,0 (Prof. Herzwurm)', cat: 'Forschung & Wissenschaft', tab: 'thesis', desc: '126 Seiten: Kritische Erfolgsfaktoren in der Transformation großer ERP-Systeme (S/4HANA Plattformisierung).' },
          { title: '12 empirische Experteninterviews', cat: 'Forschung & Wissenschaft', tab: 'thesis', desc: 'Interviews im Großprojekt SAP4SSB mit Gesamt-PL Roland Nowak, TPLs und Lead-Architekten.' },
          { title: 'Qualitative Inhaltsanalyse nach Mayring', cat: 'Forschung & Wissenschaft', tab: 'thesis', desc: 'Deduktiv-induktives Kategoriensystem und wissenschaftliches Codebuch zur Auswertung.' },
          { title: 'Boundary Resources & Bimodale IT', cat: 'Forschung & Wissenschaft', tab: 'thesis', desc: 'Theoretische Fundierung nach Ghazawneh & Henfridsson: ABR, DBR, SBR und lose Kopplung.' },
          { title: 'Absorptive Capacity & Change Management', cat: 'Forschung & Wissenschaft', tab: 'thesis', desc: 'Wissensaufnahme- und Transformationsfähigkeit (Cohen & Levinthal) in traditionsreichen Konzernen.' },
          { title: 'Masterabschluss M.Sc. 1,6 (120 ECTS)', cat: 'Forschung & Wissenschaft', tab: 'thesis', desc: 'Amtliches Zeugnis Universität Stuttgart: Bestnote 1,0 in Masterarbeit und Digitaler Nachhaltigkeit.' },
          // PRIVATE_CATALOG_START
          { title: '60-Sekunden-Elevator-Pitch', cat: 'Interview & Karriere', tab: 'interview', desc: 'Prägnanter Einstiegspitch für Vorstellungsgespräche: 24 Mo. SSB + 1,0 Masterarbeit Clean Core.' },
          { title: 'Deep-Dive-Story (3 Minuten)', cat: 'Interview & Karriere', tab: 'interview', desc: 'Ausführliche Karrierestory von Datacenter One über Uni Stuttgart bis zum Großprojekt SAP4SSB.' },
          { title: 'CV De-Risking & Gefahrenabwehr', cat: 'Interview & Karriere', tab: 'cv_defense', desc: 'Souveräne Pivot-Brücken bei Fangfragen zu Java, SPRO-Customizing, RPA oder Berufserfahrung.' },
          { title: 'STAR-Stories (Methodische Antworten)', cat: 'Interview & Karriere', tab: 'interview', desc: 'Situation, Task, Action, Result für Konflikte, Scope Creep, Tool-Einführung und Migration.' },
          { title: '90-Tage Onboarding-Roadmap', cat: 'Interview & Karriere', tab: 'career', desc: 'Strukturierter Fahrplan für die ersten 3 Monate als Consultant oder Enterprise Architekt.' },
          { title: 'Gehaltskalkulation (55.000 € – 75.000 €)', cat: 'Interview & Karriere', tab: 'career', desc: 'Fundierte Marktwertbegründung (Junior 55–65k € | Konzern/IGM 65–75k €) und Verhandlungsleitfaden.' },
          { title: 'Persönliches Second Brain & Local RAG', cat: 'Interview & Karriere', tab: 'notebook', desc: 'Interaktives Notizbuch mit Obsidian-Sync + SQLite FTS5 Volltextsuche über alle 4.980 Dokumente.' }
          // PRIVATE_CATALOG_END
        ];

        // PRIVATE_QA_FILES_START
        const allQA = [
          {
            q: 'Was genau war Ihre Rolle bei der SSB AG und wie war das Transformationsprogramm SAP4SSB strukturiert?',
            cat: 'SSB S/4HANA & Explore-Phase',
            open: true,
            a: `Ich war 24 Monate lang als Werkstudent im IT-PMO (Teilprojekt 5: Gesamtsteuerung & Architektur) unter Gesamtprojektleiter Roland Nowak und IT-Leiter Dietmar Fillinger tätig.

Das Programm SAP4SSB gliederte sich in 5 disjunkte Teilprojekte:
- TP1: Change Management & Enablement (Rollout SAP Enable Now, Coffee Corners, Key-User-Befähigung)
- TP2: Kaufmännische Prozesse & Solution Design (FI/CO/MM/RE-FX mit Nagarro ES)
- TP3: Technische Prozesse & Asset Management (Instandhaltung Stadtbahn/Busse/Fahrleitung mit Evora & Nagarro)
- TP4: IT-Unterstützung & Systemlandschaft (4-System-Landschaft ES4/QS4/PS4 mit Axians)
- TP5: Gesamtsteuerung, PMO, Vergabe & Mitbestimmung mit Betriebsrat

Meine Aufgabe war die operative Klammer: Tool-Governance (Quickguide für SAP Cloud ALM, Enable Now Übergabekonzept), Analyse der Migrationsobjekte und Statusreporting für den Lenkungsausschuss.`,
            do: 'Betone die 24 Monate Laufzeit, die 5 Teilprojekte (TP1-TP5) und konkrete Artefakte (CALM How2Handle, Enable Now Konzept).',
            dont: 'Stelle dich nicht als reiner Zuarbeiter dar – du hast Governance-Vorgaben aktiv erarbeitet und bereichsübergreifend abgestimmt!'
          },
          {
            q: 'Welcher Meilenstein markierte Ihren Projektaustritt bei der SSB und wie ging es danach weiter?',
            cat: 'SSB S/4HANA & Explore-Phase',
            open: false,
            a: `Mein Austritt erfolgte zum formalen und erfolgreichen Abschluss der Explore-Phase:
Das umfassende Solution Design Document (SDD) für die kaufmännischen und technischen Prozesse (inklusive aller Prozessmodelle in Signavio, Schnittstellenmatrizen und WRICEFA-Entwicklungsobjekte) war zu 100% finalisiert und vom Lenkungsausschuss (Steering Board) abgenommen.

Der unmittelbar anschließende nächste Projektschritt war der Eintritt in die Realize-Phase (WBS 197-202): Das Customizing im System, die Bereitstellung des Integrations-Testsystems QS4.100 durch Axians, die iterative Datenmigration via LTMC-Staging-Tabellen und die Vorbereitung der Pilot-Betriebsvereinbarung zum 01.04.2026 für die End-to-End-Tests.`,
            do: 'Nenne den exakten Meilenstein: SDD vollständig finalisiert & genehmigt, formaler Explore-Abschluss, direkter Übergang in die Realize-Phase.',
            dont: 'Verwechsle die Phasen nicht – du hast die Konzeption bis zur vollständigen Genehmigung begleitet, nicht erst mittendrin aufgehört.'
          },
          {
            q: "Was bedeutet 'Clean Core' im S/4HANA Private Cloud Kontext und wie verhindert man Wildwuchs?",
            cat: 'SSB S/4HANA & Explore-Phase',
            open: false,
            a: `Clean Core bedeutet, dass der ERP-Kern modifikationsfrei bleibt und ausschließlich über stabile, von SAP freigegebene Schnittstellen (APIs und CDS Views) angesprochen wird. Dadurch bleibt das System upgradefähig, was in Cloud-Releases essenziell ist.

In der Praxis teilt sich das auf:
1. On-Stack Extensibility: Erweiterungen im Kern erfolgen nur über ABAP Cloud und das RESTful Application Programming Model (RAP).
2. Side-by-Side Extensibility: Komplexe Eigenentwicklungen, Fiori-Frontends und Drittsystem-Integrationen laufen auf der SAP BTP.

Um Wildwuchs zu verhindern, braucht es eine strikte Governance: Jede Z-Anforderung muss durch ein Architecture Review Board (ARB), in dem geprüft wird: Geht es im Best-Practice-Standard? Wenn nein, warum nicht BTP?`,
            do: 'Erwähne die Unterscheidung On-Stack vs. Side-by-Side und das ARB (Architecture Review Board).',
            dont: "Behaupte nicht, dass man bei Clean Core gar nichts mehr programmieren darf – es geht um das 'Wo' und 'Wie'!"
          },
          {
            q: 'Warum hat sich die SSB für Greenfield und nicht für eine Systemkonvertierung (Brownfield) entschieden?',
            cat: 'SSB S/4HANA & Explore-Phase',
            open: false,
            a: `Das bestehende SAP ECC 6.0 der SSB war über 20 Jahre historisch gewachsen und wies hunderte Z-Modifikationen, ungenutzte Altdaten und veraltete Berechtigungsstrukturen auf. Ein Brownfield-Ansatz hätte diese technische Schuld 1:1 in die neue Welt mitgeschleift und zukünftige Cloud-Upgrades massiv erschwert.

Mit dem Greenfield-Ansatz in einer RISE with SAP Private Cloud Edition konnte die SSB tabula rasa machen: Rückkehr zum Best-Practice-Standard durch Fit-to-Standard Workshops, Bereinigung der Stammdaten (CVI) und strikte Einhaltung des Clean-Core-Paradigmas.`,
            do: 'Verwende Fachbegriffe: Technische Schuld, Modifikationsfreier Kern, Fit-to-Standard, Best-Practice-Standard.',
            dont: "Sage nicht einfach: 'Brownfield war zu alt.' Begründe es mit Upgrade-Sicherheit und Wartungskosten."
          },
          {
            q: 'Was versteht man unter der Trennungsrechnung nach EU-Verordnung 1370/2007 im ÖPNV?',
            cat: 'SSB S/4HANA & Explore-Phase',
            open: false,
            a: `Die Trennungsrechnung nach EU-VO 1370/2007 und § 45a PBefG verpflichtet Verkehrsunternehmen wie die SSB, die Buchführung strikt zwischen eigenwirtschaftlichen Verkehren (z.B. kommerzieller Gelegenheitsverkehr) und gemeinwirtschaftlichen, durch die öffentliche Hand bezuschussten Verkehren (ÖPNV-Linienverkehr) zu trennen.

Dadurch wird europarechtlich sichergestellt, dass keine verbotenen Quersubventionierungen öffentlicher Ausgleichsleistungen in den freien Wettbewerb fließen. Im S/4HANA-Lösungsdesign (TP2) wurde dies durch eine saubere Kostenstellen-, Profit-Center- und Buchungskreis-Segmentierung sowie parallele Ledger im Hauptbuch realisiert.`,
            do: 'Nenne die EU-Verordnung 1370/2007, § 45a PBefG und die Vermeidung von Quersubventionierungen.',
            dont: 'Tue nicht so, als sei Trennungsrechnung eine rein technische SAP-Einstellung – es ist eine rechtlich zwingende Compliance-Vorgabe.'
          },
          {
            q: 'Was sind die architektonischen Vorteile des Universal Journal (ACDOCA) gegenüber der klassischen Tabellenwelt?',
            cat: 'SSB S/4HANA & Explore-Phase',
            open: false,
            a: `Im alten ECC 6.0 waren Finanzdaten auf unzählige Tabellen verteilt: BSEG und BKPF für Hauptbuch, BSIS/BSAS für offene Posten, KNC1/LFC1 für Debitoren/Kreditoren und COEP für das Controlling. Das erforderte komplexe Abstimmungsarbeiten (Reconciliation) zwischen FI und CO am Monatsende.

Das Universal Journal (Tabelle ACDOCA) vereint Hauptbuch, Kostenrechnung, Anlagenbuchhaltung (FI-AA) und Material-Ledger in einer einzigen, spaltenbasierten 'Single Source of Truth' auf der SAP HANA In-Memory-Datenbank. FI und CO sind von vornherein abgestimmt; Berichte aggregieren Millionen Zeilen in Millisekunden on-the-fly.`,
            do: "Nenne konkrete Tabellen (BSEG, COEP, ACDOCA) und das Prinzip 'Single Source of Truth'.",
            dont: 'Vergiss nicht die betriebswirtschaftliche Konsequenz: Wegfall von zeitaufwändigen Abstimmungsarbeiten zum Periodenabschluss.'
          },
          {
            q: 'Wie unterscheiden sich PSP-Elemente und Innenaufträge in der SSB-Kostenrechnung?',
            cat: 'SSB S/4HANA & Explore-Phase',
            open: false,
            a: `In der alten ECC-Welt wurden häufig Innenaufträge für alles Mögliche genutzt, was zu unübersichtlichen Auftragsfriedhöfen führte.

Im S/4HANA-Lösungsdesign wurde eine klare Trennung definiert:
- PSP-Elemente (Projektstrukturplan im Projektsystem PS): Werden für mehrjährige, investive Großprojekte genutzt (z.B. Neubau von Stadtbahntrassen, Anschaffung neuer Fahrzeugflotten). Sie erlauben hierarchische Budgetierung, Fördermittelzuordnung (Grants Management) und Abrechnung auf Anlagen im Bau (AiB).
- Innenaufträge: Werden ausschließlich für operative, kurzfristige Gemeinkosten- oder Instandhaltungsmaßnahmen mit begrenzter Laufzeit eingesetzt.`,
            do: 'Erkläre die strategische Trennung: PSP = mehrjährige Investitionen mit Budgetierung; Innenaufträge = operative Kostenverrechnung.',
            dont: 'Verwechsle nicht PS (Projektsystem) mit PM (Plant Maintenance / Instandhaltung).'
          },
          {
            q: 'Wie funktionierte die Customer Vendor Integration (CVI) bei der SSB?',
            cat: 'SSB S/4HANA & Explore-Phase',
            open: false,
            a: `Unter ECC gab es getrennte Stammdatensätze für Kunden (Debitoren, Tabelle KNA1) und Lieferanten (Kreditoren, Tabelle LFA1). War ein Partner beides, gab es redundante Datensätze.

In S/4HANA ist der Business Partner (Geschäftspartner) das führende Objekt. Im Rahmen der CVI haben wir die Nummernkreise und Kontengruppen harmonisiert. Ein einzelner Geschäftspartner erhält verschiedene Rollen (z.B. FLCU00 für Debitor, FLVN00 für Kreditor) unter derselben ID. Das war eine zentrale Vorbedingung für die Datenmigration mit LTMC.`,
            do: 'Nenne das Führende-Objekt-Prinzip, Rollen (FLCU00, FLVN00) und die Konsolidierung redundanter Altdaten.',
            dont: 'Bezeichne CVI nicht als einfache Datenkopie – es ist eine zwingende Datenharmonisierung.'
          },
          {
            q: 'Wie lief die Datenmigration mit dem SAP Migration Cockpit (LTMC) ab und warum ist das 0,00 € Saldo entscheidend?',
            cat: 'SSB S/4HANA & Explore-Phase',
            open: false,
            a: `Die Migration erfolgte über das SAP Migration Cockpit (LTMC) primär nach dem Staging-Tabellen-Prinzip: Altdaten aus ECC wurden in Staging-Tabellen auf der HANA-DB geladen, dort über Mapping-Regeln transformiert und validiert.

Im Finanzbereich (FI) ist der Eröffnungsbilanz-Abgleich die kritischste Revisionsprüfung: Sachkontensalden, offene Posten (OP) und Anlagenbuchwerte (FI-AA) werden gegen ein zentrales Datenübernahmekonto gebucht. Nach erfolgreichem Cutover muss dieses Übernahmekonto centgenau einen Saldo von 0,00 € aufweisen. Jeder Cent Abweichung bedeutet eine unvollständige oder asynchrone Buchung, die das Testat der Wirtschaftsprüfer gefährdet.`,
            do: 'Erkläre den Cutover-Ablauf: Staging -> Mappings -> Simulation -> Import -> Abstimmung des Datenübernahmekontos auf 0,00 €.',
            dont: "Tue nicht so, als ob Datenmigration per 'Excel-Upload' erledigt wäre – es ist ein hochgradig revisionssicherer Prozess."
          },
          {
            q: 'Welche Rolle spielten die Mitbestimmungs-Meilensteine mit dem Betriebsrat?',
            cat: 'SSB S/4HANA & Explore-Phase',
            open: false,
            a: `In einem öffentlichen Verkehrsunternehmen unterliegt die Einführung eines ERP-Systems, das potenziell Leistungs- und Verhaltensdaten von Mitarbeitern verarbeiten kann, der zwingenden Mitbestimmung nach § 87 Abs. 1 Nr. 6 BetrVG.

Im Programm SAP4SSB haben Gesamtprojektleiter Roland Nowak und IT-Leiter Dietmar Fillinger den Betriebsrat (Vorsitzende Schmidt & Kraus) von Beginn an eingebunden. Wir hatten zwei verbindliche Meilensteine im Masterplan:
1. Pilot-Betriebsvereinbarung (01.04.2026): Regelung für den Testbetrieb mit anonymisierten/pseudonymisierten Echtdaten im UAT auf QS4.210.
2. Finale Betriebsvereinbarung (01.01.2027): Regelung für den Produktivbetrieb zum Go-Live mit klarem Rollen- und Berechtigungskonzept.`,
            do: 'Erwähne § 87 BetrVG, die Pilot-BV (01.04.2026) und die Finale BV (01.01.2027) sowie das Rollen-/Berechtigungskonzept.',
            dont: 'Unterschätze niemals die Mitbestimmung – in deutschen Konzernen ist das ein zentraler Erfolgsfaktor!'
          },
          {
            q: 'Welche Aufgaben hatten Sie 12 Monate lang bei Datacenter One im INOC?',
            cat: 'Datacenter One & ITIL 4',
            open: false,
            a: `Ich war 12 Monate lang als Werkstudent im Information Network Operation Center (INOC) unter Helmut Schmidpeter tätig.

Meine Hauptaufgaben umfassten:
- 24/7 Monitoring von Core-Netzwerken, Serverfarmen, USV-Anlagen (Unterbrechungsfreie Stromversorgung) und RZ-Klimatechnik.
- Single Point of Contact (SPoC) für Enterprise-Kunden und Tier-1 Carrier bei Störungen nach ITIL 4 Service Operations.
- Konzeption und Aufbau einer zentralen Wissensdatenbank in Confluence zur Prozessstandardisierung.
- Hands-on Incident- und Problem-Management via Jira Service Management.`,
            do: 'Betone die 24/7 Leitstands-Verantwortung, ITIL 4 Prinzipien und den Single Point of Contact (SPoC).',
            dont: "Reduziere den Leitstand nicht auf 'Kabel stecken' – es ging um unternehmenskritisches SLA-Management."
          },
          {
            q: 'Wie sind Sie bei Netzwerk- und Verbindungsausfällen konkret vorgegangen?',
            cat: 'Datacenter One & ITIL 4',
            open: false,
            a: `Trat im PRTG-Monitoring ein Alarm auf (z.B. Packet Loss oder Leitungsunterbrechung auf einer Glasfaserstrecke), folgte das Vorgehen einer strikten Standard Operating Procedure (SOP):
1. Verifikation & Triage: Prüfen, ob es sich um einen lokalen Port, einen Switch oder eine externe Carrier-Leitung handelt.
2. Ticket-Erstellung: Sofortige Erfassung im Jira Service Management mit Severity-Einstufung und Zuweisung an die zuständige Carrier-Eskalationsstufe.
3. Stakeholder-Kommunikation: Proaktive Kundeninformation innerhalb der vertraglichen Reaktionszeit (SLA).
4. Entstörung & Dokumentation: Koordination mit Field Service Technikern vor Ort und Revisionssichere Abschlussdokumentation im Ticket.`,
            do: 'Beschreibe die Schritte strukturiert: Alarm -> Triage -> Ticket -> Carrier-Eskalation -> SLA-Einhaltung.',
            dont: 'Antworte nicht unstrukturiert – im Leitstand zählt methodische Ruhe und standardisierte Vorgehensweise.'
          },
          {
            q: 'Wie haben Sie die Prozessstandardisierung im INOC vorangetrieben?',
            cat: 'Datacenter One & ITIL 4',
            open: false,
            a: `Vor meiner Initiative lag viel Erfahrungswissen isoliert bei einzelnen Schichtleitern. Ich habe die Initiative ergriffen, dieses Wissen in Confluence zu systematisieren.

Ich habe Standard Operating Procedures (SOPs) für wiederkehrende Störungsbilder erstellt – darunter Leitfäden für Carrier-Ausfälle, USV-Alarme, Notfall-Paging und das Onboarding neuer Rechenzentrums-Kunden. Dadurch sank die Einarbeitungszeit neuer Mitarbeiter deutlich und die Erstlösungsquote (First Contact Resolution) stieg messbar.`,
            do: 'Erwähne die Confluence-Wissensdatenbank, SOPs und die Steigerung der First Contact Resolution.',
            dont: 'Behaupte nicht, du hättest das Rechenzentrum alleine betrieben – stelle deinen Beitrag zur Standardisierung heraus.'
          },
          {
            q: 'Was war das Projekt Hardware Lifecycle Management (HLM) bei Datacenter One?',
            cat: 'Datacenter One & ITIL 4',
            open: false,
            a: `Im Rahmen des Projekts Hardware Lifecycle Management (HLM) habe ich den gesamten Lebenszyklus der Client- und Leitstands-Hardware (über 100 Systeme) analysiert und optimiert.

Ich habe den Soll-Prozess in Microsoft Visio modelliert: Von der Bedarfsanforderung über die Beschaffung, Staging/Betankung, Rollout im laufenden Betrieb bis hin zum datenschutzkonformen Decommissioning (Zertifizierte Datenlöschung). Zudem habe ich eine Excel-basierte PoC-Rollout-Matrix erstellt, um Ausfallzeiten im 24/7 Betrieb zu verhindern.`,
            do: 'Nenne die Phasen: Beschaffung -> Staging -> Rollout -> Decommissioning und die Modellierung in MS Visio.',
            dont: 'Stelle es nicht als reines Schrauben an PCs dar – es war ein strukturiertes IT-Asset-Management-Projekt.'
          },
          {
            q: 'Wie funktionierte das Carriermanagement und die Netzanbindung im Leitstand?',
            cat: 'Datacenter One & ITIL 4',
            open: false,
            a: `Datacenter One betreibt Colocation- und Rechenzentrumsflächen, in denen Kunden Leitungen unterschiedlichster Carrier (Telekom, Vodafone, Colt, GasLINE etc.) nutzen.

Im Carriermanagement ging es um die Überwachung der Meet-Me-Rooms (MMR), das Patching von Cross-Connects und die Sicherstellung vereinbarter Service Level Agreements (SLAs). Kam es zu Baggerunfällen oder Faserrissen, musste die Umschaltung auf redundante Strecken überwacht und der Ticket-Lifecycle mit dem jeweiligen Carrier koordiniert werden.`,
            do: 'Nenne Meet-Me-Room (MMR), Cross-Connects, Carrier-SLAs und Redundanzschaltungen.',
            dont: 'Verwechsle Carriermanagement nicht mit reinem Telemarketing – es ist kritische Glasfaser-Infrastruktur.'
          },
          {
            q: 'Was waren Ihre drei wichtigsten Learnings aus der Zeit bei Datacenter One?',
            cat: 'Datacenter One & ITIL 4',
            open: false,
            a: `Erstens: Absolute SLA-Disziplin. Bei einer vertraglichen Verfügbarkeit von 99,99% kosten wenige Minuten ungeplante Ausfallzeit tausende Euro Vertragsstrafen. Man lernt, unter Druck extrem präzise zu arbeiten.

Zweitens: Dokumentationsqualität ist die Lebensversicherung. Im 24/7 Schichtbetrieb muss die nachfolgende Schicht ein Ticket in 30 Sekunden vollständig verstehen, ohne nachfragen zu müssen.

Drittens: Deeskalierende Krisenkommunikation. Wenn ein Kunde anruft, dessen Kernsysteme stehen, braucht er keine Ausreden, sondern einen ruhigen Ansprechpartner, der klare Zeithorizonte und Maßnahmen kommuniziert.`,
            do: 'Nenne die 3 Punkte: 1. SLA-Disziplin, 2. Dokumentation im Schichtbetrieb, 3. Deeskalierende Kundenkommunikation.',
            dont: 'Wähle keine rein technischen Schlagworte – zeige deine persönliche Reife und Verlässlichkeit.'
          },
          {
            q: 'Wie schlägt Ihre Erfahrung bei DC1 die Brücke zu Ihrer späteren SAP-Tätigkeit?',
            cat: 'Datacenter One & ITIL 4',
            open: false,
            a: `Viele Wirtschaftsinformatiker betrachten Cloud-Systeme wie S/4HANA nur als abstrakte Software im Browser. Durch meine 12 Monate im Rechenzentrum kenne ich das physische Fundament: Ich weiß, was Latenzen, redundante Netzanbindungen, USV-Pufferung und Tier-3/Tier-4 Klassifizierungen in der Praxis bedeuten.

Als wir bei der SSB mit Axians über die Bereitstellung der Private-Cloud-Infrastruktur (ES4) und mit Nagarro über Schnittstellen diskutierten, konnte ich ITIL 4 Incident- und Change-Prozesse nahtlos mit den SAP Cloud ALM Quality Gates verbinden.`,
            do: 'Stelle die Brücke her: Physische RZ-Infrastruktur + ITIL 4 Prozessdisziplin ➔ Verständnis für Enterprise-Cloud-Architekturen.',
            dont: 'Spiele die Station bei DC1 nicht herunter – sie zeigt dein tiefes technisches Fundament vor der SAP-Spezialisierung!'
          },
          {
            q: 'Wie lautet der offizielle Titel Ihrer Masterarbeit und worum ging es im Kern?',
            cat: 'Master & Plattformisierung',
            open: false,
            a: `Der offizielle Titel lautet:
'Kritische Erfolgsfaktoren in der Transformation großer ERP-Systeme: Eine Untersuchung am Beispiel der Plattformisierung von SAP S/4HANA'
(126 Seiten, Note 1,0 'sehr gut', Erstprüfer Prof. Dr. Georg Herzwurm, Lehrstuhl für Wirtschaftsinformatik II, Universität Stuttgart).

Im Kern untersucht die Arbeit auf Basis von 12 leitfadengestützten Experteninterviews im Großprojekt SAP4SSB und einer qualitativen Inhaltsanalyse nach Mayring, welche organisatorischen, technischen, personellen und projektsteuernden Faktoren über den Erfolg einer ERP-Plattformisierung entscheiden.`,
            do: 'Zitiere den Titel exakt und nenne Umfang (126 Seiten), Note (1,0) und Lehrstuhl (Prof. Herzwurm).',
            dont: 'Verkürze die Arbeit niemals auf ein einzelnes Modul oder Schlagwort – es ist eine ganzheitliche Transformationsuntersuchung!'
          },
          {
            q: "Warum darf die Masterarbeit niemals auf das Schlagwort 'Clean Core' reduziert werden?",
            cat: 'Master & Plattformisierung',
            open: false,
            a: `Weil 'Clean Core' nur eine technische Facette einer viel größeren architektonischen und organisatorischen Herausforderung ist!

Eine moderne ERP-Transformation zur digitalen Plattform umfasst:
1. Plattform-Governance: Wie werden Schnittstellen (APIs) als Boundary Resources gesteuert?
2. Bimodale IT: Wie entkoppelt man stabile Core-Systeme (Mode 1) von agilen Innovationsschichten (Mode 2 / BTP)?
3. Soziotechnischer Wandel & Absorptive Capacity: Wie nimmt die Belegschaft neue Prozesse an (Betriebsrat, Change Management, Key User)?
4. Multiprojekt-Steuerung (PMO): Wie orchestriert man komplexe Partner-Ökosysteme (Nagarro, Evora, Axians)?

Meine Masterarbeit liefert ein ganzheitliches 4x3-Erfolgsfaktorenmodell, das all diese Dimensionen empirisch fundiert integriert.`,
            do: 'Betone die 4 Dimensionen: Organisation, Technik, Mensch und PMO.',
            dont: "Lass dich nicht in die rein technische 'Clean-Core-Schublade' stecken – deine Arbeit ist ganzheitlich strategisch."
          },
          {
            q: 'Wie haben Sie die qualitative Inhaltsanalyse nach Mayring methodisch umgesetzt?',
            cat: 'Master & Plattformisierung',
            open: false,
            a: `Ich habe 12 leitfadengestützte Experteninterviews transkribiert und nach Mayring strukturiert analysiert:
1. Deduktive Kategorienbildung: Ableitung vorläufiger Hauptkategorien aus der theoretischen Literatur (CSF-Forschung, Boundary Resources, EAM).
2. Induktive Kategorienanpassung: Während der Codierung wurden neue, praxisgetriebene Subkategorien direkt aus den Transkripten entwickelt.
3. Erstellung eines standardisierten Codebuchs: Jede Kategorie erhielt eine präzise Definition, Ankerbeispiele aus den Interviews und explizite Abgrenzungsregeln.
4. Paraphrasierung und Generalisierung: Verdichtung der Aussagen zu Kern-Erfolgsfaktoren und Validierung durch Methoden-Triangulation.`,
            do: 'Erkläre den methodischen Dreischritt: Deduktiv-induktive Kategorien, Codebuch mit Ankerbeispielen, Triangulation.',
            dont: "Beschreibe Mayring nicht als bloßes 'Texte markieren' – es ist ein streng wissenschaftliches, reliables Verfahren."
          },
          {
            q: 'Welche Kern-Erkenntnisse lieferten die Interviews mit Roland Nowak, Thomas Wimpff und Armin Heinrich?',
            cat: 'Master & Plattformisierung',
            open: false,
            a: `Die Interviews mit den Schlüsselakteuren der SSB zeigten komplementäre Perspektiven:
- Roland Nowak (Gesamtprojektleiter): Unterstrich, dass ERP-Transformationen zu 80% ein Führungs- und Kommunikationsproblem sind. Die formelle Mitbestimmung mit dem Betriebsrat und ein rigoroses Scope-Management in den Fit-to-Standard Workshops sind der Schlüssel.
- Thomas Wimpff (TPL TP2 Finance): Betonte die Notwendigkeit, das Universal Journal (ACDOCA) und die Trennungsrechnung frühzeitig architektonisch abzusichern, um spätere Steuer- und Bilanzierungsrisiken auszuschließen.
- Armin Heinrich (Basisarchitekt): Verwies auf die zwingende Trennung zwischen Core und BTP sowie die Notwendigkeit stabiler SSO- und Authentifizierungs-Infrastrukturen.`,
            do: 'Nenne die Namen der Experten und ihre spezifischen strategischen Schwerpunkte.',
            dont: 'Behandle die Interviews nicht abstrakt – zeige, dass du mit echten C-Level- und Architektur-Verantwortlichen auf Augenhöhe gesprochen hast.'
          },
          {
            q: 'Wie hängen Boundary Resources Theory und ERP-Plattformisierung zusammen?',
            cat: 'Master & Plattformisierung',
            open: false,
            a: `Die Boundary Resources Theory (Ghazawneh & Henfridsson) erklärt, wie Plattformbetreiber externe Akteure befähigen, Innovationen auf der Plattform zu bauen, ohne die Stabilität der Plattform zu gefährden.

Im ERP-Kontext ist die SAP BTP die 'Boundary Resource':
- Application Boundary Resources (ABR): Freigegebene OData- und REST-APIs, Business Accelerators.
- Development Boundary Resources (DBR): Cloud SDKs, Business Application Studio, CAP/RAP Frameworks.
- Social Boundary Resources (SBR): Architektur-Richtlinien, Clean-Core-Governance und Community-Standards.

Durch diese Grenzressourcen können Fachbereiche und Partner wie Nagarro maßgeschneiderte Apps bauen, während der S/4HANA-Kern modifikationsfrei und upgrade-sicher bleibt.`,
            do: 'Erkläre die 3 Klassen: ABR, DBR, SBR und wende sie direkt auf SAP BTP und APIs an.',
            dont: 'Vergiss nicht die theoretische Quelle: Ghazawneh & Henfridsson.'
          },
          {
            q: "Was haben Sie im Masterprojekt 'Digitale Nachhaltigkeit' (Note 1,0) bei Schmalz GmbH erarbeitet?",
            cat: 'Master & Plattformisierung',
            open: false,
            a: `In der wissenschaftlichen Fallstudie (betreut durch Dr. Dimitri Petrik) ging es um die Optimierung der betrieblichen Abfallbilanz und CSRD-Nachhaltigkeitsberichterstattung beim Weltmarktführer J. Schmalz GmbH.

Ich habe die bestehenden, manuellen Erfassungsprozesse in BPMN 2.0 modelliert, Medienbrüche identifiziert und eine automatisierte Datenextraktionsstrecke mittels PowerShell konzipiert und implementiert. Dadurch wurden Entsorgungsnachweise automatisiert extrahiert, typisiert und fehlerfrei aggregiert – eine direkte Einsparung manueller Aufwände und revisionssichere Datenbasis für den CSRD-Nachhaltigkeitsbericht.`,
            do: 'Nenne Schmalz GmbH, CSRD-Berichterstattung, BPMN 2.0 Modellierung und PowerShell-Automatisierung.',
            dont: 'Wichtig: Dies war eine Fallstudie bei der J. Schmalz GmbH – ordne das Projekt präzise diesem Unternehmen zu!'
          },
          {
            q: 'Was war das Ergebnis Ihres Forschungsprojekts FPWI (Note 1,3)?',
            cat: 'Master & Plattformisierung',
            open: false,
            a: `Im Forschungsprojekt Wirtschaftsinformatik (FPWI) habe ich ein Framework für 'Smart Service Blueprinting' zur Modellierung vernetzter cyber-physischer Systeme (CPS) und IoT-Dienstleistungen entwickelt.

Methodisch basierte die Arbeit auf der Design Science Research Methodology (DSRM nach Peffers). Das konstruierte Artefakt integriert Sensorebenen, Datenflüsse und Service-Touchpoints. In Thinking-Aloud-Tests mit Fachexperten erzielte das Framework einen empirischen System Usability Scale (SUS) Score von 85/100, was der Bestbewertung 'Grade A / Excellent' entspricht.`,
            do: 'Nenne DSRM nach Peffers, Smart Service Blueprinting, Thinking-Aloud Usability Tests und den SUS-Score 85/100.',
            dont: 'Bleibe präzise bei den Methodenbegriffen – das belegt dein universitäres Spitzenforschungs-Niveau.'
          },
          {
            q: "Was haben Sie im Projekt 'PatentRadar' für Klingele Paper & Packaging konzipiert?",
            cat: 'Master & Plattformisierung',
            open: false,
            a: `Im Rahmen der Innovationsmethoden für software- und datenintensive Geschäftsmodelle (ISG) entwickelten wir das Venture-Konzept 'PatentRadar' für die Verpackungsindustrie (Klingele Paper & Packaging).

Wir konzipierten ein hybrides Geschäftsmodell (SaaS & Beratungsdienstleistung), das manuelle Patentrecherchen und Fristenüberwachungen durch eine automatisierte RPA-Strecke (UiPath) in Verbindung mit KI-gestützter Relevanzfilterung (DEPATISnet) ablöst. Ich verantwortete die BPMN 2.0 Prozessanalyse, die Schnittstellendefinition und die wirtschaftliche Business-Case-Kalkulation für das finale Pitchdeck vor C-Level.`,
            do: 'Betone Klingele Paper & Packaging, das hybride Geschäftsmodell, RPA/UiPath-Prozessmodellierung und Wirtschaftlichkeitskalkulation.',
            dont: 'Verwechsle dieses Industrieprojekt nicht mit einem Praktikum – es war ein hochkarätiges universitäres Praxis-Innovationsprojekt.'
          },
          {
            q: 'Wie beurteilen Sie den Notensprung von 3,0 im Bachelor auf 1,6 im Master?',
            cat: 'Master & Plattformisierung',
            open: false,
            a: `Der Notensprung von 3,0 auf 1,6 (+1,4 Notenpunkte) belegt meine außerordentliche Lernkurve und Zielstrebigkeit!

Im Bachelorstudium (180 ECTS) habe ich das breite, harte Fundament erworben: Höhere Mathematik, Theoretische Informatik, Algorithmen, Datenstrukturen und Buchführung. Im Masterstudium (120 ECTS) konnte ich meine Spezialisierung voll entfalten: Software-Architektur (1,7), Advanced Software Engineering (1,6), Digitale Nachhaltigkeit (1,0) und die Masterarbeit mit der Traumnote 1,0.

Ich habe bewiesen, dass ich mich in hochkomplexe Themen verbeiße, mich kontinuierlich steigere und in meiner Fachdomäne zu absoluten Spitzenleistungen fähig bin.`,
            do: 'Framing: Bachelor = breites forderndes Fundament; Master = fokussierte Exzellenz (+1,4 Notenpunkte Leistungssteigerung).',
            dont: 'Entschuldige dich nicht für die 3,0 im Bachelor – die Universität Stuttgart ist bekannt für ihr anspruchsvolles ingenieurwissenschaftliches Niveau!'
          },
          {
            q: 'Was war der Gegenstand Ihrer Bachelorarbeit bei Prof. Herzwurm?',
            cat: 'Bachelor & Methodenkompetenz',
            open: false,
            a: `Meine Bachelorarbeit trug den Titel:
'Die Bedeutung von Boundary Resources in Low-Code Entwicklungsplattformen: Eine qualitative Untersuchung am Beispiel von OutSystems und Mendix'
(Note 1,7 'gut', Lehrstuhl für ABWL und Wirtschaftsinformatik II, Prof. Dr. Georg Herzwurm).

Ich untersuchte, wie führende Low-Code-Plattformen Grenzressourcen bereitstellen, um Citizen Developers und professionelle Software-Ingenieure in die Lage zu versetzen, Anwendungen schnell und architektonisch sauber zu erstellen.`,
            do: 'Nenne den vollen Titel, Note 1,7, die Plattformen OutSystems & Mendix sowie den Lehrstuhl Herzwurm.',
            dont: 'Vergiss nicht die Verbindung zur Masterarbeit: Die Bachelorarbeit legte das theoretische Fundament für Plattform-Architekturen!'
          },
          {
            q: 'Was sind die 14 Klassen von Boundary Resources nach Ghazawneh & Henfridsson?',
            cat: 'Bachelor & Methodenkompetenz',
            open: false,
            a: `In meiner Bachelorarbeit habe ich 14 distinkte Grenzressourcen-Klassen identifiziert und den drei Dimensionen zugeordnet:
1. Application Boundary Resources (ABR): REST/SOAP APIs, Webhooks, Datenkonnektoren und Integrationskomponenten.
2. Development Boundary Resources (DBR): Visuelle Entwicklungsumgebungen (IDE), SDKs, Komponenten-Bibliotheken, Debugging-Tools und Test-Harnesses.
3. Social Boundary Resources (SBR): Marktplätze (z.B. OutSystems Forge), Entwickler-Foren, Dokumentationen, Styleguides und Zertifizierungsprogramme.

Diese Taxonomie belegt, wie Plattform-Ökosysteme technisch und sozial gesteuert werden.`,
            do: 'Strukturiere klar nach ABR, DBR und SBR und nenne konkrete Beispiele wie Marktplätze, SDKs und APIs.',
            dont: 'Bleibe nicht bei der reinen Aufzählung stehen – erkläre den Nutzen für die Plattform-Governance.'
          },
          {
            q: "Wie haben Sie im Bachelor die Bestnote 1,0 in 'Informationssysteme im E-Business' erreicht?",
            cat: 'Bachelor & Methodenkompetenz',
            open: false,
            a: `Informationssysteme im E-Business (Teil von WI 1) war eines der Kernmodule meines Bachelorstudiums. Ich habe mich intensiv mit den Architekturen digitaler B2B- und B2C-Marktplätze, EDI-Standards (EDIFACT), E-Procurement-Katalogen und Plattformökonomie befasst.

Zudem gehörten formale Methoden des Software-Projektmanagements zum Prüfungsstoff: Function-Point-Analyse zur Aufwandsschätzung, Testmanagement-Strategien und agile Entwicklung. Mit der Traumnote 1,0 habe ich bewiesen, dass ich betriebliche Informationssysteme von Grund auf durchdrungen habe.`,
            do: 'Erwähne B2B-Marktplätze, EDIFACT, E-Procurement und die Function-Point-Analyse.',
            dont: "Reduziere E-Business nicht auf einfachen 'Online-Handel' – es geht um komplexe elektronische Wertschöpfungsketten."
          },
          {
            q: 'Was haben Sie im Informationsverarbeitungspraktikum (IVP) bei der 0x539-Wear GmbH analysiert?',
            cat: 'Bachelor & Methodenkompetenz',
            open: false,
            a: `Im Informationsverarbeitungspraktikum (Note 2,3, Lehrstuhl Abteilung VII) führten wir eine tiefgehende datengestützte Unternehmensanalyse der fiktiven 0x539-Wear GmbH durch.

Ich analysierte umfangreiche relationale Bestelldaten und erstellte mehrstufige Deckungsbeitragsrechnungen (DB I bis DB IV). Wir führten Plan-Ist-Vergleiche, ABC-Kunden- und Artikelanalysen sowie Lieferantenbewertungen durch, um margenschwache Produkte und Engpässe im Beschaffungsprozess aufzudecken. Das war mein praktischer Einstieg in Business Intelligence und operatives Controlling.`,
            do: 'Nenne mehrstufige Deckungsbeitragsrechnung, Plan-Ist-Vergleiche und relationale Datenanalysen.',
            dont: 'Tue nicht so, als sei das nur Theorie gewesen – es war ein handfestes BI- und Controlling-Projekt.'
          },
          {
            q: 'Welche Modellierungsmethoden beherrschen Sie aus dem Bachelorstudium?',
            cat: 'Bachelor & Methodenkompetenz',
            open: false,
            a: `Im Modul 'Modellierung' (Note 2,3 bei Prof. Dr. Bernhard Mitschang) und in nachfolgenden Praxisprojekten habe ich ein breites Repertoire formaler Modellierungsmethoden erlernt:
- Geschäftsprozesse: BPMN 2.0 (Gateways, Pools, Lanes, Zwischenereignisse, Nachrichtenflüsse) und erweiterte Ereignisgesteuerte Prozessketten (eEPK).
- Software- und Systemarchitektur: UML 2.0 (Klassendiagramme, Sequenzdiagramme, Zustandsautomaten, Aktivitätsdiagramme).
- Formale Systeme: Petrinetze (Erreichbarkeitsgraphen, Lebendigkeit, Verklemmungsfreiheit).
- Datenmodellierung: Entity-Relationship-Modelle (ERM), Relationale Algebra, Normalisierung (1NF bis BCNF) und SQL.`,
            do: 'Nenne BPMN 2.0, UML, Petrinetze, ERM und Normalformen.',
            dont: "Stelle Modellierung nicht als 'bunte Kästchen malen' dar – es ist die formale Semantik für fehlerfreie IT-Architekturen."
          },
          {
            q: 'Worum ging es in Ihrer Seminararbeit bei Prof. Dr. Marion Büttgen (Hohenheim)?',
            cat: 'Bachelor & Methodenkompetenz',
            open: false,
            a: `Am Lehrstuhl für Unternehmensführung der Universität Hohenheim (Prof. Dr. Marion Büttgen) verfasste ich meine Seminararbeit zum Thema Mensch-Roboter-Interaktion und Servicequalität bei digitalen Service Encountern.

Ich untersuchte auf Basis des Expectation-Confirmation-Modells (ECM) und der Servqual-Dimensionen, wie Kunden die Interaktion mit Servicerobotern und KI-Assistenten wahrnehmen und welche Faktoren die Akzeptanz und Zufriedenheit im Dienstleistungssektor determinieren. Diese Arbeit schärfte meinen Blick für User Acceptance und Human-Computer-Interaction.`,
            do: 'Nenne Prof. Büttgen, Expectation-Confirmation-Modell (ECM) und Service Encounters.',
            dont: 'Vergiss nicht den Nutzen: Akzeptanzforschung ist direkt relevant für die Einführung neuer SAP Fiori Apps bei Anwendern.'
          },
          {
            q: 'Welche mathematisch-statistischen Methoden beherrschen Sie?',
            cat: 'Bachelor & Methodenkompetenz',
            open: false,
            a: `Mein Studium umfasste 30 ECTS mathematisch-methodische Grundlagen:
- Höhere Mathematik: Lineare Algebra, Matrizenrechnung, Vektorräume, Differential- und Integralrechnung mehrerer Variablen und Optimierung unter Nebenbedingungen (Lagrange-Multiplikatoren).
- Deskriptive & Induktive Statistik: Wahrscheinlichkeitsverteilungen (Normal-, t-, Chi-Quadrat-Verteilung), Konfidenzintervalle, parametrische und nicht-parametrische Hypothesentests, lineare und multivariate Regression sowie Zeitreihenanalysen.
- Algorithmik: Analyse der asymptotischen Laufzeit- und Speicherkomplexität (O-Notation) in Datenstrukturen und Algorithmen.`,
            do: 'Betone die quantitative Denkdisziplin und das Durchhaltevermögen bei anspruchsvollen mathematischen Methoden.',
            dont: "Lass dich nicht als 'reiner BWLer' abstempeln – du hast das volle informationstechnische Mathe-Programm absolviert!"
          },
          {
            q: 'Was beinhaltet Ihre TOGAF 9 ADM Zertifizierung bei Scape Consulting?',
            cat: 'Enterprise Architecture & TOGAF',
            open: false,
            a: `Ich habe den TOGAF 9 ADM-Intensivkurs an der Universität Stuttgart bei Dr. Daniel Simon (Scape Consulting GmbH, 16.01.2020) erfolgreich absolviert.

Der Kurs vermittelte den vollständigen Architektur-Entwicklungszyklus (Architecture Development Method ADM):
- Vorphase: Architecture Principles & Governance Framework
- Phase A: Architecture Vision & Stakeholder Management
- Phase B: Business Architecture (Geschäftsprozesse, Fähigkeiten)
- Phase C: Information Systems Architecture (Data & Application Architecture)
- Phase D: Technology Architecture (Infrastruktur, Plattformen)
- Phase E & F: Opportunities & Solutions, Migration Planning
- Phase G & H: Implementation Governance & Architecture Change Management`,
            do: 'Nenne Scape Consulting, Dr. Daniel Simon, die ADM-Phasen A-H und die 4 Kernarchitekturen.',
            dont: 'Beschreibe TOGAF nicht nur theoretisch – erkläre, wie du diese Struktur im Solution Design bei der SSB genutzt hast.'
          },
          {
            q: 'Was versteht man unter dem TOGAF Architecture Metamodel?',
            cat: 'Enterprise Architecture & TOGAF',
            open: false,
            a: `Das TOGAF Architecture Metamodel definiert die formalen Objekttypen und deren Beziehungen innerhalb einer Unternehmensarchitektur.

Es verknüpft strukturiert:
- Business Architecture: Business Capabilities, Business Actors, Rollen und Geschäftsprozesse.
- Information Systems Architecture: Data Entities, Logical Data Models und Application Components.
- Technology Architecture: Technology Services, Nodes und Netzwerke.

Dieses Metamodell verhindert Insellösungen, weil jede Software-Komponente und jedes Datenobjekt exakt einem Geschäftsziel und Geschäftsprozess zugeordnet ist.`,
            do: 'Erkläre die vertikale Durchgängigkeit: Business Goal -> Capability -> Process -> Application -> Data -> Technology Node.',
            dont: 'Verliere dich nicht in Fachchinesisch – der Kern ist die lückenlose Verknüpfung von Business und IT.'
          },
          {
            q: 'Was ist der Unterschied zwischen Baseline Architecture und Target Architecture?',
            cat: 'Enterprise Architecture & TOGAF',
            open: false,
            a: `Die Baseline Architecture beschreibt den aktuellen Ist-Zustand der Anwendungs-, Daten- und Technologie-Landschaft (inklusive historischer Z-Modifikationen, redundanter Systeme und technischer Schulden).

Die Target Architecture definiert den strategischen Soll-Zustand (z.B. Greenfield S/4HANA Private Cloud, Clean Core, BTP-Integration).

Der Wert entsteht durch die Gap-Analyse: Was fällt weg? Was wird neu aufgebaut? Wie sehen die Transition Architectures (Übergangszustände) aus, um das Geschäft während der mehrjährigen Transformation ohne Unterbrechung am Laufen zu halten?`,
            do: 'Nenne Gap-Analyse, Transition Architectures und die Risikominimierung im laufenden Geschäftsbetrieb.',
            dont: 'Vergiss nicht die Transition Architectures – Großunternehmen können nicht über Nacht den Schalter umlegen.'
          },
          {
            q: 'Wie funktioniert Architecture Governance in der Praxis?',
            cat: 'Enterprise Architecture & TOGAF',
            open: false,
            a: `Architecture Governance stellt sicher, dass laufende Projekte nicht an den Unternehmensrichtlinien vorbeientwickeln.

In der Praxis wird dazu ein Architecture Review Board (ARB) etabliert. Wenn ein Projektteam oder Fachbereich eine neue Anforderung hat, die vom Standard abweicht, muss ein Architecture Compliance Review durchlaufen werden. Es wird geprüft: Entspricht die Lösung den Clean-Core-Richtlinien? Gibt es Sicherheits- oder Datenrisiken? Werden bestehende BTP-Dienste genutzt? Erst mit ARB-Freigabe darf die Implementierung beginnen.`,
            do: 'Nenne das Architecture Review Board (ARB), Architecture Compliance Reviews und Clean-Core-Gates.',
            dont: 'Stelle Governance nicht als bürokratische Bremse dar – sie schützt das Unternehmen vor Millionenverlusten durch Fehlinvestitionen.'
          },
          {
            q: 'Wie grenzt sich Enterprise Architecture von reiner Softwareentwicklung ab?',
            cat: 'Enterprise Architecture & TOGAF',
            open: false,
            a: `Klassische Softwareentwicklung fokussiert auf die Implementierung eines konkreten Systems: Code-Qualität, Frameworks, Klassen, Algorithmen und Sprint-Deliverables im Zeithorizont von Wochen bis Monaten.

Enterprise Architecture Management (EAM) blickt aus der Vogelperspektive auf das gesamte Ökosystem im Zeithorizont von 3 bis 7 Jahren: Wie spielen 50 verschiedene Systeme, ERP-Kerne, Cloud-Plattformen, Schnittstellen, regulatorische Vorgaben und Business-Fähigkeiten zusammen? EAM fragt nicht 'Wie schreibe ich den Code?', sondern 'Sollte diese Funktion überhaupt im Kern gebaut werden oder gehört sie auf die BTP?'`,
            do: 'Klarer Kontrast: Softwareentwicklung = lokale Systemimplementierung; EAM = strategische Gesamtsystem- und Portfolio-Steuerung.',
            dont: 'Werte die Softwareentwicklung nicht ab – betone, dass EAM das Dach bildet, unter dem Entwickler sauber arbeiten können.'
          },
          {
            q: 'Warum bewerben Sie sich bewusst auf eine Junior-Position oder ein Traineeprogramm?',
            cat: 'Persönlich & Trainee-Einstieg',
            open: false,
            a: `Weil ich realistische Selbsteinschätzung mit hoher Leistungsbereitschaft verbinde!

Ich bringe zwar durch 24 Monate S/4HANA Großprojekt im IT-PMO, 12 Monate Rechenzentrumsbetrieb bei DC1 und meine mit 1,0 bewertete Masterarbeit ein außergewöhnlich starkes Fundament mit. Aber: Jedes Unternehmen hat eigene Prozesse, eigene Unternehmenskulturen und spezifische Systemlandschaften.

Ich suche den Einstieg als Junior Consultant oder in einem anspruchsvollen Traineeprogramm, um mit einer gesunden Mischung aus Demut, Neugier und Engagement Ihr Unternehmen von Grund auf kennenzulernen. Ich möchte nicht mit vorgefertigten Meinungen auftreten, sondern zuhören, schnell lernen und mit hoher Verlässlichkeit binnen kürzester Zeit zur tragenden Säule in Ihrem Team heranwachsen.`,
            do: 'Betone die Haltung: Fundiertes Vorwissen vorhanden, aber bewusste Offenheit, Lernbegierde und Respekt vor der Firmenkultur.',
            dont: "Trete nicht arrogant auf ('Ich weiß schon alles wegen meiner 1,0'). Reife Absolventen zeigen Lernbereitschaft!"
          },
          {
            q: 'Wie reagieren Sie, wenn Sie in einem Projekt auf eine völlig unbekannte SAP- oder IT-Frage stoßen?',
            cat: 'Persönlich & Trainee-Einstieg',
            open: false,
            a: `Ich verfalle weder in Aktionismus noch sitze ich das Problem aus, sondern gehe in einem 4-Stufen-Modell vor:
1. Problem strukturieren: Exakte Definition des Gaps – handelt es sich um ein Prozess-, Konfigurations- oder Schnittstellenthema?
2. Eigenrecherche im Standard: Analyse der SAP Best Practice Explorer Scope-IDs, SAP Learning Hub und offizieller SAP Press Referenzen.
3. Lösungsoptionen erarbeiten: Ich erarbeite mindestens 2 fundierte Handlungsoptionen inklusive Vor- und Nachteilen.
4. Gezielte Abstimmung: Mit diesen vorstrukturierten Optionen gehe ich auf Seniorkollegen oder Fachexperten zu. So stehle ich niemandem Zeit, sondern ermögliche eine fundierte Entscheidung.`,
            do: 'Beschreibe die 4 Stufen: Strukturieren -> Eigenrecherche -> Optionen formulieren -> Gezieltes Sparring.',
            dont: "Sage niemals 'Ich frage sofort meinen Chef' (unselbstständig) oder 'Ich probiere einfach rum' (gefährlich im Produktivsystem)."
          },
          {
            q: 'Wie vermitteln Sie zwischen rein technischen Beratern und konservativen Fachbereichen?',
            cat: 'Persönlich & Trainee-Einstieg',
            open: false,
            a: `Das war genau meine tägliche Rolle im IT-PMO bei der SSB!

Fachbereiche denken in ihren gewohnten Buchungsabläufen, Belegen und Arbeitszeitplänen; technische Berater von Partnern wie Nagarro denken in CDS Views, OData-Services und RAP-Objekten. Meine Stärke ist die 'bilinguale' Vermittlung:
Ich übersetze die Anforderungen des Fachbereichs in präzise User Stories und Akzeptanzkriterien für die Entwickler. Umgekehrt erkläre ich dem Fachbereich technische Einschränkungen nicht mit IT-Jargon, sondern anhand der konkreten Auswirkungen auf ihren täglichen Arbeitsablauf in SAP Fiori.`,
            do: "Framing: Du bist der 'Bilinguale Übersetzer' zwischen Fachbereichs-Sprache und IT-Architektur.",
            dont: "Wähle keine Partei – weder Fachbereich noch IT sind 'schuld', wenn Kommunikation hakt; es braucht Empathie für beide Seiten."
          },
          {
            q: 'Welche Gehaltserwartung bringen Sie für den Berufseinstieg mit?',
            cat: 'Persönlich & Trainee-Einstieg',
            open: false,
            a: `Auf Basis meiner soliden Qualifikation – Master of Science Wirtschaftsinformatik an der Universität Stuttgart (Note 1,6), Masterarbeit mit Note 1,0 sowie insgesamt 36 Monaten relevanter Praxiserfahrung in Großprojekt (SSB) und Rechenzentrum (DC1) – sehe ich ein Einstiegsgehalt im Bereich von 55.000 € bis 65.000 € brutto pro Jahr als fair und marktüblich an.

Für mich steht jedoch der inhaltliche Fit, die Qualität des Teams, anspruchsvolle Projekte und gezielte Weiterentwicklungsmöglichkeiten klar an erster Stelle. Wenn das Gesamtpaket stimmt, finden wir mit Sicherheit eine gemeinsame Basis.`,
            do: 'Nenne die Spanne 55.000 € - 65.000 € ruhig, begründe sie sachlich mit 300 ECTS + 36 Mo. Praxis und betone die Priorität der Lernperspektive.',
            dont: 'Nenne keine überzogenen 75k-80k Senior-Forderungen und sei nicht unverschämt flexibel nach unten (unter Wert verkaufen).'
          },
          {
            q: 'Wo sehen Sie sich in 3 bis 5 Jahren in unserer Organisation?',
            cat: 'Persönlich & Trainee-Einstieg',
            open: false,
            a: `In 3 bis 5 Jahren sehe ich mich als fachlich etablierte und geschätzte Stütze in Ihrem Beratungsteam oder Enterprise-Architecture-Bereich.

Ich möchte nach meiner Junior-/Traineephase schnell eigenverantwortlich anspruchsvolle Teilprojekte und Workstreams führen, die Schnittstelle zwischen Business und IT gestalten und mein Wissen über moderne Cloud-Architekturen und Clean Core kontinuierlich vertiefen. Zudem liegt es mir am Herzen, neue Trainees und Werkstudenten an Bord zu holen und als Mentor die nächste Generation mit der gleichen Begeisterung zu unterstützen, die ich heute mitbringe.`,
            do: 'Skizziere einen klaren Entwicklungspfad: Verantwortung übernehmen -> Fachthemen prägen -> Mentoring für Nachwuchs.',
            dont: "Sage nicht 'Ich will Partner / Geschäftsführer werden' – zeige Loyalität, Teamorientierung und fachliche Reife."
          }
        ];

        const filesData = [
          // --- 00 AKTUELLE BEWERBUNGSUNTERLAGEN (Master of Science | 120 ECTS | Gesamtnote 1,6) ---
          { name: 'Lebenslauf_Murseli_Vsar.pdf', cat: 'Aktuelle Bewerbungsunterlagen', path: '00_Aktuelle_Bewerbungsunterlagen', desc: 'Offizieller, tagesaktueller Haupt-Lebenslauf (M.Sc. Wirtschaftsinformatik, Uni Stuttgart, 24 Monate SSB AG, 12 Monate Datacenter One).', impact: 'Das Herzstück deiner Bewerbung – belegt deinen lückenlosen Werdegang und SAP S/4HANA Spezialisierung.' },
          { name: 'Zeugnisse_Murseli_Visar.pdf', cat: 'Aktuelle Bewerbungsunterlagen', path: '00_Aktuelle_Bewerbungsunterlagen', desc: 'Vollständiges amtliches Zeugnispaket (Masterurkunde Note 1,6, Bachelorzeugnis, Arbeitszeugnisse SSB AG und Datacenter One, Abitur, alle Zertifikate).', impact: 'Vollständiger amtlicher Nachweis für Spitzenleistungen in Akademie und Praxis.' },
          { name: 'Zeugnisse_Murseli_kurz.pdf', cat: 'Aktuelle Bewerbungsunterlagen', path: '00_Aktuelle_Bewerbungsunterlagen', desc: 'Kompakter Zeugnisauszug für Bewerbungsportale mit restriktiven Dateigrößen-Limits.', impact: 'Optimiert für maximale Lese- und Upload-Effizienz.' },
          { name: 'Masterarbeit_Visar_Murseli.pdf', cat: 'Aktuelle Bewerbungsunterlagen', path: '00_Aktuelle_Bewerbungsunterlagen', desc: 'Vollständige Masterarbeit (Note 1,0): Kritische Erfolgsfaktoren in der Transformation großer ERP-Systeme: Eine Untersuchung am Beispiel der Plattformisierung von SAP S/4HANA (126 Seiten).', impact: 'Belegt herausragende wissenschaftliche Exzellenz und praxisorientierte Forschung.' },
          { name: 'Lebenslauf_Murseli_Vsar.docx', cat: 'Aktuelle Bewerbungsunterlagen', path: '00_Aktuelle_Bewerbungsunterlagen', desc: 'Editierbare Master-Vorlage zur individuellen Anpassung für spezifische Vakanzen.', impact: 'Flexibles Arbeitsdokument für gezielte Unternehmens-Anpassungen.' },
          { name: 'Bewerbungsverlauf.xlsx', cat: 'Aktuelle Bewerbungsunterlagen', path: '00_Aktuelle_Bewerbungsunterlagen', desc: 'Interne Steuerung und Übersicht aller laufenden Bewerbungsverfahren, Interviewphasen und Gehaltsbänder.', impact: 'Dein persönliches Cockpit für professionelles Bewerbungsmanagement.' },

          // --- SAP PRESS & RHEINWERK FACHLITERATUR (Offizielle Referenzwerke aus der SSB Transformation) ---
          { name: 'Enterprise Architecture Transformation with SAP.pdf', cat: 'SAP Fachliteratur (Rheinwerk)', path: '01_SSB/04_Architektur_Methoden_Tools/SAP_Fachbuecher_Referenzen', desc: 'Standardwerk von SAP Press zur EAM-Transformation, IT-Landschaftsplanung, Capability Mapping und Plattform-Evolution.', impact: 'Beweist, dass dein Architektur- und Transformationswissen auf den offiziellen weltweiten SAP-Standards basiert.' },
          { name: 'Migration_nach_SAP_S4HANA.pdf', cat: 'SAP Fachliteratur (Rheinwerk)', path: '01_SSB/04_Architektur_Methoden_Tools/SAP_Fachbuecher_Referenzen', desc: 'Umfassendes Handbuch (Rheinwerk): Greenfield, Brownfield, Selective Data Transition, LTMC Staging-Tabellen und Cutover.', impact: 'Zeigt tiefes methodisches Verständnis der Migrationspfade und Datenqualitätsregeln.' },
          { name: 'SAP_Cloud_ALM.pdf', cat: 'SAP Fachliteratur (Rheinwerk)', path: '01_SSB/04_Architektur_Methoden_Tools/SAP_Fachbuecher_Referenzen', desc: 'Offizielles Handbuch für Application Lifecycle Management im Cloud- und Hybrid-Zeitalter (Prozesse, Stories, Testautomation).', impact: 'Fachliches Fundament für deine Tool-Governance in CALM bei der SSB.' },
          { name: 'SAP_HANA_Cloud.pdf', cat: 'SAP Fachliteratur (Rheinwerk)', path: '01_SSB/04_Architektur_Methoden_Tools/SAP_Fachbuecher_Referenzen', desc: 'In-Memory-Architektur, Columnar Storage, ACDOCA Aggregation on-the-fly, Core Data Services (CDS Views) und Calculation Views.', impact: 'Technisches Fundament zum Verständnis von Multi-Model Data Processing und HANA Engine.' },
          { name: 'Berechtigungen_in_S4HANA_und_Fiori.pdf', cat: 'SAP Fachliteratur (Rheinwerk)', path: '01_SSB/04_Architektur_Methoden_Tools/SAP_Fachbuecher_Referenzen', desc: 'Rollen- und Berechtigungsarchitektur (PFCG), Fiori Katalogen, Spaces & Pages, SoD-Konflikte und DSGVO-Schutzmaßnahmen.', impact: 'Echtes Differenzierungsmerkmal für Governance- und Compliance-Gespräche mit C-Level und Betriebsrat.' },
          { name: 'BPI_mit_SAP.pdf', cat: 'SAP Fachliteratur (Rheinwerk)', path: '01_SSB/04_Architektur_Methoden_Tools/SAP_Fachbuecher_Referenzen', desc: 'Business Process Intelligence & SAP Signavio: Process Mining, Process Insights, Plug-and-Gain und kollaboratives Prozessdesign.', impact: 'Verbindet strategisches Prozessmanagement mit datengestütztem Process Mining.' },
          { name: 'SAP_Enable_Now_Handbuch.pdf', cat: 'SAP Fachliteratur (Rheinwerk)', path: '01_SSB/04_Architektur_Methoden_Tools/SAP_Fachbuecher_Referenzen', desc: 'Leitfaden für Single-Source-Content, In-App-Hilfe (Web Assistant), Producer, Desktop Assistant und E-Learning Rollout.', impact: 'Belegt didaktische und funktionale Exzellenz beim Rollout digitaler Lernplattformen.' },

          // --- MASTER OF SCIENCE (120 ECTS | Gesamtnote 1,6 | Uni Stuttgart) ---
          { name: 'Masterarbeit Wirtschaftsinformatik', cat: 'Master-Module (120 ECTS)', path: '02_Master/Masterarbeit Wirtschaftsinformatik', desc: 'Masterarbeit (Note 1,0, 30 ECTS): Kritische Erfolgsfaktoren in der Transformation großer ERP-Systeme: Eine Untersuchung am Beispiel der Plattformisierung von SAP S/4HANA (Prof. Dr. Georg Herzwurm). 126 Seiten, 12 Experteninterviews im Großprojekt SAP4SSB.', impact: 'Dein akademisches Meisterstück – belegt deine wissenschaftliche und architektonische Spitzenklasse.' },
          { name: 'Digitale Nachhaltigkeit', cat: 'Master-Module (120 ECTS)', path: '02_Master/Digitale Nachhaltigkeit', desc: 'Wissenschaftliches Projekt (Note 1,0, 6 ECTS): Nachhaltigkeit durch Automatisierung: Eine Fallstudie zur Optimierung der Abfallbilanz bei der Schmalz GmbH (Dr. Dimitri Petrik). PowerShell-Automatisierung & BPMN 2.0.', impact: 'Nachweis für Green-IT-, Prozessautomatisierungs- und Nachhaltigkeits-Expertise im Industrieumfeld.' },
          { name: 'Forschungsprojekte in der Wirtschaftsinformatik', cat: 'Master-Module (120 ECTS)', path: '02_Master/Forschungsprojekte in der Wirtschaftsinformatik', desc: 'Forschungsprojekt (Note 1,3, 6 ECTS): Smart Service Blueprinting (SSB) für vernetzte Produkte und cyber-physische Systeme. Research-in-Progress Paper & Abschlusspräsentation.', impact: 'Beweist hohe Forschungskompetenz im Service Engineering und IoT-Ökosystemen.' },
          { name: 'Advanced Software Engineering', cat: 'Master-Module (120 ECTS)', path: '02_Master/Advanced Software Engineering', desc: 'Vorlesung & Übung (Note 1,6, 6 ECTS): Softwareprozess-Bewertung, Requirements Engineering, agile Skalierung und Qualitätsmetriken (Prof. Dr. Steffen Becker).', impact: 'Fundiertes Software-Engineering-Wissen für die Steuerung komplexer IT-Entwicklungsprojekte.' },
          { name: 'Applied AI and Upcoming Technologies in Industries', cat: 'Master-Module (120 ECTS)', path: '02_Master/Applied AI and Upcoming Technologies in Industries', desc: 'Projekt & Vorlesung (Note 1,7, 6 ECTS): KI im industriellen Einsatz, AR/VR-Trainingssysteme, LLMs und Transformer-Modelle. Abgabevideo & Paper zum Projekt Yarro.', impact: 'Demonstriert Hands-on KI-Kompetenz und zukunftsorientierte Technologiebewertung.' },
          { name: 'Forschungsmethoden in der Wirtschaftsinformatik', cat: 'Master-Module (120 ECTS)', path: '02_Master/Forschungsmethoden in der Wirtschaftsinformatik', desc: 'Methodenmodul (Note 1,7, 6 ECTS): Design Science Research (DSR), systematische Literaturanalysen, qualitative Inhaltsanalyse (Mayring) und empirische Hypothesentests (SPSS & SmartPLS).', impact: 'Methodisches Rückgrat für forschungsnahe Beratung und strukturierte Problemzerlegung.' },
          { name: 'Innovationsmanagement', cat: 'Master-Module (120 ECTS)', path: '02_Master/Innovationsmanagement', desc: 'Modul (Note 1,7, 6 ECTS): Patentbewertung, Technologiediffusion, Quality Function Deployment (QFD/HoQ) und R-gestützte Diffusionsschätzung.', impact: 'Strategisches Innovations-Know-how zur Bewertung von Markt- und Technologiepotenzialen.' },
          { name: 'Seminar Wirtschaftsinformatik 2', cat: 'Master-Module (120 ECTS)', path: '02_Master/Seminar Wirtschaftsinformatik 2', desc: 'Seminararbeit (Note 1,7, 6 ECTS): Mensch-Roboter-Kollaboration in der Produktion: Eine systematische Literaturanalyse (PRISMA-Flowchart, Konzeptmatrix, 26 Kernstudien).', impact: 'Belegt herausragende Fähigkeiten in strukturierter Literaturarbeit und Synthese komplexer Fachdomänen.' },
          { name: 'Software-Architektur', cat: 'Master-Module (120 ECTS)', path: '02_Master/Software-Architektur', desc: 'Modul (Note 1,7, 6 ECTS): Quantitative Analyse von Softwaredesigns (QASD), UML-Profile, Markov-Ketten und Queuing Networks (Prof. Dr. Steffen Becker).', impact: 'Tiefes Architekturverständnis für skalierbare, performante und entkoppelte Enterprise-Systeme.' },
          { name: 'Theorie und Empirie internationaler Unternehmenstätigkeit', cat: 'Master-Module (120 ECTS)', path: '02_Master/Theorie und Empirie internationaler Unternehmenstätigkeit', desc: 'Modul (Note 1,7, 6 ECTS): Internationales Management, OLI-Paradigma, Globalisierungsstrategien und empirische Studien (Prof. Dr. Michael-Jörg Oesterle).', impact: 'Strategisches Verständnis globaler Wertschöpfungsketten und multinationaler Unternehmensführung.' },
          { name: 'AI4IoT – Artificial Intelligence for the Internet of Things', cat: 'Master-Module (120 ECTS)', path: '02_Master/AI4IoT – Artificial Intelligence for the Internet of Things', desc: 'Modul & Fallstudie (Note 2,0, 6 ECTS): OT-IT-IoT Konvergenz, Edge AI, Fallstudie Bademeister, Trustworthy IoT und wissenschaftliches Shortpaper.', impact: 'Verbindet Sensorik, IoT-Infrastruktur und Edge-KI zu konkreten industriellen Use Cases.' },
          { name: 'Innovationsmethoden für software- und datenintensive Geschäftsmodelle', cat: 'Master-Module (120 ECTS)', path: '02_Master/Innovationsmethoden für software- und datenintensive Geschäftsmodelle', desc: 'Praxisprojekt Klingele (Note 2,0, 6 ECTS): PatentRadar – Konzeption eines SaaS/RPA-Geschäftsmodells zur KI-gestützten Patentrecherche mit UiPath und DEPATISnet.', impact: 'Echter Business Case: RPA-Entwicklung, Wirtschaftlichkeitskalkulation und C-Level Pitchdeck.' },
          { name: 'Service Management and Cloud Computing, and Evaluation', cat: 'Master-Module (120 ECTS)', path: '02_Master/Service Management and Cloud Computing, and Evaluation', desc: 'Modul & Paper (Note 2,0, 6 ECTS): AWS Cloud Design Patterns, Serverless Web Apps (WildRydes), Lambda, API Gateway und Gartner Magic Quadrant Bewertung.', impact: 'Praxisnachweis für Cloud-Native-Architekturen, Microservices und moderne Integrationsmuster.' },
          { name: 'Datenbanken und Informationssysteme', cat: 'Master-Module (120 ECTS)', path: '02_Master/Datenbanken und Informationssysteme', desc: 'Modul (Note 2,7, 6 ECTS): Relationale Datenmodellierung, SQL, Transaktionsmanagement (ACID), Indexierung und moderne DBIS-Architekturen.', impact: 'Fundiertes Datenbank-Fundament – unverzichtbar für das Verständnis von SAP HANA und In-Memory-Tabellen.' },
          { name: 'Management von IT-Unternehmen', cat: 'Master-Module (120 ECTS)', path: '02_Master/Management von IT-Unternehmen', desc: 'Modul (Note 3,0, 6 ECTS): Geschäftsmodell-Innovation, Finanzierung, Teambildung, Funding und Skalierung von Tech-Startups und IT-Dienstleistern.', impact: 'Unternehmerisches Verständnis für IT-Geschäftsmodelle und agile Unternehmenssteuerung.' },
          { name: 'Service Operations Management', cat: 'Master-Module (120 ECTS)', path: '02_Master/Service Operations Management', desc: 'Modul (Note 3,0, 6 ECTS): Service Engineering, Service-Qualitätsmessung, Servitization und operative Steuerung industrieller Dienstleistungen.', impact: 'Koppelt Prozess- und Service-Exzellenz für kundenzentrierte B2B-Dienstleistungsmodelle.' },

          // --- BACHELOR OF SCIENCE (180 ECTS | Gesamtnote 3,0 | Uni Stuttgart) ---
          { name: 'Informationssysteme im E-Business', cat: 'Bachelor-Module (180 ECTS)', path: '03_Bachelor/Betriebliche Informationssysteme (WI 1)/01_Informationssysteme_im_E-Business_WS19', desc: 'Spitzenprüfung (Note 1,0, Teil von WI 1): E-Commerce Architekturen, elektronische Marktplätze, EDI und digitale Plattformökonomie.', impact: 'Beweist absolute Bestleistung (1,0) im Bereich betrieblicher digitaler Informationssysteme.' },
          { name: 'Bachelorarbeit Wirtschaftsinformatik', cat: 'Bachelor-Module (180 ECTS)', path: '03_Bachelor/Bachelorarbeit Wirtschaftsinformatik/01_Erfolgreiche_Bachelorarbeit_Boundary_Resources_Note_1_7', desc: 'Bachelorarbeit (Note 1,7, 12 ECTS): Die Bedeutung von Boundary Resources in Low-Code Entwicklungsplattformen: Eine qualitative Untersuchung am Beispiel von OutSystems und Mendix (Prof. Herzwurm).', impact: 'Theoretisches Fundament in Boundary Resource Theory (ABR, DBR, SBR) und Plattform-Architektur.' },
          { name: 'Betriebliche Informationssysteme (WI 1)', cat: 'Bachelor-Module (180 ECTS)', path: '03_Bachelor/Betriebliche Informationssysteme (WI 1)', desc: 'Kernmodul (Note 2,1, 9 ECTS): Management betrieblicher Informationssysteme (MBIS) und E-Business. ERP-Grundlagen, Prozessintegration und Schnittstellendesign.', impact: 'Grundlegendes Fundament für deine Spezialisierung auf Enterprise Resource Planning (ERP).' },
          { name: 'Modellierung', cat: 'Bachelor-Module (180 ECTS)', path: '03_Bachelor/Modellierung', desc: 'Informatik-Pflichtmodul (Note 2,3, 6 ECTS): Formale Modellierungsmethoden, Petri-Netze, Zustandsautomaten und konzeptionelle Datenmodellierung (Prof. Dr. Bernhard Mitschang).', impact: 'Methodische Präzision beim Entwurf formaler und konsistenter Systemmodelle.' },
          { name: 'Seminar interdisziplinäre Themen', cat: 'Bachelor-Module (180 ECTS)', path: '03_Bachelor/Seminar interdisziplinäre Themen', desc: 'Seminar (Note 2,3, 6 ECTS): Maschinelles Lernen & Big Data. Wissenschaftliches Handout, Regression und Präsentation.', impact: 'Frühzeitige Auseinandersetzung mit Data Science und angewandtem Machine Learning.' },
          { name: 'Informationsverarbeitungspraktikum', cat: 'Bachelor-Module (180 ECTS)', path: '03_Bachelor/Informationsverarbeitungspraktikum', desc: 'Praktikum (Note 2,3, 6 ECTS): Praktische Unternehmens- und Systemanalyse, Geschäftsprozessaufnahme und IT-Architekturentwurf.', impact: 'Praxisnahe Erprobung von Anforderungsanalyse und IT-Konzeption im Team.' },
          { name: 'Einführung in die Wirtschaftsinformatik', cat: 'Bachelor-Module (180 ECTS)', path: '03_Bachelor/Einführung in die Wirtschaftsinformatik', desc: 'Grundlagenmodul (Note 2,7, 6 ECTS): Informationssysteme in Wirtschaft und Verwaltung, Geschäftsprozessmanagement und Datenorganisation (Prof. Dr. Georg Herzwurm).', impact: 'Der Grundstein deines Studiums am Lehrstuhl für Wirtschaftsinformatik II.' },
          { name: 'GVWL 1 - Märkte & wirtschaftliche Entscheidungen', cat: 'Bachelor-Module (180 ECTS)', path: '03_Bachelor/GVWL 1 - Märkte & wirtschaftliche Entscheidungen', desc: 'VWL-Pflichtmodul (Note 2,7, 6 ECTS): Mikroökonomik, Marktformen, Preisbildung, Wohlfahrtstheorie und strategische Interaktion.', impact: 'Ökonomisches Fundament zum Verständnis von Marktmechanismen und Anreizstrukturen.' },
          { name: 'GBWL 1 - Strukturen der Betriebswirtschaftslehre', cat: 'Bachelor-Module (180 ECTS)', path: '03_Bachelor/GBWL 1 - Strukturen der Betriebswirtschaftslehre', desc: 'BWL-Pflichtmodul (Note 2,7, 6 ECTS): Einführung in die BWL und Einführung in das Rechnungswesen (ReWe: Buchführung, Bilanzierung, GuV, KLR).', impact: 'Unerlässlich für das Verständnis des Finanzwesens (FI) und des Controllings (CO) in SAP.' },
          { name: 'GBWL 4 - Finanzprozess', cat: 'Bachelor-Module (180 ECTS)', path: '03_Bachelor/GBWL 4 - Finanzprozess', desc: 'BWL-Pflichtmodul (Note 2,7, 6 ECTS): Investition und Finanzierung (InFi), Kapitalwertmethode, Annuitäten, Innen-/Außenfinanzierung und Derivate.', impact: 'Finanzwirtschaftliches Rüstzeug für Investitionsrechnungen und Business-Case-Modellierung.' },
          { name: 'Statistik II', cat: 'Bachelor-Module (180 ECTS)', path: '03_Bachelor/Statistik II', desc: 'Methodenmodul (Note 2,7, 6 ECTS): Induktive Statistik, Wahrscheinlichkeitsverteilungen, Konfidenzintervalle und statistische Testverfahren.', impact: 'Empirische Datenkompetenz für quantitative Analysen und wissenschaftliches Arbeiten.' },
          { name: 'Datenstrukturen und Algorithmen', cat: 'Bachelor-Module (180 ECTS)', path: '03_Bachelor/Datenstrukturen und Algorithmen', desc: 'Informatik-Pflichtmodul (Note 3,0, 9 ECTS): Bäume, Graphen, Sortieralgorithmen, Hashing, Komplexitätsanalyse (O-Notation) und Rekursion (Prof. Dr. Stefan Funke).', impact: 'Fundiertes algorithmisches Denken und Verständnis für Performanzoptimierung.' },
          { name: 'Programmentwicklung', cat: 'Bachelor-Module (180 ECTS)', path: '03_Bachelor/Programmentwicklung', desc: 'Informatik-Pflichtmodul (Note 3,0, 6 ECTS): Funktionale und logische Programmierung, Programmiersprachenkonzepte und formale Semantik.', impact: 'Erweitert das Programmierparadigma über die reine OOP hinaus.' },
          { name: 'Softwarepraktikum', cat: 'Bachelor-Module (180 ECTS)', path: '03_Bachelor/Softwarepraktikum', desc: 'Team-Projekt (Note 3,0, 6 ECTS): Entwicklung des Projektmanagementsystems taskMasterPro 3 im 5-köpfigen Team. Lastenheft, Spezifikation, Java-Implementierung und Präsentation.', impact: 'Echter Praxisnachweis für Teamarbeit, agile Softwareentwicklung und Software-Life-Cycle.' },
          { name: 'Informationsmanagement', cat: 'Bachelor-Module (180 ECTS)', path: '03_Bachelor/Informationsmanagement', desc: 'Kernmodul (Note 3,0, 9 ECTS): Grundlagen des Informationsmanagements (Note 3,3) und Business Intelligence (BIA, Note 2,7: Data Warehouse, Star-Schema, ETL, OLAP).', impact: 'Direkte Brücke zu modernen Reporting- und Analytics-Systemen wie SAP Analytics Cloud.' },
          { name: 'Profilseminar zum Human Resource Management', cat: 'Bachelor-Module (180 ECTS)', path: '03_Bachelor/Profilseminar zum Human Resource Management', desc: 'Wahlseminar (Note 3,0, 6 ECTS): Mensch-Roboter-Interaktion und wahrgenommene Servicequalität bei digitalen Service Encountern (Prof. Dr. Marion Büttgen, Uni Hohenheim).', impact: 'Erforscht die Schnittstelle von digitaler Interaktion, Akzeptanz und Servicemanagement.' },
          { name: 'Mensch-Computer-Interaktion', cat: 'Bachelor-Module (180 ECTS)', path: '03_Bachelor/Mensch-Computer-Interaktion', desc: 'Informatik-Wahlpflicht (Note 3,3, 6 ECTS): Usability Engineering, User Experience (UX), Gestaltungsrichtlinien, Prototyping und Evaluierungsmethoden.', impact: 'UX-Kompetenz – zentral für die Akzeptanz und Einführung moderner SAP Fiori UIs.' },
          { name: 'BWL 1 - Organisation, Personalführung, Strategisches Management', cat: 'Bachelor-Module (180 ECTS)', path: '03_Bachelor/BWL 1 - Organisation, Personalführung, Strategisches Management', desc: 'BWL-Pflichtmodul (Note 3,3, 9 ECTS): Strategische Unternehmensführung, Organisationsstrukturen, Change Management und Führungstheorien.', impact: 'Management-Wissen zur organisatorischen Verankerung von Transformationsprozessen.' },
          { name: 'Marketing Management', cat: 'Bachelor-Module (180 ECTS)', path: '03_Bachelor/Marketing Management', desc: 'BWL-Wahlpflicht (Note 3,3, 6 ECTS): Marktforschung, Marketing-Mix (4Ps), Kundenbindung und marktorientierte Unternehmensführung.', impact: 'Kunden- und marktorientiertes Denken für Produkt- und Servicepositionierung.' },
          { name: 'Wissensverarbeitung', cat: 'Bachelor-Module (180 ECTS)', path: '03_Bachelor/Wissensverarbeitung', desc: 'Modul (Note 3,7, 6 ECTS): Wissensrepräsentation, Ontologien, Expertensysteme, Wissensgraphen und logisches Schließen.', impact: 'Theoretische Grundlage für Wissensmanagement, semantische Netze und Knowledge Graphs.' },
          { name: 'Einführung in die Softwaretechnik', cat: 'Bachelor-Module (180 ECTS)', path: '03_Bachelor/Einführung in die Softwaretechnik', desc: 'Informatik-Pflichtmodul (Note 3,7, 6 ECTS): Softwarelebenszyklus, V-Modell, Entwurfsmuster (Design Patterns), UML und Testverfahren.', impact: 'Basiswissen über standardisierte Softwareentwicklungsmethoden und Qualitätssicherung.' },
          { name: 'Automaten und Formale Sprachen', cat: 'Bachelor-Module (180 ECTS)', path: '03_Bachelor/Automaten und Formale Sprachen', desc: 'Theoretische Informatik (Note 3,7, 6 ECTS): Endliche Automaten (DFA/NFA), reguläre Ausdrücke, kontextfreie Grammatiken, Chomsky-Hierarchie und Turingmaschinen.', impact: 'Höchste formale Abstraktionsfähigkeit und mathematische Denkdisziplin.' },
          { name: 'Informatikrecht', cat: 'Bachelor-Module (180 ECTS)', path: '03_Bachelor/Informatikrecht', desc: 'Rechtsmodul (Note 4,0, 3 ECTS): Urheberrecht, Softwarevertragsrecht, Datenschutzrecht (DSGVO), Haftung und Lizenzmodelle (Open Source vs Proprietary).', impact: 'Rechtssicherheit bei Softwarebeschaffung, Lizenz-Governance und DSGVO-Compliance.' },
          { name: 'Statistik I', cat: 'Bachelor-Module (180 ECTS)', path: '03_Bachelor/Statistik I', desc: 'Methodenmodul (Note 4,0, 6 ECTS): Deskriptive Statistik, Lage- und Streuungsmaße, Korrelations- und Regressionsanalyse sowie Indexzahlen.', impact: 'Basis-Statistik zur quantitativen Auswertung operativer Kennzahlen.' },
          { name: 'Mathematik für Wirtschaftswissenschaftler', cat: 'Bachelor-Module (180 ECTS)', path: '03_Bachelor/Mathematik für Wirtschaftswissenschaftler', desc: 'Höhere Mathematik (Note 4,0, 9 ECTS): Lineare Algebra, Matrizenrechnung, Differential- und Integralrechnung mehrerer Variablen und Optimierung unter Nebenbedingungen.', impact: 'Mathematisches Durchhaltevermögen und analytische Grundschulung.' },
          { name: 'Programmierung und Software-Entwicklung', cat: 'Bachelor-Module (180 ECTS)', path: '03_Bachelor/Programmierung und Software-Entwicklung', desc: 'Informatik-Großmodul (Note 4,0, 9 ECTS): Objektorientierte Programmierung (OOP) in Java, Vererbung, Polymorphie, Generics, Collections und Exception Handling.', impact: 'Grundlegendes Verständnis objektorientierter Programmiersprachen und Entwicklerlogik.' },
          { name: 'Management von Dienstleistungsunternehmen', cat: 'Bachelor-Module (180 ECTS)', path: '03_Bachelor/Management von Dienstleistungsunternehmen', desc: 'BWL-Modul (Note 4,0, 6 ECTS): Service Delivery, Kapazitäts- und Yield-Management, Dienstleistungsmarketing und Kundenkontaktpunkte.', impact: 'Branchenspezifisches Dienstleistungsverständnis – hochrelevant für ÖPNV und Verkehrsunternehmen.' },
          { name: 'Schreibwerkstatt: Vom studentischen zum beruflichen Schreiben', cat: 'Bachelor-Module (180 ECTS)', path: '03_Bachelor/Schreibwerkstatt - Vom studentischen zum beruflichen Schreiben', desc: 'Schlüsselqualifikation (3 ECTS, Bestanden): Wissenschaftliches Formulieren, Strukturierung von Fachpublikationen, Exzerpte und berufliche Textsorten.', impact: 'Souveräne schriftliche Ausdrucksstärke und Dokumentationskompetenz.' },

          // --- Neu kuratierte SSB Kern-Deliverables aus Tiefenanalyse ---
          { name: 'Workshops SSB.docx', cat: 'Explore & Lösungsdesign', path: '01_SSB/03_Fachstreams_Prozessdesign/Stream_MM_Materialwirtschaft/Explore_Phase_MM', desc: 'Spezifikation der Beschaffungsworkshops 1-3: 1XF Preisanfragen, BMD Rahmenverträge, BMR Lieferpläne, J45 Lagermaterial, BMY Lohnbearbeitung.', impact: 'Beweist operatives und strategisches MM-Prozesswissen im kommunalen Sektorenumfeld.' },
          { name: 'SolutionDesign_WorXX_MGe_310725.xlsx', cat: 'Explore & Lösungsdesign', path: '01_SSB/04_Architektur_Methoden_Tools/Datenmigration_LTMC', desc: 'Detailkonzept von Lösungsarchitekt Michael Gehrung zur Migration von Liegenschaften, Gebäuden (VIBDBU), Grundstücken (VIBDPR) und Verträgen (VICNCN).', impact: 'Zeigt tiefes Know-how in RE-FX Liegenschaftsstrukturen, Erbbaurechten und Schnittstellen zur Anlagenbuchhaltung.' },
          { name: 'CustomCode.xlsx', cat: 'Basis & Infrastruktur', path: '01_SSB/04_Architektur_Methoden_Tools/SAP_Readiness_Check_Clean_Core', desc: 'SAP Readiness Check 2.0 Detailreport: 166 Simplification Notes (ME21/ME51, MB-Transaktionen, KONV zu PRCD_ELEMENTS, MATDOC, BCS im Public Sector).', impact: 'Technischer Nachweis für Clean-Core-Governance und Custom Code Remediation.' },
          { name: '092025_SAP4SSB-Überblick_Regeltermin_BR_v1.pptx', cat: 'PMO & Steuerung', path: '01_SSB/02_Teilprojekte_TP1_bis_TP5/TP5_Gesamtsteuerung_Architektur/General/Betriebsrat', desc: 'Regeltermin-Abstimmung mit Betriebsrat Markus Schmidt & Joachim Kraus: Meilensteine Pilot-BV (01.04.2026) und Finale BV (01.01.2027).', impact: 'Beweist Verständnis für institutionalisierte Mitbestimmung und § 87 Abs. 1 Nr. 6 BetrVG in Großprojekten.' },
          { name: 'Entwurf_Modulbeschreibung_SAP_S4HANA.docx', cat: 'PMO & Steuerung', path: '01_SSB/01_Gesamtprojekt_SAP4SSB_Governance/01_Projektleitung_PMO_Masterplan/Projektleiter_Ordner', desc: 'Offizielle Vorlage für den Betriebsrat zur Datenverarbeitung aller S/4HANA Module (FI, CO, SD, MM, PM, EHS, Treasury) mit DSGVO-Schutzmaßnahmen.', impact: 'Demonstriert Datenschutz- und Mitbestimmungs-Governance auf C-Level-Niveau.' },
          { name: 'Aufstellung der Abwicklung von Fahrausweisverkäufen über das System PATRIS in SAP und deren Abstimmung.pdf', cat: 'Vertrieb & PATRIS', path: '01_SSB/03_Fachstreams_Prozessdesign/Stream_SD_Vertrieb_PATRIS/DDA Workshops', desc: 'Detailaufstellung zur Anbindung des Vertriebssystems PATRIS: Automatische Debitoreneinzüge, Fahrausweisverkäufe und VVS-Erlösausgleiche.', impact: 'Beweist Schnittstellenkompetenz bei der Entkopplung proprietärer ÖPNV-Vertriebssysteme ins S/4HANA Hauptbuch.' },
          { name: '20260420_GM_Entwurf_Fachkonzept_Fördermittelmanagement_12.docx', cat: 'Grants Management', path: '01_SSB/03_Fachstreams_Prozessdesign/Stream_Grants_Management_GM/_Fachkonzept_Fördermittelmanagement', desc: 'Fachkonzept Fördermittelmanagement (GM for Grantee): Abbildung von Drittmitteln, LGVFG/GVFG Bundes- und Landeszuschüssen.', impact: 'Zeigt tiefes Know-how in komplexen Spezialmodulen der öffentlichen Hand und Verwendungsnachweisführung.' },
          { name: '20251006_GM_Entwurf_Ableitungskonzept_Fördermittelmanagement.docx', cat: 'Grants Management', path: '01_SSB/03_Fachstreams_Prozessdesign/Stream_Grants_Management_GM/_Ableitungskonzept_Fördermittelmanagement', desc: 'Ableitungsregeln für Zuschüsse: Zuordnung von Sachkonten, Kostenstellen und PSP-Elementen auf spezifische Förderfonds.', impact: 'Beleg für fundiertes Ableitungs- und Kontierungsdesign im Public Sector.' },
          { name: 'PSP vs Innenauftrag.docx', cat: 'Finance & Controlling', path: '01_SSB/03_Fachstreams_Prozessdesign/Stream_CO_Controlling', desc: 'Architektur-Entscheidungsvorlage: Abgrenzung von mehrjährigen Investitionsprojekten (PSP-Elemente) vs. operativer Werkstattinstandhaltung (Innenaufträge).', impact: 'Zeigt deine Kernkompetenz im strategischen Kostenstellen- und Projekt-Controlling.' },
          { name: 'AfA-Simulation_Makro_und_Daten_20250626.xlsm', cat: 'Finance & Controlling', path: '01_SSB/03_Fachstreams_Prozessdesign/Stream_CO_Controlling', desc: 'Simulationsmodell für Anlagenabschreibungen (AfA) im Parallel-Ledger (HGB vs. Steuerrecht) über 30 Jahre Nutzungsdauer.', impact: 'Beweis für quantitative Finanzmodellierung und Anlagenbuchhaltungs-Expertise.' },
          { name: 'Gefahrstoffverzeichnis.pdf', cat: 'Sustainability & EHS', path: '01_SSB/03_Fachstreams_Prozessdesign/Stream_Sustainability_EHS/Workshop 2025.04.30', desc: 'Vollständiges Gefahrstoffkataster der Werkstätten nach EMKG-Standard inkl. Schutzstufen und Lagerklassen.', impact: 'Demonstriert fundierte Praxiserfahrung in integriertem Arbeitsschutz und Umweltmanagement.' },
          { name: 'EMKG.xlsm', cat: 'Sustainability & EHS', path: '01_SSB/03_Fachstreams_Prozessdesign/Stream_Sustainability_EHS/Gefahrgut', desc: 'Einfaches Maßnahmenkonzept Gefahrstoffe (BAuA Standard) zur automatisierten Einstufung von Chemikalien in S/4HANA.', impact: 'EHS-Kompetenz und Verknüpfung von operativer Werkstattrisikoanalyse mit ERP-Daten.' },
          { name: '20250617Vergabe_Zeitplan_Realize_bis_Run.pdf', cat: 'Vergabe & SektVO', path: '01_SSB/01_Gesamtprojekt_SAP4SSB_Governance/04_Ausschreibung_Vergabe_SektVO/Vergabe_Realize_Deploy_Run', desc: 'Gesamtablauf des EU-weiten SektVO-Vergabeverfahrens zur Auswahl des Generalübernehmers für die Realisierungs- und Betriebsphase.', impact: 'Beweist Vergaberecht- und Ausschreibungskompetenz in Milliarden-Infrastrukturunternehmen.' },
          { name: 'Bewertungsmatrix Teilnahmewettbewerb.xlsx', cat: 'Vergabe & SektVO', path: '01_SSB/01_Gesamtprojekt_SAP4SSB_Governance/04_Ausschreibung_Vergabe_SektVO/Vergabe_Realize_Deploy_Run', desc: 'Quantitative Bewertungsmatrix für den Teilnahmewettbewerb mit Gewichtung von Referenzen, Methodenkompetenz und Preis.', impact: 'Zeigt objektive Partnerbewertung und Vendor-Governance auf C-Level-Niveau.' },
          { name: 'AngebotsauswertungGrundsatzkonzeptionKTW_Murseli.xlsx', cat: 'PMO & Steuerung', path: '01_SSB/02_Teilprojekte_TP1_bis_TP5/TP3_Technische_Prozesse_Instandhaltung/Kusevic_Wimpff_Instandhaltung/Kusevic-Wimpff', desc: 'Von Visar Murseli erstellte Angebotsauswertung der Beraterangebote von Evora IT, Nagarro und Orianda für die Instandhaltung K/T/W.', impact: 'Echtes persönliches Arbeitsergebnis im PMO: Vendor Selection, Kostenvergleich und Entscheidungsvorbereitung.' },
          { name: 'apsolut_SSB_ID3758_V1.0_Workshopreihe_SAP_Ariba_20251125_signed.pdf', cat: 'Vergabe & SektVO', path: '01_SSB/03_Fachstreams_Prozessdesign/Stream_MM_Materialwirtschaft/Ariba_Fieldglass', desc: 'Vertrag und Workshopreihe zur Evaluierung von SAP Ariba (indirekte Beschaffung) und Fieldglass (Dienstleister-Steuerung).', impact: 'Belegt Einblicke in moderne Cloud-Procurement- und Workforce-Management-Lösungen.' },
          { name: 'SAP4SSB_Projektplan.mpp', cat: 'PMO & Steuerung', path: '01_SSB/01_Gesamtprojekt_SAP4SSB_Governance/01_Projektleitung_PMO_Masterplan/Projektplaene_MS_Project/Projektplan', desc: 'Offizieller Master-Projektplan in MS Project (WBS 1–297) mit allen Phasen, Vorgängen, Ressourcen und Meilensteinen.', impact: 'Das Herzstück deiner PMO-Tätigkeit: Beherrschung von Multiprojekt-Steuerung und Critical Path.' },
          { name: 'SSB Nutzerhandbuch SAP Signavio.pdf', cat: 'Tools & Enablement', path: '01_SSB/04_Architektur_Methoden_Tools/SAP_Signavio_Process_Manager/Signavio TP2 Dolde', desc: 'Offizielles Handbuch für Prozessmodellierer bei der SSB: Governance, Freigabe-Workflows und Signavio Collaboration Hub.', impact: 'Beweist Tool-Governance und Befähigung von Fachbereichen zur eigenständigen BPMN 2.0 Modellierung.' },
          { name: 'OnePager Modellierungsregeln.pdf', cat: 'Tools & Enablement', path: '01_SSB/04_Architektur_Methoden_Tools/SAP_Signavio_Process_Manager/Signavio TP2 Dolde', desc: 'Kompakter Standard für BPMN 2.0 Syntax, Naming Conventions und Lane-Zuordnungen für alle 5 Teilprojekte.', impact: 'Zeigt deinen Fokus auf strikte Standardisierung und Qualitätskontrolle.' },
          { name: 'DDA Export - Stuttgarter Straßenbahnen AG (SSB).xlsx', cat: 'Explore & Lösungsdesign', path: '01_SSB/02_Teilprojekte_TP1_bis_TP5/TP2_Kaufmaennische_Prozesse/General/Discover Phase/DDA Results/DDA all info/Excel/Archiv', desc: 'Vollständiger Scope-Katalog aus dem Digital Discovery Assessment mit Zuordnung zu Best Practice Scope-IDs.', impact: 'Belegt, dass du von Phase 0 an den Scope-Umfang für 3.700 Mitarbeiter im Detail überblickst.' },
          { name: 'Arten von personenbezogenen Daten in SAP S4HANA.pdf', cat: 'Explore & Lösungsdesign', path: '01_SSB/02_Teilprojekte_TP1_bis_TP5/TP2_Kaufmaennische_Prozesse/Explore_Phase_Desktop', desc: 'Datenschutz- und Compliance-Klassifizierung für Mitarbeiter- und Kundendaten im S/4HANA System.', impact: 'Zeigt DSGVO- und Mitbestimmungs-Kompetenz im sensiblen Umgang mit Personaldaten.' },
          { name: 'SSB_Kontengruppen_Konzept_20250829.xlsx', cat: 'Datenmigration', path: '01_SSB/03_Fachstreams_Prozessdesign/Stream_Cross_Topics_Integration/Geschäftspartner', desc: 'Definition der Kontengruppen für Business Partner (Debitoren, Kreditoren, Personal, Verbundunternehmen) und Nummernkreise.', impact: 'Technisches Detailwissen zur Stammdaten-Harmonisierung und CVI.' },
          { name: 'SSB Datenströme SAP.pdf', cat: 'Explore & Lösungsdesign', path: '01_SSB/03_Fachstreams_Prozessdesign/Stream_Cross_Topics_Integration', desc: 'Gesamtübersicht der konzernweiten Datenflüsse zwischen SAP Core, BTP, Archiv (d.velop), PATRIS und Werkstattsystemen.', impact: 'Echter Enterprise-Architecture-Plan: End-to-End Datenfluss-Verständnis im ÖPNV.' },
          { name: '20250708_LA_SAP4SSBV1.pptx', cat: 'PMO & Steuerung', path: '01_SSB/01_Gesamtprojekt_SAP4SSB_Governance/02_Steering_Board_Lenkungsausschuss/Lenkungsausschuss', desc: 'Offizielle Lenkungsausschuss-Präsentation für den Vorstand und IT-Leitung mit Statusampeln und Risiko-Matrix.', impact: 'Belegt deine direkte Zuarbeit für C-Level-Gremien und Vorstandsentscheidungen.' },
          { name: '20250225_Steering_Board.pptx', cat: 'PMO & Steuerung', path: '01_SSB/01_Gesamtprojekt_SAP4SSB_Governance/02_Steering_Board_Lenkungsausschuss/Steering_Board', desc: 'Entscheidungs- und Statusvorlage des Steering Boards zur Budget- und Ressourcenallokation.', impact: 'Beweis für strukturierte Vorbereitung strategischer Management-Entscheidungen.' },

          { name: 'SSB Executive Summary Discover Phase.docx', cat: 'Explore & Lösungsdesign', path: '01_SSB/02_Teilprojekte_TP1_bis_TP5/TP2_Kaufmaennische_Prozesse/General/Discover Phase', desc: 'Ergebnisbericht des Digital Discovery Assessments (DDA) mit Nagarro ES GmbH. Definition des S/4HANA Greenfield Scopes.', impact: 'Beweist, dass du die Phase 0 (DDA Scoping) von Grund auf verstanden hast.' },
          { name: 'SSB Lösungsdesign Dokument.docx', cat: 'Explore & Lösungsdesign', path: '01_SSB/02_Teilprojekte_TP1_bis_TP5/TP2_Kaufmaennische_Prozesse/Solution_Design_Dokumente', desc: '82.000 Zeichen starkes Architektur- und Lösungsdesigndokument für TP2 (Kaufmännische Prozesse: FI, CO, MM, RE-FX, Grants Mgmt).', impact: 'Zeigt dein tiefes Verständnis für die Gesamtarchitektur, Clean Core und WRICEFA-Objekte.' },
          { name: 'Migrationskonzept v0 1 2025_04_28.docx', cat: 'Datenmigration', path: '01_SSB/04_Architektur_Methoden_Tools/Datenmigration_LTMC', desc: 'Detailkonzept von Nagarro zur Datenmigration. Definition von Staging-Tabellen, Mapping-Regeln, Bilanzabgleich und Cutover.', impact: 'Dein Beleg für fundierte Datenmigrations- und Schnittstellenkompetenz.' },
          { name: 'SSB_Migrationsobjekte_Vorschlag.xlsx', cat: 'Datenmigration', path: '01_SSB/04_Architektur_Methoden_Tools/Datenmigration_LTMC', desc: 'Strukturierte Übersicht aller Migrationsobjekte nach Geschäftsobjekttyp, Methode (Staging vs Direct) und Custom Fields.', impact: 'Zeigt, dass du konkrete Datenobjekte (Business Partner, FI-AA, Kostenstellen) im Detail kennst.' },
          { name: '20251107_SAP_CALM_How2handle_quickguide.docx', cat: 'Tools & Enablement', path: '01_SSB/04_Architektur_Methoden_Tools/SAP_Cloud_ALM', desc: 'Von Visar verfasster Quickguide zur Nutzung von SAP Cloud ALM für Projekt-Setup, Quality Gates und Fit-to-Standard Tracking.', impact: 'Echtes Artefakt deiner Tool-Governance-Leistung. Unbedingt im Vorstellungsgespräch erwähnen!' },
          { name: 'SAP Enable Now Übergabe.docx', cat: 'Tools & Enablement', path: '01_SSB/04_Architektur_Methoden_Tools/SAP_Enable_Now', desc: 'Strategisches Übergabekonzept von UB I (IT) an UB AC (Personalentwicklung) zur Etablierung der Single-Source-Content-Strategie.', impact: 'Beweist deine Fähigkeit zur strategischen Schnittstellenkommunikation zwischen IT und HR.' },
          { name: 'TP5_Projektsteckbrief.docx', cat: 'PMO & Steuerung', path: '01_SSB/02_Teilprojekte_TP1_bis_TP5/TP5_Gesamtsteuerung_Architektur/TP5_Desktop', desc: 'Offizieller Projektauftrag für TP5 unter Roland Nowak: Steuerung von Budget, Ressourcen, Architektur, Vergabe und Berechtigungen.', impact: 'Dokumentiert dein organisatorisches "Zuhause" im Projektmanagement Office.' },
          { name: '20250922_Projektplan_GAP_Axians_Gerdes.xlsx', cat: 'PMO & Steuerung', path: '01_SSB/02_Teilprojekte_TP1_bis_TP5/TP4_IT_Infrastruktur_RISE_Basis/Axians_GAP_Tracking', desc: 'Trackingliste der technischen Basis-ToDos mit Axians (ES4 System, ADS Formulare, SSO, Transportkonsolidierung).', impact: 'Zeigt deine Hands-on Rolle bei der Steuerung technischer Infrastrukturpartner.' },
          { name: '20260211_Themensammlung_Priorisierung.xlsx', cat: 'PMO & Steuerung', path: '01_SSB/02_Teilprojekte_TP1_bis_TP5/TP4_IT_Infrastruktur_RISE_Basis/General', desc: 'Priorisierungsmatrix mit CalmIDs, T-Shirt-Sizes und Zuweisungen für anstehende S/4-Releases.', impact: 'Beweis für agile Aufwandsschätzung und Releasesteuerung.' },
          { name: 'Masterzeugnis_Murseli_Visar.pdf', cat: 'Wissenschaft & Uni', path: 'Studium_Dokumente', desc: 'Offizielles Zeugnis über die Masterprüfung der Universität Stuttgart (17. September 2026, 120 ECTS, Gesamtnote "gut" 1,6).', impact: 'Amtlicher Vollnachweis deines M.Sc. Abschlusses, der Masterarbeit (1,0) und aller 15 Fachprüfungen.' },
          { name: 'Masterarbeit_Visar_Murseli.pdf', cat: 'Wissenschaft & Uni', path: 'Studium_Dokumente', desc: 'Masterarbeit (126 Seiten, Note 1,0 bei Prof. Herzwurm, Uni Stuttgart) über Kritische Erfolgsfaktoren der S/4HANA Plattformisierung.', impact: 'Dein akademisches Meisterstück – belegt deine methodische Spitzenklasse!' },
          { name: 'DigitaleNachhaltigkeit_Ausarbeitung_Schmalz.docx', cat: 'Wissenschaft & Uni', path: 'Studium_Dokumente', desc: 'Wissenschaftliche Ausarbeitung (Note 1,0, 6 ECTS): Nachhaltigkeit durch Automatisierung: Eine Fallstudie zur Optimierung der Abfallbilanz bei der Schmalz GmbH (Dr. Dimitri Petrik).', impact: 'Beweist Green-IT-, BPMN- und CSRD/ESG-Expertise direkt am Weltmarktführer J. Schmalz GmbH.' },
          { name: 'CloudComputing_Kurzpaper_Murseli.pdf', cat: 'Wissenschaft & Uni', path: 'Studium_Dokumente', desc: 'Wissenschaftliches Kurzpaper (12 Seiten): Entwicklung einer Cloud-basierten Plattformarchitektur für einen wachsenden Onlineshop (AWS Well-Architected Framework).', impact: 'Zeigt tiefes Know-how in Cloud-Architekturen: Microservices, DynamoDB, Step Functions, QuickSight, EventBridge.' },
          { name: 'ISG_PatentRadar_Pitch.pdf', cat: 'Wissenschaft & Uni', path: 'Studium_Dokumente', desc: 'Pitch-Deck & Geschäftsmodell-Konzept: PatentRadar – Digital Venture für Klingele Paper & Packaging (Prof. Dr. Georg Herzwurm).', impact: 'Demonstriert fundierte Expertise in digitaler Geschäftsmodell-Innovation, BPMN 2.0-Prozessmodellierung und Venture-Pitching für Industrieunternehmen.' },
          { name: 'FPWI_Forschungsprojekt_Paper.pdf', cat: 'Wissenschaft & Uni', path: 'Studium_Dokumente', desc: 'Forschungspapier (Note 1,3, 6 ECTS): Integration physischer und digitaler Welten: Ein Framework für Smart Service Blueprinting (DSRM Peffers, SUS-Score 85/100).', impact: 'Beweist Methodenkompetenz in Design Science Research, IoT-Architekturen & Smart Services.' },
          { name: 'Seminararbeit_Murseli.pdf', cat: 'Wissenschaft & Uni', path: 'Studium_Dokumente', desc: 'Systematische Literaturanalyse (SLR nach PRISMA 2020, 26 Studien): Die Transformation menschlicher Arbeitsrollen durch KI-gestützte Mensch-Roboter-Kollaboration in der Produktion.', impact: 'Beweist rigorose wissenschaftliche Recherche, Industrie 5.0, Cobots & Human-AI-Kollaboration.' },
          { name: 'Leistungsnachweis_Master_SS25.pdf', cat: 'Wissenschaft & Uni', path: 'Studium_Dokumente', desc: 'Offizieller Master-Leistungsnachweis Universität Stuttgart (M.Sc. Wirtschaftsinformatik, Gesamtnote 1,6).', impact: 'Amtlicher Nachweis deiner Noten: Digitale Nachhaltigkeit 1,0, FPWI 1,3, Applied AI 1,7, Innovationsmanagement 1,7, etc.' },
          { name: 'Notenrechner_Master.xlsx', cat: 'Wissenschaft & Uni', path: 'Studium_Dokumente', desc: 'Detaillierter ECTS- und Notenrechner für das M.Sc. Studium an der Universität Stuttgart.', impact: 'Strukturierte Übersicht aller 120 ECTS Leistungspunkte.' },
          { name: 'Bachelorarbeit_Murseli.pdf', cat: 'Wissenschaft & Uni', path: 'Studium_Dokumente', desc: 'Bachelorarbeit (Note 1,7, Uni Stuttgart): Die Bedeutung von Boundary Resources in Low-Code Entwicklungsplattformen (OutSystems & Mendix).', impact: 'Beweist deinen kontinuierlichen Forschungsschwerpunkt auf Plattformen und Schnittstellen seit 2023.' },
          { name: 'Bachelorarbeit_Zusammenfassung.pdf', cat: 'Wissenschaft & Uni', path: 'Studium_Dokumente', desc: 'Executive Summary der Bachelorarbeit: 14 Boundary-Resource-Klassen bei OutSystems & Mendix.', impact: 'Kompakte 2-Seiten-Zusammenfassung für Recruiter und Fachinterviewer.' },
          { name: 'BA_Praesentation_Murseli.pptx', cat: 'Wissenschaft & Uni', path: 'Studium_Dokumente', desc: 'Offizielle Abschlusspräsentation der Bachelorarbeit bei Prof. Dr. Georg Herzwurm: Boundary Resources in Low-Code Plattformen.', impact: 'Beweist Präsentationssicherheit und fundierte Verteidigung von Architekturthemen.' },
          { name: 'Bachelorseminar_Buettgen_Murseli.pdf', cat: 'Wissenschaft & Uni', path: 'Studium_Dokumente', desc: 'Wissenschaftliche Seminararbeit (Prof. Dr. Marion Büttgen): Mensch-Roboter-Interaktion, Service Encounter und Expectation-Confirmation-Modell.', impact: 'Zeigt deine kontinuierliche Forschung zu Mensch-Technik-Interaktion und Servicequalität.' },
          { name: 'IVP_Unternehmensanalyse_0x539Wear.docx', cat: 'Wissenschaft & Uni', path: 'Studium_Dokumente', desc: 'Umfangreiche Unternehmensanalyse der 0x539-Wear GmbH: Bestellungs-, Plan-Ist-, Kunden-, Artikel- und Lieferantenanalyse.', impact: 'Praktischer Nachweis deiner BI- und Supply-Chain-Datenanalysekompetenz.' },
          { name: 'Modulhandbuch_BSc_Wirtschaftsinformatik.pdf', cat: 'Wissenschaft & Uni', path: 'Studium_Dokumente', desc: 'Offizielles Modulhandbuch der Universität Stuttgart: Detaillierte Kompetenz- und Modulbeschreibungen aller 180 ECTS.', impact: 'Referenzdokument für alle universitären Lernziele.' },
          { name: 'Togaf_Zertifikat.pdf', cat: 'Wissenschaft & Uni', path: 'Studium_Dokumente', desc: 'Offizielle Teilnahmebescheinigung TOGAF 9 ADM-Intensivkurs an der Universität Stuttgart (Dr. Daniel Simon, Scape Consulting GmbH, 16.01.2020).', impact: 'Amtlicher Beleg deiner Enterprise Architecture Management (EAM) Methodik nach TOGAF ADM.' },
          { name: 'Arbeitsbescheinigung_Daimler.pdf', cat: 'PMO & Steuerung', path: 'Studium_Dokumente', desc: 'Arbeitsbescheinigung Daimler AG (Standort Untertürkheim): Praktische Industrie- und Fertigungserfahrung.', impact: 'Belegt frühe Praxiserfahrung in einem DAX-Automobilkonzern.' },
          { name: 'Arbeitszeugnis_OTLG.jpeg', cat: 'PMO & Steuerung', path: 'Studium_Dokumente', desc: 'Arbeitszeugnis Volkswagen Original Teile Logistik (OTLG): Teiledistribution und Materialflussprozesse.', impact: 'Beweist operative Logistik- und Prozessdisziplin.' },
          { name: 'Abiturzeugnis_Murseli.pdf', cat: 'Wissenschaft & Uni', path: 'Studium_Dokumente', desc: 'Offizielles Abiturzeugnis (Allgemeine Hochschulreife, Baden-Württemberg).', impact: 'Vollständiger lückenloser Bildungsnachweis von der Schule bis zum Master.' },
          { name: 'Ehrenamtliche_Gefluechtetenhilfe.pdf', cat: 'PMO & Steuerung', path: 'Studium_Dokumente', desc: 'Bestätigung über ehrenamtliche Geflüchtetenhilfe (Refugees Welcome, HVF) und Hausaufgabenbetreuung.', impact: 'Unterstreicht soziale Verantwortung, Empathie und Führungskompetenz.' },
          { name: 'Bachelorzeugnis_Leistungsuebersicht_Murseli.pdf', cat: 'Wissenschaft & Uni', path: 'Studium_Dokumente', desc: 'Amtliche Leistungsübersicht B.Sc. Wirtschaftsinformatik (180 ECTS, Universität Stuttgart, Bestnote 1,0 in E-Business Informationssysteme).', impact: 'Belegt dein starkes informationstechnisches und betriebswirtschaftliches Fundament.' },
          { name: 'Bachelorurkunde_Murseli.pdf', cat: 'Wissenschaft & Uni', path: 'Studium_Dokumente', desc: 'Offizielle Verleihungsurkunde des akademischen Grades Bachelor of Science durch die Universität Stuttgart.', impact: 'Formaler Nachweis deines ersten berufsqualifizierenden Hochschulabschlusses.' },
          { name: 'Codebuch_Masterarbeit_Mayring.xlsx', cat: 'Wissenschaft & Uni', path: 'Studium_Dokumente', desc: 'Wissenschaftliches Mayring-Codebuch zur qualitativen Inhaltsanalyse der 12 empirischen Experteninterviews.', impact: 'Beweist höchste empirische Forschungsmethodik und qualitative Datenanalysekompetenz.' },
          { name: 'Interview_Roland_Nowak_Gesamt_PL.docx', cat: 'Explore & Lösungsdesign', path: 'Studium_Dokumente/Interviews_Masterarbeit', desc: 'Vollständiges Experteninterview-Transkript mit Roland Nowak (Gesamtprojektleiter SAP4SSB).', impact: 'Echter Primärbeleg für dein tiefes Verständnis der Management- und Architekturperspektive.' },
          { name: 'Interview_Thomas_Wimpff_TP2_Leitung.docx', cat: 'Explore & Lösungsdesign', path: 'Studium_Dokumente/Interviews_Masterarbeit', desc: 'Experteninterview-Transkript mit Thomas Wimpff (Teilprojektleiter TP2 Finance & Controlling).', impact: 'Beweist dein Detailwissen über Trennungsrechnung, ACDOCA und kaufmännische Prozesse.' },
          { name: 'Interview_Armin_Heinrich_Basis_Architektur.docx', cat: 'PMO & Steuerung', path: 'Studium_Dokumente/Interviews_Masterarbeit', desc: 'Experteninterview-Transkript mit Armin Heinrich (Enterprise Architekt & Basis SSB).', impact: 'Belegt dein Verständnis für BTP-Zielarchitektur, SSO und Cloud-Infrastruktur.' },
          { name: 'Interview_Henning_Gerdes_Axians_Lead.docx', cat: 'PMO & Steuerung', path: 'Studium_Dokumente/Interviews_Masterarbeit', desc: 'Experteninterview-Transkript mit Henning Gerdes (Lead Architect Axians ES4).', impact: 'Dokumentiert deine Schnittstellenkompetenz bei der Steuerung technischer Basispartner.' },
          { name: 'Zeugnisse_Murseli_Visar.pdf', cat: 'PMO & Steuerung', path: 'Studium_Dokumente', desc: 'Offizielle Leistungsnachweise: M.Sc. Wirtschaftsinformatik 1,6, SSB Zwischenzeugnis (Fillinger/Nowak), Datacenter One, TOGAF.', impact: 'Lückenlose Verifikation aller deiner Erfolge und Top-Referenzen.' },

          // --- DATACENTER ONE (DC1) | ITIL 4 SERVICE OPERATIONS & INFRASTRUCTURE ---
          { name: 'HLM_v2.pdf', cat: 'Datacenter One (DC1 / ITIL 4)', path: '04_DC1/02_Projekte_und_Architektur/01_Hardware_Lifecycle_Management', desc: 'BPMN-Modellierung des Hardware-Lifecycle-Management-Prozesses bei Datacenter One (Beschaffung, Bereitstellung, Betrieb, Decommissioning).', impact: 'Beweist strukturierte Prozessmodellierung und IT-Asset-Management in hochverfügbaren Umgebungen.' },
          { name: 'Hardware_Lifecycle_Management.vsdx', cat: 'Datacenter One (DC1 / ITIL 4)', path: '04_DC1/02_Projekte_und_Architektur/01_Hardware_Lifecycle_Management', desc: 'Microsoft Visio Quelldatei des HLM-Prozessdesigns und der Schnittstellen zu Lieferanten und Leitstand.', impact: 'Zeigt Beherrschung von MS Visio und Enterprise Process Modeling.' },
          { name: 'Dell PoC und Fahrplan.xlsx', cat: 'Datacenter One (DC1 / ITIL 4)', path: '04_DC1/02_Projekte_und_Architektur/01_Hardware_Lifecycle_Management', desc: 'Proof of Concept und detaillierte Rollout- und Austauschplanung für Client-Hardware im laufenden Betrieb.', impact: 'Demonstriert analytische Projektplanung und Vendor-Evaluation.' },
          { name: 'Bericht_Notebookaustausch.pdf', cat: 'Datacenter One (DC1 / ITIL 4)', path: '04_DC1/02_Projekte_und_Architektur/01_Hardware_Lifecycle_Management', desc: 'Abschluss- und Erfahrungsbericht des Hardware-Rollouts im Rechenzentrumsumfeld.', impact: 'Belegt praktische Umsetzungserfahrung und Stakeholder-Kommunikation.' },
          { name: 'CM_ins_INOC_Projekt_VIM.docx', cat: 'Datacenter One (DC1 / ITIL 4)', path: '04_DC1/02_Projekte_und_Architektur/02_Carriermanagement_INOC', desc: 'Projektkonzeption zur Übernahme von Carrier-Management- und Netzanbindungsprozessen in den INOC-Leitstand.', impact: 'Zeigt Service-Transition und Prozessoptimierung nach ITIL 4.' },
          { name: 'Togaf_DC1.pptx', cat: 'Datacenter One (DC1 / ITIL 4)', path: '04_DC1/02_Projekte_und_Architektur/03_Enterprise_Architecture_TOGAF', desc: 'Architektur-Präsentation von Visar Murseli: Adaption von TOGAF 9 ADM im Rechenzentrumsbetrieb.', impact: 'Verbindet Visars TOGAF-Zertifizierung mit realer Unternehmenspraxis.' },
          { name: 'Review_Hausmeisterseite.docx', cat: 'Datacenter One (DC1 / ITIL 4)', path: '04_DC1/01_ITIL4_Service_Operations_INOC/02_Monitoring_und_SOPs', desc: 'SOP-Review und Audit der Betriebsleitfäden für PRTG-Monitoring, Leitungsausfälle und Paketverluste.', impact: 'Belegt 24/7 Monitoring-Kompetenz und strikte Prozessdisziplin.' }
        ];
        // PRIVATE_QA_FILES_END

        const filteredQA = computed(() => {
          let list = allQA;
          if (selectedQACat.value !== 'Alle') {
            list = list.filter(item => item.cat === selectedQACat.value);
          }
          const term = (qaSearch.value || searchQuery.value || '').trim().toLowerCase();
          if (term) {
            list = list.filter(item => 
              item.q.toLowerCase().includes(term) || 
              item.a.toLowerCase().includes(term) ||
              (item.cat && item.cat.toLowerCase().includes(term))
            );
          }
          return list;
        });

        const filteredFiles = computed(() => {
          let list = filesData;
          if (selectedFileCat.value !== 'Alle') {
            list = list.filter(item => item.cat === selectedFileCat.value);
          }
          if (searchQuery.value) {
            const q = searchQuery.value.toLowerCase();
            list = list.filter(item => 
              item.name.toLowerCase().includes(q) || 
              item.desc.toLowerCase().includes(q) || 
              item.impact.toLowerCase().includes(q)
            );
          }
          return list;
        });


        const filteredWbsProjects = computed(() => {
          if (wbsFilter.value === 'all') return wbsProjects.value;
          return wbsProjects.value.filter(p => p.id.toLowerCase() === wbsFilter.value.toLowerCase() || p.phase.toLowerCase() === wbsFilter.value.toLowerCase());
        });

        const commandFilteredResults = computed(() => {
          if (!commandSearch.value) return searchCatalog.slice(0, 8);
          const q = commandSearch.value.toLowerCase();
          return searchCatalog.filter(item => 
            item.title.toLowerCase().includes(q) || 
            item.desc.toLowerCase().includes(q) || 
            item.cat.toLowerCase().includes(q)
          );
        });

        const openCommandPalette = () => {
          isCommandPaletteOpen.value = true;
          commandSearch.value = '';
          setTimeout(() => {
            const el = document.getElementById('command-palette-input');
            if (el) el.focus();
          }, 50);
        };

        const closeCommandPalette = () => {
          isCommandPaletteOpen.value = false;
          commandSearch.value = '';
        };

        const selectCommandResult = (item) => {
          activeTab.value = item.tab;
          closeCommandPalette();
          window.scrollTo({ top: 0, behavior: 'smooth' });
        };

        const toggleDarkMode = () => {
          isDark.value = !isDark.value;
          if (isDark.value) {
            document.documentElement.classList.add('dark');
          } else {
            document.documentElement.classList.remove('dark');
          }
        };

        const copyText = (txt) => {
          navigator.clipboard.writeText(txt);
          alert('Text erfolgreich in die Zwischenablage kopiert!');
        };

        // Persistent Notes logic
        const saveNotes = () => {
          localStorage.setItem('vm_second_brain_notes', personalNotes.value);
        };

        // PRIVATE_RAG_START
        const saveNotesToObsidian = async () => {
          saveNotes();
          if (!['localhost', '127.0.0.1'].includes(window.location.hostname)) {
            ragStatusMsg.value = 'Obsidian Sync steht nur im lokalen Portal (localhost:8085) zur Verfügung.';
            return;
          }
          try {
            const resp = await fetch('/api/save-note', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({ notes: personalNotes.value })
            });
            const res = await resp.json();
            ragStatusMsg.value = res.ok ? '✅ Erfolgreich in Obsidian 00_Inbox/Webapp_Notizen.md gespeichert & in FTS5-RAG indexiert!' : ('⚠️ Fehler: ' + res.error);
          } catch (e) {
            ragStatusMsg.value = '⚠️ Lokaler Portal-Server unter localhost:8085 nicht erreichbar.';
          }
        };

        const runRagSearch = async () => {
          const q = (ragQuery.value || '').trim();
          if (!q) return;
          if (!['localhost', '127.0.0.1'].includes(window.location.hostname)) {
            ragStatusMsg.value = 'Local RAG steht nur auf localhost:8085 bereit.';
            return;
          }
          ragLoading.value = true;
          try {
            const resp = await fetch('/api/rag?limit=10&q=' + encodeURIComponent(q));
            const data = await resp.json();
            ragResults.value = data.results || [];
            ragStatusMsg.value = `${ragResults.value.length} gewichtete Hybrid-Treffer aus Obsidian FTS5 für "${q}" geladen.`;
          } catch (e) {
            ragStatusMsg.value = '⚠️ Fehler bei RAG-Anfrage.';
          } finally {
            ragLoading.value = false;
          }
        };

        const runRagAsk = async () => {
          const q = (ragQuery.value || '').trim();
          if (!q) return;
          if (!['localhost', '127.0.0.1'].includes(window.location.hostname)) {
            ragStatusMsg.value = 'KI-Synthese steht nur auf localhost:8085 bereit.';
            return;
          }
          ragAskLoading.value = true;
          try {
            const resp = await fetch('/api/ask?limit=6&q=' + encodeURIComponent(q));
            const data = await resp.json();
            ragAnswer.value = data.answer || '';
            ragModel.value = data.model || '';
            if (data.sources && data.sources.length) {
              const r2 = await fetch('/api/rag?limit=8&q=' + encodeURIComponent(q));
              const d2 = await r2.json();
              ragResults.value = d2.results || [];
            }
            ragStatusMsg.value = `🤖 Gemini-Synthese (${ragModel.value || 'local'}) auf Basis verifizierter Obsidian-Quellen erstellt.`;
          } catch (e) {
            ragStatusMsg.value = '⚠️ Fehler bei KI-Synthese.';
          } finally {
            ragAskLoading.value = false;
          }
        };

        const loadPipeline = async () => {
          if (!['localhost', '127.0.0.1'].includes(window.location.hostname)) return;
          try {
            const resp = await fetch('/api/pipeline');
            const data = await resp.json();
            if (data.ok) pipelineData.value = data;
          } catch (e) {}
        };

        const prepInterview = async (company, role) => {
          ragQuery.value = `${company} ${role} Masterarbeit SSB Projekt Transformation`;
          await runRagAsk();
        };
        // PRIVATE_RAG_END

        const copyNotesToClipboard = () => {
          if (navigator.clipboard) {
            navigator.clipboard.writeText(personalNotes.value);
          }
          alert('Notizen erfolgreich in die Zwischenablage kopiert! 📋');
        };
        const exportNotes = copyNotesToClipboard;

        const clearNotes = () => {
          if (confirm('Möchtest du deine Notizen wirklich leeren?')) {
            personalNotes.value = '';
            localStorage.removeItem('vm_second_brain_notes');
          }
        };

        const insertTemplate = (type) => {
          let tpl = '';
          const today = new Date().toLocaleDateString('de-DE');
          if (type === 'interview_log') {
            tpl = `\\n\\n### Interview-Protokoll (${today})\\n- **Unternehmen:** \\n- **Rolle:** \\n- **Interviewer (Name / Rolle):** \\n- **Gefragte Schwerpunkte:** \\n  1. \\n  2. \\n- **Angewandte Pivot-Strategie:** \\n- **Feedback & Next Steps:** \\n`;
          } else if (type === 'salary_target') {
            tpl = `\\n\\n### Gehaltsziel & Verhandlung (${today})\\n- **Zielrolle:** \\n- **Unternehmen / Tarif:** (z.B. IGM EG 14 / TVöD EG 12 / All-in)\\n- **Fixgehalt-Ziel:** €\\n- **Variabler Anteil / Bonus:** €\\n- **Verhandlungs-Obergrenze:** €\\n- **Schmerzgrenze:** €\\n- **Begründung (USP):** 24 Mo. SSB + 1,0 Masterarbeit Clean Core\\n`;
          } else if (type === 'daily_focus') {
            tpl = `\\n\\n### VISMUV Tagesfokus (${today})\\n- **Prio 1 (Must-Win):** \\n- **Prio 2 (Jobsuche / Vorbereitung):** \\n- **Fitness & Mindset:** Workout erledigt? Fokuszeit eingehalten?\\n- **Gelerntes des Tages:** \\n`;
          } else if (type === 'learning_cheat') {
            tpl = `\\n\\n### SAP / IT Architektur Notiz (${today})\\n- **Thema / Service:** (z.B. BTP Event Mesh / CDS Annotation)\\n- **Problemstellung:** \\n- **Lösung / Best Practice:** \\n- **Relevanz für Vorstellungsgespräche:** \\n`;
          }
          personalNotes.value += tpl;
          saveNotes();
        };

        onMounted(() => {
          window.addEventListener('keydown', (e) => {
            if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
              e.preventDefault();
              if (isCommandPaletteOpen.value) {
                closeCommandPalette();
              } else {
                openCommandPalette();
              }
            } else if (e.key === 'Escape' && isCommandPaletteOpen.value) {
              closeCommandPalette();
            }
          });

          const saved = localStorage.getItem('vm_second_brain_notes');
          if (saved) {
            personalNotes.value = saved;
          } else {
            personalNotes.value = `# Visar Murseli | Mein persönliches Second Brain\\n\\nWillkommen in deinem persönlichen Karriere-Notizbuch!\\nHier kannst du Notizen zu Vorstellungsgesprächen, Gehaltsverhandlungen und SAP-Architekturen festhalten.\\n\\nAlles, was du hier eintippst, wird automatisch in deinem Browser gespeichert.\\n`;
          }
          loadPipeline();
        });

        return {
          activeTab,
          isMobileMenuOpen,
          currentTabName,
          currentHubName,
          degreeTab,
          searchQuery,
          isDark,
          pitchMode,
          tabs,
          qaCategories,
          fileCategories,
          selectedQACat,
          qaSearch,
          selectedFileCat,
          personalNotes,
          ragQuery,
          ragResults,
          ragLoading,
          ragAskLoading,
          ragAnswer,
          ragModel,
          ragStatusMsg,
          pipelineData,
          runRagSearch,
          runRagAsk,
          loadPipeline,
          prepInterview,
          saveNotesToObsidian,
          pitch60,
          pitchDeep,
          starStories,
          defenseScenarios,
          cvImprovements,
          filteredQA,
          filteredFiles,
          toggleDarkMode,
          copyText,
          saveNotes,
          copyNotesToClipboard,
          exportNotes,
          clearNotes,
          insertTemplate,
          isCommandPaletteOpen,
          commandSearch,
          wbsFilter,
          wbsProjects,
          filteredWbsProjects,
          searchCatalog,
          commandFilteredResults,
          openCommandPalette,
          closeCommandPalette,
          selectCommandResult
        };
      }
    }).mount('#app');
  </script>
</body>
</html>
"""
    import re
    if public_mode:
        tpl = tpl.replace('%%PRIVATE_HUB_LINE%%', '')
        tpl = re.sub(r'// PRIVATE_TABS_START.*?// PRIVATE_TABS_END', '', tpl, flags=re.DOTALL)
        tpl = re.sub(r'// PRIVATE_RAG_START.*?// PRIVATE_RAG_END',
                     "const saveNotesToObsidian = () => {};\n        const runRagSearch = () => {};\n        const runRagAsk = () => {};\n        const loadPipeline = () => {};\n        const prepInterview = () => {};",
                     tpl, flags=re.DOTALL)
        tpl = re.sub(r'// PRIVATE_DEFENSE_START.*?// PRIVATE_DEFENSE_END',
                     "const defenseScenarios = ref([]);\n        const cvImprovements = [];\n        const pitch60 = '';\n        const pitchDeep = '';\n        const starStories = ref([]);",
                     tpl, flags=re.DOTALL)
        tpl = re.sub(r'// PRIVATE_CATALOG_START.*?// PRIVATE_CATALOG_END', '', tpl, flags=re.DOTALL)
        tpl = re.sub(r'// PRIVATE_QA_FILES_START.*?// PRIVATE_QA_FILES_END',
                     "const allQA = [];\n        const filesData = [];",
                     tpl, flags=re.DOTALL)
        tpl = tpl.replace('%%CAREER_BADGE%%', 'Einstieg & Roadmap')
    else:
        tpl = tpl.replace('%%PRIVATE_HUB_LINE%%', "if (['interview', 'cv_defense', 'files', 'notebook'].includes(tabId)) return 'Interview & Nachweise';")
        tpl = tpl.replace('%%CAREER_BADGE%%', '55k–75k €')
    return tpl
