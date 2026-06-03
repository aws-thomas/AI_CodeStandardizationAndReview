/**
 * API client for myKB backend.
 * Handles all HTTP requests with proper error handling.
 */

import {
  Board,
  BoardWithColumns,
  BoardCreate,
  BoardUpdate,
  Column,
  ColumnWithCards,
  ColumnCreate,
  ColumnUpdate,
  ColumnPositionUpdate,
  Card,
  CardCreate,
  CardUpdate,
  CardMove,
  ApiError,
} from './types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

/**
 * Custom error class for API errors.
 */
export class ApiClientError extends Error {
  constructor(
    message: string,
    public statusCode?: number,
    public details?: string
  ) {
    super(message);
    this.name = 'ApiClientError';
  }
}

/**
 * Generic fetch wrapper with error handling.
 */
async function fetchApi<T>(
  endpoint: string,
  options?: RequestInit
): Promise<T> {
  try {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options?.headers,
      },
    });

    if (!response.ok) {
      let errorMessage = `HTTP ${response.status}: ${response.statusText}`;
      let errorDetails: string | undefined;

      try {
        const errorData: ApiError = await response.json();
        errorDetails = errorData.detail;
        errorMessage = errorDetails || errorMessage;
      } catch {
        // If parsing error response fails, use default message
      }

      throw new ApiClientError(errorMessage, response.status, errorDetails);
    }

    if (response.status === 204) {
      return undefined as T;
    }

    return await response.json();
  } catch (error) {
    if (error instanceof ApiClientError) {
      throw error;
    }
    throw new ApiClientError(
      error instanceof Error ? error.message : 'Network error occurred'
    );
  }
}

/**
 * Board API methods.
 */
export const boardsApi = {
  /**
   * Get all boards.
   */
  getAll: (): Promise<Board[]> => {
    return fetchApi<Board[]>('/api/boards');
  },

  /**
   * Get a single board with all columns and cards.
   */
  getById: (boardId: number): Promise<BoardWithColumns> => {
    return fetchApi<BoardWithColumns>(`/api/boards/${boardId}`);
  },

  /**
   * Create a new board.
   */
  create: (data: BoardCreate): Promise<Board> => {
    return fetchApi<Board>('/api/boards', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  },

  /**
   * Update a board's name.
   */
  update: (boardId: number, data: BoardUpdate): Promise<Board> => {
    return fetchApi<Board>(`/api/boards/${boardId}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  },

  /**
   * Delete a board.
   */
  delete: (boardId: number): Promise<void> => {
    return fetchApi<void>(`/api/boards/${boardId}`, {
      method: 'DELETE',
    });
  },
};

/**
 * Column API methods.
 */
export const columnsApi = {
  /**
   * Create a new column in a board.
   */
  create: (boardId: number, data: ColumnCreate): Promise<Column> => {
    return fetchApi<Column>(`/api/boards/${boardId}/columns`, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  },

  /**
   * Get a single column with all cards.
   */
  getById: (columnId: number): Promise<ColumnWithCards> => {
    return fetchApi<ColumnWithCards>(`/api/columns/${columnId}`);
  },

  /**
   * Update a column's name.
   */
  update: (columnId: number, data: ColumnUpdate): Promise<Column> => {
    return fetchApi<Column>(`/api/columns/${columnId}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  },

  /**
   * Update a column's position.
   */
  updatePosition: (
    columnId: number,
    data: ColumnPositionUpdate
  ): Promise<Column> => {
    return fetchApi<Column>(`/api/columns/${columnId}/position`, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  },

  /**
   * Delete a column.
   */
  delete: (columnId: number): Promise<void> => {
    return fetchApi<void>(`/api/columns/${columnId}`, {
      method: 'DELETE',
    });
  },
};

/**
 * Card API methods.
 */
export const cardsApi = {
  /**
   * Create a new card in a column.
   */
  create: (columnId: number, data: CardCreate): Promise<Card> => {
    return fetchApi<Card>(`/api/columns/${columnId}/cards`, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  },

  /**
   * Get a single card.
   */
  getById: (cardId: number): Promise<Card> => {
    return fetchApi<Card>(`/api/cards/${cardId}`);
  },

  /**
   * Update a card's title and/or description.
   */
  update: (cardId: number, data: CardUpdate): Promise<Card> => {
    return fetchApi<Card>(`/api/cards/${cardId}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  },

  /**
   * Move a card to a different column or position.
   */
  move: (cardId: number, data: CardMove): Promise<Card> => {
    return fetchApi<Card>(`/api/cards/${cardId}/move`, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  },

  /**
   * Delete a card.
   */
  delete: (cardId: number): Promise<void> => {
    return fetchApi<void>(`/api/cards/${cardId}`, {
      method: 'DELETE',
    });
  },
};
