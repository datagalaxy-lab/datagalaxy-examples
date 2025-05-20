import React from 'react';
import ForceGraph2D from 'react-force-graph-2d';

function buildGraphData(items) {
  // Create nodes for each item
  const nodes = items.map(item => ({
    id: item.id.toString(),
    name: item.name,
    // Optional: Use category name as group to auto-color nodes
    group: item.category ? item.category.name : 'none'
  }));

  const links = [];
  // Compare each pair of items for shared category or tags
  for (let i = 0; i < items.length; i++) {
    for (let j = i + 1; j < items.length; j++) {
      const itemA = items[i];
      const itemB = items[j];

      let sharedCategory = false;
      let sharedTag = false;

      if (itemA.category && itemB.category && itemA.category.id === itemB.category.id) {
        sharedCategory = true;
      }
      if (itemA.tags && itemB.tags) {
        const tagsA = itemA.tags.map(tag => tag.id);
        const tagsB = itemB.tags.map(tag => tag.id);
        sharedTag = tagsA.some(tagId => tagsB.includes(tagId));
      }

      if (sharedCategory || sharedTag) {
        links.push({
          source: itemA.id.toString(),
          target: itemB.id.toString(),
          // Use a thicker line if both category and tag are shared
          value: sharedCategory && sharedTag ? 2 : 1
        });
      }
    }
  }

  return { nodes, links };
}

const GraphView = ({ items }) => {
  const data = buildGraphData(items);

  return (
    <div style={{ height: '600px' }}>
      <ForceGraph2D
        graphData={data}
        nodeLabel="name"
        nodeAutoColorBy="group"
        linkWidth={link => link.value * 2}
        linkDirectionalParticles={1}
        linkDirectionalParticleSpeed={0.005}
      />
    </div>
  );
};

export default GraphView;
