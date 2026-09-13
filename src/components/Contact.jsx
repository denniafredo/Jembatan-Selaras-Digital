import { useState } from 'react'
import { Reveal, Marquee, ArrowIcon } from './ui'
import { contact, company } from '../data/site'

/**
 * Set VITE_CONTACT_ENDPOINT in .env to a form backend (Formspree, Basin, your own API)
 * and the form POSTs there. Without it, the form falls back to opening the visitor's
 * mail client with the brief pre-filled, so the page is never a dead end.
 */
const ENDPOINT = import.meta.env.VITE_CONTACT_ENDPOINT

const field =
  'w-full rounded-xl border border-line bg-white px-4 py-3.5 text-[0.95rem] text-ink-900 placeholder:text-muted transition-colors focus:border-brand focus:outline-none'

export default function Contact() {
  const [status, setStatus] = useState('idle') // idle | sending | sent | error
  const [interest, setInterest] = useState(contact.interests[0])

  const handleSubmit = async (event) => {
    event.preventDefault()
    const form = event.currentTarget
    const data = Object.fromEntries(new FormData(form).entries())

    if (!ENDPOINT) {
      const body = [
        `Name: ${data.name}`,
        `Company: ${data.company || '-'}`,
        `Email: ${data.email}`,
        `Phone: ${data.phone || '-'}`,
        `Interest: ${data.interest}`,
        '',
        data.message,
      ].join('\n')

      window.location.href = `mailto:${company.email}?subject=${encodeURIComponent(
        `Project brief — ${data.name}`,
      )}&body=${encodeURIComponent(body)}`
      setStatus('sent')
      return
    }

    setStatus('sending')
    try {
      const response = await fetch(ENDPOINT, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
        body: JSON.stringify(data),
      })
      if (!response.ok) throw new Error('Request failed')
      form.reset()
      setStatus('sent')
    } catch {
      setStatus('error')
    }
  }

  const details = [
    { label: 'Email', value: company.email, href: `mailto:${company.email}` },
    { label: 'Phone', value: company.phone, href: `tel:${company.phone.replace(/\s/g, '')}` },
    {
      label: 'WhatsApp',
      value: company.whatsapp,
      href: `https://wa.me/${company.whatsapp.replace(/[^0-9]/g, '')}`,
    },
    { label: 'Studio', value: company.address },
  ]

  return (
    <section id="contact" className="scroll-mt-24 py-20 md:py-32">
      {/* Contact ticker, like the reference layout */}
      <div className="border-y border-line bg-brand py-5 text-white">
        <Marquee duration={30} pauseOnHover={false}>
          <span className="flex items-center gap-8 px-8">
            <span className="whitespace-nowrap text-sm font-extrabold uppercase tracking-[0.2em]">
              Let us build something
            </span>
            <span className="h-1.5 w-1.5 rounded-full bg-white/70" />
            <span className="whitespace-nowrap text-sm font-extrabold uppercase tracking-[0.2em]">
              {company.email}
            </span>
            <span className="h-1.5 w-1.5 rounded-full bg-white/70" />
          </span>
        </Marquee>
      </div>

      <div className="shell mt-16 md:mt-24">
        <div className="grid gap-12 lg:grid-cols-12 lg:gap-16">
          {/* Details */}
          <div className="lg:col-span-5">
            <Reveal>
              <span className="eyebrow">{contact.eyebrow}</span>
            </Reveal>
            <Reveal delay={80}>
              <h2 className="mt-6 text-title font-extrabold text-ink-900">{contact.title}</h2>
            </Reveal>
            <Reveal delay={140}>
              <p className="mt-6 max-w-md text-base leading-relaxed text-ink">{contact.body}</p>
            </Reveal>

            <dl className="mt-12 space-y-px overflow-hidden rounded-2xl border border-line bg-line">
              {details.map((detail, i) => (
                <Reveal key={detail.label} delay={i * 70}>
                  <div className="bg-white px-6 py-5">
                    <dt className="text-[0.68rem] font-bold uppercase tracking-[0.18em] text-muted">
                      {detail.label}
                    </dt>
                    <dd className="mt-1.5 text-[0.95rem] font-semibold text-ink-900">
                      {detail.href ? (
                        <a
                          href={detail.href}
                          className="inline-flex items-center gap-1.5 hover:text-brand"
                        >
                          {detail.value}
                          <ArrowIcon className="h-3.5 w-3.5" />
                        </a>
                      ) : (
                        detail.value
                      )}
                    </dd>
                  </div>
                </Reveal>
              ))}
            </dl>
          </div>

          {/* Form */}
          <Reveal delay={120} className="lg:col-span-7">
            <form
              onSubmit={handleSubmit}
              className="rounded-3xl border border-line bg-paper-2 p-7 md:p-10"
            >
              <div className="grid gap-5 sm:grid-cols-2">
                <div>
                  <label htmlFor="name" className="mb-2 block text-sm font-bold text-ink-900">
                    Name *
                  </label>
                  <input id="name" name="name" required className={field} placeholder="Your name" />
                </div>
                <div>
                  <label htmlFor="company" className="mb-2 block text-sm font-bold text-ink-900">
                    Company
                  </label>
                  <input
                    id="company"
                    name="company"
                    className={field}
                    placeholder="Company name"
                  />
                </div>
                <div>
                  <label htmlFor="email" className="mb-2 block text-sm font-bold text-ink-900">
                    Email *
                  </label>
                  <input
                    id="email"
                    name="email"
                    type="email"
                    required
                    className={field}
                    placeholder="you@company.com"
                  />
                </div>
                <div>
                  <label htmlFor="phone" className="mb-2 block text-sm font-bold text-ink-900">
                    Phone
                  </label>
                  <input
                    id="phone"
                    name="phone"
                    type="tel"
                    inputMode="tel"
                    className={field}
                    placeholder="+62 ..."
                  />
                </div>
              </div>

              <fieldset className="mt-8">
                <legend className="mb-3 text-sm font-bold text-ink-900">I am looking for</legend>
                <input type="hidden" name="interest" value={interest} />
                <div className="flex flex-wrap gap-2">
                  {contact.interests.map((item) => (
                    <button
                      key={item}
                      type="button"
                      onClick={() => setInterest(item)}
                      aria-pressed={interest === item}
                      className={`rounded-full border px-4 py-2 text-[0.78rem] font-bold transition-colors ${
                        interest === item
                          ? 'border-brand bg-brand text-white'
                          : 'border-line bg-white text-ink hover:border-brand hover:text-brand'
                      }`}
                    >
                      {item}
                    </button>
                  ))}
                </div>
              </fieldset>

              <div className="mt-7">
                <label htmlFor="message" className="mb-2 block text-sm font-bold text-ink-900">
                  Tell us about the project *
                </label>
                <textarea
                  id="message"
                  name="message"
                  required
                  rows={5}
                  className={`${field} resize-y`}
                  placeholder="What are you building, who is it for, and when does it need to be live?"
                />
              </div>

              <div className="mt-8 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
                <button
                  type="submit"
                  disabled={status === 'sending'}
                  className="group inline-flex items-center justify-center gap-2.5 rounded-full bg-brand px-8 py-4 text-sm font-bold text-white transition-all duration-300 hover:bg-brand-dark hover:shadow-lg hover:shadow-brand/25 disabled:cursor-not-allowed disabled:opacity-60"
                >
                  {status === 'sending' ? 'Sending…' : 'Send the brief'}
                  <ArrowIcon className="h-4 w-4 transition-transform duration-300 group-hover:translate-x-0.5 group-hover:-translate-y-0.5" />
                </button>

                <p aria-live="polite" className="text-sm">
                  {status === 'sent' && (
                    <span className="font-semibold text-brand">
                      Thank you — we will reply within one business day.
                    </span>
                  )}
                  {status === 'error' && (
                    <span className="font-semibold text-red-600">
                      Something went wrong. Email us at {company.email}.
                    </span>
                  )}
                  {status === 'idle' && (
                    <span className="text-muted">We reply within one business day.</span>
                  )}
                </p>
              </div>
            </form>
          </Reveal>
        </div>
      </div>
    </section>
  )
}
