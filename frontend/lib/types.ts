/**
 * TypeScript interfaces for myKB application.
 * Matches the backend Pydantic schemas.
 */

export interface Board {
  id: number;
  name: string;
  createdAt: string;
  updatedAt: string;
}

export interface BoardWithColumns extends Board {
  columns: ColumnWithCards[];
}

export interface Column {
  id: number;
  boardId: number;
  name: string;
  position: number;
  createdAt: string;
  updatedAt: string;
}

export interface ColumnWithCards extends Column {
  cards: Card[];
}

export interface Card {
  id: number;
  columnId: number;
  title: string;
  description: string;
  position: number;
  createdAt: string;
  updatedAt: string;
}

export interface BoardCreate {
  name: string;
}

export interface BoardUpdate {
  name?: string;
}

export interface ColumnCreate {
  name: string;
}

export interface ColumnUpdate {
  name?: string;
}

export interface ColumnPositionUpdate {
  position: number;
}

export interface CardCreate {
  title: string;
  description?: string;
}

export interface CardUpdate {
  title?: string;
  description?: string;
}

export interface CardMove {
  columnId: number;
  position: number;
}

export interface ApiError {
  detail: string;
}
