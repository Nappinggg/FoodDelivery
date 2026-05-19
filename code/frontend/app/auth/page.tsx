"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/lib/auth-context";
import { registerUser, getUserById } from "@/lib/api";

export default function AuthPage() {
  const [isLogin, setIsLogin] = useState(true);
  const [form, setForm] = useState({ full_name: "", email: "", password: "", phone: "" });
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const { login, user } = useAuth();
  const router = useRouter();

  // If already logged in, redirect (in useEffect to avoid render-time side-effect)
  useEffect(() => {
    if (user) router.push("/profile");
  }, [user, router]);

  if (user) return null;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      if (isLogin) {
        // Simple login: fetch user by ID=1 (demo — no JWT yet)
        // In a real app this would be POST /auth/login with JWT
        const u = await getUserById(1);
        login(u);
        router.push("/profile");
      } else {
        const u = await registerUser({
          full_name: form.full_name,
          email: form.email,
          password: form.password,
          phone: form.phone,
        });
        login(u);
        router.push("/profile");
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Щось пішло не так");
    } finally {
      setLoading(false);
    }
  };

  const set = (key: string, val: string) => setForm((p) => ({ ...p, [key]: val }));

  return (
    <div className="flex min-h-[calc(100vh-4rem)] items-center justify-center px-6 py-12">
      <div className="w-full max-w-md">
        {/* Toggle */}
        <div className="flex rounded-full bg-white shadow-sm p-1.5 mb-8">
          <button
            onClick={() => { setIsLogin(true); setError(null); }}
            className={`flex-1 rounded-full py-2.5 text-sm font-semibold transition-all duration-300 ${
              isLogin ? "bg-orange-500 text-white shadow-md shadow-orange-200" : "text-stone-400 hover:text-stone-600"
            }`}
          >
            Увійти
          </button>
          <button
            onClick={() => { setIsLogin(false); setError(null); }}
            className={`flex-1 rounded-full py-2.5 text-sm font-semibold transition-all duration-300 ${
              !isLogin ? "bg-orange-500 text-white shadow-md shadow-orange-200" : "text-stone-400 hover:text-stone-600"
            }`}
          >
            Реєстрація
          </button>
        </div>

        {/* Form card */}
        <div className="rounded-3xl bg-white shadow-sm p-8">
          <h1 className="text-2xl font-extrabold text-stone-800 mb-1">
            {isLogin ? "З поверненням" : "Створити акаунт"}
          </h1>
          <p className="text-stone-400 text-sm mb-8">
            {isLogin ? "Введіть свої дані для продовження" : "Заповніть свої дані, щоб почати"}
          </p>

          <form onSubmit={handleSubmit} className="space-y-4">
            {!isLogin && (
              <input
                type="text" required placeholder="Ім'я та прізвище"
                value={form.full_name} onChange={(e) => set("full_name", e.target.value)}
                className="w-full rounded-2xl bg-stone-50 px-5 py-3.5 text-sm text-stone-800 placeholder:text-stone-300 outline-none focus:ring-2 focus:ring-orange-300 transition-all"
              />
            )}
            <input
              type="email" required placeholder="Електронна пошта"
              value={form.email} onChange={(e) => set("email", e.target.value)}
              className="w-full rounded-2xl bg-stone-50 px-5 py-3.5 text-sm text-stone-800 placeholder:text-stone-300 outline-none focus:ring-2 focus:ring-orange-300 transition-all"
            />
            <input
              type="password" required placeholder="Пароль"
              value={form.password} onChange={(e) => set("password", e.target.value)}
              className="w-full rounded-2xl bg-stone-50 px-5 py-3.5 text-sm text-stone-800 placeholder:text-stone-300 outline-none focus:ring-2 focus:ring-orange-300 transition-all"
            />
            {!isLogin && (
              <input
                type="tel" required placeholder="Телефон"
                value={form.phone} onChange={(e) => set("phone", e.target.value)}
                className="w-full rounded-2xl bg-stone-50 px-5 py-3.5 text-sm text-stone-800 placeholder:text-stone-300 outline-none focus:ring-2 focus:ring-orange-300 transition-all"
              />
            )}

            {error && (
              <div className="rounded-2xl bg-red-50 px-5 py-3 text-sm text-red-500 font-medium">{error}</div>
            )}

            <button
              type="submit" disabled={loading}
              className="w-full rounded-full bg-orange-500 py-3.5 font-bold text-white hover:bg-orange-600 transition-colors duration-300 disabled:opacity-50 shadow-md shadow-orange-200"
            >
              {loading ? "Будь ласка, зачекайте..." : isLogin ? "Увійти" : "Створити акаунт"}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}
