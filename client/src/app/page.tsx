import Link from "next/link";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col bg-gray-50">
      {/* Nav */}
      <nav className="border-b border-gray-200 bg-white">
        <div className="mx-auto flex max-w-5xl items-center justify-between px-6 py-4">
          <span className="text-lg font-bold text-gray-900">
            Smart&nbsp;Insights
          </span>
          <div className="flex gap-3">
            <Link
              href="/login"
              className="rounded-lg px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-100"
            >
              Sign in
            </Link>
            <Link
              href="/register"
              className="rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700"
            >
              Get started
            </Link>
          </div>
        </div>
      </nav>

      {/* Hero */}
      <section className="flex flex-col items-center justify-center px-6 py-24">
        <div className="max-w-2xl text-center">
          <h1 className="text-5xl font-bold tracking-tight text-gray-900">
            Golf analytics,
            <br />
            <span className="text-blue-600">beautifully simple</span>
          </h1>
          <p className="mt-6 text-lg leading-relaxed text-gray-500">
            Track player performance, spot trends, and manage your favorites —
            powered by a modern full-stack platform with FastAPI, Next.js, and
            PostgreSQL.
          </p>
          <div className="mt-10 flex justify-center gap-4">
            <Link
              href="/register"
              className="rounded-lg bg-blue-600 px-6 py-3 text-sm font-medium text-white shadow-sm hover:bg-blue-700"
            >
              Create free account
            </Link>
            <Link
              href="/login"
              className="rounded-lg border border-gray-300 bg-white px-6 py-3 text-sm font-medium text-gray-700 shadow-sm hover:bg-gray-50"
            >
              Sign in
            </Link>
          </div>
        </div>
      </section>

      {/* Dashboard preview */}
      <section className="px-6 pb-20">
        <div className="mx-auto max-w-4xl">
          <div className="overflow-hidden rounded-2xl border border-gray-200 bg-white shadow-lg">
            {/* Mock browser bar */}
            <div className="flex items-center gap-2 border-b border-gray-100 bg-gray-50 px-4 py-3">
              <div className="flex gap-1.5">
                <div className="h-3 w-3 rounded-full bg-gray-300" />
                <div className="h-3 w-3 rounded-full bg-gray-300" />
                <div className="h-3 w-3 rounded-full bg-gray-300" />
              </div>
              <div className="ml-4 flex-1 rounded-md bg-gray-200 px-3 py-1 text-xs text-gray-400">
                localhost:3000/dashboard
              </div>
            </div>
            {/* Mock dashboard content */}
            <div className="p-6">
              <div className="grid grid-cols-4 gap-3">
                {[
                  { label: "Players", value: "15" },
                  { label: "Favorites", value: "4" },
                  { label: "Stat Records", value: "180+" },
                  { label: "Top Tour", value: "PGA" },
                ].map((card) => (
                  <div
                    key={card.label}
                    className="rounded-lg border border-gray-100 bg-gray-50 p-3"
                  >
                    <p className="text-xs text-gray-400">{card.label}</p>
                    <p className="mt-1 text-lg font-bold text-gray-800">
                      {card.value}
                    </p>
                  </div>
                ))}
              </div>
              {/* Mock chart area */}
              <div className="mt-4 flex h-32 items-end gap-1 rounded-lg border border-gray-100 bg-gray-50 p-4">
                {[40, 55, 45, 65, 50, 70, 60, 75, 68, 80, 72, 78].map(
                  (h, i) => (
                    <div
                      key={i}
                      className="flex-1 rounded-t bg-blue-400"
                      style={{ height: `${h}%`, opacity: 0.6 + i * 0.03 }}
                    />
                  ),
                )}
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features section */}
      <section className="border-t border-gray-200 bg-white px-6 py-20">
        <div className="mx-auto max-w-4xl">
          <h2 className="text-center text-2xl font-bold text-gray-900">
            Why Smart Insights?
          </h2>
          <p className="mt-3 text-center text-sm text-gray-500">
            Built for golf analytics with a modern, extensible architecture.
          </p>
          <div className="mt-12 grid grid-cols-1 gap-8 sm:grid-cols-3">
            {[
              {
                icon: "📈",
                title: "Performance Tracking",
                desc: "Follow scoring averages, strokes gained, driving accuracy, and more across tournaments.",
              },
              {
                icon: "⭐",
                title: "Personal Favorites",
                desc: "Star the players you care about and get a focused dashboard tailored to your interests.",
              },
              {
                icon: "🔗",
                title: "Full-Stack Architecture",
                desc: "FastAPI backend, Next.js frontend, PostgreSQL, Redis — production-grade from day one.",
              },
            ].map(({ icon, title, desc }) => (
              <div key={title} className="text-center">
                <span className="text-3xl">{icon}</span>
                <h3 className="mt-4 font-semibold text-gray-900">{title}</h3>
                <p className="mt-2 text-sm leading-relaxed text-gray-500">
                  {desc}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Stack badges */}
      <section className="px-6 py-16">
        <div className="mx-auto max-w-3xl">
          <p className="mb-6 text-center text-sm font-medium text-gray-400 uppercase tracking-wide">
            Built with
          </p>
          <div className="grid grid-cols-2 gap-4 sm:grid-cols-4">
            {[
              { label: "Next.js", icon: "⚡" },
              { label: "FastAPI", icon: "🐍" },
              { label: "PostgreSQL", icon: "🐘" },
              { label: "Redis", icon: "🔴" },
            ].map(({ label, icon }) => (
              <div
                key={label}
                className="rounded-lg border border-gray-200 bg-white px-5 py-3 text-center shadow-sm"
              >
                <span className="text-2xl">{icon}</span>
                <p className="mt-1 text-sm font-medium text-gray-700">
                  {label}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-gray-200 bg-white px-6 py-8">
        <p className="text-center text-xs text-gray-400">
          Smart Insights Dashboard — a portfolio project by Jonatan Liljeblad
        </p>
      </footer>
    </main>
  );
}
