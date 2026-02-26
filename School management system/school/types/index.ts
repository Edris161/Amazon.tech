export type Role = 'admin' | 'teacher';

export interface User {
  id: string;
  name: string;
  email: string;
  role: Role;
  avatar?: string;
}

export interface ApiResponse<T> {
  data: T;
  message?: string;
}
