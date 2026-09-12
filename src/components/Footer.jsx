import { Logo } from './Logo'
import { ArrowIcon } from './ui'
import { company, nav, services } from '../data/site'

export default function Footer() {
  const year = new Date().getFullYear()

  return (
    <footer className="bg-ink-900 text-white">
      <div className="shell py-16 md:py-20">
        <div className="grid gap-12 md:grid-cols-12 md:gap-10">
          <div className="md:col-span-5">
            <Logo mono className="text-white" />
            <p className="mt-6 max-w-sm text-sm leading-relaxed text-muted">
              A digital product studio in Jakarta. We design and build websites and applications
              that load fast, work on every phone, and hold up after launch.
            </p>
            <a
              href={`mailto:${company.email}`}
              className="mt-7 inline-flex items-center gap-2 text-base font-bold tracking-tight text-white hover:text-brand"
            >
              {company.email}
              <ArrowIcon className="h-4 w-4" />
            </a>
          </div>

          <div className="md:col-span-3">
            <h2 className="text-[0.68rem] font-bold uppercase tracking-[0.2em] text-brand">
              Navigate
            </h2>
            <ul className="mt-5 space-y-3">
              {nav.map((item) => (
                <li key={item.href}>
                  <a href={item.href} className="text-sm text-line hover:text-white">
                    {item.label}
                  </a>
                </li>
              ))}
            </ul>
          </div>

          <div className="md:col-span-2">
            <h2 className="text-[0.68rem] font-bold uppercase tracking-[0.2em] text-brand">
              Services
            </h2>
            <ul className="mt-5 space-y-3">
              {services.map((service) => (
                <li key={service.number}>
                  <a href="#services" className="text-sm text-line hover:text-white">
                    {service.title}
                  </a>
                </li>
              ))}
            </ul>
          </div>

          <div className="md:col-span-2">
            <h2 className="text-[0.68rem] font-bold uppercase tracking-[0.2em] text-brand">
              Social
            </h2>
            <ul className="mt-5 space-y-3">
              {company.social.map((item) => (
                <li key={item.label}>
                  <a
                    href={item.href}
                    target="_blank"
                    rel="noreferrer noopener"
                    className="text-sm text-line hover:text-white"
                  >
                    {item.label}
                  </a>
                </li>
              ))}
            </ul>
          </div>
        </div>

        <div className="mt-14 flex flex-col gap-4 border-t border-white/12 pt-8 text-sm text-muted sm:flex-row sm:items-center sm:justify-between">
          <p>
            © {year} {company.name}. All rights reserved.
          </p>
          <p className="max-w-md sm:text-right">{company.address}</p>
        </div>
      </div>
    </footer>
  )
}
