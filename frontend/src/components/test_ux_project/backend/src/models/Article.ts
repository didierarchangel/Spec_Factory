// @SPEC-KIT-TASK: 07_routes_articles_backend
import { Schema, model, Document } from 'mongoose';

export interface IArticle extends Document {
  name: string;
  description: string;
  price: number;
  stock: number;
}

const articleSchema = new Schema<IArticle>({
  name: { type: String, required: true, unique: true },
  description: { type: String, required: true },
  price: { type: Number, required: true, min: 0 },
  stock: { type: Number, required: true, min: 0 },
}, { timestamps: true });

const Article = model<IArticle>('Article', articleSchema);

export { Article };