import React from 'react';

function CatalogList({ items, onEdit, onDelete, onFilter }) {
  return (
    <div>
      <h2>Catalog Items</h2>
      {items.length === 0 ? (
        <p>No items available.</p>
      ) : (
        <div className="item-grid">
          {items.map(item => (
            <div key={item.id} className="item-card">
              <h3>{item.name}</h3>
              <p>{item.description}</p>
              {item.category && (
                <p className="item-category">
                  Category:{" "}
                  <span className="clickable" onClick={() => onFilter('category', item.category.id)}>
                    {item.category.name}
                  </span>
                </p>
              )}
              {item.tags && item.tags.length > 0 && (
                <div className="item-tags">
                  Tags:{" "}
                  {item.tags.map(tag => (
                    <span key={tag.id} className="tag clickable" onClick={() => onFilter('tag', tag.id)}>
                      {tag.name}
                    </span>
                  ))}
                </div>
              )}
              <div className="item-actions">
                <button onClick={() => onEdit(item)}>Edit</button>
                <button onClick={() => onDelete(item.id)}>Delete</button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default CatalogList;
