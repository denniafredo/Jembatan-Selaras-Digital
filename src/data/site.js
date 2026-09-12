/**
 * All editable copy lives here so content can be updated without touching JSX.
 * Replace the placeholder details (address, email, phone, client names) with the real ones.
 */

export const company = {
  name: 'Jembatan Selaras Digital',
  short: 'JSD',
  tagline: 'Digital Product Studio',
  email: 'hello@jembatanselarasdigital.com',
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
}

export const nav = [
  { label: 'Services', href: '#services' },
  { label: 'About', href: '#about' },
  { label: 'Work', href: '#work' },
  { label: 'Clients', href: '#clients' },
  { label: 'Contact', href: '#contact' },
]

export const hero = {
  eyebrow: 'Digital Product Studio · Jakarta',
  headline: ['We build the bridge', 'between your business', 'and the people who', 'need it.'],
  intro:
    'Jembatan Selaras Digital designs and engineers websites, web apps, and digital products that load fast, work on every phone, and turn visitors into customers.',
  ctaPrimary: { label: 'Let us talk', href: '#contact' },
  ctaSecondary: { label: 'See our work', href: '#work' },
  badges: ['Web Development', 'UI/UX Design', 'Mobile-First', 'Performance'],
}

export const marqueeWords = [
  'Web Development',
  'UI/UX Design',
  'Mobile-First',
  'Performance Engineering',
  'Brand Identity',
  'System Integration',
  'Digital Strategy',
]

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
}

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
]

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
}

export const stats = [
  { value: 120, suffix: '+', label: 'Projects delivered' },
  { value: 60, suffix: '+', label: 'Clients across Indonesia' },
  { value: 7, suffix: ' yrs', label: 'Building digital products' },
  { value: 98, suffix: '%', label: 'Clients who come back' },
]

export const projects = [
  {
    title: 'Nusantara Logistics Portal',
    category: 'Web Application',
    year: '2025',
    summary:
      'A shipment tracking portal replacing three spreadsheets and a WhatsApp group, used daily by 400 field staff.',
    result: 'Manual reporting time cut by 70%',
    tags: ['React', 'Node.js', 'PostgreSQL'],
  },
  {
    title: 'Arta Sentosa Corporate Site',
    category: 'Company Profile',
    year: '2025',
    summary:
      'A multi-language corporate site for a manufacturing group, rebuilt from a nine-second page into a sub-two-second one.',
    result: 'Load time 9.1s to 1.4s',
    tags: ['Next.js', 'Headless CMS', 'SEO'],
  },
  {
    title: 'Selaras Health Booking',
    category: 'UI/UX & Build',
    year: '2024',
    summary:
      'An appointment booking flow for a clinic network, redesigned around what patients actually do on a phone.',
    result: 'Booking completion up 42%',
    tags: ['Figma', 'React', 'Design System'],
  },
  {
    title: 'Mitra Retail Dashboard',
    category: 'Web Application',
    year: '2024',
    summary:
      'A merchant analytics dashboard consolidating sales from twelve outlets into one live view for the owners.',
    result: '12 outlets in one live view',
    tags: ['React', 'Charts', 'REST API'],
  },
]

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
]

export const clients = [
  'Nusantara Logistics',
  'Arta Sentosa',
  'Selaras Health',
  'Mitra Retail',
  'Bumi Energi',
  'Cahaya Finansial',
  'Graha Properti',
  'Sinar Manufaktur',
]

export const contact = {
  eyebrow: 'Contact',
  title: 'Tell us what you are trying to build.',
  body: 'Send a short brief and we will reply within one business day with an honest read on scope, timeline, and budget range — before any proposal.',
  budgets: ['Below Rp 25 jt', 'Rp 25 – 75 jt', 'Rp 75 – 200 jt', 'Above Rp 200 jt'],
  interests: ['Company Profile', 'Web Application', 'UI/UX Design', 'Performance Audit'],
}
