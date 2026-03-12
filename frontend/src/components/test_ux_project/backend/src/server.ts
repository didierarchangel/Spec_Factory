// @SPEC-KIT-TASK: 07_routes_articles_backend
import { app } from './app';

const PORT = process.env.PORT || 5000;

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});