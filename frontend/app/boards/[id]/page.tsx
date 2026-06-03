'use client';

import React, { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import Link from 'next/link';
import { boardsApi, columnsApi, cardsApi, ApiClientError } from '@/lib/api';
import { BoardWithColumns, ColumnWithCards, Card } from '@/lib/types';

export default function BoardPage() {
  const params = useParams();
  const router = useRouter();
  const boardId = parseInt(params.id as string);

  const [board, setBoard] = useState<BoardWithColumns | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isAddingColumn, setIsAddingColumn] = useState(false);
  const [newColumnName, setNewColumnName] = useState('');

  useEffect(() => {
    loadBoard();
  }, [boardId]);

  const loadBoard = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await boardsApi.getById(boardId);
      setBoard(data);
    } catch (err) {
      setError(err instanceof ApiClientError ? err.message : 'Failed to load board');
    } finally {
      setLoading(false);
    }
  };

  const handleAddColumn = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newColumnName.trim()) return;

    try {
      setError(null);
      await columnsApi.create(boardId, { name: newColumnName });
      setNewColumnName('');
      setIsAddingColumn(false);
      await loadBoard();
    } catch (err) {
      setError(err instanceof ApiClientError ? err.message : 'Failed to create column');
    }
  };

  const handleDeleteColumn = async (columnId: number, columnName: string) => {
    if (!confirm(`Delete column "${columnName}" and all its cards?`)) {
      return;
    }

    try {
      setError(null);
      await columnsApi.delete(columnId);
      await loadBoard();
    } catch (err) {
      setError(err instanceof ApiClientError ? err.message : 'Failed to delete column');
    }
  };

  const handleRenameColumn = async (columnId: number, currentName: string) => {
    const newName = prompt('Enter new column name:', currentName);
    if (!newName || newName === currentName) return;

    try {
      setError(null);
      await columnsApi.update(columnId, { name: newName });
      await loadBoard();
    } catch (err) {
      setError(err instanceof ApiClientError ? err.message : 'Failed to rename column');
    }
  };

  const handleAddCard = async (columnId: number) => {
    const title = prompt('Enter card title:');
    if (!title) return;

    const description = prompt('Enter card description (optional):') || '';

    try {
      setError(null);
      await cardsApi.create(columnId, { title, description });
      await loadBoard();
    } catch (err) {
      setError(err instanceof ApiClientError ? err.message : 'Failed to create card');
    }
  };

  const handleEditCard = async (card: Card) => {
    const title = prompt('Enter card title:', card.title);
    if (!title || title === card.title) {
      const description = prompt('Enter card description:', card.description);
      if (description === null || description === card.description) return;
      
      try {
        setError(null);
        await cardsApi.update(card.id, { description });
        await loadBoard();
      } catch (err) {
        setError(err instanceof ApiClientError ? err.message : 'Failed to update card');
      }
      return;
    }

    const description = prompt('Enter card description:', card.description);

    try {
      setError(null);
      await cardsApi.update(card.id, {
        title: title !== card.title ? title : undefined,
        description: description !== null && description !== card.description ? description : undefined,
      });
      await loadBoard();
    } catch (err) {
      setError(err instanceof ApiClientError ? err.message : 'Failed to update card');
    }
  };

  const handleDeleteCard = async (cardId: number, cardTitle: string) => {
    if (!confirm(`Delete card "${cardTitle}"?`)) {
      return;
    }

    try {
      setError(null);
      await cardsApi.delete(cardId);
      await loadBoard();
    } catch (err) {
      setError(err instanceof ApiClientError ? err.message : 'Failed to delete card');
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading board...</p>
        </div>
      </div>
    );
  }

  if (!board) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <p className="text-red-600 text-lg mb-4">Board not found</p>
          <Link href="/" className="text-blue-600 hover:text-blue-700">
            Back to boards
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-full mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <Link
                href="/"
                className="text-gray-600 hover:text-gray-900 transition-colors"
              >
                ← Back
              </Link>
              <h1 className="text-2xl font-bold text-gray-900">{board.name}</h1>
            </div>
            <button
              onClick={() => setIsAddingColumn(true)}
              className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg font-medium transition-colors"
            >
              Add Column
            </button>
          </div>
        </div>
      </div>

      {error && (
        <div className="max-w-full mx-auto px-4 py-4">
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
            {error}
          </div>
        </div>
      )}

      <div className="p-4">
        <div className="flex gap-4 overflow-x-auto pb-4">
          {board.columns.map((column) => (
            <div
              key={column.id}
              className="flex-shrink-0 w-80 bg-gray-100 rounded-lg p-4"
            >
              <div className="flex items-center justify-between mb-4">
                <h2 className="font-semibold text-gray-900">{column.name}</h2>
                <div className="flex gap-2">
                  <button
                    onClick={() => handleRenameColumn(column.id, column.name)}
                    className="text-gray-600 hover:text-gray-900 text-sm"
                  >
                    Rename
                  </button>
                  <button
                    onClick={() => handleDeleteColumn(column.id, column.name)}
                    className="text-red-600 hover:text-red-700 text-sm"
                  >
                    Delete
                  </button>
                </div>
              </div>

              <div className="space-y-3 mb-3">
                {column.cards.map((card) => (
                  <div
                    key={card.id}
                    className="bg-white rounded-lg p-3 shadow-sm hover:shadow-md transition-shadow cursor-pointer"
                    onClick={() => handleEditCard(card)}
                  >
                    <h3 className="font-medium text-gray-900 mb-1">{card.title}</h3>
                    {card.description && (
                      <p className="text-sm text-gray-600">{card.description}</p>
                    )}
                    <div className="mt-2 flex justify-end">
                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          handleDeleteCard(card.id, card.title);
                        }}
                        className="text-red-600 hover:text-red-700 text-xs"
                      >
                        Delete
                      </button>
                    </div>
                  </div>
                ))}
              </div>

              <button
                onClick={() => handleAddCard(column.id)}
                className="w-full bg-white hover:bg-gray-50 text-gray-700 px-4 py-2 rounded-lg border border-gray-300 transition-colors"
              >
                + Add Card
              </button>
            </div>
          ))}

          {isAddingColumn && (
            <div className="flex-shrink-0 w-80 bg-white rounded-lg p-4 shadow-md">
              <form onSubmit={handleAddColumn}>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Column Name
                </label>
                <input
                  type="text"
                  value={newColumnName}
                  onChange={(e) => setNewColumnName(e.target.value)}
                  placeholder="Enter column name..."
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg mb-3 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  autoFocus
                />
                <div className="flex gap-2">
                  <button
                    type="submit"
                    className="flex-1 bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg font-medium transition-colors"
                  >
                    Add
                  </button>
                  <button
                    type="button"
                    onClick={() => {
                      setIsAddingColumn(false);
                      setNewColumnName('');
                    }}
                    className="flex-1 bg-gray-200 hover:bg-gray-300 text-gray-700 px-4 py-2 rounded-lg font-medium transition-colors"
                  >
                    Cancel
                  </button>
                </div>
              </form>
            </div>
          )}

          {board.columns.length === 0 && !isAddingColumn && (
            <div className="flex-shrink-0 w-80 bg-gray-100 rounded-lg p-8 text-center">
              <p className="text-gray-500 mb-4">No columns yet</p>
              <button
                onClick={() => setIsAddingColumn(true)}
                className="text-blue-600 hover:text-blue-700 font-medium"
              >
                Add your first column
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
