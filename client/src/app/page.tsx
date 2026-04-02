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
      <section className="flex flex-1 flex-col items-center justify-center px-6 py-24">
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

        {/* Stack badges */}
        <div className="mt-20 grid grid-cols-2 gap-4 sm:grid-cols-4">
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
              <p className="mt-1 text-sm font-medium text-gray-700">{label}</p>
            </div>
          ))}
        </div>
      </section>
    </main>
  );
}
