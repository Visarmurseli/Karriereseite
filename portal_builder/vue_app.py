# -*- coding: utf-8 -*-

def get_vue_app():
    return """
    </main>

    <!-- Footer -->
    <footer class="bg-white dark:bg-slate-900 border-t border-slate-200 dark:border-slate-800 py-4 px-4 text-center text-xs text-slate-500">
      <div class="max-w-7xl mx-auto flex flex-col md:flex-row justify-between items-center gap-2">
        <span>Visar Murseli, M.Sc. | Enterprise Knowledge Hub & S/4HANA Career OS</span>
        <span>Entwickelt in Antigravity IDE | Version 2026.1 | Vollständig lokal & persistent</span>
      </div>
    </footer>
  </div>

  <!-- Application Logic & Data Injection -->
  <script>
    const { createApp, ref, computed, onMounted } = Vue;

    createApp({
      setup() {
        const activeTab = ref('dashboard');
        const searchQuery = ref('');
        const isDark = ref(false);
        const pitchMode = ref('short');
        const selectedQACat = ref('Alle');
        const selectedFileCat = ref('Alle');
        const personalNotes = ref('');

        const tabs = [
          { id: 'dashboard', label: 'Dashboard', icon: '📊', badge: '' },
          { id: 'cv_defense', label: 'CV De-Risking', icon: '🛡️', badge: 'Gefahrenabwehr', badgeColor: 'bg-red-500 text-white' },
          { id: 'project', label: 'Großprojekt SSB', icon: '🏛️', badge: 'TP1-5' },
          { id: 'solution_design', label: 'Solution Design', icon: '📐', badge: 'FI/CO' },
          { id: 'migration', label: 'Datenmigration', icon: '🔄', badge: 'LTMC' },
          { id: 'tools', label: 'Toolchain Hub', icon: '🛠️', badge: 'CALM/Signavio' },
          { id: 'thesis', label: 'Masterarbeit 1,0', icon: '🎓', badge: '30 ECTS', badgeColor: 'bg-emerald-600 text-white' },
          { id: 'enterprise_arch', label: 'EAM & ITIL', icon: '🏛️', badge: 'TOGAF' },
          { id: 'cheatsheet', label: 'Tech Cheatsheet', icon: '⚡', badge: 'BTP/SQL' },
          { id: 'career', label: 'Karriere & Gehalt', icon: '🚀', badge: '90 Tage' },
          { id: 'interview', label: 'Interview Masterclass', icon: '🎙️', badge: 'Pitches' },
          { id: 'files', label: 'Dokumenten-Vault', icon: '📂', badge: '50+ Files' },
          { id: 'notebook', label: 'Mein Second Brain', icon: '📝', badge: 'Autosave', badgeColor: 'bg-purple-600 text-white' }
        ];

        const qaCategories = ['Alle', 'Architektur & Clean Core', 'Datenmigration', 'Projektmanagement & Governance', 'Persönlich & Verhalten'];

        const fileCategories = ['Alle', 'PMO & Steuerung', 'Explore & Lösungsdesign', 'Datenmigration', 'Tools & Enablement', 'Wissenschaft & Uni'];

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
            question: '"Erzählen Sie uns von Ihrer RPA-Entwicklung mit UiPath bei Bosch. Wie haben Sie Queues und Fehlerbehandlung gebaut?"',
            badAnswer: '"Ich habe da Bots gebaut mit Activities..." – Der Interviewer fragt nach REFramework, Try-Catch-Blöcken oder Orchestrator-Triggern.',
            goodAnswer: `Bei Robert Bosch im Patentwesen lag mein strategischer Schwerpunkt auf der vorgelagerten Prozessanalyse und Machbarkeitsprüfung: 

Das Patentmanagement ist stark reguliert und papierlastig. Ich habe die Abläufe der Patentrecherche und Fristenüberwachung detailliert analysiert, Prozesskosten quantifiziert und bewertet, welche Teilprozesse sich wirtschaftlich für eine robotergestützte Automatisierung eignen und wo die Schnittstellenrisiken liegen.

Die anschließende technische Skript-Implementierung in UiPath haben dedizierte RPA-Entwickler übernommen. Meine Kernkompetenz war das Anforderungsmanagement, die Erstellung des Process Design Documents (PDD) und die Validierung der Testergebnisse.

Genau diese Fähigkeit – komplexe Geschäftsprozesse strukturiert zu zerlegen und auf IT-Machbarkeit zu prüfen – war anschließend auch bei der SSB der Schlüssel für meine Arbeit mit SAP Signavio und Cloud ALM.`,
            whyItWorks: 'Du positionierst dich als Business Analyst und Solution Designer, nicht als billiger Bot-Scripter. Das erhöht dein Ansehen sofort.',
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
            oldText: 'Automatisierung & UiPath (Robert Bosch)',
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

Genau diese Schnittstelle aus 24 Monaten Greenfield-Großprojekterfahrung und modernem Architekturwissen nach dem Clean-Core-Prinzip bringe ich mit. Heute suche ich eine Rolle, in der ich dieses Praxiswissen ab dem ersten Tag wertschöpfend in Ihr Team einbringen kann.`;

        const pitchDeep = `Wenn Sie mich nach meinem fachlichen Profil fragen, lässt sich das in drei Bausteinen zusammenfassen:

Erstens: Operative ERP-Großprojekterfahrung in einem kritischen Infrastrukturunternehmen. Die SSB AG mit 3.700 Mitarbeitern migriert von einem hochgradig modifizierten ECC 6.0 auf S/4HANA in einer RISE Private Cloud. Ich war im TP5 unter Gesamtprojektleiter Roland Nowak dafür zuständig, die Projektorganisation, das Meilenstein-Controlling und die Tool-Etablierung zu steuern. Ich kenne die realen Reibungspunkte – von der Schnittstellenintegration mit Drittsystemen wie xSuite, d.velop oder PATRIS bis hin zu den Vorbehalten des Betriebsrats bei Fiori-Rollen.

Zweitens: Fundierte Daten- und Migrationskompetenz. Ich habe mich intensiv mit den Mechanismen des SAP Migration Cockpits befasst – von der Validierung der Staging-Tabellen über Feld- und Werte-Mappings bis hin zum revisionssicheren Cutover und Bilanzabgleich im FI. Ich weiß genau, warum die Eröffnungsbilanz und das Übernahmekonto centgenau auf 0,00 € abgestimmt sein müssen und wie man Stammdaten im Rahmen von CVI sauber konsolidiert.

Drittens: Strategische Architektur- und Plattformkompetenz. Viele reden über 'Clean Core', verstehen aber die Konsequenzen nicht. In meiner Masterarbeit am Lehrstuhl von Prof. Herzwurm – die mit der Note 1,0 bewertet wurde – habe ich auf Basis von 12 Experteninterviews empirisch untersucht, welche Erfolgsfaktoren die Plattformisierung erfordert. Wer den Kern reinhalten will, muss Side-by-Side-Erweiterungen auf der SAP BTP beherrschen und APIs wie ein Produkt managen.

Ich bringe die seltene Kombination aus strategischem Weitblick, wissenschaftlicher Spitzenleistung und echter Hands-on-ERP-Erfahrung mit. Genau diesen Hebel möchte ich in Ihrem Team ansetzen.`;

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

        const allQA = [
          {
            q: 'Was genau war Ihre Rolle bei der SSB AG und was haben Sie konkret gemacht?',
            cat: 'Projektmanagement & Governance',
            open: true,
            a: `Ich war 24 Monate lang als Werkstudent im IT-PMO (Teilprojekt 5: Gesamtsteuerung & Architektur) unter Gesamtprojektleiter Roland Nowak tätig. Meine Hauptaufgabe war die operative Klammer zwischen den fünf Teilprojekten (Change, Finance, Instandhaltung, HR, IT-PMO) und unseren Implementierungspartnern Nagarro, Evora und Axians.\n\nKonkret habe ich die Tool-Governance verantwortet: Ich habe den verbindlichen Quickguide für SAP Cloud ALM verfasst, die Verknüpfung von Signavio-Prozessmodellen mit Testfällen koordiniert und das strategische Übergabekonzept von SAP Enable Now an die Personalentwicklung ausgearbeitet. Außerdem habe ich die Migrationskataloge analysiert und das Meilenstein-Tracking für den Lenkungsausschuss vorbereitet.`,
            do: 'Betone die 24 Monate Laufzeit, die Schnittstellenrolle und deine konkreten Artefakte (CALM Guide, Enable Now Konzept).',
            dont: 'Stelle dich nicht als bloßer Protokollant dar – du hast Governance-Vorgaben aktiv erarbeitet!'
          },
          {
            q: 'Warum hat sich die SSB für Greenfield und nicht für eine Systemkonvertierung (Brownfield) entschieden?',
            cat: 'Architektur & Clean Core',
            open: false,
            a: `Das bestehende SAP ECC 6.0 der SSB war über 20 Jahre historisch gewachsen und wies tausende Z-Modifikationen, ungenutzte Altdaten und veraltete Berechtigungsstrukturen auf. Ein Brownfield-Ansatz hätte diese technische Schuld 1:1 in die neue Welt mitgeschleift und zukünftige Cloud-Upgrades massiv erschwert.\n\nMit dem Greenfield-Ansatz in einer RISE with SAP Private Cloud Edition konnte die SSB tabula rasa machen: Rückkehr zum Best-Practice-Standard durch Fit-to-Standard Workshops, Bereinigung der Stammdaten (CVI) und strikte Einhaltung des Clean-Core-Paradigmas.`,
            do: 'Verwende Fachbegriffe: Technische Schuld, Modifikationsfreier Kern, Fit-to-Standard, Best-Practice-Standard.',
            dont: 'Sage nicht einfach: "Brownfield war zu alt." Begründe es mit Upgrade-Sicherheit und Wartungskosten.'
          },
          {
            q: 'Was bedeutet Clean Core für Sie in der Praxis und wie verhindert man Wildwuchs?',
            cat: 'Architektur & Clean Core',
            open: false,
            a: `Clean Core bedeutet, dass der ERP-Kern frei von Modifikationen bleibt und ausschließlich über stabile, freigegebene Schnittstellen (APIs und CDS Views) angesprochen wird. Dadurch bleibt das System jederzeit upgradefähig, was in Cloud-Releases essenziell ist.\n\nIn der Praxis teilt sich das auf:\n1. On-Stack Extensibility: Erweiterungen im Kern erfolgen nur über ABAP Cloud und das RESTful Application Programming Model (RAP).\n2. Side-by-Side Extensibility: Komplexe Eigenentwicklungen, Fiori-Frontends und Drittsystem-Integrationen laufen auf der SAP BTP.\n\nUm Wildwuchs zu verhindern, braucht es eine strikte Governance: Jede Z-Anforderung muss durch ein Architecture Review Board, in dem geprüft wird: Geht es im Standard? Wenn nein, warum nicht BTP?`,
            do: 'Erwähne die Unterscheidung On-Stack vs. Side-by-Side und das ARB (Architecture Review Board).',
            dont: 'Behaupte nicht, dass man bei Clean Core gar nichts mehr programmieren darf – es geht um das "Wo" und "Wie"!'
          },
          {
            q: 'Wie lief die Datenmigration bei der SSB ab und welche Risiken gab es?',
            cat: 'Datenmigration',
            open: false,
            a: `Die Migration erfolgte über das SAP Migration Cockpit (LTMC) primär nach dem Staging-Tabellen-Prinzip. Wir haben die Altdaten aus dem ECC 6.0 extrahiert, bereinigt und in Staging-Tabellen geladen. Dort wurden Feld- und Werte-Mappings durchgeführt – beispielsweise die Zusammenführung historischer Debitoren und Kreditoren zum zentralen Business Partner (CVI) und die Zuordnung alter Buchungskreise.\n\nDas größte Risiko im FI-Bereich war der Eröffnungsbilanz-Abgleich: Nach der Übernahme von Sachkontensalden, offenen Posten und Anlagenwerten (FI-AA) gegen das zentrale Datenübernahmekonto muss dieses exakt 0,00 € aufweisen. Wir haben durch iterative Testmigrationen sichergestellt, dass die SuSa-Listen centgenau übereinstimmen.`,
            do: 'Erkläre den Ablauf: Extraktion -> Staging -> Mapping -> Simulation -> Import -> Abstimmung (0,00 € Übernahmekonto).',
            dont: 'Sage nicht, dass Datenmigration einfach "Excel-Hochladen" ist – es ist ein hochgradig revisionssicherer Prozess.'
          },
          {
            q: 'Wie sind Sie mit Widerständen im Projekt oder zwischen Abteilungen umgegangen?',
            cat: 'Projektmanagement & Governance',
            open: false,
            a: `In einem öffentlichen Verkehrsunternehmen wie der SSB ist der Betriebsrat (BR und SBV) von Tag 1 an über eine formelle Betriebsvereinbarung und Sitze im Lenkungsausschuss eingebunden.\n\nTypische Widerstände entstanden z.B. bei der Standardisierung: Fachbereiche wollten ihre vertrauten ECC-Masken und Z-Transaktionen behalten. Wir haben in TP1 und TP5 auf Transparenz und Einbindung gesetzt: Durch Fit-to-Standard Demos direkt am System haben wir gezeigt, warum Fiori Apps Prozesse beschleunigen. Bei Berechtigungskonzepten haben wir Datenschutz und Revisionssicherheit von vornherein transparent mit dem BR abgestimmt, statt ihn vor vollendete Tatsachen zu stellen.`,
            do: 'Hebe die Rolle von TP1 (Change Management) und die frühe Einbindung des Betriebsrats hervor.',
            dont: 'Tue nicht so, als gäbe es in Großprojekten keine Widerstände – das wirkt unprofessionell.'
          },
          {
            q: 'Welche Rolle spielt SAP Signavio im Zusammenspiel mit SAP Cloud ALM?',
            cat: 'Projektmanagement & Governance',
            open: false,
            a: `Signavio und Cloud ALM ergänzen sich perfekt:\n- SAP Signavio ist die Business- und Prozessplattform. Hier wird der Ist-Zustand analysiert (z.B. via Process Insights und plug-and-gain) und der Soll-Prozess in BPMN 2.0 modelliert.\n- SAP Cloud ALM ist die Ausführungs- und Implementierungsplattform. Die Prozessmodelle aus Signavio werden nach CALM synchronisiert, wo sie direkt mit Projektphasen, User Stories, funktionalen Anforderungen und Testfällen verknüpft werden.\n\nDadurch entsteht eine lückenlose Traceability vom Geschäftsprozess bis zum getesteten Fiori-Klick.`,
            do: 'Erkläre die Trennung: Signavio = "Was wollen wir?" (Prozess), Cloud ALM = "Wie setzen wir es um und testen es?" (Ausführung).',
            dont: 'Verwechsle die beiden Tools nicht oder stelle sie als Konkurrenten dar.'
          }
        ];

        const filesData = [
          { name: 'SSB Executive Summary Discover Phase.docx', cat: 'Explore & Lösungsdesign', path: 'Desktop/Discover Phase', desc: 'Ergebnisbericht des Digital Discovery Assessments (DDA) mit Nagarro ES GmbH. Definition des S/4HANA Greenfield Scopes.', impact: 'Beweist, dass du die Phase 0 (DDA Scoping) von Grund auf verstanden hast.' },
          { name: 'SSB Lösungsdesign Dokument.docx', cat: 'Explore & Lösungsdesign', path: 'Desktop/Explore Phase', desc: '82.000 Zeichen starkes Architektur- und Lösungsdesigndokument für TP2 (Kaufmännische Prozesse: FI, CO, MM, RE-FX, Grants Mgmt).', impact: 'Zeigt dein tiefes Verständnis für die Gesamtarchitektur, Clean Core und WRICEFA-Objekte.' },
          { name: 'Migrationskonzept v0 1 2025_04_28.docx', cat: 'Datenmigration', path: 'Desktop/Explore Phase/Datenmigration', desc: 'Detailkonzept von Nagarro zur Datenmigration. Definition von Staging-Tabellen, Mapping-Regeln, Bilanzabgleich und Cutover.', impact: 'Dein Beleg für fundierte Datenmigrations- und Schnittstellenkompetenz.' },
          { name: 'SSB_Migrationsobjekte_Vorschlag.xlsx', cat: 'Datenmigration', path: 'Desktop/Explore Phase/Datenmigration', desc: 'Strukturierte Übersicht aller Migrationsobjekte nach Geschäftsobjekttyp, Methode (Staging vs Direct) und Custom Fields.', impact: 'Zeigt, dass du konkrete Datenobjekte (Business Partner, FI-AA, Kostenstellen) im Detail kennst.' },
          { name: '20251107_SAP_CALM_How2handle_quickguide.docx', cat: 'Tools & Enablement', path: 'Desktop/Uni', desc: 'Von Visar verfasster Quickguide zur Nutzung von SAP Cloud ALM für Projekt-Setup, Quality Gates und Fit-to-Standard Tracking.', impact: 'Echtes Artefakt deiner Tool-Governance-Leistung. Unbedingt im Vorstellungsgespräch erwähnen!' },
          { name: 'SAP Enable Now Übergabe.docx', cat: 'Tools & Enablement', path: 'Desktop', desc: 'Strategisches Übergabekonzept von UB I (IT) an UB AC (Personalentwicklung) zur Etablierung der Single-Source-Content-Strategie.', impact: 'Beweist deine Fähigkeit zur strategischen Schnittstellenkommunikation zwischen IT und HR.' },
          { name: 'TP5_Projektsteckbrief.docx', cat: 'PMO & Steuerung', path: 'Desktop/TP5', desc: 'Offizieller Projektauftrag für TP5 unter Roland Nowak: Steuerung von Budget, Ressourcen, Architektur, Vergabe und Berechtigungen.', impact: 'Dokumentiert dein organisatorisches "Zuhause" im Projektmanagement Office.' },
          { name: '20250922_Projektplan_GAP_Axians_Gerdes.xlsx', cat: 'PMO & Steuerung', path: 'Desktop', desc: 'Trackingliste der technischen Basis-ToDos mit Axians (ES4 System, ADS Formulare, SSO, Transportkonsolidierung).', impact: 'Zeigt deine Hands-on Rolle bei der Steuerung technischer Infrastrukturpartner.' },
          { name: '20260211_Themensammlung_Priorisierung.xlsx', cat: 'PMO & Steuerung', path: 'Desktop', desc: 'Priorisierungsmatrix mit CalmIDs, T-Shirt-Sizes und Zuweisungen für anstehende S/4-Releases.', impact: 'Beweis für agile Aufwandsschätzung und Releasesteuerung.' },
          { name: 'Masterzeugnis_Murseli_Visar.pdf', cat: 'Wissenschaft & Uni', path: 'Studium_Dokumente', desc: 'Offizielles Zeugnis über die Masterprüfung der Universität Stuttgart (17. September 2026, 120 ECTS, Gesamtnote "gut" 1,6).', impact: 'Amtlicher Vollnachweis deines M.Sc. Abschlusses, der Masterarbeit (1,0) und aller 15 Fachprüfungen.' },
          { name: 'Masterarbeit_Visar_Murseli.pdf', cat: 'Wissenschaft & Uni', path: 'SSB Dateien', desc: 'Masterarbeit (126 Seiten, Note 1,0 bei Prof. Herzwurm, Uni Stuttgart) über Kritische Erfolgsfaktoren der S/4HANA Plattformisierung.', impact: 'Dein akademisches Meisterstück – belegt deine methodische Spitzenklasse!' },
          { name: 'DigitaleNachhaltigkeit_Ausarbeitung_Schmalz.docx', cat: 'Wissenschaft & Uni', path: 'Studium_Dokumente', desc: 'Wissenschaftliche Ausarbeitung (Note 1,0, 6 ECTS): Nachhaltigkeit durch Automatisierung: Eine Fallstudie zur Optimierung der Abfallbilanz bei der Schmalz GmbH (Dr. Dimitri Petrik).', impact: 'Beweist Green-IT-, BPMN- und CSRD/ESG-Expertise direkt am Weltmarktführer J. Schmalz GmbH.' },
          { name: 'CloudComputing_Kurzpaper_Murseli.pdf', cat: 'Wissenschaft & Uni', path: 'Studium_Dokumente', desc: 'Wissenschaftliches Kurzpaper (12 Seiten): Entwicklung einer Cloud-basierten Plattformarchitektur für einen wachsenden Onlineshop (AWS Well-Architected Framework).', impact: 'Zeigt tiefes Know-how in Cloud-Architekturen: Microservices, DynamoDB, Step Functions, QuickSight, EventBridge.' },
          { name: 'ISG_PatentRadar_Pitch.pdf', cat: 'Wissenschaft & Uni', path: 'Studium_Dokumente', desc: 'Pitch-Deck & Geschäftsmodell-Konzept: PatentRadar – Digital Venture für Klingele Paper & Packaging (Prof. Dr. Georg Herzwurm).', impact: 'Verknüpft Bosch-Patenterfahrung mit digitaler Geschäftsmodell-Innovation und Venture-Pitching.' },
          { name: 'FPWI_Forschungsprojekt_Paper.pdf', cat: 'Wissenschaft & Uni', path: 'Studium_Dokumente', desc: 'Forschungspapier (Note 1,3, 6 ECTS): Integration physischer und digitaler Welten: Ein Framework für Smart Service Blueprinting (DSRM Peffers, SUS-Score 85/100).', impact: 'Beweist Methodenkompetenz in Design Science Research, IoT-Architekturen & Smart Services.' },
          { name: 'Seminararbeit_Murseli.pdf', cat: 'Wissenschaft & Uni', path: 'Studium_Dokumente', desc: 'Systematische Literaturanalyse (SLR nach PRISMA 2020, 26 Studien): Die Transformation menschlicher Arbeitsrollen durch KI-gestützte Mensch-Roboter-Kollaboration in der Produktion.', impact: 'Beweist rigorose wissenschaftliche Recherche, Industrie 5.0, Cobots & Human-AI-Kollaboration.' },
          { name: 'Leistungsnachweis_Master_SS25.pdf', cat: 'Wissenschaft & Uni', path: 'Studium_Dokumente', desc: 'Offizieller Master-Leistungsnachweis Universität Stuttgart (M.Sc. Wirtschaftsinformatik, Gesamtnote 1,6).', impact: 'Amtlicher Nachweis deiner Noten: Digitale Nachhaltigkeit 1,0, FPWI 1,3, Applied AI 1,7, Innovationsmanagement 1,7, etc.' },
          { name: 'Notenrechner_Master.xlsx', cat: 'Wissenschaft & Uni', path: 'Studium_Dokumente', desc: 'Detaillierter ECTS- und Notenrechner für das M.Sc. Studium an der Universität Stuttgart.', impact: 'Strukturierte Übersicht aller 120 ECTS Leistungspunkte.' },
          { name: 'Bachelorarbeit_Murseli.pdf', cat: 'Wissenschaft & Uni', path: 'Studium_Dokumente', desc: 'Bachelorarbeit (Note 1,7, Uni Stuttgart): Die Bedeutung von Boundary Resources in Low-Code Entwicklungsplattformen (OutSystems & Mendix).', impact: 'Beweist deinen kontinuierlichen Forschungsschwerpunkt auf Plattformen und Schnittstellen seit 2023.' },
          { name: 'Bachelorzeugnis_Leistungsübersicht.pdf', cat: 'Wissenschaft & Uni', path: 'Studium_Dokumente', desc: 'Offizielle Leistungsübersicht B.Sc. Wirtschaftsinformatik (180 ECTS, Bestnote 1,0 in E-Business Informationssysteme).', impact: 'Belegt dein starkes informationstechnisches und betriebswirtschaftliches Fundament.' },
          { name: 'Bachelorurkunde_Murseli.pdf', cat: 'Wissenschaft & Uni', path: 'Studium_Dokumente', desc: 'Offizielle Verleihungsurkunde des akademischen Grades Bachelor of Science durch die Universität Stuttgart.', impact: 'Formaler Nachweis deines ersten berufsqualifizierenden Hochschulabschlusses.' },
          { name: 'Codebuch_Masterarbeit_Mayring.xlsx', cat: 'Wissenschaft & Uni', path: 'Studium_Dokumente', desc: 'Wissenschaftliches Mayring-Codebuch zur qualitativen Inhaltsanalyse der 12 empirischen Experteninterviews.', impact: 'Beweist höchste empirische Forschungsmethodik und qualitative Datenanalysekompetenz.' },
          { name: 'Interview_Roland_Nowak_Gesamt_PL.docx', cat: 'Explore & Lösungsdesign', path: 'Studium_Dokumente/Interviews', desc: 'Vollständiges Experteninterview-Transkript mit Roland Nowak (Gesamtprojektleiter SAP4SSB).', impact: 'Echter Primärbeleg für dein tiefes Verständnis der Management- und Architekturperspektive.' },
          { name: 'Interview_Thomas_Wimpff_TP2_Leitung.docx', cat: 'Explore & Lösungsdesign', path: 'Studium_Dokumente/Interviews', desc: 'Experteninterview-Transkript mit Thomas Wimpff (Teilprojektleiter TP2 Finance & Controlling).', impact: 'Beweist dein Detailwissen über Trennungsrechnung, ACDOCA und kaufmännische Prozesse.' },
          { name: 'Interview_Armin_Heinrich_Basis_Architektur.docx', cat: 'PMO & Steuerung', path: 'Studium_Dokumente/Interviews', desc: 'Experteninterview-Transkript mit Armin Heinrich (Enterprise Architekt & Basis SSB).', impact: 'Belegt dein Verständnis für BTP-Zielarchitektur, SSO und Cloud-Infrastruktur.' },
          { name: 'Interview_Henning_Gerdes_Axians_Lead.docx', cat: 'PMO & Steuerung', path: 'Studium_Dokumente/Interviews', desc: 'Experteninterview-Transkript mit Henning Gerdes (Lead Architect Axians ES4).', impact: 'Dokumentiert deine Schnittstellenkompetenz bei der Steuerung technischer Basispartner.' },
          { name: 'Zeugnisse_Murseli_Visar.pdf', cat: 'PMO & Steuerung', path: 'SSB Dateien', desc: 'Offizielle Leistungsnachweise: M.Sc. Wirtschaftsinformatik 1,6, SSB Zwischenzeugnis (Fillinger/Nowak), Datacenter One, TOGAF.', impact: 'Lückenlose Verifikation aller deiner Erfolge und Top-Referenzen.' }
        ];

        const filteredQA = computed(() => {
          let list = allQA;
          if (selectedQACat.value !== 'Alle') {
            list = list.filter(item => item.cat === selectedQACat.value);
          }
          if (searchQuery.value) {
            const q = searchQuery.value.toLowerCase();
            list = list.filter(item => item.q.toLowerCase().includes(q) || item.a.toLowerCase().includes(q));
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

        const exportNotes = () => {
          const blob = new Blob([personalNotes.value], { type: 'text/markdown;charset=utf-8' });
          const url = URL.createObjectURL(blob);
          const a = document.createElement('a');
          a.href = url;
          a.download = 'Visar_Murseli_Second_Brain_Notes.md';
          a.click();
          URL.revokeObjectURL(url);
        };

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
          const saved = localStorage.getItem('vm_second_brain_notes');
          if (saved) {
            personalNotes.value = saved;
          } else {
            personalNotes.value = `# Visar Murseli | Mein persönliches Second Brain\\n\\nWillkommen in deinem persönlichen Karriere-Notizbuch!\\nHier kannst du Notizen zu Vorstellungsgesprächen, Gehaltsverhandlungen und SAP-Architekturen festhalten.\\n\\nAlles, was du hier eintippst, wird automatisch in deinem Browser gespeichert.\\n`;
          }
        });

        return {
          activeTab,
          searchQuery,
          isDark,
          pitchMode,
          tabs,
          qaCategories,
          fileCategories,
          selectedQACat,
          selectedFileCat,
          personalNotes,
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
          exportNotes,
          clearNotes,
          insertTemplate
        };
      }
    }).mount('#app');
  </script>
</body>
</html>
"""
