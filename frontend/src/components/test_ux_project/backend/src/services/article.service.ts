// @SPEC-KIT-TASK: 07_routes_articles_backend
import { Article, IArticle } from '../models/Article';
import { CreateArticleDto, UpdateArticleDto } from '../dtos/article.dto';

class ArticleService {
  public async create(articleData: CreateArticleDto): Promise<IArticle> {
    const newArticle = new Article(articleData);
    await newArticle.save();
    return newArticle;
  }

  public async findAll(): Promise<IArticle[]> {
    return Article.find();
  }

  public async findById(id: string): Promise<IArticle | null> {
    return Article.findById(id);
  }

  public async update(id: string, articleData: UpdateArticleDto): Promise<IArticle | null> {
    return Article.findByIdAndUpdate(id, articleData, { new: true, runValidators: true });
  }

  public async delete(id: string): Promise<IArticle | null> {
    return Article.findByIdAndDelete(id);
  }
}

export { ArticleService };