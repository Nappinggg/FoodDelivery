// Types matching the backend Pydantic schemas

export interface Restaurant {
  id: number;
  name: string;
  address: string;
  rating: number;
  is_active: boolean;
}

export interface User {
  id: number;
  full_name: string;
  email: string;
  phone: string;
  role: string;
}

export interface Dish {
  id: number;
  restaurant_id: number;
  name: string;
  description: string | null;
  price: number;
  category: string;
}

export interface OrderItem {
  id: number;
  order_id: number;
  dish_id: number;
  quantity: number;
  price_at_order: number;
  dish_name: string | null;
}

export interface Order {
  id: number;
  user_id: number;
  restaurant_id: number;
  total_price: number;
  status: string;
  created_at: string;
  items: OrderItem[];
}

// Cart types (frontend-only)
export interface CartItem {
  dish_id: number;
  name: string;
  price: number;
  quantity: number;
}

export interface CartState {
  restaurant_id: number | null;
  restaurant_name: string;
  items: CartItem[];
}
