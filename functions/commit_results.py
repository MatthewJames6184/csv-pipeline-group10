import subprocess
import os
from functions.logger import get_logger


logger = get_logger(__name__)

def commit_results_to_repository():
    try:
        # Check if we're in a git repository
        result = subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            capture_output=True, text=True
        )
        
        if result.returncode != 0:
            logger.warning("Not in a git repository. Skipping commit")
            return
        
        # Add output and versions folders
        subprocess.run(["git", "add", "output/"], check=True)
        subprocess.run(["git", "add", "versions/"], check=True)
        
        # Commit changes
        result = subprocess.run(
            ["git", "commit", "-m", "Auto: commit processed output files [skip ci]"],
            capture_output=True, text=True
        )
        
        # Check commit result
        if "nothing to commit" in result.stdout or "nothing to commit" in result.stderr:
            logger.info("Nothing new to commit")
        else:
            # Push changes
            push_result = subprocess.run(
                ["git", "push"],
                capture_output=True, text=True
            )
            
            if push_result.returncode == 0:
                logger.info("Results committed and pushed")
            else:
                logger.error("Push failed: %s", push_result.stderr)
                
    except subprocess.CalledProcessError as e:
        logger.error("Git error (expected in CI, safe to ignore): %s", e)
    except FileNotFoundError:
        logger.warning("Git command not found. Skipping commit")