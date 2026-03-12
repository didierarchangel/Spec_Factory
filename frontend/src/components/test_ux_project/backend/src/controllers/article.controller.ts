// @SPEC-KIT-TASK: 07_routes_articles_backend
import { Request, Response } from 'express';
import { ArticleService } from '../services/article.service';
import { CreateArticleDto, UpdateArticleDto } from '../dtos/article.dto';

const articleService = new ArticleService();

class ArticleController {
  public static async createArticle(req: Request<object, object, CreateArticleDto>, res: Response): Promise<void> {
    try {
      const article = await articleService.create(req.body);
      res.status(201).json(article);
    } catch (error: unknown) {
      if (error instanceof Error && error.message.includes('duplicate key error')) {
        res.status(409).json({ message: 'Article with this name already exists.' });
      } else {
        res.status(500).json({ message: 'Failed to create article', error: (error as Error).message });
      }
    }
  }

  public static async getAllArticles(req: Request, res: Response): Promise<void> {
    try {
      const articles = await articleService.findAll();
      res.status(200).json(articles);
    } catch (error: unknown) {
      res.status(500).json({ message: 'Failed to retrieve articles', error: (error as Error).message });
    }
  }

  public static async getArticleById(req: Request<{ id: string }>, res: Response): Promise<void> {
    try {
      const article = await articleService.findById(req.params.id);
      if (!article) {
        res.status(404).json({ message: 'Article not found' });
        return;
      }
      res.status(200).json(article);
    } catch (error: unknown) {
      res.status(500).json({ message: 'Failed to retrieve article', error: (error as Error).message });
    }
  }

  public static async updateArticle(req: Request<{ id: string }, object, UpdateArticleDto>, res: Response): Promise<void> {
    try {
      const article = await articleService.update(req.params.id, req.body);
      if (!article) {
        res.status(404).json({ message: 'Article not found' });
        return;
      }
      res.status(200).json(article);
    } catch (error: unknown) {
      if (error instanceof Error && error.message.includes('duplicate key error')) {
        res.status(409).json({ message: 'Article with this name already exists.' });
      } else {
        res.status(500).json({ message: 'Failed to update article', error: (error as Error).message });
      }
    }
  }

  public static async deleteArticle(req: Request<{ id: string }>, res: Response): Promise<void> {
    try {
      const article = await articleService.delete(req.params.id);
      if (!article) {
        res.status(404).json({ message: 'Article not found' });
        return;
      }
      res.status(204).send(); // No content for successful deletion
    } catch (error: unknown) {
      res.status(500).json({ message: 'Failed to delete article', error: (error as Error).message });
    }
  }
}

export { ArticleController };