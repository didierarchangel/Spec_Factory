import { Request, Response, NextFunction } from "express";
import jwt from "jsonwebtoken";

// Extension de l'interface Request pour y ajouter les propriétés utilisateur
declare global {
  namespace Express {
    interface Request {
      user?: {
        id: string;
        email: string;
        iat: number;
        exp: number;
      };
    }
  }
}

/**
 * Middleware d'authentification JWT.
 * Valide le token Bearer dans le header Authorization.
 * Expose les données de l'utilisateur dans req.user.
 */
export const authMiddleware = (
  req: Request,
  res: Response,
  next: NextFunction
): void => {
  try {
    // Extraire le token du header Authorization (format: "Bearer <token>")
    const authHeader = req.headers.authorization;
    const token = authHeader?.split(" ")[1];

    if (!token) {
      res.status(401).json({ 
        message: "Token manquant",
        code: "TOKEN_MISSING"
      });
      return;
    }

    // Vérifier et décoder le token
    const decoded = jwt.verify(token, process.env.JWT_SECRET!);
    
    // Ajouter les données de l'utilisateur à la requête
    (req as any).user = decoded;
    
    next();
  } catch (error) {
    if (error instanceof jwt.TokenExpiredError) {
      res.status(401).json({ 
        message: "Token expiré",
        code: "TOKEN_EXPIRED"
      });
    } else if (error instanceof jwt.JsonWebTokenError) {
      res.status(401).json({ 
        message: "Token invalide",
        code: "TOKEN_INVALID"
      });
    } else {
      res.status(500).json({ 
        message: "Erreur serveur lors de la vérification du token",
        code: "SERVER_ERROR"
      });
    }
  }
};

/**
 * Middleware pour imprimer le contexte utilisateur (utile pour le debugging).
 * À utiliser après authMiddleware.
 */
export const logAuthContext = (
  req: Request,
  res: Response,
  next: NextFunction
): void => {
  if (req.user) {
    console.log(`[AUTH] Utilisateur authentifié: ${req.user.email} (ID: ${req.user.id})`);
  }
  next();
};
