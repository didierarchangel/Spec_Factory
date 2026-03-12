// @SPEC-KIT-TASK: 07_routes_articles_backend
import express from 'express';
import mongoose from 'mongoose';
import dotenv from 'dotenv';
import cors from 'cors';
import { articleRoutes } from './routes/article.routes';

dotenv.config();

const app = express();

// Middleware
app.use(express.json()); // To parse JSON request bodies
app.use(cors()); // Enable CORS for all routes

// Database Connection
const mongoUri = process.env.MONGO_URI || 'mongodb://localhost:27017/store_manager';

mongoose.connect(mongoUri)
  .then(() => console.log('MongoDB connected successfully'))
  .catch((err) => {
    console.error('MongoDB connection error:', err);
    process.exit(1); // Exit process with failure
  });

// Routes
app.use('/api/articles', articleRoutes);

// Basic error handling middleware (optional, but good practice)
app.use((err: Error, req: express.Request, res: express.Response, next: express.NextFunction) => {
  console.error(err.stack);
  res.status(500).send('Something broke!');
});

export { app };