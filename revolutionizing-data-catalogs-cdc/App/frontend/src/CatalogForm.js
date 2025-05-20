import React, { useState, useEffect } from 'react';

function CatalogForm({ onSubmit, editingItem, onCancel, categories, tags }) {
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [categoryId, setCategoryId] = useState('');
  const [selectedTagIds, setSelectedTagIds] = useState([]);

  useEffect(() => {
    if (editingItem) {
      setName(editingItem.name);
      setDescription(editingItem.description);
      setCategoryId(editingItem.category ? editingItem.category.id : '');
      setSelectedTagIds(editingItem.tags ? editingItem.tags.map(tag => tag.id) : []);
    } else {
      setName('');
      setDescription('');
      setCategoryId('');
      setSelectedTagIds([]);
    }
  }, [editingItem]);

  const handleTagChange = (e) => {
    const options = e.target.options;
    const values = [];
    for (let i = 0; i < options.length; i++) {
      if (options[i].selected) {
        values.push(Number(options[i].value));
      }
    }
    setSelectedTagIds(values);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!name.trim()) {
      alert("Name is required");
      return;
    }
    const data = {
      name,
      description,
      category_id: categoryId ? Number(categoryId) : null,
      tag_ids: selectedTagIds,
    };
    onSubmit(data);
    if (!editingItem) {
      setName('');
      setDescription('');
      setCategoryId('');
      setSelectedTagIds([]);
    }
  };

  return (
    <div className="form-container">
      <h2>{editingItem ? "Edit Item" : "Create New Item"}</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Name:</label>
          <input 
            type="text" 
            value={name}
            onChange={e => setName(e.target.value)}
            required 
          />
        </div>
        <div className="form-group">
          <label>Description:</label>
          <textarea 
            value={description}
            onChange={e => setDescription(e.target.value)}
          ></textarea>
        </div>
        <div className="form-group">
          <label>Category:</label>
          <select value={categoryId} onChange={e => setCategoryId(e.target.value)}>
            <option value="">None</option>
            {categories.map(cat => (
              <option key={cat.id} value={cat.id}>{cat.name}</option>
            ))}
          </select>
        </div>
        <div className="form-group">
          <label>Tags:</label>
          <select multiple value={selectedTagIds.map(String)} onChange={handleTagChange}>
            {tags.map(tag => (
              <option key={tag.id} value={tag.id}>{tag.name}</option>
            ))}
          </select>
        </div>
        <div className="form-actions">
          <button type="submit">{editingItem ? "Update" : "Create"}</button>
          {editingItem && <button type="button" onClick={onCancel}>Cancel</button>}
        </div>
      </form>
    </div>
  );
}

export default CatalogForm;
