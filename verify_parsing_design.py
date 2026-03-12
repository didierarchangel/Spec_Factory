
import logging
import sys
from pathlib import Path

# Add project root to sys.path
project_root = Path("d:/NEXT_AI/Speckit.Factory")
sys.path.append(str(project_root))

from core.graph import SpecGraphManager
from core.GraphicDesign import GraphicDesign

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_api_route_extraction():
    logger.info("🧪 Testing API Route Extraction Filtering...")
    
    checklist = """
    ## [ ] Etape 5: Routes
    - [ ] Créer `backend/src/routes/auth.routes.ts` pour définir les routes:
      - `/api/auth/register`
      - `/api/auth/login`
    - [ ] Créer `/api/users/profile`
    - [ ] Créer `backend/src/controllers/auth.controller.ts`
    """
    
    # Initialize a dummy Manager
    gm = SpecGraphManager(model=None, project_root=str(project_root))
    
    # Test the standalone pure method extraction
    extracted = gm._extract_required_files(checklist)
    
    # Assertions
    assert "backend/src/routes/auth.routes.ts" in extracted, "Should extract standard ts file"
    assert "backend/src/controllers/auth.controller.ts" in extracted, "Should extract standard ts file"
    
    # The critical test: should NOT contain API routes
    assert "/api/auth/register" not in extracted, "Should NOT extract /api/auth/register"
    assert "/api/auth/login" not in extracted, "Should NOT extract /api/auth/login"
    assert "/api/users/profile" not in extracted, "Should NOT extract /api/users/profile"
    
    logger.info("✅ API Route Extraction Filtering passed!")

def test_graphic_design_from_speclock():
    logger.info("🧪 Testing GraphicDesign Pattern Loading with fallback...")
    
    # Test project root is store-manager since that's where the user is
    user_project_root = Path("d:/NEXT_AI/store-manager")
    
    dataset_dir = project_root / "design" / "dataset"
    constitution_path = project_root / "design" / "constitution_design.yaml"
    
    # We monkeypatch the Path resolution inside GraphicDesign for the test
    import os
    original_cwd = os.getcwd()
    os.chdir(user_project_root)
    
    try:
        gd = GraphicDesign(dataset_dir=str(dataset_dir), constitution_path=str(constitution_path))
        
        # This will internally read .spec-lock.json from current dir (store-manager)
        # Store manager has "design": "premium"
        result = gd.generate("Create a dashboard")
        
        # Verify it prioritized premium
        assert result.get("design_system") == "premium", f"Should have loaded premium from spec-lock, got {result.get('design_system')}"
        
        # Also check fallback (if a premium pattern doesn't exist for the category, it should fallback to standard)
        # We know "hero" has no premium patterned defined in the json
        result2 = gd.generate("Create a hero banner")
        print(f"DEBUG: result2 = {result2}")
        assert result2.get("design_system") == "standard", f"Should fallback to standard if premium pattern missing, got {result2.get('design_system')}"
        
        logger.info("✅ GraphicDesign Loading and Fallback passed!")
    finally:
        os.chdir(original_cwd)

if __name__ == "__main__":
    try:
        test_api_route_extraction()
        test_graphic_design_from_speclock()
        print("\n🏆 ALL EXECUTION TESTS PASSED!")
    except AssertionError as e:
        logger.error(f"❌ Assertion Failed: {str(e)}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"❌ Tests failed with exception: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
