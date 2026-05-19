"use client";

import { useAuth } from "@/lib/auth-context";
import Link from "next/link";

export default function ProfilePage() {
  const { user, loading, logout } = useAuth();

  if (loading) {
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
        <p className="text-stone-500 mb-8">Будь ласка, увійдіть, щоб переглянути свій профіль</p>
        <Link href="/auth" className="inline-flex rounded-full bg-orange-500 px-7 py-3 font-bold text-white hover:bg-orange-600 transition-colors duration-300 shadow-md shadow-orange-200">
          Увійти
        </Link>
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-lg px-6 py-12">
      <h1 className="text-3xl font-extrabold tracking-tight text-stone-800 mb-8">Мій профіль</h1>

      <div className="rounded-3xl bg-white shadow-sm p-8">
        {/* Avatar */}
        <div className="flex items-center gap-5 mb-8">
          <div className="flex h-16 w-16 items-center justify-center rounded-full bg-orange-100 text-2xl font-bold text-orange-500">
            {user.full_name.charAt(0).toUpperCase()}
          </div>
          <div>
            <p className="text-xl font-bold text-stone-800">{user.full_name}</p>
            <p className="text-sm text-stone-400 capitalize">{user.role}</p>
          </div>
        </div>

        {/* Info rows */}
        <div className="space-y-4">
          <div className="rounded-2xl bg-stone-50 px-5 py-4">
            <p className="text-xs font-medium text-stone-400 mb-1">Електронна пошта</p>
            <p className="text-sm font-semibold text-stone-700">{user.email}</p>
          </div>
          <div className="rounded-2xl bg-stone-50 px-5 py-4">
            <p className="text-xs font-medium text-stone-400 mb-1">Телефон</p>
            <p className="text-sm font-semibold text-stone-700">{user.phone}</p>
          </div>
          <div className="rounded-2xl bg-stone-50 px-5 py-4">
            <p className="text-xs font-medium text-stone-400 mb-1">ID користувача</p>
            <p className="text-sm font-semibold text-stone-700">#{user.id}</p>
          </div>
        </div>

        {/* Actions */}
        <div className="mt-8 flex gap-3">
          <Link href="/orders" className="flex-1 rounded-full bg-orange-100 py-3 text-center text-sm font-bold text-orange-600 hover:bg-orange-200 transition-colors duration-300">
            Мої замовлення
          </Link>
          <button
            onClick={logout}
            className="flex-1 rounded-full bg-stone-100 py-3 text-sm font-bold text-stone-500 hover:bg-red-50 hover:text-red-500 transition-all duration-300"
          >
            Вийти
          </button>
        </div>
      </div>
    </div>
  );
}
