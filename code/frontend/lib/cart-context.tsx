"use client";

import { createContext, useContext, useState, useCallback, type ReactNode } from "react";
import type { CartItem, CartState } from "@/lib/types";

interface CartContextType {
  cart: CartState;
  addItem: (restaurantId: number, restaurantName: string, item: CartItem) => void;
  removeItem: (dishId: number) => void;
  updateQuantity: (dishId: number, quantity: number) => void;
  clearCart: () => void;
  totalPrice: number;
  totalItems: number;
}

const EMPTY_CART: CartState = { restaurant_id: null, restaurant_name: "", items: [] };

const CartContext = createContext<CartContextType | undefined>(undefined);

export function CartProvider({ children }: { children: ReactNode }) {
  const [cart, setCart] = useState<CartState>(EMPTY_CART);

  const addItem = useCallback(
    (restaurantId: number, restaurantName: string, item: CartItem) => {
      setCart((prev) => {
        // If switching restaurant, reset cart
        if (prev.restaurant_id !== null && prev.restaurant_id !== restaurantId) {
          return {
            restaurant_id: restaurantId,
            restaurant_name: restaurantName,
            items: [item],
          };
        }
        // Check if item already exists
        const existing = prev.items.find((i) => i.dish_id === item.dish_id);
        if (existing) {
          return {
            ...prev,
            restaurant_id: restaurantId,
            restaurant_name: restaurantName,
            items: prev.items.map((i) =>
              i.dish_id === item.dish_id
                ? { ...i, quantity: i.quantity + item.quantity }
                : i
            ),
          };
        }
        return {
          ...prev,
          restaurant_id: restaurantId,
          restaurant_name: restaurantName,
          items: [...prev.items, item],
        };
      });
    },
    []
  );

  const removeItem = useCallback((dishId: number) => {
    setCart((prev) => {
      const newItems = prev.items.filter((i) => i.dish_id !== dishId);
      if (newItems.length === 0) return EMPTY_CART;
      return { ...prev, items: newItems };
    });
  }, []);

  const updateQuantity = useCallback((dishId: number, quantity: number) => {
    if (quantity <= 0) {
      return removeItem(dishId);
    }
    setCart((prev) => ({
      ...prev,
      items: prev.items.map((i) =>
        i.dish_id === dishId ? { ...i, quantity } : i
      ),
    }));
  }, [removeItem]);

  const clearCart = useCallback(() => setCart(EMPTY_CART), []);

  const totalPrice = cart.items.reduce((sum, i) => sum + i.price * i.quantity, 0);
  const totalItems = cart.items.reduce((sum, i) => sum + i.quantity, 0);

  return (
    <CartContext.Provider
      value={{ cart, addItem, removeItem, updateQuantity, clearCart, totalPrice, totalItems }}
    >
      {children}
    </CartContext.Provider>
  );
}

export function useCart() {
  const ctx = useContext(CartContext);
  if (!ctx) throw new Error("useCart must be used within CartProvider");
  return ctx;
}
