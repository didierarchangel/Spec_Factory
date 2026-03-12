// @SPEC-KIT-TASK: 07_routes_articles_backend
import { z } from 'zod';

// Schema for creating an article
const createArticleDto = z.object({
  name: z.string().min(1, "Name is required"),
  description: z.string().min(1, "Description is required"),
  price: z.number().min(0, "Price must be a non-negative number"),
  stock: z.number().int().min(0, "Stock must be a non-negative integer"),
});

export type CreateArticleDto = z.infer<typeof createArticleDto>;

// Schema for updating an article
const updateArticleDto = z.object({
  name: z.string().min(1, "Name is required").optional(),
  description: z.string().min(1, "Description is required").optional(),
  price: z.number().min(0, "Price must be a non-negative number").optional(),
  stock: z.number().int().min(0, "Stock must be a non-negative integer").optional(),
});

export type UpdateArticleDto = z.infer<typeof updateArticleDto>;

export { createArticleDto, updateArticleDto };