"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useAuth } from "@/lib/auth-context";
import { getOrdersByUser } from "@/lib/api";
import type { Order } from "@/lib/types";

const STATUS_STYLES: Record<string, string> = {
  pending: "bg-amber-50 text-amber-600",
  confirmed: "bg-blue-50 text-blue-600",
  preparing: "bg-violet-50 text-violet-600",
  delivering: "bg-cyan-50 text-cyan-600",
  delivered: "bg-emerald-50 text-emerald-600",
  cancelled: "bg-red-50 text-red-500",
};

const STATUS_TRANSLATIONS: Record<string, string> = {
  pending: "В обробці",
  confirmed: "Підтверджено",
  preparing: "Готується",
  delivering: "В дорозі",
  delivered: "Доставлено",
  cancelled: "Скасовано",
};

function getOrdersDeclension(count: number): string {
  const mod10 = count % 10;
  const mod100 = count % 100;
  if (mod100 >= 11 && mod100 <= 14) return "замовлень";
  if (mod10 === 1) return "замовлення";
  if (mod10 >= 2 && mod10 <= 4) return "замовлення";
  return "замовлень";
}

export default function OrdersPage() {
  const { user, loading: authLoading } = useAuth();
  const [orders, setOrders] = useState<Order[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (authLoading) return;
    if (!user) { setLoading(false); return; }
    getOrdersByUser(user.id)
      .then((data) => setOrders([...data].reverse()))
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, [user, authLoading]);

  if (authLoading || loading) {
    return (
      <div className="flex justify-center py-24">
        <div className="h-10 w-10 animate-spin rounded-full border-4 border-orange-400 border-t-transparent" />
      </div>
    );
  }

  if (!user) {
    return (
      <div className="mx-auto max-w-md px-6 py-24 text-center">
        <span className="text-5xl block mb-5">🔒</span>
        <h1 className="text-2xl font-extrabold text-stone-800 mb-2">Ви не авторизовані</h1>
        <p className="text-stone-500 mb-8">Увійдіть, щоб переглянути історію замовлень</p>
        <Link href="/auth" className="inline-flex rounded-full bg-orange-500 px-7 py-3 font-bold text-white hover:bg-orange-600 transition-colors duration-300 shadow-md shadow-orange-200">
          Увійти
        </Link>
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-3xl px-6 py-12">
      <h1 className="text-3xl font-extrabold tracking-tight text-stone-800 mb-2">Мої замовлення</h1>
      <p className="text-stone-400 mb-10">{orders.length} {getOrdersDeclension(orders.length)}</p>

      {error && (
        <div className="rounded-2xl bg-red-50 p-5 text-sm text-red-500 font-medium mb-6">{error}</div>
      )}

      {orders.length === 0 && !error && (
        <div className="text-center py-20">
          <span className="text-5xl block mb-5">📦</span>
          <p className="text-xl font-semibold text-stone-600 mb-2">Ще немає замовлень</p>
          <p className="text-stone-400 mb-6">Зробіть своє перше замовлення, щоб побачити його тут</p>
          <Link href="/" className="inline-flex rounded-full bg-orange-500 px-7 py-3 font-bold text-white hover:bg-orange-600 transition-colors duration-300 shadow-md shadow-orange-200">
            Переглянути ресторани
          </Link>
        </div>
      )}

      <div className="space-y-6">
        {orders.map((order) => (
          <div key={order.id} className="rounded-3xl bg-white shadow-sm overflow-hidden">
            {/* Receipt header */}
            <div className="flex items-center justify-between px-7 py-5 border-b border-stone-100">
              <div>
                <p className="text-sm text-stone-400">Номер замовлення</p>
                <p className="text-lg font-bold text-stone-800">#{order.id}</p>
              </div>
              <div className="text-right">
                <span className={`inline-flex items-center gap-1.5 rounded-full px-3 py-1 text-xs font-semibold capitalize ${STATUS_STYLES[order.status] || "bg-stone-50 text-stone-500"}`}>
                  <span className="h-1.5 w-1.5 rounded-full bg-current opacity-60" />
                  {STATUS_TRANSLATIONS[order.status] || order.status}
                </span>
              </div>
            </div>

            {/* Items */}
            <div className="px-7 py-5 space-y-3">
              {order.items.map((item) => (
                <div key={item.id} className="flex items-center justify-between text-sm">
                  <div className="flex items-center gap-3">
                    <span className="flex h-7 w-7 items-center justify-center rounded-full bg-orange-50 text-xs font-bold text-orange-500">
                      {item.quantity}×
                    </span>
                    <span className="text-stone-700">{item.dish_name || `Страва #${item.dish_id}`}</span>
                  </div>
                  <span className="font-semibold text-stone-600">
                    {(item.price_at_order * item.quantity).toFixed(2)} ₴
                  </span>
                </div>
              ))}
            </div>

            {/* Receipt footer */}
            <div className="flex items-center justify-between px-7 py-5 bg-stone-50/50 border-t border-stone-100">
              <span className="text-sm text-stone-400">
                {new Date(order.created_at).toLocaleDateString("uk-UA", { day: "numeric", month: "short", year: "numeric", hour: "2-digit", minute: "2-digit" })}
              </span>
              <span className="text-lg font-extrabold text-orange-500">
                {order.total_price.toFixed(2)} ₴
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
