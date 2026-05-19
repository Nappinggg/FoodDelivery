"use client";

import Link from "next/link";
import Image from "next/image";
import { useCart } from "@/lib/cart-context";
import { useAuth } from "@/lib/auth-context";

export function Navbar() {
  const { totalItems } = useCart();
  const { user } = useAuth();

  return (
    <header className="sticky top-0 z-50 px-4 pt-4">
      <div className="mx-auto max-w-7xl rounded-full bg-white/80 backdrop-blur-md shadow-lg px-5 py-2">
        <div className="flex items-center justify-between">
          {/* Left: Logo + Nav links */}
          <div className="flex items-center gap-6">
            {/* Logo — graphic only, large */}
            <Link href="/" className="shrink-0 hover:scale-105 transition-transform duration-300">
              <Image
                src="/logo.jpg"
                alt="ТеплийСтіл"
                width={110}
                height={110}
                className="rounded-2xl"
              />
            </Link>

            {/* Navigation */}
            <nav className="flex items-center gap-1">
              <Link
                href="/"
                className="rounded-full px-5 py-2.5 text-base font-medium text-stone-600 hover:text-stone-900 hover:bg-stone-100 transition-all duration-300"
              >
                Ресторани
              </Link>
              {user && (
                <Link
                  href="/orders"
                  className="rounded-full px-5 py-2.5 text-base font-medium text-stone-600 hover:text-stone-900 hover:bg-stone-100 transition-all duration-300"
                >
                  Замовлення
                </Link>
              )}
            </nav>
          </div>

          {/* Right: Cart + Auth */}
          <div className="flex items-center gap-3">
            {/* Cart pill button */}
            <Link
              href="/cart"
              className="relative flex items-center gap-2.5 rounded-full bg-orange-500 px-6 py-3 font-bold text-white hover:bg-orange-600 transition-colors duration-300 shadow-md shadow-orange-200"
            >
              <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 100 4 2 2 0 000-4z" />
              </svg>
              Кошик
              {totalItems > 0 && (
                <span className="absolute -right-1 -top-1 flex h-6 w-6 items-center justify-center rounded-full bg-white text-xs font-extrabold text-orange-600 shadow-md ring-2 ring-orange-500">
                  {totalItems}
                </span>
              )}
            </Link>

            {/* Auth avatar / Sign In */}
            {user ? (
              <Link
                href="/profile"
                className="flex h-11 w-11 items-center justify-center rounded-full bg-stone-800 text-sm font-bold text-white hover:bg-stone-700 transition-colors duration-300 shadow-md"
              >
                {user.full_name.charAt(0).toUpperCase()}
              </Link>
            ) : (
              <Link
                href="/auth"
                className="rounded-full bg-stone-800 px-6 py-3 font-semibold text-white hover:bg-stone-700 transition-colors duration-300"
              >
                Увійти
              </Link>
            )}
          </div>
        </div>
      </div>
    </header>
  );
}
