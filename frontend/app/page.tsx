'use client';

import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import { boardsApi, ApiClientError } from '@/lib/api';
import { Board } from '@/lib/types';

export default function Home() {
  const [boards, setBoards] = useState<Board[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isCreating, setIsCreating] = useState(false);
  const [newBoardName, setNewBoardName] = useState('');

  useEffect(() => {
    loadBoards();
  }, []);

  const loadBoards = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await boardsApi.getAll();
      setBoards(data);
    } catch (err) {
      setError(err instanceof ApiClientError ? err.message : 'Failed to load boards');
    } finally {
      setLoading(false);
    }
  };

  const handleCreateBoard = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newBoardName.trim()) return;

    try {
      setError(null);
      await boardsApi.create({ name: newBoardName });
      setNewBoardName('');
      setIsCreating(false);
      await loadBoards();
    } catch (err) {
      setError(err instanceof ApiClientError ? err.message : 'Failed to create board');
    }
  };

  const handleDeleteBoard = async (boardId: number, boardName: string) => {
    if (!confirm(`Are you sure you want to delete "${boardName}"? This will delete all columns and cards.`)) {
      return;
    }

    try {
      setError(null);
      await boardsApi.delete(boardId);
      await loadBoards();
    } catch (err) {
      setError(err instanceof ApiClientError ? err.message : 'Failed to delete board');
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading boards...</p>
        </div>
      </div>
    );
  }

  return (
    <main className="min-h-screen bg-gray-50 py-8 px-4">
      <div className="max-w-6xl mx-auto">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900">myKB Boards</h1>
          <button
            onClick={() => setIsCreating(true)}
            className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg font-medium transition-colors"
          >
            Create Board
          </button>
        </div>

        {error && (
          <div className="mb-6 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
            {error}
          </div>
        )}

        {isCreating && (
          <div className="mb-6 bg-white p-6 rounded-lg shadow-md">
            <form onSubmit={handleCreateBoard}>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Board Name
              </label>
              <div className="flex gap-3">
                <input
                  type="text"
                  value={newBoardName}
                  onChange={(e) => setNewBoardName(e.target.value)}
                  placeholder="Enter board name..."
                  className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  autoFocus
                />
                <button
                  type="submit"
                  className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg font-medium transition-colors"
                >
                  Create
                </button>
                <button
                  type="button"
                  onClick={() => {
                    setIsCreating(false);
                    setNewBoardName('');
                  }}
                  className="bg-gray-200 hover:bg-gray-300 text-gray-700 px-6 py-2 rounded-lg font-medium transition-colors"
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>
        )}

        {boards.length === 0 ? (
          <div className="text-center py-12">
            <p className="text-gray-500 text-lg mb-4">No boards yet</p>
            <p className="text-gray-400">Create your first board to get started</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {boards.map((board) => (
              <div
                key={board.id}
                className="bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow overflow-hidden"
              >
                <Link href={`/boards/${board.id}`}>
                  <div className="p-6 cursor-pointer hover:bg-gray-50 transition-colors">
                    <h2 className="text-xl font-semibold text-gray-900 mb-2">
                      {board.name}
                    </h2>
                    <p className="text-sm text-gray-500">
                      Created {new Date(board.createdAt).toLocaleDateString()}
                    </p>
                  </div>
                </Link>
                <div className="px-6 py-3 bg-gray-50 border-t border-gray-200 flex justify-end">
                  <button
                    onClick={() => handleDeleteBoard(board.id, board.name)}
                    className="text-red-600 hover:text-red-700 text-sm font-medium transition-colors"
                  >
                    Delete
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </main>
  );
}
