import React, { useState, useEffect } from 'react';
import axios from 'axios';
import CatalogList from './CatalogList';
import CatalogForm from './CatalogForm';
import GraphView from './GraphView';
import './App.css';

function App() {
  const [items, setItems] = useState([]);
  const [editingItem, setEditingItem] = useState(null);
  const [categories, setCategories] = useState([]);
  const [tags, setTags] = useState([]);
  const [filter, setFilter] = useState(null); // { type: 'category'|'tag', id: number }
  const [view, setView] = useState('list'); // 'list' or 'graph'

  // Fetch catalog items from the backend API
  const fetchItems = async () => {
    try {
      const res = await axios.get('http://localhost:5000/api/items');
      setItems(res.data);
    } catch (error) {
      console.error("Error fetching items", error);
    }
  };

  // Fetch categories from API
  const fetchCategories = async () => {
    try {
      const res = await axios.get('http://localhost:5000/api/categories');
      setCategories(res.data);
    } catch (error) {
      console.error("Error fetching categories", error);
    }
  };

  // Fetch tags from API
  const fetchTags = async () => {
    try {
      const res = await axios.get('http://localhost:5000/api/tags');
      setTags(res.data);
    } catch (error) {
      console.error("Error fetching tags", error);
    }
  };

  useEffect(() => {
    fetchItems();
    fetchCategories();
    fetchTags();
  }, []);

  const handleCreate = async (itemData) => {
    try {
      const res = await axios.post('http://localhost:5000/api/items', itemData);
      setItems([...items, res.data]);
    } catch (error) {
      console.error("Error creating item", error);
    }
  };

  const handleUpdate = async (id, itemData) => {
    try {
      const res = await axios.put(`http://localhost:5000/api/items/${id}`, itemData);
      setItems(items.map(it => it.id === id ? res.data : it));
      setEditingItem(null);
    } catch (error) {
      console.error("Error updating item", error);
    }
  };

  const handleDelete = async (id) => {
    try {
      await axios.delete(`http://localhost:5000/api/items/${id}`);
      setItems(items.filter(it => it.id !== id));
    } catch (error) {
      console.error("Error deleting item", error);
    }
  };

  const startEditing = (item) => {
    setEditingItem(item);
  };

  const clearFilter = () => {
    setFilter(null);
  };

  const handleFilter = (type, id) => {
    setFilter({ type, id });
  };

  // Apply filter if set (for list view)
  const filteredItems = filter
    ? items.filter(item => {
        if (filter.type === 'category') {
          return item.category && item.category.id === filter.id;
        } else if (filter.type === 'tag') {
          return item.tags && item.tags.some(tag => tag.id === filter.id);
        }
        return true;
      })
    : items;

  return (
    <div className="container">
      <h1>Data Catalog</h1>
      <div className="view-toggle">
        <button onClick={() => setView(view === 'list' ? 'graph' : 'list')}>
          Switch to {view === 'list' ? 'Graph View' : 'List View'}
        </button>
      </div>

      {view === 'list' && (
        <>
          {filter && (
            <div className="filter-info">
              <span>
                Filtering by {filter.type}:{" "}
                {filter.type === 'category'
                  ? categories.find(cat => cat.id === filter.id)?.name
                  : tags.find(t => t.id === filter.id)?.name}
              </span>
              <button onClick={clearFilter}>Clear Filter</button>
            </div>
          )}
          <CatalogForm 
            onSubmit={editingItem ? (data) => handleUpdate(editingItem.id, data) : handleCreate}
            editingItem={editingItem}
            onCancel={() => setEditingItem(null)}
            categories={categories}
            tags={tags}
          />
          <CatalogList 
            items={filteredItems}
            onEdit={startEditing}
            onDelete={handleDelete}
            onFilter={handleFilter}
          />
        </>
      )}

      {view === 'graph' && (
        <GraphView items={items} />
      )}
    </div>
  );
}

export default App;
