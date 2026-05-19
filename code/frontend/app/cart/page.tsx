"use client";

import { useState } from "react";
import Link from "next/link";
import { useCart } from "@/lib/cart-context";
import { useAuth } from "@/lib/auth-context";
import { createOrder } from "@/lib/api";
import type { Order } from "@/lib/types";

type Step = "cart" | "checkout" | "success";
type PaymentMethod = "cash" | "card";

export default function CartPage() {
  const { cart, removeItem, updateQuantity, clearCart, totalPrice, totalItems } = useCart();
  const { user } = useAuth();

  const [step, setStep] = useState<Step>("cart");
  const [submitting, setSubmitting] = useState(false);
  const [order, setOrder] = useState<Order | null>(null);
  const [error, setError] = useState<string | null>(null);

  // Checkout form (React-only, NOT sent to API)
  const [address, setAddress] = useState({ street: "", apartment: "", comment: "" });
  const [payment, setPayment] = useState<PaymentMethod>("cash");

  const handleCheckout = async () => {
    if (!cart.restaurant_id || cart.items.length === 0) return;
    setSubmitting(true);
    setError(null);

    try {
      // Simulate bank processing for card payments
      if (payment === "card") {
        await new Promise((r) => setTimeout(r, 2000));
      }

      // Send ONLY what backend expects: { restaurant_id, items }
      const result = await createOrder(
        cart.restaurant_id,
        cart.items.map((i) => ({ dish_id: i.dish_id, quantity: i.quantity })),
        user?.id ?? 1
      );
      setOrder(result);
      clearCart();
      setStep("success");
    } catch (e) {
      setError(e instanceof Error ? e.message : "Не вдалося створити замовлення");
    } finally {
      setSubmitting(false);
    }
  };

  // ─── Success ──────────────────────────────────────────────────────
  if (step === "success" && order) {
    return (
      <div className="mx-auto max-w-lg px-6 py-24 text-center">
        <div className="mb-6 inline-flex h-20 w-20 items-center justify-center rounded-full bg-emerald-50">
          <span className="text-4xl">🎉</span>
        </div>
        <h1 className="text-3xl font-extrabold text-stone-800 mb-3">
          Ваше замовлення готується!
        </h1>
        <p className="text-stone-500 mb-1">
          Замовлення <span className="font-bold text-stone-800">#{order.id}</span>
        </p>
        <p className="text-stone-500 mb-2">
          Сума: <span className="font-bold text-orange-500">{order.total_price.toFixed(2)} ₴</span>
        </p>
        <p className="text-stone-400 text-sm mb-8">
          {payment === "card" ? "💳 Оплата карткою пройшла успішно" : "💵 Оплата готівкою при отриманні"}
        </p>

        <div className="rounded-2xl bg-white shadow-sm p-5 mb-8 text-left">
          <p className="text-xs font-medium text-stone-400 mb-1.5">Статус</p>
          <span className="inline-flex items-center gap-2 rounded-full bg-orange-50 px-4 py-1.5 text-sm font-semibold text-orange-600">
            <span className="h-2 w-2 rounded-full bg-orange-400 animate-pulse" />
            {order.status}
          </span>
        </div>

        <div className="flex gap-3 justify-center">
          <Link
            href="/orders"
            className="rounded-full bg-orange-500 px-7 py-3 font-bold text-white hover:bg-orange-600 transition-colors duration-300 shadow-md shadow-orange-200"
          >
            Перейти до моїх замовлень
          </Link>
          <Link
            href="/"
            className="rounded-full bg-stone-100 px-7 py-3 font-bold text-stone-600 hover:bg-stone-200 transition-colors duration-300"
          >
            На головну
          </Link>
        </div>
      </div>
    );
  }

  // ─── Empty cart ────────────────────────────────────────────────────
  if (totalItems === 0 && step !== "success") {
    return (
      <div className="mx-auto max-w-lg px-6 py-24 text-center">
        <span className="text-6xl block mb-5">🛒</span>
        <h1 className="text-2xl font-extrabold text-stone-800 mb-2">Кошик порожній</h1>
        <p className="text-stone-500 mb-8">Додайте страви з ресторану, щоб почати</p>
        <Link
          href="/"
          className="inline-flex rounded-full bg-orange-500 px-7 py-3 font-bold text-white hover:bg-orange-600 transition-colors duration-300 shadow-md shadow-orange-200"
        >
          Переглянути ресторани
        </Link>
      </div>
    );
  }

  // ─── Cart + Checkout ──────────────────────────────────────────────
  return (
    <div className="mx-auto max-w-3xl px-6 py-12">
      <h1 className="text-3xl font-extrabold tracking-tight text-stone-800 mb-2">Кошик</h1>
      <p className="text-stone-500 mb-10">
        З <span className="font-semibold text-stone-700">{cart.restaurant_name}</span>
      </p>

      {/* Items */}
      <div className="space-y-4 mb-10">
        {cart.items.map((item) => (
          <div key={item.dish_id} className="flex items-center gap-5 rounded-2xl bg-white shadow-sm p-5">
            <div className="flex-1 min-w-0">
              <p className="font-bold text-stone-800 truncate">{item.name}</p>
              <p className="text-sm text-orange-500 font-semibold">{item.price.toFixed(2)} ₴</p>
            </div>
            <div className="flex items-center gap-2.5">
              <button onClick={() => updateQuantity(item.dish_id, item.quantity - 1)} className="flex h-9 w-9 items-center justify-center rounded-full bg-stone-100 text-stone-500 hover:bg-orange-100 hover:text-orange-600 transition-colors duration-300 text-lg">−</button>
              <span className="w-8 text-center font-bold text-stone-800">{item.quantity}</span>
              <button onClick={() => updateQuantity(item.dish_id, item.quantity + 1)} className="flex h-9 w-9 items-center justify-center rounded-full bg-stone-100 text-stone-500 hover:bg-orange-100 hover:text-orange-600 transition-colors duration-300 text-lg">+</button>
            </div>
            <span className="w-24 text-right font-bold text-stone-800">{(item.price * item.quantity).toFixed(2)} ₴</span>
            <button onClick={() => removeItem(item.dish_id)} className="text-stone-300 hover:text-red-400 transition-colors duration-300" title="Видалити">
              <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}><path strokeLinecap="round" strokeLinejoin="round" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" /></svg>
            </button>
          </div>
        ))}
      </div>

      {/* Summary */}
      <div className="rounded-3xl bg-white shadow-sm p-8 mb-6">
        <div className="flex items-center justify-between mb-5">
          <span className="text-stone-500">Позицій</span>
          <span className="font-medium text-stone-700">{totalItems}</span>
        </div>
        <div className="flex items-center justify-between mb-8 text-xl">
          <span className="font-bold text-stone-800">Разом</span>
          <span className="font-extrabold text-orange-500">{totalPrice.toFixed(2)} ₴</span>
        </div>

        {step === "cart" && (
          <>
            <button
              onClick={() => setStep("checkout")}
              className="w-full rounded-full bg-orange-500 py-4 text-center font-bold text-white hover:bg-orange-600 transition-colors duration-300 shadow-md shadow-orange-200"
            >
              Оформити замовлення
            </button>
            <button
              onClick={clearCart}
              className="mt-3 w-full rounded-full bg-stone-50 py-3 text-center text-sm font-medium text-stone-400 hover:text-red-400 hover:bg-red-50 transition-all duration-300"
            >
              Очистити кошик
            </button>
          </>
        )}
      </div>

      {/* ─── Checkout form ─────────────────────────────────────────── */}
      {step === "checkout" && (
        <div className="rounded-3xl bg-white shadow-sm p-8 space-y-8 animate-in">
          {/* Delivery address */}
          <div>
            <h2 className="text-lg font-bold text-stone-800 mb-4 flex items-center gap-2">
              <span className="flex h-8 w-8 items-center justify-center rounded-full bg-orange-100 text-sm">📍</span>
              Адреса доставки
            </h2>
            <div className="space-y-3">
              <input
                type="text"
                placeholder="Вулиця та будинок"
                value={address.street}
                onChange={(e) => setAddress((p) => ({ ...p, street: e.target.value }))}
                className="w-full rounded-2xl bg-stone-50 px-5 py-3.5 text-sm text-stone-800 placeholder:text-stone-300 outline-none focus:ring-2 focus:ring-orange-300 transition-all"
              />
              <input
                type="text"
                placeholder="Квартира / офіс"
                value={address.apartment}
                onChange={(e) => setAddress((p) => ({ ...p, apartment: e.target.value }))}
                className="w-full rounded-2xl bg-stone-50 px-5 py-3.5 text-sm text-stone-800 placeholder:text-stone-300 outline-none focus:ring-2 focus:ring-orange-300 transition-all"
              />
              <textarea
                placeholder="Коментар для кур'єра"
                value={address.comment}
                onChange={(e) => setAddress((p) => ({ ...p, comment: e.target.value }))}
                rows={2}
                className="w-full rounded-2xl bg-stone-50 px-5 py-3.5 text-sm text-stone-800 placeholder:text-stone-300 outline-none focus:ring-2 focus:ring-orange-300 transition-all resize-none"
              />
            </div>
          </div>

          {/* Payment method */}
          <div>
            <h2 className="text-lg font-bold text-stone-800 mb-4 flex items-center gap-2">
              <span className="flex h-8 w-8 items-center justify-center rounded-full bg-orange-100 text-sm">💳</span>
              Спосіб оплати
            </h2>
            <div className="grid grid-cols-2 gap-3">
              <button
                onClick={() => setPayment("cash")}
                className={`rounded-2xl p-5 text-left transition-all duration-300 ${
                  payment === "cash"
                    ? "bg-orange-50 ring-2 ring-orange-400 shadow-sm"
                    : "bg-stone-50 hover:bg-stone-100"
                }`}
              >
                <span className="text-2xl block mb-2">💵</span>
                <p className="font-bold text-stone-800 text-sm">Готівкою</p>
                <p className="text-xs text-stone-400">Оплата кур&apos;єру</p>
              </button>
              <button
                onClick={() => setPayment("card")}
                className={`rounded-2xl p-5 text-left transition-all duration-300 ${
                  payment === "card"
                    ? "bg-orange-50 ring-2 ring-orange-400 shadow-sm"
                    : "bg-stone-50 hover:bg-stone-100"
                }`}
              >
                <span className="text-2xl block mb-2">💳</span>
                <p className="font-bold text-stone-800 text-sm">Карткою</p>
                <p className="text-xs text-stone-400">Онлайн оплата</p>
              </button>
            </div>
          </div>

          {/* Error */}
          {error && (
            <div className="rounded-2xl bg-red-50 px-5 py-3 text-sm text-red-500 font-medium">{error}</div>
          )}

          {/* Actions */}
          <div className="flex gap-3">
            <button
              onClick={() => setStep("cart")}
              className="flex-1 rounded-full bg-stone-100 py-4 text-center font-bold text-stone-600 hover:bg-stone-200 transition-colors duration-300"
            >
              ← Назад
            </button>
            <button
              onClick={handleCheckout}
              disabled={submitting || !address.street}
              className="flex-1 rounded-full bg-orange-500 py-4 text-center font-bold text-white hover:bg-orange-600 transition-colors duration-300 disabled:opacity-50 disabled:cursor-not-allowed shadow-md shadow-orange-200"
            >
              {submitting ? (
                <span className="inline-flex items-center gap-2">
                  <span className="h-4 w-4 animate-spin rounded-full border-2 border-white border-t-transparent" />
                  {payment === "card" ? "Обробка платежу..." : "Оформлення..."}
                </span>
              ) : (
                `Підтвердити · ${totalPrice.toFixed(2)} ₴`
              )}
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
