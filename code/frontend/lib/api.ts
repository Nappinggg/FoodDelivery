// API client for communicating with the FastAPI backend

import type { Restaurant, Dish, Order, User } from "./types";

const API_BASE = "http://127.0.0.1:8000/api";

async function request<T>(endpoint: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${endpoint}`, {
    headers: { "Content-Type": "application/json", ...options?.headers },
    ...options,
  });
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error(body.detail || `API error: ${res.status}`);
  }
  if (res.status === 204) return {} as T;
  return res.json();
}

// ─── Auth / Users ────────────────────────────────────────────────────

export async function registerUser(data: {
  full_name: string;
  email: string;
  password: string;
  phone: string;
}): Promise<User> {
  return request<User>("/users/register", {
    method: "POST",
    body: JSON.stringify(data),
  });
}

export async function getUserById(id: number): Promise<User> {
  return request<User>(`/users/${id}`);
}

// ─── Restaurants ─────────────────────────────────────────────────────

export async function getRestaurants(): Promise<Restaurant[]> {
  return request<Restaurant[]>("/restaurants/");
}

export async function getRestaurantById(id: number): Promise<Restaurant> {
  return request<Restaurant>(`/restaurants/${id}`);
}

// ─── Dishes ──────────────────────────────────────────────────────────

export async function getDishesByRestaurant(restaurantId: number): Promise<Dish[]> {
  return request<Dish[]>(`/dishes/restaurant/${restaurantId}`);
}

// ─── Orders ──────────────────────────────────────────────────────────

export async function createOrder(
  restaurantId: number,
  items: { dish_id: number; quantity: number }[],
  userId: number = 1
): Promise<Order> {
  return request<Order>(`/orders/?user_id=${userId}`, {
    method: "POST",
    body: JSON.stringify({ restaurant_id: restaurantId, items }),
  });
}

export async function getOrdersByUser(userId: number): Promise<Order[]> {
  return request<Order[]>(`/orders/user/${userId}`);
}
