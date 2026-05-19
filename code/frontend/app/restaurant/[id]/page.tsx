"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import { getRestaurantById, getDishesByRestaurant } from "@/lib/api";
import { useCart } from "@/lib/cart-context";
import type { Restaurant, Dish } from "@/lib/types";

// Curated Unsplash food photos — warm, appetizing, cozy
const DISH_PHOTOS = [
  "https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=400&h=300&fit=crop&q=80", // pizza
  "https://images.unsplash.com/photo-1482049016688-2d3e1b311543?w=400&h=300&fit=crop&q=80", // breakfast plate
  "https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=400&h=300&fit=crop&q=80", // grilled food
  "https://images.unsplash.com/photo-1540189549336-e6e99c3679fe?w=400&h=300&fit=crop&q=80", // salad bowl
  "https://images.unsplash.com/photo-1567620905732-2d1ec7ab7445?w=400&h=300&fit=crop&q=80", // pancakes
  "https://images.unsplash.com/photo-1476224203421-9ac39bcb3327?w=400&h=300&fit=crop&q=80", // burger
  "https://images.unsplash.com/photo-1551183053-bf91a1d81141?w=400&h=300&fit=crop&q=80", // latte art
  "https://images.unsplash.com/photo-1563379926898-05f4575a45d8?w=400&h=300&fit=crop&q=80", // pasta
  "https://images.unsplash.com/photo-1499028344343-cd173ffc68a9?w=400&h=300&fit=crop&q=80", // BBQ
  "https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=400&h=300&fit=crop&q=80", // chocolate cake
];

export default function RestaurantPage() {
  const { id } = useParams<{ id: string }>();
  const restaurantId = Number(id);
  const [restaurant, setRestaurant] = useState<Restaurant | null>(null);
  const [dishes, setDishes] = useState<Dish[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const { addItem, cart, totalItems } = useCart();
  const [addedDishId, setAddedDishId] = useState<number | null>(null);

  useEffect(() => {
    if (isNaN(restaurantId)) return;
    Promise.all([getRestaurantById(restaurantId), getDishesByRestaurant(restaurantId)])
      .then(([r, d]) => { setRestaurant(r); setDishes(d); })
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, [restaurantId]);

  const handleAdd = (dish: Dish) => {
    if (!restaurant) return;
    addItem(restaurant.id, restaurant.name, { dish_id: dish.id, name: dish.name, price: dish.price, quantity: 1 });
    setAddedDishId(dish.id);
    setTimeout(() => setAddedDishId(null), 800);
  };

  const categories = Array.from(new Set(dishes.map((d) => d.category)));

  if (loading) return <div className="flex justify-center py-24"><div className="h-10 w-10 animate-spin rounded-full border-4 border-orange-400 border-t-transparent" /></div>;
  if (error || !restaurant) return (
    <div className="mx-auto max-w-md py-24 text-center">
      <span className="text-5xl block mb-5">😕</span>
      <p className="text-xl font-semibold text-stone-600">{error || "Ресторан не знайдено"}</p>
      <Link href="/" className="inline-block mt-5 text-orange-500 hover:underline">← Назад</Link>
    </div>
  );

  return (
    <div className="mx-auto max-w-7xl px-6 py-12">
      <Link href="/" className="inline-flex items-center gap-1.5 text-sm text-stone-400 hover:text-orange-500 transition-colors duration-300 mb-6">
        <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}><path strokeLinecap="round" strokeLinejoin="round" d="M15 19l-7-7 7-7" /></svg>
        Всі ресторани
      </Link>

      <div className="rounded-3xl bg-white shadow-sm p-8 mb-12">
        <div className="flex flex-col sm:flex-row sm:items-end justify-between gap-5">
          <div>
            <h1 className="text-3xl sm:text-4xl font-extrabold tracking-tight text-stone-800 mb-3">{restaurant.name}</h1>
            <div className="flex flex-wrap items-center gap-4 text-stone-500 text-sm">
              <span className="flex items-center gap-1.5"><span className="text-amber-400 text-base">★</span><span className="font-semibold text-stone-700">{restaurant.rating.toFixed(1)}</span></span>
              <span>📍 {restaurant.address}</span>
              <span className={`text-xs font-semibold px-3 py-1 rounded-full ${restaurant.is_active ? "bg-emerald-50 text-emerald-600" : "bg-red-50 text-red-500"}`}>{restaurant.is_active ? "Відкрито" : "Зачинено"}</span>
            </div>
          </div>
          {totalItems > 0 && cart.restaurant_id === restaurantId && (
            <Link href="/cart" className="shrink-0 flex items-center gap-2 rounded-full bg-orange-500 px-6 py-3 text-sm font-bold text-white hover:bg-orange-600 transition-colors duration-300 shadow-md shadow-orange-200">
              Кошик · {totalItems} поз.
            </Link>
          )}
        </div>
      </div>

      {dishes.length === 0 && (
        <div className="text-center py-20">
          <span className="text-5xl block mb-5">📋</span>
          <p className="text-xl font-semibold text-stone-600">Меню порожнє</p>
          <p className="text-stone-400 mt-2">Додайте страви через <a href="http://127.0.0.1:8000/docs" target="_blank" rel="noreferrer" className="text-orange-500 underline">Swagger UI</a></p>
        </div>
      )}

      {categories.map((cat) => (
        <section key={cat} className="mb-12">
          <h2 className="text-xl font-bold text-stone-800 mb-6 flex items-center gap-3">
            <span className="h-1 w-8 rounded-full bg-orange-400" />
            {cat}
          </h2>
          <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
            {dishes.filter((d) => d.category === cat).map((dish) => (
              <div key={dish.id} className="group overflow-hidden rounded-3xl bg-white shadow-sm hover:shadow-md hover:-translate-y-1 transition-all duration-300">
                {/* Dish photo */}
                <div className="relative h-40 overflow-hidden">
                  <img
                    src={DISH_PHOTOS[(dish.id - 1) % DISH_PHOTOS.length]}
                    alt={dish.name}
                    className="h-full w-full object-cover group-hover:scale-105 transition-transform duration-500"
                  />
                </div>
                {/* Content */}
                <div className="p-6">
                  <div className="mb-4">
                    <h3 className="font-bold text-stone-800 group-hover:text-orange-500 transition-colors duration-300 mb-1.5">{dish.name}</h3>
                    {dish.description && <p className="text-sm text-stone-400 leading-relaxed line-clamp-2">{dish.description}</p>}
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-lg font-extrabold text-orange-500">{dish.price.toFixed(2)} ₴</span>
                    <button onClick={() => handleAdd(dish)} disabled={!restaurant.is_active}
                      className={`rounded-full px-5 py-2.5 text-sm font-bold transition-all duration-300 ${addedDishId === dish.id ? "bg-emerald-100 text-emerald-600 scale-95" : restaurant.is_active ? "bg-orange-100 text-orange-600 hover:bg-orange-500 hover:text-white" : "bg-stone-100 text-stone-400 cursor-not-allowed"}`}>
                      {addedDishId === dish.id ? "✓ Додано" : "+ Додати"}
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </section>
      ))}
    </div>
  );
}
