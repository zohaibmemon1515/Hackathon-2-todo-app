// User type definitions for frontend

export interface User {
  id: string;
  email: string;
  first_name?: string;
  last_name?: string;
  is_active: boolean;
  created_at: string; // ISO date string
  updated_at: string; // ISO date string
}

export interface UserLogin {
  email: string;
  password: string;
}

export interface UserRegister {
  email: string;
  password: string;
  first_name?: string;
  last_name?: string;
}

export interface UserToken {
  user: User;
  access_token: string;
  token_type: string;
}