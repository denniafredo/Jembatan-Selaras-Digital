/**
 * All editable copy lives here so content can be updated without touching JSX.
 * Replace the placeholder details (address, email, phone, client names) with the real ones.
 */

export const company = {
  name: 'Jembatan Selaras Digital',
  short: 'JSD',
  tagline: 'Digital Product Studio',
  email: 'jembatanselarasdigital@gmail.com',
  phone: '+62 21 5000 1234',
  whatsapp: '+62 812 3456 7890',
  address: 'Jl. Jenderal Sudirman Kav. 52, Jakarta Selatan 12190, Indonesia',
  founded: 2019,
  social: [
    { label: 'LinkedIn', href: 'https://linkedin.com/company/' },
    { label: 'Instagram', href: 'https://instagram.com/' },
    { label: 'Dribbble', href: 'https://dribbble.com/' },
    { label: 'GitHub', href: 'https://github.com/' },
  ],
};

export const nav = [
  { label: 'Services', href: '#services' },
  { label: 'About', href: '#about' },
  { label: 'Work', href: '#work' },
  { label: 'Clients', href: '#clients' },
  { label: 'Contact', href: '#contact' },
];

export const hero = {
  eyebrow: 'Digital Product Studio · Jakarta',
  headline: ['We build the bridge', 'between your business', 'and the technology', 'that powers it.'],
  // Word inside the last headline line that is painted in the brand colour.
  headlineAccent: 'powers',
  intro:
    'Jembatan Selaras Digital designs and engineers websites, web apps, and digital products that load fast, work on every phone, and turn visitors into customers.',
  ctaPrimary: { label: 'Let us talk', href: '#contact' },
  ctaSecondary: { label: 'See our work', href: '#work' },
  badges: ['Web Development', 'UI/UX Design', 'Mobile-First', 'Performance'],
};

export const marqueeWords = [
  'Web Development',
  'UI/UX Design',
  'Mobile-First',
  'Performance Engineering',
  'Brand Identity',
  'System Integration',
  'Digital Strategy',
];

/**
 * The performance & mobile message — the core belief the studio sells on.
 */
export const manifesto = {
  eyebrow: 'What most teams forget',
  title:
    'Two things quietly decide whether you win the client: load speed and how it looks on a phone.',
  body: [
    'Most of your prospects open your site on a phone, on a mobile connection, in the middle of doing something else. If it takes five seconds to show them anything, they are already gone — and you never find out they were there.',
    'It matters even more for a technology company. If your own website is slow, that is the first thing a client learns about how you build software. So we treat speed and mobile layout as requirements, not as polish at the end.',
  ],
  metrics: [
    { value: '< 2s', label: 'Target load time on 4G' },
    { value: '95+', label: 'Lighthouse performance score' },
    { value: '100%', label: 'Responsive down to 320px' },
    { value: 'AA', label: 'WCAG accessibility baseline' },
  ],
};

export const services = [
  {
    number: '01',
    title: 'Web & Company Profile',
    description:
      'Corporate sites that communicate what you actually do, built on a foundation your marketing team can update without calling a developer.',
    points: [
      'Information architecture',
      'Copy & content structure',
      'CMS integration',
      'SEO foundations',
    ],
  },
  {
    number: '02',
    title: 'Web Application',
    description:
      'Dashboards, internal tools, and customer portals — engineered for the workflows your team runs every day, not for a demo.',
    points: [
      'React & modern frontend',
      'API & backend integration',
      'Role-based access',
      'Reporting & analytics',
    ],
  },
  {
    number: '03',
    title: 'UI/UX Design',
    description:
      'Interfaces designed from real user journeys, delivered as a design system your product can keep growing into.',
    points: ['User research', 'Wireframe & prototype', 'Design system', 'Usability testing'],
  },
  {
    number: '04',
    title: 'Performance & Maintenance',
    description:
      'Audits and ongoing care that keep your site fast, secure, and online — with numbers you can show your stakeholders.',
    points: ['Core Web Vitals audit', 'Speed optimisation', 'Security patching', 'Monitoring & support'],
  },
];

export const about = {
  eyebrow: 'About us',
  title: 'A studio named after what we actually do — build bridges.',
  body: [
    'Jembatan Selaras Digital started in 2019 with a simple observation: most companies do not have a technology problem, they have a translation problem. Business teams know what they need. Engineering teams know what is possible. Very little gets across the gap.',
    'We sit in the middle. We work in small senior teams, we write the plan in language your stakeholders can approve, and we ship in short cycles so you see real screens instead of status reports.',
  ],
  principles: [
    {
      title: 'Fast by default',
      text: 'Performance budgets are set before the first line of code, not negotiated after launch.',
    },
    {
      title: 'Mobile is the main screen',
      text: 'Every layout is designed on a phone first, then allowed to grow into a desktop.',
    },
    {
      title: 'Built to be handed over',
      text: 'Documented, conventional code. You keep the repository, the accounts, and the option to leave.',
    },
  ],
};

export const projects = [
  {
    title: 'Pandji Hati Mulia',
    category: 'Mobile App',
    year: '2026',
    summary:
      'A Flutter app that takes a field sales team off paper. Visits, orders, and stock notes are filed from the phone, in the store, before the salesman walks back to the car.',
    result: 'Recaps that used to wait until the end of the week now land the moment a visit ends.',
    tags: ['Flutter', 'REST API'],
  },
  {
    title: 'Rimini',
    category: 'WordPress Site',
    year: '2026',
    summary:
      'A WordPress storefront for a clothing label, rebuilt around the product. The catalogue opens quickly on a phone connection and every piece is given room to be looked at.',
    result: 'Lighter pages, a calmer layout, and a catalogue search engines can finally read.',
    tags: ['WordPress', 'SEO'],
  },
];

export const testimonials = [
  {
    quote:
      'They asked about our sales process before they asked about our colour palette. That told us everything. The site they built now brings in more qualified leads in a week than we used to find in a month.',
    name: 'Andreas Wijaya',
    role: 'Marketing Director, Arta Sentosa Group',
  },
  {
    quote:
      'Our old portal took nine seconds to open on a phone out in the field. The team rebuilt it and it opens instantly now. Our drivers stopped calling the office to complain.',
    name: 'Ratna Puspita',
    role: 'Head of Operations, Nusantara Logistics',
  },
  {
    quote:
      'Clear plan, weekly demos, no surprises in the invoice. We have worked with four agencies before this one. It is the first handover where we actually understood the code we received.',
    name: 'Michael Tanuwijaya',
    role: 'CTO, Mitra Retail Indonesia',
  },
];

export const clients = [
  'Pandji Hati Mulia',
  'Rimini',
];

// Counted from the real arrays above, so the numbers can never drift from the work shown.
export const stats = [
  { value: projects.length, suffix: '', label: 'Projects delivered' },
  { value: clients.length, suffix: '', label: 'Clients served' },
  { value: 1, suffix: 'st yr', label: 'Studio founded in Jakarta, 2026' },
  { value: services.length, suffix: '', label: 'Service lines, from design to maintenance' },
];

export const contact = {
  eyebrow: 'Contact',
  title: 'Tell us what you are trying to build.',
  body: 'Send a short brief and we will reply within one business day with an honest read on scope and timeline — before any proposal.',
  interests: ['Company Profile', 'Web Application', 'UI/UX Design', 'Performance Audit'],
};
