export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center bg-gray-50 p-8">
      <div className="text-center">
        <h1 className="text-5xl font-bold tracking-tight text-gray-900">
          Smart Insights Dashboard
        </h1>
        <p className="mt-4 text-lg text-gray-500">
          Full-stack analytics platform — Phase 1 foundation running.
        </p>
        <div className="mt-10 grid grid-cols-2 gap-4 sm:grid-cols-4">
          {[
            { label: "Next.js", icon: "⚡" },
            { label: "FastAPI", icon: "🐍" },
            { label: "PostgreSQL", icon: "🐘" },
            { label: "Redis", icon: "🔴" },
          ].map(({ label, icon }) => (
            <div
              key={label}
              className="rounded-lg border border-gray-200 bg-white px-4 py-3 shadow-sm"
            >
              <span className="text-2xl">{icon}</span>
              <p className="mt-1 text-sm font-medium text-gray-700">{label}</p>
            </div>
          ))}
        </div>
      </div>
    </main>
  );
}
