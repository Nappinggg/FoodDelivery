"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { getRestaurants } from "@/lib/api";
import type { Restaurant } from "@/lib/types";

// Curated Unsplash food/restaurant photos — warm, cozy aesthetic
const RESTAURANT_PHOTOS = [
  "https://images.unsplash.com/photo-1554118811-1e0d58224f24?w=600&h=400&fit=crop&q=80", // cozy cafe
  "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=600&h=400&fit=crop&q=80", // restaurant interior
  "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=600&h=400&fit=crop&q=80", // warm restaurant
  "https://images.unsplash.com/photo-1466978913421-dad2ebd01d17?w=600&h=400&fit=crop&q=80", // bakery pastries
  "https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=600&h=400&fit=crop&q=80", // plated food
  "https://images.unsplash.com/photo-1559339352-11d035aa65de?w=600&h=400&fit=crop&q=80", // pizza oven
  "https://images.unsplash.com/photo-1537047902294-62a40c20a6ae?w=600&h=400&fit=crop&q=80", // table setting
  "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=600&h=400&fit=crop&q=80", // coffee latte
];

const PER_PAGE = 6;

export default function HomePage() {
  const [restaurants, setRestaurants] = useState<Restaurant[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [page, setPage] = useState(1);

  useEffect(() => {
    getRestaurants()
      .then(setRestaurants)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, []);

  const totalPages = Math.ceil(restaurants.length / PER_PAGE);
  const paginated = restaurants.slice((page - 1) * PER_PAGE, page * PER_PAGE);

  return (
    <div className="mx-auto max-w-7xl px-6 py-12">
      {/* Hero */}
      <section className="mb-16 text-center">
        <h1 className="text-4xl sm:text-5xl font-extrabold tracking-tight text-stone-800 mb-5">
          Зголоднів? Ми вже
          <span className="text-orange-500"> тут</span>.
        </h1>
        <p className="text-stone-500 text-lg max-w-2xl mx-auto leading-relaxed">
          Відкривай найкращі ресторани поруч і замовляй улюблені страви — швидко та зручно.
        </p>
      </section>

      {/* Loading */}
      {loading && (
        <div className="flex justify-center py-24">
          <div className="h-10 w-10 animate-spin rounded-full border-4 border-orange-400 border-t-transparent" />
        </div>
      )}

      {/* Error */}
      {error && (
        <div className="mx-auto max-w-md rounded-3xl bg-white p-8 text-center shadow-sm">
          <p className="text-red-500 font-semibold mb-2">Не вдалося завантажити ресторани</p>
          <p className="text-sm text-stone-500">{error}</p>
          <p className="text-sm text-stone-400 mt-4">
            Переконайтеся, що бекенд працює:{" "}
            <code className="text-orange-500 bg-orange-50 px-2 py-0.5 rounded-lg text-xs">
              uvicorn main:app --reload
            </code>
          </p>
        </div>
      )}

      {/* Empty */}
      {!loading && !error && restaurants.length === 0 && (
        <div className="text-center py-24">
          <span className="text-6xl mb-5 block">🏪</span>
          <p className="text-xl font-semibold text-stone-700 mb-2">Ще немає ресторанів</p>
          <p className="text-stone-400">
            Додайте ресторани через{" "}
            <a
              href="http://127.0.0.1:8000/docs"
              target="_blank"
              rel="noreferrer"
              className="text-orange-500 underline underline-offset-2"
            >
              Swagger UI
            </a>
          </p>
        </div>
      )}

      {/* Restaurant grid */}
      {!loading && restaurants.length > 0 && (
        <>
          <div className="grid gap-8 sm:grid-cols-2 lg:grid-cols-3">
            {paginated.map((r) => (
              <Link
                key={r.id}
                href={`/restaurant/${r.id}`}
                className="group relative overflow-hidden rounded-3xl bg-white shadow-sm hover:shadow-md hover:-translate-y-1 transition-all duration-300"
              >
                {/* Photo banner */}
                <div className="relative h-48 overflow-hidden">
                  <img
                    src={RESTAURANT_PHOTOS[(r.id - 1) % RESTAURANT_PHOTOS.length]}
                    alt={r.name}
                    className="h-full w-full object-cover group-hover:scale-105 transition-transform duration-500"
                  />
                  <div className="absolute inset-0 bg-gradient-to-t from-black/20 to-transparent" />
                </div>

                {/* Content */}
                <div className="p-6">
                  <div className="flex items-start justify-between mb-3">
                    <h2 className="text-lg font-bold text-stone-800 group-hover:text-orange-500 transition-colors duration-300">
                      {r.name}
                    </h2>
                    <span
                      className={`flex items-center gap-1.5 rounded-full px-3 py-1 text-xs font-semibold ${r.is_active
                          ? "bg-emerald-50 text-emerald-600"
                          : "bg-red-50 text-red-500"
                        }`}
                    >
                      <span className={`h-1.5 w-1.5 rounded-full ${r.is_active ? "bg-emerald-500" : "bg-red-400"}`} />
                      {r.is_active ? "Відкрито" : "Зачинено"}
                    </span>
                  </div>

                  <p className="text-sm text-stone-400 mb-4 line-clamp-1">{r.address}</p>

                  <div className="flex items-center gap-1.5 text-sm">
                    <span className="text-amber-400 text-base">★</span>
                    <span className="font-semibold text-stone-700">{r.rating.toFixed(1)}</span>
                  </div>
                </div>

                {/* Hover arrow */}
                <div className="absolute right-6 bottom-6 opacity-0 translate-x-2 group-hover:opacity-100 group-hover:translate-x-0 transition-all duration-300">
                  <svg className="h-5 w-5 text-orange-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                    <path strokeLinecap="round" strokeLinejoin="round" d="M9 5l7 7-7 7" />
                  </svg>
                </div>
              </Link>
            ))}
          </div>

          {/* Pagination */}
          {totalPages > 1 && (
            <div className="flex items-center justify-center gap-2 mt-12">
              <button
                onClick={() => setPage((p) => Math.max(1, p - 1))}
                disabled={page === 1}
                className="rounded-full px-4 py-2 text-sm font-medium text-stone-500 hover:bg-white hover:shadow-sm transition-all duration-300 disabled:opacity-30 disabled:cursor-not-allowed"
              >
                ← Назад
              </button>
              {Array.from({ length: totalPages }, (_, i) => i + 1).map((p) => (
                <button
                  key={p}
                  onClick={() => setPage(p)}
                  className={`h-10 w-10 rounded-full text-sm font-semibold transition-all duration-300 ${p === page
                      ? "bg-orange-500 text-white shadow-md shadow-orange-200"
                      : "text-stone-500 hover:bg-white hover:shadow-sm"
                    }`}
                >
                  {p}
                </button>
              ))}
              <button
                onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
                disabled={page === totalPages}
                className="rounded-full px-4 py-2 text-sm font-medium text-stone-500 hover:bg-white hover:shadow-sm transition-all duration-300 disabled:opacity-30 disabled:cursor-not-allowed"
              >
                Вперед →
              </button>
            </div>
          )}
        </>
      )}
    </div>
  );
}
