// @SPEC-KIT-TASK: 07_routes_articles_backend
import { Router } from 'express';
import { ArticleController } from '../controllers/article.controller';
import { validate } from '../middlewares/validation.middleware';
import { createArticleDto, updateArticleDto } from '../dtos/article.dto';

const router = Router();

router.post('/', validate(createArticleDto), ArticleController.createArticle);
router.get('/', ArticleController.getAllArticles);
router.get('/:id', ArticleController.getArticleById);
router.put('/:id', validate(updateArticleDto), ArticleController.updateArticle);
router.delete('/:id', ArticleController.deleteArticle);

export { router as articleRoutes };