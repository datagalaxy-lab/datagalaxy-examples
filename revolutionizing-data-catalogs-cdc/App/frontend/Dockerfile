# Use an official Node.js runtime as a parent image
FROM node:16

# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json (if available)
COPY package*.json ./

# Install dependencies defined in package.json
RUN npm install

# Install additional dependency react-force-graph-2d
RUN npm install react-force-graph-2d semantic-ui-react semantic-ui-css

# Copy the rest of the application's source code to the container
COPY . .

# Expose port 3000 (the default port for Create React App)
EXPOSE 3000

# Start the React application
CMD ["npm", "start"]
